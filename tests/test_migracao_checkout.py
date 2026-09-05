"""Exercita a migração dos campos do Checkout Pro de verdade (upgrade e downgrade).

O projeto não tem uma cadeia de migrations que crie o schema do zero (a base nasce de
`db.create_all()`), então aqui montamos só a tabela `pagamentos` no estado anterior à
migração e rodamos a revisão isoladamente sobre um SQLite temporário.
"""
import importlib.util
from pathlib import Path

import pytest
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import create_engine, inspect, text

ARQUIVO_MIGRACAO = (
    Path(__file__).resolve().parent.parent
    / 'migrations' / 'versions' / 'b3d1a7c92e4f_adiciona_campos_do_checkout_pro.py'
)

COLUNAS_NOVAS = {
    'checkout_preference_id',
    'checkout_external_reference',
    'checkout_url',
    'checkout_ambiente',
    'checkout_valor',
    'checkout_criado_em',
    'checkout_expira_em',
}

# Estado da tabela imediatamente antes desta revisão (só o necessário para o teste).
SQL_TABELA_ANTERIOR = """
CREATE TABLE pagamentos (
    id INTEGER NOT NULL PRIMARY KEY,
    aluno_id INTEGER NOT NULL,
    plano_id INTEGER NOT NULL,
    valor NUMERIC(10, 2) NOT NULL,
    vencimento DATE NOT NULL,
    data_pagamento DATE,
    status VARCHAR(20) NOT NULL,
    forma_pagamento VARCHAR(30),
    competencia VARCHAR(7),
    provider VARCHAR(20),
    provider_payment_id VARCHAR(64),
    external_reference VARCHAR(120),
    idempotency_key VARCHAR(64),
    pix_copia_cola TEXT,
    ticket_url VARCHAR(255),
    data_criacao_pix DATETIME,
    data_expiracao DATETIME,
    provider_status VARCHAR(30),
    provider_status_detail VARCHAR(60)
)
"""

SQL_LINHA_ANTIGA = """
INSERT INTO pagamentos (id, aluno_id, plano_id, valor, vencimento, status, provider, external_reference)
VALUES (1, 10, 20, 150.00, '2026-09-10', 'pendente', 'mercado_pago', 'mensalidade-1-antiga')
"""


@pytest.fixture
def migracao():
    especificacao = importlib.util.spec_from_file_location('migracao_checkout', ARQUIVO_MIGRACAO)
    modulo = importlib.util.module_from_spec(especificacao)
    especificacao.loader.exec_module(modulo)
    return modulo


@pytest.fixture
def conexao(tmp_path):
    engine = create_engine(f'sqlite:///{tmp_path}/migracao.db')
    with engine.begin() as conexao:
        conexao.execute(text(SQL_TABELA_ANTERIOR))
        conexao.execute(text(SQL_LINHA_ANTIGA))
    with engine.connect() as conexao:
        yield conexao


def _colunas(conexao):
    return {coluna['name'] for coluna in inspect(conexao).get_columns('pagamentos')}


def _rodar(migracao, conexao, sentido):
    # A conexão pode já ter uma transação implícita aberta (o inspect abre uma), então
    # aproveitamos o autobegin do SQLAlchemy em vez de chamar begin() de novo.
    contexto = MigrationContext.configure(conexao)
    with Operations.context(contexto):
        getattr(migracao, sentido)()
    conexao.commit()


def test_encadeamento_da_revisao(migracao):
    assert migracao.revision == 'b3d1a7c92e4f'
    assert migracao.down_revision == '896e70afc9c5'


def test_upgrade_adiciona_as_colunas_e_preserva_linhas_antigas(migracao, conexao):
    assert not (COLUNAS_NOVAS & _colunas(conexao))

    _rodar(migracao, conexao, 'upgrade')

    assert COLUNAS_NOVAS <= _colunas(conexao)

    linha = conexao.execute(text(
        'SELECT external_reference, checkout_external_reference FROM pagamentos WHERE id = 1'
    )).one()
    assert linha[0] == 'mensalidade-1-antiga'  # cobrança Pix existente continua intacta
    assert linha[1] is None                    # campo novo nasce vazio, sem default forçado


def test_downgrade_remove_exatamente_o_que_o_upgrade_criou(migracao, conexao):
    antes = _colunas(conexao)

    _rodar(migracao, conexao, 'upgrade')
    _rodar(migracao, conexao, 'downgrade')

    assert _colunas(conexao) == antes
    assert conexao.execute(text('SELECT COUNT(*) FROM pagamentos')).scalar() == 1
