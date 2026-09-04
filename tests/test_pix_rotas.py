import hashlib
import hmac
import os
import time
from datetime import datetime, timedelta
from decimal import Decimal

import blueprints.pix_bp as pix_bp
from dao.financeiroDAO import PagamentoDAO
from servicos.mercado_pago import MercadoPagoIndisponivel


def _resposta_criacao(payment_id='mp-1', status='pending'):
    return {
        'sucesso': True,
        'payment_id': payment_id,
        'status': status,
        'qr_code': '00020126-copia-cola',
        'qr_code_base64': 'YmFzZTY0',
        'ticket_url': 'https://mp.example/ticket',
        'data_expiracao': None,
    }


def _resposta_consulta(status='pending', external_reference=None, transaction_amount=None):
    return {
        'sucesso': True,
        'status': status,
        'status_detail': f'{status}_detail',
        'external_reference': external_reference,
        'transaction_amount': transaction_amount,
        'date_approved': '2026-08-25T10:00:00.000-03:00' if status == 'approved' else None,
        'qr_code': None,
        'qr_code_base64': None,
        'ticket_url': None,
    }


def _assinar(data_id, secret, request_id='req-1', ts=None):
    ts = ts or str(int(time.time()))
    manifest = f'id:{str(data_id).lower()};request-id:{request_id};ts:{ts};'
    v1 = hmac.new(secret.encode(), manifest.encode(), hashlib.sha256).hexdigest()
    return {'x-signature': f'ts={ts},v1={v1}', 'x-request-id': request_id}


# ---------------------------------------------------------------------------
# POST /api/mensalidades/<id>/pix
# ---------------------------------------------------------------------------

