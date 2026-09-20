# Graph Report - SistemaEXTREMETEAM  (2026-09-19)

## Corpus Check
- 125 files · ~182,071 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1673 nodes · 4328 edges · 100 communities (84 shown, 16 thin omitted)
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 907 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d5a1b606`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- PagamentoDAO
- Aluno Profile Page
- .contratar_plano
- test_plano_vigencia.py
- test_limites_pagamento.py
- test_mudanca_plano.py
- PagamentoEvento
- Relatório de segurança — Sistema Extreme Team (17/09/2026)
- SistemaEXTREMETEAM Project
- test_mercado_pago_servico.py
- test_mercado_pago_oauth.py
- ProfessorDAO
- test_migracao_checkout.py
- checkout.js
- CLAUDE.md
- planos.py
- pix_bp.py
- logar_como_admin
- MercadoPagoIndisponivel
- checkout_bp.py
- pix.js
- config.py
- env.py
- pagamento.js
- c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py
- _FakePaymentResource
- 896e70afc9c5_adiciona_foto_e_graduacao_do_aluno_.py
- test_auditoria_seguranca.py
- mercado_pago.py
- adm_bp.py
- test_perfil_e_foto.py
- criar_aluno
- turma_bp.py
- Academia
- pagamento_polling.test.cjs
- mercado_pago_conta.py
- logar_como_aluno
- criar_pagamento
- .buscar_por_id
- d9e2f6a14c80_contatos_academia_perfis_professores.py
- Professor
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
- email_valido
- test_sessao_revogada.py
- test_arranque_seguranca.py
- .totais_periodo
- MatriculaDAO
- servidor.py
- autorizacao.py
- Flask App Service (compose)
- convites.py
- referencia_credencial_admin
- shot.mjs
- _pagamento_com_acesso_ou_404
- usuario_bp.py
- cancelar_mudanca_plano_admin
- _parece_busca_por_cpf
- e4b7c2a91d35_cadastro_administrativo_e_convite_de_acesso.py
- a1f0c3e75b92_schema_inicial.py
- Contrato do redesign — SistemaEXTREMETEAM
- _chave_da_conta
- Pagamento
- limites_pagamento.py
- test_uma_falha_do_provedor_nao_queima_todas_as_tentativas
- test_jpeg_grande_e_aceito_porque_decodifica_em_escala_reduzida
- test_linha_com_defeito_nao_trava_a_fila_atras_dela
- test_decodificacao_de_imagem_e_serializada_no_processo
- mensalidade_destaque
- _carregar_senhas_comuns
- test_a_suite_nunca_escreve_na_pasta_de_uploads_do_projeto
- test_o_mesmo_aviso_pode_ser_enviado_de_novo_em_outro_dia
- test_um_envio_ainda_pendente_continua_sendo_recusado
- test_retentativa_acontece_sem_ninguem_abrir_o_painel

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

## Communities (100 total, 16 thin omitted)

### Community 0 - "PagamentoDAO"
Cohesion: 0.10
Nodes (23): PagamentoDAO, Carrega aluno e plano junto das mensalidades. O template do painel lê…, Lista completa (sem paginar). Mantida para relatórios e testes., True se já existe um Pix ou um checkout válido emitido para esta cobrança.…, Mensalidades agrupadas por aluno numa consulta só. Usado pelas telas que…, True se a cobrança Pix já gerada para este pagamento ainda pode ser…, True se a preferência do Checkout Pro já criada pode ser reaproveitada. Só…, Solta a preferência atual para que a próxima tentativa crie uma nova. Nunca… (+15 more)

### Community 1 - "Aluno Profile Page"
Cohesion: 0.05
Nodes (36): abrirmodal(), fechar(), icone_senha, input_senha, modal, mostrarSenha(), campoDuracao, campoPreco (+28 more)

### Community 2 - ".contratar_plano"
Cohesion: 0.11
Nodes (10): O que aconteceu numa tentativa de contratar/renovar/trocar de plano., Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda. O…, Aplica um pedido agendado cujo período de origem já terminou sem renovação.…, Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, Com uma troca já agendada, só dois planos fazem sentido num pedido de…, A cobrança do período seguinte tem de nascer no plano que o aluno agendou.…, `pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -…, ResultadoContratacao (+2 more)

