import logging
import os
import secrets
from datetime import date, datetime
from decimal import Decimal

from flask import Blueprint, jsonify, request, session

from dao.financeiroDAO import STATUS_FECHADOS, PagamentoDAO
from servicos.mercado_pago import (
    MercadoPagoIndisponivel,
    buscar_pagamento,
    cancelar_pagamento,
    criar_pagamento_pix,
    validar_assinatura_webhook,
)

pix_bp = Blueprint('pix', __name__)
logger = logging.getLogger(__name__)

STATUS_PAGAVEIS = ('pendente', 'atrasado')
TOLERANCIA_VALOR = Decimal('0.01')


def _pagamento_ou_none(pagamento_id):
    return PagamentoDAO.buscar_por_id(pagamento_id)


def _acesso_permitido(pagamento):
    if session.get('tipo_usuario') == 'admin':
        return True
    return session.get('tipo_usuario') == 'aluno' and session.get('aluno_id') == pagamento.aluno_id


def _serializar_pagamento(pagamento, *, qr_code_base64=None):
    return {
        'pagamento_id': pagamento.id,
        'status': pagamento.status,
        'valor': pagamento.valor,
        'vencimento': pagamento.vencimento.isoformat() if pagamento.vencimento else None,
        'data_pagamento': pagamento.data_pagamento.isoformat() if pagamento.data_pagamento else None,
        'pix_copia_cola': pagamento.pix_copia_cola,
        'qr_code_base64': qr_code_base64,
        'ticket_url': pagamento.ticket_url,
        'data_expiracao': pagamento.data_expiracao.isoformat() if pagamento.data_expiracao else None,
    }


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

    if pagamento.status in STATUS_FECHADOS or not pagamento.provider_payment_id:
        return jsonify(_serializar_pagamento(pagamento)), 200

    try:
        resultado_mp = buscar_pagamento(pagamento.provider_payment_id)
    except MercadoPagoIndisponivel:
        logger.warning('Mercado Pago indisponivel ao consultar status do pagamento %s.', pagamento.id, exc_info=True)
        return jsonify(_serializar_pagamento(pagamento)), 200

    if resultado_mp['sucesso']:
        _processar_status_mp(pagamento, resultado_mp)

    return jsonify(_serializar_pagamento(pagamento)), 200


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

    # Nunca confia no corpo do webhook - o status real vem sempre desta consulta direta a API.
    try:
        resultado_mp = buscar_pagamento(data_id)
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
    """Fonte unica de aprovacao, usada pelo webhook e pelo polling de status.

    So aprova quando o status consultado na API for 'approved' E a referencia/valor
    baterem com o que esta salvo localmente - nunca com base no corpo do webhook.
    """
    status_mp = resultado_mp.get('status')
    referencia_mp = resultado_mp.get('external_reference')

    if referencia_mp and pagamento.external_reference and referencia_mp != pagamento.external_reference:
        logger.error(
            'Divergencia de external_reference no pagamento %s: esperado=%s recebido=%s',
            pagamento.id, pagamento.external_reference, referencia_mp,
        )
        return

    valor_mp = resultado_mp.get('transaction_amount')
    if valor_mp is not None:
        diferenca = abs(Decimal(str(valor_mp)) - Decimal(str(pagamento.valor)))
        if diferenca > TOLERANCIA_VALOR:
            logger.error(
                'Divergencia de valor no pagamento %s: esperado=%s recebido=%s',
                pagamento.id, pagamento.valor, valor_mp,
            )
            return

    if provider_payment_id and pagamento.provider_payment_id != provider_payment_id:
        pagamento.provider_payment_id = provider_payment_id

    if status_mp == 'approved':
        if pagamento.status == 'pago':
            return
        data_aprovacao = resultado_mp.get('date_approved')
        try:
            data_pagamento = datetime.fromisoformat(data_aprovacao).date() if data_aprovacao else date.today()
        except ValueError:
            data_pagamento = date.today()
        PagamentoDAO.marcar_pago_via_webhook(pagamento, data_pagamento=data_pagamento)
    elif status_mp in ('refunded', 'charged_back'):
        if pagamento.status != 'reembolsado':
            PagamentoDAO.marcar_reembolsado_via_webhook(pagamento)
    # pending / in_process / rejected / cancelled: nao mexe no status local.
