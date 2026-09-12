import hashlib
import hmac
import secrets
from datetime import date

from flask import Blueprint, abort, flash, redirect, render_template, request, session
from sqlalchemy.exc import IntegrityError
from config import db
from modelos.plano import Plano
from modelos.usuario import Aluno
from dao.usuarioDAO import AlunoDAO
from dao.planoDAO import PlanoDAO
from dao.turmaDAO import TurmaDAO
from dao.financeiroDAO import ACAO_CONTRATAR, PagamentoDAO, SolicitacaoPlanoDAO, rotulo_status
from modelos.pagamento import Pagamento
from servicos.armazenamento import ArquivoInvalido, remover_arquivo, salvar_foto_perfil
from servicos.autorizacao import sessao_administrativa_valida
from servicos import convites
from servicos import fila_email
from servicos import planos as regras_plano
from servicos.formatacao import formatar_competencia, formatar_cpf, formatar_telefone, somente_digitos, variantes_cpf
from servicos.email import email_valido, enviar_email

admin_bp = Blueprint('admin_blueprint', __name__)


def usuario_e_admin():
    """Sessão administrativa ainda válida.

    Delega para `servicos.autorizacao`: checar só `session['tipo_usuario']` aqui deixava
    TODO o painel administrativo de fora da revalidação - rotacionar a credencial do
    admin não encerrava a sessão já aberta com a senha anterior.
    """
    return sessao_administrativa_valida()


