# Graph Report - SistemaEXTREMETEAM  (2026-09-06)

## Corpus Check
- 86 files · ~136,084 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1056 nodes · 2749 edges · 58 communities (51 shown, 7 thin omitted)
- Extraction: 80% EXTRACTED · 20% INFERRED · 0% AMBIGUOUS · INFERRED: 563 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4d0a2998`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_perfil_e_foto.py
- Aluno Profile Page
- adm_bp.py
- criar_aluno
- criar_pagamento
- servidor.py
- PagamentoDAO
- Relatório de segurança — Sistema Extreme Team
- SistemaEXTREMETEAM Project
- test_mercado_pago_servico.py
- test_mudanca_plano.py
- professor.py
- test_migracao_checkout.py
- checkout.js
- CLAUDE.md
- planos.py
- pix_bp.py
- PagamentoEvento
- _FakePreferenceResource
- checkout_bp.py
- pix.js
- usuario_bp.py
- env.py
- pagamento.js
- c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py
- _FakePaymentResource
- test_auditoria_seguranca.py
- mercado_pago.py
- buscar_pagamento
- logar_como_admin
- test_academia.py
- turma_bp.py
- Professor
- pagamento_polling.test.cjs
- .contratar_plano
- test_checkout_rotas.py
- test_pix_rotas.py
- .buscar_por_id
- d9e2f6a14c80_contatos_academia_perfis_professores.py
- presencaDAO.py
- botao_ocupado.test.cjs
- ambiente_mercado_pago
- checkout_abertura.test.cjs
- filtros_financeiro.js
- SolicitacaoMudancaPlano
- limites_pagamento.py
- xfail

## God Nodes (most connected - your core abstractions)
1. `PagamentoDAO` - 175 edges
2. `criar_pagamento()` - 129 edges
3. `logar_como_aluno()` - 101 edges
4. `criar_aluno()` - 80 edges
5. `AlunoDAO` - 40 edges
6. `logar_como_admin()` - 36 edges
7. `Professor` - 23 edges
8. `SolicitacaoPlanoDAO` - 22 edges
9. `_pagar()` - 21 edges
10. `usuario_e_admin()` - 21 edges

## Surprising Connections (you probably didn't know these)
- `Cadastrar Plano Form` --shares_data_with--> `Plano`  [INFERRED]
  templates/pgAdm.html → modelos/plano.py
- `Planos Disponíveis Section` --shares_data_with--> `Plano`  [INFERRED]
  templates/pgUsuario.html → modelos/plano.py
- `Histórico de Mensalidades Section` --shares_data_with--> `Pagamento`  [INFERRED]
  templates/pgUsuario.html → modelos/pagamento.py
- `Turma Detail Page` --shares_data_with--> `Turma`  [INFERRED]
  templates/turma.html → modelos/turma.py
- `Aluno Mensalidade Launch Form` --shares_data_with--> `Pagamento`  [INFERRED]
  templates/dt_aluno.html → modelos/pagamento.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Shared Confirmation Modal Pattern** — templates_components_confirm_modal_dialog, templates_pgadm_page, templates_pgprofessor_page, templates_pgusuario_page, templates_turmas_page [EXTRACTED 1.00]
- **Mensalidade (Billing) Management Flow** — templates_dt_aluno_pagamento_form, templates_pgusuario_mensalidades_section, modelos_pagamento_pagamento, modelos_plano_plano [INFERRED 0.85]
- **Turma and Attendance Management Flow** — templates_turmas_turma_form, templates_turma_presenca_form, templates_pgprofessor_page, modelos_turma_turma [INFERRED 0.85]

## Communities (58 total, 7 thin omitted)

### Community 0 - "test_perfil_e_foto.py"
Cohesion: 0.21
Nodes (10): Turma, Cadastrar Turma Form, _imagem_jpeg_valida(), test_admin_acessa_foto_de_qualquer_aluno(), test_aluno_nao_acessa_foto_de_outro_aluno(), test_aluno_ve_o_proprio_perfil(), test_professor_ve_foto_de_aluno_da_propria_turma(), test_substituir_e_remover_foto() (+2 more)

### Community 1 - "Aluno Profile Page"
Cohesion: 0.05
Nodes (44): Usuario Model, Extreme Team Logo Image, Academia do Bitelo Logo, abrirmodal(), fechar(), icone_senha, input_senha, modal (+36 more)

### Community 2 - "adm_bp.py"
Cohesion: 0.06
Nodes (60): aprovar_aluno(), aprovar_comprovante_manual(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_pagamento(), cadastrar_plano(), cancelar_mudanca_plano_admin(), cobrar_inadimplentes() (+52 more)

### Community 3 - "criar_aluno"
Cohesion: 0.14
Nodes (35): Pagamento, criar_aluno(), test_area_do_aluno_renderiza_telas_independentes_do_menu(), test_escolher_plano_cria_mensalidade_e_redireciona_para_pix(), test_perfil_so_autoriza_abertura_automatica_da_propria_mensalidade(), test_plano_atual_continua_disponivel_para_gerar_cobranca(), test_plano_invalido_nao_cria_mensalidade(), test_reenvio_da_contratacao_reutiliza_mensalidade() (+27 more)

### Community 4 - "criar_pagamento"
Cohesion: 0.08
Nodes (49): criar_pagamento(), logar_como_aluno(), Hipótese: se a resposta do MP trouxer um destino estranho, ele é salvo e…, Hipótese: cada clique cria uma cobrança nova no Mercado Pago., Hipótese: dá para injetar o valor pelo corpo do POST., Verifica a trava antes da emissão e o reaproveitamento na próxima chamada.…, test_dois_cliques_reaproveitam_a_mesma_preferencia(), test_pix_exige_trava_e_reutiliza_a_cobranca() (+41 more)

### Community 5 - "servidor.py"
Cohesion: 0.08
Nodes (28): after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, Flask App Service (compose), Postgres DB Service (compose), postgres_data Volume, context_processor, errorhandler (+20 more)

### Community 6 - "PagamentoDAO"
Cohesion: 0.11
Nodes (20): PagamentoDAO, True se já existe um Pix ou um checkout válido emitido para esta cobrança.…, `pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -…, Mensalidades agrupadas por aluno numa consulta só. Usado pelas telas que…, True se a cobrança Pix já gerada para este pagamento ainda pode ser…, True se a preferência do Checkout Pro já criada pode ser reaproveitada. Só…, Solta a preferência atual para que a próxima tentativa crie uma nova. Nunca…, Totais do painel financeiro - sempre calculados no backend a partir do banco,… (+12 more)

