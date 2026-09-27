from sqlalchemy.exc import SQLAlchemyError

from config import db
from modelos.plano import Plano

class PlanoDAO:
    @staticmethod
    def salvar(plano):
        db.session.add(plano)
        db.session.commit()

    @staticmethod
    def listar_todos():
        return Plano.query.all()

    @staticmethod
    def buscar_por_id(id_plano):
        return Plano.query.filter_by(id=id_plano).first()

    @staticmethod
    def remover(id_plano):
        plano = Plano.query.filter_by(id=id_plano).first()
        if not plano:
            return None

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
        Devolve o plano, ou None se ele não existe.
        """
        plano = Plano.query.filter_by(id=id_plano).first()
        if not plano:
            return None
        if destacar:
            Plano.query.filter(Plano.id != plano.id, Plano.destaque.is_(True)).update(
                {Plano.destaque: False}, synchronize_session=False,
            )
        plano.destaque = bool(destacar)
        db.session.commit()
        return plano

