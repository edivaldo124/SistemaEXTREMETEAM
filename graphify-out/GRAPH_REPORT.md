# Graph Report - SistemaEXTREMETEAM  (2026-09-11)

## Corpus Check
- 93 files · ~144,474 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1179 nodes · 3178 edges · 67 communities (60 shown, 7 thin omitted)
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 683 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e775d46f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- TurmaDAO
- Aluno Profile Page
- financeiroDAO.py
- criar_aluno
- test_limites_pagamento.py
- servidor.py
- PagamentoDAO
- Relatório de segurança — Sistema Extreme Team
- SistemaEXTREMETEAM Project
- test_mercado_pago_servico.py
- test_mudanca_plano.py
- test_datas_turma.py
- test_migracao_checkout.py
- checkout.js
- CLAUDE.md
- planos.py
- pix_bp.py
- AlunoDAO
- test_financeiro_dao.py
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
- turma_bp.py
- convites.py
- Professor
- pagamento_polling.test.cjs
- .contratar_plano
- criar_pagamento
- test_pix_rotas.py
- test_checkout_rotas.py
- d9e2f6a14c80_contatos_academia_perfis_professores.py
- Academia
- botao_ocupado.test.cjs
- cobrar_mensalidade
- checkout_abertura.test.cjs
- filtros_financeiro.js
- detalhe_turma
- limites_pagamento.py
- test_professor_perfil.py
- test_migracao_cadastro_administrativo.py
- armazenamento.py
- test_keep_alive.py
- keep_alive.py
- cadastrar_aluno
- ._promover_vencidos
- RuntimeError
- parametrize

## God Nodes (most connected - your core abstractions)
1. `PagamentoDAO` - 154 edges
2. `criar_pagamento()` - 131 edges
3. `logar_como_aluno()` - 101 edges
4. `criar_aluno()` - 88 edges
5. `AlunoDAO` - 75 edges
6. `logar_como_admin()` - 72 edges
7. `Aluno` - 47 edges
8. `_matricular()` - 34 edges
9. `ProfessorDAO` - 29 edges
10. `Professor` - 29 edges

## Surprising Connections (you probably didn't know these)
- `Histórico de Mensalidades Section` --shares_data_with--> `Pagamento`  [INFERRED]
  templates/pgUsuario.html → modelos/pagamento.py
- `Cadastrar Plano Form` --shares_data_with--> `Plano`  [INFERRED]
  templates/pgAdm.html → modelos/plano.py
- `Planos Disponíveis Section` --shares_data_with--> `Plano`  [INFERRED]
  templates/pgUsuario.html → modelos/plano.py
- `Turma Detail Page` --shares_data_with--> `Turma`  [INFERRED]
  templates/turma.html → modelos/turma.py
- `Aluno Detail/Admin Page` --shares_data_with--> `Matricula`  [INFERRED]
  templates/dt_aluno.html → modelos/matricula.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Shared Confirmation Modal Pattern** — templates_components_confirm_modal_dialog, templates_pgadm_page, templates_pgprofessor_page, templates_pgusuario_page, templates_turmas_page [EXTRACTED 1.00]
- **Mensalidade (Billing) Management Flow** — templates_dt_aluno_pagamento_form, templates_pgusuario_mensalidades_section, modelos_pagamento_pagamento, modelos_plano_plano [INFERRED 0.85]
- **Turma and Attendance Management Flow** — templates_turmas_turma_form, templates_turma_presenca_form, templates_pgprofessor_page, modelos_turma_turma [INFERRED 0.85]

## Communities (67 total, 7 thin omitted)

### Community 0 - "TurmaDAO"
Cohesion: 0.16
Nodes (14): cadastrar_turma(), remover_turma(), TurmaDAO, Turma, Cadastrar Turma Form, Hipótese: a foto continua acessível por URL depois de tirar a publicação., Hipótese: os contatos vazam na home antes de a publicação ser marcada., Sonda: a data vem da query string e é convertida sem tratamento. (+6 more)

