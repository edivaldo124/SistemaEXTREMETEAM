import hmac
import secrets
from datetime import date

from flask import Blueprint, abort, flash, redirect, render_template, request, session
from config import db
from modelos.plano import Plano
from dao.usuarioDAO import AlunoDAO
from dao.planoDAO import PlanoDAO
from dao.financeiroDAO import PagamentoDAO
from modelos.pagamento import Pagamento
from servicos.formatacao import formatar_telefone
from servicos.email import enviar_email

admin_bp = Blueprint('admin_blueprint', __name__)


def usuario_e_admin():
    return session.get('tipo_usuario') == 'admin'


@admin_bp.route("/admin")
def painel_adm():
    if not usuario_e_admin():
        return redirect('/login')

    lista_usuarios = [u for u in AlunoDAO.listar_todos() if u.status_cadastro != 'pendente']
    pendentes = AlunoDAO.listar_pendentes()
    lista_planos = PlanoDAO.listar_todos()
    token_exclusao = session.get('token_exclusao')

    if not token_exclusao:
        token_exclusao = secrets.token_urlsafe(32)
        session['token_exclusao'] = token_exclusao

    return render_template(
        "pgAdm.html",
        usuarios=lista_usuarios,
        pendentes=pendentes,
        planos=lista_planos,
        token_exclusao=token_exclusao
    )


@admin_bp.route("/admin/aluno/<int:aluno_id>/aprovar", methods=["POST"])
def aprovar_aluno(aluno_id):
    if not usuario_e_admin():
        return redirect('/login')

    aluno = AlunoDAO.definir_status_cadastro(aluno_id, 'aprovado')
    if aluno:
        flash('Cadastro aprovado.', 'sucesso')
        enviar_email(
            aluno.email, aluno.nome, 'Cadastro aprovado — Extreme Team', 'Seu cadastro foi aprovado!',
            [
                f'Olá, {aluno.nome.split()[0]}!',
                'Boas notícias: seu cadastro na Extreme Team foi aprovado pela administração.',
                'Você já pode entrar com seu usuário e senha para escolher um plano e começar a treinar.',
            ],
        )
    else:
        flash('Aluno não encontrado.', 'erro')
    return redirect('/admin')


@admin_bp.route("/admin/aluno/<int:aluno_id>/recusar", methods=["POST"])
def recusar_aluno(aluno_id):
    if not usuario_e_admin():
        return redirect('/login')

    aluno = AlunoDAO.definir_status_cadastro(aluno_id, 'recusado')
    if aluno:
        flash('Cadastro recusado.', 'sucesso')
        enviar_email(
            aluno.email, aluno.nome, 'Sobre seu cadastro — Extreme Team', 'Seu cadastro não foi aprovado',
            [
                f'Olá, {aluno.nome.split()[0]}.',
                'Analisamos seu cadastro na Extreme Team e, no momento, não foi possível aprová-lo.',
                'Se quiser entender o motivo ou tentar novamente, fale com a nossa administração.',
            ],
        )
    else:
        flash('Aluno não encontrado.', 'erro')
    return redirect('/admin')


@admin_bp.route("/admin/aluno/<int:aluno_id>/ativar", methods=["POST"])
def ativar_aluno(aluno_id):
    if not usuario_e_admin():
        return redirect('/login')

    AlunoDAO.definir_ativo(aluno_id, True)
    flash('Aluno ativado.', 'sucesso')
    return redirect('/admin')


@admin_bp.route("/admin/aluno/<int:aluno_id>/desativar", methods=["POST"])
def desativar_aluno(aluno_id):
    if not usuario_e_admin():
        return redirect('/login')

    AlunoDAO.definir_ativo(aluno_id, False)
    flash('Aluno desativado.', 'sucesso')
    return redirect('/admin')


@admin_bp.route("/admin/cadastrar_plano", methods=["POST"])
def cadastrar_plano():
    if not usuario_e_admin():
        return redirect('/login')

    nome_plano = request.form.get("nome_plano")
    preco_plano = request.form.get("preco_plano")
    duracao_dias = request.form.get("duracao_dias")  # Captura os dias

    if nome_plano and preco_plano and duracao_dias:
        novo_plano = Plano(nome_plano=nome_plano, preco_plano=float(preco_plano),duracao_dias=int(duracao_dias))
        PlanoDAO.salvar(novo_plano)

    return redirect('/admin')

