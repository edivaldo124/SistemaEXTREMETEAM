import secrets
import os
import requests
import logging
from urllib.parse import urlencode
from flask import Blueprint, redirect, url_for, request, session, flash, render_template
from config import db, limiter
from modelos.usuario import Aluno
from dao.usuarioDAO import AlunoDAO
from servicos.mercado_pago import base_url_publica
from servicos.autorizacao import iniciar_sessao, registrar_credencial

logger = logging.getLogger(__name__)

google_auth_bp = Blueprint('google_auth', __name__)

AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN_URL = 'https://oauth2.googleapis.com/token'
USERINFO_URL = 'https://openidconnect.googleapis.com/v1/userinfo'
CALLBACK_ROUTE = '/login/google/callback'

def redirect_uri():
    return f'{base_url_publica()}{CALLBACK_ROUTE}'

@google_auth_bp.route('/login/google')
@limiter.limit('10 per 15 minutes')
def login_google():
    client_id = os.environ.get('GMAIL_CLIENT_ID')
    if not client_id:
        flash('O Login com Google não está configurado no servidor.', 'erro')
        return redirect(url_for('auth.login'))
        
    state = secrets.token_urlsafe(32)
    session['google_oauth_state'] = state
    
    url = AUTH_URL + '?' + urlencode({
        'client_id': client_id,
        'redirect_uri': redirect_uri(),
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
        return redirect(url_for('auth.login'))
        
    if request.args.get('error'):
        flash('O login com Google foi cancelado.', 'erro')
        return redirect(url_for('auth.login'))
        
    code = request.args.get('code')
    if not code:
        return redirect(url_for('auth.login'))
        
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
    except Exception as e:
        logger.exception('Falha ao autenticar usuário via Google OAuth.')
        flash('Não foi possível se conectar com o Google. Tente novamente.', 'erro')
        return redirect(url_for('auth.login'))
        
    email = info.get('email')
    nome = info.get('name')
    
    if not email:
        flash('O Google não forneceu um e-mail válido.', 'erro')
        return redirect(url_for('auth.login'))
        
    # Verificar se o aluno já existe
    email_lower = email.strip().lower()
    aluno = Aluno.query.filter_by(email=email_lower).first()
    
    if aluno:
        # Se existe, loga o aluno (se estiver aprovado e ativo)
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
            
        # Loga o aluno com sucesso!
        session.clear()
        iniciar_sessao()
        session['usuario'] = aluno.login
        session['aluno_id'] = aluno.id
        session['tipo_usuario'] = "aluno"
        registrar_credencial(aluno.senha_hash or 'google_oauth')
        session.permanent = True
        return redirect('/perfil')
    else:
        # Aluno novo - mandar preencher o resto
        session['google_cadastro_nome'] = nome
        session['google_cadastro_email'] = email_lower
        flash('Quase lá! Para concluir o cadastro via Google, preencha os dados restantes.', 'sucesso')
        return redirect(url_for('auth.pagina_cadastro'))
