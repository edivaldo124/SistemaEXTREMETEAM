"""Auditoria de segurança: sondas escritas para TENTAR quebrar as regras.

Nenhum teste aqui fala com a API real do Mercado Pago - o serviço é sempre simulado,
e o banco é o SQLite temporário isolado do conftest. Cada teste documenta a hipótese
de ataque que ele tenta confirmar.
"""
import hashlib
import hmac
import time
from datetime import datetime, timedelta

import pytest

import blueprints.checkout_bp as checkout_bp
import blueprints.pix_bp as pix_bp
from dao.financeiroDAO import PagamentoDAO
from modelos.professor import Professor
from dao.professorDAO import ProfessorDAO
from servicos.mercado_pago import url_checkout_permitida, validar_assinatura_webhook
from servicos.autorizacao import impressao_credencial

JSON = {'Accept': 'application/json'}

URL_MP = 'https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=pref-1'


def _pagamento_mp(**over):
    base = {
        'payment_id': 'mp-1', 'status': 'approved', 'status_detail': 'accredited',
        'external_reference': None, 'transaction_amount': 150.0, 'currency_id': 'BRL',
        'payment_method_id': 'master', 'payment_type_id': 'credit_card',
        'date_approved': '2026-09-04T10:00:00.000-03:00',
        'qr_code': None, 'qr_code_base64': None, 'ticket_url': None,
    }
    base.update(over)
    return base


def _assinar(data_id, secret, request_id='req-1', ts=None):
    ts = ts or str(int(time.time()))
    manifest = f'id:{str(data_id).lower()};request-id:{request_id};ts:{ts};'
    v1 = hmac.new(secret.encode(), manifest.encode(), hashlib.sha256).hexdigest()
    return {'x-signature': f'ts={ts},v1={v1}', 'x-request-id': request_id}


@pytest.fixture
def logar_como_professor(client, contexto_app):
    def _logar(login='prof-auditoria'):
        professor = Professor(nome='Professor Auditoria', login=login, senha='senha123456')
        ProfessorDAO.salvar(professor)
        with client.session_transaction() as sess:
            sess['usuario'] = professor.login
            sess['professor_id'] = professor.id
            sess['tipo_usuario'] = 'professor'
            sess['credencial'] = impressao_credencial(professor.senha_hash)
        return professor
    return _logar


# ===========================================================================
# H1 - Trocar o ID da cobrança para alcançar a de outro aluno
# ===========================================================================

ROTAS_DE_COBRANCA = [
    ('GET', '/perfil/pagamento/{id}'),
    ('GET', '/perfil/mensalidade/{id}/comprovante'),
    ('GET', '/perfil/mensalidade/{id}/comprovante-manual/arquivo'),
    ('GET', '/perfil/mensalidade/{id}/retorno-checkout'),
    ('GET', '/perfil/mensalidade/{id}/checkout/continuar'),
    ('POST', '/perfil/mensalidade/{id}/checkout'),
    ('POST', '/api/mensalidades/{id}/pix'),
    ('GET', '/api/mensalidades/{id}/status'),
]


@pytest.mark.parametrize('metodo,rota', ROTAS_DE_COBRANCA)
def test_aluno_nao_alcanca_cobranca_de_outro_aluno(
    client, criar_pagamento, criar_aluno, logar_como_aluno, metodo, rota,
):
    """Hipótese: trocar o id na URL dá acesso à cobrança de outra pessoa."""
    alvo = criar_pagamento()
    intruso = criar_aluno()
    logar_como_aluno(intruso)

    caminho = rota.format(id=alvo.id)
    resposta = client.open(caminho, method=metodo, headers=JSON)

    assert resposta.status_code in (403, 404), (
        f'{metodo} {caminho} respondeu {resposta.status_code} para a cobrança de outro aluno'
    )
    corpo = resposta.get_data(as_text=True)
    assert alvo.aluno.nome not in corpo
    assert alvo.aluno.email not in corpo


@pytest.mark.parametrize('metodo,rota', ROTAS_DE_COBRANCA)
def test_visitante_sem_sessao_nao_alcanca_cobranca(client, criar_pagamento, metodo, rota):
    """Hipótese: as rotas de cobrança respondem sem sessão nenhuma."""
    pagamento = criar_pagamento()
    resposta = client.open(rota.format(id=pagamento.id), method=metodo, headers=JSON)
    assert resposta.status_code in (302, 401, 403, 404), resposta.status_code
    if resposta.status_code == 302:
        assert '/login' in resposta.headers['Location']


