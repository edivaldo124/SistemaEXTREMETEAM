"""Conexão da conta Mercado Pago da academia por OAuth.

Quem opera a plataforma cria UM aplicativo no Mercado Pago (client_id/client_secret).
A academia só clica em "Conectar", autoriza na tela do Mercado Pago e este módulo
guarda o token dela. Ninguém mais precisa abrir painel de desenvolvedor nem colar
credencial.

Regras que este módulo garante:

- Os tokens ficam cifrados (Fernet) no banco e nunca são logados nem devolvidos a tela.
- O access_token dura ~180 dias e é renovado sozinho antes de vencer. O refresh_token é
  de uso único: a renovação corre sob lock de linha, para dois processos não gastarem o
  mesmo refresh_token e um deles invalidar a conexão.
- Sem conexão OAuth, vale o `MERCADO_PAGO_ACCESS_TOKEN` do ambiente (instalações que já
  funcionam continuam funcionando). Com conexão, ela SEMPRE vence o ambiente.
- Toda leitura/renovação usa uma conexão de banco própria, fora da sessão da requisição:
  quem pede o token costuma estar no meio de uma transação com lock de mensalidade, e
  um commit aqui a encerraria pela metade.
"""
import base64
import hashlib
import logging
import os
import secrets
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

import requests
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from flask import current_app, has_app_context
from sqlalchemy import delete, select, update

from config import db
from modelos.mercado_pago_conexao import MercadoPagoConexao
from servicos.mercado_pago import (
    AMBIENTE_PRODUCAO,
    AMBIENTE_SANDBOX,
    ConfiguracaoInvalida,
    MercadoPagoIndisponivel,
    base_url_publica,
)

logger = logging.getLogger(__name__)

URL_AUTORIZACAO = 'https://auth.mercadopago.com.br/authorization'
URL_TOKEN = 'https://api.mercadopago.com/oauth/token'
CAMINHO_CALLBACK = '/admin/mercado-pago/callback'
TIMEOUT_OAUTH_SEGUNDOS = 6.0

# O access_token vale 180 dias. Renovar com folga larga dá semanas de tolerância a uma
# indisponibilidade do Mercado Pago sem que nenhuma cobrança seja afetada.
RENOVAR_ANTES = timedelta(days=15)

VARIAVEL_CHAVE = 'MERCADO_PAGO_TOKEN_KEY'
_INFO_HKDF = b'extremeteam/mercado-pago/tokens/v1'
_TABELA = MercadoPagoConexao.__table__


class ConexaoIlegivel(MercadoPagoIndisponivel):
    """Há conexão gravada, mas os tokens não abrem (chave trocada ou dado corrompido).

    É um MercadoPagoIndisponivel de propósito: todo chamador que já trata a falta do
    provedor passa a tratar isto do mesmo jeito, sem rota nova de erro.
    """


