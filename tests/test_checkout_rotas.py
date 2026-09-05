"""Rotas do Checkout Pro ("outras formas de pagamento").

Nenhum teste aqui fala com a API real do Mercado Pago - o serviço é sempre mockado.
"""
import hashlib
import hmac
import os
import time

import pytest
from datetime import datetime, timedelta
from decimal import Decimal

import blueprints.checkout_bp as checkout_bp
import blueprints.pix_bp as pix_bp
from dao.financeiroDAO import PagamentoDAO
from servicos.mercado_pago import ConfiguracaoInvalida, MercadoPagoIndisponivel

URL_MP = 'https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=pref-1'


def _resposta_preferencia(preference_id='pref-1', url=URL_MP, ambiente='producao', minutos=60):
    return {
        'sucesso': True,
        'preference_id': preference_id,
        'url_checkout': url,
        'ambiente': ambiente,
        'expira_em': datetime.utcnow() + timedelta(minutes=minutos),
    }


def _pagamento_mp(status='approved', external_reference='checkout-ref', valor=150.0,
                   payment_id='mp-checkout-1', payment_type_id='credit_card',
                   payment_method_id='master', currency_id='BRL'):
    return {
        'payment_id': payment_id,
        'status': status,
        'status_detail': f'{status}_detail',
        'external_reference': external_reference,
        'transaction_amount': valor,
        'currency_id': currency_id,
        'payment_method_id': payment_method_id,
        'payment_type_id': payment_type_id,
        'date_approved': '2026-09-04T10:00:00.000-03:00' if status == 'approved' else None,
        'qr_code': None,
        'qr_code_base64': None,
        'ticket_url': None,
    }


def _assinar(data_id, secret, request_id='req-1', ts=None):
    ts = ts or str(int(time.time()))
    manifest = f'id:{str(data_id).lower()};request-id:{request_id};ts:{ts};'
    v1 = hmac.new(secret.encode(), manifest.encode(), hashlib.sha256).hexdigest()
    return {'x-signature': f'ts={ts},v1={v1}', 'x-request-id': request_id}


def _mockar_preferencia(monkeypatch, resposta=None, chamadas=None, ambiente='producao'):
    resposta = resposta if resposta is not None else _resposta_preferencia(ambiente=ambiente)

    def _criar(**kwargs):
        if chamadas is not None:
            chamadas.append(kwargs)
        return resposta() if callable(resposta) else resposta

    monkeypatch.setattr(checkout_bp, 'criar_preferencia_checkout', _criar)
    monkeypatch.setattr(checkout_bp, 'ambiente_mercado_pago', lambda: ambiente)


# ---------------------------------------------------------------------------
# POST /perfil/mensalidade/<id>/checkout
# ---------------------------------------------------------------------------