@pytest.mark.parametrize('metodo,rota', ROTAS_DE_COBRANCA)
def test_professor_nao_alcanca_cobranca_de_aluno(
    client, criar_pagamento, logar_como_professor, metodo, rota,
):
    """Hipótese: a sessão de professor é aceita nas rotas financeiras do aluno."""
    pagamento = criar_pagamento()
    logar_como_professor()
    resposta = client.open(rota.format(id=pagamento.id), method=metodo, headers=JSON)
    assert resposta.status_code in (302, 401, 403, 404), resposta.status_code


# ===========================================================================
# H2 - CSRF nos POSTs, inclusive quando enviados por fetch
# ===========================================================================

def test_abrir_checkout_por_fetch_exige_csrf(app, criar_pagamento, logar_como_aluno):
    """Hipótese: como o JS agora usa fetch, o POST perdeu a exigência de CSRF."""
    pagamento = criar_pagamento()
    app.config['WTF_CSRF_ENABLED'] = True
    try:
        cliente = app.test_client()
        with cliente.session_transaction() as sess:
            sess['usuario'] = pagamento.aluno.login
            sess['aluno_id'] = pagamento.aluno_id
            sess['tipo_usuario'] = 'aluno'
        resposta = cliente.post(f'/perfil/mensalidade/{pagamento.id}/checkout', headers=JSON)
        assert resposta.status_code == 400, 'POST sem csrf_token deveria ser recusado'
    finally:
        app.config['WTF_CSRF_ENABLED'] = False


def test_pix_e_comprovante_manual_exigem_csrf(app, criar_pagamento):
    """Hipótese: as demais rotas de dinheiro aceitam POST sem token."""
    pagamento = criar_pagamento()
    app.config['WTF_CSRF_ENABLED'] = True
    try:
        cliente = app.test_client()
        with cliente.session_transaction() as sess:
            sess['usuario'] = pagamento.aluno.login
            sess['aluno_id'] = pagamento.aluno_id
            sess['tipo_usuario'] = 'aluno'
        for caminho in (
            f'/api/mensalidades/{pagamento.id}/pix',
            f'/perfil/mensalidade/{pagamento.id}/comprovante-manual',
        ):
            assert cliente.post(caminho, headers=JSON).status_code == 400, caminho
    finally:
        app.config['WTF_CSRF_ENABLED'] = False


def test_webhook_permanece_isento_de_csrf_mas_exige_assinatura(client, monkeypatch):
    """O webhook precisa ser isento de CSRF (vem de fora); a assinatura é a barreira."""
    monkeypatch.setenv('MERCADO_PAGO_WEBHOOK_SECRET', 'segredo-de-teste')
    resposta = client.post('/api/webhooks/mercado-pago?data.id=1',
                           json={'type': 'payment'},
                           headers={'x-signature': 'ts=1,v1=abc', 'x-request-id': 'r'})
    assert resposta.status_code == 401, 'assinatura inválida deveria ser recusada'


# ===========================================================================
# H3 - Cobranças que não estão em aberto
# ===========================================================================

@pytest.mark.parametrize('status', ['pago', 'cancelado', 'reembolsado', 'em_analise', 'em_processamento'])
def test_checkout_recusa_cobranca_indisponivel(
    client, criar_pagamento, logar_como_aluno, monkeypatch, status,
):
    """Hipótese: dá para abrir um checkout novo sobre uma cobrança já resolvida."""
    pagamento = criar_pagamento(status=status)
    logar_como_aluno(pagamento.aluno)

    def _nao_deveria_chamar(**kwargs):
        pytest.fail('criou preferência no Mercado Pago para cobrança indisponível')

    monkeypatch.setattr(checkout_bp, 'criar_preferencia_checkout', _nao_deveria_chamar)
    resposta = client.post(f'/perfil/mensalidade/{pagamento.id}/checkout', headers=JSON)
    assert resposta.status_code == 409


