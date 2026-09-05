"""Checkout Pro do Mercado Pago - "outras formas de pagamento" (cartão, boleto,
saldo Mercado Pago e o que mais a conta tiver habilitado).

Complementa o Pix direto de `pix_bp` sem substituí-lo: o aluno continua podendo pagar
por Pix na própria tela. Aqui ele é levado ao checkout hospedado pelo Mercado Pago e
volta para `/perfil/mensalidade/<id>/retorno-checkout`, que só mostra o estado que a
API do Mercado Pago confirmou - nada vindo da URL de retorno é levado em conta.
"""

import logging
import secrets

from flask import Blueprint, abort, flash, redirect, render_template, session, url_for

from dao.financeiroDAO import PagamentoDAO, rotulo_status
from servicos.formatacao import formatar_competencia
from servicos.mercado_pago import (
    ConfiguracaoInvalida,
    MercadoPagoIndisponivel,
    ambiente_mercado_pago,
    criar_preferencia_checkout,
)

from blueprints.pix_bp import STATUS_PAGAVEIS, sincronizar_por_referencia_checkout

checkout_bp = Blueprint('checkout', __name__)
logger = logging.getLogger(__name__)

MSG_ERRO_GENERICO = 'Não foi possível abrir as outras formas de pagamento agora. Tente novamente em instantes.'
MSG_ERRO_CONFIG = 'Pagamento online indisponível no momento. Avise a administração.'
MSG_ERRO_INDISPONIVEL = 'O Mercado Pago está indisponível no momento. Tente novamente em instantes.'
MSG_ERRO_SEM_EMAIL = 'Cadastre um e-mail válido no seu perfil para usar as outras formas de pagamento.'


def _acesso_permitido(pagamento):
    """Mesma regra já usada no Pix e na página de pagamento: o próprio aluno ou o admin."""
    if session.get('tipo_usuario') == 'admin':
        return True
    return session.get('tipo_usuario') == 'aluno' and session.get('aluno_id') == pagamento.aluno_id


def _urls_retorno(pagamento):
    """back_urls absolutas para onde o Mercado Pago devolve o aluno.

    Os três destinos são a mesma rota: o resultado real é reconsultado na API, então
    não há como um deles "declarar" aprovação por conta própria.
    """
    retorno = url_for('checkout.retorno_checkout', pagamento_id=pagamento.id, _external=True)
    return {'url_sucesso': retorno, 'url_pendente': retorno, 'url_falha': retorno}


