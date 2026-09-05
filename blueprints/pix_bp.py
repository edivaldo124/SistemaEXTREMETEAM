import logging
import os
import secrets
from datetime import date, datetime
from decimal import Decimal

from flask import Blueprint, flash, jsonify, redirect, request, session

from dao.financeiroDAO import STATUS_FECHADOS, PagamentoDAO, rotulo_acao, rotulo_status
from servicos.formatacao import formatar_competencia
from servicos.mercado_pago import (
    MAX_RETRIES_WEBHOOK,
    MOEDA,
    TIMEOUT_WEBHOOK_SEGUNDOS,
    MercadoPagoIndisponivel,
    buscar_pagamento,
    buscar_pagamentos_por_referencia,
    cancelar_pagamento,
    criar_pagamento_pix,
    validar_assinatura_webhook,
)

pix_bp = Blueprint('pix', __name__)
logger = logging.getLogger(__name__)

# 'recusado' entra aqui para permitir "Tentar novamente" - uma nova cobrança Pix
# substitui a recusada. 'em_processamento' e 'em_analise' ficam de fora de propósito:
# já existe uma decisão em andamento, não deixamos gerar uma segunda cobrança em cima.
STATUS_PAGAVEIS = ('pendente', 'atrasado', 'recusado')
TOLERANCIA_VALOR = Decimal('0.01')

# Tradução do meio de pagamento devolvido pela API do Mercado Pago (payment_type_id)
# para o rótulo curto gravado em Pagamento.forma_pagamento.
FORMAS_PAGAMENTO_MP = {
    'credit_card': 'cartao_credito',
    'debit_card': 'cartao_debito',
    'prepaid_card': 'cartao_pre_pago',
    'ticket': 'boleto',
    'bank_transfer': 'pix',
    'account_money': 'saldo_mercado_pago',
    'atm': 'deposito',
    'digital_wallet': 'carteira_digital',
    'digital_currency': 'carteira_digital',
    'voucher_card': 'voucher',
    'crypto_transfer': 'cripto',
}

# Ordem de preferência ao escolher, entre vários pagamentos da mesma referência, qual
# representa o estado real: um aprovado sempre vale mais que uma tentativa recusada.
PRIORIDADE_STATUS_MP = ('approved', 'in_process', 'pending', 'authorized', 'rejected', 'cancelled', 'refunded', 'charged_back')


def _pagamento_ou_none(pagamento_id):
    return PagamentoDAO.buscar_por_id(pagamento_id)


def _acesso_permitido(pagamento):
    if session.get('tipo_usuario') == 'admin':
        return True
    return session.get('tipo_usuario') == 'aluno' and session.get('aluno_id') == pagamento.aluno_id


def _pix_expirado(pagamento):
    if pagamento.status in STATUS_FECHADOS:
        return False
    if not pagamento.data_expiracao:
        return False
    return pagamento.data_expiracao <= datetime.utcnow()


def _serializar_pagamento(pagamento, *, qr_code_base64=None):
    return {
        'pagamento_id': pagamento.id,
        'status': pagamento.status,
        'status_rotulo': rotulo_status(pagamento.status),
        'acao_rotulo': rotulo_acao(pagamento.status),
        'valor': float(pagamento.valor),
        'vencimento': pagamento.vencimento.isoformat() if pagamento.vencimento else None,
        'competencia': pagamento.competencia,
        'competencia_formatada': formatar_competencia(pagamento.competencia),
        'plano_nome': pagamento.plano.nome_plano if pagamento.plano else None,
        'data_pagamento': pagamento.data_pagamento.isoformat() if pagamento.data_pagamento else None,
        'forma_pagamento': pagamento.forma_pagamento,
        'pix_copia_cola': pagamento.pix_copia_cola,
        'qr_code_base64': qr_code_base64,
        'ticket_url': pagamento.ticket_url,
        'data_expiracao': pagamento.data_expiracao.isoformat() if pagamento.data_expiracao else None,
        'pix_expirado': _pix_expirado(pagamento),
        'provider_status_detail': pagamento.provider_status_detail,
        'checkout_url': pagamento.checkout_url if PagamentoDAO.checkout_ainda_valido(pagamento) else None,
    }


