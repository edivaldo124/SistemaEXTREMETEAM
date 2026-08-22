from config import db


class Presenca(db.Model):
    __tablename__ = 'presencas'
    __table_args__ = (db.UniqueConstraint('aluno_id', 'turma_id', 'data_aula', name='uq_presenca_aluno_turma_data'),)

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id'), nullable=False)
    data_aula = db.Column(db.Date, nullable=False)
    presente = db.Column(db.Boolean, nullable=False, default=False)

    aluno = db.relationship('Aluno', backref='presencas', lazy=True)
    turma = db.relationship('Turma', backref='presencas', lazy=True)

    def __init__(self, aluno_id, turma_id, data_aula, presente=False):
        self.aluno_id = aluno_id
        self.turma_id = turma_id
        self.data_aula = data_aula
        self.presente = presente
