# Graph Report - SistemaEXTREMETEAM  (2026-09-21)

## Corpus Check
- 127 files · ~191,984 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1717 nodes · 4327 edges · 111 communities (101 shown, 10 thin omitted)
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 901 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `795bb2b4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- config.py
- Aluno Profile Page
- PagamentoDAO
- test_plano_vigencia.py
- test_limites_pagamento.py
- test_mudanca_plano.py
- PagamentoEvento
- Reavaliação de segurança e desempenho — 12/09/2026
- SistemaEXTREMETEAM Project
- test_mercado_pago_servico.py
- test_mercado_pago_oauth.py
- test_auditoria_seguranca.py
- test_migracao_checkout.py
- checkout.js
- CLAUDE.md
- planos.py
- pix_bp.py
- logar_como_admin
- URLPublicaInvalida
- checkout_bp.py
- pix.js
- .contratar_plano
- env.py
- pagamento.js
- c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py
- varredura.mjs
- 896e70afc9c5_adiciona_foto_e_graduacao_do_aluno_.py
- test_aprovacao_incoerente_nao_quita_mensalidade
- MercadoPagoIndisponivel
- adm_bp.py
- test_perfil_e_foto.py
- criar_aluno
- Aluno
- Academia
- pagamento_polling.test.cjs
- mercado_pago_conta.py
- test_checkout_rotas.py
- criar_pagamento
- .buscar_por_id
- d9e2f6a14c80_contatos_academia_perfis_professores.py
- test_datas_turma.py
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
- logar_como_aluno
- test_arranque_seguranca.py
- test_fila_email_concorrencia_postgres.py
- Pagamento
- servidor.py
- turma_bp.py
- _enviar_em_segundo_plano
- EmailPendente
- credenciais.py
- shot.mjs
- .totais_periodo
- usuario_bp.py
- Pagina
- _parece_busca_por_cpf
- e4b7c2a91d35_cadastro_administrativo_e_convite_de_acesso.py
- a1f0c3e75b92_schema_inicial.py
- Contrato do redesign — SistemaEXTREMETEAM
- _chave_da_conta
- Relatório de segurança — Sistema Extreme Team (17/09/2026)
- disparar
- test_professor_perfil.py
- _png_bomba
- _FakePaymentResource
- Atualização de 19/09/2026 — correções aplicadas e nova varredura
- Severidade BAIXA
- route
- test_mercado_pago_oauth_postgres.py
- Relatório de segurança — Sistema Extreme Team
- Severidade MÉDIA
- Severidade ALTA
- conftest.py
- enviar_email
- parametrize
- test_financeiro_admin_painel.py
- test_matricula_valida_dados_no_servidor
- test_retentativa_acontece_sem_ninguem_abrir_o_painel
- test_trocar_a_credencial_do_admin_encerra_a_sessao_administrativa
- limites_pagamento.py
- capturar_emails
- test_retorno_ignora_status_aprovado_da_query_string
- parametrize

## God Nodes (most connected - your core abstractions)
1. `PagamentoDAO` - 187 edges
2. `criar_pagamento()` - 139 edges
3. `criar_aluno()` - 127 edges
4. `logar_como_admin()` - 111 edges
5. `logar_como_aluno()` - 110 edges
6. `AlunoDAO` - 82 edges
7. `Aluno` - 54 edges
8. `MercadoPagoIndisponivel` - 41 edges
9. `_matricular()` - 34 edges
10. `Professor` - 33 edges

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

## Communities (111 total, 10 thin omitted)

### Community 0 - "config.py"
Cohesion: 0.12
Nodes (14): _paginar(), Aplica LIMIT/OFFSET e conta o total numa consulta separada e barata. A contagem…, Decimal, Matricula, _para_decimal(), Plano, Pedido de troca de plano agendado para a próxima renovação. Nunca altera o…, SolicitacaoMudancaPlano (+6 more)

### Community 1 - "Aluno Profile Page"
Cohesion: 0.05
Nodes (36): abrirmodal(), fechar(), icone_senha, input_senha, modal, mostrarSenha(), campoDuracao, campoPreco (+28 more)

### Community 2 - "PagamentoDAO"
Cohesion: 0.10
Nodes (23): PagamentoDAO, Carrega aluno e plano junto das mensalidades. O template do painel lê…, Lista completa (sem paginar). Mantida para relatórios e testes., True se já existe um Pix ou um checkout válido emitido para esta cobrança.…, Acha a mensalidade por qualquer uma das duas referências persistidas. O Pix…, True se a cobrança Pix já gerada para este pagamento ainda pode ser…, True se a preferência do Checkout Pro já criada pode ser reaproveitada. Só…, Solta a preferência atual para que a próxima tentativa crie uma nova. Nunca… (+15 more)

### Community 3 - "test_plano_vigencia.py"
Cohesion: 0.17
Nodes (23): _pagar(), plano_barato(), fixture, Vigência do plano: o que decide "Plano ativo" é o período pago, não o cadastro.…, Mensalidade paga cobrindo um período - o que de fato ativa o plano., test_acao_forjada_de_renovacao_sem_vigencia_apenas_contrata(), test_acao_invalida_no_formulario_cai_no_fluxo_de_contratacao(), test_admin_continua_podendo_trocar_o_plano_do_cadastro() (+15 more)

### Community 4 - "test_limites_pagamento.py"
Cohesion: 0.15
Nodes (16): consultar_mp(), fixture, parametrize, Limites de pagamento por conta, com o provedor inteiramente simulado., _sessao_admin(), _sessao_aluno(), test_admin_limite_por_usuario_persiste_entre_sessoes(), test_alunos_no_mesmo_ip_tem_limites_separados() (+8 more)

### Community 5 - "test_mudanca_plano.py"
Cohesion: 0.17
Nodes (25): Persistência dos pedidos de troca de plano agendados para a próxima renovação., Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, SolicitacaoPlanoDAO, _agendar(), _pagar(), plano_barato(), fixture, Mudança para um plano mais barato agendada para a próxima renovação. Regra… (+17 more)

### Community 6 - "PagamentoEvento"
Cohesion: 0.14
Nodes (8): Primeiro dia não coberto por outra mensalidade do mesmo aluno., Define o período coberto por uma mensalidade que ainda não tem um (lançamento…, Abre o período de acesso no momento em que o pagamento é confirmado. Se a…, Reescreve os campos denormalizados do aluno a partir das mensalidades.…, Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.…, PagamentoEvento, Histórico de auditoria de uma mensalidade (nunca grava credenciais ou dados…, test_comprovante_em_analise_marca_situacao_do_aluno()

### Community 7 - "Reavaliação de segurança e desempenho — 12/09/2026"
Cohesion: 0.25
Nodes (5): Achados, Atualização de 19/09/2026, Medições locais, Reavaliação de segurança e desempenho — 12/09/2026, Validação e limites

### Community 9 - "test_mercado_pago_servico.py"
Cohesion: 0.11
Nodes (28): Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, validar_assinatura_webhook(), Hipótese: uma notificação capturada ontem pode ser reenviada hoje., `ts=nan` fazia a comparação da janela dar False e passava pela checagem de…, test_webhook_recusa_assinatura_antiga(), test_webhook_recusa_ts_nao_numerico_finito(), base_url(), _criar_preferencia() (+20 more)

### Community 10 - "test_mercado_pago_oauth.py"
Cohesion: 0.08
Nodes (54): MercadoPagoConexao, Conta do Mercado Pago que a academia autorizou por OAuth. Uma linha só (a…, _agora(), _ajustar(), api_mp(), _conectar(), _dados_conexao(), oauth_env() (+46 more)

### Community 11 - "test_auditoria_seguranca.py"
Cohesion: 0.09
Nodes (31): cadastrar_professor(), remover_professor(), ProfessorDAO, Professor, impressao_credencial(), Resumo curto e não reversível do hash da senha, guardado na sessão. Nunca é a…, Cadastrar Professor Form, logar_como_professor() (+23 more)

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
Cohesion: 0.12
Nodes (30): _acesso_permitido(), criar_pix_mensalidade(), _forma_pagamento_confirmada(), _pagamento_mp_mais_relevante(), _pagamento_ou_none(), _pix_expirado(), _processar_status_mp(), limitar_consulta_pagamento (+22 more)

### Community 18 - "logar_como_admin"
Cohesion: 0.14
Nodes (45): AlunoDAO, logar_como_admin(), _matricular(), Cadastro de aluno pela administração, ativação de acesso e confirmação de…, test_admin_lanca_e_baixa_mensalidade_de_aluno_sem_acesso(), test_admin_matricula_aluno_sem_email_senha_nem_acesso(), test_admin_nao_pode_apagar_o_usuario_de_uma_conta_ativa(), test_admin_pode_deixar_cadastro_de_balcao_sem_usuario_e_sem_email() (+37 more)

### Community 19 - "URLPublicaInvalida"
Cohesion: 0.18
Nodes (17): back_urls absolutas para onde o Mercado Pago devolve o aluno. Os três destinos…, _urls_retorno(), solicitar_troca_email(), iniciar(), _intervalo(), _laco(), _ligado(), parar() (+9 more)

### Community 20 - "checkout_bp.py"
Cohesion: 0.09
Nodes (29): abrir_checkout(), _acesso_permitido(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), limitar_consulta_pagamento, limitar_criacao_pagamento, route (+21 more)

### Community 21 - "pix.js"
Cohesion: 0.33
Nodes (14): abrirPix(), alvoDoRotulo(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), liberarBotao(), limparConteudoAnterior() (+6 more)

### Community 22 - ".contratar_plano"
Cohesion: 0.11
Nodes (11): pagina_perfil(), O que aconteceu numa tentativa de contratar/renovar/trocar de plano., Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda. O…, Aplica um pedido agendado cujo período de origem já terminou sem renovação.…, Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, Com uma troca já agendada, só dois planos fazem sentido num pedido de…, A cobrança do período seguinte tem de nascer no plano que o aluno agendou.…, `pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -… (+3 more)

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

