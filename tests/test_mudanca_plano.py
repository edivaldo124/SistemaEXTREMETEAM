"""Mudança para um plano mais barato agendada para a próxima renovação.

Regra central: a solicitação não cobra, não reembolsa e não tira benefício nenhum antes
da hora - e, sozinha, também não libera um novo período sem o pagamento correspondente.
"""
from datetime import date, timedelta
from decimal import Decimal

import pytest

from config import db
from dao.financeiroDAO import (
    ACAO_AGENDAR_MUDANCA,
    ACAO_RENOVAR,
    CONTRATACAO_MESMO_PLANO,
    CONTRATACAO_MUDANCA_AGENDADA,
    CONTRATACAO_MUDANCA_CONFLITANTE,
    CONTRATACAO_MUDANCA_JA_EXISTE,
    CONTRATACAO_MUDANCA_SEM_VIGENCIA,
    PagamentoDAO,
    SolicitacaoPlanoDAO,
)
from modelos.pagamento import Pagamento
from modelos.plano import Plano
from modelos.solicitacao_plano import STATUS_CANCELADA, STATUS_EFETIVADA, STATUS_PENDENTE
from servicos import planos as regras_plano


@pytest.fixture
def plano_barato(contexto_app):
    plano = Plano(nome_plano='Basico', preco_plano=90.0, duracao_dias=30)
    db.session.add(plano)
    db.session.commit()
    return plano


def _pagar(aluno, plano, *, inicio=None, status='pago'):
    inicio = inicio or date.today()
    fim = inicio + timedelta(days=plano.duracao_dias - 1)
    pagamento = Pagamento(
        aluno_id=aluno.id, plano_id=plano.id, valor=Decimal(str(plano.preco_plano)),
        vencimento=inicio, status=status,
        data_pagamento=inicio if status == 'pago' else None,
        competencia=inicio.strftime('%Y-%m'), vigencia_inicio=inicio, vigencia_fim=fim,
    )
    db.session.add(pagamento)
    aluno.plano_id = plano.id
    db.session.commit()
    PagamentoDAO.sincronizar_situacao_do_aluno(aluno)
    return pagamento


def _agendar(aluno, plano_destino):
    return PagamentoDAO.contratar_plano(aluno=aluno, plano=plano_destino, acao=ACAO_AGENDAR_MUDANCA)


# --------------------------------------------------------------------------
# Solicitar
# --------------------------------------------------------------------------

def test_downgrade_nao_cobra_nem_altera_o_periodo_pago(
    contexto_app, plano, plano_barato, criar_aluno,
):
    aluno = criar_aluno()
    pago = _pagar(aluno, plano)

    resultado = _agendar(aluno, plano_barato)

    assert resultado.codigo == CONTRATACAO_MUDANCA_AGENDADA
    assert resultado.solicitacao.tipo == 'downgrade'
    assert resultado.solicitacao.vigencia_a_partir_de == pago.vigencia_fim + timedelta(days=1)
    # Nenhuma cobrança nova, nenhum reembolso, plano e validade intactos.
    assert len(PagamentoDAO.listar_por_aluno(aluno.id)) == 1
    situacao = regras_plano.situacao_plano(aluno, PagamentoDAO.listar_por_aluno(aluno.id))
    assert situacao.ativo
    assert situacao.plano.id == plano.id
    assert situacao.valido_ate == pago.vigencia_fim


def test_solicitacao_sozinha_nao_libera_novo_periodo(
    contexto_app, plano, plano_barato, criar_aluno,
):
    aluno = criar_aluno()
    pago = _pagar(aluno, plano)
    _agendar(aluno, plano_barato)

    pagamentos = PagamentoDAO.listar_por_aluno(aluno.id)
    situacao = regras_plano.situacao_plano(aluno, pagamentos)

    assert regras_plano.fim_periodo_comprometido(pagamentos) == pago.vigencia_fim
    assert situacao.valido_ate == pago.vigencia_fim  # não estendeu nada


def test_perfil_mostra_destino_valor_e_data_da_mudanca(
    client, plano, plano_barato, criar_aluno, logar_como_aluno,
):
    aluno = criar_aluno()
    pago = _pagar(aluno, plano)
    logar_como_aluno(aluno)

    client.post('/perfil', data={'plano': str(plano_barato.id), 'acao': 'agendar_mudanca'})
    corpo = client.get('/perfil').get_data(as_text=True)

    assert 'Mudança de plano agendada' in corpo
    assert plano_barato.nome_plano in corpo
    assert '90,00' in corpo
    assert (pago.vigencia_fim + timedelta(days=1)).strftime('%d/%m/%Y') in corpo
    assert 'Cancelar mudança' in corpo


