# Graph Report - SistemaEXTREMETEAM  (2026-09-30)

## Corpus Check
- 170 files · ~229,920 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2257 nodes · 5662 edges · 143 communities (128 shown, 15 thin omitted)
- Extraction: 80% EXTRACTED · 20% INFERRED · 0% AMBIGUOUS · INFERRED: 1132 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `83523880`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- criar_pagamento
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
- URLPublicaInvalida
- logar_como_admin
- MatriculaDAO
- gmail_conta.py
- convites.py
- PagamentoDAO
- pagamento_polling.test.cjs
- mercado_pago_conta.py
- test_checkout_rotas.py
- test_pix_rotas.py
- test_contratacao_plano.py
- d9e2f6a14c80_contatos_academia_perfis_professores.py
- test_conversao_home.py
- botao_ocupado.test.cjs
- test_seguranca.py
- checkout_abertura.test.cjs
- filtros_financeiro.js
- gunicorn.conf.py
- Pagamento
- fila_email.py
- test_migracao_cadastro_administrativo.py
- salvar_foto_perfil
- test_keep_alive.py
- _FakePaymentResource
- mercado_pago.py
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
- ResultadoContratacao
- Flask App Service (compose)
- cobrar_mensalidade
- Plano
- Etapa 1 — migrar páginas para os layouts (SEM mudar o visual)
- Etapas 4 a 6 — aluno, admin, professor (aplicar os componentes nas páginas)
- seo_bp.py
- Etapa 2 — biblioteca de componentes
- Etapa 3 — home com os planos + termos
- test_prontidao.py
- turma_bp.py
- editar_plano
- test_observabilidade.py
- usuario_bp.py
- PlanoDAO
- test_backup_scripts.py
- revogar_sessao_atual
- gerar_imagem_og.py
- _json_ld
- planoDAO.py
- parametrize
- _chave_lote
- Professor
- adm_bp.py
- conteudo_home.py
- TransporteEmMemoria
- route
- .criar_pelo_admin
- academia_bp.py
- .__init__
- prontidao.py
- capturar_emails
- postgres_pix
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

## Communities (143 total, 15 thin omitted)

### Community 0 - "criar_pagamento"
Cohesion: 0.07
Nodes (54): criar_pagamento(), logar_como_aluno(), Hipótese: se a resposta do MP trouxer um destino estranho, ele é salvo e…, Hipótese: cada clique cria uma cobrança nova no Mercado Pago., Hipótese: dá para injetar o valor pelo corpo do POST., Versão forte da sonda de IDOR: o alvo TEM arquivo, então um 200 seria vazamento., Verifica a trava antes da emissão e o reaproveitamento na próxima chamada.…, test_comprovante_de_outro_aluno_com_arquivo_real_nao_vaza() (+46 more)

### Community 1 - "extreme.css"
Cohesion: 0.05
Nodes (36): abrirmodal(), fechar(), icone_senha, input_senha, modal, mostrarSenha(), campoDuracao, campoPreco (+28 more)

### Community 2 - "planos.py"
Cohesion: 0.06
Nodes (42): cadeia_paga(), cartao_do_plano(), cobranca_a_pagar(), cobranca_em_decisao(), cobranca_pendente(), duracao_dias(), _duracao_por_extenso(), esta_inadimplente() (+34 more)

