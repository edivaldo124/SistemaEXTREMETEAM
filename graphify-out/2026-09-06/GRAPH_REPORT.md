# Graph Report - SistemaEXTREMETEAM  (2026-09-06)

## Corpus Check
- 81 files · ~132,057 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 957 nodes · 2580 edges · 53 communities (44 shown, 9 thin omitted)
- Extraction: 80% EXTRACTED · 20% INFERRED · 0% AMBIGUOUS · INFERRED: 524 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9101cc87`
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
- financeiroDAO.py
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
- route
- mercado_pago.py
- MercadoPagoIndisponivel
- logar_como_admin
- Academia
- turma_bp.py
- ProfessorDAO
- pagamento_polling.test.cjs
- .contratar_plano
- parametrize
- config.py
- d9e2f6a14c80_contatos_academia_perfis_professores.py
- Exception
- botao_ocupado.test.cjs
- checkout_abertura.test.cjs
- filtros_financeiro.js

## God Nodes (most connected - your core abstractions)
1. `PagamentoDAO` - 137 edges
2. `criar_pagamento()` - 101 edges
3. `logar_como_aluno()` - 83 edges
4. `criar_aluno()` - 74 edges
5. `AlunoDAO` - 47 edges
6. `logar_como_admin()` - 31 edges
7. `MercadoPagoIndisponivel` - 28 edges
8. `ProfessorDAO` - 24 edges
9. `SolicitacaoPlanoDAO` - 23 edges
10. `Aluno` - 23 edges

## Surprising Connections (you probably didn't know these)
- `Histórico de Mensalidades Section` --shares_data_with--> `Pagamento`  [INFERRED]
  templates/pgUsuario.html → modelos/pagamento.py
- `Presença Form` --shares_data_with--> `Presenca`  [INFERRED]
  templates/turma.html → modelos/presenca.py
- `Turma Detail Page` --shares_data_with--> `Turma`  [INFERRED]
  templates/turma.html → modelos/turma.py
- `Aluno Mensalidade Launch Form` --shares_data_with--> `Pagamento`  [INFERRED]
  templates/dt_aluno.html → modelos/pagamento.py
- `Cadastrar Plano Form` --shares_data_with--> `Plano`  [INFERRED]
  templates/pgAdm.html → modelos/plano.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Shared Confirmation Modal Pattern** — templates_components_confirm_modal_dialog, templates_pgadm_page, templates_pgprofessor_page, templates_pgusuario_page, templates_turmas_page [EXTRACTED 1.00]
- **Mensalidade (Billing) Management Flow** — templates_dt_aluno_pagamento_form, templates_pgusuario_mensalidades_section, modelos_pagamento_pagamento, modelos_plano_plano [INFERRED 0.85]
- **Turma and Attendance Management Flow** — templates_turmas_turma_form, templates_turma_presenca_form, templates_pgprofessor_page, modelos_turma_turma [INFERRED 0.85]

## Communities (53 total, 9 thin omitted)

### Community 0 - "test_perfil_e_foto.py"
Cohesion: 0.16
Nodes (13): cadastrar_turma(), remover_turma(), TurmaDAO, Turma, Cadastrar Turma Form, _imagem_jpeg_valida(), test_admin_acessa_foto_de_qualquer_aluno(), test_aluno_nao_acessa_foto_de_outro_aluno() (+5 more)

### Community 1 - "Aluno Profile Page"
Cohesion: 0.05
Nodes (43): Usuario Model, Extreme Team Logo Image, Academia do Bitelo Logo, abrirmodal(), fechar(), icone_senha, input_senha, modal (+35 more)

### Community 2 - "adm_bp.py"
Cohesion: 0.08
Nodes (50): aprovar_aluno(), aprovar_comprovante_manual(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_pagamento(), cadastrar_plano(), cancelar_mudanca_plano_admin(), cobrar_inadimplentes() (+42 more)

### Community 3 - "criar_aluno"
Cohesion: 0.15
Nodes (33): criar_aluno(), test_area_do_aluno_renderiza_telas_independentes_do_menu(), test_escolher_plano_cria_mensalidade_e_redireciona_para_pix(), test_plano_atual_continua_disponivel_para_gerar_cobranca(), test_plano_invalido_nao_cria_mensalidade(), test_reenvio_da_contratacao_reutiliza_mensalidade(), test_valor_enviado_pelo_navegador_e_ignorado(), _pagar() (+25 more)

### Community 4 - "criar_pagamento"
Cohesion: 0.07
Nodes (90): parametrize, criar_pagamento(), logar_como_aluno(), _assinar(), _mockar_preferencia(), _pagamento_mp(), _preparar_retorno(), Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala… (+82 more)

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
Cohesion: 0.13
Nodes (27): Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, validar_assinatura_webhook(), base_url(), _criar_preferencia(), mp_fake(), fixture, parametrize, _resposta_preferencia() (+19 more)

### Community 10 - "test_mudanca_plano.py"
Cohesion: 0.20
Nodes (22): Persistência dos pedidos de troca de plano agendados para a próxima renovação., SolicitacaoPlanoDAO, _agendar(), _pagar(), Mudança para um plano mais barato agendada para a próxima renovação. Regra…, O admin pode estornar/cancelar a mensalidade que sustentava a vigência depois…, test_admin_cancela_a_solicitacao(), test_aluno_cancela_a_solicitacao_antes_da_efetivacao() (+14 more)

### Community 11 - "financeiroDAO.py"
Cohesion: 0.16
Nodes (6): O que aconteceu numa tentativa de contratar/renovar/trocar de plano., ResultadoContratacao, Pagamento, _para_decimal(), Pedido de troca de plano agendado para a próxima renovação. Nunca altera o…, SolicitacaoMudancaPlano

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
Nodes (24): _acesso_permitido(), criar_pix_mensalidade(), _forma_pagamento_confirmada(), _pagamento_mp_mais_relevante(), _pagamento_ou_none(), _pix_expirado(), _processar_status_mp(), route (+16 more)

### Community 18 - "PagamentoEvento"
Cohesion: 0.12
Nodes (10): Primeiro dia não coberto por outra mensalidade do mesmo aluno., Define o período coberto por uma mensalidade que ainda não tem um (lançamento…, Abre o período de acesso no momento em que o pagamento é confirmado. Se a…, Reescreve os campos denormalizados do aluno a partir das mensalidades.…, forma_pagamento vem do que o Mercado Pago confirmou na consulta à API ('pix',…, Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.…, PagamentoEvento, Histórico de auditoria de uma mensalidade (nunca grava credenciais ou dados… (+2 more)

### Community 20 - "checkout_bp.py"
Cohesion: 0.12
Nodes (26): abrir_checkout(), _acesso_permitido(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), _quer_json(), Checkout Pro do Mercado Pago - "outras formas de pagamento" (cartão, boleto,…, Alternativa sem JavaScript: POST local, depois um link GET para o provedor. (+18 more)

### Community 21 - "pix.js"
Cohesion: 0.33
Nodes (14): abrirPix(), alvoDoRotulo(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), liberarBotao(), limparConteudoAnterior() (+6 more)

### Community 22 - "usuario_bp.py"
Cohesion: 0.05
Nodes (66): _acesso_permitido_pagamento(), alterar_senha_perfil(), _aluno_da_sessao(), atualizar_dados_perfil(), cancelar_mudanca_plano(), comprovante_mensalidade(), confirmar_email(), enviar_comprovante_manual_aluno() (+58 more)

### Community 23 - "env.py"
Cohesion: 0.39
Nodes (7): get_engine(), get_engine_url(), get_metadata(), Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online()

### Community 24 - "pagamento.js"
Cohesion: 0.47
Nodes (9): alvoDoRotulo(), consultarStatus(), gerarOuAtualizarPix(), iniciarPolling(), liberarBotao(), marcarOcupado(), mostrarEstado(), pararPolling() (+1 more)

### Community 25 - "c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py"
Cohesion: 0.60
Nodes (5): _backfill_vigencia(), _colunas(), _criar_tabela_solicitacoes(), downgrade(), upgrade()

### Community 34 - "mercado_pago.py"
Cohesion: 0.13
Nodes (27): Decimal, _base_url_opcional(), base_url_publica(), buscar_pagamentos_por_referencia(), cancelar_pagamento(), criar_pagamento_pix(), criar_preferencia_checkout(), _erro_menciona() (+19 more)

### Community 35 - "MercadoPagoIndisponivel"
Cohesion: 0.25
Nodes (9): Exception, buscar_pagamento(), MercadoPagoIndisponivel, Consulta o pagamento diretamente na API do Mercado Pago - fonte de verdade de…, Falha de transporte (timeout/DNS/conexao) ao falar com a API do Mercado Pago., test_buscar_pagamento_expoe_meio_de_pagamento_e_moeda(), test_buscar_pagamento_falha_de_transporte_levanta_indisponivel(), test_buscar_pagamento_sucesso() (+1 more)

### Community 36 - "logar_como_admin"
Cohesion: 0.13
Nodes (21): logar_como_admin(), test_admin_salva_atualiza_e_limpa_contatos(), test_csrf_configuracoes(), test_whatsapp_internacional_preserva_codigo_no_formulario(), test_busca_financeira_trata_curingas_como_texto(), test_painel_financeiro_busca_por_nome_do_aluno(), test_painel_financeiro_exige_admin(), test_painel_financeiro_filtra_por_status() (+13 more)

### Community 37 - "Academia"
Cohesion: 0.16
Nodes (15): configuracoes(), route, editar_professor(), Academia, admin_requerido(), link_email(), Normalização de contatos profissionais antes de montar links públicos., validar_email() (+7 more)

### Community 38 - "turma_bp.py"
Cohesion: 0.20
Nodes (13): _acesso_permitido(), desmatricular_aluno(), detalhe_turma(), foto_professor(), matricular_aluno(), painel_professor(), route, registrar_presenca() (+5 more)

### Community 41 - "ProfessorDAO"
Cohesion: 0.14
Nodes (11): cadastrar_professor(), gerenciar_turmas(), remover_professor(), ProfessorDAO, Professor, Cadastrar Professor Form, test_publicacao_professor_nao_expoe_contatos_sem_permissao(), test_professor_nao_ve_foto_de_aluno_fora_da_sua_turma() (+3 more)

### Community 42 - "pagamento_polling.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 43 - ".contratar_plano"
Cohesion: 0.15
Nodes (8): Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda. O…, Aplica um pedido agendado cujo período de origem já terminou sem renovação.…, Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, Com uma troca já agendada, só dois planos fazem sentido num pedido de…, A cobrança do período seguinte tem de nascer no plano que o aluno agendou.…, test_mudanca_nao_vale_por_prazo_enquanto_houver_periodo_pago(), test_mudanca_vale_por_decurso_de_prazo_quando_o_plano_vence()

### Community 47 - "d9e2f6a14c80_contatos_academia_perfis_professores.py"
Cohesion: 0.83
Nodes (3): _campos_professor(), downgrade(), upgrade()

### Community 50 - "botao_ocupado.test.cjs"
Cohesion: 0.18
Nodes (7): assert, criarElemento(), fs, montar(), path, test, vm

### Community 52 - "checkout_abertura.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

## Knowledge Gaps
- **60 isolated node(s):** `assert`, `fs`, `path`, `test`, `vm` (+55 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PagamentoDAO` connect `PagamentoDAO` to `adm_bp.py`, `criar_aluno`, `criar_pagamento`, `logar_como_admin`, `test_mudanca_plano.py`, `financeiroDAO.py`, `.contratar_plano`, `config.py`, `pix_bp.py`, `PagamentoEvento`, `checkout_bp.py`, `usuario_bp.py`?**
  _High betweenness centrality (0.193) - this node is a cross-community bridge._
- **Why does `Matricula` connect `config.py` to `Aluno Profile Page`, `turma_bp.py`, `PagamentoDAO`, `financeiroDAO.py`, `usuario_bp.py`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Why does `criar_pagamento()` connect `criar_pagamento` to `adm_bp.py`, `criar_aluno`, `logar_como_admin`, `PagamentoDAO`, `financeiroDAO.py`, `PagamentoEvento`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Are the 81 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 81 INFERRED edges - model-reasoned connections that need verification._
- **Are the 99 inferred relationships involving `criar_pagamento()` (e.g. with `PagamentoDAO` and `Pagamento`) actually correct?**
  _`criar_pagamento()` has 99 INFERRED edges - model-reasoned connections that need verification._
- **Are the 81 inferred relationships involving `logar_como_aluno()` (e.g. with `test_abertura_json_navega_sem_redirecionar_post_externo()` and `test_aluno_cria_checkout_da_propria_mensalidade()`) actually correct?**
  _`logar_como_aluno()` has 81 INFERRED edges - model-reasoned connections that need verification._
- **Are the 72 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 72 INFERRED edges - model-reasoned connections that need verification._