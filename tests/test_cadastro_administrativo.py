"""Cadastro de aluno pela administração, ativação de acesso e confirmação de senha.

Os três assuntos vivem no mesmo arquivo porque testam a mesma fronteira: o que separa
o CADASTRO do aluno (matrícula, plano, mensalidades) da CONTA DE ACESSO dele.
"""
import re
from datetime import datetime, timedelta

import pytest

from config import db
from dao.financeiroDAO import PagamentoDAO
from dao.usuarioDAO import AlunoDAO
from modelos.pagamento import Pagamento
from modelos.usuario import Aluno
from servicos import convites
from servicos import planos as regras_plano


@pytest.fixture
def capturar_emails(monkeypatch):
    """Intercepta o envio e devolve os e-mails que teriam saído, com os links."""
    enviados = []

    def _falso_envio(destinatario, nome, assunto, titulo, paragrafos, link_url=None, link_texto=None):
        enviados.append({
            'destinatario': destinatario, 'assunto': assunto,
            'paragrafos': paragrafos, 'link_url': link_url,
        })
        return True

    monkeypatch.setattr('servicos.convites.enviar_email', _falso_envio)
    monkeypatch.setattr('blueprints.usuario_bp.enviar_email', _falso_envio)
    monkeypatch.setattr('blueprints.adm_bp.enviar_email', _falso_envio)
    return enviados


def _token_do_convite(emails):
    link = next(e['link_url'] for e in emails if e['link_url'] and '/ativar-acesso/' in e['link_url'])
    return link.rsplit('/', 1)[1]


def _matricular(client, **campos):
    dados = {
        'nome': 'Antônia Ribeiro Souza',
        'cpf': '529.982.247-25',
        'datanascimento': '1948-03-12',
    }
    dados.update(campos)
    return client.post('/admin/alunos/novo', data=dados, follow_redirects=False)


# --------------------------------------------------------------- matrícula --

def test_admin_matricula_aluno_sem_email_senha_nem_acesso(client, logar_como_admin, contexto_app):
    logar_como_admin()

    resposta = _matricular(client)

    assert resposta.status_code == 302
    aluno = AlunoDAO.buscar_por_cpf('529.982.247-25')
    assert aluno is not None
    assert aluno.email is None and aluno.login is None and aluno.senha_hash is None
    assert aluno.acesso_ativado is False
    assert aluno.estado_acesso == 'nao_ativado'
    assert aluno.rotulo_acesso == 'Acesso não ativado'
    # Quem cadastrou já é a administração: não sobra nada para aprovar depois.
    assert aluno.status_cadastro == 'aprovado'
    assert aluno.esta_ativo is True


def test_matricula_leva_direto_para_a_gestao_de_mensalidades(client, logar_como_admin, contexto_app):
    logar_como_admin()

    resposta = _matricular(client)

    assert resposta.headers['Location'].endswith('/admin/usuario/529.982.247-25')
    pagina = client.get('/admin/usuario/529.982.247-25')
    assert pagina.status_code == 200
    assert 'Controle de mensalidades' in pagina.get_data(as_text=True)


def test_admin_lanca_e_baixa_mensalidade_de_aluno_sem_acesso(client, logar_como_admin, plano, contexto_app):
    logar_como_admin()
    _matricular(client, plano_id=str(plano.id))
    aluno = AlunoDAO.buscar_por_cpf('529.982.247-25')

    resposta = client.post(
        f'/admin/usuario/{aluno.cpf}/pagamentos',
        data={
            'plano_id': str(plano.id), 'valor': '150.00',
            'vencimento': datetime.today().date().isoformat(),
            'status': 'pago', 'forma_pagamento': 'dinheiro',
            'data_pagamento': datetime.today().date().isoformat(),
        },
    )

    assert resposta.status_code == 302
    pagamentos = PagamentoDAO.listar_por_aluno(aluno.id)
    assert len(pagamentos) == 1
    assert regras_plano.situacao_plano(aluno, pagamentos).ativo is True
    assert db.session.get(Aluno, aluno.id).mensalidade == 'Em Dia'


