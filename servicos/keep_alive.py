"""Mantém a aplicação acordada em hospedagens que hibernam por inatividade.

O plano gratuito do Render derruba o serviço depois de ~15 minutos sem nenhuma
requisição HTTP de entrada, e a volta custa quase um minuto de espera para o
primeiro visitante. Uma thread daemon bate no próprio /health em intervalos
menores que esse para o serviço nunca chegar a hibernar.

Fica desligado por padrão: só sobe quando KEEP_ALIVE=true. O destino nunca vem
da requisição (nem do cabeçalho Host), e sim de APP_BASE_URL, a mesma origem já
validada em servicos/urls.py - assim isto não vira um proxy para URLs de
terceiros.
"""

import logging
import os
import threading

import requests

from servicos.urls import URLPublicaInvalida, base_url_publica

logger = logging.getLogger(__name__)

CAMINHO_PING = '/health'
INTERVALO_PADRAO = 600
# Piso evita transformar um erro de digitação na variável de ambiente num laço
# de requisições; teto fica abaixo dos ~15 min que o Render espera para hibernar.
INTERVALO_MINIMO = 60
INTERVALO_MAXIMO = 840
TIMEOUT = 15

_parar = threading.Event()
_trava = threading.Lock()
_thread = None


def _ligado():
    return (os.environ.get('KEEP_ALIVE') or '').strip().lower() in ('1', 'true', 'yes', 'on')


def _intervalo():
    bruto = (os.environ.get('KEEP_ALIVE_INTERVALO') or '').strip()
    if not bruto:
        return INTERVALO_PADRAO
    try:
        segundos = int(bruto)
    except ValueError:
        logger.warning('KEEP_ALIVE_INTERVALO invalido (%r); usando %s s.', bruto, INTERVALO_PADRAO)
        return INTERVALO_PADRAO
    return max(INTERVALO_MINIMO, min(segundos, INTERVALO_MAXIMO))


def _pingar(url):
    try:
        resposta = requests.get(
            url,
            timeout=TIMEOUT,
            # Sem redirect: um 3xx inesperado não deve levar a requisição para
            # outro host, e o /health responde 200 direto.
            allow_redirects=False,
            headers={'User-Agent': 'extremeteam-keepalive/1.0'},
        )
    except requests.RequestException as exc:
        logger.warning('Keep-alive falhou: %s', exc)
        return
    if resposta.status_code >= 400:
        logger.warning('Keep-alive recebeu HTTP %s de %s.', resposta.status_code, url)


def _laco(url, intervalo):
    # Espera antes do primeiro ping: o processo acabou de subir, então já está acordado.
    while not _parar.wait(intervalo):
        _pingar(url)


def iniciar():
    """Sobe a thread de keep-alive quando habilitada. Seguro chamar mais de uma vez.

    O guard é por processo. O Gunicorn roda com --workers 1 (ver Dockerfile), logo
    existe um único ping por intervalo; se o número de workers subir, cada um passa
    a pingar e o intervalo efetivo cai na mesma proporção.
    """
    global _thread
    if not _ligado():
        return False
    try:
        url = base_url_publica() + CAMINHO_PING
    except URLPublicaInvalida as exc:
        logger.warning('Keep-alive desligado: %s', exc)
        return False
    with _trava:
        if _thread is not None and _thread.is_alive():
            return False
        intervalo = _intervalo()
        _thread = threading.Thread(
            target=_laco, args=(url, intervalo), name='keep-alive', daemon=True
        )
        _thread.start()
    logger.info('Keep-alive ativo: %s a cada %s s.', url, intervalo)
    return True


def parar():
    """Encerra o laço. Usado pelos testes; em produção a thread é daemon."""
    global _thread
    _parar.set()
    with _trava:
        thread, _thread = _thread, None
    if thread is not None:
        thread.join(timeout=5)
    _parar.clear()
