"""SEO técnico: robots.txt, sitemap, títulos, meta tags, noindex e JSON-LD da home."""

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.robotparser import RobotFileParser

import pytest
from flask import render_template
from PIL import Image

from config import db
from modelos.academia import Academia
from modelos.professor import Professor
from servicos.seo import dados_estruturados_academia, horarios_estruturados

BASE = 'https://academia.example.test'
RAIZ = Path(__file__).resolve().parent.parent
PUBLICAS = [
    '/', '/cadastrar', '/login', '/recuperar_senha',
    '/termos-de-servico', '/politica-privacidade', '/termos-de-responsabilidade',
]
PRIVADAS = [
    '/admin', '/admin/financeiro', '/perfil', '/perfil/pagamento/1', '/api/mensalidades/1/pix',
    '/professor', '/turmas/1', '/checkout', '/pix', '/logout', '/health',
    '/ativar-acesso/um-token', '/recuperar_senha/um-token', '/cadastro/obrigado',
]
NOINDEX = '<meta name="robots" content="noindex, nofollow">'


def _head(resposta):
    return resposta.get_data(as_text=True).split('</head>')[0]


def _robots(client):
    parser = RobotFileParser()
    parser.parse(client.get('/robots.txt').get_data(as_text=True).splitlines())
    return parser


def _json_ld(html):
    blocos = re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S)
    return [json.loads(bloco) for bloco in blocos]


def _sem_vazios(valor, caminho='raiz'):
    """Nenhum campo do JSON-LD pode sair nulo, vazio ou só com espaços."""
    assert valor not in (None, '', [], {}), caminho
    if isinstance(valor, str):
        assert valor.strip(), caminho
    elif isinstance(valor, dict):
        for chave, item in valor.items():
            _sem_vazios(item, f'{caminho}.{chave}')
    elif isinstance(valor, list):
        for i, item in enumerate(valor):
            _sem_vazios(item, f'{caminho}[{i}]')


# --- robots.txt e sitemap ----------------------------------------------------------

def test_robots_txt_bloqueia_areas_privadas(client):
    resposta = client.get('/robots.txt')
    assert resposta.status_code == 200
    assert resposta.mimetype == 'text/plain'

    robots = _robots(client)
    for caminho in PRIVADAS:
        assert not robots.can_fetch('*', f'{BASE}{caminho}'), caminho


def test_robots_txt_libera_paginas_publicas_e_fotos_da_equipe(client):
    robots = _robots(client)
    for caminho in PUBLICAS + ['/sitemap.xml', '/static/css/theme.css', '/professores/1/foto']:
        assert robots.can_fetch('*', f'{BASE}{caminho}'), caminho


def test_robots_txt_aponta_o_sitemap_pela_app_base_url(client):
    texto = client.get('/robots.txt').get_data(as_text=True)
    assert f'Sitemap: {BASE}/sitemap.xml' in texto


def test_robots_txt_usa_app_base_url_e_nao_o_host_da_requisicao(client):
    texto = client.get('/robots.txt', headers={'Host': 'localhost'}).get_data(as_text=True)
    assert f'Sitemap: {BASE}/sitemap.xml' in texto


def test_sitemap_lista_somente_paginas_publicas(client):
    resposta = client.get('/sitemap.xml')
    assert resposta.status_code == 200
    assert resposta.mimetype == 'application/xml'

    raiz = ET.fromstring(resposta.data)
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [loc.text for loc in raiz.findall('s:url/s:loc', ns)]
    assert sorted(urls) == sorted(f'{BASE}{caminho}' for caminho in PUBLICAS)

    robots = _robots(client)
    for url in urls:
        assert robots.can_fetch('*', url), url


@pytest.mark.parametrize('caminho', PUBLICAS)
def test_pagina_do_sitemap_abre_indexavel_com_canonical(client, caminho):
    resposta = client.get(caminho)
    assert resposta.status_code == 200
    head = _head(resposta)
    assert 'noindex' not in head
    assert f'<link rel="canonical" href="{BASE}{caminho}">' in head
    assert f'<meta property="og:url" content="{BASE}{caminho}">' in head


def test_canonical_ignora_query_string(client):
    head = _head(client.get('/?utm_source=instagram&x=1'))
    assert f'<link rel="canonical" href="{BASE}/">' in head
    assert 'utm_source' not in head


