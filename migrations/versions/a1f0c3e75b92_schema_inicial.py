"""schema inicial (base da cadeia de migrations)

Revision ID: a1f0c3e75b92
Revises:
Create Date: 2026-09-12 10:00:00.000000

A cadeia de migrations nunca teve uma base: a primeira revisão já começava alterando
`pagamentos`, uma tabela que migration nenhuma criava. O schema vinha, na prática, do
`db.create_all()` que `servidor.py` executava ao ser importado - inclusive no import
feito pelo próprio `flask db upgrade`.

O efeito num banco VAZIO era que `flask db upgrade` falhava: o create_all criava as
tabelas já no formato atual e a primeira revisão então tentava adicionar colunas
recém-criadas ("column \"provider\" of relation \"pagamentos\" already exists" no
PostgreSQL). Como o Dockerfile roda `flask db upgrade && gunicorn`, uma instalação nova
não subia.

Esta revisão congela o schema COMO ELE ERA ANTES DA PRIMEIRA MIGRAÇÃO e passa a ser a
base da cadeia. Ela é deliberadamente escrita à mão, e não a partir dos modelos atuais:
uma base que acompanhasse os modelos recriaria o mesmo problema a cada coluna nova.

Bancos que já existem não são tocados:

* Um banco de produção já carimbado (`alembic_version` em uma revisão da cadeia) nunca
  executa esta revisão.
* Um banco criado pelo antigo `create_all()` e nunca carimbado já tem as tabelas. Aqui
  isso é detectado e a criação é pulada; as revisões seguintes conferem coluna a coluna
  antes de agir, então basta rodar `flask db upgrade` normalmente.

NÃO use `db stamp head` nesse caso. `stamp` só escreve a versão em `alembic_version`,
sem executar DDL nenhum: um banco antigo carimbado como atualizado ficaria sem o que as
revisões seguintes deveriam ter criado (a tabela `emails_pendentes` e os índices, por
exemplo), e o upgrade posterior não voltaria para criá-los. O caminho seguro é deixar o
`upgrade` percorrer a cadeia - cada revisão inspeciona o banco antes de agir.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1f0c3e75b92'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    inspector = sa.inspect(op.get_bind())
    existentes = set(inspector.get_table_names())

    # Banco já povoado (por um create_all antigo, por exemplo): nada a criar. As
    # revisões seguintes são idempotentes e completam o que faltar.
    if 'alunos' in existentes:
        return

    op.create_table(
        'planos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome_plano', sa.String(length=100), nullable=False),
        sa.Column('preco_plano', sa.Float(), nullable=False),
        sa.Column('duracao_dias', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'professores',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=150), nullable=False),
        sa.Column('login', sa.String(length=50), nullable=False),
        sa.Column('senha_hash', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('login'),
    )

    op.create_table(
        'alunos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=150), nullable=False),
        sa.Column('datanascimento', sa.String(), nullable=False),
        sa.Column('cpf', sa.String(length=14), nullable=False),
        sa.Column('telefone', sa.String(length=20), nullable=True),
        sa.Column('mensalidade', sa.String(length=50), nullable=False),
        sa.Column('descricao', sa.String(length=255), nullable=True),
        # Obrigatórios nesta altura da história; a revisão e4b7c2a91d35 os torna
        # opcionais para permitir o cadastro administrativo sem conta de acesso.
        sa.Column('login', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=150), nullable=False),
        sa.Column('senha_hash', sa.String(length=255), nullable=False),
        sa.Column('status_cadastro', sa.String(length=20), nullable=False),
        sa.Column('ativo', sa.Boolean(), nullable=False),
        sa.Column('plano_id', sa.Integer(), nullable=True),
        sa.Column('data_vencimento', sa.String(length=10), nullable=True),
        sa.Column('token_recuperacao_hash', sa.String(length=64), nullable=True),
        sa.Column('token_recuperacao_expira', sa.DateTime(), nullable=True),
        sa.Column('email_pendente', sa.String(length=150), nullable=True),
        sa.Column('token_email_hash', sa.String(length=64), nullable=True),
        sa.Column('token_email_expira', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['plano_id'], ['planos.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('cpf'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('login'),
    )

    op.create_table(
        'turmas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=100), nullable=False),
        sa.Column('dias_semana', sa.String(length=100), nullable=False),
        sa.Column('horario', sa.String(length=20), nullable=False),
        sa.Column('limite_alunos', sa.Integer(), nullable=False),
        sa.Column('professor_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['professor_id'], ['professores.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'matriculas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('aluno_id', sa.Integer(), nullable=False),
        sa.Column('turma_id', sa.Integer(), nullable=False),
        sa.Column('data_matricula', sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(['aluno_id'], ['alunos.id']),
        sa.ForeignKeyConstraint(['turma_id'], ['turmas.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('aluno_id', 'turma_id', name='uq_matricula_aluno_turma'),
    )

    op.create_table(
        'presencas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('aluno_id', sa.Integer(), nullable=False),
        sa.Column('turma_id', sa.Integer(), nullable=False),
        sa.Column('data_aula', sa.Date(), nullable=False),
        sa.Column('presente', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['aluno_id'], ['alunos.id']),
        sa.ForeignKeyConstraint(['turma_id'], ['turmas.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('aluno_id', 'turma_id', 'data_aula', name='uq_presenca_aluno_turma_data'),
    )

    op.create_table(
        'pagamentos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('aluno_id', sa.Integer(), nullable=False),
        sa.Column('plano_id', sa.Integer(), nullable=False),
        # Float aqui é fiel ao schema da época; a revisão 896e70afc9c5 converte para
        # Numeric(10,2), que é o tipo em vigor.
        sa.Column('valor', sa.Float(), nullable=False),
        sa.Column('vencimento', sa.Date(), nullable=False),
        sa.Column('data_pagamento', sa.Date(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('forma_pagamento', sa.String(length=30), nullable=True),
        sa.ForeignKeyConstraint(['aluno_id'], ['alunos.id']),
        sa.ForeignKeyConstraint(['plano_id'], ['planos.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'pagamentos_eventos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('pagamento_id', sa.Integer(), nullable=False),
        sa.Column('tipo', sa.String(length=40), nullable=False),
        sa.Column('detalhe', sa.Text(), nullable=True),
        sa.Column('ator', sa.String(length=100), nullable=True),
        sa.Column('criado_em', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['pagamento_id'], ['pagamentos.id']),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('pagamentos_eventos')
    op.drop_table('pagamentos')
    op.drop_table('presencas')
    op.drop_table('matriculas')
    op.drop_table('turmas')
    op.drop_table('alunos')
    op.drop_table('professores')
    op.drop_table('planos')