def _referencias_conhecidas(pagamento):
    """Todas as referencias que esta mensalidade legitimamente pode receber de volta:
    a do Pix direto e a do Checkout Pro."""
    return {r for r in (pagamento.external_reference, pagamento.checkout_external_reference) if r}


def _forma_pagamento_confirmada(resultado_mp, pagamento):
    """Meio de pagamento realmente usado, sempre a partir da resposta da API."""
    if resultado_mp.get('payment_method_id') == 'pix':
        return 'pix'
    tipo = resultado_mp.get('payment_type_id')
    if tipo:
        return FORMAS_PAGAMENTO_MP.get(tipo, tipo)
    # A API nao informou o meio: se a notificacao casou com a referencia do Checkout Pro
    # nao da para afirmar que foi Pix, entao fica o rotulo generico do provedor.
    if resultado_mp.get('external_reference') and resultado_mp['external_reference'] == pagamento.checkout_external_reference:
        return 'mercado_pago'
    return 'pix'


def _pagamento_mp_mais_relevante(pagamentos_mp):
    """Entre os pagamentos que o MP associa a uma referencia, devolve o que manda no
    estado final - um aprovado nunca perde para uma tentativa recusada anterior."""
    if not pagamentos_mp:
        return None

    def peso(item):
        status = item.get('status')
        return PRIORIDADE_STATUS_MP.index(status) if status in PRIORIDADE_STATUS_MP else len(PRIORIDADE_STATUS_MP)

    return sorted(pagamentos_mp, key=peso)[0]


def sincronizar_por_referencia_checkout(pagamento, *, timeout=None, retries=None):
    """Reconsulta o Checkout Pro pela referencia persistida e aplica o estado confirmado.

    Usada na volta do Mercado Pago e no polling de status quando ainda nao existe
    provider_payment_id (a preferencia nasce antes do pagamento). Nenhum dado da URL de
    retorno entra aqui: a referencia usada e a que ESTE servidor gravou na mensalidade.

    Devolve True se conseguiu falar com o MP (mesmo sem mudanca de estado).
    Levanta MercadoPagoIndisponivel em falha de transporte.
    """
    referencia = pagamento.checkout_external_reference
    if not referencia:
        return False

    resultado = buscar_pagamentos_por_referencia(referencia, timeout=timeout, retries=retries)
    if not resultado['sucesso']:
        logger.warning('Nao foi possivel consultar pagamentos da mensalidade %s por referencia.', pagamento.id)
        return False

    escolhido = _pagamento_mp_mais_relevante(resultado['pagamentos'])
    if not escolhido:
        return True  # falou com o MP, mas ninguem pagou ainda - estado local segue valendo

    _processar_status_mp(pagamento, {'sucesso': True, **escolhido}, provider_payment_id=escolhido.get('payment_id'))
    return True


