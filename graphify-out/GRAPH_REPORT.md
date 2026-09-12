# Graph Report - SistemaEXTREMETEAM  (2026-09-12)

## Corpus Check
- 104 files · ~160,568 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1419 nodes · 3786 edges · 89 communities (76 shown, 13 thin omitted)
- Extraction: 78% EXTRACTED · 22% INFERRED · 0% AMBIGUOUS · INFERRED: 823 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ff241ce3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- PagamentoDAO
- Aluno Profile Page
- config.py
- criar_aluno
- criar_pagamento
- servidor.py
- PagamentoEvento
- Relatório de segurança — Sistema Extreme Team
- SistemaEXTREMETEAM Project
- test_mercado_pago_servico.py
- test_mudanca_plano.py
- test_professor_perfil.py
- test_migracao_checkout.py
- checkout.js
- CLAUDE.md
- planos.py
- pix_bp.py
- AlunoDAO
- Pagina
- checkout_bp.py
- pix.js
- usuario_bp.py
- env.py
- pagamento.js
- c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py
- _FakePaymentResource
- 896e70afc9c5_adiciona_foto_e_graduacao_do_aluno_.py
- test_auditoria_seguranca.py
- mercado_pago.py
- adm_bp.py
- Professor
- test_regressao_auditoria.py
- enviar_email
- test_perfil_e_foto.py
- pagamento_polling.test.cjs
- .contratar_plano
- logar_como_aluno
- test_pix_rotas.py
- .buscar_por_id
- d9e2f6a14c80_contatos_academia_perfis_professores.py
- Academia
- botao_ocupado.test.cjs
- test_seguranca.py
- checkout_abertura.test.cjs
- filtros_financeiro.js
- gunicorn.conf.py
- ambiente_mercado_pago
- fila_email.py
- test_migracao_cadastro_administrativo.py
- salvar_foto_perfil
- test_keep_alive.py
- URLPublicaInvalida
- pagina_cadastro
- validar_assinatura_webhook
- MercadoPagoIndisponivel
- test_fila_email_concorrencia_postgres.py
- EmailPendente
- turma_bp.py
- Flask App Service (compose)
- _FakePreferenceResource
- .listar_paginado
- credenciais.py
- autorizacao.py
- Revisão independente — Codex — 2026-09-12
- _laco
- _png_bomba
- _tem_limite
- e4b7c2a91d35_cadastro_administrativo_e_convite_de_acesso.py
- a1f0c3e75b92_schema_inicial.py
- buscar_pagamento
- _chave_da_conta
- test_um_envio_ainda_pendente_continua_sendo_recusado
- test_linha_com_defeito_nao_trava_a_fila_atras_dela
- test_limite_atingido_nao_mostra_login_a_quem_ja_entrou
- test_decodificacao_de_imagem_e_serializada_no_processo
- test_login_de_aluno_nao_paga_o_hash_do_admin
- test_sessao_sem_carimbo_de_credencial_e_recusada

## God Nodes (most connected - your core abstractions)
1. `PagamentoDAO` - 194 edges
2. `criar_pagamento()` - 141 edges
3. `criar_aluno()` - 120 edges
4. `logar_como_aluno()` - 107 edges
5. `AlunoDAO` - 84 edges
6. `logar_como_admin()` - 84 edges
7. `Aluno` - 49 edges
8. `Professor` - 34 edges
9. `_matricular()` - 34 edges
10. `ProfessorDAO` - 33 edges

## Surprising Connections (you probably didn't know these)
- `Histórico de Mensalidades Section` --shares_data_with--> `Pagamento`  [INFERRED]
  templates/pgUsuario.html → modelos/pagamento.py
- `Cadastrar Plano Form` --shares_data_with--> `Plano`  [INFERRED]
  templates/pgAdm.html → modelos/plano.py
- `Planos Disponíveis Section` --shares_data_with--> `Plano`  [INFERRED]
  templates/pgUsuario.html → modelos/plano.py
