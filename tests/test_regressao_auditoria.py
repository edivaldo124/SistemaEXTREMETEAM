"""Regressões da auditoria de segurança, desempenho e confiabilidade.

Cada caso aqui reproduz um problema que foi confirmado no código antes da correção.
Nenhum toca banco real, provedor de e-mail real ou arquivo de produção: o banco é o
SQLite descartável do conftest e o Brevo é sempre substituído por um duplo.
"""
from datetime import date, timedelta

import pytest
from sqlalchemy import event

from config import db
from dao.financeiroDAO import PagamentoDAO
from dao.usuarioDAO import AlunoDAO
from modelos.pagamento import Pagamento
from modelos.usuario import Aluno
from servicos.autorizacao import impressao_credencial


# ---------------------------------------------------------------------------
# P1.1 - Revogação de acesso: a sessão não pode sobreviver à desativação
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    'mudanca',
    [
        {'ativo': False},
        {'status_cadastro': 'recusado'},
        {'status_cadastro': 'pendente'},
    ],
    ids=['desativado', 'reprovado', 'voltou-a-pendente'],
)
def test_sessao_aberta_perde_o_perfil_quando_a_conta_deixa_de_valer(
    client, criar_aluno, logar_como_aluno, mudanca,
):
    aluno = criar_aluno()
    logar_como_aluno(aluno)
    assert client.get('/perfil').status_code == 200

    for campo, valor in mudanca.items():
        setattr(aluno, campo, valor)
    db.session.commit()

    resposta = client.get('/perfil')
    assert resposta.status_code == 302
    assert '/login' in resposta.headers['Location']


def test_aluno_desativado_nao_alcanca_a_propria_mensalidade_pela_sessao_antiga(
    client, criar_aluno, criar_pagamento, logar_como_aluno,
):
    aluno = criar_aluno()
    pagamento = criar_pagamento(aluno=aluno)
    logar_como_aluno(aluno)
    assert client.get(f'/perfil/pagamento/{pagamento.id}').status_code == 200

    aluno.ativo = False
    db.session.commit()

    resposta = client.get(f'/perfil/pagamento/{pagamento.id}')
    assert resposta.status_code == 302
    assert '/login' in resposta.headers['Location']


def test_aluno_desativado_nao_ve_mais_a_propria_foto_pela_sessao_antiga(
    client, criar_aluno, logar_como_aluno,
):
    aluno = criar_aluno()
    aluno.foto_arquivo = 'inexistente.jpg'
    db.session.commit()
    logar_como_aluno(aluno)
    # Sem arquivo em disco a rota devolve 404; o que importa é não ser 403.
    assert client.get(f'/perfil/foto/{aluno.id}').status_code == 404

    aluno.ativo = False
    db.session.commit()

    assert client.get(f'/perfil/foto/{aluno.id}').status_code == 403


def test_sessao_de_professor_removido_nao_abre_mais_a_area_do_professor(client, contexto_app):
    from dao.professorDAO import ProfessorDAO
    from modelos.professor import Professor

    professor = Professor(nome='Professor Teste', login='prof-teste', senha='senha-de-teste-123')
    ProfessorDAO.salvar(professor)
    professor_id = professor.id

    with client.session_transaction() as sessao:
        sessao['usuario'] = 'prof-teste'
        sessao['professor_id'] = professor_id
        sessao['tipo_usuario'] = 'professor'
        sessao['credencial'] = impressao_credencial(professor.senha_hash)

    assert client.get('/professor').status_code == 200

    ProfessorDAO.remover(professor_id)

    resposta = client.get('/professor')
    assert resposta.status_code == 302
    assert '/login' in resposta.headers['Location']


# ---------------------------------------------------------------------------
# P1.2 - Troca e recuperação de senha revogam as sessões anteriores
# ---------------------------------------------------------------------------

def test_troca_de_senha_derruba_as_outras_sessoes_e_mantem_a_que_trocou(
    app, criar_aluno, sem_email,
):
    aluno = criar_aluno(senha='SenhaAntiga-2026')
    sessao_que_troca = app.test_client()
    sessao_antiga = app.test_client()
    for cliente in (sessao_que_troca, sessao_antiga):
        with cliente.session_transaction() as sessao:
            sessao['usuario'] = aluno.login
            sessao['aluno_id'] = aluno.id
            sessao['tipo_usuario'] = 'aluno'
            sessao['credencial'] = _credencial(aluno)

    assert sessao_antiga.get('/perfil').status_code == 200

    resposta = sessao_que_troca.post('/perfil/senha', data={
        'senha_atual': 'SenhaAntiga-2026',
        'nova_senha': 'SenhaNova-2026',
        'confirmar_senha': 'SenhaNova-2026',
    })
    assert resposta.status_code == 302

    # Quem trocou continua dentro; quem tinha outra sessão é mandado ao login.
    assert sessao_que_troca.get('/perfil').status_code == 200
    outra = sessao_antiga.get('/perfil')
    assert outra.status_code == 302
    assert '/login' in outra.headers['Location']


def test_recuperacao_de_senha_derruba_as_sessoes_abertas(app, criar_aluno, sem_email):
    import hashlib
    import secrets
    from datetime import datetime

    aluno = criar_aluno(senha='SenhaAntiga-2026')
    token = secrets.token_urlsafe(32)
    aluno.token_recuperacao_hash = hashlib.sha256(token.encode()).hexdigest()
    aluno.token_recuperacao_expira = datetime.utcnow() + timedelta(minutes=10)
    db.session.commit()

    sessao_aberta = app.test_client()
    with sessao_aberta.session_transaction() as sessao:
        sessao['usuario'] = aluno.login
        sessao['aluno_id'] = aluno.id
        sessao['tipo_usuario'] = 'aluno'
        sessao['credencial'] = _credencial(aluno)
    assert sessao_aberta.get('/perfil').status_code == 200

    anonimo = app.test_client()
    anonimo.post(f'/recuperar_senha/{token}', data={'nova_senha': 'SenhaNova-2026'})

    resposta = sessao_aberta.get('/perfil')
    assert resposta.status_code == 302
    assert '/login' in resposta.headers['Location']


