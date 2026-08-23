from config import db
from werkzeug.security import generate_password_hash, check_password_hash


class Aluno(db.Model):
    __tablename__ = 'alunos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    datanascimento = db.Column(db.String, nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    mensalidade = db.Column(db.String(50), default='pendente', nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(255), nullable=True)

    # RF03: cadastro do aluno depende de aprovação do administrador.
    status_cadastro = db.Column(db.String(20), nullable=False, default='pendente')  # pendente | aprovado | recusado
    # RF04: administrador pode ativar/desativar o aluno independente da aprovação.
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    # Chave estrangeira para o plano
    plano_id = db.Column(db.Integer, db.ForeignKey('planos.id'), nullable=True)

    # Mapeamento do relacionamento para buscar os dados do plano automaticamente
    plano = db.relationship('Plano', backref='alunos', lazy=True)
    data_vencimento = db.Column(db.String(10), nullable=True)

    # RF: recuperação de senha por token de uso único (nunca a senha é trocada só com CPF+e-mail).
    token_recuperacao_hash = db.Column(db.String(64), nullable=True)
    token_recuperacao_expira = db.Column(db.DateTime, nullable=True)

    # RF: troca de e-mail pelo próprio aluno só é aplicada após confirmação por link
    # enviado ao novo endereço (evita apontar a conta para um e-mail que não é do dono).
    email_pendente = db.Column(db.String(150), nullable=True)
    token_email_hash = db.Column(db.String(64), nullable=True)
    token_email_expira = db.Column(db.DateTime, nullable=True)

    # Construtor da classe
    def __init__(self, nome, login, datanascimento, cpf, email, telefone, senha, descricao,
                 mensalidade='pendente', plano_id=None, data_vencimento=None, status_cadastro='pendente', ativo=True):
        self.nome = nome
        self.login = login
        self.datanascimento = datanascimento
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.set_senha(senha)
        self.descricao = descricao
        self.mensalidade = mensalidade
        self.plano_id = plano_id
        self.data_vencimento = data_vencimento
        self.status_cadastro = status_cadastro
        self.ativo = ativo

    def set_senha(self, senha_texto_puro):
        self.senha_hash = generate_password_hash(senha_texto_puro)

    def verificar_senha(self, senha_texto_puro):
        return check_password_hash(self.senha_hash, senha_texto_puro)

    @property
    def esta_ativo(self):
        # RN02: só é considerado ativo com cadastro aprovado e sem estar desativado pelo admin.
        return self.status_cadastro == 'aprovado' and self.ativo
