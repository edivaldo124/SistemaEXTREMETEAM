"""Logs da aplicação não guardam o e-mail completo de quem se cadastra.

O log da hospedagem (Vercel, Docker) fica fora do banco e do controle de acesso do sistema:
um e-mail inteiro ali é dado pessoal espalhado (LGPD). O Sentry já mascara o que recebe,
mas a saída padrão do processo não passa por ele.
"""

import logging

DADOS_CADASTRO = {
    'nomeusuario': 'Pessoa Cadastrada', 'loginusuario': 'pessoa-log',
    'dataNascimento': '1995-03-10', 'cpfusuario': '529.982.247-25',
    'senhausuario': 'Treino-Forte-2026', 'confirmarsenhausuario': 'Treino-Forte-2026',
    'emailusuario': 'pessoa.cadastrada@example.com', 'telefoneusuario': '11988887777',
    'descricaousuario': '', 'aceite_termos_responsabilidade': 'aceito',
}


def test_falha_no_link_de_verificacao_nao_grava_o_email_inteiro(client, sem_email, monkeypatch, caplog):
    # APP_BASE_URL inválida: o link de verificação não pode ser montado e o cadastro avisa no log.
    monkeypatch.setenv('APP_BASE_URL', 'nao-e-uma-url')

    with caplog.at_level(logging.ERROR):
        resposta = client.post('/cadastrar', data=DADOS_CADASTRO)

    assert resposta.status_code in (200, 302)
    mensagens = [registro.getMessage() for registro in caplog.records]
    aviso = [m for m in mensagens if 'e-mail de verificação não enviado' in m]
    assert aviso, mensagens
    assert all('pessoa.cadastrada@example.com' not in m for m in mensagens)
    assert '@example.com' in aviso[0]
