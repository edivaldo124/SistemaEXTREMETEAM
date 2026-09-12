"""fila de e-mail durável e índices dos tokens de conta

Revision ID: f2c81d0a6e47
Revises: e4b7c2a91d35
Create Date: 2026-09-12 11:00:00.000000

Duas mudanças aditivas, nenhuma reescreve ou apaga dado existente:

1. `emails_pendentes` - avisos e cobranças coletivas deixam de sair dentro da requisição
   e passam a ser registrados aqui antes de qualquer chamada ao provedor. A unicidade de
   `chave_idempotencia` é o que impede o mesmo envio de sair duas vezes.

2. Índices em `alunos.token_recuperacao_hash`, `token_email_hash` e `token_convite_hash`.
   Cada clique num link de recuperação, confirmação de e-mail ou convite busca
   exatamente por um desses hashes. Sem índice, a busca percorria a tabela de alunos
   inteira - e a de recuperação e confirmação chegava a carregar todas as linhas com
   token para comparar em Python.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2c81d0a6e47'
down_revision = 'e4b7c2a91d35'
branch_labels = None
depends_on = None


INDICES = (
    ('ix_alunos_token_recuperacao_hash', 'token_recuperacao_hash'),
    ('ix_alunos_token_email_hash', 'token_email_hash'),
    ('ix_alunos_token_convite_hash', 'token_convite_hash'),
)

# Medidos em PostgreSQL com 40.000 mensalidades e 2.000 alunos (ver comentário em
# modelos/pagamento.py): a listagem paginada do painel cai de 22,3 ms para 0,5 ms e as
# mensalidades de um aluno, de 2,2 ms para 0,16 ms.
INDICES_PAGAMENTOS = (
    ('ix_pagamentos_vencimento_id', ('vencimento', 'id')),
    ('ix_pagamentos_aluno_id', ('aluno_id',)),
)


def upgrade():
    inspector = sa.inspect(op.get_bind())

    if 'emails_pendentes' not in inspector.get_table_names():
        op.create_table(
            'emails_pendentes',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('destinatario', sa.String(length=150), nullable=False),
            sa.Column('nome_destinatario', sa.String(length=150), nullable=True),
            sa.Column('assunto', sa.String(length=200), nullable=False),
            sa.Column('titulo', sa.String(length=200), nullable=False),
            sa.Column('corpo', sa.Text(), nullable=False),
            sa.Column('link_url', sa.String(length=512), nullable=True),
            sa.Column('link_texto', sa.String(length=120), nullable=True),
            sa.Column('chave_idempotencia', sa.String(length=120), nullable=False),
            sa.Column('status', sa.String(length=20), nullable=False),
            sa.Column('tentativas', sa.Integer(), nullable=False),
            sa.Column('ultimo_erro', sa.String(length=255), nullable=True),
            sa.Column('criado_em', sa.DateTime(), nullable=False),
            sa.Column('processado_em', sa.DateTime(), nullable=True),
            # Adiamento da próxima tentativa. É por ele que a fila é ordenada, para uma
            # linha com defeito não ficar ocupando a cabeça e travar as demais.
            sa.Column('proxima_tentativa', sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint('id'),
        )
        # A unicidade vem do índice único abaixo (é como o modelo a declara): uma
        # UniqueConstraint separada criaria uma segunda restrição para a mesma coluna.
        op.create_index(
            'ix_emails_pendentes_chave_idempotencia', 'emails_pendentes',
            ['chave_idempotencia'], unique=True,
        )
        op.create_index('ix_emails_pendentes_status', 'emails_pendentes', ['status'])
        op.create_index(
            'ix_emails_pendentes_proxima_tentativa', 'emails_pendentes', ['proxima_tentativa'],
        )

    existentes = {i['name'] for i in inspector.get_indexes('alunos')}
    for nome, coluna in INDICES:
        if nome not in existentes:
            op.create_index(nome, 'alunos', [coluna])

    em_pagamentos = {i['name'] for i in inspector.get_indexes('pagamentos')}
    for nome, colunas in INDICES_PAGAMENTOS:
        if nome not in em_pagamentos:
            op.create_index(nome, 'pagamentos', list(colunas))


def downgrade():
    inspector = sa.inspect(op.get_bind())

    em_pagamentos = {i['name'] for i in inspector.get_indexes('pagamentos')}
    for nome, _colunas in INDICES_PAGAMENTOS:
        if nome in em_pagamentos:
            op.drop_index(nome, table_name='pagamentos')

    existentes = {i['name'] for i in inspector.get_indexes('alunos')}
    for nome, _coluna in INDICES:
        if nome in existentes:
            op.drop_index(nome, table_name='alunos')

    if 'emails_pendentes' in inspector.get_table_names():
        op.drop_index('ix_emails_pendentes_proxima_tentativa', table_name='emails_pendentes')
        op.drop_index('ix_emails_pendentes_status', table_name='emails_pendentes')
        op.drop_index('ix_emails_pendentes_chave_idempotencia', table_name='emails_pendentes')
        op.drop_table('emails_pendentes')
