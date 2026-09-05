# Graph Report - SistemaEXTREMETEAM  (2026-09-05)

## Corpus Check
- 76 files · ~127,161 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 893 nodes · 2508 edges · 40 communities (36 shown, 4 thin omitted)
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 534 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `958c2bdf`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_perfil_e_foto.py
- Aluno Profile Page
- adm_bp.py
- PagamentoDAO
- servidor.py
- Relatório de segurança — Sistema Extreme Team
- SistemaEXTREMETEAM Project
- test_mercado_pago_servico.py
- criar_aluno
- config.py
- test_migracao_checkout.py
- checkout.js
- CLAUDE.md
- planos.py
- pix_bp.py
- PagamentoEvento
- checkout_bp.py
- pix.js
- usuario_bp.py
- env.py
- pagamento.js
- c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py
- _FakePaymentResource
- mercado_pago.py
- ProfessorDAO
- Academia
- turma_bp.py
- Professor
- MercadoPagoIndisponivel
- d9e2f6a14c80_contatos_academia_perfis_professores.py

## God Nodes (most connected - your core abstractions)
1. `PagamentoDAO` - 166 edges
2. `criar_pagamento()` - 93 edges
3. `logar_como_aluno()` - 75 edges
4. `criar_aluno()` - 73 edges
5. `AlunoDAO` - 47 edges
6. `logar_como_admin()` - 31 edges
7. `MercadoPagoIndisponivel` - 26 edges
8. `ProfessorDAO` - 24 edges
9. `SolicitacaoPlanoDAO` - 23 edges
10. `Aluno` - 23 edges

## Surprising Connections (you probably didn't know these)
- `Histórico de Mensalidades Section` --shares_data_with--> `Pagamento`  [INFERRED]
  templates/pgUsuario.html → modelos/pagamento.py
- `Aluno Detail/Admin Page` --shares_data_with--> `Matricula`  [INFERRED]
  templates/dt_aluno.html → modelos/matricula.py
- `Aluno Profile Page` --shares_data_with--> `Matricula`  [INFERRED]
  templates/pgUsuario.html → modelos/matricula.py
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

## Communities (40 total, 4 thin omitted)

### Community 0 - "test_perfil_e_foto.py"
Cohesion: 0.16
Nodes (13): cadastrar_turma(), remover_turma(), TurmaDAO, Turma, Cadastrar Turma Form, _imagem_jpeg_valida(), test_admin_acessa_foto_de_qualquer_aluno(), test_aluno_nao_acessa_foto_de_outro_aluno() (+5 more)

### Community 1 - "Aluno Profile Page"
Cohesion: 0.05
Nodes (42): Usuario Model, Extreme Team Logo Image, Academia do Bitelo Logo, abrirmodal(), fechar(), icone_senha, input_senha, modal (+34 more)

