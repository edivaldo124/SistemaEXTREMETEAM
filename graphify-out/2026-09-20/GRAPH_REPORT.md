# Graph Report - SistemaEXTREMETEAM  (2026-09-20)

## Corpus Check
- 127 files · ~192,104 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1717 nodes · 4386 edges · 104 communities (97 shown, 7 thin omitted)
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 910 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6fd9855b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- config.py
- Aluno Profile Page
- pagina_perfil
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
- MercadoPagoIndisponivel
- logar_como_admin
- usuario_bp.py
- checkout_bp.py
- pix.js
- financeiroDAO.py
- env.py
- pagamento.js
- c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py
- varredura.mjs
- 896e70afc9c5_adiciona_foto_e_graduacao_do_aluno_.py
- test_auditoria_seguranca.py
- mercado_pago.py
- adm_bp.py
- test_perfil_e_foto.py
- criar_aluno
- Aluno
- Academia
- pagamento_polling.test.cjs
- mercado_pago_conta.py
- logar_como_aluno
- criar_pagamento
- .buscar_por_id
- d9e2f6a14c80_contatos_academia_perfis_professores.py
- impressao_credencial
- botao_ocupado.test.cjs
- test_seguranca.py
- checkout_abertura.test.cjs
- filtros_financeiro.js
- gunicorn.conf.py
- mercado_pago_oauth_bp.py
- fila_email.py
- test_migracao_cadastro_administrativo.py
- salvar_foto_perfil
- test_keep_alive.py
- convites.py
- .listar_paginado
- test_arranque_seguranca.py
- test_fila_email_concorrencia_postgres.py
- turma_bp.py
- servidor.py
- autorizacao.py
- pagina_cadastro
- EmailPendente
- credenciais.py
- shot.mjs
- .totais_periodo
- route
- Pagina
- _parece_busca_por_cpf
- e4b7c2a91d35_cadastro_administrativo_e_convite_de_acesso.py
- a1f0c3e75b92_schema_inicial.py
- Contrato do redesign — SistemaEXTREMETEAM
- test_regressao_auditoria.py
- Relatório de segurança — Sistema Extreme Team (17/09/2026)
- disparar
- pagina_login
- enviar_email
- _FakePaymentResource
- Atualização de 19/09/2026 — correções aplicadas e nova varredura
- Severidade BAIXA
- erro_validacao_senha
- test_matricula_valida_dados_no_servidor
- Relatório de segurança — Sistema Extreme Team
- Severidade MÉDIA
- Severidade ALTA
- capturar_emails
- test_email_gmail.py
- _convidar_cadastro_existente
- enfileirar_transacional

## God Nodes (most connected - your core abstractions)
1. `PagamentoDAO` - 196 edges
2. `criar_pagamento()` - 141 edges
3. `criar_aluno()` - 129 edges
4. `logar_como_admin()` - 111 edges
5. `logar_como_aluno()` - 110 edges
6. `AlunoDAO` - 91 edges
7. `Aluno` - 58 edges
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

## Communities (104 total, 7 thin omitted)

### Community 0 - "config.py"
Cohesion: 0.16
Nodes (14): Matricula, Plano, app(), client(), contexto_app(), limpar_banco(), logar_como_professor(), plano() (+6 more)

### Community 1 - "Aluno Profile Page"
Cohesion: 0.05
Nodes (36): abrirmodal(), fechar(), icone_senha, input_senha, modal, mostrarSenha(), campoDuracao, campoPreco (+28 more)

### Community 2 - "pagina_perfil"
Cohesion: 0.10
Nodes (18): pagina_perfil(), mensalidade_destaque(), Carrega aluno e plano junto das mensalidades. O template do painel lê…, Lista completa (sem paginar). Mantida para relatórios e testes., Escolhe a mensalidade mais relevante para o card 'Minha mensalidade': a mais…, True se já existe um Pix ou um checkout válido emitido para esta cobrança.…, True se a cobrança Pix já gerada para este pagamento ainda pode ser…, True se a preferência do Checkout Pro já criada pode ser reaproveitada. Só… (+10 more)

