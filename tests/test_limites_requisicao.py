"""Limites de requisição da rodada de 04/10/2026 (SEC-10 a SEC-17 e SEC-19).

Cada limite novo tem um teste que faz exatamente o permitido sem receber 429 e então
estoura. O conftest zera o limitador antes de cada teste (`limiter.reset()`).
"""

import hashlib
import hmac
import os
import time
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
import yaml

import blueprints.pix_bp as pix_bp
import blueprints.usuario_bp as usuario_bp
from config import limiter
from servicos.mercado_pago import MercadoPagoIndisponivel

RAIZ = Path(__file__).resolve().parent.parent
CPF_INEXISTENTE = '00000000000'


def _estourar(enviar, limite):
    """Faz `limite` requisições sem nenhum 429 e devolve a seguinte."""
    codigos = [enviar().status_code for _ in range(limite)]
    assert 429 not in codigos, f'429 antes de {limite} requisições: {codigos}'
    return enviar()


def _sessao(cliente, tipo, aluno=None):
    from servicos.autorizacao import impressao_credencial
    from servicos.credenciais import referencia_credencial_admin

    with cliente.session_transaction() as sessao:
        sessao['tipo_usuario'] = tipo
        if tipo == 'admin':
            sessao['usuario'] = os.environ['ADMIN_USER']
            sessao['credencial'] = impressao_credencial(referencia_credencial_admin())
        else:
            sessao['usuario'] = aluno.login
            sessao['aluno_id'] = aluno.id
            sessao['credencial'] = impressao_credencial(aluno.senha_hash)


# ---------------------------------------------------------------- limite padrão --

def test_limite_padrao_tem_teto_por_minuto_e_por_hora_por_conta():
    limites = {(str(lim.limit), lim.key_func.__name__) for lim in limiter.limit_manager.default_limits}
    assert limites == {('300 per 1 minute', 'chave_da_conta'), ('3000 per 1 hour', 'chave_da_conta')}


def test_limite_padrao_alcanca_rota_sem_limite_proprio(client):
    assert _estourar(lambda: client.get('/robots.txt'), 300).status_code == 429


def test_limite_padrao_e_por_conta_e_cai_no_ip_sem_sessao(app, criar_aluno):
    """Alunos no mesmo Wi-Fi não dividem o teto padrão, nem com o visitante anônimo."""
    primeiro, segundo = criar_aluno(), criar_aluno()
    cliente_primeiro, cliente_segundo, anonimo = app.test_client(), app.test_client(), app.test_client()
    _sessao(cliente_primeiro, 'aluno', primeiro)
    _sessao(cliente_segundo, 'aluno', segundo)

    assert _estourar(lambda: cliente_primeiro.get('/robots.txt'), 300).status_code == 429
    assert cliente_segundo.get('/robots.txt').status_code == 200
    assert anonimo.get('/robots.txt').status_code == 200


@pytest.mark.parametrize('caminho', ['/health', '/static/css/theme.css'])
def test_health_e_static_ficam_fora_do_limite_padrao(client, caminho):
    codigos = {client.get(caminho).status_code for _ in range(320)}
    assert codigos == {200}


# --------------------------------------------------------------------- login --

def test_login_tem_teto_por_usuario_mesmo_vindo_de_muitos_ips(client, monkeypatch):
    monkeypatch.setattr(usuario_bp.ProfessorDAO, 'autenticar', lambda *_args: None)
    monkeypatch.setattr(usuario_bp.AlunoDAO, 'autenticar', lambda *_args: None)
    monkeypatch.delenv('ADMIN_USER', raising=False)
    monkeypatch.delenv('ADMIN_PASSWORD_HASH', raising=False)
    ips = iter(f'198.51.100.{n}' for n in range(1, 50))

    def tentar(usuario='Alvo'):
        return client.post(
            '/login', data={'loginusuario': usuario, 'senhausuario': 'errada'},
            environ_base={'REMOTE_ADDR': next(ips)},
        )

    # Caixa e espaços não abrem uma cota nova para o mesmo usuário.
    assert _estourar(tentar, 10).status_code == 429
    assert tentar(' alvo ').status_code == 429
    assert tentar('outra-pessoa').status_code == 200