### Community 2 - "adm_bp.py"
Cohesion: 0.08
Nodes (49): aprovar_aluno(), aprovar_comprovante_manual(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_pagamento(), cadastrar_plano(), cancelar_mudanca_plano_admin(), cobrar_inadimplentes() (+41 more)

### Community 4 - "PagamentoDAO"
Cohesion: 0.06
Nodes (108): PagamentoDAO, True se já existe um Pix ou um checkout válido emitido para esta cobrança.…, True se a cobrança Pix já gerada para este pagamento ainda pode ser…, Solta a preferência atual para que a próxima tentativa crie uma nova. Nunca…, forma_pagamento vem do que o Mercado Pago confirmou na consulta à API ('pix',…, Totais do painel financeiro - sempre calculados no backend a partir do banco,…, criar_pagamento(), logar_como_aluno() (+100 more)

### Community 5 - "servidor.py"
Cohesion: 0.08
Nodes (28): after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, Flask App Service (compose), Postgres DB Service (compose), postgres_data Volume, context_processor, errorhandler (+20 more)

### Community 7 - "Relatório de segurança — Sistema Extreme Team"
Cohesion: 0.08
Nodes (24): A verificar em execução, Atualização após as correções, F10 — Redirecionamento aberto via `Referer`, F11 — `/logout` aceita GET, F12 — Enumeração de usuários por tempo de resposta, F13 — Senha mínima de 6 caracteres, sem outros critérios, F14 — Webhook sem verificação de recência do timestamp, F15 — Curinga de `LIKE` no filtro do financeiro (+16 more)

### Community 9 - "test_mercado_pago_servico.py"
Cohesion: 0.11
Nodes (28): ambiente_mercado_pago(), Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, Diz se a integracao esta apontando para producao ou para o sandbox. Prioriza a…, validar_assinatura_webhook(), base_url(), _criar_preferencia(), _FakePreferenceResource, mp_fake() (+20 more)

### Community 10 - "criar_aluno"
Cohesion: 0.06
Nodes (71): Persistência dos pedidos de troca de plano agendados para a próxima renovação., Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, Aplica um pedido agendado cujo período de origem já terminou sem renovação.…, Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, Com uma troca já agendada, só dois planos fazem sentido num pedido de…, A cobrança do período seguinte tem de nascer no plano que o aluno agendou.…, `pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -…, SolicitacaoPlanoDAO (+63 more)

### Community 11 - "config.py"
Cohesion: 0.29
Nodes (3): Matricula, Presenca, Presença Form

### Community 12 - "test_migracao_checkout.py"
Cohesion: 0.31
Nodes (8): _colunas(), conexao(), migracao(), fixture, Exercita a migração dos campos do Checkout Pro de verdade (upgrade e…, _rodar(), test_downgrade_remove_exatamente_o_que_o_upgrade_criou(), test_upgrade_adiciona_as_colunas_e_preserva_linhas_antigas()

### Community 16 - "planos.py"
Cohesion: 0.06
Nodes (33): cadeia_paga(), cobranca_a_pagar(), cobranca_em_decisao(), cobranca_pendente(), duracao_dias(), esta_inadimplente(), fim_periodo_comprometido(), inicio_proximo_periodo() (+25 more)

### Community 17 - "pix_bp.py"
Cohesion: 0.14
Nodes (24): _acesso_permitido(), criar_pix_mensalidade(), _forma_pagamento_confirmada(), _pagamento_mp_mais_relevante(), _pagamento_ou_none(), _pix_expirado(), _processar_status_mp(), route (+16 more)

### Community 18 - "PagamentoEvento"
Cohesion: 0.08
Nodes (12): Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda. O…, Primeiro dia não coberto por outra mensalidade do mesmo aluno., Define o período coberto por uma mensalidade que ainda não tem um (lançamento…, Abre o período de acesso no momento em que o pagamento é confirmado. Se a…, Reescreve os campos denormalizados do aluno a partir das mensalidades.…, Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.…, O que aconteceu numa tentativa de contratar/renovar/trocar de plano., ResultadoContratacao (+4 more)

### Community 20 - "checkout_bp.py"
Cohesion: 0.13
Nodes (19): abrir_checkout(), _acesso_permitido(), route, Checkout Pro do Mercado Pago - "outras formas de pagamento" (cartão, boleto,…, Volta do Mercado Pago. Ignora por completo `status`, `payment_id`,…, Mesma regra já usada no Pix e na página de pagamento: o próprio aluno ou o…, back_urls absolutas para onde o Mercado Pago devolve o aluno. Os três destinos…, Cria (ou reaproveita) a preferência do Checkout Pro e redireciona para o… (+11 more)

### Community 21 - "pix.js"
Cohesion: 0.42
Nodes (11): abrirPix(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), limparConteudoAnterior(), mensagemDeErro(), mostrarEstado() (+3 more)

### Community 22 - "usuario_bp.py"
Cohesion: 0.06
Nodes (59): _acesso_permitido_pagamento(), alterar_senha_perfil(), _aluno_da_sessao(), atualizar_dados_perfil(), cancelar_mudanca_plano(), comprovante_mensalidade(), confirmar_email(), enviar_comprovante_manual_aluno() (+51 more)

### Community 23 - "env.py"
Cohesion: 0.39
Nodes (7): get_engine(), get_engine_url(), get_metadata(), Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online()

### Community 24 - "pagamento.js"
Cohesion: 0.67
Nodes (6): consultarStatus(), gerarOuAtualizarPix(), iniciarPolling(), mostrarEstado(), pararPolling(), tratarResposta()

### Community 25 - "c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py"
Cohesion: 0.60
Nodes (5): _backfill_vigencia(), _colunas(), _criar_tabela_solicitacoes(), downgrade(), upgrade()

### Community 34 - "mercado_pago.py"
Cohesion: 0.14
Nodes (23): Decimal, _base_url_opcional(), base_url_publica(), criar_pagamento_pix(), criar_preferencia_checkout(), _erro_menciona(), _erro_menciona_expiracao(), _extrair_dados_pix() (+15 more)

### Community 36 - "ProfessorDAO"
Cohesion: 0.12
Nodes (22): cadastrar_professor(), foto_professor(), gerenciar_turmas(), painel_professor(), route, remover_professor(), ProfessorDAO, Cadastrar Professor Form (+14 more)

### Community 37 - "Academia"
Cohesion: 0.16
Nodes (17): configuracoes(), route, editar_professor(), Academia, admin_requerido(), Normalização de contatos profissionais antes de montar links públicos., validar_email(), validar_instagram() (+9 more)

### Community 38 - "turma_bp.py"
Cohesion: 0.25
Nodes (9): _acesso_permitido(), desmatricular_aluno(), detalhe_turma(), matricular_aluno(), registrar_presenca(), _turma_ou_404(), MatriculaDAO, PresencaDAO (+1 more)

### Community 41 - "Professor"
Cohesion: 0.19
Nodes (3): Professor, link_email(), test_publicacao_professor_nao_expoe_contatos_sem_permissao()

### Community 45 - "MercadoPagoIndisponivel"
Cohesion: 0.16
Nodes (17): buscar_pagamento(), buscar_pagamentos_por_referencia(), cancelar_pagamento(), MercadoPagoIndisponivel, Exception, Consulta o pagamento diretamente na API do Mercado Pago - fonte de verdade de…, Lista os pagamentos que o Mercado Pago associa a uma external_reference. Usada…, Cancela uma cobranca Pix pendente no Mercado Pago. Best-effort: nunca lanca. (+9 more)

### Community 47 - "d9e2f6a14c80_contatos_academia_perfis_professores.py"
Cohesion: 0.83
Nodes (3): _campos_professor(), downgrade(), upgrade()

## Knowledge Gaps
- **45 isolated node(s):** `modal`, `input_senha`, `icone_senha`, `campoBusca`, `linhasDeAlunos` (+40 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PagamentoDAO` connect `PagamentoDAO` to `adm_bp.py`, `criar_aluno`, `config.py`, `pix_bp.py`, `PagamentoEvento`, `checkout_bp.py`, `usuario_bp.py`?**
  _High betweenness centrality (0.256) - this node is a cross-community bridge._
- **Why does `Matricula` connect `config.py` to `turma_bp.py`, `Aluno Profile Page`, `PagamentoDAO`, `usuario_bp.py`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Why does `AlunoDAO` connect `adm_bp.py` to `test_perfil_e_foto.py`, `PagamentoDAO`, `turma_bp.py`, `criar_aluno`, `usuario_bp.py`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Are the 108 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 108 INFERRED edges - model-reasoned connections that need verification._
- **Are the 91 inferred relationships involving `criar_pagamento()` (e.g. with `PagamentoDAO` and `Pagamento`) actually correct?**
  _`criar_pagamento()` has 91 INFERRED edges - model-reasoned connections that need verification._
- **Are the 73 inferred relationships involving `logar_como_aluno()` (e.g. with `test_aluno_cria_checkout_da_propria_mensalidade()` and `test_aluno_nao_cria_checkout_de_mensalidade_de_outro_aluno()`) actually correct?**
  _`logar_como_aluno()` has 73 INFERRED edges - model-reasoned connections that need verification._
- **Are the 71 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 71 INFERRED edges - model-reasoned connections that need verification._