def test_primeira_mensalidade_opcional_nao_duplica_cobranca(client, logar_como_admin, plano, contexto_app):
    logar_como_admin()

    _matricular(client, plano_id=str(plano.id), gerar_mensalidade='sim')

    aluno = AlunoDAO.buscar_por_cpf('529.982.247-25')
    pagamentos = PagamentoDAO.listar_por_aluno(aluno.id)
    assert len(pagamentos) == 1
    assert pagamentos[0].status == 'pendente'


def test_matricula_recusa_cpf_ja_cadastrado(client, logar_como_admin, criar_aluno, contexto_app):
    criar_aluno(nome='Antônia já cadastrada', cpf='529.982.247-25')
    logar_como_admin()

    resposta = _matricular(client)

    assert resposta.status_code == 400
    assert Aluno.query.filter_by(cpf='529.982.247-25').count() == 1


def test_matricula_recusa_cpf_invalido(client, logar_como_admin, contexto_app):
    logar_como_admin()

    resposta = _matricular(client, cpf='123')

    assert resposta.status_code == 400
    assert Aluno.query.count() == 0


@pytest.mark.parametrize('rota, metodo', [
    ('/admin/alunos/novo', 'get'),
    ('/admin/alunos/novo', 'post'),
    ('/admin/usuario/529.982.247-25/convite', 'post'),
    ('/admin/usuario/529.982.247-25/convite/revogar', 'post'),
])
def test_rotas_de_matricula_e_convite_sao_so_do_admin(client, criar_aluno, rota, metodo):
    aluno = criar_aluno(cpf='529.982.247-25')
    for sessao in ({}, {'tipo_usuario': 'aluno', 'aluno_id': aluno.id}, {'tipo_usuario': 'professor'}):
        with client.session_transaction() as sess:
            sess.clear()
            sess.update(sessao)
        resposta = getattr(client, metodo)(rota, data={})
        assert resposta.status_code == 302
        assert resposta.headers['Location'].endswith('/login')


# ----------------------------------------------------------------- acesso --

def test_aluno_sem_acesso_nao_entra_com_cpf_nem_com_qualquer_senha(client, logar_como_admin, contexto_app):
    logar_como_admin()
    _matricular(client)
    with client.session_transaction() as sess:
        sess.clear()

    for identificador in ('529.982.247-25', '52998224725'):
        resposta = client.post(
            '/login', data={'loginusuario': identificador, 'senhausuario': 'qualquer-coisa'},
        )
        assert 'Credenciais incorretas' in resposta.get_data(as_text=True)
        with client.session_transaction() as sess:
            assert 'aluno_id' not in sess


def test_convite_exige_email_no_cadastro(client, logar_como_admin, capturar_emails, contexto_app):
    logar_como_admin()
    _matricular(client)

    resposta = client.post('/admin/usuario/529.982.247-25/convite', data={'email': ''})

    assert resposta.status_code == 302
    aluno = AlunoDAO.buscar_por_cpf('529.982.247-25')
    assert aluno.token_convite_hash is None
    assert not [e for e in capturar_emails if e['link_url']]


def test_convite_registra_email_e_envia_link_de_uso_unico(client, logar_como_admin, capturar_emails, contexto_app):
    logar_como_admin()
    _matricular(client)

    resposta = client.post(
        '/admin/usuario/529.982.247-25/convite', data={'email': 'Antonia@Example.com'},
    )

    assert resposta.status_code == 302
    aluno = AlunoDAO.buscar_por_cpf('529.982.247-25')
    assert aluno.email == 'antonia@example.com'
    assert aluno.estado_acesso == 'convite_enviado'
    assert aluno.rotulo_acesso == 'Convite enviado'
    # O token viaja só no e-mail: o banco guarda apenas o resumo dele.
    token = _token_do_convite(capturar_emails)
    assert token not in (aluno.token_convite_hash or '')
    assert convites.aluno_do_token(token).id == aluno.id


