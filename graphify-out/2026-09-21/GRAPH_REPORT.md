# Graph Report - SistemaEXTREMETEAM  (2026-09-21)

## Corpus Check
- 132 files · ~193,896 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1756 nodes · 4480 edges · 118 communities (108 shown, 10 thin omitted)
- Extraction: 80% EXTRACTED · 20% INFERRED · 0% AMBIGUOUS · INFERRED: 917 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5ffc6e51`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- financeiroDAO.py
- Admin Dashboard Page
- Aluno
- test_plano_vigencia.py
- test_limites_pagamento.py
- test_mudanca_plano.py
- PagamentoDAO
- Reavaliação de segurança e desempenho — 12/09/2026
- SistemaEXTREMETEAM Project
- test_mercado_pago_servico.py
- test_mercado_pago_oauth.py
- Professor
- test_migracao_checkout.py
- checkout.js
- CLAUDE.md
- planos.py
- pix_bp.py
- logar_como_admin
- test_checkout_rotas.py
- checkout_bp.py
- pix.js
- config.py
- env.py
- pagamento.js
- c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py
- varredura.mjs
- 896e70afc9c5_adiciona_foto_e_graduacao_do_aluno_.py
- test_auditoria_seguranca.py
- MercadoPagoIndisponivel
- adm_bp.py
- test_datas_turma.py
- criar_aluno
- convites.py
- Academia
- pagamento_polling.test.cjs
- mercado_pago_conta.py
- criar_pagamento
- test_pix_rotas.py
- PagamentoEvento
- d9e2f6a14c80_contatos_academia_perfis_professores.py
- conftest.py
- botao_ocupado.test.cjs
- test_seguranca.py
- checkout_abertura.test.cjs
- filtros_financeiro.js
- gunicorn.conf.py
- ConfiguracaoInvalida
- fila_email.py
- test_migracao_cadastro_administrativo.py
- salvar_foto_perfil
- test_keep_alive.py
- test_email_gmail.py
- mercado_pago.py
- test_arranque_seguranca.py
- SolicitacaoMudancaPlano
- erro_validacao_senha
- servidor.py
- autorizacao.py
- pagina_cadastro
- gmail_conta.py
- credenciais.py
- shot.mjs
- test_financeiro_admin_painel.py
- usuario_bp.py
- Pagina
- _tem_limite
- e4b7c2a91d35_cadastro_administrativo_e_convite_de_acesso.py
- a1f0c3e75b92_schema_inicial.py
- Contrato do redesign — SistemaEXTREMETEAM
- _chave_da_conta
- Relatório de segurança — Sistema Extreme Team (17/09/2026)
- test_sessao_revogada.py
- test_matricula_valida_dados_no_servidor
- .bloquear_pendente_do_aluno
- test_fila_email_concorrencia_postgres.py
- Atualização de 19/09/2026 — correções aplicadas e nova varredura
- Severidade BAIXA
- pagina_perfil
- turma_bp.py
- Relatório de segurança — Sistema Extreme Team
- Severidade MÉDIA
- Severidade ALTA
- admin_requerido
- EmailPendente
- extreme.css
- keep_alive.py
- index.js
- formatar_competencia
- Flask App Service (compose)
- Aluno Detail/Admin Page
- Aluno Profile Page
- .listar_paginado
- _FakePaymentResource
- _convidar_cadastro_existente
- Login Page
- capturar_emails
- test_reenviar_um_aviso_que_desistiu_volta_a_enfileirar
- test_decodificacao_de_imagem_e_serializada_no_processo

## God Nodes (most connected - your core abstractions)
1. `PagamentoDAO` - 196 edges
2. `criar_pagamento()` - 141 edges
3. `criar_aluno()` - 129 edges
4. `logar_como_admin()` - 111 edges
5. `logar_como_aluno()` - 110 edges
6. `AlunoDAO` - 91 edges
7. `Aluno` - 59 edges
8. `MercadoPagoIndisponivel` - 41 edges
9. `Professor` - 35 edges
10. `_matricular()` - 34 edges

## Surprising Connections (you probably didn't know these)
- `Histórico de Mensalidades Section` --shares_data_with--> `Pagamento`  [INFERRED]
  templates/pgUsuario.html → modelos/pagamento.py
- `Cadastrar Plano Form` --shares_data_with--> `Plano`  [INFERRED]
  templates/pgAdm.html → modelos/plano.py
- `Planos Disponíveis Section` --shares_data_with--> `Plano`  [INFERRED]
  templates/pgUsuario.html → modelos/plano.py
- `Presença Form` --shares_data_with--> `Presenca`  [INFERRED]
  templates/turma.html → modelos/presenca.py
- `Aluno Detail/Admin Page` --shares_data_with--> `Matricula`  [INFERRED]
  templates/dt_aluno.html → modelos/matricula.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Shared Confirmation Modal Pattern** — templates_components_confirm_modal_dialog, templates_pgadm_page, templates_pgprofessor_page, templates_pgusuario_page, templates_turmas_page [EXTRACTED 1.00]
- **Mensalidade (Billing) Management Flow** — templates_dt_aluno_pagamento_form, templates_pgusuario_mensalidades_section, modelos_pagamento_pagamento, modelos_plano_plano [INFERRED 0.85]
- **Turma and Attendance Management Flow** — templates_turmas_turma_form, templates_turma_presenca_form, templates_pgprofessor_page, modelos_turma_turma [INFERRED 0.85]

## Communities (118 total, 10 thin omitted)

### Community 0 - "financeiroDAO.py"
Cohesion: 0.16
Nodes (10): Decimal, Pagamento, _para_decimal(), Status a exibir, com o vencimento já aplicado. Uma cobrança `pendente` cujo…, postgres_pix(), fixture, parametrize, Regressão com trava de linha real, opcional na suíte que usa SQLite. Execute… (+2 more)

### Community 1 - "Admin Dashboard Page"
Cohesion: 0.16
Nodes (11): campoDuracao, campoPreco, formatadorDePreco, formularioPlano, Confirm Dialog Component, Admin Dashboard Page, Cadastrar Plano Form, Professor Turmas Page (+3 more)

### Community 2 - "Aluno"
Cohesion: 0.10
Nodes (11): Matrícula feita no balcão: sem login, sem senha e sem convite de acesso. Nasce…, Aluno, Se existe uma conta de acesso, e não se o aluno está em dia ou matriculado.…, Convite de acesso já enviado e ainda não usado (a validade é checada na rota)., Chave do estado da CONTA - nunca da situação financeira nem da matrícula., test_cadastro_publico_recusa_confirmacao_diferente(), test_cadastro_publico_recusa_confirmacao_vazia(), _dados_cadastro() (+3 more)

### Community 3 - "test_plano_vigencia.py"
Cohesion: 0.10
Nodes (35): Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, Com uma troca já agendada, só dois planos fazem sentido num pedido de…, A cobrança do período seguinte tem de nascer no plano que o aluno agendou.…, `pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -…, test_mudanca_vale_por_decurso_de_prazo_quando_o_plano_vence(), _pagar(), plano_barato(), fixture (+27 more)

