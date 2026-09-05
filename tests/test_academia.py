import pytest

from config import db
from modelos.academia import Academia
from modelos.professor import Professor
from servicos.contatos import validar_email, validar_instagram, validar_whatsapp


@pytest.mark.parametrize('tipo', [None, 'aluno', 'professor'])
def test_configuracoes_exigem_admin(client, contexto_app, tipo):
    if tipo:
        with client.session_transaction() as sess:
            sess['tipo_usuario'] = tipo
    assert client.get('/admin/academia').status_code == 302
    assert client.post('/admin/academia', data={'endereco': 'Não salvar'}).status_code == 302
    assert db.session.get(Academia, 1) is None


def test_admin_salva_atualiza_e_limpa_contatos(client, contexto_app, logar_como_admin):
    logar_como_admin()
    assert client.get('/admin/academia').status_code == 200
    resposta = client.post('/admin/academia', data={
        'instagram': 'https://www.instagram.com/equipe_teste/',
        'email': 'contato@example.com', 'whatsapp': '(81) 99999-1234',
        'endereco': 'Rua de Teste, 12, Recife, PE', 'complemento': 'Primeiro andar',
        'horarios': 'Segunda a sexta: 06h às 22h\nSábado: 08h às 12h',
    }, follow_redirects=True)
    assert resposta.status_code == 200
    academia = db.session.get(Academia, 1)
    assert academia.instagram == 'equipe_teste'
    assert academia.whatsapp == '5581999991234'
    assert 'query=Rua+de+Teste' in academia.mapa_url
    html = client.get('/').get_data(as_text=True)
    for conteudo in ('Rua de Teste', 'Primeiro andar', 'contato@example.com', 'https://wa.me/5581999991234', 'https://www.instagram.com/equipe_teste/'):
        assert conteudo in html
    client.post('/admin/academia', data={'email': 'novo@example.com'})
    assert Academia.query.count() == 1
    assert academia.instagram is None
    assert academia.endereco is None
    assert academia.email == 'novo@example.com'
    client.post('/admin/academia', data={})
    assert not academia.tem_contato


def test_erro_preserva_formulario_e_dados_salvos(client, contexto_app, logar_como_admin):
    logar_como_admin()
    db.session.add(Academia(id=1, endereco='Endereço original'))
    db.session.commit()
    resposta = client.post('/admin/academia', data={'instagram': 'javascript:alert(1)', 'endereco': 'Novo endereço'})
    assert resposta.status_code == 400
    assert 'Novo endereço' in resposta.get_data(as_text=True)
    assert db.session.get(Academia, 1).endereco == 'Endereço original'


def test_whatsapp_internacional_preserva_codigo_no_formulario(client, contexto_app, logar_como_admin):
    logar_como_admin()
    client.post('/admin/academia', data={'whatsapp': '+1 (415) 555-2671'})
    assert db.session.get(Academia, 1).whatsapp == '14155552671'
    assert 'value="+14155552671"' in client.get('/admin/academia').get_data(as_text=True)


def test_link_email_preserva_caracteres_do_endereco(client, contexto_app):
    db.session.add(Academia(id=1, email='treino#equipe+contato@example.com'))
    db.session.commit()
    html = client.get('/').get_data(as_text=True)
    assert 'mailto:treino%23equipe%2Bcontato@example.com' in html


def test_csrf_configuracoes(client, app, contexto_app, logar_como_admin):
    logar_como_admin()
    app.config['WTF_CSRF_ENABLED'] = True
    try:
        assert client.post('/admin/academia', data={'email': 'a@example.com'}).status_code == 400
        assert db.session.get(Academia, 1) is None
    finally:
        app.config['WTF_CSRF_ENABLED'] = False


def test_publicacao_professor_nao_expoe_contatos_sem_permissao(client, contexto_app):
    professor = Professor(nome='Nome interno', login='login-privado', senha='senha-teste')
    professor.nome_publico = 'Instrutor de exemplo'
    professor.email_publico = 'privado@example.com'
    professor.instagram = 'perfil_privado_teste'
    professor.whatsapp = '5581999991111'
    db.session.add(professor)
    db.session.commit()
    assert 'Instrutor de exemplo' not in client.get('/').get_data(as_text=True)
    professor.perfil_publico = True
    db.session.commit()
    html = client.get('/').get_data(as_text=True)
    assert 'Instrutor de exemplo' in html
    for privado in ('login-privado', 'privado@example.com', 'perfil_privado_teste', '5581999991111'):
        assert privado not in html
    professor.exibir_instagram = professor.exibir_email = professor.exibir_whatsapp = True
    db.session.commit()
    html = client.get('/').get_data(as_text=True)
    assert 'mailto:privado@example.com' in html
    assert 'https://www.instagram.com/perfil_privado_teste/' in html
    assert 'https://wa.me/5581999991111' in html


@pytest.mark.parametrize('funcao, valor', [
    (validar_instagram, 'https://instagram.com.evil.test/usuario'),
    (validar_instagram, 'https://instagram.com/p/post'),
    (validar_instagram, '<script>'),
    (validar_email, 'teste@example.com?subject=spam'),
    (validar_email, 'teste@example.com\nBcc:outro@example.com'),
    (validar_whatsapp, 'https://evil.test'),
    (validar_whatsapp, '123'),
])
def test_contatos_invalidos(funcao, valor):
    with pytest.raises(ValueError):
        funcao(valor)
