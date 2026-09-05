"""Vigência do plano: o que decide "Plano ativo" é o período pago, não o cadastro.

Cobre o bug relatado (plano pago continuava pedindo pagamento) e os quatro estados que
a área do aluno precisa distinguir: pago e vigente, comprovante em análise, pagamento
recusado e período vencido.
"""
from datetime import date, timedelta
from decimal import Decimal

import pytest

from config import db
from dao.financeiroDAO import (
    ACAO_CONTRATAR,
    ACAO_RENOVAR,
    CONTRATACAO_AGUARDANDO_DECISAO,
    CONTRATACAO_COBRANCA_REUTILIZADA,
    CONTRATACAO_JA_ATIVO,
    CONTRATACAO_RENOVACAO_CRIADA,
    PagamentoDAO,
)
from modelos.pagamento import Pagamento
from modelos.plano import Plano
from servicos import planos as regras_plano


@pytest.fixture
def plano_barato(contexto_app):
    plano = Plano(nome_plano='Básico', preco_plano=90.0, duracao_dias=30)
    db.session.add(plano)
    db.session.commit()
    return plano


def _pagar(aluno, plano, *, inicio=None, dias=None):
    """Mensalidade paga cobrindo um período - o que de fato ativa o plano."""
    inicio = inicio or date.today()
    fim = inicio + timedelta(days=(dias or plano.duracao_dias) - 1)
    pagamento = Pagamento(
        aluno_id=aluno.id, plano_id=plano.id, valor=Decimal(str(plano.preco_plano)),
        vencimento=inicio, status='pago', data_pagamento=inicio,
        forma_pagamento='pix', competencia=inicio.strftime('%Y-%m'),
        vigencia_inicio=inicio, vigencia_fim=fim,
    )
    db.session.add(pagamento)
    aluno.plano_id = plano.id
    db.session.commit()
    PagamentoDAO.sincronizar_situacao_do_aluno(aluno)
    return pagamento


# --------------------------------------------------------------------------
# Pagamento confirmado
# --------------------------------------------------------------------------

def test_plano_pago_aparece_ativo_com_validade_e_sem_cobranca(
    client, plano, criar_aluno, logar_como_aluno,
):
    aluno = criar_aluno()
    pago = _pagar(aluno, plano)
    logar_como_aluno(aluno)

    corpo = client.get('/perfil').get_data(as_text=True)

    assert 'Plano ativo' in corpo
    assert pago.vigencia_fim.strftime('%d/%m/%Y') in corpo
    assert 'Nada a pagar neste período' in corpo
    # Nenhum caminho de pagamento é oferecido para um período já quitado.
    assert 'data-pix-pagar' not in corpo
    assert 'Escolher plano' not in corpo


def test_aluno_com_plano_pago_nao_gera_segunda_cobranca(
    contexto_app, plano, criar_aluno,
):
    aluno = criar_aluno()
    _pagar(aluno, plano)

    resultado = PagamentoDAO.contratar_plano(aluno=aluno, plano=plano, acao=ACAO_CONTRATAR)

    assert resultado.codigo == CONTRATACAO_JA_ATIVO
    assert resultado.pagamento is None
    assert len(PagamentoDAO.listar_por_aluno(aluno.id)) == 1


def test_post_de_contratacao_com_plano_pago_nao_cria_cobranca(
    client, plano, criar_aluno, logar_como_aluno,
):
    aluno = criar_aluno()
    _pagar(aluno, plano)
    logar_como_aluno(aluno)

    resposta = client.post('/perfil', data={'plano': str(plano.id)})

    assert resposta.status_code == 302
    assert 'pix=' not in resposta.headers['Location']
    assert len(PagamentoDAO.listar_por_aluno(aluno.id)) == 1


def test_webhook_aprovado_abre_vigencia_e_atualiza_validade_do_aluno(
    contexto_app, plano, criar_pagamento,
):
    pagamento = criar_pagamento()
    aluno = pagamento.aluno

    PagamentoDAO.marcar_pago_via_webhook(pagamento, data_pagamento=date.today())

    assert pagamento.vigencia_inicio is not None
    assert pagamento.vigencia_fim == pagamento.vigencia_inicio + timedelta(days=plano.duracao_dias - 1)
    assert aluno.mensalidade == 'Em Dia'
    assert aluno.data_vencimento == pagamento.vigencia_fim.strftime('%Y-%m-%d')


