from types import SimpleNamespace
from urllib.parse import parse_qs, urlsplit

import pytest

from blueprints import google_login

REDIRECT_URI = 'https://academia.example.test/login/google/callback'


@pytest.fixture
def cliente_google(monkeypatch):
    monkeypatch.setenv('GMAIL_CLIENT_ID', 'client-id')
    monkeypatch.setenv('GMAIL_CLIENT_SECRET', 'client-secret')


@pytest.fixture
def google(monkeypatch, cliente_google):
    """Troca o token e o userinfo do Google; `perfil` é o que o userinfo devolve."""
    estado = {'perfil': {'email': 'aluno1@example.com', 'email_verified': True, 'name': 'Aluno'}, 'tokens': []}

    def post(url, data=None, timeout=None):
        estado['tokens'].append(data)
        return SimpleNamespace(raise_for_status=lambda: None, json=lambda: {'access_token': 'acesso'})

    def get(url, headers=None, timeout=None):
        return SimpleNamespace(raise_for_status=lambda: None, json=lambda: dict(estado['perfil']))

    monkeypatch.setattr(google_login.requests, 'post', post)
    monkeypatch.setattr(google_login.requests, 'get', get)
    return estado


def _voltar_do_google(client, **parametros):
    with client.session_transaction() as sess:
        sess['google_oauth_state'] = 'estado-de-teste'
    parametros.setdefault('state', 'estado-de-teste')
    parametros.setdefault('code', 'codigo')
    return client.get('/login/google/callback', query_string=parametros)


def test_manda_ao_google_com_o_redirect_uri_publico_e_state(client, cliente_google):
    resposta = client.get('/login/google')

    assert resposta.status_code == 302
    destino = urlsplit(resposta.headers['Location'])
    parametros = parse_qs(destino.query)
    assert f'{destino.scheme}://{destino.netloc}{destino.path}' == google_login.AUTH_URL
    assert parametros['redirect_uri'] == [REDIRECT_URI]
    assert parametros['client_id'] == ['client-id']
    with client.session_transaction() as sess:
        assert parametros['state'] == [sess['google_oauth_state']]


def test_sem_cliente_configurado_volta_ao_login(client, monkeypatch):
    monkeypatch.delenv('GMAIL_CLIENT_ID', raising=False)

    resposta = client.get('/login/google')

    assert resposta.status_code == 302
    assert urlsplit(resposta.headers['Location']).path == '/login'


@pytest.mark.parametrize('parametros', [{'state': 'outro'}, {'error': 'access_denied'}, {'code': ''}])
def test_retorno_invalido_volta_ao_login_sem_chamar_o_google(client, google, parametros):
    resposta = _voltar_do_google(client, **parametros)

    assert resposta.status_code == 302
    assert urlsplit(resposta.headers['Location']).path == '/login'
    assert google['tokens'] == []


def test_falha_na_troca_do_code_volta_ao_login(client, cliente_google, monkeypatch):
    def post(*args, **kwargs):
        raise google_login.requests.RequestException('fora do ar')

    monkeypatch.setattr(google_login.requests, 'post', post)

    resposta = _voltar_do_google(client)

    assert resposta.status_code == 302
    assert urlsplit(resposta.headers['Location']).path == '/login'


def test_aluno_aprovado_entra_e_a_troca_usa_o_mesmo_redirect_uri(client, google, criar_aluno):
    criar_aluno(email='aluno1@example.com')

    resposta = _voltar_do_google(client)

    assert resposta.status_code == 302
    assert urlsplit(resposta.headers['Location']).path == '/perfil'
    assert google['tokens'][0]['redirect_uri'] == REDIRECT_URI
    with client.session_transaction() as sess:
        assert sess['tipo_usuario'] == 'aluno'


def test_email_nao_verificado_pelo_google_nao_entra_na_conta(client, google, criar_aluno):
    criar_aluno(email='aluno1@example.com')
    google['perfil']['email_verified'] = False

    resposta = _voltar_do_google(client)

    assert urlsplit(resposta.headers['Location']).path == '/login'
    with client.session_transaction() as sess:
        assert 'aluno_id' not in sess


def test_painel_mostra_o_redirect_uri_do_login_com_google(client, logar_como_admin, cliente_google):
    logar_como_admin()

    resposta = client.get('/admin/academia')

    assert resposta.status_code == 200
    assert REDIRECT_URI in resposta.get_data(as_text=True)


def test_link_de_verificacao_invalido_volta_ao_login(client):
    resposta = client.get('/cadastro/verificar/token-que-nao-existe')

    assert resposta.status_code == 302
    assert urlsplit(resposta.headers['Location']).path == '/login'