def test_ativacao_vincula_conta_ao_mesmo_aluno_e_preserva_o_financeiro(
    client, logar_como_admin, capturar_emails, plano, contexto_app,
):
    logar_como_admin()
    _matricular(client, plano_id=str(plano.id), gerar_mensalidade='sim')
    client.post('/admin/usuario/529.982.247-25/convite', data={'email': 'antonia@example.com'})
    aluno_id = AlunoDAO.buscar_por_cpf('529.982.247-25').id
    pagamento_id = PagamentoDAO.listar_por_aluno(aluno_id)[0].id
    token = _token_do_convite(capturar_emails)
    with client.session_transaction() as sess:
        sess.clear()

    resposta = client.post(
        f'/ativar-acesso/{token}',
        data={
            'loginusuario': 'antonia', 'senhausuario': 'TreinoForte2026',
            'confirmarsenhausuario': 'TreinoForte2026', 'telefoneusuario': '11988887777',
        },
    )

    assert resposta.status_code == 200
    aluno = db.session.get(Aluno, aluno_id)
    assert aluno.acesso_ativado is True
    assert aluno.login == 'antonia'
    assert aluno.telefone == '(11) 98888-7777'
    # Nenhum cadastro novo, nenhuma mensalidade recriada.
    assert Aluno.query.count() == 1
    assert [p.id for p in PagamentoDAO.listar_por_aluno(aluno_id)] == [pagamento_id]
    assert aluno.plano_id == plano.id

    entrou = client.post('/login', data={'loginusuario': 'antonia', 'senhausuario': 'TreinoForte2026'})
    assert entrou.status_code == 302
    with client.session_transaction() as sess:
        assert sess['aluno_id'] == aluno_id


def test_token_de_ativacao_serve_uma_vez_so(client, logar_como_admin, capturar_emails, contexto_app):
    logar_como_admin()
    _matricular(client)
    client.post('/admin/usuario/529.982.247-25/convite', data={'email': 'antonia@example.com'})
    token = _token_do_convite(capturar_emails)
    with client.session_transaction() as sess:
        sess.clear()
    client.post(f'/ativar-acesso/{token}', data={
        'loginusuario': 'antonia', 'senhausuario': 'TreinoForte2026',
        'confirmarsenhausuario': 'TreinoForte2026',
    })

    segunda = client.post(f'/ativar-acesso/{token}', data={
        'loginusuario': 'invasor', 'senhausuario': 'OutraSenha2026',
        'confirmarsenhausuario': 'OutraSenha2026',
    })

    assert segunda.status_code == 400
    aluno = AlunoDAO.buscar_por_cpf('529.982.247-25')
    assert aluno.login == 'antonia'
    assert aluno.verificar_senha('OutraSenha2026') is False


def test_token_de_ativacao_expirado_nao_abre_a_conta(client, logar_como_admin, capturar_emails, contexto_app):
    logar_como_admin()
    _matricular(client)
    client.post('/admin/usuario/529.982.247-25/convite', data={'email': 'antonia@example.com'})
    token = _token_do_convite(capturar_emails)
    aluno = AlunoDAO.buscar_por_cpf('529.982.247-25')
    aluno.token_convite_expira = datetime.utcnow() - timedelta(minutes=1)
    db.session.commit()

    resposta = client.get(f'/ativar-acesso/{token}')

    assert resposta.status_code == 400
    assert AlunoDAO.buscar_por_cpf('529.982.247-25').acesso_ativado is False


def test_token_inventado_nao_abre_a_conta(client, logar_como_admin, contexto_app):
    logar_como_admin()
    _matricular(client)
    with client.session_transaction() as sess:
        sess.clear()

    resposta = client.post('/ativar-acesso/token-que-nunca-existiu', data={
        'loginusuario': 'invasor', 'senhausuario': 'SenhaDoInvasor1',
        'confirmarsenhausuario': 'SenhaDoInvasor1',
    })

    assert resposta.status_code == 400
    assert AlunoDAO.buscar_por_cpf('529.982.247-25').acesso_ativado is False


