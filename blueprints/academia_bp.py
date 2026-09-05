from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy.exc import SQLAlchemyError

from config import db
from modelos.academia import Academia
from servicos.autorizacao import admin_requerido
from servicos.contatos import validar_email, validar_instagram, validar_whatsapp

academia_bp = Blueprint('academia', __name__)


@academia_bp.route('/admin/academia', methods=['GET', 'POST'])
@admin_requerido
def configuracoes():
    academia = db.session.get(Academia, 1)
    if request.method == 'POST':
        dados = {campo: request.form.get(campo, '').strip() for campo in (
            'instagram', 'email', 'whatsapp', 'endereco', 'complemento', 'horarios',
        )}
        try:
            normalizados = dict(dados)
            normalizados['instagram'] = validar_instagram(dados['instagram'])
            normalizados['email'] = validar_email(dados['email'])
            normalizados['whatsapp'] = validar_whatsapp(dados['whatsapp'])
            for campo, limite, rotulo in [('endereco', 300, 'O endereço'), ('complemento', 150, 'O complemento'), ('horarios', 1000, 'Os horários')]:
                if len(dados[campo]) > limite:
                    raise ValueError(f'{rotulo} deve ter até {limite} caracteres.')
                normalizados[campo] = dados[campo] or None
            if dados['complemento'] and not dados['endereco']:
                raise ValueError('Preencha o endereço antes de adicionar um complemento.')
        except ValueError as exc:
            flash(str(exc), 'erro')
            return render_template('admin_academia.html', dados=dados), 400

        academia = academia or Academia(id=1)
        for campo, valor in normalizados.items():
            setattr(academia, campo, valor)
        try:
            db.session.add(academia)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            flash('Não foi possível salvar. Tente novamente.', 'erro')
            return render_template('admin_academia.html', dados=dados), 500
        flash('Informações da academia atualizadas.', 'sucesso')
        return redirect(url_for('academia.configuracoes'))
    return render_template('admin_academia.html', dados=academia)
