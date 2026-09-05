import hashlib
import hmac
import os
import secrets
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from flask import Blueprint, abort, flash, render_template, request, send_file, session, redirect, url_for
from sqlalchemy.exc import IntegrityError
from config import db
from modelos.usuario import Aluno
from modelos.matricula import Matricula
from modelos.turma import Turma
from dao.usuarioDAO import AlunoDAO
from dao.planoDAO import PlanoDAO
from dao.financeiroDAO import (
    ACAO_AGENDAR_MUDANCA,
    ACAO_CONTRATAR,
    ACAO_RENOVAR,
    ACOES_VALIDAS,
    CONTRATACAO_AGUARDANDO_DECISAO,
    CONTRATACAO_COBRANCA_CRIADA,
    CONTRATACAO_COBRANCA_EM_ANDAMENTO,
    CONTRATACAO_COBRANCA_REPLANEJADA,
    CONTRATACAO_COBRANCA_REUTILIZADA,
    CONTRATACAO_JA_ATIVO,
    CONTRATACAO_MESMO_PLANO,
    CONTRATACAO_MUDANCA_AGENDADA,
    CONTRATACAO_MUDANCA_CONFLITANTE,
    CONTRATACAO_MUDANCA_JA_EXISTE,
    CONTRATACAO_MUDANCA_SEM_VIGENCIA,
    CONTRATACAO_RENOVACAO_CRIADA,
    PagamentoDAO,
    SolicitacaoPlanoDAO,
    mensalidade_destaque,
    rotulo_status,
)
from dao.professorDAO import ProfessorDAO
from dao.matriculaDAO import MatriculaDAO
from dao.presencaDAO import PresencaDAO
from servicos.armazenamento import (
    ArquivoInvalido,
    caminho_arquivo,
    remover_arquivo,
    salvar_comprovante_manual,
    salvar_foto_perfil,
)
from servicos import planos as regras_plano
from servicos.formatacao import formatar_competencia, formatar_cpf, formatar_telefone, somente_digitos, variantes_cpf
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
            # O ID nao muda se o aluno editar o login ou o nome (o email so muda apos confirmacao).
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

        admin_email = os.environ.get('ADMIN_EMAIL')
        if admin_email:
            enviar_email(
                admin_email, 'Administração', 'Novo cadastro aguardando aprovação — Extreme Team', 'Novo cadastro pendente',
                [
                    f'O aluno {nome} acabou de se cadastrar e está aguardando aprovação.',
                    f'E-mail: {email}',
                    f'Telefone: {telefone}',
                    'Acesse o painel administrativo para aprovar ou recusar o cadastro.',
                ],
                link_url=url_for('admin_blueprint.painel_adm', _external=True),
                link_texto='Abrir painel administrativo',
            )

        return render_template('login.html', msg='Cadastro enviado! Assim que for aprovado pela administração você poderá entrar.')

    return render_template("cadastro.html")


# Cada código devolvido por PagamentoDAO.contratar_plano vira uma frase para o aluno.
# Nenhuma delas sugere pagar de novo quando já existe pagamento feito ou em decisão.
MENSAGENS_CONTRATACAO = {
    CONTRATACAO_COBRANCA_CRIADA: ('Plano escolhido. Conclua o pagamento para ativar.', 'sucesso'),
    CONTRATACAO_COBRANCA_REUTILIZADA: ('Esta cobrança já estava aberta. Continue o pagamento por aqui.', 'sucesso'),
    CONTRATACAO_COBRANCA_REPLANEJADA: ('Plano da cobrança em aberto atualizado. Conclua o pagamento para ativar.', 'sucesso'),
    CONTRATACAO_RENOVACAO_CRIADA: ('Renovação criada. Este pagamento é do próximo período — o atual continua valendo.', 'sucesso'),
    CONTRATACAO_JA_ATIVO: ('Seu plano já está ativo e pago neste período. Não há nada a pagar agora.', 'sucesso'),
    CONTRATACAO_AGUARDANDO_DECISAO: ('Você já tem um pagamento aguardando análise. Não é preciso pagar de novo.', 'sucesso'),
    CONTRATACAO_COBRANCA_EM_ANDAMENTO: ('Existe uma cobrança em andamento para esta mensalidade. Conclua ou aguarde ela expirar antes de trocar de plano.', 'erro'),
    CONTRATACAO_MUDANCA_AGENDADA: ('Mudança de plano agendada. Seu plano atual e seus benefícios continuam até o fim do período pago.', 'sucesso'),
    CONTRATACAO_MUDANCA_JA_EXISTE: ('Você já tem uma mudança agendada para este plano.', 'sucesso'),
    CONTRATACAO_MUDANCA_CONFLITANTE: ('Você já tem uma mudança de plano agendada. Cancele a solicitação atual antes de pedir outra.', 'erro'),
    CONTRATACAO_MUDANCA_SEM_VIGENCIA: ('Você não tem um período pago em curso, então basta contratar o plano desejado.', 'erro'),
    CONTRATACAO_MESMO_PLANO: ('Este já é o seu plano atual.', 'erro'),
}


