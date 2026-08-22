from sqlalchemy.exc import SQLAlchemyError

from config import db
from modelos.turma import Turma


class TurmaDAO:
    @staticmethod
    def salvar(turma):
        db.session.add(turma)
        db.session.commit()

    @staticmethod
    def listar_todas():
        return Turma.query.all()

    @staticmethod
    def buscar_por_id(turma_id):
        return db.session.get(Turma, turma_id)

    @staticmethod
    def remover(turma_id):
        turma = db.session.get(Turma, turma_id)
        if not turma:
            return None

        try:
            db.session.delete(turma)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False
