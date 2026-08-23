import hashlib
import hmac
import os
import secrets
from datetime import datetime, timedelta

from flask import Blueprint, render_template, request, session, redirect, url_for
from sqlalchemy.exc import IntegrityError
from config import db
from modelos.usuario import Aluno
from dao.usuarioDAO import AlunoDAO
from dao.planoDAO import PlanoDAO
from dao.financeiroDAO import PagamentoDAO
from dao.professorDAO import ProfessorDAO
from dao.matriculaDAO import MatriculaDAO
from dao.presencaDAO import PresencaDAO
from servicos.formatacao import formatar_cpf, formatar_telefone, somente_digitos, variantes_cpf
from servicos.email import enviar_email

auth_bp = Blueprint('auth', __name__)

MSG_ERRO = 'Erro: Credenciais incorretas!'


@auth_bp.route("/login", methods=["GET", "POST"])
def pagina_login():
    if request.method == "POST":
        login = (request.form.get("loginusuario") or "").strip()
        senha = request.form.get("senhausuario") or ""

        admin_user = os.environ.get('ADMIN_USER')
        admin_password = os.environ.get('ADMIN_PASSWORD')
        if admin_user and admin_password and login == admin_user and hmac.compare_digest(senha, admin_password):
            # Remove qualquer sessao anterior para evitar fixacao de sessao.
            session.clear()
            session['usuario'] = admin_user
            session['tipo_usuario'] = "admin"
            session.permanent = True
            return redirect('/admin')

        professor = ProfessorDAO.autenticar(login, senha)
        if professor:
            session.clear()
            session['usuario'] = professor.login
            session['professor_id'] = professor.id
            session['tipo_usuario'] = "professor"
            session.permanent = True
            return redirect('/professor')

        aluno = AlunoDAO.autenticar(login, senha)
        if aluno:
            if aluno.status_cadastro == 'pendente':
                return render_template('login.html', msg='Seu cadastro ainda está em análise pela administração.')
            if aluno.status_cadastro == 'recusado':
                return render_template('login.html', msg='Seu cadastro não foi aprovado. Fale com a administração.')
            if not aluno.ativo:
                return render_template('login.html', msg='Sua conta está desativada. Fale com a administração.')

            session.clear()
            # O ID nao muda se o aluno editar o login, email ou nome.
            session['usuario'] = aluno.login
            session['aluno_id'] = aluno.id
            session['tipo_usuario'] = "aluno"
            session.permanent = True
            return redirect('/perfil')

        return render_template('login.html', msg=MSG_ERRO)

    return render_template("login.html")


@auth_bp.route("/cadastrar", methods=["GET", "POST"])
def pagina_cadastro():
    if request.method == "POST":
        nome = (request.form.get("nomeusuario") or "").strip()
        login = (request.form.get("loginusuario") or "").strip()
        datanascimento = (request.form.get("dataNascimento") or "").strip()
        cpf = formatar_cpf(request.form.get("cpfusuario"))
        senha = request.form.get("senhausuario") or ""
        email = (request.form.get("emailusuario") or "").strip().lower()
        telefone = formatar_telefone(request.form.get("telefoneusuario"))
        descricao = (request.form.get("descricaousuario") or "").strip()

        if not all([nome, login, datanascimento, cpf, senha.strip(), email, telefone]):
            return render_template("cadastro.html", erro="Erro: Preencha todos os campos obrigatórios!")

        if len(somente_digitos(cpf)) != 11:
            return render_template("cadastro.html", erro="Erro: Informe um CPF com 11 dígitos!")

        if Aluno.query.filter(Aluno.cpf.in_(variantes_cpf(cpf))).first():
            return render_template("cadastro.html", erro="Erro: Este CPF já está cadastrado!")

        if Aluno.query.filter_by(login=login).first():
            return render_template("cadastro.html", erro="Erro: Este usuário já está cadastrado!")

        if Aluno.query.filter_by(email=email).first():
            return render_template("cadastro.html", erro="Erro: Este e-mail já está cadastrado!")

        novo_aluno = Aluno(nome=nome, login=login, datanascimento=datanascimento, cpf=cpf, email=email, telefone=telefone, senha=senha, descricao=descricao)

        try:
            AlunoDAO.salvar(novo_aluno)
        except IntegrityError:
            db.session.rollback()
            return render_template("cadastro.html", erro="Erro: Não foi possível cadastrar. Verifique se os dados já estão em uso.")

        enviar_email(
            email, nome, 'Cadastro recebido — Extreme Team', 'Recebemos seu cadastro',
            [
                f'Olá, {nome.split()[0]}!',
                'Seu cadastro na Extreme Team foi recebido e está em análise pela nossa administração.',
                'Assim que for aprovado, você poderá entrar com seu usuário e senha.',
            ],
        )

        return render_template('login.html', msg='Cadastro enviado! Assim que for aprovado pela administração você poderá entrar.')

    return render_template("cadastro.html")


