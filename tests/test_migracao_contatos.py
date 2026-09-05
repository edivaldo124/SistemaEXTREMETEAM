import importlib.util
from pathlib import Path

from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import create_engine, inspect, text


def test_migracao_preserva_professor_e_inicia_perfil_privado(tmp_path):
    arquivo = Path(__file__).resolve().parent.parent / 'migrations/versions/d9e2f6a14c80_contatos_academia_perfis_professores.py'
    spec = importlib.util.spec_from_file_location('migracao_contatos', arquivo)
    migracao = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migracao)
    engine = create_engine(f'sqlite:///{tmp_path}/migracao.db')
    with engine.begin() as conn:
        conn.execute(text('CREATE TABLE professores (id INTEGER PRIMARY KEY, nome VARCHAR(150), login VARCHAR(50), senha_hash VARCHAR(255))'))
        conn.execute(text("INSERT INTO professores VALUES (1, 'Professor existente', 'login-antigo', 'hash-intacto')"))
        with Operations.context(MigrationContext.configure(conn)):
            migracao.upgrade()
            migracao.upgrade()  # tolera tabelas criadas pelo create_all do servidor
        linha = conn.execute(text('SELECT nome, login, senha_hash, perfil_publico, exibir_email, exibir_instagram, exibir_whatsapp FROM professores')).one()
        assert tuple(linha) == ('Professor existente', 'login-antigo', 'hash-intacto', 0, 0, 0, 0)
        assert 'academia' in inspect(conn).get_table_names()
        with Operations.context(MigrationContext.configure(conn)):
            migracao.downgrade()
        assert {c['name'] for c in inspect(conn).get_columns('professores')} == {'id', 'nome', 'login', 'senha_hash'}
        assert conn.execute(text('SELECT senha_hash FROM professores')).scalar() == 'hash-intacto'
