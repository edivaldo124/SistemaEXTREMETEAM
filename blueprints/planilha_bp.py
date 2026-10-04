"""Planilha econômica: fluxo de caixa do ano, lançamento de despesas e download em Excel."""
from datetime import date

from flask import Blueprint, Response, abort, flash, redirect, render_template, request, session, url_for

from blueprints.adm_bp import PRECO_MAXIMO, _valor_em_reais
from config import chave_da_conta, limiter
from dao.despesaDAO import DespesaDAO
from modelos.despesa import CATEGORIAS_DESPESA, DESCRICAO_MAXIMO, Despesa
from servicos import planilha, planilha_excel
from servicos.autorizacao import admin_requerido
from servicos.formatacao import MESES_PT

planilha_bp = Blueprint('planilha', __name__)

# Fim de mês é dia de lançar as contas todas de uma vez; o limite das outras escritas do
# admin (60/h) cortaria no meio.
LIMITE_ESCRITA = '120 per hour'


def _ano_valido(ano, hoje):
    return ano is not None and planilha.ANO_MINIMO <= ano <= hoje.year + 1


def _ano_e_mes(fonte, hoje):
    """Ano e mês em exibição. Sem mês, o atual no ano corrente e dezembro nos outros."""
    ano = fonte.get('ano', type=int)
    if not _ano_valido(ano, hoje):
        ano = hoje.year
    mes = fonte.get('mes', type=int)
    if mes is None or not 1 <= mes <= 12:
        mes = hoje.month if ano == hoje.year else 12
    return ano, mes


def _ler_despesa(form, hoje):
    """`(dados, erros, valores)`: o texto digitado (para devolver ao formulário), o erro
    de cada campo e os valores prontos para gravar."""
    dados = {campo: (form.get(campo) or '').strip() for campo in ('data', 'categoria', 'descricao', 'valor')}
    erros, valores = {}, {}

    try:
        data = date.fromisoformat(dados['data'])
    except ValueError:
        erros['data'] = 'Informe a data da despesa.'
    else:
        if not _ano_valido(data.year, hoje):
            erros['data'] = f'Use uma data entre {planilha.ANO_MINIMO} e {hoje.year + 1}.'
        else:
            valores['data'] = data

    if dados['categoria'] in CATEGORIAS_DESPESA:
        valores['categoria'] = dados['categoria']
    else:
        erros['categoria'] = 'Escolha uma categoria.'

    if not dados['descricao']:
        erros['descricao'] = 'Descreva a despesa.'
    elif len(dados['descricao']) > DESCRICAO_MAXIMO:
        erros['descricao'] = f'Use até {DESCRICAO_MAXIMO} caracteres.'
    else:
        valores['descricao'] = dados['descricao']

    try:
        valor = _valor_em_reais(dados['valor'])
    except ValueError:
        valor = None
    if valor is None or valor <= 0 or valor > PRECO_MAXIMO:
        erros['valor'] = 'Informe um valor maior que zero, como 150,00.'
    else:
        valores['valor'] = valor.quantize(planilha.ZERO)

    return dados, erros, valores


def _formulario_de(despesa):
    return {
        'data': despesa.data.isoformat(),
        'categoria': despesa.categoria,
        'descricao': despesa.descricao,
        'valor': f'{despesa.valor:.2f}'.replace('.', ','),
    }


