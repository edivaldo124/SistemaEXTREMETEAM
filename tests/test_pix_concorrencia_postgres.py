"""Regressão com trava de linha real, opcional na suíte que usa SQLite.

Execute com TEST_POSTGRES_URL apontando explicitamente para um PostgreSQL de
teste local. Cada caso cria e remove somente seu próprio schema aleatório;
nenhuma tabela preexistente é utilizada. O Mercado Pago é inteiramente simulado.
"""

import importlib
import os
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta

import pytest
from flask import Flask
from sqlalchemy import create_engine, event, text
from sqlalchemy.engine import make_url

from config import db, limiter
from modelos.pagamento import Pagamento
from modelos.pagamento_evento import PagamentoEvento
from modelos.plano import Plano
from modelos.usuario import Aluno

pix_modulo = importlib.import_module('blueprints.pix_bp')


@pytest.fixture
def postgres_pix(monkeypatch):
    url_texto = os.environ.get('TEST_POSTGRES_URL')
    if not url_texto:
        pytest.skip('Requer TEST_POSTGRES_URL para PostgreSQL de teste local.')

    url = make_url(url_texto)
    host = url.query.get('host', url.host) or ''
    if url.get_backend_name() != 'postgresql' or not (
        host in ('localhost', '127.0.0.1', '::1') or host.startswith('/tmp/')
    ):
        pytest.fail('TEST_POSTGRES_URL deve indicar explicitamente PostgreSQL local de teste.')

    schema = f'teste_pix_{uuid.uuid4().hex}'
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
        WTF_CSRF_ENABLED=False,
    )
    # Este caso mede transações; os limites têm testes próprios na aplicação real.
    monkeypatch.setattr(limiter, 'enabled', False)
    db.init_app(app)
    app.register_blueprint(pix_modulo.pix_bp)
    engine = None
    try:
        with app.app_context():
            engine = db.engine
            db.create_all()
        yield app, engine, administracao, schema
    finally:
        with app.app_context():
            db.session.remove()
        if engine is not None:
            engine.dispose()
        with administracao.connect() as conn:
            conn.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
        administracao.dispose()


