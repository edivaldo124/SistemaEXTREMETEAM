import hmac

SENHAS_COMUNS = {
    '12345678',
    '123456789',
    '1234567890',
    'academia',
    'admin123',
    'password',
    'qwerty123',
    'senha123',
}

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
