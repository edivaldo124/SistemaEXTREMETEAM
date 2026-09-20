import base64
import hashlib
import time
from datetime import datetime, timedelta, timezone
from urllib.parse import parse_qs, urlsplit

import pytest
import requests

from config import db
from modelos.mercado_pago_conexao import MercadoPagoConexao
from servicos import mercado_pago, mercado_pago_conta as conta
from servicos.mercado_pago import ConfiguracaoInvalida, MercadoPagoIndisponivel

CALLBACK = '/admin/mercado-pago/callback'
REDIRECT_URI = 'https://academia.example.test/admin/mercado-pago/callback'


class _Resposta:
    def __init__(self, status_code=200, corpo=None):
        self.status_code = status_code
        self._corpo = corpo

    def json(self):
        if self._corpo is None:
            raise ValueError('sem corpo')
        return self._corpo


def _tokens(**mudancas):
    corpo = {
        'access_token': 'APP_USR-acesso-1',
        'refresh_token': 'TG-refresh-1',
        'expires_in': 15552000,
        'user_id': 123456,
        'public_key': 'APP_USR-publica-1',
        'live_mode': True,
        'token_type': 'Bearer',
    }
    corpo.update(mudancas)
    return corpo


@pytest.fixture
def oauth_env(monkeypatch):
    monkeypatch.setenv('MERCADO_PAGO_CLIENT_ID', 'app-123')
    monkeypatch.setenv('MERCADO_PAGO_CLIENT_SECRET', 'segredo-do-app')
    monkeypatch.delenv('MERCADO_PAGO_TOKEN_KEY', raising=False)
    monkeypatch.delenv('MERCADO_PAGO_AMBIENTE', raising=False)


@pytest.fixture
def api_mp(monkeypatch, oauth_env):
    """Substitui POST /oauth/token. `respostas` é consumida em ordem; a última se repete."""
    estado = {'chamadas': [], 'respostas': [_Resposta(200, _tokens())]}

    def _post(url, json=None, headers=None, timeout=None):
        estado['chamadas'].append({'url': url, 'json': dict(json), 'timeout': timeout})
        resposta = estado['respostas'][0] if len(estado['respostas']) == 1 else estado['respostas'].pop(0)
        if isinstance(resposta, Exception):
            raise resposta
        return resposta

    monkeypatch.setattr(conta.requests, 'post', _post)
    return estado


def _dados_conexao(**mudancas):
    dados = {
        'access_token': 'APP_USR-acesso-1', 'refresh_token': 'TG-refresh-1',
        'expires_in': 15552000, 'user_id': '123456', 'public_key': 'APP_USR-publica-1',
        'live_mode': True,
    }
    dados.update(mudancas)
    return dados


def _conectar(**mudancas):
    """Grava uma conexão direto pelo serviço (precisa de app context)."""
    return conta.salvar_conexao(_dados_conexao(**mudancas))


def _ajustar(**campos):
    conexao = db.session.get(MercadoPagoConexao, 1)
    for nome, valor in campos.items():
        setattr(conexao, nome, valor)
    db.session.commit()


def _agora():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _preparar_state(client, **mudancas):
    guardado = {'state': 'estado-de-teste', 'verifier': 'v' * 64, 'criado_em': time.time()}
    guardado.update(mudancas)
    with client.session_transaction() as sess:
        sess['mp_oauth'] = guardado
    return guardado


# --- iniciar a conexão -------------------------------------------------------------


def test_conectar_exige_administrador(client, oauth_env):
    resposta = client.get('/admin/mercado-pago/conectar')

    assert resposta.status_code == 302
    assert resposta.headers['Location'].endswith('/login')


