import os
from urllib.parse import urlparse

from flask import url_for


class URLPublicaInvalida(RuntimeError):
    pass


def base_url_publica():
    """Retorna a origem pública configurada, sem usar o cabeçalho Host da requisição."""
    valor = (os.environ.get('APP_BASE_URL') or '').strip().rstrip('/')
    partes = urlparse(valor)
    if (
        any(caractere.isspace() for caractere in valor)
        or partes.scheme not in ('http', 'https')
        or not partes.hostname
        or partes.username
        or partes.password
        or partes.path not in ('', '/')
        or partes.query
        or partes.fragment
        or ((os.environ.get('COOKIE_SECURE') or '').lower() == 'true' and partes.scheme != 'https')
    ):
        raise URLPublicaInvalida(
            'APP_BASE_URL ausente ou inválida; configure a origem pública http/https da aplicação.'
        )
    return valor


def url_publica(endpoint, **valores):
    return f'{base_url_publica()}{url_for(endpoint, **valores)}'