def test_mudanca_para_o_plano_atual_e_recusada(contexto_app, plano, criar_aluno):
    aluno = criar_aluno()
    _pagar(aluno, plano)

    resultado = _agendar(aluno, plano)

    assert resultado.codigo == CONTRATACAO_MESMO_PLANO
    assert SolicitacaoPlanoDAO.pendente_do_aluno(aluno.id) is None


def test_mudanca_sem_periodo_pago_e_recusada(contexto_app, plano_barato, criar_aluno):
    aluno = criar_aluno()

    resultado = _agendar(aluno, plano_barato)

    assert resultado.codigo == CONTRATACAO_MUDANCA_SEM_VIGENCIA
    assert SolicitacaoPlanoDAO.pendente_do_aluno(aluno.id) is None


def test_solicitacao_duplicada_para_o_mesmo_plano_nao_cria_outra(
    contexto_app, plano, plano_barato, criar_aluno,
):
    aluno = criar_aluno()
    _pagar(aluno, plano)

    primeira = _agendar(aluno, plano_barato)
    segunda = _agendar(aluno, plano_barato)

    assert segunda.codigo == CONTRATACAO_MUDANCA_JA_EXISTE
    assert segunda.solicitacao.id == primeira.solicitacao.id
    assert len(SolicitacaoPlanoDAO.listar_do_aluno(aluno.id)) == 1


def test_segunda_solicitacao_para_outro_plano_e_conflitante(
    contexto_app, plano, plano_barato, criar_aluno,
):
    aluno = criar_aluno()
    _pagar(aluno, plano)
    _agendar(aluno, plano_barato)
    outro = Plano(nome_plano='Intermediario', preco_plano=120.0, duracao_dias=30)
    db.session.add(outro)
    db.session.commit()

    resultado = _agendar(aluno, outro)

    assert resultado.codigo == CONTRATACAO_MUDANCA_CONFLITANTE
    assert len(SolicitacaoPlanoDAO.listar_do_aluno(aluno.id)) == 1


def test_mudanca_com_pagamento_em_analise_espera_a_decisao(
    contexto_app, plano, plano_barato, criar_aluno,
):
    aluno = criar_aluno()
    _pagar(aluno, plano, status='em_analise')

    resultado = _agendar(aluno, plano_barato)

    # Existe uma decisão em curso: nada é agendado nem cobrado por cima dela.
    assert resultado.codigo == 'aguardando_decisao'
    assert SolicitacaoPlanoDAO.pendente_do_aluno(aluno.id) is None


def test_renovacao_ja_paga_empurra_a_mudanca_para_depois_dela(
    contexto_app, plano, plano_barato, criar_aluno,
):
    aluno = criar_aluno()
    atual = _pagar(aluno, plano)
    seguinte = _pagar(aluno, plano, inicio=atual.vigencia_fim + timedelta(days=1))

    resultado = _agendar(aluno, plano_barato)

    # O período seguinte já foi pago no plano antigo: a troca só vale depois dele.
    assert resultado.solicitacao.vigencia_a_partir_de == seguinte.vigencia_fim + timedelta(days=1)


# --------------------------------------------------------------------------
# Cancelar
# --------------------------------------------------------------------------

def test_aluno_cancela_a_solicitacao_antes_da_efetivacao(
    client, plano, plano_barato, criar_aluno, logar_como_aluno,
):
    aluno = criar_aluno()
    _pagar(aluno, plano)
    solicitacao = _agendar(aluno, plano_barato).solicitacao
    logar_como_aluno(aluno)

    resposta = client.post(f'/perfil/plano/mudanca/{solicitacao.id}/cancelar')

    assert resposta.status_code == 302
    assert solicitacao.status == STATUS_CANCELADA
    assert SolicitacaoPlanoDAO.pendente_do_aluno(aluno.id) is None


def test_aluno_nao_cancela_solicitacao_de_outro(
    client, plano, plano_barato, criar_aluno, logar_como_aluno,
):
    dono = criar_aluno()
    _pagar(dono, plano)
    solicitacao = _agendar(dono, plano_barato).solicitacao
    logar_como_aluno(criar_aluno())

    resposta = client.post(f'/perfil/plano/mudanca/{solicitacao.id}/cancelar')

    assert resposta.status_code == 404
    assert solicitacao.status == STATUS_PENDENTE


def test_solicitacao_ja_cancelada_nao_cancela_de_novo(
    contexto_app, plano, plano_barato, criar_aluno,
):
    aluno = criar_aluno()
    _pagar(aluno, plano)
    solicitacao = _agendar(aluno, plano_barato).solicitacao

    assert SolicitacaoPlanoDAO.cancelar(solicitacao, ator='aluno') is True
    assert SolicitacaoPlanoDAO.cancelar(solicitacao, ator='aluno') is False