# --------------------------------------------------------------------------
# Cliques repetidos e requisições duplicadas
# --------------------------------------------------------------------------

def test_cliques_repetidos_em_escolher_plano_criam_uma_unica_cobranca(
    client, plano, criar_aluno, logar_como_aluno,
):
    aluno = criar_aluno()
    logar_como_aluno(aluno)

    primeira = client.post('/perfil', data={'plano': str(plano.id)})
    segunda = client.post('/perfil', data={'plano': str(plano.id)})
    terceira = client.post('/perfil', data={'plano': str(plano.id), 'acao': 'contratar'})

    assert len(PagamentoDAO.listar_por_aluno(aluno.id)) == 1
    assert primeira.headers['Location'] == segunda.headers['Location'] == terceira.headers['Location']


def test_renovacao_repetida_nao_cria_duas_cobrancas_do_proximo_periodo(
    contexto_app, plano, criar_aluno,
):
    aluno = criar_aluno()
    _pagar(aluno, plano)

    primeira = PagamentoDAO.contratar_plano(aluno=aluno, plano=plano, acao=ACAO_RENOVAR)
    segunda = PagamentoDAO.contratar_plano(aluno=aluno, plano=plano, acao=ACAO_RENOVAR)

    assert primeira.codigo == CONTRATACAO_RENOVACAO_CRIADA
    assert segunda.codigo == CONTRATACAO_COBRANCA_REUTILIZADA
    assert segunda.pagamento.id == primeira.pagamento.id
    assert len(PagamentoDAO.listar_por_aluno(aluno.id)) == 2  # a paga + a do próximo período


# --------------------------------------------------------------------------
# Comprovante em análise
# --------------------------------------------------------------------------

def test_comprovante_em_analise_nao_permite_abrir_outra_cobranca(
    contexto_app, plano, criar_pagamento,
):
    pagamento = criar_pagamento(status='em_analise')
    aluno = pagamento.aluno

    resultado = PagamentoDAO.contratar_plano(aluno=aluno, plano=plano, acao=ACAO_CONTRATAR)

    assert resultado.codigo == CONTRATACAO_AGUARDANDO_DECISAO
    assert resultado.pagamento.id == pagamento.id
    assert len(PagamentoDAO.listar_por_aluno(aluno.id)) == 1


def test_perfil_com_comprovante_em_analise_nao_incentiva_novo_pagamento(
    client, plano, criar_pagamento, logar_como_aluno, plano_barato,
):
    pagamento = criar_pagamento(status='em_analise')
    logar_como_aluno(pagamento.aluno)

    corpo = client.get('/perfil').get_data(as_text=True)

    assert 'Aguardando análise' in corpo
    assert 'Não é preciso pagar de novo' in corpo
    assert 'data-pix-pagar' not in corpo
    assert 'Escolher plano' not in corpo


def test_comprovante_em_analise_marca_situacao_do_aluno(contexto_app, criar_pagamento):
    pagamento = criar_pagamento()
    PagamentoDAO.enviar_comprovante_manual(pagamento, arquivo_nome='x.png', ator='aluno')

    assert pagamento.aluno.mensalidade == 'Em Análise'


# --------------------------------------------------------------------------
# Recusado e vencido
# --------------------------------------------------------------------------

def test_pagamento_recusado_permite_tentar_de_novo_sem_duplicar_cobranca(
    contexto_app, plano, criar_pagamento,
):
    pagamento = criar_pagamento(status='recusado')
    aluno = pagamento.aluno

    resultado = PagamentoDAO.contratar_plano(aluno=aluno, plano=plano, acao=ACAO_CONTRATAR)

    assert resultado.codigo == CONTRATACAO_COBRANCA_REUTILIZADA
    assert resultado.pagamento.id == pagamento.id
    assert len(PagamentoDAO.listar_por_aluno(aluno.id)) == 1


