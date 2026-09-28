import base64
from email import policy
from email.parser import BytesParser
from types import SimpleNamespace

import pytest
import requests

from servicos import email, gmail_conta


@pytest.fixture
def aplicativo_google(monkeypatch):
    monkeypatch.setenv('GMAIL_CLIENT_ID', 'client-id')
    monkeypatch.setenv('GMAIL_CLIENT_SECRET', 'client-secret')


def test_envia_pelo_gmail_com_o_refresh_token_da_conexao(contexto_app, aplicativo_google, monkeypatch):
    gmail_conta.salvar('sistema@example.com', 'refresh-token')
    chamadas = []

    def post(url, **kwargs):
        chamadas.append((url, kwargs))
        if url == gmail_conta.TOKEN_URL:
            return SimpleNamespace(raise_for_status=lambda: None, json=lambda: {
                'access_token': 'access-token', 'expires_in': 3600,
            })
        return SimpleNamespace(raise_for_status=lambda: None)

    monkeypatch.setattr(gmail_conta.requests, 'post', post)

    gmail_conta.enviar('aluno@example.com', 'Aluno', 'Aviso', '<p>Corpo</p>')

    assert [url for url, _ in chamadas] == [gmail_conta.TOKEN_URL, gmail_conta.SEND_URL]
    # O refresh token sai do banco, decifrado só na hora de pedir o access token.
    assert chamadas[0][1]['data']['refresh_token'] == 'refresh-token'
    assert chamadas[0][1]['data']['grant_type'] == 'refresh_token'
    dados_envio = chamadas[1][1]
    assert dados_envio['headers']['Authorization'] == 'Bearer access-token'
    mensagem = BytesParser(policy=policy.default).parsebytes(
        base64.urlsafe_b64decode(dados_envio['json']['raw'])
    )
    assert mensagem['To'] == 'Aluno <aluno@example.com>'
    assert mensagem['Subject'] == 'Aviso'
    assert mensagem.get_body(preferencelist=('html',)).get_content().strip() == '<p>Corpo</p>'


def test_refresh_token_fica_cifrado_no_banco(contexto_app, aplicativo_google):
    from config import db
    from modelos.gmail_conexao import GmailConexao

    gmail_conta.salvar('sistema@example.com', 'refresh-token-secreto')

    assert 'refresh-token-secreto' not in db.session.get(GmailConexao, 1).refresh_token_cifrado


def test_sem_conta_gmail_conectada_nao_chama_rede(contexto_app, aplicativo_google, monkeypatch):
    monkeypatch.setattr(gmail_conta.requests, 'post', lambda *args, **kwargs: pytest.fail('não deveria chamar a rede'))

    assert email.enviar_email('aluno@example.com', 'Aluno', 'Aviso', 'Aviso', ['Corpo']) is False


def test_falha_do_google_nao_derruba_quem_envia(contexto_app, aplicativo_google, monkeypatch):
    gmail_conta.salvar('sistema@example.com', 'refresh-token')

    def fora_do_ar(*args, **kwargs):
        raise requests.ConnectionError('sem rede')

    monkeypatch.setattr(gmail_conta.requests, 'post', fora_do_ar)

    assert email.enviar_email('aluno@example.com', 'Aluno', 'Aviso', 'Aviso', ['Corpo']) is False
