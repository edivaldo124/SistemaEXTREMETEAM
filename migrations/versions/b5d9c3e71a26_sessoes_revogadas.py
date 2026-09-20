"""guarda as sessões encerradas pelo logout

Revision ID: b5d9c3e71a26
Revises: a8c3e5f17b04
Create Date: 2026-09-19 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


revision = 'b5d9c3e71a26'
down_revision = 'a8c3e5f17b04'
branch_labels = None
depends_on = None


def upgrade():
    if sa.inspect(op.get_bind()).has_table('sessoes_revogadas'):
        return

    op.create_table(
        'sessoes_revogadas',
        sa.Column('sid', sa.String(length=32), nullable=False),
        sa.Column('expira_em', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('sid'),
    )
    op.create_index('ix_sessoes_revogadas_expira_em', 'sessoes_revogadas', ['expira_em'])


def downgrade():
    if sa.inspect(op.get_bind()).has_table('sessoes_revogadas'):
        op.drop_index('ix_sessoes_revogadas_expira_em', table_name='sessoes_revogadas')
        op.drop_table('sessoes_revogadas')
