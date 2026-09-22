from sqlalchemy.exc import IntegrityError

from config import db
from modelos.matricula import Matricula
from modelos.turma import Turma


class MatriculaDAO:
    @staticmethod
    def matricular(aluno_id, turma_id):
        try:
            if not MatriculaDAO.matricular_com_lotacao(aluno_id, turma_id, commit=False):
                db.session.rollback()
                return False
            db.session.commit()
            return True
        except IntegrityError:
            db.session.rollback()
            return False

    @staticmethod
    def matricular_com_lotacao(aluno_id, turma_id, *, commit=True):
        existente = Matricula.query.filter_by(aluno_id=aluno_id, turma_id=turma_id).first()
        if existente:
            return False

        turma = Turma.query.filter_by(id=turma_id).with_for_update().first()
        if not turma:
            return False
        quantidade = Matricula.query.filter_by(turma_id=turma_id).count()
        if quantidade >= turma.limite_alunos:
            return False

        db.session.add(Matricula(aluno_id=aluno_id, turma_id=turma_id))
        if commit:
            db.session.commit()
        return True

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
