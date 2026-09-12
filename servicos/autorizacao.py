"""Autorização das rotas protegidas.

A sessão diz quem *afirmou* ser quem; quem decide se esse acesso ainda vale é sempre o
banco, a cada requisição. Antes, desativar ou reprovar um aluno só barrava um login
novo: quem já tinha o cookie continuava entrando no perfil, nas mensalidades e na foto
até a sessão expirar por tempo.

Duas verificações acontecem aqui, juntas:

1. O estado atual da conta (`esta_ativo` para o aluno, existência para o professor).
2. A impressão da credencial guardada no login. Ela deriva do hash da senha, então
   qualquer troca de senha - pelo perfil, pela recuperação ou pela administração -
   muda o hash e invalida em bloco as sessões abertas com a senha anterior.
"""
import hashlib
import hmac
from functools import wraps

from flask import redirect, session

CHAVE_CREDENCIAL = 'credencial'


def impressao_credencial(senha_hash):
    """Resumo curto e não reversível do hash da senha, guardado na sessão.

    Nunca é a senha nem o hash: é um SHA-256 truncado do hash, suficiente para detectar
    que a credencial mudou e inútil para quem leia o cookie (que já é assinado).
    """
    if not senha_hash:
        return None
    return hashlib.sha256(senha_hash.encode('utf-8')).hexdigest()[:32]


def registrar_credencial(senha_hash):
    """Grava na sessão atual a credencial em vigor (login ou troca de senha bem-sucedida)."""
    session[CHAVE_CREDENCIAL] = impressao_credencial(senha_hash)


def _credencial_confere(senha_hash):
    """A sessão foi emitida para a credencial que vale AGORA?

    Uma sessão sem carimbo é recusada, não aceita "só desta vez". Aceitá-la abriria
    exatamente o buraco que este controle fecha: um cookie roubado antes da publicação
    sobreviveria à troca de senha feita para expulsá-lo. O preço é que a publicação
    encerra as sessões abertas uma única vez - todo mundo entra de novo, e a partir daí
    nada mais é deslogado sem motivo. Está descrito no README.
    """
    esperada = impressao_credencial(senha_hash)
    guardada = session.get(CHAVE_CREDENCIAL)
    if esperada is None or guardada is None:
        # esperada None = conta sem senha (cadastro de balcão), que não sustenta sessão.
        return False
    return hmac.compare_digest(str(guardada), esperada)


def aluno_autorizado():
    """Aluno da sessão, revalidado no banco, ou None se o acesso não vale mais."""
    from config import db
    from modelos.usuario import Aluno

    if session.get('tipo_usuario') != 'aluno' or not session.get('aluno_id'):
        return None

    aluno = db.session.get(Aluno, session['aluno_id'])
    if aluno is None or not aluno.esta_ativo or not _credencial_confere(aluno.senha_hash):
        encerrar_sessao()
        return None
    return aluno


def professor_autorizado():
    """Professor da sessão, revalidado no banco, ou None se o cadastro não existe mais."""
    from config import db
    from modelos.professor import Professor

    if session.get('tipo_usuario') != 'professor' or not session.get('professor_id'):
        return None

    professor = db.session.get(Professor, session['professor_id'])
    if professor is None or not _credencial_confere(professor.senha_hash):
        encerrar_sessao()
        return None
    return professor


def encerrar_sessao():
    session.clear()


def sessao_administrativa_valida():
    """Sessão de administrador ainda válida para a credencial em vigor.

    O admin não tem linha no banco: a credencial dele vem do ambiente. Mesmo assim a
    sessão é carimbada da mesma forma, senão a conta de MAIOR privilégio seria a única
    isenta da revogação - trocar ADMIN_PASSWORD_HASH depois de um vazamento não
    encerraria a sessão já aberta por quem usou a senha antiga.
    """
    if session.get('tipo_usuario') != 'admin':
        return False

    from servicos.credenciais import referencia_credencial_admin

    referencia = referencia_credencial_admin()
    if referencia is None or not _credencial_confere(referencia):
        encerrar_sessao()
        return False
    return True


def admin_requerido(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not sessao_administrativa_valida():
            return redirect('/login')
        return view(*args, **kwargs)
    return wrapper


def professor_ou_admin_requerido(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if sessao_administrativa_valida():
            return view(*args, **kwargs)
        if professor_autorizado() is None:
            return redirect('/login')
        return view(*args, **kwargs)
    return wrapper


def aluno_requerido(view):
    """Rotas da área do aluno: injeta o aluno já revalidado como primeiro argumento."""
    @wraps(view)
    def wrapper(*args, **kwargs):
        aluno = aluno_autorizado()
        if aluno is None:
            return redirect('/login')
        return view(aluno, *args, **kwargs)
    return wrapper
