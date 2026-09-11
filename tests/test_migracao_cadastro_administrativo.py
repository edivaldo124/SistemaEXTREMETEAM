"""Verifica a migração em um banco isolado com o schema anterior e dados."""
import importlib

import pytest
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations


@pytest.fixture
def banco_antigo():
    engine = sa.create_engine('sqlite://')
    metadata = sa.MetaData()
    alunos = sa.Table(
        'alunos', metadata,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('cpf', sa.String(14), nullable=False, unique=True),
        sa.Column('login', sa.String(50), nullable=False, unique=True),
        sa.Column('email', sa.String(150), nullable=False, unique=True),
        sa.Column('senha_hash', sa.String(255), nullable=False),
    )
    pagamentos = sa.Table(
        'pagamentos', metadata,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('aluno_id', sa.Integer, sa.ForeignKey('alunos.id'), nullable=False),
    )
    metadata.create_all(engine)
    with engine.begin() as conn:
        conn.execute(alunos.insert().values(
            id=1, cpf='52998224725', login='veterano', email='veterano@example.com', senha_hash='hash-original',
        ))
        conn.execute(pagamentos.insert().values(id=1, aluno_id=1))
        migracao = importlib.import_module(
            'migrations.versions.e4b7c2a91d35_cadastro_administrativo_e_convite_de_acesso'
        )
        with Operations.context(MigrationContext.configure(conn)):
            yield conn, migracao
    engine.dispose()


def test_migracao_preserva_dados_constraints_e_relacoes(banco_antigo):
    conn, migracao = banco_antigo
    antes = conn.execute(sa.text('SELECT * FROM alunos')).all()
    migracao.upgrade()
    migracao.upgrade()  # schema já atualizado, inclusive após create_all
    assert conn.execute(sa.text('SELECT id, cpf, login, email, senha_hash FROM alunos')).all() == antes
    assert conn.execute(sa.text('SELECT aluno_id FROM pagamentos')).scalar_one() == 1
    uniques = {tuple(c['column_names']) for c in sa.inspect(conn).get_unique_constraints('alunos')}
    assert {('cpf',), ('login',), ('email',)} <= uniques
    conn.execute(sa.text("INSERT INTO alunos (id, cpf) VALUES (2, '00000000001'), (3, '00000000002')"))
    with pytest.raises(RuntimeError, match='sem conta de acesso'):
        migracao.downgrade()
    assert conn.execute(sa.text('SELECT COUNT(*) FROM alunos')).scalar_one() == 3
    assert 'token_convite_hash' in {c['name'] for c in sa.inspect(conn).get_columns('alunos')}
    conn.execute(sa.text("UPDATE alunos SET login='aluno-' || id, email='email-' || id, senha_hash='hash' WHERE id > 1"))
    migracao.downgrade()
    colunas = {c['name']: c for c in sa.inspect(conn).get_columns('alunos')}
    assert 'token_convite_hash' not in colunas
    assert all(not colunas[n]['nullable'] for n in ('login', 'email', 'senha_hash'))
    assert conn.execute(sa.text('SELECT COUNT(*) FROM alunos')).scalar_one() == 3
    assert conn.execute(sa.text('PRAGMA foreign_key_check')).all() == []