def test_recuperacao_de_senha_descarta_o_token_de_troca_de_email_pendente(
    client, criar_aluno, sem_email,
):
    import hashlib
    import secrets
    from datetime import datetime

    aluno = criar_aluno(senha='SenhaAntiga-2026')
    token = secrets.token_urlsafe(32)
    aluno.token_recuperacao_hash = hashlib.sha256(token.encode()).hexdigest()
    aluno.token_recuperacao_expira = datetime.utcnow() + timedelta(minutes=10)
    aluno.email_pendente = 'invasor@example.com'
    aluno.token_email_hash = hashlib.sha256(b'token-de-email').hexdigest()
    aluno.token_email_expira = datetime.utcnow() + timedelta(minutes=10)
    db.session.commit()

    client.post(f'/recuperar_senha/{token}', data={'nova_senha': 'SenhaNova-2026'})

    db.session.refresh(aluno)
    assert aluno.token_email_hash is None
    assert aluno.email_pendente is None


def _credencial(aluno):
    from servicos.autorizacao import impressao_credencial

    return impressao_credencial(aluno.senha_hash)


# ---------------------------------------------------------------------------
# P1.3 - Senhas com caracteres não ASCII
# ---------------------------------------------------------------------------

SENHA_ACENTUADA = 'Ação-Sênior-2026'


def test_login_do_admin_com_senha_acentuada_nao_quebra(client, monkeypatch):
    monkeypatch.setenv('ADMIN_USER', 'admin-teste')
    monkeypatch.setenv('ADMIN_PASSWORD', SENHA_ACENTUADA)

    resposta = client.post('/login', data={
        'loginusuario': 'admin-teste', 'senhausuario': SENHA_ACENTUADA,
    })
    assert resposta.status_code == 302
    assert '/admin' in resposta.headers['Location']


def test_login_do_admin_com_senha_acentuada_errada_nao_entra(client, monkeypatch):
    monkeypatch.setenv('ADMIN_USER', 'admin-teste')
    monkeypatch.setenv('ADMIN_PASSWORD', SENHA_ACENTUADA)

    resposta = client.post('/login', data={
        'loginusuario': 'admin-teste', 'senhausuario': 'Ação-Sênior-2027',
    })
    assert resposta.status_code == 200
    assert 'Credenciais incorretas' in resposta.get_data(as_text=True)


def test_aluno_troca_a_senha_para_uma_com_acentos(client, criar_aluno, logar_como_aluno, sem_email):
    aluno = criar_aluno(senha='SenhaAntiga-2026')
    logar_como_aluno(aluno)

    resposta = client.post('/perfil/senha', data={
        'senha_atual': 'SenhaAntiga-2026',
        'nova_senha': SENHA_ACENTUADA,
        'confirmar_senha': SENHA_ACENTUADA,
    })

    assert resposta.status_code == 302
    db.session.refresh(aluno)
    assert aluno.verificar_senha(SENHA_ACENTUADA)


def test_confirmacao_acentuada_divergente_ainda_e_recusada(
    client, criar_aluno, logar_como_aluno, sem_email,
):
    aluno = criar_aluno(senha='SenhaAntiga-2026')
    logar_como_aluno(aluno)

    client.post('/perfil/senha', data={
        'senha_atual': 'SenhaAntiga-2026',
        'nova_senha': SENHA_ACENTUADA,
        'confirmar_senha': 'Ação-Sênior-2027',
    })

    db.session.refresh(aluno)
    assert aluno.verificar_senha('SenhaAntiga-2026')


# ---------------------------------------------------------------------------
# P1.4 - Credencial administrativa por hash, com transição
# ---------------------------------------------------------------------------

def test_admin_entra_pelo_hash_quando_ele_esta_configurado(client, monkeypatch):
    from werkzeug.security import generate_password_hash

    monkeypatch.delenv('ADMIN_PASSWORD', raising=False)
    monkeypatch.setenv('ADMIN_USER', 'admin-teste')
    monkeypatch.setenv('ADMIN_PASSWORD_HASH', generate_password_hash(SENHA_ACENTUADA))

    resposta = client.post('/login', data={
        'loginusuario': 'admin-teste', 'senhausuario': SENHA_ACENTUADA,
    })
    assert resposta.status_code == 302
    assert '/admin' in resposta.headers['Location']


def test_hash_do_admin_tem_precedencia_sobre_a_senha_em_texto_puro(client, monkeypatch):
    from werkzeug.security import generate_password_hash

    monkeypatch.setenv('ADMIN_USER', 'admin-teste')
    monkeypatch.setenv('ADMIN_PASSWORD', 'senha-antiga-em-texto-puro')
    monkeypatch.setenv('ADMIN_PASSWORD_HASH', generate_password_hash('senha-nova-do-hash'))

    recusado = client.post('/login', data={
        'loginusuario': 'admin-teste', 'senhausuario': 'senha-antiga-em-texto-puro',
    })
    assert recusado.status_code == 200

    aceito = client.post('/login', data={
        'loginusuario': 'admin-teste', 'senhausuario': 'senha-nova-do-hash',
    })
    assert aceito.status_code == 302


# ---------------------------------------------------------------------------
# P2.6 / P2.7 - Painel financeiro: indicadores x tabela, e sem escrita no GET
# ---------------------------------------------------------------------------

def test_indicadores_e_tabela_concordam_na_primeira_abertura(
    client, criar_aluno, criar_pagamento, logar_como_admin,
):
    aluno = criar_aluno()
    criar_pagamento(aluno=aluno, status='pendente', vencimento=date.today() - timedelta(days=3))
    logar_como_admin()

    pagina = client.get('/admin/financeiro').get_data(as_text=True)

    # A cobrança vencida conta como atrasada nos dois lugares, já na primeira abertura.
    assert 'status-atrasado' in pagina
    indicadores = PagamentoDAO.totais_periodo()
    assert indicadores['qtd_vencido'] == 1
    assert indicadores['qtd_pendente'] == 0


