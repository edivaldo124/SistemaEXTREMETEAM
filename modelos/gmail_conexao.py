from config import db


class GmailConexao(db.Model):
    __tablename__ = 'gmail_conexao'
    __table_args__ = (db.CheckConstraint('id = 1', name='ck_gmail_conexao_unica'),)

    id = db.Column(db.Integer, primary_key=True, default=1)
    email = db.Column(db.String(320), nullable=False)
    refresh_token_cifrado = db.Column(db.Text, nullable=False)
    conectado_em = db.Column(db.DateTime, nullable=False)