def test_aluno_cria_checkout_da_propria_mensalidade(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento()
    logar_como_aluno(pagamento.aluno)

    chamadas = []
    _mockar_preferencia(monkeypatch, chamadas=chamadas)

    resp = client.post(f'/perfil/mensalidade/{pagamento.id}/checkout')

    assert resp.status_code == 303
    assert resp.headers['Location'] == URL_MP
    assert len(chamadas) == 1

    atualizado = PagamentoDAO.buscar_por_id(pagamento.id)
    assert atualizado.provider == 'mercado_pago'
    assert atualizado.checkout_preference_id == 'pref-1'
    assert atualizado.checkout_url == URL_MP
    assert atualizado.checkout_ambiente == 'producao'
    # A referência do Checkout Pro é própria e não sobrescreve a do Pix direto.
    assert atualizado.checkout_external_reference.startswith(f'checkout-{pagamento.id}-')
    assert atualizado.external_reference is None
    assert atualizado.provider_payment_id is None
    assert atualizado.status == 'pendente'  # criar preferência nunca muda o status


def test_valor_vem_sempre_do_banco_e_nao_do_formulario(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento(valor=150.0)
    logar_como_aluno(pagamento.aluno)

    chamadas = []
    _mockar_preferencia(monkeypatch, chamadas=chamadas)

    resp = client.post(f'/perfil/mensalidade/{pagamento.id}/checkout',
                        data={'valor': '1.00', 'unit_price': '0.01'})

    assert resp.status_code == 303
    assert Decimal(str(chamadas[0]['valor'])) == Decimal('150.00')


def test_referencia_do_checkout_nao_e_previsivel(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento()
    logar_como_aluno(pagamento.aluno)
    chamadas = []
    _mockar_preferencia(monkeypatch, chamadas=chamadas)

    client.post(f'/perfil/mensalidade/{pagamento.id}/checkout')

    referencia = chamadas[0]['external_reference']
    assert referencia != str(pagamento.id)
    assert referencia != f'checkout-{pagamento.id}'
    assert len(referencia) > len(f'checkout-{pagamento.id}-') + 10


def test_aluno_nao_cria_checkout_de_mensalidade_de_outro_aluno(client, criar_pagamento, criar_aluno,
                                                                monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento()
    logar_como_aluno(criar_aluno())

    chamadas = []
    _mockar_preferencia(monkeypatch, chamadas=chamadas)

    resp = client.post(f'/perfil/mensalidade/{pagamento.id}/checkout')

    assert resp.status_code == 403
    assert chamadas == []
    assert PagamentoDAO.buscar_por_id(pagamento.id).checkout_preference_id is None


def test_sem_sessao_vai_para_o_login(client, criar_pagamento, monkeypatch):
    pagamento = criar_pagamento()
    chamadas = []
    _mockar_preferencia(monkeypatch, chamadas=chamadas)

    resp = client.post(f'/perfil/mensalidade/{pagamento.id}/checkout')

    assert resp.status_code == 302
    assert '/login' in resp.headers['Location']
    assert chamadas == []


def test_admin_tambem_pode_abrir_checkout(client, criar_pagamento, monkeypatch, logar_como_admin):
    pagamento = criar_pagamento()
    logar_como_admin()
    _mockar_preferencia(monkeypatch)

    resp = client.post(f'/perfil/mensalidade/{pagamento.id}/checkout')

    assert resp.status_code == 303


def test_mensalidade_paga_nao_cria_preferencia(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento(status='pago')
    logar_como_aluno(pagamento.aluno)

    chamadas = []
    _mockar_preferencia(monkeypatch, chamadas=chamadas)

    resp = client.post(f'/perfil/mensalidade/{pagamento.id}/checkout')

    assert resp.status_code == 302
    assert '/perfil/pagamento/' in resp.headers['Location']
    assert chamadas == []
    assert PagamentoDAO.buscar_por_id(pagamento.id).checkout_preference_id is None


def test_reutiliza_preferencia_valida(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento(valor=150.0)
    logar_como_aluno(pagamento.aluno)
    PagamentoDAO.salvar_dados_checkout(
        pagamento, preference_id='pref-existente', external_reference='checkout-existente',
        url_checkout='https://mp.example/checkout-existente', ambiente='producao',
        expira_em=datetime.utcnow() + timedelta(minutes=30),
    )

    chamadas = []
    _mockar_preferencia(monkeypatch, chamadas=chamadas)

    resp = client.post(f'/perfil/mensalidade/{pagamento.id}/checkout')

    assert resp.status_code == 303
    assert resp.headers['Location'] == 'https://mp.example/checkout-existente'
    assert chamadas == []  # reaproveitou, não criou outra cobrança no Mercado Pago


def test_clique_repetido_nao_gera_duas_preferencias(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento()
    logar_como_aluno(pagamento.aluno)

    chamadas = []
    _mockar_preferencia(monkeypatch, chamadas=chamadas)

    primeira = client.post(f'/perfil/mensalidade/{pagamento.id}/checkout')
    segunda = client.post(f'/perfil/mensalidade/{pagamento.id}/checkout')

    assert primeira.status_code == 303
    assert segunda.status_code == 303
    assert primeira.headers['Location'] == segunda.headers['Location']
    assert len(chamadas) == 1


def test_preferencia_expirada_gera_uma_nova(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento()
    logar_como_aluno(pagamento.aluno)
    PagamentoDAO.salvar_dados_checkout(
        pagamento, preference_id='pref-velha', external_reference='checkout-velha',
        url_checkout='https://mp.example/velha', ambiente='producao',
        expira_em=datetime.utcnow() - timedelta(minutes=1),
    )

    chamadas = []
    _mockar_preferencia(monkeypatch, chamadas=chamadas)

    resp = client.post(f'/perfil/mensalidade/{pagamento.id}/checkout')

    assert resp.status_code == 303
    assert resp.headers['Location'] == URL_MP
    assert len(chamadas) == 1
    assert PagamentoDAO.buscar_por_id(pagamento.id).checkout_preference_id == 'pref-1'


def test_valor_alterado_invalida_a_preferencia_anterior(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento(valor=150.0)
    logar_como_aluno(pagamento.aluno)
    PagamentoDAO.salvar_dados_checkout(
        pagamento, preference_id='pref-antiga', external_reference='checkout-antiga',
        url_checkout='https://mp.example/antiga', ambiente='producao',
        expira_em=datetime.utcnow() + timedelta(minutes=30),
    )
    # O admin reajusta a mensalidade: a preferência antiga cobraria o valor errado.
    pagamento.valor = Decimal('200.00')
    PagamentoDAO.salvar(pagamento)

    chamadas = []
    _mockar_preferencia(monkeypatch, chamadas=chamadas)

    resp = client.post(f'/perfil/mensalidade/{pagamento.id}/checkout')

    assert resp.status_code == 303
    assert len(chamadas) == 1
    assert Decimal(str(chamadas[0]['valor'])) == Decimal('200.00')


def test_ambiente_diferente_invalida_a_preferencia_anterior(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento()
    logar_como_aluno(pagamento.aluno)
    PagamentoDAO.salvar_dados_checkout(
        pagamento, preference_id='pref-sandbox', external_reference='checkout-sandbox',
        url_checkout='https://sandbox.mercadopago.com.br/checkout', ambiente='sandbox',
        expira_em=datetime.utcnow() + timedelta(minutes=30),
    )

    chamadas = []
    _mockar_preferencia(monkeypatch, chamadas=chamadas, ambiente='producao')

    resp = client.post(f'/perfil/mensalidade/{pagamento.id}/checkout')

    assert resp.status_code == 303
    assert len(chamadas) == 1
    assert PagamentoDAO.buscar_por_id(pagamento.id).checkout_ambiente == 'producao'


def test_mercado_pago_indisponivel_nao_persiste_nada(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento()
    logar_como_aluno(pagamento.aluno)

    def _falhar(**kwargs):
        raise MercadoPagoIndisponivel('fora do ar')

    monkeypatch.setattr(checkout_bp, 'criar_preferencia_checkout', _falhar)
    monkeypatch.setattr(checkout_bp, 'ambiente_mercado_pago', lambda: 'producao')

    resp = client.post(f'/perfil/mensalidade/{pagamento.id}/checkout', follow_redirects=True)

    assert resp.status_code == 200
    assert 'indisponível' in resp.get_data(as_text=True)
    assert PagamentoDAO.buscar_por_id(pagamento.id).checkout_preference_id is None


def test_recusa_do_mercado_pago_nao_vaza_mensagem_interna(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento()
    logar_como_aluno(pagamento.aluno)
    _mockar_preferencia(monkeypatch, resposta={'sucesso': False, 'erro': 'invalid_collector_id detail 4051'})

    resp = client.post(f'/perfil/mensalidade/{pagamento.id}/checkout', follow_redirects=True)

    corpo = resp.get_data(as_text=True)
    assert resp.status_code == 200
    assert 'invalid_collector_id' not in corpo
    assert 'Não foi possível abrir as outras formas de pagamento' in corpo
    assert PagamentoDAO.buscar_por_id(pagamento.id).checkout_preference_id is None


def test_configuracao_ausente_falha_de_forma_explicita(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento()
    logar_como_aluno(pagamento.aluno)

    def _sem_config(**kwargs):
        raise ConfiguracaoInvalida('APP_BASE_URL ausente ou invalida')

    monkeypatch.setattr(checkout_bp, 'criar_preferencia_checkout', _sem_config)
    monkeypatch.setattr(checkout_bp, 'ambiente_mercado_pago', lambda: 'producao')

    resp = client.post(f'/perfil/mensalidade/{pagamento.id}/checkout', follow_redirects=True)

    corpo = resp.get_data(as_text=True)
    assert 'Pagamento online indisponível' in corpo
    assert 'APP_BASE_URL' not in corpo  # detalhe técnico fica só no log do servidor
    assert PagamentoDAO.buscar_por_id(pagamento.id).checkout_preference_id is None


def test_aluno_sem_email_recebe_orientacao(client, criar_pagamento, criar_aluno, monkeypatch, logar_como_aluno):
    aluno = criar_aluno(email='')
    pagamento = criar_pagamento(aluno=aluno)
    logar_como_aluno(aluno)

    chamadas = []
    _mockar_preferencia(monkeypatch, chamadas=chamadas)

    resp = client.post(f'/perfil/mensalidade/{pagamento.id}/checkout', follow_redirects=True)

    assert 'e-mail válido' in resp.get_data(as_text=True)
    assert chamadas == []


# ---------------------------------------------------------------------------
# GET /perfil/mensalidade/<id>/retorno-checkout
# ---------------------------------------------------------------------------

def _preparar_retorno(pagamento, referencia='checkout-ref'):
    PagamentoDAO.salvar_dados_checkout(
        pagamento, preference_id='pref-1', external_reference=referencia,
        url_checkout=URL_MP, ambiente='producao',
        expira_em=datetime.utcnow() + timedelta(minutes=30),
    )


def test_retorno_de_sucesso_nao_marca_pago_sem_confirmacao(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento()
    logar_como_aluno(pagamento.aluno)
    _preparar_retorno(pagamento)

    # O Mercado Pago diz que ainda está pendente; a URL de retorno mente dizendo "approved".
    monkeypatch.setattr(
        pix_bp, 'buscar_pagamentos_por_referencia',
        lambda referencia, **kwargs: {'sucesso': True, 'pagamentos': [
            _pagamento_mp(status='pending', external_reference=referencia),
        ]},
    )

    resp = client.get(
        f'/perfil/mensalidade/{pagamento.id}/retorno-checkout'
        '?status=approved&collection_status=approved&payment_id=999&external_reference=checkout-ref'
    )

    corpo = resp.get_data(as_text=True)
    assert resp.status_code == 200
    assert 'Aguardando confirmação' in corpo
    assert 'Pagamento confirmado' not in corpo
    assert PagamentoDAO.buscar_por_id(pagamento.id).status == 'pendente'


def test_retorno_sem_nenhum_pagamento_no_mp_nao_muda_status(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento()
    logar_como_aluno(pagamento.aluno)
    _preparar_retorno(pagamento)

    monkeypatch.setattr(
        pix_bp, 'buscar_pagamentos_por_referencia',
        lambda referencia, **kwargs: {'sucesso': True, 'pagamentos': []},
    )

    resp = client.get(f'/perfil/mensalidade/{pagamento.id}/retorno-checkout?status=approved')

    assert resp.status_code == 200
    assert PagamentoDAO.buscar_por_id(pagamento.id).status == 'pendente'


def test_retorno_com_aprovacao_confirmada_marca_pago(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento(valor=150.0)
    logar_como_aluno(pagamento.aluno)
    _preparar_retorno(pagamento)

    monkeypatch.setattr(
        pix_bp, 'buscar_pagamentos_por_referencia',
        lambda referencia, **kwargs: {'sucesso': True, 'pagamentos': [
            _pagamento_mp(status='approved', external_reference=referencia, valor=150.0),
        ]},
    )

    resp = client.get(f'/perfil/mensalidade/{pagamento.id}/retorno-checkout')

    assert resp.status_code == 200
    assert 'Pagamento confirmado' in resp.get_data(as_text=True)
    atualizado = PagamentoDAO.buscar_por_id(pagamento.id)
    assert atualizado.status == 'pago'
    assert atualizado.provider_payment_id == 'mp-checkout-1'
    assert atualizado.forma_pagamento == 'cartao_credito'


def test_retorno_ignora_valor_divergente(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento(valor=150.0)
    logar_como_aluno(pagamento.aluno)
    _preparar_retorno(pagamento)

    monkeypatch.setattr(
        pix_bp, 'buscar_pagamentos_por_referencia',
        lambda referencia, **kwargs: {'sucesso': True, 'pagamentos': [
            _pagamento_mp(status='approved', external_reference=referencia, valor=1.0),
        ]},
    )

    client.get(f'/perfil/mensalidade/{pagamento.id}/retorno-checkout')

    assert PagamentoDAO.buscar_por_id(pagamento.id).status == 'pendente'


@pytest.mark.parametrize('campo_ausente', [
    'external_reference',
    'transaction_amount',
    'currency_id',
])
def test_retorno_nao_aprova_sem_campos_obrigatorios_de_conciliacao(
        client, criar_pagamento, monkeypatch, logar_como_aluno, campo_ausente):
    pagamento = criar_pagamento(valor=150.0)
    logar_como_aluno(pagamento.aluno)
    _preparar_retorno(pagamento)
    resposta_mp = _pagamento_mp(
        status='approved', external_reference='checkout-ref', valor=150.0,
    )
    resposta_mp[campo_ausente] = None

    monkeypatch.setattr(
        pix_bp, 'buscar_pagamentos_por_referencia',
        lambda referencia, **kwargs: {'sucesso': True, 'pagamentos': [resposta_mp]},
    )

    resposta = client.get(f'/perfil/mensalidade/{pagamento.id}/retorno-checkout')

    assert resposta.status_code == 200
    assert 'Pagamento confirmado' not in resposta.get_data(as_text=True)
    atualizado = PagamentoDAO.buscar_por_id(pagamento.id)
    assert atualizado.status == 'pendente'
    assert atualizado.provider_payment_id is None


def test_retorno_prioriza_aprovado_sobre_tentativa_recusada(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento(valor=150.0)
    logar_como_aluno(pagamento.aluno)
    _preparar_retorno(pagamento)

    monkeypatch.setattr(
        pix_bp, 'buscar_pagamentos_por_referencia',
        lambda referencia, **kwargs: {'sucesso': True, 'pagamentos': [
            _pagamento_mp(status='rejected', external_reference=referencia, payment_id='mp-recusado'),
            _pagamento_mp(status='approved', external_reference=referencia, payment_id='mp-aprovado'),
        ]},
    )

    client.get(f'/perfil/mensalidade/{pagamento.id}/retorno-checkout')

    atualizado = PagamentoDAO.buscar_por_id(pagamento.id)
    assert atualizado.status == 'pago'
    assert atualizado.provider_payment_id == 'mp-aprovado'


def test_retorno_com_mp_indisponivel_avisa_sem_mudar_status(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento()
    logar_como_aluno(pagamento.aluno)
    _preparar_retorno(pagamento)

    def _falhar(referencia, **kwargs):
        raise MercadoPagoIndisponivel('fora do ar')

    monkeypatch.setattr(pix_bp, 'buscar_pagamentos_por_referencia', _falhar)

    resp = client.get(f'/perfil/mensalidade/{pagamento.id}/retorno-checkout')

    assert resp.status_code == 200
    assert 'Não conseguimos confirmar agora' in resp.get_data(as_text=True)
    assert PagamentoDAO.buscar_por_id(pagamento.id).status == 'pendente'


def test_retorno_de_mensalidade_de_outro_aluno_e_bloqueado(client, criar_pagamento, criar_aluno, logar_como_aluno):
    pagamento = criar_pagamento()
    logar_como_aluno(criar_aluno())

    resp = client.get(f'/perfil/mensalidade/{pagamento.id}/retorno-checkout')

    assert resp.status_code == 403


def test_retorno_sem_sessao_vai_para_o_login(client, criar_pagamento):
    pagamento = criar_pagamento()
    resp = client.get(f'/perfil/mensalidade/{pagamento.id}/retorno-checkout')
    assert resp.status_code == 302
    assert '/login' in resp.headers['Location']


@pytest.mark.parametrize('status,trecho_esperado', [
    ('pendente', 'Aguardando confirmação'),
    ('atrasado', 'Aguardando confirmação'),
    ('em_processamento', 'Pagamento em análise'),
    ('em_analise', 'Comprovante em análise'),
    ('recusado', 'Pagamento recusado'),
    ('pago', 'Pagamento confirmado'),
    ('cancelado', 'não está mais disponível'),
    ('reembolsado', 'não está mais disponível'),
])
def test_retorno_tem_texto_proprio_para_cada_estado(client, criar_pagamento, monkeypatch,
                                                     logar_como_aluno, status, trecho_esperado):
    pagamento = criar_pagamento(status=status)
    logar_como_aluno(pagamento.aluno)
    _preparar_retorno(pagamento, referencia=f'checkout-{status}')

    # O Mercado Pago não tem nada novo a dizer: a tela mostra o estado já confirmado.
    monkeypatch.setattr(
        pix_bp, 'buscar_pagamentos_por_referencia',
        lambda referencia, **kwargs: {'sucesso': True, 'pagamentos': []},
    )

    resp = client.get(f'/perfil/mensalidade/{pagamento.id}/retorno-checkout')

    corpo = resp.get_data(as_text=True)
    assert resp.status_code == 200
    assert trecho_esperado in corpo
    # Só os estados ainda pagáveis reoferecem as duas formas de pagamento.
    tem_acao = f'/perfil/mensalidade/{pagamento.id}/checkout' in corpo
    assert tem_acao is (status in ('pendente', 'atrasado', 'recusado'))


def test_retorno_de_boleto_avisa_sobre_o_prazo(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento()
    logar_como_aluno(pagamento.aluno)
    _preparar_retorno(pagamento)

    monkeypatch.setattr(
        pix_bp, 'buscar_pagamentos_por_referencia',
        lambda referencia, **kwargs: {'sucesso': True, 'pagamentos': [
            _pagamento_mp(status='pending', external_reference=referencia,
                           payment_type_id='ticket', payment_method_id='bolbradesco'),
        ]},
    )

    corpo = client.get(f'/perfil/mensalidade/{pagamento.id}/retorno-checkout').get_data(as_text=True)

    assert 'boleto podem levar' in corpo
    assert 'não precisa pagar de novo' in corpo


# ---------------------------------------------------------------------------
# Webhook vindo do Checkout Pro
# ---------------------------------------------------------------------------

def test_webhook_encontra_mensalidade_por_referencia_do_checkout(client, criar_pagamento, monkeypatch):
    pagamento = criar_pagamento(valor=150.0)
    _preparar_retorno(pagamento, referencia='checkout-webhook-1')
    secret = os.environ['MERCADO_PAGO_WEBHOOK_SECRET']

    monkeypatch.setattr(
        pix_bp, 'buscar_pagamento',
        lambda payment_id, **kwargs: {'sucesso': True, **_pagamento_mp(
            status='approved', external_reference='checkout-webhook-1', valor=150.0,
            payment_id=payment_id, payment_type_id='ticket', payment_method_id='bolbradesco',
        )},
    )

    headers = _assinar('mp-boleto-9', secret)
    resp = client.post('/api/webhooks/mercado-pago?data.id=mp-boleto-9', headers=headers,
                        json={'type': 'payment', 'data': {'id': 'mp-boleto-9'}})

    assert resp.status_code == 200
    atualizado = PagamentoDAO.buscar_por_id(pagamento.id)
    assert atualizado.status == 'pago'
    assert atualizado.provider_payment_id == 'mp-boleto-9'  # id real do provedor persistido
    assert atualizado.forma_pagamento == 'boleto'
    assert atualizado.aluno.mensalidade == 'Em Dia'
    # A preferência não vira id de pagamento em nenhum momento.
    assert atualizado.checkout_preference_id == 'pref-1'


def test_webhook_do_checkout_com_referencia_inexistente_nao_afeta_ninguem(client, criar_pagamento, monkeypatch):
    pagamento = criar_pagamento()
    _preparar_retorno(pagamento, referencia='checkout-minha')
    secret = os.environ['MERCADO_PAGO_WEBHOOK_SECRET']

    monkeypatch.setattr(
        pix_bp, 'buscar_pagamento',
        lambda payment_id, **kwargs: {'sucesso': True, **_pagamento_mp(
            status='approved', external_reference='checkout-de-outro-sistema',
        )},
    )

    headers = _assinar('mp-desconhecido', secret)
    resp = client.post('/api/webhooks/mercado-pago?data.id=mp-desconhecido', headers=headers,
                        json={'type': 'payment', 'data': {'id': 'mp-desconhecido'}})

    assert resp.status_code == 200
    assert PagamentoDAO.buscar_por_id(pagamento.id).status == 'pendente'


def test_webhook_do_checkout_e_idempotente(client, criar_pagamento, monkeypatch):
    pagamento = criar_pagamento(valor=150.0)
    _preparar_retorno(pagamento, referencia='checkout-repetido')
    secret = os.environ['MERCADO_PAGO_WEBHOOK_SECRET']

    chamadas = []
    monkeypatch.setattr(
        pix_bp, 'buscar_pagamento',
        lambda payment_id, **kwargs: chamadas.append(payment_id) or {'sucesso': True, **_pagamento_mp(
            status='approved', external_reference='checkout-repetido', valor=150.0, payment_id=payment_id,
        )},
    )

    headers = _assinar('mp-repetido', secret)
    for _ in range(3):
        resp = client.post('/api/webhooks/mercado-pago?data.id=mp-repetido', headers=headers,
                            json={'type': 'payment', 'data': {'id': 'mp-repetido'}})
        assert resp.status_code == 200

    atualizado = PagamentoDAO.buscar_por_id(pagamento.id)
    assert atualizado.status == 'pago'
    # Só a primeira notificação chega a consultar o Mercado Pago; as repetidas param antes.
    assert len(chamadas) == 1
    eventos_aprovacao = [e for e in atualizado.eventos if e.tipo == 'webhook_aprovado']
    assert len(eventos_aprovacao) == 1


def test_webhook_recusado_depois_da_aprovacao_nao_rebaixa_a_mensalidade(client, criar_pagamento, monkeypatch):
    pagamento = criar_pagamento(valor=150.0, status='pago', provider='mercado_pago',
                                 provider_payment_id='mp-aprovado', forma_pagamento='cartao_credito')
    _preparar_retorno(pagamento, referencia='checkout-pago')
    secret = os.environ['MERCADO_PAGO_WEBHOOK_SECRET']

    monkeypatch.setattr(
        pix_bp, 'buscar_pagamento',
        lambda payment_id, **kwargs: {'sucesso': True, **_pagamento_mp(
            status='rejected', external_reference='checkout-pago', valor=150.0, payment_id=payment_id,
        )},
    )

    headers = _assinar('mp-tentativa-antiga', secret)
    resp = client.post('/api/webhooks/mercado-pago?data.id=mp-tentativa-antiga', headers=headers,
                        json={'type': 'payment', 'data': {'id': 'mp-tentativa-antiga'}})

    assert resp.status_code == 200
    atualizado = PagamentoDAO.buscar_por_id(pagamento.id)
    assert atualizado.status == 'pago'
    assert atualizado.provider_payment_id == 'mp-aprovado'  # id do pagamento que quitou não é sobrescrito


def test_webhook_do_checkout_recusa_moeda_diferente_de_brl(client, criar_pagamento, monkeypatch):
    pagamento = criar_pagamento(valor=150.0)
    _preparar_retorno(pagamento, referencia='checkout-moeda')
    secret = os.environ['MERCADO_PAGO_WEBHOOK_SECRET']

    monkeypatch.setattr(
        pix_bp, 'buscar_pagamento',
        lambda payment_id, **kwargs: {'sucesso': True, **_pagamento_mp(
            status='approved', external_reference='checkout-moeda', valor=150.0, currency_id='USD',
        )},
    )

    headers = _assinar('mp-usd', secret)
    resp = client.post('/api/webhooks/mercado-pago?data.id=mp-usd', headers=headers,
                        json={'type': 'payment', 'data': {'id': 'mp-usd'}})

    assert resp.status_code == 200
    assert PagamentoDAO.buscar_por_id(pagamento.id).status == 'pendente'


def test_webhook_do_checkout_com_assinatura_invalida_e_recusado(client, criar_pagamento, monkeypatch):
    pagamento = criar_pagamento(valor=150.0)
    _preparar_retorno(pagamento, referencia='checkout-assinatura')

    chamadas = []
    monkeypatch.setattr(pix_bp, 'buscar_pagamento', lambda payment_id, **kwargs: chamadas.append(payment_id))

    resp = client.post(
        '/api/webhooks/mercado-pago?data.id=mp-forjado',
        headers={'x-signature': 'ts=123,v1=assinaturainvalida', 'x-request-id': 'req-1'},
        json={'type': 'payment', 'data': {'id': 'mp-forjado'}},
    )

    assert resp.status_code == 401
    assert chamadas == []  # nem chega a consultar o Mercado Pago
    assert PagamentoDAO.buscar_por_id(pagamento.id).status == 'pendente'


# ---------------------------------------------------------------------------
# Convivência com o Pix direto
# ---------------------------------------------------------------------------

def test_pix_direto_nao_reaproveita_pagamento_do_checkout(client, criar_pagamento, monkeypatch,
                                                          logar_como_aluno):
    """Um boleto pendente do Checkout Pro grava provider_payment_id, mas não é Pix:
    clicar em "Pagar com Pix" tem de gerar uma cobrança Pix nova, não devolver uma
    cobrança sem copia-e-cola."""
    pagamento = criar_pagamento(provider='mercado_pago', provider_payment_id='mp-boleto-pendente')
    logar_como_aluno(pagamento.aluno)

    chamadas_create = []
    monkeypatch.setattr(
        pix_bp, 'criar_pagamento_pix',
        lambda **kw: chamadas_create.append(kw) or {
            'sucesso': True, 'payment_id': 'mp-pix-novo', 'status': 'pending',
            'qr_code': '00020126-novo', 'qr_code_base64': 'YmFzZTY0',
            'ticket_url': 'https://mp.example/ticket', 'data_expiracao': None,
        },
    )
    monkeypatch.setattr(pix_bp, 'cancelar_pagamento', lambda payment_id: None)

    resp = client.post(f'/api/mensalidades/{pagamento.id}/pix')

    assert resp.status_code == 200
    assert len(chamadas_create) == 1
    assert resp.get_json()['pix_copia_cola'] == '00020126-novo'


def test_status_consulta_o_checkout_mesmo_com_cobranca_pix_aberta(client, criar_pagamento,
                                                                   monkeypatch, logar_como_aluno):
    """Pix aberto e checkout concluído ao mesmo tempo: a consulta pelo provider_payment_id
    do Pix não enxerga o pagamento do checkout, então a busca por referência também roda."""
    pagamento = criar_pagamento(valor=150.0, provider='mercado_pago',
                                 provider_payment_id='mp-pix-aberto',
                                 external_reference='mensalidade-pix',
                                 pix_copia_cola='00020126-pix')
    logar_como_aluno(pagamento.aluno)
    _preparar_retorno(pagamento, referencia='checkout-paralelo')

    monkeypatch.setattr(
        pix_bp, 'buscar_pagamento',
        lambda payment_id, **kwargs: {'sucesso': True, **_pagamento_mp(
            status='pending', external_reference='mensalidade-pix', valor=150.0,
            payment_id=payment_id, payment_type_id='bank_transfer', payment_method_id='pix',
        )},
    )
    monkeypatch.setattr(
        pix_bp, 'buscar_pagamentos_por_referencia',
        lambda referencia, **kwargs: {'sucesso': True, 'pagamentos': [
            _pagamento_mp(status='approved', external_reference='checkout-paralelo',
                           valor=150.0, payment_id='mp-cartao-aprovado'),
        ]},
    )

    resp = client.get(f'/api/mensalidades/{pagamento.id}/status')

    assert resp.status_code == 200
    assert resp.get_json()['status'] == 'pago'
    atualizado = PagamentoDAO.buscar_por_id(pagamento.id)
    assert atualizado.provider_payment_id == 'mp-cartao-aprovado'
    assert atualizado.forma_pagamento == 'cartao_credito'


# ---------------------------------------------------------------------------
# Telas
# ---------------------------------------------------------------------------

def test_area_do_aluno_mostra_as_duas_acoes(client, criar_pagamento, logar_como_aluno):
    pagamento = criar_pagamento()
    logar_como_aluno(pagamento.aluno)

    corpo = client.get('/perfil').get_data(as_text=True)

    assert 'Pagar com Pix' in corpo
    assert 'Outras formas de pagamento' in corpo
    assert f'/perfil/mensalidade/{pagamento.id}/checkout' in corpo


def test_pagina_de_pagamento_mostra_a_acao_de_checkout(client, criar_pagamento, logar_como_aluno):
    pagamento = criar_pagamento()
    logar_como_aluno(pagamento.aluno)

    corpo = client.get(f'/perfil/pagamento/{pagamento.id}').get_data(as_text=True)

    assert 'Outras formas de pagamento' in corpo
    assert f'/perfil/mensalidade/{pagamento.id}/checkout' in corpo


def test_mensalidade_paga_nao_oferece_checkout_na_tela(client, criar_pagamento, logar_como_aluno):
    pagamento = criar_pagamento(status='pago')
    logar_como_aluno(pagamento.aluno)

    corpo = client.get('/perfil').get_data(as_text=True)

    assert f'/perfil/mensalidade/{pagamento.id}/checkout' not in corpo
    assert 'Ver comprovante' in corpo
