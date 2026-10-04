
from flask import session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_limiter import Limit, Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect


def chave_da_conta():
    """Chave de limite por CONTA, caindo no IP só para quem não está autenticado.

    A academia inteira costuma sair por um IP só (o Wi-Fi da recepção, o 4G de uma
    operadora). Limitar por IP as ações de quem já entrou faria um aluno consumir a cota
    do outro: quem trocasse a foto de perfil deixaria os colegas sem trocar a sua.
    """
    tipo = session.get('tipo_usuario')
    if tipo == 'aluno' and session.get('aluno_id'):
        return f'aluno:{session["aluno_id"]}'
    if tipo == 'professor' and session.get('professor_id'):
        return f'professor:{session["professor_id"]}'
    if tipo == 'admin':
        return 'admin'
    return f'ip:{get_remote_address()}'


db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
# Teto para toda rota sem limite próprio (um decorador na rota substitui este). Os
# limites declarados sem `key_func` continuam por IP; o padrão é por conta. Arquivos de
# /static/ já ficam de fora pelo próprio Flask-Limiter, e /health usa `@limiter.exempt`.
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[Limit('300 per minute;3000 per hour', key_function=chave_da_conta)],
)
