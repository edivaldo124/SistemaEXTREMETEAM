import base64
import logging
import os
import re
import threading
import time

import requests
from flask import render_template
from servicos import gmail_conta

logger = logging.getLogger(__name__)


def _destinatario_log(destinatario):
    endereco = (destinatario or '').strip()
    if '@' not in endereco:
        return '<invalido>'
    usuario, dominio = endereco.split('@', 1)
    return f'{usuario[:2]}***@{dominio}'



def email_valido(endereco):
    """Validação sintática básica, compartilhada pelos formulários do cadastro."""
    return bool(endereco and len(endereco) <= 150
                and re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+', endereco))


def enviar_email(destinatario, nome_destinatario, assunto, titulo, paragrafos, link_url=None, link_texto=None):
    """Envia e-mail transacional pela Gmail API. Retorna True/False; nunca lança."""
    if not destinatario:
        # Aluno matriculado pela administração pode não ter e-mail próprio. Isso não é
        # erro: o cadastro dele é gerido no balcão e simplesmente não recebe aviso.
        logger.info('E-mail "%s" não enviado: cadastro sem endereço.', assunto)
        return False

    if not gmail_conta.estado()['conectada']:
        logger.warning('Nenhuma conta Gmail conectada; e-mail "%s" para %s não enviado.', assunto, _destinatario_log(destinatario))
        return False

    try:
        corpo_html = render_template(
            'email/base.html', titulo=titulo, paragrafos=paragrafos, link_url=link_url, link_texto=link_texto,
        )
    except Exception:
        logger.exception('Falha ao montar o corpo do e-mail "%s" para %s.', assunto, _destinatario_log(destinatario))
        return False

    try:
        gmail_conta.enviar(destinatario, nome_destinatario, assunto, corpo_html)
        return True
    except requests.RequestException:
        logger.exception('Falha ao enviar e-mail "%s" para %s.', assunto, _destinatario_log(destinatario))
        return False
