import hashlib
import hmac
from decimal import Decimal

import pytest
import requests

from servicos import mercado_pago
from servicos.mercado_pago import MercadoPagoIndisponivel


class _FakePaymentResource:
    def __init__(self, estado):
        self._estado = estado

    def create(self, payload, request_options=None):
        self._estado['chamadas'].append(('create', payload))
        resposta = self._estado['create']
        return resposta(payload) if callable(resposta) else resposta

    def get(self, payment_id, request_options=None):
        self._estado['chamadas'].append(('get', payment_id))
        resposta = self._estado['get']
        return resposta(payment_id) if callable(resposta) else resposta

    def update(self, payment_id, payload, request_options=None):
        self._estado['chamadas'].append(('update', payment_id, payload))
        resposta = self._estado.get('update') or {'status': 200, 'response': {}}
        return resposta(payment_id, payload) if callable(resposta) else resposta

    def search(self, filters=None, request_options=None):
        self._estado['chamadas'].append(('search', filters))
        resposta = self._estado.get('search') or {'status': 200, 'response': {'results': []}}
        return resposta(filters) if callable(resposta) else resposta


class _FakePreferenceResource:
    def __init__(self, estado):
        self._estado = estado

    def create(self, payload, request_options=None):
        self._estado['chamadas'].append(('preference_create', payload))
        resposta = self._estado['preference_create']
        return resposta(payload) if callable(resposta) else resposta


@pytest.fixture
def mp_fake(monkeypatch):
    estado = {'create': None, 'get': None, 'update': None, 'search': None,
              'preference_create': None, 'chamadas': []}

    class FakeSDK:
        def __init__(self, token=None, request_options=None):
            self.token = token

        def payment(self):
            return _FakePaymentResource(estado)

        def preference(self):
            return _FakePreferenceResource(estado)

    monkeypatch.setattr(mercado_pago.mercadopago, 'SDK', FakeSDK)
    return estado


@pytest.fixture
def base_url(monkeypatch):
    monkeypatch.setenv('APP_BASE_URL', 'https://academia.example.com')
    return 'https://academia.example.com'


def test_criar_pagamento_pix_sucesso_extrai_qr_code(mp_fake):
    mp_fake['create'] = {
        'status': 201,
        'response': {
            'id': 999888777,
            'status': 'pending',
            'point_of_interaction': {
                'transaction_data': {
                    'qr_code': '00020126...copia-e-cola',
                    'qr_code_base64': 'aGVsbG8=',
                    'ticket_url': 'https://mp.example/ticket',
                },
            },
        },
    }

    resultado = mercado_pago.criar_pagamento_pix(
        valor=Decimal('150.00'),
        descricao='Mensalidade teste',
        email_pagador='aluno@example.com',
        external_reference='mensalidade-1-abc',
        idempotency_key='chave-123',
    )

    assert resultado['sucesso'] is True
    assert resultado['payment_id'] == '999888777'
    assert resultado['qr_code'] == '00020126...copia-e-cola'
    assert resultado['qr_code_base64'] == 'aGVsbG8='
    assert resultado['ticket_url'] == 'https://mp.example/ticket'


def test_criar_pagamento_pix_recusa_de_negocio_nao_lanca(mp_fake):
    mp_fake['create'] = {'status': 400, 'response': {'message': 'invalid payer email'}}

    resultado = mercado_pago.criar_pagamento_pix(
        valor=Decimal('150.00'),
        descricao='Mensalidade teste',
        email_pagador='invalido',
        external_reference='mensalidade-1-abc',
        idempotency_key='chave-123',
    )

    assert resultado['sucesso'] is False
    assert 'invalid payer email' in resultado['erro']


def test_criar_pagamento_pix_falha_de_transporte_levanta_indisponivel(mp_fake):
    def _levanta_timeout(payload):
        raise requests.exceptions.ConnectTimeout('timeout simulado')

    mp_fake['create'] = _levanta_timeout

    with pytest.raises(MercadoPagoIndisponivel):
        mercado_pago.criar_pagamento_pix(
            valor=Decimal('150.00'),
            descricao='Mensalidade teste',
            email_pagador='aluno@example.com',
            external_reference='mensalidade-1-abc',
            idempotency_key='chave-123',
        )


