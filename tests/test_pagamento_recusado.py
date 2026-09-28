"""Mensalidade recusada: a próxima tentativa do aluno a reabre, e a recusa antiga que o
Mercado Pago continua listando não a derruba de novo.

Antes, um cartão recusado no Checkout Pro deixava a tela de pagamento presa em
"Pagamento recusado": o Pix novo era gerado, mas a mensalidade seguia recusada e o
polling reaplicava a recusa a cada 5 segundos. Nenhum teste fala com o Mercado Pago real.
"""
import hashlib
import hmac
import os
import time
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import blueprints.checkout_bp as checkout_bp
import blueprints.pix_bp as pix_bp
from dao.financeiroDAO import EVENTO_NOVA_TENTATIVA, PagamentoDAO
from modelos.pagamento_evento import PagamentoEvento
from servicos.mercado_pago import MercadoPagoIndisponivel

# As datas da API do Mercado Pago vêm em -04:00.
FUSO_MP = ZoneInfo('America/Manaus')
URL_CHECKOUT = 'https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=pref-1'


def _data_mp(deslocamento=timedelta()):
    return (datetime.now(FUSO_MP) + deslocamento).isoformat(timespec='milliseconds')


def _pix_criado(payment_id='mp-pix-novo'):
    return {
        'sucesso': True, 'payment_id': payment_id, 'status': 'pending',
        'qr_code': '00020126-novo', 'qr_code_base64': 'YmFzZTY0',
        'ticket_url': 'https://mp.example/ticket',
        'data_expiracao': datetime.utcnow() + timedelta(minutes=30),
    }


def _pagamento_mp(status, *, referencia=None, payment_id='mp-1', criado_em=None, tipo='credit_card'):
    return {
        'payment_id': payment_id, 'status': status, 'status_detail': f'{status}_detail',
        'external_reference': referencia, 'transaction_amount': 150.0, 'currency_id': 'BRL',
        'payment_method_id': 'master' if tipo == 'credit_card' else 'pix', 'payment_type_id': tipo,
        'date_created': criado_em, 'date_approved': _data_mp() if status == 'approved' else None,
        'qr_code': None, 'qr_code_base64': None, 'ticket_url': None,
    }


def _recusada_no_checkout(criar_pagamento, **campos):
    """Mensalidade cujo cartão acabou de ser recusado no Checkout Pro."""
    pagamento = criar_pagamento(status='recusado', provider='mercado_pago', **campos)
    pagamento.checkout_preference_id = 'pref-1'
    pagamento.checkout_external_reference = 'checkout-ref'
    pagamento.checkout_url = URL_CHECKOUT
    pagamento.checkout_ambiente = 'producao'
    pagamento.checkout_valor = pagamento.valor
    pagamento.checkout_expira_em = datetime.utcnow() + timedelta(minutes=30)
    PagamentoDAO.salvar(pagamento)
    return pagamento


def _mockar_mp(monkeypatch, *, pix=None, busca=None, criar=None):
    """pix: resposta da consulta do Pix; busca: pagamentos do checkout; criar: emissão do Pix."""
    if pix is not None:
        monkeypatch.setattr(pix_bp, 'buscar_pagamento', lambda payment_id, **kw: {'sucesso': True, **pix})
    if busca is not None:
        monkeypatch.setattr(pix_bp, 'buscar_pagamentos_por_referencia',
                            lambda referencia, **kw: {'sucesso': True, 'pagamentos': list(busca)})
    if criar is not None:
        monkeypatch.setattr(pix_bp, 'criar_pagamento_pix', criar)
    monkeypatch.setattr(pix_bp, 'cancelar_pagamento', lambda payment_id: None)


def _eventos(pagamento_id, tipo):
    return PagamentoEvento.query.filter_by(pagamento_id=pagamento_id, tipo=tipo).count()


def _assinar(data_id, request_id='req-1'):
    ts = str(int(time.time()))
    manifest = f'id:{data_id.lower()};request-id:{request_id};ts:{ts};'
    v1 = hmac.new(os.environ['MERCADO_PAGO_WEBHOOK_SECRET'].encode(), manifest.encode(), hashlib.sha256).hexdigest()
    return {'x-signature': f'ts={ts},v1={v1}', 'x-request-id': request_id}


# ---------------------------------------------------------------------------
# Nova tentativa pelo Pix
# ---------------------------------------------------------------------------


