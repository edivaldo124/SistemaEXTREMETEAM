"""Cloudflare Turnstile no cadastro público (SEC-36).

O cadastro manda e-mail para o endereço digitado, pela conta Gmail da academia, e o
limite por IP precisa ser folgado porque a academia inteira sai pelo mesmo Wi-Fi
(SEC-17): só com ele, um IP gerava 480 e-mails por dia para quem quisesse. O Turnstile
confere a pessoa, não o IP.

Sem as três variáveis nada carrega e o cadastro segue sem a checagem (desenvolvimento e
suíte). Em produção o arranque recusa subir sem elas. O token é conferido no servidor,
junto da Cloudflare, antes de qualquer outra coisa do cadastro; se a Cloudflare não
responder, o cadastro é recusado.
"""

import logging
import os

import requests
from flask import request

logger = logging.getLogger(__name__)

SITEVERIFY_URL = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'
# O widget é um iframe desta origem, carregado pelo api.js dela. Só entra na política da
# resposta que mostra o widget (guia de CSP do Turnstile: script-src e frame-src).
CSP_ORIGEM = 'https://challenges.cloudflare.com'
ENDPOINTS_COM_TURNSTILE = ('auth.pagina_cadastro',)
# A ação vai no widget e volta no resultado: um token tirado em outra tela não serve aqui.
ACAO_CADASTRO = 'cadastro'
TAMANHO_MAXIMO_TOKEN = 2048
TIMEOUT_SEGUNDOS = 10
_ENDERECOS_LOCAIS = {'localhost', '127.0.0.1'}


def _chave_site():
    return (os.environ.get('TURNSTILE_SITEKEY') or '').strip()


def _segredo():
    return (os.environ.get('TURNSTILE_SECRET') or '').strip()


def hostnames_esperados():
    """Sites onde o widget pode ter sido resolvido, como a Cloudflare os informa."""
    return {
        host.strip().lower()
        for host in (os.environ.get('TURNSTILE_HOSTNAMES') or '').split(',')
        if host.strip()
    }


def configurado():
    return bool(_chave_site() and _segredo() and hostnames_esperados())


def validar_configuracao(exigir):
    """Chamada no arranque. `exigir` é verdadeiro em produção (endereço público em https).

    Metade das variáveis desligaria a checagem sem aviso, então também derruba a subida.
    """
    preenchidas = [bool(_chave_site()), bool(_segredo()), bool(hostnames_esperados())]
    if any(preenchidas) and not all(preenchidas):
        raise RuntimeError(
            'Defina TURNSTILE_SITEKEY, TURNSTILE_SECRET e TURNSTILE_HOSTNAMES juntas, ou nenhuma.'
        )
    if not exigir:
        return
    if not all(preenchidas):
        raise RuntimeError(
            'Em produção o cadastro público exige o Turnstile: defina TURNSTILE_SITEKEY, '
            'TURNSTILE_SECRET e TURNSTILE_HOSTNAMES (os domínios do site, separados por vírgula).'
        )
    if hostnames_esperados() & _ENDERECOS_LOCAIS:
        raise RuntimeError('TURNSTILE_HOSTNAMES de produção não pode ter localhost nem 127.0.0.1.')


def chave_site():
    """Para o template: a chave pública do widget, ou vazio quando o Turnstile está desligado."""
    return _chave_site() if configurado() else ''


def ativo_nesta_resposta():
    return configurado() and request.endpoint in ENDPOINTS_COM_TURNSTILE


def token_confere(token, ip, acao):
    """O token veio de uma pessoa, nesta ação e num site nosso? Na dúvida, não."""
    hosts = hostnames_esperados()
    if not isinstance(token, str) or not token or len(token) > TAMANHO_MAXIMO_TOKEN or not hosts:
        return False
    try:
        resposta = requests.post(
            SITEVERIFY_URL,
            data={'secret': _segredo(), 'response': token, 'remoteip': ip},
            timeout=TIMEOUT_SEGUNDOS,
        )
        resposta.raise_for_status()
        resultado = resposta.json()
    except (requests.RequestException, ValueError):
        logger.warning('Turnstile: siteverify não respondeu; cadastro recusado (ip=%s).', ip, exc_info=True)
        return False
    if not isinstance(resultado, dict):
        return False
    hostname = resultado.get('hostname')
    if (resultado.get('success') is True
            and resultado.get('action') == acao
            and isinstance(hostname, str) and hostname.lower() in hosts):
        return True
    logger.warning(
        'Turnstile recusou o cadastro: ip=%s erros=%s', ip, resultado.get('error-codes'),
    )
    return False
