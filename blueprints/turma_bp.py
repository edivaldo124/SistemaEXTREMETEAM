from datetime import date
from pathlib import Path

from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, send_file, session, url_for
from sqlalchemy.exc import SQLAlchemyError

from config import db
from dao.matriculaDAO import MatriculaDAO
from dao.presencaDAO import PresencaDAO
from dao.professorDAO import ProfessorDAO
from dao.turmaDAO import TurmaDAO
from dao.usuarioDAO import AlunoDAO
from modelos.professor import Professor
from modelos.turma import Turma
from servicos.autorizacao import admin_requerido, professor_ou_admin_requerido
from servicos.armazenamento import (
    ArquivoInvalido, TAMANHO_MAX_FOTO, caminho_arquivo, remover_arquivo, salvar_foto_perfil,
)
from servicos.contatos import validar_email, validar_instagram, validar_whatsapp
from servicos.senhas import erro_validacao_senha

turma_bp = Blueprint('turma_blueprint', __name__)

DIA_POR_INDICE = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab', 'Dom']


@turma_bp.route('/admin/turmas')
@admin_requerido
def gerenciar_turmas():
    return render_template(
        'turmas.html',
        turmas=TurmaDAO.listar_todas(),
        professores=ProfessorDAO.listar_todos(),
    )


@turma_bp.route('/admin/professores', methods=['POST'])
@admin_requerido
def cadastrar_professor():
    nome = (request.form.get('nome') or '').strip()
    login = (request.form.get('login') or '').strip()
    senha = request.form.get('senha') or ''

    if not all([nome, login, senha]):
        flash('Preencha nome, login e senha do professor.', 'erro')
        return redirect('/admin/turmas')

    erro_senha = erro_validacao_senha(senha, login)
    if erro_senha:
        flash(erro_senha, 'erro')
        return redirect('/admin/turmas')

    if Professor.query.filter_by(login=login).first():
        flash('Já existe um professor com esse login.', 'erro')
        return redirect('/admin/turmas')

    ProfessorDAO.salvar(Professor(nome=nome, login=login, senha=senha))
    flash('Professor cadastrado com sucesso.', 'sucesso')
    return redirect('/admin/turmas')


_CAMPOS_PERFIL = {
    'nome_publico': ('Nome de apresentação', 150),
    'modalidades': ('Modalidades', 200),
    'biografia': ('Apresentação', 3000),
    'formacao': ('Formação e graduações', 2000),
}
_VISIBILIDADE_PERFIL = ('perfil_publico', 'exibir_instagram', 'exibir_email', 'exibir_whatsapp')


@turma_bp.route('/admin/professores/<int:professor_id>/editar', methods=['GET', 'POST'])
@admin_requerido
def editar_professor(professor_id):
    professor = ProfessorDAO.buscar_por_id(professor_id)
    if not professor:
        abort(404)

    campos = (*_CAMPOS_PERFIL, 'instagram', 'email_publico', 'whatsapp', *_VISIBILIDADE_PERFIL)
    valores = {campo: getattr(professor, campo) for campo in campos}
    if professor.whatsapp:
        valores['whatsapp'] = '+' + professor.whatsapp
    if request.method == 'POST':
        valores = {campo: (request.form.get(campo) or '').strip() for campo in _CAMPOS_PERFIL}
        valores.update({campo: (request.form.get(campo) or '').strip()
                        for campo in ('instagram', 'email_publico', 'whatsapp')})
        valores.update({campo: request.form.get(campo) == 'on' for campo in _VISIBILIDADE_PERFIL})
        foto_nova = None
        try:
            for campo, (rotulo, limite) in _CAMPOS_PERFIL.items():
                if len(valores[campo]) > limite:
                    raise ValueError(f'{rotulo}: use no máximo {limite} caracteres.')
            dados = {campo: valores[campo] or None for campo in _CAMPOS_PERFIL}
            dados.update({
                'instagram': validar_instagram(valores['instagram']),
                'email_publico': validar_email(valores['email_publico']),
                'whatsapp': validar_whatsapp(valores['whatsapp']),
            })
            dados.update({campo: valores[campo] for campo in _VISIBILIDADE_PERFIL})
            arquivo = request.files.get('foto')
            remover_foto = request.form.get('remover_foto') == 'on'
            if arquivo and arquivo.filename and remover_foto:
                raise ValueError('Escolha uma nova foto ou marque remover foto, uma opção de cada vez.')
            if arquivo and arquivo.filename:
                foto_nova = salvar_foto_perfil(arquivo.read(TAMANHO_MAX_FOTO + 1), subpasta='professores')
            foto_anterior = professor.foto_arquivo
            for campo, valor in dados.items():
                setattr(professor, campo, valor)
            if foto_nova or remover_foto:
                professor.foto_arquivo = foto_nova
            db.session.commit()
        except (ValueError, ArquivoInvalido) as exc:
            flash(str(exc), 'erro')
            return render_template('professor_editar.html', professor=professor, valores=valores), 400
        except (SQLAlchemyError, OSError):
            db.session.rollback()
            if foto_nova:
                remover_arquivo(foto_nova, subpasta='professores')
            current_app.logger.exception('Falha ao salvar perfil do professor %s', professor_id)
            flash('Não foi possível salvar o perfil. Tente novamente.', 'erro')
            return render_template('professor_editar.html', professor=professor, valores=valores), 500
        if (foto_nova or remover_foto) and foto_anterior:
            remover_arquivo(foto_anterior, subpasta='professores')
        flash('Perfil do professor atualizado.', 'sucesso')
        return redirect(url_for('turma_blueprint.editar_professor', professor_id=professor.id))

    return render_template('professor_editar.html', professor=professor, valores=valores)