# ------------------------------------------------------------------ cadastro --

def test_cadastro_publico_aceita_20_por_hora_do_mesmo_ip(client):
    cpfs = iter(f'{n:011d}' for n in range(100, 200))

    def cadastrar():
        return client.post('/cadastrar', data={'cpfusuario': next(cpfs)})

    assert _estourar(cadastrar, 20).status_code == 429


def test_cadastro_publico_mantem_3_por_hora_por_cpf(client):
    def cadastrar():
        return client.post('/cadastrar', data={'cpfusuario': '52998224725'})

    assert _estourar(cadastrar, 3).status_code == 429


# ----------------------------------------------------- rotas por conta e por IP --

ROTAS_DO_ADMIN = [
    # E-mails em massa (SEC-12).
    ('/admin/avisos/cobranca', 5),
    ('/admin/avisos', 10),
    (f'/admin/usuario/{CPF_INEXISTENTE}/cobrar', 30),
    (f'/admin/usuario/{CPF_INEXISTENTE}/convite', 30),
    # Escritas do admin (SEC-16).
    ('/admin/gmail/desconectar', 10),
    ('/admin/mercado-pago/desconectar', 10),
    (f'/admin/usuario/{CPF_INEXISTENTE}/foto', 30),
    ('/admin/alunos/novo', 30),
    (f'/admin/usuario/{CPF_INEXISTENTE}/pagamentos', 60),
    ('/admin/pagamentos/999999/status', 60),
    ('/admin/pagamentos/999999/comprovante-manual/aprovar', 60),
    ('/admin/pagamentos/999999/comprovante-manual/rejeitar', 60),
    ('/turmas/999999/matricular', 60),
    ('/turmas/999999/presenca', 60),
]


@pytest.mark.parametrize('rota,limite', ROTAS_DO_ADMIN)
def test_escritas_do_admin_tem_limite(client, rota, limite):
    _sessao(client, 'admin')
    assert _estourar(lambda: client.post(rota), limite).status_code == 429


def test_limite_do_admin_segue_a_conta_e_nao_o_ip(app):
    """Trocar de rede ou abrir outra sessão não devolve a cota de e-mails em massa."""
    primeiro = app.test_client()
    _sessao(primeiro, 'admin')
    assert _estourar(lambda: primeiro.post('/admin/avisos/cobranca'), 5).status_code == 429

    outra_rede = app.test_client()
    _sessao(outra_rede, 'admin')
    resposta = outra_rede.post('/admin/avisos/cobranca', environ_base={'REMOTE_ADDR': '203.0.113.50'})
    assert resposta.status_code == 429


def test_tela_de_avisos_continua_abrindo_depois_do_limite_de_envio(client):
    _sessao(client, 'admin')
    assert _estourar(lambda: client.post('/admin/avisos'), 10).status_code == 429
    assert client.get('/admin/avisos').status_code == 200


ROTAS_DO_ALUNO = [
    ('post', '/perfil/presencas/999999/confirmar', 30),
    ('post', '/perfil/plano/mudanca/999999/cancelar', 10),
    ('post', '/perfil/foto/remover', 20),
    ('get', '/perfil/mensalidade/999999/checkout/continuar', 30),
]


@pytest.mark.parametrize('metodo,rota,limite', ROTAS_DO_ALUNO)
def test_escritas_do_aluno_tem_limite(client, criar_aluno, metodo, rota, limite):
    _sessao(client, 'aluno', criar_aluno())
    enviar = getattr(client, metodo)
    assert _estourar(lambda: enviar(rota), limite).status_code == 429


def test_limite_das_escritas_do_aluno_e_por_conta(app, criar_aluno):
    primeiro, segundo = app.test_client(), app.test_client()
    _sessao(primeiro, 'aluno', criar_aluno())
    _sessao(segundo, 'aluno', criar_aluno())

    assert _estourar(lambda: primeiro.post('/perfil/foto/remover'), 20).status_code == 429
    assert segundo.post('/perfil/foto/remover').status_code == 302


