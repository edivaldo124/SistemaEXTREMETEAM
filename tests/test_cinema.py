"""Hero cinematográfico da home e profundidade (tilt) dos cartões.

O hero guarda os textos no HTML (SEO e leitor de tela) e só aponta para a cena 3D,
compilada a partir de front/ em static/dist/cinema. Estes testes não rodam a cena (isso
é do navegador): garantem o contrato entre o template, o build e a CSP.
"""

import json
import re
from pathlib import Path

from flask import render_template_string
from PIL import Image

from servicos import cinema

RAIZ = Path(__file__).resolve().parents[1]
PASTA_BUILD = RAIZ / 'static' / 'dist' / 'cinema'


def _html(client, caminho='/'):
    return client.get(caminho).get_data(as_text=True)


def _secao_cinema(html):
    return re.search(r'<section class="cinema[^"]*".*?</section>', html, re.S).group(0)


# --- Textos do hero ------------------------------------------------------------------

def test_manchetes_ficam_no_html_e_so_a_primeira_e_visivel(client):
    secao = _secao_cinema(_html(client))
    manchetes = re.findall(r'<div class="cinema-manchete ([^"]+)" data-cinema-manchete([^>]*)>', secao)
    assert len(manchetes) == 4
    classes, atributos = manchetes[0]
    assert classes == 'is-active' and 'aria-hidden' not in atributos
    # As outras saem do leitor de tela e da ordem do Tab até a rolagem chegar nelas.
    for classes, atributos in manchetes[1:]:
        assert classes == 'is-after'
        assert 'aria-hidden="true"' in atributos and 'inert' in atributos


def test_so_a_primeira_manchete_e_h1_e_o_titulo_tem_espaco_entre_as_linhas(client):
    secao = _secao_cinema(_html(client))
    assert secao.count('<h1') == 1 and secao.count('<h2') == 3
    # As linhas são blocos no CSS; sem o espaço, buscador e leitor de tela leriam "Despertesua".
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', secao, re.S).group(1)
    assert ' '.join(re.sub(r'<[^>]+>', '', h1).split()) == 'Desperte sua força.'


def test_hero_tem_cadastro_seta_para_os_planos_e_poster(client):
    secao = _secao_cinema(_html(client))
    assert 'href="/cadastrar"' in secao
    assert 'class="cinema-seta" href="#planos"' in secao
    assert 'cinema-poster-largo.webp' in secao and 'cinema-poster-estreito.webp' in secao


# --- Build da cena -------------------------------------------------------------------

def test_cena_aponta_para_a_entrada_compilada_com_hash(client):
    secao = _secao_cinema(_html(client))
    src = re.search(r'data-cena-src="([^"]+)"', secao).group(1)
    assert re.fullmatch(r'/static/dist/cinema/cena-[\w-]+\.js', src)
    assert (RAIZ / src.lstrip('/')).is_file()


def test_manifest_tem_as_duas_entradas_e_todos_os_arquivos_existem():
    manifest = json.loads((PASTA_BUILD / 'manifest.json').read_text(encoding='utf-8'))
    entradas = {item['name'] for item in manifest.values() if item.get('isEntry')}
    assert entradas == {'cena', 'video'}
    for item in manifest.values():
        assert (PASTA_BUILD / item['file']).is_file(), item['file']


def test_cena_leva_a_imagem_do_emblema_no_build():
    # As brasas são sorteadas desta imagem; sem ela a cena nunca fica pronta (fica o pôster).
    manifest = json.loads((PASTA_BUILD / 'manifest.json').read_text(encoding='utf-8'))
    cena = manifest['src/cena.tsx']
    imagens = [arquivo for arquivo in cena.get('assets', []) if re.fullmatch(r'assets/emblema-[\w-]+\.webp', arquivo)]
    assert len(imagens) == 1
    assert imagens[0] in (PASTA_BUILD / cena['file']).read_text(encoding='utf-8')


def test_emblema_tem_fundo_transparente():
    # A cena só põe brasa em pixel opaco. Sem a transparência, o fundo preto do emblema
    # oficial viraria um retângulo de brasas em volta do dragão.
    with Image.open(RAIZ / 'front' / 'src' / 'emblema.webp') as emblema:
        assert emblema.mode == 'RGBA'
        alfa = emblema.getchannel('A').histogram()
    total = sum(alfa)
    assert alfa[0] / total > 0.3 and alfa[255] / total > 0.3


def test_build_nao_busca_nada_fora_do_site():
    # A CSP só aceita o próprio domínio: um HDRI ou script de CDN quebraria a cena.
    for arquivo in PASTA_BUILD.glob('*.js'):
        conteudo = arquivo.read_text(encoding='utf-8')
        for cdn in ('githack', 'jsdelivr', 'unpkg', 'drei-assets', 'gstatic', 'cdnjs'):
            assert cdn not in conteudo, f'{cdn} em {arquivo.name}'


def test_sem_build_a_home_fica_so_com_o_poster(client, monkeypatch, tmp_path):
    monkeypatch.setattr(client.application, 'static_folder', str(tmp_path))
    secao = _secao_cinema(_html(client))
    assert 'data-cena-src' not in secao
    assert 'cinema-poster-largo.webp' in secao


def test_video_so_entra_quando_o_arquivo_existe(client, monkeypatch):
    assert 'data-video-src' not in _secao_cinema(_html(client))
    monkeypatch.setattr(cinema, '_tem_video', lambda _pasta: True)
    secao = _secao_cinema(_html(client))
    assert 'data-video-src="/static/video/cinema.mp4"' in secao
    assert re.search(r'data-video-modulo="/static/dist/cinema/video-[\w-]+\.js"', secao)


def test_posteres_existem():
    for nome in ('cinema-poster-largo.webp', 'cinema-poster-estreito.webp'):
        assert (RAIZ / 'static' / 'imagens' / nome).is_file(), nome


# --- CSP -----------------------------------------------------------------------------

def test_scripts_da_home_sao_do_proprio_site_ou_tem_nonce(client):
    resposta = client.get('/')
    nonce = re.search(r"'nonce-([^']+)'", resposta.headers['Content-Security-Policy']).group(1)
    html = resposta.get_data(as_text=True)
    for src in re.findall(r'<script[^>]+src="([^"]+)"', html):
        assert src.startswith('/static/'), src
    for tag in re.findall(r'<script(?![^>]*\bsrc=)[^>]*>', html):
        assert f'nonce="{nonce}"' in tag, tag
    assert "classList.add('cinema-js')" in html


# --- Tilt (nível 1 de 3D) ------------------------------------------------------------

def test_cartao_de_plano_e_metrica_inclinam(app):
    plano = {'nome': 'Mensal', 'preco_total': 100, 'preco_mes': 100, 'meses': 1, 'url_matricula': '/x'}
    with app.test_request_context():
        html = render_template_string(
            '{% from "components/cartao_plano.html" import cartao_plano %}'
            '{% from "components/ui.html" import metrica %}'
            '{{ cartao_plano(plano) }}{{ metrica("Alunos ativos", 3) }}',
            plano=plano,
        )
    assert html.count('data-tilt') == 2
    assert 'class="et-plano et-tilt' in html
    assert 'class="et-metrica et-tilt' in html


def test_cartoes_do_metodo_na_home_inclinam(client):
    metodo = _html(client).split('id="metodo"', 1)[1].split('</section>', 1)[0]
    assert metodo.count('<article class="et-tilt" data-tilt>') == 3
