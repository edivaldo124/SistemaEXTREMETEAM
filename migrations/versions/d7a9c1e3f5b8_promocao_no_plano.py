"""promoção no plano: preço promocional com período de validade

Revision ID: d7a9c1e3f5b8
Revises: c5e7f9b0d3f2
Create Date: 2026-09-28 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'd7a9c1e3f5b8'
down_revision = 'c5e7f9b0d3f2'
branch_labels = None
depends_on = None

COLUNAS = (
    ('preco_promocional', sa.Numeric(10, 2)),
    ('promocao_inicio', sa.Date()),
    ('promocao_fim', sa.Date()),
)


def upgrade():
    inspector = sa.inspect(op.get_bind())
    existentes = {coluna['name'] for coluna in inspector.get_columns('planos')}
    with op.batch_alter_table('planos', schema=None) as batch_op:
        for nome, tipo in COLUNAS:
            if nome not in existentes:
                batch_op.add_column(sa.Column(nome, tipo, nullable=True))


def downgrade():
    inspector = sa.inspect(op.get_bind())
    existentes = {coluna['name'] for coluna in inspector.get_columns('planos')}
    with op.batch_alter_table('planos', schema=None) as batch_op:
        for nome, _tipo in reversed(COLUNAS):
            if nome in existentes:
                batch_op.drop_column(nome)
