import hashlib
import hmac
import logging
import os
from datetime import datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal
from urllib.parse import urlparse

import mercadopago
import requests
from mercadopago.config import RequestOptions

logger = logging.getLogger(__name__)

DESCRICAO_PADRAO = 'Mensalidade - Extreme Team'
TIMEOUT_SEGUNDOS = 12.0
MAX_RETRIES = 2

# O webhook do Mercado Pago aborta a entrega se a resposta demorar demais (o simulador
# do painel corta por volta de 22s). Como o processamento e sincrono - o projeto nao tem
# fila/worker - a consulta feita dentro do webhook usa um orcamento curto e sem retry,
# em vez dos 12s x 3 tentativas usados nas chamadas iniciadas pelo usuario.
TIMEOUT_WEBHOOK_SEGUNDOS = 5.0
MAX_RETRIES_WEBHOOK = 0

MOEDA = 'BRL'
AMBIENTE_PRODUCAO = 'producao'
AMBIENTE_SANDBOX = 'sandbox'
CAMINHO_WEBHOOK = '/api/webhooks/mercado-pago'

# Prefixo publico e documentado das credenciais de teste do Mercado Pago. So o prefixo
# e lido - o token em si nunca e logado, devolvido nem gravado em lugar nenhum.
PREFIXO_TOKEN_TESTE = 'TEST-'

# Janela de validade da preferencia do Checkout Pro. Curta o bastante para o valor
# cobrado nao envelhecer, longa o bastante para o aluno terminar um boleto/cartao.
CHECKOUT_MINUTOS_EXPIRACAO = 60


class MercadoPagoIndisponivel(Exception):
    """Falha de transporte (timeout/DNS/conexao) ao falar com a API do Mercado Pago."""


class ConfiguracaoInvalida(Exception):
    """Variavel de ambiente obrigatoria ausente ou com formato invalido.

    Erro de configuracao do servidor, nao do aluno - a mensagem nunca deve chegar crua
    ao navegador.
    """


def _sdk():
    token = os.environ.get('MERCADO_PAGO_ACCESS_TOKEN')
    if not token:
        raise MercadoPagoIndisponivel('MERCADO_PAGO_ACCESS_TOKEN nao configurado.')
    return mercadopago.SDK(token)


def _request_options(custom_headers=None, *, timeout=None, retries=None):
    # Cada chamada recebe suas proprias opcoes (timeout/retries) - o SDK NAO mescla
    # request_options por chamada com o default do SDK, ele substitui por completo.
    return RequestOptions(
        connection_timeout=TIMEOUT_SEGUNDOS if timeout is None else timeout,
        max_retries=MAX_RETRIES if retries is None else retries,
        custom_headers=custom_headers,
    )


def _valor_para_float(valor: Decimal) -> float:
    return float(Decimal(valor).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))


def ambiente_mercado_pago():
    """Diz se a integracao esta apontando para producao ou para o sandbox.

    Prioriza a configuracao explicita em MERCADO_PAGO_AMBIENTE; sem ela, usa o prefixo
    publico do access token ('TEST-' identifica credencial de teste). Em caso de duvida
    assume producao, que e o modo restritivo (nunca devolve uma URL de sandbox para
    quem esta com credencial real).
    """
    configurado = (os.environ.get('MERCADO_PAGO_AMBIENTE') or '').strip().lower()
    if configurado in (AMBIENTE_PRODUCAO, AMBIENTE_SANDBOX):
        return configurado
    if configurado:
        raise ConfiguracaoInvalida(
            f"MERCADO_PAGO_AMBIENTE deve ser '{AMBIENTE_PRODUCAO}' ou '{AMBIENTE_SANDBOX}'."
        )

    token = os.environ.get('MERCADO_PAGO_ACCESS_TOKEN') or ''
    return AMBIENTE_SANDBOX if token.startswith(PREFIXO_TOKEN_TESTE) else AMBIENTE_PRODUCAO


def _base_url_opcional():
    """URL publica normalizada, ou None quando nao houver uma valida configurada."""
    bruta = (os.environ.get('APP_BASE_URL') or '').strip().rstrip('/')
    if not bruta:
        return None
    partes = urlparse(bruta)
    if partes.scheme not in ('http', 'https') or not partes.netloc:
        return None
    return bruta


def base_url_publica():
    """Mesma URL, porem obrigatoria - levanta ConfiguracaoInvalida se faltar/for invalida.

    O Checkout Pro depende dela para montar back_urls e notification_url: sem uma URL
    publica valida o aluno sairia do sistema sem caminho de volta, entao falhamos antes
    de criar qualquer cobranca.
    """
    base = _base_url_opcional()
    if not base:
        raise ConfiguracaoInvalida(
            'APP_BASE_URL ausente ou invalida - defina a URL publica (http/https) da aplicacao.'
        )
    return base


