import io
from pathlib import Path

import pytest
from PIL import Image
from sqlalchemy.exc import SQLAlchemyError

from config import db
from dao.professorDAO import ProfessorDAO
from modelos.professor import Professor


@pytest.fixture
def professor(contexto_app):
    professor = Professor(nome='Professora de teste', login='acesso-privado', senha='senha123')
    ProfessorDAO.salvar(professor)
    return professor


@pytest.fixture
def pasta_fotos(tmp_path, monkeypatch):
    monkeypatch.setenv('UPLOAD_DIR', str(tmp_path))
    return tmp_path / 'professores'


def _foto():
    arquivo = io.BytesIO()
    Image.new('RGB', (300, 200), (30, 80, 120)).save(arquivo, 'JPEG')
    arquivo.seek(0)
    return arquivo, 'perfil.jpg', 'image/jpeg'


def test_novo_professor_nao_publica_perfil_ou_contatos(professor):
    assert professor.perfil_publico is False
    assert professor.exibir_instagram is False
    assert professor.exibir_email is False
    assert professor.exibir_whatsapp is False
    assert professor.nome_exibicao == professor.nome


@pytest.mark.parametrize('tipo', [None, 'aluno', 'professor'])
def test_apenas_admin_edita_perfil(client, professor, tipo):
    if tipo:
        with client.session_transaction() as sess:
            sess['tipo_usuario'] = tipo
            sess['professor_id'] = professor.id
    for metodo in (client.get, client.post):
        resposta = metodo(f'/admin/professores/{professor.id}/editar', data={'nome_publico': 'Alterado'})
        assert resposta.status_code == 302
        assert resposta.headers['Location'].endswith('/login')
    assert ProfessorDAO.buscar_por_id(professor.id).nome_publico is None


def test_admin_salva_perfil_sem_alterar_acesso(client, professor, logar_como_admin):
    logar_como_admin()
    senha_anterior = professor.senha_hash
    resposta = client.post(f'/admin/professores/{professor.id}/editar', data={
        'nome_publico': '  Mestra Ana  ',
        'modalidades': 'Muay Thai e Boxe',
        'biografia': 'Ensino focado em técnica e evolução.',
        'formacao': 'Formação em educação física.',
        'instagram': 'https://www.instagram.com/mestra.ana/',
        'email_publico': 'contato.profissional@example.com',
        'whatsapp': '(81) 99999-8888',
        'perfil_publico': 'on',
        'exibir_instagram': 'on',
        'login': 'tentativa-alterar-login',
        'senha': 'tentativa-alterar-senha',
    }, follow_redirects=True)
    assert resposta.status_code == 200
    atualizado = ProfessorDAO.buscar_por_id(professor.id)
    assert atualizado.nome_exibicao == 'Mestra Ana'
    assert atualizado.instagram_url == 'https://www.instagram.com/mestra.ana/'
    assert atualizado.whatsapp_url == 'https://wa.me/5581999998888'
    assert atualizado.email_publico == 'contato.profissional@example.com'
    assert atualizado.perfil_publico is True
    assert atualizado.exibir_instagram is True
    assert atualizado.exibir_email is False
    assert atualizado.exibir_whatsapp is False
    assert atualizado.login == 'acesso-privado'
    assert atualizado.senha_hash == senha_anterior
    assert b'acesso-privado' not in resposta.data


@pytest.mark.parametrize('campo,valor', [
    ('instagram', 'https://site-falso.example/perfil'),
    ('email_publico', 'invalido@example.com\r\nBcc:outro@example.com'),
    ('whatsapp', 'javascript:alert(1)'),
    ('nome_publico', 'x' * 151),
    ('biografia', 'x' * 3001),
])
def test_contato_invalido_nao_salva_nenhuma_alteracao(client, professor, logar_como_admin, campo, valor):
    logar_como_admin()
    resposta = client.post(f'/admin/professores/{professor.id}/editar', data={
        'nome_publico': 'Não deve ser salvo', 'perfil_publico': 'on', campo: valor,
    })
    assert resposta.status_code == 400
    assert ProfessorDAO.buscar_por_id(professor.id).nome_publico is None
    assert professor.perfil_publico is False