def test_admin_cancela_a_solicitacao(
    client, plano, plano_barato, criar_aluno, logar_como_admin,
):
    aluno = criar_aluno()
    _pagar(aluno, plano)
    solicitacao = _agendar(aluno, plano_barato).solicitacao
    logar_como_admin()

    resposta = client.post(
        f'/admin/aluno/{aluno.id}/mudanca-plano/{solicitacao.id}/cancelar',
        data={'observacao': 'a pedido do aluno no balcão'},
    )

    assert resposta.status_code == 302
    assert solicitacao.status == STATUS_CANCELADA
    assert solicitacao.observacao == 'a pedido do aluno no balcão'


# --------------------------------------------------------------------------
# Efetivar
# --------------------------------------------------------------------------

def test_proxima_cobranca_nasce_no_plano_de_destino(
    contexto_app, plano, plano_barato, criar_aluno,
):
    aluno = criar_aluno()
    pago = _pagar(aluno, plano)
    solicitacao = _agendar(aluno, plano_barato).solicitacao

    resultado = PagamentoDAO.contratar_plano(aluno=aluno, plano=plano, acao=ACAO_RENOVAR)

    assert resultado.pagamento.plano_id == plano_barato.id
    assert resultado.pagamento.valor == Decimal('90.00')
    assert resultado.pagamento.vigencia_inicio == pago.vigencia_fim + timedelta(days=1)
    assert solicitacao.status == STATUS_EFETIVADA
    assert solicitacao.pagamento_efetivacao_id == resultado.pagamento.id


def test_historico_de_planos_e_valores_e_preservado(
    contexto_app, plano, plano_barato, criar_aluno,
):
    aluno = criar_aluno()
    pago = _pagar(aluno, plano)
    _agendar(aluno, plano_barato)
    PagamentoDAO.contratar_plano(aluno=aluno, plano=plano, acao=ACAO_RENOVAR)

    pagamentos = PagamentoDAO.listar_por_aluno(aluno.id)
    antigo = next(p for p in pagamentos if p.id == pago.id)

    # A mensalidade antiga continua com o plano e o valor originais.
    assert antigo.plano_id == plano.id
    assert antigo.valor == Decimal('150.00')
    assert antigo.status == 'pago'
    solicitacao = SolicitacaoPlanoDAO.listar_do_aluno(aluno.id)[0]
    assert solicitacao.valor_origem == Decimal('150.00')
    assert solicitacao.valor_destino == Decimal('90.00')


def test_mudanca_vale_por_decurso_de_prazo_quando_o_plano_vence(
    contexto_app, plano, plano_barato, criar_aluno,
):
    aluno = criar_aluno()
    inicio = date.today() - timedelta(days=40)
    _pagar(aluno, plano, inicio=inicio)
    solicitacao = PagamentoDAO.contratar_plano(
        aluno=aluno, plano=plano_barato, acao=ACAO_AGENDAR_MUDANCA,
        hoje=inicio + timedelta(days=5),
    ).solicitacao

    PagamentoDAO.efetivar_mudancas_por_prazo(aluno)

    assert solicitacao.status == STATUS_EFETIVADA
    assert aluno.plano_id == plano_barato.id
    # Efetivar não paga nada: o aluno segue sem período ativo até pagar.
    situacao = regras_plano.situacao_plano(aluno, PagamentoDAO.listar_por_aluno(aluno.id))
    assert not situacao.ativo


def test_mudanca_nao_vale_por_prazo_enquanto_houver_periodo_pago(
    contexto_app, plano, plano_barato, criar_aluno,
):
    aluno = criar_aluno()
    antigo = _pagar(aluno, plano, inicio=date.today() - timedelta(days=40))
    solicitacao = PagamentoDAO.contratar_plano(
        aluno=aluno, plano=plano_barato, acao=ACAO_AGENDAR_MUDANCA,
        hoje=antigo.vigencia_inicio + timedelta(days=1),
    ).solicitacao
    _pagar(aluno, plano)  # o aluno pagou outro período no plano antigo

    PagamentoDAO.efetivar_mudancas_por_prazo(aluno)

    assert solicitacao.status == STATUS_PENDENTE
    assert aluno.plano_id == plano.id


# --------------------------------------------------------------------------
# Situações limite
# --------------------------------------------------------------------------

def test_perfil_abre_com_solicitacao_pendente_e_sem_periodo_ativo(
    client, plano, plano_barato, criar_aluno, logar_como_aluno,
):
    """O admin pode estornar/cancelar a mensalidade que sustentava a vigência depois de
    o aluno agendar a troca. A tela precisa continuar abrindo e explicando a situação."""
    aluno = criar_aluno()
    pago = _pagar(aluno, plano)
    _agendar(aluno, plano_barato)

    pago.status = 'reembolsado'
    db.session.commit()
    PagamentoDAO.sincronizar_situacao_do_aluno(aluno)
    logar_como_aluno(aluno)

    resposta = client.get('/perfil')

    assert resposta.status_code == 200
    corpo = resposta.get_data(as_text=True)
    assert 'vale a partir da próxima contratação' in corpo
