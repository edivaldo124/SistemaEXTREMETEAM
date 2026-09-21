import base64
import logging
import os
import re
import threading
import time
from email.message import EmailMessage

import requests
from flask import render_template

logger = logging.getLogger(__name__)

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GMAIL_SEND_URL = "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"

_token_gmail = None
_expiracao_token_gmail = 0
_lock_token_gmail = threading.Lock()


def email_valido(endereco):
    """Validação sintática básica, compartilhada pelos formulários do cadastro."""
    return bool(endereco and len(endereco) <= 150
                and re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+', endereco))


def _obter_token_gmail():
    global _token_gmail, _expiracao_token_gmail

    with _lock_token_gmail:
        if _token_gmail and time.monotonic() < _expiracao_token_gmail:
            return _token_gmail

        resposta = requests.post(
            GOOGLE_TOKEN_URL,
            data={
                'client_id': os.environ['GMAIL_CLIENT_ID'],
                'client_secret': os.environ['GMAIL_CLIENT_SECRET'],
                'refresh_token': os.environ['GMAIL_REFRESH_TOKEN'],
                'grant_type': 'refresh_token',
            },
            timeout=10,
        )
        resposta.raise_for_status()
        dados = resposta.json()
        token = dados.get('access_token')
        if not token:
            raise ValueError('Google não devolveu access_token.')
        _token_gmail = token
        _expiracao_token_gmail = time.monotonic() + max(int(dados.get('expires_in', 3600)) - 60, 60)
        return token


def _enviar_via_gmail(destinatario, nome_destinatario, assunto, corpo_html):
    mensagem = EmailMessage()
    mensagem['To'] = f'{nome_destinatario} <{destinatario}>' if nome_destinatario else destinatario
    mensagem['Subject'] = assunto
    mensagem['From'] = os.environ['GMAIL_SENDER_EMAIL']
    mensagem.set_content(corpo_html, subtype='html')
    codificada = base64.urlsafe_b64encode(mensagem.as_bytes()).decode('ascii')

    resposta = requests.post(
        GMAIL_SEND_URL,
        json={'raw': codificada},
        headers={
            'Authorization': f'Bearer {_obter_token_gmail()}',
            'Content-Type': 'application/json',
        },
        timeout=10,
    )
    resposta.raise_for_status()


def enviar_email(destinatario, nome_destinatario, assunto, titulo, paragrafos, link_url=None, link_texto=None):
    """Envia e-mail transacional pela Gmail API. Retorna True/False; nunca lança."""
    if not destinatario:
        # Aluno matriculado pela administração pode não ter e-mail próprio. Isso não é
        # erro: o cadastro dele é gerido no balcão e simplesmente não recebe aviso.
        logger.info('E-mail "%s" não enviado: cadastro sem endereço.', assunto)
        return False

    variaveis = ('GMAIL_CLIENT_ID', 'GMAIL_CLIENT_SECRET', 'GMAIL_REFRESH_TOKEN', 'GMAIL_SENDER_EMAIL')
    if any(not os.environ.get(variavel) for variavel in variaveis):
        logger.warning('Gmail não configurado; e-mail "%s" para %s não enviado.', assunto, destinatario)
        return False

    try:
        corpo_html = render_template(
            'email/base.html', titulo=titulo, paragrafos=paragrafos, link_url=link_url, link_texto=link_texto,
        )
    except Exception:
        logger.exception('Falha ao montar o corpo do e-mail "%s" para %s.', assunto, destinatario)
        return False

    try:
        _enviar_via_gmail(destinatario, nome_destinatario, assunto, corpo_html)
        return True
    except requests.RequestException:
        logger.exception('Falha ao enviar e-mail "%s" para %s.', assunto, destinatario)
        return False
