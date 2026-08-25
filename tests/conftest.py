import os
import tempfile
from datetime import date, timedelta

# Precisa rodar ANTES de qualquer "import servidor": servidor.py chama load_dotenv()
# (que nao sobrescreve env vars ja definidas) e db.create_all() no import do modulo,
# executado uma unica vez por processo de teste. NUNCA rode pytest num shell/container
# onde o DATABASE_URL real (Postgres) ja esteja exportado - setdefault perde para ele.
_DIR_TESTE = tempfile.mkdtemp(prefix='extremeteam-testes-')
os.environ.setdefault('SECRET_KEY', 'chave-de-teste-nao-usar-em-producao')
os.environ.setdefault('DATABASE_URL', f'sqlite:///{_DIR_TESTE}/teste.db')
os.environ.setdefault('MERCADO_PAGO_ACCESS_TOKEN', 'token-fake-de-teste')
os.environ.setdefault('MERCADO_PAGO_WEBHOOK_SECRET', 'segredo-fake-de-teste')

import pytest

from config import db
from dao.planoDAO import PlanoDAO
from dao.usuarioDAO import AlunoDAO
from dao.financeiroDAO import PagamentoDAO
from modelos.pagamento import Pagamento
from modelos.plano import Plano
from modelos.usuario import Aluno
from servidor import app as flask_app


@pytest.fixture
def app():
    flask_app.config.update(TESTING=True)
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def limpar_banco(app):
    yield
    with app.app_context():
        db.session.rollback()
        for tabela in reversed(db.metadata.sorted_tables):
            db.session.execute(tabela.delete())
        db.session.commit()


@pytest.fixture
def contexto_app(app):
    with app.app_context():
        yield


@pytest.fixture
def plano(contexto_app):
    novo_plano = Plano(nome_plano='Mensal', preco_plano=150.0, duracao_dias=30)
    PlanoDAO.salvar(novo_plano)
    return novo_plano


@pytest.fixture
def criar_aluno(contexto_app):
    contador = {'n': 0}

    def _criar(**overrides):
        contador['n'] += 1
        i = contador['n']
        dados = dict(
            nome=f'Aluno Teste {i}',
            login=f'aluno{i}',
            datanascimento='2000-01-01',
            cpf=f'{i:011d}',
            email=f'aluno{i}@example.com',
            telefone='11999999999',
            senha='senha123',
            descricao='',
            status_cadastro='aprovado',
            ativo=True,
        )
        dados.update(overrides)
        aluno = Aluno(**dados)
        AlunoDAO.salvar(aluno)
        return aluno

    return _criar


@pytest.fixture
def criar_pagamento(contexto_app, plano, criar_aluno):
    def _criar(aluno=None, **overrides):
        aluno = aluno or criar_aluno()
        dados = dict(
            aluno_id=aluno.id,
            plano_id=plano.id,
            valor=150.0,
            vencimento=date.today() + timedelta(days=5),
            status='pendente',
        )
        dados.update(overrides)
        pagamento = Pagamento(**dados)
        PagamentoDAO.salvar(pagamento)
        return pagamento

    return _criar


@pytest.fixture
def logar_como_aluno(client):
    def _logar(aluno):
        with client.session_transaction() as sess:
            sess['usuario'] = aluno.login
            sess['aluno_id'] = aluno.id
            sess['tipo_usuario'] = 'aluno'
    return _logar


@pytest.fixture
def logar_como_admin(client):
    def _logar():
        with client.session_transaction() as sess:
            sess['usuario'] = 'admin-teste'
            sess['tipo_usuario'] = 'admin'
    return _logar