def test_conectar_sem_aplicativo_configurado_nao_sai_do_site(client, logar_como_admin, monkeypatch):
    monkeypatch.delenv('MERCADO_PAGO_CLIENT_ID', raising=False)
    monkeypatch.delenv('MERCADO_PAGO_CLIENT_SECRET', raising=False)
    logar_como_admin()

    resposta = client.get('/admin/mercado-pago/conectar', follow_redirects=True)

    assert 'ainda não foi habilitada' in resposta.get_data(as_text=True)
    assert resposta.request.path == '/admin/academia'


def test_conectar_manda_ao_mercado_pago_com_state_e_pkce(client, logar_como_admin, oauth_env):
    logar_como_admin()

    resposta = client.get('/admin/mercado-pago/conectar')

    assert resposta.status_code == 302
    destino = urlsplit(resposta.headers['Location'])
    assert (destino.scheme, destino.netloc, destino.path) == (
        'https', 'auth.mercadopago.com.br', '/authorization',
    )
    consulta = {chave: valor[0] for chave, valor in parse_qs(destino.query).items()}
    assert consulta['client_id'] == 'app-123'
    assert consulta['response_type'] == 'code'
    assert consulta['redirect_uri'] == REDIRECT_URI
    assert consulta['code_challenge_method'] == 'S256'
    assert 'segredo-do-app' not in resposta.headers['Location']

    with client.session_transaction() as sess:
        guardado = sess['mp_oauth']
    assert guardado['state'] == consulta['state']
    desafio = base64.urlsafe_b64encode(
        hashlib.sha256(guardado['verifier'].encode()).digest()
    ).rstrip(b'=').decode()
    assert consulta['code_challenge'] == desafio
    assert 43 <= len(guardado['verifier']) <= 128


def test_cada_conexao_iniciada_usa_state_novo(client, logar_como_admin, oauth_env):
    logar_como_admin()

    estados = set()
    for _ in range(3):
        client.get('/admin/mercado-pago/conectar')
        with client.session_transaction() as sess:
            estados.add(sess['mp_oauth']['state'])

    assert len(estados) == 3


# --- volta do Mercado Pago ---------------------------------------------------------


def test_callback_grava_conexao_com_tokens_cifrados(app, client, logar_como_admin, api_mp):
    logar_como_admin()
    guardado = _preparar_state(client)

    resposta = client.get(f'{CALLBACK}?code=codigo-1&state={guardado["state"]}', follow_redirects=True)

    texto = resposta.get_data(as_text=True)
    assert 'Conta do Mercado Pago conectada' in texto
    assert 'Conectada' in texto and '123456' in texto

    (chamada,) = api_mp['chamadas']
    assert chamada['url'] == 'https://api.mercadopago.com/oauth/token'
    assert chamada['json'] == {
        'client_id': 'app-123', 'client_secret': 'segredo-do-app',
        'grant_type': 'authorization_code', 'code': 'codigo-1',
        'redirect_uri': REDIRECT_URI, 'code_verifier': guardado['verifier'],
    }

    with app.app_context():
        linha = db.session.get(MercadoPagoConexao, 1)
        assert linha.mp_user_id == '123456'
        assert linha.live_mode is True
        assert 'APP_USR-acesso-1' not in linha.access_token_cifrado
        assert 'TG-refresh-1' not in linha.refresh_token_cifrado
        assert conta.access_token_vigente() == 'APP_USR-acesso-1'

    with client.session_transaction() as sess:
        assert 'mp_oauth' not in sess


def test_tokens_nunca_aparecem_na_tela_nem_no_log(client, logar_como_admin, api_mp, caplog):
    logar_como_admin()
    guardado = _preparar_state(client)

    with caplog.at_level('DEBUG'):
        resposta = client.get(f'{CALLBACK}?code=codigo-1&state={guardado["state"]}', follow_redirects=True)
        pagina = client.get('/admin/academia').get_data(as_text=True)

    for segredo in ('APP_USR-acesso-1', 'TG-refresh-1', 'segredo-do-app', 'codigo-1'):
        assert segredo not in resposta.get_data(as_text=True)
        assert segredo not in pagina
        assert segredo not in caplog.text