### Community 3 - ".listar_por_aluno"
Cohesion: 0.10
Nodes (34): Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, `pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -…, parametrize, test_admin_lanca_mensalidade_paga_no_cartao(), test_cobranca_criada_na_promocao_sai_pelo_preco_promocional(), test_fim_da_promocao_nao_muda_cobranca_ja_emitida(), _pagar(), plano_barato() (+26 more)

### Community 4 - "MercadoPagoIndisponivel"
Cohesion: 0.25
Nodes (9): buscar_pagamentos_por_referencia(), MercadoPagoIndisponivel, Exception, Lista os pagamentos que o Mercado Pago associa a uma external_reference. Usada…, Falha de transporte (timeout/DNS/conexao) ao falar com a API do Mercado Pago., test_busca_por_referencia_expoe_a_data_de_criacao(), test_buscar_pagamentos_por_referencia_falha_de_transporte(), test_buscar_pagamentos_por_referencia_normaliza_resultados() (+1 more)

### Community 5 - "test_mudanca_plano.py"
Cohesion: 0.14
Nodes (28): Persistência dos pedidos de troca de plano agendados para a próxima renovação., Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, Aplica um pedido agendado cujo período de origem já terminou sem renovação.…, SolicitacaoPlanoDAO, _agendar(), _pagar(), plano_barato(), fixture (+20 more)

### Community 6 - "test_pagamento_recusado.py"
Cohesion: 0.22
Nodes (23): _data_da_aprovacao(), Dia do pagamento no horário da academia. O Mercado Pago devolve as datas em…, _assinar(), _data_mp(), _eventos(), _mockar_mp(), _pagamento_mp(), _pix_criado() (+15 more)

### Community 7 - "criar_aluno"
Cohesion: 0.03
Nodes (82): _chave_da_conta(), Chave de limite por CONTA, caindo no IP só para quem não está autenticado. A…, _parece_busca_por_cpf(), O termo é um CPF, ou um pedaço dele, e não um nome que por acaso tem número?, Uma página de alunos já cadastrados, recortada e filtrada pelo banco. O painel…, criar_aluno(), test_aluno_existente_continua_entrando_normalmente(), test_busca_financeira_trata_curingas_como_texto() (+74 more)

### Community 9 - "test_mercado_pago_servico.py"
Cohesion: 0.09
Nodes (35): ambiente_mercado_pago(), Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, Diz se a integracao esta apontando para producao ou para o sandbox. Prioriza a…, validar_assinatura_webhook(), Hipótese: uma notificação capturada ontem pode ser reenviada hoje., `ts=nan` fazia a comparação da janela dar False e passava pela checagem de…, test_webhook_recusa_assinatura_antiga(), test_webhook_recusa_ts_nao_numerico_finito() (+27 more)

### Community 10 - "test_mercado_pago_oauth.py"
Cohesion: 0.09
Nodes (45): MercadoPagoConexao, Conta do Mercado Pago que a academia autorizou por OAuth. Uma linha só (a…, _agora(), _ajustar(), api_mp(), _conectar(), _dados_conexao(), oauth_env() (+37 more)

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

### Community 17 - "pix_bp.py"
Cohesion: 0.09
Nodes (30): _acesso_permitido(), criar_pix_mensalidade(), _forma_pagamento_confirmada(), _instante_utc(), _iso_utc(), _pagamento_ou_none(), _pix_expirado(), exempt (+22 more)

### Community 18 - "AlunoDAO"
Cohesion: 0.14
Nodes (41): _convidar_cadastro_existente(), Cadastro administrativo que alguém tentou recriar pelo formulário público. Em…, AlunoDAO, _matricular(), Cadastro de aluno pela administração, ativação de acesso e confirmação de…, test_admin_lanca_e_baixa_mensalidade_de_aluno_sem_acesso(), test_admin_matricula_aluno_sem_email_senha_nem_acesso(), test_admin_pode_deixar_cadastro_de_balcao_sem_usuario_e_sem_email() (+33 more)

### Community 19 - "test_mercado_pago_oauth_postgres.py"
Cohesion: 0.18
Nodes (8): postgres_mp(), fixture, Renovação do token OAuth com trava de linha real, opcional na suíte que usa…, _Resposta, test_dois_processos_perto_do_vencimento_gastam_o_refresh_token_uma_vez(), _migracao(), test_migracao_cria_a_tabela_igual_ao_modelo_e_e_reentrante(), test_migracao_encadeia_na_ultima_revisao_existente()

### Community 20 - "checkout_bp.py"
Cohesion: 0.10
Nodes (27): abrir_checkout(), _acesso_permitido(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), limitar_consulta_pagamento, limitar_criacao_pagamento, route (+19 more)

### Community 21 - "pix.js"
Cohesion: 0.33
Nodes (14): abrirPix(), alvoDoRotulo(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), liberarBotao(), limparConteudoAnterior() (+6 more)

### Community 22 - "config.py"
Cohesion: 0.31
Nodes (4): Decimal, Matricula, Regressão com trava de linha real, opcional na suíte que usa SQLite. Execute…, Instância descartável para conferir o redesign no navegador (porta 4002).…

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
Cohesion: 0.07
Nodes (40): _assinar(), logar_como_professor(), _pagamento_mp(), _preparar_para_conciliacao(), fixture, parametrize, Auditoria de segurança: sondas escritas para TENTAR quebrar as regras. Nenhum…, Hipótese: a sessão de professor é aceita nas rotas financeiras do aluno. (+32 more)

### Community 34 - "URLPublicaInvalida"
Cohesion: 0.08
Nodes (38): analytics_ativo(), id_analytics(), marcar_conversao_cadastro(), Google Analytics 4 opcional, só em página pública e só com consentimento. Sem…, Chamada no arranque: um ID malformado derruba a subida, como as demais…, Esta resposta pode carregar o GA4? Visitante, página pública indexável ou…, validar_configuracao(), iniciar() (+30 more)

### Community 35 - "logar_como_admin"
Cohesion: 0.10
Nodes (29): logar_como_admin(), test_convite_recusado_para_quem_ja_tem_acesso(), _preparar_state(), parametrize, test_aviso_de_autorizacao_vencida_aparece_uma_vez(), test_cada_conexao_iniciada_usa_state_novo(), test_callback_cancelado_no_mercado_pago_consome_o_state(), test_callback_com_erro_do_mercado_pago_que_nao_e_cancelamento() (+21 more)

### Community 36 - "MatriculaDAO"
Cohesion: 0.19
Nodes (16): MatriculaDAO, Presenca, impressao_credencial(), Resumo curto e não reversível do hash da senha, guardado na sessão. Nunca é a…, Valor que representa a credencial administrativa em vigor, ou None se não há…, referencia_credencial_admin(), parametrize, test_aluno_confirma_sua_frequencia() (+8 more)

### Community 37 - "gmail_conta.py"
Cohesion: 0.16
Nodes (18): GmailConexao, _access_token(), _cifrar(), _client_id(), _client_secret(), _decifrar(), enviar(), estado() (+10 more)

### Community 38 - "convites.py"
Cohesion: 0.14
Nodes (18): aluno_do_token(), ConviteIndisponivel, descartar(), enviar(), gerar_token(), _hash(), RuntimeError, Convite de acesso: como um cadastro criado pela administração vira uma conta.… (+10 more)

### Community 41 - "PagamentoDAO"
Cohesion: 0.09
Nodes (24): PagamentoDAO, Status como o painel deve LER, com o vencimento aplicado na própria consulta. A…, Carrega aluno e plano junto das mensalidades. O template do painel lê…, Lista completa (sem paginar). Mantida para relatórios e testes., Uma página de mensalidades, recortada pelo banco (LIMIT/OFFSET). O painel…, Totais do painel financeiro - sempre calculados no backend a partir do banco,…, True se já existe um Pix ou um checkout válido emitido para esta cobrança.…, Com uma troca já agendada, só dois planos fazem sentido num pedido de… (+16 more)

### Community 42 - "pagamento_polling.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 43 - "mercado_pago_conta.py"
Cohesion: 0.09
Nodes (39): access_token_vigente(), _agora(), ambiente_da_conexao(), _cifrar(), _client_id(), _client_secret(), ConexaoIlegivel, _configuracao_do_aplicativo() (+31 more)

### Community 44 - "test_checkout_rotas.py"
Cohesion: 0.16
Nodes (24): _mockar_preferencia(), parametrize, Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala…, _resposta_preferencia(), test_abertura_json_navega_sem_redirecionar_post_externo(), test_admin_tambem_pode_abrir_checkout(), test_aluno_cria_checkout_da_propria_mensalidade(), test_aluno_nao_cria_checkout_de_mensalidade_de_outro_aluno() (+16 more)

### Community 45 - "test_pix_rotas.py"
Cohesion: 0.19
Nodes (21): _agora_mercado_pago(), _assinar(), _resposta_consulta(), _resposta_criacao(), test_admin_tambem_pode_gerar_pix(), test_aluno_gera_pix_da_propria_mensalidade(), test_aluno_nao_acessa_mensalidade_de_outro_aluno(), test_falha_de_indisponibilidade_do_mp_retorna_503() (+13 more)

### Community 46 - "test_contratacao_plano.py"
Cohesion: 0.22
Nodes (8): test_area_do_aluno_renderiza_telas_independentes_do_menu(), test_escolher_plano_com_turma_cria_matricula(), test_escolher_plano_cria_mensalidade_e_redireciona_para_pix(), test_plano_atual_continua_disponivel_para_gerar_cobranca(), test_plano_invalido_nao_cria_mensalidade(), test_reenvio_da_contratacao_reutiliza_mensalidade(), test_turma_lotada_nao_vira_matricula_apos_pagamento(), test_valor_enviado_pelo_navegador_e_ignorado()

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
Nodes (26): test_upload_de_arquivo_disfarcado_e_recusado(), _cadastro_publico(), _imagem_jpeg(), _mensagem_da_resposta(), O `login` de um aluno pode ser o e-mail de outro; quem entra é decidido pela…, O ramo "par existe" não pode pagar a ida ao provedor dentro da requisição., Cadastro novo, CPF existente e e-mail existente respondem com a MESMA tela., Quem ainda controla a caixa antiga não pode assumir a conta depois da troca. (+18 more)

### Community 52 - "checkout_abertura.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 55 - "gunicorn.conf.py"
Cohesion: 0.25
Nodes (9): post_worker_init(), Hooks carregados pelo Gunicorn; nunca executados por flask db upgrade., worker_exit(), iniciar(), _laco(), parar(), Aciona a fila periodicamente durante a vida de um worker Gunicorn. Importar…, Inicia uma vez por processo, depois de carregar a aplicação e migrar o banco. (+1 more)

### Community 56 - "Pagamento"
Cohesion: 0.07
Nodes (21): cadastrar_pagamento(), _processar_status_mp(), Fonte unica de aprovacao, usada pelo webhook, pelo polling de status e pela…, A recusa (criada em `criada_em`, UTC) é de antes da última nova tentativa? Sem…, Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.…, Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda. O…, Primeiro dia não coberto por outra mensalidade do mesmo aluno., Define o período coberto por uma mensalidade que ainda não tem um (lançamento… (+13 more)

### Community 57 - "fila_email.py"
Cohesion: 0.06
Nodes (40): EmailPendente, espera_da_proxima_tentativa(), Fila de e-mails no banco. Aviso e cobrança coletivos saíam um a um dentro da…, contar_falhados(), contar_pendentes(), disparar(), enfileirar(), enfileirar_transacional() (+32 more)

### Community 58 - "test_migracao_cadastro_administrativo.py"
Cohesion: 0.40
Nodes (3): banco_antigo(), fixture, Verifica a migração em um banco isolado com o schema anterior e dados.

### Community 59 - "salvar_foto_perfil"
Cohesion: 0.12
Nodes (28): editar_professor(), ArquivoInvalido, caminho_arquivo(), _conferir_dimensoes(), _detectar_tipo_imagem_real(), ImagemGrandeDemais, _pasta(), Exception (+20 more)

### Community 60 - "test_keep_alive.py"
Cohesion: 0.16
Nodes (7): ambiente_limpo(), fixture, parametrize, Garante que o keep-alive fica desligado por padrão e só pinga a própria origem., test_intervalo_fica_dentro_da_faixa(), test_nao_liga_com_valor_negativo(), test_ping_so_considera_200_como_sucesso()

### Community 62 - "mercado_pago.py"
Cohesion: 0.10
Nodes (32): _base_url_opcional(), base_url_publica(), cancelar_pagamento(), criar_pagamento_pix(), criar_preferencia_checkout(), _erro_menciona(), _erro_menciona_expiracao(), _extrair_dados_pix() (+24 more)

### Community 63 - "test_arranque_seguranca.py"
Cohesion: 0.22
Nodes (14): _env_arranque(), Validações feitas por servidor.py no arranque (COOKIE_SECURE, TRUSTED_HOSTS,…, `python -m servicos.credenciais`: o hash sai entre aspas simples. O hash do…, Desenvolvimento local sem HTTPS (sem Caddy) não pode ficar travado., _rodar(), test_arranque_falha_com_cookie_secure_false_e_app_base_url_https(), test_arranque_falha_com_cookie_secure_invalido(), test_arranque_falha_sem_trusted_hosts() (+6 more)

### Community 64 - "Aluno"
Cohesion: 0.11
Nodes (11): Aluno, Se existe uma conta de acesso, e não se o aluno está em dia ou matriculado.…, Convite de acesso já enviado e ainda não usado (a validade é checada na rota)., Chave do estado da CONTA - nunca da situação financeira nem da matrícula., test_admin_nao_pode_apagar_o_usuario_de_uma_conta_ativa(), test_cadastro_publico_recusa_confirmacao_diferente(), test_cadastro_publico_recusa_confirmacao_vazia(), _dados_cadastro() (+3 more)

### Community 66 - "autorizacao.py"
Cohesion: 0.14
Nodes (21): _acesso_permitido(), detalhe_turma(), foto_professor(), registrar_presenca(), confirmar_presenca(), PresencaDAO, aluno_autorizado(), aluno_requerido() (+13 more)

### Community 67 - "servidor.py"
Cohesion: 0.14
Nodes (20): after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, context_processor, errorhandler, formatar_moeda(), Formata um valor em reais no padrão brasileiro: R$ 1.080,00. Usado como filtro…, acesso_negado() (+12 more)

### Community 69 - "ConfiguracaoInvalida"
Cohesion: 0.30
Nodes (11): _autorizacao_valida(), callback(), conectar(), desconectar(), limit, route, O state devolvido é o que ESTA sessão emitiu, há pouco tempo?, Só monta o state/PKCE na sessão e manda o administrador ao Mercado Pago. É um… (+3 more)

### Community 70 - "test_admin_mercado_pago.py"
Cohesion: 0.15
Nodes (17): Nome legível da forma de pagamento. Antes as telas usavam `|replace('_','…, rotulo_forma_pagamento(), _aprovado_no_checkout(), Painel do admin com mensalidades do Mercado Pago: formas de pagamento,…, Cartão/boleto: a preferência existe, o webhook ainda não trouxe o payment_id., _so_com_checkout(), test_admin_muda_o_status_sem_perder_a_forma_do_mercado_pago(), test_admin_nao_grava_forma_inventada() (+9 more)

### Community 71 - "pagina_login"
Cohesion: 0.12
Nodes (16): pagina_login(), iniciar_sessao(), Grava na sessão atual a credencial em vigor (login ou troca de senha bem-…, Dá um identificador à sessão recém-aberta, para o logout poder revogá-la.…, registrar_credencial(), admin_configurado(), comparar_em_tempo_constante(), credencial_admin_confere() (+8 more)

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
Cohesion: 0.12
Nodes (7): Pagina, _paginar(), Uma fatia de resultados já recortada pelo banco, com o que a navegação precisa., Uma página existe mesmo quando está vazia. Sem isto, `__len__` fazia `{% if…, Aplica LIMIT/OFFSET e conta o total numa consulta separada e barata. A contagem…, `__len__` fazia `{% if pagina %}` ser falso numa página sem itens, escondendo…, test_pagina_vazia_ainda_mostra_a_navegacao()

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
Cohesion: 0.29
Nodes (6): Controles verificados, Histórico de auditorias, Pendências não relacionadas a segurança, Relatório de segurança — Sistema Extreme Team, Situação atual (22/09/2026 — 2ª rodada), Validação executada em 22/09/2026

### Community 94 - "test_seo.py"
Cohesion: 0.13
Nodes (18): _head(), parametrize, SEO técnico: robots.txt, sitemap, títulos, meta tags, noindex e JSON-LD da home., _robots(), test_area_do_admin_sai_do_indice(), test_area_do_aluno_sai_do_indice(), test_area_do_professor_sai_do_indice(), test_canonical_ignora_query_string() (+10 more)

### Community 95 - "test_email_componentes.py"
Cohesion: 0.33
Nodes (7): E-mails: base com a logo oficial e componentes seguros para cliente de e-mail…, _render(), _sem_recursos_externos(), test_base_sem_url_publica_cai_para_o_nome_em_texto(), test_base_usa_a_logo_quando_ha_url_publica(), test_botao_do_email_usa_o_ouro_do_sistema(), test_cartao_de_resumo_com_badge()

### Community 96 - ".buscar_por_id"
Cohesion: 0.25
Nodes (19): _assinar(), _pagamento_mp(), _preparar_retorno(), Pix aberto e checkout concluído ao mesmo tempo: a consulta pelo…, test_retorno_com_aprovacao_confirmada_marca_pago(), test_retorno_com_mp_indisponivel_avisa_sem_mudar_status(), test_retorno_de_boleto_avisa_sobre_o_prazo(), test_retorno_de_sucesso_nao_marca_pago_sem_confirmacao() (+11 more)

### Community 97 - "painel_adm"
Cohesion: 0.15
Nodes (7): painel_adm(), Apaga um plano que nunca foi usado. True, None (não existe) ou False (em uso)., Os planos à venda: home, perfil do aluno e formulários de contratação., Planos que algum registro referencia: mensalidade, cadastro de aluno ou pedido…, Quantos alunos a academia tem, sem filtro de busca. O card do topo do painel é…, home(), test_plano_so_no_cadastro_do_aluno_tambem_conta_como_em_uso()

### Community 98 - "test_layouts.py"
Cohesion: 0.29
Nodes (8): _conferir_head_comum(), parametrize, Layouts base (templates/layouts/) e toasts. Cada página estende o layout da sua…, test_area_do_aluno_carrega_o_layout(), test_flash_de_erro_vira_toast_que_nao_some_sozinho(), test_paginas_publicas_carregam_o_head_comum(), test_painel_admin_carrega_o_layout_admin(), test_toda_pagina_estende_um_layout()

### Community 99 - "Academia"
Cohesion: 0.22
Nodes (9): Academia, parametrize, test_admin_salva_atualiza_e_limpa_contatos(), test_configuracoes_exigem_admin(), test_contatos_invalidos(), test_csrf_configuracoes(), test_erro_preserva_formulario_e_dados_salvos(), test_link_email_preserva_caracteres_do_endereco() (+1 more)

### Community 102 - "Flask App Service (compose)"
Cohesion: 0.22
Nodes (9): Flask App Service (compose), Postgres DB Service (compose), postgres_data Volume, Flask, Flask-SQLAlchemy, Gunicorn, psycopg2-binary, python-dotenv (+1 more)

### Community 103 - "cobrar_mensalidade"
Cohesion: 0.20
Nodes (10): cobrar_mensalidade(), _esta_inadimplente(), _paragrafos_cobranca(), Situação de todos os alunos ativos com UMA consulta de mensalidades., Quem realmente deve receber cobrança: nem quem está com o plano ativo, nem quem…, Texto da cobrança montado a partir da situação real, não de campos guardados: o…, _situacao_do_aluno(), _situacoes_dos_ativos() (+2 more)

### Community 104 - "Plano"
Cohesion: 0.28
Nodes (3): Plano, Preço de uma cobrança criada em `hoje`., Cadastrar Plano Form

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

### Community 113 - "turma_bp.py"
Cohesion: 0.16
Nodes (21): callback(), conectar(), desconectar(), limit, route, _voltar(), cadastrar_professor(), cadastrar_turma() (+13 more)

### Community 115 - "editar_plano"
Cohesion: 0.20
Nodes (10): cadastrar_plano(), editar_plano(), _ler_plano(), _ler_promocao(), 80', '80.5', '80,50' ou '1.234,56' -> Decimal. None se vazio; ValueError se…, Nome, preço e duração do formulário de plano: `(campos, None)` ou `(None,…, Preço promocional e período: `(campos, None)` ou `(None, erro)`. Os três campos…, Nome, preço, duração e promoção. Vale para as cobranças criadas daqui em… (+2 more)

### Community 116 - "test_observabilidade.py"
Cohesion: 0.18
Nodes (18): before_breadcrumb(), before_send(), iniciar_sentry(), _limpar(), mascarar(), Rastreamento de erros opcional com Sentry. Sem `SENTRY_DSN`, nada é importado…, _evento(), fixture (+10 more)

### Community 117 - "usuario_bp.py"
Cohesion: 0.06
Nodes (70): _acesso_permitido_pagamento(), alterar_senha_perfil(), _aluno_da_sessao(), _aluno_por_token(), ativar_acesso(), atualizar_dados_perfil(), cadastro_obrigado(), _cadastro_recebido() (+62 more)

### Community 118 - "PlanoDAO"
Cohesion: 0.13
Nodes (33): _plano_do_formulario(), PlanoDAO, Tira o plano de venda. Devolve `(plano, pedidos_cancelados)`, ou None. Pedidos…, _pagar(), _plano(), _promocao(), parametrize, Plano fora de venda (arquivar/reativar/excluir), edição e promoção com período.… (+25 more)

### Community 119 - "test_backup_scripts.py"
Cohesion: 0.27
Nodes (11): ambiente(), _executavel(), fixture, Scripts de backup (tools/backup/): retenção, falha sem backup "pela metade" e a…, _rodar(), test_backup_gera_dump_e_uploads_e_aplica_a_retencao(), test_dump_ilegivel_nao_vira_backup(), test_restaurar_em_banco_descartavel_e_extrair_uploads() (+3 more)

### Community 120 - "revogar_sessao_atual"
Cohesion: 0.29
Nodes (7): Registra a sessão como encerrada: cópias antigas do cookie deixam de valer.…, revogar_sessao_atual(), health(), health_pronto(), logout(), exempt, route

### Community 122 - "_json_ld"
Cohesion: 0.38
Nodes (7): _json_ld(), Nenhum campo do JSON-LD pode sair nulo, vazio ou só com espaços., _sem_vazios(), test_json_ld_completo_a_partir_da_academia(), test_json_ld_nao_deixa_texto_do_painel_fechar_o_script(), test_json_ld_omite_campos_vazios(), test_json_ld_sem_dados_da_academia_so_tem_o_basico()

### Community 124 - "parametrize"
Cohesion: 0.40
Nodes (5): parametrize, test_confirmacao_aceita_unicode(), test_matricula_valida_dados_no_servidor(), test_novos_formularios_exigem_csrf(), test_rotas_de_matricula_e_convite_sao_so_do_admin()

### Community 125 - "_chave_lote"
Cohesion: 0.50
Nodes (4): _chave_lote(), Identidade de um aviso: o conteúdo MAIS o dia. Só o conteúdo não serve. Um…, A chave de idempotência inclui o dia. Só o conteúdo suprimiria para sempre um…, test_o_mesmo_aviso_pode_ser_enviado_de_novo_em_outro_dia()

### Community 126 - "Professor"
Cohesion: 0.08
Nodes (31): ProfessorDAO, Professor, test_publicacao_professor_nao_expoe_contatos_sem_permissao(), Hipótese: a foto continua acessível por URL depois de tirar a publicação., Hipótese: os contatos vazam na home antes de a publicação ser marcada., Sonda: a data vem da query string e é convertida sem tratamento., test_contatos_do_professor_so_aparecem_quando_publicados(), test_data_invalida_na_turma_nao_derruba_a_rota() (+23 more)

### Community 127 - "adm_bp.py"
Cohesion: 0.10
Nodes (42): _aluno_do_cpf_ou_painel(), aprovar_aluno(), aprovar_comprovante_manual(), arquivar_plano(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_aluno(), cancelar_mudanca_plano_admin() (+34 more)

### Community 128 - "conteudo_home.py"
Cohesion: 0.50
Nodes (3): faq_estruturado(), Textos editáveis da página inicial: perguntas frequentes e prazos de…, JSON-LD FAQPage com exatamente as perguntas mostradas na página.

### Community 130 - "route"
Cohesion: 0.67
Nodes (3): route, vitrine(), vitrine_enviar()

### Community 133 - "academia_bp.py"
Cohesion: 0.24
Nodes (10): configuracoes(), _pagina(), route, O administrador foi ao Mercado Pago e a autorização não voltou para cá? O state…, tentativa_sem_retorno(), link_email(), Normalização de contatos profissionais antes de montar links públicos., validar_email() (+2 more)

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
- **134 isolated node(s):** `modal`, `input_senha`, `icone_senha`, `formularioPlano`, `campoPreco` (+129 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PagamentoDAO` connect `PagamentoDAO` to `criar_pagamento`, `.listar_por_aluno`, `test_mudanca_plano.py`, `test_pagamento_recusado.py`, `criar_aluno`, `pix_bp.py`, `AlunoDAO`, `checkout_bp.py`, `config.py`, `test_auditoria_seguranca.py`, `MatriculaDAO`, `test_checkout_rotas.py`, `test_pix_rotas.py`, `test_contratacao_plano.py`, `test_seguranca.py`, `Pagamento`, `Aluno`, `test_admin_mercado_pago.py`, `conftest.py`, `.buscar_por_id`, `ResultadoContratacao`, `cobrar_mensalidade`, `usuario_bp.py`, `PlanoDAO`, `planoDAO.py`, `adm_bp.py`?**
  _High betweenness centrality (0.114) - this node is a cross-community bridge._
- **Why does `AlunoDAO` connect `AlunoDAO` to `Aluno`, `painel_adm`, `autorizacao.py`, `.criar_pelo_admin`, `cobrar_mensalidade`, `pagina_login`, `PagamentoDAO`, `google_login.py`, `criar_aluno`, `Plano`, `turma_bp.py`, `conftest.py`, `test_seguranca.py`, `usuario_bp.py`, `config.py`, `Pagamento`, `Professor`, `adm_bp.py`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `criar_aluno()` connect `criar_aluno` to `criar_pagamento`, `.listar_por_aluno`, `test_mudanca_plano.py`, `test_mercado_pago_oauth.py`, `test_analytics.py`, `test_home_planos.py`, `AlunoDAO`, `test_auditoria_seguranca.py`, `logar_como_admin`, `MatriculaDAO`, `PagamentoDAO`, `test_checkout_rotas.py`, `test_pix_rotas.py`, `test_contratacao_plano.py`, `test_conversao_home.py`, `test_seguranca.py`, `Aluno`, `conftest.py`, `test_paginas_erro.py`, `test_seo.py`, `painel_adm`, `test_layouts.py`, `PlanoDAO`, `parametrize`, `Professor`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Are the 157 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 157 INFERRED edges - model-reasoned connections that need verification._
- **Are the 157 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 157 INFERRED edges - model-reasoned connections that need verification._
- **Are the 155 inferred relationships involving `criar_pagamento()` (e.g. with `PagamentoDAO` and `Pagamento`) actually correct?**
  _`criar_pagamento()` has 155 INFERRED edges - model-reasoned connections that need verification._
- **Are the 152 inferred relationships involving `logar_como_admin()` (e.g. with `test_admin_salva_atualiza_e_limpa_contatos()` and `test_csrf_configuracoes()`) actually correct?**
  _`logar_como_admin()` has 152 INFERRED edges - model-reasoned connections that need verification._