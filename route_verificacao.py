
@auth_bp.route("/cadastro/verificar/<token>")
def verificar_email_cadastro(token):
    aluno = _aluno_por_token(Aluno.token_verificacao_hash, token)
    
    if not aluno:
        flash("Link de verificação inválido ou já utilizado.", "erro")
        return redirect(url_for('auth.login'))
        
    if aluno.token_verificacao_expira and aluno.token_verificacao_expira < datetime.utcnow():
        flash("Este link de verificação expirou. Por favor, solicite um novo.", "erro")
        return redirect(url_for('auth.login'))
        
    aluno.email_verificado = True
    aluno.token_verificacao_hash = None
    aluno.token_verificacao_expira = None
    db.session.commit()
    
    # Agora que o email foi verificado, avisamos o admin
    admin_email = os.environ.get('ADMIN_EMAIL')
    if admin_email:
        try:
            link_admin = url_publica('admin_blueprint.painel_adm')
            fila_email.enfileirar_transacional(
                f'cadastro-aviso-admin:{aluno.id}',
                destinatario=admin_email, nome_destinatario='Administração',
                assunto='Novo cadastro aguardando aprovação — Extreme Team', titulo='Novo cadastro pendente',
                paragrafos=[
                    f'O aluno {aluno.nome} confirmou o e-mail e seu cadastro está aguardando aprovação.',
                    f'E-mail: {aluno.email}',
                    f'Telefone: {aluno.telefone}',
                    'Acesse o painel administrativo para aprovar ou recusar o cadastro.',
                ],
                link_url=link_admin,
                link_texto='Abrir painel administrativo',
            )
        except URLPublicaInvalida:
            logger.error('APP_BASE_URL inválida; aviso de novo cadastro não foi enviado ao administrador.')
            
    flash("E-mail verificado com sucesso! Seu cadastro já foi enviado para análise da administração.", "sucesso")
    return redirect(url_for('auth.login'))