def test_tela_de_ativacao_nao_mostra_dado_pessoal_nem_financeiro(
    client, logar_como_admin, capturar_emails, plano, contexto_app,
):
    logar_como_admin()
    _matricular(client, plano_id=str(plano.id), gerar_mensalidade='sim')
    client.post('/admin/usuario/529.982.247-25/convite', data={'email': 'antonia@example.com'})
    token = _token_do_convite(capturar_emails)
    with client.session_transaction() as sess:
        sess.clear()

    pagina = client.get(f'/ativar-acesso/{token}').get_data(as_text=True)

    assert 'Antônia' in pagina                      # o primeiro nome, para se reconhecer
    assert '529.982.247-25' not in pagina
    assert '52998224725' not in pagina
    assert 'antonia@example.com' not in pagina      # o e-mail aparece mascarado
    assert 'an*****@example.com' in pagina
    assert plano.nome_plano not in pagina
    assert '150' not in pagina


def test_convite_revogado_derruba_o_link_enviado(client, logar_como_admin, capturar_emails, contexto_app):
    logar_como_admin()
    _matricular(client)
    client.post('/admin/usuario/529.982.247-25/convite', data={'email': 'antonia@example.com'})
    token = _token_do_convite(capturar_emails)

    client.post('/admin/usuario/529.982.247-25/convite/revogar')

    assert AlunoDAO.buscar_por_cpf('529.982.247-25').convite_pendente is False
    with client.session_transaction() as sess:
        sess.clear()
    assert client.get(f'/ativar-acesso/{token}').status_code == 400


def test_convite_recusado_para_quem_ja_tem_acesso(client, logar_como_admin, criar_aluno, capturar_emails, contexto_app):
    aluno = criar_aluno(cpf='529.982.247-25', email='antonia@example.com')
    logar_como_admin()

    resposta = client.post('/admin/usuario/529.982.247-25/convite', data={'email': 'antonia@example.com'})

    assert resposta.status_code == 302
    assert db.session.get(Aluno, aluno.id).token_convite_hash is None


# ------------------------------------------------------------ duplicidade --

def test_cadastro_publico_com_cpf_de_cadastro_administrativo_nao_duplica(
    client, logar_como_admin, capturar_emails, contexto_app,
):
    logar_como_admin()
    _matricular(client, email='antonia@example.com')
    with client.session_transaction() as sess:
        sess.clear()
    capturar_emails.clear()

    resposta = client.post('/cadastrar', data={
        'nomeusuario': 'Pessoa Qualquer', 'loginusuario': 'qualquer',
        'dataNascimento': '1948-03-12', 'cpfusuario': '529.982.247-25',
        'emailusuario': 'outro-endereco@example.com', 'telefoneusuario': '11999999999',
        'senhausuario': 'TreinoForte2026', 'confirmarsenhausuario': 'TreinoForte2026',
        'descricaousuario': '',
    })

    corpo = resposta.get_data(as_text=True)
    assert Aluno.query.count() == 1
    # Nada sobre quem já está na base: nem nome, nem e-mail, nem situação.
    assert 'Antônia' not in corpo and 'Souza' not in corpo
    assert 'antonia@example.com' not in corpo
    # O convite vai para o e-mail do cadastro, nunca para o que foi digitado agora.
    convite = next(e for e in capturar_emails if e['link_url'] and '/ativar-acesso/' in e['link_url'])
    assert convite['destinatario'] == 'antonia@example.com'


def test_cadastro_publico_com_cpf_sem_email_no_cadastro_nao_envia_nada(
    client, logar_como_admin, capturar_emails, contexto_app,
):
    logar_como_admin()
    _matricular(client)
    with client.session_transaction() as sess:
        sess.clear()
    capturar_emails.clear()

    client.post('/cadastrar', data={
        'nomeusuario': 'Pessoa Qualquer', 'loginusuario': 'qualquer',
        'dataNascimento': '1948-03-12', 'cpfusuario': '529.982.247-25',
        'emailusuario': 'outro-endereco@example.com', 'telefoneusuario': '11999999999',
        'senhausuario': 'TreinoForte2026', 'confirmarsenhausuario': 'TreinoForte2026',
        'descricaousuario': '',
    })

    assert Aluno.query.count() == 1
    assert AlunoDAO.buscar_por_cpf('529.982.247-25').email is None
    assert not [e for e in capturar_emails if e['link_url']]


