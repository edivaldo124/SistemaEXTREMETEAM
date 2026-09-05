from config import db
from dao.financeiroDAO import PagamentoDAO
from modelos.plano import Plano
from modelos.usuario import Aluno
from sqlalchemy.exc import SQLAlchemyError
from servicos.formatacao import variantes_cpf

class AlunoDAO:
    @staticmethod
    def salvar(aluno):
        db.session.add(aluno)
        db.session.commit()

    @staticmethod
    def listar_todos():
        return Aluno.query.all()

    @staticmethod
    def listar_pendentes():
        return Aluno.query.filter_by(status_cadastro='pendente').all()

    @staticmethod
    def definir_status_cadastro(aluno_id, status):
        aluno = db.session.get(Aluno, aluno_id)
        if not aluno:
            return None
        aluno.status_cadastro = status
        db.session.commit()
        return aluno

    @staticmethod
    def definir_ativo(aluno_id, ativo):
        aluno = db.session.get(Aluno, aluno_id)
        if not aluno:
            return False
        aluno.ativo = ativo
        db.session.commit()
        return True

    @staticmethod
    def autenticar(usuario, senha):
        # Busca por usuário/email/login/cpf e só então confere o hash da senha em Python.
        cpfs_possiveis = variantes_cpf(usuario)
        aluno = Aluno.query.filter(
            (Aluno.nome == usuario) |
            (Aluno.login == usuario) |
            (Aluno.email == usuario) |
            (Aluno.cpf.in_(cpfs_possiveis))
        ).first()

        if aluno and aluno.verificar_senha(senha):
            return aluno
        return None

    @staticmethod
    def buscar_por_id(aluno_id):
        return db.session.get(Aluno, aluno_id)

    @staticmethod
    def buscar_por_usuario(usuario):
        # Busca o perfil pelo nome, email ou cpf que está salvo na sessão
        return Aluno.query.filter(
            (Aluno.nome == usuario) |(Aluno.login == usuario)| (Aluno.email == usuario) | (Aluno.descricao == usuario)| (Aluno.cpf == usuario)
        ).first()

    @staticmethod
    def atualizar_mensalidade(cpf, nova_situacao):
        aluno = Aluno.query.filter_by(cpf=cpf).first()
        if aluno:
            aluno.mensalidade = nova_situacao
            db.session.commit()
            return True
        return False

    @staticmethod
    def remover(aluno_id):
        aluno = db.session.get(Aluno, aluno_id)
        if not aluno:
            return None

        try:
            db.session.delete(aluno)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

    @staticmethod
    def definir_foto(aluno_id, nome_arquivo):
        aluno = db.session.get(Aluno, aluno_id)
        if not aluno:
            return None
        aluno.foto_arquivo = nome_arquivo
        db.session.commit()
        return aluno

    @staticmethod
    def atualizar_dados_completos(cpf, dados):
        aluno = Aluno.query.filter_by(cpf=cpf).first()
        if aluno:
            aluno.nome = dados.get('nome')
            aluno.login = dados.get('login')
            aluno.datanascimento = dados.get('datanascimento')
            aluno.email = dados.get('email')

            # Garantir que não enviam None para campos de texto opcionais
            aluno.telefone = dados.get('telefone', '')
            aluno.descricao = dados.get('descricao', '')
            if 'graduacao' in dados:
                aluno.graduacao = (dados.get('graduacao') or '').strip() or None

            # Só aceita um plano que exista de verdade: um id inválido no formulário
            # gravaria uma FK pendurada (ou estouraria um 500 na conversão).
            plano_escolhido = dados.get('plano_id')
            plano = None
            if plano_escolhido and plano_escolhido != 'Nenhum':
                try:
                    plano = Plano.query.filter_by(id=int(plano_escolhido)).first()
                except (TypeError, ValueError):
                    plano = None
                if not plano:
                    return False
            aluno.plano_id = plano.id if plano else None

            # `mensalidade` e `data_vencimento` são derivados das mensalidades pagas -
            # trocar o plano no cadastro não paga período nenhum e por isso não pode
            # inventar uma nova validade. Antes, o admin editar o plano estendia o
            # vencimento em `duracao_dias` sem nenhum pagamento por trás, e o valor
            # ficava divergindo do histórico financeiro.
            PagamentoDAO.sincronizar_situacao_do_aluno(aluno)
            return True
        return False