def test_periodo_vencido_deixa_de_ser_ativo_e_permite_nova_contratacao(
    client, plano, criar_aluno, logar_como_aluno,
):
    aluno = criar_aluno()
    inicio = date.today() - timedelta(days=60)
    _pagar(aluno, plano, inicio=inicio)
    logar_como_aluno(aluno)

    corpo = client.get('/perfil').get_data(as_text=True)
    assert 'Plano vencido' in corpo
    assert 'Escolher plano' in corpo

    client.post('/perfil', data={'plano': str(plano.id)})
    pagamentos = PagamentoDAO.listar_por_aluno(aluno.id)
    novo = next(p for p in pagamentos if p.status != 'pago')
    assert novo.vigencia_inicio == date.today()  # não encadeia num período já vencido


def test_cobranca_de_periodo_futuro_nao_e_marcada_como_vencida(contexto_app, plano, criar_aluno):
    aluno = criar_aluno()
    _pagar(aluno, plano)

    resultado = PagamentoDAO.contratar_plano(aluno=aluno, plano=plano, acao=ACAO_RENOVAR)
    PagamentoDAO.listar_por_aluno(aluno.id)  # dispara a promoção pendente -> atrasado

    assert resultado.pagamento.vencimento > date.today()
    assert resultado.pagamento.status == 'pendente'


# --------------------------------------------------------------------------
# Renovação antecipada
# --------------------------------------------------------------------------

def test_renovacao_antecipada_cobre_o_proximo_periodo_e_preserva_o_atual(
    contexto_app, plano, criar_aluno,
):
    aluno = criar_aluno()
    pago = _pagar(aluno, plano)

    resultado = PagamentoDAO.contratar_plano(aluno=aluno, plano=plano, acao=ACAO_RENOVAR)

    assert resultado.codigo == CONTRATACAO_RENOVACAO_CRIADA
    assert resultado.pagamento.vigencia_inicio == pago.vigencia_fim + timedelta(days=1)
    assert pago.status == 'pago' and pago.vigencia_fim == pago.vigencia_fim
    situacao = regras_plano.situacao_plano(aluno, PagamentoDAO.listar_por_aluno(aluno.id))
    assert situacao.ativo and situacao.renovacao_antecipada


def test_perfil_identifica_a_cobranca_como_do_proximo_periodo(
    client, plano, criar_aluno, logar_como_aluno,
):
    aluno = criar_aluno()
    _pagar(aluno, plano)
    logar_como_aluno(aluno)
    client.post('/perfil', data={'plano': str(plano.id), 'acao': 'renovar'})

    corpo = client.get('/perfil').get_data(as_text=True)

    assert 'Plano ativo' in corpo
    assert 'renovação antecipada' in corpo
    assert 'próximo período' in corpo


def test_acao_forjada_de_renovacao_sem_vigencia_apenas_contrata(
    contexto_app, plano, criar_aluno,
):
    aluno = criar_aluno()

    resultado = PagamentoDAO.contratar_plano(aluno=aluno, plano=plano, acao=ACAO_RENOVAR)

    assert resultado.pagamento.vigencia_inicio == date.today()
    assert len(PagamentoDAO.listar_por_aluno(aluno.id)) == 1


def test_acao_invalida_no_formulario_cai_no_fluxo_de_contratacao(
    client, plano, criar_aluno, logar_como_aluno,
):
    aluno = criar_aluno()
    _pagar(aluno, plano)
    logar_como_aluno(aluno)

    client.post('/perfil', data={'plano': str(plano.id), 'acao': 'qualquer-coisa'})

    assert len(PagamentoDAO.listar_por_aluno(aluno.id)) == 1


# --------------------------------------------------------------------------
# Renovação já paga: a validade soma os períodos encadeados
# --------------------------------------------------------------------------

def test_validade_soma_o_periodo_seguinte_ja_pago(contexto_app, plano, criar_aluno):
    aluno = criar_aluno()
    atual = _pagar(aluno, plano)
    seguinte = _pagar(aluno, plano, inicio=atual.vigencia_fim + timedelta(days=1))

    situacao = regras_plano.situacao_plano(aluno, PagamentoDAO.listar_por_aluno(aluno.id))

    assert situacao.ativo
    assert situacao.fim_periodo_atual == atual.vigencia_fim
    assert situacao.valido_ate == seguinte.vigencia_fim
    assert situacao.proximo_periodo_pago.id == seguinte.id
    assert aluno.data_vencimento == seguinte.vigencia_fim.strftime('%Y-%m-%d')


