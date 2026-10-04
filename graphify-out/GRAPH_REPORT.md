# Graph Report - SistemaEXTREMETEAM  (2026-10-04)

## Corpus Check
- 175 files · ~236,359 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2377 nodes · 5883 edges · 136 communities (127 shown, 9 thin omitted)
- Extraction: 81% EXTRACTED · 19% INFERRED · 0% AMBIGUOUS · INFERRED: 1141 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `35741178`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- logar_como_aluno
- extreme.css
- planos.py
- .listar_por_aluno
- test_pagamento_recusado.py
- test_mudanca_plano.py
- pix_bp.py
- criar_aluno
- SistemaEXTREMETEAM Project
- test_mercado_pago_servico.py
- fase3b.js
- test_analytics.py
- test_migracao_checkout.py
- checkout.js
- CLAUDE.md
- test_home_planos.py
- test_mercado_pago_oauth_postgres.py
- AlunoDAO
- logar_como_admin
- checkout_bp.py
- pix.js
- config.py
- env.py
- pagamento.js
- c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py
- varredura.mjs
- 896e70afc9c5_adiciona_foto_e_graduacao_do_aluno_.py
- test_auditoria_seguranca.py
- test_mercado_pago_oauth.py
- test_limites_requisicao.py
- MatriculaDAO
- gmail_conta.py
- .contratar_plano
- turma_bp.py
- pagamento_polling.test.cjs
- MercadoPagoIndisponivel
- admin_requerido
- criar_pagamento
- Plano
- d9e2f6a14c80_contatos_academia_perfis_professores.py
- botao_ocupado.test.cjs
- test_seguranca.py
- checkout_abertura.test.cjs
- filtros_financeiro.js
- gunicorn.conf.py
- PagamentoDAO
- fila_email.py
- test_migracao_cadastro_administrativo.py
- salvar_foto_perfil
- test_keep_alive.py
- test_google_login.py
- mercado_pago.py
- test_arranque_seguranca.py
- Aluno
- autorizacao.py
- servidor.py
- mercado_pago_oauth_bp.py
- test_admin_mercado_pago.py
- credenciais.py
- shot.mjs
- Componentes
- keep_alive.py
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
- test_layouts.py
- Flask App Service (compose)
- erro_validacao_senha
- Etapa 1 — migrar páginas para os layouts (SEM mudar o visual)
- Etapas 4 a 6 — aluno, admin, professor (aplicar os componentes nas páginas)
- seo_bp.py
- Etapa 2 — biblioteca de componentes
- Etapa 3 — home com os planos + termos
- test_prontidao.py
- test_perfil_e_foto.py
- PagamentoEvento
- test_observabilidade.py
- usuario_bp.py
- test_plano_arquivo_promocao.py
- test_backup_scripts.py
- google_login.py
- gerar_imagem_og.py
- revogar_sessao_atual
- pagina_cadastro
- PlanoDAO
- Professor
- adm_bp.py
- TransporteEmMemoria
- _aluno_por_token
- parametrize
- test_conversao_home.py
- URLPublicaInvalida
- prontidao.py
- capturar_emails
- backup.sh
- Biblioteca no Figma
- agendar.sh
- restaurar.sh

## God Nodes (most connected - your core abstractions)
1. `PagamentoDAO` - 228 edges
2. `criar_aluno()` - 164 edges
3. `criar_pagamento()` - 157 edges
4. `logar_como_admin()` - 155 edges
5. `logar_como_aluno()` - 135 edges
6. `AlunoDAO` - 93 edges
7. `PlanoDAO` - 69 edges
8. `Aluno` - 64 edges
9. `MercadoPagoIndisponivel` - 45 edges
10. `Professor` - 44 edges

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

## Communities (136 total, 9 thin omitted)

### Community 0 - "logar_como_aluno"
Cohesion: 0.12
Nodes (38): logar_como_aluno(), _mockar_preferencia(), parametrize, Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala…, Um boleto pendente do Checkout Pro grava provider_payment_id, mas não é Pix:…, _resposta_preferencia(), test_abertura_json_navega_sem_redirecionar_post_externo(), test_admin_tambem_pode_abrir_checkout() (+30 more)

### Community 1 - "extreme.css"
Cohesion: 0.05
Nodes (35): abrirmodal(), fechar(), icone_senha, input_senha, modal, mostrarSenha(), campoDuracao, campoPreco (+27 more)