@pytest.mark.parametrize('status', ['pago', 'cancelado', 'reembolsado', 'em_analise', 'em_processamento'])
def test_pix_recusa_cobranca_indisponivel(
    client, criar_pagamento, logar_como_aluno, monkeypatch, status,
):
    pagamento = criar_pagamento(status=status)
    logar_como_aluno(pagamento.aluno)

    def _nao_deveria_chamar(**kwargs):
        pytest.fail('criou cobrança Pix para mensalidade indisponível')

    monkeypatch.setattr(pix_bp, 'criar_pagamento_pix', _nao_deveria_chamar)
    resposta = client.post(f'/api/mensalidades/{pagamento.id}/pix', headers=JSON)
    assert resposta.status_code == 409


# ===========================================================================
# H4 - Destino do checkout
# ===========================================================================

@pytest.mark.parametrize('url', [
    'http://www.mercadopago.com.br/checkout',                 # sem TLS
    'https://www.mercadopago.com.br.evil.test/checkout',      # domínio parecido
    'https://evil.test/www.mercadopago.com.br',               # host errado
    'https://www.mercadopago.com.br@evil.test/checkout',      # credenciais no host
    'https://www.mercadopago.com.br:8443/checkout',           # porta alternativa
    'https://mercadopago.com.br/checkout',                    # sem o www
    'javascript:alert(1)',
    'data:text/html,<script>alert(1)</script>',
    '//www.mercadopago.com.br/checkout',                      # sem esquema
    '',
    None,
])
def test_destino_de_checkout_hostil_e_recusado(url):
    """Hipótese: a validação do destino aceita algo além do checkout do MP Brasil."""
    assert url_checkout_permitida(url) is False


@pytest.mark.parametrize('url', [
    'https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=1',
    'https://sandbox.mercadopago.com.br/checkout/v1/redirect?pref_id=1',
])
def test_destino_legitimo_e_aceito(url):
    assert url_checkout_permitida(url) is True


def test_url_hostil_do_mercado_pago_nao_e_persistida(
    client, criar_pagamento, logar_como_aluno, monkeypatch,
):
    """Hipótese: se a resposta do MP trouxer um destino estranho, ele é salvo e servido."""
    pagamento = criar_pagamento()
    logar_como_aluno(pagamento.aluno)
    monkeypatch.setattr(checkout_bp, 'ambiente_mercado_pago', lambda: 'producao')
    monkeypatch.setattr(checkout_bp, 'criar_preferencia_checkout', lambda **kwargs: {
        'sucesso': True, 'preference_id': 'p1',
        'url_checkout': 'https://evil.test/checkout',
        'ambiente': 'producao', 'expira_em': datetime.utcnow() + timedelta(minutes=60),
    })

    resposta = client.post(f'/perfil/mensalidade/{pagamento.id}/checkout', headers=JSON)

    assert resposta.status_code == 502
    assert 'evil.test' not in resposta.get_data(as_text=True)
    atualizado = PagamentoDAO.buscar_por_id(pagamento.id)
    assert atualizado.checkout_url is None


# ===========================================================================
# H5 - O retorno do Mercado Pago não pode declarar aprovação
# ===========================================================================

def test_retorno_ignora_status_aprovado_da_query_string(
    client, criar_pagamento, logar_como_aluno, monkeypatch,
):
    """Hipótese: forjar ?status=approved na volta do MP quita a mensalidade."""
    pagamento = criar_pagamento()
    logar_como_aluno(pagamento.aluno)
    PagamentoDAO.salvar_dados_checkout(
        pagamento, preference_id='p1', external_reference='checkout-ref',
        url_checkout=URL_MP, ambiente='producao',
        expira_em=datetime.utcnow() + timedelta(minutes=60),
    )
    # O MP, consultado de verdade, diz que ninguém pagou.
    monkeypatch.setattr(pix_bp, 'buscar_pagamentos_por_referencia',
                        lambda ref, **kw: {'sucesso': True, 'pagamentos': []})

    resposta = client.get(
        f'/perfil/mensalidade/{pagamento.id}/retorno-checkout'
        '?status=approved&collection_status=approved&payment_id=999&external_reference=checkout-ref'
    )

    assert resposta.status_code == 200
    assert PagamentoDAO.buscar_por_id(pagamento.id).status == 'pendente'
    corpo = resposta.get_data(as_text=True)
    assert 'Pagamento confirmado' not in corpo


