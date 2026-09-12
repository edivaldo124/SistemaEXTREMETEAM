"""Idempotência da fila de e-mail sob concorrência real, em PostgreSQL descartável.

SQLite não comprova isto: a unicidade que impede a cobrança duplicada é imposta pelo
banco, e é sob duas transações simultâneas que ela precisa valer. O cenário é o admin
clicando duas vezes em "enviar cobrança", ou duas abas fazendo o mesmo POST.

Cada caso cria e derruba o próprio schema aleatório. Nenhuma tabela preexistente é
usada e nenhum e-mail sai: o provedor é inteiramente simulado.
"""
import os
import uuid
from concurrent.futures import ThreadPoolExecutor

import pytest
from flask import Flask
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

from config import db
from modelos.email_pendente import EmailPendente
from servicos import fila_email


@pytest.fixture
def postgres_fila():
    url_texto = os.environ.get('TEST_POSTGRES_URL')
    if not url_texto:
        pytest.skip('Requer TEST_POSTGRES_URL para PostgreSQL de teste local.')

    url = make_url(url_texto)
    host = url.query.get('host', url.host) or ''
    if url.get_backend_name() != 'postgresql' or not (
        host in ('localhost', '127.0.0.1', '::1') or host.startswith('/tmp/')
    ):
        pytest.fail('TEST_POSTGRES_URL deve indicar explicitamente PostgreSQL local de teste.')

    schema = f'teste_fila_{uuid.uuid4().hex}'
    administracao = create_engine(url, isolation_level='AUTOCOMMIT')
    with administracao.connect() as conn:
        conn.execute(text(f'CREATE SCHEMA "{schema}"'))

    app = Flask(__name__)
    app.config.update(
        TESTING=True,
        SECRET_KEY='chave-exclusiva-do-teste-postgres',
        SQLALCHEMY_DATABASE_URI=url,
        SQLALCHEMY_ENGINE_OPTIONS={
            'connect_args': {
                'options': f'-csearch_path={schema} -clock_timeout=10000 -cstatement_timeout=15000',
                'application_name': schema,
            },
        },
    )
    db.init_app(app)
    engine = None
    try:
        with app.app_context():
            engine = db.engine
            db.create_all()
        yield app
    finally:
        with app.app_context():
            db.session.remove()
        if engine is not None:
            engine.dispose()
        with administracao.connect() as conn:
            conn.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
        administracao.dispose()


def _enfileirar_em_transacao_propria(app, chave):
    """Enfileira e comita numa sessão própria, como faria outra requisição."""
    with app.app_context():
        try:
            criado = fila_email.enfileirar(
                destinatario='aluno@example.test', nome_destinatario='Aluno',
                assunto='Mensalidade pendente', titulo='Mensalidade pendente',
                paragrafos=['Regularize sua mensalidade.'],
                chave_idempotencia=chave,
            )
            db.session.commit()
            return criado is not None
        except Exception:
            db.session.rollback()
            return False
        finally:
            db.session.remove()


def test_dois_envios_simultaneos_geram_uma_cobranca_so(postgres_fila):
    app = postgres_fila
    chave = 'cobranca:2026-09-12:42'

    with ThreadPoolExecutor(max_workers=2) as executor:
        resultados = list(executor.map(
            lambda _: _enfileirar_em_transacao_propria(app, chave), range(2),
        ))

    with app.app_context():
        linhas = EmailPendente.query.filter_by(chave_idempotencia=chave).all()

    assert len(linhas) == 1, 'A unicidade do banco deveria ter barrado a segunda linha.'
    assert sum(resultados) == 1, 'Exatamente uma das duas chamadas deve reportar criação.'