@pytest.mark.parametrize('query', [
    'code=codigo-1&state=outro-estado',
    'code=codigo-1',
    'state=estado-de-teste',
    'code=&state=estado-de-teste',
])
def test_callback_com_state_ou_code_invalido_nao_troca_nada(app, client, logar_como_admin, api_mp, query):
    logar_como_admin()
    _preparar_state(client)

    resposta = client.get(f'{CALLBACK}?{query}', follow_redirects=True)

    assert 'Não foi possível validar a autorização' in resposta.get_data(as_text=True)
    assert api_mp['chamadas'] == []
    with app.app_context():
        assert db.session.get(MercadoPagoConexao, 1) is None


def test_callback_sem_conexao_iniciada_pela_sessao(app, client, logar_como_admin, api_mp):
    logar_como_admin()

    resposta = client.get(f'{CALLBACK}?code=codigo-1&state=qualquer', follow_redirects=True)

    assert 'Não foi possível validar a autorização' in resposta.get_data(as_text=True)
    assert api_mp['chamadas'] == []


def test_callback_com_state_expirado(app, client, logar_como_admin, api_mp):
    logar_como_admin()
    guardado = _preparar_state(client, criado_em=time.time() - 11 * 60)

    resposta = client.get(f'{CALLBACK}?code=codigo-1&state={guardado["state"]}', follow_redirects=True)

    assert 'Não foi possível validar a autorização' in resposta.get_data(as_text=True)
    assert api_mp['chamadas'] == []


@pytest.mark.parametrize('lixo', ['texto', 5, ['a'], {'state': 1, 'verifier': 2, 'criado_em': 'x'}])
def test_callback_ignora_estado_malformado_na_sessao(client, logar_como_admin, api_mp, lixo):
    logar_como_admin()
    with client.session_transaction() as sess:
        sess['mp_oauth'] = lixo

    resposta = client.get(f'{CALLBACK}?code=codigo-1&state=1', follow_redirects=True)

    assert resposta.status_code == 200
    assert api_mp['chamadas'] == []


def test_state_e_de_uso_unico(client, logar_como_admin, api_mp):
    logar_como_admin()
    guardado = _preparar_state(client)
    url = f'{CALLBACK}?code=codigo-1&state={guardado["state"]}'

    client.get(url)
    segunda = client.get(url, follow_redirects=True)

    assert len(api_mp['chamadas']) == 1
    assert 'Não foi possível validar a autorização' in segunda.get_data(as_text=True)


def test_callback_cancelado_no_mercado_pago_consome_o_state(client, logar_como_admin, api_mp):
    logar_como_admin()
    guardado = _preparar_state(client)

    resposta = client.get(
        f'{CALLBACK}?error=access_denied&state={guardado["state"]}', follow_redirects=True,
    )

    assert 'cancelada no Mercado Pago' in resposta.get_data(as_text=True)
    assert api_mp['chamadas'] == []
    with client.session_transaction() as sess:
        assert 'mp_oauth' not in sess


def test_callback_com_code_recusado_nao_grava(app, client, logar_como_admin, api_mp):
    api_mp['respostas'] = [_Resposta(400, {'error': 'invalid_grant', 'message': 'code expirado'})]
    logar_como_admin()
    guardado = _preparar_state(client)

    resposta = client.get(f'{CALLBACK}?code=codigo-1&state={guardado["state"]}', follow_redirects=True)

    assert 'não concluiu a conexão' in resposta.get_data(as_text=True)
    with app.app_context():
        assert db.session.get(MercadoPagoConexao, 1) is None


@pytest.mark.parametrize('resposta', [
    requests.exceptions.ConnectTimeout('lento'),
    _Resposta(503, {'message': 'fora'}),
    _Resposta(429, {'message': 'muitas'}),
])
def test_callback_com_mercado_pago_fora_do_ar_nao_grava(app, client, logar_como_admin, api_mp, resposta):
    api_mp['respostas'] = [resposta]
    logar_como_admin()
    guardado = _preparar_state(client)

    pagina = client.get(f'{CALLBACK}?code=codigo-1&state={guardado["state"]}', follow_redirects=True)

    assert 'não respondeu agora' in pagina.get_data(as_text=True)
    with app.app_context():
        assert db.session.get(MercadoPagoConexao, 1) is None


