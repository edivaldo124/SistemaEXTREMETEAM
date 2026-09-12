"""Fila de e-mails no banco.

Aviso e cobrança coletivos saíam um a um dentro da requisição, com timeout de 10s por
destinatário: 60 alunos podiam segurar a resposta por minutos e estourar o timeout do
Gunicorn, e um deploy no meio do laço perdia silenciosamente o resto da lista.

A linha aqui é o registro durável do envio. Ela existe ANTES de qualquer chamada ao
provedor e só sai da fila depois de uma entrega confirmada, então um restart no meio do
processamento retoma de onde parou em vez de recomeçar ou desistir.
"""
from datetime import datetime

from config import db

STATUS_PENDENTE = 'pendente'
STATUS_ENVIADO = 'enviado'
STATUS_DESISTIU = 'desistiu'

# Depois disso a linha para de ser tentada e fica visível para a administração decidir.
MAX_TENTATIVAS = 5

# Espera antes de cada nova tentativa, em minutos, indexada pela tentativa já feita.
ESPERA_POR_TENTATIVA_MINUTOS = (1, 2, 4, 8, 15)


def espera_da_proxima_tentativa(tentativas):
    indice = min(max(tentativas, 1), len(ESPERA_POR_TENTATIVA_MINUTOS)) - 1
    return ESPERA_POR_TENTATIVA_MINUTOS[indice]


class EmailPendente(db.Model):
    __tablename__ = 'emails_pendentes'

    id = db.Column(db.Integer, primary_key=True)

    destinatario = db.Column(db.String(150), nullable=False)
    nome_destinatario = db.Column(db.String(150), nullable=True)
    assunto = db.Column(db.String(200), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    # Parágrafos do corpo, separados por quebra de linha. Texto, nunca HTML montado:
    # o HTML continua sendo renderizado pelo template no momento do envio.
    corpo = db.Column(db.Text, nullable=False)
    link_url = db.Column(db.String(512), nullable=True)
    link_texto = db.Column(db.String(120), nullable=True)

    # Identidade do envio. É o que impede a mesma cobrança de sair duas vezes quando o
    # admin clica de novo ou recarrega a página: a unicidade é garantida pelo banco,
    # não por uma checagem em Python que duas requisições simultâneas veriam igual.
    chave_idempotencia = db.Column(db.String(120), nullable=False, unique=True, index=True)

    status = db.Column(db.String(20), nullable=False, default=STATUS_PENDENTE, index=True)
    tentativas = db.Column(db.Integer, nullable=False, default=0)
    ultimo_erro = db.Column(db.String(255), nullable=True)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    processado_em = db.Column(db.DateTime, nullable=True)

    # Momento a partir do qual esta linha pode ser tentada de novo.
    #
    # Sem isso, uma linha que falha volta imediatamente ao topo da fila: as 5 tentativas
    # eram gastas em segundos por uma indisponibilidade de um minuto, e enquanto ela
    # ocupava a cabeça da fila os destinatários seguintes nunca chegavam a ser tentados.
    # O adiamento cresce a cada falha (1, 2, 4, 8... minutos) e é por ele que a fila é
    # ordenada, então uma linha problemática sai da frente das outras.
    proxima_tentativa = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, index=True,
    )

    @property
    def paragrafos(self):
        return [linha for linha in (self.corpo or '').split('\n') if linha.strip()]
