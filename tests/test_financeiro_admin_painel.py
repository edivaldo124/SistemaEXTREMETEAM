from dao.financeiroDAO import PagamentoDAO


def test_painel_financeiro_exige_admin(client, logar_como_aluno, criar_aluno):
    aluno = criar_aluno()
    logar_como_aluno(aluno)

    resp = client.get('/admin/financeiro')
    assert resp.status_code == 302
    assert '/login' in resp.headers['Location']


def test_painel_financeiro_mostra_totais_do_backend(client, logar_como_admin, criar_pagamento):
    criar_pagamento(status='pago', valor=100.0)
    criar_pagamento(status='pendente', valor=50.0)
    logar_como_admin()

    resp = client.get('/admin/financeiro')

    assert resp.status_code == 200
    assert 'R$ 100,00'.encode() in resp.data
    assert 'R$ 50,00'.encode() in resp.data


def test_painel_financeiro_filtra_por_status(client, logar_como_admin, criar_aluno, criar_pagamento):
    aluno_pago = criar_aluno(nome='Aluno Pago')
    aluno_pendente = criar_aluno(nome='Aluno Pendente')
    criar_pagamento(aluno=aluno_pago, status='pago', valor=100.0)
    criar_pagamento(aluno=aluno_pendente, status='pendente', valor=50.0)
    logar_como_admin()

    resp = client.get('/admin/financeiro?status=pago')

    assert resp.status_code == 200
    assert b'Aluno Pago' in resp.data
    assert b'Aluno Pendente' not in resp.data


def test_painel_financeiro_busca_por_nome_do_aluno(client, logar_como_admin, criar_aluno, criar_pagamento):
    alvo = criar_aluno(nome='Joana Muay Thai')
    outro = criar_aluno(nome='Carlos Boxe')
    criar_pagamento(aluno=alvo, status='pendente', valor=80.0)
    criar_pagamento(aluno=outro, status='pendente', valor=80.0)
    logar_como_admin()

    resp = client.get('/admin/financeiro?busca_aluno=Joana')

    assert resp.status_code == 200
    assert b'Joana Muay Thai' in resp.data
    assert b'Carlos Boxe' not in resp.data


def test_busca_financeira_trata_curingas_como_texto(client, logar_como_admin, criar_aluno, criar_pagamento):
    nome_com_percentual = criar_aluno(nome='Equipe 100%')
    outro = criar_aluno(nome='Equipe comum')
    criar_pagamento(aluno=nome_com_percentual)
    criar_pagamento(aluno=outro)
    logar_como_admin()

    resp = client.get('/admin/financeiro?busca_aluno=%25')

    assert resp.status_code == 200
    assert b'Equipe 100%' in resp.data
    assert b'Equipe comum' not in resp.data
