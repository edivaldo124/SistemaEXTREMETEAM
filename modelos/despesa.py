"""Saídas de caixa lançadas pelo admin (aluguel, luz, salários...).

As entradas da planilha econômica não moram aqui: saem das mensalidades pagas
(`pagamentos`). Esta tabela guarda só o que sai, já pago na data informada.
"""
from datetime import datetime

from config import db

# Lista fixa, escolhida pela academia. A chave vai para o banco; o rótulo, para a tela e
# para o Excel. Trocar um rótulo não mexe nos lançamentos antigos; apagar uma chave deixa
# os lançamentos dela sem rótulo, então chave não se apaga.
CATEGORIAS_DESPESA = {
    'aluguel': 'Aluguel',
    'contas': 'Água, luz e internet',
    'pessoal': 'Salários e professores',
    'equipamentos': 'Equipamentos',
    'manutencao': 'Manutenção e limpeza',
    'marketing': 'Marketing',
    'impostos': 'Impostos e taxas',
    'outros': 'Outros',
}

DESCRICAO_MAXIMO = 120


def rotulo_categoria(chave):
    return CATEGORIAS_DESPESA.get(chave, chave or '—')


class Despesa(db.Model):
    __tablename__ = 'despesas'

    # A planilha sempre lê um intervalo de datas (o ano ou o mês escolhido).
    __table_args__ = (db.Index('ix_despesas_data', 'data'),)

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    categoria = db.Column(db.String(20), nullable=False)
    descricao = db.Column(db.String(DESCRICAO_MAXIMO), nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    # Login do admin que lançou ou alterou por último; só para conferência no Excel.
    lancado_por = db.Column(db.String(80), nullable=True)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @property
    def rotulo_categoria(self):
        return rotulo_categoria(self.categoria)