def test_aluno_gera_pix_da_propria_mensalidade(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento()
    logar_como_aluno(pagamento.aluno)

    chamadas = []
    monkeypatch.setattr(pix_bp, 'criar_pagamento_pix', lambda **kw: chamadas.append(kw) or _resposta_criacao())

    resp = client.post(f'/api/mensalidades/{pagamento.id}/pix')

    assert resp.status_code == 200
    corpo = resp.get_json()
    assert corpo['status'] == 'pendente'
    assert corpo['qr_code_base64'] == 'YmFzZTY0'
    assert len(chamadas) == 1
    assert chamadas[0]['valor'] == Decimal('150.00')  # valor sempre vem do banco

    atualizado = PagamentoDAO.buscar_por_id(pagamento.id)
    assert atualizado.provider == 'mercado_pago'
    assert atualizado.provider_payment_id == 'mp-1'


def test_aluno_nao_acessa_mensalidade_de_outro_aluno(client, criar_pagamento, criar_aluno, logar_como_aluno):
    pagamento = criar_pagamento()
    outro_aluno = criar_aluno()
    logar_como_aluno(outro_aluno)

    resp = client.post(f'/api/mensalidades/{pagamento.id}/pix')

    assert resp.status_code == 403


def test_sem_sessao_retorna_401(client, criar_pagamento):
    pagamento = criar_pagamento()
    resp = client.post(f'/api/mensalidades/{pagamento.id}/pix')
    assert resp.status_code == 401


def test_mensalidade_ja_paga_retorna_409(client, criar_pagamento, logar_como_aluno):
    pagamento = criar_pagamento(status='pago')
    logar_como_aluno(pagamento.aluno)
    resp = client.post(f'/api/mensalidades/{pagamento.id}/pix')
    assert resp.status_code == 409


def test_reutiliza_cobranca_pendente_valida(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento(
        provider='mercado_pago', provider_payment_id='mp-existente',
        external_reference='mensalidade-x', idempotency_key='chave-existente',
        pix_copia_cola='codigo-existente', ticket_url='https://mp.example/ticket-existente',
        data_expiracao=datetime.utcnow() + timedelta(minutes=20),
    )
    logar_como_aluno(pagamento.aluno)

    chamadas_create = []
    monkeypatch.setattr(pix_bp, 'criar_pagamento_pix', lambda **kw: chamadas_create.append(kw) or _resposta_criacao())
    monkeypatch.setattr(
        pix_bp, 'buscar_pagamento',
        lambda payment_id: _resposta_consulta(status='pending', external_reference='mensalidade-x', transaction_amount=150.0),
    )

    resp = client.post(f'/api/mensalidades/{pagamento.id}/pix')

    assert resp.status_code == 200
    assert len(chamadas_create) == 0  # nao criou uma nova cobranca - reaproveitou a existente
    assert resp.get_json()['pix_copia_cola'] == 'codigo-existente'


def test_impede_cobranca_duplicada_em_chamadas_consecutivas(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento()
    logar_como_aluno(pagamento.aluno)

    chamadas_create = []
    monkeypatch.setattr(
        pix_bp, 'criar_pagamento_pix',
        lambda **kw: chamadas_create.append(kw) or _resposta_criacao(payment_id='mp-unico'),
    )
    monkeypatch.setattr(
        pix_bp, 'buscar_pagamento',
        lambda payment_id: _resposta_consulta(status='pending', transaction_amount=150.0),
    )

    primeira = client.post(f'/api/mensalidades/{pagamento.id}/pix')
    segunda = client.post(f'/api/mensalidades/{pagamento.id}/pix')

    assert primeira.status_code == 200
    assert segunda.status_code == 200
    assert len(chamadas_create) == 1  # a segunda chamada reaproveitou, nao criou de novo


def test_admin_tambem_pode_gerar_pix(client, criar_pagamento, monkeypatch, logar_como_admin):
    pagamento = criar_pagamento()
    logar_como_admin()
    monkeypatch.setattr(pix_bp, 'criar_pagamento_pix', lambda **kw: _resposta_criacao())

    resp = client.post(f'/api/mensalidades/{pagamento.id}/pix')
    assert resp.status_code == 200


def test_falha_de_indisponibilidade_do_mp_retorna_503(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento()
    logar_como_aluno(pagamento.aluno)

    def _fake_criar(**kwargs):
        raise MercadoPagoIndisponivel('fora do ar')

    monkeypatch.setattr(pix_bp, 'criar_pagamento_pix', _fake_criar)

    resp = client.post(f'/api/mensalidades/{pagamento.id}/pix')
    assert resp.status_code == 503


# ---------------------------------------------------------------------------
# GET /api/mensalidades/<id>/status
# ---------------------------------------------------------------------------

def test_status_nao_bate_no_mp_quando_ja_fechado(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento(status='pago')
    logar_como_aluno(pagamento.aluno)

    chamadas = []
    monkeypatch.setattr(pix_bp, 'buscar_pagamento', lambda payment_id: chamadas.append(payment_id) or _resposta_consulta())

    resp = client.get(f'/api/mensalidades/{pagamento.id}/status')

    assert resp.status_code == 200
    assert resp.get_json()['status'] == 'pago'
    assert len(chamadas) == 0


# ---------------------------------------------------------------------------
# POST /api/webhooks/mercado-pago
# ---------------------------------------------------------------------------

def test_webhook_processa_aprovado(client, criar_pagamento, monkeypatch):
    pagamento = criar_pagamento(provider='mercado_pago', provider_payment_id='mp-1', external_reference='ref-1', valor=150.0)
    secret = os.environ['MERCADO_PAGO_WEBHOOK_SECRET']

    monkeypatch.setattr(
        pix_bp, 'buscar_pagamento',
        lambda payment_id: _resposta_consulta(status='approved', external_reference='ref-1', transaction_amount=150.0),
    )

    headers = _assinar('mp-1', secret)
    resp = client.post('/api/webhooks/mercado-pago?data.id=mp-1', headers=headers,
                        json={'type': 'payment', 'data': {'id': 'mp-1'}})

    assert resp.status_code == 200
    atualizado = PagamentoDAO.buscar_por_id(pagamento.id)
    assert atualizado.status == 'pago'
    assert atualizado.aluno.mensalidade == 'Em Dia'


def test_webhook_rejeita_assinatura_invalida(client, criar_pagamento):
    pagamento = criar_pagamento(provider='mercado_pago', provider_payment_id='mp-1', external_reference='ref-1')

    resp = client.post(
        '/api/webhooks/mercado-pago?data.id=mp-1',
        headers={'x-signature': 'ts=123,v1=assinaturainvalida', 'x-request-id': 'req-1'},
        json={'type': 'payment', 'data': {'id': 'mp-1'}},
    )

    assert resp.status_code == 401
    atualizado = PagamentoDAO.buscar_por_id(pagamento.id)
    assert atualizado.status == 'pendente'


def test_webhook_nao_aprova_pagamento_pendente(client, criar_pagamento, monkeypatch):
    pagamento = criar_pagamento(provider='mercado_pago', provider_payment_id='mp-1', external_reference='ref-1', valor=150.0)
    secret = os.environ['MERCADO_PAGO_WEBHOOK_SECRET']

    monkeypatch.setattr(
        pix_bp, 'buscar_pagamento',
        lambda payment_id: _resposta_consulta(status='pending', external_reference='ref-1', transaction_amount=150.0),
    )

    headers = _assinar('mp-1', secret)
    resp = client.post('/api/webhooks/mercado-pago?data.id=mp-1', headers=headers,
                        json={'type': 'payment', 'data': {'id': 'mp-1'}})

    assert resp.status_code == 200
    atualizado = PagamentoDAO.buscar_por_id(pagamento.id)
    assert atualizado.status == 'pendente'


def test_webhook_rejeita_divergencia_de_valor(client, criar_pagamento, monkeypatch):
    pagamento = criar_pagamento(provider='mercado_pago', provider_payment_id='mp-1', external_reference='ref-1', valor=150.0)
    secret = os.environ['MERCADO_PAGO_WEBHOOK_SECRET']

    monkeypatch.setattr(
        pix_bp, 'buscar_pagamento',
        lambda payment_id: _resposta_consulta(status='approved', external_reference='ref-1', transaction_amount=1.0),
    )

    headers = _assinar('mp-1', secret)
    resp = client.post('/api/webhooks/mercado-pago?data.id=mp-1', headers=headers,
                        json={'type': 'payment', 'data': {'id': 'mp-1'}})

    assert resp.status_code == 200
    atualizado = PagamentoDAO.buscar_por_id(pagamento.id)
    assert atualizado.status == 'pendente'  # divergencia de valor - nao aprova


def test_webhook_repetido_e_idempotente(client, criar_pagamento, monkeypatch):
    pagamento = criar_pagamento(status='pago', provider='mercado_pago', provider_payment_id='mp-1', external_reference='ref-1')
    secret = os.environ['MERCADO_PAGO_WEBHOOK_SECRET']

    chamadas = []
    monkeypatch.setattr(pix_bp, 'buscar_pagamento', lambda payment_id: chamadas.append(payment_id) or _resposta_consulta(status='approved'))

    headers = _assinar('mp-1', secret)
    resp = client.post('/api/webhooks/mercado-pago?data.id=mp-1', headers=headers,
                        json={'type': 'payment', 'data': {'id': 'mp-1'}})

    assert resp.status_code == 200
    assert len(chamadas) == 0  # ja estava pago com o mesmo provider_payment_id - nem consulta o MP de novo


def test_webhook_processa_em_processamento(client, criar_pagamento, monkeypatch):
    pagamento = criar_pagamento(provider='mercado_pago', provider_payment_id='mp-1', external_reference='ref-1', valor=150.0)
    secret = os.environ['MERCADO_PAGO_WEBHOOK_SECRET']

    monkeypatch.setattr(
        pix_bp, 'buscar_pagamento',
        lambda payment_id: _resposta_consulta(status='in_process', external_reference='ref-1', transaction_amount=150.0),
    )

    headers = _assinar('mp-1', secret)
    resp = client.post('/api/webhooks/mercado-pago?data.id=mp-1', headers=headers,
                        json={'type': 'payment', 'data': {'id': 'mp-1'}})

    assert resp.status_code == 200
    atualizado = PagamentoDAO.buscar_por_id(pagamento.id)
    assert atualizado.status == 'em_processamento'


def test_webhook_processa_recusado_e_permite_nova_tentativa(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento(provider='mercado_pago', provider_payment_id='mp-1', external_reference='ref-1', valor=150.0)
    secret = os.environ['MERCADO_PAGO_WEBHOOK_SECRET']

    monkeypatch.setattr(
        pix_bp, 'buscar_pagamento',
        lambda payment_id: _resposta_consulta(status='rejected', external_reference='ref-1', transaction_amount=150.0),
    )

    headers = _assinar('mp-1', secret)
    resp = client.post('/api/webhooks/mercado-pago?data.id=mp-1', headers=headers,
                        json={'type': 'payment', 'data': {'id': 'mp-1'}})

    assert resp.status_code == 200
    atualizado = PagamentoDAO.buscar_por_id(pagamento.id)
    assert atualizado.status == 'recusado'

    # 'recusado' entra em STATUS_PAGAVEIS - o aluno consegue gerar uma nova cobranca.
    logar_como_aluno(atualizado.aluno)
    monkeypatch.setattr(pix_bp, 'criar_pagamento_pix', lambda **kw: _resposta_criacao(payment_id='mp-2'))
    monkeypatch.setattr(pix_bp, 'cancelar_pagamento', lambda payment_id: None)
    resp_retry = client.post(f'/api/mensalidades/{atualizado.id}/pix')
    assert resp_retry.status_code == 200


def test_webhook_falha_indisponibilidade_mp(client, criar_pagamento, monkeypatch):
    pagamento = criar_pagamento(provider='mercado_pago', provider_payment_id='mp-1', external_reference='ref-1')
    secret = os.environ['MERCADO_PAGO_WEBHOOK_SECRET']

    def _fake_buscar(payment_id):
        raise MercadoPagoIndisponivel('fora do ar')

    monkeypatch.setattr(pix_bp, 'buscar_pagamento', _fake_buscar)

    headers = _assinar('mp-1', secret)
    resp = client.post('/api/webhooks/mercado-pago?data.id=mp-1', headers=headers,
                        json={'type': 'payment', 'data': {'id': 'mp-1'}})

    assert resp.status_code == 503
    atualizado = PagamentoDAO.buscar_por_id(pagamento.id)
    assert atualizado.status == 'pendente'
