from config import db
from modelos.presenca import Presenca


class PresencaDAO:
    @staticmethod
    def registrar_lote(turma_id, data_aula, presencas_por_aluno):
        existentes = {
            p.aluno_id: p
            for p in Presenca.query.filter_by(turma_id=turma_id, data_aula=data_aula).all()
        }

        for aluno_id, presente in presencas_por_aluno.items():
            registro = existentes.get(aluno_id)
            if registro:
                registro.presente = presente
            else:
                db.session.add(Presenca(aluno_id=aluno_id, turma_id=turma_id, data_aula=data_aula, presente=presente))

        db.session.commit()

    @staticmethod
    def listar_por_turma_e_data(turma_id, data_aula):
        return Presenca.query.filter_by(turma_id=turma_id, data_aula=data_aula).all()

    @staticmethod
    def listar_por_aluno(aluno_id):
        return Presenca.query.filter_by(aluno_id=aluno_id).order_by(Presenca.data_aula.desc()).all()
