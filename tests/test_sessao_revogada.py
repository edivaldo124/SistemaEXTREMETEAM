import importlib.util
from datetime import datetime, timedelta
from pathlib import Path

from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import create_engine, inspect

from config import db
from modelos.sessao_revogada import SessaoRevogada

ARQUIVO_MIGRACAO = (
    Path(__file__).resolve().parent.parent / 'migrations/versions/b5d9c3e71a26_sessoes_revogadas.py'
)
SENHA_ADMIN = 'senha-de-teste-nao-usar-em-producao'


def _entrar_como_admin(client):
    resposta = client.post('/login', data={'loginusuario': 'admin-teste', 'senhausuario': SENHA_ADMIN})
    assert resposta.status_code == 302 and resposta.headers['Location'].endswith('/admin')
    return client.get_cookie('session').value


def _cliente_com_cookie(app, valor):
    outro = app.test_client()
    outro.set_cookie('session', valor, domain='localhost')
    return outro


def test_logout_revoga_a_copia_do_cookie_feita_antes(app, client):
    """`session.clear()` só limpava o navegador de quem saiu; a cópia do cookie seguia valendo."""
    copia = _entrar_como_admin(client)
    atacante = _cliente_com_cookie(app, copia)
    assert atacante.get('/admin').status_code == 200

    assert client.post('/logout').status_code == 302

    resposta = _cliente_com_cookie(app, copia).get('/admin')
    assert resposta.status_code == 302
    assert resposta.headers['Location'].endswith('/login')


def test_logout_de_uma_sessao_nao_derruba_as_outras(app, client):
    _entrar_como_admin(client)
    outro_aparelho = app.test_client()
    _entrar_como_admin(outro_aparelho)

    client.post('/logout')

    assert outro_aparelho.get('/admin').status_code == 200


def test_sessao_sem_identificador_e_recusada(client, logar_como_admin):
    logar_como_admin()
    with client.session_transaction() as sessao:
        sessao['sid'] = ''

    resposta = client.get('/admin')

    assert resposta.status_code == 302
    assert resposta.headers['Location'].endswith('/login')


def test_logout_apaga_revogacoes_vencidas(client, contexto_app):
    db.session.add(SessaoRevogada(sid='vencida', expira_em=datetime.utcnow() - timedelta(minutes=1)))
    db.session.commit()
    _entrar_como_admin(client)

    client.post('/logout')

    db.session.expire_all()
    assert db.session.get(SessaoRevogada, 'vencida') is None


def test_pagina_autenticada_nao_vai_para_o_cache_do_navegador(client, logar_como_admin):
    assert 'no-store' not in client.get('/login').headers.get('Cache-Control', '')

    logar_como_admin()
    assert client.get('/admin').headers['Cache-Control'] == 'no-store'


def test_migracao_cria_a_tabela_igual_ao_modelo_e_e_reentrante(tmp_path):
    spec = importlib.util.spec_from_file_location('migracao_sessoes_revogadas', ARQUIVO_MIGRACAO)
    migracao = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migracao)

    engine = create_engine(f'sqlite:///{tmp_path}/migracao.db')
    with engine.begin() as conn:
        with Operations.context(MigrationContext.configure(conn)):
            migracao.upgrade()
            migracao.upgrade()  # tolera a tabela já criada (banco vindo do create_all)

        colunas = {c['name']: c for c in inspect(conn).get_columns('sessoes_revogadas')}
        assert set(colunas) == {c.name for c in SessaoRevogada.__table__.columns}
        assert not colunas['expira_em']['nullable']
        assert 'ix_sessoes_revogadas_expira_em' in {i['name'] for i in inspect(conn).get_indexes('sessoes_revogadas')}

        with Operations.context(MigrationContext.configure(conn)):
            migracao.downgrade()
        assert not inspect(conn).has_table('sessoes_revogadas')