def test_pix_depois_do_cartao_recusado_reabre_e_nao_volta_a_recusado(client, criar_pagamento, monkeypatch,
                                                                     logar_como_aluno):
    pagamento = _recusada_no_checkout(criar_pagamento)
    logar_como_aluno(pagamento.aluno)
    recusa_antiga = _pagamento_mp('rejected', referencia='checkout-ref', criado_em=_data_mp(-timedelta(minutes=10)))
    _mockar_mp(monkeypatch, criar=lambda **kw: _pix_criado(), busca=[recusa_antiga],
               pix=_pagamento_mp('pending', payment_id='mp-pix-novo', tipo='bank_transfer'))

    criado = client.post(f'/api/mensalidades/{pagamento.id}/pix')

    assert criado.status_code == 200
    assert criado.get_json()['status'] == 'pendente'
    assert criado.get_json()['pix_copia_cola'] == '00020126-novo'
    assert _eventos(pagamento.id, EVENTO_NOVA_TENTATIVA) == 1

    # O polling ainda encontra a recusa do cartão pela referência do checkout.
    for _ in range(3):
        status = client.get(f'/api/mensalidades/{pagamento.id}/status')
        assert status.get_json()['status'] == 'pendente'
    assert PagamentoDAO.buscar_por_id(pagamento.id).status == 'pendente'
    assert _eventos(pagamento.id, 'webhook_recusado') == 0


def test_recusa_nova_depois_da_nova_tentativa_continua_valendo(client, criar_pagamento, monkeypatch,
                                                               logar_como_aluno):
    pagamento = _recusada_no_checkout(criar_pagamento)
    logar_como_aluno(pagamento.aluno)
    _mockar_mp(monkeypatch, criar=lambda **kw: _pix_criado(), busca=[],
               pix=_pagamento_mp('pending', payment_id='mp-pix-novo', tipo='bank_transfer'))
    client.post(f'/api/mensalidades/{pagamento.id}/pix')

    # O aluno volta ao checkout e o cartão é recusado outra vez, agora.
    recusa_nova = _pagamento_mp('rejected', referencia='checkout-ref', payment_id='mp-2',
                                criado_em=_data_mp(timedelta(minutes=1)))
    _mockar_mp(monkeypatch, busca=[recusa_nova])

    resposta = client.get(f'/api/mensalidades/{pagamento.id}/status')

    assert resposta.get_json()['status'] == 'recusado'


