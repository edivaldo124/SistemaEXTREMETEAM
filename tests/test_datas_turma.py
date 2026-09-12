from datetime import date

import pytest

from dao.matriculaDAO import MatriculaDAO
from dao.professorDAO import ProfessorDAO
from dao.turmaDAO import TurmaDAO
from modelos.presenca import Presenca
from modelos.professor import Professor
from modelos.turma import Turma
from servicos.autorizacao import impressao_credencial


@pytest.fixture
def turma(contexto_app):
    professor = Professor(nome='Professor Data', login='professor-data', senha='senha123456')
    ProfessorDAO.salvar(professor)
    turma = Turma('Turma Data', 'Seg', '19:00', professor.id, 20)
    TurmaDAO.salvar(turma)
    return turma


@pytest.mark.parametrize('valor', ['abc', '2026-13-45', '2026-02-30', '../../etc/passwd'])
def test_consulta_com_data_invalida_exibe_hoje_e_aviso(client, logar_como_admin, turma, valor):
    logar_como_admin()

    resposta = client.get(f'/turmas/{turma.id}', query_string={'data': valor})

    assert resposta.status_code == 200
    pagina = resposta.get_data(as_text=True)
    assert f'value="{date.today().isoformat()}"' in pagina
    assert 'Data inválida. Exibindo a aula de hoje' in pagina
    assert 'role="alert"' in pagina


def test_consulta_com_data_valida_preserva_data_selecionada(client, logar_como_admin, turma):
    logar_como_admin()

    resposta = client.get(f'/turmas/{turma.id}', query_string={'data': '2026-09-07'})

    assert resposta.status_code == 200
    pagina = resposta.get_data(as_text=True)
    assert 'value="2026-09-07"' in pagina
    assert 'Data inválida.' not in pagina


@pytest.mark.parametrize('valor', [None, '', 'abc', '2026-13-45', '2026-02-30', '../../etc/passwd'])
def test_presenca_com_data_invalida_nao_grava(client, logar_como_admin, criar_aluno, turma, valor):
    aluno = criar_aluno()
    MatriculaDAO.matricular(aluno.id, turma.id)
    logar_como_admin()
    dados = {f'presente_{aluno.id}': 'on'}
    if valor is not None:
        dados['data_aula'] = valor

    resposta = client.post(f'/turmas/{turma.id}/presenca', data=dados)

    assert resposta.status_code == 400
    assert 'Informe uma data válida' in resposta.get_data(as_text=True)
    assert Presenca.query.count() == 0


@pytest.mark.parametrize('papel', ['admin', 'professor'])
def test_presenca_com_data_valida_continua_disponivel(client, criar_aluno, turma, papel):
    aluno = criar_aluno()
    MatriculaDAO.matricular(aluno.id, turma.id)
    with client.session_transaction() as sessao:
        sessao['tipo_usuario'] = papel
        sessao['professor_id'] = turma.professor_id
        # Cada papel carrega a credencial do SEU dono: a do admin vem do ambiente.
        if papel == 'admin':
            from servicos.credenciais import referencia_credencial_admin
            sessao['credencial'] = impressao_credencial(referencia_credencial_admin())
        else:
            sessao['credencial'] = impressao_credencial(turma.professor.senha_hash)

    resposta = client.post(f'/turmas/{turma.id}/presenca', data={
        'data_aula': '2026-09-07',
        f'presente_{aluno.id}': 'on',
    })

    assert resposta.status_code == 302
    assert resposta.headers['Location'] == f'/turmas/{turma.id}?data=2026-09-07'
    presenca = Presenca.query.one()
    assert presenca.aluno_id == aluno.id
    assert presenca.data_aula == date(2026, 9, 7)
    assert presenca.presente is True


@pytest.mark.parametrize(
    'papel,codigo',
    [(None, 302), ('aluno', 302), ('professor', 403), ('professor_inexistente', 302)],
)
@pytest.mark.parametrize('metodo', ['GET', 'POST'])
def test_data_invalida_nao_contorna_permissoes(client, turma, papel, codigo, metodo):
    if papel == 'professor':
        # Um professor REAL, dono de outra turma: o acesso é negado com 403 porque a
        # sessão vale, mas a turma não é dele.
        from dao.professorDAO import ProfessorDAO
        from modelos.professor import Professor

        outro = Professor(nome='Outro Professor', login='outro-prof', senha='senha-de-teste-123')
        ProfessorDAO.salvar(outro)
        with client.session_transaction() as sessao:
            sessao['tipo_usuario'] = 'professor'
            sessao['professor_id'] = outro.id
            sessao['credencial'] = impressao_credencial(outro.senha_hash)
    elif papel == 'professor_inexistente':
        # Sessão apontando para um cadastro que não existe mais: agora ela é encerrada
        # e o pedido volta ao login, em vez de seguir até a checagem da turma.
        with client.session_transaction() as sessao:
            sessao['tipo_usuario'] = 'professor'
            sessao['professor_id'] = turma.professor_id + 1000
            sessao['credencial'] = impressao_credencial(turma.professor.senha_hash)
    elif papel:
        with client.session_transaction() as sessao:
            sessao['tipo_usuario'] = papel
            sessao['professor_id'] = turma.professor_id + 1
    if metodo == 'GET':
        resposta = client.get(f'/turmas/{turma.id}', query_string={'data': 'invalida'})
    else:
        resposta = client.post(f'/turmas/{turma.id}/presenca', data={'data_aula': 'invalida'})

    assert resposta.status_code == codigo
    if codigo == 302:
        assert resposta.headers['Location'] == '/login'
    assert Presenca.query.count() == 0
