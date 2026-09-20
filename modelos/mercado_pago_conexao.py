from config import db


class MercadoPagoConexao(db.Model):
    """Conta do Mercado Pago que a academia autorizou por OAuth.

    Uma linha só (a academia é única). Os tokens ficam cifrados: quem lê o banco ou um
    backup não consegue movimentar a conta. Quem cifra e decifra é
    `servicos.mercado_pago_conta` - nada fora dele deve tocar nessas colunas.
    """
    __tablename__ = 'mercado_pago_conexao'
    __table_args__ = (db.CheckConstraint('id = 1', name='ck_mercado_pago_conexao_unica'),)

    id = db.Column(db.Integer, primary_key=True, default=1)
    mp_user_id = db.Column(db.String(40), nullable=False)
    public_key = db.Column(db.String(200), nullable=True)
    access_token_cifrado = db.Column(db.Text, nullable=False)
    refresh_token_cifrado = db.Column(db.Text, nullable=False)
    live_mode = db.Column(db.Boolean, nullable=False, default=True)
    expira_em = db.Column(db.DateTime, nullable=False)
    conectado_em = db.Column(db.DateTime, nullable=False)
    renovado_em = db.Column(db.DateTime, nullable=True)
    # O Mercado Pago recusou a renovação (autorização revogada ou refresh_token
    # inválido): só um novo "Conectar" resolve.
    precisa_reconectar = db.Column(db.Boolean, nullable=False, default=False)