def test_abrir_o_painel_financeiro_nao_grava_no_banco(
    client, criar_aluno, criar_pagamento, logar_como_admin,
):
    aluno = criar_aluno()
    criar_pagamento(aluno=aluno, status='pendente', vencimento=date.today() - timedelta(days=3))
    logar_como_admin()

    escritas = []
    motor = db.engine

    def registrar(conn, cursor, instrucao, *_resto):
        if instrucao.lstrip()[:6].upper() in ('UPDATE', 'INSERT', 'DELETE'):
            escritas.append(instrucao)

    event.listen(motor, 'before_cursor_execute', registrar)
    try:
        assert client.get('/admin/financeiro').status_code == 200
    finally:
        event.remove(motor, 'before_cursor_execute', registrar)

    assert escritas == [], f'GET do painel financeiro gravou no banco: {escritas}'


def test_painel_financeiro_nao_varre_mensalidades_fora_do_filtro(
    client, criar_aluno, criar_pagamento, logar_como_admin,
):
    """Abrir o painel filtrado por um plano não pode tocar as mensalidades dos outros."""
    from modelos.plano import Plano
    from dao.planoDAO import PlanoDAO

    outro_plano = Plano(nome_plano='Trimestral', preco_plano=400.0, duracao_dias=90)
    PlanoDAO.salvar(outro_plano)

    aluno = criar_aluno()
    de_fora = criar_pagamento(
        aluno=aluno, status='pendente', vencimento=date.today() - timedelta(days=10),
        plano_id=outro_plano.id,
    )
    logar_como_admin()

    client.get('/admin/financeiro', query_string={'plano_id': de_fora.plano_id + 1000})

    db.session.refresh(de_fora)
    assert de_fora.status == 'pendente'


# ---------------------------------------------------------------------------
# P2.9 - Paginação no banco
# ---------------------------------------------------------------------------

def test_financeiro_pagina_no_banco_sem_carregar_tudo(
    client, criar_aluno, criar_pagamento, logar_como_admin,
):
    aluno = criar_aluno()
    for dia in range(1, 31):
        criar_pagamento(aluno=aluno, vencimento=date.today() + timedelta(days=dia))
    logar_como_admin()

    pagina = PagamentoDAO.listar_paginado(pagina=1, por_pagina=10)
    assert len(pagina.itens) == 10
    assert pagina.total == 30
    assert pagina.total_paginas == 3
    assert pagina.tem_proxima and not pagina.tem_anterior

    ultima = PagamentoDAO.listar_paginado(pagina=3, por_pagina=10)
    assert len(ultima.itens) == 10
    assert ultima.tem_anterior and not ultima.tem_proxima

    resposta = client.get('/admin/financeiro', query_string={'pagina': 2})
    assert resposta.status_code == 200


def test_painel_admin_pagina_alunos_no_banco(client, criar_aluno, logar_como_admin):
    for _ in range(25):
        criar_aluno()
    logar_como_admin()

    pagina = AlunoDAO.listar_paginado(pagina=1, por_pagina=10)
    assert len(pagina.itens) == 10
    assert pagina.total == 25
    assert client.get('/admin', query_string={'pagina': 3}).status_code == 200


def test_paginacao_do_admin_ignora_pendentes_como_a_tela_sempre_fez(client, criar_aluno):
    criar_aluno(status_cadastro='pendente')
    criar_aluno(status_cadastro='aprovado')

    pagina = AlunoDAO.listar_paginado(pagina=1, por_pagina=10)
    assert pagina.total == 1
    assert pagina.itens[0].status_cadastro == 'aprovado'


# ---------------------------------------------------------------------------
# P2.10 - Busca de token por consulta direta
# ---------------------------------------------------------------------------

def _contar_selects_em_alunos(funcao):
    consultas = []

    def registrar(conn, cursor, instrucao, *_resto):
        if 'FROM alunos' in instrucao:
            consultas.append(instrucao)

    event.listen(db.engine, 'before_cursor_execute', registrar)
    try:
        funcao()
    finally:
        event.remove(db.engine, 'before_cursor_execute', registrar)
    return consultas


def test_confirmacao_de_email_consulta_pelo_hash_e_nao_varre_a_tabela(
    client, criar_aluno, sem_email,
):
    import hashlib
    import secrets
    from datetime import datetime

    for _ in range(5):
        criar_aluno()
    aluno = criar_aluno()
    token = secrets.token_urlsafe(32)
    aluno.email_pendente = 'novo@example.com'
    aluno.token_email_hash = hashlib.sha256(token.encode()).hexdigest()
    aluno.token_email_expira = datetime.utcnow() + timedelta(minutes=10)
    db.session.commit()

    consultas = _contar_selects_em_alunos(
        lambda: client.get(f'/perfil/confirmar_email/{token}')
    )

    assert any('token_email_hash' in c for c in consultas), (
        'A confirmação precisa filtrar pelo hash no banco, não em Python.'
    )
    db.session.refresh(aluno)
    assert aluno.email == 'novo@example.com'


def test_token_de_email_e_de_uso_unico_e_expira(client, criar_aluno, sem_email):
    import hashlib
    import secrets
    from datetime import datetime

    aluno = criar_aluno()
    token = secrets.token_urlsafe(32)
    aluno.email_pendente = 'novo@example.com'
    aluno.token_email_hash = hashlib.sha256(token.encode()).hexdigest()
    aluno.token_email_expira = datetime.utcnow() + timedelta(minutes=10)
    db.session.commit()

    client.get(f'/perfil/confirmar_email/{token}')
    db.session.refresh(aluno)
    assert aluno.token_email_hash is None

    # Segundo uso não pode reabrir nada.
    client.get(f'/perfil/confirmar_email/{token}')
    db.session.refresh(aluno)
    assert aluno.email == 'novo@example.com'


def test_token_de_recuperacao_expirado_nao_troca_a_senha(client, criar_aluno, sem_email):
    import hashlib
    import secrets
    from datetime import datetime

    aluno = criar_aluno(senha='SenhaAntiga-2026')
    token = secrets.token_urlsafe(32)
    aluno.token_recuperacao_hash = hashlib.sha256(token.encode()).hexdigest()
    aluno.token_recuperacao_expira = datetime.utcnow() - timedelta(minutes=1)
    db.session.commit()

    resposta = client.post(f'/recuperar_senha/{token}', data={'nova_senha': 'SenhaNova-2026'})

    assert 'inválido ou expirado' in resposta.get_data(as_text=True)
    db.session.refresh(aluno)
    assert aluno.verificar_senha('SenhaAntiga-2026')


