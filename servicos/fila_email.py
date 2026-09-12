"""Processamento dos e-mails coletivos fora da requisição.

O que muda em relação ao envio direto:

* **Durabilidade.** Cada destinatário vira uma linha em `emails_pendentes` dentro da
  transação da requisição. Se o processo cair, for reiniciado ou for redeployado no
  meio do envio, a fila continua no banco e é retomada - uma thread solta perderia
  tudo o que ainda estava na lista.
* **Resposta imediata.** A requisição enfileira e responde. Antes ela segurava um
  timeout de 10s por destinatário, somados em série.
* **Sem enfileiramento duplicado.** `chave_idempotencia` é única no banco. Clicar duas
  vezes em "enviar cobrança", ou duas abas fazendo o mesmo POST, produzem uma linha só.

  Isso NÃO é o mesmo que entrega exatamente uma vez, e a diferença importa: a garantia
  aqui é *pelo menos uma vez*. `processar_agora` entrega o lote e só então grava o
  resultado; se o processo cair depois de o provedor aceitar uma mensagem e antes do
  commit, a linha volta como pendente e será entregue de novo. Entrega exatamente uma
  vez dependeria de uma chave de idempotência aceita pelo próprio provedor, que a API
  usada aqui não oferece. O que a fila promete é: nada se perde, e o mesmo pedido não
  vira dois envios enfileirados.
* **Resultado observável.** `status`, `tentativas` e `ultimo_erro` ficam na linha, e o
  painel de avisos mostra o que ainda está na fila e o que falhou.

O consumidor é uma thread de fundo do próprio processo (um worker Gunicorn, uma
aplicação de academia). Ela é o transporte, não a garantia: a garantia é a linha no
banco, que sobrevive a ela.
"""
import logging
import os
import threading
from datetime import datetime, timedelta

from sqlalchemy.exc import IntegrityError

from config import db
from modelos.email_pendente import (
    MAX_TENTATIVAS,
    STATUS_DESISTIU,
    STATUS_ENVIADO,
    STATUS_PENDENTE,
    EmailPendente,
    espera_da_proxima_tentativa,
)
from servicos.email import enviar_email

logger = logging.getLogger(__name__)

# Quantas linhas cada passada processa. Mantém a thread previsível e deixa espaço para
# os e-mails transacionais (que continuam saindo na hora) disputarem a mesma saída.
LOTE = 20

_disparador = threading.Lock()
_thread = None
_app = None
# Alguém pediu processamento enquanto o laço já estava rodando? Sem esta marca, um
# `disparar()` que acontece no instante em que o laço está saindo se perderia, e as
# linhas recém-gravadas ficariam sem consumidor até o próximo clique.
_novo_trabalho = False


def registrar_app(app):
    """Guarda a aplicação para a thread de fundo abrir contexto próprio."""
    global _app
    _app = app


def enfileirar(*, destinatario, nome_destinatario, assunto, titulo, paragrafos,
               chave_idempotencia, link_url=None, link_texto=None):
    """Registra um e-mail para envio. Devolve a linha criada, ou None se já existia.

    Não faz commit: quem chama decide o momento, para o enfileiramento de uma lista
    inteira ser uma transação só.
    """
    if not destinatario:
        return None

    item = EmailPendente(
        destinatario=destinatario,
        nome_destinatario=nome_destinatario,
        assunto=assunto,
        titulo=titulo,
        corpo='\n'.join(paragrafos or []),
        link_url=link_url,
        link_texto=link_texto,
        chave_idempotencia=chave_idempotencia,
        status=STATUS_PENDENTE,
        tentativas=0,
    )
    # SAVEPOINT: uma chave repetida desfaz SÓ esta linha. Um `rollback()` na transação
    # inteira descartaria todos os destinatários já enfileirados no mesmo lote - o
    # primeiro duplicado esvaziaria o envio.
    try:
        with db.session.begin_nested():
            db.session.add(item)
            db.session.flush()
    except IntegrityError:
        # Já existe uma linha com esta chave. Se ela DESISTIU, o e-mail nunca chegou:
        # recusar o reenvio aqui faria a tela dizer "já recebeu" sobre algo que não foi
        # entregue. A linha volta à fila, zerada. Se estiver pendente ou enviada, aí sim
        # a repetição é o clique duplo que a unicidade existe para absorver.
        existente = EmailPendente.query.filter_by(
            chave_idempotencia=chave_idempotencia,
        ).first()
        if existente is not None and existente.status == STATUS_DESISTIU:
            existente.status = STATUS_PENDENTE
            existente.tentativas = 0
            existente.ultimo_erro = None
            existente.processado_em = None
            existente.proxima_tentativa = datetime.utcnow()
            return existente
        return None
    return item


