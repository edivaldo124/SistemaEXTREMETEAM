"""Sentry opcional (servicos/observabilidade.py): desligado sem SENTRY_DSN e sem PII.

O teste de ponta a ponta usa o SDK de verdade com um transporte que guarda o evento em
memória: nada sai para a rede.
"""

import json

import pytest
import sentry_sdk
from flask import Flask
from sentry_sdk.transport import Transport

from servicos import observabilidade
from servicos.observabilidade import before_breadcrumb, before_send

CPF = '529.982.247-25'
EMAIL = 'fulana.silva@example.com'


@pytest.fixture(autouse=True)
def sem_dsn(monkeypatch):
    monkeypatch.delenv('SENTRY_DSN', raising=False)


# --- Ligar e desligar --------------------------------------------------------------

def test_sem_dsn_nao_inicia(monkeypatch):
    def _nao_chamar(**_opcoes):
        raise AssertionError('sentry_sdk.init não deveria ser chamado sem SENTRY_DSN')

    monkeypatch.setattr(sentry_sdk, 'init', _nao_chamar)
    assert observabilidade.iniciar_sentry() is False
    monkeypatch.setenv('SENTRY_DSN', '   ')
    assert observabilidade.iniciar_sentry() is False


def test_com_dsn_inicia_sem_pii(monkeypatch):
    recebido = {}
    monkeypatch.setattr(sentry_sdk, 'init', lambda **opcoes: recebido.update(opcoes))
    monkeypatch.setenv('SENTRY_DSN', 'https://chave@o0.ingest.sentry.io/0')

    assert observabilidade.iniciar_sentry() is True
    assert recebido['send_default_pii'] is False
    assert recebido['include_local_variables'] is False
    assert recebido['max_request_body_size'] == 'never'
    assert recebido['before_send'] is before_send
    assert recebido['before_breadcrumb'] is before_breadcrumb
    assert recebido['traces_sample_rate'] == 0.0
    assert recebido['environment'] == 'producao'


# --- before_send ---------------------------------------------------------------------

def _evento():
    return {
        'message': f'Falha ao avisar {EMAIL} (CPF {CPF})',
        'user': {'ip_address': '200.1.2.3', 'email': EMAIL},
        'request': {
            'url': 'https://academia.example.test/recuperar_senha/tok-secreto-123',
            'method': 'POST',
            'query_string': 'code=codigo-oauth-xyz&state=estado-xyz',
            'cookies': {'session': 'cookie-da-sessao'},
            'data': {'cpfusuario': CPF, 'senhausuario': 'Senha-Forte-1'},
            'env': {'REMOTE_ADDR': '200.1.2.3'},
            'headers': {
                'Cookie': 'session=cookie-da-sessao', 'Authorization': 'Bearer token-mp',
                'X-CSRFToken': 'csrf-123', 'X-Forwarded-For': '200.1.2.3',
                'User-Agent': 'Mozilla/5.0 teste', 'Referer': 'https://academia.example.test/ativar-acesso/tok-convite',
            },
        },
        'exception': {'values': [{
            'type': 'IntegrityError',
            'value': (
                '(psycopg2.errors.UniqueViolation) duplicate key\n'
                '[SQL: INSERT INTO alunos (nome, cpf, telefone) VALUES (%(nome)s, %(cpf)s, %(telefone)s)]\n'
                "[parameters: {'nome': 'Fulana da Silva', 'cpf': '52998224725', 'telefone': '11988887777'}]\n"
                '(Background on this error at: https://sqlalche.me/e/20/gkpj)'
            ),
            'stacktrace': {'frames': [{'function': 'pagina_cadastro', 'vars': {'senha': 'Senha-Forte-1'}}]},
        }]},
        'breadcrumbs': {'values': [
            {'message': f'Convite enviado para {EMAIL}', 'category': 'log'},
            {'category': 'httplib', 'data': {
                'url': 'https://api.mercadopago.com/v1/payments', 'http.query': 'access_token=APP_USR-segredo',
            }},
        ]},
        'extra': {'contexto': f'aluno {CPF}'},
    }


def test_before_send_remove_pii():
    limpo = before_send(_evento(), {})
    texto = json.dumps(limpo, ensure_ascii=False)

    for vazado in (
        CPF, '52998224725', EMAIL, 'cookie-da-sessao', 'Bearer', 'token-mp', 'csrf-123', '200.1.2.3',
        'codigo-oauth-xyz', 'estado-xyz', 'Senha-Forte-1', 'tok-secreto-123', 'tok-convite',
        'Fulana da Silva', '11988887777', 'APP_USR-segredo',
    ):
        assert vazado not in texto, vazado

    requisicao = limpo['request']
    for chave in ('cookies', 'data', 'query_string', 'env'):
        assert chave not in requisicao
    assert 'user' not in limpo
    assert set(requisicao['headers']) == {'User-Agent', 'Referer'}
    assert requisicao['url'] == 'https://academia.example.test/recuperar_senha/[token]'