@admin_bp.route("/admin")
def painel_adm():
    if not usuario_e_admin():
        return redirect('/login')

    # Recorte e filtro vêm do banco: a tela carregava todos os alunos e separava os
    # pendentes em Python a cada abertura.
    pagina_alunos = AlunoDAO.listar_paginado(
        pagina=request.args.get('pagina', type=int) or 1,
        busca=(request.args.get('busca') or '').strip() or None,
    )
    pendentes = AlunoDAO.listar_pendentes()
    lista_planos = PlanoDAO.listar_todos()
    token_exclusao = session.get('token_exclusao')

    if not token_exclusao:
        token_exclusao = secrets.token_urlsafe(32)
        session['token_exclusao'] = token_exclusao

    return render_template(
        "pgAdm.html",
        usuarios=pagina_alunos.itens,
        pagina=pagina_alunos,
        total_alunos=AlunoDAO.contar_cadastrados(),
        busca=(request.args.get('busca') or '').strip(),
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


def _aluno_do_cpf_ou_painel(cpf):
    """Aluno de uma rota administrativa, ou None (a rota redireciona ao painel)."""
    aluno = AlunoDAO.buscar_por_cpf(cpf)
    if not aluno:
        flash('Aluno não encontrado.', 'erro')
    return aluno


@admin_bp.route("/admin/alunos/novo", methods=["GET", "POST"])
def cadastrar_aluno():
    """Matrícula feita pela administração, sem conta de acesso.

    Pede só o que identifica a pessoa e o que configura o plano dela. E-mail, usuário e
    senha ficam de fora: quem nunca vai entrar no sistema não precisa de conta, e quem
    quiser entrar depois recebe um convite (ver `enviar_convite_acesso`).
    """
    if not usuario_e_admin():
        return redirect('/login')

    planos = PlanoDAO.listar_todos()

    if request.method == "POST":
        dados = {
            'nome': (request.form.get('nome') or '').strip(),
            'cpf': formatar_cpf(request.form.get('cpf')),
            'datanascimento': (request.form.get('datanascimento') or '').strip(),
            'telefone': formatar_telefone(request.form.get('telefone')),
            'email': (request.form.get('email') or '').strip().lower(),
            'graduacao': (request.form.get('graduacao') or '').strip(),
            'descricao': (request.form.get('descricao') or '').strip(),
            'plano_id': (request.form.get('plano_id') or '').strip(),
            'gerar_mensalidade': request.form.get('gerar_mensalidade') == 'sim',
        }

        def recusar(mensagem):
            return render_template(
                'admin_aluno_novo.html', planos=planos, dados=dados, erro=mensagem,
            ), 400

        if not dados['nome'] or not dados['datanascimento'] or not dados['cpf']:
            return recusar('Informe nome, data de nascimento e CPF para matricular o aluno.')

        if len(somente_digitos(request.form.get('cpf'))) != 11:
            return recusar('Informe um CPF com 11 dígitos.')

        existente = AlunoDAO.buscar_por_cpf(dados['cpf'])
        if existente:
            # No painel administrativo dizer isso é o certo: o admin precisa saber que a
            # pessoa já está na base para não abrir um segundo cadastro para ela.
            return recusar(
                f'Este CPF já pertence ao cadastro de {existente.nome}. '
                'Abra o perfil dele em vez de criar um novo cadastro.'
            )

        if dados['email'] and not email_valido(dados['email']):
            return recusar('Informe um e-mail válido ou deixe o campo vazio.')

        if dados['email'] and AlunoDAO.buscar_por_email(dados['email']):
            return recusar('Este e-mail já está em uso por outro aluno.')

        try:
            nascimento = date.fromisoformat(dados['datanascimento'])
            if nascimento > date.today():
                raise ValueError
        except ValueError:
            return recusar('Informe uma data de nascimento válida, que não esteja no futuro.')
        for campo, limite in (('nome', 150), ('email', 150), ('telefone', 20),
                              ('graduacao', 80), ('descricao', 255)):
            if len(dados[campo]) > limite:
                return recusar(f'O campo {campo} deve ter no máximo {limite} caracteres.')
        try:
            plano_id = int(dados['plano_id']) if dados['plano_id'] else None
        except ValueError:
            return recusar('Selecione um plano válido.')
        plano = PlanoDAO.buscar_por_id(plano_id) if plano_id is not None else None
        if dados['plano_id'] and not plano:
            return recusar('Selecione um plano válido.')

        if dados['gerar_mensalidade'] and not plano:
            return recusar('Escolha um plano para lançar a primeira mensalidade.')

        try:
            aluno = AlunoDAO.criar_pelo_admin(
                nome=dados['nome'], cpf=dados['cpf'], datanascimento=dados['datanascimento'],
                telefone=dados['telefone'] or None, email=dados['email'] or None,
                descricao=dados['descricao'] or None, graduacao=dados['graduacao'] or None,
                plano_id=plano.id if plano else None,
            )
        except IntegrityError:
            db.session.rollback()
            return recusar('Não foi possível cadastrar: verifique se o CPF ou o e-mail já estão em uso.')

        if plano and dados['gerar_mensalidade']:
            # Mesma porta usada pelo aluno ao contratar um plano: ela revalida tudo
            # contra o banco e reaproveita uma cobrança aberta em vez de duplicá-la.
            PagamentoDAO.contratar_plano(
                aluno=aluno, plano=plano, acao=ACAO_CONTRATAR, ator=session.get('usuario'),
            )
            flash(f'{aluno.nome} foi matriculado e a primeira mensalidade já foi lançada.', 'sucesso')
        else:
            flash(f'{aluno.nome} foi matriculado. Lance as mensalidades por aqui.', 'sucesso')

        return redirect(f'/admin/usuario/{aluno.cpf}')

    return render_template('admin_aluno_novo.html', planos=planos, dados={})


@admin_bp.route("/admin/usuario/<cpf>/convite", methods=["POST"])
def enviar_convite_acesso(cpf):
    """Envia ao aluno o link de uso único que transforma o cadastro numa conta.

    O convite vai sempre para o e-mail gravado no cadastro. O admin pode registrar um
    e-mail aqui quando ainda não houver um, e é esse registro - feito por quem já tem
    autoridade sobre o cadastro - que passa a valer como canal de confirmação.
    """
    if not usuario_e_admin():
        return redirect('/login')

    aluno = _aluno_do_cpf_ou_painel(cpf)
    if not aluno:
        return redirect('/admin')

    if aluno.acesso_ativado:
        flash('Este aluno já tem acesso ativado. Para trocar a senha, use "Esqueci minha senha".', 'erro')
        return redirect(f'/admin/usuario/{cpf}')

    email = (request.form.get('email') or '').strip().lower() or aluno.email
    if not email:
        flash('Informe o e-mail do aluno para enviar o convite de acesso.', 'erro')
        return redirect(f'/admin/usuario/{cpf}')

    em_uso = AlunoDAO.buscar_por_email(email)
    if em_uso and em_uso.id != aluno.id:
        flash('Este e-mail já está em uso por outro aluno.', 'erro')
        return redirect(f'/admin/usuario/{cpf}')

    aluno.email = email
    try:
        convites.enviar(aluno)
    except convites.ConviteIndisponivel as erro:
        flash(str(erro), 'erro')
        return redirect(f'/admin/usuario/{cpf}')

    flash(f'Convite de acesso enviado para {email}. O link vale por 7 dias.', 'sucesso')
    return redirect(f'/admin/usuario/{cpf}')


@admin_bp.route("/admin/usuario/<cpf>/convite/revogar", methods=["POST"])
def revogar_convite_acesso(cpf):
    if not usuario_e_admin():
        return redirect('/login')

    aluno = _aluno_do_cpf_ou_painel(cpf)
    if not aluno:
        return redirect('/admin')

    if aluno.convite_pendente:
        convites.descartar(aluno)
        db.session.commit()
        flash('Convite cancelado. O link enviado deixou de funcionar.', 'sucesso')
    else:
        flash('Não há convite pendente para cancelar.', 'erro')

    return redirect(f'/admin/usuario/{cpf}')


@admin_bp.route("/admin/usuario/<cpf>", methods=["GET", "POST"])
def detalhes_usuario(cpf):
    if not usuario_e_admin():
        return redirect('/login')

    aluno = AlunoDAO.buscar_por_cpf(cpf)

    if not aluno:
        return redirect('/admin')

    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        login = (request.form.get("login") or "").strip()

        # Usuário e e-mail só são obrigatórios para quem tem conta: é por eles que o
        # aluno entra e recebe os links de recuperação. Um cadastro de balcão pode
        # continuar sem os dois sem deixar de ser gerenciável.
        if aluno.acesso_ativado and not (email and login):
            flash('Contas com acesso ativado precisam de nome de usuário e e-mail.', 'erro')
            return redirect(f'/admin/usuario/{cpf}')

        if (email and not email_valido(email)) or len(login) > 50:
            flash('Informe um e-mail válido e um usuário com até 50 caracteres.', 'erro')
            return redirect(f'/admin/usuario/{cpf}')

        if email and Aluno.query.filter(Aluno.email == email, Aluno.id != aluno.id).first():
            flash('Este e-mail já está em uso por outro aluno.', 'erro')
            return redirect(f'/admin/usuario/{cpf}')

        if login and Aluno.query.filter(Aluno.login == login, Aluno.id != aluno.id).first():
            flash('Este nome de usuário já está em uso por outro aluno.', 'erro')
            return redirect(f'/admin/usuario/{cpf}')

        dados_atualizados = {
            'nome': request.form.get("nome"),
            'login': login,
            'datanascimento': request.form.get("datanascimento"),
            'email': email,
            'telefone': formatar_telefone(request.form.get("telefone")),
            'plano_id': request.form.get("plano_id"),
            'descricao': request.form.get('descricao'),
            'graduacao': request.form.get('graduacao'),
        }

        if not AlunoDAO.atualizar_dados_completos(cpf, dados_atualizados):
            flash('Não foi possível salvar: verifique o plano selecionado.', 'erro')
            return redirect(f'/admin/usuario/{cpf}')

        return redirect('/admin')

    PagamentoDAO.efetivar_mudancas_por_prazo(aluno)
    planos = PlanoDAO.listar_todos()
    pagamentos = PagamentoDAO.listar_por_aluno(aluno.id)
    solicitacao = SolicitacaoPlanoDAO.pendente_do_aluno(aluno.id)
    return render_template(
        "dt_aluno.html", u=aluno, planos=planos, pagamentos=pagamentos,
        situacao=regras_plano.situacao_plano(aluno, pagamentos, solicitacao_mudanca=solicitacao),
        solicitacoes=SolicitacaoPlanoDAO.listar_do_aluno(aluno.id),
        rotulo_status=rotulo_status, formatar_competencia=formatar_competencia,
    )


@admin_bp.route("/admin/usuario/<cpf>/foto", methods=["POST"])
def enviar_foto_aluno(cpf):
    if not usuario_e_admin():
        return redirect('/login')

    aluno = AlunoDAO.buscar_por_cpf(cpf)
    if not aluno:
        flash('Aluno não encontrado.', 'erro')
        return redirect('/admin')

    arquivo = request.files.get('foto')
    if not arquivo or not arquivo.filename:
        flash('Selecione uma imagem para enviar.', 'erro')
        return redirect(f'/admin/usuario/{cpf}')

    try:
        nome_arquivo = salvar_foto_perfil(arquivo.read())
    except ArquivoInvalido as erro:
        flash(str(erro), 'erro')
        return redirect(f'/admin/usuario/{cpf}')

    foto_antiga = aluno.foto_arquivo
    AlunoDAO.definir_foto(aluno.id, nome_arquivo)
    if foto_antiga:
        remover_arquivo(foto_antiga, subpasta='fotos')

    flash('Foto do aluno atualizada com sucesso.', 'sucesso')
    return redirect(f'/admin/usuario/{cpf}')


@admin_bp.route("/admin/usuario/<cpf>/foto/remover", methods=["POST"])
def remover_foto_aluno(cpf):
    if not usuario_e_admin():
        return redirect('/login')

    aluno = AlunoDAO.buscar_por_cpf(cpf)
    if not aluno:
        flash('Aluno não encontrado.', 'erro')
        return redirect('/admin')

    if aluno.foto_arquivo:
        remover_arquivo(aluno.foto_arquivo, subpasta='fotos')
        AlunoDAO.definir_foto(aluno.id, None)
        flash('Foto do aluno removida.', 'sucesso')

    return redirect(f'/admin/usuario/{cpf}')


@admin_bp.route("/admin/usuario/<cpf>/pagamentos", methods=["POST"])
def cadastrar_pagamento(cpf):
    if not usuario_e_admin():
        return redirect('/login')

    aluno = AlunoDAO.buscar_por_cpf(cpf)
    plano = PlanoDAO.buscar_por_id(request.form.get('plano_id'))

    valor = request.form.get('valor')
    vencimento = request.form.get('vencimento')
    status = request.form.get('status')
    forma_pagamento = request.form.get('forma_pagamento')
    data_pagamento = request.form.get('data_pagamento')
    competencia = (request.form.get('competencia') or '').strip() or None
    observacao = (request.form.get('observacao') or '').strip() or None

    if aluno and plano and valor and vencimento:
        novo_pagamento = Pagamento(
            aluno_id=aluno.id,
            plano_id=plano.id,
            valor=float(valor),
            vencimento=date.fromisoformat(vencimento),
            status=status,
            forma_pagamento=forma_pagamento if forma_pagamento else None,
            data_pagamento=date.fromisoformat(data_pagamento) if data_pagamento else None,
            competencia=competencia,
        )
        if status != 'pendente':
            # Lançamento já nasce decidido pelo admin (dinheiro/transferência/ajuste) -
            # separa claramente de uma cobrança Pix, que é sempre provider='mercado_pago'.
            novo_pagamento.provider = 'manual'

        PagamentoDAO.salvar(novo_pagamento)
        # Um lançamento já pago abre o período de acesso; qualquer outro status não.
        # A vigência parte da data informada pelo admin, mas nunca sobrepõe um período
        # já pago - lançar o mês seguinte em dinheiro soma 30 dias ao que existe.
        if novo_pagamento.status == 'pago':
            PagamentoDAO.garantir_vigencia(
                novo_pagamento, referencia=novo_pagamento.data_pagamento or novo_pagamento.vencimento,
            )
        PagamentoDAO.registrar_evento(
            novo_pagamento.id, 'manual_registrado',
            detalhe=observacao or f'Mensalidade lançada manualmente pelo admin ({forma_pagamento or "sem forma informada"}).',
            ator=session.get('usuario'),
        )
        # A situação do aluno é sempre recalculada a partir das mensalidades - nunca
        # escrita a partir do formulário, para não voltar a divergir do histórico.
        PagamentoDAO.sincronizar_situacao_do_aluno(aluno)

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
    status_antes = pagamento.status

    PagamentoDAO.atualizar_status(pagamento_id, status, forma_pagamento)
    if status != status_antes:
        PagamentoDAO.registrar_evento(
            pagamento.id, 'status_alterado_admin',
            detalhe=f'Status alterado manualmente: {rotulo_status(status_antes)} → {rotulo_status(status)}.',
            ator=session.get('usuario'),
        )

    return redirect(f'/admin/usuario/{pagamento.aluno.cpf}')


@admin_bp.route("/admin/pagamentos/<int:pagamento_id>/comprovante-manual/aprovar", methods=["POST"])
def aprovar_comprovante_manual(pagamento_id):
    if not usuario_e_admin():
        return redirect('/login')

    pagamento = PagamentoDAO.buscar_por_id(pagamento_id)
    if not pagamento:
        flash('Mensalidade não encontrada.', 'erro')
        return redirect('/admin/financeiro')

    if pagamento.status != 'em_analise':
        flash('Esta mensalidade não está com um comprovante em análise.', 'erro')
        return redirect('/admin/financeiro')

    observacao = (request.form.get('observacao') or '').strip() or None
    data_pagamento = _data_do_form(request.form.get('data_pagamento'))
    forma_pagamento = request.form.get('forma_pagamento') or 'transferencia'

    PagamentoDAO.aprovar_comprovante_manual(
        pagamento, admin_login=session.get('usuario'), observacao=observacao,
        data_pagamento=data_pagamento, forma_pagamento=forma_pagamento,
    )
    flash('Comprovante aprovado - mensalidade marcada como paga.', 'sucesso')
    return redirect('/admin/financeiro')


@admin_bp.route("/admin/pagamentos/<int:pagamento_id>/comprovante-manual/rejeitar", methods=["POST"])
def rejeitar_comprovante_manual(pagamento_id):
    if not usuario_e_admin():
        return redirect('/login')

    pagamento = PagamentoDAO.buscar_por_id(pagamento_id)
    if not pagamento:
        flash('Mensalidade não encontrada.', 'erro')
        return redirect('/admin/financeiro')

    if pagamento.status != 'em_analise':
        flash('Esta mensalidade não está com um comprovante em análise.', 'erro')
        return redirect('/admin/financeiro')

    observacao = (request.form.get('observacao') or '').strip() or None
    PagamentoDAO.rejeitar_comprovante_manual(pagamento, admin_login=session.get('usuario'), observacao=observacao)
    flash('Comprovante rejeitado. O aluno poderá enviar um novo ou pagar via Pix.', 'sucesso')
    return redirect('/admin/financeiro')


@admin_bp.route("/admin/aluno/<int:aluno_id>/mudanca-plano/<int:solicitacao_id>/cancelar", methods=["POST"])
def cancelar_mudanca_plano_admin(aluno_id, solicitacao_id):
    """A administração pode cancelar um pedido de troca ainda não aplicado.

    Não existe aprovação manual para agendar a troca: contratar plano neste sistema já é
    auto-serviço do aluno, e a mudança agendada não gera cobrança nem libera benefício
    nenhum por si só. O admin entra apenas onde já entrava - revisando as mensalidades.
    """
    if not usuario_e_admin():
        return redirect('/login')

    aluno = AlunoDAO.buscar_por_id(aluno_id)
    solicitacao = SolicitacaoPlanoDAO.buscar_por_id(solicitacao_id)
    if not aluno or not solicitacao or solicitacao.aluno_id != aluno.id:
        flash('Solicitação de mudança não encontrada.', 'erro')
        return redirect('/admin')

    observacao = (request.form.get('observacao') or '').strip() or None
    if SolicitacaoPlanoDAO.cancelar(solicitacao, ator=session.get('usuario'), observacao=observacao):
        flash('Solicitação de mudança de plano cancelada.', 'sucesso')
    else:
        flash('Esta solicitação não está mais pendente.', 'erro')

    return redirect(f'/admin/usuario/{aluno.cpf}')


def _data_do_form(valor):
    try:
        return date.fromisoformat(valor) if valor else None
    except ValueError:
        return None


@admin_bp.route("/admin/financeiro")
def painel_financeiro():
    if not usuario_e_admin():
        return redirect('/login')

    filtros = {
        'inicio': _data_do_form(request.args.get('inicio')),
        'fim': _data_do_form(request.args.get('fim')),
        'turma_id': request.args.get('turma_id', type=int),
        'plano_id': request.args.get('plano_id', type=int),
        'forma_pagamento': request.args.get('forma_pagamento') or None,
        'status': request.args.get('status') or None,
        'busca_aluno': (request.args.get('busca_aluno') or '').strip() or None,
    }

    # Uma única data para toda a requisição: indicadores e tabela julgam o vencimento
    # pelo mesmo "hoje", mesmo que a página seja aberta na virada da meia-noite.
    hoje = date.today()

    totais = PagamentoDAO.totais_periodo(inicio=filtros['inicio'], fim=filtros['fim'], hoje=hoje)
    pagina = PagamentoDAO.listar_paginado(
        pagina=request.args.get('pagina', type=int) or 1, hoje=hoje, **filtros,
    )

    return render_template(
        "financeiro.html",
        totais=totais,
        pagamentos=pagina.itens,
        pagina=pagina,
        turmas=TurmaDAO.listar_todas(),
        planos=PlanoDAO.listar_todos(),
        filtros=request.args,
        rotulo_status=rotulo_status,
        formatar_competencia=formatar_competencia,
    )


def _situacao_do_aluno(aluno, pagamentos=None):
    if pagamentos is None:
        pagamentos = PagamentoDAO.listar_por_aluno(aluno.id)
    return regras_plano.situacao_plano(aluno, pagamentos)


def _situacoes_dos_ativos():
    """Situação de todos os alunos ativos com UMA consulta de mensalidades."""
    alunos = [a for a in AlunoDAO.listar_todos() if a.esta_ativo]
    mapa = PagamentoDAO.mapa_por_aluno([a.id for a in alunos])
    return [(aluno, _situacao_do_aluno(aluno, mapa.get(aluno.id, []))) for aluno in alunos]


def _esta_inadimplente(aluno, situacao=None):
    """Quem realmente deve receber cobrança: nem quem está com o plano ativo, nem quem
    já pagou e aguarda uma decisão (comprovante em análise, pagamento processando).
    Cobrar essas pessoas era pedir um segundo pagamento pelo mesmo período."""
    return regras_plano.esta_inadimplente(situacao or _situacao_do_aluno(aluno))


def _paragrafos_cobranca(aluno, situacao=None):
    """Texto da cobrança montado a partir da situação real, não de campos guardados:
    o valor e o período citados são os da mensalidade que está mesmo em aberto."""
    situacao = situacao or _situacao_do_aluno(aluno)
    cobranca = situacao.cobranca
    paragrafos = [
        f'Olá, {aluno.nome.split()[0]}.',
        'Identificamos uma pendência na sua mensalidade na Extreme Team.',
    ]
    plano = (cobranca.plano if cobranca else None) or situacao.plano
    if plano:
        valor = cobranca.valor if cobranca else plano.preco_plano
        paragrafos.append(f'Plano: {plano.nome_plano} — R$ {f"{valor:.2f}".replace(".", ",")}')
    if cobranca and cobranca.vencimento:
        paragrafos.append(f'Vencimento: {cobranca.vencimento.strftime("%d/%m/%Y")}')
    elif situacao.valido_ate:
        paragrafos.append(f'Seu acesso foi pago até: {situacao.valido_ate.strftime("%d/%m/%Y")}')
    paragrafos.append('Regularize o quanto antes para continuar treinando sem interrupções. Qualquer dúvida, fale com a nossa administração.')
    return paragrafos


def _chave_lote(assunto, mensagem):
    """Identidade de um aviso: o conteúdo MAIS o dia.

    Só o conteúdo não serve. Um aviso recorrente ("não vai ter treino amanhã") tem
    sempre o mesmo texto, e sem a data o segundo envio seria descartado em silêncio
    para sempre - com a tela ainda dizendo "enviado". A data protege contra o clique
    duplo e o recarregar da página, que é o que a idempotência precisa cobrir, sem
    bloquear o mesmo aviso numa outra ocasião.
    """
    material = f'{date.today().isoformat()}\n{assunto}\n{mensagem}'
    return hashlib.sha256(material.encode('utf-8')).hexdigest()[:32]


def _token_aviso():
    token = session.get('token_aviso')
    if not token:
        token = secrets.token_urlsafe(32)
        session['token_aviso'] = token
    return token


def _token_aviso_valido():
    token_formulario = request.form.get('token_aviso', '')
    token_sessao = session.get('token_aviso', '')
    return bool(token_sessao) and hmac.compare_digest(token_formulario, token_sessao)


@admin_bp.route("/admin/avisos", methods=["GET", "POST"])
def enviar_aviso():
    if not usuario_e_admin():
        return redirect('/login')

    if request.method == "POST":
        if not _token_aviso_valido():
            abort(400)

        assunto = (request.form.get('assunto') or '').strip()
        mensagem = (request.form.get('mensagem') or '').strip()
        destinatarios = request.form.get('destinatarios', 'todos')

        if not assunto or not mensagem:
            flash('Preencha o assunto e a mensagem do aviso.', 'erro')
            return redirect('/admin/avisos')

        ativos = _situacoes_dos_ativos()
        if destinatarios == 'inadimplentes':
            ativos = [(a, s) for a, s in ativos if _esta_inadimplente(a, s)]
        # Cadastro de balcão pode não ter e-mail. Ele não entra na conta de destinatários
        # para o "X de Y" continuar dizendo a verdade sobre quem podia ser avisado.
        alunos = [aluno for aluno, _ in ativos if aluno.email]

        paragrafos = [linha.strip() for linha in mensagem.splitlines() if linha.strip()]
        # O envio sai da requisição: enfileirar é uma transação curta, entregar é da
        # fila. A chave inclui o conteúdo, então reenviar o MESMO aviso ao MESMO aluno
        # (recarregar a página, clicar duas vezes) não duplica, e um aviso novo passa.
        lote = _chave_lote(assunto, mensagem)
        enfileirados = sum(
            1 for aluno in alunos
            if fila_email.enfileirar(
                destinatario=aluno.email, nome_destinatario=aluno.nome,
                assunto=assunto, titulo=assunto, paragrafos=paragrafos,
                chave_idempotencia=f'aviso:{lote}:{aluno.id}',
            ) is not None
        )
        db.session.commit()
        fila_email.disparar()

        # "0 de 50" não é sucesso: quer dizer que este mesmo aviso já foi enfileirado
        # hoje. Sem dizer isso, a tela comemorava um envio que não vai acontecer.
        if enfileirados:
            mensagem = (
                f'Aviso na fila de envio para {enfileirados} de {len(alunos)} aluno(s). '
                'O envio continua em segundo plano.'
            )
            repetidos = len(alunos) - enfileirados
            if repetidos:
                mensagem += f' {repetidos} já tinha(m) recebido este aviso hoje.'
            flash(mensagem, 'sucesso')
        elif alunos:
            flash(
                'Este aviso, com este mesmo texto, já foi enviado hoje para todos os '
                'alunos. Altere o texto ou aguarde até amanhã para reenviar.',
                'erro',
            )
        else:
            flash('Nenhum aluno ativo com e-mail para receber este aviso.', 'erro')
        return redirect('/admin/avisos')

    ativos = _situacoes_dos_ativos()
    inadimplentes = [(a, s) for a, s in ativos if _esta_inadimplente(a, s)]
    # Quantos alunos DEVEM e quantos dá para AVISAR são números diferentes desde que o
    # cadastro de balcão existe. A tela mostra os dois para o total do botão bater com
    # o que o envio realmente alcança.
    # Abrir a tela também retoma a fila: se a thread morreu num restart, as linhas
    # pendentes voltam a ser processadas sem depender de um novo clique em "enviar".
    fila_email.disparar()

    return render_template(
        "admin_avisos.html",
        total_ativos=len(ativos),
        total_inadimplentes=len(inadimplentes),
        total_cobraveis=sum(1 for aluno, _ in inadimplentes if aluno.email),
        total_sem_email=sum(1 for aluno, _ in ativos if not aluno.email),
        fila_pendentes=fila_email.contar_pendentes(),
        fila_falhados=fila_email.contar_falhados(),
        token_aviso=_token_aviso(),
    )


@admin_bp.route("/admin/avisos/cobranca", methods=["POST"])
def cobrar_inadimplentes():
    if not usuario_e_admin():
        return redirect('/login')

    if not _token_aviso_valido():
        abort(400)

    # A situação de cada aluno é calculada uma única vez e reaproveitada no texto do
    # e-mail, para o valor citado ser exatamente o da mensalidade que está em aberto.
    devedores = [(aluno, situacao) for aluno, situacao in _situacoes_dos_ativos()
                 if aluno.email and _esta_inadimplente(aluno, situacao)]

    # A chave é por aluno e por dia: o mesmo devedor não recebe duas cobranças na mesma
    # data, mesmo que a administração clique de novo, e amanhã a cobrança volta a poder
    # sair se a pendência continuar.
    hoje = date.today().isoformat()
    enfileirados = sum(
        1 for aluno, situacao in devedores
        if fila_email.enfileirar(
            destinatario=aluno.email, nome_destinatario=aluno.nome,
            assunto='Mensalidade pendente — Extreme Team',
            titulo='Sua mensalidade está pendente',
            paragrafos=_paragrafos_cobranca(aluno, situacao),
            chave_idempotencia=f'cobranca:{hoje}:{aluno.id}',
        ) is not None
    )
    db.session.commit()
    fila_email.disparar()

    ja_enviados = len(devedores) - enfileirados
    if enfileirados:
        mensagem = (
            f'Cobrança na fila de envio para {enfileirados} de {len(devedores)} '
            f'aluno(s) inadimplente(s).'
        )
        if ja_enviados:
            mensagem += f' {ja_enviados} já tinha(m) recebido a cobrança hoje.'
        flash(mensagem, 'sucesso')
    elif devedores:
        flash(
            f'Os {len(devedores)} inadimplente(s) já receberam a cobrança hoje. '
            'Nada foi reenviado.',
            'erro',
        )
    else:
        flash('Nenhum aluno inadimplente com e-mail para cobrar.', 'sucesso')
    return redirect('/admin/avisos')


@admin_bp.route("/admin/usuario/<cpf>/cobrar", methods=["POST"])
def cobrar_mensalidade(cpf):
    if not usuario_e_admin():
        return redirect('/login')

    aluno = AlunoDAO.buscar_por_cpf(cpf)
    if not aluno:
        flash('Aluno não encontrado.', 'erro')
        return redirect('/admin')

    if not aluno.email:
        flash('Este aluno não tem e-mail cadastrado. Registre um e-mail para enviar a cobrança.', 'erro')
        return redirect(f'/admin/usuario/{cpf}')

    situacao = _situacao_do_aluno(aluno)
    if not _esta_inadimplente(aluno, situacao):
        # Cobrar quem está com o plano ativo (ou aguardando análise) é justamente o que
        # levava o aluno a pagar duas vezes o mesmo período.
        flash('Este aluno não tem pendência: o plano está ativo ou o pagamento aguarda análise.', 'erro')
        return redirect(f'/admin/usuario/{cpf}')

    if enviar_email(
        aluno.email, aluno.nome, 'Mensalidade pendente — Extreme Team', 'Sua mensalidade está pendente',
        _paragrafos_cobranca(aluno, situacao),
    ):
        flash('Cobrança enviada por e-mail.', 'sucesso')
    else:
        flash('Não foi possível enviar o e-mail de cobrança.', 'erro')

    return redirect(f'/admin/usuario/{cpf}')