# ===========================================================================
# H6 - Conciliação em _processar_status_mp
# ===========================================================================

def _preparar_para_conciliacao(pagamento):
    PagamentoDAO.salvar_dados_pix(
        pagamento, provider_payment_id='mp-1', external_reference='mensalidade-legitima',
        idempotency_key='k', pix_copia_cola='pix', ticket_url=None,
        data_expiracao=datetime.utcnow() + timedelta(minutes=30),
    )


@pytest.mark.parametrize('nome,alteracao', [
    ('referência de outra mensalidade', {'external_reference': 'mensalidade-de-outro-aluno'}),
    ('moeda diferente', {'currency_id': 'USD', 'external_reference': 'mensalidade-legitima'}),
    ('valor menor', {'transaction_amount': 1.0, 'external_reference': 'mensalidade-legitima'}),
    ('valor maior', {'transaction_amount': 999.0, 'external_reference': 'mensalidade-legitima'}),
    ('sem external_reference', {'external_reference': None}),
    ('sem valor', {'transaction_amount': None, 'external_reference': 'mensalidade-legitima'}),
    ('sem moeda', {'currency_id': None, 'external_reference': 'mensalidade-legitima'}),
])
def test_aprovacao_incoerente_nao_quita_mensalidade(criar_pagamento, nome, alteracao):
    """Hipótese: uma resposta 'approved' incoerente quita a mensalidade mesmo assim."""
    pagamento = criar_pagamento()
    _preparar_para_conciliacao(pagamento)

    pix_bp._processar_status_mp(pagamento, {'sucesso': True, **_pagamento_mp(**alteracao)})

    assert PagamentoDAO.buscar_por_id(pagamento.id).status != 'pago', nome


def test_aprovacao_coerente_quita_a_mensalidade(criar_pagamento):
    """Contraprova: com tudo batendo, a baixa acontece."""
    pagamento = criar_pagamento()
    _preparar_para_conciliacao(pagamento)

    pix_bp._processar_status_mp(
        pagamento, {'sucesso': True, **_pagamento_mp(external_reference='mensalidade-legitima')},
    )

    assert PagamentoDAO.buscar_por_id(pagamento.id).status == 'pago'


# ===========================================================================
# H7 - Assinatura do webhook
# ===========================================================================

@pytest.mark.parametrize('assinatura,request_id,esperado', [
    (None, 'req-1', 400),                      # sem header de assinatura
    ('ts=1,v1=deadbeef', 'req-1', 401),        # assinatura forjada
    ('v1=deadbeef', 'req-1', 401),             # sem ts
    ('ts=1', 'req-1', 401),                    # sem v1
    ('lixo', 'req-1', 401),                    # formato inesperado
])
def test_webhook_recusa_assinaturas_invalidas(client, monkeypatch, assinatura, request_id, esperado):
    monkeypatch.setenv('MERCADO_PAGO_WEBHOOK_SECRET', 'segredo-de-teste')

    def _nao_deveria_consultar(*a, **k):
        pytest.fail('consultou o Mercado Pago antes de validar a assinatura')

    monkeypatch.setattr(pix_bp, 'buscar_pagamento', _nao_deveria_consultar)
    headers = {'x-request-id': request_id}
    if assinatura is not None:
        headers['x-signature'] = assinatura
    resposta = client.post('/api/webhooks/mercado-pago?data.id=mp-1',
                           json={'type': 'payment'}, headers=headers)
    assert resposta.status_code == esperado


def test_webhook_recusa_assinatura_antiga(criar_pagamento):
    """Hipótese: uma notificação capturada ontem pode ser reenviada hoje."""
    antiga = time.time() - 3600
    ts = str(int(antiga))
    manifest = f'id:mp-1;request-id:req-1;ts:{ts};'
    v1 = hmac.new(b'segredo', manifest.encode(), hashlib.sha256).hexdigest()
    assert validar_assinatura_webhook(
        x_signature=f'ts={ts},v1={v1}', x_request_id='req-1', data_id='mp-1', secret='segredo',
    ) is False


