"""guarda a conta do Mercado Pago conectada por OAuth

Revision ID: a8c3e5f17b04
Revises: 1b7c45ea93d1
Create Date: 2026-09-19 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


revision = 'a8c3e5f17b04'
down_revision = '1b7c45ea93d1'
branch_labels = None
depends_on = None


def upgrade():
    if sa.inspect(op.get_bind()).has_table('mercado_pago_conexao'):
        return

    op.create_table(
        'mercado_pago_conexao',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('mp_user_id', sa.String(length=40), nullable=False),
        sa.Column('public_key', sa.String(length=200), nullable=True),
        sa.Column('access_token_cifrado', sa.Text(), nullable=False),
        sa.Column('refresh_token_cifrado', sa.Text(), nullable=False),
        sa.Column('live_mode', sa.Boolean(), nullable=False),
        sa.Column('expira_em', sa.DateTime(), nullable=False),
        sa.Column('conectado_em', sa.DateTime(), nullable=False),
        sa.Column('renovado_em', sa.DateTime(), nullable=True),
        sa.Column('precisa_reconectar', sa.Boolean(), nullable=False),
        sa.CheckConstraint('id = 1', name='ck_mercado_pago_conexao_unica'),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    if sa.inspect(op.get_bind()).has_table('mercado_pago_conexao'):
        op.drop_table('mercado_pago_conexao')
