"""Segundo fator do administrador (SEC-30).

Com ADMIN_TOTP_SECRET definida, a senha certa só leva à tela do código de 6 dígitos do app
autenticador, e só o código abre a sessão de admin. Cada código vale uma vez, a etapa tem
limite e vence em 5 minutos, e ligar o segundo fator encerra as sessões de admin abertas.
Sem a variável, o login do admin continua só com a senha.
"""
import base64
import os
import time
from urllib.parse import urlsplit

import pytest

from servicos import credenciais

SENHA_ADMIN = 'senha-de-teste-nao-usar-em-producao'
# Segredo dos vetores de teste da RFC 6238 (apêndice B).
SEGREDO_RFC = b'12345678901234567890'
SEGREDO_B32 = base64.b32encode(SEGREDO_RFC).decode('ascii')


@pytest.mark.parametrize('instante,codigo', [
    (59, '287082'), (1111111109, '081804'), (1234567890, '005924'), (2000000000, '279037'),
])
def test_codigo_segue_os_vetores_da_rfc_6238(instante, codigo):
    assert credenciais.codigo_totp(SEGREDO_RFC, instante // 30) == codigo


@pytest.fixture
def segundo_fator(monkeypatch):
    monkeypatch.setenv('ADMIN_TOTP_SECRET', SEGREDO_B32)


def _codigo_agora(deslocamento=0):
    return credenciais.codigo_totp(SEGREDO_RFC, int(time.time() // 30) + deslocamento)


def _codigo_errado():
    validos = {_codigo_agora(passo) for passo in (-1, 0, 1)}
    return next(codigo for codigo in ('000000', '111111', '222222', '333333') if codigo not in validos)


def _entrar_com_senha(cliente):
    return cliente.post('/login', data={'loginusuario': os.environ['ADMIN_USER'], 'senhausuario': SENHA_ADMIN})


def _destino(resposta):
    return urlsplit(resposta.headers['Location']).path


def test_sem_segundo_fator_o_admin_entra_so_com_a_senha(client):
    assert _destino(_entrar_com_senha(client)) == '/admin'


def test_com_segundo_fator_a_senha_so_leva_ao_codigo(client, segundo_fator):
    assert _destino(_entrar_com_senha(client)) == '/login/verificacao'

    with client.session_transaction() as sess:
        assert 'tipo_usuario' not in sess
    assert _destino(client.get('/admin')) == '/login'

    pagina = client.get('/login/verificacao').get_data(as_text=True)
    assert 'autocomplete="one-time-code"' in pagina
    assert 'inputmode="numeric"' in pagina


def test_codigo_certo_abre_a_sessao_de_admin(client, segundo_fator):
    _entrar_com_senha(client)

    resposta = client.post('/login/verificacao', data={'codigo': _codigo_agora()})

    assert _destino(resposta) == '/admin'
    with client.session_transaction() as sess:
        assert sess['tipo_usuario'] == 'admin'
        assert 'admin_segundo_fator' not in sess
    assert client.get('/admin').status_code == 200


def test_relogio_do_celular_30_segundos_atrasado_ainda_entra(client, segundo_fator):
    _entrar_com_senha(client)

    assert _destino(client.post('/login/verificacao', data={'codigo': _codigo_agora(-1)})) == '/admin'


@pytest.mark.parametrize('codigo', ['errado', '12345', 'abcdef', '', '١٢٣٤٥٦'])
def test_codigo_errado_nao_abre_a_sessao(client, segundo_fator, codigo):
    _entrar_com_senha(client)
    codigo = _codigo_errado() if codigo == 'errado' else codigo

    resposta = client.post('/login/verificacao', data={'codigo': codigo})

    assert resposta.status_code == 200
    assert 'Código inválido' in resposta.get_data(as_text=True)
    with client.session_transaction() as sess:
        assert 'tipo_usuario' not in sess


def test_codigo_nao_vale_duas_vezes(app, client, segundo_fator):
    codigo = _codigo_agora()
    _entrar_com_senha(client)
    assert _destino(client.post('/login/verificacao', data={'codigo': codigo})) == '/admin'

    # Quem viu o código na tela (ou o pegou no caminho) e tem a senha não entra com ele.
    outro = app.test_client()
    _entrar_com_senha(outro)
    resposta = outro.post('/login/verificacao', data={'codigo': codigo})

    assert resposta.status_code == 200
    assert 'já usado' in resposta.get_data(as_text=True)
    with outro.session_transaction() as sess:
        assert 'tipo_usuario' not in sess


def test_codigo_sem_a_senha_antes_volta_ao_login(client, segundo_fator):
    resposta = client.post('/login/verificacao', data={'codigo': _codigo_agora()})

    assert _destino(resposta) == '/login'
    with client.session_transaction() as sess:
        assert 'tipo_usuario' not in sess


def test_etapa_do_codigo_vence_em_5_minutos(client, segundo_fator):
    _entrar_com_senha(client)
    with client.session_transaction() as sess:
        sess['admin_segundo_fator'] = time.time() - 301

    assert _destino(client.post('/login/verificacao', data={'codigo': _codigo_agora()})) == '/login'


def test_etapa_do_codigo_tem_limite(client, segundo_fator):
    _entrar_com_senha(client)
    errado = _codigo_errado()

    for _ in range(5):
        assert client.post('/login/verificacao', data={'codigo': errado}).status_code == 200
    assert client.post('/login/verificacao', data={'codigo': errado}).status_code == 429


def test_ligar_o_segundo_fator_encerra_as_sessoes_de_admin_abertas(client, logar_como_admin, monkeypatch):
    # Uma sessão aberta só com a senha (inclusive um cookie roubado) não sobrevive à ativação.
    logar_como_admin()
    assert client.get('/admin').status_code == 200

    monkeypatch.setenv('ADMIN_TOTP_SECRET', SEGREDO_B32)

    assert _destino(client.get('/admin')) == '/login'


def test_segredo_gerado_pelo_utilitario_e_aceito(monkeypatch):
    segredo = credenciais.gerar_segredo_totp()
    monkeypatch.setenv('ADMIN_TOTP_SECRET', segredo)

    credenciais.validar_segundo_fator_admin()
    assert len(base64.b32decode(segredo)) == 20


@pytest.mark.parametrize('segredo', ['nao-e-base32!', 'MFRGGZDF'])
def test_segredo_ilegivel_ou_curto_e_recusado(monkeypatch, segredo):
    monkeypatch.setenv('ADMIN_TOTP_SECRET', segredo)

    with pytest.raises(ValueError):
        credenciais.validar_segundo_fator_admin()