#


@admin_bp.route("/admin/remover/<int:aluno_id>", methods=["POST"])
def remover_usuario(aluno_id):
    if not usuario_e_admin():
        return redirect('/login')

    token_formulario = request.form.get('token_exclusao', '')
    token_sessao = session.get('token_exclusao', '')

    if not token_sessao or not hmac.compare_digest(token_formulario, token_sessao):
        abort(400)

    resultado = AlunoDAO.remover(aluno_id)
    session['token_exclusao'] = secrets.token_urlsafe(32)

    if resultado is True:
        flash('Aluno removido com sucesso.', 'sucesso')
    elif resultado is None:
        flash('Aluno não encontrado.', 'erro')
    else:
        flash('Não foi possível remover o aluno porque existem dados vinculados.', 'erro')

    return redirect('/admin')





@admin_bp.route("/admin/mensalidade/<cpf>/<status>", methods=["POST"])
def alterar_mensalidade(cpf, status):
    if not usuario_e_admin():
        return redirect('/login')

    AlunoDAO.atualizar_mensalidade(cpf, status)

    return redirect('/admin')


@admin_bp.route('/admin/remover_plano/<int:plano_id>', methods=["POST"])
def remover_plano(plano_id):
    if not usuario_e_admin():
        return redirect('/login')

    resultado = PlanoDAO.remover(plano_id)
    if resultado is True:
        flash('Plano removido com sucesso.', 'sucesso')
    elif resultado is None:
        flash('Plano não encontrado.', 'erro')
    else:
        flash('Não foi possível remover: existem mensalidades vinculadas a esse plano.', 'erro')
    return redirect('/admin')


@admin_bp.route("/admin/usuario/<cpf>", methods=["GET", "POST"])
def detalhes_usuario(cpf):
    if not usuario_e_admin():
        return redirect('/login')

    aluno = AlunoDAO.buscar_por_usuario(cpf)

    if not aluno:
        return redirect('/admin')

    if request.method == "POST":
        dados_atualizados = {
            'nome': request.form.get("nome"),
            'login': request.form.get("login"),
            'datanascimento': request.form.get("datanascimento"),
            'email': request.form.get("email"),
            'telefone': formatar_telefone(request.form.get("telefone")),
            'mensalidade': request.form.get("mensalidade"),
            'plano_id': request.form.get("plano_id"),
            'descricao': request.form.get('descricao')
        }

        AlunoDAO.atualizar_dados_completos(cpf, dados_atualizados)

        return redirect('/admin')


    planos = PlanoDAO.listar_todos()
    pagamentos = PagamentoDAO.listar_por_aluno(aluno.id)
    return render_template("dt_aluno.html", u=aluno, planos=planos, pagamentos=pagamentos)


@admin_bp.route("/admin/usuario/<cpf>/pagamentos", methods=["POST"])
def cadastrar_pagamento(cpf):
    if not usuario_e_admin():
        return redirect('/login')

    aluno = AlunoDAO.buscar_por_usuario(cpf)
    plano = PlanoDAO.buscar_por_id(request.form.get('plano_id'))

    valor = request.form.get('valor')
    vencimento = request.form.get('vencimento')
    status = request.form.get('status')
    forma_pagamento = request.form.get('forma_pagamento')
    data_pagamento = request.form.get('data_pagamento')

    if aluno and plano and valor and vencimento:
        novo_pagamento = Pagamento(
            aluno_id=aluno.id,
            plano_id=plano.id,
            valor=float(valor),
            vencimento=date.fromisoformat(vencimento),
            status=status,
            forma_pagamento=forma_pagamento if forma_pagamento else None,
            data_pagamento=date.fromisoformat(data_pagamento) if data_pagamento else None
        )

        PagamentoDAO.salvar(novo_pagamento)
        aluno.mensalidade = 'Em Dia' if status == 'pago' else status.capitalize()
        db.session.commit()

    return redirect(f'/admin/usuario/{cpf}')


