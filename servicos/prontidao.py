"""Verificação de prontidão (/health/pronto): o banco e o Redis respondem agora?

/health continua sendo só "o processo está de pé" (liveness, usado pelo healthcheck do
compose). Este aqui é para o monitor externo: responde 503 quando uma dependência cai.
Cada verificação tem prazo curto e devolve só verdadeiro/falso; o motivo vai para o log
do servidor, nunca para a resposta (nem mensagem de erro, nem host, nem credencial).
"""

import logging
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as PrazoEsgotado

from sqlalchemy import text

from config import db

logger = logging.getLogger(__name__)

PRAZO_SEGUNDOS = 2
# O psycopg2 não tem prazo de leitura: com o servidor do banco inalcançável, um SELECT
# numa conexão do pool pode travar por minutos. A consulta roda numa thread à parte e a
# resposta sai no prazo de qualquer jeito; a thread presa termina sozinha quando o TCP
# desistir. Duas threads bastam para o ritmo de um monitor externo.
_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix='prontidao')


def _consultar_banco(app):
    with app.app_context():
        with db.engine.connect() as conexao:
            if conexao.dialect.name == 'postgresql':
                conexao.execute(text(f"SET LOCAL statement_timeout = '{PRAZO_SEGUNDOS}s'"))
            conexao.execute(text('SELECT 1'))


def banco_responde(app):
    futuro = _executor.submit(_consultar_banco, app)
    try:
        futuro.result(timeout=PRAZO_SEGUNDOS + 1)
        return True
    except PrazoEsgotado:
        logger.warning('Prontidão: o banco não respondeu em %ss.', PRAZO_SEGUNDOS + 1)
    except Exception:
        logger.warning('Prontidão: o banco recusou a consulta.', exc_info=True)
    return False


def redis_responde(uri):
    """None quando o limite de requisições não usa Redis (memory:// em desenvolvimento)."""
    if not uri.startswith(('redis://', 'rediss://')):
        return None
    import redis

    cliente = redis.Redis.from_url(
        uri, socket_connect_timeout=PRAZO_SEGUNDOS, socket_timeout=PRAZO_SEGUNDOS,
    )
    try:
        return bool(cliente.ping())
    except Exception:
        logger.warning('Prontidão: o Redis não respondeu.', exc_info=True)
        return False
    finally:
        cliente.close()


def verificar(app):
    resultado = {'banco': banco_responde(app)}
    redis_ok = redis_responde(app.config.get('RATELIMIT_STORAGE_URI') or '')
    if redis_ok is not None:
        resultado['redis'] = redis_ok
    return resultado
