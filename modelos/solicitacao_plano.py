from datetime import datetime

from config import db

STATUS_PENDENTE = 'pendente'
STATUS_EFETIVADA = 'efetivada'
STATUS_CANCELADA = 'cancelada'

TIPO_DOWNGRADE = 'downgrade'
TIPO_UPGRADE = 'upgrade'


class SolicitacaoMudancaPlano(db.Model):
    """Pedido de troca de plano agendado para a próxima renovação.

    Nunca altera o plano vigente, nunca gera cobrança e nunca devolve dinheiro: o aluno
    mantém o plano que pagou (e os benefícios dele) até o fim da vigência, e a mudança
    só é aplicada quando nasce a cobrança do período seguinte. Sozinha, a solicitação
    também não libera o novo período - isso continua dependendo do pagamento.
    """

    __tablename__ = 'solicitacoes_mudanca_plano'

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)

    # Plano em que o aluno estava quando pediu a troca. Guardado junto com o valor para
    # que o histórico continue verdadeiro mesmo que o admin reajuste o preço depois.
    plano_origem_id = db.Column(db.Integer, db.ForeignKey('planos.id'), nullable=True)
    plano_destino_id = db.Column(db.Integer, db.ForeignKey('planos.id'), nullable=False)
    valor_origem = db.Column(db.Numeric(10, 2), nullable=True)
    valor_destino = db.Column(db.Numeric(10, 2), nullable=False)

    tipo = db.Column(db.String(20), nullable=False, default=TIPO_DOWNGRADE)
    status = db.Column(db.String(20), nullable=False, default=STATUS_PENDENTE)

    # Primeiro dia em que a mudança passa a valer: o dia seguinte ao fim do último
    # período já pago ou já aguardando decisão (comprovante em análise, por exemplo).
    vigencia_a_partir_de = db.Column(db.Date, nullable=True)

    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    criado_por = db.Column(db.String(100), nullable=True)
    efetivado_em = db.Column(db.DateTime, nullable=True)
    # Mensalidade do novo período que aplicou a mudança - rastreia a efetivação.
    pagamento_efetivacao_id = db.Column(db.Integer, db.ForeignKey('pagamentos.id'), nullable=True)
    cancelado_em = db.Column(db.DateTime, nullable=True)
    cancelado_por = db.Column(db.String(100), nullable=True)
    observacao = db.Column(db.String(255), nullable=True)

    aluno = db.relationship('Aluno', backref=db.backref('solicitacoes_plano', lazy=True))
    plano_origem = db.relationship('Plano', foreign_keys=[plano_origem_id], lazy=True)
    plano_destino = db.relationship('Plano', foreign_keys=[plano_destino_id], lazy=True)

    def __init__(self, aluno_id, plano_destino_id, valor_destino, plano_origem_id=None,
                 valor_origem=None, tipo=TIPO_DOWNGRADE, vigencia_a_partir_de=None,
                 criado_por=None, observacao=None):
        self.aluno_id = aluno_id
        self.plano_origem_id = plano_origem_id
        self.plano_destino_id = plano_destino_id
        self.valor_origem = valor_origem
        self.valor_destino = valor_destino
        self.tipo = tipo
        self.status = STATUS_PENDENTE
        self.vigencia_a_partir_de = vigencia_a_partir_de
        self.criado_por = criado_por
        self.observacao = observacao

    @property
    def esta_pendente(self):
        return self.status == STATUS_PENDENTE
