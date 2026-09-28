from flask import Blueprint, Response

from servicos import seo

seo_bp = Blueprint('seo', __name__)

# Uma hora de cache: os dois arquivos só mudam com deploy (ou com APP_BASE_URL).
CACHE_PUBLICO = 'public, max-age=3600'


@seo_bp.route('/robots.txt')
def robots():
    resposta = Response(seo.conteudo_robots(), mimetype='text/plain')
    resposta.headers['Cache-Control'] = CACHE_PUBLICO
    return resposta


@seo_bp.route('/sitemap.xml')
def sitemap():
    resposta = Response(seo.conteudo_sitemap(), mimetype='application/xml')
    resposta.headers['Cache-Control'] = CACHE_PUBLICO
    return resposta