def test_webhook_valido_com_valor_divergente_nao_quita(client, criar_pagamento, monkeypatch):
    """Hipótese: assinatura válida basta para quitar, mesmo com valor errado."""
    monkeypatch.setenv('MERCADO_PAGO_WEBHOOK_SECRET', 'segredo-de-teste')
    pagamento = criar_pagamento()
    _preparar_para_conciliacao(pagamento)
    monkeypatch.setattr(pix_bp, 'buscar_pagamento', lambda *a, **k: {
        'sucesso': True, **_pagamento_mp(external_reference='mensalidade-legitima', transaction_amount=1.0),
    })

    resposta = client.post('/api/webhooks/mercado-pago?data.id=mp-1', json={'type': 'payment'},
                           headers=_assinar('mp-1', 'segredo-de-teste'))

    assert resposta.status_code == 200
    assert PagamentoDAO.buscar_por_id(pagamento.id).status != 'pago'


def test_webhook_repetido_nao_duplica_baixa(client, criar_pagamento, monkeypatch):
    """Reenvio da mesma notificação não pode gerar segunda baixa nem novo evento."""
    monkeypatch.setenv('MERCADO_PAGO_WEBHOOK_SECRET', 'segredo-de-teste')
    pagamento = criar_pagamento()
    _preparar_para_conciliacao(pagamento)
    monkeypatch.setattr(pix_bp, 'buscar_pagamento', lambda *a, **k: {
        'sucesso': True, **_pagamento_mp(external_reference='mensalidade-legitima'),
    })

    for _ in range(3):
        assert client.post('/api/webhooks/mercado-pago?data.id=mp-1', json={'type': 'payment'},
                           headers=_assinar('mp-1', 'segredo-de-teste')).status_code == 200

    atualizado = PagamentoDAO.buscar_por_id(pagamento.id)
    assert atualizado.status == 'pago'
    aprovacoes = [e for e in atualizado.eventos if e.tipo == 'webhook_aprovado']
    assert len(aprovacoes) == 1, f'{len(aprovacoes)} baixas registradas para a mesma notificação'


# ===========================================================================
# H8 - Cliques simultâneos / múltiplas abas
# ===========================================================================

def test_dois_cliques_reaproveitam_a_mesma_preferencia(
    client, criar_pagamento, logar_como_aluno, monkeypatch,
):
    """Hipótese: cada clique cria uma cobrança nova no Mercado Pago."""
    pagamento = criar_pagamento()
    logar_como_aluno(pagamento.aluno)
    chamadas = []
    monkeypatch.setattr(checkout_bp, 'ambiente_mercado_pago', lambda: 'producao')

    def _criar(**kwargs):
        chamadas.append(kwargs)
        return {'sucesso': True, 'preference_id': 'p1', 'url_checkout': URL_MP,
                'ambiente': 'producao', 'expira_em': datetime.utcnow() + timedelta(minutes=60)}

    monkeypatch.setattr(checkout_bp, 'criar_preferencia_checkout', _criar)

    primeira = client.post(f'/perfil/mensalidade/{pagamento.id}/checkout', headers=JSON)
    segunda = client.post(f'/perfil/mensalidade/{pagamento.id}/checkout', headers=JSON)

    assert primeira.status_code == 200 and segunda.status_code == 200
    assert primeira.get_json()['url_checkout'] == segunda.get_json()['url_checkout']
    assert len(chamadas) == 1, f'{len(chamadas)} preferências criadas para dois cliques'


def test_valor_cobrado_vem_do_banco_e_nao_do_navegador(
    client, criar_pagamento, logar_como_aluno, monkeypatch,
):
    """Hipótese: dá para injetar o valor pelo corpo do POST."""
    pagamento = criar_pagamento(valor=150.0)
    logar_como_aluno(pagamento.aluno)
    capturado = {}
    monkeypatch.setattr(checkout_bp, 'ambiente_mercado_pago', lambda: 'producao')

    def _criar(**kwargs):
        capturado.update(kwargs)
        return {'sucesso': True, 'preference_id': 'p1', 'url_checkout': URL_MP,
                'ambiente': 'producao', 'expira_em': datetime.utcnow() + timedelta(minutes=60)}

    monkeypatch.setattr(checkout_bp, 'criar_preferencia_checkout', _criar)

    client.post(f'/perfil/mensalidade/{pagamento.id}/checkout',
                data={'valor': '1.00', 'unit_price': '1.00', 'transaction_amount': '1.00'},
                headers=JSON)

    assert float(capturado['valor']) == 150.0