@turma_bp.route('/professores/<int:professor_id>/foto')
def foto_professor(professor_id):
    professor = ProfessorDAO.buscar_por_id(professor_id)
    if not professor:
        abort(404)
    proprio_professor = (session.get('tipo_usuario') == 'professor'
                        and session.get('professor_id') == professor.id)
    if not professor.perfil_publico and session.get('tipo_usuario') != 'admin' and not proprio_professor:
        abort(404)
    caminho = caminho_arquivo(professor.foto_arquivo, subpasta='professores')
    if not caminho:
        abort(404)
    resposta = send_file(Path(caminho).resolve(), mimetype='image/jpeg', conditional=False)
    resposta.headers['Cache-Control'] = 'private, no-store'
    resposta.headers['X-Content-Type-Options'] = 'nosniff'
    return resposta


@turma_bp.route('/admin/professores/<int:professor_id>/remover', methods=['POST'])
@admin_requerido
def remover_professor(professor_id):
    professor = ProfessorDAO.buscar_por_id(professor_id)
    foto_anterior = professor.foto_arquivo if professor else None
    resultado = ProfessorDAO.remover(professor_id)
    if resultado is True:
        if foto_anterior:
            remover_arquivo(foto_anterior, subpasta='professores')
        flash('Professor removido com sucesso.', 'sucesso')
    elif resultado is None:
        flash('Professor não encontrado.', 'erro')
    else:
        flash('Não foi possível remover: existem turmas vinculadas a esse professor.', 'erro')
    return redirect('/admin/turmas')


@turma_bp.route('/admin/turmas/cadastrar', methods=['POST'])
@admin_requerido
def cadastrar_turma():
    nome = (request.form.get('nome') or '').strip()
    dias = request.form.getlist('dias_semana')
    horario = (request.form.get('horario') or '').strip()
    professor_id = request.form.get('professor_id')
    limite_alunos = request.form.get('limite_alunos') or 20

    if not all([nome, dias, horario, professor_id]):
        flash('Preencha todos os campos da turma.', 'erro')
        return redirect('/admin/turmas')

    turma = Turma(
        nome=nome,
        dias_semana=','.join(dias),
        horario=horario,
        professor_id=int(professor_id),
        limite_alunos=int(limite_alunos),
    )
    TurmaDAO.salvar(turma)
    flash('Turma cadastrada com sucesso.', 'sucesso')
    return redirect('/admin/turmas')


@turma_bp.route('/admin/turmas/<int:turma_id>/remover', methods=['POST'])
@admin_requerido
def remover_turma(turma_id):
    resultado = TurmaDAO.remover(turma_id)
    if resultado is True:
        flash('Turma removida com sucesso.', 'sucesso')
    elif resultado is None:
        flash('Turma não encontrada.', 'erro')
    else:
        flash('Não foi possível remover: existem matrículas ou presenças vinculadas.', 'erro')
    return redirect('/admin/turmas')


def _turma_ou_404(turma_id):
    turma = TurmaDAO.buscar_por_id(turma_id)
    if not turma:
        abort(404)
    return turma


