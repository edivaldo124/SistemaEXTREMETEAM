from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import func

from config import db
from modelos.matricula import Matricula
from modelos.pagamento import Pagamento
from modelos.pagamento_evento import PagamentoEvento
from modelos.usuario import Aluno

# Estados "fechados": não geram mais cobrança Pix nova nem esperam decisão de ninguém.
STATUS_FECHADOS = ('pago', 'cancelado', 'reembolsado')

# Estados "em aberto": ainda pedem alguma ação (do aluno ou de uma decisão pendente).
STATUS_ABERTOS = ('pendente', 'atrasado', 'em_processamento', 'em_analise', 'recusado')

# Rótulo humano de cada status interno - usado nos badges (nunca só a cor comunica o estado).
ROTULO_STATUS = {
    'pendente': 'Pendente',
    'atrasado': 'Vencida',
    'em_processamento': 'Processando',
    'em_analise': 'Em análise',
    'pago': 'Paga',
    'recusado': 'Recusada',
    'reembolsado': 'Reembolsada',
    'cancelado': 'Cancelada',
}

# Texto do botão principal do card "Minha mensalidade" para cada status.
ROTULO_ACAO_STATUS = {
    'pendente': 'Pagar agora',
    'atrasado': 'Regularizar',
    'em_processamento': 'Ver situação',
    'em_analise': 'Ver situação',
    'pago': 'Ver comprovante',
    'recusado': 'Tentar novamente',
    'reembolsado': 'Ver detalhes',
    'cancelado': 'Ver detalhes',
}


def rotulo_status(status):
    return ROTULO_STATUS.get(status, (status or '').capitalize())


def rotulo_acao(status):
    return ROTULO_ACAO_STATUS.get(status, 'Ver detalhes')


def mensalidade_destaque(pagamentos):
    """Escolhe a mensalidade mais relevante para o card 'Minha mensalidade':
    a mais próxima de vencer entre as em aberto ou, se não houver nenhuma em
    aberto, a mais recente já encerrada (paga/reembolsada/cancelada)."""
    abertos = [p for p in pagamentos if p.status in STATUS_ABERTOS]
    if abertos:
        return sorted(abertos, key=lambda p: p.vencimento)[0]

    fechados = [p for p in pagamentos if p.status not in STATUS_ABERTOS]
    if fechados:
        return sorted(fechados, key=lambda p: p.vencimento, reverse=True)[0]

    return None


