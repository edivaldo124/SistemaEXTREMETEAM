from modelos.usuario import Aluno


def _dados_cadastro(**sobrescritas):
    dados = {
        'nomeusuario': 'Bruno Alves',
        'loginusuario': 'bruno',
        'dataNascimento': '1990-05-02',
        'cpfusuario': '529.982.247-25',
        'emailusuario': 'bruno@example.com',
        'telefoneusuario': '11999999999',
        'senhausuario': 'TreinoForte2026',
        'confirmarsenhausuario': 'TreinoForte2026',
        'descricaousuario': '',
    }
    dados.update(sobrescritas)
    return dados


def test_termo_e_publico_e_identifica_sua_versao(client):
    resposta = client.get('/termos-de-responsabilidade')

    corpo = resposta.get_data(as_text=True)
    assert resposta.status_code == 200
    assert 'Termo de Responsabilidade' in corpo
    assert 'Versão 2026-09' in corpo


def test_cadastro_exige_aceite_do_termo(client, contexto_app):
    resposta = client.post('/cadastrar', data=_dados_cadastro())

    assert 'Leia e aceite o Termo de Responsabilidade' in resposta.get_data(as_text=True)
    assert Aluno.query.count() == 0


def test_cadastro_registra_versao_e_horario_do_aceite(client, sem_email, contexto_app):
    resposta = client.post(
        '/cadastrar',
        data=_dados_cadastro(aceite_termos_responsabilidade='aceito'),
    )

    aluno = Aluno.query.one()
    assert resposta.status_code == 200
    assert aluno.termos_responsabilidade_versao == '2026-09'
    assert aluno.termos_responsabilidade_aceito_em is not None
