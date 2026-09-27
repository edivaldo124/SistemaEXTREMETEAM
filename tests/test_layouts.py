"""Layouts base (templates/layouts/) e toasts.

Cada página estende o layout da sua área, que estende layouts/base.html. Estes testes
cobram o que o layout garante: o <head> comum aparece uma vez só (sem <link>/<script>
duplicado), a região de toasts existe e o flash() vira toast.
"""

from pathlib import Path

import pytest

RAIZ_TEMPLATES = Path(__file__).resolve().parent.parent / 'templates'
PAGINAS = sorted(p.name for p in RAIZ_TEMPLATES.glob('*.html'))

PUBLICAS = [
    '/', '/login', '/cadastrar', '/recuperar_senha',
    '/termos-de-servico', '/politica-privacidade', '/termos-de-responsabilidade',
]


def _conferir_head_comum(html):
    assert html.count('js/componentes.js') == 1
    assert html.count('css/theme.css') == 1
    assert html.count('css/extreme.css') == 1
    assert html.count('<!DOCTYPE html>') == 1
    assert 'data-toasts' in html
    assert 'imagens/favicon-32.png' in html


@pytest.mark.parametrize('pagina', PAGINAS)
def test_toda_pagina_estende_um_layout(pagina):
    fonte = (RAIZ_TEMPLATES / pagina).read_text(encoding='utf-8')
    assert '{% extends "layouts/' in fonte or "{% extends 'layouts/" in fonte, pagina
    # O esqueleto (doctype, <head>, <body>) mora só em layouts/base.html.
    assert '<!DOCTYPE' not in fonte, pagina
    assert '<head>' not in fonte, pagina
    # flash() é mostrado pelo toast do layout; um bloco próprio na página duplicaria o aviso.
    assert 'get_flashed_messages' not in fonte, pagina


@pytest.mark.parametrize('caminho', PUBLICAS)
def test_paginas_publicas_carregam_o_head_comum(client, caminho):
    resposta = client.get(caminho)
    assert resposta.status_code == 200
    _conferir_head_comum(resposta.get_data(as_text=True))


def test_painel_admin_carrega_o_layout_admin(client, logar_como_admin):
    logar_como_admin()
    resposta = client.get('/admin')
    assert resposta.status_code == 200
    html = resposta.get_data(as_text=True)
    _conferir_head_comum(html)
    assert 'class="admin-shell"' in html
    # Deslize entre telas só na área logada.
    assert '@view-transition' in html


def test_pagina_publica_nao_carrega_o_deslize(client):
    html = client.get('/').get_data(as_text=True)
    assert '@view-transition' not in html


def test_area_do_aluno_carrega_o_layout(client, criar_aluno, logar_como_aluno):
    aluno = criar_aluno()
    logar_como_aluno(aluno)
    resposta = client.get('/perfil')
    assert resposta.status_code == 200
    _conferir_head_comum(resposta.get_data(as_text=True))


def test_flash_de_erro_vira_toast_que_nao_some_sozinho(client, criar_aluno, logar_como_aluno):
    aluno = criar_aluno()
    logar_como_aluno(aluno)
    resposta = client.post('/perfil', data={'plano': '999999'}, follow_redirects=True)
    html = resposta.get_data(as_text=True)
    assert 'Plano inválido ou indisponível.' in html
    assert 'et-toast--erro' in html
    assert 'role="alert"' in html
    # Só avisos que não são erro recebem a saída automática.
    trecho = html[html.index('et-toast--erro'):]
    trecho = trecho[:trecho.index('>')]
    assert 'data-toast-some' not in trecho
    # A mensagem aparece uma vez: no toast, não também num bloco antigo da página.
    assert html.count('Plano inválido ou indisponível.') == 1
