import hmac
from pathlib import Path

_ARQUIVO_SENHAS_COMUNS = Path(__file__).with_name('senhas_comuns.txt')


def _carregar_senhas_comuns():
    """Lê a lista de senhas comuns (uma por linha; `#` abre comentário) para um conjunto.

    Sem o arquivo a validação não pode ficar frouxa em silêncio: o mínimo embutido
    mantém as piores senhas recusadas e o erro aparece no arranque, não em produção.
    """
    embutidas = {'12345678', '123456789', '1234567890', 'academia', 'admin123', 'password', 'qwerty123', 'senha123'}
    try:
        linhas = _ARQUIVO_SENHAS_COMUNS.read_text(encoding='utf-8').splitlines()
    except OSError as erro:
        raise RuntimeError(f'Lista de senhas comuns ausente: {_ARQUIVO_SENHAS_COMUNS}') from erro
    return frozenset(embutidas | {l.strip().casefold() for l in linhas if l.strip() and not l.startswith('#')})


SENHAS_COMUNS = _carregar_senhas_comuns()

MSG_CONFIRMACAO_DIVERGENTE = 'A senha e a confirmação não são iguais. Digite a mesma senha nos dois campos.'


def erro_validacao_senha(senha, *identificadores):
    """Retorna uma mensagem quando a senha é curta, comum ou igual ao identificador."""
    if len(senha or '') < 8:
        return 'A senha deve ter pelo menos 8 caracteres.'

    normalizada = senha.casefold()
    if normalizada in SENHAS_COMUNS:
        return 'Escolha uma senha menos comum.'

    identificadores_validos = {
        (valor or '').strip().casefold() for valor in identificadores if (valor or '').strip()
    }
    if normalizada in identificadores_validos:
        return 'A senha não pode ser igual ao seu usuário, e-mail ou CPF.'
    return None


def erro_confirmacao_senha(senha, confirmacao):
    """Retorna uma mensagem quando a confirmação não repete exatamente a senha.

    A confirmação existe só para o tempo da requisição: nunca é gravada, nem registrada
    em log. A comparação é feita em tempo constante, como no resto do projeto.
    """
    if not hmac.compare_digest((senha or '').encode('utf-8'), (confirmacao or '').encode('utf-8')):
        return MSG_CONFIRMACAO_DIVERGENTE
    return None
