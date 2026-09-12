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


COLUNAS_CHECKOUT = (
    ('checkout_preference_id', sa.String(length=64)),
    ('checkout_external_reference', sa.String(length=120)),
    ('checkout_url', sa.String(length=512)),
    ('checkout_ambiente', sa.String(length=20)),
    ('checkout_valor', sa.Numeric(precision=10, scale=2)),
    ('checkout_criado_em', sa.DateTime()),
    ('checkout_expira_em', sa.DateTime()),
)


RESTRICOES_CHECKOUT = (
    ('uq_pagamentos_checkout_preference_id', ['checkout_preference_id']),
    ('uq_pagamentos_checkout_external_reference', ['checkout_external_reference']),
)


def upgrade():
    # Confere o banco real antes de agir (ver a revisão base a1f0c3e75b92). Colunas e
    # restrições são conferidas separadamente, pelo mesmo motivo da revisão 50f97271f0a2.
    inspector = sa.inspect(op.get_bind())
    colunas = {c['name'] for c in inspector.get_columns('pagamentos')}
    faltantes = [(nome, tipo) for nome, tipo in COLUNAS_CHECKOUT if nome not in colunas]

    nomes_existentes = {
        r['name'] for r in inspector.get_unique_constraints('pagamentos') if r.get('name')
    } | {i['name'] for i in inspector.get_indexes('pagamentos')}
    restricoes = [(n, c) for n, c in RESTRICOES_CHECKOUT if n not in nomes_existentes]

    if not faltantes and not restricoes:
        return

    with op.batch_alter_table('pagamentos', schema=None) as batch_op:
        for nome, tipo in faltantes:
            batch_op.add_column(sa.Column(nome, tipo, nullable=True))
        for nome, colunas_da_restricao in restricoes:
            batch_op.create_unique_constraint(nome, colunas_da_restricao)


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
