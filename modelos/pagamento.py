from config import db


class Pagamento(db.Model):
    __tablename__ = 'pagamentos'

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    plano_id = db.Column(db.Integer, db.ForeignKey('planos.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    vencimento = db.Column(db.Date, nullable=False)
    data_pagamento = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pendente')
    forma_pagamento = db.Column(db.String(30), nullable=True)

    # RF: pagamento via Pix (Mercado Pago). Todos nullable/aditivos - linhas antigas
    # (lançamentos manuais do admin) ficam com provider=None e não são afetadas.
    provider = db.Column(db.String(20), nullable=True)  # None (manual/legado) | 'mercado_pago'
    provider_payment_id = db.Column(db.String(64), nullable=True, unique=True)
    external_reference = db.Column(db.String(120), nullable=True, unique=True)
    idempotency_key = db.Column(db.String(64), nullable=True)
    pix_copia_cola = db.Column(db.Text, nullable=True)
    ticket_url = db.Column(db.String(255), nullable=True)
    data_criacao_pix = db.Column(db.DateTime, nullable=True)
    data_expiracao = db.Column(db.DateTime, nullable=True)

    aluno = db.relationship('Aluno', backref='pagamentos', lazy=True)
    plano = db.relationship('Plano', backref='pagamentos', lazy=True)

    def __init__(self, aluno_id, plano_id, valor, vencimento, status='pendente', data_pagamento=None,
                 forma_pagamento=None, provider=None, provider_payment_id=None, external_reference=None,
                 idempotency_key=None, pix_copia_cola=None, ticket_url=None, data_criacao_pix=None,
                 data_expiracao=None):
        self.aluno_id = aluno_id
        self.plano_id = plano_id
        self.valor = valor
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
