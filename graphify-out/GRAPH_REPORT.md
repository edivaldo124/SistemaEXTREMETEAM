# Graph Report - SistemaEXTREMETEAM  (2026-09-05)

## Corpus Check
- 69 files · ~121,799 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 838 nodes · 2357 edges · 41 communities (36 shown, 5 thin omitted)
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 505 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d3650543`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- turma_bp.py
- Aluno Profile Page
- adm_bp.py
- armazenamento.py
- PagamentoDAO
- servidor.py
- pgAdm.js
- Relatório de segurança — Sistema Extreme Team
- SistemaEXTREMETEAM Project
- test_mercado_pago_servico.py
- logar_como_aluno
- financeiroDAO.py
- test_migracao_checkout.py
- checkout.js
- CLAUDE.md
- planos.py
- pix_bp.py
- PagamentoEvento
- checkout_bp.py
- mercado_pago.py
- pix.js
- test_seguranca.py
- env.py
- pagamento.js
- c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py
- _FakePaymentResource
- usuario_bp.py
- buscar_pagamento
- ambiente_mercado_pago
- route
- pagina_cadastro
- buscar_pagamentos_por_referencia

## God Nodes (most connected - your core abstractions)
1. `PagamentoDAO` - 166 edges
2. `criar_pagamento()` - 93 edges
3. `logar_como_aluno()` - 75 edges
4. `criar_aluno()` - 73 edges
5. `AlunoDAO` - 47 edges
6. `MercadoPagoIndisponivel` - 26 edges
7. `SolicitacaoPlanoDAO` - 23 edges
8. `Aluno` - 23 edges
9. `usuario_e_admin()` - 21 edges
10. `PagamentoEvento` - 21 edges

## Surprising Connections (you probably didn't know these)
- `Aluno Detail/Admin Page` --shares_data_with--> `Matricula`  [INFERRED]
  templates/dt_aluno.html → modelos/matricula.py
- `Aluno Profile Page` --shares_data_with--> `Matricula`  [INFERRED]
  templates/pgUsuario.html → modelos/matricula.py
- `Aluno Mensalidade Launch Form` --shares_data_with--> `Pagamento`  [INFERRED]
  templates/dt_aluno.html → modelos/pagamento.py
- `Histórico de Mensalidades Section` --shares_data_with--> `Pagamento`  [INFERRED]
  templates/pgUsuario.html → modelos/pagamento.py
- `Cadastrar Plano Form` --shares_data_with--> `Plano`  [INFERRED]
  templates/pgAdm.html → modelos/plano.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Shared Confirmation Modal Pattern** — templates_components_confirm_modal_dialog, templates_pgadm_page, templates_pgprofessor_page, templates_pgusuario_page, templates_turmas_page [EXTRACTED 1.00]
- **Mensalidade (Billing) Management Flow** — templates_dt_aluno_pagamento_form, templates_pgusuario_mensalidades_section, modelos_pagamento_pagamento, modelos_plano_plano [INFERRED 0.85]
- **Turma and Attendance Management Flow** — templates_turmas_turma_form, templates_turma_presenca_form, templates_pgprofessor_page, modelos_turma_turma [INFERRED 0.85]

## Communities (41 total, 5 thin omitted)

### Community 0 - "turma_bp.py"
Cohesion: 0.07
Nodes (35): _acesso_permitido(), cadastrar_professor(), cadastrar_turma(), desmatricular_aluno(), detalhe_turma(), gerenciar_turmas(), matricular_aluno(), painel_professor() (+27 more)

### Community 1 - "Aluno Profile Page"
Cohesion: 0.07
Nodes (31): Usuario Model, Extreme Team Logo Image, Academia do Bitelo Logo, abrirmodal(), fechar(), icone_senha, input_senha, modal (+23 more)

### Community 2 - "adm_bp.py"
Cohesion: 0.07
Nodes (51): aprovar_aluno(), aprovar_comprovante_manual(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_pagamento(), cadastrar_plano(), cancelar_mudanca_plano_admin(), cobrar_inadimplentes() (+43 more)

### Community 3 - "armazenamento.py"
Cohesion: 0.21
Nodes (14): ArquivoInvalido, caminho_arquivo(), _detectar_tipo_imagem_real(), _pasta(), Exception, _raiz_uploads(), Armazenamento de arquivos enviados por usuários (fotos de perfil, comprovantes…, Resolve o caminho em disco de um arquivo já salvo, ou None se não existir/for… (+6 more)

### Community 4 - "PagamentoDAO"
Cohesion: 0.06
Nodes (90): mensalidade_destaque(), PagamentoDAO, True se já existe um Pix ou um checkout válido emitido para esta cobrança.…, Escolhe a mensalidade mais relevante para o card 'Minha mensalidade': a mais…, True se a cobrança Pix já gerada para este pagamento ainda pode ser…, True se a preferência do Checkout Pro já criada pode ser reaproveitada. Só…, Solta a preferência atual para que a próxima tentativa crie uma nova. Nunca…, Totais do painel financeiro - sempre calculados no backend a partir do banco,… (+82 more)

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
Cohesion: 0.13
Nodes (24): Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, validar_assinatura_webhook(), base_url(), _criar_preferencia(), _FakePreferenceResource, mp_fake(), fixture, parametrize (+16 more)

### Community 10 - "logar_como_aluno"
Cohesion: 0.06
Nodes (83): Persistência dos pedidos de troca de plano agendados para a próxima renovação., Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, Aplica um pedido agendado cujo período de origem já terminou sem renovação.…, Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, Com uma troca já agendada, só dois planos fazem sentido num pedido de…, A cobrança do período seguinte tem de nascer no plano que o aluno agendou.…, `pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -…, SolicitacaoPlanoDAO (+75 more)

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
Cohesion: 0.07
Nodes (15): Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda. O…, Primeiro dia não coberto por outra mensalidade do mesmo aluno., Define o período coberto por uma mensalidade que ainda não tem um (lançamento…, Abre o período de acesso no momento em que o pagamento é confirmado. Se a…, Reescreve os campos denormalizados do aluno a partir das mensalidades.…, forma_pagamento vem do que o Mercado Pago confirmou na consulta à API ('pix',…, Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.…, O que aconteceu numa tentativa de contratar/renovar/trocar de plano. (+7 more)

### Community 19 - "checkout_bp.py"
Cohesion: 0.16
Nodes (16): abrir_checkout(), _acesso_permitido(), route, Checkout Pro do Mercado Pago - "outras formas de pagamento" (cartão, boleto,…, Volta do Mercado Pago. Ignora por completo `status`, `payment_id`,…, Mesma regra já usada no Pix e na página de pagamento: o próprio aluno ou o…, back_urls absolutas para onde o Mercado Pago devolve o aluno. Os três destinos…, Cria (ou reaproveita) a preferência do Checkout Pro e redireciona para o… (+8 more)

### Community 20 - "mercado_pago.py"
Cohesion: 0.13
Nodes (28): Decimal, _base_url_opcional(), base_url_publica(), cancelar_pagamento(), criar_pagamento_pix(), criar_preferencia_checkout(), _erro_menciona(), _erro_menciona_expiracao() (+20 more)

### Community 21 - "pix.js"
Cohesion: 0.42
Nodes (11): abrirPix(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), limparConteudoAnterior(), mensagemDeErro(), mostrarEstado() (+3 more)

### Community 22 - "test_seguranca.py"
Cohesion: 0.14
Nodes (9): erro_validacao_senha(), Retorna uma mensagem quando a senha é curta, comum ou igual ao identificador., _imagem_jpeg(), test_api_post_aceita_token_csrf_no_cabecalho(), test_limite_de_login_por_ip_e_identificador(), test_recuperacao_envia_link_da_url_configurada(), test_rotas_admin_nao_colidem_cpf_com_campos_editaveis(), test_senha_recusa_valores_curtos_comuns_e_iguais_ao_login() (+1 more)

### Community 23 - "env.py"
Cohesion: 0.39
Nodes (7): get_engine(), get_engine_url(), get_metadata(), Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online()

### Community 24 - "pagamento.js"
Cohesion: 0.67
Nodes (6): consultarStatus(), gerarOuAtualizarPix(), iniciarPolling(), mostrarEstado(), pararPolling(), tratarResposta()

### Community 25 - "c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py"
Cohesion: 0.60
Nodes (5): _backfill_vigencia(), _colunas(), _criar_tabela_solicitacoes(), downgrade(), upgrade()

### Community 33 - "usuario_bp.py"
Cohesion: 0.23
Nodes (14): _acesso_permitido_pagamento(), comprovante_mensalidade(), confirmar_email(), foto_perfil(), _pagamento_com_acesso_ou_404(), pagina_pagamento(), pagina_perfil(), _plano_do_formulario() (+6 more)

### Community 34 - "buscar_pagamento"
Cohesion: 0.40
Nodes (5): buscar_pagamento(), Consulta o pagamento diretamente na API do Mercado Pago - fonte de verdade de…, test_buscar_pagamento_expoe_meio_de_pagamento_e_moeda(), test_buscar_pagamento_falha_de_transporte_levanta_indisponivel(), test_buscar_pagamento_sucesso()

### Community 35 - "ambiente_mercado_pago"
Cohesion: 0.20
Nodes (10): ambiente_mercado_pago(), ConfiguracaoInvalida, Exception, Variavel de ambiente obrigatoria ausente ou com formato invalido. Erro de…, Diz se a integracao esta apontando para producao ou para o sandbox. Prioriza a…, test_configuracao_ausente_falha_de_forma_explicita(), test_ambiente_assume_producao_para_token_sem_prefixo_de_teste(), test_ambiente_cai_no_prefixo_do_token_quando_nao_configurado() (+2 more)

### Community 36 - "route"
Cohesion: 0.23
Nodes (14): alterar_senha_perfil(), _aluno_da_sessao(), atualizar_dados_perfil(), cancelar_mudanca_plano(), enviar_comprovante_manual_aluno(), enviar_foto_perfil(), route, Cancela um pedido de troca antes de ele ser aplicado. Depois de efetivado não… (+6 more)

### Community 37 - "pagina_cadastro"
Cohesion: 0.36
Nodes (9): pagina_cadastro(), pagina_login(), recuperar_senha(), limit, formatar_cpf(), formatar_telefone(), somente_digitos(), variantes_cpf() (+1 more)

### Community 38 - "buscar_pagamentos_por_referencia"
Cohesion: 0.40
Nodes (5): buscar_pagamentos_por_referencia(), Lista os pagamentos que o Mercado Pago associa a uma external_reference. Usada…, test_buscar_pagamentos_por_referencia_falha_de_transporte(), test_buscar_pagamentos_por_referencia_normaliza_resultados(), test_buscar_pagamentos_por_referencia_sem_resultado()

## Knowledge Gaps
- **45 isolated node(s):** `modal`, `input_senha`, `icone_senha`, `campoBusca`, `linhasDeAlunos` (+40 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PagamentoDAO` connect `PagamentoDAO` to `turma_bp.py`, `usuario_bp.py`, `adm_bp.py`, `ambiente_mercado_pago`, `route`, `logar_como_aluno`, `financeiroDAO.py`, `pix_bp.py`, `PagamentoEvento`, `checkout_bp.py`, `mercado_pago.py`, `test_seguranca.py`?**
  _High betweenness centrality (0.278) - this node is a cross-community bridge._
- **Why does `Matricula` connect `turma_bp.py` to `usuario_bp.py`, `financeiroDAO.py`, `PagamentoDAO`, `Aluno Profile Page`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Why does `AlunoDAO` connect `adm_bp.py` to `turma_bp.py`, `usuario_bp.py`, `PagamentoDAO`, `pagina_cadastro`, `logar_como_aluno`, `financeiroDAO.py`, `test_seguranca.py`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 108 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 108 INFERRED edges - model-reasoned connections that need verification._
- **Are the 91 inferred relationships involving `criar_pagamento()` (e.g. with `PagamentoDAO` and `Pagamento`) actually correct?**
  _`criar_pagamento()` has 91 INFERRED edges - model-reasoned connections that need verification._
- **Are the 73 inferred relationships involving `logar_como_aluno()` (e.g. with `test_aluno_cria_checkout_da_propria_mensalidade()` and `test_aluno_nao_cria_checkout_de_mensalidade_de_outro_aluno()`) actually correct?**
  _`logar_como_aluno()` has 73 INFERRED edges - model-reasoned connections that need verification._
- **Are the 71 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 71 INFERRED edges - model-reasoned connections that need verification._