### Community 3 - "test_plano_vigencia.py"
Cohesion: 0.17
Nodes (23): _pagar(), plano_barato(), fixture, Vigência do plano: o que decide "Plano ativo" é o período pago, não o cadastro.…, Mensalidade paga cobrindo um período - o que de fato ativa o plano., test_acao_forjada_de_renovacao_sem_vigencia_apenas_contrata(), test_acao_invalida_no_formulario_cai_no_fluxo_de_contratacao(), test_admin_continua_podendo_trocar_o_plano_do_cadastro() (+15 more)

### Community 4 - "test_limites_pagamento.py"
Cohesion: 0.15
Nodes (16): consultar_mp(), fixture, parametrize, Limites de pagamento por conta, com o provedor inteiramente simulado., _sessao_admin(), _sessao_aluno(), test_admin_limite_por_usuario_persiste_entre_sessoes(), test_alunos_no_mesmo_ip_tem_limites_separados() (+8 more)

### Community 5 - "test_mudanca_plano.py"
Cohesion: 0.18
Nodes (25): Persistência dos pedidos de troca de plano agendados para a próxima renovação., Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, SolicitacaoPlanoDAO, _agendar(), _pagar(), plano_barato(), fixture, Mudança para um plano mais barato agendada para a próxima renovação. Regra… (+17 more)

