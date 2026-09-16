"""registra o aceite do termo de responsabilidade no cadastro

Revision ID: 1b7c45ea93d1
Revises: f2c81d0a6e47
Create Date: 2026-09-16 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


revision = '1b7c45ea93d1'
down_revision = 'f2c81d0a6e47'
branch_labels = None
depends_on = None


COLUNAS_TERMOS = (
    ('termos_responsabilidade_versao', sa.String(length=20)),
    ('termos_responsabilidade_aceito_em', sa.DateTime()),
)


def upgrade():
    inspector = sa.inspect(op.get_bind())
    existentes = {coluna['name'] for coluna in inspector.get_columns('alunos')}
    faltantes = [(nome, tipo) for nome, tipo in COLUNAS_TERMOS if nome not in existentes]
    if not faltantes:
        return

    with op.batch_alter_table('alunos', schema=None) as batch_op:
        for nome, tipo in faltantes:
            batch_op.add_column(sa.Column(nome, tipo, nullable=True))


def downgrade():
    inspector = sa.inspect(op.get_bind())
    existentes = {coluna['name'] for coluna in inspector.get_columns('alunos')}
    with op.batch_alter_table('alunos', schema=None) as batch_op:
        for nome, _ in reversed(COLUNAS_TERMOS):
            if nome in existentes:
                batch_op.drop_column(nome)