@pix_bp.route('/api/mensalidades/<int:pagamento_id>/pix', methods=['POST'])
def criar_pix_mensalidade(pagamento_id):
    if session.get('tipo_usuario') not in ('admin', 'aluno'):
        return jsonify({'erro': 'Autenticacao necessaria.'}), 401

    pagamento = _pagamento_ou_none(pagamento_id)
    if not pagamento:
        return jsonify({'erro': 'Mensalidade nao encontrada.'}), 404

    if not _acesso_permitido(pagamento):
        return jsonify({'erro': 'Sem permissao para esta mensalidade.'}), 403

    if pagamento.status not in STATUS_PAGAVEIS:
        return jsonify({'erro': 'Esta mensalidade nao esta pendente.'}), 409

    if PagamentoDAO.pix_ainda_valido(pagamento):
        try:
            resultado_mp = buscar_pagamento(pagamento.provider_payment_id)
        except MercadoPagoIndisponivel:
            logger.warning(
                'Mercado Pago indisponivel ao reconferir cobranca pendente do pagamento %s; devolvendo dados ja salvos.',
                pagamento.id, exc_info=True,
            )
            # Nao arrisca criar uma segunda cobranca so porque a consulta falhou -
            # devolve o copia-e-cola ja persistido (sem QR novo em base64, que nao e salvo).
            return jsonify(_serializar_pagamento(pagamento)), 200

        if resultado_mp['sucesso']:
            _processar_status_mp(pagamento, resultado_mp)
            if pagamento.status not in STATUS_PAGAVEIS:
                # A consulta acima ja aprovou/reembolsou a cobranca existente - nada a gerar.
                return jsonify(_serializar_pagamento(pagamento)), 200
            if resultado_mp['status'] in ('pending', 'in_process'):
                return jsonify(_serializar_pagamento(
                    pagamento, qr_code_base64=resultado_mp.get('qr_code_base64'),
                )), 200
        # Senao (MP diz cancelado/rejeitado/expirado) cai para gerar uma nova tentativa abaixo.

    aluno = pagamento.aluno
    if not aluno or not aluno.email:
        return jsonify({'erro': 'Aluno sem e-mail cadastrado; nao e possivel gerar o Pix.'}), 422

    if pagamento.provider_payment_id:
        cancelar_pagamento(pagamento.provider_payment_id)

    idempotency_key = secrets.token_urlsafe(24)
    external_reference = f'mensalidade-{pagamento.id}-{secrets.token_urlsafe(8)}'

    # O valor cobrado vem sempre do banco - nunca do corpo da requisicao.
    try:
        resultado = criar_pagamento_pix(
            valor=Decimal(str(pagamento.valor)),
            descricao=f'Mensalidade {pagamento.plano.nome_plano}' if pagamento.plano else None,
            email_pagador=aluno.email,
            external_reference=external_reference,
            idempotency_key=idempotency_key,
        )
    except MercadoPagoIndisponivel:
        logger.error('Mercado Pago indisponivel ao criar Pix para o pagamento %s.', pagamento.id, exc_info=True)
        return jsonify({'erro': 'Mercado Pago indisponivel no momento. Tente novamente em instantes.'}), 503

    if not resultado['sucesso']:
        logger.error('Mercado Pago recusou a criacao do Pix para o pagamento %s: %s', pagamento.id, resultado['erro'])
        return jsonify({'erro': 'Nao foi possivel gerar a cobranca Pix. Tente novamente.'}), 502

    PagamentoDAO.salvar_dados_pix(
        pagamento,
        provider_payment_id=resultado['payment_id'],
        external_reference=external_reference,
        idempotency_key=idempotency_key,
        pix_copia_cola=resultado['qr_code'],
        ticket_url=resultado['ticket_url'],
        data_expiracao=resultado['data_expiracao'],
    )

    return jsonify(_serializar_pagamento(pagamento, qr_code_base64=resultado['qr_code_base64'])), 200


@pix_bp.route('/api/mensalidades/<int:pagamento_id>/status', methods=['GET'])
def status_pix_mensalidade(pagamento_id):
    if session.get('tipo_usuario') not in ('admin', 'aluno'):
        return jsonify({'erro': 'Autenticacao necessaria.'}), 401

    pagamento = _pagamento_ou_none(pagamento_id)
    if not pagamento:
        return jsonify({'erro': 'Mensalidade nao encontrada.'}), 404

    if not _acesso_permitido(pagamento):
        return jsonify({'erro': 'Sem permissao para esta mensalidade.'}), 403

    if pagamento.status in STATUS_FECHADOS:
        return jsonify(_serializar_pagamento(pagamento)), 200

    try:
        if pagamento.provider_payment_id:
            resultado_mp = buscar_pagamento(pagamento.provider_payment_id)
            if resultado_mp['sucesso']:
                _processar_status_mp(pagamento, resultado_mp)
        # A preferencia do Checkout Pro existe antes de haver qualquer payment_id, entao
        # a consulta e feita pela referencia persistida. Roda tambem quando ja existe um
        # provider_payment_id (do Pix): o aluno pode ter uma cobranca Pix aberta e ainda
        # assim concluir pelo checkout - a consulta acima nao enxergaria esse pagamento.
        if pagamento.status not in STATUS_FECHADOS and pagamento.checkout_external_reference:
            sincronizar_por_referencia_checkout(pagamento)
    except MercadoPagoIndisponivel:
        logger.warning('Mercado Pago indisponivel ao consultar status do pagamento %s.', pagamento.id, exc_info=True)

    return jsonify(_serializar_pagamento(pagamento)), 200