@admin_bp.route("/admin/pagamentos/<int:pagamento_id>/status", methods=["POST"])
def atualizar_status_pagamento(pagamento_id):
    if not usuario_e_admin():
        return redirect('/login')

    pagamento = PagamentoDAO.buscar_por_id(pagamento_id)
    if not pagamento:
        flash('Pagamento não encontrado.', 'erro')
        return redirect('/admin')

    status = request.form.get('status')
    forma_pagamento = request.form.get('forma_pagamento')

    PagamentoDAO.atualizar_status(pagamento_id, status, forma_pagamento)
    pagamento.aluno.mensalidade = 'Em Dia' if status == 'pago' else status.capitalize()
    db.session.commit()

    return redirect(f'/admin/usuario/{pagamento.aluno.cpf}')


def _esta_inadimplente(aluno):
    return (aluno.mensalidade or '').strip().lower() not in ('em dia', '')


def _paragrafos_cobranca(aluno):
    paragrafos = [
        f'Olá, {aluno.nome.split()[0]}.',
        'Identificamos uma pendência na sua mensalidade na Extreme Team.',
    ]
    if aluno.plano:
        preco = f"{aluno.plano.preco_plano:.2f}".replace('.', ',')
        paragrafos.append(f'Plano: {aluno.plano.nome_plano} — R$ {preco}')
    if aluno.data_vencimento:
        paragrafos.append(f'Vencimento: {aluno.data_vencimento}')
    paragrafos.append('Regularize o quanto antes para continuar treinando sem interrupções. Qualquer dúvida, fale com a nossa administração.')
    return paragrafos


@admin_bp.route("/admin/avisos", methods=["GET", "POST"])
def enviar_aviso():
    if not usuario_e_admin():
        return redirect('/login')

    if request.method == "POST":
        assunto = (request.form.get('assunto') or '').strip()
        mensagem = (request.form.get('mensagem') or '').strip()
        destinatarios = request.form.get('destinatarios', 'todos')

        if not assunto or not mensagem:
            flash('Preencha o assunto e a mensagem do aviso.', 'erro')
            return redirect('/admin/avisos')

        alunos = [a for a in AlunoDAO.listar_todos() if a.esta_ativo]
        if destinatarios == 'inadimplentes':
            alunos = [a for a in alunos if _esta_inadimplente(a)]

        paragrafos = [linha.strip() for linha in mensagem.splitlines() if linha.strip()]
        enviados = sum(1 for aluno in alunos if enviar_email(aluno.email, aluno.nome, assunto, assunto, paragrafos))

        flash(f'Aviso enviado para {enviados} de {len(alunos)} aluno(s).', 'sucesso')
        return redirect('/admin/avisos')

    alunos_ativos = [a for a in AlunoDAO.listar_todos() if a.esta_ativo]
    total_inadimplentes = sum(1 for a in alunos_ativos if _esta_inadimplente(a))
    return render_template(
        "admin_avisos.html",
        total_ativos=len(alunos_ativos),
        total_inadimplentes=total_inadimplentes,
    )


@admin_bp.route("/admin/avisos/cobranca", methods=["POST"])
def cobrar_inadimplentes():
    if not usuario_e_admin():
        return redirect('/login')

    alunos = [a for a in AlunoDAO.listar_todos() if a.esta_ativo and _esta_inadimplente(a)]
    enviados = sum(
        1 for aluno in alunos
        if enviar_email(
            aluno.email, aluno.nome, 'Mensalidade pendente — Extreme Team', 'Sua mensalidade está pendente',
            _paragrafos_cobranca(aluno),
        )
    )

    flash(f'Cobrança de mensalidade enviada para {enviados} de {len(alunos)} aluno(s) inadimplente(s).', 'sucesso')
    return redirect('/admin/avisos')


@admin_bp.route("/admin/usuario/<cpf>/cobrar", methods=["POST"])
def cobrar_mensalidade(cpf):
    if not usuario_e_admin():
        return redirect('/login')

    aluno = AlunoDAO.buscar_por_usuario(cpf)
    if not aluno:
        flash('Aluno não encontrado.', 'erro')
        return redirect('/admin')

    if enviar_email(
        aluno.email, aluno.nome, 'Mensalidade pendente — Extreme Team', 'Sua mensalidade está pendente',
        _paragrafos_cobranca(aluno),
    ):
        flash('Cobrança enviada por e-mail.', 'sucesso')
    else:
        flash('Não foi possível enviar o e-mail de cobrança.', 'erro')

    return redirect(f'/admin/usuario/{cpf}')
