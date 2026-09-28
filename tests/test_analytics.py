"""GA4 opcional (servicos/analytics.py): nada sem ANALYTICS_ID, nunca em área logada.

O comportamento do navegador (nada antes do "Aceitar", endereço sem query string) está
em tests/js/analytics.test.cjs.
"""

import re

import pytest

from config import db
from modelos.professor import Professor
from servicos import analytics

ID = 'G-TESTE12345'
PUBLICAS = [
    '/', '/cadastrar', '/login', '/recuperar_senha',
    '/termos-de-servico', '/politica-privacidade', '/termos-de-responsabilidade', '/cadastro/obrigado',
]
DADOS_CADASTRO = {
    'nomeusuario': 'Pessoa Medida', 'loginusuario': 'pessoa-medida', 'dataNascimento': '1998-07-01',
    'cpfusuario': '529.982.247-25', 'senhausuario': 'Treino-Forte-2026',
    'confirmarsenhausuario': 'Treino-Forte-2026', 'emailusuario': 'medida@example.com',
    'telefoneusuario': '11977776666', 'descricaousuario': '', 'aceite_termos_responsabilidade': 'aceito',
}


@pytest.fixture
def com_analytics(monkeypatch):
    monkeypatch.setenv('ANALYTICS_ID', ID)


@pytest.fixture(autouse=True)
def sem_analytics_por_padrao(monkeypatch):
    # O .env de quem roda a suíte pode ter um ID de verdade.
    monkeypatch.delenv('ANALYTICS_ID', raising=False)


def _carrega_analytics(resposta):
    html = resposta.get_data(as_text=True)
    return 'js/analytics.js' in html or 'data-consentimento' in html or 'googletagmanager' in html


def _csp_com_google(resposta):
    # As fontes do Google (fonts.googleapis.com) já estão na política base; aqui só o GA4.
    csp = resposta.headers['Content-Security-Policy']
    return any(dominio in csp for dominio in ('googletagmanager', 'google-analytics', 'analytics.google'))


# --- Desligado sem ANALYTICS_ID ----------------------------------------------------

@pytest.mark.parametrize('caminho', PUBLICAS)
def test_sem_analytics_id_nada_e_carregado(client, caminho):
    resposta = client.get(caminho)
    assert resposta.status_code == 200
    assert not _carrega_analytics(resposta)
    assert not _csp_com_google(resposta)


def test_sem_analytics_id_o_cadastro_nao_marca_conversao(client, sem_email):
    client.post('/cadastrar', data=DADOS_CADASTRO)
    with client.session_transaction() as sess:
        assert analytics.CHAVE_CONVERSAO not in sess


# --- Ligado: só em página pública para visitante -----------------------------------

@pytest.mark.parametrize('caminho', PUBLICAS)
def test_com_analytics_id_paginas_publicas_carregam_com_nonce(client, com_analytics, caminho):
    resposta = client.get(caminho)
    html = resposta.get_data(as_text=True)
    csp = resposta.headers['Content-Security-Policy']
    nonce = re.search(r"'nonce-([^']+)'", csp).group(1)

    tag = re.search(r'<script src="/static/js/analytics\.js"[^>]*>', html).group(0)
    assert f'nonce="{nonce}"' in tag
    assert f'data-analytics-id="{ID}"' in tag
    # O aviso nasce escondido e o gtag.js nunca vem no HTML: só o JS o baixa após o aceite.
    assert re.search(r'<section class="et-consentimento" data-consentimento[^>]*hidden>', html)
    assert 'googletagmanager.com/gtag/js' not in html

    assert "script-src 'self' 'nonce-" in csp and analytics.CSP_SCRIPT in csp
    assert 'https://*.google-analytics.com' in csp.split('connect-src', 1)[1].split(';', 1)[0]
    assert 'https://*.google-analytics.com' in csp.split('img-src', 1)[1].split(';', 1)[0]


@pytest.mark.parametrize('caminho', [
    '/recuperar_senha/token-secreto', '/ativar-acesso/token-secreto', '/nao-existe',
    '/robots.txt', '/sitemap.xml', '/health',
])
def test_com_analytics_id_links_com_token_erro_e_rotas_tecnicas_ficam_de_fora(client, com_analytics, caminho):
    resposta = client.get(caminho)
    assert not _carrega_analytics(resposta)
    assert not _csp_com_google(resposta)


def test_nunca_em_area_do_aluno(client, com_analytics, logar_como_aluno, criar_aluno):
    logar_como_aluno(criar_aluno())
    for caminho in ('/perfil', '/'):
        resposta = client.get(caminho)
        assert resposta.status_code == 200, caminho
        assert not _carrega_analytics(resposta), caminho
        assert not _csp_com_google(resposta), caminho


