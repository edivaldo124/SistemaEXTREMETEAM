"""vincula turma escolhida à cobrança até o pagamento"""
from alembic import op
import sqlalchemy as sa

revision = 'e8f9a0b1c2d3'
down_revision = 'd7e8f9a0b1c2'
branch_labels = None
depends_on = None


def upgrade():
    inspector = sa.inspect(op.get_bind())
    colunas = {coluna['name'] for coluna in inspector.get_columns('pagamentos')}
    if 'turma_id' not in colunas:
        with op.batch_alter_table('pagamentos', schema=None) as batch_op:
            batch_op.add_column(sa.Column('turma_id', sa.Integer(), nullable=True))
            batch_op.create_foreign_key(
                'fk_pagamentos_turma_id', 'turmas', ['turma_id'], ['id'],
            )


def downgrade():
    inspector = sa.inspect(op.get_bind())
    colunas = {coluna['name'] for coluna in inspector.get_columns('pagamentos')}
    if 'turma_id' in colunas:
        with op.batch_alter_table('pagamentos', schema=None) as batch_op:
            batch_op.drop_constraint('fk_pagamentos_turma_id', type_='foreignkey')
            batch_op.drop_column('turma_id')
