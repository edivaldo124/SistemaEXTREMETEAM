from config import db


class Turma(db.Model):
    __tablename__ = 'turmas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    dias_semana = db.Column(db.String(100), nullable=False)  # ex.: "Seg,Qua,Sex"
    horario = db.Column(db.String(20), nullable=False)  # ex.: "19:00"
    limite_alunos = db.Column(db.Integer, nullable=False, default=20)

    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'), nullable=False)
    professor = db.relationship('Professor', backref='turmas', lazy=True)

    def __init__(self, nome, dias_semana, horario, professor_id, limite_alunos=20):
        self.nome = nome
        self.dias_semana = dias_semana
        self.horario = horario
        self.professor_id = professor_id
        self.limite_alunos = limite_alunos

    @property
    def lista_dias(self):
        return [d.strip() for d in self.dias_semana.split(',') if d.strip()]
