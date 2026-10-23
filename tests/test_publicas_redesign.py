import re


def test_landing_page(client):
    resposta = client.get('/')
    assert resposta.status_code == 200
    html = resposta.get_data(as_text=True)

    # Logo horizontal oficial
    assert 'logo-horizontal-400.png' in html
    assert 'logo-horizontal-800.png' in html

    # Hero cinematográfico: a primeira manchete é o único <h1> (a caixa alta é do CSS).
    assert 'data-cinema' in html
    assert html.count('<h1') == 1
    assert re.search(r'<h1 class="cinema-titulo">.*Desperte.*sua força\.</span></span>\s*</h1>', html, re.S)

    # Planos logo depois do hero (sem planos cadastrados: o estado vazio real).
    assert 'id="planos"' in html
    assert 'Os planos ainda não foram publicados.' in html

    # Âncoras e ações da landing
    assert 'href="#estrutura"' in html
    assert 'href="#metodo"' in html
    assert 'href="#planos"' in html
    assert 'data-abrir-login' in html

    # Faixa do método em 3 etapas
    assert 'Crie sua conta' in html
    assert 'Escolha seu plano' in html
    assert 'Treine e acompanhe' in html

    # Modal de login da landing com campos e CSRF
    assert 'id="meuModal"' in html
    assert 'name="loginusuario"' in html
    assert 'name="senhausuario"' in html
    assert 'name="csrf_token"' in html
    # O "lembrar usuário" do modal é o do auth.js, com a regra da tela de login (sem CPF).
    assert 'js/auth.js' in html


def _cabecalho(html):
    return html.split('<header class="home-header">', 1)[1].split('</header>', 1)[0]


def _entrar_fixo(html):
    return re.search(r'<div class="entrar-fixo" data-entrar-fixo>(.*?)</div>', html, re.S).group(1)


def test_visitante_tem_entrar_fixo_que_abre_o_mesmo_modal(client):
    # O cabeçalho rola embora com o hero de 400svh; a pílula fixa assume o botão dele.
    pilula = _entrar_fixo(client.get('/').get_data(as_text=True))

    assert 'data-abrir-login' in pilula
    assert 'Entrar' in pilula


def test_aluno_logado_vai_da_home_direto_para_a_area_do_aluno(client, criar_aluno, logar_como_aluno):
    # O botão abria o modal de login de novo para quem já tinha entrado.
    logar_como_aluno(criar_aluno())

    html = client.get('/').get_data(as_text=True)

    for trecho in (_cabecalho(html), _entrar_fixo(html)):
        assert 'href="/perfil"' in trecho
        assert 'Área do aluno' in trecho
        assert 'data-abrir-login' not in trecho


def test_admin_logado_vai_da_home_para_o_painel(client, logar_como_admin):
    logar_como_admin()

    html = client.get('/').get_data(as_text=True)

    for trecho in (_cabecalho(html), _entrar_fixo(html)):
        assert 'href="/admin"' in trecho
        assert 'data-abrir-login' not in trecho


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
    # Exigências da verificação do app no Google (escopo sensível gmail.send).
    assert 'https://developers.google.com/terms/api-services-user-data-policy' in html
    assert 'requisitos de Uso Limitado' in html
    assert 'myaccount.google.com/permissions' in html


def test_pagina_inicial_liga_a_politica_e_os_termos(client):
    html = client.get('/').get_data(as_text=True)

    # O Google recusa a verificação do app sem o link da política na página inicial.
    assert 'href="/politica-privacidade"' in html
    assert 'href="/termos-de-servico"' in html


def test_termos_servico_page(client):
    resposta = client.get('/termos-de-servico')
    assert resposta.status_code == 200
    html = resposta.get_data(as_text=True)

    assert 'Termos de Serviço' in html
    assert 'Conexão com o Gmail' in html
    assert 'Ao utilizar o sistema' in html
