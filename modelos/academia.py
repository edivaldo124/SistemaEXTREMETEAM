from urllib.parse import urlencode

from config import db
from servicos.contatos import link_email


class Academia(db.Model):
    __tablename__ = 'academia'
    __table_args__ = (db.CheckConstraint('id = 1', name='ck_academia_unica'),)

    id = db.Column(db.Integer, primary_key=True, default=1)
    instagram = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(150), nullable=True)
    whatsapp = db.Column(db.String(20), nullable=True)
    endereco = db.Column(db.String(300), nullable=True)
    complemento = db.Column(db.String(150), nullable=True)
    horarios = db.Column(db.String(1000), nullable=True)

    @property
    def instagram_url(self):
        return f'https://www.instagram.com/{self.instagram}/' if self.instagram else None

    @property
    def email_url(self):
        return link_email(self.email)

    @property
    def whatsapp_url(self):
        return f'https://wa.me/{self.whatsapp}' if self.whatsapp else None

    @property
    def mapa_url(self):
        if not self.endereco:
            return None
        return 'https://www.google.com/maps/search/?' + urlencode({'api': '1', 'query': self.endereco})

    @property
    def tem_contato(self):
        return bool(self.instagram or self.email or self.whatsapp or self.endereco or self.horarios)
