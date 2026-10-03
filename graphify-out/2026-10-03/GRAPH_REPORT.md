# Graph Report - SistemaEXTREMETEAM  (2026-09-30)

## Corpus Check
- 170 files · ~229,914 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2259 nodes · 5663 edges · 141 communities (129 shown, 12 thin omitted)
- Extraction: 80% EXTRACTED · 20% INFERRED · 0% AMBIGUOUS · INFERRED: 1132 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `77be81f9`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- criar_pagamento
- extreme.css
- planos.py
- criar_aluno
- test_pagamento_recusado.py
- test_mudanca_plano.py
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
- test_mercado_pago_oauth_postgres.py
- AlunoDAO
- test_mercado_pago_oauth.py
- checkout_bp.py
- pix.js
- config.py
- env.py
- pagamento.js
- c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py
- varredura.mjs
- 896e70afc9c5_adiciona_foto_e_graduacao_do_aluno_.py
- test_auditoria_seguranca.py
- test_fila_email_concorrencia_postgres.py
- test_limites_pagamento.py
- MatriculaDAO
- gmail_conta.py
- convites.py
- PagamentoDAO
- pagamento_polling.test.cjs
- mercado_pago_conta.py
- .status_efetivo
- test_pix_rotas.py
- EmailPendente
- d9e2f6a14c80_contatos_academia_perfis_professores.py
- test_conversao_home.py
- botao_ocupado.test.cjs
- test_seguranca.py
- checkout_abertura.test.cjs
- filtros_financeiro.js
- gunicorn.conf.py
- .contratar_plano
- fila_email.py
- test_migracao_cadastro_administrativo.py
- salvar_foto_perfil
- test_keep_alive.py
- _FakePaymentResource
- MercadoPagoIndisponivel
- test_arranque_seguranca.py
- Aluno
- autorizacao.py
- servidor.py
- ConfiguracaoInvalida
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
- .buscar_por_id
- painel_adm
- test_layouts.py
- Academia
- disparar
- Flask App Service (compose)
- parametrize
- enfileirar_transacional
- Etapa 1 — migrar páginas para os layouts (SEM mudar o visual)
- Etapas 4 a 6 — aluno, admin, professor (aplicar os componentes nas páginas)
- seo_bp.py
- Etapa 2 — biblioteca de componentes
- Etapa 3 — home com os planos + termos
- test_prontidao.py
- test_perfil_e_foto.py
- Plano
- test_observabilidade.py
- usuario_bp.py
- PlanoDAO
- test_backup_scripts.py
- .__init__
- gerar_imagem_og.py
- route
- erro_validacao_senha
- pagina_cadastro
- Professor
- adm_bp.py
- conteudo_home.py
- email.py
- turma_bp.py
- academia_bp.py
- URLPublicaInvalida
- prontidao.py
- capturar_emails
- backup.sh
- test_financeiro_admin_painel.py
- agendar.sh
- restaurar.sh

## God Nodes (most connected - your core abstractions)
1. `PagamentoDAO` - 228 edges
2. `criar_aluno()` - 159 edges
3. `criar_pagamento()` - 157 edges
4. `logar_como_admin()` - 154 edges
5. `logar_como_aluno()` - 135 edges
6. `AlunoDAO` - 94 edges
7. `PlanoDAO` - 69 edges
8. `Aluno` - 64 edges
9. `Professor` - 44 edges
10. `MercadoPagoIndisponivel` - 43 edges

## Surprising Connections (you probably didn't know these)
- `Planos Disponíveis Section` --shares_data_with--> `Plano`  [INFERRED]
  templates/pgUsuario.html → modelos/plano.py
- `Histórico de Mensalidades Section` --shares_data_with--> `Pagamento`  [INFERRED]
  templates/pgUsuario.html → modelos/pagamento.py
- `Presença Form` --shares_data_with--> `Presenca`  [INFERRED]
  templates/turma.html → modelos/presenca.py
- `Turma Detail Page` --shares_data_with--> `Turma`  [INFERRED]
  templates/turma.html → modelos/turma.py
- `Cadastrar Turma Form` --shares_data_with--> `Turma`  [INFERRED]
  templates/turmas.html → modelos/turma.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Shared Confirmation Modal Pattern** — templates_components_confirm_modal_dialog, templates_pgadm_page, templates_pgprofessor_page, templates_pgusuario_page, templates_turmas_page [EXTRACTED 1.00]
