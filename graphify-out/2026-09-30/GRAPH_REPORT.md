# Graph Report - SistemaEXTREMETEAM  (2026-09-30)

## Corpus Check
- 169 files · ~225,126 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2220 nodes · 5626 edges · 139 communities (123 shown, 16 thin omitted)
- Extraction: 80% EXTRACTED · 20% INFERRED · 0% AMBIGUOUS · INFERRED: 1132 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `83523880`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- route
- extreme.css
- planos.py
- .listar_por_aluno
- MercadoPagoIndisponivel
- test_mudanca_plano.py
- test_pagamento_recusado.py
- criar_aluno
- SistemaEXTREMETEAM Project
- test_mercado_pago_servico.py
- test_mercado_pago_oauth.py
- test_analytics.py
- test_migracao_checkout.py
- checkout.js
- CLAUDE.md
- test_home_planos.py
- pix_bp.py
- AlunoDAO
- test_mercado_pago_oauth_postgres.py
- checkout_bp.py
- pix.js
- config.py
- env.py
- pagamento.js
- c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py
- varredura.mjs
- 896e70afc9c5_adiciona_foto_e_graduacao_do_aluno_.py
- test_auditoria_seguranca.py
- test_seo.py
- logar_como_admin
- MatriculaDAO
- gmail_conta.py
- URLPublicaInvalida
- PagamentoDAO
- pagamento_polling.test.cjs
- mercado_pago_conta.py
- logar_como_aluno
- criar_pagamento
- test_contratacao_plano.py
- d9e2f6a14c80_contatos_academia_perfis_professores.py
- test_conversao_home.py
- botao_ocupado.test.cjs
- test_seguranca.py
- checkout_abertura.test.cjs
- filtros_financeiro.js
- gunicorn.conf.py
- test_email_gmail.py
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
- ConfiguracaoInvalida
- test_admin_mercado_pago.py
- credenciais.py
- shot.mjs
- _aluno_por_token
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
- admin_requerido
- test_email_componentes.py
- keep_alive.py
- PlanoDAO
- test_layouts.py
- test_linha_com_defeito_nao_trava_a_fila_atras_dela
- SolicitacaoMudancaPlano
- Flask App Service (compose)
- test_reenviar_um_aviso_que_desistiu_volta_a_enfileirar
- Plano
- Etapa 1 — migrar páginas para os layouts (SEM mudar o visual)
- Etapas 4 a 6 — aluno, admin, professor (aplicar os componentes nas páginas)
- seo_bp.py
- Etapa 2 — biblioteca de componentes
- Etapa 3 — home com os planos + termos
- test_prontidao.py
- test_perfil_e_foto.py
- test_um_envio_ainda_pendente_continua_sendo_recusado
- test_observabilidade.py
- usuario_bp.py
- test_plano_arquivo_promocao.py
- test_backup_scripts.py
- _parece_busca_por_cpf
- gerar_imagem_og.py
- test_retentativa_acontece_sem_ninguem_abrir_o_painel
- test_trocar_a_credencial_do_admin_encerra_a_sessao_administrativa
- test_uma_falha_do_provedor_nao_queima_todas_as_tentativas
- Professor
- adm_bp.py
- _chave_da_conta
- Academia
- rotulo_forma_pagamento
- prontidao.py
- capturar_emails
- .bloquear_pendente_do_aluno
- backup.sh
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

## Communities (139 total, 16 thin omitted)

### Community 0 - "route"
Cohesion: 0.10
Nodes (30): _acesso_permitido_pagamento(), _aluno_da_sessao(), cadastro_obrigado(), cancelar_mudanca_plano(), comprovante_mensalidade(), confirmar_presenca(), enviar_comprovante_manual_aluno(), enviar_foto_perfil() (+22 more)

### Community 1 - "extreme.css"
Cohesion: 0.05
Nodes (36): abrirmodal(), fechar(), icone_senha, input_senha, modal, mostrarSenha(), campoDuracao, campoPreco (+28 more)

