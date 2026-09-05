"""Contatos da academia e perfis profissionais opcionais dos professores.

Revision ID: d9e2f6a14c80
Revises: c7a4e1b93d20
"""
from alembic import op
import sqlalchemy as sa

revision = 'd9e2f6a14c80'
down_revision = 'c7a4e1b93d20'
branch_labels = None
depends_on = None


def _campos_professor():
    return [
        sa.Column('nome_publico', sa.String(150), nullable=True),
        sa.Column('modalidades', sa.String(200), nullable=True),
        sa.Column('biografia', sa.Text(), nullable=True),
        sa.Column('formacao', sa.Text(), nullable=True),
        sa.Column('instagram', sa.String(30), nullable=True),
        sa.Column('email_publico', sa.String(150), nullable=True),
        sa.Column('whatsapp', sa.String(20), nullable=True),
        sa.Column('foto_arquivo', sa.String(64), nullable=True),
        *[sa.Column(nome, sa.Boolean(), nullable=False, server_default=sa.false())
          for nome in ('perfil_publico', 'exibir_instagram', 'exibir_email', 'exibir_whatsapp')],
    ]


def upgrade():
    inspector = sa.inspect(op.get_bind())
    # O create_all no início da aplicação pode já ter criado a tabela nova.
    if 'academia' not in inspector.get_table_names():
        op.create_table(
            'academia',
            sa.Column('id', sa.Integer(), primary_key=True),
            sa.Column('instagram', sa.String(30), nullable=True),
            sa.Column('email', sa.String(150), nullable=True),
            sa.Column('whatsapp', sa.String(20), nullable=True),
            sa.Column('endereco', sa.String(300), nullable=True),
            sa.Column('complemento', sa.String(150), nullable=True),
            sa.Column('horarios', sa.String(1000), nullable=True),
            sa.CheckConstraint('id = 1', name='ck_academia_unica'),
        )
    existentes = {c['name'] for c in inspector.get_columns('professores')}
    novos = [c for c in _campos_professor() if c.name not in existentes]
    if novos:
        with op.batch_alter_table('professores') as batch:
            for coluna in novos:
                batch.add_column(coluna)


def downgrade():
    inspector = sa.inspect(op.get_bind())
    existentes = {c['name'] for c in inspector.get_columns('professores')}
    remover = [c.name for c in _campos_professor() if c.name in existentes]
    if remover:
        with op.batch_alter_table('professores') as batch:
            for coluna in reversed(remover):
                batch.drop_column(coluna)
    if 'academia' in inspector.get_table_names():
        op.drop_table('academia')