def test_cadastro_publico_sem_conflito_continua_criando_a_conta(client, capturar_emails, contexto_app):
    resposta = client.post('/cadastrar', data={
        'nomeusuario': 'Bruno Alves', 'loginusuario': 'bruno',
        'dataNascimento': '1990-05-02', 'cpfusuario': '529.982.247-25',
        'emailusuario': 'bruno@example.com', 'telefoneusuario': '11999999999',
        'senhausuario': 'TreinoForte2026', 'confirmarsenhausuario': 'TreinoForte2026',
        'descricaousuario': '',
    })

    assert resposta.status_code == 200
    aluno = AlunoDAO.buscar_por_cpf('529.982.247-25')
    assert aluno.acesso_ativado is True
    assert aluno.status_cadastro == 'pendente'


# ---------------------------------------------------- confirmação de senha --

def test_cadastro_publico_recusa_confirmacao_diferente(client, contexto_app):
    resposta = client.post('/cadastrar', data={
        'nomeusuario': 'Bruno Alves', 'loginusuario': 'bruno',
        'dataNascimento': '1990-05-02', 'cpfusuario': '529.982.247-25',
        'emailusuario': 'bruno@example.com', 'telefoneusuario': '11999999999',
        'senhausuario': 'TreinoForte2026', 'confirmarsenhausuario': 'TreinoForte2027',
        'descricaousuario': '',
    })

    corpo = resposta.get_data(as_text=True)
    assert 'não são iguais' in corpo
    assert Aluno.query.count() == 0


def test_cadastro_publico_recusa_confirmacao_vazia(client, contexto_app):
    resposta = client.post('/cadastrar', data={
        'nomeusuario': 'Bruno Alves', 'loginusuario': 'bruno',
        'dataNascimento': '1990-05-02', 'cpfusuario': '529.982.247-25',
        'emailusuario': 'bruno@example.com', 'telefoneusuario': '11999999999',
        'senhausuario': 'TreinoForte2026', 'descricaousuario': '',
    })

    assert 'não são iguais' in resposta.get_data(as_text=True)
    assert Aluno.query.count() == 0


def test_ativacao_recusa_confirmacao_diferente(client, logar_como_admin, capturar_emails, contexto_app):
    logar_como_admin()
    _matricular(client)
    client.post('/admin/usuario/529.982.247-25/convite', data={'email': 'antonia@example.com'})
    token = _token_do_convite(capturar_emails)
    with client.session_transaction() as sess:
        sess.clear()

    resposta = client.post(f'/ativar-acesso/{token}', data={
        'loginusuario': 'antonia', 'senhausuario': 'TreinoForte2026',
        'confirmarsenhausuario': 'TreinoFort32026',
    })

    assert resposta.status_code == 400
    assert 'não são iguais' in resposta.get_data(as_text=True)
    assert AlunoDAO.buscar_por_cpf('529.982.247-25').acesso_ativado is False


def test_ativacao_mantem_as_regras_de_senha_do_projeto(client, logar_como_admin, capturar_emails, contexto_app):
    logar_como_admin()
    _matricular(client)
    client.post('/admin/usuario/529.982.247-25/convite', data={'email': 'antonia@example.com'})
    token = _token_do_convite(capturar_emails)
    with client.session_transaction() as sess:
        sess.clear()

    curta = client.post(f'/ativar-acesso/{token}', data={
        'loginusuario': 'antonia', 'senhausuario': 'abc123', 'confirmarsenhausuario': 'abc123',
    })
    comum = client.post(f'/ativar-acesso/{token}', data={
        'loginusuario': 'antonia', 'senhausuario': 'senha123', 'confirmarsenhausuario': 'senha123',
    })

    assert 'pelo menos 8 caracteres' in curta.get_data(as_text=True)
    assert 'menos comum' in comum.get_data(as_text=True)
    assert AlunoDAO.buscar_por_cpf('529.982.247-25').acesso_ativado is False