def test_link_de_verificacao_do_cadastro_tem_limite(client):
    tokens = iter(f'tentativa-{n}' for n in range(100))
    assert _estourar(lambda: client.get(f'/cadastro/verificar/{next(tokens)}'), 30).status_code == 429


def test_logout_tem_limite_por_ip(client):
    assert _estourar(lambda: client.post('/logout'), 60).status_code == 429
    assert client.post('/logout', environ_base={'REMOTE_ADDR': '203.0.113.7'}).status_code == 302


# ------------------------------------------------------- webhook do Mercado Pago --

def _webhook(client, data_id='mp-1', request_id='req-1'):
    ts = str(int(time.time()))
    manifesto = f'id:{data_id.lower()};request-id:{request_id};ts:{ts};'
    v1 = hmac.new(
        os.environ['MERCADO_PAGO_WEBHOOK_SECRET'].encode(), manifesto.encode(), hashlib.sha256,
    ).hexdigest()
    return client.post(
        f'/api/webhooks/mercado-pago?data.id={data_id}',
        headers={'x-signature': f'ts={ts},v1={v1}', 'x-request-id': request_id},
        json={'type': 'payment', 'data': {'id': data_id}},
    )


@pytest.fixture
def consultar_mp(monkeypatch):
    consulta = Mock(return_value={'sucesso': False, 'erro': 'não encontrado'})
    monkeypatch.setattr(pix_bp, 'buscar_pagamento', consulta)
    return consulta


def test_webhook_tem_limite_por_ip(client):
    def sem_assinatura():
        return client.post('/api/webhooks/mercado-pago')

    assert _estourar(sem_assinatura, 120).status_code == 429


def test_webhook_repetido_responde_200_sem_reprocessar(client, consultar_mp):
    assert _webhook(client).status_code == 200
    assert _webhook(client).status_code == 200
    assert consultar_mp.call_count == 1

    # Outra notificação (outro x-request-id) continua sendo processada.
    assert _webhook(client, request_id='req-2').status_code == 200
    assert consultar_mp.call_count == 2


def test_webhook_com_assinatura_invalida_nao_queima_o_request_id(client, consultar_mp):
    resposta = client.post(
        '/api/webhooks/mercado-pago?data.id=mp-1',
        headers={'x-signature': f'ts={int(time.time())},v1=falsa', 'x-request-id': 'req-1'},
    )
    assert resposta.status_code == 401
    assert _webhook(client).status_code == 200
    assert consultar_mp.call_count == 1


def test_webhook_que_falhou_do_nosso_lado_e_reprocessado_no_reenvio(client, consultar_mp):
    consultar_mp.side_effect = [MercadoPagoIndisponivel('fora do ar'), {'sucesso': False, 'erro': 'x'}]

    assert _webhook(client).status_code == 503
    assert _webhook(client).status_code == 200
    assert consultar_mp.call_count == 2


def test_webhook_segue_se_o_storage_do_limitador_cair(client, consultar_mp, monkeypatch):
    class _StorageFora:
        def incr(self, *_args, **_kwargs):
            raise ConnectionError('redis fora')

    # Só a marca de entrega perde o storage; o limite por IP da rota segue o real.
    monkeypatch.setattr(pix_bp, 'limiter', SimpleNamespace(storage=_StorageFora()))
    assert _webhook(client).status_code == 200
    assert consultar_mp.call_count == 1


# ------------------------------------------------------------ Redis do compose --

def test_redis_do_rate_limit_nao_apaga_contadores_sob_carga():
    servico = yaml.safe_load((RAIZ / 'compose.yaml').read_text(encoding='utf-8'))['services']['rate-limit']
    comando = servico['command']

    assert comando[comando.index('--maxmemory-policy') + 1] == 'volatile-ttl'
    assert comando[comando.index('--maxmemory') + 1] == '64mb'
    # O container precisa caber o maxmemory e o próprio processo do Redis.
    assert int(servico['mem_limit'].rstrip('m')) > 64
