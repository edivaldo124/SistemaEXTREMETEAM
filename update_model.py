import re

with open('modelos/usuario.py', 'r') as f:
    content = f.read()

new_cols = """
    # RF: verificação do endereço de e-mail ao criar o cadastro
    email_verificado = db.Column(db.Boolean, nullable=False, default=False)
    token_verificacao_hash = db.Column(db.String(64), nullable=True, index=True)
    token_verificacao_expira = db.Column(db.DateTime, nullable=True)

    email_pendente"""

content = content.replace("    email_pendente", new_cols)

# Update the constructor to include email_verificado
init_signature = "def __init__(self, nome, datanascimento, cpf, login=None, email=None, telefone=None, senha=None,\n                 descricao=None, mensalidade='pendente', plano_id=None, data_vencimento=None,\n                 status_cadastro='pendente', ativo=True, graduacao=None,\n                 termos_responsabilidade_versao=None, termos_responsabilidade_aceito_em=None, email_verificado=False):"
content = re.sub(r"def __init__\(self, nome, datanascimento, cpf, login=None, email=None, telefone=None, senha=None,\s+descricao=None, mensalidade='pendente', plano_id=None, data_vencimento=None,\s+status_cadastro='pendente', ativo=True, graduacao=None,\s+termos_responsabilidade_versao=None, termos_responsabilidade_aceito_em=None\):", init_signature, content)

init_body = """        self.graduacao = graduacao
        self.email_verificado = email_verificado"""
content = content.replace("        self.graduacao = graduacao", init_body)

with open('modelos/usuario.py', 'w') as f:
    f.write(content)
