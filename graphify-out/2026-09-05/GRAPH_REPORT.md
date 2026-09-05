# Graph Report - SistemaEXTREMETEAM  (2026-09-05)

## Corpus Check
- 63 files · ~115,599 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 774 nodes · 2229 edges · 38 communities (33 shown, 5 thin omitted)
- Extraction: 78% EXTRACTED · 22% INFERRED · 0% AMBIGUOUS · INFERRED: 486 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d3650543`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- turma_bp.py
- Aluno Profile Page
- adm_bp.py
- usuario_bp.py
- criar_pagamento
- Flask App Service (compose)
- pgAdm.js
- test_mudanca_plano.py
- SistemaEXTREMETEAM Project
- test_mercado_pago_servico.py
- criar_aluno
- financeiroDAO.py
- test_migracao_checkout.py
- checkout.js
- CLAUDE.md
- planos.py
- pix_bp.py
- PagamentoDAO
- checkout_bp.py
- mercado_pago.py
- pix.js
- .contratar_plano
- env.py
- pagamento.js
- c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py
- _FakePaymentResource
- test_financeiro_dao.py
- MercadoPagoIndisponivel
- ambiente_mercado_pago
- ._promover_vencidos
- .marcar_pago_via_webhook

## God Nodes (most connected - your core abstractions)
1. `PagamentoDAO` - 164 edges
2. `criar_pagamento()` - 91 edges
3. `logar_como_aluno()` - 74 edges
4. `criar_aluno()` - 69 edges
5. `AlunoDAO` - 43 edges
6. `MercadoPagoIndisponivel` - 26 edges
7. `SolicitacaoPlanoDAO` - 23 edges
8. `Aluno` - 23 edges
9. `usuario_e_admin()` - 21 edges
10. `PagamentoEvento` - 21 edges

## Surprising Connections (you probably didn't know these)
- `Histórico de Mensalidades Section` --shares_data_with--> `Pagamento`  [INFERRED]
  templates/pgUsuario.html → modelos/pagamento.py
- `Planos Disponíveis Section` --shares_data_with--> `Plano`  [INFERRED]
  templates/pgUsuario.html → modelos/plano.py
- `Aluno Detail/Admin Page` --shares_data_with--> `Matricula`  [INFERRED]
  templates/dt_aluno.html → modelos/matricula.py
- `Aluno Profile Page` --shares_data_with--> `Matricula`  [INFERRED]
  templates/pgUsuario.html → modelos/matricula.py
- `Aluno Mensalidade Launch Form` --shares_data_with--> `Pagamento`  [INFERRED]
  templates/dt_aluno.html → modelos/pagamento.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Shared Confirmation Modal Pattern** — templates_components_confirm_modal_dialog, templates_pgadm_page, templates_pgprofessor_page, templates_pgusuario_page, templates_turmas_page [EXTRACTED 1.00]
- **Mensalidade (Billing) Management Flow** — templates_dt_aluno_pagamento_form, templates_pgusuario_mensalidades_section, modelos_pagamento_pagamento, modelos_plano_plano [INFERRED 0.85]
- **Turma and Attendance Management Flow** — templates_turmas_turma_form, templates_turma_presenca_form, templates_pgprofessor_page, modelos_turma_turma [INFERRED 0.85]

## Communities (38 total, 5 thin omitted)

### Community 0 - "turma_bp.py"
Cohesion: 0.07
Nodes (36): _acesso_permitido(), cadastrar_professor(), cadastrar_turma(), desmatricular_aluno(), detalhe_turma(), gerenciar_turmas(), matricular_aluno(), painel_professor() (+28 more)

### Community 1 - "Aluno Profile Page"
Cohesion: 0.07
Nodes (33): Usuario Model, Extreme Team Logo Image, Academia do Bitelo Logo, abrirmodal(), fechar(), icone_senha, input_senha, modal (+25 more)

### Community 2 - "adm_bp.py"
Cohesion: 0.11
Nodes (38): aprovar_aluno(), aprovar_comprovante_manual(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_pagamento(), cadastrar_plano(), cancelar_mudanca_plano_admin(), cobrar_inadimplentes() (+30 more)

### Community 3 - "usuario_bp.py"
Cohesion: 0.07
Nodes (54): Ponto de entrada WSGI usado pelo Gunicorn em producao., _acesso_permitido_pagamento(), alterar_senha_perfil(), _aluno_da_sessao(), atualizar_dados_perfil(), cancelar_mudanca_plano(), comprovante_mensalidade(), confirmar_email() (+46 more)

### Community 4 - "criar_pagamento"
Cohesion: 0.08
Nodes (81): criar_pagamento(), logar_como_aluno(), _assinar(), _mockar_preferencia(), _pagamento_mp(), _preparar_retorno(), parametrize, Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala… (+73 more)

### Community 5 - "Flask App Service (compose)"
Cohesion: 0.22
Nodes (9): Flask App Service (compose), Postgres DB Service (compose), postgres_data Volume, Flask, Flask-SQLAlchemy, Gunicorn, psycopg2-binary, python-dotenv (+1 more)

### Community 6 - "pgAdm.js"
Cohesion: 0.20
Nodes (10): atualizarListaDeAlunos(), avisoSemResultados, campoBusca, campoDuracao, campoPreco, contadorAlunos, formatadorDePreco, formularioPlano (+2 more)

### Community 7 - "test_mudanca_plano.py"
Cohesion: 0.16
Nodes (25): Persistência dos pedidos de troca de plano agendados para a próxima renovação., Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, SolicitacaoPlanoDAO, _agendar(), _pagar(), plano_barato(), fixture, Mudança para um plano mais barato agendada para a próxima renovação. Regra… (+17 more)

### Community 9 - "test_mercado_pago_servico.py"
Cohesion: 0.14
Nodes (23): Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, validar_assinatura_webhook(), base_url(), _criar_preferencia(), _FakePreferenceResource, mp_fake(), fixture, parametrize (+15 more)

### Community 10 - "criar_aluno"
Cohesion: 0.14
Nodes (33): criar_aluno(), logar_como_admin(), test_area_do_aluno_renderiza_telas_independentes_do_menu(), test_escolher_plano_cria_mensalidade_e_redireciona_para_pix(), test_plano_atual_continua_disponivel_para_gerar_cobranca(), test_plano_invalido_nao_cria_mensalidade(), test_reenvio_da_contratacao_reutiliza_mensalidade(), test_valor_enviado_pelo_navegador_e_ignorado() (+25 more)

### Community 11 - "financeiroDAO.py"
Cohesion: 0.11
Nodes (16): O que aconteceu numa tentativa de contratar/renovar/trocar de plano., ResultadoContratacao, Decimal, _para_decimal(), Plano, Pedido de troca de plano agendado para a próxima renovação. Nunca altera o…, SolicitacaoMudancaPlano, Cadastrar Plano Form (+8 more)

### Community 12 - "test_migracao_checkout.py"
Cohesion: 0.31
Nodes (8): _colunas(), conexao(), migracao(), fixture, Exercita a migração dos campos do Checkout Pro de verdade (upgrade e…, _rodar(), test_downgrade_remove_exatamente_o_que_o_upgrade_criou(), test_upgrade_adiciona_as_colunas_e_preserva_linhas_antigas()

### Community 16 - "planos.py"
Cohesion: 0.06
Nodes (33): cadeia_paga(), cobranca_a_pagar(), cobranca_em_decisao(), cobranca_pendente(), duracao_dias(), esta_inadimplente(), fim_periodo_comprometido(), inicio_proximo_periodo() (+25 more)

### Community 17 - "pix_bp.py"
Cohesion: 0.18
Nodes (19): _acesso_permitido(), criar_pix_mensalidade(), _forma_pagamento_confirmada(), _pagamento_ou_none(), _pix_expirado(), _processar_status_mp(), route, Meio de pagamento realmente usado, sempre a partir da resposta da API. (+11 more)

### Community 18 - "PagamentoDAO"
Cohesion: 0.12
Nodes (13): PagamentoDAO, Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda. O…, Primeiro dia não coberto por outra mensalidade do mesmo aluno., Define o período coberto por uma mensalidade que ainda não tem um (lançamento…, Abre o período de acesso no momento em que o pagamento é confirmado. Se a…, Reescreve os campos denormalizados do aluno a partir das mensalidades.…, Solta a preferência atual para que a próxima tentativa crie uma nova. Nunca…, Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.… (+5 more)

### Community 19 - "checkout_bp.py"
Cohesion: 0.13
Nodes (18): abrir_checkout(), _acesso_permitido(), route, Checkout Pro do Mercado Pago - "outras formas de pagamento" (cartão, boleto,…, Volta do Mercado Pago. Ignora por completo `status`, `payment_id`,…, Mesma regra já usada no Pix e na página de pagamento: o próprio aluno ou o…, back_urls absolutas para onde o Mercado Pago devolve o aluno. Os três destinos…, Cria (ou reaproveita) a preferência do Checkout Pro e redireciona para o… (+10 more)

### Community 20 - "mercado_pago.py"
Cohesion: 0.15
Nodes (23): _base_url_opcional(), base_url_publica(), cancelar_pagamento(), criar_pagamento_pix(), criar_preferencia_checkout(), _erro_menciona(), _erro_menciona_expiracao(), _extrair_dados_pix() (+15 more)

### Community 21 - "pix.js"
Cohesion: 0.42
Nodes (11): abrirPix(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), limparConteudoAnterior(), mensagemDeErro(), mostrarEstado() (+3 more)

### Community 22 - ".contratar_plano"
Cohesion: 0.15
Nodes (10): Aplica um pedido agendado cujo período de origem já terminou sem renovação.…, Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, Com uma troca já agendada, só dois planos fazem sentido num pedido de…, A cobrança do período seguinte tem de nascer no plano que o aluno agendou.…, test_mudanca_nao_vale_por_prazo_enquanto_houver_periodo_pago(), test_mudanca_vale_por_decurso_de_prazo_quando_o_plano_vence(), test_acao_forjada_de_renovacao_sem_vigencia_apenas_contrata(), test_aluno_com_plano_pago_nao_gera_segunda_cobranca() (+2 more)

### Community 23 - "env.py"
Cohesion: 0.39
Nodes (7): get_engine(), get_engine_url(), get_metadata(), Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online()

### Community 24 - "pagamento.js"
Cohesion: 0.67
Nodes (6): consultarStatus(), gerarOuAtualizarPix(), iniciarPolling(), mostrarEstado(), pararPolling(), tratarResposta()

### Community 25 - "c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py"
Cohesion: 0.60
Nodes (5): _backfill_vigencia(), _colunas(), _criar_tabela_solicitacoes(), downgrade(), upgrade()

### Community 33 - "test_financeiro_dao.py"
Cohesion: 0.12
Nodes (15): mensalidade_destaque(), True se já existe um Pix ou um checkout válido emitido para esta cobrança.…, Escolhe a mensalidade mais relevante para o card 'Minha mensalidade': a mais…, True se a cobrança Pix já gerada para este pagamento ainda pode ser…, Totais do painel financeiro - sempre calculados no backend a partir do banco,…, provider_payment_id sozinho não basta: pagamentos do Checkout Pro…, test_listar_filtrado_por_status_e_busca_de_aluno(), test_mensalidade_destaque_prioriza_a_mais_proxima_de_vencer() (+7 more)

### Community 34 - "MercadoPagoIndisponivel"
Cohesion: 0.21
Nodes (13): buscar_pagamento(), buscar_pagamentos_por_referencia(), MercadoPagoIndisponivel, Consulta o pagamento diretamente na API do Mercado Pago - fonte de verdade de…, Lista os pagamentos que o Mercado Pago associa a uma external_reference. Usada…, Falha de transporte (timeout/DNS/conexao) ao falar com a API do Mercado Pago., _sdk(), test_buscar_pagamento_expoe_meio_de_pagamento_e_moeda() (+5 more)

### Community 35 - "ambiente_mercado_pago"
Cohesion: 0.22
Nodes (9): ambiente_mercado_pago(), ConfiguracaoInvalida, Exception, Variavel de ambiente obrigatoria ausente ou com formato invalido. Erro de…, Diz se a integracao esta apontando para producao ou para o sandbox. Prioriza a…, test_ambiente_assume_producao_para_token_sem_prefixo_de_teste(), test_ambiente_cai_no_prefixo_do_token_quando_nao_configurado(), test_ambiente_invalido_e_recusado() (+1 more)

### Community 37 - ".marcar_pago_via_webhook"
Cohesion: 0.29
Nodes (6): forma_pagamento vem do que o Mercado Pago confirmou na consulta à API ('pix',…, test_marcar_pago_via_webhook_sincroniza_mensalidade_do_aluno(), Quem paga uma cobrança vencida há semanas tem de receber os 30 dias a partir da…, test_cobranca_antiga_quitada_hoje_abre_o_periodo_a_partir_de_hoje(), test_renovacao_antecipada_paga_hoje_mantem_a_janela_futura(), test_webhook_aprovado_abre_vigencia_e_atualiza_validade_do_aluno()

## Knowledge Gaps
- **25 isolated node(s):** `modal`, `input_senha`, `icone_senha`, `campoBusca`, `linhasDeAlunos` (+20 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PagamentoDAO` connect `PagamentoDAO` to `turma_bp.py`, `test_financeiro_dao.py`, `adm_bp.py`, `usuario_bp.py`, `criar_pagamento`, `._promover_vencidos`, `.marcar_pago_via_webhook`, `test_mudanca_plano.py`, `criar_aluno`, `financeiroDAO.py`, `pix_bp.py`, `checkout_bp.py`, `.contratar_plano`?**
  _High betweenness centrality (0.309) - this node is a cross-community bridge._
- **Why does `Matricula` connect `turma_bp.py` to `financeiroDAO.py`, `Aluno Profile Page`, `PagamentoDAO`, `usuario_bp.py`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Why does `AlunoDAO` connect `adm_bp.py` to `turma_bp.py`, `usuario_bp.py`, `criar_aluno`, `financeiroDAO.py`, `PagamentoDAO`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Are the 107 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 107 INFERRED edges - model-reasoned connections that need verification._
- **Are the 89 inferred relationships involving `criar_pagamento()` (e.g. with `PagamentoDAO` and `Pagamento`) actually correct?**
  _`criar_pagamento()` has 89 INFERRED edges - model-reasoned connections that need verification._
- **Are the 72 inferred relationships involving `logar_como_aluno()` (e.g. with `test_aluno_cria_checkout_da_propria_mensalidade()` and `test_aluno_nao_cria_checkout_de_mensalidade_de_outro_aluno()`) actually correct?**
  _`logar_como_aluno()` has 72 INFERRED edges - model-reasoned connections that need verification._
- **Are the 67 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 67 INFERRED edges - model-reasoned connections that need verification._