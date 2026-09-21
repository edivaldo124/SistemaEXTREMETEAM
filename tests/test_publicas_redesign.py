import re


def test_landing_page(client):
    resposta = client.get('/')
    assert resposta.status_code == 200
    html = resposta.get_data(as_text=True)

    # Logo horizontal oficial
    assert 'logo-horizontal-400.png' in html
    assert 'logo-horizontal-800.png' in html

    # Título do Hero em caixa alta
    assert 'DESPERTE SUA FORÇA.' in html
    assert 'VÁ AO EXTREMO.' in html

    # Visual do dragão recortado
    assert 'hero-emblema.webp' in html

    # Âncoras e ações da landing
    assert 'href="#estrutura"' in html
    assert 'href="#metodo"' in html
    assert 'data-abrir-login' in html

    # Faixa do método em 3 etapas
    assert 'Comece' in html
    assert 'Mantenha' in html
    assert 'Supere' in html

    # Modal de login da landing com campos e CSRF
    assert 'id="meuModal"' in html
    assert 'name="loginusuario"' in html
    assert 'name="senhausuario"' in html
    assert 'name="csrf_token"' in html


def test_login_page(client):
    resposta = client.get('/login')
    assert resposta.status_code == 200
    html = resposta.get_data(as_text=True)

    # Emblema da marca e controle ⇄
    assert 'logo-icon.png' in html
    assert 'flow-swap-btn' in html

    # Abas no mobile com link ativo
    assert 'class="auth-tabs"' in html
    assert 'aria-current="page"' in html
    assert 'href="/cadastrar"' in html

    # Campos de formulário e CSRF
    assert 'name="loginusuario"' in html
    assert 'id="loginusuario"' in html
    assert 'name="senhausuario"' in html
    assert 'id="senhausuario"' in html
    assert 'password-toggle' in html
    assert 'Lembrar meu usuário neste aparelho' in html
    assert 'href="/recuperar_senha"' in html
    assert 'name="csrf_token"' in html

    # Nonce CSP no script
    # O "mostrar senha" vive só em auth.js: um <script> inline repetindo a lógica alternava
    # o tipo duas vezes por clique e a senha nunca aparecia.
    assert 'js/auth.js' in html
    assert '<script nonce' not in html


def test_cadastro_page(client):
    resposta = client.get('/cadastrar')
    assert resposta.status_code == 200
    html = resposta.get_data(as_text=True)

    # Emblema da marca e botão ⇄ voltando para o login
    assert 'logo-icon.png' in html
    assert 'href="/login"' in html
    assert 'flow-swap-btn' in html

    # Abas mobile com link de criar conta ativo
    assert 'class="auth-tabs"' in html
    assert 'aria-current="page"' in html

    # Todos os campos obrigatórios preservados
    assert 'name="nomeusuario"' in html
    assert 'name="dataNascimento"' in html
    assert 'name="cpfusuario"' in html
    assert 'name="emailusuario"' in html
    assert 'name="telefoneusuario"' in html
    assert 'name="loginusuario"' in html
    assert 'name="senhausuario"' in html
    assert 'name="confirmarsenhausuario"' in html
    assert 'name="descricaousuario"' in html
    assert 'name="aceite_termos_responsabilidade"' in html
    assert 'name="csrf_token"' in html


def test_recuperar_senha_page(client):
    resposta = client.get('/recuperar_senha')
    assert resposta.status_code == 200
    html = resposta.get_data(as_text=True)

    # Campos de recuperação, CSRF e botão com verbo
    assert 'name="cpf"' in html
    assert 'name="email"' in html
    assert 'Enviar link de recuperação' in html
    assert 'name="csrf_token"' in html
    assert 'href="/login"' in html


def test_termos_responsabilidade_page(client):
    resposta = client.get('/termos-de-responsabilidade')
    assert resposta.status_code == 200
    html = resposta.get_data(as_text=True)

    assert 'Termo de Responsabilidade' in html
    assert 'Versão 2026-09' in html


def test_politica_privacidade_page(client):
    resposta = client.get('/politica-privacidade')
    assert resposta.status_code == 200
    html = resposta.get_data(as_text=True)

    assert 'Política de Privacidade' in html
    assert 'Gmail' in html
    assert 'Extreme Team' in html


def test_termos_servico_page(client):
    resposta = client.get('/termos-de-servico')
    assert resposta.status_code == 200
    html = resposta.get_data(as_text=True)

    assert 'Termos de Serviço' in html
    assert 'Conexão com o Gmail' in html
    assert 'Ao utilizar o sistema' in html
