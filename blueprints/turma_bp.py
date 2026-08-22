from datetime import date

from flask import Blueprint, abort, flash, redirect, render_template, request, session

from dao.matriculaDAO import MatriculaDAO
from dao.presencaDAO import PresencaDAO
from dao.professorDAO import ProfessorDAO
from dao.turmaDAO import TurmaDAO
from dao.usuarioDAO import AlunoDAO
from modelos.professor import Professor
from modelos.turma import Turma
from servicos.autorizacao import admin_requerido, professor_ou_admin_requerido

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

    if Professor.query.filter_by(login=login).first():
        flash('Já existe um professor com esse login.', 'erro')
        return redirect('/admin/turmas')

    ProfessorDAO.salvar(Professor(nome=nome, login=login, senha=senha))
    flash('Professor cadastrado com sucesso.', 'sucesso')
    return redirect('/admin/turmas')


@turma_bp.route('/admin/professores/<int:professor_id>/remover', methods=['POST'])
@admin_requerido
def remover_professor(professor_id):
    resultado = ProfessorDAO.remover(professor_id)
    if resultado is True:
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
    alunos_disponiveis = [a for a in AlunoDAO.listar_todos() if a.id not in ids_matriculados] if eh_admin else []

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