def _plano_do_formulario():
    try:
        plano_id = int(request.form.get("plano") or 0)
    except (TypeError, ValueError):
        return None
    return PlanoDAO.buscar_por_id(plano_id) if plano_id else None


@auth_bp.route("/perfil", methods=["GET", "POST"])
def pagina_perfil():
    if session.get('tipo_usuario') != 'aluno' or not session.get('aluno_id'):
        return redirect('/login')

    aluno_dados = db.session.get(Aluno, session['aluno_id'])

    if not aluno_dados:
        session.clear()
        return redirect('/logout')

    if request.method == "POST":
        plano = _plano_do_formulario()
        if not plano:
            flash('Plano inválido ou indisponível.', 'erro')
            return redirect(url_for('auth.pagina_perfil', _anchor='planos'))

        # A ação declarada pelo formulário é só uma intenção: o DAO revalida tudo contra
        # o banco, então um `acao` forjado não consegue gerar cobrança onde a regra não
        # permite (período pago, comprovante em análise, mudança conflitante...).
        acao = request.form.get("acao") or ACAO_CONTRATAR
        if acao not in ACOES_VALIDAS:
            acao = ACAO_CONTRATAR

        try:
            resultado = PagamentoDAO.contratar_plano(
                aluno=aluno_dados, plano=plano, acao=acao, ator=aluno_dados.login,
            )
        except Exception:
            db.session.rollback()
            flash('Não foi possível concluir a operação. Tente novamente.', 'erro')
            return redirect(url_for('auth.pagina_perfil', _anchor='planos'))

        mensagem, categoria = MENSAGENS_CONTRATACAO.get(
            resultado.codigo, ('Operação concluída.', 'sucesso'),
        )
        flash(mensagem, categoria)

        # Só abre o Pix automaticamente quando existe mesmo algo a pagar agora.
        if resultado.gerou_cobranca and resultado.pagamento.status in regras_plano.STATUS_A_PAGAR:
            return redirect(url_for('auth.pagina_perfil', pix=resultado.pagamento.id, _anchor='mensalidades'))
        return redirect(url_for('auth.pagina_perfil', _anchor='planos'))

    # Um pedido de troca cuja data já chegou sem renovação passa a valer agora - isso
    # muda o plano do cadastro, mas não libera período nenhum sem pagamento.
    PagamentoDAO.efetivar_mudancas_por_prazo(aluno_dados)

    lista_planos = PlanoDAO.listar_todos()
    pagamentos = PagamentoDAO.listar_por_aluno(aluno_dados.id)
    solicitacao = SolicitacaoPlanoDAO.pendente_do_aluno(aluno_dados.id)
    situacao = regras_plano.situacao_plano(
        aluno_dados, pagamentos, solicitacao_mudanca=solicitacao,
    )
    matriculas = MatriculaDAO.listar_por_aluno(aluno_dados.id)
    presencas = PresencaDAO.listar_por_aluno(aluno_dados.id)
    total_presencas = sum(1 for p in presencas if p.presente)

    abrir_pix_id = request.args.get('pix', type=int)
    if abrir_pix_id:
        pagamento_pix = PagamentoDAO.buscar_por_id(abrir_pix_id)
        if not pagamento_pix or pagamento_pix.aluno_id != aluno_dados.id or pagamento_pix.status not in ('pendente', 'atrasado', 'recusado'):
            abrir_pix_id = None

    return render_template(
        "pgUsuario.html",
        usuario=aluno_dados,
        planos=lista_planos,
        pagamentos=pagamentos,
        situacao=situacao,
        # O card destaca o que exige atenção; sem nada em aberto, mostra a mensalidade
        # que sustenta a vigência (em vez de pedir um pagamento que não existe).
        mensalidade_atual=situacao.cobranca or situacao.mensalidade_vigente or mensalidade_destaque(pagamentos),
        matriculas=matriculas,
        presencas=presencas,
        total_presencas=total_presencas,
        rotulo_status=rotulo_status,
        formatar_competencia=formatar_competencia,
        abrir_pix_id=abrir_pix_id,
    )


