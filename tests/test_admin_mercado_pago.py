"""Painel do admin com mensalidades do Mercado Pago: formas de pagamento, sincronização
de cobranças do Checkout Pro e rótulos. Nenhum teste fala com o Mercado Pago real."""
from datetime import date, datetime, timedelta

import pytest

import blueprints.pix_bp as pix_bp
from dao.financeiroDAO import PagamentoDAO
from servicos.formatacao import rotulo_forma_pagamento


def _aprovado_no_checkout(referencia):
    return {
        'payment_id': 'mp-cartao-1', 'status': 'approved', 'status_detail': 'accredited',
        'external_reference': referencia, 'transaction_amount': 150.0, 'currency_id': 'BRL',
        'payment_method_id': 'master', 'payment_type_id': 'credit_card',
        'date_created': '2026-09-27T10:00:00.000-04:00', 'date_approved': '2026-09-27T10:01:00.000-04:00',
        'qr_code': None, 'qr_code_base64': None, 'ticket_url': None,
    }


def _so_com_checkout(criar_pagamento, referencia='checkout-ref'):
    """Cartão/boleto: a preferência existe, o webhook ainda não trouxe o payment_id."""
    pagamento = criar_pagamento(provider='mercado_pago')
    pagamento.checkout_preference_id = 'pref-1'
    pagamento.checkout_external_reference = referencia
    PagamentoDAO.salvar(pagamento)
    return pagamento


# ---------------------------------------------------------------------------
# Formas de pagamento
# ---------------------------------------------------------------------------


@pytest.mark.parametrize('forma', ['cartao_credito', 'cartao_debito'])
def test_admin_lanca_mensalidade_paga_no_cartao(client, criar_aluno, plano, logar_como_admin, forma):
    aluno = criar_aluno()
    logar_como_admin()

    client.post(f'/admin/usuario/{aluno.cpf}/pagamentos', data={
        'plano_id': plano.id, 'valor': '150.00', 'vencimento': date.today().isoformat(),
        'status': 'pago', 'forma_pagamento': forma, 'data_pagamento': date.today().isoformat(),
    })

    # O formulário oferecia cartão, mas o servidor recusava: "forma de pagamento inválida".
    [pagamento] = PagamentoDAO.listar_por_aluno(aluno.id)
    assert pagamento.forma_pagamento == forma


def test_admin_muda_o_status_sem_perder_a_forma_do_mercado_pago(client, criar_pagamento, logar_como_admin):
    pagamento = criar_pagamento(status='pago', forma_pagamento='saldo_mercado_pago',
                                data_pagamento=date.today(), provider='mercado_pago')
    logar_como_admin()

    client.post(f'/admin/pagamentos/{pagamento.id}/status',
                data={'status': 'reembolsado', 'forma_pagamento': 'saldo_mercado_pago'})

    atualizado = PagamentoDAO.buscar_por_id(pagamento.id)
    assert atualizado.status == 'reembolsado'
    assert atualizado.forma_pagamento == 'saldo_mercado_pago'


def test_admin_nao_grava_forma_inventada(client, criar_pagamento, logar_como_admin):
    pagamento = criar_pagamento()
    logar_como_admin()

    client.post(f'/admin/pagamentos/{pagamento.id}/status',
                data={'status': 'pago', 'forma_pagamento': 'qualquer-coisa'})

    atualizado = PagamentoDAO.buscar_por_id(pagamento.id)
    assert atualizado.status == 'pendente'
    assert atualizado.forma_pagamento is None


def test_forma_em_branco_fica_sem_forma(client, criar_pagamento, logar_como_admin):
    pagamento = criar_pagamento(forma_pagamento='pix')
    logar_como_admin()

    client.post(f'/admin/pagamentos/{pagamento.id}/status', data={'status': 'cancelado', 'forma_pagamento': ''})

    assert PagamentoDAO.buscar_por_id(pagamento.id).forma_pagamento is None


def test_aprovar_comprovante_recusa_forma_inventada(client, criar_pagamento, logar_como_admin):
    pagamento = criar_pagamento(status='em_analise')
    logar_como_admin()

    client.post(f'/admin/pagamentos/{pagamento.id}/comprovante-manual/aprovar',
                data={'forma_pagamento': 'x' * 80})

    assert PagamentoDAO.buscar_por_id(pagamento.id).status == 'em_analise'