@pytest.mark.parametrize('situacao', ['sem_pix', 'pix_expirado', 'pix_rejeitado'])
def test_duas_requisicoes_pix_reutilizam_uma_cobranca_postgres(postgres_pix, monkeypatch, situacao):
    app, engine, administracao, schema = postgres_pix
    with app.app_context():
        plano = Plano(nome_plano='Semanal', preco_plano=7, duracao_dias=7)
        aluno = Aluno(
            nome='Aluno de teste', login='aluno-pg', datanascimento='2000-01-01',
            cpf='00000000000', email='aluno-pg@example.test', telefone='',
            senha='senha-de-teste', descricao='', status_cadastro='aprovado',
        )
        db.session.add_all([plano, aluno])
        db.session.flush()
        pagamento = Pagamento(
            aluno_id=aluno.id, plano_id=plano.id, valor=7,
            vencimento=date.today() + timedelta(days=1),
        )
        if situacao != 'sem_pix':
            pagamento.provider = 'mercado_pago'
            pagamento.provider_payment_id = 'pix-antigo'
            pagamento.external_reference = 'referencia-antiga'
            pagamento.pix_copia_cola = 'copia-e-cola-antigo'
            pagamento.data_expiracao = datetime.utcnow() + timedelta(
                minutes=-1 if situacao == 'pix_expirado' else 30,
            )
        db.session.add(pagamento)
        db.session.commit()
        pagamento_id, aluno_id = pagamento.id, aluno.id

    entrou_na_criacao = threading.Event()
    liberar_criacao = threading.Event()
    segunda_enviou_select = threading.Event()
    segunda_obteve_trava = threading.Event()
    estado_lock = threading.Lock()
    criacoes = []
    cancelamentos = []
    referencias = {}

    def criar_pix(**kwargs):
        with estado_lock:
            criacoes.append(kwargs)
            provider_id = f'pix-novo-{len(criacoes)}'
            referencias[provider_id] = kwargs['external_reference']
        entrou_na_criacao.set()
        assert liberar_criacao.wait(timeout=12), 'Teste não liberou a criação simulada.'
        return {
            'sucesso': True, 'payment_id': provider_id, 'status': 'pending',
            'qr_code': f'copia-e-cola-{provider_id}', 'qr_code_base64': None,
            'ticket_url': None, 'data_expiracao': datetime.utcnow() + timedelta(minutes=30),
        }

    def buscar_pix(provider_id, **kwargs):
        if provider_id == 'pix-antigo':
            return {
                'sucesso': True, 'status': 'rejected',
                'external_reference': 'referencia-antiga',
                'transaction_amount': 7, 'currency_id': 'BRL',
            }
        return {
            'sucesso': True, 'status': 'pending',
            'external_reference': referencias[provider_id],
            'transaction_amount': 7, 'currency_id': 'BRL',
        }

    monkeypatch.setattr(pix_modulo, 'criar_pagamento_pix', criar_pix)
    monkeypatch.setattr(pix_modulo, 'buscar_pagamento', buscar_pix)
    monkeypatch.setattr(pix_modulo, 'cancelar_pagamento', lambda provider_id: cancelamentos.append(provider_id))

    def antes_select(conn, cursor, statement, parameters, context, executemany):
        if threading.current_thread().name == 'pix-segundo' and 'FOR UPDATE' in statement.upper():
            segunda_enviou_select.set()

    def depois_select(conn, cursor, statement, parameters, context, executemany):
        if threading.current_thread().name == 'pix-segundo' and 'FOR UPDATE' in statement.upper():
            segunda_obteve_trava.set()

    event.listen(engine, 'before_cursor_execute', antes_select)
    event.listen(engine, 'after_cursor_execute', depois_select)

    def requisitar(nome):
        threading.current_thread().name = nome
        with app.test_client() as client:
            with client.session_transaction() as sessao:
                sessao.update(usuario='aluno-pg', aluno_id=aluno_id, tipo_usuario='aluno')
            resposta = client.post(f'/api/mensalidades/{pagamento_id}/pix')
            return resposta.status_code, resposta.get_json()

    try:
        with ThreadPoolExecutor(max_workers=2) as executor:
            primeira = executor.submit(requisitar, 'pix-primeiro')
            try:
                assert entrou_na_criacao.wait(timeout=5), 'Primeira requisição não chegou à criação.'
                segunda = executor.submit(requisitar, 'pix-segundo')
                assert segunda_enviou_select.wait(timeout=5), 'Segunda requisição não usou SELECT FOR UPDATE.'
                # Observar o servidor evita confundir demora de agendamento da thread
                # com bloqueio: o próprio PostgreSQL deve informar espera por trava.
                bloqueou = False
                prazo = time.monotonic() + 5
                with administracao.connect() as conn:
                    while time.monotonic() < prazo:
                        bloqueou = bool(conn.execute(text(
                            'SELECT EXISTS (SELECT 1 FROM pg_stat_activity '
                            "WHERE application_name = :schema AND wait_event_type = 'Lock' "
                            'AND cardinality(pg_blocking_pids(pid)) > 0)'
                        ), {'schema': schema}).scalar())
                        if bloqueou:
                            break
                        time.sleep(0.02)
                assert bloqueou, 'PostgreSQL não bloqueou a segunda requisição na linha da cobrança.'
                assert not segunda_obteve_trava.is_set()
                assert len(criacoes) == 1
            finally:
                liberar_criacao.set()
            respostas = [primeira.result(timeout=10), segunda.result(timeout=10)]
    finally:
        liberar_criacao.set()
        event.remove(engine, 'before_cursor_execute', antes_select)
        event.remove(engine, 'after_cursor_execute', depois_select)

    assert segunda_obteve_trava.is_set()
    assert len(criacoes) == 1
    assert cancelamentos == ([] if situacao == 'sem_pix' else ['pix-antigo'])
    assert [codigo for codigo, _ in respostas] == [200, 200]
    assert [dados['pix_copia_cola'] for _, dados in respostas] == ['copia-e-cola-pix-novo-1'] * 2
    with app.app_context():
        salvo = db.session.get(Pagamento, pagamento_id)
        assert salvo.provider_payment_id == 'pix-novo-1'
        assert PagamentoEvento.query.filter_by(pagamento_id=pagamento_id, tipo='pix_gerado').count() == 1