@auth_bp.route("/perfil/plano/mudanca/<int:solicitacao_id>/cancelar", methods=["POST"])
def cancelar_mudanca_plano(solicitacao_id):
    """Cancela um pedido de troca antes de ele ser aplicado.

    Depois de efetivado não há o que cancelar por aqui: a mudança já virou a cobrança de
    um período, e desfazer isso é decisão da administração sobre aquela mensalidade.
    """
    aluno = _aluno_da_sessao()
    if not aluno:
        return redirect('/login')

    solicitacao = SolicitacaoPlanoDAO.buscar_por_id(solicitacao_id)
    if not solicitacao or solicitacao.aluno_id != aluno.id:
        abort(404)

    if SolicitacaoPlanoDAO.cancelar(solicitacao, ator=aluno.login):
        flash('Mudança de plano cancelada. Seu plano atual segue valendo normalmente.', 'sucesso')
    else:
        flash('Esta solicitação não está mais pendente e não pode ser cancelada.', 'erro')

    return redirect(url_for('auth.pagina_perfil', _anchor='planos'))


TOKEN_EMAIL_VALIDADE = timedelta(minutes=30)


def _aluno_da_sessao():
    if session.get('tipo_usuario') != 'aluno' or not session.get('aluno_id'):
        return None
    return db.session.get(Aluno, session['aluno_id'])


@auth_bp.route("/perfil/dados", methods=["POST"])
def atualizar_dados_perfil():
    aluno = _aluno_da_sessao()
    if not aluno:
        return redirect('/login')

    senha_atual = request.form.get("senha_atual") or ""
    if not aluno.verificar_senha(senha_atual):
        flash('Senha atual incorreta. Nenhum dado foi alterado.', 'erro')
        return redirect('/perfil')

    nome = (request.form.get("nome") or "").strip()
    login = (request.form.get("login") or "").strip()
    telefone = formatar_telefone(request.form.get("telefone"))
    descricao = (request.form.get("descricao") or "").strip()

    if not all([nome, login]):
        flash('Preencha nome e usuário para salvar as alterações.', 'erro')
        return redirect('/perfil')

    if Aluno.query.filter(Aluno.login == login, Aluno.id != aluno.id).first():
        flash('Este nome de usuário já está em uso.', 'erro')
        return redirect('/perfil')

    aluno.nome = nome
    aluno.login = login
    aluno.telefone = telefone
    aluno.descricao = descricao
    db.session.commit()

    # Mantem a sessao coerente caso o login exibido tenha mudado.
    session['usuario'] = aluno.login

    flash('Dados atualizados com sucesso.', 'sucesso')
    return redirect('/perfil')


