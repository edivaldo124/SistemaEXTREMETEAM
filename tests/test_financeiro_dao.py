from datetime import date, datetime, timedelta
from decimal import Decimal

from dao.financeiroDAO import PagamentoDAO


def test_pix_ainda_valido_falso_sem_provider_payment_id(criar_pagamento):
    pagamento = criar_pagamento()
    assert PagamentoDAO.pix_ainda_valido(pagamento) is False


def test_pix_ainda_valido_true_dentro_da_validade(criar_pagamento):
    pagamento = criar_pagamento(
        provider='mercado_pago',
        provider_payment_id='123',
        pix_copia_cola='00020126-copia-cola',
        data_expiracao=datetime.utcnow() + timedelta(minutes=10),
    )
    assert PagamentoDAO.pix_ainda_valido(pagamento) is True


def test_pix_ainda_valido_falso_sem_copia_e_cola(criar_pagamento):
    """provider_payment_id sozinho não basta: pagamentos do Checkout Pro (cartão/boleto)
    também preenchem esse campo e não têm copia-e-cola para reaproveitar."""
    pagamento = criar_pagamento(
        provider='mercado_pago',
        provider_payment_id='mp-boleto-do-checkout',
        data_expiracao=datetime.utcnow() + timedelta(minutes=10),
    )
    assert PagamentoDAO.pix_ainda_valido(pagamento) is False


def test_pix_ainda_valido_falso_apos_expirar(criar_pagamento):
    pagamento = criar_pagamento(
        provider='mercado_pago',
        provider_payment_id='123',
        data_expiracao=datetime.utcnow() - timedelta(minutes=1),
    )
    assert PagamentoDAO.pix_ainda_valido(pagamento) is False


def test_pix_ainda_valido_falso_quando_ja_pago(criar_pagamento):
    pagamento = criar_pagamento(
        status='pago',
        provider='mercado_pago',
        provider_payment_id='123',
        data_expiracao=datetime.utcnow() + timedelta(minutes=10),
    )
    assert PagamentoDAO.pix_ainda_valido(pagamento) is False


def test_marcar_pago_via_webhook_sincroniza_mensalidade_do_aluno(criar_pagamento):
    pagamento = criar_pagamento()
    aluno = pagamento.aluno
    aluno.mensalidade = 'Pendente'

    PagamentoDAO.marcar_pago_via_webhook(pagamento, data_pagamento=datetime.utcnow().date())

    assert pagamento.status == 'pago'
    assert pagamento.forma_pagamento == 'pix'
    assert aluno.mensalidade == 'Em Dia'


def test_marcar_reembolsado_via_webhook_sincroniza_mensalidade_do_aluno(criar_pagamento):
    pagamento = criar_pagamento(status='pago')
    aluno = pagamento.aluno
    aluno.mensalidade = 'Em Dia'

    PagamentoDAO.marcar_reembolsado_via_webhook(pagamento)

    assert pagamento.status == 'reembolsado'
    assert aluno.mensalidade == 'Pendente'


def test_valor_do_pagamento_e_decimal_nao_float(criar_pagamento):
    pagamento = criar_pagamento(valor=99.9)
    assert isinstance(pagamento.valor, Decimal)


def test_totais_periodo_soma_apenas_o_que_bate_com_o_status(criar_pagamento):
    criar_pagamento(status='pago', valor=100.0, data_pagamento=date.today())
    criar_pagamento(status='pendente', valor=50.0)
    criar_pagamento(status='atrasado', valor=30.0)
    criar_pagamento(status='em_analise', valor=20.0)

    totais = PagamentoDAO.totais_periodo()

    assert totais['total_recebido'] == Decimal('100.00')
    assert totais['total_pendente'] == Decimal('50.00')
    assert totais['total_vencido'] == Decimal('30.00')
    assert totais['total_em_analise'] == Decimal('20.00')
    assert totais['alunos_inadimplentes'] == 1


def test_listar_filtrado_por_status_e_busca_de_aluno(criar_aluno, criar_pagamento):
    aluno_alvo = criar_aluno(nome='Maria Muay Thai')
    criar_pagamento(aluno=aluno_alvo, status='pago', valor=100.0)
    criar_pagamento(status='pendente', valor=50.0)

    resultado = PagamentoDAO.listar_filtrado(status='pago')
    assert len(resultado) == 1
    assert resultado[0].aluno_id == aluno_alvo.id

    resultado_busca = PagamentoDAO.listar_filtrado(busca_aluno='Muay')
    assert len(resultado_busca) == 1
    assert resultado_busca[0].aluno_id == aluno_alvo.id


def test_mensalidade_destaque_prioriza_a_mais_proxima_de_vencer(criar_pagamento):
    from dao.financeiroDAO import mensalidade_destaque

    aluno = criar_pagamento(status='pendente', vencimento=date.today() + timedelta(days=20)).aluno
    proxima = criar_pagamento(aluno=aluno, status='pendente', vencimento=date.today() + timedelta(days=2))

    pagamentos = PagamentoDAO.listar_por_aluno(aluno.id)
    destaque = mensalidade_destaque(pagamentos)

    assert destaque.id == proxima.id