### Community 2 - "planos.py"
Cohesion: 0.06
Nodes (42): cadeia_paga(), cartao_do_plano(), cobranca_a_pagar(), cobranca_em_decisao(), cobranca_pendente(), duracao_dias(), _duracao_por_extenso(), esta_inadimplente() (+34 more)

### Community 3 - ".listar_por_aluno"
Cohesion: 0.10
Nodes (34): parametrize, test_admin_lanca_mensalidade_paga_no_cartao(), test_escolher_plano_cria_mensalidade_e_redireciona_para_pix(), test_plano_invalido_nao_cria_mensalidade(), test_reenvio_da_contratacao_reutiliza_mensalidade(), test_valor_enviado_pelo_navegador_e_ignorado(), _pagar(), plano_barato() (+26 more)

### Community 4 - "test_pagamento_recusado.py"
Cohesion: 0.28
Nodes (20): _assinar(), _data_mp(), _eventos(), _mockar_mp(), _pagamento_mp(), _pix_criado(), Mensalidade recusada: a próxima tentativa do aluno a reabre, e a recusa antiga…, Mensalidade cujo cartão acabou de ser recusado no Checkout Pro. (+12 more)

### Community 5 - "test_mudanca_plano.py"
Cohesion: 0.17
Nodes (24): Persistência dos pedidos de troca de plano agendados para a próxima renovação., SolicitacaoPlanoDAO, _agendar(), _pagar(), plano_barato(), fixture, Mudança para um plano mais barato agendada para a próxima renovação. Regra…, O admin pode estornar/cancelar a mensalidade que sustentava a vigência depois… (+16 more)

### Community 6 - "pix_bp.py"
Cohesion: 0.07
Nodes (47): _acesso_permitido(), _chave_entrega_webhook(), criar_pix_mensalidade(), _data_da_aprovacao(), _forma_pagamento_confirmada(), _instante_utc(), _iso_utc(), _liberar_entrega_webhook() (+39 more)

### Community 7 - "criar_aluno"
Cohesion: 0.03
Nodes (79): _parece_busca_por_cpf(), O termo é um CPF, ou um pedaço dele, e não um nome que por acaso tem número?, Uma página de alunos já cadastrados, recortada e filtrada pelo banco. O painel…, criar_aluno(), test_aluno_existente_continua_entrando_normalmente(), test_area_do_aluno_renderiza_telas_independentes_do_menu(), test_plano_atual_continua_disponivel_para_gerar_cobranca(), test_busca_financeira_trata_curingas_como_texto() (+71 more)

### Community 9 - "test_mercado_pago_servico.py"
Cohesion: 0.09
Nodes (35): buscar_pagamentos_por_referencia(), Lista os pagamentos que o Mercado Pago associa a uma external_reference. Usada…, Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, validar_assinatura_webhook(), Hipótese: uma notificação capturada ontem pode ser reenviada hoje., `ts=nan` fazia a comparação da janela dar False e passava pela checagem de…, test_webhook_recusa_assinatura_antiga(), test_webhook_recusa_ts_nao_numerico_finito() (+27 more)

### Community 10 - "fase3b.js"
Cohesion: 0.06
Nodes (47): avisos, bind(), caixas, campos, col(), D(), estados, faixa (+39 more)

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
Cohesion: 0.20
Nodes (7): postgres_mp(), fixture, Renovação do token OAuth com trava de linha real, opcional na suíte que usa…, _Resposta, _migracao(), test_migracao_cria_a_tabela_igual_ao_modelo_e_e_reentrante(), test_migracao_encadeia_na_ultima_revisao_existente()

### Community 18 - "AlunoDAO"
Cohesion: 0.15
Nodes (38): AlunoDAO, _matricular(), Cadastro de aluno pela administração, ativação de acesso e confirmação de…, test_admin_lanca_e_baixa_mensalidade_de_aluno_sem_acesso(), test_admin_matricula_aluno_sem_email_senha_nem_acesso(), test_admin_pode_deixar_cadastro_de_balcao_sem_usuario_e_sem_email(), test_admin_rejeita_status_financeiro_desconhecido(), test_admin_rejeita_valor_financeiro_invalido() (+30 more)

### Community 19 - "logar_como_admin"
Cohesion: 0.13
Nodes (25): logar_como_admin(), test_admin_nao_pode_apagar_o_usuario_de_uma_conta_ativa(), test_convite_recusado_para_quem_ja_tem_acesso(), _preparar_state(), parametrize, test_aviso_de_autorizacao_vencida_aparece_uma_vez(), test_cada_conexao_iniciada_usa_state_novo(), test_callback_avisa_quando_a_conta_muda() (+17 more)