# --- Títulos, descrição e compartilhamento -----------------------------------------

def test_titulos_das_paginas_seguem_o_padrao_e_nao_se_repetem():
    titulos = {}
    for arquivo in sorted((RAIZ / 'templates').glob('*.html')):
        achado = re.search(r'\{% block titulo %\}(.*?)\{% endblock %\}', arquivo.read_text(encoding='utf-8'))
        if achado:
            titulos[arquivo.name] = achado.group(1)
    assert len(titulos) >= 20
    for arquivo, titulo in titulos.items():
        assert titulo.endswith(' | Extreme Team'), arquivo
    assert len(set(titulos.values())) == len(titulos)


def test_publicas_tem_titulo_e_descricao_proprios(client):
    titulos, descricoes = set(), set()
    for caminho in PUBLICAS:
        head = _head(client.get(caminho))
        titulo = re.search(r'<title>(.*?)</title>', head).group(1)
        descricao = re.search(r'<meta name="description" content="([^"]+)">', head).group(1)
        assert titulo.endswith(' | Extreme Team')
        assert 50 <= len(descricao) <= 160, caminho
        titulos.add(titulo)
        descricoes.add(descricao)
    assert len(titulos) == len(descricoes) == len(PUBLICAS)


def test_open_graph_e_twitter_card_na_home(client):
    head = _head(client.get('/'))
    for trecho in (
        '<meta property="og:locale" content="pt_BR">',
        '<meta property="og:title" content="Centro de Treinamento | Extreme Team">',
        f'<meta property="og:image" content="{BASE}/static/imagens/og-extreme-team.jpg">',
        '<meta name="twitter:card" content="summary_large_image">',
    ):
        assert trecho in head
    assert re.search(r'<meta property="og:description" content="[^"]{50,}">', head)


def test_imagem_de_compartilhamento_tem_1200x630():
    with Image.open(RAIZ / 'static/imagens/og-extreme-team.jpg') as imagem:
        assert imagem.size == (1200, 630)
        assert imagem.format == 'JPEG'


def test_ficha_do_aluno_nao_poe_o_nome_no_titulo(client, logar_como_admin, criar_aluno):
    aluno = criar_aluno(nome='Fulana Sigilosa da Silva')
    logar_como_admin()
    html = client.get(f'/admin/usuario/{aluno.cpf}').get_data(as_text=True)
    titulo = re.search(r'<title>(.*?)</title>', html).group(1)
    assert titulo == 'Ficha do aluno | Extreme Team'


# --- noindex -----------------------------------------------------------------------

def test_area_do_admin_sai_do_indice(client, logar_como_admin):
    logar_como_admin()
    head = _head(client.get('/admin'))
    assert NOINDEX in head
    assert 'canonical' not in head and 'og:title' not in head


def test_area_do_aluno_sai_do_indice(client, logar_como_aluno, criar_aluno):
    logar_como_aluno(criar_aluno())
    resposta = client.get('/perfil')
    assert resposta.status_code == 200
    assert NOINDEX in _head(resposta)


def test_area_do_professor_sai_do_indice(client, logar_como_professor, contexto_app):
    professor = Professor(nome='Professor SEO', login='prof-seo', senha='senha123456')
    db.session.add(professor)
    db.session.commit()
    logar_como_professor(professor)
    resposta = client.get('/professor')
    assert resposta.status_code == 200
    assert NOINDEX in _head(resposta)


@pytest.mark.parametrize('caminho', ['/recuperar_senha/token-secreto-123', '/ativar-acesso/token-secreto-123'])
def test_links_com_token_saem_do_indice_sem_vazar_o_token(client, caminho):
    head = _head(client.get(caminho))
    assert NOINDEX in head
    assert 'token-secreto-123' not in head
    assert 'canonical' not in head and 'og:url' not in head


def test_pagina_de_erro_sai_do_indice(client):
    head = _head(client.get('/nao-existe'))
    assert NOINDEX in head
    assert 'canonical' not in head


def test_pagina_de_erro_sai_do_indice_mesmo_numa_rota_indexavel(app, contexto_app):
    # Um 500 na home desenha erro.html com request.endpoint == 'home'.
    with app.test_request_context('/'):
        html = render_template('erro.html', codigo=500, titulo='Falha', texto='x', acao_href='', acao_texto='')
    assert NOINDEX in html
    assert 'canonical' not in html


