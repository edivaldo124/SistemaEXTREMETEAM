"""Rastreamento de erros opcional com Sentry. Sem `SENTRY_DSN`, nada é importado nem enviado.

O sistema lida com CPF, e-mail, telefone, comprovantes e sessões de alunos, então o que
sai para o Sentry é só o necessário para achar o erro:
- `send_default_pii=False` (sem IP, usuário nem cookies) e `include_local_variables=False`
  (variáveis locais de um frame podem ter senha, CPF ou o formulário inteiro);
- corpo da requisição nunca é lido (`max_request_body_size='never'`);
- `before_send` tira de novo cookies, query string, corpo, ambiente e usuário, deixa só
  cabeçalhos inofensivos e mascara CPF, e-mail, tokens de link e os parâmetros de SQL
  (um IntegrityError do SQLAlchemy traz todos os valores do INSERT) em qualquer texto.

Limite: tokens são reconhecidos em URL (caminho de /recuperar_senha, /ativar-acesso,
/confirmar_email e parâmetros token/code/state). Um token solto no texto de uma
exceção não tem forma reconhecível; o código não deve montar mensagens assim.
"""

import os
import re

# Cabeçalhos que ajudam a reproduzir o erro e não identificam nem autenticam ninguém.
# Todo o resto (Cookie, Authorization, X-CSRFToken, X-Forwarded-For...) sai.
CABECALHOS_PERMITIDOS = {
    'accept', 'accept-language', 'content-length', 'content-type', 'host', 'referer', 'user-agent',
}
# Chaves removidas em qualquer nível do evento.
CHAVES_REMOVIDAS = {'cookies', 'query_string', 'env', 'user', 'vars', 'http.query', 'http.fragment'}

_CPF = re.compile(r'(?<!\d)\d{3}\.?\d{3}\.?\d{3}-?\d{2}(?!\d)')
_EMAIL = re.compile(r'[\w.+-]+@[\w-]+(?:\.[\w-]+)+')
_TOKEN_NO_CAMINHO = re.compile(r'(/(?:recuperar_senha|ativar-acesso|confirmar_email)/)[^/\s?#"\'<>]+')
_TOKEN_NA_QUERY = re.compile(r'([?&](?:token|code|state|access_token|refresh_token)=)[^&\s#"\'<>]+', re.I)
_PARAMETROS_SQL = re.compile(r'\[parameters: .*?(?=\n\(Background on this error|\Z)', re.S)


def mascarar(texto):
    texto = _PARAMETROS_SQL.sub('[parameters: removidos]', texto)
    texto = _TOKEN_NO_CAMINHO.sub(r'\1[token]', texto)
    texto = _TOKEN_NA_QUERY.sub(r'\1[token]', texto)
    texto = _EMAIL.sub('[e-mail]', texto)
    return _CPF.sub('[cpf]', texto)


def _limpar(valor):
    if isinstance(valor, str):
        return mascarar(valor)
    if isinstance(valor, dict):
        return {chave: _limpar(item) for chave, item in valor.items() if chave not in CHAVES_REMOVIDAS}
    if isinstance(valor, (list, tuple)):
        return [_limpar(item) for item in valor]
    return valor


def before_send(evento, _dica=None):
    requisicao = evento.get('request')
    if isinstance(requisicao, dict):
        requisicao.pop('data', None)
        cabecalhos = requisicao.get('headers')
        if isinstance(cabecalhos, dict):
            requisicao['headers'] = {
                nome: valor for nome, valor in cabecalhos.items()
                if nome.lower() in CABECALHOS_PERMITIDOS
            }
    return _limpar(evento)


def before_breadcrumb(rastro, _dica=None):
    return _limpar(rastro)


def iniciar_sentry():
    dsn = (os.environ.get('SENTRY_DSN') or '').strip()
    if not dsn:
        return False

    import sentry_sdk
    from sentry_sdk.integrations.flask import FlaskIntegration

    sentry_sdk.init(
        dsn=dsn,
        environment=(os.environ.get('SENTRY_ENVIRONMENT') or 'producao').strip(),
        # Nome da rota ("auth.pagina_login"), nunca o caminho com CPF ou token.
        integrations=[FlaskIntegration(transaction_style='endpoint')],
        send_default_pii=False,
        include_local_variables=False,
        max_request_body_size='never',
        before_send=before_send,
        before_breadcrumb=before_breadcrumb,
        # Só erros: sem rastreamento de desempenho.
        traces_sample_rate=0.0,
    )
    return True