@pytest.mark.parametrize('corpo', [
    _tokens(refresh_token=''),
    _tokens(access_token=None),
    _tokens(expires_in=0),
    _tokens(expires_in='longo'),
    _tokens(user_id=None),
    {'algo': 'inesperado'},
    None,
])
def test_callback_com_resposta_incompleta_nao_grava(app, client, logar_como_admin, api_mp, corpo):
    api_mp['respostas'] = [_Resposta(200, corpo)]
    logar_como_admin()
    guardado = _preparar_state(client)

    client.get(f'{CALLBACK}?code=codigo-1&state={guardado["state"]}')

    with app.app_context():
        assert db.session.get(MercadoPagoConexao, 1) is None


def test_callback_avisa_quando_a_conta_muda(app, client, logar_como_admin, api_mp, contexto_app):
    _conectar(user_id='999')
    logar_como_admin()
    guardado = _preparar_state(client)

    resposta = client.get(f'{CALLBACK}?code=codigo-1&state={guardado["state"]}', follow_redirects=True)

    assert 'Você trocou de conta' in resposta.get_data(as_text=True)


def test_reconectar_a_mesma_conta_nao_avisa_troca(client, logar_como_admin, api_mp, contexto_app):
    _conectar(user_id='123456')
    logar_como_admin()
    guardado = _preparar_state(client)

    resposta = client.get(f'{CALLBACK}?code=codigo-1&state={guardado["state"]}', follow_redirects=True)

    assert 'Você trocou de conta' not in resposta.get_data(as_text=True)


def test_reconectar_limpa_o_pedido_de_reconexao(client, logar_como_admin, api_mp, contexto_app):
    _conectar()
    _ajustar(precisa_reconectar=True)
    logar_como_admin()
    guardado = _preparar_state(client)

    client.get(f'{CALLBACK}?code=codigo-1&state={guardado["state"]}')

    db.session.expire_all()
    assert db.session.get(MercadoPagoConexao, 1).precisa_reconectar is False


def test_callback_exige_administrador(app, client, api_mp):
    resposta = client.get(f'{CALLBACK}?code=codigo-1&state=x')

    assert resposta.status_code == 302
    assert resposta.headers['Location'].endswith('/login')
    assert api_mp['chamadas'] == []


def test_callback_de_aluno_nao_conecta_conta(client, logar_como_aluno, criar_aluno, api_mp):
    logar_como_aluno(criar_aluno())

    resposta = client.get(f'{CALLBACK}?code=codigo-1&state=x')

    assert resposta.headers['Location'].endswith('/login')
    assert api_mp['chamadas'] == []


# --- desconectar -------------------------------------------------------------------


def test_desconectar_remove_a_conexao(client, logar_como_admin, contexto_app):
    _conectar()
    logar_como_admin()

    resposta = client.post('/admin/mercado-pago/desconectar', follow_redirects=True)

    assert 'Conta desconectada' in resposta.get_data(as_text=True)
    db.session.expire_all()
    assert db.session.get(MercadoPagoConexao, 1) is None


def test_desconectar_exige_post_e_administrador(client, contexto_app):
    _conectar()

    assert client.get('/admin/mercado-pago/desconectar').status_code == 405
    anonimo = client.post('/admin/mercado-pago/desconectar')

    assert anonimo.headers['Location'].endswith('/login')
    db.session.expire_all()
    assert db.session.get(MercadoPagoConexao, 1) is not None