### Community 4 - "test_limites_pagamento.py"
Cohesion: 0.15
Nodes (16): consultar_mp(), fixture, parametrize, Limites de pagamento por conta, com o provedor inteiramente simulado., _sessao_admin(), _sessao_aluno(), test_admin_limite_por_usuario_persiste_entre_sessoes(), test_alunos_no_mesmo_ip_tem_limites_separados() (+8 more)

### Community 5 - "test_mudanca_plano.py"
Cohesion: 0.14
Nodes (27): detalhes_usuario(), Persistência dos pedidos de troca de plano agendados para a próxima renovação., Aplica um pedido agendado cujo período de origem já terminou sem renovação.…, SolicitacaoPlanoDAO, _agendar(), _pagar(), plano_barato(), fixture (+19 more)

### Community 6 - "PagamentoDAO"
Cohesion: 0.07
Nodes (36): PagamentoDAO, Carrega aluno e plano junto das mensalidades. O template do painel lê…, Lista completa (sem paginar). Mantida para relatórios e testes., Uma página de mensalidades, recortada pelo banco (LIMIT/OFFSET). O painel…, Totais do painel financeiro - sempre calculados no backend a partir do banco,…, True se já existe um Pix ou um checkout válido emitido para esta cobrança.…, True se a cobrança Pix já gerada para este pagamento ainda pode ser…, Solta a preferência atual para que a próxima tentativa crie uma nova. Nunca… (+28 more)

### Community 7 - "Reavaliação de segurança e desempenho — 12/09/2026"
Cohesion: 0.25
Nodes (5): Achados, Atualização de 19/09/2026, Medições locais, Reavaliação de segurança e desempenho — 12/09/2026, Validação e limites

### Community 9 - "test_mercado_pago_servico.py"
Cohesion: 0.09
Nodes (34): ambiente_mercado_pago(), Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, Diz se a integracao esta apontando para producao ou para o sandbox. Prioriza a…, validar_assinatura_webhook(), Hipótese: uma notificação capturada ontem pode ser reenviada hoje., `ts=nan` fazia a comparação da janela dar False e passava pela checagem de…, test_webhook_recusa_assinatura_antiga(), test_webhook_recusa_ts_nao_numerico_finito() (+26 more)

