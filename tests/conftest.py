import os
import tempfile
from datetime import date, timedelta

# Precisa rodar ANTES de qualquer "import servidor": servidor.py chama load_dotenv()
# (que nao sobrescreve env vars ja definidas) e db.create_all() no import do modulo,
# executado uma unica vez por processo de teste. NUNCA rode pytest num shell/container
# onde o DATABASE_URL real (Postgres) ja esteja exportado - setdefault perde para ele.
_DIR_TESTE = tempfile.mkdtemp(prefix='extremeteam-testes-')
os.environ['SECRET_KEY'] = 'chave-de-teste-nao-usar-em-producao'
os.environ['DATABASE_URL'] = f'sqlite:///{_DIR_TESTE}/teste.db'
os.environ['MERCADO_PAGO_ACCESS_TOKEN'] = 'token-fake-de-teste'
os.environ['MERCADO_PAGO_WEBHOOK_SECRET'] = 'segredo-fake-de-teste'
os.environ['APP_BASE_URL'] = 'https://academia.example.test'
os.environ['TRUSTED_HOSTS'] = 'localhost,academia.example.test'
os.environ['TRUST_PROXY_COUNT'] = '0'
os.environ['RATELIMIT_STORAGE_URI'] = 'memory://'
# Sem isto, `servicos.armazenamento` cai no padrão 'uploads' e a suíte grava fotos e
# comprovantes de teste DENTRO da pasta real do projeto, misturados aos arquivos de
# alunos de verdade. Aponta para o mesmo diretório temporário descartável do banco.
os.environ['UPLOAD_DIR'] = os.path.join(_DIR_TESTE, 'uploads')
# Credencial administrativa descartável: servidor.py agora recusa subir sem nenhuma.
os.environ.setdefault('ADMIN_USER', 'admin-teste')
os.environ.setdefault('ADMIN_PASSWORD', 'senha-de-teste-nao-usar-em-producao')
# A suíte não roda migrations: o schema do SQLite descartável sai direto dos modelos.
os.environ['CRIAR_SCHEMA_NA_IMPORTACAO'] = 'true'
# A fila de e-mail é drenada pelo próprio teste, nunca por uma thread de fundo.
os.environ['FILA_EMAIL_SINCRONA'] = 'true'

import pytest

from config import db, limiter
from dao.planoDAO import PlanoDAO
from dao.usuarioDAO import AlunoDAO
from dao.financeiroDAO import PagamentoDAO
from modelos.pagamento import Pagamento
from modelos.plano import Plano
from modelos.usuario import Aluno
from servidor import app as flask_app


@pytest.fixture
def app():
    flask_app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def limpar_banco(app):
    limiter.reset()
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
def sem_email(monkeypatch):
    """Substitui o provedor de e-mail em todos os módulos que o chamam.

    A suíte nunca deve alcançar a rede: sem a chave do Brevo `enviar_email` já sai
    antes do POST, mas o duplo torna isso explícito e devolve os envios ao teste.
    """
    import blueprints.adm_bp as adm_bp
    import blueprints.usuario_bp as usuario_bp
    import servicos.convites as convites
    import servicos.email as servico_email
    import servicos.fila_email as fila_email

    enviados = []

    def _falso(destinatario, nome_destinatario, assunto, *_args, **_kwargs):
        enviados.append({'para': destinatario, 'assunto': assunto})
        return True

    for modulo in (servico_email, usuario_bp, adm_bp, convites, fila_email):
        if hasattr(modulo, 'enviar_email'):
            monkeypatch.setattr(modulo, 'enviar_email', _falso)
    return enviados


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


# A sessão carrega a "impressão" da credencial usada no login, e as rotas protegidas a
# conferem a cada requisição (ver servicos/autorizacao.py). As fixtures precisam montar a
# sessão como o login real monta - sem o carimbo, nenhuma rota protegida abre.
@pytest.fixture
def logar_como_aluno(client):
    from servicos.autorizacao import impressao_credencial

    def _logar(aluno):
        with client.session_transaction() as sess:
            sess['usuario'] = aluno.login
            sess['aluno_id'] = aluno.id
            sess['tipo_usuario'] = 'aluno'
            sess['credencial'] = impressao_credencial(aluno.senha_hash)
    return _logar


@pytest.fixture
def logar_como_professor(client):
    from servicos.autorizacao import impressao_credencial

    def _logar(professor):
        with client.session_transaction() as sess:
            sess['usuario'] = professor.login
            sess['professor_id'] = professor.id
            sess['tipo_usuario'] = 'professor'
            sess['credencial'] = impressao_credencial(professor.senha_hash)
    return _logar


@pytest.fixture
def logar_como_admin(client):
    from servicos.autorizacao import impressao_credencial
    from servicos.credenciais import referencia_credencial_admin

    def _logar():
        with client.session_transaction() as sess:
            sess['usuario'] = os.environ['ADMIN_USER']
            sess['tipo_usuario'] = 'admin'
            sess['credencial'] = impressao_credencial(referencia_credencial_admin())
    return _logar
