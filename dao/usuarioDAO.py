from config import db
from dao.financeiroDAO import PAGINA_TAMANHO_PADRAO, PagamentoDAO, _paginar
from modelos.plano import Plano
from modelos.usuario import Aluno
from sqlalchemy import func, or_
from sqlalchemy.exc import SQLAlchemyError
from servicos.formatacao import somente_digitos, variantes_cpf
from werkzeug.security import check_password_hash, generate_password_hash


_HASH_DESCARTAVEL = generate_password_hash('senha-descartavel-para-equalizar-tempo')

# Mínimo de dígitos para tratar o termo como CPF. Abaixo disso o trecho é curto demais
# para identificar alguém e casaria com quase todo mundo.
_MIN_DIGITOS_CPF = 4


def _parece_busca_por_cpf(termo):
    """O termo é um CPF, ou um pedaço dele, e não um nome que por acaso tem número?"""
    limpo = (termo or '').strip()
    if not limpo:
        return False
    # Aceita só dígitos e a pontuação usada em CPF: "529982", "529.982", "529.982.247-25".
    if any(c not in '0123456789.-' for c in limpo):
        return False
    return len(somente_digitos(limpo)) >= _MIN_DIGITOS_CPF

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
    def contar_cadastrados():
        """Quantos alunos a academia tem, sem filtro de busca.

        O card do topo do painel é uma métrica da academia e fica lado a lado com
        "Cadastros pendentes", que é global: mostrar ali o total da busca em curso
        faria os dois números falarem de universos diferentes.
        """
        return Aluno.query.filter(Aluno.status_cadastro != 'pendente').count()

    @staticmethod
    def listar_paginado(*, pagina=1, por_pagina=PAGINA_TAMANHO_PADRAO, busca=None):
        """Uma página de alunos já cadastrados, recortada e filtrada pelo banco.

        O painel administrativo carregava TODOS os alunos e descartava os pendentes em
        Python (`[u for u in listar_todos() if ...]`), trazendo a tabela inteira para a
        memória a cada abertura. O filtro e o recorte agora são do banco; os pendentes
        continuam saindo desta lista porque têm seção própria na tela.
        """
        consulta = Aluno.query.filter(Aluno.status_cadastro != 'pendente')
        if busca:
            def _escapar(valor):
                return valor.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')

            criterios = [Aluno.nome.ilike(f'%{_escapar(busca)}%', escape='\\')]

            # O CPF é guardado formatado ("529.982.247-25"). Comparar o que foi digitado
            # com a coluna crua falharia para quem digita só os números - e também para
            # um trecho que atravesse um ponto ("529982"). Os separadores são removidos
            # dos DOIS lados, então as três formas encontram a mesma pessoa.
            #
            # Só entra quando o termo é MESMO um CPF ou um pedaço dele: com qualquer
            # dígito servindo, buscar "Aluno 3" virava `CPF LIKE '%3%'` e devolvia a
            # academia inteira.
            if _parece_busca_por_cpf(busca):
                digitos = somente_digitos(busca)
                cpf_so_digitos = func.replace(
                    func.replace(Aluno.cpf, '.', ''), '-', '',
                )
                criterios.append(cpf_so_digitos.like(f'%{_escapar(digitos)}%', escape='\\'))

            consulta = consulta.filter(or_(*criterios))
        consulta = consulta.order_by(Aluno.nome.asc(), Aluno.id.asc())
        return _paginar(consulta, pagina=pagina, por_pagina=por_pagina)

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
            # Cadastro sem conta de acesso não é candidato a login. Sem este filtro, o
            # CPF - que é público e está impresso em qualquer ficha - selecionaria o
            # registro de um aluno matriculado pela administração.
            Aluno.senha_hash.isnot(None),
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
    def buscar_por_email(email):
        alvo = (email or '').strip().lower()
        return Aluno.query.filter(Aluno.email == alvo).first() if alvo else None

    @staticmethod
    def criar_pelo_admin(*, nome, cpf, datanascimento, telefone=None, email=None,
                         descricao=None, graduacao=None, plano_id=None):
        """Matrícula feita no balcão: sem login, sem senha e sem convite de acesso.

        Nasce 'aprovado' e ativo porque quem cadastrou já é a administração - não há
        nada a aprovar depois. O acesso ao sistema continua inexistente até o aluno
        aceitar um convite, e isso não impede plano, mensalidades nem histórico.
        """
        aluno = Aluno(
            nome=nome, cpf=cpf, datanascimento=datanascimento, telefone=telefone,
            email=email, descricao=descricao, graduacao=graduacao, plano_id=plano_id,
            status_cadastro='aprovado', ativo=True,
        )
        db.session.add(aluno)
        db.session.commit()
        return aluno

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
            aluno.datanascimento = dados.get('datanascimento')

            # Login e e-mail pertencem à CONTA. Um cadastro sem acesso pode ficar sem os
            # dois; uma conta ativa nunca pode perdê-los (é por eles que o aluno entra e
            # recebe os links de recuperação), então um campo vazio aqui é recusado.
            login = (dados.get('login') or '').strip() or None
            email = (dados.get('email') or '').strip().lower() or None
            if aluno.acesso_ativado and not (login and email):
                return False
            aluno.login = login
            if aluno.email != email:
                # Links entregues ao endereço anterior deixam de autorizar acesso.
                aluno.token_convite_hash = None
                aluno.token_convite_expira = None
                aluno.token_recuperacao_hash = None
                aluno.token_recuperacao_expira = None
            aluno.email = email

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
