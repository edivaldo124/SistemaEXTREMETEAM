import base64
import hashlib
import logging
import os
import secrets
import time
from datetime import datetime
from email.message import EmailMessage
from urllib.parse import urlencode

import requests
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from flask import current_app
from sqlalchemy import delete

from config import db
from modelos.gmail_conexao import GmailConexao
from servicos.mercado_pago import base_url_publica

logger = logging.getLogger(__name__)
AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN_URL = 'https://oauth2.googleapis.com/token'
USERINFO_URL = 'https://openidconnect.googleapis.com/v1/userinfo'
SEND_URL = 'https://gmail.googleapis.com/gmail/v1/users/me/messages/send'
SCOPE = 'https://www.googleapis.com/auth/gmail.send'
CALLBACK = '/admin/gmail/callback'


def _client_id():
    return (os.environ.get('GMAIL_CLIENT_ID') or '').strip()


def _client_secret():
    return (os.environ.get('GMAIL_CLIENT_SECRET') or '').strip()


def oauth_configurado():
    return bool(_client_id() and _client_secret())


def redirect_uri():
    return f'{base_url_publica()}{CALLBACK}'


def _fernet():
    derivada = HKDF(algorithm=hashes.SHA256(), length=32, salt=None,
                    info=b'extremeteam/gmail/tokens/v1').derive(
        str(current_app.secret_key).encode('utf-8')
    )
    return Fernet(base64.urlsafe_b64encode(derivada))


def _cifrar(valor):
    return _fernet().encrypt(valor.encode()).decode('ascii')


def _decifrar(valor):
    try:
        return _fernet().decrypt(valor.encode('ascii')).decode()
    except InvalidToken as exc:
        raise RuntimeError('Token Gmail ilegível; conecte a conta novamente.') from exc


def nova_autorizacao():
    state = secrets.token_urlsafe(32)
    url = AUTH_URL + '?' + urlencode({
        'client_id': _client_id(),
        'redirect_uri': redirect_uri(),
        'response_type': 'code',
        'scope': f'openid email {SCOPE}',
        'access_type': 'offline',
        'prompt': 'consent',
        'state': state,
    })
    return url, state


def trocar_codigo(code):
    resposta = requests.post(TOKEN_URL, data={
        'code': code,
        'client_id': _client_id(),
        'client_secret': _client_secret(),
        'redirect_uri': redirect_uri(),
        'grant_type': 'authorization_code',
    }, timeout=10)
    resposta.raise_for_status()
    dados = resposta.json()
    refresh = dados.get('refresh_token')
    if not refresh:
        raise ValueError('Google não devolveu refresh token; reconecte com consentimento.')
    perfil = requests.get(USERINFO_URL, headers={
        'Authorization': f"Bearer {dados['access_token']}"
    }, timeout=10)
    perfil.raise_for_status()
    email = perfil.json().get('email')
    if not email:
        raise ValueError('Google não devolveu o e-mail autorizado.')
    return email, refresh


def salvar(email, refresh_token):
    conexao = db.session.get(GmailConexao, 1) or GmailConexao(id=1)
    conexao.email = email
    conexao.refresh_token_cifrado = _cifrar(refresh_token)
    conexao.conectado_em = datetime.utcnow()
    db.session.add(conexao)
    db.session.commit()


def remover():
    db.session.execute(delete(GmailConexao))
    db.session.commit()


def estado():
    conexao = db.session.get(GmailConexao, 1)
    return {
        'oauth_disponivel': oauth_configurado(),
        'conectada': conexao is not None,
        'email': conexao.email if conexao else None,
        'conectado_em': conexao.conectado_em if conexao else None,
    }


def _access_token():
    conexao = db.session.get(GmailConexao, 1)
    if not conexao:
        raise RuntimeError('Nenhuma conta Gmail conectada.')
    resposta = requests.post(TOKEN_URL, data={
        'client_id': _client_id(),
        'client_secret': _client_secret(),
        'refresh_token': _decifrar(conexao.refresh_token_cifrado),
        'grant_type': 'refresh_token',
    }, timeout=10)
    resposta.raise_for_status()
    return resposta.json()['access_token']


def enviar(destinatario, nome, assunto, corpo_html):
    mensagem = EmailMessage()
    mensagem['To'] = f'{nome} <{destinatario}>' if nome else destinatario
    mensagem['Subject'] = assunto
    mensagem.set_content(corpo_html, subtype='html')
    raw = base64.urlsafe_b64encode(mensagem.as_bytes()).decode('ascii')
    resposta = requests.post(SEND_URL, json={'raw': raw}, headers={
        'Authorization': f'Bearer {_access_token()}',
        'Content-Type': 'application/json',
    }, timeout=10)
    resposta.raise_for_status()