def test_nunca_em_area_do_admin(client, com_analytics, logar_como_admin):
    logar_como_admin()
    for caminho in ('/admin', '/admin/financeiro', '/admin/academia', '/politica-privacidade'):
        resposta = client.get(caminho)
        assert resposta.status_code == 200, caminho
        assert not _carrega_analytics(resposta), caminho
        assert not _csp_com_google(resposta), caminho


def test_nunca_em_area_do_professor(client, com_analytics, logar_como_professor, contexto_app):
    professor = Professor(nome='Professor GA', login='prof-ga', senha='senha123456')
    db.session.add(professor)
    db.session.commit()
    logar_como_professor(professor)
    resposta = client.get('/professor')
    assert resposta.status_code == 200
    assert not _carrega_analytics(resposta)
    assert not _csp_com_google(resposta)


def test_rodape_e_politica_oferecem_rever_a_escolha(client, com_analytics):
    assert 'data-consentimento-abrir' in client.get('/').get_data(as_text=True)
    politica = client.get('/politica-privacidade').get_data(as_text=True)
    assert 'data-consentimento-abrir' in politica


def test_politica_de_privacidade_explica_a_coleta(client):
    html = client.get('/politica-privacidade').get_data(as_text=True)
    assert 'id="secao-7"' in html
    assert 'Google Analytics' in html
    assert 'consentimento' in html


# --- Evento de conversão -----------------------------------------------------------

def _evento(resposta):
    return re.search(r'data-evento="([^"]*)"', resposta.get_data(as_text=True)).group(1)


def test_conversao_sai_uma_vez_no_obrigado_depois_do_cadastro(client, com_analytics, sem_email):
    resposta = client.post('/cadastrar', data=DADOS_CADASTRO, follow_redirects=True)
    assert resposta.request.path == '/cadastro/obrigado'
    assert _evento(resposta) == 'sign_up'
    # Recarregar não conta de novo.
    assert _evento(client.get('/cadastro/obrigado')) == ''


def test_obrigado_aberto_direto_nao_conta_conversao(client, com_analytics):
    assert _evento(client.get('/cadastro/obrigado')) == ''


def test_conversao_nao_leva_dado_do_cadastro(client, com_analytics, sem_email):
    html = client.post('/cadastrar', data=DADOS_CADASTRO, follow_redirects=True).get_data(as_text=True)
    tag = re.search(r'<script src="/static/js/analytics\.js"[^>]*>', html).group(0)
    for valor in ('Pessoa', 'pessoa-medida', 'medida@example.com', '529', '11977776666'):
        assert valor not in tag


def test_conversao_igual_para_cadastro_novo_e_cpf_ou_email_existentes(client, com_analytics, criar_aluno, sem_email):
    existente = criar_aluno(cpf='111.444.777-35', email='existente@example.com', login='existente')
    tentativas = [
        DADOS_CADASTRO,
        dict(DADOS_CADASTRO, cpfusuario=existente.cpf, loginusuario='outro-1', emailusuario='a@example.com'),
        dict(DADOS_CADASTRO, cpfusuario='390.533.447-05', loginusuario='outro-2', emailusuario=existente.email),
    ]
    for dados in tentativas:
        resposta = client.post('/cadastrar', data=dados)
        assert resposta.status_code == 302
        with client.session_transaction() as sess:
            assert sess.pop(analytics.CHAVE_CONVERSAO) is True


# --- Configuração ------------------------------------------------------------------

@pytest.mark.parametrize('valor', ['UA-12345-1', 'G-abc', 'G-TESTE"><script>', 'GTM-ABC1234'])
def test_id_malformado_derruba_o_arranque_e_nao_e_usado(monkeypatch, valor):
    monkeypatch.setenv('ANALYTICS_ID', valor)
    with pytest.raises(RuntimeError, match='ANALYTICS_ID'):
        analytics.validar_configuracao()
    assert analytics.id_analytics() is None


@pytest.mark.parametrize('valor', ['', '  ', ID])
def test_id_vazio_ou_valido_passa_no_arranque(monkeypatch, valor):
    monkeypatch.setenv('ANALYTICS_ID', valor)
    analytics.validar_configuracao()


def test_id_malformado_em_execucao_nao_carrega_nada(client, monkeypatch):
    monkeypatch.setenv('ANALYTICS_ID', 'G-TESTE"><script>')
    resposta = client.get('/')
    assert not _carrega_analytics(resposta)
    assert not _csp_com_google(resposta)