def test_token_invalido_nao_revela_se_a_conta_existe(client, criar_aluno):
    criar_aluno()
    resposta = client.get('/recuperar_senha/token-que-nao-existe')
    texto = resposta.get_data(as_text=True)
    assert 'inválido ou expirado' in texto
    assert 'example.com' not in texto


# ---------------------------------------------------------------------------
# P2.11 - Consultas N+1 no painel financeiro
# ---------------------------------------------------------------------------

def test_painel_financeiro_nao_faz_uma_consulta_por_linha(
    client, criar_aluno, criar_pagamento, logar_como_admin,
):
    for _ in range(12):
        criar_pagamento(aluno=criar_aluno())
    logar_como_admin()

    consultas = []

    def registrar(conn, cursor, instrucao, *_resto):
        if instrucao.lstrip().upper().startswith('SELECT'):
            consultas.append(instrucao)

    event.listen(db.engine, 'before_cursor_execute', registrar)
    try:
        assert client.get('/admin/financeiro').status_code == 200
    finally:
        event.remove(db.engine, 'before_cursor_execute', registrar)

    # Sem carregamento antecipado eram ~2 consultas por linha (aluno + plano).
    assert len(consultas) < 20, f'{len(consultas)} consultas para 12 linhas: N+1 de volta.'


def test_indicadores_saem_de_uma_consulta_de_agregacao(
    criar_aluno, criar_pagamento, contexto_app,
):
    for _ in range(5):
        criar_pagamento(aluno=criar_aluno())

    consultas = []

    def registrar(conn, cursor, instrucao, *_resto):
        if instrucao.lstrip().upper().startswith('SELECT'):
            consultas.append(instrucao)

    event.listen(db.engine, 'before_cursor_execute', registrar)
    try:
        PagamentoDAO.totais_periodo()
    finally:
        event.remove(db.engine, 'before_cursor_execute', registrar)

    assert len(consultas) <= 2, f'Os indicadores ainda fazem {len(consultas)} consultas.'


def test_totais_periodo_preserva_o_escopo_dos_filtros_de_data(
    criar_aluno, criar_pagamento, contexto_app,
):
    aluno = criar_aluno()
    dentro = criar_pagamento(aluno=aluno, status='pago', vencimento=date(2026, 5, 10))
    criar_pagamento(aluno=aluno, status='pago', vencimento=date(2026, 8, 10))

    totais = PagamentoDAO.totais_periodo(inicio=date(2026, 5, 1), fim=date(2026, 5, 31))

    assert totais['qtd_pago'] == 1
    assert totais['total_recebido'] == dentro.valor


# ---------------------------------------------------------------------------
# P2.8 - E-mails coletivos saem da requisição, com durabilidade
# ---------------------------------------------------------------------------

def test_aviso_coletivo_enfileira_em_vez_de_enviar_na_requisicao(
    client, criar_aluno, logar_como_admin, monkeypatch,
):
    from servicos import fila_email

    enviados = []
    monkeypatch.setattr(fila_email, 'processar_agora', lambda *a, **k: None)
    monkeypatch.setattr('servicos.email.enviar_email', lambda *a, **k: enviados.append(a) or True)

    for _ in range(3):
        criar_aluno()
    logar_como_admin()

    with client.session_transaction() as sessao:
        sessao['token_aviso'] = 'token-de-teste'

    resposta = client.post('/admin/avisos', data={
        'token_aviso': 'token-de-teste',
        'assunto': 'Aviso de teste',
        'mensagem': 'Corpo do aviso.',
        'destinatarios': 'todos',
    })

    assert resposta.status_code == 302
    assert enviados == [], 'O envio não pode acontecer dentro da requisição.'
    assert fila_email.contar_pendentes() == 3


def test_fila_de_email_nao_duplica_o_mesmo_envio(contexto_app, monkeypatch):
    from servicos import fila_email

    chamadas = []
    monkeypatch.setattr(fila_email, '_entregar', lambda item: chamadas.append(item.id) or True)

    for _ in range(2):
        fila_email.enfileirar(
            destinatario='aluno@example.com', nome_destinatario='Aluno',
            assunto='Aviso', titulo='Aviso', paragrafos=['Corpo.'],
            chave_idempotencia='aviso-2026-09-12-aluno@example.com',
        )

    assert fila_email.contar_pendentes() == 1
    fila_email.processar_agora()
    assert len(chamadas) == 1
    assert fila_email.contar_pendentes() == 0


def test_fila_de_email_sobrevive_ao_reinicio_e_registra_a_falha(contexto_app, monkeypatch):
    from servicos import fila_email

    from datetime import datetime

    monkeypatch.setattr(fila_email, '_entregar', lambda item: False)
    fila_email.enfileirar(
        destinatario='aluno@example.com', nome_destinatario='Aluno',
        assunto='Aviso', titulo='Aviso', paragrafos=['Corpo.'],
        chave_idempotencia='falha-1',
    )
    fila_email.processar_agora()

    # A linha continua no banco para a próxima tentativa: nada se perde num restart.
    assert fila_email.contar_pendentes() == 1
    depois_da_espera = datetime.utcnow() + timedelta(hours=1)
    pendente = fila_email.listar_pendentes(agora=depois_da_espera)[0]
    assert pendente.tentativas == 1
    assert pendente.ultimo_erro
    # A falha adia a próxima tentativa em vez de devolver a linha à cabeça da fila.
    assert pendente.proxima_tentativa > datetime.utcnow()
    assert fila_email.listar_pendentes() == []

    monkeypatch.setattr(fila_email, '_entregar', lambda item: True)
    fila_email.processar_agora(agora=depois_da_espera)
    assert fila_email.contar_pendentes() == 0


