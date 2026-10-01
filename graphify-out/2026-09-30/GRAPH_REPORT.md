# Graph Report - SistemaEXTREMETEAM  (2026-09-30)

## Corpus Check
- 170 files · ~229,950 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2260 nodes · 5542 edges · 166 communities (136 shown, 30 thin omitted)
- Extraction: 80% EXTRACTED · 20% INFERRED · 0% AMBIGUOUS · INFERRED: 1094 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1ad814aa`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- criar_pagamento
- extreme.css
- planos.py
- .listar_por_aluno
- .buscar_por_id
- criar_aluno
- pix_bp.py
- test_regressao_auditoria.py
- SistemaEXTREMETEAM Project
- test_mercado_pago_servico.py
- logar_como_admin
- test_analytics.py
- test_migracao_checkout.py
- checkout.js
- CLAUDE.md
- test_home_planos.py
- MercadoPagoIndisponivel
- AlunoDAO
- MercadoPagoConexao
- checkout_bp.py
- pix.js
- config.py
- env.py
- pagamento.js
- c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py
- varredura.mjs
- 896e70afc9c5_adiciona_foto_e_graduacao_do_aluno_.py
- test_auditoria_seguranca.py
- seo.py
- test_limites_pagamento.py
- impressao_credencial
- gmail_conta.py
- convites.py
- PagamentoDAO
- pagamento_polling.test.cjs
- mercado_pago_conta.py
- Pagamento
- test_pix_rotas.py
- limit
- d9e2f6a14c80_contatos_academia_perfis_professores.py
- test_conversao_home.py
- botao_ocupado.test.cjs
- test_seguranca.py
- checkout_abertura.test.cjs
- filtros_financeiro.js
- gunicorn.conf.py
- PagamentoEvento
- fila_email.py
- test_migracao_cadastro_administrativo.py
- salvar_foto_perfil
- test_keep_alive.py
- _FakePaymentResource
- mercado_pago.py
- test_arranque_seguranca.py
- Aluno
- turma_bp.py
- servidor.py
- mercado_pago_oauth_bp.py
- test_admin_mercado_pago.py
- pagina_login
- shot.mjs
- Componentes
- google_login.py
- Pagina
- analytics.test.cjs
- e4b7c2a91d35_cadastro_administrativo_e_convite_de_acesso.py
- a1f0c3e75b92_schema_inicial.py
- Contrato do redesign — SistemaEXTREMETEAM
- conftest.py
- test_sessao_revogada.py
- Skills Disponíveis
- componentes.js
- test_paginas_erro.py
- analytics.js
- Relatório de segurança — Sistema Extreme Team
- test_seo.py
- test_email_componentes.py
- test_checkout_rotas.py
- painel_adm
- test_layouts.py
- Academia
- ResultadoContratacao
- Flask App Service (compose)
- enviar_aviso
- Plano
- Etapa 1 — migrar páginas para os layouts (SEM mudar o visual)
- Etapas 4 a 6 — aluno, admin, professor (aplicar os componentes nas páginas)
- seo_bp.py
- Etapa 2 — biblioteca de componentes
- Etapa 3 — home com os planos + termos
- test_prontidao.py
- test_perfil_e_foto.py
- editar_plano
- test_observabilidade.py
- usuario_bp.py
- PlanoDAO
- test_backup_scripts.py
- revogar_sessao_atual
- gerar_imagem_og.py
- _json_ld
- erro_validacao_senha
- pagina_cadastro
- test_o_mesmo_aviso_pode_ser_enviado_de_novo_em_outro_dia
- Professor
- adm_bp.py
- conteudo_home.py
- url_publica
- .listar_paginado
- admin_requerido
- academia_bp.py
- keep_alive.py
- prontidao.py
- capturar_emails
- analytics.py
- _tem_limite
- backup.sh
- _png_bomba
- .efetivar_mudancas_por_prazo
- test_financeiro_admin_painel.py
- _chave_da_conta
- verificar_email_cadastro
- agendar.sh
- restaurar.sh
- preparar_nonce_csp
- formatar_moeda
- test_admin_lanca_mensalidade_paga_no_cartao
- test_linha_com_defeito_nao_trava_a_fila_atras_dela
- test_reenviar_um_aviso_que_desistiu_volta_a_enfileirar
- test_um_envio_ainda_pendente_continua_sendo_recusado
- test_limite_atingido_nao_mostra_login_a_quem_ja_entrou
- test_retentativa_acontece_sem_ninguem_abrir_o_painel
- test_jpeg_grande_e_aceito_porque_decodifica_em_escala_reduzida
- test_decodificacao_de_imagem_e_serializada_no_processo
- test_a_suite_nunca_escreve_na_pasta_de_uploads_do_projeto
- test_sessao_sem_carimbo_de_credencial_e_recusada
- test_trocar_a_credencial_do_admin_encerra_a_sessao_administrativa
- test_uma_falha_do_provedor_nao_queima_todas_as_tentativas
- test_login_de_aluno_nao_paga_o_hash_do_admin
- exempt
- parametrize

## God Nodes (most connected - your core abstractions)
1. `PagamentoDAO` - 210 edges
2. `criar_aluno()` - 159 edges
3. `criar_pagamento()` - 157 edges
4. `logar_como_admin()` - 154 edges
5. `logar_como_aluno()` - 135 edges
6. `AlunoDAO` - 92 edges
7. `Aluno` - 64 edges
8. `PlanoDAO` - 62 edges
9. `MercadoPagoIndisponivel` - 43 edges
10. `Professor` - 40 edges

## Surprising Connections (you probably didn't know these)
- `Planos Disponíveis Section` --shares_data_with--> `Plano`  [INFERRED]
  templates/pgUsuario.html → modelos/plano.py
- `Presença Form` --shares_data_with--> `Presenca`  [INFERRED]
  templates/turma.html → modelos/presenca.py
- `Histórico de Mensalidades Section` --shares_data_with--> `Pagamento`  [INFERRED]
  templates/pgUsuario.html → modelos/pagamento.py
- `Cadastrar Plano Form` --shares_data_with--> `Plano`  [INFERRED]
  templates/pgAdm.html → modelos/plano.py
- `Turma Detail Page` --shares_data_with--> `Turma`  [INFERRED]
  templates/turma.html → modelos/turma.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Shared Confirmation Modal Pattern** — templates_components_confirm_modal_dialog, templates_pgadm_page, templates_pgprofessor_page, templates_pgusuario_page, templates_turmas_page [EXTRACTED 1.00]
- **Mensalidade (Billing) Management Flow** — templates_dt_aluno_pagamento_form, templates_pgusuario_mensalidades_section, modelos_pagamento_pagamento, modelos_plano_plano [INFERRED 0.85]
- **Turma and Attendance Management Flow** — templates_turmas_turma_form, templates_turma_presenca_form, templates_pgprofessor_page, modelos_turma_turma [INFERRED 0.85]

## Communities (166 total, 30 thin omitted)

### Community 0 - "criar_pagamento"
Cohesion: 0.11
Nodes (40): criar_pagamento(), logar_como_aluno(), Hipótese: forjar ?status=approved na volta do MP quita a mensalidade., test_retorno_ignora_status_aprovado_da_query_string(), _mockar_preferencia(), Um boleto pendente do Checkout Pro grava provider_payment_id, mas não é Pix:…, test_abertura_json_navega_sem_redirecionar_post_externo(), test_admin_tambem_pode_abrir_checkout() (+32 more)

### Community 1 - "extreme.css"
Cohesion: 0.05
Nodes (34): abrirmodal(), fechar(), icone_senha, input_senha, modal, mostrarSenha(), campoDuracao, campoPreco (+26 more)

### Community 2 - "planos.py"
Cohesion: 0.06
Nodes (44): cadeia_paga(), cartao_do_plano(), cobranca_a_pagar(), cobranca_em_decisao(), cobranca_pendente(), duracao_dias(), _duracao_por_extenso(), esta_inadimplente() (+36 more)

### Community 3 - ".listar_por_aluno"
Cohesion: 0.11
Nodes (32): Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, `pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -…, test_escolher_plano_cria_mensalidade_e_redireciona_para_pix(), test_plano_invalido_nao_cria_mensalidade(), test_reenvio_da_contratacao_reutiliza_mensalidade(), test_valor_enviado_pelo_navegador_e_ignorado(), test_cobranca_criada_na_promocao_sai_pelo_preco_promocional() (+24 more)

