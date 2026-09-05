import io
import re
from datetime import date

from PIL import Image

import blueprints.adm_bp as adm_bp
import blueprints.pix_bp as pix_bp
import blueprints.usuario_bp as usuario_bp
from config import db, limiter
from dao.financeiroDAO import PagamentoDAO
from dao.usuarioDAO import AlunoDAO
from servicos.urls import url_publica
from servicos.senhas import erro_validacao_senha


def _imagem_jpeg():
    conteudo = io.BytesIO()
    Image.new('RGB', (40, 40), color=(30, 60, 90)).save(conteudo, format='JPEG')
    conteudo.seek(0)
    return conteudo


def test_rotas_admin_nao_colidem_cpf_com_campos_editaveis(
    client, criar_aluno, plano, logar_como_admin, monkeypatch,
):
    alvo = criar_aluno(
        nome='Aluno correto', cpf='123.456.789-01', email='correto@example.com', login='correto',
    )
    impostor = criar_aluno(
        nome='123.456.789-01', descricao='12345678901', email='impostor@example.com', login='impostor',
    )
    logar_como_admin()

    resposta = client.get('/admin/usuario/12345678901')
    assert resposta.status_code == 200
    assert b'Aluno correto' in resposta.data
    assert b'impostor@example.com' not in resposta.data

    resposta = client.post(
        '/admin/usuario/12345678901',
        data={
            'nome': 'Aluno correto editado', 'login': alvo.login,
            'datanascimento': alvo.datanascimento, 'email': alvo.email,
            'telefone': alvo.telefone, 'plano_id': 'Nenhum', 'descricao': '',
        },
    )
    assert resposta.status_code == 302
    assert db.session.get(type(alvo), alvo.id).nome == 'Aluno correto editado'
    assert db.session.get(type(impostor), impostor.id).nome == '123.456.789-01'

    resposta = client.post(
        '/admin/usuario/12345678901/foto',
        data={'foto': (_imagem_jpeg(), 'foto.jpg', 'image/jpeg')},
        content_type='multipart/form-data',
    )
    assert resposta.status_code == 302
    assert AlunoDAO.buscar_por_id(alvo.id).foto_arquivo
    assert AlunoDAO.buscar_por_id(impostor.id).foto_arquivo is None

    resposta = client.post(
        '/admin/usuario/12345678901/pagamentos',
        data={
            'plano_id': plano.id, 'valor': '150.00', 'vencimento': date.today().isoformat(),
            'status': 'pendente', 'forma_pagamento': '', 'data_pagamento': '',
        },
    )
    assert resposta.status_code == 302
    pagamentos = PagamentoDAO.listar_por_aluno(alvo.id)
    assert len(pagamentos) == 1
    assert PagamentoDAO.listar_por_aluno(impostor.id) == []

    destinatarios = []
    monkeypatch.setattr(
        adm_bp, 'enviar_email',
        lambda email, *_args, **_kwargs: destinatarios.append(email) or True,
    )
    resposta = client.post('/admin/usuario/12345678901/cobrar')
    assert resposta.status_code == 302
    assert destinatarios == [alvo.email]


def test_login_nao_aceita_nome_do_aluno(contexto_app, criar_aluno):
    aluno = criar_aluno(nome='nome-publico', login='login-unico', senha='senha123')
    assert AlunoDAO.autenticar('nome-publico', 'senha123') is None
    assert AlunoDAO.autenticar('login-unico', 'senha123').id == aluno.id


def test_csrf_rejeita_token_ausente_e_aceita_token_valido(app, client):
    app.config['WTF_CSRF_ENABLED'] = True
    try:
        assert client.post('/logout').status_code == 400

        pagina = client.get('/login')
        token = re.search(rb'name="csrf_token" value="([^"]+)"', pagina.data).group(1).decode()
        assert client.post('/logout', data={'csrf_token': token}).status_code == 302
    finally:
        app.config['WTF_CSRF_ENABLED'] = False


def test_webhook_e_excecao_especifica_do_csrf(app, client):
    app.config['WTF_CSRF_ENABLED'] = True
    try:
        resposta = client.post('/api/webhooks/mercado-pago?data.id=1')
        assert resposta.status_code == 400
        assert b'sess' not in resposta.data.lower()
    finally:
        app.config['WTF_CSRF_ENABLED'] = False


