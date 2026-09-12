"""Limites de pagamento por conta, com o provedor inteiramente simulado."""

from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest

import blueprints.checkout_bp as checkout_bp
import blueprints.pix_bp as pix_bp
from config import db


JSON = {'Accept': 'application/json'}


# As rotas protegidas conferem a credencial carimbada no login (servicos/autorizacao.py),
# então a sessão montada à mão precisa carregá-la como o login real carrega.
def _sessao_aluno(cliente, aluno):
    from servicos.autorizacao import impressao_credencial

    with cliente.session_transaction() as sessao:
        sessao['usuario'] = aluno.login
        sessao['tipo_usuario'] = 'aluno'
        sessao['aluno_id'] = aluno.id
        sessao['credencial'] = impressao_credencial(aluno.senha_hash)


def _sessao_admin(cliente, usuario):
    from servicos.autorizacao import impressao_credencial
    from servicos.credenciais import referencia_credencial_admin

    with cliente.session_transaction() as sessao:
        sessao['usuario'] = usuario
        sessao['tipo_usuario'] = 'admin'
        sessao['credencial'] = impressao_credencial(referencia_credencial_admin())


@pytest.fixture
def consultar_mp(monkeypatch):
    consulta = Mock(return_value={'sucesso': True, 'status': 'pending'})
    monkeypatch.setattr(pix_bp, 'buscar_pagamento', consulta)
    return consulta


def test_status_bloqueia_31a_consulta_antes_do_provedor(
    client, criar_pagamento, logar_como_aluno, consultar_mp,
):
    pagamento = criar_pagamento(provider_payment_id='mp-teste')
    logar_como_aluno(pagamento.aluno)
    url = f'/api/mensalidades/{pagamento.id}/status'

    for _ in range(30):
        assert client.get(url).status_code == 200
    resposta = client.get(url)

    assert resposta.status_code == 429
    assert resposta.is_json
    assert resposta.get_json() == {
        'erro': 'Muitas tentativas. Aguarde alguns minutos e tente novamente.',
    }
    assert resposta.headers['Retry-After'] == '60'
    assert consultar_mp.call_count == 30


def test_alunos_no_mesmo_ip_tem_limites_separados(
    app, client, criar_pagamento, logar_como_aluno, consultar_mp,
):
    primeiro = criar_pagamento(provider_payment_id='mp-primeiro')
    segundo = criar_pagamento(provider_payment_id='mp-segundo')
    logar_como_aluno(primeiro.aluno)
    url = f'/api/mensalidades/{primeiro.id}/status'
    for _ in range(30):
        assert client.get(url).status_code == 200
    assert client.get(url).status_code == 429

    outro_cliente = app.test_client()
    _sessao_aluno(outro_cliente, segundo.aluno)
    assert outro_cliente.get(f'/api/mensalidades/{segundo.id}/status').status_code == 200
    assert consultar_mp.call_count == 31


def test_nova_sessao_e_outra_mensalidade_nao_renovam_limite_da_conta(
    app, client, criar_pagamento, logar_como_aluno, consultar_mp,
):
    primeiro = criar_pagamento(provider_payment_id='mp-primeiro')
    segundo = criar_pagamento(aluno=primeiro.aluno, provider_payment_id='mp-segundo')
    logar_como_aluno(primeiro.aluno)
    for _ in range(30):
        assert client.get(f'/api/mensalidades/{primeiro.id}/status').status_code == 200

    outro_cliente = app.test_client()
    _sessao_aluno(outro_cliente, primeiro.aluno)
    with outro_cliente.session_transaction() as sessao:
        sessao['csrf_token'] = 'outra-sessao'
    resposta = outro_cliente.get(f'/api/mensalidades/{segundo.id}/status')

    assert resposta.status_code == 429
    assert consultar_mp.call_count == 30


def test_admin_limite_por_usuario_persiste_entre_sessoes(
    app, client, criar_pagamento, consultar_mp,
):
    pagamento = criar_pagamento(provider_payment_id='mp-teste')
    _sessao_admin(client, 'admin-um')
    url = f'/api/mensalidades/{pagamento.id}/status'
    for _ in range(30):
        assert client.get(url).status_code == 200

    nova_sessao = app.test_client()
    _sessao_admin(nova_sessao, 'admin-um')
    assert nova_sessao.get(url).status_code == 429
    outro_admin = app.test_client()
    _sessao_admin(outro_admin, 'admin-dois')
    assert outro_admin.get(url).status_code == 200
    assert consultar_mp.call_count == 31