### Community 4 - ".buscar_por_id"
Cohesion: 0.14
Nodes (16): test_admin_muda_o_status_sem_perder_a_forma_do_mercado_pago(), test_admin_nao_grava_forma_inventada(), test_aprovar_comprovante_recusa_forma_inventada(), test_forma_em_branco_fica_sem_forma(), Hipótese: se a resposta do MP trouxer um destino estranho, ele é salvo e…, test_url_hostil_do_mercado_pago_nao_e_persistida(), test_configuracao_ausente_falha_de_forma_explicita(), test_mercado_pago_indisponivel_nao_persiste_nada() (+8 more)

### Community 5 - "criar_aluno"
Cohesion: 0.17
Nodes (29): Persistência dos pedidos de troca de plano agendados para a próxima renovação., SolicitacaoPlanoDAO, criar_aluno(), test_aluno_existente_continua_entrando_normalmente(), test_area_do_aluno_renderiza_telas_independentes_do_menu(), test_plano_atual_continua_disponivel_para_gerar_cobranca(), _agendar(), _pagar() (+21 more)

### Community 6 - "pix_bp.py"
Cohesion: 0.08
Nodes (49): _data_da_aprovacao(), _forma_pagamento_confirmada(), _instante_utc(), _iso_utc(), _pagamento_mp_mais_relevante(), _pagamento_ou_none(), _pix_expirado(), limitar_consulta_pagamento (+41 more)

### Community 7 - "test_regressao_auditoria.py"
Cohesion: 0.07
Nodes (22): _contar_selects_em_alunos(), _credencial(), Regressões da auditoria de segurança, desempenho e confiabilidade. Cada caso…, test_abrir_o_painel_financeiro_nao_grava_no_banco(), test_aluno_desativado_nao_ve_mais_a_propria_foto_pela_sessao_antiga(), test_aluno_troca_a_senha_para_uma_com_acentos(), test_aviso_coletivo_enfileira_em_vez_de_enviar_na_requisicao(), test_aviso_repetido_no_mesmo_dia_avisa_em_vez_de_comemorar() (+14 more)

### Community 9 - "test_mercado_pago_servico.py"
Cohesion: 0.11
Nodes (29): Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, validar_assinatura_webhook(), Hipótese: uma notificação capturada ontem pode ser reenviada hoje., `ts=nan` fazia a comparação da janela dar False e passava pela checagem de…, test_webhook_recusa_assinatura_antiga(), test_webhook_recusa_ts_nao_numerico_finito(), base_url(), _criar_preferencia() (+21 more)

### Community 10 - "logar_como_admin"
Cohesion: 0.07
Nodes (55): logar_como_admin(), _conectar(), _dados_conexao(), _preparar_state(), parametrize, Grava uma conexão direto pelo serviço (precisa de app context)., test_ambiente_explicito_vence_a_conta_conectada(), test_ambiente_segue_o_live_mode_da_conta() (+47 more)

### Community 11 - "test_analytics.py"
Cohesion: 0.14
Nodes (20): _carrega_analytics(), com_analytics(), _csp_com_google(), _evento(), fixture, parametrize, GA4 opcional (servicos/analytics.py): nada sem ANALYTICS_ID, nunca em área…, sem_analytics_por_padrao() (+12 more)