### Community 1 - "Aluno Profile Page"
Cohesion: 0.05
Nodes (44): Extreme Team Logo Image, Academia do Bitelo Logo, abrirmodal(), fechar(), icone_senha, input_senha, modal, mostrarSenha() (+36 more)

### Community 2 - "financeiroDAO.py"
Cohesion: 0.07
Nodes (26): PlanoDAO, Decimal, _para_decimal(), Plano, Pedido de troca de plano agendado para a próxima renovação. Nunca altera o…, SolicitacaoMudancaPlano, app(), client() (+18 more)

### Community 3 - "criar_aluno"
Cohesion: 0.13
Nodes (35): criar_aluno(), test_aluno_existente_continua_entrando_normalmente(), test_area_do_aluno_renderiza_telas_independentes_do_menu(), test_escolher_plano_cria_mensalidade_e_redireciona_para_pix(), test_perfil_so_autoriza_abertura_automatica_da_propria_mensalidade(), test_plano_atual_continua_disponivel_para_gerar_cobranca(), test_plano_invalido_nao_cria_mensalidade(), test_reenvio_da_contratacao_reutiliza_mensalidade() (+27 more)

### Community 4 - "test_limites_pagamento.py"
Cohesion: 0.15
Nodes (16): consultar_mp(), fixture, parametrize, Limites de pagamento por conta, com o provedor inteiramente simulado., _sessao_admin(), _sessao_aluno(), test_admin_limite_por_usuario_persiste_entre_sessoes(), test_alunos_no_mesmo_ip_tem_limites_separados() (+8 more)

### Community 5 - "servidor.py"
Cohesion: 0.08
Nodes (28): after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, Flask App Service (compose), Postgres DB Service (compose), postgres_data Volume, context_processor, errorhandler (+20 more)

