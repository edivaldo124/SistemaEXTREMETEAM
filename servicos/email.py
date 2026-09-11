import re
import logging
import os

import requests
from flask import render_template

logger = logging.getLogger(__name__)

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


def email_valido(endereco):
    """Validação sintática básica, compartilhada pelos formulários do cadastro."""
    return bool(endereco and len(endereco) <= 150
                and re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+', endereco))


def enviar_email(destinatario, nome_destinatario, assunto, titulo, paragrafos, link_url=None, link_texto=None):
    """Envia um e-mail transacional via Brevo. Retorna True/False; nunca lança."""
    if not destinatario:
        # Aluno matriculado pela administração pode não ter e-mail próprio. Isso não é
        # erro: o cadastro dele é gerido no balcão e simplesmente não recebe aviso.
        logger.info('E-mail "%s" não enviado: cadastro sem endereço.', assunto)
        return False

    api_key = os.environ.get('BREVO_API_KEY')
    remetente_email = os.environ.get('BREVO_SENDER_EMAIL')
    if not api_key or not remetente_email:
        logger.warning('Brevo nao configurado; e-mail "%s" para %s nao enviado.', assunto, destinatario)
        return False

    try:
        corpo_html = render_template(
            'email/base.html', titulo=titulo, paragrafos=paragrafos, link_url=link_url, link_texto=link_texto,
        )
    except Exception:
        logger.exception('Falha ao montar o corpo do e-mail "%s" para %s.', assunto, destinatario)
        return False

    payload = {
        'sender': {
            'name': os.environ.get('BREVO_SENDER_NAME', 'Extreme Team'),
            'email': remetente_email,
        },
        'to': [{'email': destinatario, 'name': nome_destinatario}],
        'subject': assunto,
        'htmlContent': corpo_html,
    }

    try:
        resposta = requests.post(
            BREVO_API_URL,
            json=payload,
            headers={'api-key': api_key, 'Content-Type': 'application/json', 'Accept': 'application/json'},
            timeout=10,
        )
        resposta.raise_for_status()
        return True
    except requests.RequestException:
        logger.exception('Falha ao enviar e-mail "%s" para %s.', assunto, destinatario)
        return False