### Community 33 - "test_aprovacao_incoerente_nao_quita_mensalidade"
Cohesion: 0.20
Nodes (13): _assinar(), _pagamento_mp(), _preparar_para_conciliacao(), Hipótese: uma resposta 'approved' incoerente quita a mensalidade mesmo assim., Contraprova: com tudo batendo, a baixa acontece., Hipótese: assinatura válida basta para quitar, mesmo com valor errado., Reenvio da mesma notificação não pode gerar segunda baixa nem novo evento., Sonda: cada GET de status pode disparar consultas à API do Mercado Pago. Sem… (+5 more)

### Community 34 - "MercadoPagoIndisponivel"
Cohesion: 0.10
Nodes (37): _base_url_opcional(), base_url_publica(), buscar_pagamentos_por_referencia(), cancelar_pagamento(), criar_pagamento_pix(), criar_preferencia_checkout(), _erro_menciona(), _erro_menciona_expiracao() (+29 more)

### Community 35 - "adm_bp.py"
Cohesion: 0.07
Nodes (53): _aluno_do_cpf_ou_painel(), aprovar_aluno(), aprovar_comprovante_manual(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_aluno(), cadastrar_pagamento(), cadastrar_plano() (+45 more)

### Community 36 - "test_perfil_e_foto.py"
Cohesion: 0.16
Nodes (11): gerenciar_turmas(), remover_turma(), _turma_ou_404(), TurmaDAO, Turma, Cadastrar Turma Form, _imagem_jpeg_valida(), test_admin_acessa_foto_de_qualquer_aluno() (+3 more)

### Community 37 - "criar_aluno"
Cohesion: 0.05
Nodes (52): Uma página de alunos já cadastrados, recortada e filtrada pelo banco. O painel…, criar_aluno(), Sonda: a foto do aluno é resposta autenticada; um cache compartilhado não pode…, test_foto_do_aluno_nao_e_cacheavel_por_proxy(), test_aluno_existente_continua_entrando_normalmente(), test_area_do_aluno_renderiza_telas_independentes_do_menu(), test_plano_atual_continua_disponivel_para_gerar_cobranca(), test_aluno_ve_o_proprio_perfil() (+44 more)

### Community 38 - "Aluno"
Cohesion: 0.08
Nodes (16): _convidar_cadastro_existente(), _convidar_cadastro_existente_por_id(), Cadastro administrativo que alguém tentou recriar pelo formulário público. Em…, Versão para thread de fundo: a sessão da requisição não vale fora dela., Matrícula feita no balcão: sem login, sem senha e sem convite de acesso. Nasce…, Aluno, Se existe uma conta de acesso, e não se o aluno está em dia ou matriculado.…, Convite de acesso já enviado e ainda não usado (a validade é checada na rota). (+8 more)

### Community 41 - "Academia"
Cohesion: 0.13
Nodes (20): configuracoes(), _pagina(), route, editar_professor(), Academia, admin_requerido(), link_email(), Normalização de contatos profissionais antes de montar links públicos. (+12 more)

### Community 42 - "pagamento_polling.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 43 - "mercado_pago_conta.py"
Cohesion: 0.10
Nodes (37): ConfiguracaoInvalida, access_token_vigente(), _agora(), ambiente_da_conexao(), _cifrar(), _client_id(), _client_secret(), ConexaoIlegivel (+29 more)

### Community 44 - "test_checkout_rotas.py"
Cohesion: 0.13
Nodes (27): _mockar_preferencia(), parametrize, Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala…, _resposta_preferencia(), test_abertura_json_navega_sem_redirecionar_post_externo(), test_admin_tambem_pode_abrir_checkout(), test_aluno_cria_checkout_da_propria_mensalidade(), test_aluno_nao_cria_checkout_de_mensalidade_de_outro_aluno() (+19 more)

### Community 45 - "criar_pagamento"
Cohesion: 0.25
Nodes (21): criar_pagamento(), _assinar(), _resposta_consulta(), _resposta_criacao(), test_admin_tambem_pode_gerar_pix(), test_aluno_gera_pix_da_propria_mensalidade(), test_aluno_nao_acessa_mensalidade_de_outro_aluno(), test_falha_de_indisponibilidade_do_mp_retorna_503() (+13 more)

### Community 46 - ".buscar_por_id"
Cohesion: 0.21
Nodes (21): Hipótese: se a resposta do MP trouxer um destino estranho, ele é salvo e…, test_url_hostil_do_mercado_pago_nao_e_persistida(), _assinar(), _pagamento_mp(), _preparar_retorno(), Pix aberto e checkout concluído ao mesmo tempo: a consulta pelo…, test_retorno_com_aprovacao_confirmada_marca_pago(), test_retorno_com_mp_indisponivel_avisa_sem_mudar_status() (+13 more)

### Community 47 - "d9e2f6a14c80_contatos_academia_perfis_professores.py"
Cohesion: 0.83
Nodes (3): _campos_professor(), downgrade(), upgrade()

### Community 49 - "test_datas_turma.py"
Cohesion: 0.20
Nodes (11): desmatricular_aluno(), matricular_aluno(), MatriculaDAO, Presenca, Valor que representa a credencial administrativa em vigor, ou None se não há…, referencia_credencial_admin(), parametrize, test_consulta_com_data_invalida_exibe_hoje_e_aviso() (+3 more)

### Community 50 - "botao_ocupado.test.cjs"
Cohesion: 0.18
Nodes (7): assert, criarElemento(), fs, montar(), path, test, vm

### Community 51 - "test_seguranca.py"
Cohesion: 0.08
Nodes (22): test_upload_de_arquivo_disfarcado_e_recusado(), _cadastro_publico(), _imagem_jpeg(), _mensagem_da_resposta(), O `login` de um aluno pode ser o e-mail de outro; quem entra é decidido pela…, O ramo "par existe" não pode pagar a ida ao provedor dentro da requisição., Cadastro novo, CPF existente e e-mail existente respondem com a MESMA tela., Quem ainda controla a caixa antiga não pode assumir a conta depois da troca. (+14 more)

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
Cohesion: 0.13
Nodes (18): espera_da_proxima_tentativa(), Fila de e-mails no banco. Aviso e cobrança coletivos saíam um a um dentro da…, contar_falhados(), contar_pendentes(), enfileirar(), enfileirar_transacional(), _entregar(), listar_pendentes() (+10 more)

### Community 58 - "test_migracao_cadastro_administrativo.py"
Cohesion: 0.40
Nodes (3): banco_antigo(), fixture, Verifica a migração em um banco isolado com o schema anterior e dados.

### Community 59 - "salvar_foto_perfil"
Cohesion: 0.11
Nodes (26): enviar_comprovante_manual_aluno(), enviar_foto_perfil(), ArquivoInvalido, _conferir_dimensoes(), _detectar_tipo_imagem_real(), ImagemGrandeDemais, _pasta(), Exception (+18 more)

### Community 60 - "test_keep_alive.py"
Cohesion: 0.16
Nodes (7): ambiente_limpo(), fixture, parametrize, Garante que o keep-alive fica desligado por padrão e só pinga a própria origem., test_intervalo_fica_dentro_da_faixa(), test_nao_liga_com_valor_negativo(), test_ping_so_considera_200_como_sucesso()

### Community 61 - "convites.py"
Cohesion: 0.17
Nodes (15): aluno_do_token(), ConviteIndisponivel, descartar(), enviar(), gerar_token(), _hash(), RuntimeError, Convite de acesso: como um cadastro criado pela administração vira uma conta.… (+7 more)

### Community 62 - "logar_como_aluno"
Cohesion: 0.07
Nodes (31): logar_como_aluno(), Hipótese: cada clique cria uma cobrança nova no Mercado Pago., Hipótese: dá para injetar o valor pelo corpo do POST., Versão forte da sonda de IDOR: o alvo TEM arquivo, então um 200 seria vazamento., Verifica a trava antes da emissão e o reaproveitamento na próxima chamada.…, test_comprovante_de_outro_aluno_com_arquivo_real_nao_vaza(), test_dois_cliques_reaproveitam_a_mesma_preferencia(), test_pix_exige_trava_e_reutiliza_a_cobranca() (+23 more)

### Community 63 - "test_arranque_seguranca.py"
Cohesion: 0.22
Nodes (14): _env_arranque(), Validações feitas por servidor.py no arranque (COOKIE_SECURE, TRUSTED_HOSTS,…, `python -m servicos.credenciais`: o hash sai entre aspas simples. O hash do…, Desenvolvimento local sem HTTPS (sem Caddy) não pode ficar travado., _rodar(), test_arranque_falha_com_cookie_secure_false_e_app_base_url_https(), test_arranque_falha_com_cookie_secure_invalido(), test_arranque_falha_sem_trusted_hosts() (+6 more)

### Community 64 - "test_fila_email_concorrencia_postgres.py"
Cohesion: 0.18
Nodes (10): _enfileirar_em_transacao_propria(), postgres_fila(), fixture, Idempotência da fila de e-mail sob concorrência real, em PostgreSQL…, A recusa de uma chave repetida não pode desfazer o lote inteiro. Um…, A trava do lote precisa valer até o fim do lote. Comitar linha a linha…, Enfileira e comita numa sessão própria, como faria outra requisição., test_chave_duplicada_nao_descarta_os_outros_destinatarios_do_lote() (+2 more)

### Community 66 - "Pagamento"
Cohesion: 0.15
Nodes (10): forma_pagamento vem do que o Mercado Pago confirmou na consulta à API ('pix',…, Pagamento, Status a exibir, com o vencimento já aplicado. Uma cobrança `pendente` cujo…, test_marcar_pago_via_webhook_sincroniza_mensalidade_do_aluno(), parametrize, test_duas_requisicoes_pix_reutilizam_uma_cobranca_postgres(), Quem paga uma cobrança vencida há semanas tem de receber os 30 dias a partir da…, test_cobranca_antiga_quitada_hoje_abre_o_periodo_a_partir_de_hoje() (+2 more)

### Community 67 - "servidor.py"
Cohesion: 0.06
Nodes (41): after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, Flask App Service (compose), Postgres DB Service (compose), postgres_data Volume, context_processor, errorhandler (+33 more)

### Community 68 - "turma_bp.py"
Cohesion: 0.15
Nodes (23): _acesso_permitido(), cadastrar_turma(), detalhe_turma(), foto_professor(), painel_professor(), route, registrar_presenca(), PresencaDAO (+15 more)

### Community 69 - "_enviar_em_segundo_plano"
Cohesion: 0.50
Nodes (4): _em_segundo_plano(), _enviar_em_segundo_plano(), Roda `tarefa` fora da requisição, para o tempo de resposta não revelar nada. Em…, E-mail COM token (recuperação, confirmação): não pode ir para a `fila_email`. A…

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
Cohesion: 0.20
Nodes (7): Uma página de mensalidades, recortada pelo banco (LIMIT/OFFSET). O painel…, Totais do painel financeiro - sempre calculados no backend a partir do banco,…, Status como o painel deve LER, com o vencimento aplicado na própria consulta. A…, test_financeiro_pagina_no_banco_sem_carregar_tudo(), test_indicadores_e_tabela_concordam_na_primeira_abertura(), test_indicadores_saem_de_uma_consulta_de_agregacao(), test_totais_periodo_preserva_o_escopo_dos_filtros_de_data()

### Community 74 - "usuario_bp.py"
Cohesion: 0.13
Nodes (24): _acesso_permitido_pagamento(), _aluno_da_sessao(), cancelar_mudanca_plano(), comprovante_mensalidade(), foto_perfil(), _pagamento_com_acesso_ou_404(), pagina_pagamento(), pagina_termos_responsabilidade() (+16 more)

### Community 76 - "Pagina"
Cohesion: 0.14
Nodes (5): Pagina, Uma fatia de resultados já recortada pelo banco, com o que a navegação precisa., Uma página existe mesmo quando está vazia. Sem isto, `__len__` fazia `{% if…, `__len__` fazia `{% if pagina %}` ser falso numa página sem itens, escondendo…, test_pagina_vazia_ainda_mostra_a_navegacao()

### Community 77 - "_parece_busca_por_cpf"
Cohesion: 0.17
Nodes (12): _parece_busca_por_cpf(), O termo é um CPF, ou um pedaço dele, e não um nome que por acaso tem número?, parametrize, Qualquer dígito no termo virava `CPF LIKE '%3%'` e devolvia a academia inteira., Rotas que custam hash de senha, processamento de imagem ou sondagem de token., Limites declarados por decorador NAQUELA rota. `resolve_limits` não serve aqui:…, Guarda do teste acima: uma rota sem limite precisa ser reprovada por ele., _tem_limite() (+4 more)

### Community 81 - "Contrato do redesign — SistemaEXTREMETEAM"
Cohesion: 0.09
Nodes (20): 0. Antes de escrever código, 1. Identidade visual (design tokens), 2. Logo oficial (usar SOMENTE a logo original), 3. Telas a implementar, 4. Regras e dados, 5. Forma de trabalhar, Painel administrativo (desktop, sidebar preta com o emblema do dragão), Prompt para o Claude Code — Redesign do SistemaEXTREMETEAM (+12 more)

### Community 82 - "_chave_da_conta"
Cohesion: 0.40
Nodes (5): _chave_da_conta(), Chave de limite por CONTA, caindo no IP só para quem não está autenticado. A…, Alunos atrás do mesmo IP (o Wi-Fi da academia) não dividem a cota., test_limite_de_upload_e_por_conta_e_nao_por_ip(), test_visitante_sem_sessao_ainda_e_limitado_por_ip()

### Community 83 - "Relatório de segurança — Sistema Extreme Team (17/09/2026)"
Cohesion: 0.20
Nodes (10): A1 — `/recuperar_senha` revela por tempo de resposta se o CPF+e-mail existe (Média, CORRIGIDA em 19/09/2026), A2 — `/perfil/dados` sem limite de tentativas na senha atual (Baixa–Média, CORRIGIDA em 19/09/2026), A3 — `/perfil/dados` não valida tamanho de `nome`/`login`/`descricao` (Baixa, CORRIGIDA em 19/09/2026), A4 — Enumeração de usuário/e-mail no cadastro público (Baixa / informativa, CORRIGIDA em 19/09/2026 para CPF e e-mail), Housekeeping: `pip` desatualizado no ambiente virtual local (CORRIGIDO em 19/09/2026: pip 26.2.1), Ordem de correção sugerida (executada em 19/09/2026, ver a seção de atualização), Relatório de segurança — Sistema Extreme Team (17/09/2026), Situação dos 15 achados do relatório de 05/09 (revalidados hoje, código lido diretamente) (+2 more)

### Community 84 - "disparar"
Cohesion: 0.29
Nodes (7): disparar(), _laco(), _liberar_e_retomar_se_preciso(), Drena a fila enquanto houver entrega acontecendo. Encerra na primeira passada…, Desregistra a thread e sobe outra se alguém pediu trabalho durante a queda. Sem…, Acorda o processamento em segundo plano, sem bloquear a requisição. Se a thread…, test_reaciona_fila_sem_requisicao_e_sobrevive_a_falha()

### Community 85 - "test_professor_perfil.py"
Cohesion: 0.23
Nodes (10): _foto(), pasta_fotos(), fixture, parametrize, test_admin_salva_perfil_sem_alterar_acesso(), test_apenas_admin_edita_perfil(), test_contato_invalido_nao_salva_nenhuma_alteracao(), test_falha_ao_salvar_preserva_foto_anterior() (+2 more)

### Community 86 - "_png_bomba"
Cohesion: 0.29
Nodes (7): _png_bomba(), Bomba de descompressão: arquivo minúsculo, imagem gigante. O PNG aqui tem 285…, PNG válido e altamente compressível: linhas zeradas, como uma bomba real., O teto de pixels vale para a FOTO, que é decodificada, não para o comprovante.…, test_comprovante_a4_escaneado_continua_sendo_aceito(), test_foto_de_perfil_mantem_o_teto_de_pixels(), test_png_com_pixels_demais_e_recusado_pelo_cabecalho()

### Community 90 - "Atualização de 19/09/2026 — correções aplicadas e nova varredura"
Cohesion: 0.25
Nodes (8): Atualização de 19/09/2026 — correções aplicadas e nova varredura, Correções dos achados de 17/09, Nova varredura independente (19/09) — S1 e S2, Não alterado (decisão ou baixo valor), Reauditoria de 12/09 (itens de desempenho), Reforços em achados de 05/09 (F1–F15 seguem corrigidos), Revisão do fluxo OAuth do Mercado Pago (código novo da branch), Validação e implantação

### Community 94 - "Severidade BAIXA"
Cohesion: 0.29
Nodes (7): F10 — Redirecionamento aberto via `Referer`, F11 — `/logout` aceita GET, F12 — Enumeração de usuários por tempo de resposta, F13 — Senha mínima de 6 caracteres, sem outros critérios, F14 — Webhook sem verificação de recência do timestamp, F15 — Curinga de `LIKE` no filtro do financeiro, Severidade BAIXA

### Community 95 - "route"
Cohesion: 0.11
Nodes (31): alterar_senha_perfil(), _aluno_por_token(), ativar_acesso(), atualizar_dados_perfil(), confirmar_email(), pagina_cadastro(), pagina_login(), limit (+23 more)

### Community 96 - "test_mercado_pago_oauth_postgres.py"
Cohesion: 0.18
Nodes (8): postgres_mp(), fixture, Renovação do token OAuth com trava de linha real, opcional na suíte que usa…, _Resposta, test_dois_processos_perto_do_vencimento_gastam_o_refresh_token_uma_vez(), _migracao(), test_migracao_cria_a_tabela_igual_ao_modelo_e_e_reentrante(), test_migracao_encadeia_na_ultima_revisao_existente()

### Community 97 - "Relatório de segurança — Sistema Extreme Team"
Cohesion: 0.33
Nodes (6): A verificar em execução, Atualização após as correções, Ordem de correção sugerida, Relatório de segurança — Sistema Extreme Team, Sumário executivo, Verificado e correto

### Community 98 - "Severidade MÉDIA"
Cohesion: 0.33
Nodes (6): F5 — Sem limite de tamanho de requisição: negação de serviço por memória, F6 — Comprovante em PDF servido inline, F7 — Nenhum cabeçalho de segurança HTTP, F8 — Autenticação aceita campo não único e editável pelo usuário, F9 — Confiança em proxy não configurada, Severidade MÉDIA

### Community 99 - "Severidade ALTA"
Cohesion: 0.40
Nodes (5): F1 — Aluno consegue desviar a ficha administrativa de outro aluno, F2 — Ausência de proteção CSRF em 46 de 49 formulários, F3 — Sem limite de tentativas: força bruta na senha do administrador, F4 — Link de recuperação de senha montado a partir do cabeçalho `Host`, Severidade ALTA

### Community 100 - "conftest.py"
Cohesion: 0.27
Nodes (11): app(), client(), contexto_app(), limpar_banco(), logar_como_professor(), plano(), fixture, Substitui o provedor de e-mail em todos os módulos que o chamam. A suíte nunca… (+3 more)

### Community 101 - "enviar_email"
Cohesion: 0.24
Nodes (6): enviar_email(), _enviar_via_gmail(), _obter_token_gmail(), Envia e-mail transacional pela Gmail API. Retorna True/False; nunca lança., limpar_cache_token(), fixture

### Community 102 - "parametrize"
Cohesion: 0.25
Nodes (8): parametrize, Hipótese: dá para abrir um checkout novo sobre uma cobrança já resolvida., Hipótese: trocar o id na URL dá acesso à cobrança de outra pessoa., Hipótese: as rotas de cobrança respondem sem sessão nenhuma., test_aluno_nao_alcanca_cobranca_de_outro_aluno(), test_checkout_recusa_cobranca_indisponivel(), test_pix_recusa_cobranca_indisponivel(), test_visitante_sem_sessao_nao_alcanca_cobranca()

### Community 103 - "test_financeiro_admin_painel.py"
Cohesion: 0.33
Nodes (5): test_busca_financeira_trata_curingas_como_texto(), test_painel_financeiro_busca_por_nome_do_aluno(), test_painel_financeiro_exige_admin(), test_painel_financeiro_filtra_por_status(), test_painel_financeiro_mostra_totais_do_backend()

### Community 104 - "test_matricula_valida_dados_no_servidor"
Cohesion: 0.40
Nodes (5): parametrize, test_confirmacao_aceita_unicode(), test_matricula_valida_dados_no_servidor(), test_novos_formularios_exigem_csrf(), test_rotas_de_matricula_e_convite_sao_so_do_admin()

### Community 107 - "limites_pagamento.py"
Cohesion: 0.50
Nodes (3): chave_pagamento(), Orçamentos compartilhados das chamadas interativas ao provedor de pagamento., A mesma conta mantém seu limite entre sessões, rotas e mensalidades. Alunos que…

### Community 108 - "capturar_emails"
Cohesion: 0.67
Nodes (3): capturar_emails(), fixture, Intercepta o envio e devolve os e-mails que teriam saído, com os links.

## Knowledge Gaps
- **112 isolated node(s):** `modal`, `input_senha`, `icone_senha`, `campoDuracao`, `campoPreco` (+107 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PagamentoDAO` connect `PagamentoDAO` to `config.py`, `test_plano_vigencia.py`, `test_mudanca_plano.py`, `PagamentoEvento`, `test_auditoria_seguranca.py`, `pix_bp.py`, `logar_como_admin`, `checkout_bp.py`, `.contratar_plano`, `test_aprovacao_incoerente_nao_quita_mensalidade`, `adm_bp.py`, `Aluno`, `test_checkout_rotas.py`, `criar_pagamento`, `.buscar_por_id`, `test_seguranca.py`, `salvar_foto_perfil`, `logar_como_aluno`, `Pagamento`, `.totais_periodo`, `usuario_bp.py`, `test_financeiro_admin_painel.py`, `test_retorno_ignora_status_aprovado_da_query_string`?**
  _High betweenness centrality (0.133) - this node is a cross-community bridge._
- **Why does `logar_como_admin()` connect `logar_como_admin` to `test_plano_vigencia.py`, `test_limites_pagamento.py`, `test_mudanca_plano.py`, `test_mercado_pago_oauth.py`, `test_auditoria_seguranca.py`, `test_perfil_e_foto.py`, `criar_aluno`, `Aluno`, `Academia`, `test_checkout_rotas.py`, `criar_pagamento`, `test_datas_turma.py`, `test_seguranca.py`, `logar_como_aluno`, `servidor.py`, `.totais_periodo`, `test_professor_perfil.py`, `conftest.py`, `test_financeiro_admin_painel.py`, `test_matricula_valida_dados_no_servidor`, `test_trocar_a_credencial_do_admin_encerra_a_sessao_administrativa`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `criar_pagamento()` connect `criar_pagamento` to `test_aprovacao_incoerente_nao_quita_mensalidade`, `PagamentoDAO`, `Pagamento`, `conftest.py`, `test_limites_pagamento.py`, `parametrize`, `test_financeiro_admin_painel.py`, `PagamentoEvento`, `test_plano_vigencia.py`, `criar_aluno`, `test_auditoria_seguranca.py`, `test_checkout_rotas.py`, `test_retorno_ignora_status_aprovado_da_query_string`, `.buscar_por_id`, `.totais_periodo`, `logar_como_admin`, `logar_como_aluno`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Are the 125 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 125 INFERRED edges - model-reasoned connections that need verification._
- **Are the 137 inferred relationships involving `criar_pagamento()` (e.g. with `test_abrir_checkout_por_fetch_exige_csrf()` and `test_aluno_nao_alcanca_cobranca_de_outro_aluno()`) actually correct?**
  _`criar_pagamento()` has 137 INFERRED edges - model-reasoned connections that need verification._
- **Are the 125 inferred relationships involving `criar_aluno()` (e.g. with `test_aluno_nao_alcanca_cobranca_de_outro_aluno()` and `test_comprovante_de_outro_aluno_com_arquivo_real_nao_vaza()`) actually correct?**
  _`criar_aluno()` has 125 INFERRED edges - model-reasoned connections that need verification._
- **Are the 109 inferred relationships involving `logar_como_admin()` (e.g. with `test_admin_salva_atualiza_e_limpa_contatos()` and `test_csrf_configuracoes()`) actually correct?**
  _`logar_como_admin()` has 109 INFERRED edges - model-reasoned connections that need verification._