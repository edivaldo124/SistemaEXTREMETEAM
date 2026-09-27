"""Página de erro (templates/erro.html) e os handlers de 404, 403, 500 e CSRF."""

import pytest
from werkzeug.exceptions import InternalServerError


def test_404_mostra_a_pagina_de_erro_com_o_proximo_passo(client):
    resposta = client.get('/pagina-que-nao-existe')
    assert resposta.status_code == 404
    html = resposta.get_data(as_text=True)
    assert 'Página não encontrada' in html
    assert 'class="et-vazio"' in html
    # Visitante volta ao início.
    assert 'href="/">Voltar ao início</a>' in html
    # Estende o layout: head comum e região de toasts.
    assert 'js/componentes.js' in html and 'data-toasts' in html


def test_404_para_quem_esta_logado_leva_a_area_dele(client, criar_aluno, logar_como_aluno):
    logar_como_aluno(criar_aluno())
    html = client.get('/nada-aqui').get_data(as_text=True)
    assert 'href="/perfil">Ir para minha área</a>' in html


def test_404_em_rota_de_api_continua_json(client):
    resposta = client.get('/api/nao-existe')
    assert resposta.status_code == 404
    assert resposta.is_json
    assert 'erro' in resposta.get_json()


def test_403_oferece_entrar_de_novo(client, criar_aluno, criar_pagamento, logar_como_aluno):
    dono = criar_aluno()
    pagamento = criar_pagamento(aluno=dono)
    logar_como_aluno(criar_aluno())  # outro aluno tentando abrir a cobrança do primeiro
    resposta = client.post(f'/perfil/mensalidade/{pagamento.id}/checkout')
    assert resposta.status_code == 403
    html = resposta.get_data(as_text=True)
    assert 'Você não tem acesso a esta página' in html
    assert 'href="/login">Entrar de novo</a>' in html
    # A ação secundária leva à área de quem está logado.
    assert 'href="/perfil"' in html


def test_500_mostra_a_pagina_de_erro(app):
    # Em teste o Flask propaga exceções em vez de chamar o handler; chama-se o handler direto.
    from servidor import erro_interno

    with app.test_request_context('/qualquer'):
        html, codigo = erro_interno(InternalServerError())
    assert codigo == 500
    assert 'Algo falhou do nosso lado' in html
    assert 'Traceback' not in html


@pytest.fixture
def csrf_ligado(app):
    app.config['WTF_CSRF_ENABLED'] = True
    yield
    app.config['WTF_CSRF_ENABLED'] = False


def test_csrf_expirado_mostra_a_pagina_de_erro_e_volta_para_a_origem(client, csrf_ligado):
    resposta = client.post(
        '/recuperar_senha', data={'cpf': '000.000.000-00', 'email': 'a@b.com'},
        headers={'Referer': 'https://localhost/recuperar_senha'},
    )
    assert resposta.status_code == 400
    html = resposta.get_data(as_text=True)
    assert 'Sua sessão de segurança expirou' in html
    assert 'href="/recuperar_senha">Voltar à página</a>' in html


def test_csrf_nao_segue_referer_de_outro_site(client, csrf_ligado):
    resposta = client.post('/recuperar_senha', data={}, headers={'Referer': 'https://golpe.example/x'})
    html = resposta.get_data(as_text=True)
    assert 'golpe.example' not in html
    assert 'href="/">Voltar à página</a>' in html


def test_csrf_no_login_continua_devolvendo_o_login(client, csrf_ligado):
    resposta = client.post('/login', data={'loginusuario': 'x', 'senhausuario': 'y'})
    assert resposta.status_code == 400
    html = resposta.get_data(as_text=True)
    assert 'name="loginusuario"' in html
    assert 'erro-cartao' not in html


def test_csrf_em_api_continua_json(client, csrf_ligado):
    resposta = client.post('/api/mensalidades/1/pix')
    assert resposta.status_code == 400
    assert resposta.is_json
