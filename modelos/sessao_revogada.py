"""Sessões encerradas pelo logout.

A sessão do Flask é um cookie assinado, sem estado no servidor: `session.clear()` limpa
só a cópia do navegador de quem clicou em "Sair". Uma cópia feita antes (perfil do
navegador de um PC compartilhado, extensão, log de proxy com inspeção TLS) seguia valendo,
e a renovação a cada requisição a mantinha viva sem limite.

Cada login recebe um identificador aleatório (`sid`) dentro do cookie e o logout grava esse
identificador aqui. Toda verificação de acesso recusa um `sid` que esteja nesta tabela.

A linha só precisa existir enquanto alguma cópia do cookie puder valer: o cookie expira
`PERMANENT_SESSION_LIFETIME` depois da última renovação, e a última renovação é anterior ao
logout. Depois disso a linha é apagada na próxima revogação.
"""
from config import db


class SessaoRevogada(db.Model):
    __tablename__ = 'sessoes_revogadas'

    sid = db.Column(db.String(32), primary_key=True)
    expira_em = db.Column(db.DateTime, nullable=False, index=True)
