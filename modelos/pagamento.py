from datetime import date
from decimal import Decimal

from config import db


def _para_decimal(valor):
    if valor is None:
        return None
    return valor if isinstance(valor, Decimal) else Decimal(str(valor))


class Pagamento(db.Model):
    __tablename__ = 'pagamentos'

    # Dois índices, cada um escolhido por uma consulta que roda de verdade e medido em
    # PostgreSQL com 40.000 mensalidades e 2.000 alunos. Nenhum índice foi criado "por
    # via das dúvidas": status, forma_pagamento e plano_id são filtros opcionais e de
    # baixa cardinalidade, e os indicadores varrem o período inteiro de qualquer jeito.
    __table_args__ = (
        # Painel financeiro: ORDER BY vencimento DESC, id DESC com LIMIT/OFFSET.
        # Ordenar 40.000 linhas custava 22,3 ms; com o índice, 0,5 ms. Ascendente de
        # propósito - o PostgreSQL o percorre de trás para frente ("Index Scan
        # Backward") e o mesmo índice serve às duas direções.
        db.Index('ix_pagamentos_vencimento_id', 'vencimento', 'id'),
        # Mensalidades de um aluno: roda a cada abertura do perfil. 2,2 ms -> 0,16 ms.
        # Chave estrangeira não ganha índice sozinha no PostgreSQL.
        db.Index('ix_pagamentos_aluno_id', 'aluno_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    plano_id = db.Column(db.Integer, db.ForeignKey('planos.id'), nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    vencimento = db.Column(db.Date, nullable=False)
    data_pagamento = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pendente')
    forma_pagamento = db.Column(db.String(30), nullable=True)

    # Competência da mensalidade no formato 'AAAA-MM' (ex.: '2026-09' = Setembro de 2026).
    competencia = db.Column(db.String(7), nullable=True)

    # Período de acesso que ESTA mensalidade cobre, calculado a partir de
    # Plano.duracao_dias e encadeado ao fim do período já pago (quem renova antes do
    # vencimento não perde os dias que já comprou). É por este intervalo - nunca pelo
    # texto livre de Aluno.mensalidade nem pela competência - que o sistema decide se o
    # aluno tem plano ativo hoje e até quando. Nullable: lançamentos antigos não têm.
    vigencia_inicio = db.Column(db.Date, nullable=True)
    vigencia_fim = db.Column(db.Date, nullable=True)

    # RF: pagamento via Pix (Mercado Pago). Todos nullable/aditivos - linhas antigas
    # (lançamentos manuais do admin) ficam com provider=None e não são afetadas.
    provider = db.Column(db.String(20), nullable=True)  # None/'manual' (sem integração) | 'mercado_pago'
    provider_payment_id = db.Column(db.String(64), nullable=True, unique=True)
    external_reference = db.Column(db.String(120), nullable=True, unique=True)
    idempotency_key = db.Column(db.String(64), nullable=True)
    pix_copia_cola = db.Column(db.Text, nullable=True)
    ticket_url = db.Column(db.String(255), nullable=True)
    data_criacao_pix = db.Column(db.DateTime, nullable=True)
    data_expiracao = db.Column(db.DateTime, nullable=True)

    # RF: Checkout Pro (outras formas de pagamento - cartão, boleto, saldo MP...).
    # Colunas próprias, separadas das do Pix direto: a preferência existe ANTES de haver
    # qualquer payment_id, então nada disso pode reaproveitar provider_payment_id. As duas
    # cobranças podem coexistir na mesma mensalidade sem uma sobrescrever a outra.
    checkout_preference_id = db.Column(db.String(64), nullable=True, unique=True)
    # Referência aleatória (não é o id da mensalidade), persistida e única. É por ela que
    # o webhook reencontra a mensalidade quando a notificação vem do Checkout Pro.
    checkout_external_reference = db.Column(db.String(120), nullable=True, unique=True)
    checkout_url = db.Column(db.String(512), nullable=True)
    checkout_ambiente = db.Column(db.String(20), nullable=True)  # 'producao' | 'sandbox'
    # Valor congelado na criação da preferência: se o admin alterar a mensalidade depois,
    # a preferência antiga cobraria o valor errado e precisa ser descartada.
    checkout_valor = db.Column(db.Numeric(10, 2), nullable=True)
    checkout_criado_em = db.Column(db.DateTime, nullable=True)
    checkout_expira_em = db.Column(db.DateTime, nullable=True)

    # Último status/detalhe bruto devolvido pelo provedor - só para exibição ao
    # admin, nunca usado sozinho para decidir se o pagamento foi aprovado.
    provider_status = db.Column(db.String(30), nullable=True)
    provider_status_detail = db.Column(db.String(60), nullable=True)

    # Comprovante manual (dinheiro/transferência) enviado pelo próprio aluno.
    # Enviar o arquivo NUNCA muda o status sozinho - fica 'em_analise' até o admin decidir.
    comprovante_manual_arquivo = db.Column(db.String(64), nullable=True)
    comprovante_manual_enviado_em = db.Column(db.DateTime, nullable=True)
    comprovante_manual_analisado_por = db.Column(db.String(100), nullable=True)
    comprovante_manual_analisado_em = db.Column(db.DateTime, nullable=True)
    comprovante_manual_observacao = db.Column(db.Text, nullable=True)

    aluno = db.relationship('Aluno', backref='pagamentos', lazy=True)
    plano = db.relationship('Plano', backref='pagamentos', lazy=True)

    @property
    def status_efetivo(self):
        """Status a exibir, com o vencimento já aplicado.

        Uma cobrança `pendente` cujo vencimento passou é uma cobrança atrasada, tenha ou
        não a coluna sido promovida ainda. É esta a regra que
        `PagamentoDAO.status_efetivo()` espelha em SQL para os indicadores e os filtros
        do painel: assim a mesma linha nunca aparece como "Pendente" no indicador e
        "Vencida" na tabela.
        """
        if self.status == 'pendente' and self.vencimento and self.vencimento < date.today():
            return 'atrasado'
        return self.status

    def __init__(self, aluno_id, plano_id, valor, vencimento, status='pendente', data_pagamento=None,
                 forma_pagamento=None, provider=None, provider_payment_id=None, external_reference=None,
                 idempotency_key=None, pix_copia_cola=None, ticket_url=None, data_criacao_pix=None,
                 data_expiracao=None, competencia=None, vigencia_inicio=None, vigencia_fim=None):
        self.aluno_id = aluno_id
        self.plano_id = plano_id
        self.valor = _para_decimal(valor)
        self.vencimento = vencimento
        self.status = status
        self.data_pagamento = data_pagamento
        self.forma_pagamento = forma_pagamento
        self.provider = provider
        self.provider_payment_id = provider_payment_id
        self.external_reference = external_reference
        self.idempotency_key = idempotency_key
        self.pix_copia_cola = pix_copia_cola
        self.ticket_url = ticket_url
        self.data_criacao_pix = data_criacao_pix
        self.data_expiracao = data_expiracao
        self.competencia = competencia or (vencimento.strftime('%Y-%m') if vencimento else None)
        self.vigencia_inicio = vigencia_inicio
        self.vigencia_fim = vigencia_fim
