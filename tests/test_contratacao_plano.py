from datetime import date
from decimal import Decimal

from dao.financeiroDAO import PagamentoDAO
from dao.matriculaDAO import MatriculaDAO
from dao.professorDAO import ProfessorDAO
from dao.turmaDAO import TurmaDAO
from modelos.professor import Professor
from modelos.turma import Turma


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


def test_escolher_plano_com_turma_cria_matricula(
    client, plano, criar_aluno, logar_como_aluno, contexto_app,
):
    professor = Professor(nome='Professor da turma', login='prof-turma', senha='senha123456')
    ProfessorDAO.salvar(professor)
    turma = Turma('Turma escolhida', 'Seg', '19:00', professor.id, 20)
    TurmaDAO.salvar(turma)
    aluno = criar_aluno()
    logar_como_aluno(aluno)

    resposta = client.post('/perfil', data={'plano': str(plano.id), 'turma_id': str(turma.id)})

    assert resposta.status_code == 302
    pagamento = PagamentoDAO.listar_por_aluno(aluno.id)[0]
    assert pagamento.turma_id == turma.id
    assert MatriculaDAO.listar_por_aluno(aluno.id) == []

    PagamentoDAO.marcar_pago_via_webhook(pagamento, data_pagamento=date.today())

    matriculas = MatriculaDAO.listar_por_aluno(aluno.id)
    assert len(matriculas) == 1
    assert matriculas[0].turma_id == turma.id


def test_valor_enviado_pelo_navegador_e_ignorado(client, plano, criar_aluno, logar_como_aluno):
    aluno = criar_aluno()
    logar_como_aluno(aluno)

    client.post('/perfil', data={'plano': str(plano.id), 'valor': '0.01'})

    pagamento = PagamentoDAO.listar_por_aluno(aluno.id)[0]
    assert pagamento.valor == Decimal('150.00')


def test_turma_lotada_nao_vira_matricula_apos_pagamento(
    client, plano, criar_aluno, logar_como_aluno, contexto_app,
):
    professor = Professor(nome='Professor lotado', login='prof-lotado', senha='senha123456')
    ProfessorDAO.salvar(professor)
    turma = Turma('Turma lotada', 'Seg', '19:00', professor.id, 1)
    TurmaDAO.salvar(turma)
    outro = criar_aluno(login='outro-lotado')
    MatriculaDAO.matricular(outro.id, turma.id)
    aluno = criar_aluno(login='aluno-lotado')
    logar_como_aluno(aluno)

    client.post('/perfil', data={'plano': str(plano.id), 'turma_id': str(turma.id)})
    pagamento = PagamentoDAO.listar_por_aluno(aluno.id)[0]
    PagamentoDAO.marcar_pago_via_webhook(pagamento, data_pagamento=date.today())

    assert MatriculaDAO.listar_por_aluno(aluno.id) == []


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
