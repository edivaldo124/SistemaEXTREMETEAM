"""E-mails: base com a logo oficial e componentes seguros para cliente de e-mail
(templates/email/componentes.html) — só tabela e estilo inline."""

import re

from flask import render_template, render_template_string


def _render(app, **extra):
    dados = dict(titulo='Mensalidade confirmada', paragrafos=['Olá, Marina.'], link_url='https://x.test/perfil',
                 link_texto='Abrir minha área')
    dados.update(extra)
    with app.test_request_context('/'):
        return render_template('email/base.html', **dados)


def _sem_recursos_externos(html):
    assert '<script' not in html
    assert '<link' not in html
    assert '<style' not in html
    assert 'var(--' not in html
    assert 'class="' not in html  # clientes de e-mail descartam classes sem folha de estilo


def test_base_usa_a_logo_quando_ha_url_publica(app):
    html = _render(app, logo_url='https://academia.example.test/static/imagens/logo-horizontal-400.png')
    assert 'src="https://academia.example.test/static/imagens/logo-horizontal-400.png"' in html
    assert 'alt="Extreme Team"' in html
    assert 'EXTREME TEAM' not in html
    _sem_recursos_externos(html)


def test_base_sem_url_publica_cai_para_o_nome_em_texto(app):
    html = _render(app, logo_url=None)
    assert '<img' not in html
    assert 'EXTREME TEAM' in html


def test_botao_do_email_usa_o_ouro_do_sistema(app):
    html = _render(app)
    assert 'href="https://x.test/perfil"' in html
    assert 'Abrir minha área' in html
    assert '#F5B914' in html and '#FDCF17' not in html


def test_cartao_de_resumo_com_badge(app):
    resumo = {
        'titulo': 'Mensalidade de outubro', 'estado': 'pago', 'rotulo_estado': 'Paga',
        'linhas': [('Plano', 'Trimestral'), ('Valor', 'R$ 320,00'), ('Vencimento', '04/10/2026')],
    }
    html = _render(app, resumo=resumo)
    assert 'Mensalidade de outubro' in html
    assert 'R$ 320,00' in html and '04/10/2026' in html
    assert 'Paga' in html and '#DFEEE7' in html  # par fundo/tinta de "pago"
    _sem_recursos_externos(html)


def test_badge_de_estado_desconhecido_usa_o_neutro(app):
    with app.test_request_context('/'):
        html = render_template_string(
            '{% from "email/componentes.html" import badge %}{{ badge("qualquer", "Outro") }}',
        )
    assert 'Outro' in html and '#E4E2DC' in html


def test_enviar_email_monta_a_logo_com_a_url_publica(app, monkeypatch):
    from servicos import email as servico_email

    enviados = {}
    monkeypatch.setattr(servico_email.gmail_conta, 'estado', lambda: {'conectada': True})
    monkeypatch.setattr(servico_email.gmail_conta, 'enviar',
                        lambda dest, nome, assunto, corpo: enviados.update(corpo=corpo))
    with app.test_request_context('/'):
        assert servico_email.enviar_email('a@b.com', 'A', 'Assunto', 'Título', ['Texto']) is True
    assert re.search(r'src="https://academia\.example\.test/static/imagens/logo-horizontal-400\.png[^"]*"',
                     enviados['corpo'])
