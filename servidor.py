from flask import *
from config import csrf, db, limiter, migrate
import os
import secrets
import ipaddress
from datetime import timedelta
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFError
from werkzeug.exceptions import TooManyRequests
from werkzeug.middleware.proxy_fix import ProxyFix
from urllib.parse import urlsplit

load_dotenv()

from blueprints.usuario_bp import auth_bp
from blueprints.adm_bp import admin_bp
from blueprints.turma_bp import turma_bp
from blueprints.pix_bp import pix_bp
from blueprints.checkout_bp import checkout_bp
from blueprints.academia_bp import academia_bp
from blueprints.mercado_pago_oauth_bp import mercado_pago_oauth_bp
from blueprints.gmail_oauth_bp import gmail_oauth_bp
from modelos.academia import Academia
from modelos.email_pendente import EmailPendente
from modelos.professor import Professor
from modelos.sessao_revogada import SessaoRevogada  # noqa: F401  (registra a tabela no metadata)
from modelos.gmail_conexao import GmailConexao  # noqa: F401
from servicos import credenciais, fila_email, keep_alive
from servicos.autorizacao import revogar_sessao_atual

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
if not app.secret_key:
    raise RuntimeError('A variavel de ambiente SECRET_KEY e obrigatoria.')

valor_cookie_secure = (os.environ.get('COOKIE_SECURE') or '').strip().lower()
if not valor_cookie_secure:
    cookie_secure = True
elif valor_cookie_secure == 'true':
    cookie_secure = True
elif valor_cookie_secure == 'false':
    cookie_secure = False
else:
    raise RuntimeError('COOKIE_SECURE deve ser true ou false.')

app_base_url = (os.environ.get('APP_BASE_URL') or '').strip()
url_base_publica = urlsplit(app_base_url)
if not cookie_secure and url_base_publica.scheme.lower() == 'https':
    raise RuntimeError('COOKIE_SECURE=false não é permitido quando APP_BASE_URL usa HTTPS.')

hostname_base_publica = url_base_publica.hostname
try:
    base_publica_em_loopback = bool(hostname_base_publica) and ipaddress.ip_address(
        hostname_base_publica
    ).is_loopback
except ValueError:
    base_publica_em_loopback = False
enviar_hsts = (
    url_base_publica.scheme.lower() == 'https'
    and hostname_base_publica not in (None, 'localhost')
    and not base_publica_em_loopback
)

app.config.update(
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=cookie_secure,
    SESSION_REFRESH_EACH_REQUEST=True,
    MAX_CONTENT_LENGTH=10 * 1024 * 1024,
    MAX_FORM_MEMORY_SIZE=512 * 1024,
    MAX_FORM_PARTS=100,
    RATELIMIT_STORAGE_URI=os.environ.get('RATELIMIT_STORAGE_URI', 'memory://'),
)

hosts_confiaveis = [
    host.strip() for host in (os.environ.get('TRUSTED_HOSTS') or '').split(',') if host.strip()
]
if not hosts_confiaveis:
    raise RuntimeError(
        'TRUSTED_HOSTS é obrigatória. Use localhost,127.0.0.1 em desenvolvimento ou '
        'o domínio real em produção.'
    )
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

# Sem a credencial administrativa baseada em hash, a academia fica sem acesso; falhar
# no arranque é mais seguro do que descobrir isso na tela de login.
if not credenciais.admin_configurado():
    raise RuntimeError(
        'Defina ADMIN_USER e ADMIN_PASSWORD_HASH (gere com '
        '"python -m servicos.credenciais").'
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
app.register_blueprint(mercado_pago_oauth_bp)
app.register_blueprint(gmail_oauth_bp)


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
    if enviar_hsts:
        resposta.headers.setdefault('Strict-Transport-Security', 'max-age=31536000')
    # Página de quem está autenticado (CPF, financeiro, fichas) nunca vai para o cache nem
    # para o bfcache do navegador: depois do logout o botão "Voltar" não a reexibe. Quem
    # já definiu a própria política (as fotos, `private, no-store`) é preservado.
    if request.endpoint != 'static' and session.get('tipo_usuario'):
        resposta.headers.setdefault('Cache-Control', 'no-store')
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
    pagamento = request.blueprint in ('pix', 'checkout')
    quer_json = request.accept_mimetypes.best_match(('text/html', 'application/json')) == 'application/json'
    if request.path.startswith('/api/') or (pagamento and quer_json):
        return {'erro': mensagem}, 429, {'Retry-After': '60'}

    # A tela de login só faz sentido para quem ainda não entrou. Trocar a senha, o
    # e-mail ou a foto são ações de quem JÁ está autenticado: devolver o formulário de
    # login ali parecia que a sessão tinha caído. E nenhuma resposta expõe a chave
    # interna nem os detalhes do limite.
    if pagamento or session.get('tipo_usuario'):
        resposta = TooManyRequests(description=mensagem).get_response()
        resposta.headers['Retry-After'] = '60'
        return resposta
    return render_template('login.html', msg=mensagem), 429

# O schema é responsabilidade das migrations (`flask db upgrade`, executado pelo
# Dockerfile antes do Gunicorn), nunca da importação do módulo.
#
# `db.create_all()` rodava aqui a cada import - inclusive no import que o PRÓPRIO
# `flask db upgrade` faz. Num banco vazio ele criava as tabelas já no formato atual e
# a primeira migration então tentava adicionar colunas que acabavam de existir, com
# "column ... already exists" no PostgreSQL: um banco novo simplesmente não subia.
#
# Em teste, onde cada processo usa um SQLite descartável e não há migrations a aplicar,
# criar o schema direto do modelo continua sendo o caminho.
if os.environ.get('CRIAR_SCHEMA_NA_IMPORTACAO', '').lower() == 'true':
    with app.app_context():
        db.create_all()

fila_email.registrar_app(app)


@app.route("/")
def home():
    professores = Professor.query.filter_by(perfil_publico=True).order_by(Professor.nome).all()
    return render_template("index.html", professores_publicos=professores)


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/logout", methods=['POST'])
def logout():
    # Só limpar o cookie do navegador não encerra nada: o cookie é assinado e sem estado,
    # e uma cópia dele continuaria aceita. Revoga-se o identificador da sessão no banco.
    revogar_sessao_atual()
    session.clear()
    return redirect('/')


# Inicia somente quando KEEP_ALIVE estiver habilitado no ambiente.
keep_alive.iniciar()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4001)
