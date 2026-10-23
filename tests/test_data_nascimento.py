"""Data de nascimento: o mesmo seletor de data e a mesma regra no cadastro, na matrícula e na
ficha do aluno.

A ficha do admin era um campo de texto livre: mostrava o AAAA-MM-DD cru do banco e gravava
qualquer texto ("ontem", data no futuro, dd/mm/aaaa). Agora usa <input type="date"> e valida
como as outras duas telas: data real e que já passou.
"""
import re
from datetime import date, timedelta

import pytest

from config import db
from modelos.usuario import Aluno
from servicos.formatacao import data_iso

CPF = '529.982.247-25'


@pytest.mark.parametrize('valor,esperado', [
    ('2000-01-31', '2000-01-31'),
    ('31/01/2000', '2000-01-31'),
    ('1/2/2000', '2000-02-01'),
    ('31-01-2000', '2000-01-31'),
    ('31/02/2000', ''),
    ('ontem', ''),
    ('', ''),
    (None, ''),
])
def test_data_iso_aceita_aaaa_mm_dd_e_dd_mm_aaaa(valor, esperado):
    assert data_iso(valor) == esperado


def _salvar_ficha(client, aluno, nascimento):
    return client.post(f'/admin/usuario/{CPF}', data={
        'nome': aluno.nome, 'login': aluno.login, 'datanascimento': nascimento,
        'email': aluno.email, 'telefone': aluno.telefone, 'plano_id': 'Nenhum', 'descricao': '',
    })


@pytest.mark.parametrize('nascimento', ['ontem', (date.today() + timedelta(days=1)).isoformat(), ''])
def test_ficha_do_admin_recusa_data_invalida_ou_futura(client, logar_como_admin, criar_aluno, nascimento):
    aluno = criar_aluno(cpf=CPF, datanascimento='1990-05-20')
    logar_como_admin()

    resposta = _salvar_ficha(client, aluno, nascimento)

    assert resposta.status_code == 302
    assert resposta.headers['Location'].endswith(f'/admin/usuario/{CPF}')
    db.session.expire_all()
    assert db.session.get(Aluno, aluno.id).datanascimento == '1990-05-20'


@pytest.mark.parametrize('enviado,gravado', [('1991-07-09', '1991-07-09'), ('09/07/1991', '1991-07-09')])
def test_ficha_do_admin_grava_no_formato_do_seletor(client, logar_como_admin, criar_aluno, enviado, gravado):
    aluno = criar_aluno(cpf=CPF, datanascimento='1990-05-20')
    logar_como_admin()

    resposta = _salvar_ficha(client, aluno, enviado)

    assert resposta.status_code == 302
    assert resposta.headers['Location'].endswith('/admin')
    db.session.expire_all()
    assert db.session.get(Aluno, aluno.id).datanascimento == gravado


def test_ficha_mostra_no_seletor_a_data_digitada_no_campo_antigo(client, logar_como_admin, criar_aluno):
    # Sem a conversão, o dd/mm/aaaa gravado pelo campo de texto apareceria vazio no seletor.
    criar_aluno(cpf=CPF, datanascimento='20/05/1990')
    logar_como_admin()

    html = client.get(f'/admin/usuario/{CPF}').get_data(as_text=True)

    campo = re.search(r'<input[^>]*id="dt-nascimento"[^>]*>', html, re.S).group(0)
    assert 'type="date"' in campo
    assert 'value="1990-05-20"' in campo
    assert f'max="{date.today().isoformat()}"' in campo


@pytest.mark.parametrize('caminho,campo,admin', [
    ('/cadastrar', 'dataNascimento', False),
    ('/admin/alunos/novo', 'novo-nascimento', True),
])
def test_seletor_de_data_nao_oferece_o_futuro(client, logar_como_admin, caminho, campo, admin):
    if admin:
        logar_como_admin()

    html = client.get(caminho).get_data(as_text=True)

    tag = re.search(rf'<input[^>]*id="{campo}"[^>]*>', html, re.S).group(0)
    assert f'max="{date.today().isoformat()}"' in tag