# --- JSON-LD da home ---------------------------------------------------------------

def test_json_ld_sem_dados_da_academia_so_tem_o_basico(client):
    [dados] = _json_ld(client.get('/').get_data(as_text=True))
    assert dados['@type'] == 'ExerciseGym'
    assert dados['name'] == 'Centro de Treinamento Extreme Team'
    assert dados['url'] == f'{BASE}/'
    for ausente in ('address', 'telephone', 'email', 'sameAs', 'openingHoursSpecification', 'hasMap'):
        assert ausente not in dados
    _sem_vazios(dados)


def test_json_ld_omite_campos_vazios(client, contexto_app):
    db.session.add(Academia(id=1, instagram='', email=None, whatsapp='', endereco='', complemento='', horarios='  '))
    db.session.commit()
    [dados] = _json_ld(client.get('/').get_data(as_text=True))
    for ausente in ('address', 'telephone', 'email', 'sameAs', 'openingHoursSpecification', 'hasMap'):
        assert ausente not in dados
    _sem_vazios(dados)


def test_json_ld_completo_a_partir_da_academia(client, contexto_app):
    db.session.add(Academia(
        id=1, instagram='extremeteam', email='contato@example.com', whatsapp='5511999998888',
        endereco='Rua das Lutas, 100 - Centro, São Paulo - SP', complemento='Sala 2',
        horarios='Segunda a sexta: 06:00 às 22:00\nSábado: 8h às 12h\nDomingo: fechado',
    ))
    db.session.commit()
    [dados] = _json_ld(client.get('/').get_data(as_text=True))

    assert dados['address'] == {
        '@type': 'PostalAddress',
        'streetAddress': 'Rua das Lutas, 100 - Centro, São Paulo - SP, Sala 2',
        'addressCountry': 'BR',
    }
    assert dados['telephone'] == '+5511999998888'
    assert dados['email'] == 'contato@example.com'
    assert dados['sameAs'] == ['https://www.instagram.com/extremeteam/']
    assert dados['logo'].startswith(f'{BASE}/static/')
    assert [(h['dayOfWeek'], h['opens'], h['closes']) for h in dados['openingHoursSpecification']] == [
        (['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], '06:00', '22:00'),
        (['Saturday'], '08:00', '12:00'),
    ]
    _sem_vazios(dados)


def test_json_ld_nao_deixa_texto_do_painel_fechar_o_script(client, contexto_app):
    db.session.add(Academia(id=1, endereco='</script><script>alert(1)</script>'))
    db.session.commit()
    html = client.get('/').get_data(as_text=True)
    assert '<script>alert(1)' not in html
    [dados] = _json_ld(html)
    assert dados['address']['streetAddress'] == '</script><script>alert(1)</script>'


def test_json_ld_leva_o_nonce_da_csp(client):
    resposta = client.get('/')
    nonce = re.search(r"'nonce-([^']+)'", resposta.headers['Content-Security-Policy']).group(1)
    assert f'<script type="application/ld+json" nonce="{nonce}">' in resposta.get_data(as_text=True)


def test_dados_estruturados_sem_academia(app):
    with app.test_request_context('/'):
        dados = dados_estruturados_academia(None)
    assert set(dados) == {'@context', '@type', 'name', 'url', 'logo', 'image'}


@pytest.mark.parametrize('texto, esperado', [
    ('Seg a Sex 6h às 12h e 15h às 22h', [(5, '06:00', '12:00'), (5, '15:00', '22:00')]),
    ('Sáb e Dom: 9h30 às 13h', [(2, '09:30', '13:00')]),
    ('Segunda-feira até sexta-feira 5h - 24h', [(5, '05:00', '23:59')]),
    ('Domingo: fechado', []),
    ('Feriados: 8h às 12h', []),
    ('Horário combinado com o professor', []),
    ('Seg a Qui 25h às 30h', []),
    ('Sex a Seg 6h às 10h', []),
])
def test_horarios_so_viram_dado_estruturado_quando_reconhecidos(texto, esperado):
    obtido = [(len(h['dayOfWeek']), h['opens'], h['closes']) for h in horarios_estruturados(texto)]
    assert obtido == esperado
