"""vigencia da mensalidade e mudanca de plano agendada

Revision ID: c7a4e1b93d20
Revises: b3d1a7c92e4f
Create Date: 2026-09-05 01:10:00.000000

As duas colunas novas em `pagamentos` são nullable e aditivas: mensalidades antigas
continuam válidas com elas em NULL e o período delas passa a ser deduzido da data de
pagamento somada à duração do plano (ver servicos/planos.intervalo_vigencia).

Nenhum dado é apagado ou reescrito por esta migração - o backfill abaixo apenas
preenche a vigência das mensalidades JÁ PAGAS que ainda não tinham o período gravado,
usando exatamente a mesma regra de dedução, para que a área do aluno passe a mostrar
"Plano ativo" para quem já pagou sem depender de um novo pagamento.
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7a4e1b93d20'
down_revision = 'b3d1a7c92e4f'
branch_labels = None
depends_on = None


def _colunas(inspector, tabela):
    return {c['name'] for c in inspector.get_columns(tabela)}


def upgrade():
    # `servidor.py` chama `db.create_all()` no import, e o deploy roda
    # `flask --app servidor db upgrade` - ou seja, o create_all acontece ANTES desta
    # migração e pode já ter criado a tabela nova num banco onde ela faltava. Por isso
    # cada passo confere o schema real antes de agir: aplicar duas vezes é inofensivo.
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    colunas_pagamentos = _colunas(inspector, 'pagamentos')
    tabelas = set(inspector.get_table_names())

    novas = [c for c in ('vigencia_inicio', 'vigencia_fim') if c not in colunas_pagamentos]
    if novas:
        with op.batch_alter_table('pagamentos', schema=None) as batch_op:
            for coluna in novas:
                batch_op.add_column(sa.Column(coluna, sa.Date(), nullable=True))

    if 'solicitacoes_mudanca_plano' not in tabelas:
        _criar_tabela_solicitacoes()
    else:
        # A tabela veio do create_all, que não cria este índice.
        indices = {i['name'] for i in inspector.get_indexes('solicitacoes_mudanca_plano')}
        if 'ix_solicitacoes_mudanca_plano_aluno_status' not in indices:
            op.create_index('ix_solicitacoes_mudanca_plano_aluno_status',
                            'solicitacoes_mudanca_plano', ['aluno_id', 'status'])

    _backfill_vigencia(bind)


def _criar_tabela_solicitacoes():
    op.create_table(
        'solicitacoes_mudanca_plano',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('aluno_id', sa.Integer(), nullable=False),
        sa.Column('plano_origem_id', sa.Integer(), nullable=True),
        sa.Column('plano_destino_id', sa.Integer(), nullable=False),
        sa.Column('valor_origem', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('valor_destino', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('tipo', sa.String(length=20), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('vigencia_a_partir_de', sa.Date(), nullable=True),
        sa.Column('criado_em', sa.DateTime(), nullable=False),
        sa.Column('criado_por', sa.String(length=100), nullable=True),
        sa.Column('efetivado_em', sa.DateTime(), nullable=True),
        sa.Column('pagamento_efetivacao_id', sa.Integer(), nullable=True),
        sa.Column('cancelado_em', sa.DateTime(), nullable=True),
        sa.Column('cancelado_por', sa.String(length=100), nullable=True),
        sa.Column('observacao', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['aluno_id'], ['alunos.id'], name='fk_solicitacao_plano_aluno'),
        sa.ForeignKeyConstraint(['plano_origem_id'], ['planos.id'], name='fk_solicitacao_plano_origem'),
        sa.ForeignKeyConstraint(['plano_destino_id'], ['planos.id'], name='fk_solicitacao_plano_destino'),
        sa.ForeignKeyConstraint(['pagamento_efetivacao_id'], ['pagamentos.id'], name='fk_solicitacao_plano_pagamento'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_solicitacoes_mudanca_plano_aluno_status',
                    'solicitacoes_mudanca_plano', ['aluno_id', 'status'])


def _backfill_vigencia(bind):
    # Só preenche onde está NULL e só para mensalidades pagas, sem tocar em status,
    # valores ou datas de pagamento. É o que faz quem JÁ pagou passar a aparecer como
    # "Plano ativo" sem precisar de um novo pagamento.
    op.execute(
        """
        UPDATE pagamentos
           SET vigencia_inicio = COALESCE(data_pagamento, vencimento)
         WHERE vigencia_inicio IS NULL
           AND status = 'pago'
           AND COALESCE(data_pagamento, vencimento) IS NOT NULL
        """
    )
    if bind.dialect.name == 'postgresql':
        fim = ("vigencia_inicio + ((SELECT COALESCE(planos.duracao_dias, 30) FROM planos "
               "WHERE planos.id = pagamentos.plano_id) - 1) * INTERVAL '1 day'")
    else:
        fim = ("DATE(vigencia_inicio, '+' || ((SELECT COALESCE(planos.duracao_dias, 30) FROM planos "
               "WHERE planos.id = pagamentos.plano_id) - 1) || ' day')")
    op.execute(
        f"""
        UPDATE pagamentos
           SET vigencia_fim = {fim}
         WHERE vigencia_fim IS NULL
           AND vigencia_inicio IS NOT NULL
        """
    )


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if 'solicitacoes_mudanca_plano' in set(inspector.get_table_names()):
        op.drop_index('ix_solicitacoes_mudanca_plano_aluno_status', table_name='solicitacoes_mudanca_plano')
        op.drop_table('solicitacoes_mudanca_plano')
    existentes = _colunas(inspector, 'pagamentos')
    a_remover = [c for c in ('vigencia_fim', 'vigencia_inicio') if c in existentes]
    if a_remover:
        with op.batch_alter_table('pagamentos', schema=None) as batch_op:
            for coluna in a_remover:
                batch_op.drop_column(coluna)