def test_buscar_pagamento_sucesso(mp_fake):
    mp_fake['get'] = {
        'status': 200,
        'response': {
            'status': 'approved',
            'status_detail': 'accredited',
            'external_reference': 'mensalidade-1-abc',
            'transaction_amount': 150.0,
            'date_approved': '2026-08-25T10:00:00.000-03:00',
            'point_of_interaction': {'transaction_data': {}},
        },
    }

    resultado = mercado_pago.buscar_pagamento('999888777')

    assert resultado['sucesso'] is True
    assert resultado['status'] == 'approved'
    assert resultado['transaction_amount'] == 150.0


def test_buscar_pagamento_falha_de_transporte_levanta_indisponivel(mp_fake):
    def _levanta_conexao(payment_id):
        raise requests.exceptions.ConnectionError('sem rede')

    mp_fake['get'] = _levanta_conexao

    with pytest.raises(MercadoPagoIndisponivel):
        mercado_pago.buscar_pagamento('999888777')


def test_validar_assinatura_webhook_aceita_assinatura_correta():
    secret = 'segredo-teste'
    data_id = '123456'
    request_id = 'req-abc'
    ts = '1700000000'
    manifest = f'id:{data_id};request-id:{request_id};ts:{ts};'
    v1 = hmac.new(secret.encode(), manifest.encode(), hashlib.sha256).hexdigest()

    assert mercado_pago.validar_assinatura_webhook(
        x_signature=f'ts={ts},v1={v1}', x_request_id=request_id, data_id=data_id, secret=secret,
    ) is True


def test_validar_assinatura_webhook_rejeita_assinatura_incorreta():
    assert mercado_pago.validar_assinatura_webhook(
        x_signature='ts=1700000000,v1=assinaturaerrada', x_request_id='req-abc', data_id='123456',
        secret='segredo-teste',
    ) is False


def test_validar_assinatura_webhook_rejeita_formato_inesperado():
    assert mercado_pago.validar_assinatura_webhook(
        x_signature='formato-invalido-sem-igual', x_request_id='req-abc', data_id='123456', secret='segredo-teste',
    ) is False


def test_validar_assinatura_webhook_rejeita_campos_ausentes():
    assert mercado_pago.validar_assinatura_webhook(
        x_signature='', x_request_id='req-abc', data_id='123456', secret='segredo-teste',
    ) is False


# ---------------------------------------------------------------------------
# Ambiente e URL publica
# ---------------------------------------------------------------------------

def test_ambiente_usa_configuracao_explicita(monkeypatch):
    monkeypatch.setenv('MERCADO_PAGO_AMBIENTE', 'sandbox')
    monkeypatch.setenv('MERCADO_PAGO_ACCESS_TOKEN', 'APP_USR-token-de-producao')

    assert mercado_pago.ambiente_mercado_pago() == 'sandbox'


def test_ambiente_cai_no_prefixo_do_token_quando_nao_configurado(monkeypatch):
    monkeypatch.delenv('MERCADO_PAGO_AMBIENTE', raising=False)
    monkeypatch.setenv('MERCADO_PAGO_ACCESS_TOKEN', 'TEST-1234567890')

    assert mercado_pago.ambiente_mercado_pago() == 'sandbox'


def test_ambiente_assume_producao_para_token_sem_prefixo_de_teste(monkeypatch):
    monkeypatch.delenv('MERCADO_PAGO_AMBIENTE', raising=False)
    monkeypatch.setenv('MERCADO_PAGO_ACCESS_TOKEN', 'APP_USR-1234567890')

    assert mercado_pago.ambiente_mercado_pago() == 'producao'


def test_ambiente_invalido_e_recusado(monkeypatch):
    monkeypatch.setenv('MERCADO_PAGO_AMBIENTE', 'homologacao')

    with pytest.raises(mercado_pago.ConfiguracaoInvalida):
        mercado_pago.ambiente_mercado_pago()


@pytest.mark.parametrize('valor', ['', '   ', 'academia.example.com', 'ftp://academia.example.com'])
def test_base_url_publica_recusa_valor_ausente_ou_invalido(monkeypatch, valor):
    monkeypatch.setenv('APP_BASE_URL', valor)

    with pytest.raises(mercado_pago.ConfiguracaoInvalida):
        mercado_pago.base_url_publica()


