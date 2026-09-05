"""adiciona campos do checkout pro (outras formas de pagamento)

Revision ID: b3d1a7c92e4f
Revises: 896e70afc9c5
Create Date: 2026-09-04 19:05:00.000000

Todas as colunas são nullable e aditivas: mensalidades antigas (lançamentos manuais e
cobranças Pix já existentes) continuam válidas com todos esses campos em NULL, e o
fluxo do Pix direto não depende de nenhuma delas.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3d1a7c92e4f'
down_revision = '896e70afc9c5'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('pagamentos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('checkout_preference_id', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('checkout_external_reference', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('checkout_url', sa.String(length=512), nullable=True))
        batch_op.add_column(sa.Column('checkout_ambiente', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('checkout_valor', sa.Numeric(precision=10, scale=2), nullable=True))
        batch_op.add_column(sa.Column('checkout_criado_em', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('checkout_expira_em', sa.DateTime(), nullable=True))
        batch_op.create_unique_constraint('uq_pagamentos_checkout_preference_id', ['checkout_preference_id'])
        batch_op.create_unique_constraint('uq_pagamentos_checkout_external_reference', ['checkout_external_reference'])


def downgrade():
    with op.batch_alter_table('pagamentos', schema=None) as batch_op:
        batch_op.drop_constraint('uq_pagamentos_checkout_external_reference', type_='unique')
        batch_op.drop_constraint('uq_pagamentos_checkout_preference_id', type_='unique')
        batch_op.drop_column('checkout_expira_em')
        batch_op.drop_column('checkout_criado_em')
        batch_op.drop_column('checkout_valor')
        batch_op.drop_column('checkout_ambiente')
        batch_op.drop_column('checkout_url')
        batch_op.drop_column('checkout_external_reference')
        batch_op.drop_column('checkout_preference_id')