@pix_bp.route('/admin/pagamentos/<int:pagamento_id>/sincronizar', methods=['POST'])
def sincronizar_pagamento(pagamento_id):
    """Reconsulta manualmente o status no Mercado Pago - protegido por permissão de admin,
    útil quando o webhook atrasa ou falhou e o admin quer conferir agora."""
    if session.get('tipo_usuario') != 'admin':
        return redirect('/login')

    pagamento = _pagamento_ou_none(pagamento_id)
    if not pagamento:
        flash('Mensalidade não encontrada.', 'erro')
        return redirect('/admin/financeiro')

    if not pagamento.provider_payment_id:
        flash('Esta mensalidade não tem cobrança do Mercado Pago para sincronizar.', 'erro')
        return redirect(request.referrer or '/admin/financeiro')

    try:
        resultado_mp = buscar_pagamento(pagamento.provider_payment_id)
    except MercadoPagoIndisponivel:
        flash('Mercado Pago indisponível no momento. Tente novamente em instantes.', 'erro')
        return redirect(request.referrer or '/admin/financeiro')

    if not resultado_mp['sucesso']:
        flash('Não foi possível consultar esta cobrança no Mercado Pago.', 'erro')
        return redirect(request.referrer or '/admin/financeiro')

    status_antes = pagamento.status
    _processar_status_mp(pagamento, resultado_mp)
    if pagamento.status != status_antes:
        flash(f'Situação atualizada: {rotulo_status(status_antes)} → {rotulo_status(pagamento.status)}.', 'sucesso')
    else:
        flash('Situação confirmada junto ao Mercado Pago - nenhuma mudança.', 'sucesso')

    return redirect(request.referrer or '/admin/financeiro')


@pix_bp.route('/api/webhooks/mercado-pago', methods=['POST'])
def webhook_mercado_pago():
    x_signature = request.headers.get('x-signature', '')
    x_request_id = request.headers.get('x-request-id', '')
    data_id = request.args.get('data.id', '')

    if not x_signature or not x_request_id or not data_id:
        logger.warning('Webhook Mercado Pago sem headers/parametros esperados.')
        return '', 400

    secret = os.environ.get('MERCADO_PAGO_WEBHOOK_SECRET')
    if not secret:
        logger.error('MERCADO_PAGO_WEBHOOK_SECRET nao configurado; webhook recusado.')
        return '', 500

    if not validar_assinatura_webhook(x_signature=x_signature, x_request_id=x_request_id, data_id=data_id, secret=secret):
        logger.warning('Webhook Mercado Pago com assinatura invalida (request-id=%s).', x_request_id)
        return '', 401

    corpo = request.get_json(silent=True) or {}
    tipo = corpo.get('type', corpo.get('topic'))
    if tipo not in (None, 'payment'):
        return '', 200

    pagamento = PagamentoDAO.buscar_por_provider_payment_id(data_id)

    if pagamento and pagamento.status == 'pago' and pagamento.provider_payment_id == data_id:
        return '', 200  # notificacao repetida - ja processada, nem chama o MP de novo.

    # Nunca confia no corpo do webhook - o status real vem sempre desta consulta direta a
    # API. Orcamento curto e sem retry: o Mercado Pago desiste da entrega se a resposta
    # demorar, e o projeto nao tem fila/worker para empurrar isso para segundo plano
    # (criar thread solta no processo web perderia o trabalho num restart).
    try:
        resultado_mp = buscar_pagamento(data_id, timeout=TIMEOUT_WEBHOOK_SEGUNDOS, retries=MAX_RETRIES_WEBHOOK)
    except MercadoPagoIndisponivel:
        logger.error('Mercado Pago indisponivel ao processar webhook do pagamento %s.', data_id, exc_info=True)
        return '', 503

    if not resultado_mp['sucesso']:
        logger.error('Nao foi possivel consultar o pagamento %s no Mercado Pago: %s', data_id, resultado_mp['erro'])
        return '', 200

    if not pagamento and resultado_mp.get('external_reference'):
        pagamento = PagamentoDAO.buscar_por_external_reference(resultado_mp['external_reference'])

    if not pagamento:
        logger.info('Webhook Mercado Pago para pagamento %s nao corresponde a nenhuma mensalidade local.', data_id)
        return '', 200

    _processar_status_mp(pagamento, resultado_mp, provider_payment_id=data_id)
    return '', 200


