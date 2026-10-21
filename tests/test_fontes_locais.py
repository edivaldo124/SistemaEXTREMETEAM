"""Fontes servidas pelo próprio site (SEC-18).

Com o Google Fonts, o navegador de todo visitante mandava o IP ao Google já na página
inicial, antes de qualquer consentimento. Agora a CSP só aceita fonte deste domínio e
os arquivos ficam em static/fonts, com a licença OFL ao lado.
"""

import re
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
CSS_FONTES = RAIZ / 'static' / 'css' / 'fontes.css'


@pytest.mark.parametrize('caminho', ['/', '/login', '/cadastrar', '/termos-de-servico'])
def test_csp_nao_libera_o_google_fonts(client, caminho):
    csp = client.get(caminho).headers['Content-Security-Policy']
    assert 'fonts.googleapis.com' not in csp
    assert 'fonts.gstatic.com' not in csp
    assert "font-src 'self';" in csp


def test_nenhuma_folha_importa_fonte_de_fora():
    for folha in (RAIZ / 'static' / 'css').glob('*.css'):
        conteudo = folha.read_text(encoding='utf-8')
        assert 'fonts.googleapis.com' not in conteudo, folha.name
        assert 'fonts.gstatic.com' not in conteudo, folha.name
    assert "@import url('fontes.css');" in (RAIZ / 'static' / 'css' / 'theme.css').read_text(encoding='utf-8')


def test_cada_fonte_declarada_existe_e_tem_licenca():
    arquivos = re.findall(r'url\("\.\./fonts/([^"]+)"\)', CSS_FONTES.read_text(encoding='utf-8'))
    assert len(arquivos) == 10
    for arquivo in arquivos:
        assert (RAIZ / 'static' / 'fonts' / arquivo).is_file(), arquivo
    for familia in ('inter', 'bebas-neue'):
        licenca = (RAIZ / 'static' / 'fonts' / f'LICENCA-{familia}.txt').read_text(encoding='utf-8')
        assert 'SIL OPEN FONT LICENSE' in licenca.upper()


def test_pesos_usados_pelo_sistema_estao_declarados():
    css = CSS_FONTES.read_text(encoding='utf-8')
    declarados = set(re.findall(r'font-family: "([^"]+)";\s+font-style: normal;\s+font-weight: (\d+);', css))
    esperados = {('Bebas Neue', '400')} | {('Inter', peso) for peso in ('400', '500', '600', '700')}
    assert esperados <= declarados


def test_as_duas_fontes_de_toda_tela_sao_pedidas_no_head(client):
    html = client.get('/login').get_data(as_text=True)
    cabeca = html.split('</head>', 1)[0]
    for arquivo in ('inter-latin-400-normal.woff2', 'bebas-neue-latin-400-normal.woff2'):
        assert re.search(rf'<link rel="preload" href="/static/fonts/{arquivo}" as="font" type="font/woff2" crossorigin>', cabeca)
