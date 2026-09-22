"""adiciona confirmacao de frequencia pelo aluno"""
from alembic import op
import sqlalchemy as sa

revision = 'd7e8f9a0b1c2'
down_revision = 'c1d4e5f6a7b8'
branch_labels = None
depends_on = None


def upgrade():
    inspector = sa.inspect(op.get_bind())
    colunas = {coluna['name'] for coluna in inspector.get_columns('presencas')}
    if 'confirmada_aluno' not in colunas:
        op.add_column(
            'presencas',
            sa.Column('confirmada_aluno', sa.Boolean(), nullable=False, server_default=sa.false()),
        )
    if 'confirmada_em' not in colunas:
        op.add_column('presencas', sa.Column('confirmada_em', sa.DateTime(), nullable=True))


def downgrade():
    inspector = sa.inspect(op.get_bind())
    colunas = {coluna['name'] for coluna in inspector.get_columns('presencas')}
    if 'confirmada_em' in colunas:
        op.drop_column('presencas', 'confirmada_em')
    if 'confirmada_aluno' in colunas:
        op.drop_column('presencas', 'confirmada_aluno')