def _acesso_permitido(turma):
    if session.get('tipo_usuario') == 'admin':
        return True
    return session.get('tipo_usuario') == 'professor' and session.get('professor_id') == turma.professor_id


@turma_bp.route('/turmas/<int:turma_id>')
@professor_ou_admin_requerido
def detalhe_turma(turma_id):
    turma = _turma_ou_404(turma_id)
    if not _acesso_permitido(turma):
        abort(403)

    data_str = request.args.get('data') or date.today().isoformat()
    data_aula = date.fromisoformat(data_str)

    matriculados = [m.aluno for m in MatriculaDAO.listar_por_turma(turma_id)]
    presencas = {p.aluno_id: p.presente for p in PresencaDAO.listar_por_turma_e_data(turma_id, data_aula)}
    dia_valido = DIA_POR_INDICE[data_aula.weekday()] in turma.lista_dias

    eh_admin = session.get('tipo_usuario') == 'admin'
    ids_matriculados = {a.id for a in matriculados}
    alunos_disponiveis = [a for a in AlunoDAO.listar_todos() if a.id not in ids_matriculados and a.esta_ativo] if eh_admin else []

    return render_template(
        'turma.html',
        turma=turma,
        matriculados=matriculados,
        alunos_disponiveis=alunos_disponiveis,
        presencas=presencas,
        data_aula=data_aula,
        dia_valido=dia_valido,
        eh_admin=eh_admin,
    )


@turma_bp.route('/turmas/<int:turma_id>/matricular', methods=['POST'])
@admin_requerido
def matricular_aluno(turma_id):
    turma = _turma_ou_404(turma_id)
    aluno_id = request.form.get('aluno_id')

    if not aluno_id:
        flash('Selecione um aluno para matricular.', 'erro')
        return redirect(f'/turmas/{turma_id}')

    aluno = AlunoDAO.buscar_por_id(int(aluno_id))
    if not aluno or not aluno.esta_ativo:
        flash('Este aluno não pode ser matriculado (cadastro pendente, recusado ou desativado).', 'erro')
        return redirect(f'/turmas/{turma_id}')

    if MatriculaDAO.contar_por_turma(turma_id) >= turma.limite_alunos:
        flash('A turma já atingiu o limite de alunos.', 'erro')
        return redirect(f'/turmas/{turma_id}')

    if MatriculaDAO.matricular(int(aluno_id), turma_id):
        flash('Aluno matriculado com sucesso.', 'sucesso')
    else:
        flash('Este aluno já está matriculado nessa turma.', 'erro')
    return redirect(f'/turmas/{turma_id}')


@turma_bp.route('/turmas/<int:turma_id>/desmatricular/<int:aluno_id>', methods=['POST'])
@admin_requerido
def desmatricular_aluno(turma_id, aluno_id):
    _turma_ou_404(turma_id)
    MatriculaDAO.desmatricular(aluno_id, turma_id)
    flash('Aluno removido da turma.', 'sucesso')
    return redirect(f'/turmas/{turma_id}')


@turma_bp.route('/turmas/<int:turma_id>/presenca', methods=['POST'])
@professor_ou_admin_requerido
def registrar_presenca(turma_id):
    turma = _turma_ou_404(turma_id)
    if not _acesso_permitido(turma):
        abort(403)

    data_aula = date.fromisoformat(request.form.get('data_aula'))

    # RN05: só registra presença em turma e data de aula existentes (dia em que a turma efetivamente ocorre).
    if DIA_POR_INDICE[data_aula.weekday()] not in turma.lista_dias:
        flash('Essa turma não tem aula nesse dia da semana.', 'erro')
        return redirect(f'/turmas/{turma_id}?data={data_aula.isoformat()}')

    matriculados = MatriculaDAO.listar_por_turma(turma_id)
    presencas_por_aluno = {
        m.aluno_id: request.form.get(f'presente_{m.aluno_id}') == 'on'
        for m in matriculados
    }

    PresencaDAO.registrar_lote(turma_id, data_aula, presencas_por_aluno)
    flash('Presença registrada com sucesso.', 'sucesso')
    return redirect(f'/turmas/{turma_id}?data={data_aula.isoformat()}')


@turma_bp.route('/professor')
def painel_professor():
    if session.get('tipo_usuario') != 'professor':
        return redirect('/login')

    professor = ProfessorDAO.buscar_por_id(session['professor_id'])
    return render_template('pgProfessor.html', professor=professor, turmas=professor.turmas if professor else [])
