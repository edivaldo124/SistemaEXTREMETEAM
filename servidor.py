from flask import *
from config import csrf, db, limiter, migrate
import os
import secrets
from datetime import timedelta
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFError
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv()

from blueprints.usuario_bp import auth_bp
from blueprints.adm_bp import admin_bp
from blueprints.turma_bp import turma_bp
from blueprints.pix_bp import pix_bp
from blueprints.checkout_bp import checkout_bp
from blueprints.academia_bp import academia_bp
from modelos.academia import Academia
from modelos.professor import Professor

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
if not app.secret_key:
    raise RuntimeError('A variavel de ambiente SECRET_KEY e obrigatoria.')

app.config.update(
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=os.environ.get('COOKIE_SECURE', 'false').lower() == 'true',
    SESSION_REFRESH_EACH_REQUEST=True,
    MAX_CONTENT_LENGTH=10 * 1024 * 1024,
    MAX_FORM_MEMORY_SIZE=512 * 1024,
    MAX_FORM_PARTS=100,
    RATELIMIT_STORAGE_URI=os.environ.get('RATELIMIT_STORAGE_URI', 'memory://'),
)

hosts_confiaveis = [
    host.strip() for host in (os.environ.get('TRUSTED_HOSTS') or '').split(',') if host.strip()
]
if hosts_confiaveis:
    app.config['TRUSTED_HOSTS'] = hosts_confiaveis

try:
    quantidade_proxies = int(os.environ.get('TRUST_PROXY_COUNT', '0'))
except ValueError as exc:
    raise RuntimeError('TRUST_PROXY_COUNT deve ser um número inteiro.') from exc
if quantidade_proxies < 0 or quantidade_proxies > 3:
    raise RuntimeError('TRUST_PROXY_COUNT deve estar entre 0 e 3.')
if quantidade_proxies:
    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=quantidade_proxies,
        x_proto=quantidade_proxies,
        x_host=quantidade_proxies,
    )

database_url = os.environ.get('DATABASE_URL')
if not database_url:
    raise RuntimeError('A variavel de ambiente DATABASE_URL e obrigatoria.')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.before_request
def preparar_nonce_csp():
    g.csp_nonce = secrets.token_urlsafe(18)


app.jinja_env.globals['csp_nonce'] = lambda: getattr(g, 'csp_nonce', '')


db.init_app(app)
migrate.init_app(app, db)
csrf.init_app(app)
limiter.init_app(app)

# Filtros de exibição usados pelos templates (formatação, nunca regra de negócio).
from servicos.formatacao import formatar_moeda, rotulo_forma_pagamento

app.jinja_env.filters['moeda'] = formatar_moeda
app.jinja_env.filters['forma_pagamento'] = rotulo_forma_pagamento

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(turma_bp)
app.register_blueprint(pix_bp)
app.register_blueprint(checkout_bp)
app.register_blueprint(academia_bp)


@app.context_processor
def contatos_da_academia():
    return {'academia': db.session.get(Academia, 1)}


@app.after_request
def adicionar_cabecalhos_de_seguranca(resposta):
    nonce = getattr(g, 'csp_nonce', '')
    resposta.headers.setdefault('X-Content-Type-Options', 'nosniff')
    resposta.headers.setdefault('X-Frame-Options', 'SAMEORIGIN')
    resposta.headers.setdefault('Referrer-Policy', 'same-origin')
    resposta.headers.setdefault('Permissions-Policy', 'camera=(), microphone=(), geolocation=()')
    resposta.headers.setdefault(
        'Content-Security-Policy',
        "default-src 'self'; "
        f"script-src 'self' 'nonce-{nonce}'; "
        "script-src-attr 'none'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data:; connect-src 'self'; object-src 'none'; "
        "base-uri 'self'; form-action 'self'; frame-ancestors 'self'",
    )
    return resposta


@app.errorhandler(CSRFError)
def erro_csrf(_erro):
    mensagem = 'Sua sessão de segurança expirou. Atualize a página e tente novamente.'
    if request.path.startswith('/api/'):
        return {'erro': mensagem}, 400
    return mensagem, 400


@app.errorhandler(413)
def requisicao_muito_grande(_erro):
    mensagem = 'O arquivo ou formulário enviado excede o limite permitido.'
    if request.path.startswith('/api/'):
        return {'erro': mensagem}, 413
    return mensagem, 413


@app.errorhandler(429)
def tentativas_demais(_erro):
    mensagem = 'Muitas tentativas. Aguarde alguns minutos e tente novamente.'
    if request.path.startswith('/api/'):
        return {'erro': mensagem}, 429
    return render_template('login.html', msg=mensagem), 429

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    professores = Professor.query.filter_by(perfil_publico=True).order_by(Professor.nome).all()
    return render_template("index.html", professores_publicos=professores)


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/logout", methods=['POST'])
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4001)