def contar_pendentes():
    """Tudo o que ainda vai sair, inclusive o que está aguardando o adiamento."""
    return EmailPendente.query.filter_by(status=STATUS_PENDENTE).count()


def contar_falhados():
    return EmailPendente.query.filter_by(status=STATUS_DESISTIU).count()


def listar_pendentes(limite=LOTE, *, travar=False, agora=None):
    """Próximas linhas a processar, já liberadas pelo adiamento.

    `travar` reserva as linhas para este processo (`FOR UPDATE SKIP LOCKED`), de modo que
    dois consumidores simultâneos peguem lotes diferentes em vez do mesmo. A unicidade de
    `chave_idempotencia` protege o ENFILEIRAMENTO; ela não impediria dois processos de
    ENTREGAREM a mesma linha, e é isso que a trava cobre.

    Hoje o compose roda um worker só, então a disputa não acontece - mas subir o número
    de workers não pode virar, em silêncio, cobrança duplicada para todo inadimplente.
    O SQLite ignora a cláusula; quem a exercita é o teste em PostgreSQL.
    """
    agora = agora or datetime.utcnow()
    consulta = (
        EmailPendente.query
        .filter(
            EmailPendente.status == STATUS_PENDENTE,
            EmailPendente.proxima_tentativa <= agora,
        )
        # Ordenar pelo adiamento (e não só pelo id) é o que tira uma linha problemática
        # da frente das outras: quem falhou vai para o futuro e os demais passam.
        .order_by(EmailPendente.proxima_tentativa.asc(), EmailPendente.id.asc())
        .limit(limite)
    )
    if travar:
        consulta = consulta.with_for_update(skip_locked=True)
    return consulta.all()


def _entregar(item):
    """Chamada real ao provedor. Isolada para os testes substituírem só isto."""
    return enviar_email(
        item.destinatario, item.nome_destinatario, item.assunto, item.titulo,
        item.paragrafos, link_url=item.link_url, link_texto=item.link_texto,
    )


