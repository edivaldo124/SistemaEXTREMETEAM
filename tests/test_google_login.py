import base64
import hashlib
import time
from types import SimpleNamespace
from urllib.parse import parse_qs, urlsplit

import pytest

from blueprints import google_login

REDIRECT_URI = 'https://academia.example.test/login/google/callback'
VERIFIER_DE_TESTE = 'verificador-de-teste-' + 'x' * 40


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


def _voltar_do_google(client, *, criado_em=None, guardada=None, **parametros):
    with client.session_transaction() as sess:
        sess[google_login.CHAVE_SESSAO] = guardada if guardada is not None else {
            'state': 'estado-de-teste',
            'verifier': VERIFIER_DE_TESTE,
            'criado_em': time.time() if criado_em is None else criado_em,
        }
    parametros.setdefault('state', 'estado-de-teste')
    parametros.setdefault('code', 'codigo')
    return client.get('/login/google/callback', query_string=parametros)


def test_manda_ao_google_com_o_redirect_uri_publico_state_e_pkce(client, cliente_google):
    resposta = client.get('/login/google')

    assert resposta.status_code == 302
    destino = urlsplit(resposta.headers['Location'])
    parametros = parse_qs(destino.query)
    assert f'{destino.scheme}://{destino.netloc}{destino.path}' == google_login.AUTH_URL
    assert parametros['redirect_uri'] == [REDIRECT_URI]
    assert parametros['client_id'] == ['client-id']
    with client.session_transaction() as sess:
        guardada = sess[google_login.CHAVE_SESSAO]
    assert parametros['state'] == [guardada['state']]
    # O desafio é o SHA-256 do verificador que ficou na sessão (PKCE S256).
    esperado = base64.urlsafe_b64encode(hashlib.sha256(guardada['verifier'].encode()).digest()).rstrip(b'=').decode()
    assert parametros['code_challenge'] == [esperado]
    assert parametros['code_challenge_method'] == ['S256']
    assert 43 <= len(guardada['verifier']) <= 128
    # Só o necessário para achar a conta: nada de nome e foto (escopo `profile`).
    assert parametros['scope'] == ['openid email']


def test_troca_do_code_manda_o_verificador_da_sessao(client, google, criar_aluno):
    criar_aluno(email='aluno1@example.com')

    _voltar_do_google(client)

    assert google['tokens'][0]['code_verifier'] == VERIFIER_DE_TESTE


@pytest.mark.parametrize('guardada', [
    {'state': 'estado-de-teste', 'criado_em': 0},  # sem verificador
    'estado-de-teste',  # formato antigo da sessão
])
def test_sessao_sem_pkce_nao_troca_o_code(client, google, guardada):
    if isinstance(guardada, dict):
        guardada = {**guardada, 'criado_em': time.time()}

    resposta = _voltar_do_google(client, guardada=guardada)

    assert urlsplit(resposta.headers['Location']).path == '/login'
    assert google['tokens'] == []


def test_state_vencido_nao_troca_o_code(client, google, criar_aluno):
    criar_aluno(email='aluno1@example.com')

    resposta = _voltar_do_google(client, criado_em=time.time() - google_login.VALIDADE_AUTORIZACAO_SEGUNDOS - 1)

    assert urlsplit(resposta.headers['Location']).path == '/login'
    assert google['tokens'] == []
    with client.session_transaction() as sess:
        assert 'aluno_id' not in sess


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


def test_email_sem_conta_volta_ao_login_sem_cadastrar(client, google):
    resposta = _voltar_do_google(client)

    assert resposta.status_code == 302
    assert urlsplit(resposta.headers['Location']).path == '/login'
    with client.session_transaction() as sess:
        assert 'aluno_id' not in sess
        assert not any(chave.startswith('google_cadastro') for chave in sess)


def test_cadastro_nao_oferece_criar_conta_com_o_google(client):
    pagina = client.get('/cadastrar').get_data(as_text=True)

    assert '/login/google' not in pagina


@pytest.mark.parametrize('caminho,inicio', [('/login', 'id="login-title"'), ('/', 'id="meuModal"')])
def test_login_e_modal_da_home_oferecem_entrar_com_o_google(client, caminho, inicio):
    pagina = client.get(caminho).get_data(as_text=True)
    trecho = pagina[pagina.index(inicio):]

    # O botão vem antes do formulário de usuário e senha, como na página de login.
    assert trecho.index('href="/login/google"') < trecho.index('name="loginusuario"')


def test_painel_mostra_o_redirect_uri_do_login_com_google(client, logar_como_admin, cliente_google):
    logar_como_admin()

    resposta = client.get('/admin/academia')

    assert resposta.status_code == 200
    assert REDIRECT_URI in resposta.get_data(as_text=True)


def test_politica_de_privacidade_descreve_o_login_com_google(client):
    # LGPD (transparência) e exigência do Google: quem oferece o login conta o que recebe.
    politica = client.get('/politica-privacidade').get_data(as_text=True)

    assert 'Entrar com o Google (alunos)' in politica
    assert 'apenas o endereço de e-mail e se ele foi confirmado' in politica
    assert 'não conectam contas do Google.</p>' not in politica


def test_link_de_verificacao_invalido_volta_ao_login(client):
    resposta = client.get('/cadastro/verificar/token-que-nao-existe')

    assert resposta.status_code == 302
    assert urlsplit(resposta.headers['Location']).path == '/login'
