"""Orçamentos compartilhados das chamadas interativas ao provedor de pagamento."""

from flask import session
from flask_limiter.util import get_remote_address

from config import limiter


def chave_pagamento():
    """A mesma conta mantém seu limite entre sessões, rotas e mensalidades.

    Alunos que usam a mesma rede têm orçamentos separados. Sem identidade
    autenticada, o IP limita as tentativas que as próprias rotas vão recusar.
    """
    tipo = session.get('tipo_usuario')
    if tipo == 'aluno' and session.get('aluno_id') is not None:
        return f"pagamento:aluno:{session['aluno_id']}"
    if tipo == 'admin' and session.get('usuario'):
        return f"pagamento:admin:{session['usuario']}"
    return f'pagamento:anonimo:{get_remote_address()}'


limitar_criacao_pagamento = limiter.shared_limit(
    '10 per minute', scope='pagamentos:criacao', key_func=chave_pagamento,
)
limitar_consulta_pagamento = limiter.shared_limit(
    '30 per minute', scope='pagamentos:consulta', key_func=chave_pagamento,
)
