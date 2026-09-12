"""Agendamento sem rede, threads reais ou esperas de relógio."""
from types import SimpleNamespace
import runpy
from pathlib import Path

import pytest

from servicos import consumidor_email as consumidor


def test_retomada_de_item_persistido_e_retentativa_sem_painel(contexto_app, monkeypatch):
    from datetime import datetime, timedelta
    from config import db
    from modelos.email_pendente import EmailPendente, STATUS_ENVIADO

    fila = consumidor.fila_email
    item = fila.enfileirar(
        destinatario='teste@example.test', nome_destinatario='Teste',
        assunto='Aviso', titulo='Aviso', paragrafos=['Teste'],
        chave_idempotencia='retomada-consumidor',
    )
    db.session.commit()
    item_id = item.id
    db.session.remove()  # O consumidor precisa recuperar o item persistido.
    entregas = []

    def entregar(item):
        entregas.append(item.id)
        return len(entregas) > 1

    class Parada:
        def is_set(self):
            return False

        def wait(self, intervalo):
            if len(entregas) >= 2:
                return True
            pendente = db.session.get(EmailPendente, item_id)
            assert pendente.tentativas == 1
            assert pendente.proxima_tentativa > datetime.utcnow()
            # Simula passagem do prazo, sem dormir nem acessar um provedor.
            pendente.proxima_tentativa = datetime.utcnow() - timedelta(seconds=1)
            db.session.commit()
            return False

    monkeypatch.setattr(fila, '_entregar', entregar)
    monkeypatch.setattr(fila, 'disparar', fila.processar_agora)
    monkeypatch.setattr(consumidor, '_parar', Parada())
    consumidor._laco()
    assert entregas == [item_id, item_id]
    assert db.session.get(EmailPendente, item_id).status == STATUS_ENVIADO


def test_reaciona_fila_sem_requisicao_e_sobrevive_a_falha(monkeypatch):
    chamadas = []

    def disparar():
        chamadas.append('disparo')
        if len(chamadas) == 1:
            raise RuntimeError('falha temporária')

    class Parada:
        def is_set(self):
            return False

        def wait(self, intervalo):
            assert intervalo == 30
            return len(chamadas) == 3

    monkeypatch.setattr(consumidor, '_parar', Parada())
    monkeypatch.setattr(consumidor.fila_email, 'disparar', disparar)
    consumidor._laco()
    assert chamadas == ['disparo'] * 3


@pytest.mark.parametrize('testing,sincrona', [(True, 'false'), (False, 'true')])
def test_nao_inicia_em_testes(monkeypatch, testing, sincrona):
    monkeypatch.setenv('FILA_EMAIL_SINCRONA', sincrona)
    monkeypatch.setattr(consumidor.fila_email, 'registrar_app', lambda app: pytest.fail('iniciou'))
    assert consumidor.iniciar(SimpleNamespace(testing=testing)) is False


def test_inicializacao_unica_e_parada(monkeypatch):
    import threading

    inicios = []
    apps = []

    class ThreadFalsa:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

        def start(self):
            inicios.append(self)

        def is_alive(self):
            return True

    monkeypatch.setenv('FILA_EMAIL_SINCRONA', 'false')
    monkeypatch.setattr(consumidor, '_thread', None)
    monkeypatch.setattr(consumidor, '_parar', threading.Event())
    monkeypatch.setattr(consumidor.threading, 'Thread', ThreadFalsa)
    monkeypatch.setattr(consumidor.fila_email, 'registrar_app', apps.append)
    app = SimpleNamespace(testing=False)
    assert consumidor.iniciar(app) is True
    assert consumidor.iniciar(app) is False
    assert apps == [app]
    assert len(inicios) == 1
    assert inicios[0].kwargs['target'] is consumidor._laco
    consumidor.parar()
    assert consumidor._parar.is_set()


def test_hooks_nao_iniciam_consumidor_ao_importar(monkeypatch):
    chamadas = []
    monkeypatch.setattr(consumidor, 'iniciar', lambda app: chamadas.append(app))
    monkeypatch.setattr(consumidor, 'parar', lambda: chamadas.append('parou'))
    config = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'gunicorn.conf.py'))
    assert chamadas == []
    app = object()
    config['post_worker_init'](SimpleNamespace(wsgi=app))
    config['worker_exit'](None, None)
    assert chamadas == [app, 'parou']
