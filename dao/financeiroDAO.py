from datetime import date, datetime

from config import db
from modelos.pagamento import Pagamento

STATUS_FECHADOS = ('pago', 'cancelado', 'reembolsado')


class PagamentoDAO:
    @staticmethod
    def salvar(pagamento):
        db.session.add(pagamento)
        db.session.commit()

    @staticmethod
    def listar_por_aluno(aluno_id):
        pagamentos = Pagamento.query.filter_by(aluno_id=aluno_id).all()

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
        db.session.commit()

    @staticmethod
    def marcar_pago_via_webhook(pagamento, *, data_pagamento):
        pagamento.status = 'pago'
        pagamento.data_pagamento = data_pagamento
        pagamento.forma_pagamento = 'pix'
        if pagamento.aluno:
            pagamento.aluno.mensalidade = 'Em Dia'
        db.session.commit()

    @staticmethod
    def marcar_reembolsado_via_webhook(pagamento):
        pagamento.status = 'reembolsado'
        if pagamento.aluno:
            pagamento.aluno.mensalidade = 'Pendente'
        db.session.commit()
