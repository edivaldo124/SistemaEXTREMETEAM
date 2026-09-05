from sqlalchemy.exc import SQLAlchemyError

from config import db
from modelos.professor import Professor
from werkzeug.security import check_password_hash, generate_password_hash


_HASH_DESCARTAVEL = generate_password_hash('senha-descartavel-para-equalizar-tempo')


class ProfessorDAO:
    @staticmethod
    def salvar(professor):
        db.session.add(professor)
        db.session.commit()

    @staticmethod
    def listar_todos():
        return Professor.query.all()

    @staticmethod
    def buscar_por_id(professor_id):
        return db.session.get(Professor, professor_id)

    @staticmethod
    def autenticar(login, senha):
        professor = Professor.query.filter_by(login=login).first()
        senha_valida = professor.verificar_senha(senha) if professor else check_password_hash(_HASH_DESCARTAVEL, senha)
        if professor and senha_valida:
            return professor
        return None

    @staticmethod
    def remover(professor_id):
        professor = db.session.get(Professor, professor_id)
        if not professor:
            return None

        try:
            db.session.delete(professor)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False