### Community 20 - "checkout_bp.py"
Cohesion: 0.08
Nodes (32): abrir_checkout(), _acesso_permitido(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), limitar_consulta_pagamento, limitar_criacao_pagamento, route (+24 more)

### Community 21 - "pix.js"
Cohesion: 0.33
Nodes (14): abrirPix(), alvoDoRotulo(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), liberarBotao(), limparConteudoAnterior() (+6 more)

### Community 22 - "config.py"
Cohesion: 0.14
Nodes (14): _paginar(), Aplica LIMIT/OFFSET e conta o total numa consulta separada e barata. A contagem…, Decimal, Matricula, _para_decimal(), Pedido de troca de plano agendado para a próxima renovação. Nunca altera o…, SolicitacaoMudancaPlano, postgres_pix() (+6 more)

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
Nodes (48): _agora_mercado_pago(), _assinar(), _pagamento_mp(), _preparar_para_conciliacao(), parametrize, Auditoria de segurança: sondas escritas para TENTAR quebrar as regras. Nenhum…, Hipótese: as rotas de cobrança respondem sem sessão nenhuma., Hipótese: a sessão de professor é aceita nas rotas financeiras do aluno. (+40 more)

### Community 34 - "test_mercado_pago_oauth.py"
Cohesion: 0.07
Nodes (52): MercadoPagoConexao, Conta do Mercado Pago que a academia autorizou por OAuth. Uma linha só (a…, _sdk(), _agora(), _ajustar(), api_mp(), _conectar(), _dados_conexao() (+44 more)

### Community 35 - "test_limites_requisicao.py"
Cohesion: 0.12
Nodes (28): consultar_mp(), _estourar(), fixture, parametrize, Limites de requisição da rodada de 04/10/2026 (SEC-10 a SEC-17 e SEC-19). Cada…, Trocar de rede ou abrir outra sessão não devolve a cota de e-mails em massa., Faz `limite` requisições sem nenhum 429 e devolve a seguinte., Alunos no mesmo Wi-Fi não dividem o teto padrão, nem com o visitante anônimo. (+20 more)

### Community 36 - "MatriculaDAO"
Cohesion: 0.19
Nodes (16): MatriculaDAO, Presenca, impressao_credencial(), Resumo curto e não reversível do hash da senha, guardado na sessão. Nunca é a…, Valor que representa a credencial administrativa em vigor, ou None se não há…, referencia_credencial_admin(), parametrize, test_aluno_confirma_sua_frequencia() (+8 more)

### Community 37 - "gmail_conta.py"
Cohesion: 0.16
Nodes (18): GmailConexao, _access_token(), _cifrar(), _client_id(), _client_secret(), _decifrar(), enviar(), estado() (+10 more)

### Community 38 - ".contratar_plano"
Cohesion: 0.10
Nodes (12): O que aconteceu numa tentativa de contratar/renovar/trocar de plano., Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda. O…, Aplica um pedido agendado cujo período de origem já terminou sem renovação.…, Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, Com uma troca já agendada, só dois planos fazem sentido num pedido de…, A cobrança do período seguinte tem de nascer no plano que o aluno agendou.…, `pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -… (+4 more)

### Community 41 - "turma_bp.py"
Cohesion: 0.13
Nodes (19): configuracoes(), route, editar_professor(), remover_professor(), Academia, remover_arquivo(), link_email(), Normalização de contatos profissionais antes de montar links públicos. (+11 more)

### Community 42 - "pagamento_polling.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 43 - "MercadoPagoIndisponivel"
Cohesion: 0.08
Nodes (46): _pagina(), ConfiguracaoInvalida, access_token_vigente(), _agora(), ambiente_da_conexao(), _cifrar(), _client_id(), _client_secret() (+38 more)

### Community 44 - "admin_requerido"
Cohesion: 0.42
Nodes (9): callback(), conectar(), desconectar(), limit, route, _voltar(), chave_da_conta(), Chave de limite por CONTA, caindo no IP só para quem não está autenticado. A… (+1 more)

### Community 45 - "criar_pagamento"
Cohesion: 0.09
Nodes (45): criar_pagamento(), test_retorno_sem_sessao_vai_para_o_login(), test_perfil_so_autoriza_abertura_automatica_da_propria_mensalidade(), consultar_mp(), fixture, parametrize, Limites de pagamento por conta, com o provedor inteiramente simulado., _sessao_aluno() (+37 more)

### Community 46 - "Plano"
Cohesion: 0.24
Nodes (4): Plano, Preço de uma cobrança criada em `hoje`., parametrize, test_duas_requisicoes_pix_reutilizam_uma_cobranca_postgres()

### Community 47 - "d9e2f6a14c80_contatos_academia_perfis_professores.py"
Cohesion: 0.83
Nodes (3): _campos_professor(), downgrade(), upgrade()

### Community 50 - "botao_ocupado.test.cjs"
Cohesion: 0.18
Nodes (7): assert, criarElemento(), fs, montar(), path, test, vm

### Community 51 - "test_seguranca.py"
Cohesion: 0.07
Nodes (24): test_upload_de_arquivo_disfarcado_e_recusado(), _cadastro_publico(), _imagem_jpeg(), _mensagem_da_resposta(), O `login` de um aluno pode ser o e-mail de outro; quem entra é decidido pela…, O ramo "par existe" não pode pagar a ida ao provedor dentro da requisição., Cadastro novo, CPF existente e e-mail existente respondem com a MESMA tela., Quem ainda controla a caixa antiga não pode assumir a conta depois da troca. (+16 more)

### Community 52 - "checkout_abertura.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 55 - "gunicorn.conf.py"
Cohesion: 0.25
Nodes (9): post_worker_init(), Hooks carregados pelo Gunicorn; nunca executados por flask db upgrade., worker_exit(), iniciar(), _laco(), parar(), Aciona a fila periodicamente durante a vida de um worker Gunicorn. Importar…, Inicia uma vez por processo, depois de carregar a aplicação e migrar o banco. (+1 more)

### Community 56 - "PagamentoDAO"
Cohesion: 0.10
Nodes (25): PagamentoDAO, Status como o painel deve LER, com o vencimento aplicado na própria consulta. A…, Carrega aluno e plano junto das mensalidades. O template do painel lê…, Lista completa (sem paginar). Mantida para relatórios e testes., Uma página de mensalidades, recortada pelo banco (LIMIT/OFFSET). O painel…, Totais do painel financeiro - sempre calculados no backend a partir do banco,…, True se já existe um Pix ou um checkout válido emitido para esta cobrança.…, True se a cobrança Pix já gerada para este pagamento ainda pode ser… (+17 more)

### Community 57 - "fila_email.py"
Cohesion: 0.06
Nodes (40): EmailPendente, espera_da_proxima_tentativa(), Fila de e-mails no banco. Aviso e cobrança coletivos saíam um a um dentro da…, contar_falhados(), contar_pendentes(), disparar(), enfileirar(), enfileirar_transacional() (+32 more)

### Community 58 - "test_migracao_cadastro_administrativo.py"
Cohesion: 0.40
Nodes (3): banco_antigo(), fixture, Verifica a migração em um banco isolado com o schema anterior e dados.

### Community 59 - "salvar_foto_perfil"
Cohesion: 0.12
Nodes (26): ArquivoInvalido, caminho_arquivo(), _conferir_dimensoes(), _detectar_tipo_imagem_real(), ImagemGrandeDemais, _pasta(), Exception, _raiz_uploads() (+18 more)

### Community 60 - "test_keep_alive.py"
Cohesion: 0.16
Nodes (7): ambiente_limpo(), fixture, parametrize, Garante que o keep-alive fica desligado por padrão e só pinga a própria origem., test_intervalo_fica_dentro_da_faixa(), test_nao_liga_com_valor_negativo(), test_ping_so_considera_200_como_sucesso()

### Community 61 - "test_google_login.py"
Cohesion: 0.11
Nodes (13): cliente_google(), google(), fixture, parametrize, Troca o token e o userinfo do Google; `perfil` é o que o userinfo devolve., test_aluno_aprovado_entra_e_a_troca_usa_o_mesmo_redirect_uri(), test_email_nao_verificado_pelo_google_nao_entra_na_conta(), test_email_sem_conta_volta_ao_login_sem_cadastrar() (+5 more)

### Community 62 - "mercado_pago.py"
Cohesion: 0.11
Nodes (30): _base_url_opcional(), base_url_publica(), cancelar_pagamento(), criar_pagamento_pix(), criar_preferencia_checkout(), _erro_menciona(), _erro_menciona_expiracao(), _extrair_dados_pix() (+22 more)

### Community 63 - "test_arranque_seguranca.py"
Cohesion: 0.22
Nodes (14): _env_arranque(), Validações feitas por servidor.py no arranque (COOKIE_SECURE, TRUSTED_HOSTS,…, `python -m servicos.credenciais`: o hash sai entre aspas simples. O hash do…, Desenvolvimento local sem HTTPS (sem Caddy) não pode ficar travado., _rodar(), test_arranque_falha_com_cookie_secure_false_e_app_base_url_https(), test_arranque_falha_com_cookie_secure_invalido(), test_arranque_falha_sem_trusted_hosts() (+6 more)

### Community 64 - "Aluno"
Cohesion: 0.08
Nodes (16): _convidar_cadastro_existente(), _convidar_cadastro_existente_por_id(), Cadastro administrativo que alguém tentou recriar pelo formulário público. Em…, Versão para thread de fundo: a sessão da requisição não vale fora dela., Matrícula feita no balcão: sem login, sem senha e sem convite de acesso. Nasce…, Aluno, Se existe uma conta de acesso, e não se o aluno está em dia ou matriculado.…, Convite de acesso já enviado e ainda não usado (a validade é checada na rota). (+8 more)

### Community 66 - "autorizacao.py"
Cohesion: 0.10
Nodes (26): _acesso_permitido(), desmatricular_aluno(), detalhe_turma(), foto_professor(), gerenciar_turmas(), matricular_aluno(), painel_professor(), limit (+18 more)

### Community 67 - "servidor.py"
Cohesion: 0.14
Nodes (20): after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, context_processor, errorhandler, formatar_moeda(), Formata um valor em reais no padrão brasileiro: R$ 1.080,00. Usado como filtro…, acesso_negado() (+12 more)

### Community 69 - "mercado_pago_oauth_bp.py"
Cohesion: 0.29
Nodes (11): _autorizacao_valida(), callback(), conectar(), desconectar(), limit, route, O administrador foi ao Mercado Pago e a autorização não voltou para cá? O state…, O state devolvido é o que ESTA sessão emitiu, há pouco tempo? (+3 more)

### Community 70 - "test_admin_mercado_pago.py"
Cohesion: 0.15
Nodes (17): Nome legível da forma de pagamento. Antes as telas usavam `|replace('_','…, rotulo_forma_pagamento(), _aprovado_no_checkout(), Painel do admin com mensalidades do Mercado Pago: formas de pagamento,…, Cartão/boleto: a preferência existe, o webhook ainda não trouxe o payment_id., _so_com_checkout(), test_admin_muda_o_status_sem_perder_a_forma_do_mercado_pago(), test_admin_nao_grava_forma_inventada() (+9 more)

### Community 71 - "credenciais.py"
Cohesion: 0.20
Nodes (11): admin_configurado(), comparar_em_tempo_constante(), credencial_admin_confere(), gerar_hash_admin(), _main(), Credencial administrativa baseada exclusivamente em hash de senha. O…, Compara duas senhas em tempo constante, sem restrição de alfabeto. Codificar…, True quando existe usuário e hash da senha do administrador. (+3 more)

### Community 72 - "shot.mjs"
Cohesion: 0.29
Nodes (5): { chromium }, contextos, CREDS, jobs, require

### Community 73 - "Componentes"
Cohesion: 0.05
Nodes (36): Altura de controle, Avisos flutuantes, Botões — `.et-botao` + variante (+ tamanho), Cartões e contêineres, Componentes, Contêiner e estrutura, Cores, Dados (+28 more)

### Community 74 - "keep_alive.py"
Cohesion: 0.29
Nodes (9): iniciar(), _intervalo(), _laco(), _ligado(), parar(), _pingar(), Mantém a aplicação acordada em hospedagens que hibernam por inatividade. Uma…, Encerra o laço. Usado pelos testes; em produção a thread é daemon. (+1 more)

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
Nodes (5): csrf_ligado(), fixture, Página de erro (templates/erro.html) e os handlers de 404, 403, 500 e CSRF., test_404_para_quem_esta_logado_leva_a_area_dele(), test_500_mostra_a_pagina_de_erro()

### Community 89 - "analytics.js"
Cohesion: 0.28
Nodes (4): apagarCookiesGa(), carregar(), origemDoReferrer(), revogar()

### Community 90 - "Relatório de segurança — Sistema Extreme Team"
Cohesion: 0.22
Nodes (8): Controles verificados, Histórico de auditorias, Pendências não relacionadas a segurança, Relatório de segurança — Sistema Extreme Team, Rodada anterior (22/09/2026 — 2ª rodada), Situação atual (04/10/2026 — limites de requisição), Validação executada em 04/10/2026, Validação executada em 22/09/2026

### Community 94 - "test_seo.py"
Cohesion: 0.06
Nodes (50): analytics_ativo(), id_analytics(), marcar_conversao_cadastro(), Google Analytics 4 opcional, só em página pública e só com consentimento. Sem…, Chamada no arranque: um ID malformado derruba a subida, como as demais…, Esta resposta pode carregar o GA4? Visitante, página pública indexável ou…, validar_configuracao(), conteudo_robots() (+42 more)

### Community 95 - "test_email_componentes.py"
Cohesion: 0.33
Nodes (7): E-mails: base com a logo oficial e componentes seguros para cliente de e-mail…, _render(), _sem_recursos_externos(), test_base_sem_url_publica_cai_para_o_nome_em_texto(), test_base_usa_a_logo_quando_ha_url_publica(), test_botao_do_email_usa_o_ouro_do_sistema(), test_cartao_de_resumo_com_badge()

### Community 96 - ".buscar_por_id"
Cohesion: 0.15
Nodes (26): _agora_mercado_pago(), _assinar(), _pagamento_mp(), _preparar_retorno(), Pix aberto e checkout concluído ao mesmo tempo: a consulta pelo…, test_retorno_com_aprovacao_confirmada_marca_pago(), test_retorno_com_mp_indisponivel_avisa_sem_mudar_status(), test_retorno_de_boleto_avisa_sobre_o_prazo() (+18 more)

### Community 98 - "test_layouts.py"
Cohesion: 0.29
Nodes (8): _conferir_head_comum(), parametrize, Layouts base (templates/layouts/) e toasts. Cada página estende o layout da sua…, test_area_do_aluno_carrega_o_layout(), test_flash_de_erro_vira_toast_que_nao_some_sozinho(), test_paginas_publicas_carregam_o_head_comum(), test_painel_admin_carrega_o_layout_admin(), test_toda_pagina_estende_um_layout()

### Community 102 - "Flask App Service (compose)"
Cohesion: 0.22
Nodes (9): Flask App Service (compose), Postgres DB Service (compose), postgres_data Volume, Flask, Flask-SQLAlchemy, Gunicorn, psycopg2-binary, python-dotenv (+1 more)

### Community 104 - "erro_validacao_senha"
Cohesion: 0.16
Nodes (13): alterar_senha_perfil(), ativar_acesso(), Transforma um cadastro feito no balcão na conta do próprio aluno. Quem chega…, mascarar_email(), Mostra o bastante do e-mail para o dono se reconhecer, sem revelá-lo a…, _carregar_senhas_comuns(), erro_confirmacao_senha(), erro_validacao_senha() (+5 more)

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
Cohesion: 0.14
Nodes (5): banco_fora(), fixture, /health/pronto: 503 quando banco ou Redis caem, sem expor detalhe nem criar…, Cada chamada consulta banco e Redis: 60 por minuto bastam ao monitor externo., test_pronto_tem_limite_por_ip()

### Community 113 - "test_perfil_e_foto.py"
Cohesion: 0.19
Nodes (13): cadastrar_turma(), remover_turma(), TurmaDAO, Turma, Cadastrar Turma Form, test_escolher_plano_com_turma_cria_matricula(), test_turma_lotada_nao_vira_matricula_apos_pagamento(), _imagem_jpeg_valida() (+5 more)

### Community 115 - "PagamentoEvento"
Cohesion: 0.12
Nodes (11): Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.…, Primeiro dia não coberto por outra mensalidade do mesmo aluno., Define o período coberto por uma mensalidade que ainda não tem um (lançamento…, Abre o período de acesso no momento em que o pagamento é confirmado. Se a…, Reescreve os campos denormalizados do aluno a partir das mensalidades.…, forma_pagamento vem do que o Mercado Pago confirmou na consulta à API ('pix',…, Uma recusa encerra aquela tentativa, não a mensalidade. Quando o aluno gera um…, PagamentoEvento (+3 more)

### Community 116 - "test_observabilidade.py"
Cohesion: 0.18
Nodes (18): before_breadcrumb(), before_send(), iniciar_sentry(), _limpar(), mascarar(), Rastreamento de erros opcional com Sentry. Sem `SENTRY_DSN`, nada é importado…, _evento(), fixture (+10 more)

### Community 117 - "usuario_bp.py"
Cohesion: 0.12
Nodes (35): _acesso_permitido_pagamento(), _aluno_da_sessao(), atualizar_dados_perfil(), cadastro_obrigado(), cancelar_mudanca_plano(), _chave_ip_e_identificador(), comprovante_mensalidade(), confirmar_presenca() (+27 more)

### Community 118 - "test_plano_arquivo_promocao.py"
Cohesion: 0.14
Nodes (25): Tira o plano de venda. Devolve `(plano, pedidos_cancelados)`, ou None. Pedidos…, Pagamento, Status a exibir, com o vencimento já aplicado. Uma cobrança `pendente` cujo…, _pagar(), _plano(), _promocao(), Plano fora de venda (arquivar/reativar/excluir), edição e promoção com período.…, test_admin_nao_lanca_mensalidade_nova_em_plano_arquivado() (+17 more)

### Community 119 - "test_backup_scripts.py"
Cohesion: 0.27
Nodes (11): ambiente(), _executavel(), fixture, Scripts de backup (tools/backup/): retenção, falha sem backup "pela metade" e a…, _rodar(), test_backup_gera_dump_e_uploads_e_aplica_a_retencao(), test_dump_ilegivel_nao_vira_backup(), test_restaurar_em_banco_descartavel_e_extrair_uploads() (+3 more)

### Community 120 - "google_login.py"
Cohesion: 0.27
Nodes (10): callback(), login_google(), limit, route, redirect_uri(), pagina_login(), iniciar_sessao(), Grava na sessão atual a credencial em vigor (login ou troca de senha bem-… (+2 more)

### Community 122 - "revogar_sessao_atual"
Cohesion: 0.29
Nodes (8): Registra a sessão como encerrada: cópias antigas do cookie deixam de valer.…, revogar_sessao_atual(), health(), health_pronto(), logout(), exempt, limit, route

### Community 124 - "pagina_cadastro"
Cohesion: 0.25
Nodes (13): _cadastro_recebido(), _em_segundo_plano(), pagina_cadastro(), Post/Redirect/Get para a página de obrigado. Cadastro novo, CPF já cadastrado e…, Roda `tarefa` fora da requisição, para o tempo de resposta não revelar nada. Em…, cpf_valido(), data_nascimento_valida(), formatar_cpf() (+5 more)

### Community 125 - "PlanoDAO"
Cohesion: 0.13
Nodes (17): PlanoDAO, Apaga um plano que nunca foi usado. True, None (não existe) ou False (em uso)., Os planos à venda: home, perfil do aluno e formulários de contratação., Planos que algum registro referencia: mensalidade, cadastro de aluno ou pedido…, Grava a edição do admin. Vale para as cobranças criadas daqui em diante: as…, home(), parametrize, test_admin_cria_promocao() (+9 more)

### Community 126 - "Professor"
Cohesion: 0.09
Nodes (28): cadastrar_professor(), ProfessorDAO, Professor, Cadastrar Professor Form, test_publicacao_professor_nao_expoe_contatos_sem_permissao(), logar_como_professor(), fixture, Hipótese: a foto continua acessível por URL depois de tirar a publicação. (+20 more)

### Community 127 - "adm_bp.py"
Cohesion: 0.06
Nodes (67): _aluno_do_cpf_ou_painel(), aprovar_aluno(), aprovar_comprovante_manual(), arquivar_plano(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_aluno(), cadastrar_pagamento() (+59 more)

### Community 130 - "_aluno_por_token"
Cohesion: 0.25
Nodes (8): _aluno_por_token(), confirmar_email(), Descarta todo link pendente que ainda autorizaria assumir ou redirecionar a…, Localiza o aluno pelo hash do token, filtrando no banco por uma coluna indexada., redefinir_senha(), _revogar_tokens_de_conta(), route, verificar_email_cadastro()

### Community 131 - "parametrize"
Cohesion: 0.40
Nodes (5): parametrize, test_confirmacao_aceita_unicode(), test_matricula_valida_dados_no_servidor(), test_novos_formularios_exigem_csrf(), test_rotas_de_matricula_e_convite_sao_so_do_admin()

### Community 133 - "test_conversao_home.py"
Cohesion: 0.14
Nodes (17): faq_estruturado(), Textos editáveis da página inicial: perguntas frequentes e prazos de…, JSON-LD FAQPage com exatamente as perguntas mostradas na página., _body_tag(), _html(), parametrize, Conversão na home: perguntas frequentes, CTA fixo no celular e página de…, test_admin_logado_nao_ve_o_cta_fixo() (+9 more)

### Community 134 - "URLPublicaInvalida"
Cohesion: 0.11
Nodes (30): _enviar_em_segundo_plano(), E-mail COM token (recuperação, confirmação): não pode ir para a `fila_email`. A…, recuperar_senha(), solicitar_troca_email(), verificar_email_cadastro(), aluno_do_token(), ConviteIndisponivel, descartar() (+22 more)

### Community 135 - "prontidao.py"
Cohesion: 0.43
Nodes (6): banco_responde(), _consultar_banco(), Verificação de prontidão (/health/pronto): o banco e o Redis respondem agora?…, None quando o limite de requisições não usa Redis (memory:// em…, redis_responde(), verificar()

### Community 136 - "capturar_emails"
Cohesion: 0.67
Nodes (3): capturar_emails(), fixture, Intercepta o envio e devolve os e-mails que teriam saído, com os links.

### Community 140 - "backup.sh"
Cohesion: 1.00
Nodes (3): registrar(), reter(), backup.sh script

### Community 143 - "Biblioteca no Figma"
Cohesion: 0.50
Nodes (3): Biblioteca no Figma, Falta (ordem de retomada), Limites do plano Starter que moldaram o arquivo

## Knowledge Gaps
- **166 isolated node(s):** `modal`, `input_senha`, `icone_senha`, `formularioPlano`, `campoPreco` (+161 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PagamentoDAO` connect `PagamentoDAO` to `logar_como_aluno`, `.listar_por_aluno`, `test_pagamento_recusado.py`, `test_mudanca_plano.py`, `pix_bp.py`, `criar_aluno`, `AlunoDAO`, `checkout_bp.py`, `config.py`, `test_auditoria_seguranca.py`, `MatriculaDAO`, `.contratar_plano`, `criar_pagamento`, `test_seguranca.py`, `Aluno`, `test_admin_mercado_pago.py`, `conftest.py`, `.buscar_por_id`, `test_perfil_e_foto.py`, `PagamentoEvento`, `usuario_bp.py`, `test_plano_arquivo_promocao.py`, `adm_bp.py`?**
  _High betweenness centrality (0.120) - this node is a cross-community bridge._
- **Why does `criar_aluno()` connect `criar_aluno` to `logar_como_aluno`, `.listar_por_aluno`, `parametrize`, `test_conversao_home.py`, `test_mudanca_plano.py`, `test_analytics.py`, `test_home_planos.py`, `AlunoDAO`, `logar_como_admin`, `test_auditoria_seguranca.py`, `test_mercado_pago_oauth.py`, `test_limites_requisicao.py`, `MatriculaDAO`, `.contratar_plano`, `criar_pagamento`, `test_seguranca.py`, `PagamentoDAO`, `test_google_login.py`, `Aluno`, `conftest.py`, `test_paginas_erro.py`, `test_seo.py`, `.buscar_por_id`, `test_layouts.py`, `test_perfil_e_foto.py`, `test_plano_arquivo_promocao.py`, `PlanoDAO`, `Professor`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Why does `logar_como_admin()` connect `logar_como_admin` to `logar_como_aluno`, `.listar_por_aluno`, `parametrize`, `test_conversao_home.py`, `test_mudanca_plano.py`, `criar_aluno`, `test_analytics.py`, `test_home_planos.py`, `AlunoDAO`, `test_mercado_pago_oauth.py`, `MatriculaDAO`, `turma_bp.py`, `criar_pagamento`, `test_seguranca.py`, `PagamentoDAO`, `test_google_login.py`, `Aluno`, `test_admin_mercado_pago.py`, `conftest.py`, `test_sessao_revogada.py`, `test_seo.py`, `.buscar_por_id`, `test_layouts.py`, `test_perfil_e_foto.py`, `test_plano_arquivo_promocao.py`, `PlanoDAO`, `Professor`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Are the 157 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 157 INFERRED edges - model-reasoned connections that need verification._
- **Are the 162 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 162 INFERRED edges - model-reasoned connections that need verification._
- **Are the 155 inferred relationships involving `criar_pagamento()` (e.g. with `PagamentoDAO` and `Pagamento`) actually correct?**
  _`criar_pagamento()` has 155 INFERRED edges - model-reasoned connections that need verification._
- **Are the 153 inferred relationships involving `logar_como_admin()` (e.g. with `test_admin_salva_atualiza_e_limpa_contatos()` and `test_csrf_configuracoes()`) actually correct?**
  _`logar_como_admin()` has 153 INFERRED edges - model-reasoned connections that need verification._