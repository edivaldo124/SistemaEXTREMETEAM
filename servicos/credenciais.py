"""Credencial administrativa baseada exclusivamente em hash de senha.

O administrador existe antes de qualquer dado do banco, portanto suas credenciais vêm
do ambiente. A senha nunca é aceita em texto puro: `ADMIN_PASSWORD_HASH` deve conter o
valor produzido por `werkzeug.security.generate_password_hash`, no mesmo formato usado
para alunos e professores.

Com `ADMIN_TOTP_SECRET` definida, a senha passa a ser só o primeiro fator: o login do
admin pede também o código de 6 dígitos de um app autenticador (TOTP, RFC 6238).
"""
import base64
import hashlib
import hmac
import os
import re
import secrets
import struct
import time
from urllib.parse import quote

from werkzeug.security import check_password_hash, generate_password_hash

# Segundo fator do administrador (SEC-30): 6 dígitos, passo de 30 s e HMAC-SHA1, o formato
# que todo app autenticador lê. Feito com a biblioteca padrão para não trazer dependência.
TOTP_PASSO_SEGUNDOS = 30
TOTP_DIGITOS = 6
# Aceita também o passo anterior e o seguinte: o relógio do celular até 30 s fora não trava.
TOTP_TOLERANCIA_PASSOS = 1
# A RFC 4226 exige pelo menos 128 bits de segredo (e recomenda 160).
TOTP_SEGREDO_MINIMO_BYTES = 16

def comparar_em_tempo_constante(informada, esperada):
    """Compara duas senhas em tempo constante, sem restrição de alfabeto.

    Codificar antes é o que permite acento, cedilha e emoji: a senha não é normalizada
    nem truncada em momento nenhum, então o que o usuário digitou é exatamente o que é
    comparado.
    """
    return hmac.compare_digest(
        (informada or '').encode('utf-8'), (esperada or '').encode('utf-8'),
    )


def admin_configurado():
    """True quando existe usuário e hash da senha do administrador."""
    return bool(os.environ.get('ADMIN_USER')) and bool(os.environ.get('ADMIN_PASSWORD_HASH'))


def credencial_admin_confere(login, senha):
    """Confere usuário e senha do administrador contra o ambiente."""
    usuario = os.environ.get('ADMIN_USER')
    hash_configurado = os.environ.get('ADMIN_PASSWORD_HASH')

    if not usuario or not hash_configurado:
        return False

    # O usuário é comparado PRIMEIRO, em tempo constante, e a senha só é processada
    # quando ele confere.
    #
    # Gastar o hash antes esconderia o tempo, mas ao custo de um scrypt (~74 ms e ~32 MB
    # medidos) em TODO login - inclusive o de aluno, que já paga o seu próprio logo em
    # seguida. São dois scrypt por login num container de 192 MB com 2 threads, para
    # esconder apenas se o texto digitado é igual ao nome de usuário do administrador -
    # que não é segredo e cujas tentativas já são limitadas a 5 por 15 minutos por
    # IP+identificador. A senha, essa sim, continua comparada em tempo constante.
    if not comparar_em_tempo_constante(login, usuario):
        return False

    return check_password_hash(hash_configurado, senha or '')


def referencia_credencial_admin():
    """Valor que representa a credencial administrativa em vigor, ou None se não há uma.

    Serve ao mesmo carimbo de sessão usado para alunos e professores: quando muda, as
    sessões administrativas abertas com a credencial anterior deixam de valer. Não é a
    senha - é o hash configurado, que nunca sai daqui (quem o consome só o transforma
    de novo em `impressao_credencial`).

    Com o segundo fator, entra também um resumo do segredo (nunca o segredo: o carimbo
    fica no cookie): ligar, trocar ou desligar o código encerra as sessões de admin
    abertas antes, que não passaram por ele.
    """
    hash_senha = os.environ.get('ADMIN_PASSWORD_HASH')
    segredo = (os.environ.get('ADMIN_TOTP_SECRET') or '').strip()
    if hash_senha and segredo:
        return f"{hash_senha}|totp:{hashlib.sha256(segredo.encode('utf-8')).hexdigest()}"
    return hash_senha


def gerar_hash_admin(senha):
    """Gera o valor de ADMIN_PASSWORD_HASH. Usado pelo utilitário de linha de comando."""
    return generate_password_hash(senha)


def _segredo_totp_admin():
    """Bytes do ADMIN_TOTP_SECRET (base32, como o app autenticador mostra), ou None se vazio.

    Levanta ValueError quando a variável existe mas não é um segredo utilizável.
    """
    texto = re.sub(r'[\s-]', '', os.environ.get('ADMIN_TOTP_SECRET') or '').upper()
    if not texto:
        return None
    try:
        segredo = base64.b32decode(texto + '=' * (-len(texto) % 8))
    except ValueError as exc:
        raise ValueError('ADMIN_TOTP_SECRET não está em base32.') from exc
    if len(segredo) < TOTP_SEGREDO_MINIMO_BYTES:
        raise ValueError(
            'ADMIN_TOTP_SECRET é curta demais. Gere uma com: python -m servicos.credenciais totp'
        )
    return segredo


