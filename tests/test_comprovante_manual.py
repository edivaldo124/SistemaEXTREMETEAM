import io

from dao.financeiroDAO import PagamentoDAO

PDF_VALIDO = b'%PDF-1.4\n%conteudo de teste\n'


def test_envio_de_comprovante_manual_fica_em_analise(client, criar_pagamento, logar_como_aluno):
    pagamento = criar_pagamento(status='pendente')
    logar_como_aluno(pagamento.aluno)

    resp = client.post(
        f'/perfil/mensalidade/{pagamento.id}/comprovante-manual',
        data={'comprovante': (io.BytesIO(PDF_VALIDO), 'comprovante.pdf', 'application/pdf')},
        content_type='multipart/form-data',
    )

    assert resp.status_code == 302
    atualizado = PagamentoDAO.buscar_por_id(pagamento.id)
    assert atualizado.status == 'em_analise'
    assert atualizado.comprovante_manual_arquivo is not None
    assert atualizado.comprovante_manual_arquivo.endswith('.pdf')

    arquivo = client.get(f'/perfil/mensalidade/{pagamento.id}/comprovante-manual/arquivo')
    assert arquivo.status_code == 200
    assert arquivo.headers['Content-Type'].startswith('application/pdf')
    assert arquivo.headers['Content-Disposition'].startswith('attachment;')


def test_envio_sozinho_nunca_marca_como_pago(client, criar_pagamento, logar_como_aluno):
    pagamento = criar_pagamento(status='pendente')
    logar_como_aluno(pagamento.aluno)

    client.post(
        f'/perfil/mensalidade/{pagamento.id}/comprovante-manual',
        data={'comprovante': (io.BytesIO(PDF_VALIDO), 'comprovante.pdf', 'application/pdf')},
        content_type='multipart/form-data',
    )

    assert PagamentoDAO.buscar_por_id(pagamento.id).status != 'pago'


def test_arquivo_invalido_e_recusado(client, criar_pagamento, logar_como_aluno):
    pagamento = criar_pagamento(status='pendente')
    logar_como_aluno(pagamento.aluno)

    resp = client.post(
        f'/perfil/mensalidade/{pagamento.id}/comprovante-manual',
        data={'comprovante': (io.BytesIO(b'conteudo qualquer'), 'comprovante.txt', 'text/plain')},
        content_type='multipart/form-data',
        follow_redirects=True,
    )

    assert resp.status_code == 200
    assert PagamentoDAO.buscar_por_id(pagamento.id).status == 'pendente'


def test_aluno_nao_envia_comprovante_de_outro_aluno(client, criar_pagamento, criar_aluno, logar_como_aluno):
    pagamento = criar_pagamento(status='pendente')
    outro = criar_aluno()
    logar_como_aluno(outro)

    resp = client.post(
        f'/perfil/mensalidade/{pagamento.id}/comprovante-manual',
        data={'comprovante': (io.BytesIO(PDF_VALIDO), 'comprovante.pdf', 'application/pdf')},
        content_type='multipart/form-data',
    )

    assert resp.status_code == 404
    assert PagamentoDAO.buscar_por_id(pagamento.id).status == 'pendente'


def test_admin_aprova_comprovante_manual(client, criar_pagamento, logar_como_aluno, logar_como_admin):
    pagamento = criar_pagamento(status='pendente')
    logar_como_aluno(pagamento.aluno)
    client.post(
        f'/perfil/mensalidade/{pagamento.id}/comprovante-manual',
        data={'comprovante': (io.BytesIO(PDF_VALIDO), 'comprovante.pdf', 'application/pdf')},
        content_type='multipart/form-data',
    )
    client.post('/logout')

    logar_como_admin()
    resp = client.post(
        f'/admin/pagamentos/{pagamento.id}/comprovante-manual/aprovar',
        data={'forma_pagamento': 'transferencia', 'observacao': 'confirmado no extrato'},
    )

    assert resp.status_code == 302
    atualizado = PagamentoDAO.buscar_por_id(pagamento.id)
    assert atualizado.status == 'pago'
    assert atualizado.comprovante_manual_analisado_por == 'admin-teste'
    tipos_evento = [e.tipo for e in atualizado.eventos]
    assert 'comprovante_aprovado' in tipos_evento


def test_admin_rejeita_comprovante_manual_volta_para_pendente(client, criar_pagamento, logar_como_aluno, logar_como_admin):
    pagamento = criar_pagamento(status='pendente')
    logar_como_aluno(pagamento.aluno)
    client.post(
        f'/perfil/mensalidade/{pagamento.id}/comprovante-manual',
        data={'comprovante': (io.BytesIO(PDF_VALIDO), 'comprovante.pdf', 'application/pdf')},
        content_type='multipart/form-data',
    )
    client.post('/logout')

    logar_como_admin()
    resp = client.post(
        f'/admin/pagamentos/{pagamento.id}/comprovante-manual/rejeitar',
        data={'observacao': 'comprovante ilegível'},
    )

    assert resp.status_code == 302
    atualizado = PagamentoDAO.buscar_por_id(pagamento.id)
    assert atualizado.status == 'pendente'
    assert atualizado.comprovante_manual_observacao == 'comprovante ilegível'


def test_aluno_nao_acessa_arquivo_de_comprovante_de_outro(client, criar_pagamento, criar_aluno, logar_como_aluno):
    pagamento = criar_pagamento(status='pendente')
    logar_como_aluno(pagamento.aluno)
    client.post(
        f'/perfil/mensalidade/{pagamento.id}/comprovante-manual',
        data={'comprovante': (io.BytesIO(PDF_VALIDO), 'comprovante.pdf', 'application/pdf')},
        content_type='multipart/form-data',
    )
    client.post('/logout')

    outro = criar_aluno()
    logar_como_aluno(outro)
    resp = client.get(f'/perfil/mensalidade/{pagamento.id}/comprovante-manual/arquivo')
    assert resp.status_code == 404