### Community 7 - "Relatório de segurança — Sistema Extreme Team"
Cohesion: 0.08
Nodes (24): A verificar em execução, Atualização após as correções, F10 — Redirecionamento aberto via `Referer`, F11 — `/logout` aceita GET, F12 — Enumeração de usuários por tempo de resposta, F13 — Senha mínima de 6 caracteres, sem outros critérios, F14 — Webhook sem verificação de recência do timestamp, F15 — Curinga de `LIKE` no filtro do financeiro (+16 more)

### Community 9 - "test_mercado_pago_servico.py"
Cohesion: 0.14
Nodes (25): Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, validar_assinatura_webhook(), base_url(), _criar_preferencia(), mp_fake(), fixture, parametrize, _resposta_preferencia() (+17 more)

### Community 10 - "test_mudanca_plano.py"
Cohesion: 0.21
Nodes (22): Persistência dos pedidos de troca de plano agendados para a próxima renovação., SolicitacaoPlanoDAO, _agendar(), _pagar(), Mudança para um plano mais barato agendada para a próxima renovação. Regra…, O admin pode estornar/cancelar a mensalidade que sustentava a vigência depois…, test_admin_cancela_a_solicitacao(), test_aluno_cancela_a_solicitacao_antes_da_efetivacao() (+14 more)

### Community 11 - "professor.py"
Cohesion: 0.17
Nodes (8): MatriculaDAO, Matricula, parametrize, test_consulta_com_data_invalida_exibe_hoje_e_aviso(), test_consulta_com_data_valida_preserva_data_selecionada(), test_data_invalida_nao_contorna_permissoes(), test_presenca_com_data_invalida_nao_grava(), test_presenca_com_data_valida_continua_disponivel()

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
Cohesion: 0.13
Nodes (25): _acesso_permitido(), criar_pix_mensalidade(), _forma_pagamento_confirmada(), _pagamento_mp_mais_relevante(), _pagamento_ou_none(), _pix_expirado(), _processar_status_mp(), limitar_consulta_pagamento (+17 more)

