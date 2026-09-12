"""Aciona a fila periodicamente durante a vida de um worker Gunicorn.

Importar este módulo não inicia threads. As migrations continuam sem consumidor.
O envio e as travas permanecem sob responsabilidade de fila_email.
"""
import logging
import os
import threading

from servicos import fila_email

logger = logging.getLogger(__name__)
INTERVALO_SEGUNDOS = 30
_trava = threading.Lock()
_thread = None
_parar = threading.Event()


def _laco():
    while not _parar.is_set():
        try:
            fila_email.disparar()
        except Exception:
            # Uma falha ao criar a thread de entrega não desliga o agendamento.
            logger.exception('Falha ao acionar a fila de e-mail; haverá nova tentativa.')
        if _parar.wait(INTERVALO_SEGUNDOS):
            return


def iniciar(app):
    """Inicia uma vez por processo, depois de carregar a aplicação e migrar o banco."""
    global _thread
    if app.testing or os.environ.get('FILA_EMAIL_SINCRONA', '').lower() == 'true':
        return False
    with _trava:
        if _thread is not None and _thread.is_alive():
            return False
        fila_email.registrar_app(app)
        _parar.clear()
        _thread = threading.Thread(target=_laco, name='agenda-email', daemon=True)
        _thread.start()
        return True


def parar():
    """Interrompe novas ativações; itens não confirmados permanecem na fila durável."""
    _parar.set()