@auth_bp.route("/perfil", methods=["GET", "POST"])
def pagina_perfil():
    if session.get('tipo_usuario') != 'aluno' or not session.get('aluno_id'):
        return redirect('/login')

    aluno_dados = db.session.get(Aluno, session['aluno_id'])

    if not aluno_dados:
        session.clear()
        return redirect('/logout')

    if request.method == "POST":
        plano_id_escolhido = request.form.get("plano")
        if plano_id_escolhido and plano_id_escolhido != "Nenhum":
            aluno_dados.plano_id = int(plano_id_escolhido)
            db.session.commit()

    lista_planos = PlanoDAO.listar_todos()
    pagamentos = PagamentoDAO.listar_por_aluno(aluno_dados.id)
    matriculas = MatriculaDAO.listar_por_aluno(aluno_dados.id)
    presencas = PresencaDAO.listar_por_aluno(aluno_dados.id)

    return render_template(
        "pgUsuario.html",
        usuario=aluno_dados,
        planos=lista_planos,
        pagamentos=pagamentos,
        matriculas=matriculas,
        presencas=presencas,
    )

MSG_RECUPERACAO_ENVIADA = "Se os dados informados estiverem corretos, enviamos um e-mail com instruções para redefinir sua senha."
TOKEN_RECUPERACAO_VALIDADE = timedelta(minutes=30)


@auth_bp.route("/recuperar_senha", methods=["GET", "POST"])
def recuperar_senha():
    if request.method == "POST":
        cpf = formatar_cpf(request.form.get("cpf"))
        email = (request.form.get("email") or "").strip().lower()

        aluno = Aluno.query.filter(Aluno.cpf.in_(variantes_cpf(cpf)), Aluno.email == email).first()

        # Resposta identica para CPF/e-mail validos ou invalidos: evita que alguem use este
        # formulario para descobrir quais pares de CPF+e-mail existem na base.
        if aluno:
            token = secrets.token_urlsafe(32)
            aluno.token_recuperacao_hash = hashlib.sha256(token.encode()).hexdigest()
            aluno.token_recuperacao_expira = datetime.utcnow() + TOKEN_RECUPERACAO_VALIDADE
            db.session.commit()

            enviar_email(
                aluno.email, aluno.nome, 'Redefinir sua senha — Extreme Team', 'Redefinir sua senha',
                [
                    f'Olá, {aluno.nome.split()[0]}.',
                    'Recebemos um pedido para redefinir a senha da sua conta na Extreme Team.',
                    'Se foi você, clique no botão abaixo para escolher uma nova senha. O link expira em 30 minutos.',
                    'Se não foi você, pode ignorar este e-mail — sua senha continua a mesma.',
                ],
                link_url=url_for('auth.redefinir_senha', token=token, _external=True),
                link_texto='Redefinir minha senha',
            )

        return render_template("login.html", msg=MSG_RECUPERACAO_ENVIADA)

    return render_template("recuperar.html")


@auth_bp.route("/recuperar_senha/<token>", methods=["GET", "POST"])
def redefinir_senha(token):
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    aluno = next(
        (
            a for a in Aluno.query.filter(Aluno.token_recuperacao_hash.isnot(None)).all()
            if hmac.compare_digest(a.token_recuperacao_hash, token_hash)
        ),
        None,
    )

    if not aluno or not aluno.token_recuperacao_expira or aluno.token_recuperacao_expira < datetime.utcnow():
        return render_template("recuperar.html", erro="Link inválido ou expirado. Solicite uma nova recuperação de senha.")

    if request.method == "POST":
        nova_senha = request.form.get("nova_senha") or ""
        if len(nova_senha) < 6:
            return render_template("redefinir_senha.html", token=token, erro="A senha deve ter pelo menos 6 caracteres.")

        aluno.set_senha(nova_senha)
        aluno.token_recuperacao_hash = None
        aluno.token_recuperacao_expira = None
        db.session.commit()

        enviar_email(
            aluno.email, aluno.nome, 'Sua senha foi alterada — Extreme Team', 'Senha alterada com sucesso',
            [
                f'Olá, {aluno.nome.split()[0]}.',
                'A senha da sua conta na Extreme Team acabou de ser alterada.',
                'Se não foi você quem fez isso, entre em contato com a nossa administração imediatamente.',
            ],
        )
        return render_template("login.html", msg="Senha alterada com sucesso! Faça login.")

    return render_template("redefinir_senha.html", token=token)
