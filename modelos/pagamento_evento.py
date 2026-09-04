from datetime import datetime

from config import db


class PagamentoEvento(db.Model):
    """Histórico de auditoria de uma mensalidade (nunca grava credenciais ou dados sensíveis)."""

    __tablename__ = 'pagamentos_eventos'

    id = db.Column(db.Integer, primary_key=True)
    pagamento_id = db.Column(db.Integer, db.ForeignKey('pagamentos.id'), nullable=False)
    tipo = db.Column(db.String(40), nullable=False)
    detalhe = db.Column(db.Text, nullable=True)
    # Quem originou o evento: 'sistema', 'webhook_mercado_pago', login do admin ou do aluno.
    ator = db.Column(db.String(100), nullable=True)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    pagamento = db.relationship(
        'Pagamento',
        backref=db.backref('eventos', lazy=True, order_by='PagamentoEvento.criado_em.desc()'),
    )

    def __init__(self, pagamento_id, tipo, detalhe=None, ator=None):
        self.pagamento_id = pagamento_id
        self.tipo = tipo
        self.detalhe = detalhe
        self.ator = ator
