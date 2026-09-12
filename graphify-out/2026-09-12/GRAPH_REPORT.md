# Graph Report - SistemaEXTREMETEAM  (2026-09-12)

## Corpus Check
- 104 files · ~159,762 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1415 nodes · 3782 edges · 92 communities (77 shown, 15 thin omitted)
- Extraction: 78% EXTRACTED · 22% INFERRED · 0% AMBIGUOUS · INFERRED: 823 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ff241ce3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- .totais_periodo
- Aluno Profile Page
- config.py
- criar_aluno
- test_limites_pagamento.py
- servidor.py
- PagamentoDAO
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
- test_financeiro_dao.py
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
- .buscar_por_id
- pagamento_polling.test.cjs
- .contratar_plano
- logar_como_aluno
- criar_pagamento
- .buscar_por_id
- d9e2f6a14c80_contatos_academia_perfis_professores.py
- Academia
- botao_ocupado.test.cjs
- test_seguranca.py
- checkout_abertura.test.cjs
- filtros_financeiro.js
- gunicorn.conf.py
- limites_pagamento.py
- fila_email.py
- test_migracao_cadastro_administrativo.py
- salvar_foto_perfil
- test_keep_alive.py
- keep_alive.py
- pagina_cadastro
- autorizacao.py
- erro_validacao_senha
- test_fila_email_concorrencia_postgres.py
- EmailPendente
- turma_bp.py
- Flask App Service (compose)
- _FakePreferenceResource
- .listar_paginado
- credenciais.py
- referencia_credencial_admin
- Revisão independente — Codex — 2026-09-12
- _laco
- _png_bomba
- _tem_limite
- e4b7c2a91d35_cadastro_administrativo_e_convite_de_acesso.py
- pagina_login
- _chave_da_conta
- test_retorno_ignora_status_aprovado_da_query_string
- test_linha_com_defeito_nao_trava_a_fila_atras_dela
- test_jpeg_grande_e_aceito_porque_decodifica_em_escala_reduzida
- test_decodificacao_de_imagem_e_serializada_no_processo
- test_a_suite_nunca_escreve_na_pasta_de_uploads_do_projeto
- test_sessao_sem_carimbo_de_credencial_e_recusada
- test_trocar_a_credencial_do_admin_encerra_a_sessao_administrativa
- test_o_mesmo_aviso_pode_ser_enviado_de_novo_em_outro_dia
- test_uma_falha_do_provedor_nao_queima_todas_as_tentativas

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

## Communities (92 total, 15 thin omitted)

### Community 0 - ".totais_periodo"
Cohesion: 0.14
Nodes (10): Carrega aluno e plano junto das mensalidades. O template do painel lê…, Lista completa (sem paginar). Mantida para relatórios e testes., Uma página de mensalidades, recortada pelo banco (LIMIT/OFFSET). O painel…, Totais do painel financeiro - sempre calculados no backend a partir do banco,…, Status como o painel deve LER, com o vencimento aplicado na própria consulta. A…, test_listar_filtrado_por_status_e_busca_de_aluno(), test_financeiro_pagina_no_banco_sem_carregar_tudo(), test_indicadores_e_tabela_concordam_na_primeira_abertura() (+2 more)

### Community 1 - "Aluno Profile Page"
Cohesion: 0.06
Nodes (38): Extreme Team Logo Image, Academia do Bitelo Logo, abrirmodal(), fechar(), icone_senha, input_senha, modal, mostrarSenha() (+30 more)