### Community 2 - "planos.py"
Cohesion: 0.06
Nodes (42): cadeia_paga(), cartao_do_plano(), cobranca_a_pagar(), cobranca_em_decisao(), cobranca_pendente(), duracao_dias(), _duracao_por_extenso(), esta_inadimplente() (+34 more)

### Community 3 - ".listar_por_aluno"
Cohesion: 0.10
Nodes (34): Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, Com uma troca já agendada, só dois planos fazem sentido num pedido de…, A cobrança do período seguinte tem de nascer no plano que o aluno agendou.…, `pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -…, _pagar(), plano_barato(), fixture, Vigência do plano: o que decide "Plano ativo" é o período pago, não o cadastro.… (+26 more)

### Community 4 - "MercadoPagoIndisponivel"
Cohesion: 0.16
Nodes (18): buscar_pagamento(), buscar_pagamentos_por_referencia(), cancelar_pagamento(), MercadoPagoIndisponivel, Consulta o pagamento diretamente na API do Mercado Pago - fonte de verdade de…, Lista os pagamentos que o Mercado Pago associa a uma external_reference. Usada…, Cancela uma cobranca Pix pendente no Mercado Pago. Best-effort: nunca lanca., Falha de transporte (timeout/DNS/conexao) ao falar com a API do Mercado Pago. (+10 more)

### Community 5 - "test_mudanca_plano.py"
Cohesion: 0.14
Nodes (28): detalhes_usuario(), Persistência dos pedidos de troca de plano agendados para a próxima renovação., Aplica um pedido agendado cujo período de origem já terminou sem renovação.…, SolicitacaoPlanoDAO, _agendar(), _pagar(), plano_barato(), fixture (+20 more)

### Community 6 - "test_pagamento_recusado.py"
Cohesion: 0.23
Nodes (22): test_polling_usa_consultas_curtas_sem_retentativas(), test_retorno_checkout_usa_consulta_curta_sem_retentativas(), _assinar(), _data_mp(), _eventos(), _mockar_mp(), _pagamento_mp(), _pix_criado() (+14 more)

### Community 7 - "criar_aluno"
Cohesion: 0.06
Nodes (44): Totais do painel financeiro - sempre calculados no backend a partir do banco,…, Uma página de alunos já cadastrados, recortada e filtrada pelo banco. O painel…, criar_aluno(), test_aluno_existente_continua_entrando_normalmente(), _contar_selects_em_alunos(), _credencial(), Regressões da auditoria de segurança, desempenho e confiabilidade. Cada caso…, Trocar senha, e-mail ou foto são ações de quem JÁ está autenticado. Devolver o… (+36 more)

### Community 9 - "test_mercado_pago_servico.py"
Cohesion: 0.09
Nodes (35): ambiente_mercado_pago(), Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, Diz se a integracao esta apontando para producao ou para o sandbox. Prioriza a…, validar_assinatura_webhook(), Hipótese: uma notificação capturada ontem pode ser reenviada hoje., `ts=nan` fazia a comparação da janela dar False e passava pela checagem de…, test_webhook_recusa_assinatura_antiga(), test_webhook_recusa_ts_nao_numerico_finito() (+27 more)

### Community 10 - "test_mercado_pago_oauth.py"
Cohesion: 0.08
Nodes (58): MercadoPagoConexao, Conta do Mercado Pago que a academia autorizou por OAuth. Uma linha só (a…, _agora(), _ajustar(), api_mp(), _conectar(), _dados_conexao(), oauth_env() (+50 more)

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
Cohesion: 0.20
Nodes (16): Inclusive os arquivados: serve a quem olha o histórico (filtro do financeiro)., Planos da página inicial, prontos para `components/cartao_plano.html`. O preço…, vitrine_planos(), _plano(), _quatro_planos(), Planos na página inicial: cálculo (servicos/planos.vitrine_planos), destaque…, test_admin_destaca_e_tira_o_destaque(), test_admin_pode_criar_plano_ja_em_destaque() (+8 more)

### Community 17 - "pix_bp.py"
Cohesion: 0.09
Nodes (36): _acesso_permitido(), criar_pix_mensalidade(), _data_da_aprovacao(), _forma_pagamento_confirmada(), _instante_utc(), _iso_utc(), _pagamento_mp_mais_relevante(), _pagamento_ou_none() (+28 more)

### Community 18 - "AlunoDAO"
Cohesion: 0.15
Nodes (39): _convidar_cadastro_existente(), Cadastro administrativo que alguém tentou recriar pelo formulário público. Em…, AlunoDAO, _matricular(), Cadastro de aluno pela administração, ativação de acesso e confirmação de…, test_admin_lanca_e_baixa_mensalidade_de_aluno_sem_acesso(), test_admin_matricula_aluno_sem_email_senha_nem_acesso(), test_admin_pode_deixar_cadastro_de_balcao_sem_usuario_e_sem_email() (+31 more)

### Community 19 - "test_mercado_pago_oauth_postgres.py"
Cohesion: 0.18
Nodes (8): postgres_mp(), fixture, Renovação do token OAuth com trava de linha real, opcional na suíte que usa…, _Resposta, test_dois_processos_perto_do_vencimento_gastam_o_refresh_token_uma_vez(), _migracao(), test_migracao_cria_a_tabela_igual_ao_modelo_e_e_reentrante(), test_migracao_encadeia_na_ultima_revisao_existente()

### Community 20 - "checkout_bp.py"
Cohesion: 0.11
Nodes (24): abrir_checkout(), _acesso_permitido(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), limitar_consulta_pagamento, limitar_criacao_pagamento, route (+16 more)

### Community 21 - "pix.js"
Cohesion: 0.33
Nodes (14): abrirPix(), alvoDoRotulo(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), liberarBotao(), limparConteudoAnterior() (+6 more)

### Community 22 - "config.py"
Cohesion: 0.16
Nodes (12): _paginar(), Aplica LIMIT/OFFSET e conta o total numa consulta separada e barata. A contagem…, Decimal, Matricula, _para_decimal(), postgres_pix(), fixture, Regressão com trava de linha real, opcional na suíte que usa SQLite. Execute… (+4 more)

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
Nodes (46): _assinar(), logar_como_professor(), _pagamento_mp(), _preparar_para_conciliacao(), fixture, parametrize, Auditoria de segurança: sondas escritas para TENTAR quebrar as regras. Nenhum…, Hipótese: a sessão de professor é aceita nas rotas financeiras do aluno. (+38 more)

### Community 34 - "test_seo.py"
Cohesion: 0.06
Nodes (50): analytics_ativo(), id_analytics(), marcar_conversao_cadastro(), Google Analytics 4 opcional, só em página pública e só com consentimento. Sem…, Chamada no arranque: um ID malformado derruba a subida, como as demais…, Esta resposta pode carregar o GA4? Visitante, página pública indexável ou…, validar_configuracao(), conteudo_robots() (+42 more)

### Community 35 - "logar_como_admin"
Cohesion: 0.11
Nodes (20): logar_como_admin(), parametrize, test_admin_nao_pode_apagar_o_usuario_de_uma_conta_ativa(), test_confirmacao_aceita_unicode(), test_convite_recusado_para_quem_ja_tem_acesso(), test_matricula_valida_dados_no_servidor(), test_novos_formularios_exigem_csrf(), test_rotas_de_matricula_e_convite_sao_so_do_admin() (+12 more)

### Community 36 - "MatriculaDAO"
Cohesion: 0.18
Nodes (16): MatriculaDAO, Presenca, impressao_credencial(), Resumo curto e não reversível do hash da senha, guardado na sessão. Nunca é a…, Valor que representa a credencial administrativa em vigor, ou None se não há…, referencia_credencial_admin(), parametrize, test_aluno_confirma_sua_frequencia() (+8 more)

### Community 37 - "gmail_conta.py"
Cohesion: 0.27
Nodes (15): GmailConexao, _access_token(), _cifrar(), _client_id(), _client_secret(), _decifrar(), enviar(), estado() (+7 more)

### Community 38 - "URLPublicaInvalida"
Cohesion: 0.12
Nodes (27): solicitar_troca_email(), verificar_email_cadastro(), aluno_do_token(), ConviteIndisponivel, descartar(), enviar(), gerar_token(), _hash() (+19 more)

### Community 41 - "PagamentoDAO"
Cohesion: 0.05
Nodes (42): mensalidade_destaque(), PagamentoDAO, Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.…, Status como o painel deve LER, com o vencimento aplicado na própria consulta. A…, Carrega aluno e plano junto das mensalidades. O template do painel lê…, Lista completa (sem paginar). Mantida para relatórios e testes., Uma página de mensalidades, recortada pelo banco (LIMIT/OFFSET). O painel…, Escolhe a mensalidade mais relevante para o card 'Minha mensalidade': a mais… (+34 more)

### Community 42 - "pagamento_polling.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 43 - "mercado_pago_conta.py"
Cohesion: 0.09
Nodes (39): access_token_vigente(), _agora(), ambiente_da_conexao(), _cifrar(), _client_id(), _client_secret(), ConexaoIlegivel, _configuracao_do_aplicativo() (+31 more)

### Community 44 - "logar_como_aluno"
Cohesion: 0.08
Nodes (65): logar_como_aluno(), Hipótese: forjar ?status=approved na volta do MP quita a mensalidade., test_retorno_ignora_status_aprovado_da_query_string(), _assinar(), _mockar_preferencia(), _pagamento_mp(), _preparar_retorno(), parametrize (+57 more)

### Community 45 - "criar_pagamento"
Cohesion: 0.10
Nodes (42): criar_pagamento(), test_busca_financeira_trata_curingas_como_texto(), test_painel_financeiro_busca_por_nome_do_aluno(), test_painel_financeiro_exige_admin(), test_painel_financeiro_filtra_por_status(), test_painel_financeiro_mostra_totais_do_backend(), consultar_mp(), fixture (+34 more)

### Community 46 - "test_contratacao_plano.py"
Cohesion: 0.29
Nodes (6): test_area_do_aluno_renderiza_telas_independentes_do_menu(), test_escolher_plano_cria_mensalidade_e_redireciona_para_pix(), test_plano_atual_continua_disponivel_para_gerar_cobranca(), test_plano_invalido_nao_cria_mensalidade(), test_reenvio_da_contratacao_reutiliza_mensalidade(), test_valor_enviado_pelo_navegador_e_ignorado()

### Community 47 - "d9e2f6a14c80_contatos_academia_perfis_professores.py"
Cohesion: 0.83
Nodes (3): _campos_professor(), downgrade(), upgrade()

### Community 49 - "test_conversao_home.py"
Cohesion: 0.14
Nodes (17): faq_estruturado(), Textos editáveis da página inicial: perguntas frequentes e prazos de…, JSON-LD FAQPage com exatamente as perguntas mostradas na página., _body_tag(), _html(), parametrize, Conversão na home: perguntas frequentes, CTA fixo no celular e página de…, test_admin_logado_nao_ve_o_cta_fixo() (+9 more)

### Community 50 - "botao_ocupado.test.cjs"
Cohesion: 0.18
Nodes (7): assert, criarElemento(), fs, montar(), path, test, vm

### Community 51 - "test_seguranca.py"
Cohesion: 0.07
Nodes (26): test_upload_de_arquivo_disfarcado_e_recusado(), _cadastro_publico(), _imagem_jpeg(), _mensagem_da_resposta(), O `login` de um aluno pode ser o e-mail de outro; quem entra é decidido pela…, O ramo "par existe" não pode pagar a ida ao provedor dentro da requisição., Cadastro novo, CPF existente e e-mail existente respondem com a MESMA tela., Quem ainda controla a caixa antiga não pode assumir a conta depois da troca. (+18 more)

### Community 52 - "checkout_abertura.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 55 - "gunicorn.conf.py"
Cohesion: 0.25
Nodes (9): post_worker_init(), Hooks carregados pelo Gunicorn; nunca executados por flask db upgrade., worker_exit(), iniciar(), _laco(), parar(), Aciona a fila periodicamente durante a vida de um worker Gunicorn. Importar…, Inicia uma vez por processo, depois de carregar a aplicação e migrar o banco. (+1 more)

### Community 56 - "test_email_gmail.py"
Cohesion: 0.29
Nodes (3): aplicativo_google(), fixture, test_refresh_token_fica_cifrado_no_banco()

### Community 57 - "fila_email.py"
Cohesion: 0.06
Nodes (40): EmailPendente, espera_da_proxima_tentativa(), Fila de e-mails no banco. Aviso e cobrança coletivos saíam um a um dentro da…, contar_falhados(), contar_pendentes(), disparar(), enfileirar(), enfileirar_transacional() (+32 more)

### Community 58 - "test_migracao_cadastro_administrativo.py"
Cohesion: 0.40
Nodes (3): banco_antigo(), fixture, Verifica a migração em um banco isolado com o schema anterior e dados.

### Community 59 - "salvar_foto_perfil"
Cohesion: 0.09
Nodes (32): ArquivoInvalido, caminho_arquivo(), _conferir_dimensoes(), _detectar_tipo_imagem_real(), ImagemGrandeDemais, _pasta(), Exception, _raiz_uploads() (+24 more)

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
Cohesion: 0.09
Nodes (13): Matrícula feita no balcão: sem login, sem senha e sem convite de acesso. Nasce…, Aluno, Se existe uma conta de acesso, e não se o aluno está em dia ou matriculado.…, Convite de acesso já enviado e ainda não usado (a validade é checada na rota)., Chave do estado da CONTA - nunca da situação financeira nem da matrícula., test_cadastro_publico_recusa_confirmacao_diferente(), test_cadastro_publico_recusa_confirmacao_vazia(), test_matricula_recusa_cpf_invalido() (+5 more)

### Community 66 - "turma_bp.py"
Cohesion: 0.16
Nodes (25): _acesso_permitido(), cadastrar_professor(), desmatricular_aluno(), detalhe_turma(), foto_professor(), matricular_aluno(), painel_professor(), route (+17 more)

### Community 67 - "servidor.py"
Cohesion: 0.12
Nodes (23): after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, context_processor, errorhandler, Registra a sessão como encerrada: cópias antigas do cookie deixam de valer.…, revogar_sessao_atual(), formatar_moeda() (+15 more)

### Community 69 - "ConfiguracaoInvalida"
Cohesion: 0.27
Nodes (12): _autorizacao_valida(), callback(), conectar(), desconectar(), limit, route, O state devolvido é o que ESTA sessão emitiu, há pouco tempo?, Só monta o state/PKCE na sessão e manda o administrador ao Mercado Pago. É um… (+4 more)

### Community 70 - "test_admin_mercado_pago.py"
Cohesion: 0.15
Nodes (16): _aprovado_no_checkout(), parametrize, Painel do admin com mensalidades do Mercado Pago: formas de pagamento,…, Cartão/boleto: a preferência existe, o webhook ainda não trouxe o payment_id., _so_com_checkout(), test_admin_lanca_mensalidade_paga_no_cartao(), test_admin_muda_o_status_sem_perder_a_forma_do_mercado_pago(), test_admin_nao_grava_forma_inventada() (+8 more)

### Community 71 - "credenciais.py"
Cohesion: 0.20
Nodes (11): admin_configurado(), comparar_em_tempo_constante(), credencial_admin_confere(), gerar_hash_admin(), _main(), Credencial administrativa baseada exclusivamente em hash de senha. O…, Compara duas senhas em tempo constante, sem restrição de alfabeto. Codificar…, True quando existe usuário e hash da senha do administrador. (+3 more)

### Community 72 - "shot.mjs"
Cohesion: 0.29
Nodes (5): { chromium }, contextos, CREDS, jobs, require

### Community 73 - "_aluno_por_token"
Cohesion: 0.40
Nodes (4): _aluno_por_token(), Localiza o aluno pelo hash do token, filtrando no banco por uma coluna indexada., route, verificar_email_cadastro()

### Community 74 - "google_login.py"
Cohesion: 0.27
Nodes (10): callback(), login_google(), limit, route, redirect_uri(), pagina_login(), iniciar_sessao(), Grava na sessão atual a credencial em vigor (login ou troca de senha bem-… (+2 more)

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
Cohesion: 0.20
Nodes (14): health_pronto(), exempt, route, app(), client(), contexto_app(), limpar_banco(), logar_como_professor() (+6 more)

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
Cohesion: 0.29
Nodes (6): Controles verificados, Histórico de auditorias, Pendências não relacionadas a segurança, Relatório de segurança — Sistema Extreme Team, Situação atual (22/09/2026 — 2ª rodada), Validação executada em 22/09/2026

### Community 94 - "admin_requerido"
Cohesion: 0.57
Nodes (7): callback(), conectar(), desconectar(), limit, route, _voltar(), admin_requerido()

### Community 95 - "test_email_componentes.py"
Cohesion: 0.33
Nodes (7): E-mails: base com a logo oficial e componentes seguros para cliente de e-mail…, _render(), _sem_recursos_externos(), test_base_sem_url_publica_cai_para_o_nome_em_texto(), test_base_usa_a_logo_quando_ha_url_publica(), test_botao_do_email_usa_o_ouro_do_sistema(), test_cartao_de_resumo_com_badge()

### Community 96 - "keep_alive.py"
Cohesion: 0.29
Nodes (9): iniciar(), _intervalo(), _laco(), _ligado(), parar(), _pingar(), Mantém a aplicação acordada em hospedagens que hibernam por inatividade. Uma…, Encerra o laço. Usado pelos testes; em produção a thread é daemon. (+1 more)

### Community 97 - "PlanoDAO"
Cohesion: 0.14
Nodes (18): PlanoDAO, Apaga um plano que nunca foi usado. True, None (não existe) ou False (em uso)., Marca o plano em destaque da página inicial, desmarcando qualquer outro.…, Os planos à venda: home, perfil do aluno e formulários de contratação., Planos que algum registro referencia: mensalidade, cadastro de aluno ou pedido…, Grava a edição do admin. Vale para as cobranças criadas daqui em diante: as…, home(), parametrize (+10 more)

### Community 98 - "test_layouts.py"
Cohesion: 0.29
Nodes (8): _conferir_head_comum(), parametrize, Layouts base (templates/layouts/) e toasts. Cada página estende o layout da sua…, test_area_do_aluno_carrega_o_layout(), test_flash_de_erro_vira_toast_que_nao_some_sozinho(), test_paginas_publicas_carregam_o_head_comum(), test_painel_admin_carrega_o_layout_admin(), test_toda_pagina_estende_um_layout()

### Community 100 - "SolicitacaoMudancaPlano"
Cohesion: 0.22
Nodes (4): O que aconteceu numa tentativa de contratar/renovar/trocar de plano., ResultadoContratacao, Pedido de troca de plano agendado para a próxima renovação. Nunca altera o…, SolicitacaoMudancaPlano

### Community 102 - "Flask App Service (compose)"
Cohesion: 0.20
Nodes (10): Flask App Service (compose), Postgres DB Service (compose), postgres_data Volume, Flask, Flask-SQLAlchemy, Gunicorn, psycopg2-binary, python-dotenv (+2 more)

### Community 104 - "Plano"
Cohesion: 0.24
Nodes (4): Plano, Preço de uma cobrança criada em `hoje`., parametrize, test_duas_requisicoes_pix_reutilizam_uma_cobranca_postgres()

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
Nodes (18): cadastrar_turma(), remover_turma(), TurmaDAO, Turma, Sonda: a data vem da query string e é convertida sem tratamento., test_data_invalida_na_turma_nao_derruba_a_rota(), test_escolher_plano_com_turma_cria_matricula(), test_turma_lotada_nao_vira_matricula_apos_pagamento() (+10 more)

### Community 116 - "test_observabilidade.py"
Cohesion: 0.14
Nodes (20): before_breadcrumb(), before_send(), iniciar_sentry(), _limpar(), mascarar(), Rastreamento de erros opcional com Sentry. Sem `SENTRY_DSN`, nada é importado…, _evento(), fixture (+12 more)

### Community 117 - "usuario_bp.py"
Cohesion: 0.11
Nodes (35): alterar_senha_perfil(), ativar_acesso(), atualizar_dados_perfil(), _cadastro_recebido(), confirmar_email(), _convidar_cadastro_existente_por_id(), _em_segundo_plano(), _enviar_em_segundo_plano() (+27 more)

### Community 118 - "test_plano_arquivo_promocao.py"
Cohesion: 0.14
Nodes (26): Tira o plano de venda. Devolve `(plano, pedidos_cancelados)`, ou None. Pedidos…, Pagamento, Status a exibir, com o vencimento já aplicado. Uma cobrança `pendente` cujo…, _pagar(), _plano(), _promocao(), Plano fora de venda (arquivar/reativar/excluir), edição e promoção com período.…, test_admin_nao_lanca_mensalidade_nova_em_plano_arquivado() (+18 more)

### Community 119 - "test_backup_scripts.py"
Cohesion: 0.27
Nodes (11): ambiente(), _executavel(), fixture, Scripts de backup (tools/backup/): retenção, falha sem backup "pela metade" e a…, _rodar(), test_backup_gera_dump_e_uploads_e_aplica_a_retencao(), test_dump_ilegivel_nao_vira_backup(), test_restaurar_em_banco_descartavel_e_extrair_uploads() (+3 more)

### Community 120 - "_parece_busca_por_cpf"
Cohesion: 0.18
Nodes (11): _parece_busca_por_cpf(), O termo é um CPF, ou um pedaço dele, e não um nome que por acaso tem número?, parametrize, Qualquer dígito no termo virava `CPF LIKE '%3%'` e devolvia a academia inteira., Rotas que custam hash de senha, processamento de imagem ou sondagem de token., Limites declarados por decorador NAQUELA rota. `resolve_limits` não serve aqui:…, Guarda do teste acima: uma rota sem limite precisa ser reprovada por ele., _tem_limite() (+3 more)

### Community 126 - "Professor"
Cohesion: 0.09
Nodes (23): gerenciar_turmas(), remover_professor(), ProfessorDAO, Professor, Cadastrar Professor Form, Hipótese: a foto continua acessível por URL depois de tirar a publicação., Hipótese: os contatos vazam na home antes de a publicação ser marcada., test_contatos_do_professor_so_aparecem_quando_publicados() (+15 more)

### Community 127 - "adm_bp.py"
Cohesion: 0.05
Nodes (64): _aluno_do_cpf_ou_painel(), aprovar_aluno(), aprovar_comprovante_manual(), arquivar_plano(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_aluno(), cadastrar_pagamento() (+56 more)

### Community 128 - "_chave_da_conta"
Cohesion: 0.40
Nodes (5): _chave_da_conta(), Chave de limite por CONTA, caindo no IP só para quem não está autenticado. A…, Alunos atrás do mesmo IP (o Wi-Fi da academia) não dividem a cota., test_limite_de_upload_e_por_conta_e_nao_por_ip(), test_visitante_sem_sessao_ainda_e_limitado_por_ip()

### Community 133 - "Academia"
Cohesion: 0.12
Nodes (21): configuracoes(), _pagina(), route, O administrador foi ao Mercado Pago e a autorização não voltou para cá? O state…, tentativa_sem_retorno(), editar_professor(), Academia, link_email() (+13 more)

### Community 134 - "rotulo_forma_pagamento"
Cohesion: 0.67
Nodes (3): Nome legível da forma de pagamento. Antes as telas usavam `|replace('_','…, rotulo_forma_pagamento(), test_rotulos_das_formas_do_mercado_pago()

### Community 135 - "prontidao.py"
Cohesion: 0.43
Nodes (6): banco_responde(), _consultar_banco(), Verificação de prontidão (/health/pronto): o banco e o Redis respondem agora?…, None quando o limite de requisições não usa Redis (memory:// em…, redis_responde(), verificar()

### Community 136 - "capturar_emails"
Cohesion: 0.67
Nodes (3): capturar_emails(), fixture, Intercepta o envio e devolve os e-mails que teriam saído, com os links.

### Community 140 - "backup.sh"
Cohesion: 1.00
Nodes (3): registrar(), reter(), backup.sh script

## Knowledge Gaps
- **105 isolated node(s):** `modal`, `input_senha`, `icone_senha`, `formularioPlano`, `campoPreco` (+100 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PagamentoDAO` connect `PagamentoDAO` to `route`, `.listar_por_aluno`, `test_mudanca_plano.py`, `test_pagamento_recusado.py`, `criar_aluno`, `pix_bp.py`, `AlunoDAO`, `checkout_bp.py`, `config.py`, `test_auditoria_seguranca.py`, `MatriculaDAO`, `logar_como_aluno`, `criar_pagamento`, `test_contratacao_plano.py`, `test_seguranca.py`, `Aluno`, `test_admin_mercado_pago.py`, `conftest.py`, `SolicitacaoMudancaPlano`, `test_perfil_e_foto.py`, `usuario_bp.py`, `test_plano_arquivo_promocao.py`, `adm_bp.py`?**
  _High betweenness centrality (0.120) - this node is a cross-community bridge._
- **Why does `AlunoDAO` connect `AlunoDAO` to `route`, `Aluno`, `turma_bp.py`, `test_mudanca_plano.py`, `criar_aluno`, `Plano`, `PagamentoDAO`, `google_login.py`, `test_perfil_e_foto.py`, `conftest.py`, `test_seguranca.py`, `usuario_bp.py`, `config.py`, `adm_bp.py`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `criar_aluno()` connect `criar_aluno` to `_chave_da_conta`, `.listar_por_aluno`, `test_mudanca_plano.py`, `test_mercado_pago_oauth.py`, `test_analytics.py`, `test_home_planos.py`, `AlunoDAO`, `test_auditoria_seguranca.py`, `test_seo.py`, `logar_como_admin`, `MatriculaDAO`, `PagamentoDAO`, `logar_como_aluno`, `criar_pagamento`, `test_contratacao_plano.py`, `test_conversao_home.py`, `test_seguranca.py`, `Aluno`, `test_admin_mercado_pago.py`, `conftest.py`, `test_paginas_erro.py`, `PlanoDAO`, `test_layouts.py`, `test_perfil_e_foto.py`, `test_plano_arquivo_promocao.py`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Are the 157 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 157 INFERRED edges - model-reasoned connections that need verification._
- **Are the 157 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 157 INFERRED edges - model-reasoned connections that need verification._
- **Are the 155 inferred relationships involving `criar_pagamento()` (e.g. with `PagamentoDAO` and `Pagamento`) actually correct?**
  _`criar_pagamento()` has 155 INFERRED edges - model-reasoned connections that need verification._
- **Are the 152 inferred relationships involving `logar_como_admin()` (e.g. with `test_admin_salva_atualiza_e_limpa_contatos()` and `test_csrf_configuracoes()`) actually correct?**
  _`logar_como_admin()` has 152 INFERRED edges - model-reasoned connections that need verification._