def test_pix_aberto_reoferecido_tambem_reabre_a_mensalidade(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = _recusada_no_checkout(
        criar_pagamento, provider_payment_id='mp-pix-aberto', external_reference='mensalidade-pix',
        pix_copia_cola='00020126-aberto', data_expiracao=datetime.utcnow() + timedelta(minutes=20),
    )
    logar_como_aluno(pagamento.aluno)
    emissoes = []
    recusa_antiga = _pagamento_mp('rejected', referencia='checkout-ref', criado_em=_data_mp(-timedelta(minutes=5)))
    _mockar_mp(
        monkeypatch, criar=lambda **kw: emissoes.append(kw) or _pix_criado(), busca=[recusa_antiga],
        pix=_pagamento_mp('pending', referencia='mensalidade-pix', payment_id='mp-pix-aberto', tipo='bank_transfer'),
    )

    resposta = client.post(f'/api/mensalidades/{pagamento.id}/pix')

    assert resposta.get_json()['status'] == 'pendente'
    assert resposta.get_json()['pix_copia_cola'] == '00020126-aberto'
    assert emissoes == []
    assert client.get(f'/api/mensalidades/{pagamento.id}/status').get_json()['status'] == 'pendente'


def test_falha_ao_gerar_o_pix_nao_reabre_a_mensalidade(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = _recusada_no_checkout(criar_pagamento)
    logar_como_aluno(pagamento.aluno)

    def _fora_do_ar(**kwargs):
        raise MercadoPagoIndisponivel('fora do ar')

    _mockar_mp(monkeypatch, criar=_fora_do_ar)

    resposta = client.post(f'/api/mensalidades/{pagamento.id}/pix')

    assert resposta.status_code == 503
    assert PagamentoDAO.buscar_por_id(pagamento.id).status == 'recusado'
    assert _eventos(pagamento.id, EVENTO_NOVA_TENTATIVA) == 0


def test_mensalidade_vencida_reabre_como_atrasada(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = _recusada_no_checkout(criar_pagamento, vencimento=date.today() - timedelta(days=3))
    logar_como_aluno(pagamento.aluno)
    _mockar_mp(monkeypatch, criar=lambda **kw: _pix_criado(), busca=[])

    resposta = client.post(f'/api/mensalidades/{pagamento.id}/pix')

    assert resposta.get_json()['status'] == 'atrasado'


# ---------------------------------------------------------------------------
# Nova tentativa pelo checkout e webhook atrasado
# ---------------------------------------------------------------------------


def test_voltar_ao_checkout_reabre_a_mensalidade(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = _recusada_no_checkout(criar_pagamento)
    logar_como_aluno(pagamento.aluno)
    monkeypatch.setattr(checkout_bp, 'ambiente_mercado_pago', lambda: 'producao')

    resposta = client.post(f'/perfil/mensalidade/{pagamento.id}/checkout', headers={'Accept': 'application/json'})

    # A preferência ainda vale e é reaproveitada; a mensalidade volta a aguardar pagamento.
    assert resposta.get_json() == {'url_checkout': URL_CHECKOUT}
    assert PagamentoDAO.buscar_por_id(pagamento.id).status == 'pendente'
    assert _eventos(pagamento.id, EVENTO_NOVA_TENTATIVA) == 1


def test_webhook_atrasado_da_recusa_antiga_nao_derruba_a_nova_tentativa(client, criar_pagamento, monkeypatch,
                                                                       logar_como_aluno):
    pagamento = _recusada_no_checkout(criar_pagamento)
    logar_como_aluno(pagamento.aluno)
    _mockar_mp(monkeypatch, criar=lambda **kw: _pix_criado(), busca=[])
    client.post(f'/api/mensalidades/{pagamento.id}/pix')

    _mockar_mp(monkeypatch, pix=_pagamento_mp('rejected', referencia='checkout-ref', payment_id='mp-cartao',
                                              criado_em=_data_mp(-timedelta(minutes=10))))
    resposta = client.post('/api/webhooks/mercado-pago?data.id=mp-cartao', headers=_assinar('mp-cartao'),
                           json={'type': 'payment', 'data': {'id': 'mp-cartao'}})

    assert resposta.status_code == 200
    assert PagamentoDAO.buscar_por_id(pagamento.id).status == 'pendente'


# ---------------------------------------------------------------------------
# Eventos sem repetição
# ---------------------------------------------------------------------------


def test_polling_em_processamento_grava_um_evento_so(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento(provider='mercado_pago', provider_payment_id='mp-cartao', external_reference='ref-1')
    logar_como_aluno(pagamento.aluno)
    _mockar_mp(monkeypatch, pix=_pagamento_mp('in_process', referencia='ref-1', payment_id='mp-cartao'))

    for _ in range(4):
        assert client.get(f'/api/mensalidades/{pagamento.id}/status').get_json()['status'] == 'em_processamento'

    assert _eventos(pagamento.id, 'webhook_em_processamento') == 1


def test_recusa_consultada_varias_vezes_grava_um_evento_so(client, criar_pagamento, monkeypatch, logar_como_aluno):
    pagamento = criar_pagamento(provider='mercado_pago')
    pagamento.checkout_external_reference = 'checkout-ref'
    PagamentoDAO.salvar(pagamento)
    logar_como_aluno(pagamento.aluno)
    _mockar_mp(monkeypatch, busca=[_pagamento_mp('rejected', referencia='checkout-ref', criado_em=_data_mp())])

    for _ in range(3):
        client.get(f'/api/mensalidades/{pagamento.id}/status')

    assert PagamentoDAO.buscar_por_id(pagamento.id).status == 'recusado'
    assert _eventos(pagamento.id, 'webhook_recusado') == 1


# ---------------------------------------------------------------------------
# Datas vindas do Mercado Pago
# ---------------------------------------------------------------------------


def test_pix_pago_logo_depois_da_meia_noite_fica_no_dia_certo():
    # 23:30 em -04:00 é 00:30 do dia seguinte em Brasília.
    assert pix_bp._data_da_aprovacao('2026-09-27T23:30:00.000-04:00') == date(2026, 9, 28)
    assert pix_bp._data_da_aprovacao('2026-09-27T10:00:00.000-04:00') == date(2026, 9, 27)
    assert pix_bp._data_da_aprovacao('') is None


def test_entre_duas_recusas_vale_a_mais_recente():
    antiga = _pagamento_mp('rejected', payment_id='antiga', criado_em='2026-09-27T10:00:00.000-04:00')
    nova = _pagamento_mp('rejected', payment_id='nova', criado_em='2026-09-27T11:00:00.000-04:00')
    aprovado = _pagamento_mp('approved', payment_id='aprovado', criado_em='2026-09-27T09:00:00.000-04:00')

    assert pix_bp._pagamento_mp_mais_relevante([antiga, nova])['payment_id'] == 'nova'
    assert pix_bp._pagamento_mp_mais_relevante([nova, antiga])['payment_id'] == 'nova'
    # Aprovação continua valendo mais que qualquer recusa, mesmo mais antiga.
    assert pix_bp._pagamento_mp_mais_relevante([nova, aprovado])['payment_id'] == 'aprovado'


def test_validade_do_pix_sai_com_fuso_para_o_navegador(client, criar_pagamento, logar_como_aluno):
    pagamento = criar_pagamento(status='pago', data_expiracao=datetime(2026, 9, 27, 18, 30))
    logar_como_aluno(pagamento.aluno)

    dados = client.get(f'/api/mensalidades/{pagamento.id}/status').get_json()

    # Sem o fuso o JavaScript lia 18:30 como hora local; o Pix vencia às 15:30 de Brasília.
    assert dados['data_expiracao'] == '2026-09-27T18:30:00+00:00'