### Community 10 - "test_mercado_pago_oauth.py"
Cohesion: 0.05
Nodes (70): MercadoPagoConexao, Conta do Mercado Pago que a academia autorizou por OAuth. Uma linha só (a…, _sdk(), _agora(), _ajustar(), api_mp(), _conectar(), _dados_conexao() (+62 more)

### Community 11 - "Professor"
Cohesion: 0.10
Nodes (25): cadastrar_professor(), remover_professor(), ProfessorDAO, Professor, impressao_credencial(), Resumo curto e não reversível do hash da senha, guardado na sessão. Nunca é a…, Hipótese: a foto continua acessível por URL depois de tirar a publicação., Hipótese: os contatos vazam na home antes de a publicação ser marcada. (+17 more)

### Community 12 - "test_migracao_checkout.py"
Cohesion: 0.31
Nodes (8): _colunas(), conexao(), migracao(), fixture, Exercita a migração dos campos do Checkout Pro de verdade (upgrade e…, _rodar(), test_downgrade_remove_exatamente_o_que_o_upgrade_criou(), test_upgrade_adiciona_as_colunas_e_preserva_linhas_antigas()

### Community 14 - "checkout.js"
Cohesion: 0.47
Nodes (4): cancelarAberturas(), consultar(), finalizarAbertura(), parar()

### Community 16 - "planos.py"
Cohesion: 0.06
Nodes (33): cadeia_paga(), cobranca_a_pagar(), cobranca_em_decisao(), cobranca_pendente(), duracao_dias(), esta_inadimplente(), fim_periodo_comprometido(), inicio_proximo_periodo() (+25 more)

### Community 17 - "pix_bp.py"
Cohesion: 0.11
Nodes (31): _acesso_permitido(), criar_pix_mensalidade(), _forma_pagamento_confirmada(), _pagamento_mp_mais_relevante(), _pagamento_ou_none(), _pix_expirado(), _processar_status_mp(), limitar_consulta_pagamento (+23 more)

### Community 18 - "logar_como_admin"
Cohesion: 0.17
Nodes (40): AlunoDAO, logar_como_admin(), _matricular(), Cadastro de aluno pela administração, ativação de acesso e confirmação de…, test_admin_lanca_e_baixa_mensalidade_de_aluno_sem_acesso(), test_admin_matricula_aluno_sem_email_senha_nem_acesso(), test_admin_nao_pode_apagar_o_usuario_de_uma_conta_ativa(), test_admin_pode_deixar_cadastro_de_balcao_sem_usuario_e_sem_email() (+32 more)

### Community 19 - "test_checkout_rotas.py"
Cohesion: 0.25
Nodes (22): _assinar(), _pagamento_mp(), _preparar_retorno(), Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala…, Pix aberto e checkout concluído ao mesmo tempo: a consulta pelo…, test_configuracao_ausente_falha_de_forma_explicita(), test_mercado_pago_indisponivel_nao_persiste_nada(), test_retorno_com_aprovacao_confirmada_marca_pago() (+14 more)

### Community 20 - "checkout_bp.py"
Cohesion: 0.11
Nodes (24): abrir_checkout(), _acesso_permitido(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), limitar_consulta_pagamento, limitar_criacao_pagamento, route (+16 more)

### Community 21 - "pix.js"
Cohesion: 0.33
Nodes (14): abrirPix(), alvoDoRotulo(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), liberarBotao(), limparConteudoAnterior() (+6 more)

### Community 22 - "config.py"
Cohesion: 0.21
Nodes (6): Matricula, Plano, Presenca, Abrir o painel filtrado por um plano não pode tocar as mensalidades dos outros., test_painel_financeiro_nao_varre_mensalidades_fora_do_filtro(), Instância descartável para conferir o redesign no navegador (porta 4002).…

### Community 23 - "env.py"
Cohesion: 0.39
Nodes (7): get_engine(), get_engine_url(), get_metadata(), Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online()

### Community 24 - "pagamento.js"
Cohesion: 0.47
Nodes (9): alvoDoRotulo(), consultarStatus(), gerarOuAtualizarPix(), iniciarPolling(), liberarBotao(), marcarOcupado(), mostrarEstado(), pararPolling() (+1 more)

### Community 25 - "c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py"
Cohesion: 0.60
Nodes (5): _backfill_vigencia(), _colunas(), _criar_tabela_solicitacoes(), downgrade(), upgrade()

### Community 26 - "varredura.mjs"
Cohesion: 0.11
Nodes (23): aberto(), ACESSO, auditar(), { chromium }, CONF, confirmacoes(), crc, CREDS (+15 more)

### Community 29 - "896e70afc9c5_adiciona_foto_e_graduacao_do_aluno_.py"
Cohesion: 0.60
Nodes (3): _e_decimal(), _faltantes(), upgrade()

### Community 33 - "test_auditoria_seguranca.py"
Cohesion: 0.07
Nodes (42): _assinar(), logar_como_professor(), _pagamento_mp(), _preparar_para_conciliacao(), fixture, parametrize, Auditoria de segurança: sondas escritas para TENTAR quebrar as regras. Nenhum…, Hipótese: a sessão de professor é aceita nas rotas financeiras do aluno. (+34 more)

### Community 34 - "MercadoPagoIndisponivel"
Cohesion: 0.29
Nodes (8): buscar_pagamentos_por_referencia(), MercadoPagoIndisponivel, Exception, Lista os pagamentos que o Mercado Pago associa a uma external_reference. Usada…, Falha de transporte (timeout/DNS/conexao) ao falar com a API do Mercado Pago., test_buscar_pagamentos_por_referencia_falha_de_transporte(), test_buscar_pagamentos_por_referencia_normaliza_resultados(), test_buscar_pagamentos_por_referencia_sem_resultado()

### Community 35 - "adm_bp.py"
Cohesion: 0.07
Nodes (48): _aluno_do_cpf_ou_painel(), aprovar_aluno(), aprovar_comprovante_manual(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_aluno(), cadastrar_pagamento(), cadastrar_plano() (+40 more)

### Community 36 - "test_datas_turma.py"
Cohesion: 0.18
Nodes (16): _acesso_permitido(), desmatricular_aluno(), detalhe_turma(), matricular_aluno(), painel_professor(), route, registrar_presenca(), _turma_ou_404() (+8 more)

### Community 37 - "criar_aluno"
Cohesion: 0.05
Nodes (52): criar_aluno(), test_aluno_existente_continua_entrando_normalmente(), test_area_do_aluno_renderiza_telas_independentes_do_menu(), test_escolher_plano_cria_mensalidade_e_redireciona_para_pix(), test_perfil_so_autoriza_abertura_automatica_da_propria_mensalidade(), test_plano_atual_continua_disponivel_para_gerar_cobranca(), test_plano_invalido_nao_cria_mensalidade(), test_reenvio_da_contratacao_reutiliza_mensalidade() (+44 more)

### Community 38 - "convites.py"
Cohesion: 0.13
Nodes (22): aluno_do_token(), ConviteIndisponivel, descartar(), enviar(), gerar_token(), _hash(), RuntimeError, Convite de acesso: como um cadastro criado pela administração vira uma conta.… (+14 more)

### Community 41 - "Academia"
Cohesion: 0.13
Nodes (19): configuracoes(), _pagina(), route, editar_professor(), Academia, link_email(), Normalização de contatos profissionais antes de montar links públicos., validar_email() (+11 more)

### Community 42 - "pagamento_polling.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 43 - "mercado_pago_conta.py"
Cohesion: 0.10
Nodes (35): access_token_vigente(), _agora(), ambiente_da_conexao(), _cifrar(), _client_id(), _client_secret(), ConexaoIlegivel, _decifrar() (+27 more)

### Community 44 - "criar_pagamento"
Cohesion: 0.08
Nodes (51): criar_pagamento(), logar_como_aluno(), Hipótese: forjar ?status=approved na volta do MP quita a mensalidade., Hipótese: cada clique cria uma cobrança nova no Mercado Pago., Hipótese: dá para injetar o valor pelo corpo do POST., test_dois_cliques_reaproveitam_a_mesma_preferencia(), test_retorno_ignora_status_aprovado_da_query_string(), test_valor_cobrado_vem_do_banco_e_nao_do_navegador() (+43 more)

### Community 45 - "test_pix_rotas.py"
Cohesion: 0.25
Nodes (17): _assinar(), _resposta_consulta(), _resposta_criacao(), test_admin_tambem_pode_gerar_pix(), test_aluno_gera_pix_da_propria_mensalidade(), test_impede_cobranca_duplicada_em_chamadas_consecutivas(), test_reutiliza_cobranca_pendente_valida(), test_sem_sessao_retorna_401() (+9 more)

### Community 46 - "PagamentoEvento"
Cohesion: 0.14
Nodes (8): Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda. O…, Primeiro dia não coberto por outra mensalidade do mesmo aluno., Define o período coberto por uma mensalidade que ainda não tem um (lançamento…, Abre o período de acesso no momento em que o pagamento é confirmado. Se a…, Reescreve os campos denormalizados do aluno a partir das mensalidades.…, Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.…, PagamentoEvento, Histórico de auditoria de uma mensalidade (nunca grava credenciais ou dados…

### Community 47 - "d9e2f6a14c80_contatos_academia_perfis_professores.py"
Cohesion: 0.83
Nodes (3): _campos_professor(), downgrade(), upgrade()

### Community 49 - "conftest.py"
Cohesion: 0.27
Nodes (11): app(), client(), contexto_app(), limpar_banco(), logar_como_professor(), plano(), fixture, Substitui o provedor de e-mail em todos os módulos que o chamam. A suíte nunca… (+3 more)

### Community 50 - "botao_ocupado.test.cjs"
Cohesion: 0.18
Nodes (7): assert, criarElemento(), fs, montar(), path, test, vm

### Community 51 - "test_seguranca.py"
Cohesion: 0.07
Nodes (26): test_upload_de_arquivo_disfarcado_e_recusado(), _cadastro_publico(), _imagem_jpeg(), _mensagem_da_resposta(), O `login` de um aluno pode ser o e-mail de outro; quem entra é decidido pela…, O ramo "par existe" não pode pagar a ida ao provedor dentro da requisição., Cadastro novo, CPF existente e e-mail existente respondem com a MESMA tela., Quem ainda controla a caixa antiga não pode assumir a conta depois da troca. (+18 more)

### Community 52 - "checkout_abertura.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 55 - "gunicorn.conf.py"
Cohesion: 0.25
Nodes (9): post_worker_init(), Hooks carregados pelo Gunicorn; nunca executados por flask db upgrade., worker_exit(), iniciar(), _laco(), parar(), Aciona a fila periodicamente durante a vida de um worker Gunicorn. Importar…, Inicia uma vez por processo, depois de carregar a aplicação e migrar o banco. (+1 more)

### Community 56 - "ConfiguracaoInvalida"
Cohesion: 0.30
Nodes (11): _autorizacao_valida(), callback(), conectar(), desconectar(), limit, route, O state devolvido é o que ESTA sessão emitiu, há pouco tempo?, Só monta o state/PKCE na sessão e manda o administrador ao Mercado Pago. É um… (+3 more)

### Community 57 - "fila_email.py"
Cohesion: 0.11
Nodes (23): espera_da_proxima_tentativa(), Fila de e-mails no banco. Aviso e cobrança coletivos saíam um a um dentro da…, contar_falhados(), disparar(), enfileirar(), enfileirar_transacional(), _entregar(), _laco() (+15 more)

### Community 58 - "test_migracao_cadastro_administrativo.py"
Cohesion: 0.40
Nodes (3): banco_antigo(), fixture, Verifica a migração em um banco isolado com o schema anterior e dados.

### Community 59 - "salvar_foto_perfil"
Cohesion: 0.12
Nodes (26): ArquivoInvalido, caminho_arquivo(), _conferir_dimensoes(), _detectar_tipo_imagem_real(), ImagemGrandeDemais, _pasta(), Exception, _raiz_uploads() (+18 more)

### Community 60 - "test_keep_alive.py"
Cohesion: 0.16
Nodes (7): ambiente_limpo(), fixture, parametrize, Garante que o keep-alive fica desligado por padrão e só pinga a própria origem., test_intervalo_fica_dentro_da_faixa(), test_nao_liga_com_valor_negativo(), test_ping_so_considera_200_como_sucesso()

### Community 62 - "mercado_pago.py"
Cohesion: 0.13
Nodes (25): _base_url_opcional(), base_url_publica(), cancelar_pagamento(), criar_pagamento_pix(), criar_preferencia_checkout(), _erro_menciona(), _erro_menciona_expiracao(), _extrair_dados_pix() (+17 more)

### Community 63 - "test_arranque_seguranca.py"
Cohesion: 0.22
Nodes (14): _env_arranque(), Validações feitas por servidor.py no arranque (COOKIE_SECURE, TRUSTED_HOSTS,…, `python -m servicos.credenciais`: o hash sai entre aspas simples. O hash do…, Desenvolvimento local sem HTTPS (sem Caddy) não pode ficar travado., _rodar(), test_arranque_falha_com_cookie_secure_false_e_app_base_url_https(), test_arranque_falha_com_cookie_secure_invalido(), test_arranque_falha_sem_trusted_hosts() (+6 more)

### Community 64 - "SolicitacaoMudancaPlano"
Cohesion: 0.20
Nodes (4): O que aconteceu numa tentativa de contratar/renovar/trocar de plano., ResultadoContratacao, Pedido de troca de plano agendado para a próxima renovação. Nunca altera o…, SolicitacaoMudancaPlano

### Community 66 - "erro_validacao_senha"
Cohesion: 0.20
Nodes (10): ativar_acesso(), Transforma um cadastro feito no balcão na conta do próprio aluno. Quem chega…, mascarar_email(), Mostra o bastante do e-mail para o dono se reconhecer, sem revelá-lo a…, _carregar_senhas_comuns(), erro_confirmacao_senha(), erro_validacao_senha(), Retorna uma mensagem quando a senha é curta, comum ou igual ao identificador. (+2 more)

### Community 67 - "servidor.py"
Cohesion: 0.13
Nodes (17): after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, context_processor, errorhandler, Registra a sessão como encerrada: cópias antigas do cookie deixam de valer.…, revogar_sessao_atual(), adicionar_cabecalhos_de_seguranca() (+9 more)

### Community 68 - "autorizacao.py"
Cohesion: 0.14
Nodes (22): foto_professor(), pagina_login(), aluno_autorizado(), aluno_requerido(), _credencial_confere(), encerrar_sessao(), iniciar_sessao(), professor_autorizado() (+14 more)

### Community 69 - "pagina_cadastro"
Cohesion: 0.15
Nodes (20): _em_segundo_plano(), _enviar_em_segundo_plano(), pagina_cadastro(), Roda `tarefa` fora da requisição, para o tempo de resposta não revelar nada. Em…, E-mail COM token (recuperação, confirmação): não pode ir para a `fila_email`. A…, recuperar_senha(), _parece_busca_por_cpf(), O termo é um CPF, ou um pedaço dele, e não um nome que por acaso tem número? (+12 more)

### Community 70 - "gmail_conta.py"
Cohesion: 0.26
Nodes (15): GmailConexao, _access_token(), _cifrar(), _client_id(), _client_secret(), _decifrar(), enviar(), estado() (+7 more)

### Community 71 - "credenciais.py"
Cohesion: 0.20
Nodes (11): admin_configurado(), comparar_em_tempo_constante(), credencial_admin_confere(), gerar_hash_admin(), _main(), Credencial administrativa baseada exclusivamente em hash de senha. O…, Compara duas senhas em tempo constante, sem restrição de alfabeto. Codificar…, True quando existe usuário e hash da senha do administrador. (+3 more)

### Community 72 - "shot.mjs"
Cohesion: 0.29
Nodes (5): { chromium }, contextos, CREDS, jobs, require

### Community 73 - "test_financeiro_admin_painel.py"
Cohesion: 0.33
Nodes (5): test_busca_financeira_trata_curingas_como_texto(), test_painel_financeiro_busca_por_nome_do_aluno(), test_painel_financeiro_exige_admin(), test_painel_financeiro_filtra_por_status(), test_painel_financeiro_mostra_totais_do_backend()

### Community 74 - "usuario_bp.py"
Cohesion: 0.18
Nodes (25): alterar_senha_perfil(), _aluno_da_sessao(), _aluno_por_token(), atualizar_dados_perfil(), cancelar_mudanca_plano(), confirmar_email(), enviar_comprovante_manual_aluno(), enviar_foto_perfil() (+17 more)

### Community 76 - "Pagina"
Cohesion: 0.12
Nodes (7): Pagina, _paginar(), Uma fatia de resultados já recortada pelo banco, com o que a navegação precisa., Uma página existe mesmo quando está vazia. Sem isto, `__len__` fazia `{% if…, Aplica LIMIT/OFFSET e conta o total numa consulta separada e barata. A contagem…, `__len__` fazia `{% if pagina %}` ser falso numa página sem itens, escondendo…, test_pagina_vazia_ainda_mostra_a_navegacao()

### Community 77 - "_tem_limite"
Cohesion: 0.20
Nodes (10): parametrize, Qualquer dígito no termo virava `CPF LIKE '%3%'` e devolvia a academia inteira., Rotas que custam hash de senha, processamento de imagem ou sondagem de token., Limites declarados por decorador NAQUELA rota. `resolve_limits` não serve aqui:…, Guarda do teste acima: uma rota sem limite precisa ser reprovada por ele., _tem_limite(), test_busca_so_trata_como_cpf_o_que_parece_cpf(), test_o_detector_de_limite_realmente_discrimina() (+2 more)

### Community 81 - "Contrato do redesign — SistemaEXTREMETEAM"
Cohesion: 0.09
Nodes (20): 0. Antes de escrever código, 1. Identidade visual (design tokens), 2. Logo oficial (usar SOMENTE a logo original), 3. Telas a implementar, 4. Regras e dados, 5. Forma de trabalhar, Painel administrativo (desktop, sidebar preta com o emblema do dragão), Prompt para o Claude Code — Redesign do SistemaEXTREMETEAM (+12 more)

### Community 82 - "_chave_da_conta"
Cohesion: 0.40
Nodes (5): _chave_da_conta(), Chave de limite por CONTA, caindo no IP só para quem não está autenticado. A…, Alunos atrás do mesmo IP (o Wi-Fi da academia) não dividem a cota., test_limite_de_upload_e_por_conta_e_nao_por_ip(), test_visitante_sem_sessao_ainda_e_limitado_por_ip()

### Community 83 - "Relatório de segurança — Sistema Extreme Team (17/09/2026)"
Cohesion: 0.20
Nodes (10): A1 — `/recuperar_senha` revela por tempo de resposta se o CPF+e-mail existe (Média, CORRIGIDA em 19/09/2026), A2 — `/perfil/dados` sem limite de tentativas na senha atual (Baixa–Média, CORRIGIDA em 19/09/2026), A3 — `/perfil/dados` não valida tamanho de `nome`/`login`/`descricao` (Baixa, CORRIGIDA em 19/09/2026), A4 — Enumeração de usuário/e-mail no cadastro público (Baixa / informativa, CORRIGIDA em 19/09/2026 para CPF e e-mail), Housekeeping: `pip` desatualizado no ambiente virtual local (CORRIGIDO em 19/09/2026: pip 26.2.1), Ordem de correção sugerida (executada em 19/09/2026, ver a seção de atualização), Relatório de segurança — Sistema Extreme Team (17/09/2026), Situação dos 15 achados do relatório de 05/09 (revalidados hoje, código lido diretamente) (+2 more)

### Community 84 - "test_sessao_revogada.py"
Cohesion: 0.24
Nodes (11): Sessões encerradas pelo logout. A sessão do Flask é um cookie assinado, sem…, SessaoRevogada, _cliente_com_cookie(), _entrar_como_admin(), `session.clear()` só limpava o navegador de quem saiu; a cópia do cookie seguia…, test_logout_apaga_revogacoes_vencidas(), test_logout_de_uma_sessao_nao_derruba_as_outras(), test_logout_revoga_a_copia_do_cookie_feita_antes() (+3 more)

### Community 85 - "test_matricula_valida_dados_no_servidor"
Cohesion: 0.40
Nodes (5): parametrize, test_confirmacao_aceita_unicode(), test_matricula_valida_dados_no_servidor(), test_novos_formularios_exigem_csrf(), test_rotas_de_matricula_e_convite_sao_so_do_admin()

### Community 89 - "test_fila_email_concorrencia_postgres.py"
Cohesion: 0.18
Nodes (10): _enfileirar_em_transacao_propria(), postgres_fila(), fixture, Idempotência da fila de e-mail sob concorrência real, em PostgreSQL…, A recusa de uma chave repetida não pode desfazer o lote inteiro. Um…, A trava do lote precisa valer até o fim do lote. Comitar linha a linha…, Enfileira e comita numa sessão própria, como faria outra requisição., test_chave_duplicada_nao_descarta_os_outros_destinatarios_do_lote() (+2 more)

### Community 90 - "Atualização de 19/09/2026 — correções aplicadas e nova varredura"
Cohesion: 0.25
Nodes (8): Atualização de 19/09/2026 — correções aplicadas e nova varredura, Correções dos achados de 17/09, Nova varredura independente (19/09) — S1 e S2, Não alterado (decisão ou baixo valor), Reauditoria de 12/09 (itens de desempenho), Reforços em achados de 05/09 (F1–F15 seguem corrigidos), Revisão do fluxo OAuth do Mercado Pago (código novo da branch), Validação e implantação

### Community 94 - "Severidade BAIXA"
Cohesion: 0.29
Nodes (7): F10 — Redirecionamento aberto via `Referer`, F11 — `/logout` aceita GET, F12 — Enumeração de usuários por tempo de resposta, F13 — Senha mínima de 6 caracteres, sem outros critérios, F14 — Webhook sem verificação de recência do timestamp, F15 — Curinga de `LIKE` no filtro do financeiro, Severidade BAIXA

### Community 95 - "pagina_perfil"
Cohesion: 0.22
Nodes (7): confirmar_presenca(), pagina_perfil(), _plano_do_formulario(), _turma_do_formulario(), mensalidade_destaque(), Escolhe a mensalidade mais relevante para o card 'Minha mensalidade': a mais…, PresencaDAO

### Community 96 - "turma_bp.py"
Cohesion: 0.15
Nodes (16): cadastrar_turma(), gerenciar_turmas(), remover_turma(), TurmaDAO, Turma, Sonda: a data vem da query string e é convertida sem tratamento., test_data_invalida_na_turma_nao_derruba_a_rota(), fixture (+8 more)

### Community 97 - "Relatório de segurança — Sistema Extreme Team"
Cohesion: 0.33
Nodes (6): A verificar em execução, Atualização após as correções, Ordem de correção sugerida, Relatório de segurança — Sistema Extreme Team, Sumário executivo, Verificado e correto

### Community 98 - "Severidade MÉDIA"
Cohesion: 0.33
Nodes (6): F5 — Sem limite de tamanho de requisição: negação de serviço por memória, F6 — Comprovante em PDF servido inline, F7 — Nenhum cabeçalho de segurança HTTP, F8 — Autenticação aceita campo não único e editável pelo usuário, F9 — Confiança em proxy não configurada, Severidade MÉDIA

### Community 99 - "Severidade ALTA"
Cohesion: 0.40
Nodes (5): F1 — Aluno consegue desviar a ficha administrativa de outro aluno, F2 — Ausência de proteção CSRF em 46 de 49 formulários, F3 — Sem limite de tentativas: força bruta na senha do administrador, F4 — Link de recuperação de senha montado a partir do cabeçalho `Host`, Severidade ALTA

### Community 100 - "admin_requerido"
Cohesion: 0.67
Nodes (6): callback(), conectar(), desconectar(), route, _voltar(), admin_requerido()

### Community 101 - "EmailPendente"
Cohesion: 0.20
Nodes (7): EmailPendente, contar_pendentes(), Tudo o que ainda vai sair, inclusive o que está aguardando o adiamento., parametrize, Agendamento sem rede, threads reais ou esperas de relógio., test_nao_inicia_em_testes(), test_retomada_de_item_persistido_e_retentativa_sem_painel()

### Community 102 - "extreme.css"
Cohesion: 0.22
Nodes (4): cadastro-form Registration Form, Cadastro (Registration) Page, Recuperar Senha Form, Recuperar Senha Page

### Community 103 - "keep_alive.py"
Cohesion: 0.29
Nodes (9): iniciar(), _intervalo(), _laco(), _ligado(), parar(), _pingar(), Mantém a aplicação acordada em hospedagens que hibernam por inatividade. Uma…, Encerra o laço. Usado pelos testes; em produção a thread é daemon. (+1 more)

### Community 104 - "index.js"
Cohesion: 0.27
Nodes (8): abrirmodal(), fechar(), icone_senha, input_senha, modal, mostrarSenha(), meuModal Login Modal, Home Page

### Community 106 - "formatar_competencia"
Cohesion: 0.33
Nodes (9): _acesso_permitido_pagamento(), comprovante_mensalidade(), _pagamento_com_acesso_ou_404(), pagina_pagamento(), Há alguém autorizado a ver mensalidades nesta sessão (admin ou aluno ativo)?, _sessao_financeira_valida(), ver_comprovante_manual(), formatar_competencia() (+1 more)

### Community 107 - "Flask App Service (compose)"
Cohesion: 0.22
Nodes (9): Flask App Service (compose), Postgres DB Service (compose), postgres_data Volume, Flask, Flask-SQLAlchemy, Gunicorn, psycopg2-binary, python-dotenv (+1 more)

### Community 108 - "Aluno Detail/Admin Page"
Cohesion: 0.22
Nodes (7): Aluno Mensalidade Launch Form, Aluno Detail/Admin Page, Aluno Profile Update Form, preencherValor() Inline Script, Matrícula Form, Turma Detail Page, Presença Form

### Community 109 - "Aluno Profile Page"
Cohesion: 0.22
Nodes (5): formatadorDePreco, gradePlanos, Histórico de Mensalidades Section, Aluno Profile Page, Planos Disponíveis Section

### Community 110 - ".listar_paginado"
Cohesion: 0.29
Nodes (6): Uma página de alunos já cadastrados, recortada e filtrada pelo banco. O painel…, O CPF é guardado formatado; digitar só os números precisa encontrar mesmo assim., test_busca_do_admin_encontra_o_aluno_pelo_cpf_so_com_digitos(), test_busca_por_nome_com_numero_nao_devolve_todo_mundo(), test_paginacao_do_admin_ignora_pendentes_como_a_tela_sempre_fez(), test_painel_admin_pagina_alunos_no_banco()

### Community 112 - "_convidar_cadastro_existente"
Cohesion: 0.50
Nodes (4): _convidar_cadastro_existente(), _convidar_cadastro_existente_por_id(), Cadastro administrativo que alguém tentou recriar pelo formulário público. Em…, Versão para thread de fundo: a sessão da requisição não vale fora dela.

### Community 113 - "Login Page"
Cohesion: 0.50
Nodes (3): login-form Login Form, Login Page, Password Toggle Inline Script

### Community 115 - "capturar_emails"
Cohesion: 0.67
Nodes (3): capturar_emails(), fixture, Intercepta o envio e devolve os e-mails que teriam saído, com os links.

## Knowledge Gaps
- **112 isolated node(s):** `modal`, `input_senha`, `icone_senha`, `formularioPlano`, `campoPreco` (+107 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PagamentoDAO` connect `PagamentoDAO` to `financeiroDAO.py`, `Aluno`, `test_plano_vigencia.py`, `test_mudanca_plano.py`, `pix_bp.py`, `logar_como_admin`, `test_checkout_rotas.py`, `checkout_bp.py`, `config.py`, `test_auditoria_seguranca.py`, `adm_bp.py`, `criar_aluno`, `criar_pagamento`, `test_pix_rotas.py`, `PagamentoEvento`, `conftest.py`, `test_seguranca.py`, `SolicitacaoMudancaPlano`, `test_financeiro_admin_painel.py`, `usuario_bp.py`, `pagina_perfil`, `formatar_competencia`?**
  _High betweenness centrality (0.162) - this node is a cross-community bridge._
- **Why does `AlunoDAO` connect `logar_como_admin` to `turma_bp.py`, `Aluno`, `adm_bp.py`, `test_datas_turma.py`, `test_mudanca_plano.py`, `pagina_cadastro`, `autorizacao.py`, `PagamentoDAO`, `criar_aluno`, `usuario_bp.py`, `.listar_paginado`, `conftest.py`, `test_seguranca.py`, `config.py`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Why does `logar_como_admin()` connect `logar_como_admin` to `test_plano_vigencia.py`, `test_limites_pagamento.py`, `test_mudanca_plano.py`, `PagamentoDAO`, `test_mercado_pago_oauth.py`, `Professor`, `config.py`, `test_datas_turma.py`, `criar_aluno`, `Academia`, `criar_pagamento`, `test_pix_rotas.py`, `conftest.py`, `test_seguranca.py`, `test_financeiro_admin_painel.py`, `test_sessao_revogada.py`, `test_matricula_valida_dados_no_servidor`, `turma_bp.py`, `.listar_paginado`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Are the 131 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 131 INFERRED edges - model-reasoned connections that need verification._
- **Are the 139 inferred relationships involving `criar_pagamento()` (e.g. with `PagamentoDAO` and `Pagamento`) actually correct?**
  _`criar_pagamento()` has 139 INFERRED edges - model-reasoned connections that need verification._
- **Are the 127 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 127 INFERRED edges - model-reasoned connections that need verification._
- **Are the 109 inferred relationships involving `logar_como_admin()` (e.g. with `test_admin_salva_atualiza_e_limpa_contatos()` and `test_csrf_configuracoes()`) actually correct?**
  _`logar_como_admin()` has 109 INFERRED edges - model-reasoned connections that need verification._