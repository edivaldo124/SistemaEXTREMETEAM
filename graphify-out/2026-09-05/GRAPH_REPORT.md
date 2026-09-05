# Graph Report - SistemaEXTREMETEAM  (2026-08-24)

## Corpus Check
- 28 files · ~82,268 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 222 nodes · 567 edges · 8 communities (7 shown, 1 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 82 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d08a5d1e`
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
- SistemaEXTREMETEAM Project

## God Nodes (most connected - your core abstractions)
1. `AlunoDAO` - 33 edges
2. `Aluno` - 18 edges
3. `usuario_e_admin()` - 16 edges
4. `MatriculaDAO` - 14 edges
5. `PlanoDAO` - 14 edges
6. `ProfessorDAO` - 14 edges
7. `enviar_email()` - 14 edges
8. `Aluno Profile Page` - 14 edges
9. `detalhes_usuario()` - 12 edges
10. `PagamentoDAO` - 12 edges

## Surprising Connections (you probably didn't know these)
- `Aluno Detail/Admin Page` --shares_data_with--> `Matricula`  [INFERRED]
  templates/dt_aluno.html → modelos/matricula.py
- `Aluno Profile Page` --shares_data_with--> `Matricula`  [INFERRED]
  templates/pgUsuario.html → modelos/matricula.py
- `Histórico de Mensalidades Section` --shares_data_with--> `Pagamento`  [INFERRED]
  templates/pgUsuario.html → modelos/pagamento.py
- `Cadastrar Plano Form` --shares_data_with--> `Plano`  [INFERRED]
  templates/pgAdm.html → modelos/plano.py
- `Planos Disponíveis Section` --shares_data_with--> `Plano`  [INFERRED]
  templates/pgUsuario.html → modelos/plano.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Shared Confirmation Modal Pattern** — templates_components_confirm_modal_dialog, templates_pgadm_page, templates_pgprofessor_page, templates_pgusuario_page, templates_turmas_page [EXTRACTED 1.00]
- **Mensalidade (Billing) Management Flow** — templates_dt_aluno_pagamento_form, templates_pgusuario_mensalidades_section, modelos_pagamento_pagamento, modelos_plano_plano [INFERRED 0.85]
- **Turma and Attendance Management Flow** — templates_turmas_turma_form, templates_turma_presenca_form, templates_pgprofessor_page, modelos_turma_turma [INFERRED 0.85]

## Communities (8 total, 1 thin omitted)

### Community 0 - "turma_bp.py"
Cohesion: 0.10
Nodes (23): _acesso_permitido(), cadastrar_professor(), cadastrar_turma(), desmatricular_aluno(), detalhe_turma(), gerenciar_turmas(), matricular_aluno(), painel_professor() (+15 more)

### Community 1 - "Aluno Profile Page"
Cohesion: 0.08
Nodes (29): Usuario Model, Extreme Team Logo Image, Academia do Bitelo Logo, abrirmodal(), fechar(), icone_senha, input_senha, modal (+21 more)

### Community 2 - "adm_bp.py"
Cohesion: 0.10
Nodes (31): alterar_mensalidade(), aprovar_aluno(), ativar_aluno(), cadastrar_pagamento(), cadastrar_plano(), cobrar_inadimplentes(), cobrar_mensalidade(), desativar_aluno() (+23 more)

### Community 3 - "usuario_bp.py"
Cohesion: 0.20
Nodes (17): alterar_senha_perfil(), _aluno_da_sessao(), atualizar_dados_perfil(), confirmar_email(), pagina_cadastro(), pagina_login(), route, recuperar_senha() (+9 more)

### Community 4 - "PagamentoDAO"
Cohesion: 0.17
Nodes (6): atualizar_status_pagamento(), pagina_perfil(), PagamentoDAO, PresencaDAO, Presenca, Presença Form

### Community 5 - "servidor.py"
Cohesion: 0.16
Nodes (13): Flask App Service (compose), Postgres DB Service (compose), postgres_data Volume, Flask, Flask-SQLAlchemy, Gunicorn, psycopg2-binary, python-dotenv (+5 more)

### Community 6 - "pgAdm.js"
Cohesion: 0.20
Nodes (10): atualizarListaDeAlunos(), avisoSemResultados, campoBusca, campoDuracao, campoPreco, contadorAlunos, formatadorDePreco, formularioPlano (+2 more)

## Knowledge Gaps
- **24 isolated node(s):** `modal`, `input_senha`, `icone_senha`, `campoBusca`, `linhasDeAlunos` (+19 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Admin Dashboard Page` connect `Aluno Profile Page` to `adm_bp.py`, `pgAdm.js`?**
  _High betweenness centrality (0.161) - this node is a cross-community bridge._
- **Why does `AlunoDAO` connect `adm_bp.py` to `turma_bp.py`, `usuario_bp.py`?**
  _High betweenness centrality (0.160) - this node is a cross-community bridge._
- **Why does `Aluno Profile Page` connect `Aluno Profile Page` to `turma_bp.py`, `adm_bp.py`?**
  _High betweenness centrality (0.105) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `AlunoDAO` (e.g. with `alterar_mensalidade()` and `aprovar_aluno()`) actually correct?**
  _`AlunoDAO` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `Aluno` (e.g. with `detalhes_usuario()` and `_aluno_da_sessao()`) actually correct?**
  _`Aluno` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `MatriculaDAO` (e.g. with `desmatricular_aluno()` and `detalhe_turma()`) actually correct?**
  _`MatriculaDAO` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `modal`, `input_senha`, `icone_senha` to the rest of the system?**
  _24 weakly-connected nodes found - possible documentation gaps or missing edges._