def test_chave_duplicada_nao_descarta_os_outros_destinatarios_do_lote(postgres_fila):
    """A recusa de uma chave repetida não pode desfazer o lote inteiro.

    Um `rollback()` da transação toda derrubaria todos os destinatários já enfileirados,
    e o primeiro duplicado esvaziaria o envio. Por isso o enfileiramento usa SAVEPOINT.
    """
    app = postgres_fila
    with app.app_context():
        fila_email.enfileirar(
            destinatario='ja@example.test', nome_destinatario='Já Cobrado',
            assunto='Mensalidade pendente', titulo='Mensalidade pendente',
            paragrafos=['Corpo.'], chave_idempotencia='cobranca:2026-09-12:1',
        )
        db.session.commit()

        criados = 0
        for numero in (1, 2, 3):   # o primeiro repete a chave que já existe
            if fila_email.enfileirar(
                destinatario=f'aluno{numero}@example.test', nome_destinatario=f'Aluno {numero}',
                assunto='Mensalidade pendente', titulo='Mensalidade pendente',
                paragrafos=['Corpo.'], chave_idempotencia=f'cobranca:2026-09-12:{numero}',
            ) is not None:
                criados += 1
        db.session.commit()

        assert criados == 2
        assert EmailPendente.query.count() == 3
        db.session.remove()


def test_fila_processa_cada_linha_uma_vez_so(postgres_fila, monkeypatch):
    app = postgres_fila
    entregues = []
    monkeypatch.setattr(fila_email, '_entregar', lambda item: entregues.append(item.destinatario) or True)

    with app.app_context():
        for numero in range(5):
            fila_email.enfileirar(
                destinatario=f'aluno{numero}@example.test', nome_destinatario=f'Aluno {numero}',
                assunto='Aviso', titulo='Aviso', paragrafos=['Corpo.'],
                chave_idempotencia=f'aviso:lote-x:{numero}',
            )
        db.session.commit()

        fila_email.processar_agora()
        fila_email.processar_agora()   # a segunda passada não pode reenviar nada

        assert len(entregues) == 5
        assert len(set(entregues)) == 5
        assert fila_email.contar_pendentes() == 0
        db.session.remove()


def test_dois_consumidores_nao_entregam_a_mesma_linha(postgres_fila, monkeypatch):
    """A trava do lote precisa valer até o fim do lote.

    Comitar linha a linha encerrava a transação e soltava a reserva
    `FOR UPDATE SKIP LOCKED` das linhas restantes: o segundo consumidor as reivindicava
    e entregava em paralelo. Com um worker só o problema não aparece - mas subir o
    número de workers viraria cobrança duplicada para todo inadimplente.
    """
    import threading

    app = postgres_fila
    with app.app_context():
        for numero in range(12):
            fila_email.enfileirar(
                destinatario=f'aluno{numero}@example.test', nome_destinatario=f'Aluno {numero}',
                assunto='Mensalidade pendente', titulo='Mensalidade pendente',
                paragrafos=['Corpo.'], chave_idempotencia=f'cobranca:2026-09-12:{numero}',
            )
        db.session.commit()
        db.session.remove()

    entregues = []
    trava = threading.Lock()
    pode_soltar_o_segundo = threading.Event()
    segundo_terminou = threading.Event()
    estado = {'entregas_do_primeiro': 0}

    def entregar(item):
        with trava:
            entregues.append(item.destinatario)
            meu_numero = estado['entregas_do_primeiro'] = estado['entregas_do_primeiro'] + 1

        # Pausa o primeiro consumidor DEPOIS de já ter processado uma linha. É esse o
        # momento em que a versão com commit por linha teria encerrado a transação e
        # solto a reserva das 11 linhas restantes.
        if meu_numero == 2 and not pode_soltar_o_segundo.is_set():
            pode_soltar_o_segundo.set()
            segundo_terminou.wait(timeout=10)
        return True

    monkeypatch.setattr(fila_email, '_entregar', entregar)

    def consumir(marcar_fim):
        with app.app_context():
            try:
                fila_email.processar_agora()
            finally:
                if marcar_fim:
                    segundo_terminou.set()
                db.session.remove()

    primeiro = threading.Thread(target=consumir, args=(False,))
    primeiro.start()
    assert pode_soltar_o_segundo.wait(timeout=10), 'O primeiro consumidor não avançou.'

    segundo = threading.Thread(target=consumir, args=(True,))
    segundo.start()
    segundo.join(timeout=30)
    primeiro.join(timeout=30)

    assert len(entregues) == len(set(entregues)), (
        f'Destinatário entregue mais de uma vez: {entregues}'
    )
    with app.app_context():
        assert fila_email.contar_pendentes() == 0
        db.session.remove()
