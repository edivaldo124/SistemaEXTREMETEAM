from datetime import datetime

from sqlalchemy import select, union
from sqlalchemy.exc import SQLAlchemyError

from config import db
from modelos.pagamento import Pagamento
from modelos.plano import Plano
from modelos.solicitacao_plano import STATUS_CANCELADA, STATUS_PENDENTE, SolicitacaoMudancaPlano
from modelos.usuario import Aluno

class PlanoDAO:
    @staticmethod
    def salvar(plano):
        db.session.add(plano)
        db.session.commit()

    @staticmethod
    def listar_todos():
        """Inclusive os arquivados: serve a quem olha o histórico (filtro do financeiro)."""
        return Plano.query.order_by(Plano.arquivado, Plano.id).all()

    @staticmethod
    def listar_ativos():
        """Os planos à venda: home, perfil do aluno e formulários de contratação."""
        return Plano.query.filter(Plano.arquivado.is_(False)).order_by(Plano.id).all()

    @staticmethod
    def listar_arquivados():
        return Plano.query.filter(Plano.arquivado.is_(True)).order_by(Plano.nome_plano).all()

    @staticmethod
    def buscar_por_id(id_plano):
        return Plano.query.filter_by(id=id_plano).first()

    @staticmethod
    def buscar_ativo_por_id(id_plano):
        return Plano.query.filter_by(id=id_plano, arquivado=False).first()

    @staticmethod
    def ids_em_uso():
        """Planos que algum registro referencia: mensalidade, cadastro de aluno ou pedido
        de troca. Esses só podem ser arquivados - apagar levaria o histórico junto."""
        consulta = union(
            select(Pagamento.plano_id),
            select(Aluno.plano_id).where(Aluno.plano_id.is_not(None)),
            select(SolicitacaoMudancaPlano.plano_origem_id).where(
                SolicitacaoMudancaPlano.plano_origem_id.is_not(None)),
            select(SolicitacaoMudancaPlano.plano_destino_id),
        )
        return set(db.session.execute(consulta).scalars())

    @staticmethod
    def em_uso(id_plano):
        return id_plano in PlanoDAO.ids_em_uso()

    @staticmethod
    def atualizar(id_plano, *, nome, preco, duracao, preco_promocional=None,
                  promocao_inicio=None, promocao_fim=None):
        """Grava a edição do admin. Vale para as cobranças criadas daqui em diante: as
        mensalidades já lançadas guardam o próprio valor."""
        plano = PlanoDAO.buscar_por_id(id_plano)
        if not plano:
            return None
        plano.nome_plano = nome
        plano.preco_plano = preco
        plano.duracao_dias = duracao
        plano.preco_promocional = preco_promocional
        plano.promocao_inicio = promocao_inicio
        plano.promocao_fim = promocao_fim
        db.session.commit()
        return plano

    @staticmethod
    def arquivar(id_plano, *, ator):
        """Tira o plano de venda. Devolve `(plano, pedidos_cancelados)`, ou None.

        Pedidos de troca PARA este plano são cancelados: a troca só se concretiza numa
        cobrança nova, e plano arquivado não recebe cobrança nova - o aluno ficaria preso
        a um agendamento impossível. Quem está NO plano não é tocado: termina o período
        pago e escolhe outro na renovação.
        """
        plano = PlanoDAO.buscar_por_id(id_plano)
        if not plano:
            return None
        plano.arquivado = True
        plano.destaque = False
        pedidos = SolicitacaoMudancaPlano.query.filter_by(
            plano_destino_id=plano.id, status=STATUS_PENDENTE,
        ).all()
        for pedido in pedidos:
            pedido.status = STATUS_CANCELADA
            pedido.cancelado_em = datetime.utcnow()
            pedido.cancelado_por = ator
            pedido.observacao = f'O plano {plano.nome_plano} foi arquivado pela administração.'[:255]
        db.session.commit()
        return plano, len(pedidos)

    @staticmethod
    def reativar(id_plano):
        plano = PlanoDAO.buscar_por_id(id_plano)
        if not plano:
            return None
        plano.arquivado = False
        db.session.commit()
        return plano

    @staticmethod
    def remover(id_plano):
        """Apaga um plano que nunca foi usado. True, None (não existe) ou False (em uso)."""
        plano = Plano.query.filter_by(id=id_plano).first()
        if not plano:
            return None
        if PlanoDAO.em_uso(plano.id):
            return False

        try:
            db.session.delete(plano)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

    @staticmethod
    def definir_destaque(id_plano, destacar=True):
        """Marca o plano em destaque da página inicial, desmarcando qualquer outro.

        `destacar=False` só tira a marcação desse plano (a home volta à regra padrão).
        Devolve o plano, ou None se ele não existe (ou está arquivado, ao destacar).
        """
        plano = Plano.query.filter_by(id=id_plano).first()
        if not plano or (destacar and plano.arquivado):
            return None
        if destacar:
            Plano.query.filter(Plano.id != plano.id, Plano.destaque.is_(True)).update(
                {Plano.destaque: False}, synchronize_session=False,
            )
        plano.destaque = bool(destacar)
        db.session.commit()
        return plano
