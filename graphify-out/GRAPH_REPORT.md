# Graph Report - SistemaEXTREMETEAM  (2026-09-05)

## Corpus Check
- 69 files · ~121,797 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 842 nodes · 2265 edges · 38 communities (31 shown, 7 thin omitted)
- Extraction: 80% EXTRACTED · 20% INFERRED · 0% AMBIGUOUS · INFERRED: 451 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ecf01abd`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- turma_bp.py
- Aluno Profile Page
- adm_bp.py
- _FakePreferenceResource
- PagamentoDAO
- servidor.py
- pgAdm.js
- Relatório de segurança — Sistema Extreme Team
- SistemaEXTREMETEAM Project
- test_mercado_pago_servico.py
- criar_aluno
- financeiroDAO.py
- test_migracao_checkout.py
- checkout.js
- CLAUDE.md
- planos.py
- pix_bp.py
- PagamentoEvento
- abrir_checkout
- mercado_pago.py
- pix.js
- usuario_bp.py
- env.py
- pagamento.js
- c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py
- _FakePaymentResource
- parametrize
- MercadoPagoIndisponivel
- Exception

## God Nodes (most connected - your core abstractions)
1. `PagamentoDAO` - 161 edges
2. `criar_pagamento()` - 92 edges
3. `logar_como_aluno()` - 75 edges
4. `criar_aluno()` - 72 edges
5. `AlunoDAO` - 45 edges
6. `MercadoPagoIndisponivel` - 26 edges
7. `SolicitacaoPlanoDAO` - 22 edges
8. `usuario_e_admin()` - 21 edges
9. `_pagar()` - 21 edges
10. `logar_como_admin()` - 20 edges

## Surprising Connections (you probably didn't know these)
- `Presença Form` --shares_data_with--> `Presenca`  [INFERRED]
  templates/turma.html → modelos/presenca.py
- `Histórico de Mensalidades Section` --shares_data_with--> `Pagamento`  [INFERRED]
  templates/pgUsuario.html → modelos/pagamento.py
- `Aluno Detail/Admin Page` --shares_data_with--> `Matricula`  [INFERRED]
  templates/dt_aluno.html → modelos/matricula.py
- `Aluno Profile Page` --shares_data_with--> `Matricula`  [INFERRED]
  templates/pgUsuario.html → modelos/matricula.py
- `Turma Detail Page` --shares_data_with--> `Turma`  [INFERRED]
  templates/turma.html → modelos/turma.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Shared Confirmation Modal Pattern** — templates_components_confirm_modal_dialog, templates_pgadm_page, templates_pgprofessor_page, templates_pgusuario_page, templates_turmas_page [EXTRACTED 1.00]
- **Mensalidade (Billing) Management Flow** — templates_dt_aluno_pagamento_form, templates_pgusuario_mensalidades_section, modelos_pagamento_pagamento, modelos_plano_plano [INFERRED 0.85]
- **Turma and Attendance Management Flow** — templates_turmas_turma_form, templates_turma_presenca_form, templates_pgprofessor_page, modelos_turma_turma [INFERRED 0.85]

## Communities (38 total, 7 thin omitted)

### Community 0 - "turma_bp.py"
Cohesion: 0.06
Nodes (35): admin_requerido, _acesso_permitido(), cadastrar_professor(), cadastrar_turma(), desmatricular_aluno(), detalhe_turma(), gerenciar_turmas(), matricular_aluno() (+27 more)

### Community 1 - "Aluno Profile Page"
Cohesion: 0.07
Nodes (33): Usuario Model, Extreme Team Logo Image, Academia do Bitelo Logo, abrirmodal(), fechar(), icone_senha, input_senha, modal (+25 more)

### Community 2 - "adm_bp.py"
Cohesion: 0.10
Nodes (41): aprovar_aluno(), aprovar_comprovante_manual(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_pagamento(), cadastrar_plano(), cancelar_mudanca_plano_admin(), cobrar_inadimplentes() (+33 more)

### Community 4 - "PagamentoDAO"
Cohesion: 0.06
Nodes (100): PagamentoDAO, True se já existe um Pix ou um checkout válido emitido para esta cobrança.…, True se a cobrança Pix já gerada para este pagamento ainda pode ser…, Solta a preferência atual para que a próxima tentativa crie uma nova. Nunca…, Totais do painel financeiro - sempre calculados no backend a partir do banco,…, criar_pagamento(), logar_como_aluno(), _assinar() (+92 more)

### Community 5 - "servidor.py"
Cohesion: 0.08
Nodes (26): after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, Flask App Service (compose), Postgres DB Service (compose), postgres_data Volume, errorhandler, Flask (+18 more)

### Community 6 - "pgAdm.js"
Cohesion: 0.20
Nodes (10): atualizarListaDeAlunos(), avisoSemResultados, campoBusca, campoDuracao, campoPreco, contadorAlunos, formatadorDePreco, formularioPlano (+2 more)

### Community 7 - "Relatório de segurança — Sistema Extreme Team"
Cohesion: 0.08
Nodes (24): A verificar em execução, Atualização após as correções, F10 — Redirecionamento aberto via `Referer`, F11 — `/logout` aceita GET, F12 — Enumeração de usuários por tempo de resposta, F13 — Senha mínima de 6 caracteres, sem outros critérios, F14 — Webhook sem verificação de recência do timestamp, F15 — Curinga de `LIKE` no filtro do financeiro (+16 more)

### Community 9 - "test_mercado_pago_servico.py"
Cohesion: 0.16
Nodes (23): parametrize, Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, validar_assinatura_webhook(), base_url(), _criar_preferencia(), mp_fake(), fixture, _resposta_preferencia() (+15 more)

### Community 10 - "criar_aluno"
Cohesion: 0.06
Nodes (74): Persistência dos pedidos de troca de plano agendados para a próxima renovação., Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, Aplica um pedido agendado cujo período de origem já terminou sem renovação.…, Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, Com uma troca já agendada, só dois planos fazem sentido num pedido de…, A cobrança do período seguinte tem de nascer no plano que o aluno agendou.…, `pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -…, forma_pagamento vem do que o Mercado Pago confirmou na consulta à API ('pix',… (+66 more)

### Community 11 - "financeiroDAO.py"
Cohesion: 0.07
Nodes (20): O que aconteceu numa tentativa de contratar/renovar/trocar de plano., ResultadoContratacao, Decimal, _para_decimal(), Plano, Pedido de troca de plano agendado para a próxima renovação. Nunca altera o…, SolicitacaoMudancaPlano, Aluno (+12 more)

### Community 12 - "test_migracao_checkout.py"
Cohesion: 0.31
Nodes (8): _colunas(), conexao(), migracao(), fixture, Exercita a migração dos campos do Checkout Pro de verdade (upgrade e…, _rodar(), test_downgrade_remove_exatamente_o_que_o_upgrade_criou(), test_upgrade_adiciona_as_colunas_e_preserva_linhas_antigas()

### Community 16 - "planos.py"
Cohesion: 0.06
Nodes (33): cadeia_paga(), cobranca_a_pagar(), cobranca_em_decisao(), cobranca_pendente(), duracao_dias(), esta_inadimplente(), fim_periodo_comprometido(), inicio_proximo_periodo() (+25 more)

### Community 17 - "pix_bp.py"
Cohesion: 0.14
Nodes (23): _acesso_permitido(), criar_pix_mensalidade(), _forma_pagamento_confirmada(), _pagamento_mp_mais_relevante(), _pagamento_ou_none(), _pix_expirado(), _processar_status_mp(), route (+15 more)

### Community 18 - "PagamentoEvento"
Cohesion: 0.12
Nodes (8): Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda. O…, Primeiro dia não coberto por outra mensalidade do mesmo aluno., Define o período coberto por uma mensalidade que ainda não tem um (lançamento…, Abre o período de acesso no momento em que o pagamento é confirmado. Se a…, Reescreve os campos denormalizados do aluno a partir das mensalidades.…, Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.…, PagamentoEvento, Histórico de auditoria de uma mensalidade (nunca grava credenciais ou dados…

### Community 19 - "abrir_checkout"
Cohesion: 0.12
Nodes (15): abrir_checkout(), _acesso_permitido(), route, Volta do Mercado Pago. Ignora por completo `status`, `payment_id`,…, Mesma regra já usada no Pix e na página de pagamento: o próprio aluno ou o…, Cria (ou reaproveita) a preferência do Checkout Pro e redireciona para o…, retorno_checkout(), Relê a mensalidade com trava de linha (SELECT ... FOR UPDATE). Serializa… (+7 more)

### Community 20 - "mercado_pago.py"
Cohesion: 0.14
Nodes (24): Checkout Pro do Mercado Pago - "outras formas de pagamento" (cartão, boleto,…, back_urls absolutas para onde o Mercado Pago devolve o aluno. Os três destinos…, _urls_retorno(), Exception, RuntimeError, _base_url_opcional(), base_url_publica(), ConfiguracaoInvalida (+16 more)

### Community 21 - "pix.js"
Cohesion: 0.42
Nodes (11): abrirPix(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), limparConteudoAnterior(), mensagemDeErro(), mostrarEstado() (+3 more)

### Community 22 - "usuario_bp.py"
Cohesion: 0.06
Nodes (57): _acesso_permitido_pagamento(), alterar_senha_perfil(), _aluno_da_sessao(), atualizar_dados_perfil(), cancelar_mudanca_plano(), comprovante_mensalidade(), confirmar_email(), enviar_comprovante_manual_aluno() (+49 more)

### Community 23 - "env.py"
Cohesion: 0.39
Nodes (7): get_engine(), get_engine_url(), get_metadata(), Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online()

### Community 24 - "pagamento.js"
Cohesion: 0.67
Nodes (6): consultarStatus(), gerarOuAtualizarPix(), iniciarPolling(), mostrarEstado(), pararPolling(), tratarResposta()

### Community 25 - "c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py"
Cohesion: 0.60
Nodes (5): _backfill_vigencia(), _colunas(), _criar_tabela_solicitacoes(), downgrade(), upgrade()

### Community 34 - "MercadoPagoIndisponivel"
Cohesion: 0.13
Nodes (23): buscar_pagamento(), buscar_pagamentos_por_referencia(), cancelar_pagamento(), criar_pagamento_pix(), _extrair_dados_pix(), MercadoPagoIndisponivel, _normalizar_pagamento(), Cria uma cobranca Pix no Mercado Pago. Retorna sempre um dict: sucesso ->… (+15 more)

## Knowledge Gaps
- **45 isolated node(s):** `Atualização após as correções`, `Sumário executivo`, `F1 — Aluno consegue desviar a ficha administrativa de outro aluno`, `F2 — Ausência de proteção CSRF em 46 de 49 formulários`, `F3 — Sem limite de tentativas: força bruta na senha do administrador` (+40 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PagamentoDAO` connect `PagamentoDAO` to `adm_bp.py`, `criar_aluno`, `financeiroDAO.py`, `pix_bp.py`, `PagamentoEvento`, `abrir_checkout`, `mercado_pago.py`, `usuario_bp.py`?**
  _High betweenness centrality (0.255) - this node is a cross-community bridge._
- **Why does `AlunoDAO` connect `adm_bp.py` to `turma_bp.py`, `PagamentoDAO`, `criar_aluno`, `financeiroDAO.py`, `usuario_bp.py`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Why does `Admin Dashboard Page` connect `Aluno Profile Page` to `adm_bp.py`, `financeiroDAO.py`, `pgAdm.js`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Are the 103 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 103 INFERRED edges - model-reasoned connections that need verification._
- **Are the 90 inferred relationships involving `criar_pagamento()` (e.g. with `PagamentoDAO` and `test_admin_tambem_pode_abrir_checkout()`) actually correct?**
  _`criar_pagamento()` has 90 INFERRED edges - model-reasoned connections that need verification._
- **Are the 73 inferred relationships involving `logar_como_aluno()` (e.g. with `test_aluno_cria_checkout_da_propria_mensalidade()` and `test_aluno_nao_cria_checkout_de_mensalidade_de_outro_aluno()`) actually correct?**
  _`logar_como_aluno()` has 73 INFERRED edges - model-reasoned connections that need verification._
- **Are the 70 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `test_aluno_nao_cria_checkout_de_mensalidade_de_outro_aluno()`) actually correct?**
  _`criar_aluno()` has 70 INFERRED edges - model-reasoned connections that need verification._