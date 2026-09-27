"""Planos na página inicial: cálculo (servicos/planos.vitrine_planos), destaque escolhido
pelo admin e o que a rota "/" entrega."""

from decimal import Decimal

from dao.planoDAO import PlanoDAO
from modelos.plano import Plano
from servicos.planos import vitrine_planos


def _plano(nome, preco, dias, destaque=False):
    plano = Plano(nome_plano=nome, preco_plano=preco, duracao_dias=dias)
    plano.destaque = destaque
    PlanoDAO.salvar(plano)
    return plano


def _quatro_planos():
    return [
        _plano('Anual', '1080.00', 365),
        _plano('Mensal', '120.00', 30),
        _plano('Semestral', '600.00', 180),
        _plano('Trimestral', '320.00', 90),
    ]


def test_calcula_preco_por_mes_economia_e_duracao(contexto_app):
    itens = vitrine_planos(_quatro_planos(), '/cadastrar')
    por_nome = {item['nome']: item for item in itens}

    assert [item['nome'] for item in itens] == ['Mensal', 'Trimestral', 'Semestral', 'Anual']
    assert por_nome['Trimestral']['preco_mes'] == Decimal('106.67')
    assert por_nome['Trimestral']['economia'] == Decimal('40.00')
    assert por_nome['Anual']['economia'] == Decimal('360.00')
    assert por_nome['Anual']['duracao_texto'] == '1 ano'
    assert por_nome['Semestral']['duracao_texto'] == '6 meses'
    assert por_nome['Mensal']['economia'] is None
    assert all(item['texto_botao'] == 'Matricular agora' for item in itens)


def test_sem_plano_de_30_dias_nao_inventa_economia(contexto_app):
    itens = vitrine_planos([_plano('Trimestral', '320.00', 90)], '/cadastrar')
    assert itens[0]['economia'] is None


def test_sem_destaque_marcado_vale_o_menor_preco_por_mes(contexto_app):
    itens = vitrine_planos(_quatro_planos(), '/cadastrar')
    assert [item['nome'] for item in itens if item['recomendado']] == ['Anual']


def test_destaque_do_admin_vence_a_regra_padrao(contexto_app):
    planos = _quatro_planos()
    trimestral = next(p for p in planos if p.nome_plano == 'Trimestral')
    PlanoDAO.definir_destaque(trimestral.id)
    itens = vitrine_planos(PlanoDAO.listar_todos(), '/cadastrar')
    assert [item['nome'] for item in itens if item['recomendado']] == ['Trimestral']


def test_so_um_plano_fica_em_destaque(contexto_app):
    planos = _quatro_planos()
    for plano in planos:
        PlanoDAO.definir_destaque(plano.id)
    assert [p.nome_plano for p in PlanoDAO.listar_todos() if p.destaque] == [planos[-1].nome_plano]


def test_home_mostra_os_planos_com_o_destaque_e_o_link_de_matricula(client, contexto_app):
    _quatro_planos()
    html = client.get('/').get_data(as_text=True)
    assert 'R$ 106,67' in html and 'R$ 90,00' in html
    assert 'Economia de R$ 360,00' in html
    assert html.count('Matricular agora') == 4
    assert 'href="/cadastrar"' in html
    assert html.count('et-plano--destaque') >= 1
    assert html.count('et-borda-brilho') == 1
    # A seção de planos vem antes de "Nosso método".
    assert html.index('R$ 106,67') < html.index('id="metodo"')


def test_aluno_logado_matricula_pela_area_do_aluno(client, contexto_app, criar_aluno, logar_como_aluno):
    _quatro_planos()
    logar_como_aluno(criar_aluno())
    html = client.get('/').get_data(as_text=True)
    assert 'href="/perfil#planos"' in html


def test_home_sem_planos_mostra_estado_vazio(client):
    html = client.get('/').get_data(as_text=True)
    assert 'Os planos ainda não foram publicados.' in html
    assert 'Matricular agora' not in html


def test_admin_destaca_e_tira_o_destaque(client, contexto_app, logar_como_admin):
    planos = _quatro_planos()
    mensal = next(p for p in planos if p.nome_plano == 'Mensal')
    logar_como_admin()

    resposta = client.post(f'/admin/planos/{mensal.id}/destaque', follow_redirects=True)
    assert 'Mensal agora aparece em destaque na página inicial.' in resposta.get_data(as_text=True)
    assert PlanoDAO.buscar_por_id(mensal.id).destaque is True

    client.post(f'/admin/planos/{mensal.id}/destaque', data={'acao': 'remover'})
    assert PlanoDAO.buscar_por_id(mensal.id).destaque is False


def test_admin_pode_criar_plano_ja_em_destaque(client, contexto_app, logar_como_admin):
    _quatro_planos()
    logar_como_admin()
    client.post('/admin/cadastrar_plano', data={
        'nome_plano': 'Bimestral', 'preco_plano': '230.00', 'duracao_dias': '60', 'destaque': 'sim',
    })
    assert [p.nome_plano for p in PlanoDAO.listar_todos() if p.destaque] == ['Bimestral']


def test_destacar_exige_admin(client, contexto_app, criar_aluno, logar_como_aluno):
    plano = _plano('Mensal', '120.00', 30)
    logar_como_aluno(criar_aluno())
    client.post(f'/admin/planos/{plano.id}/destaque')
    assert PlanoDAO.buscar_por_id(plano.id).destaque is False