def test_cobranca_coletiva_so_enfileira_para_quem_deve(
    client, criar_aluno, criar_pagamento, logar_como_admin, monkeypatch,
):
    from servicos import fila_email

    monkeypatch.setattr(fila_email, 'processar_agora', lambda *a, **k: None)

    devedor = criar_aluno()
    criar_pagamento(aluno=devedor, status='atrasado', vencimento=date.today() - timedelta(days=5))
    em_dia = criar_aluno()
    criar_pagamento(
        aluno=em_dia, status='pago', vencimento=date.today() - timedelta(days=5),
        data_pagamento=date.today() - timedelta(days=5),
        vigencia_inicio=date.today() - timedelta(days=5),
        vigencia_fim=date.today() + timedelta(days=25),
    )
    logar_como_admin()

    with client.session_transaction() as sessao:
        sessao['token_aviso'] = 'token-de-teste'
    client.post('/admin/avisos/cobranca', data={'token_aviso': 'token-de-teste'})

    pendentes = fila_email.listar_pendentes()
    assert [p.destinatario for p in pendentes] == [devedor.email]


# ---------------------------------------------------------------------------
# P3.14 - Limites e tratamento de imagem
# ---------------------------------------------------------------------------

def test_png_com_pixels_demais_e_recusado_pelo_cabecalho(contexto_app):
    """Bomba de descompressão: arquivo minúsculo, imagem gigante.

    O PNG aqui tem 285 KB e declara 10000x10000. Decodificá-lo custava 1146 MB medidos,
    num container de 192 MB. A recusa acontece lendo o cabeçalho, sem alocar os pixels.
    """
    from servicos.armazenamento import ImagemGrandeDemais, salvar_foto_perfil

    with pytest.raises(ImagemGrandeDemais):
        salvar_foto_perfil(_png_bomba(4000, 4000))


def test_jpeg_grande_e_aceito_porque_decodifica_em_escala_reduzida(contexto_app):
    """O limite protege a memória, não pune a resolução: JPEG usa `draft()`."""
    from io import BytesIO

    from PIL import Image

    from servicos.armazenamento import salvar_foto_perfil

    buffer = BytesIO()
    Image.new('RGB', (6000, 4000), 'darkred').save(buffer, format='JPEG', quality=60)

    assert salvar_foto_perfil(buffer.getvalue()).endswith('.jpg')


def _png_bomba(largura, altura):
    """PNG válido e altamente compressível: linhas zeradas, como uma bomba real."""
    import struct
    import zlib

    def bloco(tipo, dados):
        return (
            struct.pack('>I', len(dados)) + tipo + dados
            + struct.pack('>I', zlib.crc32(tipo + dados) & 0xFFFFFFFF)
        )

    ihdr = struct.pack('>IIBBBBB', largura, altura, 8, 2, 0, 0, 0)
    compressor = zlib.compressobj(9)
    linha = b'\x00' + b'\x00' * (largura * 3)
    partes = [compressor.compress(linha) for _ in range(altura)]
    partes.append(compressor.flush())
    return (
        b'\x89PNG\r\n\x1a\n' + bloco(b'IHDR', ihdr)
        + bloco(b'IDAT', b''.join(partes)) + bloco(b'IEND', b'')
    )


def test_imagem_invalida_continua_sendo_recusada_com_mensagem(contexto_app):
    from servicos.armazenamento import ArquivoInvalido, salvar_foto_perfil

    with pytest.raises(ArquivoInvalido):
        salvar_foto_perfil(b'isto nao e uma imagem')


def test_foto_legitima_continua_sendo_aceita(contexto_app):
    from io import BytesIO

    from PIL import Image

    from servicos.armazenamento import salvar_foto_perfil

    buffer = BytesIO()
    Image.new('RGB', (800, 600), 'navy').save(buffer, format='JPEG')

    nome = salvar_foto_perfil(buffer.getvalue())
    assert nome.endswith('.jpg')


@pytest.mark.parametrize(
    'rota,metodo',
    [
        ('/perfil/senha', 'post'),
        ('/perfil/email', 'post'),
        ('/perfil/foto', 'post'),
        ('/perfil/confirmar_email/token-qualquer', 'get'),
        ('/recuperar_senha/token-qualquer', 'get'),
    ],
)
def test_rotas_caras_tem_limite_de_requisicoes(app, rota, metodo):
    """Rotas que custam hash de senha, processamento de imagem ou sondagem de token."""
    assert _tem_limite(app, rota, metodo), f'{rota} não tem limite de requisições.'


def _tem_limite(app, rota, metodo):
    """Limites declarados por decorador NAQUELA rota.

    `resolve_limits` não serve aqui: ele mistura os limites padrão da aplicação e
    devolve algo para qualquer endpoint, inclusive `/health`.
    """
    from config import limiter

    adaptador = app.url_map.bind('localhost')
    endpoint, _argumentos = adaptador.match(rota, method=metodo.upper())
    funcao = app.view_functions[endpoint]
    nome = f'{funcao.__module__}.{funcao.__name__}.{funcao.__qualname__}'
    return bool(list(limiter.limit_manager.decorated_limits(nome)))


def test_o_detector_de_limite_realmente_discrimina():
    """Guarda do teste acima: uma rota sem limite precisa ser reprovada por ele."""
    from servidor import app as aplicacao

    assert not _tem_limite(aplicacao, '/health', 'get')


def test_decodificacao_de_imagem_e_serializada_no_processo(contexto_app):
    """Duas fotos ao mesmo tempo não podem somar seus picos de memória.

    A aplicação ocupa 89 MB medidos num container de 192 MB. Uma imagem de 8 MP sem
    escala reduzida custa ~92 MB: uma cabe, duas simultâneas derrubariam o processo.
    """
    import threading
    from io import BytesIO

    from PIL import Image

    from servicos.armazenamento import salvar_foto_perfil

    buffer = BytesIO()
    Image.new('RGB', (1200, 900), 'teal').save(buffer, format='PNG')
    imagem = buffer.getvalue()

    simultaneos = []
    dentro = threading.Semaphore(0)
    maximo = {'valor': 0}
    trava = threading.Lock()
    original = Image.Image.resize

    def resize_lento(self, *args, **kwargs):
        with trava:
            simultaneos.append(1)
            maximo['valor'] = max(maximo['valor'], len(simultaneos))
        dentro.release()
        resultado = original(self, *args, **kwargs)
        with trava:
            simultaneos.pop()
        return resultado

    Image.Image.resize = resize_lento
    try:
        threads = [threading.Thread(target=salvar_foto_perfil, args=(imagem,)) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=30)
    finally:
        Image.Image.resize = original

    assert maximo['valor'] == 1, (
        f'{maximo["valor"]} decodificações simultâneas: o limite do processo não vale.'
    )