- `Presença Form` --shares_data_with--> `Presenca`  [INFERRED]
  templates/turma.html → modelos/presenca.py
- `Aluno Detail/Admin Page` --shares_data_with--> `Matricula`  [INFERRED]
  templates/dt_aluno.html → modelos/matricula.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Shared Confirmation Modal Pattern** — templates_components_confirm_modal_dialog, templates_pgadm_page, templates_pgprofessor_page, templates_pgusuario_page, templates_turmas_page [EXTRACTED 1.00]
- **Mensalidade (Billing) Management Flow** — templates_dt_aluno_pagamento_form, templates_pgusuario_mensalidades_section, modelos_pagamento_pagamento, modelos_plano_plano [INFERRED 0.85]
- **Turma and Attendance Management Flow** — templates_turmas_turma_form, templates_turma_presenca_form, templates_pgprofessor_page, modelos_turma_turma [INFERRED 0.85]

## Communities (89 total, 13 thin omitted)

### Community 0 - "PagamentoDAO"
Cohesion: 0.09
Nodes (26): PagamentoDAO, Carrega aluno e plano junto das mensalidades. O template do painel lê…, Lista completa (sem paginar). Mantida para relatórios e testes., Uma página de mensalidades, recortada pelo banco (LIMIT/OFFSET). O painel…, Totais do painel financeiro - sempre calculados no backend a partir do banco,…, True se já existe um Pix ou um checkout válido emitido para esta cobrança.…, True se a cobrança Pix já gerada para este pagamento ainda pode ser…, True se a preferência do Checkout Pro já criada pode ser reaproveitada. Só… (+18 more)

### Community 1 - "Aluno Profile Page"
Cohesion: 0.06
Nodes (40): Extreme Team Logo Image, Academia do Bitelo Logo, abrirmodal(), fechar(), icone_senha, input_senha, modal, mostrarSenha() (+32 more)

### Community 2 - "config.py"
Cohesion: 0.08
Nodes (29): Decimal, Matricula, Pagamento, _para_decimal(), Status a exibir, com o vencimento já aplicado. Uma cobrança `pendente` cujo…, Plano, Pedido de troca de plano agendado para a próxima renovação. Nunca altera o…, SolicitacaoMudancaPlano (+21 more)

### Community 3 - "criar_aluno"
Cohesion: 0.14
Nodes (34): criar_aluno(), test_aluno_existente_continua_entrando_normalmente(), test_area_do_aluno_renderiza_telas_independentes_do_menu(), test_escolher_plano_cria_mensalidade_e_redireciona_para_pix(), test_plano_atual_continua_disponivel_para_gerar_cobranca(), test_plano_invalido_nao_cria_mensalidade(), test_reenvio_da_contratacao_reutiliza_mensalidade(), test_valor_enviado_pelo_navegador_e_ignorado() (+26 more)

### Community 4 - "criar_pagamento"
Cohesion: 0.10
Nodes (30): criar_pagamento(), test_admin_aprova_comprovante_manual(), test_admin_rejeita_comprovante_manual_volta_para_pendente(), test_aluno_nao_acessa_arquivo_de_comprovante_de_outro(), test_aluno_nao_envia_comprovante_de_outro_aluno(), test_arquivo_invalido_e_recusado(), test_envio_de_comprovante_manual_fica_em_analise(), test_envio_sozinho_nunca_marca_como_pago() (+22 more)