@auth_bp.route("/perfil/senha", methods=["POST"])
def alterar_senha_perfil():
    aluno = _aluno_da_sessao()
    if not aluno:
        return redirect('/login')

    senha_atual = request.form.get("senha_atual") or ""
    nova_senha = request.form.get("nova_senha") or ""
    confirmar_senha = request.form.get("confirmar_senha") or ""

    if not aluno.verificar_senha(senha_atual):
        flash('Senha atual incorreta. Nenhuma alteração foi feita.', 'erro')
        return redirect('/perfil')

    if len(nova_senha) < 6:
        flash('A nova senha deve ter pelo menos 6 caracteres.', 'erro')
        return redirect('/perfil')

    if not hmac.compare_digest(nova_senha, confirmar_senha):
        flash('A confirmação não coincide com a nova senha.', 'erro')
        return redirect('/perfil')

    aluno.set_senha(nova_senha)
    db.session.commit()

    enviar_email(
        aluno.email, aluno.nome, 'Sua senha foi alterada — Extreme Team', 'Senha alterada com sucesso',
        [
            f'Olá, {aluno.nome.split()[0]}.',
            'A senha da sua conta na Extreme Team acabou de ser alterada pelo seu perfil.',
            'Se não foi você quem fez isso, entre em contato com a nossa administração imediatamente.',
        ],
    )

    flash('Senha alterada com sucesso.', 'sucesso')
    return redirect('/perfil')


@auth_bp.route("/perfil/email", methods=["POST"])
def solicitar_troca_email():
    aluno = _aluno_da_sessao()
    if not aluno:
        return redirect('/login')

    senha_atual = request.form.get("senha_atual") or ""
    novo_email = (request.form.get("novo_email") or "").strip().lower()

    if not aluno.verificar_senha(senha_atual):
        flash('Senha atual incorreta. Nenhuma alteração foi feita.', 'erro')
        return redirect('/perfil')

    if not novo_email:
        flash('Informe o novo e-mail.', 'erro')
        return redirect('/perfil')

    if novo_email == aluno.email:
        flash('Este já é o seu e-mail atual.', 'erro')
        return redirect('/perfil')

    if Aluno.query.filter(Aluno.email == novo_email, Aluno.id != aluno.id).first():
        flash('Este e-mail já está em uso por outra conta.', 'erro')
        return redirect('/perfil')

    token = secrets.token_urlsafe(32)
    aluno.email_pendente = novo_email
    aluno.token_email_hash = hashlib.sha256(token.encode()).hexdigest()
    aluno.token_email_expira = datetime.utcnow() + TOKEN_EMAIL_VALIDADE
    db.session.commit()

    enviar_email(
        novo_email, aluno.nome, 'Confirme seu novo e-mail — Extreme Team', 'Confirme seu novo e-mail',
        [
            f'Olá, {aluno.nome.split()[0]}.',
            'Recebemos um pedido para associar este e-mail à sua conta na Extreme Team.',
            'Se foi você, clique no botão abaixo para confirmar a troca. O link expira em 30 minutos.',
            'Se não foi você, pode ignorar este e-mail — nada será alterado.',
        ],
        link_url=url_for('auth.confirmar_email', token=token, _external=True),
        link_texto='Confirmar novo e-mail',
    )
    enviar_email(
        aluno.email, aluno.nome, 'Pedido de troca de e-mail — Extreme Team', 'Pedido de troca de e-mail',
        [
            f'Olá, {aluno.nome.split()[0]}.',
            f'Foi solicitada a troca do e-mail da sua conta na Extreme Team para {novo_email}.',
            'Enviamos um link de confirmação para o novo endereço. Se não foi você quem pediu, fale com a nossa administração.',
        ],
    )

    flash(f'Enviamos um link de confirmação para {novo_email}. Seu e-mail só muda depois de confirmado.', 'sucesso')
    return redirect('/perfil')


@auth_bp.route("/perfil/confirmar_email/<token>")
def confirmar_email(token):
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    aluno = next(
        (
            a for a in Aluno.query.filter(Aluno.token_email_hash.isnot(None)).all()
            if hmac.compare_digest(a.token_email_hash, token_hash)
        ),
        None,
    )

    if not aluno or not aluno.token_email_expira or aluno.token_email_expira < datetime.utcnow() or not aluno.email_pendente:
        flash('Link de confirmação inválido ou expirado. Solicite a troca de e-mail novamente.', 'erro')
        return redirect('/perfil' if session.get('tipo_usuario') == 'aluno' else '/login')

    aluno.email = aluno.email_pendente
    aluno.email_pendente = None
    aluno.token_email_hash = None
    aluno.token_email_expira = None
    db.session.commit()

    flash('E-mail confirmado e atualizado com sucesso.', 'sucesso')
    return redirect('/perfil' if session.get('tipo_usuario') == 'aluno' else '/login')


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