def url_webhook(base_url=None):
    return f'{base_url or base_url_publica()}{CAMINHO_WEBHOOK}'


def _extrair_dados_pix(resposta_pagamento):
    dados_transacao = ((resposta_pagamento or {}).get('point_of_interaction') or {}).get('transaction_data') or {}
    return {
        'qr_code': dados_transacao.get('qr_code'),
        'qr_code_base64': dados_transacao.get('qr_code_base64'),
        'ticket_url': dados_transacao.get('ticket_url'),
    }


def _erro_menciona(resultado, termo):
    causas = (resultado.get('response') or {}).get('cause', [])
    if isinstance(causas, list) and causas:
        return any(termo in str(causa) for causa in causas)
    return termo in str(resultado.get('response') or '')


def _erro_menciona_expiracao(resultado):
    return _erro_menciona(resultado, 'date_of_expiration')


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
    # O Pix continua funcionando sem APP_BASE_URL (so perde a notificacao push do MP,
    # que o polling de status cobre) - diferente do Checkout Pro, que a exige.
    app_base_url = _base_url_opcional()
    if app_base_url:
        payload['notification_url'] = url_webhook(app_base_url)
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


def criar_preferencia_checkout(*, valor, titulo, descricao, email_pagador, external_reference,
                               idempotency_key, url_sucesso, url_pendente, url_falha,
                               minutos_para_expirar=CHECKOUT_MINUTOS_EXPIRACAO):
    """Cria uma preferencia do Checkout Pro (cartao, boleto, saldo MP, Pix e o que mais
    a conta tiver habilitado) e devolve a URL hospedada para onde o aluno vai.

    O valor vem sempre de quem chama (que o le do banco) - nunca do navegador. O
    external_reference deve ser uma referencia aleatoria ja persistida na mensalidade.

    Retorna:
      sucesso -> {'sucesso': True, 'preference_id', 'url_checkout', 'ambiente', 'expira_em'}
      recusa de negocio do MP -> {'sucesso': False, 'erro': '<mensagem do MP>'}

    Levanta MercadoPagoIndisponivel em falha de transporte e ConfiguracaoInvalida quando
    APP_BASE_URL estiver ausente/invalida (checado antes de qualquer chamada externa).
    """
    base_url = base_url_publica()
    ambiente = ambiente_mercado_pago()
    sdk = _sdk()

    agora = datetime.now().astimezone()
    expira_em = agora + timedelta(minutes=minutos_para_expirar)

    payload = {
        'items': [{
            'id': external_reference,
            'title': (titulo or DESCRICAO_PADRAO)[:250],
            'description': (descricao or DESCRICAO_PADRAO)[:250],
            'quantity': 1,
            'currency_id': MOEDA,
            'unit_price': _valor_para_float(valor),
        }],
        'external_reference': external_reference,
        'notification_url': url_webhook(base_url),
        'back_urls': {'success': url_sucesso, 'pending': url_pendente, 'failure': url_falha},
        'auto_return': 'approved',
        'binary_mode': False,
        'expires': True,
        'expiration_date_from': agora.isoformat(timespec='milliseconds'),
        'expiration_date_to': expira_em.isoformat(timespec='milliseconds'),
    }
    # O e-mail so entra quando parece valido - o MP recusa a preferencia inteira se
    # o payer.email for malformado, e ele e opcional para o Checkout Pro.
    if email_pagador and '@' in email_pagador:
        payload['payer'] = {'email': email_pagador}

    request_options = _request_options({'x-idempotency-key': idempotency_key})

    def _criar(corpo):
        try:
            return sdk.preference().create(corpo, request_options)
        except requests.exceptions.RequestException as exc:
            raise MercadoPagoIndisponivel(f'Falha de comunicacao com o Mercado Pago: {exc}') from exc

    resultado = _criar(payload)

    # Mesmo tratamento dado ao date_of_expiration do Pix: contas/ambientes que recusam
    # auto_return (ex.: back_urls sem dominio publico) ainda conseguem checkout, so sem
    # o retorno automatico depois da aprovacao.
    if resultado['status'] >= 400 and _erro_menciona(resultado, 'auto_return'):
        logger.warning('Mercado Pago recusou auto_return; recriando a preferencia sem o campo.')
        resultado = _criar({k: v for k, v in payload.items() if k != 'auto_return'})

    if resultado['status'] >= 400:
        logger.warning('Mercado Pago recusou a criacao da preferencia (status=%s).', resultado['status'])
        mensagem = (resultado.get('response') or {}).get('message', 'Falha ao criar a preferencia de checkout.')
        return {'sucesso': False, 'erro': mensagem}

    resposta = resultado.get('response') or {}
    url_checkout = _url_checkout(resposta, ambiente)
    if not url_checkout:
        logger.error('Preferencia criada sem URL de checkout utilizavel no ambiente %s.', ambiente)
        return {'sucesso': False, 'erro': 'Preferencia criada sem URL de checkout.'}

    return {
        'sucesso': True,
        'preference_id': str(resposta.get('id')),
        'url_checkout': url_checkout,
        'ambiente': ambiente,
        'expira_em': expira_em,
    }


