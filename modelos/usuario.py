from config import db
from werkzeug.security import generate_password_hash, check_password_hash


class Aluno(db.Model):
    __tablename__ = 'alunos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    datanascimento = db.Column(db.String, nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    mensalidade = db.Column(db.String(50), default='pendente', nullable=False)
    descricao = db.Column(db.String(255), nullable=True)

    # RF: o cadastro do aluno na academia existe sem conta de acesso. `login`, `email` e
    # `senha_hash` descrevem SÓ a conta - um aluno matriculado pela administração nasce
    # com os três em NULL e mesmo assim tem plano, mensalidades e histórico próprios.
    # (Unique aceita vários NULL tanto no SQLite quanto no PostgreSQL.)
    login = db.Column(db.String(50), unique=True, nullable=True)
    email = db.Column(db.String(150), unique=True, nullable=True)
    senha_hash = db.Column(db.String(255), nullable=True)

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
    # Indexado porque a validação do link busca EXATAMENTE por este hash a cada clique;
    # sem índice a rota varria a tabela de alunos inteira.
    token_recuperacao_hash = db.Column(db.String(64), nullable=True, index=True)
    token_recuperacao_expira = db.Column(db.DateTime, nullable=True)

    # RF: troca de e-mail pelo próprio aluno só é aplicada após confirmação por link
    # enviado ao novo endereço (evita apontar a conta para um e-mail que não é do dono).
    email_pendente = db.Column(db.String(150), nullable=True)
    token_email_hash = db.Column(db.String(64), nullable=True, index=True)
    token_email_expira = db.Column(db.DateTime, nullable=True)

    # RF: convite de acesso para um cadastro criado pela administração. O aluno só vira
    # dono da conta clicando num link de uso único enviado ao e-mail que a administração
    # registrou - CPF, nome ou data de nascimento nunca bastam para assumir um cadastro.
    token_convite_hash = db.Column(db.String(64), nullable=True, index=True)
    token_convite_expira = db.Column(db.DateTime, nullable=True)
    convite_enviado_em = db.Column(db.DateTime, nullable=True)

    # RF: foto de perfil - guarda só o nome gerado (UUID + extensão) do arquivo já
    # reprocessado pelo servico de armazenamento; nunca o nome original nem base64.
    foto_arquivo = db.Column(db.String(64), nullable=True)
    # Graduação/nível do aluno (ex.: "Kruang branco") - texto livre definido pelo admin.
    graduacao = db.Column(db.String(80), nullable=True)

    # Construtor da classe
    def __init__(self, nome, datanascimento, cpf, login=None, email=None, telefone=None, senha=None,
                 descricao=None, mensalidade='pendente', plano_id=None, data_vencimento=None,
                 status_cadastro='pendente', ativo=True, graduacao=None):
        self.nome = nome
        self.login = login or None
        self.datanascimento = datanascimento
        self.cpf = cpf
        self.email = email or None
        self.telefone = telefone
        if senha:
            self.set_senha(senha)
        self.descricao = descricao
        self.mensalidade = mensalidade
        self.plano_id = plano_id
        self.data_vencimento = data_vencimento
        self.status_cadastro = status_cadastro
        self.ativo = ativo
        self.graduacao = graduacao

    @property
    def iniciais(self):
        partes = [p for p in (self.nome or '').split() if p]
        if not partes:
            return '?'
        if len(partes) == 1:
            return partes[0][0].upper()
        return (partes[0][0] + partes[-1][0]).upper()

    def set_senha(self, senha_texto_puro):
        self.senha_hash = generate_password_hash(senha_texto_puro)

    def verificar_senha(self, senha_texto_puro):
        # Cadastro sem conta de acesso não tem hash para comparar: nenhuma senha serve.
        if not self.senha_hash:
            return False
        return check_password_hash(self.senha_hash, senha_texto_puro)

    @property
    def esta_ativo(self):
        # RN02: só é considerado ativo com cadastro aprovado e sem estar desativado pelo admin.
        return self.status_cadastro == 'aprovado' and self.ativo

    @property
    def acesso_ativado(self):
        """Se existe uma conta de acesso, e não se o aluno está em dia ou matriculado.

        Derivado do hash em vez de guardado numa coluna própria: assim não há como o
        estado de acesso divergir da senha que de fato permite entrar.
        """
        return bool(self.senha_hash)

    @property
    def convite_pendente(self):
        """Convite de acesso já enviado e ainda não usado (a validade é checada na rota)."""
        return not self.acesso_ativado and bool(self.token_convite_hash)

    @property
    def estado_acesso(self):
        """Chave do estado da CONTA - nunca da situação financeira nem da matrícula."""
        if self.acesso_ativado:
            return 'ativado'
        if self.convite_pendente:
            return 'convite_enviado'
        return 'nao_ativado'

    @property
    def rotulo_acesso(self):
        return {
            'ativado': 'Acesso ativado',
            'convite_enviado': 'Convite enviado',
            'nao_ativado': 'Acesso não ativado',
        }[self.estado_acesso]
