from config import db
from dao.financeiroDAO import PagamentoDAO
from modelos.plano import Plano
from modelos.usuario import Aluno
from sqlalchemy.exc import SQLAlchemyError
from servicos.formatacao import variantes_cpf
from werkzeug.security import check_password_hash, generate_password_hash


_HASH_DESCARTAVEL = generate_password_hash('senha-descartavel-para-equalizar-tempo')

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
        # Nome não é identificador: não é único e pode ser editado pelo próprio aluno.
        cpfs_possiveis = variantes_cpf(usuario)
        aluno = Aluno.query.filter(
            (Aluno.login == usuario) |
            (Aluno.email == usuario) |
            (Aluno.cpf.in_(cpfs_possiveis))
        ).first()

        # Mantém uma verificação de hash mesmo quando a conta não existe, reduzindo a
        # diferença de tempo usada para enumerar logins válidos.
        senha_valida = aluno.verificar_senha(senha) if aluno else check_password_hash(_HASH_DESCARTAVEL, senha)
        if aluno and senha_valida:
            return aluno
        return None

    @staticmethod
    def buscar_por_id(aluno_id):
        return db.session.get(Aluno, aluno_id)

    @staticmethod
    def buscar_por_cpf(cpf):
        # Rotas administrativas recebem CPF. Comparar esse valor com campos editáveis
        # permitia selecionar e alterar o registro de outro aluno.
        return Aluno.query.filter(Aluno.cpf.in_(variantes_cpf(cpf))).first()

    @staticmethod
    def atualizar_mensalidade(cpf, nova_situacao):
        aluno = AlunoDAO.buscar_por_cpf(cpf)
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
        aluno = AlunoDAO.buscar_por_cpf(cpf)
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
