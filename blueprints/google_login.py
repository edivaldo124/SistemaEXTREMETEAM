import secrets
import os
import requests
import logging
from urllib.parse import urlencode
from flask import Blueprint, redirect, url_for, request, session, flash, render_template
from config import db, limiter
from modelos.usuario import Aluno
from servicos.mercado_pago import ConfiguracaoInvalida, base_url_publica
from servicos.autorizacao import iniciar_sessao, registrar_credencial

logger = logging.getLogger(__name__)

google_auth_bp = Blueprint('google_auth', __name__)

AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN_URL = 'https://oauth2.googleapis.com/token'
USERINFO_URL = 'https://openidconnect.googleapis.com/v1/userinfo'
CALLBACK_ROUTE = '/login/google/callback'

def redirect_uri():
    # Precisa estar cadastrado, igual, em "URIs de redirecionamento autorizados" do
    # cliente OAuth do GMAIL_CLIENT_ID (o mesmo cliente do Gmail, que usa outro caminho).
    return f'{base_url_publica()}{CALLBACK_ROUTE}'

@google_auth_bp.route('/login/google')
@limiter.limit('10 per 15 minutes')
def login_google():
    client_id = os.environ.get('GMAIL_CLIENT_ID')
    if not client_id:
        flash('O Login com Google não está configurado no servidor.', 'erro')
        return redirect(url_for('auth.pagina_login'))
        
    try:
        retorno = redirect_uri()
    except ConfiguracaoInvalida:
        logger.error('APP_BASE_URL inválida; o login com Google não tem para onde voltar.')
        flash('O Login com Google não está configurado no servidor.', 'erro')
        return redirect(url_for('auth.pagina_login'))

    state = secrets.token_urlsafe(32)
    session['google_oauth_state'] = state
    
    url = AUTH_URL + '?' + urlencode({
        'client_id': client_id,
        'redirect_uri': retorno,
        'response_type': 'code',
        'scope': 'openid email profile',
        'access_type': 'online',
        'prompt': 'select_account',
        'state': state,
    })
    return redirect(url)

@google_auth_bp.route(CALLBACK_ROUTE)
@limiter.limit('10 per 15 minutes')
def callback():
    state_guardado = session.pop('google_oauth_state', None)
    state_recebido = request.args.get('state')
    
    if not state_guardado or state_guardado != state_recebido:
        flash('Falha na validação de segurança do Google. Tente novamente.', 'erro')
        return redirect(url_for('auth.pagina_login'))
        
    if request.args.get('error'):
        flash('O login com Google foi cancelado.', 'erro')
        return redirect(url_for('auth.pagina_login'))
        
    code = request.args.get('code')
    if not code:
        return redirect(url_for('auth.pagina_login'))
        
    try:
        resposta = requests.post(TOKEN_URL, data={
            'code': code,
            'client_id': os.environ.get('GMAIL_CLIENT_ID'),
            'client_secret': os.environ.get('GMAIL_CLIENT_SECRET'),
            'redirect_uri': redirect_uri(),
            'grant_type': 'authorization_code',
        }, timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()
        
        perfil = requests.get(USERINFO_URL, headers={
            'Authorization': f"Bearer {dados['access_token']}"
        }, timeout=10)
        perfil.raise_for_status()
        info = perfil.json()
    except Exception:
        logger.exception('Falha ao autenticar usuário via Google OAuth.')
        flash('Não foi possível se conectar com o Google. Tente novamente.', 'erro')
        return redirect(url_for('auth.pagina_login'))
        
    email = info.get('email')

    # O e-mail é a única ligação com a conta do aluno: sem a confirmação do Google,
    # qualquer conta com esse endereço digitado entraria no lugar dele.
    if not email or info.get('email_verified') is not True:
        flash('O Google não forneceu um e-mail válido.', 'erro')
        return redirect(url_for('auth.pagina_login'))
        
    email_lower = email.strip().lower()
    aluno = Aluno.query.filter_by(email=email_lower).first()

    # O Google só serve para entrar: a conta nasce pelo formulário de cadastro.
    if not aluno:
        flash('Não há conta com este e-mail do Google. Crie sua conta pelo cadastro e depois entre com o Google.', 'erro')
        return redirect(url_for('auth.pagina_login'))

    if aluno.status_cadastro == 'pendente':
        # Como autenticou no google, marcamos o email como verificado caso não esteja
        if not aluno.email_verificado:
            aluno.email_verificado = True
            db.session.commit()
        return render_template('login.html', msg='Seu cadastro ainda está em análise pela administração.')

    if aluno.status_cadastro == 'recusado':
        return render_template('login.html', msg='Seu cadastro não foi aprovado. Fale com a administração.')

    if not aluno.ativo:
        return render_template('login.html', msg='Sua conta está desativada. Fale com a administração.')

    session.clear()
    iniciar_sessao()
    session['usuario'] = aluno.login
    session['aluno_id'] = aluno.id
    session['tipo_usuario'] = "aluno"
    registrar_credencial(aluno.senha_hash or 'google_oauth')
    session.permanent = True
    return redirect('/perfil')