def test_confirmacao_de_senha_nao_e_gravada_nem_registrada_em_log(
    client, logar_como_admin, capturar_emails, caplog, contexto_app,
):
    logar_como_admin()
    _matricular(client)
    client.post('/admin/usuario/529.982.247-25/convite', data={'email': 'antonia@example.com'})
    token = _token_do_convite(capturar_emails)
    with client.session_transaction() as sess:
        sess.clear()

    with caplog.at_level('DEBUG'):
        client.post(f'/ativar-acesso/{token}', data={
            'loginusuario': 'antonia', 'senhausuario': 'TreinoForte2026',
            'confirmarsenhausuario': 'TreinoForte2026',
        })

    assert 'TreinoForte2026' not in caplog.text
    aluno = AlunoDAO.buscar_por_cpf('529.982.247-25')
    colunas = {c.name for c in Aluno.__table__.columns}
    assert not any('confirm' in coluna for coluna in colunas)
    assert 'TreinoForte2026' not in (aluno.senha_hash or '')


# ----------------------------------------------------- cadastros que já existem --

def test_aluno_existente_continua_entrando_normalmente(client, criar_aluno, contexto_app):
    aluno = criar_aluno(login='veterano', senha='TreinoForte2026', email='veterano@example.com')

    resposta = client.post('/login', data={'loginusuario': 'veterano', 'senhausuario': 'TreinoForte2026'})

    assert resposta.status_code == 302
    assert aluno.acesso_ativado is True
    with client.session_transaction() as sess:
        assert sess['aluno_id'] == aluno.id


def test_admin_nao_pode_apagar_o_usuario_de_uma_conta_ativa(client, logar_como_admin, criar_aluno, contexto_app):
    aluno = criar_aluno(cpf='529.982.247-25', login='veterano', email='veterano@example.com')
    logar_como_admin()

    resposta = client.post('/admin/usuario/529.982.247-25', data={
        'nome': aluno.nome, 'login': '', 'datanascimento': aluno.datanascimento,
        'email': '', 'telefone': aluno.telefone, 'plano_id': 'Nenhum', 'descricao': '',
    })

    assert resposta.status_code == 302
    recarregado = db.session.get(Aluno, aluno.id)
    assert recarregado.login == 'veterano'
    assert recarregado.email == 'veterano@example.com'


def test_admin_pode_deixar_cadastro_de_balcao_sem_usuario_e_sem_email(
    client, logar_como_admin, contexto_app,
):
    logar_como_admin()
    _matricular(client, email='antonia@example.com')

    resposta = client.post('/admin/usuario/529.982.247-25', data={
        'nome': 'Antônia Ribeiro Souza', 'login': '', 'datanascimento': '1948-03-12',
        'email': '', 'telefone': '11999999999', 'plano_id': 'Nenhum', 'descricao': '',
    })

    assert resposta.status_code == 302
    aluno = AlunoDAO.buscar_por_cpf('529.982.247-25')
    assert aluno.login is None and aluno.email is None
    assert aluno.acesso_ativado is False


# ------------------------------------------------------- avisos e cobrança --

def test_painel_de_avisos_separa_quem_deve_de_quem_da_para_avisar(
    client, logar_como_admin, criar_aluno, criar_pagamento, plano, contexto_app,
):
    from datetime import date, timedelta

    com_email = criar_aluno(cpf='111.222.333-44', email='com@example.com')
    criar_pagamento(aluno=com_email, status='atrasado', vencimento=date.today() - timedelta(days=10))
    logar_como_admin()
    _matricular(client)  # cadastro de balcão, sem e-mail
    sem_email = AlunoDAO.buscar_por_cpf('529.982.247-25')
    PagamentoDAO.salvar(Pagamento(
        aluno_id=sem_email.id, plano_id=plano.id, valor=150.0,
        vencimento=date.today() - timedelta(days=10), status='atrasado',
    ))

    pagina = client.get('/admin/avisos').get_data(as_text=True)

    # Os dois devem; só um tem canal de e-mail. O botão promete o que dá para cumprir.
    assert re.search(r'>2</strong>\s*<span>Com mensalidade pendente', pagina)
    assert re.search(r'>1</strong>\s*<span>Sem e-mail', pagina)
    assert 'Enviar cobrança para 1 aluno<' in pagina


