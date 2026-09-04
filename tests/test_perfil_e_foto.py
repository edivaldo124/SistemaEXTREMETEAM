import io

import pytest
from PIL import Image

from dao.usuarioDAO import AlunoDAO
from dao.professorDAO import ProfessorDAO
from dao.turmaDAO import TurmaDAO
from dao.matriculaDAO import MatriculaDAO
from modelos.professor import Professor
from modelos.turma import Turma


def _imagem_jpeg_valida():
    buffer = io.BytesIO()
    Image.new('RGB', (300, 200), color=(120, 30, 30)).save(buffer, format='JPEG')
    buffer.seek(0)
    return buffer


# ---------------------------------------------------------------------------
# GET /perfil - aluno vendo o proprio perfil
# ---------------------------------------------------------------------------

def test_aluno_ve_o_proprio_perfil(client, criar_aluno, logar_como_aluno):
    aluno = criar_aluno(graduacao='Kruang branco')
    logar_como_aluno(aluno)

    resp = client.get('/perfil')

    assert resp.status_code == 200
    assert aluno.nome.encode() in resp.data


def test_perfil_sem_sessao_redireciona_para_login(client):
    resp = client.get('/perfil')
    assert resp.status_code == 302
    assert '/login' in resp.headers['Location']


# ---------------------------------------------------------------------------
# Upload/remocao/substituicao de foto de perfil
# ---------------------------------------------------------------------------

def test_upload_de_foto_valida(client, criar_aluno, logar_como_aluno, contexto_app):
    aluno = criar_aluno()
    logar_como_aluno(aluno)

    resp = client.post('/perfil/foto', data={'foto': (_imagem_jpeg_valida(), 'foto.jpg', 'image/jpeg')},
                        content_type='multipart/form-data')

    assert resp.status_code == 302
    atualizado = AlunoDAO.buscar_por_id(aluno.id)
    assert atualizado.foto_arquivo is not None
    assert atualizado.foto_arquivo.endswith('.jpg')


def test_upload_de_arquivo_disfarcado_e_recusado(client, criar_aluno, logar_como_aluno):
    aluno = criar_aluno()
    logar_como_aluno(aluno)

    resp = client.post(
        '/perfil/foto',
        data={'foto': (io.BytesIO(b'<script>alert(1)</script>'), 'evil.jpg', 'image/jpeg')},
        content_type='multipart/form-data', follow_redirects=True,
    )

    assert resp.status_code == 200
    atualizado = AlunoDAO.buscar_por_id(aluno.id)
    assert atualizado.foto_arquivo is None


def test_substituir_e_remover_foto(client, criar_aluno, logar_como_aluno):
    aluno = criar_aluno()
    logar_como_aluno(aluno)

    client.post('/perfil/foto', data={'foto': (_imagem_jpeg_valida(), 'foto1.jpg', 'image/jpeg')},
                content_type='multipart/form-data')
    primeira = AlunoDAO.buscar_por_id(aluno.id).foto_arquivo
    assert primeira is not None

    client.post('/perfil/foto', data={'foto': (_imagem_jpeg_valida(), 'foto2.jpg', 'image/jpeg')},
                content_type='multipart/form-data')
    segunda = AlunoDAO.buscar_por_id(aluno.id).foto_arquivo
    assert segunda is not None
    assert segunda != primeira

    resp = client.post('/perfil/foto/remover')
    assert resp.status_code == 302
    assert AlunoDAO.buscar_por_id(aluno.id).foto_arquivo is None


def test_aluno_nao_acessa_foto_de_outro_aluno(client, criar_aluno, logar_como_aluno):
    aluno = criar_aluno()
    outro = criar_aluno()
    logar_como_aluno(aluno)

    client.post('/perfil/foto', data={'foto': (_imagem_jpeg_valida(), 'foto.jpg', 'image/jpeg')},
                content_type='multipart/form-data')

    resp = client.get(f'/perfil/foto/{outro.id}')
    assert resp.status_code == 403


def test_admin_acessa_foto_de_qualquer_aluno(client, criar_aluno, logar_como_aluno, logar_como_admin):
    aluno = criar_aluno()

    logar_como_aluno(aluno)
    client.post('/perfil/foto', data={'foto': (_imagem_jpeg_valida(), 'foto.jpg', 'image/jpeg')},
                content_type='multipart/form-data')
    client.get('/logout')

    logar_como_admin()
    resp = client.get(f'/perfil/foto/{aluno.id}')
    assert resp.status_code == 200


def test_professor_ve_foto_de_aluno_da_propria_turma(client, criar_aluno, contexto_app):
    aluno = criar_aluno()
    professor = Professor(nome='Prof Teste', login='prof-teste', senha='senha123')
    ProfessorDAO.salvar(professor)
    turma = Turma(nome='Turma Teste', dias_semana='Seg,Qua', horario='19:00', professor_id=professor.id)
    TurmaDAO.salvar(turma)
    MatriculaDAO.matricular(aluno.id, turma.id)

    with client.session_transaction() as sess:
        sess['usuario'] = aluno.login
        sess['aluno_id'] = aluno.id
        sess['tipo_usuario'] = 'aluno'
    client.post('/perfil/foto', data={'foto': (_imagem_jpeg_valida(), 'foto.jpg', 'image/jpeg')},
                content_type='multipart/form-data')
    client.get('/logout')

    with client.session_transaction() as sess:
        sess['usuario'] = professor.login
        sess['professor_id'] = professor.id
        sess['tipo_usuario'] = 'professor'

    resp = client.get(f'/perfil/foto/{aluno.id}')
    assert resp.status_code == 200


def test_professor_nao_ve_foto_de_aluno_fora_da_sua_turma(client, criar_aluno, contexto_app):
    aluno = criar_aluno()
    professor = Professor(nome='Prof Sem Turma', login='prof-sem-turma', senha='senha123')
    ProfessorDAO.salvar(professor)

    with client.session_transaction() as sess:
        sess['usuario'] = professor.login
        sess['professor_id'] = professor.id
        sess['tipo_usuario'] = 'professor'

    resp = client.get(f'/perfil/foto/{aluno.id}')
    assert resp.status_code == 403


# ---------------------------------------------------------------------------
# Pagina de pagamento - permissao entre alunos
# ---------------------------------------------------------------------------

def test_aluno_impedido_de_acessar_pagamento_de_outro_aluno(client, criar_pagamento, criar_aluno, logar_como_aluno):
    pagamento = criar_pagamento()
    outro_aluno = criar_aluno()
    logar_como_aluno(outro_aluno)

    resp = client.get(f'/perfil/pagamento/{pagamento.id}')
    assert resp.status_code == 404


def test_aluno_impedido_de_acessar_comprovante_de_outro_aluno(client, criar_pagamento, criar_aluno, logar_como_aluno):
    pagamento = criar_pagamento(status='pago')
    outro_aluno = criar_aluno()
    logar_como_aluno(outro_aluno)

    resp = client.get(f'/perfil/mensalidade/{pagamento.id}/comprovante')
    assert resp.status_code == 404


def test_comprovante_so_disponivel_quando_pago(client, criar_pagamento, logar_como_aluno):
    pagamento = criar_pagamento(status='pendente')
    logar_como_aluno(pagamento.aluno)

    resp = client.get(f'/perfil/mensalidade/{pagamento.id}/comprovante', follow_redirects=True)
    assert resp.status_code == 200
    assert f'/perfil/pagamento/{pagamento.id}' in resp.request.path