### Community 5 - "servidor.py"
Cohesion: 0.11
Nodes (19): after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, context_processor, errorhandler, formatar_moeda(), Nome legível da forma de pagamento. Antes as telas usavam `|replace('_','…, Formata um valor em reais no padrão brasileiro: R$ 1.080,00. Usado como filtro… (+11 more)

### Community 6 - "PagamentoEvento"
Cohesion: 0.12
Nodes (10): Primeiro dia não coberto por outra mensalidade do mesmo aluno., Define o período coberto por uma mensalidade que ainda não tem um (lançamento…, Abre o período de acesso no momento em que o pagamento é confirmado. Se a…, Reescreve os campos denormalizados do aluno a partir das mensalidades.…, forma_pagamento vem do que o Mercado Pago confirmou na consulta à API ('pix',…, Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.…, PagamentoEvento, Histórico de auditoria de uma mensalidade (nunca grava credenciais ou dados… (+2 more)

### Community 7 - "Relatório de segurança — Sistema Extreme Team"
Cohesion: 0.08
Nodes (24): A verificar em execução, Atualização após as correções, F10 — Redirecionamento aberto via `Referer`, F11 — `/logout` aceita GET, F12 — Enumeração de usuários por tempo de resposta, F13 — Senha mínima de 6 caracteres, sem outros critérios, F14 — Webhook sem verificação de recência do timestamp, F15 — Curinga de `LIKE` no filtro do financeiro (+16 more)

### Community 9 - "test_mercado_pago_servico.py"
Cohesion: 0.18
Nodes (20): base_url(), _criar_preferencia(), mp_fake(), fixture, parametrize, _resposta_preferencia(), test_base_url_publica_recusa_valor_ausente_ou_invalido(), test_criar_pagamento_pix_recusa_de_negocio_nao_lanca() (+12 more)

### Community 10 - "test_mudanca_plano.py"
Cohesion: 0.20
Nodes (22): Persistência dos pedidos de troca de plano agendados para a próxima renovação., SolicitacaoPlanoDAO, _agendar(), _pagar(), Mudança para um plano mais barato agendada para a próxima renovação. Regra…, O admin pode estornar/cancelar a mensalidade que sustentava a vigência depois…, test_admin_cancela_a_solicitacao(), test_aluno_cancela_a_solicitacao_antes_da_efetivacao() (+14 more)

### Community 11 - "test_professor_perfil.py"
Cohesion: 0.17
Nodes (12): _foto(), pasta_fotos(), fixture, parametrize, test_admin_salva_perfil_sem_alterar_acesso(), test_apenas_admin_edita_perfil(), test_contato_invalido_nao_salva_nenhuma_alteracao(), test_edicao_professor_tem_protecao_csrf() (+4 more)

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
Nodes (26): _acesso_permitido(), criar_pix_mensalidade(), _forma_pagamento_confirmada(), _pagamento_mp_mais_relevante(), _pagamento_ou_none(), _pix_expirado(), _processar_status_mp(), limitar_consulta_pagamento (+18 more)

### Community 18 - "AlunoDAO"
Cohesion: 0.07
Nodes (63): AlunoDAO, Matrícula feita no balcão: sem login, sem senha e sem convite de acesso. Nasce…, Aluno, Se existe uma conta de acesso, e não se o aluno está em dia ou matriculado.…, Convite de acesso já enviado e ainda não usado (a validade é checada na rota)., Chave do estado da CONTA - nunca da situação financeira nem da matrícula., logar_como_admin(), capturar_emails() (+55 more)

### Community 19 - "Pagina"
Cohesion: 0.14
Nodes (5): Pagina, Uma fatia de resultados já recortada pelo banco, com o que a navegação precisa., Uma página existe mesmo quando está vazia. Sem isto, `__len__` fazia `{% if…, `__len__` fazia `{% if pagina %}` ser falso numa página sem itens, escondendo…, test_pagina_vazia_ainda_mostra_a_navegacao()

### Community 20 - "checkout_bp.py"
Cohesion: 0.13
Nodes (25): abrir_checkout(), _acesso_permitido(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), limitar_consulta_pagamento, limitar_criacao_pagamento, route (+17 more)

### Community 21 - "pix.js"
Cohesion: 0.33
Nodes (14): abrirPix(), alvoDoRotulo(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), liberarBotao(), limparConteudoAnterior() (+6 more)

### Community 22 - "usuario_bp.py"
Cohesion: 0.13
Nodes (36): _acesso_permitido_pagamento(), alterar_senha_perfil(), _aluno_da_sessao(), _aluno_por_token(), atualizar_dados_perfil(), cancelar_mudanca_plano(), comprovante_mensalidade(), confirmar_email() (+28 more)

### Community 23 - "env.py"
Cohesion: 0.39
Nodes (7): get_engine(), get_engine_url(), get_metadata(), Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online()

### Community 24 - "pagamento.js"
Cohesion: 0.47
Nodes (9): alvoDoRotulo(), consultarStatus(), gerarOuAtualizarPix(), iniciarPolling(), liberarBotao(), marcarOcupado(), mostrarEstado(), pararPolling() (+1 more)

### Community 25 - "c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py"
Cohesion: 0.60
Nodes (5): _backfill_vigencia(), _colunas(), _criar_tabela_solicitacoes(), downgrade(), upgrade()

### Community 29 - "896e70afc9c5_adiciona_foto_e_graduacao_do_aluno_.py"
Cohesion: 0.60
Nodes (3): _e_decimal(), _faltantes(), upgrade()

### Community 33 - "test_auditoria_seguranca.py"
Cohesion: 0.06
Nodes (50): Só abre o checkout HTTPS do Mercado Pago Brasil, inclusive no sandbox., url_checkout_permitida(), _assinar(), _pagamento_mp(), _preparar_para_conciliacao(), parametrize, Auditoria de segurança: sondas escritas para TENTAR quebrar as regras. Nenhum…, Hipótese: a sessão de professor é aceita nas rotas financeiras do aluno. (+42 more)

### Community 34 - "mercado_pago.py"
Cohesion: 0.18
Nodes (21): _base_url_opcional(), base_url_publica(), cancelar_pagamento(), criar_pagamento_pix(), criar_preferencia_checkout(), _erro_menciona(), _erro_menciona_expiracao(), _extrair_dados_pix() (+13 more)

### Community 35 - "adm_bp.py"
Cohesion: 0.07
Nodes (50): _aluno_do_cpf_ou_painel(), aprovar_aluno(), aprovar_comprovante_manual(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_aluno(), cadastrar_pagamento(), cadastrar_plano() (+42 more)

### Community 36 - "Professor"
Cohesion: 0.13
Nodes (15): cadastrar_professor(), gerenciar_turmas(), remover_professor(), ProfessorDAO, Professor, test_publicacao_professor_nao_expoe_contatos_sem_permissao(), logar_como_professor(), fixture (+7 more)

### Community 37 - "test_regressao_auditoria.py"
Cohesion: 0.06
Nodes (30): _contar_selects_em_alunos(), _credencial(), Regressões da auditoria de segurança, desempenho e confiabilidade. Cada caso…, Uma linha `desistiu` nunca foi entregue: recusar o reenvio fazia a tela dizer…, Persistência não é retomada: alguém precisa acordar a fila quando o adiamento…, A conta de maior privilégio não pode ser a única isenta da revogação., A chave de idempotência inclui o dia. Só o conteúdo suprimiria para sempre um…, O laço parava só quando nada acontecia, então uma indisponibilidade gastava as… (+22 more)

### Community 38 - "enviar_email"
Cohesion: 0.15
Nodes (17): aluno_do_token(), ConviteIndisponivel, descartar(), enviar(), gerar_token(), _hash(), RuntimeError, Convite de acesso: como um cadastro criado pela administração vira uma conta.… (+9 more)

### Community 41 - "test_perfil_e_foto.py"
Cohesion: 0.14
Nodes (16): cadastrar_turma(), remover_turma(), TurmaDAO, Turma, Sonda: a data vem da query string e é convertida sem tratamento., test_data_invalida_na_turma_nao_derruba_a_rota(), fixture, turma() (+8 more)

### Community 42 - "pagamento_polling.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 43 - ".contratar_plano"
Cohesion: 0.10
Nodes (11): O que aconteceu numa tentativa de contratar/renovar/trocar de plano., Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda. O…, Aplica um pedido agendado cujo período de origem já terminou sem renovação.…, Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, Com uma troca já agendada, só dois planos fazem sentido num pedido de…, A cobrança do período seguinte tem de nascer no plano que o aluno agendou.…, `pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -… (+3 more)

### Community 44 - "logar_como_aluno"
Cohesion: 0.12
Nodes (37): logar_como_aluno(), _mockar_preferencia(), parametrize, Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala…, Um boleto pendente do Checkout Pro grava provider_payment_id, mas não é Pix:…, _resposta_preferencia(), test_abertura_json_navega_sem_redirecionar_post_externo(), test_admin_tambem_pode_abrir_checkout() (+29 more)

### Community 45 - "test_pix_rotas.py"
Cohesion: 0.20
Nodes (20): _assinar(), _resposta_consulta(), _resposta_criacao(), test_admin_tambem_pode_gerar_pix(), test_aluno_gera_pix_da_propria_mensalidade(), test_aluno_nao_acessa_mensalidade_de_outro_aluno(), test_falha_de_indisponibilidade_do_mp_retorna_503(), test_impede_cobranca_duplicada_em_chamadas_consecutivas() (+12 more)

### Community 46 - ".buscar_por_id"
Cohesion: 0.25
Nodes (19): _assinar(), _pagamento_mp(), _preparar_retorno(), Pix aberto e checkout concluído ao mesmo tempo: a consulta pelo…, test_retorno_com_aprovacao_confirmada_marca_pago(), test_retorno_com_mp_indisponivel_avisa_sem_mudar_status(), test_retorno_de_boleto_avisa_sobre_o_prazo(), test_retorno_de_sucesso_nao_marca_pago_sem_confirmacao() (+11 more)

### Community 47 - "d9e2f6a14c80_contatos_academia_perfis_professores.py"
Cohesion: 0.83
Nodes (3): _campos_professor(), downgrade(), upgrade()

### Community 49 - "Academia"
Cohesion: 0.14
Nodes (18): configuracoes(), route, editar_professor(), Academia, admin_requerido(), link_email(), Normalização de contatos profissionais antes de montar links públicos., validar_email() (+10 more)

### Community 50 - "botao_ocupado.test.cjs"
Cohesion: 0.18
Nodes (7): assert, criarElemento(), fs, montar(), path, test, vm

### Community 51 - "test_seguranca.py"
Cohesion: 0.12
Nodes (12): ativar_acesso(), Transforma um cadastro feito no balcão na conta do próprio aluno. Quem chega…, erro_confirmacao_senha(), erro_validacao_senha(), Retorna uma mensagem quando a senha é curta, comum ou igual ao identificador., Retorna uma mensagem quando a confirmação não repete exatamente a senha. A…, _imagem_jpeg(), test_limite_de_login_por_ip_e_identificador() (+4 more)

### Community 52 - "checkout_abertura.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 55 - "gunicorn.conf.py"
Cohesion: 0.25
Nodes (9): post_worker_init(), Hooks carregados pelo Gunicorn; nunca executados por flask db upgrade., worker_exit(), iniciar(), _laco(), parar(), Aciona a fila periodicamente durante a vida de um worker Gunicorn. Importar…, Inicia uma vez por processo, depois de carregar a aplicação e migrar o banco. (+1 more)

### Community 56 - "ambiente_mercado_pago"
Cohesion: 0.22
Nodes (9): ambiente_mercado_pago(), ConfiguracaoInvalida, Exception, Variavel de ambiente obrigatoria ausente ou com formato invalido. Erro de…, Diz se a integracao esta apontando para producao ou para o sandbox. Prioriza a…, test_ambiente_assume_producao_para_token_sem_prefixo_de_teste(), test_ambiente_cai_no_prefixo_do_token_quando_nao_configurado(), test_ambiente_invalido_e_recusado() (+1 more)

### Community 57 - "fila_email.py"
Cohesion: 0.16
Nodes (14): espera_da_proxima_tentativa(), Fila de e-mails no banco. Aviso e cobrança coletivos saíam um a um dentro da…, contar_falhados(), contar_pendentes(), _entregar(), listar_pendentes(), processar_agora(), Processamento dos e-mails coletivos fora da requisição. O que muda em relação… (+6 more)

### Community 58 - "test_migracao_cadastro_administrativo.py"
Cohesion: 0.40
Nodes (3): banco_antigo(), fixture, Verifica a migração em um banco isolado com o schema anterior e dados.

### Community 59 - "salvar_foto_perfil"
Cohesion: 0.13
Nodes (22): ArquivoInvalido, _conferir_dimensoes(), _detectar_tipo_imagem_real(), ImagemGrandeDemais, _pasta(), Exception, _raiz_uploads(), Armazenamento de arquivos enviados por usuários (fotos de perfil, comprovantes… (+14 more)

### Community 60 - "test_keep_alive.py"
Cohesion: 0.16
Nodes (7): ambiente_limpo(), fixture, parametrize, Garante que o keep-alive fica desligado por padrão e só pinga a própria origem., test_intervalo_fica_dentro_da_faixa(), test_nao_liga_com_valor_negativo(), test_ping_so_considera_200_como_sucesso()

### Community 61 - "URLPublicaInvalida"
Cohesion: 0.21
Nodes (14): iniciar(), _intervalo(), _laco(), _ligado(), parar(), _pingar(), Mantém a aplicação acordada em hospedagens que hibernam por inatividade. Uma…, Encerra o laço. Usado pelos testes; em produção a thread é daemon. (+6 more)

### Community 62 - "pagina_cadastro"
Cohesion: 0.26
Nodes (11): _convidar_cadastro_existente(), pagina_cadastro(), Cadastro administrativo que alguém tentou recriar pelo formulário público. Em…, recuperar_senha(), formatar_cpf(), formatar_telefone(), mascarar_email(), Mostra o bastante do e-mail para o dono se reconhecer, sem revelá-lo a… (+3 more)

### Community 63 - "validar_assinatura_webhook"
Cohesion: 0.22
Nodes (9): Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, validar_assinatura_webhook(), Hipótese: uma notificação capturada ontem pode ser reenviada hoje., test_webhook_recusa_assinatura_antiga(), test_validar_assinatura_webhook_aceita_assinatura_correta(), test_validar_assinatura_webhook_rejeita_assinatura_incorreta(), test_validar_assinatura_webhook_rejeita_campos_ausentes(), test_validar_assinatura_webhook_rejeita_formato_inesperado() (+1 more)

### Community 64 - "MercadoPagoIndisponivel"
Cohesion: 0.29
Nodes (8): buscar_pagamentos_por_referencia(), MercadoPagoIndisponivel, Lista os pagamentos que o Mercado Pago associa a uma external_reference. Usada…, Falha de transporte (timeout/DNS/conexao) ao falar com a API do Mercado Pago., test_buscar_pagamentos_por_referencia_falha_de_transporte(), test_buscar_pagamentos_por_referencia_normaliza_resultados(), test_buscar_pagamentos_por_referencia_sem_resultado(), test_criar_pagamento_pix_falha_de_transporte_levanta_indisponivel()

### Community 66 - "test_fila_email_concorrencia_postgres.py"
Cohesion: 0.18
Nodes (10): _enfileirar_em_transacao_propria(), postgres_fila(), fixture, Idempotência da fila de e-mail sob concorrência real, em PostgreSQL…, A recusa de uma chave repetida não pode desfazer o lote inteiro. Um…, A trava do lote precisa valer até o fim do lote. Comitar linha a linha…, Enfileira e comita numa sessão própria, como faria outra requisição., test_chave_duplicada_nao_descarta_os_outros_destinatarios_do_lote() (+2 more)

### Community 67 - "EmailPendente"
Cohesion: 0.20
Nodes (7): EmailPendente, enfileirar(), Registra um e-mail para envio. Devolve a linha criada, ou None se já existia.…, parametrize, Agendamento sem rede, threads reais ou esperas de relógio., test_nao_inicia_em_testes(), test_retomada_de_item_persistido_e_retentativa_sem_painel()

### Community 68 - "turma_bp.py"
Cohesion: 0.20
Nodes (14): _acesso_permitido(), desmatricular_aluno(), detalhe_turma(), foto_professor(), matricular_aluno(), painel_professor(), route, registrar_presenca() (+6 more)

### Community 69 - "Flask App Service (compose)"
Cohesion: 0.22
Nodes (9): Flask App Service (compose), Postgres DB Service (compose), postgres_data Volume, Flask, Flask-SQLAlchemy, Gunicorn, psycopg2-binary, python-dotenv (+1 more)

### Community 71 - ".listar_paginado"
Cohesion: 0.17
Nodes (11): _paginar(), Aplica LIMIT/OFFSET e conta o total numa consulta separada e barata. A contagem…, _parece_busca_por_cpf(), O termo é um CPF, ou um pedaço dele, e não um nome que por acaso tem número?, Uma página de alunos já cadastrados, recortada e filtrada pelo banco. O painel…, Qualquer dígito no termo virava `CPF LIKE '%3%'` e devolvia a academia inteira., O CPF é guardado formatado; digitar só os números precisa encontrar mesmo assim., test_busca_do_admin_encontra_o_aluno_pelo_cpf_so_com_digitos() (+3 more)

### Community 72 - "credenciais.py"
Cohesion: 0.20
Nodes (11): admin_configurado(), comparar_em_tempo_constante(), credencial_admin_confere(), gerar_hash_admin(), _main(), Credencial do administrador, com transição de texto puro para hash. O login do…, Gera o valor de ADMIN_PASSWORD_HASH. Usado pelo utilitário de linha de comando., `python -m servicos.credenciais` - gera o valor de ADMIN_PASSWORD_HASH. A senha… (+3 more)

### Community 73 - "autorizacao.py"
Cohesion: 0.14
Nodes (19): Presenca, aluno_requerido(), _credencial_confere(), impressao_credencial(), Autorização das rotas protegidas. A sessão diz quem *afirmou* ser quem; quem…, Rotas da área do aluno: injeta o aluno já revalidado como primeiro argumento., Resumo curto e não reversível do hash da senha, guardado na sessão. Nunca é a…, Grava na sessão atual a credencial em vigor (login ou troca de senha bem-… (+11 more)

### Community 74 - "Revisão independente — Codex — 2026-09-12"
Cohesion: 0.18
Nodes (10): 1. Retomada automática da fila de e-mails, 2. Orientação perigosa de migration, 3. Limite da garantia de envio único, Canal de coordenação solicitado pelo usuário, Implementação complementar entregue pelo Codex, Limites desta revisão, Pendências para integração pelo Claude, Resposta do Claude — 2026-09-12 (+2 more)

### Community 75 - "_laco"
Cohesion: 0.29
Nodes (7): disparar(), _laco(), _liberar_e_retomar_se_preciso(), Drena a fila enquanto houver entrega acontecendo. Encerra na primeira passada…, Desregistra a thread e sobe outra se alguém pediu trabalho durante a queda. Sem…, Acorda o processamento em segundo plano, sem bloquear a requisição. Se a thread…, test_reaciona_fila_sem_requisicao_e_sobrevive_a_falha()

### Community 76 - "_png_bomba"
Cohesion: 0.29
Nodes (7): _png_bomba(), Bomba de descompressão: arquivo minúsculo, imagem gigante. O PNG aqui tem 285…, PNG válido e altamente compressível: linhas zeradas, como uma bomba real., O teto de pixels vale para a FOTO, que é decodificada, não para o comprovante.…, test_comprovante_a4_escaneado_continua_sendo_aceito(), test_foto_de_perfil_mantem_o_teto_de_pixels(), test_png_com_pixels_demais_e_recusado_pelo_cabecalho()

### Community 77 - "_tem_limite"
Cohesion: 0.25
Nodes (8): parametrize, Rotas que custam hash de senha, processamento de imagem ou sondagem de token., Limites declarados por decorador NAQUELA rota. `resolve_limits` não serve aqui:…, Guarda do teste acima: uma rota sem limite precisa ser reprovada por ele., _tem_limite(), test_o_detector_de_limite_realmente_discrimina(), test_rotas_caras_tem_limite_de_requisicoes(), test_sessao_aberta_perde_o_perfil_quando_a_conta_deixa_de_valer()

### Community 81 - "buscar_pagamento"
Cohesion: 0.40
Nodes (5): buscar_pagamento(), Consulta o pagamento diretamente na API do Mercado Pago - fonte de verdade de…, test_buscar_pagamento_expoe_meio_de_pagamento_e_moeda(), test_buscar_pagamento_falha_de_transporte_levanta_indisponivel(), test_buscar_pagamento_sucesso()

### Community 82 - "_chave_da_conta"
Cohesion: 0.40
Nodes (5): _chave_da_conta(), Chave de limite por CONTA, caindo no IP só para quem não está autenticado. A…, Alunos atrás do mesmo IP (o Wi-Fi da academia) não dividem a cota., test_limite_de_upload_e_por_conta_e_nao_por_ip(), test_visitante_sem_sessao_ainda_e_limitado_por_ip()

## Knowledge Gaps
- **65 isolated node(s):** `modal`, `input_senha`, `icone_senha`, `formularioPlano`, `campoPreco` (+60 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PagamentoDAO` connect `PagamentoDAO` to `test_auditoria_seguranca.py`, `config.py`, `adm_bp.py`, `criar_aluno`, `criar_pagamento`, `PagamentoEvento`, `test_regressao_auditoria.py`, `test_mudanca_plano.py`, `.contratar_plano`, `logar_como_aluno`, `test_pix_rotas.py`, `.buscar_por_id`, `pix_bp.py`, `AlunoDAO`, `test_seguranca.py`, `checkout_bp.py`, `usuario_bp.py`?**
  _High betweenness centrality (0.193) - this node is a cross-community bridge._
- **Why does `Aluno` connect `AlunoDAO` to `PagamentoDAO`, `config.py`, `adm_bp.py`, `criar_aluno`, `test_regressao_auditoria.py`, `enviar_email`, `autorizacao.py`, `test_seguranca.py`, `checkout_bp.py`, `usuario_bp.py`, `pagina_cadastro`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Why does `AlunoDAO` connect `AlunoDAO` to `PagamentoDAO`, `config.py`, `adm_bp.py`, `turma_bp.py`, `criar_aluno`, `test_regressao_auditoria.py`, `.listar_paginado`, `test_perfil_e_foto.py`, `test_seguranca.py`, `usuario_bp.py`, `pagina_cadastro`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Are the 130 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 130 INFERRED edges - model-reasoned connections that need verification._
- **Are the 139 inferred relationships involving `criar_pagamento()` (e.g. with `PagamentoDAO` and `Pagamento`) actually correct?**
  _`criar_pagamento()` has 139 INFERRED edges - model-reasoned connections that need verification._
- **Are the 118 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 118 INFERRED edges - model-reasoned connections that need verification._
- **Are the 105 inferred relationships involving `logar_como_aluno()` (e.g. with `test_aluno_nao_alcanca_cobranca_de_outro_aluno()` and `test_checkout_recusa_cobranca_indisponivel()`) actually correct?**
  _`logar_como_aluno()` has 105 INFERRED edges - model-reasoned connections that need verification._