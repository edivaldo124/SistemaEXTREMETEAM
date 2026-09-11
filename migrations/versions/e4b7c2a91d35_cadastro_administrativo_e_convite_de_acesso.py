"""cadastro de aluno sem conta de acesso e convite de ativacao

Revision ID: e4b7c2a91d35
Revises: d9e2f6a14c80
Create Date: 2026-09-10 21:30:00.000000

Separa o CADASTRO do aluno (nome, CPF, plano, mensalidades) da CONTA DE ACESSO
(login, e-mail, senha). `login`, `email` e `senha_hash` passam a aceitar NULL para
que a administração matricule um aluno que nunca vai entrar no sistema.

Nenhum dado é apagado ou reescrito: alunos existentes continuam com os três campos
preenchidos e, portanto, com o acesso ativado. As colunas de convite nascem em NULL.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4b7c2a91d35'
down_revision = 'd9e2f6a14c80'
branch_labels = None
depends_on = None


COLUNAS_CONVITE = (
    ('token_convite_hash', sa.String(length=64)),
    ('token_convite_expira', sa.DateTime()),
    ('convite_enviado_em', sa.DateTime()),
)

# Tipo real de cada coluna que deixa de ser obrigatória. O SQLite recria a tabela em
# batch e precisa do tipo declarado; o PostgreSQL só emite DROP NOT NULL.
COLUNAS_OPCIONAIS = (
    ('login', sa.String(length=50)),
    ('email', sa.String(length=150)),
    ('senha_hash', sa.String(length=255)),
)


def _colunas(inspector, tabela):
    return {c['name']: c for c in inspector.get_columns(tabela)}


def upgrade():
    # Mesmo cuidado das migrações anteriores: `servidor.py` roda `db.create_all()` no
    # import, então parte do schema pode já existir quando o upgrade executa. Cada
    # passo confere o banco real antes de agir, e reaplicar é inofensivo.
    inspector = sa.inspect(op.get_bind())
    colunas = _colunas(inspector, 'alunos')

    faltantes = [(nome, tipo) for nome, tipo in COLUNAS_CONVITE if nome not in colunas]
    obrigatorias = [(nome, tipo) for nome, tipo in COLUNAS_OPCIONAIS
                    if nome in colunas and not colunas[nome]['nullable']]

    if not faltantes and not obrigatorias:
        return

    with op.batch_alter_table('alunos', schema=None) as batch_op:
        for nome, tipo in faltantes:
            batch_op.add_column(sa.Column(nome, tipo, nullable=True))
        for nome, tipo in obrigatorias:
            batch_op.alter_column(nome, existing_type=tipo, nullable=True)


def downgrade():
    # Volta a exigir conta de acesso. Só é possível se nenhum cadastro estiver sem ela:
    # apagar esses alunos (e as mensalidades deles) seria perda de dado silenciosa.
    bind = op.get_bind()
    sem_acesso = bind.execute(sa.text(
        'SELECT COUNT(*) FROM alunos WHERE senha_hash IS NULL OR login IS NULL OR email IS NULL'
    )).scalar()
    if sem_acesso:
        raise RuntimeError(
            f'{sem_acesso} aluno(s) sem conta de acesso. A reversão foi bloqueada para preservar '
            'os cadastros. Preencha os dados de acesso antes de reverter esta migração.'
        )

    with op.batch_alter_table('alunos', schema=None) as batch_op:
        for nome, tipo in COLUNAS_OPCIONAIS:
            batch_op.alter_column(nome, existing_type=tipo, nullable=False)
        for nome, _ in reversed(COLUNAS_CONVITE):
            batch_op.drop_column(nome)
