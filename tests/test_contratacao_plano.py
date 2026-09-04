from datetime import date
from decimal import Decimal

from dao.financeiroDAO import PagamentoDAO


def test_escolher_plano_cria_mensalidade_e_redireciona_para_pix(
    client, plano, criar_aluno, logar_como_aluno,
):
    aluno = criar_aluno()
    logar_como_aluno(aluno)

    resposta = client.post('/perfil', data={'plano': str(plano.id)})

    assert resposta.status_code == 302
    pagamento = PagamentoDAO.listar_por_aluno(aluno.id)[0]
    assert f'pix={pagamento.id}' in resposta.headers['Location']
    assert pagamento.status == 'pendente'
    assert pagamento.valor == Decimal('150.00')
    assert pagamento.vencimento == date.today()
    assert pagamento.competencia == date.today().strftime('%Y-%m')


def test_valor_enviado_pelo_navegador_e_ignorado(client, plano, criar_aluno, logar_como_aluno):
    aluno = criar_aluno()
    logar_como_aluno(aluno)

    client.post('/perfil', data={'plano': str(plano.id), 'valor': '0.01'})

    pagamento = PagamentoDAO.listar_por_aluno(aluno.id)[0]
    assert pagamento.valor == Decimal('150.00')


def test_reenvio_da_contratacao_reutiliza_mensalidade(client, plano, criar_aluno, logar_como_aluno):
    aluno = criar_aluno()
    logar_como_aluno(aluno)

    primeira = client.post('/perfil', data={'plano': str(plano.id)})
    segunda = client.post('/perfil', data={'plano': str(plano.id)})

    pagamentos = PagamentoDAO.listar_por_aluno(aluno.id)
    assert len(pagamentos) == 1
    assert primeira.headers['Location'] == segunda.headers['Location']


def test_plano_invalido_nao_cria_mensalidade(client, criar_aluno, logar_como_aluno):
    aluno = criar_aluno()
    logar_como_aluno(aluno)

    resposta = client.post('/perfil', data={'plano': '999999'})

    assert resposta.status_code == 302
    assert PagamentoDAO.listar_por_aluno(aluno.id) == []


def test_perfil_so_autoriza_abertura_automatica_da_propria_mensalidade(
    client, criar_pagamento, criar_aluno, logar_como_aluno,
):
    pagamento = criar_pagamento()
    outro_aluno = criar_aluno()
    logar_como_aluno(outro_aluno)

    resposta = client.get(f'/perfil?pix={pagamento.id}')

    assert resposta.status_code == 200
    assert b'data-auto-pix-id' not in resposta.data


def test_plano_atual_continua_disponivel_para_gerar_cobranca(
    client, plano, criar_aluno, logar_como_aluno,
):
    aluno = criar_aluno(plano_id=plano.id)
    logar_como_aluno(aluno)

    resposta = client.get('/perfil')

    assert resposta.status_code == 200
    assert b'Pagar plano atual' not in resposta.data  # texto é aplicado pelo JS
    assert b'class="btn-escolher"' in resposta.data
    assert b'disabled' not in resposta.data


def test_area_do_aluno_renderiza_telas_independentes_do_menu(
    client, criar_aluno, logar_como_aluno,
):
    aluno = criar_aluno()
    logar_como_aluno(aluno)

    resposta = client.get('/perfil')

    assert resposta.status_code == 200
    for tela in (b'visao-geral', b'turmas', b'mensalidades', b'planos', b'meus-dados'):
        assert b'id="' + tela + b'"' in resposta.data
        assert b'data-menu-screen="' + tela + b'"' in resposta.data
