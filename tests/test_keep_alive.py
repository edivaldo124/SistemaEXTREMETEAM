"""Garante que o keep-alive fica desligado por padrão e só pinga a própria origem."""

import pytest

from servicos import keep_alive


@pytest.fixture(autouse=True)
def ambiente_limpo(monkeypatch):
    monkeypatch.delenv('KEEP_ALIVE', raising=False)
    monkeypatch.delenv('KEEP_ALIVE_INTERVALO', raising=False)
    monkeypatch.setenv('APP_BASE_URL', 'https://academia.example.test')
    yield
    keep_alive.parar()


def test_desligado_por_padrao():
    assert keep_alive.iniciar() is False


@pytest.mark.parametrize('valor', ['false', 'no', '0', ''])
def test_nao_liga_com_valor_negativo(monkeypatch, valor):
    monkeypatch.setenv('KEEP_ALIVE', valor)
    assert keep_alive.iniciar() is False


def test_nao_liga_sem_origem_publica_valida(monkeypatch):
    monkeypatch.setenv('KEEP_ALIVE', 'true')
    monkeypatch.setenv('APP_BASE_URL', 'javascript:alert(1)')
    assert keep_alive.iniciar() is False


def test_liga_uma_unica_thread(monkeypatch):
    monkeypatch.setenv('KEEP_ALIVE', 'true')
    assert keep_alive.iniciar() is True
    # Segunda chamada não empilha outra thread no mesmo processo.
    assert keep_alive.iniciar() is False


@pytest.mark.parametrize(
    'configurado, esperado',
    [
        (None, keep_alive.INTERVALO_PADRAO),
        ('5', keep_alive.INTERVALO_MINIMO),
        ('99999', keep_alive.INTERVALO_MAXIMO),
        ('nao-e-numero', keep_alive.INTERVALO_PADRAO),
        ('300', 300),
    ],
)
def test_intervalo_fica_dentro_da_faixa(monkeypatch, configurado, esperado):
    if configurado is None:
        monkeypatch.delenv('KEEP_ALIVE_INTERVALO', raising=False)
    else:
        monkeypatch.setenv('KEEP_ALIVE_INTERVALO', configurado)
    assert keep_alive._intervalo() == esperado


def test_ping_usa_timeout_e_nao_segue_redirect(monkeypatch):
    chamadas = []

    class RespostaFake:
        status_code = 200

    def get_fake(url, **kwargs):
        chamadas.append((url, kwargs))
        return RespostaFake()

    monkeypatch.setattr(keep_alive.requests, 'get', get_fake)
    keep_alive._pingar('https://academia.example.test/health')

    (url, kwargs), = chamadas
    assert url == 'https://academia.example.test/health'
    assert kwargs['allow_redirects'] is False
    assert kwargs['timeout'] == keep_alive.TIMEOUT


def test_ping_engole_erro_de_rede(monkeypatch):
    def get_fake(url, **kwargs):
        raise keep_alive.requests.ConnectionError('sem rede')

    monkeypatch.setattr(keep_alive.requests, 'get', get_fake)
    keep_alive._pingar('https://academia.example.test/health')