def test_a_suite_nunca_escreve_na_pasta_de_uploads_do_projeto():
    """Guarda do isolamento: a suíte gravava fotos e comprovantes reais em `uploads/`.

    `servicos.armazenamento` cai no padrão 'uploads' quando UPLOAD_DIR não é definido,
    então cada execução misturava arquivos de teste aos de alunos de verdade.
    """
    import os
    from pathlib import Path

    from servicos.armazenamento import _raiz_uploads

    raiz_testes = Path(_raiz_uploads()).resolve()
    uploads_do_projeto = (Path(__file__).resolve().parent.parent / 'uploads').resolve()

    assert os.environ.get('UPLOAD_DIR'), 'UPLOAD_DIR precisa ser definido pelo conftest.'
    assert raiz_testes != uploads_do_projeto
    assert uploads_do_projeto not in raiz_testes.parents


# ---------------------------------------------------------------------------
# Achados da revisão de código sobre estas próprias mudanças
# ---------------------------------------------------------------------------

def test_sessao_sem_carimbo_de_credencial_e_recusada(client, criar_aluno):
    """Aceitar uma sessão sem carimbo reabriria o buraco que o carimbo fecha.

    Um cookie roubado antes da publicação sobreviveria à troca de senha feita para
    expulsá-lo. O preço é encerrar as sessões abertas uma vez, na publicação.
    """
    aluno = criar_aluno()
    with client.session_transaction() as sessao:
        sessao['usuario'] = aluno.login
        sessao['aluno_id'] = aluno.id
        sessao['tipo_usuario'] = 'aluno'
        # sem 'credencial', como um cookie emitido pela versão anterior

    resposta = client.get('/perfil')
    assert resposta.status_code == 302
    assert '/login' in resposta.headers['Location']


def test_trocar_a_credencial_do_admin_encerra_a_sessao_administrativa(
    client, logar_como_admin, monkeypatch,
):
    """A conta de maior privilégio não pode ser a única isenta da revogação."""
    from werkzeug.security import generate_password_hash

    logar_como_admin()
    assert client.get('/admin').status_code == 200

    monkeypatch.setenv('ADMIN_PASSWORD_HASH', generate_password_hash('senha-nova-do-admin'))

    resposta = client.get('/admin')
    assert resposta.status_code == 302
    assert '/login' in resposta.headers['Location']


def test_o_mesmo_aviso_pode_ser_enviado_de_novo_em_outro_dia(contexto_app):
    """A chave de idempotência inclui o dia.

    Só o conteúdo suprimiria para sempre um aviso recorrente ("não vai ter treino"),
    com a tela ainda dizendo que enviou.
    """
    from blueprints.adm_bp import _chave_lote

    hoje = _chave_lote('Aviso', 'Não vai ter treino amanhã.')
    assert hoje == _chave_lote('Aviso', 'Não vai ter treino amanhã.')
    assert hoje != _chave_lote('Aviso', 'Vai ter treino amanhã.')

    import blueprints.adm_bp as adm_bp
    from datetime import date as data_real

    class OutroDia(data_real):
        @classmethod
        def today(cls):
            return data_real(2027, 1, 1)

    adm_bp.date = OutroDia
    try:
        assert _chave_lote('Aviso', 'Não vai ter treino amanhã.') != hoje
    finally:
        adm_bp.date = data_real


def test_uma_falha_do_provedor_nao_queima_todas_as_tentativas(contexto_app, monkeypatch):
    """O laço parava só quando nada acontecia, então uma indisponibilidade gastava as
    5 tentativas em segundos e marcava o lote inteiro como desistido."""
    from servicos import fila_email

    fila_email.enfileirar(
        destinatario='aluno@example.test', nome_destinatario='Aluno',
        assunto='Aviso', titulo='Aviso', paragrafos=['Corpo.'],
        chave_idempotencia='aviso:instabilidade:1',
    )
    db.session.commit()

    from datetime import datetime

    monkeypatch.setattr(fila_email, '_entregar', lambda item: False)
    fila_email.processar_agora()

    depois_da_espera = datetime.utcnow() + timedelta(hours=1)
    pendente = fila_email.listar_pendentes(agora=depois_da_espera)[0]
    assert pendente.tentativas == 1, 'Uma passada deve gastar UMA tentativa, não todas.'
    assert fila_email.contar_falhados() == 0

    # Insistir agora não gasta tentativa nenhuma: a linha está adiada.
    fila_email.processar_agora()
    fila_email.processar_agora()
    db.session.refresh(pendente)
    assert pendente.tentativas == 1

    monkeypatch.setattr(fila_email, '_entregar', lambda item: True)
    fila_email.processar_agora(agora=depois_da_espera)
    assert fila_email.contar_pendentes() == 0


def test_busca_do_admin_encontra_o_aluno_pelo_cpf_so_com_digitos(client, criar_aluno):
    """O CPF é guardado formatado; digitar só os números precisa encontrar mesmo assim."""
    aluno = criar_aluno(cpf='529.982.247-25', nome='Pessoa Com CPF Formatado')

    por_digitos = AlunoDAO.listar_paginado(pagina=1, busca='52998224725')
    por_formatado = AlunoDAO.listar_paginado(pagina=1, busca='529.982.247-25')
    por_parte = AlunoDAO.listar_paginado(pagina=1, busca='529982')

    assert [a.id for a in por_digitos.itens] == [aluno.id]
    assert [a.id for a in por_formatado.itens] == [aluno.id]
    assert [a.id for a in por_parte.itens] == [aluno.id]