def test_periodo_seguinte_pago_nao_encadeia_se_houver_buraco(contexto_app, plano, criar_aluno):
    aluno = criar_aluno()
    atual = _pagar(aluno, plano)
    # Começa dois dias depois do fim: não é continuação, é outro período solto.
    _pagar(aluno, plano, inicio=atual.vigencia_fim + timedelta(days=2))

    situacao = regras_plano.situacao_plano(aluno, PagamentoDAO.listar_por_aluno(aluno.id))

    assert situacao.valido_ate == atual.vigencia_fim
    assert situacao.proximo_periodo_pago is None


# --------------------------------------------------------------------------
# Cobrança por e-mail
# --------------------------------------------------------------------------

def test_admin_nao_cobra_aluno_com_plano_ativo(
    client, plano, criar_aluno, logar_como_admin, monkeypatch,
):
    aluno = criar_aluno()
    _pagar(aluno, plano)
    logar_como_admin()

    enviados = []
    monkeypatch.setattr('blueprints.adm_bp.enviar_email', lambda *a, **k: enviados.append(a))

    resposta = client.post(f'/admin/usuario/{aluno.cpf}/cobrar', follow_redirects=True)

    assert resposta.status_code == 200
    assert enviados == []
    assert 'não tem pendência' in resposta.get_data(as_text=True)


def test_admin_nao_cobra_aluno_com_comprovante_em_analise(
    client, criar_pagamento, logar_como_admin, monkeypatch,
):
    pagamento = criar_pagamento(status='em_analise')
    logar_como_admin()

    enviados = []
    monkeypatch.setattr('blueprints.adm_bp.enviar_email', lambda *a, **k: enviados.append(a))
    client.post(f'/admin/usuario/{pagamento.aluno.cpf}/cobrar')

    assert enviados == []


def test_admin_cobra_aluno_com_mensalidade_vencida(
    client, plano, criar_pagamento, logar_como_admin, monkeypatch,
):
    pagamento = criar_pagamento(vencimento=date.today() - timedelta(days=3), status='atrasado')
    logar_como_admin()

    enviados = []
    monkeypatch.setattr('blueprints.adm_bp.enviar_email',
                        lambda *a, **k: enviados.append(a) or True)
    client.post(f'/admin/usuario/{pagamento.aluno.cpf}/cobrar')

    assert len(enviados) == 1
    corpo = ' '.join(enviados[0][4])
    assert 'R$ 150,00' in corpo
    assert pagamento.vencimento.strftime('%d/%m/%Y') in corpo


# --------------------------------------------------------------------------
# Pagamento confirmado depois do fim da janela original
# --------------------------------------------------------------------------

def test_cobranca_antiga_quitada_hoje_abre_o_periodo_a_partir_de_hoje(
    contexto_app, plano, criar_aluno,
):
    """Quem paga uma cobrança vencida há semanas tem de receber os 30 dias a partir da
    confirmação - senão pagaria por dias que já passaram e seguiria sem acesso."""
    aluno = criar_aluno()
    inicio_antigo = date.today() - timedelta(days=45)
    pagamento = Pagamento(
        aluno_id=aluno.id, plano_id=plano.id, valor=Decimal('150.00'),
        vencimento=inicio_antigo, status='atrasado',
        competencia=inicio_antigo.strftime('%Y-%m'),
        vigencia_inicio=inicio_antigo,
        vigencia_fim=inicio_antigo + timedelta(days=plano.duracao_dias - 1),
    )
    db.session.add(pagamento)
    db.session.commit()

    PagamentoDAO.marcar_pago_via_webhook(pagamento, data_pagamento=date.today())

    assert pagamento.vigencia_inicio == date.today()
    assert pagamento.vigencia_fim == date.today() + timedelta(days=plano.duracao_dias - 1)
    assert aluno.mensalidade == 'Em Dia'
    situacao = regras_plano.situacao_plano(aluno, PagamentoDAO.listar_por_aluno(aluno.id))
    assert situacao.ativo
    assert any(e.tipo == 'vigencia_ajustada' for e in pagamento.eventos)


