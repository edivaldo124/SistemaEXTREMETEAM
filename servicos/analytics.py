"""Google Analytics 4 opcional, só em página pública e só com consentimento.

Sem `ANALYTICS_ID` nada é carregado nem liberado na CSP. Com ela, as páginas públicas
indexáveis (e a de obrigado do cadastro) mostram o aviso de cookies; o gtag.js só é
baixado depois que a pessoa aceita (static/js/analytics.js). Área autenticada, link com
token e página de erro nunca carregam nada, nem para visitante.
"""

import os
import re

from flask import request, session

from servicos.seo import ENDPOINTS_SITEMAP

# ID de medição do GA4: "G-" seguido de letras maiúsculas e dígitos.
FORMATO_ID = re.compile(r'G-[A-Z0-9]{4,20}')
ENDPOINTS_COM_ANALYTICS = ENDPOINTS_SITEMAP + ('auth.cadastro_obrigado',)
EVENTO_CONVERSAO_CADASTRO = 'sign_up'
# Chave de uso único na sessão: o evento sai uma vez, no primeiro GET do obrigado.
CHAVE_CONVERSAO = 'analytics_conversao_cadastro'

# Domínios do GA4 segundo o guia de CSP do Google Analytics. Só entram na política da
# resposta que de fato pode carregar o script.
CSP_SCRIPT = 'https://*.googletagmanager.com'
CSP_IMG = 'https://*.google-analytics.com https://*.googletagmanager.com'
CSP_CONNECT = (
    'https://*.google-analytics.com https://*.analytics.google.com '
    'https://*.googletagmanager.com'
)


def validar_configuracao():
    """Chamada no arranque: um ID malformado derruba a subida, como as demais variáveis."""
    valor = (os.environ.get('ANALYTICS_ID') or '').strip()
    if valor and not FORMATO_ID.fullmatch(valor):
        raise RuntimeError('ANALYTICS_ID deve ser o ID de medição do GA4 (ex.: G-ABC123XYZ9) ou ficar vazia.')


def id_analytics():
    valor = (os.environ.get('ANALYTICS_ID') or '').strip()
    return valor if FORMATO_ID.fullmatch(valor) else None


def analytics_ativo():
    """Esta resposta pode carregar o GA4? Visitante, página pública indexável ou obrigado."""
    return bool(
        id_analytics()
        and not session.get('tipo_usuario')
        and request.endpoint in ENDPOINTS_COM_ANALYTICS
    )


def marcar_conversao_cadastro():
    # Só com o GA4 ligado: sem ele, o visitante não ganha cookie de sessão à toa.
    if id_analytics():
        session[CHAVE_CONVERSAO] = True


def consumir_conversao_cadastro():
    return bool(session.pop(CHAVE_CONVERSAO, False))
