"""despesas da planilha econômica

Revision ID: f4a6c8e0b2d1
Revises: b565d2f8bd5e
Create Date: 2026-10-04 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


revision = 'f4a6c8e0b2d1'
down_revision = 'b565d2f8bd5e'
branch_labels = None
depends_on = None


def upgrade():
    if sa.inspect(op.get_bind()).has_table('despesas'):
        return

    op.create_table(
        'despesas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('data', sa.Date(), nullable=False),
        sa.Column('categoria', sa.String(length=20), nullable=False),
        sa.Column('descricao', sa.String(length=120), nullable=False),
        sa.Column('valor', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('lancado_por', sa.String(length=80), nullable=True),
        sa.Column('criado_em', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_despesas_data', 'despesas', ['data'])


def downgrade():
    if sa.inspect(op.get_bind()).has_table('despesas'):
        op.drop_index('ix_despesas_data', table_name='despesas')
        op.drop_table('despesas')