def test_desconectar_exige_token_csrf(app, client, logar_como_admin, contexto_app):
    _conectar()
    logar_como_admin()
    app.config['WTF_CSRF_ENABLED'] = True
    try:
        assert client.post('/admin/mercado-pago/desconectar').status_code == 400
    finally:
        app.config['WTF_CSRF_ENABLED'] = False
    db.session.expire_all()
    assert db.session.get(MercadoPagoConexao, 1) is not None


# --- tela da academia --------------------------------------------------------------


def test_tela_sem_conexao_oferece_conectar(client, logar_como_admin, oauth_env):
    logar_como_admin()

    pagina = client.get('/admin/academia').get_data(as_text=True)

    assert 'href="/admin/mercado-pago/conectar"' in pagina
    assert 'Conectar Mercado Pago' in pagina
    assert 'Desconectar' not in pagina


def test_tela_conectada_mostra_conta_e_permite_desconectar(client, logar_como_admin, oauth_env, contexto_app):
    _conectar()
    logar_como_admin()

    pagina = client.get('/admin/academia').get_data(as_text=True)

    assert 'Conectada' in pagina and '123456' in pagina and 'Produção' in pagina
    assert 'action="/admin/mercado-pago/desconectar"' in pagina
    # sem o <dialog> e o modal.js o formulário desconectaria sem pedir confirmação
    assert 'id="confirm-dialog"' in pagina and 'js/modal.js' in pagina
    assert 'Reconexão necessária' not in pagina


def test_tela_avisa_quando_a_reconexao_e_necessaria(client, logar_como_admin, oauth_env, contexto_app):
    _conectar()
    _ajustar(precisa_reconectar=True)
    logar_como_admin()

    pagina = client.get('/admin/academia').get_data(as_text=True)

    assert 'Reconexão necessária' in pagina
    assert 'Reconectar' in pagina


def test_tela_sem_aplicativo_nem_conexao_nao_mostra_botao(client, logar_como_admin, monkeypatch):
    monkeypatch.delenv('MERCADO_PAGO_CLIENT_ID', raising=False)
    monkeypatch.delenv('MERCADO_PAGO_CLIENT_SECRET', raising=False)
    logar_como_admin()

    pagina = client.get('/admin/academia').get_data(as_text=True)

    assert '/admin/mercado-pago/conectar' not in pagina
    # o ambiente de teste tem MERCADO_PAGO_ACCESS_TOKEN: a tela diz que usa o do servidor
    assert 'credencial do Mercado Pago configurada no servidor' in pagina


def test_erro_de_validacao_da_academia_mantem_a_secao_do_mercado_pago(client, logar_como_admin, oauth_env):
    logar_como_admin()

    resposta = client.post('/admin/academia', data={'email': 'isto-nao-e-email'})

    assert resposta.status_code == 400
    assert 'Conectar Mercado Pago' in resposta.get_data(as_text=True)


# --- token usado pelo serviço de pagamentos ---------------------------------------


def test_sem_conexao_vale_o_token_do_ambiente(contexto_app):
    assert conta.access_token_vigente() == 'token-fake-de-teste'


def test_fora_de_contexto_de_app_vale_o_token_do_ambiente():
    assert conta.access_token_vigente() == 'token-fake-de-teste'


def test_conexao_tem_prioridade_sobre_o_token_do_ambiente(contexto_app):
    _conectar(access_token='APP_USR-da-academia')

    assert conta.access_token_vigente() == 'APP_USR-da-academia'


def test_desconectar_volta_ao_token_do_ambiente(contexto_app):
    _conectar()
    assert conta.remover_conexao() is True

    assert conta.access_token_vigente() == 'token-fake-de-teste'
    assert conta.remover_conexao() is False


def test_sem_nenhuma_credencial_o_servico_recusa(contexto_app, monkeypatch):
    monkeypatch.delenv('MERCADO_PAGO_ACCESS_TOKEN')

    with pytest.raises(MercadoPagoIndisponivel):
        mercado_pago._sdk()


