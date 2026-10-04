"""Planilha econômica: fluxo de caixa mês a mês.

Entrada é a mensalidade paga, no mês em que o dinheiro entrou: a data do pagamento, ou o
vencimento nos lançamentos antigos que não têm essa data. Pendente, em análise, recusada,
cancelada e reembolsada não entram. Saída é a despesa lançada pelo admin, no mês da data
informada.

Os totais saem agregados do banco, como os do painel financeiro, e nunca somados no front.
"""
import calendar
from dataclasses import dataclass
from datetime import date
from decimal import ROUND_HALF_UP, Decimal

from sqlalchemy import func
from sqlalchemy.orm import joinedload

from config import db
from modelos.despesa import CATEGORIAS_DESPESA, Despesa, rotulo_categoria
from modelos.pagamento import Pagamento
from servicos.formatacao import MESES_PT

ANO_MINIMO = 2000
ZERO = Decimal('0.00')


@dataclass(frozen=True)
class Mes:
    numero: int
    entradas: Decimal
    saidas: Decimal
    acumulado: Decimal

    @property
    def nome(self):
        return MESES_PT[self.numero]

    @property
    def saldo(self):
        return self.entradas - self.saidas


@dataclass(frozen=True)
class Categoria:
    chave: str
    total: Decimal
    por_mes: dict
    percentual: int

    @property
    def rotulo(self):
        return rotulo_categoria(self.chave)


@dataclass(frozen=True)
class ResumoAnual:
    ano: int
    meses: list
    categorias: list
    entradas: Decimal
    saidas: Decimal

    @property
    def saldo(self):
        return self.entradas - self.saidas

    def mes(self, numero):
        return next((m for m in self.meses if m.numero == numero), None)


def limites_do_ano(ano):
    return date(ano, 1, 1), date(ano, 12, 31)


def limites_do_mes(ano, mes):
    return date(ano, mes, 1), date(ano, mes, calendar.monthrange(ano, mes)[1])


def data_da_entrada():
    return func.coalesce(Pagamento.data_pagamento, Pagamento.vencimento)


def _entradas(inicio, fim):
    data = data_da_entrada()
    return Pagamento.query.filter(Pagamento.status == 'pago', data >= inicio, data <= fim)


def _decimal(valor):
    return Decimal(valor or 0).quantize(ZERO)


def resumo_anual(ano, *, hoje):
    """Entradas, saídas e saldo de cada mês do ano, e as saídas por categoria.

    Um mês que ainda não começou só aparece se já tiver movimento (uma despesa lançada
    adiantada): doze linhas zeradas no começo do ano não dizem nada.
    """
    inicio, fim = limites_do_ano(ano)

    mes_da_entrada = func.extract('month', data_da_entrada())
    entradas = {
        int(mes): _decimal(total)
        for mes, total in _entradas(inicio, fim)
        .with_entities(mes_da_entrada, func.sum(Pagamento.valor))
        .group_by(mes_da_entrada)
    }

    mes_da_saida = func.extract('month', Despesa.data)
    saidas = {}
    por_categoria = {}
    for mes, categoria, total in (
        db.session.query(mes_da_saida, Despesa.categoria, func.sum(Despesa.valor))
        .filter(Despesa.data >= inicio, Despesa.data <= fim)
        .group_by(mes_da_saida, Despesa.categoria)
    ):
        mes, total = int(mes), _decimal(total)
        saidas[mes] = saidas.get(mes, ZERO) + total
        por_categoria.setdefault(categoria, {})[mes] = total

    meses = []
    acumulado = ZERO
    for numero in range(1, 13):
        entrada, saida = entradas.get(numero, ZERO), saidas.get(numero, ZERO)
        if date(ano, numero, 1) > hoje and not (entrada or saida):
            continue
        acumulado += entrada - saida
        meses.append(Mes(numero, entrada, saida, acumulado))

    total_saidas = sum(saidas.values(), ZERO)

    def percentual(parte):
        if not total_saidas:
            return 0
        return int((parte * 100 / total_saidas).quantize(Decimal('1'), rounding=ROUND_HALF_UP))

    categorias = []
    for chave, valores in por_categoria.items():
        total = sum(valores.values(), ZERO)
        categorias.append(Categoria(chave=chave, total=total, por_mes=valores, percentual=percentual(total)))
    # Maior gasto primeiro; no empate, a ordem da lista fixa de categorias.
    ordem = list(CATEGORIAS_DESPESA)
    categorias.sort(key=lambda c: (-c.total, ordem.index(c.chave) if c.chave in ordem else len(ordem)))

    return ResumoAnual(
        ano=ano, meses=meses, categorias=categorias,
        entradas=sum(entradas.values(), ZERO), saidas=total_saidas,
    )


def anos_disponiveis(*, hoje):
    """Do primeiro ano com movimento até o último (ou o atual), do mais recente ao mais antigo."""
    datas = [
        db.session.query(func.min(data_da_entrada()), func.max(data_da_entrada()))
        .filter(Pagamento.status == 'pago').one(),
        db.session.query(func.min(Despesa.data), func.max(Despesa.data)).one(),
    ]
    anos = [hoje.year] + [d.year for par in datas for d in par if d]
    primeiro = max(min(anos), ANO_MINIMO)
    return list(range(max(anos), primeiro - 1, -1))


def entradas_detalhadas(ano):
    """Mensalidades pagas no ano, na ordem em que o dinheiro entrou (para o Excel)."""
    inicio, fim = limites_do_ano(ano)
    return (
        _entradas(inicio, fim)
        .options(joinedload(Pagamento.aluno), joinedload(Pagamento.plano))
        .order_by(data_da_entrada(), Pagamento.id)
        .all()
    )


def saidas_detalhadas(ano):
    inicio, fim = limites_do_ano(ano)
    return (
        Despesa.query
        .filter(Despesa.data >= inicio, Despesa.data <= fim)
        .order_by(Despesa.data, Despesa.id)
        .all()
    )
