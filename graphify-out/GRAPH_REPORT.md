# Graph Report - SistemaEXTREMETEAM  (2026-09-05)

## Corpus Check
- 58 files · ~104,117 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 480 nodes · 1192 edges · 16 communities (13 shown, 3 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 134 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3d6cabf4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- turma_bp.py
- Aluno Profile Page
- adm_bp.py
- usuario_bp.py
- PagamentoDAO
- servidor.py
- pgAdm.js
- pix_bp.py
- SistemaEXTREMETEAM Project
- test_mercado_pago_servico.py
- test_pix_rotas.py
- Pagamento
- test_migracao_checkout.py
- checkout.js
- CLAUDE.md

## God Nodes (most connected - your core abstractions)
1. `PagamentoDAO` - 91 edges
2. `AlunoDAO` - 30 edges
3. `MercadoPagoIndisponivel` - 26 edges
4. `_preparar_retorno()` - 19 edges
5. `_mockar_preferencia()` - 16 edges
6. `usuario_e_admin()` - 16 edges
7. `criar_pagamento_pix()` - 15 edges
8. `_processar_status_mp()` - 14 edges
9. `buscar_pagamento()` - 14 edges
10. `Aluno Profile Page` - 14 edges

## Surprising Connections (you probably didn't know these)
- `Histórico de Mensalidades Section` --shares_data_with--> `Pagamento`  [INFERRED]
  templates/pgUsuario.html → modelos/pagamento.py
- `Aluno Detail/Admin Page` --shares_data_with--> `Matricula`  [INFERRED]
  templates/dt_aluno.html → modelos/matricula.py
- `Aluno Profile Page` --shares_data_with--> `Matricula`  [INFERRED]
  templates/pgUsuario.html → modelos/matricula.py
- `Turma Detail Page` --shares_data_with--> `Turma`  [INFERRED]
  templates/turma.html → modelos/turma.py
- `Cadastrar Plano Form` --shares_data_with--> `Plano`  [INFERRED]
  templates/pgAdm.html → modelos/plano.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Shared Confirmation Modal Pattern** — templates_components_confirm_modal_dialog, templates_pgadm_page, templates_pgprofessor_page, templates_pgusuario_page, templates_turmas_page [EXTRACTED 1.00]
- **Mensalidade (Billing) Management Flow** — templates_dt_aluno_pagamento_form, templates_pgusuario_mensalidades_section, modelos_pagamento_pagamento, modelos_plano_plano [INFERRED 0.85]
- **Turma and Attendance Management Flow** — templates_turmas_turma_form, templates_turma_presenca_form, templates_pgprofessor_page, modelos_turma_turma [INFERRED 0.85]

## Communities (16 total, 3 thin omitted)

### Community 0 - "turma_bp.py"
Cohesion: 0.08
Nodes (26): _acesso_permitido(), cadastrar_professor(), cadastrar_turma(), desmatricular_aluno(), detalhe_turma(), gerenciar_turmas(), matricular_aluno(), painel_professor() (+18 more)

### Community 1 - "Aluno Profile Page"
Cohesion: 0.08
Nodes (29): Usuario Model, Extreme Team Logo Image, Academia do Bitelo Logo, abrirmodal(), fechar(), icone_senha, input_senha, modal (+21 more)

### Community 2 - "adm_bp.py"
Cohesion: 0.11
Nodes (29): alterar_mensalidade(), aprovar_aluno(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_pagamento(), cadastrar_plano(), cobrar_inadimplentes(), cobrar_mensalidade() (+21 more)

### Community 3 - "usuario_bp.py"
Cohesion: 0.12
Nodes (30): _acesso_permitido_pagamento(), alterar_senha_perfil(), _aluno_da_sessao(), atualizar_dados_perfil(), comprovante_mensalidade(), confirmar_email(), enviar_comprovante_manual_aluno(), enviar_foto_perfil() (+22 more)

### Community 4 - "PagamentoDAO"
Cohesion: 0.06
Nodes (57): PagamentoDAO, True se a cobrança Pix já gerada para este pagamento ainda pode ser…, Solta a preferência atual para que a próxima tentativa crie uma nova. Nunca…, forma_pagamento vem do que o Mercado Pago confirmou na consulta à API ('pix',…, Totais do painel financeiro - sempre calculados no backend a partir do banco,…, _assinar(), _mockar_preferencia(), _pagamento_mp() (+49 more)

### Community 5 - "servidor.py"
Cohesion: 0.16
Nodes (13): Flask App Service (compose), Postgres DB Service (compose), postgres_data Volume, Flask, Flask-SQLAlchemy, Gunicorn, psycopg2-binary, python-dotenv (+5 more)

### Community 6 - "pgAdm.js"
Cohesion: 0.20
Nodes (10): atualizarListaDeAlunos(), avisoSemResultados, campoBusca, campoDuracao, campoPreco, contadorAlunos, formatadorDePreco, formularioPlano (+2 more)

### Community 7 - "pix_bp.py"
Cohesion: 0.06
Nodes (71): abrir_checkout(), _acesso_permitido(), route, Checkout Pro do Mercado Pago - "outras formas de pagamento" (cartão, boleto,…, Volta do Mercado Pago. Ignora por completo `status`, `payment_id`,…, Mesma regra já usada no Pix e na página de pagamento: o próprio aluno ou o…, back_urls absolutas para onde o Mercado Pago devolve o aluno. Os três destinos…, Cria (ou reaproveita) a preferência do Checkout Pro e redireciona para o… (+63 more)

### Community 9 - "test_mercado_pago_servico.py"
Cohesion: 0.07
Nodes (35): ambiente_mercado_pago(), Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, Diz se a integracao esta apontando para producao ou para o sandbox. Prioriza a…, validar_assinatura_webhook(), base_url(), _criar_preferencia(), _FakePaymentResource, _FakePreferenceResource (+27 more)

### Community 10 - "test_pix_rotas.py"
Cohesion: 0.20
Nodes (17): _assinar(), _resposta_consulta(), _resposta_criacao(), test_admin_tambem_pode_gerar_pix(), test_aluno_gera_pix_da_propria_mensalidade(), test_falha_de_indisponibilidade_do_mp_retorna_503(), test_impede_cobranca_duplicada_em_chamadas_consecutivas(), test_reutiliza_cobranca_pendente_valida() (+9 more)

### Community 11 - "Pagamento"
Cohesion: 0.20
Nodes (7): Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.…, Cria a cobrança da contratação ou reutiliza a equivalente em aberto. O preço…, Pagamento, _para_decimal(), Aluno Mensalidade Launch Form, preencherValor() Inline Script, Histórico de Mensalidades Section

### Community 12 - "test_migracao_checkout.py"
Cohesion: 0.31
Nodes (8): _colunas(), conexao(), migracao(), fixture, Exercita a migração dos campos do Checkout Pro de verdade (upgrade e…, _rodar(), test_downgrade_remove_exatamente_o_que_o_upgrade_criou(), test_upgrade_adiciona_as_colunas_e_preserva_linhas_antigas()

## Knowledge Gaps
- **25 isolated node(s):** `graphify`, `icone_senha`, `input_senha`, `modal`, `formatadorDePreco` (+20 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PagamentoDAO` connect `PagamentoDAO` to `adm_bp.py`, `usuario_bp.py`, `pix_bp.py`, `test_pix_rotas.py`, `Pagamento`?**
  _High betweenness centrality (0.326) - this node is a cross-community bridge._
- **Why does `Pagamento` connect `Pagamento` to `adm_bp.py`, `PagamentoDAO`, `pix_bp.py`?**
  _High betweenness centrality (0.091) - this node is a cross-community bridge._
- **Why does `Aluno Profile Page` connect `Aluno Profile Page` to `turma_bp.py`, `adm_bp.py`, `Pagamento`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Are the 57 inferred relationships involving `PagamentoDAO` (e.g. with `atualizar_status_pagamento()` and `cadastrar_pagamento()`) actually correct?**
  _`PagamentoDAO` has 57 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `AlunoDAO` (e.g. with `alterar_mensalidade()` and `aprovar_aluno()`) actually correct?**
  _`AlunoDAO` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `MercadoPagoIndisponivel` (e.g. with `abrir_checkout()` and `retorno_checkout()`) actually correct?**
  _`MercadoPagoIndisponivel` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `graphify`, `icone_senha`, `input_senha` to the rest of the system?**
  _25 weakly-connected nodes found - possible documentation gaps or missing edges._