from datetime import datetime, timedelta

from dao.financeiroDAO import PagamentoDAO


def test_pix_ainda_valido_falso_sem_provider_payment_id(criar_pagamento):
    pagamento = criar_pagamento()
    assert PagamentoDAO.pix_ainda_valido(pagamento) is False


def test_pix_ainda_valido_true_dentro_da_validade(criar_pagamento):
    pagamento = criar_pagamento(
        provider='mercado_pago',
        provider_payment_id='123',
        data_expiracao=datetime.utcnow() + timedelta(minutes=10),
    )
    assert PagamentoDAO.pix_ainda_valido(pagamento) is True


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
