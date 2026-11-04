"""Turnstile da Cloudflare no cadastro público (SEC-36).

O cadastro manda e-mail para o endereço digitado, e o limite por IP precisa ser folgado
porque a academia inteira sai pelo mesmo Wi-Fi (SEC-17). A suíte nunca fala com a
Cloudflare: o siteverify é um duplo que devolve o que cada teste mandar e guarda o que
recebeu.
"""
import re

import pytest
import requests

import servicos.turnstile as turnstile
from modelos.email_pendente import EmailPendente
from modelos.usuario import Aluno

CHAVE_SITE = '0x4AAAAAAAchave-de-teste'
HOST = 'academia.example.test'
TOKEN = 'token-de-teste-do-widget'

FORMULARIO = {
    'nomeusuario': 'Pessoa Nova', 'loginusuario': 'pessoa-nova', 'dataNascimento': '2000-01-01',
    'cpfusuario': '529.982.247-25', 'senhausuario': 'Treino-Forte-2026',
    'confirmarsenhausuario': 'Treino-Forte-2026', 'emailusuario': 'nova@example.com',
    'telefoneusuario': '11999999999', 'descricaousuario': '',
    'aceite_termos_responsabilidade': 'aceito',
}


def _cadastrar(client, **campos):
    return client.post('/cadastrar', data={**FORMULARIO, **campos})


class _Resposta:
    def __init__(self, corpo, status=200):
        self.corpo = corpo
        self.status_code = status

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f'{self.status_code}')

    def json(self):
        if isinstance(self.corpo, Exception):
            raise self.corpo
        return self.corpo


class _Siteverify:
    def __init__(self):
        self.chamadas = []
        self.resposta = _Resposta({'success': True, 'action': turnstile.ACAO_CADASTRO, 'hostname': HOST})

    def __call__(self, url, data=None, timeout=None, **_kwargs):
        self.chamadas.append({'url': url, 'data': data, 'timeout': timeout})
        if isinstance(self.resposta, Exception):
            raise self.resposta
        return self.resposta


@pytest.fixture
def siteverify(monkeypatch):
    monkeypatch.setenv('TURNSTILE_SITEKEY', CHAVE_SITE)
    monkeypatch.setenv('TURNSTILE_SECRET', 'segredo-de-teste-turnstile')
    # Lista por vírgula, como TRUSTED_HOSTS; espaços em volta não contam.
    monkeypatch.setenv('TURNSTILE_HOSTNAMES', f' {HOST} , outro-site.example.test')
    duplo = _Siteverify()
    monkeypatch.setattr(turnstile.requests, 'post', duplo)
    return duplo


def test_cadastro_com_token_valido_segue_o_fluxo_de_sempre(client, contexto_app, sem_email, siteverify):
    resposta = _cadastrar(client, **{'cf-turnstile-response': TOKEN})

    assert resposta.status_code == 302
    assert resposta.location == '/cadastro/obrigado'
    assert Aluno.query.filter_by(email='nova@example.com').count() == 1
    assert [e['para'] for e in sem_email] == ['nova@example.com']
    [chamada] = siteverify.chamadas
    assert chamada['url'] == 'https://challenges.cloudflare.com/turnstile/v0/siteverify'
    assert chamada['data'] == {
        'secret': 'segredo-de-teste-turnstile', 'response': TOKEN, 'remoteip': '127.0.0.1',
    }
    assert chamada['timeout'] == 10


def test_cadastro_sem_token_nao_cria_conta_nem_manda_email(client, contexto_app, sem_email, siteverify):
    resposta = _cadastrar(client)

    assert resposta.status_code == 403
    assert 'verificação de segurança' in resposta.get_data(as_text=True)
    # O formulário volta preenchido (menos as senhas), como nos outros erros.
    assert 'value="Pessoa Nova"' in resposta.get_data(as_text=True)
    assert Aluno.query.count() == 0
    assert sem_email == []
    assert EmailPendente.query.count() == 0
    assert siteverify.chamadas == []