def test_cobranca_em_massa_nao_conta_quem_nao_tem_email(
    client, logar_como_admin, criar_aluno, criar_pagamento, capturar_emails, contexto_app,
):
    from datetime import date, timedelta

    com_email = criar_aluno(cpf='111.222.333-44', email='com@example.com')
    criar_pagamento(aluno=com_email, status='atrasado', vencimento=date.today() - timedelta(days=10))
    logar_como_admin()
    _matricular(client)
    client.get('/admin/avisos')
    with client.session_transaction() as sess:
        token_aviso = sess['token_aviso']

    resposta = client.post('/admin/avisos/cobranca', data={'token_aviso': token_aviso}, follow_redirects=True)

    corpo = resposta.get_data(as_text=True)
    assert 'para 1 de 1 aluno' in corpo
    assert [e['destinatario'] for e in capturar_emails if 'pendente' in e['assunto']] == ['com@example.com']


def test_cobranca_individual_avisa_que_falta_email(client, logar_como_admin, contexto_app):
    logar_como_admin()
    _matricular(client)

    resposta = client.post('/admin/usuario/529.982.247-25/cobrar', follow_redirects=True)

    assert 'não tem e-mail cadastrado' in resposta.get_data(as_text=True)


def test_tentativas_de_adivinhar_token_sao_limitadas(client, contexto_app):
    respostas = [client.get(f'/ativar-acesso/tentativa-{i}').status_code for i in range(35)]

    assert 429 in respostas
    assert respostas.count(400) <= 30


@pytest.mark.parametrize('senha,confirmacao,esperado', [
    ('MuayThái2026!', 'MuayThái2026!', None),
    ('MuayThái2026!', 'MuayThai2026!', 'diferente'),
])
def test_confirmacao_aceita_unicode(senha, confirmacao, esperado):
    from servicos.senhas import erro_confirmacao_senha
    resultado = erro_confirmacao_senha(senha, confirmacao)
    assert (resultado is None) == (esperado is None)


@pytest.mark.parametrize('campos', [
    {'cpf': '529982247250'}, {'datanascimento': 'ontem'},
    {'datanascimento': '2999-01-01'}, {'plano_id': 'invalido'},
    {'nome': 'A' * 151}, {'graduacao': 'A' * 81}, {'email': 'invalido'},
])
def test_matricula_valida_dados_no_servidor(client, logar_como_admin, contexto_app, campos):
    logar_como_admin()
    assert _matricular(client, **campos).status_code == 400
    assert Aluno.query.count() == 0


def test_recuperacao_nao_ativa_cadastro_sem_conta(client, logar_como_admin, capturar_emails, contexto_app):
    logar_como_admin()
    _matricular(client, email='antonia@example.com')
    resposta = client.post('/recuperar_senha', data={
        'cpf': '529.982.247-25', 'email': 'antonia@example.com',
    })
    assert resposta.status_code == 200
    aluno = AlunoDAO.buscar_por_cpf('529.982.247-25')
    assert aluno.token_recuperacao_hash is None
    assert not capturar_emails


def test_troca_de_email_revoga_convite_anterior(client, logar_como_admin, capturar_emails, contexto_app):
    logar_como_admin()
    _matricular(client, email='antonia@example.com')
    client.post('/admin/usuario/529.982.247-25/convite')
    token = _token_do_convite(capturar_emails)
    client.post('/admin/usuario/529.982.247-25', data={
        'nome': 'Antônia Ribeiro', 'datanascimento': '1948-03-12',
        'email': 'novo@example.com', 'plano_id': 'Nenhum',
    })
    assert client.get(f'/ativar-acesso/{token}').status_code == 400


def test_ativacao_revalida_token_no_momento_da_gravacao(
    client, logar_como_admin, capturar_emails, contexto_app, monkeypatch,
):
    logar_como_admin()
    _matricular(client, email='antonia@example.com')
    client.post('/admin/usuario/529.982.247-25/convite')
    token = _token_do_convite(capturar_emails)
    buscar = convites.aluno_do_token

    def revogar_apos_leitura(valor):
        aluno = buscar(valor)
        # Simula outra requisição revogando o token entre a leitura e a escrita.
        Aluno.query.filter_by(id=aluno.id).update({
            'token_convite_hash': None, 'token_convite_expira': None,
        }, synchronize_session=False)
        db.session.commit()
        return aluno

    monkeypatch.setattr(convites, 'aluno_do_token', revogar_apos_leitura)
    resposta = client.post(f'/ativar-acesso/{token}', data={
        'loginusuario': 'antonia', 'senhausuario': 'MuayThái2026!',
        'confirmarsenhausuario': 'MuayThái2026!',
    })
    assert resposta.status_code == 400
    assert not AlunoDAO.buscar_por_cpf('529.982.247-25').acesso_ativado


