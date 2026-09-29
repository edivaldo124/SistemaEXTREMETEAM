"""Plano fora de venda (arquivar/reativar/excluir), edição e promoção com período.

Regras centrais:
* plano com histórico (mensalidade, aluno ou pedido de troca) não é apagado - é arquivado;
* plano arquivado some da home, do perfil e dos formulários, e não recebe cobrança nova;
  quem está nele termina o período pago e escolhe outro;
* durante a promoção, toda cobrança NOVA sai pelo preço promocional; as já emitidas não mudam.
"""
from datetime import date, timedelta
from decimal import Decimal

import pytest

from config import db
from dao.financeiroDAO import (
    ACAO_AGENDAR_MUDANCA,
    ACAO_CONTRATAR,
    ACAO_RENOVAR,
    CONTRATACAO_COBRANCA_CRIADA,
    CONTRATACAO_MUDANCA_AGENDADA,
    CONTRATACAO_PLANO_INDISPONIVEL,
    PagamentoDAO,
    SolicitacaoPlanoDAO,
)
from dao.planoDAO import PlanoDAO
from modelos.pagamento import Pagamento
from modelos.plano import Plano
from modelos.solicitacao_plano import STATUS_CANCELADA
from servicos import planos as regras_plano
from servicos.planos import vitrine_planos

HOJE = date.today()


def _plano(nome, preco, dias=30):
    plano = Plano(nome_plano=nome, preco_plano=preco, duracao_dias=dias)
    PlanoDAO.salvar(plano)
    return plano


def _pagar(aluno, plano, *, inicio=None):
    inicio = inicio or HOJE
    pagamento = Pagamento(
        aluno_id=aluno.id, plano_id=plano.id, valor=Decimal(str(plano.preco_plano)),
        vencimento=inicio, status='pago', data_pagamento=inicio,
        competencia=inicio.strftime('%Y-%m'), vigencia_inicio=inicio,
        vigencia_fim=inicio + timedelta(days=plano.duracao_dias - 1),
    )
    db.session.add(pagamento)
    aluno.plano_id = plano.id
    db.session.commit()
    PagamentoDAO.sincronizar_situacao_do_aluno(aluno)
    return pagamento


def _promocao(plano, preco, inicio=None, fim=None):
    plano.preco_promocional = Decimal(preco)
    plano.promocao_inicio = inicio or HOJE - timedelta(days=1)
    plano.promocao_fim = fim or HOJE + timedelta(days=10)
    db.session.commit()
    return plano


# --------------------------------------------------------------------------
# Excluir x arquivar
# --------------------------------------------------------------------------

def test_plano_nunca_usado_e_excluido(client, contexto_app, logar_como_admin):
    plano = _plano('Teste', '10.00')
    logar_como_admin()

    resposta = client.post(f'/admin/remover_plano/{plano.id}', follow_redirects=True)

    assert 'Plano excluído.' in resposta.get_data(as_text=True)
    assert PlanoDAO.buscar_por_id(plano.id) is None


def test_plano_com_mensalidade_vencida_nao_e_excluido(client, contexto_app, plano, criar_pagamento,
                                                      logar_como_admin):
    criar_pagamento(status='atrasado', vencimento=HOJE - timedelta(days=20))
    logar_como_admin()

    resposta = client.post(f'/admin/remover_plano/{plano.id}', follow_redirects=True)

    assert 'Use &#34;Arquivar&#34;' in resposta.get_data(as_text=True)
    assert PlanoDAO.buscar_por_id(plano.id) is not None


def test_plano_so_no_cadastro_do_aluno_tambem_conta_como_em_uso(contexto_app, plano, criar_aluno):
    criar_aluno(plano_id=plano.id)
    assert PlanoDAO.em_uso(plano.id)
    assert PlanoDAO.remover(plano.id) is False


def test_painel_so_oferece_excluir_para_plano_sem_historico(client, contexto_app, plano, criar_pagamento,
                                                            logar_como_admin):
    criar_pagamento()
    livre = _plano('Livre', '50.00')
    logar_como_admin()

    html = client.get('/admin').get_data(as_text=True)

    assert f'/admin/remover_plano/{livre.id}' in html
    assert f'/admin/remover_plano/{plano.id}' not in html
    assert f'/admin/planos/{plano.id}/arquivar' in html