def segundo_fator_admin_ativo():
    """True quando o login do admin exige o código do app autenticador."""
    return bool((os.environ.get('ADMIN_TOTP_SECRET') or '').strip())


def validar_segundo_fator_admin():
    """No arranque: ValueError se ADMIN_TOTP_SECRET estiver definida e inválida."""
    _segredo_totp_admin()


def codigo_totp(segredo, passo):
    """Código do passo de tempo `passo` (truncamento dinâmico da RFC 4226)."""
    resumo = hmac.new(segredo, struct.pack('>Q', passo), hashlib.sha1).digest()
    inicio = resumo[-1] & 0x0F
    numero = struct.unpack('>I', resumo[inicio:inicio + 4])[0] & 0x7FFFFFFF
    return str(numero % 10 ** TOTP_DIGITOS).zfill(TOTP_DIGITOS)


def passo_do_codigo_admin(codigo, agora=None):
    """Passo de tempo em que `codigo` vale para o admin, ou None se não confere.

    Confere todos os passos da tolerância em tempo constante, sem parar no primeiro.
    """
    codigo = re.sub(r'\s', '', codigo or '')
    if not re.fullmatch(rf'[0-9]{{{TOTP_DIGITOS}}}', codigo):
        return None
    try:
        segredo = _segredo_totp_admin()
    except ValueError:
        return None
    if segredo is None:
        return None
    atual = int((time.time() if agora is None else agora) // TOTP_PASSO_SEGUNDOS)
    encontrado = None
    for passo in range(atual - TOTP_TOLERANCIA_PASSOS, atual + TOTP_TOLERANCIA_PASSOS + 1):
        if hmac.compare_digest(codigo_totp(segredo, passo), codigo):
            encontrado = passo
    return encontrado


def gerar_segredo_totp():
    """Segredo novo de 160 bits em base32 (32 caracteres), para ADMIN_TOTP_SECRET."""
    return base64.b32encode(secrets.token_bytes(20)).decode('ascii')


def _main_totp():
    """`python -m servicos.credenciais totp` - gera o ADMIN_TOTP_SECRET e explica o cadastro."""
    segredo = gerar_segredo_totp()
    rotulo = quote(f"Extreme Team:{os.environ.get('ADMIN_USER') or 'admin'}")
    print('No app autenticador (Google Authenticator, Microsoft Authenticator, Authy ou')
    print('1Password), escolha "inserir chave de configuração", tipo "baseada em tempo", e')
    print('digite a chave abaixo:')
    print()
    print('    ' + ' '.join(segredo[i:i + 4] for i in range(0, len(segredo), 4)))
    print()
    print('Ou gere o QR code num programa local (nunca num site) a partir de:')
    print(f'    otpauth://totp/{rotulo}?secret={segredo}&issuer=Extreme%20Team&digits=6&period=30')
    print()
    print('Quando o app já estiver mostrando os códigos, defina no ambiente:')
    print()
    print(f'ADMIN_TOTP_SECRET={segredo}')
    print()
    print('As sessões de admin abertas se encerram e o próximo login pede o código.')


def _main():
    """`python -m servicos.credenciais` - gera o valor de ADMIN_PASSWORD_HASH.
    `python -m servicos.credenciais totp` - gera o ADMIN_TOTP_SECRET (segundo fator).

    A senha é lida sem eco e nunca aparece em argumento de linha de comando (que ficaria
    visível em `ps` e no histórico do shell). O que sai na tela é só o hash.
    """
    import getpass
    import sys

    if sys.argv[1:] == ['totp']:
        _main_totp()
        return

    senha = getpass.getpass('Nova senha do administrador: ')
    if not senha:
        print('Nenhuma senha informada.', file=sys.stderr)
        raise SystemExit(1)
    if senha != getpass.getpass('Repita a senha: '):
        print('As senhas não coincidem.', file=sys.stderr)
        raise SystemExit(1)
    if len(senha) < 12:
        print('Use pelo menos 12 caracteres para a conta administrativa.', file=sys.stderr)
        raise SystemExit(1)

    print()
    print('Coloque a linha abaixo no .env:')
    print()
    print(f"ADMIN_PASSWORD_HASH='{gerar_hash_admin(senha)}'")
    print('As aspas simples são necessárias no .env; no painel da Vercel, informe o valor sem aspas.')


if __name__ == '__main__':
    _main()