def test_api_post_aceita_token_csrf_no_cabecalho(
    app, client, criar_pagamento, logar_como_aluno, monkeypatch,
):
    pagamento = criar_pagamento()
    logar_como_aluno(pagamento.aluno)
    monkeypatch.setattr(
        pix_bp, 'criar_pagamento_pix',
        lambda **_kwargs: {
            'sucesso': True, 'payment_id': 'mp-csrf', 'status': 'pending',
            'qr_code': 'copia-cola', 'qr_code_base64': None,
            'ticket_url': None, 'data_expiracao': None,
        },
    )
    app.config['WTF_CSRF_ENABLED'] = True
    try:
        pagina = client.get(f'/perfil/pagamento/{pagamento.id}')
        token = re.search(rb'name="csrf-token" content="([^"]+)"', pagina.data).group(1).decode()

        sem_token = client.post(f'/api/mensalidades/{pagamento.id}/pix')
        com_token = client.post(
            f'/api/mensalidades/{pagamento.id}/pix', headers={'X-CSRFToken': token},
        )
        assert sem_token.status_code == 400
        assert com_token.status_code == 200
    finally:
        app.config['WTF_CSRF_ENABLED'] = False


def test_limite_de_login_por_ip_e_identificador(client, monkeypatch):
    limiter.reset()
    monkeypatch.setattr(usuario_bp.ProfessorDAO, 'autenticar', lambda *_args: None)
    monkeypatch.setattr(usuario_bp.AlunoDAO, 'autenticar', lambda *_args: None)
    monkeypatch.delenv('ADMIN_USER', raising=False)
    monkeypatch.delenv('ADMIN_PASSWORD', raising=False)

    respostas = [
        client.post('/login', data={'loginusuario': 'alvo', 'senhausuario': 'errada'})
        for _ in range(6)
    ]
    assert [resposta.status_code for resposta in respostas[:5]] == [200] * 5
    assert respostas[5].status_code == 429


def test_host_nao_confiavel_e_rejeitado(client):
    assert client.get('/', headers={'Host': 'atacante.example'}).status_code == 400


def test_url_publica_independe_do_host_da_requisicao(app):
    with app.test_request_context('/', headers={'Host': 'localhost'}):
        assert url_publica('auth.redefinir_senha', token='teste') == (
            'https://academia.example.test/recuperar_senha/teste'
        )


def test_recuperacao_envia_link_da_url_configurada(client, criar_aluno, monkeypatch):
    aluno = criar_aluno(cpf='987.654.321-00', email='recuperacao@example.com')
    links = []
    monkeypatch.setattr(
        usuario_bp, 'enviar_email',
        lambda *_args, **kwargs: links.append(kwargs.get('link_url')) or True,
    )

    resposta = client.post(
        '/recuperar_senha',
        data={'cpf': aluno.cpf, 'email': aluno.email},
        headers={'Host': 'localhost'},
    )

    assert resposta.status_code == 200
    assert len(links) == 1
    assert links[0].startswith('https://academia.example.test/recuperar_senha/')


def test_cabecalhos_de_seguranca(client):
    resposta = client.get('/login')
    politica = resposta.headers['Content-Security-Policy']
    nonce = re.search(rb'<script nonce="([^"]+)"', resposta.data).group(1).decode()
    assert f"script-src 'self' 'nonce-{nonce}'" in politica
    assert "script-src-attr 'none'" in politica
    assert resposta.headers['X-Content-Type-Options'] == 'nosniff'
    assert resposta.headers['X-Frame-Options'] == 'SAMEORIGIN'
    assert resposta.headers['Referrer-Policy'] == 'same-origin'


def test_limite_global_de_requisicao(client):
    resposta = client.post('/login', data={'campo': 'x' * (10 * 1024 * 1024 + 1)})
    assert resposta.status_code == 413


def test_logout_exige_post(client):
    assert client.get('/logout').status_code == 405
    assert client.post('/logout').status_code == 302


def test_senha_recusa_valores_curtos_comuns_e_iguais_ao_login():
    assert erro_validacao_senha('curta')
    assert erro_validacao_senha('senha123')
    assert erro_validacao_senha('meu-login', 'meu-login')
    assert erro_validacao_senha('uma senha longa e exclusiva') is None
