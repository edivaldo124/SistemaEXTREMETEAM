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