@pytest.mark.parametrize('primeiro', ['pix', 'checkout'])
def test_criacao_pix_e_checkout_compartilham_dez_tentativas(
    client, criar_pagamento, logar_como_aluno, monkeypatch, consultar_mp, primeiro,
):
    pagamento = criar_pagamento()
    logar_como_aluno(pagamento.aluno)
    criar_pix = Mock(return_value={
        'sucesso': True, 'payment_id': 'mp-criado', 'status': 'pending',
        'qr_code': 'copia-e-cola', 'qr_code_base64': None, 'ticket_url': None,
        'data_expiracao': datetime.utcnow() + timedelta(minutes=30),
    })
    criar_checkout = Mock(return_value={
        'sucesso': True, 'preference_id': 'pref-teste',
        'url_checkout': 'https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=pref-teste',
        'ambiente': 'producao', 'expira_em': datetime.utcnow() + timedelta(minutes=30),
    })
    monkeypatch.setattr(pix_bp, 'criar_pagamento_pix', criar_pix)
    monkeypatch.setattr(checkout_bp, 'criar_preferencia_checkout', criar_checkout)
    monkeypatch.setattr(checkout_bp, 'ambiente_mercado_pago', lambda: 'producao')
    urls = {
        'pix': f'/api/mensalidades/{pagamento.id}/pix',
        'checkout': f'/perfil/mensalidade/{pagamento.id}/checkout',
    }
    segundo = 'checkout' if primeiro == 'pix' else 'pix'
    for meio in [primeiro, segundo] * 5:
        assert client.post(urls[meio], headers=JSON).status_code == 200

    consultas_antes = consultar_mp.call_count
    for meio in (primeiro, segundo):
        resposta = client.post(urls[meio], headers=JSON)
        assert resposta.status_code == 429
        assert resposta.is_json
        assert 'erro' in resposta.get_json()
    assert criar_pix.call_count == 1
    assert criar_checkout.call_count == 1
    assert consultar_mp.call_count == consultas_antes


def test_status_e_retorno_checkout_compartilham_consultas(
    client, criar_pagamento, logar_como_aluno, monkeypatch,
):
    pagamento = criar_pagamento()
    pagamento.checkout_external_reference = 'checkout-teste'
    db.session.commit()
    logar_como_aluno(pagamento.aluno)
    consulta = Mock(return_value={'sucesso': True, 'pagamentos': []})
    monkeypatch.setattr(pix_bp, 'buscar_pagamentos_por_referencia', consulta)
    status = f'/api/mensalidades/{pagamento.id}/status'
    retorno = f'/perfil/mensalidade/{pagamento.id}/retorno-checkout'
    for url in [status, retorno] * 15:
        assert client.get(url).status_code == 200

    assert client.get(status).status_code == 429
    resposta = client.get(retorno)
    assert resposta.status_code == 429
    assert resposta.mimetype == 'text/html'
    assert 'Muitas tentativas.' in resposta.get_data(as_text=True)
    assert '<form' not in resposta.get_data(as_text=True)
    assert consulta.call_count == 30


def test_sincronizacao_admin_compartilha_limite_das_consultas(
    client, criar_pagamento, logar_como_admin, consultar_mp,
):
    pagamento = criar_pagamento(provider_payment_id='mp-teste')
    logar_como_admin()
    for _ in range(30):
        assert client.get(f'/api/mensalidades/{pagamento.id}/status').status_code == 200

    resposta = client.post(f'/admin/pagamentos/{pagamento.id}/sincronizar')
    assert resposta.status_code == 429
    assert '<form' not in resposta.get_data(as_text=True)
    assert consultar_mp.call_count == 30


def test_checkout_formulario_limitado_nao_exibe_login(
    client, criar_pagamento, logar_como_aluno,
):
    pagamento = criar_pagamento(status='pago')
    logar_como_aluno(pagamento.aluno)
    url = f'/perfil/mensalidade/{pagamento.id}/checkout'
    for _ in range(10):
        assert client.post(url, headers=JSON).status_code == 409

    resposta = client.post(url)
    assert resposta.status_code == 429
    html = resposta.get_data(as_text=True)
    assert 'Muitas tentativas.' in html
    assert '<form' not in html
    assert '10 per' not in html
    assert pagamento.aluno.login not in html


def test_anonimos_limitados_por_ip_sem_consultar_provedor(
    app, client, criar_pagamento, consultar_mp,
):
    pagamento = criar_pagamento(provider_payment_id='mp-teste')
    url = f'/api/mensalidades/{pagamento.id}/status'
    for _ in range(30):
        assert client.get(url).status_code == 401
    assert app.test_client().get(url).status_code == 429
    assert app.test_client().get(url, environ_overrides={'REMOTE_ADDR': '192.0.2.2'}).status_code == 401
    consultar_mp.assert_not_called()


@pytest.mark.parametrize('meio', ['pix', 'checkout'])
def test_limite_nao_substitui_csrf_nem_autorizacao(
    app, client, criar_pagamento, criar_aluno, logar_como_aluno, monkeypatch, meio,
):
    pagamento = criar_pagamento()
    url = (f'/api/mensalidades/{pagamento.id}/pix' if meio == 'pix'
           else f'/perfil/mensalidade/{pagamento.id}/checkout')
    criar_pix = Mock()
    criar_checkout = Mock()
    monkeypatch.setattr(pix_bp, 'criar_pagamento_pix', criar_pix)
    monkeypatch.setattr(checkout_bp, 'criar_preferencia_checkout', criar_checkout)

    assert client.post(url, headers=JSON).status_code == 401
    logar_como_aluno(criar_aluno())
    assert client.post(url, headers=JSON).status_code == 403
    logar_como_aluno(pagamento.aluno)
    monkeypatch.setitem(app.config, 'WTF_CSRF_ENABLED', True)
    assert client.post(url, headers=JSON).status_code == 400
    criar_pix.assert_not_called()
    criar_checkout.assert_not_called()
