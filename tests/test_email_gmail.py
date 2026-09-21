import base64
from email import policy
from email.parser import BytesParser
from types import SimpleNamespace

import pytest

from servicos import email


@pytest.fixture(autouse=True)
def limpar_cache_token():
    email._token_gmail = None
    email._expiracao_token_gmail = 0
    yield
    email._token_gmail = None
    email._expiracao_token_gmail = 0


def test_envia_pelo_gmail_com_refresh_token(monkeypatch):
    monkeypatch.setenv('GMAIL_CLIENT_ID', 'client-id')
    monkeypatch.setenv('GMAIL_CLIENT_SECRET', 'client-secret')
    monkeypatch.setenv('GMAIL_REFRESH_TOKEN', 'refresh-token')
    monkeypatch.setenv('GMAIL_SENDER_EMAIL', 'sistema@example.com')
    chamadas = []

    def post(url, **kwargs):
        chamadas.append((url, kwargs))
        if url == email.GOOGLE_TOKEN_URL:
            return SimpleNamespace(raise_for_status=lambda: None, json=lambda: {
                'access_token': 'access-token', 'expires_in': 3600,
            })
        return SimpleNamespace(raise_for_status=lambda: None)

    monkeypatch.setattr(email.requests, 'post', post)

    email._enviar_via_gmail('aluno@example.com', 'Aluno', 'Aviso', '<p>Corpo</p>')

    assert [url for url, _ in chamadas] == [email.GOOGLE_TOKEN_URL, email.GMAIL_SEND_URL]
    dados_envio = chamadas[1][1]
    assert dados_envio['headers']['Authorization'] == 'Bearer access-token'
    mensagem = BytesParser(policy=policy.default).parsebytes(
        base64.urlsafe_b64decode(dados_envio['json']['raw'])
    )
    assert mensagem['To'] == 'Aluno <aluno@example.com>'
    assert mensagem['From'] == 'sistema@example.com'
    assert mensagem['Subject'] == 'Aviso'
    assert mensagem.get_body(preferencelist=('html',)).get_content().strip() == '<p>Corpo</p>'


def test_gmail_sem_credenciais_nao_chama_rede(monkeypatch):
    monkeypatch.setenv('EMAIL_PROVIDER', 'gmail')
    monkeypatch.delenv('GMAIL_CLIENT_ID', raising=False)
    monkeypatch.delenv('GMAIL_CLIENT_SECRET', raising=False)
    monkeypatch.delenv('GMAIL_REFRESH_TOKEN', raising=False)
    monkeypatch.delenv('GMAIL_SENDER_EMAIL', raising=False)
    monkeypatch.setattr(email.requests, 'post', lambda *args, **kwargs: pytest.fail('não deveria chamar a rede'))

    assert email.enviar_email('aluno@example.com', 'Aluno', 'Aviso', 'Aviso', ['Corpo']) is False