def _agora():
    """UTC sem fuso, o mesmo formato que o restante do projeto grava no banco."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


# --- cifra ------------------------------------------------------------------------


def _fernet():
    chave = (os.environ.get(VARIAVEL_CHAVE) or '').strip()
    if chave:
        try:
            return Fernet(chave.encode())
        except ValueError as exc:
            raise ConfiguracaoInvalida(
                f'{VARIAVEL_CHAVE} deve ser uma chave Fernet (32 bytes em base64 url-safe).'
            ) from exc

    # Sem chave dedicada, deriva uma da SECRET_KEY. Funciona sem configurar nada, mas
    # trocar a SECRET_KEY torna os tokens ilegíveis (basta reconectar a conta).
    derivada = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=_INFO_HKDF).derive(
        str(current_app.secret_key).encode('utf-8')
    )
    return Fernet(base64.urlsafe_b64encode(derivada))


def _cifrar(texto):
    return _fernet().encrypt(texto.encode('utf-8')).decode('ascii')


def _decifrar(cifrado):
    try:
        return _fernet().decrypt(cifrado.encode('ascii')).decode('utf-8')
    except InvalidToken as exc:
        raise ConexaoIlegivel(
            'Credenciais do Mercado Pago ilegíveis; reconecte a conta no painel da academia.'
        ) from exc
    except ConfiguracaoInvalida as exc:
        raise ConexaoIlegivel(str(exc)) from exc


# --- configuração e URLs ----------------------------------------------------------


def _client_id():
    return (os.environ.get('MERCADO_PAGO_CLIENT_ID') or '').strip()


def _client_secret():
    return (os.environ.get('MERCADO_PAGO_CLIENT_SECRET') or '').strip()


def oauth_configurado():
    """O servidor tem o aplicativo do Mercado Pago (client_id + client_secret)?"""
    return bool(_client_id() and _client_secret())


def redirect_uri():
    """Endereço de retorno. Vem de APP_BASE_URL, nunca do Host da requisição.

    É exatamente este valor que precisa estar cadastrado no aplicativo do Mercado Pago.
    """
    return f'{base_url_publica()}{CAMINHO_CALLBACK}'


def _token_do_ambiente():
    return os.environ.get('MERCADO_PAGO_ACCESS_TOKEN') or None


# --- autorização (ida) ------------------------------------------------------------


def nova_autorizacao():
    """Prepara uma ida ao Mercado Pago.

    Devolve (url, segredos). `segredos` (state + code_verifier) fica na sessão do
    administrador e só volta a ser lido no callback: o state amarra a volta a quem
    iniciou, e o PKCE impede que um code interceptado seja trocado por outra pessoa.
    """
    if not oauth_configurado():
        raise ConfiguracaoInvalida('MERCADO_PAGO_CLIENT_ID/MERCADO_PAGO_CLIENT_SECRET ausentes.')

    state = secrets.token_urlsafe(32)
    code_verifier = secrets.token_urlsafe(64)  # 86 caracteres; o limite do PKCE é 43-128
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode('ascii')).digest()
    ).rstrip(b'=').decode('ascii')

    url = f'{URL_AUTORIZACAO}?' + urlencode({
        'client_id': _client_id(),
        'response_type': 'code',
        'platform_id': 'mp',
        'state': state,
        'redirect_uri': redirect_uri(),
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256',
    })
    return url, {'state': state, 'verifier': code_verifier}


# --- chamadas ao endpoint de token ------------------------------------------------


def _pedir_token(corpo):
    """POST /oauth/token. Nunca loga o corpo (tem segredos) nem a resposta (tem tokens).

    Retorna {'sucesso': True, access_token, refresh_token, expires_in, user_id,
    public_key, live_mode} ou {'sucesso': False, 'erro': '<codigo do MP>'}.
    Levanta MercadoPagoIndisponivel em falha de transporte, 429 ou 5xx.
    """
    corpo = {'client_id': _client_id(), 'client_secret': _client_secret(), **corpo}
    try:
        resposta = requests.post(
            URL_TOKEN, json=corpo, headers={'Accept': 'application/json'},
            timeout=TIMEOUT_OAUTH_SEGUNDOS,
        )
    except requests.exceptions.RequestException as exc:
        raise MercadoPagoIndisponivel(f'Falha de comunicacao com o Mercado Pago: {exc}') from exc

    if resposta.status_code >= 500 or resposta.status_code == 429:
        raise MercadoPagoIndisponivel(
            f'Mercado Pago respondeu {resposta.status_code} ao trocar credenciais OAuth.'
        )

    try:
        dados = resposta.json()
    except ValueError:
        dados = None
    if not isinstance(dados, dict):
        dados = {}

    if resposta.status_code >= 400:
        erro = str(dados.get('error') or 'recusado')[:60]
        logger.warning('Mercado Pago recusou a troca de credenciais OAuth (status=%s, erro=%s).',
                       resposta.status_code, erro)
        return {'sucesso': False, 'erro': erro}

    access_token, refresh_token = dados.get('access_token'), dados.get('refresh_token')
    expires_in, user_id = dados.get('expires_in'), dados.get('user_id')
    if (not isinstance(access_token, str) or not access_token
            or not isinstance(refresh_token, str) or not refresh_token
            or isinstance(expires_in, bool) or not isinstance(expires_in, int) or expires_in <= 0
            or user_id in (None, '') or len(str(user_id)) > 40):
        logger.error('Resposta OAuth do Mercado Pago incompleta ou fora do formato esperado.')
        return {'sucesso': False, 'erro': 'resposta_invalida'}

    public_key = dados.get('public_key')
    return {
        'sucesso': True,
        'access_token': access_token,
        'refresh_token': refresh_token,
        'expires_in': expires_in,
        'user_id': str(user_id),
        'public_key': public_key[:200] if isinstance(public_key, str) else None,
        # Na dúvida, produção - o mesmo critério restritivo de ambiente_mercado_pago().
        'live_mode': dados.get('live_mode') is not False,
    }


def trocar_codigo(code, code_verifier):
    """Troca o code do callback pelos tokens da conta que autorizou."""
    return _pedir_token({
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri(),
        'code_verifier': code_verifier,
    })


# --- persistência -----------------------------------------------------------------


def salvar_conexao(dados):
    """Grava (ou substitui) a conexão a partir de uma resposta `sucesso` do token.

    Devolve o id da conta anterior quando havia outra conectada, ou None.
    """
    access_cifrado = _cifrar(dados['access_token'])
    refresh_cifrado = _cifrar(dados['refresh_token'])
    agora = _agora()

    conexao = db.session.get(MercadoPagoConexao, 1)
    anterior = conexao.mp_user_id if conexao else None
    if conexao is None:
        conexao = MercadoPagoConexao(id=1)

    conexao.mp_user_id = dados['user_id']
    conexao.public_key = dados['public_key']
    conexao.access_token_cifrado = access_cifrado
    conexao.refresh_token_cifrado = refresh_cifrado
    conexao.live_mode = dados['live_mode']
    conexao.expira_em = agora + timedelta(seconds=dados['expires_in'])
    conexao.conectado_em = agora
    conexao.renovado_em = None
    conexao.precisa_reconectar = False

    db.session.add(conexao)
    db.session.commit()
    return anterior


def remover_conexao():
    """Esquece a conta conectada. Devolve True se havia uma."""
    removidas = db.session.execute(delete(MercadoPagoConexao)).rowcount
    db.session.commit()
    return bool(removidas)


def estado_conexao():
    """Resumo para a tela do administrador. Não expõe token algum."""
    conexao = db.session.get(MercadoPagoConexao, 1)
    base = {
        'oauth_disponivel': oauth_configurado(),
        'usa_credencial_do_servidor': bool(_token_do_ambiente()),
        'conectada': conexao is not None,
    }
    if conexao is None:
        return base

    try:
        _decifrar(conexao.access_token_cifrado)
        legivel = True
    except MercadoPagoIndisponivel:
        legivel = False

    base.update({
        'mp_user_id': conexao.mp_user_id,
        'live_mode': conexao.live_mode,
        'conectado_em': conexao.conectado_em,
        'precisa_reconectar': (
            conexao.precisa_reconectar or not legivel or conexao.expira_em <= _agora()
        ),
    })
    return base


# --- uso pelo serviço de pagamentos -----------------------------------------------


def _ler_conexao():
    with db.engine.connect() as conn:
        return conn.execute(select(_TABELA).where(_TABELA.c.id == 1)).first()


def _precisa_renovar(linha):
    return not linha.precisa_reconectar and linha.expira_em - _agora() <= RENOVAR_ANTES


def _renovar():
    """Troca o refresh_token por um par novo e devolve a linha já atualizada.

    O lock de linha serializa processos: quem chega depois espera, relê a linha e
    encontra o par novo em vez de gastar (de novo) um refresh_token já consumido.
    """
    with db.engine.begin() as conn:
        linha = conn.execute(select(_TABELA).where(_TABELA.c.id == 1).with_for_update()).first()
        if linha is None or not _precisa_renovar(linha):
            return linha

        resposta = _pedir_token({
            'grant_type': 'refresh_token',
            'refresh_token': _decifrar(linha.refresh_token_cifrado),
        })
        agora = _agora()
        if resposta['sucesso']:
            valores = {
                'access_token_cifrado': _cifrar(resposta['access_token']),
                'refresh_token_cifrado': _cifrar(resposta['refresh_token']),
                'expira_em': agora + timedelta(seconds=resposta['expires_in']),
                'renovado_em': agora,
                'live_mode': resposta['live_mode'],
            }
            if resposta['public_key']:
                valores['public_key'] = resposta['public_key']
            conn.execute(update(_TABELA).where(_TABELA.c.id == 1).values(**valores))
        elif resposta['erro'] == 'invalid_grant':
            # Autorização revogada pela academia (ou refresh_token já gasto): nenhuma
            # nova tentativa resolve, só reconectar. Marca para a tela avisar.
            logger.error('Mercado Pago recusou o refresh_token; a conta precisa ser reconectada.')
            conn.execute(update(_TABELA).where(_TABELA.c.id == 1).values(precisa_reconectar=True))
        else:
            raise MercadoPagoIndisponivel(
                f'Mercado Pago recusou renovar as credenciais ({resposta["erro"]}).'
            )
        return conn.execute(select(_TABELA).where(_TABELA.c.id == 1)).first()


def access_token_vigente():
    """Access token que o serviço de pagamentos deve usar agora, ou None se não há nenhum.

    Levanta MercadoPagoIndisponivel quando há conexão, mas ela não pode ser usada
    (expirada sem renovação possível, ou ilegível).
    """
    if not has_app_context():
        return _token_do_ambiente()

    linha = _ler_conexao()
    if linha is None:
        return _token_do_ambiente()

    if _precisa_renovar(linha):
        try:
            linha = _renovar()
        except ConexaoIlegivel:
            raise
        except MercadoPagoIndisponivel:
            # Falha passageira: o token atual segue valendo até vencer de verdade.
            if linha.expira_em <= _agora():
                raise
            logger.warning('Nao foi possivel renovar as credenciais do Mercado Pago agora; '
                           'seguindo com o token atual.', exc_info=True)
        if linha is None:  # desconectada enquanto renovávamos
            return _token_do_ambiente()

    if linha.expira_em <= _agora():
        raise MercadoPagoIndisponivel(
            'A conexao com o Mercado Pago expirou; reconecte a conta no painel da academia.'
        )
    return _decifrar(linha.access_token_cifrado)


def ambiente_da_conexao():
    """'producao'/'sandbox' segundo a conta conectada, ou None se não há conexão."""
    if not has_app_context():
        return None
    linha = _ler_conexao()
    if linha is None:
        return None
    return AMBIENTE_PRODUCAO if linha.live_mode else AMBIENTE_SANDBOX
