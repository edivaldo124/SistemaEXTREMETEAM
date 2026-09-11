# Graph Report - SistemaEXTREMETEAM  (2026-09-10)

## Corpus Check
- 92 files · ~143,496 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1160 nodes · 3197 edges · 66 communities (58 shown, 8 thin omitted)
- Extraction: 77% EXTRACTED · 23% INFERRED · 0% AMBIGUOUS · INFERRED: 721 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c36d63d7`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_perfil_e_foto.py
- Aluno Profile Page
- financeiroDAO.py
- test_plano_vigencia.py
- test_limites_pagamento.py
- servidor.py
- PagamentoDAO
- Relatório de segurança — Sistema Extreme Team
- SistemaEXTREMETEAM Project
- test_mercado_pago_servico.py
- criar_aluno
- turma_bp.py
- test_migracao_checkout.py
- checkout.js
- CLAUDE.md
- planos.py
- pix_bp.py
- AlunoDAO
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
- adm_bp.py
- ProfessorDAO
- Academia
- convites.py
- Professor
- pagamento_polling.test.cjs
- ResultadoContratacao
- criar_pagamento
- test_pix_rotas.py
- test_checkout_rotas.py
- d9e2f6a14c80_contatos_academia_perfis_professores.py
- enviar_email
- botao_ocupado.test.cjs
- Flask App Service (compose)
- checkout_abertura.test.cjs
- filtros_financeiro.js
- criar_preferencia_checkout
- limites_pagamento.py
- test_contratacao_plano.py
- test_seguranca.py
- armazenamento.py
- test_keep_alive.py
- keep_alive.py
- pagina_cadastro
- ._promover_vencidos
- e4b7c2a91d35_cadastro_administrativo_e_convite_de_acesso.py

## God Nodes (most connected - your core abstractions)
1. `PagamentoDAO` - 186 edges
2. `criar_pagamento()` - 131 edges
3. `logar_como_aluno()` - 101 edges
4. `criar_aluno()` - 87 edges
5. `AlunoDAO` - 70 edges
6. `logar_como_admin()` - 62 edges
7. `Aluno` - 45 edges
8. `ProfessorDAO` - 31 edges
9. `Professor` - 29 edges
10. `MercadoPagoIndisponivel` - 28 edges

## Surprising Connections (you probably didn't know these)
- `Histórico de Mensalidades Section` --shares_data_with--> `Pagamento`  [INFERRED]
  templates/pgUsuario.html → modelos/pagamento.py
- `Presença Form` --shares_data_with--> `Presenca`  [INFERRED]
  templates/turma.html → modelos/presenca.py
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

## Communities (66 total, 8 thin omitted)

### Community 0 - "test_perfil_e_foto.py"
Cohesion: 0.14
Nodes (17): cadastrar_turma(), remover_turma(), TurmaDAO, Turma, Cadastrar Turma Form, Sonda: a data vem da query string e é convertida sem tratamento., test_data_invalida_na_turma_nao_derruba_a_rota(), fixture (+9 more)

### Community 1 - "Aluno Profile Page"
Cohesion: 0.05
Nodes (43): Usuario Model, Extreme Team Logo Image, Academia do Bitelo Logo, abrirmodal(), fechar(), icone_senha, input_senha, modal (+35 more)

### Community 2 - "financeiroDAO.py"
Cohesion: 0.10
Nodes (23): Decimal, Pagamento, _para_decimal(), Plano, Pedido de troca de plano agendado para a próxima renovação. Nunca altera o…, SolicitacaoMudancaPlano, Cadastrar Plano Form, Planos Disponíveis Section (+15 more)

### Community 3 - "test_plano_vigencia.py"
Cohesion: 0.11
Nodes (30): Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, Com uma troca já agendada, só dois planos fazem sentido num pedido de…, A cobrança do período seguinte tem de nascer no plano que o aluno agendou.…, _pagar(), Vigência do plano: o que decide "Plano ativo" é o período pago, não o cadastro.…, Mensalidade paga cobrindo um período - o que de fato ativa o plano., Quem paga uma cobrança vencida há semanas tem de receber os 30 dias a partir da… (+22 more)

### Community 4 - "test_limites_pagamento.py"
Cohesion: 0.15
Nodes (16): consultar_mp(), fixture, parametrize, Limites de pagamento por conta, com o provedor inteiramente simulado., _sessao_admin(), _sessao_aluno(), test_admin_limite_por_usuario_persiste_entre_sessoes(), test_alunos_no_mesmo_ip_tem_limites_separados() (+8 more)

### Community 5 - "servidor.py"
Cohesion: 0.15
Nodes (15): after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, context_processor, errorhandler, adicionar_cabecalhos_de_seguranca(), contatos_da_academia(), erro_csrf() (+7 more)

### Community 6 - "PagamentoDAO"
Cohesion: 0.07
Nodes (30): mensalidade_destaque(), PagamentoDAO, True se já existe um Pix ou um checkout válido emitido para esta cobrança.…, Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda. O…, Primeiro dia não coberto por outra mensalidade do mesmo aluno., Define o período coberto por uma mensalidade que ainda não tem um (lançamento…, Abre o período de acesso no momento em que o pagamento é confirmado. Se a…, Reescreve os campos denormalizados do aluno a partir das mensalidades.… (+22 more)

### Community 7 - "Relatório de segurança — Sistema Extreme Team"
Cohesion: 0.08
Nodes (24): A verificar em execução, Atualização após as correções, F10 — Redirecionamento aberto via `Referer`, F11 — `/logout` aceita GET, F12 — Enumeração de usuários por tempo de resposta, F13 — Senha mínima de 6 caracteres, sem outros critérios, F14 — Webhook sem verificação de recência do timestamp, F15 — Curinga de `LIKE` no filtro do financeiro (+16 more)

### Community 9 - "test_mercado_pago_servico.py"
Cohesion: 0.14
Nodes (25): Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, validar_assinatura_webhook(), Hipótese: uma notificação capturada ontem pode ser reenviada hoje., test_webhook_recusa_assinatura_antiga(), base_url(), _criar_preferencia(), mp_fake(), fixture (+17 more)

### Community 10 - "criar_aluno"
Cohesion: 0.17
Nodes (28): Persistência dos pedidos de troca de plano agendados para a próxima renovação., Aplica um pedido agendado cujo período de origem já terminou sem renovação.…, SolicitacaoPlanoDAO, criar_aluno(), test_aluno_existente_continua_entrando_normalmente(), _agendar(), _pagar(), Mudança para um plano mais barato agendada para a próxima renovação. Regra… (+20 more)

### Community 11 - "turma_bp.py"
Cohesion: 0.15
Nodes (16): _acesso_permitido(), desmatricular_aluno(), detalhe_turma(), matricular_aluno(), registrar_presenca(), _turma_ou_404(), MatriculaDAO, PresencaDAO (+8 more)

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

### Community 18 - "AlunoDAO"
Cohesion: 0.07
Nodes (57): AlunoDAO, Matrícula feita no balcão: sem login, sem senha e sem convite de acesso. Nasce…, Aluno, Se existe uma conta de acesso, e não se o aluno está em dia ou matriculado.…, Convite de acesso já enviado e ainda não usado (a validade é checada na rota)., Chave do estado da CONTA - nunca da situação financeira nem da matrícula., logar_como_admin(), test_admin_salva_atualiza_e_limpa_contatos() (+49 more)

### Community 20 - "checkout_bp.py"
Cohesion: 0.10
Nodes (29): abrir_checkout(), _acesso_permitido(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), limitar_consulta_pagamento, limitar_criacao_pagamento, route (+21 more)

### Community 21 - "pix.js"
Cohesion: 0.33
Nodes (14): abrirPix(), alvoDoRotulo(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), liberarBotao(), limparConteudoAnterior() (+6 more)

### Community 22 - "usuario_bp.py"
Cohesion: 0.21
Nodes (17): _acesso_permitido_pagamento(), _aluno_da_sessao(), atualizar_dados_perfil(), cancelar_mudanca_plano(), comprovante_mensalidade(), confirmar_email(), foto_perfil(), _pagamento_com_acesso_ou_404() (+9 more)

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
Cohesion: 0.06
Nodes (46): _assinar(), _pagamento_mp(), _preparar_para_conciliacao(), parametrize, Auditoria de segurança: sondas escritas para TENTAR quebrar as regras. Nenhum…, Hipótese: a sessão de professor é aceita nas rotas financeiras do aluno., Hipótese: como o JS agora usa fetch, o POST perdeu a exigência de CSRF., Hipótese: as demais rotas de dinheiro aceitam POST sem token. (+38 more)

### Community 34 - "mercado_pago.py"
Cohesion: 0.12
Nodes (28): _base_url_opcional(), buscar_pagamento(), buscar_pagamentos_por_referencia(), cancelar_pagamento(), criar_pagamento_pix(), _erro_menciona(), _erro_menciona_expiracao(), _extrair_dados_pix() (+20 more)

### Community 35 - "adm_bp.py"
Cohesion: 0.08
Nodes (46): _aluno_do_cpf_ou_painel(), aprovar_aluno(), aprovar_comprovante_manual(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_aluno(), cadastrar_pagamento(), cadastrar_plano() (+38 more)

### Community 36 - "ProfessorDAO"
Cohesion: 0.16
Nodes (18): cadastrar_professor(), foto_professor(), gerenciar_turmas(), painel_professor(), route, remover_professor(), ProfessorDAO, _foto() (+10 more)

### Community 37 - "Academia"
Cohesion: 0.15
Nodes (15): configuracoes(), route, editar_professor(), Academia, admin_requerido(), link_email(), Normalização de contatos profissionais antes de montar links públicos., validar_email() (+7 more)

### Community 38 - "convites.py"
Cohesion: 0.15
Nodes (19): solicitar_troca_email(), aluno_do_token(), ConviteIndisponivel, descartar(), enviar(), gerar_token(), _hash(), RuntimeError (+11 more)

### Community 41 - "Professor"
Cohesion: 0.14
Nodes (9): Professor, Cadastrar Professor Form, test_publicacao_professor_nao_expoe_contatos_sem_permissao(), logar_como_professor(), fixture, Hipótese: a foto continua acessível por URL depois de tirar a publicação., Hipótese: os contatos vazam na home antes de a publicação ser marcada., test_contatos_do_professor_so_aparecem_quando_publicados() (+1 more)

### Community 42 - "pagamento_polling.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 44 - "criar_pagamento"
Cohesion: 0.10
Nodes (46): criar_pagamento(), logar_como_aluno(), Hipótese: forjar ?status=approved na volta do MP quita a mensalidade., test_retorno_ignora_status_aprovado_da_query_string(), _mockar_preferencia(), Um boleto pendente do Checkout Pro grava provider_payment_id, mas não é Pix:…, test_abertura_json_navega_sem_redirecionar_post_externo(), test_admin_tambem_pode_abrir_checkout() (+38 more)

### Community 45 - "test_pix_rotas.py"
Cohesion: 0.20
Nodes (20): _assinar(), _resposta_consulta(), _resposta_criacao(), test_admin_tambem_pode_gerar_pix(), test_aluno_gera_pix_da_propria_mensalidade(), test_aluno_nao_acessa_mensalidade_de_outro_aluno(), test_falha_de_indisponibilidade_do_mp_retorna_503(), test_impede_cobranca_duplicada_em_chamadas_consecutivas() (+12 more)

### Community 46 - "test_checkout_rotas.py"
Cohesion: 0.21
Nodes (26): _assinar(), _pagamento_mp(), _preparar_retorno(), parametrize, Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala…, Pix aberto e checkout concluído ao mesmo tempo: a consulta pelo…, _resposta_preferencia(), test_configuracao_ausente_falha_de_forma_explicita() (+18 more)

### Community 47 - "d9e2f6a14c80_contatos_academia_perfis_professores.py"
Cohesion: 0.83
Nodes (3): _campos_professor(), downgrade(), upgrade()

### Community 49 - "enviar_email"
Cohesion: 0.16
Nodes (13): alterar_senha_perfil(), ativar_acesso(), Transforma um cadastro feito no balcão na conta do próprio aluno. Quem chega…, redefinir_senha(), enviar_email(), Envia um e-mail transacional via Brevo. Retorna True/False; nunca lança., mascarar_email(), Mostra o bastante do e-mail para o dono se reconhecer, sem revelá-lo a… (+5 more)

### Community 50 - "botao_ocupado.test.cjs"
Cohesion: 0.18
Nodes (7): assert, criarElemento(), fs, montar(), path, test, vm

### Community 51 - "Flask App Service (compose)"
Cohesion: 0.22
Nodes (9): Flask App Service (compose), Postgres DB Service (compose), postgres_data Volume, Flask, Flask-SQLAlchemy, Gunicorn, psycopg2-binary, python-dotenv (+1 more)

### Community 52 - "checkout_abertura.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 55 - "criar_preferencia_checkout"
Cohesion: 0.22
Nodes (11): base_url_publica(), criar_preferencia_checkout(), Mantém a exceção pública usada pelo serviço do Mercado Pago., Cria uma preferencia do Checkout Pro (cartao, boleto, saldo MP, Pix e o que…, Escolhe init_point/sandbox_init_point conforme o ambiente. Em producao NUNCA…, _url_checkout(), url_webhook(), _valor_para_float() (+3 more)

### Community 56 - "limites_pagamento.py"
Cohesion: 0.50
Nodes (3): chave_pagamento(), Orçamentos compartilhados das chamadas interativas ao provedor de pagamento., A mesma conta mantém seu limite entre sessões, rotas e mensalidades. Alunos que…

### Community 57 - "test_contratacao_plano.py"
Cohesion: 0.29
Nodes (6): test_area_do_aluno_renderiza_telas_independentes_do_menu(), test_escolher_plano_cria_mensalidade_e_redireciona_para_pix(), test_plano_atual_continua_disponivel_para_gerar_cobranca(), test_plano_invalido_nao_cria_mensalidade(), test_reenvio_da_contratacao_reutiliza_mensalidade(), test_valor_enviado_pelo_navegador_e_ignorado()

### Community 58 - "test_seguranca.py"
Cohesion: 0.18
Nodes (5): _imagem_jpeg(), test_limite_de_login_por_ip_e_identificador(), test_recuperacao_envia_link_da_url_configurada(), test_rotas_admin_nao_colidem_cpf_com_campos_editaveis(), test_url_publica_independe_do_host_da_requisicao()

### Community 59 - "armazenamento.py"
Cohesion: 0.20
Nodes (17): enviar_comprovante_manual_aluno(), enviar_foto_perfil(), ArquivoInvalido, caminho_arquivo(), _detectar_tipo_imagem_real(), _pasta(), Exception, _raiz_uploads() (+9 more)

### Community 60 - "test_keep_alive.py"
Cohesion: 0.18
Nodes (6): ambiente_limpo(), fixture, parametrize, Garante que o keep-alive fica desligado por padrão e só pinga a própria origem., test_intervalo_fica_dentro_da_faixa(), test_nao_liga_com_valor_negativo()

### Community 61 - "keep_alive.py"
Cohesion: 0.29
Nodes (9): iniciar(), _intervalo(), _laco(), _ligado(), parar(), _pingar(), Mantém a aplicação acordada em hospedagens que hibernam por inatividade. O…, Encerra o laço. Usado pelos testes; em produção a thread é daemon. (+1 more)

### Community 62 - "pagina_cadastro"
Cohesion: 0.18
Nodes (15): _convidar_cadastro_existente(), pagina_cadastro(), pagina_login(), Cadastro administrativo que alguém tentou recriar pelo formulário público. Em…, recuperar_senha(), limit, formatar_cpf(), formatar_moeda() (+7 more)

## Knowledge Gaps
- **60 isolated node(s):** `modal`, `input_senha`, `icone_senha`, `campoBusca`, `linhasDeAlunos` (+55 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PagamentoDAO` connect `PagamentoDAO` to `test_auditoria_seguranca.py`, `financeiroDAO.py`, `adm_bp.py`, `test_plano_vigencia.py`, `criar_aluno`, `ResultadoContratacao`, `criar_pagamento`, `turma_bp.py`, `test_checkout_rotas.py`, `test_pix_rotas.py`, `pix_bp.py`, `AlunoDAO`, `checkout_bp.py`, `usuario_bp.py`, `test_contratacao_plano.py`, `test_seguranca.py`, `armazenamento.py`, `._promover_vencidos`?**
  _High betweenness centrality (0.244) - this node is a cross-community bridge._
- **Why does `AlunoDAO` connect `AlunoDAO` to `test_perfil_e_foto.py`, `financeiroDAO.py`, `adm_bp.py`, `PagamentoDAO`, `criar_aluno`, `turma_bp.py`, `usuario_bp.py`, `test_seguranca.py`, `pagina_cadastro`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Why does `Matricula` connect `turma_bp.py` to `Aluno Profile Page`, `financeiroDAO.py`, `usuario_bp.py`, `PagamentoDAO`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Are the 126 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 126 INFERRED edges - model-reasoned connections that need verification._
- **Are the 129 inferred relationships involving `criar_pagamento()` (e.g. with `PagamentoDAO` and `Pagamento`) actually correct?**
  _`criar_pagamento()` has 129 INFERRED edges - model-reasoned connections that need verification._
- **Are the 99 inferred relationships involving `logar_como_aluno()` (e.g. with `test_aluno_nao_alcanca_cobranca_de_outro_aluno()` and `test_checkout_recusa_cobranca_indisponivel()`) actually correct?**
  _`logar_como_aluno()` has 99 INFERRED edges - model-reasoned connections that need verification._
- **Are the 85 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 85 INFERRED edges - model-reasoned connections that need verification._