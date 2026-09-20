import importlib.util
from pathlib import Path

import pytest
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import IntegrityError

from modelos.mercado_pago_conexao import MercadoPagoConexao

ARQUIVO = (
    Path(__file__).resolve().parent.parent
    / 'migrations/versions/a8c3e5f17b04_conexao_oauth_mercado_pago.py'
)


def _migracao():
    spec = importlib.util.spec_from_file_location('migracao_conexao_mp', ARQUIVO)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def test_migracao_cria_a_tabela_igual_ao_modelo_e_e_reentrante(tmp_path):
    migracao = _migracao()
    engine = create_engine(f'sqlite:///{tmp_path}/migracao.db')
    with engine.begin() as conn:
        with Operations.context(MigrationContext.configure(conn)):
            migracao.upgrade()
            migracao.upgrade()  # tolera a tabela já criada (banco vindo do create_all)

        colunas = {c['name']: c for c in inspect(conn).get_columns('mercado_pago_conexao')}
        assert set(colunas) == {c.name for c in MercadoPagoConexao.__table__.columns}
        for coluna in MercadoPagoConexao.__table__.columns:
            assert colunas[coluna.name]['nullable'] == coluna.nullable, coluna.name

        agora = '2026-09-19 00:00:00'
        valores = dict(mp='1', a='x', r='y', agora=agora)
        conn.execute(text(
            "INSERT INTO mercado_pago_conexao (id, mp_user_id, access_token_cifrado, refresh_token_cifrado,"
            " live_mode, expira_em, conectado_em, precisa_reconectar)"
            " VALUES (1, :mp, :a, :r, 1, :agora, :agora, 0)"
        ), valores)

    # uma única conta por academia: o CHECK id = 1 barra a segunda linha
    with pytest.raises(IntegrityError):
        with engine.begin() as conn:
            conn.execute(text(
                "INSERT INTO mercado_pago_conexao (id, mp_user_id, access_token_cifrado, refresh_token_cifrado,"
                " live_mode, expira_em, conectado_em, precisa_reconectar)"
                " VALUES (2, :mp, :a, :r, 1, :agora, :agora, 0)"
            ), valores)

    with engine.begin() as conn:
        with Operations.context(MigrationContext.configure(conn)):
            migracao.downgrade()
        assert 'mercado_pago_conexao' not in inspect(conn).get_table_names()
        with Operations.context(MigrationContext.configure(conn)):
            migracao.downgrade()  # sem a tabela, não falha


def test_migracao_encadeia_na_ultima_revisao_existente():
    migracao = _migracao()
    revisoes = {}
    for arquivo in ARQUIVO.parent.glob('*.py'):
        spec = importlib.util.spec_from_file_location(f'rev_{arquivo.stem}', arquivo)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        revisoes[modulo.revision] = modulo.down_revision

    assert migracao.down_revision in revisoes
    filhas = [rev for rev, pai in revisoes.items() if pai == migracao.down_revision]
    assert filhas == [migracao.revision], 'a cadeia de migrations ganhou um segundo head'
