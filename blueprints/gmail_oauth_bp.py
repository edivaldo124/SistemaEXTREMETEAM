import hmac
import logging
import time

from flask import Blueprint, flash, redirect, request, session, url_for
from config import limiter
from servicos.autorizacao import admin_requerido
from servicos import gmail_conta

logger = logging.getLogger(__name__)
gmail_oauth_bp = Blueprint('gmail_oauth', __name__)
CHAVE_SESSAO = 'gmail_oauth'


def _voltar():
    return redirect(url_for('academia.configuracoes'))


@gmail_oauth_bp.route('/admin/gmail/conectar')
@limiter.limit('10 per 15 minutes')
@admin_requerido
def conectar():
    if not gmail_conta.oauth_configurado():
        flash('Configure GMAIL_CLIENT_ID e GMAIL_CLIENT_SECRET no servidor.', 'erro')
        return _voltar()
    url, state = gmail_conta.nova_autorizacao()
    session[CHAVE_SESSAO] = {'state': state, 'criado_em': time.time()}
    return redirect(url)


@gmail_oauth_bp.route('/admin/gmail/callback')
@limiter.limit('20 per 15 minutes')
@admin_requerido
def callback():
    guardada = session.pop(CHAVE_SESSAO, None)
    recebido = request.args.get('state', '')
    if (not guardada or not isinstance(recebido, str)
            or time.time() - guardada.get('criado_em', 0) > 600
            or not hmac.compare_digest(guardada.get('state', ''), recebido)):
        flash('Não foi possível validar a autorização do Gmail.', 'erro')
        return _voltar()
    if request.args.get('error'):
        flash('A conexão com o Gmail foi cancelada.', 'erro')
        return _voltar()
    try:
        email, refresh_token = gmail_conta.trocar_codigo(request.args.get('code', ''))
        gmail_conta.salvar(email, refresh_token)
    except Exception:
        logger.exception('Falha ao conectar a conta Gmail do administrador.')
        flash('Não foi possível conectar o Gmail. Tente novamente.', 'erro')
        return _voltar()
    flash(f'Gmail conectado: {email}.', 'sucesso')
    return _voltar()


@gmail_oauth_bp.route('/admin/gmail/desconectar', methods=['POST'])
@admin_requerido
def desconectar():
    gmail_conta.remover()
    flash('Conta Gmail desconectada.', 'sucesso')
    return _voltar()