### Community 2 - "config.py"
Cohesion: 0.06
Nodes (30): Pagina, _paginar(), O que aconteceu numa tentativa de contratar/renovar/trocar de plano., Uma fatia de resultados já recortada pelo banco, com o que a navegação precisa., Uma página existe mesmo quando está vazia. Sem isto, `__len__` fazia `{% if…, Aplica LIMIT/OFFSET e conta o total numa consulta separada e barata. A contagem…, ResultadoContratacao, Decimal (+22 more)

### Community 3 - "criar_aluno"
Cohesion: 0.11
Nodes (40): criar_aluno(), test_aluno_existente_continua_entrando_normalmente(), test_area_do_aluno_renderiza_telas_independentes_do_menu(), test_escolher_plano_cria_mensalidade_e_redireciona_para_pix(), test_perfil_so_autoriza_abertura_automatica_da_propria_mensalidade(), test_plano_atual_continua_disponivel_para_gerar_cobranca(), test_plano_invalido_nao_cria_mensalidade(), test_reenvio_da_contratacao_reutiliza_mensalidade() (+32 more)

### Community 4 - "test_limites_pagamento.py"
Cohesion: 0.15
Nodes (16): consultar_mp(), fixture, parametrize, Limites de pagamento por conta, com o provedor inteiramente simulado., _sessao_admin(), _sessao_aluno(), test_admin_limite_por_usuario_persiste_entre_sessoes(), test_alunos_no_mesmo_ip_tem_limites_separados() (+8 more)

### Community 5 - "servidor.py"
Cohesion: 0.11
Nodes (19): after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, context_processor, errorhandler, formatar_moeda(), Nome legível da forma de pagamento. Antes as telas usavam `|replace('_','…, Formata um valor em reais no padrão brasileiro: R$ 1.080,00. Usado como filtro… (+11 more)

### Community 6 - "PagamentoDAO"
Cohesion: 0.08
Nodes (23): criar_pix_mensalidade(), _processar_status_mp(), limitar_criacao_pagamento, Fonte unica de aprovacao, usada pelo webhook, pelo polling de status e pela…, webhook_mercado_pago(), PagamentoDAO, Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda. O…, Primeiro dia não coberto por outra mensalidade do mesmo aluno. (+15 more)

### Community 7 - "Relatório de segurança — Sistema Extreme Team"
Cohesion: 0.08
Nodes (24): A verificar em execução, Atualização após as correções, F10 — Redirecionamento aberto via `Referer`, F11 — `/logout` aceita GET, F12 — Enumeração de usuários por tempo de resposta, F13 — Senha mínima de 6 caracteres, sem outros critérios, F14 — Webhook sem verificação de recência do timestamp, F15 — Curinga de `LIKE` no filtro do financeiro (+16 more)

### Community 9 - "test_mercado_pago_servico.py"
Cohesion: 0.13
Nodes (27): Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, validar_assinatura_webhook(), Hipótese: uma notificação capturada ontem pode ser reenviada hoje., test_webhook_recusa_assinatura_antiga(), base_url(), _criar_preferencia(), mp_fake(), fixture (+19 more)

### Community 10 - "test_mudanca_plano.py"
Cohesion: 0.15
Nodes (28): cancelar_mudanca_plano_admin(), A administração pode cancelar um pedido de troca ainda não aplicado. Não existe…, cancelar_mudanca_plano(), Cancela um pedido de troca antes de ele ser aplicado. Depois de efetivado não…, Persistência dos pedidos de troca de plano agendados para a próxima renovação., SolicitacaoPlanoDAO, _agendar(), _pagar() (+20 more)

### Community 11 - "test_professor_perfil.py"
Cohesion: 0.19
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
Cohesion: 0.13
Nodes (22): _forma_pagamento_confirmada(), _pagamento_mp_mais_relevante(), _pagamento_ou_none(), _pix_expirado(), limitar_consulta_pagamento, route, Todas as referencias que esta mensalidade legitimamente pode receber de volta:…, Meio de pagamento realmente usado, sempre a partir da resposta da API. (+14 more)

### Community 18 - "AlunoDAO"
Cohesion: 0.07
Nodes (67): _aluno_do_cpf_ou_painel(), enviar_convite_acesso(), Aluno de uma rota administrativa, ou None (a rota redireciona ao painel)., Envia ao aluno o link de uso único que transforma o cadastro numa conta. O…, _convidar_cadastro_existente(), Cadastro administrativo que alguém tentou recriar pelo formulário público. Em…, AlunoDAO, Matrícula feita no balcão: sem login, sem senha e sem convite de acesso. Nasce… (+59 more)

### Community 19 - "test_financeiro_dao.py"
Cohesion: 0.14
Nodes (14): mensalidade_destaque(), Escolhe a mensalidade mais relevante para o card 'Minha mensalidade': a mais…, True se já existe um Pix ou um checkout válido emitido para esta cobrança.…, True se a cobrança Pix já gerada para este pagamento ainda pode ser…, True se a preferência do Checkout Pro já criada pode ser reaproveitada. Só…, provider_payment_id sozinho não basta: pagamentos do Checkout Pro…, test_mensalidade_destaque_prioriza_a_mais_proxima_de_vencer(), test_pix_ainda_valido_falso_apos_expirar() (+6 more)

### Community 20 - "checkout_bp.py"
Cohesion: 0.12
Nodes (28): abrir_checkout(), _acesso_permitido(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), limitar_consulta_pagamento, limitar_criacao_pagamento, route (+20 more)

### Community 21 - "pix.js"
Cohesion: 0.33
Nodes (14): abrirPix(), alvoDoRotulo(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), liberarBotao(), limparConteudoAnterior() (+6 more)

### Community 22 - "usuario_bp.py"
Cohesion: 0.15
Nodes (21): _acesso_permitido_pagamento(), _aluno_da_sessao(), atualizar_dados_perfil(), comprovante_mensalidade(), foto_perfil(), _pagamento_com_acesso_ou_404(), pagina_pagamento(), pagina_perfil() (+13 more)

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
Nodes (46): _assinar(), _pagamento_mp(), _preparar_para_conciliacao(), parametrize, Auditoria de segurança: sondas escritas para TENTAR quebrar as regras. Nenhum…, Hipótese: a sessão de professor é aceita nas rotas financeiras do aluno., Hipótese: como o JS agora usa fetch, o POST perdeu a exigência de CSRF., Hipótese: as demais rotas de dinheiro aceitam POST sem token. (+38 more)

### Community 34 - "mercado_pago.py"
Cohesion: 0.12
Nodes (29): _base_url_opcional(), base_url_publica(), buscar_pagamentos_por_referencia(), cancelar_pagamento(), criar_pagamento_pix(), criar_preferencia_checkout(), _erro_menciona(), _erro_menciona_expiracao() (+21 more)

### Community 35 - "adm_bp.py"
Cohesion: 0.08
Nodes (47): aprovar_aluno(), aprovar_comprovante_manual(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_aluno(), cadastrar_pagamento(), cadastrar_plano(), _chave_lote() (+39 more)

### Community 36 - "Professor"
Cohesion: 0.12
Nodes (22): ProfessorDAO, TurmaDAO, Professor, Turma, impressao_credencial(), Resumo curto e não reversível do hash da senha, guardado na sessão. Nunca é a…, logar_como_professor(), fixture (+14 more)

### Community 37 - "test_regressao_auditoria.py"
Cohesion: 0.06
Nodes (28): _contar_selects_em_alunos(), _credencial(), Regressões da auditoria de segurança, desempenho e confiabilidade. Cada caso…, Uma linha `desistiu` nunca foi entregue: recusar o reenvio fazia a tela dizer…, A revivência vale só para o abandonado: clique duplo continua virando um envio., Trocar senha, e-mail ou foto são ações de quem JÁ está autenticado. Devolver o…, Conferir a credencial do admin custava um scrypt em TODO login. São ~74 ms e…, test_abrir_o_painel_financeiro_nao_grava_no_banco() (+20 more)

### Community 38 - "enviar_email"
Cohesion: 0.14
Nodes (22): recuperar_senha(), solicitar_troca_email(), aluno_do_token(), ConviteIndisponivel, descartar(), enviar(), gerar_token(), _hash() (+14 more)

### Community 41 - ".buscar_por_id"
Cohesion: 0.33
Nodes (6): _imagem_jpeg_valida(), test_admin_acessa_foto_de_qualquer_aluno(), test_aluno_nao_acessa_foto_de_outro_aluno(), test_substituir_e_remover_foto(), test_upload_de_arquivo_disfarcado_e_recusado(), test_upload_de_foto_valida()

### Community 42 - "pagamento_polling.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 43 - ".contratar_plano"
Cohesion: 0.15
Nodes (8): Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, Aplica um pedido agendado cujo período de origem já terminou sem renovação.…, Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, Com uma troca já agendada, só dois planos fazem sentido num pedido de…, A cobrança do período seguinte tem de nascer no plano que o aluno agendou.…, `pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -…, test_mudanca_nao_vale_por_prazo_enquanto_houver_periodo_pago(), test_mudanca_vale_por_decurso_de_prazo_quando_o_plano_vence()

### Community 44 - "logar_como_aluno"
Cohesion: 0.10
Nodes (42): logar_como_aluno(), _mockar_preferencia(), parametrize, Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala…, Um boleto pendente do Checkout Pro grava provider_payment_id, mas não é Pix:…, _resposta_preferencia(), test_abertura_json_navega_sem_redirecionar_post_externo(), test_admin_tambem_pode_abrir_checkout() (+34 more)

### Community 45 - "criar_pagamento"
Cohesion: 0.21
Nodes (24): MercadoPagoIndisponivel, Falha de transporte (timeout/DNS/conexao) ao falar com a API do Mercado Pago., criar_pagamento(), test_mercado_pago_indisponivel_nao_persiste_nada(), _assinar(), _resposta_consulta(), _resposta_criacao(), test_admin_tambem_pode_gerar_pix() (+16 more)

### Community 46 - ".buscar_por_id"
Cohesion: 0.16
Nodes (26): _assinar(), _pagamento_mp(), _preparar_retorno(), Pix aberto e checkout concluído ao mesmo tempo: a consulta pelo…, test_retorno_com_aprovacao_confirmada_marca_pago(), test_retorno_com_mp_indisponivel_avisa_sem_mudar_status(), test_retorno_de_boleto_avisa_sobre_o_prazo(), test_retorno_de_sucesso_nao_marca_pago_sem_confirmacao() (+18 more)

### Community 47 - "d9e2f6a14c80_contatos_academia_perfis_professores.py"
Cohesion: 0.83
Nodes (3): _campos_professor(), downgrade(), upgrade()

### Community 49 - "Academia"
Cohesion: 0.14
Nodes (17): configuracoes(), route, Academia, link_email(), Normalização de contatos profissionais antes de montar links públicos., validar_email(), validar_instagram(), validar_whatsapp() (+9 more)

### Community 50 - "botao_ocupado.test.cjs"
Cohesion: 0.18
Nodes (7): assert, criarElemento(), fs, montar(), path, test, vm

### Community 51 - "test_seguranca.py"
Cohesion: 0.18
Nodes (5): _imagem_jpeg(), test_limite_de_login_por_ip_e_identificador(), test_recuperacao_envia_link_da_url_configurada(), test_rotas_admin_nao_colidem_cpf_com_campos_editaveis(), test_url_publica_independe_do_host_da_requisicao()

### Community 52 - "checkout_abertura.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 55 - "gunicorn.conf.py"
Cohesion: 0.25
Nodes (9): post_worker_init(), Hooks carregados pelo Gunicorn; nunca executados por flask db upgrade., worker_exit(), iniciar(), _laco(), parar(), Aciona a fila periodicamente durante a vida de um worker Gunicorn. Importar…, Inicia uma vez por processo, depois de carregar a aplicação e migrar o banco. (+1 more)

### Community 56 - "limites_pagamento.py"
Cohesion: 0.50
Nodes (3): chave_pagamento(), Orçamentos compartilhados das chamadas interativas ao provedor de pagamento., A mesma conta mantém seu limite entre sessões, rotas e mensalidades. Alunos que…

### Community 57 - "fila_email.py"
Cohesion: 0.16
Nodes (14): espera_da_proxima_tentativa(), Fila de e-mails no banco. Aviso e cobrança coletivos saíam um a um dentro da…, contar_falhados(), contar_pendentes(), _entregar(), listar_pendentes(), processar_agora(), Processamento dos e-mails coletivos fora da requisição. O que muda em relação… (+6 more)

### Community 58 - "test_migracao_cadastro_administrativo.py"
Cohesion: 0.40
Nodes (3): banco_antigo(), fixture, Verifica a migração em um banco isolado com o schema anterior e dados.

### Community 59 - "salvar_foto_perfil"
Cohesion: 0.18
Nodes (18): ArquivoInvalido, _conferir_dimensoes(), _detectar_tipo_imagem_real(), ImagemGrandeDemais, _pasta(), Exception, _raiz_uploads(), Armazenamento de arquivos enviados por usuários (fotos de perfil, comprovantes… (+10 more)

### Community 60 - "test_keep_alive.py"
Cohesion: 0.16
Nodes (7): ambiente_limpo(), fixture, parametrize, Garante que o keep-alive fica desligado por padrão e só pinga a própria origem., test_intervalo_fica_dentro_da_faixa(), test_nao_liga_com_valor_negativo(), test_ping_so_considera_200_como_sucesso()

### Community 61 - "keep_alive.py"
Cohesion: 0.29
Nodes (9): iniciar(), _intervalo(), _laco(), _ligado(), parar(), _pingar(), Mantém a aplicação acordada em hospedagens que hibernam por inatividade. Uma…, Encerra o laço. Usado pelos testes; em produção a thread é daemon. (+1 more)

### Community 62 - "pagina_cadastro"
Cohesion: 0.42
Nodes (7): pagina_cadastro(), formatar_cpf(), formatar_telefone(), mascarar_email(), Mostra o bastante do e-mail para o dono se reconhecer, sem revelá-lo a…, somente_digitos(), variantes_cpf()

### Community 63 - "autorizacao.py"
Cohesion: 0.22
Nodes (13): _acesso_permitido(), aluno_autorizado(), aluno_requerido(), _credencial_confere(), encerrar_sessao(), professor_autorizado(), Autorização das rotas protegidas. A sessão diz quem *afirmou* ser quem; quem…, Rotas da área do aluno: injeta o aluno já revalidado como primeiro argumento. (+5 more)

### Community 64 - "erro_validacao_senha"
Cohesion: 0.15
Nodes (17): alterar_senha_perfil(), _aluno_por_token(), ativar_acesso(), confirmar_email(), enviar_comprovante_manual_aluno(), enviar_foto_perfil(), Descarta todo link pendente que ainda autorizaria assumir ou redirecionar a…, Localiza o aluno pelo hash do token, filtrando no banco por uma coluna indexada. (+9 more)

### Community 66 - "test_fila_email_concorrencia_postgres.py"
Cohesion: 0.18
Nodes (10): _enfileirar_em_transacao_propria(), postgres_fila(), fixture, Idempotência da fila de e-mail sob concorrência real, em PostgreSQL…, A recusa de uma chave repetida não pode desfazer o lote inteiro. Um…, A trava do lote precisa valer até o fim do lote. Comitar linha a linha…, Enfileira e comita numa sessão própria, como faria outra requisição., test_chave_duplicada_nao_descarta_os_outros_destinatarios_do_lote() (+2 more)

### Community 67 - "EmailPendente"
Cohesion: 0.20
Nodes (7): EmailPendente, enfileirar(), Registra um e-mail para envio. Devolve a linha criada, ou None se já existia.…, parametrize, Agendamento sem rede, threads reais ou esperas de relógio., test_nao_inicia_em_testes(), test_retomada_de_item_persistido_e_retentativa_sem_painel()

### Community 68 - "turma_bp.py"
Cohesion: 0.15
Nodes (22): _acesso_permitido(), cadastrar_professor(), cadastrar_turma(), desmatricular_aluno(), detalhe_turma(), editar_professor(), foto_professor(), gerenciar_turmas() (+14 more)

### Community 69 - "Flask App Service (compose)"
Cohesion: 0.22
Nodes (9): Flask App Service (compose), Postgres DB Service (compose), postgres_data Volume, Flask, Flask-SQLAlchemy, Gunicorn, psycopg2-binary, python-dotenv (+1 more)

### Community 71 - ".listar_paginado"
Cohesion: 0.20
Nodes (9): _parece_busca_por_cpf(), O termo é um CPF, ou um pedaço dele, e não um nome que por acaso tem número?, Uma página de alunos já cadastrados, recortada e filtrada pelo banco. O painel…, Qualquer dígito no termo virava `CPF LIKE '%3%'` e devolvia a academia inteira., O CPF é guardado formatado; digitar só os números precisa encontrar mesmo assim., test_busca_do_admin_encontra_o_aluno_pelo_cpf_so_com_digitos(), test_busca_por_nome_com_numero_nao_devolve_todo_mundo(), test_busca_so_trata_como_cpf_o_que_parece_cpf() (+1 more)

### Community 72 - "credenciais.py"
Cohesion: 0.20
Nodes (11): admin_configurado(), comparar_em_tempo_constante(), credencial_admin_confere(), gerar_hash_admin(), _main(), Credencial do administrador, com transição de texto puro para hash. O login do…, Gera o valor de ADMIN_PASSWORD_HASH. Usado pelo utilitário de linha de comando., `python -m servicos.credenciais` - gera o valor de ADMIN_PASSWORD_HASH. A senha… (+3 more)

### Community 73 - "referencia_credencial_admin"
Cohesion: 0.18
Nodes (8): PresencaDAO, Presenca, Valor que representa a credencial administrativa em vigor, ou None se não há…, referencia_credencial_admin(), parametrize, test_consulta_com_data_invalida_exibe_hoje_e_aviso(), test_presenca_com_data_invalida_nao_grava(), test_presenca_com_data_valida_continua_disponivel()

### Community 74 - "Revisão independente — Codex — 2026-09-12"
Cohesion: 0.20
Nodes (9): 1. Retomada automática da fila de e-mails, 2. Orientação perigosa de migration, 3. Limite da garantia de envio único, Canal de coordenação solicitado pelo usuário, Implementação complementar entregue pelo Codex, Limites desta revisão, Pendências para integração pelo Claude, Revisão independente — Codex — 2026-09-12 (+1 more)

### Community 75 - "_laco"
Cohesion: 0.29
Nodes (7): disparar(), _laco(), _liberar_e_retomar_se_preciso(), Drena a fila enquanto houver entrega acontecendo. Encerra na primeira passada…, Desregistra a thread e sobe outra se alguém pediu trabalho durante a queda. Sem…, Acorda o processamento em segundo plano, sem bloquear a requisição. Se a thread…, test_reaciona_fila_sem_requisicao_e_sobrevive_a_falha()

### Community 76 - "_png_bomba"
Cohesion: 0.29
Nodes (7): _png_bomba(), Bomba de descompressão: arquivo minúsculo, imagem gigante. O PNG aqui tem 285…, PNG válido e altamente compressível: linhas zeradas, como uma bomba real., O teto de pixels vale para a FOTO, que é decodificada, não para o comprovante.…, test_comprovante_a4_escaneado_continua_sendo_aceito(), test_foto_de_perfil_mantem_o_teto_de_pixels(), test_png_com_pixels_demais_e_recusado_pelo_cabecalho()

### Community 77 - "_tem_limite"
Cohesion: 0.25
Nodes (8): parametrize, Rotas que custam hash de senha, processamento de imagem ou sondagem de token., Limites declarados por decorador NAQUELA rota. `resolve_limits` não serve aqui:…, Guarda do teste acima: uma rota sem limite precisa ser reprovada por ele., _tem_limite(), test_o_detector_de_limite_realmente_discrimina(), test_rotas_caras_tem_limite_de_requisicoes(), test_sessao_aberta_perde_o_perfil_quando_a_conta_deixa_de_valer()

### Community 81 - "pagina_login"
Cohesion: 0.33
Nodes (4): pagina_login(), Grava na sessão atual a credencial em vigor (login ou troca de senha bem-…, registrar_credencial(), test_login_nao_aceita_nome_do_aluno()

### Community 82 - "_chave_da_conta"
Cohesion: 0.40
Nodes (5): _chave_da_conta(), Chave de limite por CONTA, caindo no IP só para quem não está autenticado. A…, Alunos atrás do mesmo IP (o Wi-Fi da academia) não dividem a cota., test_limite_de_upload_e_por_conta_e_nao_por_ip(), test_visitante_sem_sessao_ainda_e_limitado_por_ip()

## Knowledge Gaps
- **64 isolated node(s):** `modal`, `input_senha`, `icone_senha`, `formularioPlano`, `campoPreco` (+59 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PagamentoDAO` connect `PagamentoDAO` to `.totais_periodo`, `config.py`, `criar_aluno`, `test_mudanca_plano.py`, `pix_bp.py`, `AlunoDAO`, `test_financeiro_dao.py`, `checkout_bp.py`, `usuario_bp.py`, `test_auditoria_seguranca.py`, `adm_bp.py`, `test_regressao_auditoria.py`, `.contratar_plano`, `logar_como_aluno`, `criar_pagamento`, `.buscar_por_id`, `test_seguranca.py`, `erro_validacao_senha`, `test_retorno_ignora_status_aprovado_da_query_string`?**
  _High betweenness centrality (0.183) - this node is a cross-community bridge._
- **Why does `AlunoDAO` connect `AlunoDAO` to `config.py`, `adm_bp.py`, `turma_bp.py`, `criar_aluno`, `PagamentoDAO`, `.listar_paginado`, `Professor`, `.buscar_por_id`, `test_mudanca_plano.py`, `test_regressao_auditoria.py`, `pagina_login`, `test_seguranca.py`, `usuario_bp.py`, `pagina_cadastro`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Why does `Aluno` connect `AlunoDAO` to `erro_validacao_senha`, `config.py`, `adm_bp.py`, `criar_aluno`, `test_regressao_auditoria.py`, `enviar_email`, `PagamentoDAO`, `usuario_bp.py`, `pagina_cadastro`, `autorizacao.py`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Are the 130 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 130 INFERRED edges - model-reasoned connections that need verification._
- **Are the 139 inferred relationships involving `criar_pagamento()` (e.g. with `PagamentoDAO` and `Pagamento`) actually correct?**
  _`criar_pagamento()` has 139 INFERRED edges - model-reasoned connections that need verification._
- **Are the 118 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 118 INFERRED edges - model-reasoned connections that need verification._
- **Are the 105 inferred relationships involving `logar_como_aluno()` (e.g. with `test_aluno_nao_alcanca_cobranca_de_outro_aluno()` and `test_checkout_recusa_cobranca_indisponivel()`) actually correct?**
  _`logar_como_aluno()` has 105 INFERRED edges - model-reasoned connections that need verification._