def processar_agora(limite=LOTE, *, agora=None):
    """Drena até `limite` e-mails pendentes. Devolve (enviados, falhados).

    Uma falha não derruba a passada nem perde a linha: ela volta para `pendente` com a
    tentativa contada, e só vira `desistiu` depois de MAX_TENTATIVAS.
    """
    enviados = falhados = 0
    try:
        # UM commit para o lote inteiro, no fim. Comitar linha a linha encerrava a
        # transação e, com ela, a reserva `FOR UPDATE SKIP LOCKED` das linhas ainda não
        # processadas: outro worker podia reivindicá-las e entregá-las em paralelo,
        # justamente a duplicação que a trava existe para impedir.
        for item in listar_pendentes(limite, travar=True, agora=agora):
            item.tentativas += 1
            try:
                sucesso = _entregar(item)
                erro = None if sucesso else 'O provedor recusou ou não confirmou o envio.'
            except Exception as excecao:  # nunca deixa a thread morrer por um destinatário
                sucesso = False
                erro = f'{type(excecao).__name__}: {excecao}'[:255]
                logger.exception('Falha ao enviar o e-mail %s da fila.', item.id)

            if sucesso:
                item.status = STATUS_ENVIADO
                item.processado_em = datetime.utcnow()
                item.ultimo_erro = None
                enviados += 1
            else:
                item.ultimo_erro = (erro or 'Erro desconhecido.')[:255]
                if item.tentativas >= MAX_TENTATIVAS:
                    item.status = STATUS_DESISTIU
                    item.processado_em = datetime.utcnow()
                else:
                    # Adia a próxima tentativa. Sem isto, uma indisponibilidade de um
                    # minuto gastava as 5 tentativas em segundos.
                    item.proxima_tentativa = datetime.utcnow() + timedelta(
                        minutes=espera_da_proxima_tentativa(item.tentativas),
                    )
                falhados += 1
        db.session.commit()
    except Exception:
        # O lote volta a `pendente` e é retomado depois. Entrega é "pelo menos uma vez":
        # cair depois de o provedor aceitar pode reenviar, o que é preferível a sumir.
        db.session.rollback()
        logger.exception('Lote da fila de e-mail não pôde ser gravado; segue pendente.')
        raise

    return enviados, falhados


def _laco():
    """Drena a fila enquanto houver entrega acontecendo.

    Encerra na primeira passada sem nenhum envio bem-sucedido, em vez de repetir sem
    pausa sobre as mesmas linhas com defeito. Quem reabre a fila depois é a próxima
    chamada a `disparar()` - o próximo envio ou simplesmente abrir a tela de avisos - e
    as linhas que falharam só voltam a ser elegíveis quando o adiamento delas vence.
    """
    global _thread, _novo_trabalho
    try:
        with _app.app_context():
            while True:
                with _disparador:
                    # Consome a marca ANTES de processar: o que for enfileirado daqui
                    # em diante marca de novo e garante mais uma passada.
                    _novo_trabalho = False
                enviados, _falhados = processar_agora()
                if enviados:
                    continue
                # Nada saiu nesta passada. Só encerra se ninguém pediu trabalho no
                # meio-tempo - a checagem é feita sob a mesma trava que `disparar()`
                # usa, senão um pedido que chega agora se perderia.
                with _disparador:
                    if not _novo_trabalho:
                        _thread = None
                        return
    except Exception:
        logger.exception('Laço da fila de e-mail encerrou com erro; a fila segue no banco.')
        _liberar_e_retomar_se_preciso()


def _liberar_e_retomar_se_preciso():
    """Desregistra a thread e sobe outra se alguém pediu trabalho durante a queda.

    Sem isso, um `disparar()` que chegou enquanto esta thread já estava morrendo via
    `_thread` ainda registrado, só marcava o pedido e ia embora - e o lote recém-gravado
    ficava sem consumidor até alguém reabrir a tela de avisos.
    """
    global _thread, _novo_trabalho
    with _disparador:
        _thread = None
        if not _novo_trabalho:
            return
        _novo_trabalho = False
        _thread = threading.Thread(target=_laco, name='fila-email', daemon=True)
        _thread.start()


def disparar():
    """Acorda o processamento em segundo plano, sem bloquear a requisição.

    Se a thread não subir (ou morrer), nada se perde: as linhas continuam pendentes e a
    próxima chamada - a próxima abertura do painel de avisos, por exemplo - retoma.
    """
    global _thread, _novo_trabalho
    if _app is None or os.environ.get('FILA_EMAIL_SINCRONA', '').lower() == 'true':
        return
    with _disparador:
        _novo_trabalho = True
        if _thread is not None:
            # O laço está de pé: registra o pedido em vez de abrir outra thread. Ele
            # confere esta marca antes de encerrar, então nada fica sem consumidor.
            return
        _novo_trabalho = False
        _thread = threading.Thread(target=_laco, name='fila-email', daemon=True)
        _thread.start()