def test_ativacao_com_senha_unicode(client, logar_como_admin, capturar_emails, contexto_app):
    logar_como_admin()
    _matricular(client, email='antonia@example.com')
    client.post('/admin/usuario/529.982.247-25/convite')
    token = _token_do_convite(capturar_emails)
    resposta = client.post(f'/ativar-acesso/{token}', data={
        'loginusuario': 'antonia', 'senhausuario': 'MuayThái2026!',
        'confirmarsenhausuario': 'MuayThái2026!',
    })
    assert resposta.status_code == 200
    assert AlunoDAO.buscar_por_cpf('529.982.247-25').verificar_senha('MuayThái2026!')


def test_pedido_publico_nao_invalida_convite_ainda_valido(
    client, logar_como_admin, capturar_emails, contexto_app,
):
    from blueprints.usuario_bp import _convidar_cadastro_existente
    logar_como_admin()
    _matricular(client, email='antonia@example.com')
    client.post('/admin/usuario/529.982.247-25/convite')
    token = _token_do_convite(capturar_emails)
    quantidade = len(capturar_emails)
    _convidar_cadastro_existente(AlunoDAO.buscar_por_cpf('529.982.247-25'))
    assert len(capturar_emails) == quantidade
    assert convites.aluno_do_token(token) is not None


def test_token_recuperacao_antigo_nao_cria_conta_sem_convite(
    client, logar_como_admin, contexto_app,
):
    import hashlib
    logar_como_admin()
    _matricular(client, email='antonia@example.com')
    aluno = AlunoDAO.buscar_por_cpf('529.982.247-25')
    aluno.token_recuperacao_hash = hashlib.sha256(b'token-antigo').hexdigest()
    aluno.token_recuperacao_expira = datetime.utcnow() + timedelta(minutes=20)
    db.session.commit()
    client.post('/recuperar_senha/token-antigo', data={'nova_senha': 'OutraSenha2026!'})
    assert not aluno.acesso_ativado


@pytest.mark.parametrize('rota', [
    '/admin/alunos/novo', '/admin/usuario/529.982.247-25/convite',
    '/admin/usuario/529.982.247-25/convite/revogar', '/ativar-acesso/token',
])
def test_novos_formularios_exigem_csrf(client, app, logar_como_admin, rota):
    logar_como_admin()
    app.config['WTF_CSRF_ENABLED'] = True
    try:
        resposta = client.post(rota, data={})
        assert resposta.status_code == 400
        assert 'segurança expirou' in resposta.get_data(as_text=True)
    finally:
        app.config['WTF_CSRF_ENABLED'] = False


def test_falha_de_envio_preserva_convite_anterior(
    client, logar_como_admin, capturar_emails, contexto_app, monkeypatch,
):
    logar_como_admin()
    _matricular(client, email='antonia@example.com')
    client.post('/admin/usuario/529.982.247-25/convite')
    token = _token_do_convite(capturar_emails)
    monkeypatch.setattr(convites, 'enviar_email', lambda *a, **kw: False)
    client.post('/admin/usuario/529.982.247-25/convite', data={'email': 'novo@example.com'})
    assert convites.aluno_do_token(token) is not None
    assert AlunoDAO.buscar_por_cpf('529.982.247-25').email == 'antonia@example.com'


def test_convite_com_email_duplicado_nao_envia_link(
    client, app, logar_como_admin, capturar_emails, contexto_app, criar_aluno,
):
    criar_aluno(email='ocupado@example.com')
    logar_como_admin()
    _matricular(client, email='antonia@example.com')
    aluno = AlunoDAO.buscar_por_cpf('529.982.247-25')
    aluno.email = 'ocupado@example.com'
    with app.test_request_context('/admin'):
        with pytest.raises(convites.ConviteIndisponivel, match='já está em uso'):
            convites.enviar(aluno)
    assert not capturar_emails
    assert aluno.email == 'antonia@example.com'