def test_renovacao_antecipada_paga_hoje_mantem_a_janela_futura(contexto_app, plano, criar_aluno):
    aluno = criar_aluno()
    atual = _pagar(aluno, plano)
    renovacao = PagamentoDAO.contratar_plano(aluno=aluno, plano=plano, acao=ACAO_RENOVAR).pagamento
    inicio_planejado = renovacao.vigencia_inicio

    PagamentoDAO.marcar_pago_via_webhook(renovacao, data_pagamento=date.today())

    # A janela já estava no período certo: não pode ser puxada para hoje.
    assert renovacao.vigencia_inicio == inicio_planejado == atual.vigencia_fim + timedelta(days=1)


# --------------------------------------------------------------------------
# Lançamento manual do admin
# --------------------------------------------------------------------------

def test_recebimento_manual_encadeia_ao_periodo_ja_pago(
    client, plano, criar_aluno, logar_como_admin,
):
    aluno = criar_aluno()
    atual = _pagar(aluno, plano)
    logar_como_admin()

    client.post(f'/admin/usuario/{aluno.cpf}/pagamentos', data={
        'plano_id': str(plano.id), 'valor': '150.00',
        'vencimento': date.today().isoformat(), 'status': 'pago',
        'data_pagamento': date.today().isoformat(), 'forma_pagamento': 'dinheiro',
    })

    novo = [p for p in PagamentoDAO.listar_por_aluno(aluno.id) if p.id != atual.id][0]
    assert novo.vigencia_inicio == atual.vigencia_fim + timedelta(days=1)
    situacao = regras_plano.situacao_plano(aluno, PagamentoDAO.listar_por_aluno(aluno.id))
    assert situacao.valido_ate == novo.vigencia_fim  # somou 30 dias, não sobrepôs


def test_admin_continua_podendo_trocar_o_plano_do_cadastro(
    client, plano, plano_barato, criar_aluno, logar_como_admin,
):
    aluno = criar_aluno(plano_id=plano.id)
    _pagar(aluno, plano)
    logar_como_admin()

    client.post(f'/admin/usuario/{aluno.cpf}', data={
        'nome': aluno.nome, 'login': aluno.login, 'datanascimento': aluno.datanascimento,
        'email': aluno.email, 'telefone': aluno.telefone, 'descricao': '',
        'plano_id': str(plano_barato.id),
    })

    assert aluno.plano_id == plano_barato.id
    # O plano que vale continua saindo da mensalidade paga, não do cadastro.
    situacao = regras_plano.situacao_plano(aluno, PagamentoDAO.listar_por_aluno(aluno.id))
    assert situacao.plano.id == plano.id


def test_admin_pode_remover_o_plano_do_cadastro(client, plano, criar_aluno, logar_como_admin):
    aluno = criar_aluno(plano_id=plano.id)
    logar_como_admin()

    client.post(f'/admin/usuario/{aluno.cpf}', data={
        'nome': aluno.nome, 'login': aluno.login, 'datanascimento': aluno.datanascimento,
        'email': aluno.email, 'telefone': aluno.telefone, 'descricao': '',
        'plano_id': 'Nenhum',
    })

    assert aluno.plano_id is None


def test_plano_inexistente_no_cadastro_e_recusado(client, plano, criar_aluno, logar_como_admin):
    aluno = criar_aluno(plano_id=plano.id)
    logar_como_admin()

    resposta = client.post(f'/admin/usuario/{aluno.cpf}', data={
        'nome': aluno.nome, 'login': aluno.login, 'datanascimento': aluno.datanascimento,
        'email': aluno.email, 'telefone': aluno.telefone, 'descricao': '',
        'plano_id': '999999',
    }, follow_redirects=True)

    assert resposta.status_code == 200
    assert 'verifique o plano selecionado' in resposta.get_data(as_text=True)
    assert aluno.plano_id == plano.id  # nada foi gravado com FK pendurada