def _processar_status_mp(pagamento, resultado_mp, provider_payment_id=None):
    """Fonte unica de aprovacao, usada pelo webhook, pelo polling de status e pela
    sincronizacao manual do admin.

    So aprova quando o status consultado na API for 'approved' E a referencia/valor
    baterem com o que esta salvo localmente - nunca com base no corpo do webhook.
    """
    status_mp = resultado_mp.get('status')
    referencia_mp = resultado_mp.get('external_reference')
    moeda_mp = resultado_mp.get('currency_id')
    valor_mp = resultado_mp.get('transaction_amount')

    # Uma aprovacao produz baixa financeira definitiva. Para esse estado, nao basta
    # que os dados presentes sejam coerentes: os tres campos de conciliacao precisam
    # existir na resposta autenticada do provedor. Assim, uma resposta incompleta nunca
    # consegue quitar uma mensalidade por acidente.
    if status_mp == 'approved':
        campos_ausentes = [
            nome for nome, valor in (
                ('external_reference', referencia_mp),
                ('transaction_amount', valor_mp),
                ('currency_id', moeda_mp),
            ) if valor is None or valor == ''
        ]
        if campos_ausentes:
            logger.error(
                'Pagamento aprovado incompleto para a mensalidade %s: campos de conciliacao ausentes=%s.',
                pagamento.id, ','.join(campos_ausentes),
            )
            return

    # A referencia confirmada pela API tem de ser uma das que ESTE servidor gerou e
    # gravou para esta mensalidade (Pix direto ou Checkout Pro).
    referencias = _referencias_conhecidas(pagamento)
    if referencia_mp and referencias and referencia_mp not in referencias:
        logger.error(
            'Divergencia de external_reference no pagamento %s: recebida uma referencia que nao pertence a esta mensalidade.',
            pagamento.id,
        )
        return

    if moeda_mp and moeda_mp != MOEDA:
        logger.error('Moeda inesperada no pagamento %s: esperado=%s recebido=%s', pagamento.id, MOEDA, moeda_mp)
        return

    if valor_mp is not None:
        diferenca = abs(Decimal(str(valor_mp)) - Decimal(str(pagamento.valor)))
        if diferenca > TOLERANCIA_VALOR:
            logger.error(
                'Divergencia de valor no pagamento %s: esperado=%s recebido=%s',
                pagamento.id, pagamento.valor, valor_mp,
            )
            return

    if provider_payment_id and pagamento.provider_payment_id != provider_payment_id:
        # So sobrescreve o id do provedor quando ainda nao ha um, ou quando esta chegando
        # a aprovacao de fato - uma notificacao atrasada de tentativa recusada nao pode
        # apagar o id do pagamento que ja quitou a mensalidade.
        if not pagamento.provider_payment_id or (status_mp == 'approved' and pagamento.status != 'pago'):
            pagamento.provider_payment_id = provider_payment_id

    if status_mp == 'approved':
        if pagamento.status == 'pago':
            return
        data_aprovacao = resultado_mp.get('date_approved')
        try:
            data_pagamento = datetime.fromisoformat(data_aprovacao).date() if data_aprovacao else date.today()
        except ValueError:
            data_pagamento = date.today()
        PagamentoDAO.marcar_pago_via_webhook(
            pagamento, data_pagamento=data_pagamento,
            forma_pagamento=_forma_pagamento_confirmada(resultado_mp, pagamento),
        )
    elif status_mp in ('refunded', 'charged_back'):
        if pagamento.status != 'reembolsado':
            PagamentoDAO.marcar_reembolsado_via_webhook(pagamento)
    elif status_mp == 'in_process':
        PagamentoDAO.marcar_em_processamento_via_webhook(pagamento)
    elif status_mp == 'rejected':
        PagamentoDAO.marcar_recusado_via_webhook(pagamento, status_detail=resultado_mp.get('status_detail'))
    # pending / cancelled: nao mexe no status local (cancelled costuma ser uma
    # tentativa antiga substituida por uma nova cobranca, nao a mensalidade toda).