def test_before_send_preserva_o_que_ajuda_a_achar_o_erro():
    limpo = before_send(_evento(), {})
    assert limpo['message'] == 'Falha ao avisar [e-mail] (CPF [cpf])'
    excecao = limpo['exception']['values'][0]
    assert excecao['type'] == 'IntegrityError'
    assert 'UniqueViolation' in excecao['value'] and '[SQL: INSERT INTO alunos' in excecao['value']
    assert '[parameters: removidos]' in excecao['value']
    assert excecao['stacktrace']['frames'] == [{'function': 'pagina_cadastro'}]
    assert limpo['request']['method'] == 'POST'
    assert limpo['breadcrumbs']['values'][1]['data'] == {'url': 'https://api.mercadopago.com/v1/payments'}


def test_before_breadcrumb_mascara():
    rastro = before_breadcrumb({'message': f'login de {EMAIL}', 'data': {'http.query': 'token=x'}}, {})
    assert rastro == {'message': 'login de [e-mail]', 'data': {}}


@pytest.mark.parametrize('texto, esperado', [
    ('cpf 52998224725 fim', 'cpf [cpf] fim'),
    ('pedido 1234567890123 não é CPF', 'pedido 1234567890123 não é CPF'),
    ('/perfil/confirmar_email/abc.def-123?x=1', '/perfil/confirmar_email/[token]?x=1'),
    ('/admin/gmail/callback?state=s1&code=c2', '/admin/gmail/callback?state=[token]&code=[token]'),
])
def test_mascaras(texto, esperado):
    assert observabilidade.mascarar(texto) == esperado


# --- Ponta a ponta com o SDK real ----------------------------------------------------

class TransporteEmMemoria(Transport):
    def __init__(self, options=None):
        super().__init__(options)
        self.eventos = []

    def capture_envelope(self, envelope):
        for item in envelope.items:
            if item.type == 'event':
                self.eventos.append(item.payload.json)


@pytest.fixture
def sentry_em_memoria(monkeypatch):
    init_original = sentry_sdk.init
    transporte = TransporteEmMemoria()
    monkeypatch.setattr(sentry_sdk, 'init', lambda **opcoes: init_original(transport=transporte, **opcoes))
    monkeypatch.setenv('SENTRY_DSN', 'https://chave@o0.ingest.sentry.io/0')
    assert observabilidade.iniciar_sentry() is True
    yield transporte
    # Desliga de verdade. Não use sentry_sdk.init() sem argumentos aqui: ele lê
    # SENTRY_DSN do ambiente (que o monkeypatch ainda não restaurou) e passaria a enviar
    # os erros dos testes seguintes para a rede.
    sentry_sdk.get_client().close(timeout=0)
    sentry_sdk.get_global_scope().set_client(None)
    assert not sentry_sdk.get_client().is_active()


def test_erro_real_no_flask_chega_ao_sentry_sem_pii(sentry_em_memoria):
    mini = Flask('mini_sentry')

    @mini.route('/recuperar_senha/<token>', methods=['POST'])
    def quebra(token):
        # O token só aparece em URL (caminho, Referer, log "Exception on /..."), onde é
        # mascarado. Um token solto no texto de uma exceção não é reconhecível.
        raise RuntimeError(f'falhou para {CPF} / {EMAIL}')

    cliente = mini.test_client()
    cliente.set_cookie('session', 'cookie-da-sessao')
    resposta = cliente.post(
        '/recuperar_senha/tok-secreto-123?code=codigo-oauth-xyz',
        data={'cpf': '52998224725', 'email': EMAIL, 'senha': 'Senha-Forte-1'},
        headers={
            'Authorization': 'Bearer token-mp', 'X-CSRFToken': 'csrf-123',
            'X-Forwarded-For': '200.1.2.3', 'User-Agent': 'agente-de-teste',
        },
    )
    assert resposta.status_code == 500
    sentry_sdk.flush()

    [evento] = sentry_em_memoria.eventos
    # O Sentry anexa as linhas de código em volta de cada frame (pre_context etc.). Aqui
    # esse código é o próprio teste, que tem os valores falsos escritos nele; em produção
    # são linhas do sistema, nunca dados da requisição. Ficam de fora da comparação.
    for valor in evento['exception']['values']:
        for frame in valor['stacktrace']['frames']:
            for chave in ('pre_context', 'context_line', 'post_context'):
                frame.pop(chave, None)
    texto = json.dumps(evento, ensure_ascii=False)
    assert 'RuntimeError' in texto
    assert 'agente-de-teste' in texto
    for vazado in (
        CPF, '52998224725', EMAIL, 'cookie-da-sessao', 'token-mp', 'csrf-123', '200.1.2.3',
        'codigo-oauth-xyz', 'tok-secreto-123', 'Senha-Forte-1',
    ):
        assert vazado not in texto, vazado
    assert evento['transaction'] == 'quebra'