### Community 12 - "test_migracao_checkout.py"
Cohesion: 0.31
Nodes (8): _colunas(), conexao(), migracao(), fixture, Exercita a migração dos campos do Checkout Pro de verdade (upgrade e…, _rodar(), test_downgrade_remove_exatamente_o_que_o_upgrade_criou(), test_upgrade_adiciona_as_colunas_e_preserva_linhas_antigas()

### Community 14 - "checkout.js"
Cohesion: 0.47
Nodes (4): cancelarAberturas(), consultar(), finalizarAbertura(), parar()

### Community 16 - "test_home_planos.py"
Cohesion: 0.19
Nodes (15): Marca o plano em destaque da página inicial, desmarcando qualquer outro.…, Inclusive os arquivados: serve a quem olha o histórico (filtro do financeiro)., _plano(), _quatro_planos(), Planos na página inicial: cálculo (servicos/planos.vitrine_planos), destaque…, test_admin_destaca_e_tira_o_destaque(), test_admin_pode_criar_plano_ja_em_destaque(), test_aluno_logado_matricula_pela_area_do_aluno() (+7 more)

### Community 17 - "MercadoPagoIndisponivel"
Cohesion: 0.12
Nodes (21): exempt, webhook_mercado_pago(), Acha a mensalidade por qualquer uma das duas referências persistidas. O Pix…, buscar_pagamento(), buscar_pagamentos_por_referencia(), cancelar_pagamento(), MercadoPagoIndisponivel, Consulta o pagamento diretamente na API do Mercado Pago - fonte de verdade de… (+13 more)

### Community 18 - "AlunoDAO"
Cohesion: 0.12
Nodes (44): AlunoDAO, _matricular(), parametrize, Cadastro de aluno pela administração, ativação de acesso e confirmação de…, test_admin_lanca_e_baixa_mensalidade_de_aluno_sem_acesso(), test_admin_matricula_aluno_sem_email_senha_nem_acesso(), test_admin_pode_deixar_cadastro_de_balcao_sem_usuario_e_sem_email(), test_admin_rejeita_status_financeiro_desconhecido() (+36 more)

### Community 19 - "MercadoPagoConexao"
Cohesion: 0.09
Nodes (30): MercadoPagoConexao, Conta do Mercado Pago que a academia autorizou por OAuth. Uma linha só (a…, _agora(), _ajustar(), api_mp(), oauth_env(), postgres_mp(), fixture (+22 more)

### Community 20 - "checkout_bp.py"
Cohesion: 0.12
Nodes (26): abrir_checkout(), _acesso_permitido(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), limitar_consulta_pagamento, limitar_criacao_pagamento, route (+18 more)

### Community 21 - "pix.js"
Cohesion: 0.33
Nodes (14): abrirPix(), alvoDoRotulo(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), liberarBotao(), limparConteudoAnterior() (+6 more)

### Community 22 - "config.py"
Cohesion: 0.14
Nodes (12): Decimal, Matricula, _para_decimal(), Pedido de troca de plano agendado para a próxima renovação. Nunca altera o…, SolicitacaoMudancaPlano, postgres_pix(), fixture, Regressão com trava de linha real, opcional na suíte que usa SQLite. Execute… (+4 more)

### Community 23 - "env.py"
Cohesion: 0.39
Nodes (7): get_engine(), get_engine_url(), get_metadata(), Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online()

### Community 24 - "pagamento.js"
Cohesion: 0.47
Nodes (9): alvoDoRotulo(), consultarStatus(), gerarOuAtualizarPix(), iniciarPolling(), liberarBotao(), marcarOcupado(), mostrarEstado(), pararPolling() (+1 more)

### Community 25 - "c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py"
Cohesion: 0.60
Nodes (5): _backfill_vigencia(), _colunas(), _criar_tabela_solicitacoes(), downgrade(), upgrade()

### Community 26 - "varredura.mjs"
Cohesion: 0.11
Nodes (23): aberto(), ACESSO, auditar(), { chromium }, CONF, confirmacoes(), crc, CREDS (+15 more)

### Community 29 - "896e70afc9c5_adiciona_foto_e_graduacao_do_aluno_.py"
Cohesion: 0.60
Nodes (3): _e_decimal(), _faltantes(), upgrade()

### Community 33 - "test_auditoria_seguranca.py"
Cohesion: 0.06
Nodes (48): Só abre o checkout HTTPS do Mercado Pago Brasil, inclusive no sandbox., url_checkout_permitida(), _assinar(), logar_como_professor(), _pagamento_mp(), _preparar_para_conciliacao(), fixture, parametrize (+40 more)

### Community 34 - "seo.py"
Cohesion: 0.18
Nodes (18): conteudo_robots(), conteudo_sitemap(), dados_estruturados_academia(), _dia(), _dias_da_linha(), _hora(), horarios_estruturados(), origem_publica() (+10 more)

### Community 35 - "test_limites_pagamento.py"
Cohesion: 0.15
Nodes (15): consultar_mp(), fixture, parametrize, Limites de pagamento por conta, com o provedor inteiramente simulado., _sessao_aluno(), test_admin_limite_por_usuario_persiste_entre_sessoes(), test_alunos_no_mesmo_ip_tem_limites_separados(), test_anonimos_limitados_por_ip_sem_consultar_provedor() (+7 more)

### Community 36 - "impressao_credencial"
Cohesion: 0.20
Nodes (16): MatriculaDAO, Presenca, impressao_credencial(), Resumo curto e não reversível do hash da senha, guardado na sessão. Nunca é a…, Valor que representa a credencial administrativa em vigor, ou None se não há…, referencia_credencial_admin(), parametrize, test_aluno_confirma_sua_frequencia() (+8 more)

### Community 37 - "gmail_conta.py"
Cohesion: 0.16
Nodes (18): GmailConexao, _access_token(), _cifrar(), _client_id(), _client_secret(), _decifrar(), enviar(), estado() (+10 more)

### Community 38 - "convites.py"
Cohesion: 0.19
Nodes (13): aluno_do_token(), ConviteIndisponivel, descartar(), enviar(), gerar_token(), _hash(), RuntimeError, Convite de acesso: como um cadastro criado pela administração vira uma conta.… (+5 more)

### Community 41 - "PagamentoDAO"
Cohesion: 0.07
Nodes (30): mensalidade_destaque(), PagamentoDAO, Status como o painel deve LER, com o vencimento aplicado na própria consulta. A…, Carrega aluno e plano junto das mensalidades. O template do painel lê…, Lista completa (sem paginar). Mantida para relatórios e testes., Uma página de mensalidades, recortada pelo banco (LIMIT/OFFSET). O painel…, Totais do painel financeiro - sempre calculados no backend a partir do banco,…, Escolhe a mensalidade mais relevante para o card 'Minha mensalidade': a mais… (+22 more)

### Community 42 - "pagamento_polling.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 43 - "mercado_pago_conta.py"
Cohesion: 0.09
Nodes (39): access_token_vigente(), _agora(), ambiente_da_conexao(), _cifrar(), _client_id(), _client_secret(), ConexaoIlegivel, _configuracao_do_aplicativo() (+31 more)

### Community 44 - "Pagamento"
Cohesion: 0.14
Nodes (9): cadastrar_pagamento(), Define o período coberto por uma mensalidade que ainda não tem um (lançamento…, Pagamento, Status a exibir, com o vencimento já aplicado. Uma cobrança `pendente` cujo…, parametrize, test_duas_requisicoes_pix_reutilizam_uma_cobranca_postgres(), Quem paga uma cobrança vencida há semanas tem de receber os 30 dias a partir da…, test_cobranca_antiga_quitada_hoje_abre_o_periodo_a_partir_de_hoje() (+1 more)

### Community 45 - "test_pix_rotas.py"
Cohesion: 0.20
Nodes (20): _agora_mercado_pago(), _assinar(), _resposta_consulta(), _resposta_criacao(), test_admin_tambem_pode_gerar_pix(), test_aluno_gera_pix_da_propria_mensalidade(), test_aluno_nao_acessa_mensalidade_de_outro_aluno(), test_falha_de_indisponibilidade_do_mp_retorna_503() (+12 more)

### Community 46 - "limit"
Cohesion: 0.16
Nodes (15): _aluno_por_token(), atualizar_dados_perfil(), confirmar_email(), _em_segundo_plano(), _enviar_em_segundo_plano(), limit, Roda `tarefa` fora da requisição, para o tempo de resposta não revelar nada. Em…, E-mail COM token (recuperação, confirmação): não pode ir para a `fila_email`. A… (+7 more)

### Community 47 - "d9e2f6a14c80_contatos_academia_perfis_professores.py"
Cohesion: 0.83
Nodes (3): _campos_professor(), downgrade(), upgrade()

### Community 49 - "test_conversao_home.py"
Cohesion: 0.19
Nodes (14): _body_tag(), _html(), parametrize, Conversão na home: perguntas frequentes, CTA fixo no celular e página de…, test_admin_logado_nao_ve_o_cta_fixo(), test_aluno_logado_nao_ve_o_cta_fixo(), test_cta_fixo_fica_so_na_home(), test_cta_fixo_sem_whatsapp_so_tem_o_cadastro() (+6 more)

### Community 50 - "botao_ocupado.test.cjs"
Cohesion: 0.18
Nodes (7): assert, criarElemento(), fs, montar(), path, test, vm

### Community 51 - "test_seguranca.py"
Cohesion: 0.09
Nodes (20): test_upload_de_arquivo_disfarcado_e_recusado(), _cadastro_publico(), _imagem_jpeg(), _mensagem_da_resposta(), O ramo "par existe" não pode pagar a ida ao provedor dentro da requisição., Cadastro novo, CPF existente e e-mail existente respondem com a MESMA tela., Quem ainda controla a caixa antiga não pode assumir a conta depois da troca., test_cabecalhos_de_seguranca() (+12 more)

### Community 52 - "checkout_abertura.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 55 - "gunicorn.conf.py"
Cohesion: 0.25
Nodes (9): post_worker_init(), Hooks carregados pelo Gunicorn; nunca executados por flask db upgrade., worker_exit(), iniciar(), _laco(), parar(), Aciona a fila periodicamente durante a vida de um worker Gunicorn. Importar…, Inicia uma vez por processo, depois de carregar a aplicação e migrar o banco. (+1 more)

### Community 56 - "PagamentoEvento"
Cohesion: 0.09
Nodes (17): criar_pix_mensalidade(), _processar_status_mp(), limitar_criacao_pagamento, Fonte unica de aprovacao, usada pelo webhook, pelo polling de status e pela…, A recusa (criada em `criada_em`, UTC) é de antes da última nova tentativa? Sem…, Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.…, Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda. O…, Abre o período de acesso no momento em que o pagamento é confirmado. Se a… (+9 more)

### Community 57 - "fila_email.py"
Cohesion: 0.06
Nodes (40): EmailPendente, espera_da_proxima_tentativa(), Fila de e-mails no banco. Aviso e cobrança coletivos saíam um a um dentro da…, contar_falhados(), contar_pendentes(), disparar(), enfileirar(), enfileirar_transacional() (+32 more)

### Community 58 - "test_migracao_cadastro_administrativo.py"
Cohesion: 0.40
Nodes (3): banco_antigo(), fixture, Verifica a migração em um banco isolado com o schema anterior e dados.

### Community 59 - "salvar_foto_perfil"
Cohesion: 0.18
Nodes (18): ArquivoInvalido, caminho_arquivo(), _conferir_dimensoes(), _detectar_tipo_imagem_real(), ImagemGrandeDemais, _pasta(), Exception, _raiz_uploads() (+10 more)

### Community 60 - "test_keep_alive.py"
Cohesion: 0.16
Nodes (7): ambiente_limpo(), fixture, parametrize, Garante que o keep-alive fica desligado por padrão e só pinga a própria origem., test_intervalo_fica_dentro_da_faixa(), test_nao_liga_com_valor_negativo(), test_ping_so_considera_200_como_sucesso()

### Community 62 - "mercado_pago.py"
Cohesion: 0.12
Nodes (27): _base_url_opcional(), base_url_publica(), criar_pagamento_pix(), criar_preferencia_checkout(), _erro_menciona(), _erro_menciona_expiracao(), _extrair_dados_pix(), _normalizar_pagamento() (+19 more)

### Community 63 - "test_arranque_seguranca.py"
Cohesion: 0.22
Nodes (14): _env_arranque(), Validações feitas por servidor.py no arranque (COOKIE_SECURE, TRUSTED_HOSTS,…, `python -m servicos.credenciais`: o hash sai entre aspas simples. O hash do…, Desenvolvimento local sem HTTPS (sem Caddy) não pode ficar travado., _rodar(), test_arranque_falha_com_cookie_secure_false_e_app_base_url_https(), test_arranque_falha_com_cookie_secure_invalido(), test_arranque_falha_sem_trusted_hosts() (+6 more)

### Community 64 - "Aluno"
Cohesion: 0.08
Nodes (17): _convidar_cadastro_existente(), _convidar_cadastro_existente_por_id(), Cadastro administrativo que alguém tentou recriar pelo formulário público. Em…, Versão para thread de fundo: a sessão da requisição não vale fora dela., Matrícula feita no balcão: sem login, sem senha e sem convite de acesso. Nasce…, Aluno, Se existe uma conta de acesso, e não se o aluno está em dia ou matriculado.…, Convite de acesso já enviado e ainda não usado (a validade é checada na rota). (+9 more)

### Community 66 - "turma_bp.py"
Cohesion: 0.13
Nodes (27): _acesso_permitido(), _acesso_permitido(), desmatricular_aluno(), detalhe_turma(), editar_professor(), foto_professor(), matricular_aluno(), painel_professor() (+19 more)

### Community 67 - "servidor.py"
Cohesion: 0.18
Nodes (15): after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., context_processor, errorhandler, acesso_negado(), adicionar_cabecalhos_de_seguranca(), contatos_da_academia(), erro_csrf() (+7 more)

### Community 69 - "mercado_pago_oauth_bp.py"
Cohesion: 0.36
Nodes (9): _autorizacao_valida(), callback(), conectar(), desconectar(), limit, route, O state devolvido é o que ESTA sessão emitiu, há pouco tempo?, Só monta o state/PKCE na sessão e manda o administrador ao Mercado Pago. É um… (+1 more)

### Community 70 - "test_admin_mercado_pago.py"
Cohesion: 0.21
Nodes (13): Nome legível da forma de pagamento. Antes as telas usavam `|replace('_','…, rotulo_forma_pagamento(), _aprovado_no_checkout(), Painel do admin com mensalidades do Mercado Pago: formas de pagamento,…, Cartão/boleto: a preferência existe, o webhook ainda não trouxe o payment_id., _so_com_checkout(), test_ficha_mantem_no_select_a_forma_confirmada_pelo_mercado_pago(), test_rotulos_das_formas_do_mercado_pago() (+5 more)

### Community 71 - "pagina_login"
Cohesion: 0.12
Nodes (15): pagina_login(), admin_configurado(), comparar_em_tempo_constante(), credencial_admin_confere(), gerar_hash_admin(), _main(), Credencial administrativa baseada exclusivamente em hash de senha. O…, Compara duas senhas em tempo constante, sem restrição de alfabeto. Codificar… (+7 more)

### Community 72 - "shot.mjs"
Cohesion: 0.29
Nodes (5): { chromium }, contextos, CREDS, jobs, require

### Community 73 - "Componentes"
Cohesion: 0.05
Nodes (36): Altura de controle, Avisos flutuantes, Botões — `.et-botao` + variante (+ tamanho), Cartões e contêineres, Componentes, Contêiner e estrutura, Cores, Dados (+28 more)

### Community 74 - "google_login.py"
Cohesion: 0.29
Nodes (9): callback(), login_google(), limit, route, redirect_uri(), iniciar_sessao(), Grava na sessão atual a credencial em vigor (login ou troca de senha bem-…, Dá um identificador à sessão recém-aberta, para o logout poder revogá-la.… (+1 more)

### Community 76 - "Pagina"
Cohesion: 0.14
Nodes (5): Pagina, Uma fatia de resultados já recortada pelo banco, com o que a navegação precisa., Uma página existe mesmo quando está vazia. Sem isto, `__len__` fazia `{% if…, `__len__` fazia `{% if pagina %}` ser falso numa página sem itens, escondendo…, test_pagina_vazia_ainda_mostra_a_navegacao()

### Community 77 - "analytics.test.cjs"
Cohesion: 0.18
Nodes (7): assert, CODIGO, Element, fs, path, test, vm

### Community 81 - "Contrato do redesign — SistemaEXTREMETEAM"
Cohesion: 0.09
Nodes (20): 0. Antes de escrever código, 1. Identidade visual (design tokens), 2. Logo oficial (usar SOMENTE a logo original), 3. Telas a implementar, 4. Regras e dados, 5. Forma de trabalhar, Painel administrativo (desktop, sidebar preta com o emblema do dragão), Prompt para o Claude Code — Redesign do SistemaEXTREMETEAM (+12 more)

### Community 82 - "conftest.py"
Cohesion: 0.27
Nodes (11): app(), client(), contexto_app(), limpar_banco(), logar_como_professor(), plano(), fixture, Substitui o provedor de e-mail em todos os módulos que o chamam. A suíte nunca… (+3 more)

### Community 83 - "test_sessao_revogada.py"
Cohesion: 0.24
Nodes (11): Sessões encerradas pelo logout. A sessão do Flask é um cookie assinado, sem…, SessaoRevogada, _cliente_com_cookie(), _entrar_como_admin(), `session.clear()` só limpava o navegador de quem saiu; a cópia do cookie seguia…, test_logout_apaga_revogacoes_vencidas(), test_logout_de_uma_sessao_nao_derruba_as_outras(), test_logout_revoga_a_copia_do_cookie_feita_antes() (+3 more)

### Community 84 - "Skills Disponíveis"
Cohesion: 0.22
Nodes (8): Assistente e Automação (Antigravity), Ciências e Bioinformática (Plugins de Ciência), Dados e Google Cloud Platform (GCP), Desenvolvimento Mobile e Flutter/Dart, Desenvolvimento Web e Frontend, Firebase e Backend, GenAI e Machine Learning, Skills Disponíveis

### Community 85 - "componentes.js"
Cohesion: 0.22
Nodes (7): abrir(), agendarSaida(), fecharMenu(), fecharToast(), limpar(), mostrarErro(), prepararToast()

### Community 86 - "test_paginas_erro.py"
Cohesion: 0.17
Nodes (6): erro_interno(), csrf_ligado(), fixture, Página de erro (templates/erro.html) e os handlers de 404, 403, 500 e CSRF., test_404_para_quem_esta_logado_leva_a_area_dele(), test_500_mostra_a_pagina_de_erro()

### Community 89 - "analytics.js"
Cohesion: 0.28
Nodes (4): apagarCookiesGa(), carregar(), origemDoReferrer(), revogar()

### Community 90 - "Relatório de segurança — Sistema Extreme Team"
Cohesion: 0.29
Nodes (6): Controles verificados, Histórico de auditorias, Pendências não relacionadas a segurança, Relatório de segurança — Sistema Extreme Team, Situação atual (22/09/2026 — 2ª rodada), Validação executada em 22/09/2026

### Community 94 - "test_seo.py"
Cohesion: 0.13
Nodes (18): _head(), parametrize, SEO técnico: robots.txt, sitemap, títulos, meta tags, noindex e JSON-LD da home., _robots(), test_area_do_admin_sai_do_indice(), test_area_do_aluno_sai_do_indice(), test_area_do_professor_sai_do_indice(), test_canonical_ignora_query_string() (+10 more)

### Community 95 - "test_email_componentes.py"
Cohesion: 0.33
Nodes (7): E-mails: base com a logo oficial e componentes seguros para cliente de e-mail…, _render(), _sem_recursos_externos(), test_base_sem_url_publica_cai_para_o_nome_em_texto(), test_base_usa_a_logo_quando_ha_url_publica(), test_botao_do_email_usa_o_ouro_do_sistema(), test_cartao_de_resumo_com_badge()

### Community 96 - "test_checkout_rotas.py"
Cohesion: 0.18
Nodes (26): _assinar(), _pagamento_mp(), _preparar_retorno(), parametrize, Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala…, Pix aberto e checkout concluído ao mesmo tempo: a consulta pelo…, _resposta_preferencia(), test_json_nao_abre_cobranca_encerrada() (+18 more)

### Community 97 - "painel_adm"
Cohesion: 0.22
Nodes (5): painel_adm(), Apaga um plano que nunca foi usado. True, None (não existe) ou False (em uso)., Planos que algum registro referencia: mensalidade, cadastro de aluno ou pedido…, Quantos alunos a academia tem, sem filtro de busca. O card do topo do painel é…, test_plano_so_no_cadastro_do_aluno_tambem_conta_como_em_uso()

### Community 98 - "test_layouts.py"
Cohesion: 0.29
Nodes (8): _conferir_head_comum(), parametrize, Layouts base (templates/layouts/) e toasts. Cada página estende o layout da sua…, test_area_do_aluno_carrega_o_layout(), test_flash_de_erro_vira_toast_que_nao_some_sozinho(), test_paginas_publicas_carregam_o_head_comum(), test_painel_admin_carrega_o_layout_admin(), test_toda_pagina_estende_um_layout()

### Community 99 - "Academia"
Cohesion: 0.20
Nodes (10): Academia, parametrize, test_admin_salva_atualiza_e_limpa_contatos(), test_configuracoes_exigem_admin(), test_contatos_invalidos(), test_csrf_configuracoes(), test_erro_preserva_formulario_e_dados_salvos(), test_link_email_preserva_caracteres_do_endereco() (+2 more)

### Community 102 - "Flask App Service (compose)"
Cohesion: 0.22
Nodes (9): Flask App Service (compose), Postgres DB Service (compose), postgres_data Volume, Flask, Flask-SQLAlchemy, Gunicorn, psycopg2-binary, python-dotenv (+1 more)

### Community 103 - "enviar_aviso"
Cohesion: 0.16
Nodes (16): _chave_lote(), cobrar_inadimplentes(), cobrar_mensalidade(), enviar_aviso(), _esta_inadimplente(), _paragrafos_cobranca(), Situação de todos os alunos ativos com UMA consulta de mensalidades., Quem realmente deve receber cobrança: nem quem está com o plano ativo, nem quem… (+8 more)

### Community 104 - "Plano"
Cohesion: 0.18
Nodes (7): Plano, Preço de uma cobrança criada em `hoje`., Cadastrar Plano Form, plano_barato(), fixture, plano_barato(), fixture

### Community 106 - "Etapa 1 — migrar páginas para os layouts (SEM mudar o visual)"
Cohesion: 0.29
Nodes (6): Conferência (agentes Claude), Divisão, Etapa 1 — migrar páginas para os layouts (SEM mudar o visual), O que já existe (não edite), Receita por página, Relatório (curto)

### Community 107 - "Etapas 4 a 6 — aluno, admin, professor (aplicar os componentes nas páginas)"
Cohesion: 0.29
Nodes (6): Agente A — área do aluno + pagamento, Agente B — admin, Antigravity — financeiro, turmas, professor, Etapas 4 a 6 — aluno, admin, professor (aplicar os componentes nas páginas), Orquestrador (Claude), Regras para todos

### Community 108 - "seo_bp.py"
Cohesion: 0.67
Nodes (3): route, robots(), sitemap()

### Community 109 - "Etapa 2 — biblioteca de componentes"
Cohesion: 0.33
Nodes (5): Entregas e arquivos exclusivos, Etapa 2 — biblioteca de componentes, Ganchos de JS (Claude escreve `static/js/componentes.js`; markup e CSS usam EXATAMENTE isto), Macros (Agente A), cada uma no seu arquivo em `templates/components/`, Regras visuais (REDESIGN_CONTRATO.md seção 2 — leia)

### Community 110 - "Etapa 3 — home com os planos + termos"
Cohesion: 0.40
Nodes (4): Agente A — `templates/index.html` e `static/css/index.css`, Antigravity — `termos_de_servico.html`, `politica_privacidade.html`, `termos_responsabilidade.html` + `static/css/termos.css` (novo), Dados da home (Claude entrega em servidor.py — não edite), Etapa 3 — home com os planos + termos

### Community 111 - "test_prontidao.py"
Cohesion: 0.15
Nodes (3): banco_fora(), fixture, /health/pronto: 503 quando banco ou Redis caem, sem expor detalhe nem criar…

### Community 113 - "test_perfil_e_foto.py"
Cohesion: 0.17
Nodes (13): cadastrar_turma(), remover_turma(), TurmaDAO, Turma, Cadastrar Turma Form, test_escolher_plano_com_turma_cria_matricula(), test_turma_lotada_nao_vira_matricula_apos_pagamento(), _imagem_jpeg_valida() (+5 more)

### Community 115 - "editar_plano"
Cohesion: 0.15
Nodes (12): cadastrar_plano(), editar_plano(), _ler_plano(), _ler_promocao(), 80', '80.5', '80,50' ou '1.234,56' -> Decimal. None se vazio; ValueError se…, Nome, preço e duração do formulário de plano: `(campos, None)` ou `(None,…, Preço promocional e período: `(campos, None)` ou `(None, erro)`. Os três campos…, Nome, preço, duração e promoção. Vale para as cobranças criadas daqui em… (+4 more)

### Community 116 - "test_observabilidade.py"
Cohesion: 0.14
Nodes (20): before_breadcrumb(), before_send(), iniciar_sentry(), _limpar(), mascarar(), Rastreamento de erros opcional com Sentry. Sem `SENTRY_DSN`, nada é importado…, _evento(), fixture (+12 more)

### Community 117 - "usuario_bp.py"
Cohesion: 0.13
Nodes (31): _acesso_permitido_pagamento(), _aluno_da_sessao(), cadastro_obrigado(), _cadastro_recebido(), cancelar_mudanca_plano(), comprovante_mensalidade(), confirmar_presenca(), enviar_comprovante_manual_aluno() (+23 more)

### Community 118 - "PlanoDAO"
Cohesion: 0.14
Nodes (32): PlanoDAO, Os planos à venda: home, perfil do aluno e formulários de contratação., Tira o plano de venda. Devolve `(plano, pedidos_cancelados)`, ou None. Pedidos…, _pagar(), _plano(), _promocao(), parametrize, Plano fora de venda (arquivar/reativar/excluir), edição e promoção com período.… (+24 more)

### Community 119 - "test_backup_scripts.py"
Cohesion: 0.27
Nodes (11): ambiente(), _executavel(), fixture, Scripts de backup (tools/backup/): retenção, falha sem backup "pela metade" e a…, _rodar(), test_backup_gera_dump_e_uploads_e_aplica_a_retencao(), test_dump_ilegivel_nao_vira_backup(), test_restaurar_em_banco_descartavel_e_extrair_uploads() (+3 more)

### Community 120 - "revogar_sessao_atual"
Cohesion: 0.25
Nodes (8): exempt, Registra a sessão como encerrada: cópias antigas do cookie deixam de valer.…, revogar_sessao_atual(), health(), health_pronto(), home(), logout(), route

### Community 122 - "_json_ld"
Cohesion: 0.38
Nodes (7): _json_ld(), Nenhum campo do JSON-LD pode sair nulo, vazio ou só com espaços., _sem_vazios(), test_json_ld_completo_a_partir_da_academia(), test_json_ld_nao_deixa_texto_do_painel_fechar_o_script(), test_json_ld_omite_campos_vazios(), test_json_ld_sem_dados_da_academia_so_tem_o_basico()

### Community 123 - "erro_validacao_senha"
Cohesion: 0.16
Nodes (13): alterar_senha_perfil(), ativar_acesso(), Transforma um cadastro feito no balcão na conta do próprio aluno. Quem chega…, mascarar_email(), Mostra o bastante do e-mail para o dono se reconhecer, sem revelá-lo a…, _carregar_senhas_comuns(), erro_confirmacao_senha(), erro_validacao_senha() (+5 more)

### Community 124 - "pagina_cadastro"
Cohesion: 0.31
Nodes (11): cadastrar_aluno(), Matrícula feita pela administração, sem conta de acesso. Pede só o que…, pagina_cadastro(), cpf_valido(), data_nascimento_valida(), formatar_cpf(), formatar_telefone(), Valida os 11 dígitos do CPF, incluindo os dois verificadores. (+3 more)

### Community 126 - "Professor"
Cohesion: 0.10
Nodes (26): cadastrar_professor(), remover_professor(), ProfessorDAO, Professor, Cadastrar Professor Form, Hipótese: a foto continua acessível por URL depois de tirar a publicação., Hipótese: os contatos vazam na home antes de a publicação ser marcada., Sonda: a data vem da query string e é convertida sem tratamento. (+18 more)

### Community 127 - "adm_bp.py"
Cohesion: 0.11
Nodes (36): _aluno_do_cpf_ou_painel(), aprovar_aluno(), aprovar_comprovante_manual(), arquivar_plano(), ativar_aluno(), atualizar_status_pagamento(), cancelar_mudanca_plano_admin(), _data_do_form() (+28 more)

### Community 128 - "conteudo_home.py"
Cohesion: 0.50
Nodes (3): faq_estruturado(), Textos editáveis da página inicial: perguntas frequentes e prazos de…, JSON-LD FAQPage com exatamente as perguntas mostradas na página.

### Community 129 - "url_publica"
Cohesion: 0.26
Nodes (11): _destinatario_log(), enviar_email(), _logo_publica(), Endereço absoluto da logo horizontal para o cabeçalho do e-mail, ou None. O…, Envia e-mail transacional pela Gmail API. Retorna True/False; nunca lança., base_url_publica(), RuntimeError, Retorna a origem pública configurada, sem usar o cabeçalho Host da requisição. (+3 more)

### Community 130 - ".listar_paginado"
Cohesion: 0.17
Nodes (11): _paginar(), Aplica LIMIT/OFFSET e conta o total numa consulta separada e barata. A contagem…, _parece_busca_por_cpf(), O termo é um CPF, ou um pedaço dele, e não um nome que por acaso tem número?, Uma página de alunos já cadastrados, recortada e filtrada pelo banco. O painel…, Qualquer dígito no termo virava `CPF LIKE '%3%'` e devolvia a academia inteira., O CPF é guardado formatado; digitar só os números precisa encontrar mesmo assim., test_busca_do_admin_encontra_o_aluno_pelo_cpf_so_com_digitos() (+3 more)

### Community 131 - "admin_requerido"
Cohesion: 0.35
Nodes (8): callback(), conectar(), desconectar(), limit, route, _voltar(), gerenciar_turmas(), admin_requerido()

### Community 133 - "academia_bp.py"
Cohesion: 0.23
Nodes (10): configuracoes(), _pagina(), route, O administrador foi ao Mercado Pago e a autorização não voltou para cá? O state…, tentativa_sem_retorno(), link_email(), Normalização de contatos profissionais antes de montar links públicos., validar_email() (+2 more)

### Community 134 - "keep_alive.py"
Cohesion: 0.29
Nodes (9): iniciar(), _intervalo(), _laco(), _ligado(), parar(), _pingar(), Mantém a aplicação acordada em hospedagens que hibernam por inatividade. Uma…, Encerra o laço. Usado pelos testes; em produção a thread é daemon. (+1 more)

### Community 135 - "prontidao.py"
Cohesion: 0.43
Nodes (6): banco_responde(), _consultar_banco(), Verificação de prontidão (/health/pronto): o banco e o Redis respondem agora?…, None quando o limite de requisições não usa Redis (memory:// em…, redis_responde(), verificar()

### Community 136 - "capturar_emails"
Cohesion: 0.67
Nodes (3): capturar_emails(), fixture, Intercepta o envio e devolve os e-mails que teriam saído, com os links.

### Community 137 - "analytics.py"
Cohesion: 0.28
Nodes (7): analytics_ativo(), id_analytics(), marcar_conversao_cadastro(), Google Analytics 4 opcional, só em página pública e só com consentimento. Sem…, Chamada no arranque: um ID malformado derruba a subida, como as demais…, Esta resposta pode carregar o GA4? Visitante, página pública indexável ou…, validar_configuracao()

### Community 139 - "_tem_limite"
Cohesion: 0.25
Nodes (8): parametrize, Rotas que custam hash de senha, processamento de imagem ou sondagem de token., Limites declarados por decorador NAQUELA rota. `resolve_limits` não serve aqui:…, Guarda do teste acima: uma rota sem limite precisa ser reprovada por ele., _tem_limite(), test_o_detector_de_limite_realmente_discrimina(), test_rotas_caras_tem_limite_de_requisicoes(), test_sessao_aberta_perde_o_perfil_quando_a_conta_deixa_de_valer()

### Community 140 - "backup.sh"
Cohesion: 1.00
Nodes (3): registrar(), reter(), backup.sh script

### Community 141 - "_png_bomba"
Cohesion: 0.29
Nodes (7): _png_bomba(), Bomba de descompressão: arquivo minúsculo, imagem gigante. O PNG aqui tem 285…, PNG válido e altamente compressível: linhas zeradas, como uma bomba real., O teto de pixels vale para a FOTO, que é decodificada, não para o comprovante.…, test_comprovante_a4_escaneado_continua_sendo_aceito(), test_foto_de_perfil_mantem_o_teto_de_pixels(), test_png_com_pixels_demais_e_recusado_pelo_cabecalho()

### Community 144 - "test_financeiro_admin_painel.py"
Cohesion: 0.33
Nodes (5): test_busca_financeira_trata_curingas_como_texto(), test_painel_financeiro_busca_por_nome_do_aluno(), test_painel_financeiro_exige_admin(), test_painel_financeiro_filtra_por_status(), test_painel_financeiro_mostra_totais_do_backend()

### Community 145 - "_chave_da_conta"
Cohesion: 0.40
Nodes (5): _chave_da_conta(), Chave de limite por CONTA, caindo no IP só para quem não está autenticado. A…, Alunos atrás do mesmo IP (o Wi-Fi da academia) não dividem a cota., test_limite_de_upload_e_por_conta_e_nao_por_ip(), test_visitante_sem_sessao_ainda_e_limitado_por_ip()

## Knowledge Gaps
- **135 isolated node(s):** `Design`, `graphify`, `Visão geral`, `Marca`, `Superfícies claras` (+130 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **30 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PagamentoDAO` connect `PagamentoDAO` to `criar_pagamento`, `.listar_por_aluno`, `.buscar_por_id`, `criar_aluno`, `pix_bp.py`, `.efetivar_mudancas_por_prazo`, `test_financeiro_admin_painel.py`, `MercadoPagoIndisponivel`, `AlunoDAO`, `checkout_bp.py`, `config.py`, `test_admin_lanca_mensalidade_paga_no_cartao`, `test_auditoria_seguranca.py`, `impressao_credencial`, `Pagamento`, `test_pix_rotas.py`, `test_seguranca.py`, `PagamentoEvento`, `Aluno`, `test_admin_mercado_pago.py`, `conftest.py`, `test_checkout_rotas.py`, `ResultadoContratacao`, `enviar_aviso`, `PlanoDAO`, `pagina_cadastro`, `adm_bp.py`?**
  _High betweenness centrality (0.123) - this node is a cross-community bridge._
- **Why does `logar_como_admin()` connect `logar_como_admin` to `criar_pagamento`, `.listar_por_aluno`, `.buscar_por_id`, `criar_aluno`, `test_regressao_auditoria.py`, `test_analytics.py`, `test_financeiro_admin_painel.py`, `test_home_planos.py`, `AlunoDAO`, `MercadoPagoConexao`, `test_admin_lanca_mensalidade_paga_no_cartao`, `test_trocar_a_credencial_do_admin_encerra_a_sessao_administrativa`, `test_limites_pagamento.py`, `impressao_credencial`, `PagamentoDAO`, `test_pix_rotas.py`, `test_conversao_home.py`, `test_seguranca.py`, `Aluno`, `test_admin_mercado_pago.py`, `conftest.py`, `test_sessao_revogada.py`, `test_seo.py`, `test_layouts.py`, `Academia`, `test_perfil_e_foto.py`, `editar_plano`, `PlanoDAO`, `Professor`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Why does `criar_aluno()` connect `criar_aluno` to `criar_pagamento`, `.listar_paginado`, `.listar_por_aluno`, `.buscar_por_id`, `test_regressao_auditoria.py`, `logar_como_admin`, `test_analytics.py`, `_tem_limite`, `test_financeiro_admin_painel.py`, `test_home_planos.py`, `AlunoDAO`, `_chave_da_conta`, `test_admin_lanca_mensalidade_paga_no_cartao`, `test_limite_atingido_nao_mostra_login_a_quem_ja_entrou`, `test_sessao_sem_carimbo_de_credencial_e_recusada`, `test_auditoria_seguranca.py`, `test_limites_pagamento.py`, `impressao_credencial`, `test_login_de_aluno_nao_paga_o_hash_do_admin`, `PagamentoDAO`, `Pagamento`, `test_pix_rotas.py`, `test_conversao_home.py`, `test_seguranca.py`, `PagamentoEvento`, `Aluno`, `pagina_login`, `conftest.py`, `test_paginas_erro.py`, `test_seo.py`, `painel_adm`, `test_layouts.py`, `test_perfil_e_foto.py`, `editar_plano`, `PlanoDAO`, `Professor`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Are the 143 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 143 INFERRED edges - model-reasoned connections that need verification._
- **Are the 157 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 157 INFERRED edges - model-reasoned connections that need verification._
- **Are the 155 inferred relationships involving `criar_pagamento()` (e.g. with `PagamentoDAO` and `Pagamento`) actually correct?**
  _`criar_pagamento()` has 155 INFERRED edges - model-reasoned connections that need verification._
- **Are the 152 inferred relationships involving `logar_como_admin()` (e.g. with `test_admin_salva_atualiza_e_limpa_contatos()` and `test_csrf_configuracoes()`) actually correct?**
  _`logar_como_admin()` has 152 INFERRED edges - model-reasoned connections that need verification._