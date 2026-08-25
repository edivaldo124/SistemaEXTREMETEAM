import hashlib
import hmac
import logging
import os
from datetime import datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal

import mercadopago
import requests
from mercadopago.config import RequestOptions

logger = logging.getLogger(__name__)

DESCRICAO_PADRAO = 'Mensalidade - Extreme Team'
TIMEOUT_SEGUNDOS = 12.0
MAX_RETRIES = 2


class MercadoPagoIndisponivel(Exception):
    """Falha de transporte (timeout/DNS/conexao) ao falar com a API do Mercado Pago."""


def _sdk():
    token = os.environ.get('MERCADO_PAGO_ACCESS_TOKEN')
    if not token:
        raise MercadoPagoIndisponivel('MERCADO_PAGO_ACCESS_TOKEN nao configurado.')
    return mercadopago.SDK(token)


def _request_options(custom_headers=None):
    # Cada chamada recebe suas proprias opcoes (timeout/retries) - o SDK NAO mescla
    # request_options por chamada com o default do SDK, ele substitui por completo.
    return RequestOptions(connection_timeout=TIMEOUT_SEGUNDOS, max_retries=MAX_RETRIES, custom_headers=custom_headers)


def _valor_para_float(valor: Decimal) -> float:
    return float(Decimal(valor).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))


def _extrair_dados_pix(resposta_pagamento):
    dados_transacao = ((resposta_pagamento or {}).get('point_of_interaction') or {}).get('transaction_data') or {}
    return {
        'qr_code': dados_transacao.get('qr_code'),
        'qr_code_base64': dados_transacao.get('qr_code_base64'),
        'ticket_url': dados_transacao.get('ticket_url'),
    }


def _erro_menciona_expiracao(resultado):
    causas = (resultado.get('response') or {}).get('cause', [])
    if isinstance(causas, list):
        return any('date_of_expiration' in str(causa) for causa in causas)
    return 'date_of_expiration' in str(resultado.get('response') or '')


def criar_pagamento_pix(*, valor, descricao, email_pagador, external_reference, idempotency_key,
                         minutos_para_expirar=30):
    """Cria uma cobranca Pix no Mercado Pago.

    Retorna sempre um dict:
      sucesso -> {'sucesso': True, 'payment_id', 'status', 'qr_code', 'qr_code_base64',
                  'ticket_url', 'data_expiracao'}
      recusa de negocio do MP -> {'sucesso': False, 'erro': '<mensagem>'}

    Levanta MercadoPagoIndisponivel apenas para falha de transporte (timeout/DNS/conexao).
    """
    sdk = _sdk()
    data_expiracao = datetime.now().astimezone() + timedelta(minutes=minutos_para_expirar)

    payload = {
        'transaction_amount': _valor_para_float(valor),
        'description': descricao or DESCRICAO_PADRAO,
        'payment_method_id': 'pix',
        'payer': {'email': email_pagador},
        'external_reference': external_reference,
        'date_of_expiration': data_expiracao.isoformat(timespec='milliseconds'),
    }
    request_options = _request_options({'x-idempotency-key': idempotency_key})

    try:
        resultado = sdk.payment().create(payload, request_options)
    except requests.exceptions.RequestException as exc:
        raise MercadoPagoIndisponivel(f'Falha de comunicacao com o Mercado Pago: {exc}') from exc

    if resultado['status'] >= 400 and _erro_menciona_expiracao(resultado):
        logger.warning('Mercado Pago recusou date_of_expiration; tentando novamente sem o campo.')
        payload_sem_expiracao = {k: v for k, v in payload.items() if k != 'date_of_expiration'}
        try:
            resultado = sdk.payment().create(payload_sem_expiracao, request_options)
        except requests.exceptions.RequestException as exc:
            raise MercadoPagoIndisponivel(f'Falha de comunicacao com o Mercado Pago: {exc}') from exc
        data_expiracao = None

    if resultado['status'] >= 400:
        logger.warning('Mercado Pago recusou a criacao do Pix (status=%s).', resultado['status'])
        mensagem = (resultado.get('response') or {}).get('message', 'Falha ao criar cobranca Pix.')
        return {'sucesso': False, 'erro': mensagem}

    resposta = resultado.get('response') or {}
    dados_pix = _extrair_dados_pix(resposta)

    return {
        'sucesso': True,
        'payment_id': str(resposta.get('id')),
        'status': resposta.get('status'),
        'qr_code': dados_pix['qr_code'],
        'qr_code_base64': dados_pix['qr_code_base64'],
        'ticket_url': dados_pix['ticket_url'],
        'data_expiracao': data_expiracao,
    }


def buscar_pagamento(provider_payment_id):
    """Consulta o pagamento diretamente na API do Mercado Pago - fonte de verdade de status.

    Retorna {'sucesso': True, 'status', 'status_detail', 'external_reference',
    'transaction_amount', 'date_approved', 'qr_code', 'qr_code_base64', 'ticket_url'}
    ou {'sucesso': False, 'erro': '...'}. Levanta MercadoPagoIndisponivel em falha de transporte.
    """
    sdk = _sdk()
    try:
        resultado = sdk.payment().get(provider_payment_id, request_options=_request_options())
    except requests.exceptions.RequestException as exc:
        raise MercadoPagoIndisponivel(f'Falha de comunicacao com o Mercado Pago: {exc}') from exc

    if resultado['status'] >= 400:
        mensagem = (resultado.get('response') or {}).get('message', 'Pagamento nao encontrado no Mercado Pago.')
        return {'sucesso': False, 'erro': mensagem}

    resposta = resultado.get('response') or {}
    dados_pix = _extrair_dados_pix(resposta)
    return {
        'sucesso': True,
        'status': resposta.get('status'),
        'status_detail': resposta.get('status_detail'),
        'external_reference': resposta.get('external_reference'),
        'transaction_amount': resposta.get('transaction_amount'),
        'date_approved': resposta.get('date_approved'),
        'qr_code': dados_pix['qr_code'],
        'qr_code_base64': dados_pix['qr_code_base64'],
        'ticket_url': dados_pix['ticket_url'],
    }


def cancelar_pagamento(provider_payment_id):
    """Cancela uma cobranca Pix pendente no Mercado Pago. Best-effort: nunca lanca."""
    try:
        sdk = _sdk()
        sdk.payment().update(provider_payment_id, {'status': 'cancelled'}, request_options=_request_options())
    except Exception:
        logger.warning('Nao foi possivel cancelar a cobranca Pix %s no Mercado Pago.', provider_payment_id, exc_info=True)


def validar_assinatura_webhook(*, x_signature, x_request_id, data_id, secret):
    """Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago.

    Nunca lanca - retorna False para qualquer formato de header inesperado.
    """
    if not x_signature or not x_request_id or not data_id or not secret:
        return False

    ts, v1 = None, None
    for parte in x_signature.split(','):
        if '=' not in parte:
            continue
        chave, _, valor = parte.partition('=')
        chave, valor = chave.strip(), valor.strip()
        if chave == 'ts':
            ts = valor
        elif chave == 'v1':
            v1 = valor

    if not ts or not v1:
        return False

    manifest = f'id:{str(data_id).lower()};request-id:{x_request_id};ts:{ts};'
    assinatura_calculada = hmac.new(secret.encode(), manifest.encode(), hashlib.sha256).hexdigest()

    return hmac.compare_digest(assinatura_calculada, v1)