def test_arquivar_tira_de_venda_e_preserva_o_historico(client, contexto_app, plano, criar_pagamento,
                                                       logar_como_admin):
    pagamento = criar_pagamento(status='pago', data_pagamento=HOJE)
    plano.destaque = True
    db.session.commit()
    logar_como_admin()

    resposta = client.post(f'/admin/planos/{plano.id}/arquivar', follow_redirects=True)

    html = resposta.get_data(as_text=True)
    assert 'Mensal foi arquivado' in html
    assert 'Planos arquivados (1)' in html
    arquivado = PlanoDAO.buscar_por_id(plano.id)
    assert arquivado.arquivado is True and arquivado.destaque is False
    assert db.session.get(Pagamento, pagamento.id).plano_id == plano.id
    assert PlanoDAO.listar_ativos() == []
    assert 'Mensal' not in client.get('/').get_data(as_text=True)


def test_reativar_volta_a_oferecer(client, contexto_app, plano, logar_como_admin):
    PlanoDAO.arquivar(plano.id, ator='admin')
    logar_como_admin()

    client.post(f'/admin/planos/{plano.id}/reativar')

    assert PlanoDAO.buscar_por_id(plano.id).arquivado is False
    assert [p.id for p in PlanoDAO.listar_ativos()] == [plano.id]


def test_arquivar_exige_admin(client, contexto_app, plano, criar_aluno, logar_como_aluno):
    logar_como_aluno(criar_aluno())
    client.post(f'/admin/planos/{plano.id}/arquivar')
    assert PlanoDAO.buscar_por_id(plano.id).arquivado is False


def test_plano_arquivado_nao_pode_ser_destacado(contexto_app, plano):
    PlanoDAO.arquivar(plano.id, ator='admin')
    assert PlanoDAO.definir_destaque(plano.id) is None
    assert PlanoDAO.buscar_por_id(plano.id).destaque is False


# --------------------------------------------------------------------------
# Aluno no plano arquivado: termina o período e escolhe outro
# --------------------------------------------------------------------------

def test_periodo_pago_continua_valendo_depois_de_arquivar(contexto_app, plano, criar_aluno):
    aluno = criar_aluno()
    _pagar(aluno, plano)
    PlanoDAO.arquivar(plano.id, ator='admin')

    situacao = regras_plano.situacao_plano(aluno, PagamentoDAO.listar_por_aluno(aluno.id))

    assert situacao.ativo and situacao.plano.id == plano.id


def test_plano_arquivado_nao_gera_cobranca_nova(contexto_app, plano, criar_aluno):
    aluno = criar_aluno()
    PlanoDAO.arquivar(plano.id, ator='admin')

    resultado = PagamentoDAO.contratar_plano(aluno=aluno, plano=plano, acao=ACAO_CONTRATAR)

    assert resultado.codigo == CONTRATACAO_PLANO_INDISPONIVEL
    assert Pagamento.query.filter_by(aluno_id=aluno.id).count() == 0


def test_renovar_plano_arquivado_e_recusado(contexto_app, plano, criar_aluno):
    aluno = criar_aluno()
    _pagar(aluno, plano)
    PlanoDAO.arquivar(plano.id, ator='admin')

    resultado = PagamentoDAO.contratar_plano(aluno=aluno, plano=plano, acao=ACAO_RENOVAR)

    assert resultado.codigo == CONTRATACAO_PLANO_INDISPONIVEL
    assert Pagamento.query.filter_by(aluno_id=aluno.id).count() == 1


def test_quem_esta_no_arquivado_agenda_troca_para_um_ativo(contexto_app, plano, criar_aluno):
    aluno = criar_aluno()
    _pagar(aluno, plano)
    PlanoDAO.arquivar(plano.id, ator='admin')
    outro = _plano('Trimestral', '400.00', 90)

    resultado = PagamentoDAO.contratar_plano(aluno=aluno, plano=outro, acao=ACAO_AGENDAR_MUDANCA)

    assert resultado.codigo == CONTRATACAO_MUDANCA_AGENDADA
    assert PagamentoDAO.contratar_plano(aluno=aluno, plano=outro, acao=ACAO_RENOVAR).pagamento.plano_id == outro.id


def test_troca_agendada_para_o_plano_arquivado_e_cancelada(contexto_app, plano, criar_aluno):
    aluno = criar_aluno()
    _pagar(aluno, plano)
    destino = _plano('Basico', '90.00')
    PagamentoDAO.contratar_plano(aluno=aluno, plano=destino, acao=ACAO_AGENDAR_MUDANCA)

    _, cancelados = PlanoDAO.arquivar(destino.id, ator='admin')

    assert cancelados == 1
    assert SolicitacaoPlanoDAO.pendente_do_aluno(aluno.id) is None
    assert SolicitacaoPlanoDAO.listar_do_aluno(aluno.id)[0].status == STATUS_CANCELADA