### Community 18 - "PagamentoEvento"
Cohesion: 0.11
Nodes (12): Primeiro dia não coberto por outra mensalidade do mesmo aluno., Define o período coberto por uma mensalidade que ainda não tem um (lançamento…, Abre o período de acesso no momento em que o pagamento é confirmado. Se a…, Reescreve os campos denormalizados do aluno a partir das mensalidades.…, forma_pagamento vem do que o Mercado Pago confirmou na consulta à API ('pix',…, Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.…, PagamentoEvento, Histórico de auditoria de uma mensalidade (nunca grava credenciais ou dados… (+4 more)

### Community 20 - "checkout_bp.py"
Cohesion: 0.12
Nodes (23): abrir_checkout(), _acesso_permitido(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), limitar_consulta_pagamento, limitar_criacao_pagamento, route (+15 more)

### Community 21 - "pix.js"
Cohesion: 0.33
Nodes (14): abrirPix(), alvoDoRotulo(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), liberarBotao(), limparConteudoAnterior() (+6 more)

### Community 22 - "usuario_bp.py"
Cohesion: 0.05
Nodes (63): _acesso_permitido_pagamento(), alterar_senha_perfil(), _aluno_da_sessao(), atualizar_dados_perfil(), cancelar_mudanca_plano(), comprovante_mensalidade(), confirmar_email(), enviar_comprovante_manual_aluno() (+55 more)

### Community 23 - "env.py"
Cohesion: 0.39
Nodes (7): get_engine(), get_engine_url(), get_metadata(), Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online()

### Community 24 - "pagamento.js"
Cohesion: 0.47
Nodes (9): alvoDoRotulo(), consultarStatus(), gerarOuAtualizarPix(), iniciarPolling(), liberarBotao(), marcarOcupado(), mostrarEstado(), pararPolling() (+1 more)

### Community 25 - "c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py"
Cohesion: 0.60
Nodes (5): _backfill_vigencia(), _colunas(), _criar_tabela_solicitacoes(), downgrade(), upgrade()

### Community 33 - "test_auditoria_seguranca.py"
Cohesion: 0.07
Nodes (39): _assinar(), logar_como_professor(), _pagamento_mp(), _preparar_para_conciliacao(), fixture, parametrize, Auditoria de segurança: sondas escritas para TENTAR quebrar as regras. Nenhum…, Hipótese: a sessão de professor é aceita nas rotas financeiras do aluno. (+31 more)

### Community 34 - "mercado_pago.py"
Cohesion: 0.12
Nodes (29): _base_url_opcional(), base_url_publica(), buscar_pagamentos_por_referencia(), cancelar_pagamento(), criar_pagamento_pix(), criar_preferencia_checkout(), _erro_menciona(), _erro_menciona_expiracao() (+21 more)

### Community 35 - "buscar_pagamento"
Cohesion: 0.40
Nodes (5): buscar_pagamento(), Consulta o pagamento diretamente na API do Mercado Pago - fonte de verdade de…, test_buscar_pagamento_expoe_meio_de_pagamento_e_moeda(), test_buscar_pagamento_falha_de_transporte_levanta_indisponivel(), test_buscar_pagamento_sucesso()

### Community 36 - "logar_como_admin"
Cohesion: 0.13
Nodes (22): ProfessorDAO, logar_como_admin(), test_busca_financeira_trata_curingas_como_texto(), test_painel_financeiro_busca_por_nome_do_aluno(), test_painel_financeiro_exige_admin(), test_painel_financeiro_filtra_por_status(), test_painel_financeiro_mostra_totais_do_backend(), test_admin_cobra_aluno_com_mensalidade_vencida() (+14 more)

### Community 37 - "test_academia.py"
Cohesion: 0.13
Nodes (18): configuracoes(), route, editar_professor(), Academia, admin_requerido(), link_email(), Normalização de contatos profissionais antes de montar links públicos., validar_email() (+10 more)

### Community 38 - "turma_bp.py"
Cohesion: 0.19
Nodes (17): admin_requerido, _acesso_permitido(), cadastrar_professor(), cadastrar_turma(), desmatricular_aluno(), detalhe_turma(), foto_professor(), gerenciar_turmas() (+9 more)

### Community 41 - "Professor"
Cohesion: 0.14
Nodes (11): Professor, test_publicacao_professor_nao_expoe_contatos_sem_permissao(), Hipótese: a foto continua acessível por URL depois de tirar a publicação., Hipótese: os contatos vazam na home antes de a publicação ser marcada., Sonda: a data vem da query string e é convertida sem tratamento., test_contatos_do_professor_so_aparecem_quando_publicados(), test_data_invalida_na_turma_nao_derruba_a_rota(), test_foto_do_professor_some_ao_despublicar() (+3 more)

### Community 42 - "pagamento_polling.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 43 - ".contratar_plano"
Cohesion: 0.12
Nodes (10): Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda. O…, Aplica um pedido agendado cujo período de origem já terminou sem renovação.…, Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, Com uma troca já agendada, só dois planos fazem sentido num pedido de…, A cobrança do período seguinte tem de nascer no plano que o aluno agendou.…, O que aconteceu numa tentativa de contratar/renovar/trocar de plano., ResultadoContratacao (+2 more)

### Community 44 - "test_checkout_rotas.py"
Cohesion: 0.16
Nodes (24): _mockar_preferencia(), parametrize, Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala…, _resposta_preferencia(), test_abertura_json_navega_sem_redirecionar_post_externo(), test_admin_tambem_pode_abrir_checkout(), test_aluno_cria_checkout_da_propria_mensalidade(), test_aluno_nao_cria_checkout_de_mensalidade_de_outro_aluno() (+16 more)

### Community 45 - "test_pix_rotas.py"
Cohesion: 0.17
Nodes (23): MercadoPagoIndisponivel, Falha de transporte (timeout/DNS/conexao) ao falar com a API do Mercado Pago., test_mercado_pago_indisponivel_nao_persiste_nada(), _assinar(), _resposta_consulta(), _resposta_criacao(), test_admin_tambem_pode_gerar_pix(), test_aluno_gera_pix_da_propria_mensalidade() (+15 more)

### Community 46 - ".buscar_por_id"
Cohesion: 0.25
Nodes (19): _assinar(), _pagamento_mp(), _preparar_retorno(), Pix aberto e checkout concluído ao mesmo tempo: a consulta pelo…, test_retorno_com_aprovacao_confirmada_marca_pago(), test_retorno_com_mp_indisponivel_avisa_sem_mudar_status(), test_retorno_de_boleto_avisa_sobre_o_prazo(), test_retorno_de_sucesso_nao_marca_pago_sem_confirmacao() (+11 more)

### Community 47 - "d9e2f6a14c80_contatos_academia_perfis_professores.py"
Cohesion: 0.83
Nodes (3): _campos_professor(), downgrade(), upgrade()

### Community 49 - "presencaDAO.py"
Cohesion: 0.31
Nodes (3): PresencaDAO, Presenca, Presença Form

### Community 50 - "botao_ocupado.test.cjs"
Cohesion: 0.18
Nodes (7): assert, criarElemento(), fs, montar(), path, test, vm

### Community 51 - "ambiente_mercado_pago"
Cohesion: 0.22
Nodes (9): ambiente_mercado_pago(), ConfiguracaoInvalida, Exception, Variavel de ambiente obrigatoria ausente ou com formato invalido. Erro de…, Diz se a integracao esta apontando para producao ou para o sandbox. Prioriza a…, test_ambiente_assume_producao_para_token_sem_prefixo_de_teste(), test_ambiente_cai_no_prefixo_do_token_quando_nao_configurado(), test_ambiente_invalido_e_recusado() (+1 more)

### Community 52 - "checkout_abertura.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 56 - "limites_pagamento.py"
Cohesion: 0.50
Nodes (3): chave_pagamento(), Orçamentos compartilhados das chamadas interativas ao provedor de pagamento., A mesma conta mantém seu limite entre sessões, rotas e mensalidades. Alunos que…

## Knowledge Gaps
- **60 isolated node(s):** `icone_senha`, `input_senha`, `modal`, `avisoSemResultados`, `campoBusca` (+55 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PagamentoDAO` connect `PagamentoDAO` to `test_auditoria_seguranca.py`, `adm_bp.py`, `criar_aluno`, `criar_pagamento`, `logar_como_admin`, `test_mudanca_plano.py`, `.contratar_plano`, `test_checkout_rotas.py`, `test_pix_rotas.py`, `.buscar_por_id`, `pix_bp.py`, `PagamentoEvento`, `checkout_bp.py`, `usuario_bp.py`?**
  _High betweenness centrality (0.223) - this node is a cross-community bridge._
- **Why does `criar_pagamento()` connect `criar_pagamento` to `test_auditoria_seguranca.py`, `adm_bp.py`, `criar_aluno`, `logar_como_admin`, `PagamentoDAO`, `test_checkout_rotas.py`, `test_pix_rotas.py`, `.buscar_por_id`, `PagamentoEvento`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Why does `AlunoDAO` connect `adm_bp.py` to `test_perfil_e_foto.py`, `criar_aluno`, `PagamentoDAO`, `usuario_bp.py`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Are the 116 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 116 INFERRED edges - model-reasoned connections that need verification._
- **Are the 127 inferred relationships involving `criar_pagamento()` (e.g. with `PagamentoDAO` and `Pagamento`) actually correct?**
  _`criar_pagamento()` has 127 INFERRED edges - model-reasoned connections that need verification._
- **Are the 99 inferred relationships involving `logar_como_aluno()` (e.g. with `test_aluno_nao_alcanca_cobranca_de_outro_aluno()` and `test_checkout_recusa_cobranca_indisponivel()`) actually correct?**
  _`logar_como_aluno()` has 99 INFERRED edges - model-reasoned connections that need verification._
- **Are the 78 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 78 INFERRED edges - model-reasoned connections that need verification._