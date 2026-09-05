import re


def somente_digitos(valor):
    return re.sub(r'\D', '', valor or '')


def formatar_cpf(valor):
    digitos = somente_digitos(valor)[:11]
    if len(digitos) != 11:
        return (valor or '').strip()
    return f'{digitos[:3]}.{digitos[3:6]}.{digitos[6:9]}-{digitos[9:]}'


def variantes_cpf(valor):
    digitos = somente_digitos(valor)
    if len(digitos) != 11:
        return [(valor or '').strip()]
    return [digitos, formatar_cpf(digitos)]


def formatar_telefone(valor):
    digitos = somente_digitos(valor)[:11]
    if len(digitos) == 11:
        return f'({digitos[:2]}) {digitos[2:7]}-{digitos[7:]}'
    if len(digitos) == 10:
        return f'({digitos[:2]}) {digitos[2:6]}-{digitos[6:]}'
    return (valor or '').strip()


MESES_PT = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
    7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro',
}


def formatar_competencia(competencia):
    """Converte 'AAAA-MM' em algo como 'Setembro de 2026'. Devolve o valor original
    se não estiver no formato esperado (evita quebrar a tela por um dado antigo/ausente)."""
    if not competencia or '-' not in competencia:
        return competencia or '—'
    ano_str, mes_str = competencia.split('-', 1)
    try:
        mes = int(mes_str)
        ano = int(ano_str)
    except ValueError:
        return competencia
    nome_mes = MESES_PT.get(mes)
    if not nome_mes:
        return competencia
    return f'{nome_mes} de {ano}'


def formatar_moeda(valor):
    """Formata um valor em reais no padrão brasileiro: R$ 1.080,00.

    Usado como filtro Jinja (`{{ valor|moeda }}`) no lugar de
    `'%.2f'|format(v)|replace('.', ',')`, que não separava o milhar."""
    if valor is None:
        return '—'
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        return str(valor)
    inteiro, centavos = f'{abs(numero):.2f}'.split('.')
    grupos = []
    while len(inteiro) > 3:
        grupos.insert(0, inteiro[-3:])
        inteiro = inteiro[:-3]
    grupos.insert(0, inteiro)
    sinal = '-' if numero < 0 else ''
    return f'R$ {sinal}{".".join(grupos)},{centavos}'


ROTULOS_FORMA_PAGAMENTO = {
    'pix': 'Pix',
    'dinheiro': 'Dinheiro',
    'transferencia': 'Transferência',
    'cartao_credito': 'Cartão de crédito',
    'cartao_debito': 'Cartão de débito',
    'boleto': 'Boleto',
}


def rotulo_forma_pagamento(forma):
    """Nome legível da forma de pagamento. Antes as telas usavam
    `|replace('_',' ')|title`, que devolvia "Cartao Credito", sem acento."""
    if not forma:
        return '—'
    return ROTULOS_FORMA_PAGAMENTO.get(forma, forma.replace('_', ' ').capitalize())