def test_whatsapp_internacional_preservado_ao_reeditar(client, professor, logar_como_admin):
    logar_como_admin()
    url = f'/admin/professores/{professor.id}/editar'
    client.post(url, data={'whatsapp': '+14155552671'})
    assert professor.whatsapp == '14155552671'
    resposta = client.get(url)
    assert b'value="+14155552671"' in resposta.data
    client.post(url, data={'whatsapp': '+14155552671'})
    assert professor.whatsapp_url == 'https://wa.me/14155552671'


def test_publicar_e_retirar_foto_do_site(client, professor, logar_como_admin, pasta_fotos):
    logar_como_admin()
    url = f'/admin/professores/{professor.id}/editar'
    foto_url = f'/professores/{professor.id}/foto'
    resposta = client.post(url, data={'foto': _foto()}, content_type='multipart/form-data')
    assert resposta.status_code == 302
    arquivo = pasta_fotos / professor.foto_arquivo
    assert arquivo.exists()
    assert client.get(foto_url).status_code == 200  # administrador
    with client.session_transaction() as sess:
        sess.clear()
    assert client.get(foto_url).status_code == 404  # perfil privado
    with client.session_transaction() as sess:
        sess['tipo_usuario'] = 'professor'
        sess['professor_id'] = professor.id
    assert client.get(foto_url).status_code == 200  # próprio professor
    with client.session_transaction() as sess:
        sess['professor_id'] = professor.id + 1
    assert client.get(foto_url).status_code == 404  # outro professor
    logar_como_admin()
    client.post(url, data={'perfil_publico': 'on'})
    with client.session_transaction() as sess:
        sess.clear()
    publicada = client.get(foto_url)
    assert publicada.status_code == 200
    assert publicada.mimetype == 'image/jpeg'
    assert publicada.headers['Cache-Control'] == 'private, no-store'
    logar_como_admin()
    client.post(url, data={})
    with client.session_transaction() as sess:
        sess.clear()
    assert client.get(foto_url).status_code == 404
    assert arquivo.exists()


def test_substituir_remover_e_recusar_foto_falsa(client, professor, logar_como_admin, pasta_fotos):
    logar_como_admin()
    url = f'/admin/professores/{professor.id}/editar'
    client.post(url, data={'foto': _foto()}, content_type='multipart/form-data')
    antiga = professor.foto_arquivo
    falsa = client.post(url, data={'foto': (io.BytesIO(b'<script>evil</script>'), 'fake.jpg')}, content_type='multipart/form-data')
    assert falsa.status_code == 400
    assert professor.foto_arquivo == antiga
    assert (pasta_fotos / antiga).exists()
    client.post(url, data={'foto': _foto()}, content_type='multipart/form-data')
    nova = professor.foto_arquivo
    assert nova != antiga
    assert not (pasta_fotos / antiga).exists()
    assert (pasta_fotos / nova).exists()
    client.post(url, data={'remover_foto': 'on'})
    assert professor.foto_arquivo is None
    assert not (pasta_fotos / nova).exists()


def test_falha_ao_salvar_preserva_foto_anterior(client, professor, logar_como_admin, pasta_fotos, monkeypatch):
    logar_como_admin()
    url = f'/admin/professores/{professor.id}/editar'
    client.post(url, data={'foto': _foto()}, content_type='multipart/form-data')
    antiga = professor.foto_arquivo
    def falhar():
        raise SQLAlchemyError('falha simulada')
    with monkeypatch.context() as patch:
        patch.setattr(db.session, 'commit', falhar)
        resposta = client.post(url, data={'foto': _foto()}, content_type='multipart/form-data')
    assert resposta.status_code == 500
    assert professor.foto_arquivo == antiga
    assert list(pasta_fotos.iterdir()) == [Path(pasta_fotos / antiga)]


def test_edicao_professor_tem_protecao_csrf(client, app, professor, logar_como_admin):
    logar_como_admin()
    app.config['WTF_CSRF_ENABLED'] = True
    try:
        resposta = client.post(f'/admin/professores/{professor.id}/editar', data={'nome_publico': 'Inválido'})
        assert resposta.status_code == 400
        assert professor.nome_publico is None
    finally:
        app.config['WTF_CSRF_ENABLED'] = False
