"""Normalização de contatos profissionais antes de montar links públicos."""
import re
from urllib.parse import quote, urlsplit


def link_email(valor):
    return 'mailto:' + quote(valor, safe='@') if valor else None


def validar_instagram(valor):
    valor = (valor or '').strip()
    if not valor:
        return None
    if valor.startswith(('https://', 'http://')):
        url = urlsplit(valor)
        if url.netloc.lower() not in ('instagram.com', 'www.instagram.com'):
            raise ValueError('Informe o usuário ou o link do perfil no Instagram.')
        valor = url.path.strip('/')
    valor = valor.removeprefix('@')
    if not re.fullmatch(r'[A-Za-z0-9_](?:[A-Za-z0-9_.]{0,28}[A-Za-z0-9_])?', valor) or '..' in valor:
        raise ValueError('Informe um usuário válido do Instagram, com até 30 caracteres.')
    return valor


def validar_email(valor):
    valor = (valor or '').strip()
    if not valor:
        return None
    if len(valor) > 150 or not re.fullmatch(r"[A-Za-z0-9.!#$%&'*+/=_`{|}~^-]+@[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?\.[A-Za-z]{2,63}", valor):
        raise ValueError('Informe um e-mail válido, com até 150 caracteres.')
    return valor


def validar_whatsapp(valor):
    valor = (valor or '').strip()
    if not valor:
        return None
    if not re.fullmatch(r'\+?[0-9 ()-]+', valor):
        raise ValueError('Informe o WhatsApp com DDD; para outros países, use + e o código do país.')
    numero = re.sub(r'\D', '', valor)
    if not valor.startswith('+') and len(numero) in (10, 11):
        numero = '55' + numero
    if not 10 <= len(numero) <= 15 or numero.startswith('0'):
        raise ValueError('Informe um WhatsApp válido com DDD e código do país.')
    return numero