@checkout_bp.route('/perfil/mensalidade/<int:pagamento_id>/checkout', methods=['POST'])
def abrir_checkout(pagamento_id):
    """Cria (ou reaproveita) a preferência do Checkout Pro e redireciona para o Mercado Pago."""
    if session.get('tipo_usuario') not in ('admin', 'aluno'):
        flash('Sua sessão expirou. Entre novamente para continuar o pagamento.', 'erro')
        return redirect(url_for('auth.pagina_login'))

    pagamento = PagamentoDAO.bloquear_para_atualizacao(pagamento_id)
    if not pagamento:
        abort(404)

    if not _acesso_permitido(pagamento):
        abort(403)

    destino_erro = url_for('auth.pagina_pagamento', pagamento_id=pagamento.id)

    if pagamento.status not in STATUS_PAGAVEIS:
        # Mensalidade paga/cancelada/em análise não gera preferência nova.
        flash('Esta mensalidade não está disponível para pagamento online.', 'erro')
        return redirect(destino_erro)

    try:
        ambiente = ambiente_mercado_pago()
    except ConfiguracaoInvalida:
        logger.error('Ambiente do Mercado Pago mal configurado ao abrir checkout do pagamento %s.',
                     pagamento.id, exc_info=True)
        flash(MSG_ERRO_CONFIG, 'erro')
        return redirect(destino_erro)

    # Clique repetido / duas abas: se já existe uma preferência válida para ESTA
    # mensalidade, com o mesmo valor e no mesmo ambiente, reusa a mesma URL em vez de
    # criar outra cobrança no Mercado Pago.
    if PagamentoDAO.checkout_ainda_valido(pagamento, ambiente_atual=ambiente):
        return redirect(pagamento.checkout_url, code=303)

    aluno = pagamento.aluno
    email_pagador = aluno.email if aluno and aluno.email and '@' in aluno.email else None
    if session.get('tipo_usuario') == 'aluno' and not email_pagador:
        flash(MSG_ERRO_SEM_EMAIL, 'erro')
        return redirect(destino_erro)

    # Referência aleatória, própria do Checkout Pro e persistida antes de qualquer
    # confirmação. Não é o id da mensalidade justamente para não ser adivinhável.
    external_reference = f'checkout-{pagamento.id}-{secrets.token_urlsafe(16)}'
    nome_plano = pagamento.plano.nome_plano if pagamento.plano else 'Mensalidade'
    competencia = formatar_competencia(pagamento.competencia) or ''

    try:
        # O valor cobrado vem sempre do banco - o navegador não envia valor nenhum.
        resultado = criar_preferencia_checkout(
            valor=pagamento.valor,
            titulo=f'Mensalidade {nome_plano}'.strip(),
            descricao=f'Mensalidade {nome_plano} {competencia}'.strip(),
            email_pagador=email_pagador,
            external_reference=external_reference,
            idempotency_key=secrets.token_urlsafe(24),
            **_urls_retorno(pagamento),
        )
    except ConfiguracaoInvalida:
        logger.error('Configuracao ausente/invalida ao criar preferencia do pagamento %s.',
                     pagamento.id, exc_info=True)
        flash(MSG_ERRO_CONFIG, 'erro')
        return redirect(destino_erro)
    except MercadoPagoIndisponivel:
        logger.error('Mercado Pago indisponivel ao criar preferencia do pagamento %s.',
                     pagamento.id, exc_info=True)
        flash(MSG_ERRO_INDISPONIVEL, 'erro')
        return redirect(destino_erro)

    if not resultado['sucesso']:
        # A mensagem crua do Mercado Pago fica só no log do servidor.
        logger.error('Mercado Pago recusou a preferencia do pagamento %s: %s', pagamento.id, resultado['erro'])
        flash(MSG_ERRO_GENERICO, 'erro')
        return redirect(destino_erro)

    PagamentoDAO.salvar_dados_checkout(
        pagamento,
        preference_id=resultado['preference_id'],
        external_reference=external_reference,
        url_checkout=resultado['url_checkout'],
        ambiente=resultado['ambiente'],
        expira_em=resultado['expira_em'],
        ator=session.get('usuario') or 'sistema',
    )

    # 303 força GET no destino, que é o correto depois de um POST.
    return redirect(resultado['url_checkout'], code=303)


@checkout_bp.route('/perfil/mensalidade/<int:pagamento_id>/retorno-checkout')
def retorno_checkout(pagamento_id):
    """Volta do Mercado Pago.

    Ignora por completo `status`, `payment_id`, `external_reference` e afins da query
    string: o estado exibido vem de uma consulta autenticada à API pela referência que
    este servidor gravou. Sem confirmação, a tela diz que está aguardando - nunca
    "aprovado".
    """
    if session.get('tipo_usuario') not in ('admin', 'aluno'):
        flash('Sua sessão expirou. Entre novamente para ver a situação da mensalidade.', 'erro')
        return redirect(url_for('auth.pagina_login'))

    pagamento = PagamentoDAO.buscar_por_id(pagamento_id)
    if not pagamento:
        abort(404)

    if not _acesso_permitido(pagamento):
        abort(403)

    consulta_falhou = False
    try:
        sincronizar_por_referencia_checkout(pagamento)
    except MercadoPagoIndisponivel:
        consulta_falhou = True
        logger.warning('Mercado Pago indisponivel ao confirmar o retorno do pagamento %s.',
                       pagamento.id, exc_info=True)

    return render_template(
        'checkout_retorno.html',
        pagamento=pagamento,
        consulta_falhou=consulta_falhou,
        pode_tentar_de_novo=pagamento.status in STATUS_PAGAVEIS,
        rotulo_status=rotulo_status,
        formatar_competencia=formatar_competencia,
    )
