import io
import logging
import re
import threading
from datetime import date

from PIL import Image

import blueprints.adm_bp as adm_bp
import blueprints.pix_bp as pix_bp
import blueprints.usuario_bp as usuario_bp
from config import db, limiter
from dao.financeiroDAO import PagamentoDAO
from dao.usuarioDAO import AlunoDAO
from modelos.usuario import Aluno
from servicos.urls import url_publica
from servicos.senhas import SENHAS_COMUNS, erro_validacao_senha


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
    monkeypatch.delenv('ADMIN_PASSWORD_HASH', raising=False)

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


def test_cabecalhos_de_seguranca(client, logar_como_admin):
    # O /login não tem mais script inline (usa js/auth.js); o painel de avisos ainda tem,
    # e é nele que dá para conferir que o nonce da política é o mesmo do <script>.
    logar_como_admin()
    resposta = client.get('/admin/avisos')
    politica = resposta.headers['Content-Security-Policy']
    nonce = re.search(rb'<script nonce="([^"]+)"', resposta.data).group(1).decode()
    assert f"script-src 'self' 'nonce-{nonce}'" in politica
    assert "script-src-attr 'none'" in politica
    assert resposta.headers['X-Content-Type-Options'] == 'nosniff'
    assert resposta.headers['X-Frame-Options'] == 'SAMEORIGIN'
    assert resposta.headers['Referrer-Policy'] == 'same-origin'


def test_nonce_da_csp_muda_a_cada_requisicao(client):
    nonces = {
        re.search(r"'nonce-([^']+)'", client.get('/login').headers['Content-Security-Policy']).group(1)
        for _ in range(3)
    }
    assert len(nonces) == 3


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


def test_login_com_identificador_repetido_em_outra_coluna_nao_bloqueia_a_vitima(contexto_app, criar_aluno):
    """O `login` de um aluno pode ser o e-mail de outro; quem entra é decidido pela senha."""
    atacante = criar_aluno(login='vitima@example.com', email='atacante@example.com', senha='SenhaDoAtacante-1')
    vitima = criar_aluno(login='vitima', email='vitima@example.com', senha='SenhaDaVitima-2026')

    assert AlunoDAO.autenticar('vitima@example.com', 'SenhaDaVitima-2026').id == vitima.id
    assert AlunoDAO.autenticar('vitima@example.com', 'SenhaDoAtacante-1').id == atacante.id
    assert AlunoDAO.autenticar('vitima@example.com', 'errada') is None


def test_login_recusado_e_registrado_sem_o_identificador_cru(client, caplog):
    with caplog.at_level(logging.WARNING, logger='blueprints.usuario_bp'):
        client.post('/login', data={'loginusuario': 'digitou-a-senha-aqui', 'senhausuario': 'x'})

    registros = [r.getMessage() for r in caplog.records if 'Login recusado' in r.getMessage()]
    assert len(registros) == 1
    assert 'digitou-a-senha-aqui' not in registros[0]


def test_recuperacao_envia_email_fora_da_thread_da_requisicao(client, criar_aluno, monkeypatch):
    """O ramo "par existe" não pode pagar a ida ao provedor dentro da requisição."""
    aluno = criar_aluno(cpf='987.654.321-00', email='recuperacao@example.com')
    monkeypatch.setenv('FILA_EMAIL_SINCRONA', 'false')
    threads, enviado = [], threading.Event()

    def _falso(*_args, **_kwargs):
        threads.append(threading.current_thread())
        enviado.set()
        return True

    monkeypatch.setattr(usuario_bp, 'enviar_email', _falso)

    resposta = client.post('/recuperar_senha', data={'cpf': aluno.cpf, 'email': aluno.email})

    assert resposta.status_code == 200
    assert enviado.wait(timeout=5), 'O e-mail de recuperação não foi enviado.'
    assert threads[0] is not threading.current_thread()


def test_perfil_dados_recusa_campo_maior_que_a_coluna(client, criar_aluno, logar_como_aluno):
    aluno = criar_aluno(senha='SenhaDoAluno-2026', nome='Nome Original')
    logar_como_aluno(aluno)

    for campo in ('nome', 'login', 'telefone', 'descricao'):
        dados = {
            'senha_atual': 'SenhaDoAluno-2026', 'nome': 'Novo Nome', 'login': 'novo-login',
            'telefone': '', 'descricao': '',
        }
        dados[campo] = 'x' * 256
        resposta = client.post('/perfil/dados', data=dados)

        assert resposta.status_code == 302, campo
        db.session.expire_all()
        atual = AlunoDAO.buscar_por_id(aluno.id)
        assert atual.nome == 'Nome Original', f'{campo} grande demais alterou o cadastro.'
        assert atual.login != 'novo-login'


