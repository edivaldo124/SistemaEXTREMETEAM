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


@pytest.fixture
def mp_fake(monkeypatch):
    estado = {'create': None, 'get': None, 'update': None, 'chamadas': []}

    class FakeSDK:
        def __init__(self, token=None, request_options=None):
            self.token = token

        def payment(self):
            return _FakePaymentResource(estado)

    monkeypatch.setattr(mercado_pago.mercadopago, 'SDK', FakeSDK)
    return estado


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
