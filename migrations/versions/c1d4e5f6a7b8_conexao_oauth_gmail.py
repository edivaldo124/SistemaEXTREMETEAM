"""guarda a conta Gmail conectada pelo administrador"""
from alembic import op
import sqlalchemy as sa

revision = 'c1d4e5f6a7b8'
down_revision = 'b5d9c3e71a26'
branch_labels = None
depends_on = None


def upgrade():
    if sa.inspect(op.get_bind()).has_table('gmail_conexao'):
        return
    op.create_table(
        'gmail_conexao',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=320), nullable=False),
        sa.Column('refresh_token_cifrado', sa.Text(), nullable=False),
        sa.Column('conectado_em', sa.DateTime(), nullable=False),
        sa.CheckConstraint('id = 1', name='ck_gmail_conexao_unica'),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    if sa.inspect(op.get_bind()).has_table('gmail_conexao'):
        op.drop_table('gmail_conexao')