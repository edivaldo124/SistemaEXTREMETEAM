"""adiciona_coluna_arquivado_no_plano

Revision ID: c5e7f9b0d3f2
Revises: b4d6f8a0c2e1
Create Date: 2026-09-28 14:22:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5e7f9b0d3f2'
down_revision = 'b4d6f8a0c2e1'
branch_labels = None
depends_on = None


def upgrade():
    # Adiciona a coluna arquivado no plano
    op.add_column('planos', sa.Column('arquivado', sa.Boolean(), server_default=sa.text('false'), nullable=False))


def downgrade():
    op.drop_column('planos', 'arquivado')