def test_limite_de_upload_e_por_conta_e_nao_por_ip(app, criar_aluno, logar_como_aluno):
    """Alunos atrás do mesmo IP (o Wi-Fi da academia) não dividem a cota."""
    from blueprints.usuario_bp import _chave_da_conta

    primeiro = criar_aluno()
    segundo = criar_aluno()

    with app.test_request_context('/perfil/foto', method='POST'):
        from flask import session

        session['tipo_usuario'] = 'aluno'
        session['aluno_id'] = primeiro.id
        chave_primeiro = _chave_da_conta()
        session['aluno_id'] = segundo.id
        chave_segundo = _chave_da_conta()

    assert chave_primeiro != chave_segundo
    assert str(primeiro.id) in chave_primeiro


def test_visitante_sem_sessao_ainda_e_limitado_por_ip(app):
    from blueprints.usuario_bp import _chave_da_conta

    with app.test_request_context('/perfil/foto', method='POST'):
        assert _chave_da_conta().startswith('ip:')


def test_comprovante_a4_escaneado_continua_sendo_aceito(contexto_app):
    """O teto de pixels vale para a FOTO, que é decodificada, não para o comprovante.

    Um A4 a 300 dpi tem 8,7 MP e passava do limite pensado para o avatar, embora o
    comprovante seja guardado como veio, sem decodificar pixel nenhum.
    """
    from servicos.armazenamento import salvar_comprovante_manual

    a4_300dpi = _png_bomba(2480, 3508)
    assert len(a4_300dpi) < 8 * 1024 * 1024

    assert salvar_comprovante_manual(a4_300dpi).endswith('.png')


def test_foto_de_perfil_mantem_o_teto_de_pixels(contexto_app):
    from servicos.armazenamento import ImagemGrandeDemais, salvar_foto_perfil

    with pytest.raises(ImagemGrandeDemais):
        salvar_foto_perfil(_png_bomba(2480, 3508))


def test_login_de_aluno_nao_paga_o_hash_do_admin(client, criar_aluno, monkeypatch):
    """Conferir a credencial do admin custava um scrypt em TODO login.

    São ~74 ms e ~32 MB por chamada, num container de 192 MB - e o aluno já paga o seu
    próprio hash logo em seguida.
    """
    from servicos import credenciais

    chamadas = []
    original = credenciais.check_password_hash
    monkeypatch.setattr(
        credenciais, 'check_password_hash',
        lambda *args, **kwargs: chamadas.append(1) or original(*args, **kwargs),
    )

    aluno = criar_aluno(login='aluno-comum', senha='SenhaDoAluno-2026')
    client.post('/login', data={
        'loginusuario': aluno.login, 'senhausuario': 'SenhaDoAluno-2026',
    })

    assert chamadas == [], 'O login de aluno não deve acionar o hash da credencial admin.'


def test_aviso_repetido_no_mesmo_dia_avisa_em_vez_de_comemorar(
    client, criar_aluno, logar_como_admin, monkeypatch,
):
    from servicos import fila_email

    monkeypatch.setattr(fila_email, 'processar_agora', lambda *a, **k: None)
    criar_aluno()
    logar_como_admin()
    with client.session_transaction() as sessao:
        sessao['token_aviso'] = 'token-de-teste'

    dados = {
        'token_aviso': 'token-de-teste', 'assunto': 'Sem treino',
        'mensagem': 'Não vai ter treino amanhã.', 'destinatarios': 'todos',
    }
    client.post('/admin/avisos', data=dados)
    segunda = client.post('/admin/avisos', data=dados, follow_redirects=True)

    corpo = segunda.get_data(as_text=True)
    assert 'já foi enviado hoje' in corpo
    assert 'msg-erro' in corpo


def test_contador_do_financeiro_mostra_o_total_e_nao_a_pagina(
    client, criar_aluno, criar_pagamento, logar_como_admin,
):
    aluno = criar_aluno()
    for dia in range(1, 41):
        criar_pagamento(aluno=aluno, vencimento=date.today() + timedelta(days=dia))
    logar_como_admin()

    corpo = client.get('/admin/financeiro').get_data(as_text=True)

    assert '40 resultados com os filtros atuais' in corpo


def test_card_de_alunos_nao_muda_com_a_busca(client, criar_aluno, logar_como_admin):
    for _ in range(6):
        criar_aluno()
    criar_aluno(nome='Nome Bem Especifico')
    logar_como_admin()

    com_busca = client.get('/admin', query_string={'busca': 'Especifico'}).get_data(as_text=True)

    # O card do topo é uma métrica da academia; ele fica ao lado de "Cadastros
    # pendentes", que é global.
    assert '<strong>7</strong>' in com_busca
    assert '1 de 7 aluno' in com_busca


def test_linha_com_defeito_nao_trava_a_fila_atras_dela(contexto_app, monkeypatch):
    """Head-of-line blocking: a primeira linha falhando não pode impedir as seguintes.

    Antes, a fila era ordenada só por id e relia sempre as mesmas linhas do topo: quem
    estava atrás de um endereço com problema nunca chegava a ser tentado.
    """
    from servicos import fila_email

    for numero in range(5):
        fila_email.enfileirar(
            destinatario=f'aluno{numero}@example.test', nome_destinatario=f'Aluno {numero}',
            assunto='Aviso', titulo='Aviso', paragrafos=['Corpo.'],
            chave_idempotencia=f'aviso:fila-travada:{numero}',
        )
    db.session.commit()

    entregues = []

    def entregar(item):
        if item.destinatario == 'aluno0@example.test':
            return False
        entregues.append(item.destinatario)
        return True

    monkeypatch.setattr(fila_email, '_entregar', entregar)
    fila_email.processar_agora()

    assert len(entregues) == 4, 'Os outros quatro precisam sair mesmo com o primeiro falhando.'
    assert 'aluno0@example.test' not in entregues