def _url_checkout(resposta, ambiente):
    """Escolhe init_point/sandbox_init_point conforme o ambiente.

    Em producao NUNCA cai para o sandbox_init_point: um checkout de sandbox parece
    concluido para o aluno mas nao cobra nada de verdade. Sem init_point em producao,
    a criacao e tratada como falha.
    """
    init_point = resposta.get('init_point')
    sandbox_init_point = resposta.get('sandbox_init_point')
    if ambiente == AMBIENTE_SANDBOX:
        return sandbox_init_point or init_point
    return init_point


def _normalizar_pagamento(resposta):
    dados_pix = _extrair_dados_pix(resposta)
    return {
        'payment_id': str(resposta.get('id')) if resposta.get('id') is not None else None,
        'status': resposta.get('status'),
        'status_detail': resposta.get('status_detail'),
        'external_reference': resposta.get('external_reference'),
        'transaction_amount': resposta.get('transaction_amount'),
        'currency_id': resposta.get('currency_id'),
        'payment_method_id': resposta.get('payment_method_id'),
        'payment_type_id': resposta.get('payment_type_id'),
        'date_approved': resposta.get('date_approved'),
        'qr_code': dados_pix['qr_code'],
        'qr_code_base64': dados_pix['qr_code_base64'],
        'ticket_url': dados_pix['ticket_url'],
    }


def buscar_pagamento(provider_payment_id, *, timeout=None, retries=None):
    """Consulta o pagamento diretamente na API do Mercado Pago - fonte de verdade de status.

    Retorna {'sucesso': True, 'payment_id', 'status', 'status_detail', 'external_reference',
    'transaction_amount', 'currency_id', 'payment_method_id', 'payment_type_id',
    'date_approved', 'qr_code', 'qr_code_base64', 'ticket_url'} ou {'sucesso': False,
    'erro': '...'}. Levanta MercadoPagoIndisponivel em falha de transporte.

    timeout/retries permitem que o webhook use um orcamento curto (ver
    TIMEOUT_WEBHOOK_SEGUNDOS) sem mudar o das chamadas iniciadas pelo aluno.
    """
    sdk = _sdk()
    try:
        resultado = sdk.payment().get(
            provider_payment_id, request_options=_request_options(timeout=timeout, retries=retries),
        )
    except requests.exceptions.RequestException as exc:
        raise MercadoPagoIndisponivel(f'Falha de comunicacao com o Mercado Pago: {exc}') from exc

    if resultado['status'] >= 400:
        mensagem = (resultado.get('response') or {}).get('message', 'Pagamento nao encontrado no Mercado Pago.')
        return {'sucesso': False, 'erro': mensagem}

    return {'sucesso': True, **_normalizar_pagamento(resultado.get('response') or {})}


def buscar_pagamentos_por_referencia(external_reference, *, timeout=None, retries=None):
    """Lista os pagamentos que o Mercado Pago associa a uma external_reference.

    Usada na volta do Checkout Pro: o payment_id vem na URL de retorno e nao merece
    confianca, entao perguntamos ao MP quais pagamentos existem para a NOSSA referencia
    (que e aleatoria e ja esta persistida na mensalidade).

    Retorna {'sucesso': True, 'pagamentos': [<normalizado>, ...]} ou {'sucesso': False, 'erro'}.
    """
    sdk = _sdk()
    try:
        resultado = sdk.payment().search(
            filters={'external_reference': external_reference},
            request_options=_request_options(timeout=timeout, retries=retries),
        )
    except requests.exceptions.RequestException as exc:
        raise MercadoPagoIndisponivel(f'Falha de comunicacao com o Mercado Pago: {exc}') from exc

    if resultado['status'] >= 400:
        mensagem = (resultado.get('response') or {}).get('message', 'Falha ao consultar pagamentos no Mercado Pago.')
        return {'sucesso': False, 'erro': mensagem}

    encontrados = (resultado.get('response') or {}).get('results') or []
    return {'sucesso': True, 'pagamentos': [_normalizar_pagamento(item or {}) for item in encontrados]}


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