# ===========================================================================
# H9 - Perfil do professor: publicação e foto
# ===========================================================================

def test_foto_do_professor_some_ao_despublicar(client, contexto_app, tmp_path, monkeypatch):
    """Hipótese: a foto continua acessível por URL depois de tirar a publicação."""
    monkeypatch.setenv('UPLOAD_DIR', str(tmp_path))
    professor = Professor(nome='Professora Publicada', login='publicada', senha='senha123456')
    professor.perfil_publico = True
    professor.foto_arquivo = 'foto.jpg'
    ProfessorDAO.salvar(professor)
    pasta = tmp_path / 'professores'
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / 'foto.jpg').write_bytes(b'conteudo-de-teste')

    assert client.get(f'/professores/{professor.id}/foto').status_code == 200

    professor.perfil_publico = False
    ProfessorDAO.salvar(professor)

    resposta = client.get(f'/professores/{professor.id}/foto')
    assert resposta.status_code == 404


def test_contatos_do_professor_so_aparecem_quando_publicados(client, contexto_app):
    """Hipótese: os contatos vazam na home antes de a publicação ser marcada."""
    professor = Professor(nome='Professor Reservado', login='reservado', senha='senha123456')
    professor.instagram = 'reservado'
    professor.email_publico = 'reservado@example.com'
    professor.whatsapp = '5581999999999'
    professor.perfil_publico = False
    ProfessorDAO.salvar(professor)

    corpo = client.get('/').get_data(as_text=True)
    assert 'reservado@example.com' not in corpo
    assert 'Professor Reservado' not in corpo

    professor.perfil_publico = True
    professor.exibir_email = False
    ProfessorDAO.salvar(professor)

    corpo = client.get('/').get_data(as_text=True)
    assert 'Professor Reservado' in corpo
    assert 'reservado@example.com' not in corpo, 'e-mail apareceu sem exibir_email marcado'


# ===========================================================================
# H10 - Sondas que expõem lacunas (não necessariamente vulnerabilidades)
# ===========================================================================

def test_comprovante_de_outro_aluno_com_arquivo_real_nao_vaza(
    client, criar_pagamento, criar_aluno, logar_como_aluno, tmp_path, monkeypatch,
):
    """Versão forte da sonda de IDOR: o alvo TEM arquivo, então um 200 seria vazamento."""
    monkeypatch.setenv('UPLOAD_DIR', str(tmp_path))
    pasta = tmp_path / 'comprovantes'
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / 'segredo.pdf').write_bytes(b'%PDF-1.4 comprovante confidencial')

    alvo = criar_pagamento()
    PagamentoDAO.enviar_comprovante_manual(alvo, arquivo_nome='segredo.pdf', ator='alvo')

    intruso = criar_aluno()
    logar_como_aluno(intruso)
    resposta = client.get(f'/perfil/mensalidade/{alvo.id}/comprovante-manual/arquivo')

    assert resposta.status_code in (403, 404)
    assert b'confidencial' not in resposta.data


def test_pix_exige_trava_e_reutiliza_a_cobranca(
    client, criar_pagamento, logar_como_aluno, monkeypatch,
):
    """Verifica a trava antes da emissão e o reaproveitamento na próxima chamada.

    SQLite ignora FOR UPDATE. A concorrência real, com sessões independentes e
    espera pela trava, é verificada em test_pix_concorrencia_postgres.py.
    """
    pagamento = criar_pagamento()
    logar_como_aluno(pagamento.aluno)
    chamadas = []
    bloqueios = []
    bloquear = PagamentoDAO.bloquear_para_atualizacao

    def _bloquear(pagamento_id):
        bloqueios.append(pagamento_id)
        return bloquear(pagamento_id)

    def _criar_pix(**kwargs):
        assert bloqueios == [pagamento.id]
        chamadas.append(kwargs['external_reference'])
        return {
            'sucesso': True, 'payment_id': 'mp-unico', 'status': 'pending',
            'qr_code': 'copia-e-cola', 'qr_code_base64': None, 'ticket_url': None,
            'data_expiracao': datetime.utcnow() + timedelta(minutes=30),
        }

    monkeypatch.setattr(pix_bp, 'criar_pagamento_pix', _criar_pix)
    monkeypatch.setattr(PagamentoDAO, 'bloquear_para_atualizacao', _bloquear)
    monkeypatch.setattr(pix_bp, 'buscar_pagamento', lambda *a, **k: {
        'sucesso': True, 'status': 'pending', 'external_reference': chamadas[0],
    })

    primeira = client.post(f'/api/mensalidades/{pagamento.id}/pix', headers=JSON)
    segunda = client.post(f'/api/mensalidades/{pagamento.id}/pix', headers=JSON)

    assert primeira.status_code == segunda.status_code == 200
    assert primeira.json['pix_copia_cola'] == segunda.json['pix_copia_cola'] == 'copia-e-cola'
    assert bloqueios == [pagamento.id, pagamento.id]
    assert len(chamadas) == 1