def test_ficha_mantem_no_select_a_forma_confirmada_pelo_mercado_pago(client, criar_pagamento, logar_como_admin):
    pagamento = criar_pagamento(status='pago', forma_pagamento='saldo_mercado_pago',
                                data_pagamento=date.today(), provider='mercado_pago',
                                provider_payment_id='mp-saldo-1')
    logar_como_admin()

    pagina = client.get(f'/admin/usuario/{pagamento.aluno.cpf}').get_data(as_text=True)

    assert '<option value="saldo_mercado_pago" selected>Saldo Mercado Pago</option>' in pagina


def test_rotulos_das_formas_do_mercado_pago():
    assert rotulo_forma_pagamento('saldo_mercado_pago') == 'Saldo Mercado Pago'
    assert rotulo_forma_pagamento('cartao_pre_pago') == 'Cartão pré-pago'
    assert rotulo_forma_pagamento('mercado_pago') == 'Mercado Pago'


# ---------------------------------------------------------------------------
# Sincronizar com o Mercado Pago
# ---------------------------------------------------------------------------


def test_sincronizar_confirma_cartao_do_checkout_sem_payment_id(client, criar_pagamento, logar_como_admin,
                                                               monkeypatch):
    pagamento = _so_com_checkout(criar_pagamento)
    logar_como_admin()
    monkeypatch.setattr(pix_bp, 'buscar_pagamentos_por_referencia',
                        lambda referencia, **kw: {'sucesso': True, 'pagamentos': [_aprovado_no_checkout(referencia)]})

    resposta = client.post(f'/admin/pagamentos/{pagamento.id}/sincronizar', follow_redirects=True)

    assert 'Pendente → Paga' in resposta.get_data(as_text=True)
    atualizado = PagamentoDAO.buscar_por_id(pagamento.id)
    assert atualizado.status == 'pago'
    assert atualizado.forma_pagamento == 'cartao_credito'


def test_sincronizar_volta_para_a_ficha_do_aluno(client, criar_pagamento, logar_como_admin, monkeypatch):
    pagamento = _so_com_checkout(criar_pagamento)
    logar_como_admin()
    monkeypatch.setattr(pix_bp, 'buscar_pagamentos_por_referencia',
                        lambda referencia, **kw: {'sucesso': True, 'pagamentos': []})
    ficha = f'/admin/usuario/{pagamento.aluno.cpf}'

    resposta = client.post(f'/admin/pagamentos/{pagamento.id}/sincronizar',
                           headers={'Referer': f'http://localhost{ficha}'})

    assert resposta.headers['Location'] == ficha


def test_sincronizar_ignora_referer_de_outro_site(client, criar_pagamento, logar_como_admin, monkeypatch):
    pagamento = _so_com_checkout(criar_pagamento)
    logar_como_admin()
    monkeypatch.setattr(pix_bp, 'buscar_pagamentos_por_referencia',
                        lambda referencia, **kw: {'sucesso': True, 'pagamentos': []})

    resposta = client.post(f'/admin/pagamentos/{pagamento.id}/sincronizar',
                           headers={'Referer': 'https://outro-site.example/admin/usuario/1'})

    assert resposta.headers['Location'] == '/admin/financeiro'


def test_sincronizar_sem_cobranca_no_mercado_pago_avisa(client, criar_pagamento, logar_como_admin):
    pagamento = criar_pagamento()
    logar_como_admin()

    resposta = client.post(f'/admin/pagamentos/{pagamento.id}/sincronizar', follow_redirects=True)

    assert 'não tem cobrança do Mercado Pago' in resposta.get_data(as_text=True)


def test_telas_oferecem_sincronizar_para_cobranca_do_checkout(client, criar_pagamento, logar_como_admin):
    pagamento = _so_com_checkout(criar_pagamento)
    logar_como_admin()
    acao = f'action="/admin/pagamentos/{pagamento.id}/sincronizar"'

    ficha = client.get(f'/admin/usuario/{pagamento.aluno.cpf}').get_data(as_text=True)
    financeiro = client.get('/admin/financeiro').get_data(as_text=True)

    assert acao in ficha and acao in financeiro
    # Cartão e boleto também passam pelo Mercado Pago: a origem não é "Pix".
    assert 'Mercado Pago' in financeiro
