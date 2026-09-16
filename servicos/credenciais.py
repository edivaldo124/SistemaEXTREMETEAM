"""Credencial administrativa baseada exclusivamente em hash de senha.

O administrador existe antes de qualquer dado do banco, portanto suas credenciais vêm
do ambiente. A senha nunca é aceita em texto puro: `ADMIN_PASSWORD_HASH` deve conter o
valor produzido por `werkzeug.security.generate_password_hash`, no mesmo formato usado
para alunos e professores.
"""
import hmac
import os

from werkzeug.security import check_password_hash, generate_password_hash

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
    """
    return os.environ.get('ADMIN_PASSWORD_HASH')


def gerar_hash_admin(senha):
    """Gera o valor de ADMIN_PASSWORD_HASH. Usado pelo utilitário de linha de comando."""
    return generate_password_hash(senha)


def _main():
    """`python -m servicos.credenciais` - gera o valor de ADMIN_PASSWORD_HASH.

    A senha é lida sem eco e nunca aparece em argumento de linha de comando (que ficaria
    visível em `ps` e no histórico do shell). O que sai na tela é só o hash.
    """
    import getpass
    import sys

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
    print('As aspas simples são necessárias no .env; no painel do Render, informe o valor sem aspas.')


if __name__ == '__main__':
    _main()
