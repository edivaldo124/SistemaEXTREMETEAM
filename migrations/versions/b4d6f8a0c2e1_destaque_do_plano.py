"""plano em destaque na página inicial (escolhido pelo admin)"""
from alembic import op
import sqlalchemy as sa

revision = 'b4d6f8a0c2e1'
down_revision = 'e8f9a0b1c2d3'
branch_labels = None
depends_on = None


def upgrade():
    inspector = sa.inspect(op.get_bind())
    colunas = {coluna['name'] for coluna in inspector.get_columns('planos')}
    if 'destaque' not in colunas:
        with op.batch_alter_table('planos', schema=None) as batch_op:
            batch_op.add_column(
                sa.Column('destaque', sa.Boolean(), nullable=False, server_default=sa.false()),
            )


def downgrade():
    inspector = sa.inspect(op.get_bind())
    colunas = {coluna['name'] for coluna in inspector.get_columns('planos')}
    if 'destaque' in colunas:
        with op.batch_alter_table('planos', schema=None) as batch_op:
            batch_op.drop_column('destaque')
