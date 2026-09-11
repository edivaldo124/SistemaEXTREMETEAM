"""Convite de acesso: como um cadastro criado pela administração vira uma conta.

Regra central: um aluno só assume o próprio cadastro clicando num link de uso único
enviado ao e-mail que a administração registrou. CPF, nome e data de nascimento são
dados conhecidos de terceiros e, sozinhos, nunca vinculam uma conta a um cadastro.

O token segue o mesmo desenho da recuperação de senha deste projeto: 32 bytes
aleatórios que só existem no e-mail, com apenas o SHA-256 gravado no banco, validade
curta e descarte na primeira utilização.
"""
import hashlib
import logging
import secrets
from datetime import datetime, timedelta

from sqlalchemy.exc import IntegrityError

from config import db
from modelos.usuario import Aluno
from servicos.email import email_valido, enviar_email
from servicos.urls import URLPublicaInvalida, url_publica

logger = logging.getLogger(__name__)

TOKEN_CONVITE_VALIDADE = timedelta(days=7)


class ConviteIndisponivel(RuntimeError):
    """O convite não pôde ser preparado ou entregue."""


def _hash(token):
    return hashlib.sha256(token.encode()).hexdigest()


def gerar_token(aluno):
    """Cria (ou substitui) o convite do aluno e devolve o token em claro.

    Gerar um novo convite invalida o anterior: só o último hash fica gravado.
    """
    token = secrets.token_urlsafe(32)
    aluno.token_convite_hash = _hash(token)
    aluno.token_convite_expira = datetime.utcnow() + TOKEN_CONVITE_VALIDADE
    aluno.convite_enviado_em = datetime.utcnow()
    return token


def aluno_do_token(token):
    """Aluno dono de um convite válido, ou None.

    Busca pelo resumo completo, sem carregar os demais cadastros na memória.
    """
    if not token:
        return None
    aluno = Aluno.query.filter(
        Aluno.token_convite_hash == _hash(token),
        Aluno.token_convite_expira > datetime.utcnow(),
        Aluno.email.isnot(None),
    ).first()
    if not aluno:
        return None
    # Um convite emitido antes de a conta ser ativada não pode reabrir o acesso depois.
    if aluno.acesso_ativado:
        return None
    return aluno


def descartar(aluno):
    """Queima o convite. Chamado ao ativar o acesso e ao revogar pelo painel."""
    aluno.token_convite_hash = None
    aluno.token_convite_expira = None


def enviar(aluno):
    """Gera o convite e envia o link para o e-mail JÁ GRAVADO no cadastro.

    A função não aceita um destinatário avulso de propósito: quem quiser mudar o destino
    precisa antes gravar o novo e-mail no cadastro, o que só a administração faz. Assim
    não existe caminho para o convite sair para um endereço digitado por um terceiro.
    """
    email = (aluno.email or '').strip().lower()
    if not email:
        raise ConviteIndisponivel(
            'Este aluno não tem e-mail cadastrado. Registre um e-mail antes de enviar o convite.'
        )

    if not email_valido(email):
        raise ConviteIndisponivel('Informe um e-mail válido para enviar o convite.')
    if aluno.acesso_ativado:
        raise ConviteIndisponivel('Este aluno já tem acesso ativado.')

    token = gerar_token(aluno)
    try:
        link = url_publica('auth.ativar_acesso', token=token)
    except URLPublicaInvalida:
        db.session.rollback()
        logger.error('APP_BASE_URL inválida; convite de acesso não foi gerado.')
        raise ConviteIndisponivel(
            'Não foi possível gerar o link de convite. Verifique a configuração APP_BASE_URL.'
        )

    # Valida as constraints antes de entregar um link que não poderia ser salvo.
    try:
        db.session.flush()
    except IntegrityError as exc:
        db.session.rollback()
        raise ConviteIndisponivel('Este e-mail já está em uso por outro aluno.') from exc

    # O convite só é gravado depois de entregue: um token que ninguém recebeu deixaria o
    # painel anunciando "Convite enviado" para um e-mail que nunca chegou.
    primeiro_nome = (aluno.nome or '').split()[0] if (aluno.nome or '').strip() else 'aluno'
    enviado = enviar_email(
        email, aluno.nome, 'Ative seu acesso — Extreme Team', 'Ative seu acesso',
        [
            f'Olá, {primeiro_nome}!',
            'A administração da Extreme Team criou seu cadastro de aluno e preparou um acesso à área do aluno.',
            'Clique no botão abaixo para escolher seu usuário e sua senha. O link vale por 7 dias e só pode ser usado uma vez.',
            'Se você não quiser acessar o sistema, ignore este e-mail: sua matrícula e suas mensalidades continuam normalmente.',
        ],
        link_url=link,
        link_texto='Ativar meu acesso',
    )
    if not enviado:
        db.session.rollback()
        raise ConviteIndisponivel(
            'Não foi possível enviar o e-mail de convite. Verifique a configuração de e-mail e tente de novo.'
        )

    db.session.commit()
    return email