def test_perfil_email_recusa_endereco_invalido_ou_grande_demais(client, criar_aluno, logar_como_aluno):
    aluno = criar_aluno(senha='SenhaDoAluno-2026')
    logar_como_aluno(aluno)

    for novo in ('sem-arroba', f'{"a" * 200}@example.com'):
        resposta = client.post('/perfil/email', data={'senha_atual': 'SenhaDoAluno-2026', 'novo_email': novo})

        assert resposta.status_code == 302
        db.session.expire_all()
        assert AlunoDAO.buscar_por_id(aluno.id).email_pendente is None


def test_lista_de_senhas_comuns_tem_milhares_de_entradas():
    assert erro_validacao_senha('iloveyou')
    assert erro_validacao_senha('ILoveYou'), 'A comparação ignora maiúsculas e minúsculas.'
    assert len(SENHAS_COMUNS) >= 3000
    assert erro_validacao_senha('Treino-Forte-2026') is None


def _cadastro_publico(client, **campos):
    dados = {
        'nomeusuario': 'Pessoa Nova', 'loginusuario': 'pessoa-nova', 'dataNascimento': '2000-01-01',
        'cpfusuario': '529.982.247-25', 'senhausuario': 'Treino-Forte-2026',
        'confirmarsenhausuario': 'Treino-Forte-2026', 'emailusuario': 'nova@example.com',
        'telefoneusuario': '11999999999', 'descricaousuario': '',
        'aceite_termos_responsabilidade': 'aceito',
    }
    dados.update(campos)
    return client.post('/cadastrar', data=dados)


def _mensagem_da_resposta(resposta):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', resposta.get_data(as_text=True)))


def test_cadastro_publico_nao_revela_cpf_nem_email_ja_cadastrados(client, criar_aluno, sem_email):
    """Cadastro novo, CPF existente e e-mail existente respondem com a MESMA tela."""
    existente = criar_aluno(cpf='111.444.777-35', email='existente@example.com', login='existente')

    novo = _cadastro_publico(client)
    cpf_repetido = _cadastro_publico(client, cpfusuario=existente.cpf, loginusuario='outro-1', emailusuario='a@example.com')
    email_repetido = _cadastro_publico(client, cpfusuario='390.533.447-05', loginusuario='outro-2', emailusuario=existente.email)

    assert novo.status_code == cpf_repetido.status_code == email_repetido.status_code == 200
    assert _mensagem_da_resposta(novo) == _mensagem_da_resposta(cpf_repetido) == _mensagem_da_resposta(email_repetido)


def test_cadastro_com_email_existente_nao_cria_conta_e_avisa_o_dono(client, criar_aluno, sem_email):
    existente = criar_aluno(cpf='111.444.777-35', email='existente@example.com', login='existente')
    total = Aluno.query.count()

    _cadastro_publico(client, cpfusuario='390.533.447-05', loginusuario='outro-2', emailusuario=existente.email)

    assert Aluno.query.count() == total
    assert [e['para'] for e in sem_email] == [existente.email]


def test_cadastro_publico_continua_avisando_usuario_repetido(client, criar_aluno):
    criar_aluno(login='pessoa-nova')

    resposta = _cadastro_publico(client)

    assert 'já está em uso' in resposta.get_data(as_text=True)
    assert Aluno.query.filter_by(email='nova@example.com').first() is None


def test_confirmar_troca_de_email_descarta_link_de_recuperacao_do_endereco_antigo(client, criar_aluno):
    """Quem ainda controla a caixa antiga não pode assumir a conta depois da troca."""
    import hashlib
    import secrets
    from datetime import datetime, timedelta

    aluno = criar_aluno(email='antigo@example.com')
    token = secrets.token_urlsafe(32)
    aluno.email_pendente = 'novo@example.com'
    aluno.token_email_hash = hashlib.sha256(token.encode()).hexdigest()
    aluno.token_email_expira = datetime.utcnow() + timedelta(minutes=10)
    aluno.token_recuperacao_hash = hashlib.sha256(b'enviado-ao-email-antigo').hexdigest()
    aluno.token_recuperacao_expira = datetime.utcnow() + timedelta(minutes=10)
    db.session.commit()

    client.get(f'/perfil/confirmar_email/{token}')

    db.session.refresh(aluno)
    assert aluno.email == 'novo@example.com'
    assert aluno.token_recuperacao_hash is None and aluno.token_recuperacao_expira is None
