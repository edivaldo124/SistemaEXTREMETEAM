import hmac
import logging
import time

from flask import Blueprint, flash, redirect, request, session, url_for
from sqlalchemy.exc import SQLAlchemyError

from config import db, limiter
from servicos import mercado_pago_conta as conta
from servicos.autorizacao import admin_requerido
from servicos.mercado_pago import ConfiguracaoInvalida, MercadoPagoIndisponivel

mercado_pago_oauth_bp = Blueprint('mercado_pago_oauth', __name__)
logger = logging.getLogger(__name__)

CHAVE_SESSAO = 'mp_oauth'
# O code do Mercado Pago vale 10 minutos; o state guardado não precisa viver mais que isso.
VALIDADE_AUTORIZACAO_SEGUNDOS = 10 * 60

MSG_NAO_HABILITADO = (
    'A conexão com o Mercado Pago ainda não foi habilitada neste servidor. '
    'Avise quem administra a plataforma.'
)
MSG_FALHA_VALIDACAO = 'Não foi possível validar a autorização. Clique em “Conectar” para tentar de novo.'
MSG_INDISPONIVEL = 'O Mercado Pago não respondeu agora. Tente conectar novamente em instantes.'
MSG_FALHA_GENERICA = 'O Mercado Pago não concluiu a conexão. Tente novamente.'


def _voltar():
    return redirect(url_for('academia.configuracoes'))


def _autorizacao_valida(guardada, state_recebido):
    """O state devolvido é o que ESTA sessão emitiu, há pouco tempo?"""
    if not isinstance(guardada, dict):
        return False
    state, verifier, criado_em = guardada.get('state'), guardada.get('verifier'), guardada.get('criado_em')
    if not isinstance(state, str) or not isinstance(verifier, str) or not isinstance(criado_em, (int, float)):
        return False
    if time.time() - criado_em > VALIDADE_AUTORIZACAO_SEGUNDOS:
        return False
    return hmac.compare_digest(state.encode('utf-8'), state_recebido.encode('utf-8'))


@mercado_pago_oauth_bp.route('/admin/mercado-pago/conectar')
@limiter.limit('10 per 15 minutes')
@admin_requerido
def conectar():
    """Só monta o state/PKCE na sessão e manda o administrador ao Mercado Pago.

    É um GET porque o destino é outro domínio e a política de segurança da aplicação
    limita `form-action` a este site. Não altera nada além da sessão de quem clica.
    """
    if not conta.oauth_configurado():
        flash(MSG_NAO_HABILITADO, 'erro')
        return _voltar()

    try:
        url, segredos = conta.nova_autorizacao()
    except ConfiguracaoInvalida:
        logger.error('Configuracao invalida ao iniciar a conexao OAuth do Mercado Pago.', exc_info=True)
        flash(MSG_NAO_HABILITADO, 'erro')
        return _voltar()

    session[CHAVE_SESSAO] = {**segredos, 'criado_em': time.time()}
    return redirect(url)


@mercado_pago_oauth_bp.route('/admin/mercado-pago/callback')
@limiter.limit('20 per 15 minutes')
@admin_requerido
def callback():
    # Uso único: o state sai da sessão já na primeira leitura, deu certo ou não. Repetir
    # a URL de retorno (histórico, atualizar a página) nunca reaproveita uma autorização.
    guardada = session.pop(CHAVE_SESSAO, None)

    if request.args.get('error'):
        # access_denied: a pessoa clicou em "Cancelar" na tela do Mercado Pago.
        flash('A conexão foi cancelada no Mercado Pago. Nada foi alterado.', 'erro')
        return _voltar()

    code = request.args.get('code', '')
    state_recebido = request.args.get('state', '')
    if not code or len(code) > 512 or not _autorizacao_valida(guardada, state_recebido):
        logger.warning('Callback OAuth do Mercado Pago recusado: state ausente, invalido ou expirado.')
        flash(MSG_FALHA_VALIDACAO, 'erro')
        return _voltar()

    try:
        dados = conta.trocar_codigo(code, guardada['verifier'])
    except MercadoPagoIndisponivel:
        logger.error('Mercado Pago indisponivel ao trocar o code OAuth.', exc_info=True)
        flash(MSG_INDISPONIVEL, 'erro')
        return _voltar()
    except ConfiguracaoInvalida:
        logger.error('Configuracao invalida ao trocar o code OAuth.', exc_info=True)
        flash(MSG_NAO_HABILITADO, 'erro')
        return _voltar()

    if not dados['sucesso']:
        flash(MSG_FALHA_GENERICA, 'erro')
        return _voltar()

    try:
        anterior = conta.salvar_conexao(dados)
    except ConfiguracaoInvalida:
        db.session.rollback()
        logger.error('Chave de cifra dos tokens do Mercado Pago invalida.', exc_info=True)
        flash(MSG_NAO_HABILITADO, 'erro')
        return _voltar()
    except SQLAlchemyError:
        db.session.rollback()
        logger.error('Falha ao gravar a conexao do Mercado Pago.', exc_info=True)
        flash('Não foi possível salvar a conexão. Tente novamente.', 'erro')
        return _voltar()

    mensagem = 'Conta do Mercado Pago conectada. As mensalidades pagas online passam a cair nela.'
    if anterior and anterior != dados['user_id']:
        mensagem += (
            ' Você trocou de conta: cobranças abertas na conta anterior deixam de ser '
            'confirmadas automaticamente.'
        )
    flash(mensagem, 'sucesso')
    return _voltar()


@mercado_pago_oauth_bp.route('/admin/mercado-pago/desconectar', methods=['POST'])
@admin_requerido
def desconectar():
    try:
        removida = conta.remover_conexao()
    except SQLAlchemyError:
        db.session.rollback()
        logger.error('Falha ao remover a conexao do Mercado Pago.', exc_info=True)
        flash('Não foi possível desconectar. Tente novamente.', 'erro')
        return _voltar()

    if removida:
        flash(
            'Conta desconectada deste sistema. A autorização continua listada na sua conta '
            'do Mercado Pago até você removê-la por lá.',
            'sucesso',
        )
    return _voltar()