def test_base_url_publica_normaliza_barra_final(monkeypatch):
    monkeypatch.setenv('APP_BASE_URL', 'https://academia.example.com/')

    assert mercado_pago.base_url_publica() == 'https://academia.example.com'
    assert mercado_pago.url_webhook() == 'https://academia.example.com/api/webhooks/mercado-pago'


# ---------------------------------------------------------------------------
# criar_preferencia_checkout
# ---------------------------------------------------------------------------

def _resposta_preferencia(status=201, **extras):
    resposta = {
        'id': 'pref-123',
        'init_point': 'https://www.mercadopago.com.br/checkout?pref_id=pref-123',
        'sandbox_init_point': 'https://sandbox.mercadopago.com.br/checkout?pref_id=pref-123',
    }
    resposta.update(extras)
    return {'status': status, 'response': resposta}


def _criar_preferencia(**overrides):
    argumentos = dict(
        valor=Decimal('150.00'),
        titulo='Mensalidade Mensal',
        descricao='Mensalidade Mensal Setembro/2026',
        email_pagador='aluno@example.com',
        external_reference='checkout-1-abc',
        idempotency_key='chave-123',
        url_sucesso='https://academia.example.com/retorno',
        url_pendente='https://academia.example.com/retorno',
        url_falha='https://academia.example.com/retorno',
    )
    argumentos.update(overrides)
    return mercado_pago.criar_preferencia_checkout(**argumentos)


def test_criar_preferencia_monta_payload_esperado(mp_fake, base_url, monkeypatch):
    monkeypatch.setenv('MERCADO_PAGO_AMBIENTE', 'producao')
    mp_fake['preference_create'] = _resposta_preferencia()

    resultado = _criar_preferencia()

    assert resultado['sucesso'] is True
    assert resultado['preference_id'] == 'pref-123'
    assert resultado['ambiente'] == 'producao'

    _, payload = mp_fake['chamadas'][0]
    item = payload['items'][0]
    assert item['quantity'] == 1
    assert item['currency_id'] == 'BRL'
    assert item['unit_price'] == 150.0
    assert payload['external_reference'] == 'checkout-1-abc'
    assert payload['payer']['email'] == 'aluno@example.com'
    assert payload['notification_url'] == f'{base_url}/api/webhooks/mercado-pago'
    assert payload['back_urls']['success'] == 'https://academia.example.com/retorno'
    assert payload['auto_return'] == 'approved'


def test_criar_preferencia_usa_init_point_em_producao(mp_fake, base_url, monkeypatch):
    monkeypatch.setenv('MERCADO_PAGO_AMBIENTE', 'producao')
    mp_fake['preference_create'] = _resposta_preferencia()

    resultado = _criar_preferencia()

    assert resultado['url_checkout'] == 'https://www.mercadopago.com.br/checkout?pref_id=pref-123'


def test_criar_preferencia_usa_sandbox_init_point_no_sandbox(mp_fake, base_url, monkeypatch):
    monkeypatch.setenv('MERCADO_PAGO_AMBIENTE', 'sandbox')
    mp_fake['preference_create'] = _resposta_preferencia()

    resultado = _criar_preferencia()

    assert resultado['ambiente'] == 'sandbox'
    assert resultado['url_checkout'] == 'https://sandbox.mercadopago.com.br/checkout?pref_id=pref-123'


def test_producao_nunca_cai_para_a_url_de_sandbox(mp_fake, base_url, monkeypatch):
    monkeypatch.setenv('MERCADO_PAGO_AMBIENTE', 'producao')
    mp_fake['preference_create'] = {'status': 201, 'response': {
        'id': 'pref-123',
        'sandbox_init_point': 'https://sandbox.mercadopago.com.br/checkout?pref_id=pref-123',
    }}

    resultado = _criar_preferencia()

    assert resultado['sucesso'] is False


def test_criar_preferencia_omite_email_invalido(mp_fake, base_url, monkeypatch):
    monkeypatch.setenv('MERCADO_PAGO_AMBIENTE', 'producao')
    mp_fake['preference_create'] = _resposta_preferencia()

    _criar_preferencia(email_pagador='sem-arroba')

    _, payload = mp_fake['chamadas'][0]
    assert 'payer' not in payload


