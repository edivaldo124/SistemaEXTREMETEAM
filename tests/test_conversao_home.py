"""Conversão na home: perguntas frequentes, cadastro no hero e página de obrigado."""

import json
import re

from config import db
from modelos.academia import Academia
from servicos.conteudo_home import PERGUNTAS_FREQUENTES, TEMPO_RESPOSTA_WHATSAPP

DADOS_CADASTRO = {
    'nomeusuario': 'Visitante Convertido', 'loginusuario': 'visitante-conv',
    'dataNascimento': '1995-03-10', 'cpfusuario': '529.982.247-25',
    'senhausuario': 'Treino-Forte-2026', 'confirmarsenhausuario': 'Treino-Forte-2026',
    'emailusuario': 'visitante.conv@example.com', 'telefoneusuario': '11988887777',
    'descricaousuario': '', 'aceite_termos_responsabilidade': 'aceito',
}


def _html(client, caminho='/'):
    return client.get(caminho).get_data(as_text=True)


def _body_tag(html):
    return re.search(r'<body[^>]*>', html).group(0)


# --- Perguntas frequentes ----------------------------------------------------------

def test_home_mostra_as_perguntas_frequentes_em_details(client):
    html = _html(client)
    secao = html.split('id="duvidas"', 1)[1].split('</section>', 1)[0]
    assert secao.count('<details class="et-acordeao"') == len(PERGUNTAS_FREQUENTES) >= 5
    assert secao.count('<summary>') == len(PERGUNTAS_FREQUENTES)
    for item in PERGUNTAS_FREQUENTES:
        assert item['pergunta'] in secao


def test_json_ld_faq_repete_exatamente_as_perguntas_da_pagina(client):
    html = _html(client)
    blocos = [json.loads(b) for b in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S)]
    [faq] = [b for b in blocos if b['@type'] == 'FAQPage']
    assert [(q['name'], q['acceptedAnswer']['text']) for q in faq['mainEntity']] == [
        (item['pergunta'], item['resposta']) for item in PERGUNTAS_FREQUENTES
    ]


def test_tempo_de_resposta_so_aparece_com_whatsapp(client, contexto_app):
    assert 'Chame no WhatsApp' not in _html(client)

    db.session.add(Academia(id=1, whatsapp='5511999998888'))
    db.session.commit()
    html = _html(client)
    assert 'Chame no WhatsApp' in html
    assert f'respondemos {TEMPO_RESPOSTA_WHATSAPP}' in html


# --- Cadastro no hero ---------------------------------------------------------------

# A barra fixa de cadastro no pé do celular saiu em 23/10/2026: ela acompanhava a rolagem e
# cobria o conteúdo. O cadastro fica no próprio hero, para todo mundo e em qualquer largura.
def test_home_nao_tem_barra_fixa_de_cadastro(client):
    html = _html(client)
    assert 'et-cta-fixo' not in html
    assert 'has-cta-fixo' not in _body_tag(html)


def test_cadastro_fica_no_hero(client):
    html = _html(client)
    hero = html.split('class="cinema-rodape"', 1)[1].split('class="cinema-medidor"', 1)[0]
    assert re.search(r'<a class="[^"]*cinema-cadastro[^"]*" href="/cadastrar">Criar minha conta</a>', hero)


def test_whatsapp_da_academia_segue_na_home_sem_a_barra(client, contexto_app):
    db.session.add(Academia(id=1, whatsapp='5511999998888'))
    db.session.commit()
    assert 'href="https://wa.me/5511999998888"' in _html(client)


# --- Página de obrigado (PRG) ------------------------------------------------------

def test_cadastro_com_sucesso_redireciona_para_o_obrigado(client, sem_email):
    resposta = client.post('/cadastrar', data=DADOS_CADASTRO)
    assert resposta.status_code == 302
    assert resposta.location == '/cadastro/obrigado'


def test_pagina_de_obrigado_nao_expoe_dados_do_cadastro(client, sem_email):
    resposta = client.post('/cadastrar', data=DADOS_CADASTRO, follow_redirects=True)
    assert resposta.status_code == 200
    assert resposta.request.path == '/cadastro/obrigado'
    html = resposta.get_data(as_text=True)
    assert 'Recebemos sua solicitação' in html
    for valor in ('Visitante', 'visitante-conv', 'visitante.conv@example.com', '529.982.247-25', '52998224725', '11988887777'):
        assert valor not in html, valor


def test_pagina_de_obrigado_explica_os_proximos_passos_e_sai_do_indice(client, contexto_app):
    db.session.add(Academia(id=1, whatsapp='5511999998888', email='contato@example.com'))
    db.session.commit()
    html = _html(client, '/cadastro/obrigado')
    for trecho in ('Confira seu e-mail', 'Análise da administração', 'Primeiro acesso', 'href="/login"', 'wa.me/5511999998888'):
        assert trecho in html, trecho
    assert '<meta name="robots" content="noindex, nofollow">' in html
    assert 'rel="canonical"' not in html


def test_erro_de_validacao_continua_no_formulario(client):
    dados = dict(DADOS_CADASTRO, cpfusuario='529.982.247-26')
    resposta = client.post('/cadastrar', data=dados)
    assert resposta.status_code == 200
    assert 'CPF válido' in resposta.get_data(as_text=True)