def test_perfil_nao_oferece_plano_arquivado_e_avisa_quem_esta_nele(client, contexto_app, plano, criar_aluno,
                                                                   logar_como_aluno):
    aluno = criar_aluno()
    _pagar(aluno, plano)
    PlanoDAO.arquivar(plano.id, ator='admin')
    _plano('Trimestral', '400.00', 90)
    logar_como_aluno(aluno)

    html = client.get('/perfil').get_data(as_text=True)

    assert 'saiu de venda e não pode ser renovado' in html
    assert 'Substitui o Mensal, que saiu de venda.' in html
    assert f'data-plano-id="{plano.id}"' not in html
    assert 'Trimestral' in html


def test_formulario_do_perfil_recusa_plano_arquivado(client, contexto_app, plano, criar_aluno, logar_como_aluno):
    aluno = criar_aluno()
    PlanoDAO.arquivar(plano.id, ator='admin')
    logar_como_aluno(aluno)

    resposta = client.post('/perfil', data={'plano': plano.id, 'acao': 'contratar'}, follow_redirects=True)

    assert 'Plano inválido ou indisponível.' in resposta.get_data(as_text=True)
    assert Pagamento.query.filter_by(aluno_id=aluno.id).count() == 0


def test_ficha_do_aluno_mantem_o_plano_arquivado_do_cadastro(client, contexto_app, plano, criar_aluno,
                                                             logar_como_admin):
    aluno = criar_aluno(plano_id=plano.id)
    PlanoDAO.arquivar(plano.id, ator='admin')
    logar_como_admin()

    html = client.get(f'/admin/usuario/{aluno.cpf}').get_data(as_text=True)

    assert f'<option value="{plano.id}" selected>Mensal (arquivado)</option>' in html


def test_admin_nao_lanca_mensalidade_nova_em_plano_arquivado(client, contexto_app, plano, criar_aluno,
                                                             logar_como_admin):
    aluno = criar_aluno()
    PlanoDAO.arquivar(plano.id, ator='admin')
    logar_como_admin()

    resposta = client.post(f'/admin/usuario/{aluno.cpf}/pagamentos', data={
        'plano_id': plano.id, 'valor': '150.00', 'vencimento': HOJE.isoformat(),
        'status': 'pendente', 'forma_pagamento': 'pix',
    }, follow_redirects=True)

    assert 'está arquivado e não recebe mensalidades novas' in resposta.get_data(as_text=True)
    assert Pagamento.query.filter_by(aluno_id=aluno.id).count() == 0


# --------------------------------------------------------------------------
# Edição e promoção
# --------------------------------------------------------------------------

def test_admin_edita_nome_preco_e_duracao(client, contexto_app, plano, logar_como_admin):
    logar_como_admin()

    client.post(f'/admin/planos/{plano.id}/editar', data={
        'nome_plano': 'Mensal Plus', 'preco_plano': '1.234,50', 'duracao_dias': '31',
    })

    editado = PlanoDAO.buscar_por_id(plano.id)
    assert (editado.nome_plano, editado.preco_plano, editado.duracao_dias) == ('Mensal Plus', Decimal('1234.50'), 31)
    assert not editado.tem_promocao


def test_editar_preco_nao_muda_mensalidade_ja_lancada(client, contexto_app, plano, criar_pagamento,
                                                      logar_como_admin):
    pagamento = criar_pagamento()
    logar_como_admin()

    client.post(f'/admin/planos/{plano.id}/editar', data={
        'nome_plano': 'Mensal', 'preco_plano': '200,00', 'duracao_dias': '30',
    })

    assert db.session.get(Pagamento, pagamento.id).valor == Decimal('150.00')


def test_admin_cria_promocao(client, contexto_app, plano, logar_como_admin):
    logar_como_admin()
    fim = HOJE + timedelta(days=15)

    client.post(f'/admin/planos/{plano.id}/editar', data={
        'nome_plano': 'Mensal', 'preco_plano': '150,00', 'duracao_dias': '30',
        'preco_promocional': '120,00', 'promocao_inicio': HOJE.isoformat(), 'promocao_fim': fim.isoformat(),
    })

    editado = PlanoDAO.buscar_por_id(plano.id)
    assert editado.promocao_ativa() and editado.preco_atual == Decimal('120.00')
    assert editado.promocao_fim == fim