def test_sdk_do_servico_usa_o_token_da_conexao(contexto_app, monkeypatch):
    usados = []
    monkeypatch.setattr(mercado_pago.mercadopago, 'SDK', lambda token: usados.append(token) or object())
    _conectar(access_token='APP_USR-da-academia')

    mercado_pago._sdk()

    assert usados == ['APP_USR-da-academia']


def test_ambiente_segue_o_live_mode_da_conta(contexto_app, monkeypatch):
    monkeypatch.delenv('MERCADO_PAGO_AMBIENTE', raising=False)
    assert mercado_pago.ambiente_mercado_pago() == 'producao'  # token do ambiente, sem prefixo TEST-

    _conectar(live_mode=False)
    assert mercado_pago.ambiente_mercado_pago() == 'sandbox'

    _conectar(live_mode=True)
    assert mercado_pago.ambiente_mercado_pago() == 'producao'


def test_ambiente_explicito_vence_a_conta_conectada(contexto_app, monkeypatch):
    _conectar(live_mode=False)
    monkeypatch.setenv('MERCADO_PAGO_AMBIENTE', 'producao')

    assert mercado_pago.ambiente_mercado_pago() == 'producao'


def test_resposta_sem_live_mode_e_tratada_como_producao(contexto_app, api_mp):
    api_mp['respostas'] = [_Resposta(200, {k: v for k, v in _tokens().items() if k != 'live_mode'})]

    assert conta.trocar_codigo('c', 'v' * 64)['live_mode'] is True


# --- renovação ---------------------------------------------------------------------


def test_token_com_folga_nao_e_renovado(contexto_app, api_mp):
    _conectar()

    assert conta.access_token_vigente() == 'APP_USR-acesso-1'
    assert api_mp['chamadas'] == []


def test_token_perto_de_vencer_e_renovado_uma_vez(contexto_app, api_mp):
    _conectar()
    _ajustar(expira_em=_agora() + timedelta(days=5))
    api_mp['respostas'] = [_Resposta(200, _tokens(
        access_token='APP_USR-acesso-2', refresh_token='TG-refresh-2', expires_in=15552000,
    ))]

    assert conta.access_token_vigente() == 'APP_USR-acesso-2'
    assert conta.access_token_vigente() == 'APP_USR-acesso-2'

    (chamada,) = api_mp['chamadas']
    assert chamada['json'] == {
        'client_id': 'app-123', 'client_secret': 'segredo-do-app',
        'grant_type': 'refresh_token', 'refresh_token': 'TG-refresh-1',
    }
    db.session.expire_all()
    linha = db.session.get(MercadoPagoConexao, 1)
    assert linha.renovado_em is not None
    assert linha.expira_em > _agora() + timedelta(days=100)
    assert 'TG-refresh-2' not in linha.refresh_token_cifrado
    # o refresh_token novo é o que será usado na próxima renovação
    assert conta._decifrar(linha.refresh_token_cifrado) == 'TG-refresh-2'


def test_renovacao_recusada_marca_reconexao_e_nao_insiste(contexto_app, api_mp):
    _conectar()
    _ajustar(expira_em=_agora() + timedelta(days=5))
    api_mp['respostas'] = [_Resposta(400, {'error': 'invalid_grant'})]

    # o token atual ainda vale: os pagamentos seguem até o vencimento real
    assert conta.access_token_vigente() == 'APP_USR-acesso-1'
    assert conta.access_token_vigente() == 'APP_USR-acesso-1'

    assert len(api_mp['chamadas']) == 1
    db.session.expire_all()
    assert db.session.get(MercadoPagoConexao, 1).precisa_reconectar is True
    assert conta.estado_conexao()['precisa_reconectar'] is True


def test_conexao_vencida_e_sem_renovacao_possivel_recusa(contexto_app, api_mp):
    _conectar()
    _ajustar(expira_em=_agora() - timedelta(minutes=1), precisa_reconectar=True)

    with pytest.raises(MercadoPagoIndisponivel, match='reconecte'):
        conta.access_token_vigente()
    assert api_mp['chamadas'] == []