def _pagina(ano, mes, *, hoje, editando=None, form=None, erros=None, status=200):
    resumo = planilha.resumo_anual(ano, hoje=hoje)
    inicio, fim = planilha.limites_do_mes(ano, mes)
    if form is None:
        if editando:
            form = _formulario_de(editando)
        else:
            # Lançar no mês que está aberto: hoje no mês corrente, o dia 1 nos outros.
            sugestao = hoje if (ano, mes) == (hoje.year, hoje.month) else inicio
            form = {'data': sugestao.isoformat(), 'categoria': '', 'descricao': '', 'valor': ''}
    anterior = (ano, mes - 1) if mes > 1 else (ano - 1, 12)
    proximo = (ano, mes + 1) if mes < 12 else (ano + 1, 1)
    return render_template(
        'planilha.html',
        ano=ano,
        mes=mes,
        nome_mes=MESES_PT[mes],
        mes_anterior=anterior if _ano_valido(anterior[0], hoje) else None,
        mes_seguinte=proximo if _ano_valido(proximo[0], hoje) else None,
        meses_nomes=MESES_PT,
        anos=planilha.anos_disponiveis(hoje=hoje),
        resumo=resumo,
        despesas=DespesaDAO.listar_periodo(inicio, fim),
        categorias=CATEGORIAS_DESPESA,
        descricao_maximo=DESCRICAO_MAXIMO,
        editando=editando,
        form=form,
        erros=erros or {},
    ), status


def _voltar_para(despesa_ou_data):
    data = getattr(despesa_ou_data, 'data', despesa_ou_data)
    return redirect(url_for('planilha.pagina', ano=data.year, mes=data.month, _anchor='saidas'))


@planilha_bp.route('/admin/planilha')
@admin_requerido
def pagina():
    hoje = date.today()
    ano, mes = _ano_e_mes(request.args, hoje)
    editando = None
    editar_id = request.args.get('editar', type=int)
    if editar_id:
        editando = DespesaDAO.buscar_por_id(editar_id)
        if editando:
            ano, mes = editando.data.year, editando.data.month
    return _pagina(ano, mes, hoje=hoje, editando=editando)


@planilha_bp.route('/admin/planilha/despesas', methods=['POST'])
@limiter.limit(LIMITE_ESCRITA, key_func=chave_da_conta)
@admin_requerido
def lancar_despesa():
    hoje = date.today()
    dados, erros, valores = _ler_despesa(request.form, hoje)
    if erros:
        ano, mes = _ano_e_mes(request.form, hoje)
        return _pagina(ano, mes, hoje=hoje, form=dados, erros=erros, status=400)

    despesa = Despesa(**valores, lancado_por=session.get('usuario'))
    DespesaDAO.salvar(despesa)
    flash(f'Despesa de {MESES_PT[despesa.data.month].lower()} lançada.', 'sucesso')
    return _voltar_para(despesa)


@planilha_bp.route('/admin/planilha/despesas/<int:despesa_id>', methods=['POST'])
@limiter.limit(LIMITE_ESCRITA, key_func=chave_da_conta)
@admin_requerido
def alterar_despesa(despesa_id):
    despesa = DespesaDAO.buscar_por_id(despesa_id) or abort(404)
    hoje = date.today()
    dados, erros, valores = _ler_despesa(request.form, hoje)
    if erros:
        return _pagina(despesa.data.year, despesa.data.month, hoje=hoje,
                       editando=despesa, form=dados, erros=erros, status=400)

    for campo, valor in valores.items():
        setattr(despesa, campo, valor)
    despesa.lancado_por = session.get('usuario')
    DespesaDAO.salvar(despesa)
    flash('Despesa alterada.', 'sucesso')
    return _voltar_para(despesa)


@planilha_bp.route('/admin/planilha/despesas/<int:despesa_id>/excluir', methods=['POST'])
@limiter.limit(LIMITE_ESCRITA, key_func=chave_da_conta)
@admin_requerido
def excluir_despesa(despesa_id):
    despesa = DespesaDAO.buscar_por_id(despesa_id) or abort(404)
    data = despesa.data
    DespesaDAO.excluir(despesa)
    flash('Despesa excluída.', 'sucesso')
    return _voltar_para(data)


@planilha_bp.route('/admin/planilha/<int:ano>.xlsx')
@limiter.limit('30 per hour', key_func=chave_da_conta)
@admin_requerido
def baixar_excel(ano):
    hoje = date.today()
    if not _ano_valido(ano, hoje):
        abort(404)
    return Response(
        planilha_excel.gerar(ano, hoje=hoje),
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': f'attachment; filename="planilha-economica-{ano}.xlsx"',
            'Cache-Control': 'private, no-store',
        },
    )