@pytest.mark.parametrize('promocao, erro', [
    ({'preco_promocional': '160,00'}, 'menor que o preço normal'),
    ({'preco_promocional': '120,00', 'promocao_inicio': '', 'promocao_fim': ''}, 'informe o preço promocional e as datas'),
    ({'promocao_inicio': (HOJE + timedelta(days=5)).isoformat(), 'promocao_fim': HOJE.isoformat()},
     'terminar depois de começar'),
    ({'promocao_inicio': (HOJE - timedelta(days=9)).isoformat(),
      'promocao_fim': (HOJE - timedelta(days=1)).isoformat()}, 'já terminou'),
])
def test_promocao_invalida_e_recusada(client, contexto_app, plano, logar_como_admin, promocao, erro):
    logar_como_admin()
    dados = {
        'nome_plano': 'Mensal', 'preco_plano': '150,00', 'duracao_dias': '30',
        'preco_promocional': '120,00', 'promocao_inicio': HOJE.isoformat(),
        'promocao_fim': (HOJE + timedelta(days=5)).isoformat(),
    }
    dados.update(promocao)

    resposta = client.post(f'/admin/planos/{plano.id}/editar', data=dados)

    assert resposta.status_code == 400
    assert erro in resposta.get_data(as_text=True)
    assert not PlanoDAO.buscar_por_id(plano.id).tem_promocao


def test_apagar_os_campos_tira_a_promocao(client, contexto_app, plano, logar_como_admin):
    _promocao(plano, '120.00')
    logar_como_admin()

    client.post(f'/admin/planos/{plano.id}/editar', data={
        'nome_plano': 'Mensal', 'preco_plano': '150,00', 'duracao_dias': '30',
        'preco_promocional': '', 'promocao_inicio': '', 'promocao_fim': '',
    })

    assert not PlanoDAO.buscar_por_id(plano.id).tem_promocao


def test_promocao_encerrada_nao_volta_preenchida(client, contexto_app, plano, logar_como_admin):
    _promocao(plano, '120.00', inicio=HOJE - timedelta(days=30), fim=HOJE - timedelta(days=1))
    logar_como_admin()

    html = client.get(f'/admin/planos/{plano.id}/editar').get_data(as_text=True)

    assert 'já terminou' in html
    assert 'value="120,00"' not in html


def test_preco_promocional_so_vale_dentro_do_periodo(contexto_app, plano):
    _promocao(plano, '120.00', inicio=HOJE + timedelta(days=2), fim=HOJE + timedelta(days=4))

    assert regras_plano.preco(plano, HOJE) == Decimal('150.00')
    assert regras_plano.preco(plano, HOJE + timedelta(days=2)) == Decimal('120.00')
    assert regras_plano.preco(plano, HOJE + timedelta(days=4)) == Decimal('120.00')
    assert regras_plano.preco(plano, HOJE + timedelta(days=5)) == Decimal('150.00')
    assert plano.promocao_agendada(HOJE)


def test_cobranca_criada_na_promocao_sai_pelo_preco_promocional(contexto_app, plano, criar_aluno):
    _promocao(plano, '120.00')
    aluno = criar_aluno()

    resultado = PagamentoDAO.contratar_plano(aluno=aluno, plano=plano, acao=ACAO_CONTRATAR)

    assert resultado.codigo == CONTRATACAO_COBRANCA_CRIADA
    assert resultado.pagamento.valor == Decimal('120.00')


def test_fim_da_promocao_nao_muda_cobranca_ja_emitida(contexto_app, plano, criar_aluno):
    _promocao(plano, '120.00')
    aluno = criar_aluno()
    pagamento = PagamentoDAO.contratar_plano(aluno=aluno, plano=plano, acao=ACAO_CONTRATAR).pagamento

    plano.promocao_fim = HOJE - timedelta(days=1)
    plano.promocao_inicio = HOJE - timedelta(days=5)
    db.session.commit()

    assert db.session.get(Pagamento, pagamento.id).valor == Decimal('120.00')
    assert plano.preco_atual == Decimal('150.00')


def test_home_mostra_o_de_por_da_promocao(client, contexto_app, plano):
    _promocao(plano, '120.00', fim=HOJE + timedelta(days=10))

    html = client.get('/').get_data(as_text=True)

    assert 'Promoção até ' + (HOJE + timedelta(days=10)).strftime('%d/%m') in html
    assert 'class="et-plano-de"' in html
    assert 'R$\xa0120,00' in html or 'R$ 120,00' in html


def test_vitrine_mostra_plano_curto_pelo_proprio_periodo(contexto_app):
    semanal = _plano('Semanal', '7.00', 7)
    diaria = _plano('Diaria', '0.50', 1)
    mensal = _plano('Mensal', '120.00', 30)

    itens = {item['nome']: item for item in vitrine_planos([semanal, diaria, mensal], '/cadastrar')}

    assert itens['Semanal']['unidade'] == 'por 7 dias' and itens['Semanal']['preco_mes'] == Decimal('7.00')
    assert itens['Diaria']['unidade'] == 'por dia'
    assert itens['Semanal']['economia'] is None
    # Sem destaque marcado, a recomendação padrão ignora a diária "barata".
    assert itens['Mensal']['recomendado'] and not itens['Diaria']['recomendado']