@pytest.mark.parametrize('resultado', [
    {'success': False, 'error-codes': ['timeout-or-duplicate']},
    # Token de outro widget da mesma conta, ou tirado em outra tela.
    {'success': True, 'action': 'login', 'hostname': HOST},
    {'success': True, 'hostname': HOST},
    # Token emitido para um site que não é este.
    {'success': True, 'action': turnstile.ACAO_CADASTRO, 'hostname': 'golpe.example'},
    # Só `True` vale: um "sucesso" em texto não passa.
    {'success': 'true', 'action': turnstile.ACAO_CADASTRO, 'hostname': HOST},
    ['nao', 'e', 'objeto'],
])
def test_token_recusado_pela_cloudflare_nao_cria_conta(client, contexto_app, sem_email, siteverify, resultado):
    siteverify.resposta = _Resposta(resultado)

    resposta = _cadastrar(client, **{'cf-turnstile-response': TOKEN})

    assert resposta.status_code == 403
    assert Aluno.query.count() == 0
    assert sem_email == []


@pytest.mark.parametrize('falha', [
    requests.Timeout('demorou'),
    requests.ConnectionError('sem rede'),
    _Resposta({'success': True}, status=500),
    _Resposta(ValueError('não é JSON')),
])
def test_siteverify_fora_do_ar_recusa_o_cadastro(client, contexto_app, sem_email, siteverify, falha):
    siteverify.resposta = falha

    resposta = _cadastrar(client, **{'cf-turnstile-response': TOKEN})

    assert resposta.status_code == 403
    assert Aluno.query.count() == 0
    assert sem_email == []


def test_token_grande_demais_nem_chega_a_cloudflare(client, contexto_app, siteverify):
    resposta = _cadastrar(client, **{'cf-turnstile-response': 'x' * 2049})

    assert resposta.status_code == 403
    assert siteverify.chamadas == []
    assert Aluno.query.count() == 0


def test_tela_de_cadastro_mostra_o_widget_com_a_acao_que_o_servidor_confere(client, siteverify):
    resposta = client.get('/cadastrar')
    html = resposta.get_data(as_text=True)
    politica = resposta.headers['Content-Security-Policy']

    assert f'data-sitekey="{CHAVE_SITE}"' in html
    assert f'data-action="{turnstile.ACAO_CADASTRO}"' in html
    # O api.js leva o nonce da própria resposta: é como a Cloudflare recomenda com CSP.
    nonce = re.search(r"'nonce-([^']+)'", politica).group(1)
    assert re.search(
        rf'<script src="https://challenges\.cloudflare\.com/turnstile/v0/api\.js"[^>]*nonce="{re.escape(nonce)}"',
        html,
    )
    assert re.search(r"script-src [^;]*https://challenges\.cloudflare\.com", politica)
    assert 'frame-src https://challenges.cloudflare.com' in politica


def test_cloudflare_so_entra_na_tela_de_cadastro(client, siteverify):
    for caminho in ('/login', '/recuperar_senha', '/'):
        resposta = client.get(caminho)
        assert 'challenges.cloudflare.com' not in resposta.headers['Content-Security-Policy'], caminho
        assert 'challenges.cloudflare.com' not in resposta.get_data(as_text=True), caminho


def test_politica_de_privacidade_descreve_o_turnstile(client):
    # LGPD (transparência): o cadastro passa a mandar IP e dados do navegador à Cloudflare.
    politica = client.get('/politica-privacidade').get_data(as_text=True)

    assert 'href="#secao-8"' in politica
    assert 'Verificação contra robôs no cadastro' in politica
    assert 'nunca são enviados à Cloudflare' in politica
    assert 'https://www.cloudflare.com/turnstile-privacy-policy/' in politica


def test_sem_turnstile_configurado_nada_carrega(client, contexto_app, sem_email):
    # Desenvolvimento e suíte: sem as variáveis, nem script, nem CSP, nem checagem.
    # Em produção o arranque recusa subir assim (tests/test_arranque_seguranca.py).
    resposta = client.get('/cadastrar')
    assert 'challenges.cloudflare.com' not in resposta.headers['Content-Security-Policy']
    assert 'cf-turnstile' not in resposta.get_data(as_text=True)

    assert _cadastrar(client).status_code == 302
    assert Aluno.query.count() == 1