### Community 6 - "PagamentoEvento"
Cohesion: 0.12
Nodes (12): Primeiro dia não coberto por outra mensalidade do mesmo aluno., Define o período coberto por uma mensalidade que ainda não tem um (lançamento…, Abre o período de acesso no momento em que o pagamento é confirmado. Se a…, Reescreve os campos denormalizados do aluno a partir das mensalidades.…, forma_pagamento vem do que o Mercado Pago confirmou na consulta à API ('pix',…, Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.…, PagamentoEvento, Histórico de auditoria de uma mensalidade (nunca grava credenciais ou dados… (+4 more)

### Community 7 - "Relatório de segurança — Sistema Extreme Team (17/09/2026)"
Cohesion: 0.05
Nodes (38): Achados, Medições locais, Reavaliação de segurança e desempenho — 12/09/2026, Validação e limites, A verificar em execução, Atualização após as correções, F10 — Redirecionamento aberto via `Referer`, F11 — `/logout` aceita GET (+30 more)

### Community 9 - "test_mercado_pago_servico.py"
Cohesion: 0.11
Nodes (28): Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, validar_assinatura_webhook(), Hipótese: uma notificação capturada ontem pode ser reenviada hoje., `ts=nan` fazia a comparação da janela dar False e passava pela checagem de…, test_webhook_recusa_assinatura_antiga(), test_webhook_recusa_ts_nao_numerico_finito(), base_url(), _criar_preferencia() (+20 more)

### Community 10 - "test_mercado_pago_oauth.py"
Cohesion: 0.05
Nodes (68): MercadoPagoConexao, Conta do Mercado Pago que a academia autorizou por OAuth. Uma linha só (a…, _agora(), _ajustar(), api_mp(), _conectar(), _dados_conexao(), oauth_env() (+60 more)

### Community 11 - "ProfessorDAO"
Cohesion: 0.13
Nodes (24): remover_professor(), ProfessorDAO, impressao_credencial(), Resumo curto e não reversível do hash da senha, guardado na sessão. Nunca é a…, Hipótese: a foto continua acessível por URL depois de tirar a publicação., Hipótese: os contatos vazam na home antes de a publicação ser marcada., test_contatos_do_professor_so_aparecem_quando_publicados(), test_foto_do_professor_some_ao_despublicar() (+16 more)

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
Cohesion: 0.14
Nodes (23): _acesso_permitido(), criar_pix_mensalidade(), _forma_pagamento_confirmada(), _pagamento_mp_mais_relevante(), _pagamento_ou_none(), _pix_expirado(), _processar_status_mp(), limitar_consulta_pagamento (+15 more)

### Community 18 - "logar_como_admin"
Cohesion: 0.06
Nodes (71): _convidar_cadastro_existente(), Cadastro administrativo que alguém tentou recriar pelo formulário público. Em…, AlunoDAO, Matrícula feita no balcão: sem login, sem senha e sem convite de acesso. Nasce…, Quantos alunos a academia tem, sem filtro de busca. O card do topo do painel é…, Aluno, Se existe uma conta de acesso, e não se o aluno está em dia ou matriculado.…, Convite de acesso já enviado e ainda não usado (a validade é checada na rota). (+63 more)

### Community 19 - "MercadoPagoIndisponivel"
Cohesion: 0.12
Nodes (21): webhook_mercado_pago(), Acha a mensalidade por qualquer uma das duas referências persistidas. O Pix…, exempt, buscar_pagamento(), buscar_pagamentos_por_referencia(), cancelar_pagamento(), MercadoPagoIndisponivel, Exception (+13 more)

### Community 20 - "checkout_bp.py"
Cohesion: 0.12
Nodes (27): abrir_checkout(), _acesso_permitido(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), limitar_consulta_pagamento, limitar_criacao_pagamento, route (+19 more)

### Community 21 - "pix.js"
Cohesion: 0.33
Nodes (14): abrirPix(), alvoDoRotulo(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), liberarBotao(), limparConteudoAnterior() (+6 more)

### Community 22 - "config.py"
Cohesion: 0.06
Nodes (30): Pagina, _paginar(), Uma fatia de resultados já recortada pelo banco, com o que a navegação precisa., Uma página existe mesmo quando está vazia. Sem isto, `__len__` fazia `{% if…, Aplica LIMIT/OFFSET e conta o total numa consulta separada e barata. A contagem…, Decimal, Matricula, _para_decimal() (+22 more)

### Community 23 - "env.py"
Cohesion: 0.39
Nodes (7): get_engine(), get_engine_url(), get_metadata(), Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online()

### Community 24 - "pagamento.js"
Cohesion: 0.47
Nodes (9): alvoDoRotulo(), consultarStatus(), gerarOuAtualizarPix(), iniciarPolling(), liberarBotao(), marcarOcupado(), mostrarEstado(), pararPolling() (+1 more)

### Community 25 - "c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py"
Cohesion: 0.60
Nodes (5): _backfill_vigencia(), _colunas(), _criar_tabela_solicitacoes(), downgrade(), upgrade()

### Community 29 - "896e70afc9c5_adiciona_foto_e_graduacao_do_aluno_.py"
Cohesion: 0.60
Nodes (3): _e_decimal(), _faltantes(), upgrade()

### Community 33 - "test_auditoria_seguranca.py"
Cohesion: 0.06
Nodes (46): _assinar(), _pagamento_mp(), _preparar_para_conciliacao(), parametrize, Auditoria de segurança: sondas escritas para TENTAR quebrar as regras. Nenhum…, Hipótese: a sessão de professor é aceita nas rotas financeiras do aluno., Hipótese: como o JS agora usa fetch, o POST perdeu a exigência de CSRF., Hipótese: as demais rotas de dinheiro aceitam POST sem token. (+38 more)

### Community 34 - "mercado_pago.py"
Cohesion: 0.15
Nodes (22): _base_url_opcional(), base_url_publica(), criar_pagamento_pix(), criar_preferencia_checkout(), _erro_menciona(), _erro_menciona_expiracao(), _extrair_dados_pix(), _normalizar_pagamento() (+14 more)

### Community 35 - "adm_bp.py"
Cohesion: 0.09
Nodes (47): _aluno_do_cpf_ou_painel(), aprovar_aluno(), aprovar_comprovante_manual(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_aluno(), cadastrar_plano(), _chave_lote() (+39 more)

### Community 36 - "test_perfil_e_foto.py"
Cohesion: 0.15
Nodes (14): TurmaDAO, Turma, Cadastrar Turma Form, Sonda: a data vem da query string e é convertida sem tratamento., test_data_invalida_na_turma_nao_derruba_a_rota(), fixture, test_consulta_com_data_valida_preserva_data_selecionada(), turma() (+6 more)

### Community 37 - "criar_aluno"
Cohesion: 0.06
Nodes (45): Uma página de alunos já cadastrados, recortada e filtrada pelo banco. O painel…, criar_aluno(), test_aluno_existente_continua_entrando_normalmente(), test_area_do_aluno_renderiza_telas_independentes_do_menu(), test_plano_atual_continua_disponivel_para_gerar_cobranca(), test_aluno_ve_o_proprio_perfil(), test_admin_pode_remover_o_plano_do_cadastro(), test_plano_inexistente_no_cadastro_e_recusado() (+37 more)

### Community 38 - "turma_bp.py"
Cohesion: 0.21
Nodes (16): configuracoes(), _pagina(), route, cadastrar_professor(), cadastrar_turma(), desmatricular_aluno(), editar_professor(), gerenciar_turmas() (+8 more)

### Community 41 - "Academia"
Cohesion: 0.18
Nodes (10): Academia, parametrize, test_admin_salva_atualiza_e_limpa_contatos(), test_configuracoes_exigem_admin(), test_contatos_invalidos(), test_csrf_configuracoes(), test_erro_preserva_formulario_e_dados_salvos(), test_link_email_preserva_caracteres_do_endereco() (+2 more)

### Community 42 - "pagamento_polling.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 43 - "mercado_pago_conta.py"
Cohesion: 0.10
Nodes (35): access_token_vigente(), _agora(), ambiente_da_conexao(), _cifrar(), _client_id(), _client_secret(), ConexaoIlegivel, _decifrar() (+27 more)

### Community 44 - "logar_como_aluno"
Cohesion: 0.09
Nodes (45): logar_como_aluno(), Hipótese: forjar ?status=approved na volta do MP quita a mensalidade., test_retorno_ignora_status_aprovado_da_query_string(), _mockar_preferencia(), parametrize, Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala…, Um boleto pendente do Checkout Pro grava provider_payment_id, mas não é Pix:…, _resposta_preferencia() (+37 more)

### Community 45 - "criar_pagamento"
Cohesion: 0.25
Nodes (21): criar_pagamento(), _assinar(), _resposta_consulta(), _resposta_criacao(), test_admin_tambem_pode_gerar_pix(), test_aluno_gera_pix_da_propria_mensalidade(), test_aluno_nao_acessa_mensalidade_de_outro_aluno(), test_falha_de_indisponibilidade_do_mp_retorna_503() (+13 more)

### Community 46 - ".buscar_por_id"
Cohesion: 0.16
Nodes (26): _assinar(), _pagamento_mp(), _preparar_retorno(), Pix aberto e checkout concluído ao mesmo tempo: a consulta pelo…, test_retorno_com_aprovacao_confirmada_marca_pago(), test_retorno_com_mp_indisponivel_avisa_sem_mudar_status(), test_retorno_de_boleto_avisa_sobre_o_prazo(), test_retorno_de_sucesso_nao_marca_pago_sem_confirmacao() (+18 more)

### Community 47 - "d9e2f6a14c80_contatos_academia_perfis_professores.py"
Cohesion: 0.83
Nodes (3): _campos_professor(), downgrade(), upgrade()

### Community 49 - "Professor"
Cohesion: 0.18
Nodes (5): Professor, link_email(), Cadastrar Professor Form, logar_como_professor(), fixture

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
Cohesion: 0.06
Nodes (40): EmailPendente, espera_da_proxima_tentativa(), Fila de e-mails no banco. Aviso e cobrança coletivos saíam um a um dentro da…, contar_falhados(), contar_pendentes(), disparar(), enfileirar(), enfileirar_transacional() (+32 more)

### Community 58 - "test_migracao_cadastro_administrativo.py"
Cohesion: 0.40
Nodes (3): banco_antigo(), fixture, Verifica a migração em um banco isolado com o schema anterior e dados.

### Community 59 - "salvar_foto_perfil"
Cohesion: 0.11
Nodes (29): enviar_foto_aluno(), remover_foto_aluno(), ArquivoInvalido, caminho_arquivo(), _conferir_dimensoes(), _detectar_tipo_imagem_real(), ImagemGrandeDemais, _pasta() (+21 more)

### Community 60 - "test_keep_alive.py"
Cohesion: 0.16
Nodes (7): ambiente_limpo(), fixture, parametrize, Garante que o keep-alive fica desligado por padrão e só pinga a própria origem., test_intervalo_fica_dentro_da_faixa(), test_nao_liga_com_valor_negativo(), test_ping_so_considera_200_como_sucesso()

### Community 61 - "email_valido"
Cohesion: 0.40
Nodes (4): email_valido(), enviar_email(), Validação sintática básica, compartilhada pelos formulários do cadastro., Envia um e-mail transacional via Brevo. Retorna True/False; nunca lança.

### Community 62 - "test_sessao_revogada.py"
Cohesion: 0.24
Nodes (11): Sessões encerradas pelo logout. A sessão do Flask é um cookie assinado, sem…, SessaoRevogada, _cliente_com_cookie(), _entrar_como_admin(), `session.clear()` só limpava o navegador de quem saiu; a cópia do cookie seguia…, test_logout_apaga_revogacoes_vencidas(), test_logout_de_uma_sessao_nao_derruba_as_outras(), test_logout_revoga_a_copia_do_cookie_feita_antes() (+3 more)

### Community 63 - "test_arranque_seguranca.py"
Cohesion: 0.22
Nodes (14): _env_arranque(), Validações feitas por servidor.py no arranque (COOKIE_SECURE, TRUSTED_HOSTS,…, `python -m servicos.credenciais`: o hash sai entre aspas simples. O hash do…, Desenvolvimento local sem HTTPS (sem Caddy) não pode ficar travado., _rodar(), test_arranque_falha_com_cookie_secure_false_e_app_base_url_https(), test_arranque_falha_com_cookie_secure_invalido(), test_arranque_falha_sem_trusted_hosts() (+6 more)

### Community 64 - ".totais_periodo"
Cohesion: 0.20
Nodes (7): Uma página de mensalidades, recortada pelo banco (LIMIT/OFFSET). O painel…, Totais do painel financeiro - sempre calculados no backend a partir do banco,…, Status como o painel deve LER, com o vencimento aplicado na própria consulta. A…, test_financeiro_pagina_no_banco_sem_carregar_tudo(), test_indicadores_e_tabela_concordam_na_primeira_abertura(), test_indicadores_saem_de_uma_consulta_de_agregacao(), test_totais_periodo_preserva_o_escopo_dos_filtros_de_data()

### Community 66 - "MatriculaDAO"
Cohesion: 0.15
Nodes (13): _acesso_permitido(), detalhe_turma(), matricular_aluno(), registrar_presenca(), _turma_ou_404(), MatriculaDAO, PresencaDAO, Presenca (+5 more)

### Community 67 - "servidor.py"
Cohesion: 0.11
Nodes (21): after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, context_processor, errorhandler, Registra a sessão como encerrada: cópias antigas do cookie deixam de valer.…, revogar_sessao_atual(), formatar_moeda() (+13 more)

### Community 68 - "autorizacao.py"
Cohesion: 0.18
Nodes (17): foto_professor(), aluno_autorizado(), aluno_requerido(), _credencial_confere(), encerrar_sessao(), professor_autorizado(), Autorização das rotas protegidas. A sessão diz quem *afirmou* ser quem; quem…, Grava na sessão atual a credencial em vigor (login ou troca de senha bem-… (+9 more)

### Community 69 - "Flask App Service (compose)"
Cohesion: 0.22
Nodes (9): Flask App Service (compose), Postgres DB Service (compose), postgres_data Volume, Flask, Flask-SQLAlchemy, Gunicorn, psycopg2-binary, python-dotenv (+1 more)

### Community 70 - "convites.py"
Cohesion: 0.11
Nodes (27): aluno_do_token(), ConviteIndisponivel, descartar(), enviar(), gerar_token(), _hash(), RuntimeError, Convite de acesso: como um cadastro criado pela administração vira uma conta.… (+19 more)

### Community 71 - "referencia_credencial_admin"
Cohesion: 0.16
Nodes (13): admin_configurado(), comparar_em_tempo_constante(), credencial_admin_confere(), gerar_hash_admin(), _main(), Credencial administrativa baseada exclusivamente em hash de senha. O…, Compara duas senhas em tempo constante, sem restrição de alfabeto. Codificar…, True quando existe usuário e hash da senha do administrador. (+5 more)

### Community 72 - "shot.mjs"
Cohesion: 0.29
Nodes (5): { chromium }, contextos, CREDS, jobs, require

### Community 73 - "_pagamento_com_acesso_ou_404"
Cohesion: 0.43
Nodes (7): _acesso_permitido_pagamento(), comprovante_mensalidade(), _pagamento_com_acesso_ou_404(), pagina_pagamento(), Há alguém autorizado a ver mensalidades nesta sessão (admin ou aluno ativo)?, _sessao_financeira_valida(), ver_comprovante_manual()

### Community 74 - "usuario_bp.py"
Cohesion: 0.10
Nodes (43): alterar_senha_perfil(), _aluno_da_sessao(), _aluno_por_token(), ativar_acesso(), atualizar_dados_perfil(), confirmar_email(), _convidar_cadastro_existente_por_id(), _em_segundo_plano() (+35 more)

### Community 76 - "cancelar_mudanca_plano_admin"
Cohesion: 0.40
Nodes (4): cancelar_mudanca_plano_admin(), A administração pode cancelar um pedido de troca ainda não aplicado. Não existe…, cancelar_mudanca_plano(), Cancela um pedido de troca antes de ele ser aplicado. Depois de efetivado não…

### Community 77 - "_parece_busca_por_cpf"
Cohesion: 0.17
Nodes (12): _parece_busca_por_cpf(), O termo é um CPF, ou um pedaço dele, e não um nome que por acaso tem número?, parametrize, Qualquer dígito no termo virava `CPF LIKE '%3%'` e devolvia a academia inteira., Rotas que custam hash de senha, processamento de imagem ou sondagem de token., Limites declarados por decorador NAQUELA rota. `resolve_limits` não serve aqui:…, Guarda do teste acima: uma rota sem limite precisa ser reprovada por ele., _tem_limite() (+4 more)

### Community 81 - "Contrato do redesign — SistemaEXTREMETEAM"
Cohesion: 0.09
Nodes (20): 0. Antes de escrever código, 1. Identidade visual (design tokens), 2. Logo oficial (usar SOMENTE a logo original), 3. Telas a implementar, 4. Regras e dados, 5. Forma de trabalhar, Painel administrativo (desktop, sidebar preta com o emblema do dragão), Prompt para o Claude Code — Redesign do SistemaEXTREMETEAM (+12 more)

### Community 82 - "_chave_da_conta"
Cohesion: 0.40
Nodes (5): _chave_da_conta(), Chave de limite por CONTA, caindo no IP só para quem não está autenticado. A…, Alunos atrás do mesmo IP (o Wi-Fi da academia) não dividem a cota., test_limite_de_upload_e_por_conta_e_nao_por_ip(), test_visitante_sem_sessao_ainda_e_limitado_por_ip()

### Community 83 - "Pagamento"
Cohesion: 0.20
Nodes (6): cadastrar_pagamento(), Pagamento, Status a exibir, com o vencimento já aplicado. Uma cobrança `pendente` cujo…, Quem paga uma cobrança vencida há semanas tem de receber os 30 dias a partir da…, test_cobranca_antiga_quitada_hoje_abre_o_periodo_a_partir_de_hoje(), cobranca()

### Community 84 - "limites_pagamento.py"
Cohesion: 0.50
Nodes (3): chave_pagamento(), Orçamentos compartilhados das chamadas interativas ao provedor de pagamento., A mesma conta mantém seu limite entre sessões, rotas e mensalidades. Alunos que…

## Knowledge Gaps
- **91 isolated node(s):** `modal`, `input_senha`, `icone_senha`, `formularioPlano`, `campoPreco` (+86 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PagamentoDAO` connect `PagamentoDAO` to `.contratar_plano`, `test_plano_vigencia.py`, `test_mudanca_plano.py`, `PagamentoEvento`, `pix_bp.py`, `logar_como_admin`, `MercadoPagoIndisponivel`, `checkout_bp.py`, `config.py`, `test_auditoria_seguranca.py`, `adm_bp.py`, `criar_aluno`, `logar_como_aluno`, `criar_pagamento`, `.buscar_por_id`, `test_seguranca.py`, `.totais_periodo`, `_pagamento_com_acesso_ou_404`, `usuario_bp.py`, `Pagamento`?**
  _High betweenness centrality (0.178) - this node is a cross-community bridge._
- **Why does `AlunoDAO` connect `logar_como_admin` to `PagamentoDAO`, `MatriculaDAO`, `adm_bp.py`, `test_perfil_e_foto.py`, `criar_aluno`, `turma_bp.py`, `usuario_bp.py`, `cancelar_mudanca_plano_admin`, `Pagamento`, `test_seguranca.py`, `config.py`, `salvar_foto_perfil`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Why does `Aluno` connect `logar_como_admin` to `PagamentoDAO`, `adm_bp.py`, `autorizacao.py`, `criar_aluno`, `convites.py`, `usuario_bp.py`, `test_seguranca.py`, `config.py`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Are the 131 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 131 INFERRED edges - model-reasoned connections that need verification._
- **Are the 139 inferred relationships involving `criar_pagamento()` (e.g. with `PagamentoDAO` and `Pagamento`) actually correct?**
  _`criar_pagamento()` has 139 INFERRED edges - model-reasoned connections that need verification._
- **Are the 127 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 127 INFERRED edges - model-reasoned connections that need verification._
- **Are the 109 inferred relationships involving `logar_como_admin()` (e.g. with `test_admin_salva_atualiza_e_limpa_contatos()` and `test_csrf_configuracoes()`) actually correct?**
  _`logar_como_admin()` has 109 INFERRED edges - model-reasoned connections that need verification._