### Community 6 - "PagamentoDAO"
Cohesion: 0.10
Nodes (19): cadastrar_pagamento(), PagamentoDAO, Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda. O…, Primeiro dia não coberto por outra mensalidade do mesmo aluno., Define o período coberto por uma mensalidade que ainda não tem um (lançamento…, Abre o período de acesso no momento em que o pagamento é confirmado. Se a…, Reescreve os campos denormalizados do aluno a partir das mensalidades.…, Solta a preferência atual para que a próxima tentativa crie uma nova. Nunca… (+11 more)

### Community 7 - "Relatório de segurança — Sistema Extreme Team"
Cohesion: 0.08
Nodes (24): A verificar em execução, Atualização após as correções, F10 — Redirecionamento aberto via `Referer`, F11 — `/logout` aceita GET, F12 — Enumeração de usuários por tempo de resposta, F13 — Senha mínima de 6 caracteres, sem outros critérios, F14 — Webhook sem verificação de recência do timestamp, F15 — Curinga de `LIKE` no filtro do financeiro (+16 more)

### Community 9 - "test_mercado_pago_servico.py"
Cohesion: 0.12
Nodes (26): Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, validar_assinatura_webhook(), Hipótese: uma notificação capturada ontem pode ser reenviada hoje., test_webhook_recusa_assinatura_antiga(), base_url(), _criar_preferencia(), _FakePreferenceResource, mp_fake() (+18 more)

### Community 10 - "test_mudanca_plano.py"
Cohesion: 0.22
Nodes (22): Persistência dos pedidos de troca de plano agendados para a próxima renovação., SolicitacaoPlanoDAO, _agendar(), _pagar(), Mudança para um plano mais barato agendada para a próxima renovação. Regra…, O admin pode estornar/cancelar a mensalidade que sustentava a vigência depois…, test_admin_cancela_a_solicitacao(), test_aluno_cancela_a_solicitacao_antes_da_efetivacao() (+14 more)

### Community 11 - "test_datas_turma.py"
Cohesion: 0.16
Nodes (12): desmatricular_aluno(), matricular_aluno(), MatriculaDAO, Matricula, Presenca, Presença Form, parametrize, test_consulta_com_data_invalida_exibe_hoje_e_aviso() (+4 more)

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
Cohesion: 0.11
Nodes (29): _acesso_permitido(), criar_pix_mensalidade(), _forma_pagamento_confirmada(), _pagamento_mp_mais_relevante(), _pagamento_ou_none(), _pix_expirado(), _processar_status_mp(), limitar_consulta_pagamento (+21 more)

### Community 18 - "AlunoDAO"
Cohesion: 0.08
Nodes (62): _convidar_cadastro_existente(), Cadastro administrativo que alguém tentou recriar pelo formulário público. Em…, AlunoDAO, Matrícula feita no balcão: sem login, sem senha e sem convite de acesso. Nasce…, Aluno, Se existe uma conta de acesso, e não se o aluno está em dia ou matriculado.…, Convite de acesso já enviado e ainda não usado (a validade é checada na rota)., Chave do estado da CONTA - nunca da situação financeira nem da matrícula. (+54 more)

### Community 19 - "test_financeiro_dao.py"
Cohesion: 0.12
Nodes (16): mensalidade_destaque(), Escolhe a mensalidade mais relevante para o card 'Minha mensalidade': a mais…, True se a cobrança Pix já gerada para este pagamento ainda pode ser…, Totais do painel financeiro - sempre calculados no backend a partir do banco,…, provider_payment_id sozinho não basta: pagamentos do Checkout Pro…, test_listar_filtrado_por_status_e_busca_de_aluno(), test_marcar_pago_via_webhook_sincroniza_mensalidade_do_aluno(), test_marcar_reembolsado_via_webhook_sincroniza_mensalidade_do_aluno() (+8 more)

### Community 20 - "checkout_bp.py"
Cohesion: 0.12
Nodes (26): abrir_checkout(), _acesso_permitido(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), limitar_consulta_pagamento, limitar_criacao_pagamento, route (+18 more)

### Community 21 - "pix.js"
Cohesion: 0.33
Nodes (14): abrirPix(), alvoDoRotulo(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), liberarBotao(), limparConteudoAnterior() (+6 more)

### Community 22 - "usuario_bp.py"
Cohesion: 0.12
Nodes (31): _acesso_permitido_pagamento(), alterar_senha_perfil(), _aluno_da_sessao(), ativar_acesso(), atualizar_dados_perfil(), cancelar_mudanca_plano(), comprovante_mensalidade(), confirmar_email() (+23 more)

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
Nodes (48): Só abre o checkout HTTPS do Mercado Pago Brasil, inclusive no sandbox., url_checkout_permitida(), _assinar(), _pagamento_mp(), _preparar_para_conciliacao(), parametrize, Auditoria de segurança: sondas escritas para TENTAR quebrar as regras. Nenhum…, Hipótese: a sessão de professor é aceita nas rotas financeiras do aluno. (+40 more)

### Community 34 - "mercado_pago.py"
Cohesion: 0.09
Nodes (39): _base_url_opcional(), base_url_publica(), buscar_pagamento(), buscar_pagamentos_por_referencia(), cancelar_pagamento(), criar_pagamento_pix(), criar_preferencia_checkout(), _erro_menciona() (+31 more)

### Community 35 - "adm_bp.py"
Cohesion: 0.14
Nodes (27): _aluno_do_cpf_ou_painel(), aprovar_aluno(), aprovar_comprovante_manual(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_plano(), cancelar_mudanca_plano_admin(), _data_do_form() (+19 more)

### Community 36 - "ProfessorDAO"
Cohesion: 0.20
Nodes (13): cadastrar_professor(), foto_professor(), gerenciar_turmas(), painel_professor(), route, remover_professor(), ProfessorDAO, logar_como_professor() (+5 more)

### Community 37 - "turma_bp.py"
Cohesion: 0.38
Nodes (8): configuracoes(), route, editar_professor(), admin_requerido(), Normalização de contatos profissionais antes de montar links públicos., validar_email(), validar_instagram(), validar_whatsapp()

### Community 38 - "convites.py"
Cohesion: 0.14
Nodes (16): _colunas(), downgrade(), upgrade(), RuntimeError, aluno_do_token(), ConviteIndisponivel, descartar(), enviar() (+8 more)

### Community 41 - "Professor"
Cohesion: 0.13
Nodes (10): Professor, link_email(), _imagem_jpeg_valida(), test_admin_acessa_foto_de_qualquer_aluno(), test_aluno_nao_acessa_foto_de_outro_aluno(), test_aluno_ve_o_proprio_perfil(), test_professor_nao_ve_foto_de_aluno_fora_da_sua_turma(), test_substituir_e_remover_foto() (+2 more)

### Community 42 - "pagamento_polling.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 43 - ".contratar_plano"
Cohesion: 0.10
Nodes (12): pagina_perfil(), Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, True se já existe um Pix ou um checkout válido emitido para esta cobrança.…, Aplica um pedido agendado cujo período de origem já terminou sem renovação.…, Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, Com uma troca já agendada, só dois planos fazem sentido num pedido de…, A cobrança do período seguinte tem de nascer no plano que o aluno agendou.…, True se a preferência do Checkout Pro já criada pode ser reaproveitada. Só… (+4 more)

### Community 44 - "criar_pagamento"
Cohesion: 0.10
Nodes (45): criar_pagamento(), logar_como_aluno(), Hipótese: forjar ?status=approved na volta do MP quita a mensalidade., test_retorno_ignora_status_aprovado_da_query_string(), _mockar_preferencia(), Um boleto pendente do Checkout Pro grava provider_payment_id, mas não é Pix:…, test_abertura_json_navega_sem_redirecionar_post_externo(), test_admin_tambem_pode_abrir_checkout() (+37 more)

### Community 45 - "test_pix_rotas.py"
Cohesion: 0.20
Nodes (20): _assinar(), _resposta_consulta(), _resposta_criacao(), test_admin_tambem_pode_gerar_pix(), test_aluno_gera_pix_da_propria_mensalidade(), test_aluno_nao_acessa_mensalidade_de_outro_aluno(), test_falha_de_indisponibilidade_do_mp_retorna_503(), test_impede_cobranca_duplicada_em_chamadas_consecutivas() (+12 more)

### Community 46 - "test_checkout_rotas.py"
Cohesion: 0.21
Nodes (26): _assinar(), _pagamento_mp(), _preparar_retorno(), parametrize, Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala…, Pix aberto e checkout concluído ao mesmo tempo: a consulta pelo…, _resposta_preferencia(), test_configuracao_ausente_falha_de_forma_explicita() (+18 more)

### Community 47 - "d9e2f6a14c80_contatos_academia_perfis_professores.py"
Cohesion: 0.83
Nodes (3): _campos_professor(), downgrade(), upgrade()

### Community 49 - "Academia"
Cohesion: 0.20
Nodes (10): Academia, parametrize, test_admin_salva_atualiza_e_limpa_contatos(), test_configuracoes_exigem_admin(), test_contatos_invalidos(), test_csrf_configuracoes(), test_erro_preserva_formulario_e_dados_salvos(), test_link_email_preserva_caracteres_do_endereco() (+2 more)

### Community 50 - "botao_ocupado.test.cjs"
Cohesion: 0.18
Nodes (7): assert, criarElemento(), fs, montar(), path, test, vm

### Community 51 - "cobrar_mensalidade"
Cohesion: 0.23
Nodes (12): cobrar_inadimplentes(), cobrar_mensalidade(), enviar_aviso(), _esta_inadimplente(), _paragrafos_cobranca(), Situação de todos os alunos ativos com UMA consulta de mensalidades., Quem realmente deve receber cobrança: nem quem está com o plano ativo, nem quem…, Texto da cobrança montado a partir da situação real, não de campos guardados: o… (+4 more)

### Community 52 - "checkout_abertura.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 55 - "detalhe_turma"
Cohesion: 0.29
Nodes (6): _acesso_permitido(), detalhe_turma(), registrar_presenca(), _turma_ou_404(), PresencaDAO, professor_ou_admin_requerido()

### Community 56 - "limites_pagamento.py"
Cohesion: 0.50
Nodes (3): chave_pagamento(), Orçamentos compartilhados das chamadas interativas ao provedor de pagamento., A mesma conta mantém seu limite entre sessões, rotas e mensalidades. Alunos que…

### Community 57 - "test_professor_perfil.py"
Cohesion: 0.25
Nodes (9): _foto(), pasta_fotos(), professor(), fixture, test_edicao_professor_tem_protecao_csrf(), test_falha_ao_salvar_preserva_foto_anterior(), test_publicar_e_retirar_foto_do_site(), test_substituir_remover_e_recusar_foto_falsa() (+1 more)

### Community 58 - "test_migracao_cadastro_administrativo.py"
Cohesion: 0.40
Nodes (3): banco_antigo(), fixture, Verifica a migração em um banco isolado com o schema anterior e dados.

### Community 59 - "armazenamento.py"
Cohesion: 0.19
Nodes (16): enviar_comprovante_manual_aluno(), ArquivoInvalido, caminho_arquivo(), _detectar_tipo_imagem_real(), _pasta(), Exception, _raiz_uploads(), Armazenamento de arquivos enviados por usuários (fotos de perfil, comprovantes… (+8 more)

### Community 60 - "test_keep_alive.py"
Cohesion: 0.18
Nodes (6): ambiente_limpo(), fixture, parametrize, Garante que o keep-alive fica desligado por padrão e só pinga a própria origem., test_intervalo_fica_dentro_da_faixa(), test_nao_liga_com_valor_negativo()

### Community 61 - "keep_alive.py"
Cohesion: 0.21
Nodes (14): iniciar(), _intervalo(), _laco(), _ligado(), parar(), _pingar(), Mantém a aplicação acordada em hospedagens que hibernam por inatividade. O…, Encerra o laço. Usado pelos testes; em produção a thread é daemon. (+6 more)

### Community 62 - "cadastrar_aluno"
Cohesion: 0.23
Nodes (10): cadastrar_aluno(), Matrícula feita pela administração, sem conta de acesso. Pede só o que…, pagina_login(), _plano_do_formulario(), recuperar_senha(), limit, formatar_cpf(), formatar_telefone() (+2 more)

## Knowledge Gaps
- **61 isolated node(s):** `icone_senha`, `input_senha`, `modal`, `avisoSemResultados`, `campoBusca` (+56 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PagamentoDAO` connect `PagamentoDAO` to `test_auditoria_seguranca.py`, `financeiroDAO.py`, `criar_aluno`, `test_mudanca_plano.py`, `.contratar_plano`, `criar_pagamento`, `test_datas_turma.py`, `test_checkout_rotas.py`, `test_pix_rotas.py`, `pix_bp.py`, `AlunoDAO`, `test_financeiro_dao.py`, `checkout_bp.py`, `._promover_vencidos`?**
  _High betweenness centrality (0.164) - this node is a cross-community bridge._
- **Why does `Aluno` connect `AlunoDAO` to `financeiroDAO.py`, `adm_bp.py`, `criar_aluno`, `PagamentoDAO`, `convites.py`, `.contratar_plano`, `usuario_bp.py`, `cadastrar_aluno`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Why does `AlunoDAO` connect `AlunoDAO` to `financeiroDAO.py`, `adm_bp.py`, `criar_aluno`, `turma_bp.py`, `PagamentoDAO`, `Professor`, `test_datas_turma.py`, `cobrar_mensalidade`, `usuario_bp.py`, `detalhe_turma`, `cadastrar_aluno`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Are the 99 inferred relationships involving `PagamentoDAO` (e.g. with `abrir_checkout()` and `continuar_checkout()`) actually correct?**
  _`PagamentoDAO` has 99 INFERRED edges - model-reasoned connections that need verification._
- **Are the 129 inferred relationships involving `criar_pagamento()` (e.g. with `PagamentoDAO` and `Pagamento`) actually correct?**
  _`criar_pagamento()` has 129 INFERRED edges - model-reasoned connections that need verification._
- **Are the 99 inferred relationships involving `logar_como_aluno()` (e.g. with `test_aluno_nao_alcanca_cobranca_de_outro_aluno()` and `test_checkout_recusa_cobranca_indisponivel()`) actually correct?**
  _`logar_como_aluno()` has 99 INFERRED edges - model-reasoned connections that need verification._
- **Are the 86 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 86 INFERRED edges - model-reasoned connections that need verification._