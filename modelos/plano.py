from datetime import date
from decimal import Decimal

from config import db

class Plano(db.Model):
    __tablename__ = 'planos'

    id = db.Column(db.Integer, primary_key=True)
    nome_plano = db.Column(db.String(100), nullable=False)
    preco_plano = db.Column(db.Numeric(10, 2), nullable=False)

    duracao_dias = db.Column(db.Integer, nullable=False, default=30)

    # Plano que a página inicial mostra em destaque. O admin marca no painel; no máximo
    # um fica marcado (PlanoDAO.definir_destaque garante isso).
    destaque = db.Column(db.Boolean, nullable=False, default=False, server_default=db.false())

    # Plano fora de venda. Um plano com mensalidades não pode ser apagado (elas são o
    # histórico financeiro e apontam para ele), então sai de cena assim: some da home,
    # do perfil e dos formulários, e nenhuma cobrança nova nasce nele. O que já existe
    # continua valendo - quem está nele termina o período pago e escolhe outro.
    arquivado = db.Column(db.Boolean, nullable=False, default=False, server_default=db.false())

    # Promoção: de `promocao_inicio` a `promocao_fim` (inclusive), toda cobrança NOVA do
    # plano sai por `preco_promocional`. Cobranças já emitidas não mudam de valor.
    preco_promocional = db.Column(db.Numeric(10, 2), nullable=True)
    promocao_inicio = db.Column(db.Date, nullable=True)
    promocao_fim = db.Column(db.Date, nullable=True)

    def __init__(self, nome_plano, preco_plano, duracao_dias):
        self.nome_plano = nome_plano
        self.preco_plano = preco_plano if isinstance(preco_plano, Decimal) else Decimal(str(preco_plano))
        self.duracao_dias = duracao_dias

    @property
    def tem_promocao(self):
        return self.preco_promocional is not None and bool(self.promocao_inicio and self.promocao_fim)

    def promocao_ativa(self, hoje=None):
        if not self.tem_promocao:
            return False
        return self.promocao_inicio <= (hoje or date.today()) <= self.promocao_fim

    def promocao_agendada(self, hoje=None):
        return self.tem_promocao and (hoje or date.today()) < self.promocao_inicio

    def preco_em(self, hoje=None):
        """Preço de uma cobrança criada em `hoje`."""
        return self.preco_promocional if self.promocao_ativa(hoje) else self.preco_plano

    @property
    def preco_atual(self):
        return self.preco_em()
