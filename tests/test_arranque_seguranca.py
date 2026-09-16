"""Validações feitas por servidor.py no arranque (COOKIE_SECURE, TRUSTED_HOSTS, HSTS).

Cada caso importa servidor.py num PROCESSO SEPARADO, nunca no processo da suíte:
essas checagens rodam uma única vez, na importação do módulo, e servidor.py já
está importado (com seu próprio `app`) pelo `conftest.py` para todo o resto dos
testes. Reimportar no mesmo processo reconstruiria `app` e reaplicaria
`db.init_app`/`register_blueprint` por cima do app que os outros testes usam.
"""
import subprocess
import sys
from pathlib import Path

from werkzeug.security import generate_password_hash

REPO_ROOT = str(Path(__file__).resolve().parent.parent)

_HASH_ADMIN_TESTE = generate_password_hash('senha-de-teste-nao-usar-em-producao')

# Variáveis que cada caso controla explicitamente. Removidas do ambiente herdado do
# processo pai (que já tem as suas, vindas do conftest.py) para o subprocesso partir
# de uma base conhecida em vez de misturar as duas.
_CHAVES_CONTROLADAS = (
    'COOKIE_SECURE', 'TRUSTED_HOSTS', 'APP_BASE_URL', 'SECRET_KEY', 'DATABASE_URL',
    'ADMIN_USER', 'ADMIN_PASSWORD_HASH', 'ADMIN_PASSWORD', 'TRUST_PROXY_COUNT',
    'CRIAR_SCHEMA_NA_IMPORTACAO',
)


def _env_arranque(tmp_path, **overrides):
    import os

    base = {
        chave: valor for chave, valor in os.environ.items() if chave not in _CHAVES_CONTROLADAS
    }
    base.update({
        'SECRET_KEY': 'chave-de-teste-nao-usar-em-producao',
        'DATABASE_URL': f'sqlite:///{tmp_path}/teste-arranque.db',
        'ADMIN_USER': 'admin-teste',
        'ADMIN_PASSWORD_HASH': _HASH_ADMIN_TESTE,
        'TRUSTED_HOSTS': 'localhost',
        'TRUST_PROXY_COUNT': '0',
        # Sempre presentes, mesmo vazias: servidor.py chama load_dotenv(), que só NÃO
        # sobrescreve uma variável já definida - se ela estiver simplesmente ausente
        # daqui, o valor real do .env do projeto vaza para o subprocesso de teste.
        'COOKIE_SECURE': '',
        'APP_BASE_URL': '',
    })
    base.update(overrides)
    return base


def _rodar(tmp_path, codigo='import servidor', **overrides):
    return subprocess.run(
        [sys.executable, '-c', codigo],
        cwd=REPO_ROOT,
        env=_env_arranque(tmp_path, **overrides),
        capture_output=True,
        text=True,
        timeout=30,
    )


def test_arranque_falha_sem_trusted_hosts(tmp_path):
    resultado = _rodar(tmp_path, TRUSTED_HOSTS='')
    assert resultado.returncode != 0
    assert 'TRUSTED_HOSTS' in resultado.stderr


def test_arranque_falha_com_cookie_secure_invalido(tmp_path):
    resultado = _rodar(tmp_path, COOKIE_SECURE='talvez')
    assert resultado.returncode != 0
    assert 'COOKIE_SECURE deve ser true ou false' in resultado.stderr


def test_arranque_falha_com_cookie_secure_false_e_app_base_url_https(tmp_path):
    resultado = _rodar(
        tmp_path, COOKIE_SECURE='false', APP_BASE_URL='https://academia.example.com',
    )
    assert resultado.returncode != 0
    assert 'COOKIE_SECURE=false' in resultado.stderr


def test_cookie_secure_false_continua_permitido_sem_app_base_url_https(tmp_path):
    """Desenvolvimento local sem HTTPS (sem Caddy) não pode ficar travado."""
    resultado = _rodar(tmp_path, COOKIE_SECURE='false', APP_BASE_URL='')
    assert resultado.returncode == 0, resultado.stderr


def test_cookie_secure_padrao_e_true(tmp_path):
    resultado = _rodar(
        tmp_path,
        codigo='import servidor; print(servidor.app.config["SESSION_COOKIE_SECURE"])',
        COOKIE_SECURE='',
        APP_BASE_URL='',
    )
    assert resultado.returncode == 0, resultado.stderr
    assert resultado.stdout.strip() == 'True'


def test_hsts_presente_para_dominio_publico_https(tmp_path):
    resultado = _rodar(
        tmp_path,
        codigo=(
            "import servidor\n"
            "cliente = servidor.app.test_client()\n"
            "resposta = cliente.get('/health')\n"
            "print(resposta.headers.get('Strict-Transport-Security', ''))\n"
        ),
        APP_BASE_URL='https://academia.example.com',
    )
    assert resultado.returncode == 0, resultado.stderr
    assert resultado.stdout.strip() == 'max-age=31536000'


def test_hsts_ausente_para_localhost(tmp_path):
    resultado = _rodar(
        tmp_path,
        codigo=(
            "import servidor\n"
            "cliente = servidor.app.test_client()\n"
            "resposta = cliente.get('/health')\n"
            "print(repr(resposta.headers.get('Strict-Transport-Security')))\n"
        ),
        APP_BASE_URL='https://localhost',
    )
    assert resultado.returncode == 0, resultado.stderr
    assert resultado.stdout.strip() == 'None'


def test_hsts_ausente_sem_app_base_url(tmp_path):
    resultado = _rodar(
        tmp_path,
        codigo=(
            "import servidor\n"
            "cliente = servidor.app.test_client()\n"
            "resposta = cliente.get('/health')\n"
            "print(repr(resposta.headers.get('Strict-Transport-Security')))\n"
        ),
        APP_BASE_URL='',
    )
    assert resultado.returncode == 0, resultado.stderr
    assert resultado.stdout.strip() == 'None'


def test_gerador_de_hash_imprime_entre_aspas_simples():
    """`python -m servicos.credenciais`: o hash sai entre aspas simples.

    O hash do Werkzeug contém `$` (ex.: scrypt:32768:8:1$sal$hash), e o Docker Compose
    interpola `$` em valores do .env - sem aspas simples ao redor, o hash chegaria
    corrompido na aplicação.
    """
    resultado = subprocess.run(
        [sys.executable, '-m', 'servicos.credenciais'],
        cwd=REPO_ROOT,
        input='senha-de-teste-bem-longa\nsenha-de-teste-bem-longa\n',
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert resultado.returncode == 0, resultado.stderr
    linha = next(
        linha for linha in resultado.stdout.splitlines()
        if linha.startswith('ADMIN_PASSWORD_HASH=')
    )
    assert linha.startswith("ADMIN_PASSWORD_HASH='")
    assert linha.endswith("'")