- **Mensalidade (Billing) Management Flow** — templates_dt_aluno_pagamento_form, templates_pgusuario_mensalidades_section, modelos_pagamento_pagamento, modelos_plano_plano [INFERRED 0.85]
- **Turma and Attendance Management Flow** — templates_turmas_turma_form, templates_turma_presenca_form, templates_pgprofessor_page, modelos_turma_turma [INFERRED 0.85]

## Communities (141 total, 12 thin omitted)

### Community 0 - "criar_pagamento"
Cohesion: 0.11
Nodes (51): criar_pagamento(), logar_como_aluno(), Hipótese: forjar ?status=approved na volta do MP quita a mensalidade., test_retorno_ignora_status_aprovado_da_query_string(), _mockar_preferencia(), parametrize, Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala…, Um boleto pendente do Checkout Pro grava provider_payment_id, mas não é Pix:… (+43 more)

### Community 1 - "extreme.css"
Cohesion: 0.05
Nodes (34): abrirmodal(), fechar(), icone_senha, input_senha, modal, mostrarSenha(), campoDuracao, campoPreco (+26 more)

### Community 2 - "planos.py"
Cohesion: 0.06
Nodes (42): cadeia_paga(), cartao_do_plano(), cobranca_a_pagar(), cobranca_em_decisao(), cobranca_pendente(), duracao_dias(), _duracao_por_extenso(), esta_inadimplente() (+34 more)

### Community 3 - "criar_aluno"
Cohesion: 0.13
Nodes (36): criar_aluno(), parametrize, test_admin_lanca_mensalidade_paga_no_cartao(), test_escolher_plano_cria_mensalidade_e_redireciona_para_pix(), test_plano_invalido_nao_cria_mensalidade(), test_reenvio_da_contratacao_reutiliza_mensalidade(), test_valor_enviado_pelo_navegador_e_ignorado(), _pagar() (+28 more)

### Community 4 - "test_pagamento_recusado.py"
Cohesion: 0.28
Nodes (20): _assinar(), _data_mp(), _eventos(), _mockar_mp(), _pagamento_mp(), _pix_criado(), Mensalidade recusada: a próxima tentativa do aluno a reabre, e a recusa antiga…, Mensalidade cujo cartão acabou de ser recusado no Checkout Pro. (+12 more)

### Community 5 - "test_mudanca_plano.py"
Cohesion: 0.14
Nodes (28): detalhes_usuario(), Persistência dos pedidos de troca de plano agendados para a próxima renovação., Aplica um pedido agendado cujo período de origem já terminou sem renovação.…, SolicitacaoPlanoDAO, _agendar(), _pagar(), plano_barato(), fixture (+20 more)

### Community 6 - "pix_bp.py"
Cohesion: 0.09
Nodes (36): _acesso_permitido(), criar_pix_mensalidade(), _data_da_aprovacao(), _forma_pagamento_confirmada(), _instante_utc(), _iso_utc(), _pagamento_mp_mais_relevante(), _pagamento_ou_none() (+28 more)

### Community 7 - "test_regressao_auditoria.py"
Cohesion: 0.04
Nodes (57): _chave_da_conta(), Chave de limite por CONTA, caindo no IP só para quem não está autenticado. A…, Uma página de alunos já cadastrados, recortada e filtrada pelo banco. O painel…, _contar_selects_em_alunos(), _credencial(), parametrize, Regressões da auditoria de segurança, desempenho e confiabilidade. Cada caso…, Head-of-line blocking: a primeira linha falhando não pode impedir as seguintes.… (+49 more)

### Community 9 - "test_mercado_pago_servico.py"
Cohesion: 0.09
Nodes (35): Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, validar_assinatura_webhook(), Hipótese: uma notificação capturada ontem pode ser reenviada hoje., `ts=nan` fazia a comparação da janela dar False e passava pela checagem de…, test_webhook_recusa_assinatura_antiga(), test_webhook_recusa_ts_nao_numerico_finito(), base_url(), _criar_preferencia() (+27 more)

### Community 10 - "logar_como_admin"
Cohesion: 0.09
Nodes (32): logar_como_admin(), test_convite_recusado_para_quem_ja_tem_acesso(), _preparar_state(), parametrize, test_aviso_de_autorizacao_vencida_aparece_uma_vez(), test_cada_conexao_iniciada_usa_state_novo(), test_callback_cancelado_no_mercado_pago_consome_o_state(), test_callback_com_erro_do_mercado_pago_que_nao_e_cancelamento() (+24 more)

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
Cohesion: 0.18
Nodes (17): Marca o plano em destaque da página inicial, desmarcando qualquer outro.…, Inclusive os arquivados: serve a quem olha o histórico (filtro do financeiro)., Planos da página inicial, prontos para `components/cartao_plano.html`. O preço…, vitrine_planos(), _plano(), _quatro_planos(), Planos na página inicial: cálculo (servicos/planos.vitrine_planos), destaque…, test_admin_destaca_e_tira_o_destaque() (+9 more)

