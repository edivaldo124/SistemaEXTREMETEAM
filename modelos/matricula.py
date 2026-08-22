from datetime import date

from config import db


class Matricula(db.Model):
    __tablename__ = 'matriculas'
    __table_args__ = (db.UniqueConstraint('aluno_id', 'turma_id', name='uq_matricula_aluno_turma'),)

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id'), nullable=False)
    data_matricula = db.Column(db.Date, nullable=False, default=date.today)

    aluno = db.relationship('Aluno', backref='matriculas', lazy=True)
    turma = db.relationship('Turma', backref='matriculas', lazy=True)

    def __init__(self, aluno_id, turma_id, data_matricula=None):
        self.aluno_id = aluno_id
        self.turma_id = turma_id
        self.data_matricula = data_matricula or date.today()