def test_criar_preferencia_tenta_de_novo_sem_auto_return(mp_fake, base_url, monkeypatch):
    monkeypatch.setenv('MERCADO_PAGO_AMBIENTE', 'producao')
    respostas = [
        {'status': 400, 'response': {'message': 'invalid', 'cause': [{'description': 'auto_return invalid'}]}},
        _resposta_preferencia(),
    ]
    mp_fake['preference_create'] = lambda payload: respostas.pop(0)

    resultado = _criar_preferencia()

    assert resultado['sucesso'] is True
    _, segundo_payload = mp_fake['chamadas'][1]
    assert 'auto_return' not in segundo_payload


def test_criar_preferencia_recusa_de_negocio_nao_lanca(mp_fake, base_url, monkeypatch):
    monkeypatch.setenv('MERCADO_PAGO_AMBIENTE', 'producao')
    mp_fake['preference_create'] = {'status': 400, 'response': {'message': 'invalid collector'}}

    resultado = _criar_preferencia()

    assert resultado['sucesso'] is False
    assert 'invalid collector' in resultado['erro']


def test_criar_preferencia_falha_de_transporte_levanta_indisponivel(mp_fake, base_url, monkeypatch):
    monkeypatch.setenv('MERCADO_PAGO_AMBIENTE', 'producao')

    def _levanta(payload):
        raise requests.exceptions.ConnectTimeout('timeout simulado')

    mp_fake['preference_create'] = _levanta

    with pytest.raises(MercadoPagoIndisponivel):
        _criar_preferencia()


def test_criar_preferencia_sem_base_url_falha_antes_de_chamar_o_mp(mp_fake, monkeypatch):
    monkeypatch.delenv('APP_BASE_URL', raising=False)
    mp_fake['preference_create'] = _resposta_preferencia()

    with pytest.raises(mercado_pago.ConfiguracaoInvalida):
        _criar_preferencia()

    assert mp_fake['chamadas'] == []  # nenhuma cobranca chegou a ser criada


# ---------------------------------------------------------------------------
# buscar_pagamentos_por_referencia
# ---------------------------------------------------------------------------

def test_buscar_pagamentos_por_referencia_normaliza_resultados(mp_fake):
    mp_fake['search'] = {'status': 200, 'response': {'results': [
        {'id': 777, 'status': 'approved', 'external_reference': 'checkout-1-abc',
         'transaction_amount': 150.0, 'currency_id': 'BRL',
         'payment_type_id': 'credit_card', 'payment_method_id': 'master'},
    ]}}

    resultado = mercado_pago.buscar_pagamentos_por_referencia('checkout-1-abc')

    assert resultado['sucesso'] is True
    assert resultado['pagamentos'][0]['payment_id'] == '777'
    assert resultado['pagamentos'][0]['payment_type_id'] == 'credit_card'
    assert mp_fake['chamadas'][0] == ('search', {'external_reference': 'checkout-1-abc'})


def test_buscar_pagamentos_por_referencia_sem_resultado(mp_fake):
    mp_fake['search'] = {'status': 200, 'response': {'results': []}}

    assert mercado_pago.buscar_pagamentos_por_referencia('nao-existe') == {'sucesso': True, 'pagamentos': []}


def test_buscar_pagamentos_por_referencia_falha_de_transporte(mp_fake):
    def _levanta(filters):
        raise requests.exceptions.ConnectionError('sem rede')

    mp_fake['search'] = _levanta

    with pytest.raises(MercadoPagoIndisponivel):
        mercado_pago.buscar_pagamentos_por_referencia('checkout-1-abc')


def test_buscar_pagamento_expoe_meio_de_pagamento_e_moeda(mp_fake):
    mp_fake['get'] = {'status': 200, 'response': {
        'id': 42, 'status': 'approved', 'transaction_amount': 150.0, 'currency_id': 'BRL',
        'payment_type_id': 'ticket', 'payment_method_id': 'bolbradesco',
    }}

    resultado = mercado_pago.buscar_pagamento('42')

    assert resultado['payment_id'] == '42'
    assert resultado['currency_id'] == 'BRL'
    assert resultado['payment_type_id'] == 'ticket'