# ---------------------------------------------------------------------------
# Foto de perfil
# ---------------------------------------------------------------------------

def _professor_pode_ver_aluno(aluno_id):
    professor_id = session.get('professor_id')
    if not professor_id:
        return False
    return (
        db.session.query(Matricula.id)
        .join(Turma, Matricula.turma_id == Turma.id)
        .filter(Matricula.aluno_id == aluno_id, Turma.professor_id == professor_id)
        .first() is not None
    )


def _pode_ver_foto(aluno_id):
    tipo = session.get('tipo_usuario')
    if tipo == 'admin':
        return True
    if tipo == 'aluno' and session.get('aluno_id') == aluno_id:
        return True
    if tipo == 'professor':
        return _professor_pode_ver_aluno(aluno_id)
    return False


@auth_bp.route('/perfil/foto/<int:aluno_id>')
def foto_perfil(aluno_id):
    # Nunca fica em static/ nem tem URL previsível por enumeração de nada além do
    # próprio ID do aluno - e mesmo assim exige sessão com permissão sobre esse aluno.
    if not _pode_ver_foto(aluno_id):
        abort(403)

    aluno = AlunoDAO.buscar_por_id(aluno_id)
    if not aluno or not aluno.foto_arquivo:
        abort(404)

    caminho = caminho_arquivo(aluno.foto_arquivo, subpasta='fotos')
    if not caminho:
        abort(404)

    return send_file(caminho, mimetype='image/jpeg', max_age=3600)


@auth_bp.route('/perfil/foto', methods=['POST'])
def enviar_foto_perfil():
    aluno = _aluno_da_sessao()
    if not aluno:
        return redirect('/login')

    arquivo = request.files.get('foto')
    if not arquivo or not arquivo.filename:
        flash('Selecione uma imagem para enviar.', 'erro')
        return redirect('/perfil')

    try:
        nome_arquivo = salvar_foto_perfil(arquivo.read())
    except ArquivoInvalido as erro:
        flash(str(erro), 'erro')
        return redirect('/perfil')

    foto_antiga = aluno.foto_arquivo
    aluno.foto_arquivo = nome_arquivo
    db.session.commit()
    if foto_antiga:
        remover_arquivo(foto_antiga, subpasta='fotos')

    flash('Foto atualizada com sucesso.', 'sucesso')
    return redirect('/perfil')


@auth_bp.route('/perfil/foto/remover', methods=['POST'])
def remover_foto_perfil():
    aluno = _aluno_da_sessao()
    if not aluno:
        return redirect('/login')

    if aluno.foto_arquivo:
        remover_arquivo(aluno.foto_arquivo, subpasta='fotos')
        aluno.foto_arquivo = None
        db.session.commit()
        flash('Foto removida.', 'sucesso')

    return redirect('/perfil')


# ---------------------------------------------------------------------------
# Tela de pagamento, comprovante e comprovante manual de uma mensalidade
# ---------------------------------------------------------------------------

STATUS_ACEITA_COMPROVANTE_MANUAL = ('pendente', 'atrasado', 'recusado')


def _acesso_permitido_pagamento(pagamento):
    if session.get('tipo_usuario') == 'admin':
        return True
    return session.get('tipo_usuario') == 'aluno' and session.get('aluno_id') == pagamento.aluno_id


def _pagamento_com_acesso_ou_404(pagamento_id):
    if session.get('tipo_usuario') not in ('admin', 'aluno'):
        return None
    pagamento = PagamentoDAO.buscar_por_id(pagamento_id)
    if not pagamento or not _acesso_permitido_pagamento(pagamento):
        return None
    return pagamento


@auth_bp.route('/perfil/pagamento/<int:pagamento_id>')
def pagina_pagamento(pagamento_id):
    if session.get('tipo_usuario') not in ('admin', 'aluno'):
        return redirect('/login')

    pagamento = _pagamento_com_acesso_ou_404(pagamento_id)
    if not pagamento:
        abort(404)

    if pagamento.status == 'pago':
        return redirect(url_for('auth.comprovante_mensalidade', pagamento_id=pagamento.id))

    return render_template(
        'pagamento.html',
        pagamento=pagamento,
        pode_enviar_comprovante=pagamento.status in STATUS_ACEITA_COMPROVANTE_MANUAL,
        # Mesma lista de status que o Checkout Pro aceita - só oferece a ação quando ela
        # realmente pode ser concluída.
        pode_pagar_online=pagamento.status in STATUS_ACEITA_COMPROVANTE_MANUAL,
        rotulo_status=rotulo_status,
        formatar_competencia=formatar_competencia,
    )


