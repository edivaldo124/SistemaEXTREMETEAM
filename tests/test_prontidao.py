"""/health/pronto: 503 quando banco ou Redis caem, sem expor detalhe nem criar sessão."""

import threading
import time

import pytest
from sqlalchemy.exc import OperationalError

from servicos import prontidao

SEGREDO = 'password authentication failed for user "academia" host=db senha=hunter2'


@pytest.fixture
def banco_fora(monkeypatch):
    def _falha(_app):
        raise OperationalError('SELECT 1', {}, Exception(SEGREDO))
    monkeypatch.setattr(prontidao, '_consultar_banco', _falha)


def test_liveness_continua_igual(client):
    resposta = client.get('/health')
    assert resposta.status_code == 200
    assert resposta.get_json() == {'status': 'ok'}


def test_pronto_com_banco_respondendo(client):
    resposta = client.get('/health/pronto')
    assert resposta.status_code == 200
    assert resposta.get_json() == {'status': 'ok', 'banco': 'ok'}
    assert resposta.headers['Cache-Control'] == 'no-store'


def test_banco_indisponivel_responde_503_sem_detalhe(client, banco_fora):
    resposta = client.get('/health/pronto')
    assert resposta.status_code == 503
    assert resposta.get_json() == {'status': 'indisponivel', 'banco': 'falha'}
    corpo = resposta.get_data(as_text=True)
    for trecho in ('password', 'hunter2', 'host=db', 'academia', 'OperationalError'):
        assert trecho not in corpo


def test_banco_travado_responde_503_dentro_do_prazo(client, monkeypatch):
    liberar = threading.Event()

    def _trava(_app):
        liberar.wait(10)

    monkeypatch.setattr(prontidao, '_consultar_banco', _trava)
    monkeypatch.setattr(prontidao, 'PRAZO_SEGUNDOS', 0.2)
    inicio = time.monotonic()
    try:
        resposta = client.get('/health/pronto')
    finally:
        liberar.set()
    assert resposta.status_code == 503
    assert time.monotonic() - inicio < 2


def test_redis_indisponivel_responde_503(client, app, monkeypatch):
    # Porta 1 recusa a conexão na hora: nada sai da máquina.
    monkeypatch.setitem(app.config, 'RATELIMIT_STORAGE_URI', 'redis://127.0.0.1:1/0')
    resposta = client.get('/health/pronto')
    assert resposta.status_code == 503
    assert resposta.get_json() == {'status': 'indisponivel', 'banco': 'ok', 'redis': 'falha'}
    assert '127.0.0.1' not in resposta.get_data(as_text=True)


def test_redis_respondendo(client, app, monkeypatch):
    import redis

    class RedisFalso:
        def ping(self):
            return True

        def close(self):
            pass

    monkeypatch.setitem(app.config, 'RATELIMIT_STORAGE_URI', 'redis://rate-limit:6379/0')
    monkeypatch.setattr(redis.Redis, 'from_url', classmethod(lambda cls, *a, **k: RedisFalso()))
    resposta = client.get('/health/pronto')
    assert resposta.status_code == 200
    assert resposta.get_json() == {'status': 'ok', 'banco': 'ok', 'redis': 'ok'}


def test_prazo_curto_no_cliente_redis(app, monkeypatch):
    import redis

    recebido = {}

    class RedisFalso:
        def ping(self):
            return True

        def close(self):
            pass

    def _from_url(cls, uri, **opcoes):
        recebido.update(opcoes)
        return RedisFalso()

    monkeypatch.setattr(redis.Redis, 'from_url', classmethod(_from_url))
    assert prontidao.redis_responde('redis://rate-limit:6379/0') is True
    assert recebido == {'socket_connect_timeout': 2, 'socket_timeout': 2}


def test_pronto_nao_cria_sessao(client, banco_fora):
    for caminho in ('/health/pronto', '/health'):
        resposta = client.get(caminho)
        assert 'Set-Cookie' not in resposta.headers, caminho


def test_pronto_tem_limite_por_ip(client):
    """Cada chamada consulta banco e Redis: 60 por minuto bastam ao monitor externo."""
    for _ in range(60):
        assert client.get('/health/pronto').status_code == 200
    assert client.get('/health/pronto').status_code == 429
    # O teto é por IP: o monitor, vindo de outro endereço, continua sendo atendido.
    outro_ip = client.get('/health/pronto', environ_base={'REMOTE_ADDR': '203.0.113.9'})
    assert outro_ip.status_code == 200