class PagamentoDAO:
    @staticmethod
    def criar_ou_obter_mensalidade_plano(*, aluno, plano, hoje=None):
        """Cria a cobrança da contratação ou reutiliza a equivalente em aberto.

        O preço sempre vem do plano persistido. A competência torna o POST
        idempotente em reenvios e evita duas cobranças abertas do mesmo plano no mês.
        """
        hoje = hoje or date.today()
        competencia = hoje.strftime('%Y-%m')
        existente = Pagamento.query.filter(
            Pagamento.aluno_id == aluno.id,
            Pagamento.plano_id == plano.id,
            Pagamento.competencia == competencia,
            Pagamento.status.in_(STATUS_ABERTOS),
        ).order_by(Pagamento.id.desc()).first()

        if existente:
            if aluno.plano_id != plano.id:
                aluno.plano_id = plano.id
                db.session.commit()
            return existente, False

        pagamento = Pagamento(
            aluno_id=aluno.id,
            plano_id=plano.id,
            valor=Decimal(str(plano.preco_plano)),
            vencimento=hoje,
            status='pendente',
            competencia=competencia,
        )
        aluno.plano_id = plano.id
        aluno.mensalidade = 'Pendente'
        db.session.add(pagamento)
        db.session.flush()
        db.session.add(PagamentoEvento(
            pagamento_id=pagamento.id,
            tipo='plano_contratado',
            detalhe=f'Cobrança criada para contratação do plano {plano.nome_plano}.',
            ator=aluno.login,
        ))
        db.session.commit()
        return pagamento, True

    @staticmethod
    def salvar(pagamento):
        db.session.add(pagamento)
        db.session.commit()

    @staticmethod
    def listar_por_aluno(aluno_id):
        pagamentos = Pagamento.query.filter_by(aluno_id=aluno_id).order_by(Pagamento.vencimento.desc()).all()

        for p in pagamentos:
            if p.status == 'pendente' and p.vencimento < date.today():
                p.status = 'atrasado'

        db.session.commit()
        return pagamentos

    @staticmethod
    def buscar_por_id(pagamento_id):
        return Pagamento.query.filter_by(id=pagamento_id).first()

    @staticmethod
    def atualizar_status(pagamento_id, status, forma_pagamento):
        pagamento = Pagamento.query.filter_by(id=pagamento_id).first()

        if pagamento:
            pagamento.status = status
            pagamento.forma_pagamento = forma_pagamento

            if status == 'pago':
                pagamento.data_pagamento = date.today()
            else:
                pagamento.data_pagamento = None

            db.session.commit()
            return True

        return False

    @staticmethod
    def buscar_por_provider_payment_id(provider_payment_id):
        return Pagamento.query.filter_by(provider_payment_id=provider_payment_id).first()

    @staticmethod
    def buscar_por_external_reference(external_reference):
        return Pagamento.query.filter_by(external_reference=external_reference).first()

    @staticmethod
    def pix_ainda_valido(pagamento):
        """True se a cobrança Pix já gerada para este pagamento ainda pode ser
        reaproveitada (mesma idempotency_key), em vez de criar uma nova."""
        if not pagamento.provider_payment_id or pagamento.status in STATUS_FECHADOS:
            return False
        if pagamento.data_expiracao and pagamento.data_expiracao <= datetime.utcnow():
            return False
        return True

    @staticmethod
    def registrar_evento(pagamento_id, tipo, detalhe=None, ator=None):
        db.session.add(PagamentoEvento(pagamento_id=pagamento_id, tipo=tipo, detalhe=detalhe, ator=ator))
        db.session.commit()

    @staticmethod
    def salvar_dados_pix(pagamento, *, provider_payment_id, external_reference, idempotency_key,
                          pix_copia_cola, ticket_url, data_expiracao):
        pagamento.provider = 'mercado_pago'
        pagamento.provider_payment_id = provider_payment_id
        pagamento.external_reference = external_reference
        pagamento.idempotency_key = idempotency_key
        pagamento.pix_copia_cola = pix_copia_cola
        pagamento.ticket_url = ticket_url
        pagamento.data_criacao_pix = datetime.utcnow()
        pagamento.data_expiracao = data_expiracao
        db.session.add(PagamentoEvento(
            pagamento_id=pagamento.id, tipo='pix_gerado',
            detalhe=f'Cobrança Pix criada (id provedor {provider_payment_id}).', ator='sistema',
        ))
        db.session.commit()

    @staticmethod
    def marcar_pago_via_webhook(pagamento, *, data_pagamento):
        pagamento.status = 'pago'
        pagamento.data_pagamento = data_pagamento
        pagamento.forma_pagamento = 'pix'
        pagamento.provider_status = 'approved'
        if pagamento.aluno:
            pagamento.aluno.mensalidade = 'Em Dia'
        db.session.add(PagamentoEvento(
            pagamento_id=pagamento.id, tipo='webhook_aprovado',
            detalhe='Pagamento aprovado e confirmado pelo Mercado Pago.', ator='webhook_mercado_pago',
        ))
        db.session.commit()

    @staticmethod
    def marcar_reembolsado_via_webhook(pagamento):
        pagamento.status = 'reembolsado'
        pagamento.provider_status = 'refunded'
        if pagamento.aluno:
            pagamento.aluno.mensalidade = 'Pendente'
        db.session.add(PagamentoEvento(
            pagamento_id=pagamento.id, tipo='webhook_reembolso',
            detalhe='Pagamento reembolsado/estornado conforme notificação do Mercado Pago.',
            ator='webhook_mercado_pago',
        ))
        db.session.commit()

    @staticmethod
    def marcar_em_processamento_via_webhook(pagamento):
        if pagamento.status in STATUS_FECHADOS:
            return
        pagamento.status = 'em_processamento'
        pagamento.provider_status = 'in_process'
        db.session.add(PagamentoEvento(
            pagamento_id=pagamento.id, tipo='webhook_em_processamento',
            detalhe='Mercado Pago está analisando o pagamento.', ator='webhook_mercado_pago',
        ))
        db.session.commit()

    @staticmethod
    def marcar_recusado_via_webhook(pagamento, *, status_detail=None):
        if pagamento.status in STATUS_FECHADOS:
            return
        pagamento.status = 'recusado'
        pagamento.provider_status = 'rejected'
        pagamento.provider_status_detail = (status_detail or '')[:60] or None
        db.session.add(PagamentoEvento(
            pagamento_id=pagamento.id, tipo='webhook_recusado',
            detalhe='Pagamento recusado pelo Mercado Pago.', ator='webhook_mercado_pago',
        ))
        db.session.commit()

    # ---------------- Comprovante manual (dinheiro/transferência) ----------------

    @staticmethod
    def enviar_comprovante_manual(pagamento, *, arquivo_nome, ator):
        pagamento.comprovante_manual_arquivo = arquivo_nome
        pagamento.comprovante_manual_enviado_em = datetime.utcnow()
        pagamento.comprovante_manual_analisado_por = None
        pagamento.comprovante_manual_analisado_em = None
        pagamento.comprovante_manual_observacao = None
        pagamento.status = 'em_analise'
        db.session.add(PagamentoEvento(
            pagamento_id=pagamento.id, tipo='comprovante_enviado',
            detalhe='Aluno enviou comprovante manual para análise.', ator=ator,
        ))
        db.session.commit()

    @staticmethod
    def aprovar_comprovante_manual(pagamento, *, admin_login, observacao=None, data_pagamento=None,
                                    forma_pagamento='transferencia'):
        pagamento.status = 'pago'
        pagamento.data_pagamento = data_pagamento or date.today()
        pagamento.forma_pagamento = forma_pagamento
        pagamento.comprovante_manual_analisado_por = admin_login
        pagamento.comprovante_manual_analisado_em = datetime.utcnow()
        pagamento.comprovante_manual_observacao = observacao
        if pagamento.aluno:
            pagamento.aluno.mensalidade = 'Em Dia'
        db.session.add(PagamentoEvento(
            pagamento_id=pagamento.id, tipo='comprovante_aprovado',
            detalhe=observacao or 'Comprovante manual aprovado pela administração.', ator=admin_login,
        ))
        db.session.commit()

    @staticmethod
    def rejeitar_comprovante_manual(pagamento, *, admin_login, observacao=None):
        pagamento.status = 'atrasado' if pagamento.vencimento < date.today() else 'pendente'
        pagamento.comprovante_manual_analisado_por = admin_login
        pagamento.comprovante_manual_analisado_em = datetime.utcnow()
        pagamento.comprovante_manual_observacao = observacao
        db.session.add(PagamentoEvento(
            pagamento_id=pagamento.id, tipo='comprovante_rejeitado',
            detalhe=observacao or 'Comprovante manual rejeitado pela administração.', ator=admin_login,
        ))
        db.session.commit()

    @staticmethod
    def registrar_pagamento_manual(*, aluno_id, plano_id, valor, vencimento, competencia=None,
                                    data_pagamento=None, forma_pagamento='dinheiro', observacao=None, ator):
        """Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.
        Sempre nasce com provider='manual' e já fica 'pago' (o admin está confirmando
        um recebimento que já aconteceu, ao contrário do comprovante enviado pelo aluno,
        que fica 'em_analise' até ser revisado)."""
        pagamento = Pagamento(
            aluno_id=aluno_id, plano_id=plano_id, valor=valor, vencimento=vencimento,
            status='pago', data_pagamento=data_pagamento or date.today(),
            forma_pagamento=forma_pagamento, provider='manual', competencia=competencia,
        )
        db.session.add(pagamento)
        db.session.flush()
        db.session.add(PagamentoEvento(
            pagamento_id=pagamento.id, tipo='manual_registrado',
            detalhe=observacao or f'Recebimento manual registrado ({forma_pagamento}).', ator=ator,
        ))
        db.session.commit()
        return pagamento

    # ---------------- Painel financeiro (admin) ----------------

    @staticmethod
    def _query_filtrada(*, inicio=None, fim=None, turma_id=None, plano_id=None, forma_pagamento=None,
                         status=None, busca_aluno=None):
        consulta = Pagamento.query.join(Aluno, Pagamento.aluno_id == Aluno.id)

        if inicio:
            consulta = consulta.filter(Pagamento.vencimento >= inicio)
        if fim:
            consulta = consulta.filter(Pagamento.vencimento <= fim)
        if turma_id:
            ids_alunos = [m.aluno_id for m in Matricula.query.filter_by(turma_id=turma_id).all()]
            consulta = consulta.filter(Pagamento.aluno_id.in_(ids_alunos or [-1]))
        if plano_id:
            consulta = consulta.filter(Pagamento.plano_id == plano_id)
        if forma_pagamento:
            consulta = consulta.filter(Pagamento.forma_pagamento == forma_pagamento)
        if status:
            consulta = consulta.filter(Pagamento.status == status)
        if busca_aluno:
            consulta = consulta.filter(Aluno.nome.ilike(f'%{busca_aluno}%'))

        return consulta

    @staticmethod
    def listar_filtrado(**filtros):
        # Reaproveita a mesma promoção pendente->atrasado usada na área do aluno.
        pendentes_vencidos = Pagamento.query.filter(Pagamento.status == 'pendente', Pagamento.vencimento < date.today()).all()
        for p in pendentes_vencidos:
            p.status = 'atrasado'
        if pendentes_vencidos:
            db.session.commit()

        return PagamentoDAO._query_filtrada(**filtros).order_by(Pagamento.vencimento.desc()).all()

    @staticmethod
    def totais_periodo(*, inicio=None, fim=None):
        """Totais do painel financeiro - sempre calculados no backend a partir do banco,
        nunca somados no front. `inicio`/`fim` filtram pelo vencimento da mensalidade."""
        base = PagamentoDAO._query_filtrada(inicio=inicio, fim=fim)

        def soma(status_lista):
            valor = base.filter(Pagamento.status.in_(status_lista)).with_entities(func.coalesce(func.sum(Pagamento.valor), 0)).scalar()
            return Decimal(valor or 0)

        def conta(status_lista):
            return base.filter(Pagamento.status.in_(status_lista)).count()

        alunos_inadimplentes = (
            base.filter(Pagamento.status == 'atrasado')
            .with_entities(Pagamento.aluno_id).distinct().count()
        )

        return {
            'total_recebido': soma(['pago']),
            'total_pendente': soma(['pendente']),
            'total_vencido': soma(['atrasado']),
            'total_em_analise': soma(['em_analise']),
            'qtd_pago': conta(['pago']),
            'qtd_pendente': conta(['pendente']),
            'qtd_vencido': conta(['atrasado']),
            'qtd_em_analise': conta(['em_analise']),
            'alunos_inadimplentes': alunos_inadimplentes,
        }
