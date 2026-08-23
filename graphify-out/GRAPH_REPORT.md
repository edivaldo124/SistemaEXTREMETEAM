# Graph Report - SistemaEXTREMETEAM  (2026-08-22)

## Corpus Check
- 41 files · ~84,793 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 205 nodes · 499 edges · 9 communities (8 shown, 1 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 72 edges (avg confidence: 0.92)
- Token cost: 138,366 input · 0 output

## Community Hubs (Navigation)
- Turma & Class Management
- Templates & Static Assets
- Admin Blueprint
- Auth & User Registration
- Data Access & Domain Models
- Deployment & Server Bootstrap
- Admin Panel Frontend (JS)
- Login Modal Frontend (JS)
- Project README

## God Nodes (most connected - your core abstractions)
1. `AlunoDAO` - 28 edges
2. `MatriculaDAO` - 14 edges
3. `PlanoDAO` - 14 edges
4. `ProfessorDAO` - 14 edges
5. `Aluno Profile Page` - 14 edges
6. `usuario_e_admin()` - 13 edges
7. `PagamentoDAO` - 12 edges
8. `Admin Dashboard Page` - 12 edges
9. `detalhes_usuario()` - 11 edges
10. `detalhe_turma()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `Cadastrar Plano Form` --shares_data_with--> `Plano`  [INFERRED]
  templates/pgAdm.html → modelos/plano.py
- `Planos Disponíveis Section` --shares_data_with--> `Plano`  [INFERRED]
  templates/pgUsuario.html → modelos/plano.py
- `Presença Form` --shares_data_with--> `Presenca`  [INFERRED]
  templates/turma.html → modelos/presenca.py
- `Aluno Detail/Admin Page` --shares_data_with--> `Matricula`  [INFERRED]
  templates/dt_aluno.html → modelos/matricula.py
- `Aluno Profile Page` --shares_data_with--> `Matricula`  [INFERRED]
  templates/pgUsuario.html → modelos/matricula.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Shared Confirmation Modal Pattern** — templates_components_confirm_modal_dialog, templates_pgadm_page, templates_pgprofessor_page, templates_pgusuario_page, templates_turmas_page [EXTRACTED 1.00]
- **Mensalidade (Billing) Management Flow** — templates_dt_aluno_pagamento_form, templates_pgusuario_mensalidades_section, modelos_pagamento_pagamento, modelos_plano_plano [INFERRED 0.85]
- **Turma and Attendance Management Flow** — templates_turmas_turma_form, templates_turma_presenca_form, templates_pgprofessor_page, modelos_turma_turma [INFERRED 0.85]

## Communities (9 total, 1 thin omitted)

### Community 0 - "Turma & Class Management"
Cohesion: 0.11
Nodes (22): _acesso_permitido(), cadastrar_professor(), cadastrar_turma(), desmatricular_aluno(), detalhe_turma(), gerenciar_turmas(), matricular_aluno(), painel_professor() (+14 more)

### Community 1 - "Templates & Static Assets"
Cohesion: 0.09
Nodes (24): Usuario Model, Extreme Team Logo Image, Academia do Bitelo Logo, formatadorDePreco, gradePlanos, cadastro-form Registration Form, Cadastro (Registration) Page, Confirm Dialog Component (+16 more)

### Community 2 - "Admin Blueprint"
Cohesion: 0.14
Nodes (20): alterar_mensalidade(), aprovar_aluno(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_pagamento(), cadastrar_plano(), desativar_aluno(), detalhes_usuario() (+12 more)

### Community 3 - "Auth & User Registration"
Cohesion: 0.18
Nodes (10): pagina_cadastro(), pagina_login(), pagina_perfil(), route, recuperar_senha(), Aluno, formatar_cpf(), formatar_telefone() (+2 more)

### Community 4 - "Data Access & Domain Models"
Cohesion: 0.15
Nodes (7): PresencaDAO, Matricula, Pagamento, Presenca, Aluno Mensalidade Launch Form, preencherValor() Inline Script, Histórico de Mensalidades Section

### Community 5 - "Deployment & Server Bootstrap"
Cohesion: 0.16
Nodes (13): Flask App Service (compose), Postgres DB Service (compose), postgres_data Volume, Flask, Flask-SQLAlchemy, Gunicorn, psycopg2-binary, python-dotenv (+5 more)

### Community 6 - "Admin Panel Frontend (JS)"
Cohesion: 0.20
Nodes (10): atualizarListaDeAlunos(), avisoSemResultados, campoBusca, campoDuracao, campoPreco, contadorAlunos, formatadorDePreco, formularioPlano (+2 more)

### Community 7 - "Login Modal Frontend (JS)"
Cohesion: 0.25
Nodes (8): abrirmodal(), fechar(), icone_senha, input_senha, modal, mostrarSenha(), meuModal Login Modal, login-form Login Form

## Knowledge Gaps
- **24 isolated node(s):** `modal`, `input_senha`, `icone_senha`, `campoBusca`, `linhasDeAlunos` (+19 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Admin Dashboard Page` connect `Templates & Static Assets` to `Admin Blueprint`, `Admin Panel Frontend (JS)`?**
  _High betweenness centrality (0.164) - this node is a cross-community bridge._
- **Why does `AlunoDAO` connect `Admin Blueprint` to `Turma & Class Management`, `Auth & User Registration`?**
  _High betweenness centrality (0.159) - this node is a cross-community bridge._
- **Why does `Aluno Profile Page` connect `Templates & Static Assets` to `Data Access & Domain Models`?**
  _High betweenness centrality (0.114) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `AlunoDAO` (e.g. with `alterar_mensalidade()` and `aprovar_aluno()`) actually correct?**
  _`AlunoDAO` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `MatriculaDAO` (e.g. with `desmatricular_aluno()` and `detalhe_turma()`) actually correct?**
  _`MatriculaDAO` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `PlanoDAO` (e.g. with `cadastrar_pagamento()` and `cadastrar_plano()`) actually correct?**
  _`PlanoDAO` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `ProfessorDAO` (e.g. with `cadastrar_professor()` and `gerenciar_turmas()`) actually correct?**
  _`ProfessorDAO` has 6 INFERRED edges - model-reasoned connections that need verification._