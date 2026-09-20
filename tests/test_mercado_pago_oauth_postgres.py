"""Renovação do token OAuth com trava de linha real, opcional na suíte que usa SQLite.

O refresh_token do Mercado Pago é de uso único: se dois processos o gastassem ao mesmo
tempo, um deles receberia `invalid_grant` e marcaria a conexão como quebrada sem que
nada tivesse dado errado. Só o PostgreSQL aplica `SELECT ... FOR UPDATE`, então este
caso exige TEST_POSTGRES_URL apontando para um PostgreSQL local de teste (mesma regra de
test_pix_concorrencia_postgres.py). Cada execução cria e remove só o próprio schema, e o
Mercado Pago é inteiramente simulado.
"""

import os
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

import pytest
from flask import Flask
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

from config import db
from modelos.mercado_pago_conexao import MercadoPagoConexao
from servicos import mercado_pago_conta as conta


class _Resposta:
    status_code = 200

    def __init__(self, corpo):
        self._corpo = corpo

    def json(self):
        return self._corpo


@pytest.fixture
def postgres_mp():
    url_texto = os.environ.get('TEST_POSTGRES_URL')
    if not url_texto:
        pytest.skip('Requer TEST_POSTGRES_URL para PostgreSQL de teste local.')

    url = make_url(url_texto)
    host = url.query.get('host', url.host) or ''
    if url.get_backend_name() != 'postgresql' or not (
        host in ('localhost', '127.0.0.1', '::1') or host.startswith('/tmp/') or host.startswith('/var/run/')
    ):
        pytest.fail('TEST_POSTGRES_URL deve indicar explicitamente PostgreSQL local de teste.')

    schema = f'teste_mp_oauth_{uuid.uuid4().hex}'
    administracao = create_engine(url, isolation_level='AUTOCOMMIT')
    with administracao.connect() as conn:
        conn.execute(text(f'CREATE SCHEMA "{schema}"'))

    app = Flask(__name__)
    app.config.update(
        TESTING=True,
        SECRET_KEY='chave-exclusiva-do-teste-postgres',
        SQLALCHEMY_DATABASE_URI=url,
        SQLALCHEMY_ENGINE_OPTIONS={
            'connect_args': {
                'options': f'-csearch_path={schema} -clock_timeout=10000 -cstatement_timeout=15000',
                'application_name': schema,
            },
        },
    )
    db.init_app(app)
    engine = None
    try:
        with app.app_context():
            engine = db.engine
            db.create_all()
        yield app
    finally:
        with app.app_context():
            db.session.remove()
        if engine is not None:
            engine.dispose()
        with administracao.connect() as conn:
            conn.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
        administracao.dispose()


def test_dois_processos_perto_do_vencimento_gastam_o_refresh_token_uma_vez(postgres_mp, monkeypatch):
    app = postgres_mp
    monkeypatch.setenv('MERCADO_PAGO_CLIENT_ID', 'app-123')
    monkeypatch.setenv('MERCADO_PAGO_CLIENT_SECRET', 'segredo-do-app')
    monkeypatch.delenv('MERCADO_PAGO_TOKEN_KEY', raising=False)

    with app.app_context():
        conta.salvar_conexao({
            'access_token': 'acesso-1', 'refresh_token': 'refresh-1', 'expires_in': 15552000,
            'user_id': '123456', 'public_key': None, 'live_mode': True,
        })
        conexao = db.session.get(MercadoPagoConexao, 1)
        conexao.expira_em = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(days=3)
        db.session.commit()

    chamadas = []
    trava = threading.Lock()

    def _post(url, json=None, headers=None, timeout=None):
        with trava:
            chamadas.append(json['refresh_token'])
            numero = len(chamadas)
        time.sleep(0.4)  # janela larga o bastante para a outra thread chegar durante a renovação
        return _Resposta({
            'access_token': f'acesso-{numero + 1}', 'refresh_token': f'refresh-{numero + 1}',
            'expires_in': 15552000, 'user_id': 123456, 'live_mode': True,
        })

    monkeypatch.setattr(conta.requests, 'post', _post)
    largada = threading.Barrier(2)

    def _pedir_token():
        with app.app_context():
            largada.wait(timeout=5)
            return conta.access_token_vigente()

    with ThreadPoolExecutor(max_workers=2) as pool:
        tokens = list(pool.map(lambda _: _pedir_token(), range(2)))

    assert chamadas == ['refresh-1'], 'o refresh_token de uso único foi gasto mais de uma vez'
    assert tokens == ['acesso-2', 'acesso-2']
    with app.app_context():
        linha = db.session.get(MercadoPagoConexao, 1)
        assert conta._decifrar(linha.refresh_token_cifrado) == 'refresh-2'
        assert linha.precisa_reconectar is False