@auth_bp.route('/perfil/mensalidade/<int:pagamento_id>/comprovante')
def comprovante_mensalidade(pagamento_id):
    if session.get('tipo_usuario') not in ('admin', 'aluno'):
        return redirect('/login')

    pagamento = _pagamento_com_acesso_ou_404(pagamento_id)
    if not pagamento:
        abort(404)

    if pagamento.status != 'pago':
        flash('O comprovante só fica disponível depois que o pagamento é confirmado.', 'erro')
        return redirect(url_for('auth.pagina_pagamento', pagamento_id=pagamento.id))

    eventos_confirmacao = ('webhook_aprovado', 'comprovante_aprovado', 'manual_registrado')
    evento_confirmacao = next((e for e in pagamento.eventos if e.tipo in eventos_confirmacao), None)
    data_hora_confirmacao = None
    if evento_confirmacao:
        # Eventos são salvos em UTC (datetime.utcnow) - converte para o horário de
        # Brasília só na exibição do comprovante, sem alterar o que fica no banco.
        data_hora_confirmacao = evento_confirmacao.criado_em.replace(tzinfo=timezone.utc).astimezone(
            ZoneInfo('America/Sao_Paulo')
        )

    return render_template(
        'comprovante.html', pagamento=pagamento, formatar_competencia=formatar_competencia,
        data_hora_confirmacao=data_hora_confirmacao,
    )


@auth_bp.route('/perfil/mensalidade/<int:pagamento_id>/comprovante-manual', methods=['POST'])
def enviar_comprovante_manual_aluno(pagamento_id):
    aluno = _aluno_da_sessao()
    if not aluno:
        return redirect('/login')

    pagamento = PagamentoDAO.buscar_por_id(pagamento_id)
    if not pagamento or pagamento.aluno_id != aluno.id:
        abort(404)

    if pagamento.status not in STATUS_ACEITA_COMPROVANTE_MANUAL:
        flash('Esta mensalidade não está disponível para envio de comprovante.', 'erro')
        return redirect(url_for('auth.pagina_pagamento', pagamento_id=pagamento.id))

    arquivo = request.files.get('comprovante')
    if not arquivo or not arquivo.filename:
        flash('Selecione um arquivo para enviar.', 'erro')
        return redirect(url_for('auth.pagina_pagamento', pagamento_id=pagamento.id))

    try:
        nome_arquivo = salvar_comprovante_manual(arquivo.read())
    except ArquivoInvalido as erro:
        flash(str(erro), 'erro')
        return redirect(url_for('auth.pagina_pagamento', pagamento_id=pagamento.id))

    arquivo_antigo = pagamento.comprovante_manual_arquivo
    PagamentoDAO.enviar_comprovante_manual(pagamento, arquivo_nome=nome_arquivo, ator=aluno.login)
    if arquivo_antigo:
        remover_arquivo(arquivo_antigo, subpasta='comprovantes')

    flash('Comprovante enviado! Você será avisado quando a administração analisar.', 'sucesso')
    return redirect(url_for('auth.pagina_pagamento', pagamento_id=pagamento.id))


@auth_bp.route('/perfil/mensalidade/<int:pagamento_id>/comprovante-manual/arquivo')
def ver_comprovante_manual(pagamento_id):
    if session.get('tipo_usuario') not in ('admin', 'aluno'):
        return redirect('/login')

    pagamento = _pagamento_com_acesso_ou_404(pagamento_id)
    if not pagamento or not pagamento.comprovante_manual_arquivo:
        abort(404)

    caminho = caminho_arquivo(pagamento.comprovante_manual_arquivo, subpasta='comprovantes')
    if not caminho:
        abort(404)

    return send_file(caminho, max_age=0, as_attachment=False)