### Community 17 - "test_mercado_pago_oauth_postgres.py"
Cohesion: 0.18
Nodes (8): postgres_mp(), fixture, Renovação do token OAuth com trava de linha real, opcional na suíte que usa…, _Resposta, test_dois_processos_perto_do_vencimento_gastam_o_refresh_token_uma_vez(), _migracao(), test_migracao_cria_a_tabela_igual_ao_modelo_e_e_reentrante(), test_migracao_encadeia_na_ultima_revisao_existente()

### Community 18 - "AlunoDAO"
Cohesion: 0.15
Nodes (39): AlunoDAO, _matricular(), Cadastro de aluno pela administração, ativação de acesso e confirmação de…, test_admin_lanca_e_baixa_mensalidade_de_aluno_sem_acesso(), test_admin_matricula_aluno_sem_email_senha_nem_acesso(), test_admin_pode_deixar_cadastro_de_balcao_sem_usuario_e_sem_email(), test_admin_rejeita_status_financeiro_desconhecido(), test_admin_rejeita_valor_financeiro_invalido() (+31 more)

### Community 19 - "test_mercado_pago_oauth.py"
Cohesion: 0.09
Nodes (45): MercadoPagoConexao, Conta do Mercado Pago que a academia autorizou por OAuth. Uma linha só (a…, _agora(), _ajustar(), api_mp(), _conectar(), _dados_conexao(), oauth_env() (+37 more)

### Community 20 - "checkout_bp.py"
Cohesion: 0.09
Nodes (28): abrir_checkout(), _acesso_permitido(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), limitar_consulta_pagamento, limitar_criacao_pagamento, route (+20 more)

### Community 21 - "pix.js"
Cohesion: 0.33
Nodes (14): abrirPix(), alvoDoRotulo(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), liberarBotao(), limparConteudoAnterior() (+6 more)

### Community 22 - "config.py"
Cohesion: 0.15
Nodes (12): _paginar(), Aplica LIMIT/OFFSET e conta o total numa consulta separada e barata. A contagem…, Decimal, Pedido de troca de plano agendado para a próxima renovação. Nunca altera o…, SolicitacaoMudancaPlano, postgres_pix(), fixture, Regressão com trava de linha real, opcional na suíte que usa SQLite. Execute… (+4 more)

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
Nodes (46): _assinar(), _pagamento_mp(), _preparar_para_conciliacao(), parametrize, Auditoria de segurança: sondas escritas para TENTAR quebrar as regras. Nenhum…, Hipótese: a sessão de professor é aceita nas rotas financeiras do aluno., Hipótese: como o JS agora usa fetch, o POST perdeu a exigência de CSRF., Hipótese: as demais rotas de dinheiro aceitam POST sem token. (+38 more)

### Community 34 - "test_fila_email_concorrencia_postgres.py"
Cohesion: 0.18
Nodes (10): _enfileirar_em_transacao_propria(), postgres_fila(), fixture, Idempotência da fila de e-mail sob concorrência real, em PostgreSQL…, A recusa de uma chave repetida não pode desfazer o lote inteiro. Um…, A trava do lote precisa valer até o fim do lote. Comitar linha a linha…, Enfileira e comita numa sessão própria, como faria outra requisição., test_chave_duplicada_nao_descarta_os_outros_destinatarios_do_lote() (+2 more)

### Community 35 - "test_limites_pagamento.py"
Cohesion: 0.15
Nodes (15): consultar_mp(), fixture, parametrize, Limites de pagamento por conta, com o provedor inteiramente simulado., _sessao_aluno(), test_admin_limite_por_usuario_persiste_entre_sessoes(), test_alunos_no_mesmo_ip_tem_limites_separados(), test_anonimos_limitados_por_ip_sem_consultar_provedor() (+7 more)

### Community 36 - "MatriculaDAO"
Cohesion: 0.16
Nodes (19): MatriculaDAO, Matricula, Presenca, impressao_credencial(), Resumo curto e não reversível do hash da senha, guardado na sessão. Nunca é a…, Valor que representa a credencial administrativa em vigor, ou None se não há…, referencia_credencial_admin(), parametrize (+11 more)

### Community 37 - "gmail_conta.py"
Cohesion: 0.16
Nodes (18): GmailConexao, _access_token(), _cifrar(), _client_id(), _client_secret(), _decifrar(), enviar(), estado() (+10 more)

### Community 38 - "convites.py"
Cohesion: 0.19
Nodes (13): aluno_do_token(), ConviteIndisponivel, descartar(), enviar(), gerar_token(), _hash(), RuntimeError, Convite de acesso: como um cadastro criado pela administração vira uma conta.… (+5 more)

### Community 41 - "PagamentoDAO"
Cohesion: 0.10
Nodes (24): PagamentoDAO, Status como o painel deve LER, com o vencimento aplicado na própria consulta. A…, Carrega aluno e plano junto das mensalidades. O template do painel lê…, Lista completa (sem paginar). Mantida para relatórios e testes., Uma página de mensalidades, recortada pelo banco (LIMIT/OFFSET). O painel…, Totais do painel financeiro - sempre calculados no backend a partir do banco,…, True se já existe um Pix ou um checkout válido emitido para esta cobrança.…, True se a cobrança Pix já gerada para este pagamento ainda pode ser… (+16 more)

### Community 42 - "pagamento_polling.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 43 - "mercado_pago_conta.py"
Cohesion: 0.09
Nodes (39): access_token_vigente(), _agora(), ambiente_da_conexao(), _cifrar(), _client_id(), _client_secret(), ConexaoIlegivel, _configuracao_do_aplicativo() (+31 more)

### Community 45 - "test_pix_rotas.py"
Cohesion: 0.22
Nodes (19): _agora_mercado_pago(), _assinar(), _resposta_consulta(), _resposta_criacao(), test_admin_tambem_pode_gerar_pix(), test_aluno_gera_pix_da_propria_mensalidade(), test_aluno_nao_acessa_mensalidade_de_outro_aluno(), test_impede_cobranca_duplicada_em_chamadas_consecutivas() (+11 more)

### Community 46 - "EmailPendente"
Cohesion: 0.25
Nodes (5): EmailPendente, parametrize, Agendamento sem rede, threads reais ou esperas de relógio., test_nao_inicia_em_testes(), test_retomada_de_item_persistido_e_retentativa_sem_painel()

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
Cohesion: 0.07
Nodes (25): test_upload_de_arquivo_disfarcado_e_recusado(), _cadastro_publico(), _imagem_jpeg(), _mensagem_da_resposta(), O `login` de um aluno pode ser o e-mail de outro; quem entra é decidido pela…, O ramo "par existe" não pode pagar a ida ao provedor dentro da requisição., Cadastro novo, CPF existente e e-mail existente respondem com a MESMA tela., Quem ainda controla a caixa antiga não pode assumir a conta depois da troca. (+17 more)

### Community 52 - "checkout_abertura.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 55 - "gunicorn.conf.py"
Cohesion: 0.25
Nodes (9): post_worker_init(), Hooks carregados pelo Gunicorn; nunca executados por flask db upgrade., worker_exit(), iniciar(), _laco(), parar(), Aciona a fila periodicamente durante a vida de um worker Gunicorn. Importar…, Inicia uma vez por processo, depois de carregar a aplicação e migrar o banco. (+1 more)

### Community 56 - ".contratar_plano"
Cohesion: 0.06
Nodes (22): Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.…, O que aconteceu numa tentativa de contratar/renovar/trocar de plano., Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda. O…, Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, Com uma troca já agendada, só dois planos fazem sentido num pedido de…, A cobrança do período seguinte tem de nascer no plano que o aluno agendou.…, `pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -… (+14 more)

### Community 57 - "fila_email.py"
Cohesion: 0.16
Nodes (14): espera_da_proxima_tentativa(), Fila de e-mails no banco. Aviso e cobrança coletivos saíam um a um dentro da…, contar_falhados(), contar_pendentes(), _entregar(), listar_pendentes(), processar_agora(), Processamento dos e-mails coletivos fora da requisição. O que muda em relação… (+6 more)

### Community 58 - "test_migracao_cadastro_administrativo.py"
Cohesion: 0.40
Nodes (3): banco_antigo(), fixture, Verifica a migração em um banco isolado com o schema anterior e dados.

### Community 59 - "salvar_foto_perfil"
Cohesion: 0.09
Nodes (33): enviar_comprovante_manual_aluno(), ArquivoInvalido, caminho_arquivo(), _conferir_dimensoes(), _detectar_tipo_imagem_real(), ImagemGrandeDemais, _pasta(), Exception (+25 more)

### Community 60 - "test_keep_alive.py"
Cohesion: 0.16
Nodes (7): ambiente_limpo(), fixture, parametrize, Garante que o keep-alive fica desligado por padrão e só pinga a própria origem., test_intervalo_fica_dentro_da_faixa(), test_nao_liga_com_valor_negativo(), test_ping_so_considera_200_como_sucesso()

### Community 62 - "MercadoPagoIndisponivel"
Cohesion: 0.09
Nodes (40): _base_url_opcional(), base_url_publica(), buscar_pagamento(), buscar_pagamentos_por_referencia(), cancelar_pagamento(), criar_pagamento_pix(), criar_preferencia_checkout(), _erro_menciona() (+32 more)

### Community 63 - "test_arranque_seguranca.py"
Cohesion: 0.22
Nodes (14): _env_arranque(), Validações feitas por servidor.py no arranque (COOKIE_SECURE, TRUSTED_HOSTS,…, `python -m servicos.credenciais`: o hash sai entre aspas simples. O hash do…, Desenvolvimento local sem HTTPS (sem Caddy) não pode ficar travado., _rodar(), test_arranque_falha_com_cookie_secure_false_e_app_base_url_https(), test_arranque_falha_com_cookie_secure_invalido(), test_arranque_falha_sem_trusted_hosts() (+6 more)

### Community 64 - "Aluno"
Cohesion: 0.08
Nodes (17): _convidar_cadastro_existente(), _convidar_cadastro_existente_por_id(), Cadastro administrativo que alguém tentou recriar pelo formulário público. Em…, Versão para thread de fundo: a sessão da requisição não vale fora dela., Matrícula feita no balcão: sem login, sem senha e sem convite de acesso. Nasce…, Aluno, Se existe uma conta de acesso, e não se o aluno está em dia ou matriculado.…, Convite de acesso já enviado e ainda não usado (a validade é checada na rota). (+9 more)

### Community 66 - "autorizacao.py"
Cohesion: 0.21
Nodes (15): foto_professor(), aluno_autorizado(), aluno_requerido(), _credencial_confere(), encerrar_sessao(), professor_autorizado(), Autorização das rotas protegidas. A sessão diz quem *afirmou* ser quem; quem…, A sessão foi emitida para a credencial que vale AGORA? Uma sessão sem carimbo é… (+7 more)

### Community 67 - "servidor.py"
Cohesion: 0.13
Nodes (22): after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, errorhandler, Registra a sessão como encerrada: cópias antigas do cookie deixam de valer.…, revogar_sessao_atual(), acesso_negado(), adicionar_cabecalhos_de_seguranca() (+14 more)

### Community 69 - "ConfiguracaoInvalida"
Cohesion: 0.30
Nodes (11): _autorizacao_valida(), callback(), conectar(), desconectar(), limit, route, O state devolvido é o que ESTA sessão emitiu, há pouco tempo?, Só monta o state/PKCE na sessão e manda o administrador ao Mercado Pago. É um… (+3 more)

### Community 70 - "test_admin_mercado_pago.py"
Cohesion: 0.15
Nodes (17): Nome legível da forma de pagamento. Antes as telas usavam `|replace('_','…, rotulo_forma_pagamento(), _aprovado_no_checkout(), Painel do admin com mensalidades do Mercado Pago: formas de pagamento,…, Cartão/boleto: a preferência existe, o webhook ainda não trouxe o payment_id., _so_com_checkout(), test_admin_muda_o_status_sem_perder_a_forma_do_mercado_pago(), test_admin_nao_grava_forma_inventada() (+9 more)

### Community 71 - "pagina_login"
Cohesion: 0.15
Nodes (14): pagina_login(), iniciar_sessao(), Dá um identificador à sessão recém-aberta, para o logout poder revogá-la.…, admin_configurado(), comparar_em_tempo_constante(), credencial_admin_confere(), gerar_hash_admin(), _main() (+6 more)

### Community 72 - "shot.mjs"
Cohesion: 0.29
Nodes (5): { chromium }, contextos, CREDS, jobs, require

### Community 73 - "Componentes"
Cohesion: 0.05
Nodes (36): Altura de controle, Avisos flutuantes, Botões — `.et-botao` + variante (+ tamanho), Cartões e contêineres, Componentes, Contêiner e estrutura, Cores, Dados (+28 more)

### Community 74 - "google_login.py"
Cohesion: 0.60
Nodes (5): callback(), login_google(), limit, route, redirect_uri()

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
Cohesion: 0.06
Nodes (50): analytics_ativo(), id_analytics(), marcar_conversao_cadastro(), Google Analytics 4 opcional, só em página pública e só com consentimento. Sem…, Chamada no arranque: um ID malformado derruba a subida, como as demais…, Esta resposta pode carregar o GA4? Visitante, página pública indexável ou…, validar_configuracao(), conteudo_robots() (+42 more)

### Community 95 - "test_email_componentes.py"
Cohesion: 0.33
Nodes (7): E-mails: base com a logo oficial e componentes seguros para cliente de e-mail…, _render(), _sem_recursos_externos(), test_base_sem_url_publica_cai_para_o_nome_em_texto(), test_base_usa_a_logo_quando_ha_url_publica(), test_botao_do_email_usa_o_ouro_do_sistema(), test_cartao_de_resumo_com_badge()

### Community 96 - ".buscar_por_id"
Cohesion: 0.16
Nodes (26): _assinar(), _pagamento_mp(), _preparar_retorno(), Pix aberto e checkout concluído ao mesmo tempo: a consulta pelo…, test_retorno_com_aprovacao_confirmada_marca_pago(), test_retorno_com_mp_indisponivel_avisa_sem_mudar_status(), test_retorno_de_boleto_avisa_sobre_o_prazo(), test_retorno_de_sucesso_nao_marca_pago_sem_confirmacao() (+18 more)

### Community 97 - "painel_adm"
Cohesion: 0.15
Nodes (7): painel_adm(), Apaga um plano que nunca foi usado. True, None (não existe) ou False (em uso)., Os planos à venda: home, perfil do aluno e formulários de contratação., Planos que algum registro referencia: mensalidade, cadastro de aluno ou pedido…, Quantos alunos a academia tem, sem filtro de busca. O card do topo do painel é…, home(), test_plano_so_no_cadastro_do_aluno_tambem_conta_como_em_uso()

### Community 98 - "test_layouts.py"
Cohesion: 0.29
Nodes (8): _conferir_head_comum(), parametrize, Layouts base (templates/layouts/) e toasts. Cada página estende o layout da sua…, test_area_do_aluno_carrega_o_layout(), test_flash_de_erro_vira_toast_que_nao_some_sozinho(), test_paginas_publicas_carregam_o_head_comum(), test_painel_admin_carrega_o_layout_admin(), test_toda_pagina_estende_um_layout()

### Community 99 - "Academia"
Cohesion: 0.14
Nodes (13): context_processor, Academia, link_email(), contatos_da_academia(), parametrize, test_admin_salva_atualiza_e_limpa_contatos(), test_configuracoes_exigem_admin(), test_contatos_invalidos() (+5 more)

### Community 100 - "disparar"
Cohesion: 0.29
Nodes (7): disparar(), _laco(), _liberar_e_retomar_se_preciso(), Drena a fila enquanto houver entrega acontecendo. Encerra na primeira passada…, Desregistra a thread e sobe outra se alguém pediu trabalho durante a queda. Sem…, Acorda o processamento em segundo plano, sem bloquear a requisição. Se a thread…, test_reaciona_fila_sem_requisicao_e_sobrevive_a_falha()

### Community 102 - "Flask App Service (compose)"
Cohesion: 0.22
Nodes (9): Flask App Service (compose), Postgres DB Service (compose), postgres_data Volume, Flask, Flask-SQLAlchemy, Gunicorn, psycopg2-binary, python-dotenv (+1 more)

### Community 103 - "parametrize"
Cohesion: 0.40
Nodes (5): parametrize, test_confirmacao_aceita_unicode(), test_matricula_valida_dados_no_servidor(), test_novos_formularios_exigem_csrf(), test_rotas_de_matricula_e_convite_sao_so_do_admin()

### Community 104 - "enfileirar_transacional"
Cohesion: 0.50
Nodes (4): enfileirar(), enfileirar_transacional(), E-mail transacional que NÃO carrega token, pela fila durável e fora da…, Registra um e-mail para envio. Devolve a linha criada, ou None se já existia.…

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
Cohesion: 0.15
Nodes (19): cadastrar_turma(), TurmaDAO, Turma, Sonda: a data vem da query string e é convertida sem tratamento., test_data_invalida_na_turma_nao_derruba_a_rota(), test_area_do_aluno_renderiza_telas_independentes_do_menu(), test_escolher_plano_com_turma_cria_matricula(), test_plano_atual_continua_disponivel_para_gerar_cobranca() (+11 more)

### Community 115 - "Plano"
Cohesion: 0.12
Nodes (12): cadastrar_plano(), _ler_plano(), _ler_promocao(), 80', '80.5', '80,50' ou '1.234,56' -> Decimal. None se vazio; ValueError se…, Nome, preço e duração do formulário de plano: `(campos, None)` ou `(None,…, Preço promocional e período: `(campos, None)` ou `(None, erro)`. Os três campos…, _valor_em_reais(), Plano (+4 more)

### Community 116 - "test_observabilidade.py"
Cohesion: 0.14
Nodes (20): before_breadcrumb(), before_send(), iniciar_sentry(), _limpar(), mascarar(), Rastreamento de erros opcional com Sentry. Sem `SENTRY_DSN`, nada é importado…, _evento(), fixture (+12 more)

### Community 117 - "usuario_bp.py"
Cohesion: 0.13
Nodes (30): _acesso_permitido_pagamento(), _aluno_da_sessao(), cadastro_obrigado(), cancelar_mudanca_plano(), comprovante_mensalidade(), confirmar_presenca(), enviar_foto_perfil(), foto_perfil() (+22 more)

### Community 118 - "PlanoDAO"
Cohesion: 0.12
Nodes (38): editar_plano(), Nome, preço, duração e promoção. Vale para as cobranças criadas daqui em…, reativar_plano(), PlanoDAO, Grava a edição do admin. Vale para as cobranças criadas daqui em diante: as…, Tira o plano de venda. Devolve `(plano, pedidos_cancelados)`, ou None. Pedidos…, Pagamento, _pagar() (+30 more)

### Community 119 - "test_backup_scripts.py"
Cohesion: 0.27
Nodes (11): ambiente(), _executavel(), fixture, Scripts de backup (tools/backup/): retenção, falha sem backup "pela metade" e a…, _rodar(), test_backup_gera_dump_e_uploads_e_aplica_a_retencao(), test_dump_ilegivel_nao_vira_backup(), test_restaurar_em_banco_descartavel_e_extrair_uploads() (+3 more)

### Community 123 - "erro_validacao_senha"
Cohesion: 0.10
Nodes (22): alterar_senha_perfil(), _aluno_por_token(), ativar_acesso(), confirmar_email(), Descarta todo link pendente que ainda autorizaria assumir ou redirecionar a…, Localiza o aluno pelo hash do token, filtrando no banco por uma coluna indexada., Transforma um cadastro feito no balcão na conta do próprio aluno. Quem chega…, redefinir_senha() (+14 more)

### Community 124 - "pagina_cadastro"
Cohesion: 0.12
Nodes (27): cadastrar_aluno(), Matrícula feita pela administração, sem conta de acesso. Pede só o que…, atualizar_dados_perfil(), _cadastro_recebido(), _em_segundo_plano(), _enviar_em_segundo_plano(), pagina_cadastro(), limit (+19 more)

### Community 126 - "Professor"
Cohesion: 0.09
Nodes (24): remover_professor(), ProfessorDAO, Professor, Cadastrar Professor Form, logar_como_professor(), fixture, Hipótese: a foto continua acessível por URL depois de tirar a publicação., Hipótese: os contatos vazam na home antes de a publicação ser marcada. (+16 more)

### Community 127 - "adm_bp.py"
Cohesion: 0.08
Nodes (50): _aluno_do_cpf_ou_painel(), aprovar_aluno(), aprovar_comprovante_manual(), arquivar_plano(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_pagamento(), cancelar_mudanca_plano_admin() (+42 more)

### Community 128 - "conteudo_home.py"
Cohesion: 0.50
Nodes (3): faq_estruturado(), Textos editáveis da página inicial: perguntas frequentes e prazos de…, JSON-LD FAQPage com exatamente as perguntas mostradas na página.

### Community 129 - "email.py"
Cohesion: 0.47
Nodes (5): _destinatario_log(), enviar_email(), _logo_publica(), Endereço absoluto da logo horizontal para o cabeçalho do e-mail, ou None. O…, Envia e-mail transacional pela Gmail API. Retorna True/False; nunca lança.

### Community 131 - "turma_bp.py"
Cohesion: 0.13
Nodes (21): callback(), conectar(), desconectar(), limit, route, _voltar(), _acesso_permitido(), cadastrar_professor() (+13 more)

### Community 133 - "academia_bp.py"
Cohesion: 0.32
Nodes (10): configuracoes(), _pagina(), route, O administrador foi ao Mercado Pago e a autorização não voltou para cá? O state…, tentativa_sem_retorno(), editar_professor(), Normalização de contatos profissionais antes de montar links públicos., validar_email() (+2 more)

### Community 134 - "URLPublicaInvalida"
Cohesion: 0.18
Nodes (16): back_urls absolutas para onde o Mercado Pago devolve o aluno. Os três destinos…, _urls_retorno(), iniciar(), _intervalo(), _laco(), _ligado(), parar(), _pingar() (+8 more)

### Community 135 - "prontidao.py"
Cohesion: 0.43
Nodes (6): banco_responde(), _consultar_banco(), Verificação de prontidão (/health/pronto): o banco e o Redis respondem agora?…, None quando o limite de requisições não usa Redis (memory:// em…, redis_responde(), verificar()

### Community 136 - "capturar_emails"
Cohesion: 0.67
Nodes (3): capturar_emails(), fixture, Intercepta o envio e devolve os e-mails que teriam saído, com os links.

### Community 140 - "backup.sh"
Cohesion: 1.00
Nodes (3): registrar(), reter(), backup.sh script

### Community 144 - "test_financeiro_admin_painel.py"
Cohesion: 0.33
Nodes (5): test_busca_financeira_trata_curingas_como_texto(), test_painel_financeiro_busca_por_nome_do_aluno(), test_painel_financeiro_exige_admin(), test_painel_financeiro_filtra_por_status(), test_painel_financeiro_mostra_totais_do_backend()

## Knowledge Gaps
- **135 isolated node(s):** `icone_senha`, `input_senha`, `modal`, `campoDuracao`, `campoPreco` (+130 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PagamentoDAO` connect `PagamentoDAO` to `criar_pagamento`, `criar_aluno`, `test_pagamento_recusado.py`, `test_mudanca_plano.py`, `pix_bp.py`, `test_regressao_auditoria.py`, `test_financeiro_admin_painel.py`, `AlunoDAO`, `checkout_bp.py`, `config.py`, `test_auditoria_seguranca.py`, `MatriculaDAO`, `test_pix_rotas.py`, `test_seguranca.py`, `.contratar_plano`, `salvar_foto_perfil`, `Aluno`, `test_admin_mercado_pago.py`, `conftest.py`, `.buscar_por_id`, `test_perfil_e_foto.py`, `usuario_bp.py`, `PlanoDAO`, `pagina_cadastro`, `adm_bp.py`?**
  _High betweenness centrality (0.125) - this node is a cross-community bridge._
- **Why does `logar_como_admin()` connect `logar_como_admin` to `criar_pagamento`, `criar_aluno`, `test_mudanca_plano.py`, `test_regressao_auditoria.py`, `test_analytics.py`, `test_financeiro_admin_painel.py`, `test_home_planos.py`, `AlunoDAO`, `test_mercado_pago_oauth.py`, `test_limites_pagamento.py`, `MatriculaDAO`, `PagamentoDAO`, `test_pix_rotas.py`, `test_conversao_home.py`, `test_seguranca.py`, `Aluno`, `test_admin_mercado_pago.py`, `conftest.py`, `test_sessao_revogada.py`, `test_seo.py`, `.buscar_por_id`, `test_layouts.py`, `Academia`, `parametrize`, `test_perfil_e_foto.py`, `Plano`, `PlanoDAO`, `Professor`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `AlunoDAO` connect `AlunoDAO` to `Aluno`, `painel_adm`, `turma_bp.py`, `criar_aluno`, `test_mudanca_plano.py`, `pagina_login`, `test_regressao_auditoria.py`, `PagamentoDAO`, `google_login.py`, `logar_como_admin`, `test_perfil_e_foto.py`, `conftest.py`, `test_seguranca.py`, `Plano`, `usuario_bp.py`, `config.py`, `pagina_cadastro`, `adm_bp.py`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Are the 157 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 157 INFERRED edges - model-reasoned connections that need verification._
- **Are the 157 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 157 INFERRED edges - model-reasoned connections that need verification._
- **Are the 155 inferred relationships involving `criar_pagamento()` (e.g. with `PagamentoDAO` and `Pagamento`) actually correct?**
  _`criar_pagamento()` has 155 INFERRED edges - model-reasoned connections that need verification._
- **Are the 152 inferred relationships involving `logar_como_admin()` (e.g. with `test_admin_salva_atualiza_e_limpa_contatos()` and `test_csrf_configuracoes()`) actually correct?**
  _`logar_como_admin()` has 152 INFERRED edges - model-reasoned connections that need verification._