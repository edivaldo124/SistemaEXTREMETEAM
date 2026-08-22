from sqlalchemy.exc import IntegrityError

from config import db
from modelos.matricula import Matricula


class MatriculaDAO:
    @staticmethod
    def matricular(aluno_id, turma_id):
        db.session.add(Matricula(aluno_id=aluno_id, turma_id=turma_id))
        try:
            db.session.commit()
            return True
        except IntegrityError:
            db.session.rollback()
            return False

    @staticmethod
    def desmatricular(aluno_id, turma_id):
        matricula = Matricula.query.filter_by(aluno_id=aluno_id, turma_id=turma_id).first()
        if not matricula:
            return False
        db.session.delete(matricula)
        db.session.commit()
        return True

    @staticmethod
    def contar_por_turma(turma_id):
        return Matricula.query.filter_by(turma_id=turma_id).count()

    @staticmethod
    def listar_por_turma(turma_id):
        return Matricula.query.filter_by(turma_id=turma_id).all()

    @staticmethod
    def listar_por_aluno(aluno_id):
        return Matricula.query.filter_by(aluno_id=aluno_id).all()
