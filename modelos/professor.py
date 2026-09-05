from config import db
from servicos.contatos import link_email
from werkzeug.security import generate_password_hash, check_password_hash


class Professor(db.Model):
    __tablename__ = 'professores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    nome_publico = db.Column(db.String(150), nullable=True)
    modalidades = db.Column(db.String(200), nullable=True)
    biografia = db.Column(db.Text, nullable=True)
    formacao = db.Column(db.Text, nullable=True)
    instagram = db.Column(db.String(30), nullable=True)
    email_publico = db.Column(db.String(150), nullable=True)
    whatsapp = db.Column(db.String(20), nullable=True)
    foto_arquivo = db.Column(db.String(64), nullable=True)
    perfil_publico = db.Column(db.Boolean, nullable=False, default=False, server_default=db.false())
    exibir_instagram = db.Column(db.Boolean, nullable=False, default=False, server_default=db.false())
    exibir_email = db.Column(db.Boolean, nullable=False, default=False, server_default=db.false())
    exibir_whatsapp = db.Column(db.Boolean, nullable=False, default=False, server_default=db.false())

    def __init__(self, nome, login, senha):
        self.nome = nome
        self.login = login
        self.set_senha(senha)

    def set_senha(self, senha_texto_puro):
        self.senha_hash = generate_password_hash(senha_texto_puro)

    def verificar_senha(self, senha_texto_puro):
        return check_password_hash(self.senha_hash, senha_texto_puro)

    @property
    def nome_exibicao(self):
        return self.nome_publico or self.nome

    @property
    def instagram_url(self):
        return f'https://www.instagram.com/{self.instagram}/' if self.instagram else None

    @property
    def email_url(self):
        return link_email(self.email_publico)

    @property
    def whatsapp_url(self):
        return f'https://wa.me/{self.whatsapp}' if self.whatsapp else None