def test_reenviar_um_aviso_que_desistiu_volta_a_enfileirar(contexto_app, monkeypatch):
    """Uma linha `desistiu` nunca foi entregue: recusar o reenvio fazia a tela dizer
    "já recebeu" sobre um e-mail que não chegou."""
    from modelos.email_pendente import MAX_TENTATIVAS, STATUS_DESISTIU
    from servicos import fila_email

    chave = 'cobranca:2026-09-12:99'
    item = fila_email.enfileirar(
        destinatario='aluno@example.test', nome_destinatario='Aluno',
        assunto='Mensalidade pendente', titulo='Mensalidade pendente',
        paragrafos=['Corpo.'], chave_idempotencia=chave,
    )
    item.status = STATUS_DESISTIU
    item.tentativas = MAX_TENTATIVAS
    item.ultimo_erro = 'provedor fora do ar'
    db.session.commit()
    assert fila_email.contar_pendentes() == 0

    revivido = fila_email.enfileirar(
        destinatario='aluno@example.test', nome_destinatario='Aluno',
        assunto='Mensalidade pendente', titulo='Mensalidade pendente',
        paragrafos=['Corpo.'], chave_idempotencia=chave,
    )
    db.session.commit()

    assert revivido is not None, 'Um envio abandonado precisa poder ser tentado de novo.'
    assert fila_email.contar_pendentes() == 1
    assert revivido.tentativas == 0
    assert fila_email.contar_falhados() == 0


def test_um_envio_ainda_pendente_continua_sendo_recusado(contexto_app):
    """A revivência vale só para o abandonado: clique duplo continua virando um envio."""
    from servicos import fila_email

    chave = 'cobranca:2026-09-12:100'
    dados = dict(
        destinatario='aluno@example.test', nome_destinatario='Aluno',
        assunto='Mensalidade pendente', titulo='Mensalidade pendente',
        paragrafos=['Corpo.'], chave_idempotencia=chave,
    )
    assert fila_email.enfileirar(**dados) is not None
    assert fila_email.enfileirar(**dados) is None
    db.session.commit()
    assert fila_email.contar_pendentes() == 1


@pytest.mark.parametrize(
    'termo,acha_por_cpf',
    [
        ('52998224725', True),
        ('529.982.247-25', True),
        ('529982', True),
        ('Aluno 3', False),
        ('3', False),
        ('Maria', False),
    ],
)
def test_busca_so_trata_como_cpf_o_que_parece_cpf(contexto_app, termo, acha_por_cpf):
    """Qualquer dígito no termo virava `CPF LIKE '%3%'` e devolvia a academia inteira."""
    from dao.usuarioDAO import _parece_busca_por_cpf

    assert _parece_busca_por_cpf(termo) is acha_por_cpf


def test_busca_por_nome_com_numero_nao_devolve_todo_mundo(client, criar_aluno):
    for _ in range(8):
        criar_aluno()
    alvo = criar_aluno(nome='Aluno Numero 3', cpf='111.222.333-44')

    pagina = AlunoDAO.listar_paginado(pagina=1, busca='Aluno Numero 3')

    assert [a.id for a in pagina.itens] == [alvo.id]


def test_limite_atingido_nao_mostra_login_a_quem_ja_entrou(client, criar_aluno, logar_como_aluno):
    """Trocar senha, e-mail ou foto são ações de quem JÁ está autenticado.

    Devolver o formulário de login ao estourar o limite parecia que a sessão tinha
    caído, e ainda convidava a digitar a senha de novo.
    """
    aluno = criar_aluno(senha='SenhaDoAluno-2026')
    logar_como_aluno(aluno)

    ultima = None
    for _ in range(20):
        ultima = client.post('/perfil/senha', data={
            'senha_atual': 'errada', 'nova_senha': 'X', 'confirmar_senha': 'X',
        })
        if ultima.status_code == 429:
            break

    assert ultima.status_code == 429, 'O limite da rota de senha não foi atingido.'
    corpo = ultima.get_data(as_text=True)
    assert 'Muitas tentativas' in corpo
    assert 'senhausuario' not in corpo, 'Não mostre o formulário de login a quem está logado.'


def test_visitante_que_estoura_o_login_ainda_ve_a_tela_de_login(client):
    ultima = None
    for numero in range(30):
        ultima = client.post('/login', data={
            'loginusuario': f'nao-existe-{numero}', 'senhausuario': 'seja-la-o-que-for',
        })
        if ultima.status_code == 429:
            break

    assert ultima.status_code == 429
    assert 'Muitas tentativas' in ultima.get_data(as_text=True)


def test_pagina_vazia_ainda_mostra_a_navegacao(contexto_app):
    """`__len__` fazia `{% if pagina %}` ser falso numa página sem itens, escondendo
    justamente os botões para voltar."""
    from dao.financeiroDAO import Pagina

    vazia = Pagina([], pagina=3, por_pagina=25, total=0)
    assert bool(vazia) is True
    assert len(vazia) == 0


def test_retentativa_acontece_sem_ninguem_abrir_o_painel(app, monkeypatch):
    """Persistência não é retomada: alguém precisa acordar a fila quando o adiamento vence.

    Quem faz isso em produção é `servicos.consumidor_email`, iniciado pelo worker do
    Gunicorn (`gunicorn.conf.py`). Aqui o agendador é exercitado com relógio controlado,
    sem thread de fundo nem reinício real.
    """
    from datetime import datetime

    from servicos import consumidor_email, fila_email

    with app.app_context():
        fila_email.enfileirar(
            destinatario='aluno@example.test', nome_destinatario='Aluno',
            assunto='Aviso', titulo='Aviso', paragrafos=['Corpo.'],
            chave_idempotencia='aviso:retomada:1',
        )
        db.session.commit()

        tentativas = {'n': 0}

        def entregar(item):
            tentativas['n'] += 1
            return tentativas['n'] > 1   # a primeira falha, a segunda funciona

        monkeypatch.setattr(fila_email, '_entregar', entregar)

        fila_email.processar_agora()
        assert tentativas['n'] == 1
        assert fila_email.contar_pendentes() == 1
        assert fila_email.listar_pendentes() == [], 'A linha precisa ficar adiada.'

        # Sem ninguém abrir o painel: o agendador dispara de novo quando a espera vence.
        depois = datetime.utcnow() + timedelta(minutes=5)
        fila_email.processar_agora(agora=depois)

        assert tentativas['n'] == 2
        assert fila_email.contar_pendentes() == 0

    # O agendador não sobe em teste nem no comando de migrations.
    assert consumidor_email.iniciar(app) is False