### Community 3 - "test_plano_vigencia.py"
Cohesion: 0.12
Nodes (30): Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, Com uma troca já agendada, só dois planos fazem sentido num pedido de…, A cobrança do período seguinte tem de nascer no plano que o aluno agendou.…, `pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -…, _pagar(), plano_barato(), fixture, Vigência do plano: o que decide "Plano ativo" é o período pago, não o cadastro.… (+22 more)

### Community 4 - "test_limites_pagamento.py"
Cohesion: 0.15
Nodes (16): consultar_mp(), fixture, parametrize, Limites de pagamento por conta, com o provedor inteiramente simulado., _sessao_admin(), _sessao_aluno(), test_admin_limite_por_usuario_persiste_entre_sessoes(), test_alunos_no_mesmo_ip_tem_limites_separados() (+8 more)

### Community 5 - "test_mudanca_plano.py"
Cohesion: 0.18
Nodes (25): Persistência dos pedidos de troca de plano agendados para a próxima renovação., Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, SolicitacaoPlanoDAO, _agendar(), _pagar(), plano_barato(), fixture, Mudança para um plano mais barato agendada para a próxima renovação. Regra… (+17 more)

### Community 6 - "PagamentoDAO"
Cohesion: 0.09
Nodes (20): cadastrar_pagamento(), PagamentoDAO, Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda. O…, Aplica um pedido agendado cujo período de origem já terminou sem renovação.…, Primeiro dia não coberto por outra mensalidade do mesmo aluno., Define o período coberto por uma mensalidade que ainda não tem um (lançamento…, Abre o período de acesso no momento em que o pagamento é confirmado. Se a…, Reescreve os campos denormalizados do aluno a partir das mensalidades.… (+12 more)

### Community 7 - "Reavaliação de segurança e desempenho — 12/09/2026"
Cohesion: 0.25
Nodes (5): Achados, Atualização de 19/09/2026, Medições locais, Reavaliação de segurança e desempenho — 12/09/2026, Validação e limites

### Community 9 - "test_mercado_pago_servico.py"
Cohesion: 0.10
Nodes (30): Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, validar_assinatura_webhook(), Hipótese: uma notificação capturada ontem pode ser reenviada hoje., `ts=nan` fazia a comparação da janela dar False e passava pela checagem de…, test_webhook_recusa_assinatura_antiga(), test_webhook_recusa_ts_nao_numerico_finito(), base_url(), _criar_preferencia() (+22 more)

### Community 10 - "test_mercado_pago_oauth.py"
Cohesion: 0.05
Nodes (70): MercadoPagoConexao, Conta do Mercado Pago que a academia autorizou por OAuth. Uma linha só (a…, _sdk(), _agora(), _ajustar(), api_mp(), _conectar(), _dados_conexao() (+62 more)

### Community 11 - "Professor"
Cohesion: 0.09
Nodes (26): gerenciar_turmas(), remover_professor(), ProfessorDAO, Professor, Cadastrar Professor Form, logar_como_professor(), fixture, Hipótese: a foto continua acessível por URL depois de tirar a publicação. (+18 more)

### Community 12 - "test_migracao_checkout.py"
Cohesion: 0.31
Nodes (8): _colunas(), conexao(), migracao(), fixture, Exercita a migração dos campos do Checkout Pro de verdade (upgrade e…, _rodar(), test_downgrade_remove_exatamente_o_que_o_upgrade_criou(), test_upgrade_adiciona_as_colunas_e_preserva_linhas_antigas()

### Community 14 - "checkout.js"
Cohesion: 0.47
Nodes (4): cancelarAberturas(), consultar(), finalizarAbertura(), parar()

### Community 16 - "planos.py"
Cohesion: 0.06
Nodes (33): cadeia_paga(), cobranca_a_pagar(), cobranca_em_decisao(), cobranca_pendente(), duracao_dias(), esta_inadimplente(), fim_periodo_comprometido(), inicio_proximo_periodo() (+25 more)

### Community 17 - "MercadoPagoIndisponivel"
Cohesion: 0.08
Nodes (42): _acesso_permitido(), criar_pix_mensalidade(), _forma_pagamento_confirmada(), _pagamento_mp_mais_relevante(), _pagamento_ou_none(), _pix_expirado(), _processar_status_mp(), limitar_consulta_pagamento (+34 more)

### Community 18 - "logar_como_admin"
Cohesion: 0.16
Nodes (42): AlunoDAO, logar_como_admin(), _matricular(), Cadastro de aluno pela administração, ativação de acesso e confirmação de…, test_admin_lanca_e_baixa_mensalidade_de_aluno_sem_acesso(), test_admin_matricula_aluno_sem_email_senha_nem_acesso(), test_admin_nao_pode_apagar_o_usuario_de_uma_conta_ativa(), test_admin_pode_deixar_cadastro_de_balcao_sem_usuario_e_sem_email() (+34 more)

### Community 19 - "usuario_bp.py"
Cohesion: 0.22
Nodes (15): _acesso_permitido_pagamento(), comprovante_mensalidade(), foto_perfil(), _pagamento_com_acesso_ou_404(), pagina_pagamento(), pagina_termos_responsabilidade(), _pode_ver_foto(), _professor_pode_ver_aluno() (+7 more)

### Community 20 - "checkout_bp.py"
Cohesion: 0.09
Nodes (28): abrir_checkout(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), limitar_consulta_pagamento, limitar_criacao_pagamento, route, _quer_json() (+20 more)

### Community 21 - "pix.js"
Cohesion: 0.33
Nodes (14): abrirPix(), alvoDoRotulo(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), liberarBotao(), limparConteudoAnterior() (+6 more)

### Community 22 - "financeiroDAO.py"
Cohesion: 0.09
Nodes (17): O que aconteceu numa tentativa de contratar/renovar/trocar de plano., ResultadoContratacao, Decimal, Pagamento, _para_decimal(), Status a exibir, com o vencimento já aplicado. Uma cobrança `pendente` cujo…, Pedido de troca de plano agendado para a próxima renovação. Nunca altera o…, SolicitacaoMudancaPlano (+9 more)

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
Cohesion: 0.06
Nodes (47): _assinar(), _pagamento_mp(), _preparar_para_conciliacao(), parametrize, Auditoria de segurança: sondas escritas para TENTAR quebrar as regras. Nenhum…, Hipótese: a sessão de professor é aceita nas rotas financeiras do aluno., Hipótese: como o JS agora usa fetch, o POST perdeu a exigência de CSRF., Hipótese: as demais rotas de dinheiro aceitam POST sem token. (+39 more)

### Community 34 - "mercado_pago.py"
Cohesion: 0.10
Nodes (33): iniciar(), _intervalo(), _laco(), _ligado(), parar(), _pingar(), Mantém a aplicação acordada em hospedagens que hibernam por inatividade. Uma…, Encerra o laço. Usado pelos testes; em produção a thread é daemon. (+25 more)

### Community 35 - "adm_bp.py"
Cohesion: 0.07
Nodes (53): _aluno_do_cpf_ou_painel(), aprovar_aluno(), aprovar_comprovante_manual(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_aluno(), cadastrar_plano(), cancelar_mudanca_plano_admin() (+45 more)

### Community 36 - "test_perfil_e_foto.py"
Cohesion: 0.17
Nodes (15): cadastrar_turma(), remover_turma(), TurmaDAO, Turma, Cadastrar Turma Form, Sonda: a data vem da query string e é convertida sem tratamento., test_data_invalida_na_turma_nao_derruba_a_rota(), fixture (+7 more)

### Community 37 - "criar_aluno"
Cohesion: 0.06
Nodes (35): criar_aluno(), test_aluno_existente_continua_entrando_normalmente(), test_area_do_aluno_renderiza_telas_independentes_do_menu(), test_plano_atual_continua_disponivel_para_gerar_cobranca(), test_busca_financeira_trata_curingas_como_texto(), test_painel_financeiro_busca_por_nome_do_aluno(), test_painel_financeiro_exige_admin(), test_painel_financeiro_filtra_por_status() (+27 more)

### Community 38 - "Aluno"
Cohesion: 0.10
Nodes (11): Matrícula feita no balcão: sem login, sem senha e sem convite de acesso. Nasce…, Aluno, Se existe uma conta de acesso, e não se o aluno está em dia ou matriculado.…, Convite de acesso já enviado e ainda não usado (a validade é checada na rota)., Chave do estado da CONTA - nunca da situação financeira nem da matrícula., test_cadastro_publico_recusa_confirmacao_diferente(), test_cadastro_publico_recusa_confirmacao_vazia(), _dados_cadastro() (+3 more)

### Community 41 - "Academia"
Cohesion: 0.13
Nodes (20): configuracoes(), _pagina(), route, editar_professor(), Academia, admin_requerido(), link_email(), Normalização de contatos profissionais antes de montar links públicos. (+12 more)

### Community 42 - "pagamento_polling.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 43 - "mercado_pago_conta.py"
Cohesion: 0.10
Nodes (37): ConfiguracaoInvalida, access_token_vigente(), _agora(), ambiente_da_conexao(), _cifrar(), _client_id(), _client_secret(), ConexaoIlegivel (+29 more)

### Community 44 - "logar_como_aluno"
Cohesion: 0.10
Nodes (42): logar_como_aluno(), _mockar_preferencia(), parametrize, Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala…, Um boleto pendente do Checkout Pro grava provider_payment_id, mas não é Pix:…, _resposta_preferencia(), test_abertura_json_navega_sem_redirecionar_post_externo(), test_admin_tambem_pode_abrir_checkout() (+34 more)

### Community 45 - "criar_pagamento"
Cohesion: 0.25
Nodes (21): criar_pagamento(), _assinar(), _resposta_consulta(), _resposta_criacao(), test_admin_tambem_pode_gerar_pix(), test_aluno_gera_pix_da_propria_mensalidade(), test_aluno_nao_acessa_mensalidade_de_outro_aluno(), test_falha_de_indisponibilidade_do_mp_retorna_503() (+13 more)

### Community 46 - ".buscar_por_id"
Cohesion: 0.15
Nodes (27): _assinar(), _pagamento_mp(), _preparar_retorno(), Pix aberto e checkout concluído ao mesmo tempo: a consulta pelo…, test_configuracao_ausente_falha_de_forma_explicita(), test_mercado_pago_indisponivel_nao_persiste_nada(), test_retorno_com_aprovacao_confirmada_marca_pago(), test_retorno_com_mp_indisponivel_avisa_sem_mudar_status() (+19 more)

### Community 47 - "d9e2f6a14c80_contatos_academia_perfis_professores.py"
Cohesion: 0.83
Nodes (3): _campos_professor(), downgrade(), upgrade()

### Community 49 - "impressao_credencial"
Cohesion: 0.21
Nodes (10): PresencaDAO, Presenca, impressao_credencial(), Resumo curto e não reversível do hash da senha, guardado na sessão. Nunca é a…, parametrize, test_consulta_com_data_invalida_exibe_hoje_e_aviso(), test_consulta_com_data_valida_preserva_data_selecionada(), test_data_invalida_nao_contorna_permissoes() (+2 more)

### Community 50 - "botao_ocupado.test.cjs"
Cohesion: 0.18
Nodes (7): assert, criarElemento(), fs, montar(), path, test, vm

### Community 51 - "test_seguranca.py"
Cohesion: 0.07
Nodes (24): test_upload_de_arquivo_disfarcado_e_recusado(), _cadastro_publico(), _imagem_jpeg(), _mensagem_da_resposta(), O `login` de um aluno pode ser o e-mail de outro; quem entra é decidido pela…, O ramo "par existe" não pode pagar a ida ao provedor dentro da requisição., Cadastro novo, CPF existente e e-mail existente respondem com a MESMA tela., Quem ainda controla a caixa antiga não pode assumir a conta depois da troca. (+16 more)

### Community 52 - "checkout_abertura.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 55 - "gunicorn.conf.py"
Cohesion: 0.25
Nodes (9): post_worker_init(), Hooks carregados pelo Gunicorn; nunca executados por flask db upgrade., worker_exit(), iniciar(), _laco(), parar(), Aciona a fila periodicamente durante a vida de um worker Gunicorn. Importar…, Inicia uma vez por processo, depois de carregar a aplicação e migrar o banco. (+1 more)

### Community 56 - "mercado_pago_oauth_bp.py"
Cohesion: 0.36
Nodes (9): _autorizacao_valida(), callback(), conectar(), desconectar(), limit, route, O state devolvido é o que ESTA sessão emitiu, há pouco tempo?, Só monta o state/PKCE na sessão e manda o administrador ao Mercado Pago. É um… (+1 more)

### Community 57 - "fila_email.py"
Cohesion: 0.16
Nodes (14): espera_da_proxima_tentativa(), Fila de e-mails no banco. Aviso e cobrança coletivos saíam um a um dentro da…, contar_falhados(), contar_pendentes(), _entregar(), listar_pendentes(), processar_agora(), Processamento dos e-mails coletivos fora da requisição. O que muda em relação… (+6 more)

### Community 58 - "test_migracao_cadastro_administrativo.py"
Cohesion: 0.40
Nodes (3): banco_antigo(), fixture, Verifica a migração em um banco isolado com o schema anterior e dados.

### Community 59 - "salvar_foto_perfil"
Cohesion: 0.10
Nodes (30): ArquivoInvalido, _conferir_dimensoes(), _detectar_tipo_imagem_real(), ImagemGrandeDemais, _pasta(), Exception, _raiz_uploads(), Armazenamento de arquivos enviados por usuários (fotos de perfil, comprovantes… (+22 more)

### Community 60 - "test_keep_alive.py"
Cohesion: 0.16
Nodes (7): ambiente_limpo(), fixture, parametrize, Garante que o keep-alive fica desligado por padrão e só pinga a própria origem., test_intervalo_fica_dentro_da_faixa(), test_nao_liga_com_valor_negativo(), test_ping_so_considera_200_como_sucesso()

### Community 61 - "convites.py"
Cohesion: 0.16
Nodes (16): aluno_do_token(), ConviteIndisponivel, descartar(), enviar(), gerar_token(), _hash(), RuntimeError, Convite de acesso: como um cadastro criado pela administração vira uma conta.… (+8 more)

### Community 62 - ".listar_paginado"
Cohesion: 0.17
Nodes (10): _paginar(), Uma página de mensalidades, recortada pelo banco (LIMIT/OFFSET). O painel…, Aplica LIMIT/OFFSET e conta o total numa consulta separada e barata. A contagem…, Uma página de alunos já cadastrados, recortada e filtrada pelo banco. O painel…, O CPF é guardado formatado; digitar só os números precisa encontrar mesmo assim., test_busca_do_admin_encontra_o_aluno_pelo_cpf_so_com_digitos(), test_busca_por_nome_com_numero_nao_devolve_todo_mundo(), test_financeiro_pagina_no_banco_sem_carregar_tudo() (+2 more)

### Community 63 - "test_arranque_seguranca.py"
Cohesion: 0.22
Nodes (14): _env_arranque(), Validações feitas por servidor.py no arranque (COOKIE_SECURE, TRUSTED_HOSTS,…, `python -m servicos.credenciais`: o hash sai entre aspas simples. O hash do…, Desenvolvimento local sem HTTPS (sem Caddy) não pode ficar travado., _rodar(), test_arranque_falha_com_cookie_secure_false_e_app_base_url_https(), test_arranque_falha_com_cookie_secure_invalido(), test_arranque_falha_sem_trusted_hosts() (+6 more)

### Community 64 - "test_fila_email_concorrencia_postgres.py"
Cohesion: 0.18
Nodes (10): _enfileirar_em_transacao_propria(), postgres_fila(), fixture, Idempotência da fila de e-mail sob concorrência real, em PostgreSQL…, A recusa de uma chave repetida não pode desfazer o lote inteiro. Um…, A trava do lote precisa valer até o fim do lote. Comitar linha a linha…, Enfileira e comita numa sessão própria, como faria outra requisição., test_chave_duplicada_nao_descarta_os_outros_destinatarios_do_lote() (+2 more)

### Community 66 - "turma_bp.py"
Cohesion: 0.25
Nodes (11): _acesso_permitido(), cadastrar_professor(), desmatricular_aluno(), detalhe_turma(), matricular_aluno(), painel_professor(), route, registrar_presenca() (+3 more)

### Community 67 - "servidor.py"
Cohesion: 0.06
Nodes (41): after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, Flask App Service (compose), Postgres DB Service (compose), postgres_data Volume, context_processor, errorhandler (+33 more)

### Community 68 - "autorizacao.py"
Cohesion: 0.16
Nodes (19): _acesso_permitido(), Mesma regra já usada no Pix e na página de pagamento: o próprio aluno ou o…, foto_professor(), aluno_autorizado(), aluno_requerido(), _credencial_confere(), encerrar_sessao(), professor_autorizado() (+11 more)

### Community 69 - "pagina_cadastro"
Cohesion: 0.35
Nodes (10): _em_segundo_plano(), _enviar_em_segundo_plano(), pagina_cadastro(), Roda `tarefa` fora da requisição, para o tempo de resposta não revelar nada. Em…, E-mail COM token (recuperação, confirmação): não pode ir para a `fila_email`. A…, recuperar_senha(), formatar_cpf(), formatar_telefone() (+2 more)

### Community 70 - "EmailPendente"
Cohesion: 0.25
Nodes (5): EmailPendente, parametrize, Agendamento sem rede, threads reais ou esperas de relógio., test_nao_inicia_em_testes(), test_retomada_de_item_persistido_e_retentativa_sem_painel()

### Community 71 - "credenciais.py"
Cohesion: 0.20
Nodes (11): admin_configurado(), comparar_em_tempo_constante(), credencial_admin_confere(), gerar_hash_admin(), _main(), Credencial administrativa baseada exclusivamente em hash de senha. O…, Compara duas senhas em tempo constante, sem restrição de alfabeto. Codificar…, True quando existe usuário e hash da senha do administrador. (+3 more)

### Community 72 - "shot.mjs"
Cohesion: 0.29
Nodes (5): { chromium }, contextos, CREDS, jobs, require

### Community 73 - ".totais_periodo"
Cohesion: 0.29
Nodes (5): Totais do painel financeiro - sempre calculados no backend a partir do banco,…, Status como o painel deve LER, com o vencimento aplicado na própria consulta. A…, test_indicadores_e_tabela_concordam_na_primeira_abertura(), test_indicadores_saem_de_uma_consulta_de_agregacao(), test_totais_periodo_preserva_o_escopo_dos_filtros_de_data()

### Community 74 - "route"
Cohesion: 0.24
Nodes (17): alterar_senha_perfil(), _aluno_da_sessao(), _aluno_por_token(), atualizar_dados_perfil(), confirmar_email(), enviar_comprovante_manual_aluno(), enviar_foto_perfil(), limit (+9 more)

### Community 76 - "Pagina"
Cohesion: 0.14
Nodes (5): Pagina, Uma fatia de resultados já recortada pelo banco, com o que a navegação precisa., Uma página existe mesmo quando está vazia. Sem isto, `__len__` fazia `{% if…, `__len__` fazia `{% if pagina %}` ser falso numa página sem itens, escondendo…, test_pagina_vazia_ainda_mostra_a_navegacao()

### Community 77 - "_parece_busca_por_cpf"
Cohesion: 0.17
Nodes (12): _parece_busca_por_cpf(), O termo é um CPF, ou um pedaço dele, e não um nome que por acaso tem número?, parametrize, Qualquer dígito no termo virava `CPF LIKE '%3%'` e devolvia a academia inteira., Rotas que custam hash de senha, processamento de imagem ou sondagem de token., Limites declarados por decorador NAQUELA rota. `resolve_limits` não serve aqui:…, Guarda do teste acima: uma rota sem limite precisa ser reprovada por ele., _tem_limite() (+4 more)

### Community 81 - "Contrato do redesign — SistemaEXTREMETEAM"
Cohesion: 0.09
Nodes (20): 0. Antes de escrever código, 1. Identidade visual (design tokens), 2. Logo oficial (usar SOMENTE a logo original), 3. Telas a implementar, 4. Regras e dados, 5. Forma de trabalhar, Painel administrativo (desktop, sidebar preta com o emblema do dragão), Prompt para o Claude Code — Redesign do SistemaEXTREMETEAM (+12 more)

### Community 82 - "test_regressao_auditoria.py"
Cohesion: 0.07
Nodes (24): _chave_da_conta(), Chave de limite por CONTA, caindo no IP só para quem não está autenticado. A…, _contar_selects_em_alunos(), _credencial(), Regressões da auditoria de segurança, desempenho e confiabilidade. Cada caso…, Head-of-line blocking: a primeira linha falhando não pode impedir as seguintes.…, Uma linha `desistiu` nunca foi entregue: recusar o reenvio fazia a tela dizer…, A revivência vale só para o abandonado: clique duplo continua virando um envio. (+16 more)

### Community 83 - "Relatório de segurança — Sistema Extreme Team (17/09/2026)"
Cohesion: 0.20
Nodes (10): A1 — `/recuperar_senha` revela por tempo de resposta se o CPF+e-mail existe (Média, CORRIGIDA em 19/09/2026), A2 — `/perfil/dados` sem limite de tentativas na senha atual (Baixa–Média, CORRIGIDA em 19/09/2026), A3 — `/perfil/dados` não valida tamanho de `nome`/`login`/`descricao` (Baixa, CORRIGIDA em 19/09/2026), A4 — Enumeração de usuário/e-mail no cadastro público (Baixa / informativa, CORRIGIDA em 19/09/2026 para CPF e e-mail), Housekeeping: `pip` desatualizado no ambiente virtual local (CORRIGIDO em 19/09/2026: pip 26.2.1), Ordem de correção sugerida (executada em 19/09/2026, ver a seção de atualização), Relatório de segurança — Sistema Extreme Team (17/09/2026), Situação dos 15 achados do relatório de 05/09 (revalidados hoje, código lido diretamente) (+2 more)

### Community 84 - "disparar"
Cohesion: 0.29
Nodes (7): disparar(), _laco(), _liberar_e_retomar_se_preciso(), Drena a fila enquanto houver entrega acontecendo. Encerra na primeira passada…, Desregistra a thread e sobe outra se alguém pediu trabalho durante a queda. Sem…, Acorda o processamento em segundo plano, sem bloquear a requisição. Se a thread…, test_reaciona_fila_sem_requisicao_e_sobrevive_a_falha()

### Community 85 - "pagina_login"
Cohesion: 0.33
Nodes (5): pagina_login(), iniciar_sessao(), Grava na sessão atual a credencial em vigor (login ou troca de senha bem-…, Dá um identificador à sessão recém-aberta, para o logout poder revogá-la.…, registrar_credencial()

### Community 86 - "enviar_email"
Cohesion: 0.53
Nodes (5): enviar_email(), _enviar_via_brevo(), _enviar_via_gmail(), _obter_token_gmail(), Envia e-mail transacional pelo provedor configurado. Retorna True/False; nunca…

### Community 90 - "Atualização de 19/09/2026 — correções aplicadas e nova varredura"
Cohesion: 0.25
Nodes (8): Atualização de 19/09/2026 — correções aplicadas e nova varredura, Correções dos achados de 17/09, Nova varredura independente (19/09) — S1 e S2, Não alterado (decisão ou baixo valor), Reauditoria de 12/09 (itens de desempenho), Reforços em achados de 05/09 (F1–F15 seguem corrigidos), Revisão do fluxo OAuth do Mercado Pago (código novo da branch), Validação e implantação

### Community 94 - "Severidade BAIXA"
Cohesion: 0.29
Nodes (7): F10 — Redirecionamento aberto via `Referer`, F11 — `/logout` aceita GET, F12 — Enumeração de usuários por tempo de resposta, F13 — Senha mínima de 6 caracteres, sem outros critérios, F14 — Webhook sem verificação de recência do timestamp, F15 — Curinga de `LIKE` no filtro do financeiro, Severidade BAIXA

### Community 95 - "erro_validacao_senha"
Cohesion: 0.20
Nodes (10): ativar_acesso(), Transforma um cadastro feito no balcão na conta do próprio aluno. Quem chega…, mascarar_email(), Mostra o bastante do e-mail para o dono se reconhecer, sem revelá-lo a…, _carregar_senhas_comuns(), erro_confirmacao_senha(), erro_validacao_senha(), Retorna uma mensagem quando a senha é curta, comum ou igual ao identificador. (+2 more)

### Community 96 - "test_matricula_valida_dados_no_servidor"
Cohesion: 0.40
Nodes (5): parametrize, test_confirmacao_aceita_unicode(), test_matricula_valida_dados_no_servidor(), test_novos_formularios_exigem_csrf(), test_rotas_de_matricula_e_convite_sao_so_do_admin()

### Community 97 - "Relatório de segurança — Sistema Extreme Team"
Cohesion: 0.33
Nodes (6): A verificar em execução, Atualização após as correções, Ordem de correção sugerida, Relatório de segurança — Sistema Extreme Team, Sumário executivo, Verificado e correto

### Community 98 - "Severidade MÉDIA"
Cohesion: 0.33
Nodes (6): F5 — Sem limite de tamanho de requisição: negação de serviço por memória, F6 — Comprovante em PDF servido inline, F7 — Nenhum cabeçalho de segurança HTTP, F8 — Autenticação aceita campo não único e editável pelo usuário, F9 — Confiança em proxy não configurada, Severidade MÉDIA

### Community 99 - "Severidade ALTA"
Cohesion: 0.40
Nodes (5): F1 — Aluno consegue desviar a ficha administrativa de outro aluno, F2 — Ausência de proteção CSRF em 46 de 49 formulários, F3 — Sem limite de tentativas: força bruta na senha do administrador, F4 — Link de recuperação de senha montado a partir do cabeçalho `Host`, Severidade ALTA

### Community 100 - "capturar_emails"
Cohesion: 0.67
Nodes (3): capturar_emails(), fixture, Intercepta o envio e devolve os e-mails que teriam saído, com os links.

### Community 102 - "_convidar_cadastro_existente"
Cohesion: 0.50
Nodes (4): _convidar_cadastro_existente(), _convidar_cadastro_existente_por_id(), Cadastro administrativo que alguém tentou recriar pelo formulário público. Em…, Versão para thread de fundo: a sessão da requisição não vale fora dela.

### Community 103 - "enfileirar_transacional"
Cohesion: 0.50
Nodes (4): enfileirar(), enfileirar_transacional(), E-mail transacional que NÃO carrega token, pela fila durável e fora da…, Registra um e-mail para envio. Devolve a linha criada, ou None se já existia.…

## Knowledge Gaps
- **112 isolated node(s):** `modal`, `input_senha`, `icone_senha`, `formularioPlano`, `campoPreco` (+107 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PagamentoDAO` connect `PagamentoDAO` to `config.py`, `pagina_perfil`, `test_plano_vigencia.py`, `test_mudanca_plano.py`, `MercadoPagoIndisponivel`, `logar_como_admin`, `usuario_bp.py`, `checkout_bp.py`, `financeiroDAO.py`, `test_auditoria_seguranca.py`, `adm_bp.py`, `criar_aluno`, `Aluno`, `logar_como_aluno`, `criar_pagamento`, `.buscar_por_id`, `test_seguranca.py`, `.listar_paginado`, `.totais_periodo`, `route`, `test_regressao_auditoria.py`?**
  _High betweenness centrality (0.158) - this node is a cross-community bridge._
- **Why does `logar_como_admin()` connect `logar_como_admin` to `config.py`, `test_plano_vigencia.py`, `test_limites_pagamento.py`, `test_mudanca_plano.py`, `test_mercado_pago_oauth.py`, `Professor`, `test_perfil_e_foto.py`, `criar_aluno`, `Academia`, `logar_como_aluno`, `criar_pagamento`, `.buscar_por_id`, `impressao_credencial`, `test_seguranca.py`, `.listar_paginado`, `servidor.py`, `.totais_periodo`, `test_regressao_auditoria.py`, `test_matricula_valida_dados_no_servidor`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `AlunoDAO` connect `logar_como_admin` to `config.py`, `turma_bp.py`, `adm_bp.py`, `test_perfil_e_foto.py`, `pagina_cadastro`, `PagamentoDAO`, `Aluno`, `criar_aluno`, `test_regressao_auditoria.py`, `usuario_bp.py`, `test_seguranca.py`, `pagina_login`, `.listar_paginado`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Are the 131 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 131 INFERRED edges - model-reasoned connections that need verification._
- **Are the 139 inferred relationships involving `criar_pagamento()` (e.g. with `PagamentoDAO` and `Pagamento`) actually correct?**
  _`criar_pagamento()` has 139 INFERRED edges - model-reasoned connections that need verification._
- **Are the 127 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 127 INFERRED edges - model-reasoned connections that need verification._
- **Are the 109 inferred relationships involving `logar_como_admin()` (e.g. with `test_admin_salva_atualiza_e_limpa_contatos()` and `test_csrf_configuracoes()`) actually correct?**
  _`logar_como_admin()` has 109 INFERRED edges - model-reasoned connections that need verification._