def test_falha_passageira_na_renovacao_usa_o_token_ainda_valido(contexto_app, api_mp):
    _conectar()
    _ajustar(expira_em=_agora() + timedelta(days=5))
    api_mp['respostas'] = [requests.exceptions.ConnectionError('sem rede')]

    assert conta.access_token_vigente() == 'APP_USR-acesso-1'
    db.session.expire_all()
    assert db.session.get(MercadoPagoConexao, 1).precisa_reconectar is False


def test_falha_na_renovacao_com_token_vencido_levanta(contexto_app, api_mp):
    _conectar()
    _ajustar(expira_em=_agora() - timedelta(minutes=1))
    api_mp['respostas'] = [_Resposta(503, {})]

    with pytest.raises(MercadoPagoIndisponivel):
        conta.access_token_vigente()


def test_erro_diferente_de_invalid_grant_nao_marca_reconexao(contexto_app, api_mp):
    _conectar()
    _ajustar(expira_em=_agora() + timedelta(days=5))
    api_mp['respostas'] = [_Resposta(401, {'error': 'invalid_client'})]

    assert conta.access_token_vigente() == 'APP_USR-acesso-1'
    db.session.expire_all()
    assert db.session.get(MercadoPagoConexao, 1).precisa_reconectar is False


def test_renovacao_nao_encerra_a_transacao_de_quem_pediu_o_token(contexto_app, api_mp):
    """A rota de checkout pede o token com a mensalidade travada na sessão dela."""
    _conectar()
    _ajustar(expira_em=_agora() + timedelta(days=5))
    api_mp['respostas'] = [_Resposta(200, _tokens(access_token='APP_USR-acesso-2'))]
    conexao = db.session.get(MercadoPagoConexao, 1)
    conexao.mp_user_id = 'pendente-na-sessao'  # alteração ainda não confirmada

    assert conta.access_token_vigente() == 'APP_USR-acesso-2'

    assert conexao in db.session.dirty
    db.session.rollback()
    assert db.session.get(MercadoPagoConexao, 1).mp_user_id == '123456'


# --- cifra -------------------------------------------------------------------------


def test_chave_dedicada_cifra_e_troca_de_chave_torna_ilegivel(contexto_app, monkeypatch):
    from cryptography.fernet import Fernet

    monkeypatch.setenv('MERCADO_PAGO_TOKEN_KEY', Fernet.generate_key().decode())
    _conectar()
    assert conta.access_token_vigente() == 'APP_USR-acesso-1'

    monkeypatch.setenv('MERCADO_PAGO_TOKEN_KEY', Fernet.generate_key().decode())

    with pytest.raises(conta.ConexaoIlegivel):
        conta.access_token_vigente()
    estado = conta.estado_conexao()
    assert estado['conectada'] and estado['precisa_reconectar']


def test_conexao_ilegivel_e_tratada_como_mercado_pago_indisponivel(contexto_app, monkeypatch):
    from cryptography.fernet import Fernet

    _conectar()
    monkeypatch.setenv('MERCADO_PAGO_TOKEN_KEY', Fernet.generate_key().decode())

    with pytest.raises(MercadoPagoIndisponivel):
        mercado_pago._sdk()


def test_chave_dedicada_malformada_e_erro_de_configuracao(contexto_app, monkeypatch):
    monkeypatch.setenv('MERCADO_PAGO_TOKEN_KEY', 'isto-nao-e-uma-chave-fernet')

    with pytest.raises(ConfiguracaoInvalida):
        _conectar()


def test_sem_chave_dedicada_a_cifra_deriva_da_secret_key(contexto_app, app, monkeypatch):
    _conectar()
    monkeypatch.setattr(app, 'secret_key', 'outra-secret-key')

    with pytest.raises(conta.ConexaoIlegivel):
        conta.access_token_vigente()