def test_status_de_pagamento_tem_limite_de_requisicoes(client, criar_pagamento, logar_como_aluno, monkeypatch):
    """Sonda: cada GET de status pode disparar consultas à API do Mercado Pago.

    Sem limite, um aluno autenticado consegue transformar o endpoint em amplificador
    de chamadas contra a cota do provedor.
    """
    pagamento = criar_pagamento()
    logar_como_aluno(pagamento.aluno)
    PagamentoDAO.salvar_dados_pix(
        pagamento, provider_payment_id='mp-1', external_reference='ref',
        idempotency_key='k', pix_copia_cola='pix', ticket_url=None,
        data_expiracao=datetime.utcnow() + timedelta(minutes=30),
    )
    consultas = []
    monkeypatch.setattr(pix_bp, 'buscar_pagamento', lambda *a, **k: (
        consultas.append(1) or {'sucesso': True, **_pagamento_mp(status='pending', external_reference='ref')}
    ))

    codigos = [client.get(f'/api/mensalidades/{pagamento.id}/status').status_code for _ in range(120)]

    assert 429 in codigos, (
        f'120 consultas seguidas aceitas ({len(consultas)} chamadas ao Mercado Pago) sem nenhum 429'
    )


def test_foto_do_aluno_nao_e_cacheavel_por_proxy(client, criar_aluno, logar_como_aluno, tmp_path, monkeypatch):
    """Sonda: a foto do aluno é resposta autenticada; um cache compartilhado não pode guardá-la."""
    monkeypatch.setenv('UPLOAD_DIR', str(tmp_path))
    pasta = tmp_path / 'fotos'
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / 'aluno.jpg').write_bytes(b'bytes-da-foto')

    aluno = criar_aluno()
    aluno.foto_arquivo = 'aluno.jpg'
    logar_como_aluno(aluno)

    resposta = client.get(f'/perfil/foto/{aluno.id}')
    assert resposta.status_code == 200
    cache = resposta.headers.get('Cache-Control', '')
    assert 'private' in cache and 'no-store' in cache and 'public' not in cache, f'Cache-Control={cache!r}'
    # Uma requisição condicional também precisa passar pela autorização e receber
    # a política privada, sem revalidar uma cópia pública com 304.
    condicional = client.get(f'/perfil/foto/{aluno.id}', headers={
        'If-None-Match': resposta.headers['ETag'],
    })
    assert condicional.status_code == 200
    assert condicional.headers['Cache-Control'] == 'private, no-store'
    with client.session_transaction() as sess:
        sess.clear()
    assert client.get(f'/perfil/foto/{aluno.id}', headers={
        'If-None-Match': resposta.headers['ETag'],
    }).status_code == 403


@pytest.mark.parametrize('valor', [
    'abc',
    '2026-13-45',
    '',  # cai no valor padrão (hoje) e não quebra
    '../../etc/passwd',
])
def test_data_invalida_na_turma_nao_derruba_a_rota(client, contexto_app, logar_como_admin, valor):
    """Sonda: a data vem da query string e é convertida sem tratamento."""
    from modelos.turma import Turma
    from dao.turmaDAO import TurmaDAO
    professor = Professor(nome='Prof Data', login='profdata', senha='senha123456')
    ProfessorDAO.salvar(professor)
    turma = Turma('Turma Data', 'Seg', '19:00', professor.id, 20)
    TurmaDAO.salvar(turma)
    logar_como_admin()

    resposta = client.get(f'/turmas/{turma.id}?data={valor}')

    assert resposta.status_code != 500, f'?data={valor!r} derrubou a rota'
