# Graph Report - SistemaEXTREMETEAM  (2026-09-27)

## Corpus Check
- 142 files · ~201,921 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1846 nodes · 4743 edges · 118 communities (109 shown, 9 thin omitted)
- Extraction: 80% EXTRACTED · 20% INFERRED · 0% AMBIGUOUS · INFERRED: 971 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5a99fa67`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- route
- Aluno Profile Page
- test_home_planos.py
- .listar_por_aluno
- criar_pagamento
- test_mudanca_plano.py
- AlunoDAO
- criar_aluno
- SistemaEXTREMETEAM Project
- test_mercado_pago_servico.py
- test_mercado_pago_oauth.py
- Professor
- test_migracao_checkout.py
- checkout.js
- CLAUDE.md
- planos.py
- MercadoPagoIndisponivel
- logar_como_admin
- PagamentoDAO
- checkout_bp.py
- pix.js
- config.py
- env.py
- pagamento.js
- c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py
- varredura.mjs
- 896e70afc9c5_adiciona_foto_e_graduacao_do_aluno_.py
- test_auditoria_seguranca.py
- turma_bp.py
- usuario_e_admin
- MatriculaDAO
- gmail_conta.py
- URLPublicaInvalida
- .listar_paginado
- pagamento_polling.test.cjs
- mercado_pago_conta.py
- logar_como_aluno
- test_pix_rotas.py
- PagamentoEvento
- d9e2f6a14c80_contatos_academia_perfis_professores.py
- ProfessorDAO
- botao_ocupado.test.cjs
- test_seguranca.py
- checkout_abertura.test.cjs
- filtros_financeiro.js
- gunicorn.conf.py
- ConfiguracaoInvalida
- fila_email.py
- test_migracao_cadastro_administrativo.py
- salvar_foto_perfil
- test_keep_alive.py
- Academia
- mercado_pago.py
- test_arranque_seguranca.py
- Aluno
- autorizacao.py
- servidor.py
- test_retorno_ignora_status_aprovado_da_query_string
- pagina_cadastro
- PlanoDAO
- credenciais.py
- shot.mjs
- Pagamento
- usuario_bp.py
- Pagina
- _parece_busca_por_cpf
- e4b7c2a91d35_cadastro_administrativo_e_convite_de_acesso.py
- a1f0c3e75b92_schema_inicial.py
- Contrato do redesign — SistemaEXTREMETEAM
- _chave_da_conta
- test_sessao_revogada.py
- Skills Disponíveis
- componentes.js
- test_paginas_erro.py
- adm_bp.py
- Relatório de segurança — Sistema Extreme Team
- gmail_oauth_bp.py
- test_email_componentes.py
- test_perfil_e_foto.py
- test_email_gmail.py
- test_layouts.py
- conftest.py
- erro_validacao_senha
- Flask App Service (compose)
- SolicitacaoMudancaPlano
- Plano
- Etapa 1 — migrar páginas para os layouts (SEM mudar o visual)
- Etapas 4 a 6 — aluno, admin, professor (aplicar os componentes nas páginas)
- enviar_convite_acesso
- Etapa 2 — biblioteca de componentes
- Etapa 3 — home com os planos + termos
- _FakePaymentResource
- test_pedido_publico_nao_invalida_convite_ainda_valido
- test_comprovante_de_outro_aluno_com_arquivo_real_nao_vaza
- capturar_emails
- test_trocar_a_credencial_do_admin_encerra_a_sessao_administrativa

## God Nodes (most connected - your core abstractions)
1. `PagamentoDAO` - 202 edges
2. `criar_pagamento()` - 142 edges
3. `criar_aluno()` - 140 edges
4. `logar_como_aluno()` - 119 edges
5. `logar_como_admin()` - 116 edges
6. `AlunoDAO` - 93 edges
7. `Aluno` - 59 edges
8. `MercadoPagoIndisponivel` - 41 edges
9. `Professor` - 38 edges
10. `ProfessorDAO` - 36 edges

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

## Communities (118 total, 9 thin omitted)

### Community 0 - "route"
Cohesion: 0.16
Nodes (23): alterar_senha_perfil(), _aluno_da_sessao(), _aluno_por_token(), atualizar_dados_perfil(), cancelar_mudanca_plano(), confirmar_email(), confirmar_presenca(), enviar_comprovante_manual_aluno() (+15 more)

### Community 1 - "Aluno Profile Page"
Cohesion: 0.05
Nodes (37): abrirmodal(), fechar(), icone_senha, input_senha, modal, mostrarSenha(), campoDuracao, campoPreco (+29 more)

### Community 2 - "test_home_planos.py"
Cohesion: 0.16
Nodes (18): cadastrar_plano(), Marca o plano em destaque da página inicial, desmarcando qualquer outro.…, preco(), Planos da página inicial, prontos para `components/cartao_plano.html`. O preço…, vitrine_planos(), _plano(), _quatro_planos(), Planos na página inicial: cálculo (servicos/planos.vitrine_planos), destaque… (+10 more)

### Community 3 - ".listar_por_aluno"
Cohesion: 0.08
Nodes (37): Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, Com uma troca já agendada, só dois planos fazem sentido num pedido de…, A cobrança do período seguinte tem de nascer no plano que o aluno agendou.…, `pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -…, forma_pagamento vem do que o Mercado Pago confirmou na consulta à API ('pix',…, _pagar(), plano_barato() (+29 more)

### Community 4 - "criar_pagamento"
Cohesion: 0.10
Nodes (31): True se já existe um Pix ou um checkout válido emitido para esta cobrança.…, True se a cobrança Pix já gerada para este pagamento ainda pode ser…, criar_pagamento(), test_retorno_sem_sessao_vai_para_o_login(), provider_payment_id sozinho não basta: pagamentos do Checkout Pro…, test_marcar_pago_via_webhook_sincroniza_mensalidade_do_aluno(), test_marcar_reembolsado_via_webhook_sincroniza_mensalidade_do_aluno(), test_mensalidade_destaque_prioriza_a_mais_proxima_de_vencer() (+23 more)

### Community 5 - "test_mudanca_plano.py"
Cohesion: 0.14
Nodes (27): Persistência dos pedidos de troca de plano agendados para a próxima renovação., Aplica um pedido agendado cujo período de origem já terminou sem renovação.…, SolicitacaoPlanoDAO, _agendar(), _pagar(), plano_barato(), fixture, Mudança para um plano mais barato agendada para a próxima renovação. Regra… (+19 more)

### Community 6 - "AlunoDAO"
Cohesion: 0.18
Nodes (15): AlunoDAO, test_admin_lanca_e_baixa_mensalidade_de_aluno_sem_acesso(), test_admin_matricula_aluno_sem_email_senha_nem_acesso(), test_admin_pode_deixar_cadastro_de_balcao_sem_usuario_e_sem_email(), test_admin_rejeita_status_financeiro_desconhecido(), test_cadastro_publico_com_cpf_sem_email_no_cadastro_nao_envia_nada(), test_cadastro_publico_sem_conflito_continua_criando_a_conta(), test_convite_com_email_duplicado_nao_envia_link() (+7 more)

### Community 7 - "criar_aluno"
Cohesion: 0.05
Nodes (52): Totais do painel financeiro - sempre calculados no backend a partir do banco,…, Uma página de alunos já cadastrados, recortada e filtrada pelo banco. O painel…, criar_aluno(), test_aluno_existente_continua_entrando_normalmente(), _contar_selects_em_alunos(), _credencial(), Regressões da auditoria de segurança, desempenho e confiabilidade. Cada caso…, Head-of-line blocking: a primeira linha falhando não pode impedir as seguintes.… (+44 more)

### Community 9 - "test_mercado_pago_servico.py"
Cohesion: 0.09
Nodes (34): ambiente_mercado_pago(), Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, Diz se a integracao esta apontando para producao ou para o sandbox. Prioriza a…, validar_assinatura_webhook(), Hipótese: uma notificação capturada ontem pode ser reenviada hoje., `ts=nan` fazia a comparação da janela dar False e passava pela checagem de…, test_webhook_recusa_assinatura_antiga(), test_webhook_recusa_ts_nao_numerico_finito() (+26 more)

### Community 10 - "test_mercado_pago_oauth.py"
Cohesion: 0.05
Nodes (70): MercadoPagoConexao, Conta do Mercado Pago que a academia autorizou por OAuth. Uma linha só (a…, _sdk(), _agora(), _ajustar(), api_mp(), _conectar(), _dados_conexao() (+62 more)

### Community 11 - "Professor"
Cohesion: 0.17
Nodes (7): Professor, Cadastrar Professor Form, test_publicacao_professor_nao_expoe_contatos_sem_permissao(), Hipótese: a foto continua acessível por URL depois de tirar a publicação., Hipótese: os contatos vazam na home antes de a publicação ser marcada., test_contatos_do_professor_so_aparecem_quando_publicados(), test_foto_do_professor_some_ao_despublicar()

### Community 12 - "test_migracao_checkout.py"
Cohesion: 0.31
Nodes (8): _colunas(), conexao(), migracao(), fixture, Exercita a migração dos campos do Checkout Pro de verdade (upgrade e…, _rodar(), test_downgrade_remove_exatamente_o_que_o_upgrade_criou(), test_upgrade_adiciona_as_colunas_e_preserva_linhas_antigas()

### Community 14 - "checkout.js"
Cohesion: 0.47
Nodes (4): cancelarAberturas(), consultar(), finalizarAbertura(), parar()

### Community 16 - "planos.py"
Cohesion: 0.06
Nodes (36): cadeia_paga(), cobranca_a_pagar(), cobranca_em_decisao(), cobranca_pendente(), duracao_dias(), _duracao_por_extenso(), esta_inadimplente(), fim_periodo_comprometido() (+28 more)

### Community 17 - "MercadoPagoIndisponivel"
Cohesion: 0.08
Nodes (41): _acesso_permitido(), criar_pix_mensalidade(), _forma_pagamento_confirmada(), _pagamento_mp_mais_relevante(), _pagamento_ou_none(), _pix_expirado(), _processar_status_mp(), limitar_consulta_pagamento (+33 more)

### Community 18 - "logar_como_admin"
Cohesion: 0.12
Nodes (39): logar_como_admin(), _matricular(), parametrize, Cadastro de aluno pela administração, ativação de acesso e confirmação de…, test_admin_nao_pode_apagar_o_usuario_de_uma_conta_ativa(), test_admin_rejeita_valor_financeiro_invalido(), test_aluno_sem_acesso_nao_entra_com_cpf_nem_com_qualquer_senha(), test_ativacao_com_senha_unicode() (+31 more)

### Community 19 - "PagamentoDAO"
Cohesion: 0.15
Nodes (32): PagamentoDAO, Solta a preferência atual para que a próxima tentativa crie uma nova. Nunca…, Hipótese: se a resposta do MP trouxer um destino estranho, ele é salvo e…, test_url_hostil_do_mercado_pago_nao_e_persistida(), _assinar(), _pagamento_mp(), _preparar_retorno(), Pix aberto e checkout concluído ao mesmo tempo: a consulta pelo… (+24 more)

### Community 20 - "checkout_bp.py"
Cohesion: 0.11
Nodes (22): abrir_checkout(), _acesso_permitido(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), limitar_consulta_pagamento, limitar_criacao_pagamento, route (+14 more)

### Community 21 - "pix.js"
Cohesion: 0.33
Nodes (14): abrirPix(), alvoDoRotulo(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), liberarBotao(), limparConteudoAnterior() (+6 more)

### Community 22 - "config.py"
Cohesion: 0.22
Nodes (7): _paginar(), Aplica LIMIT/OFFSET e conta o total numa consulta separada e barata. A contagem…, Matricula, route, Instância descartável para conferir o redesign no navegador (porta 4002).…, vitrine(), vitrine_enviar()

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
Nodes (46): Só abre o checkout HTTPS do Mercado Pago Brasil, inclusive no sandbox., url_checkout_permitida(), _assinar(), logar_como_professor(), _pagamento_mp(), _preparar_para_conciliacao(), fixture, parametrize (+38 more)

### Community 34 - "turma_bp.py"
Cohesion: 0.18
Nodes (15): _acesso_permitido(), cadastrar_professor(), cadastrar_turma(), desmatricular_aluno(), detalhe_turma(), gerenciar_turmas(), matricular_aluno(), painel_professor() (+7 more)

### Community 35 - "usuario_e_admin"
Cohesion: 0.14
Nodes (20): aprovar_aluno(), aprovar_comprovante_manual(), ativar_aluno(), cancelar_mudanca_plano_admin(), _data_do_form(), desativar_aluno(), destacar_plano(), enviar_foto_aluno() (+12 more)

### Community 36 - "MatriculaDAO"
Cohesion: 0.25
Nodes (13): MatriculaDAO, Presenca, impressao_credencial(), Resumo curto e não reversível do hash da senha, guardado na sessão. Nunca é a…, parametrize, test_aluno_confirma_sua_frequencia(), test_consulta_com_data_invalida_exibe_hoje_e_aviso(), test_consulta_com_data_valida_preserva_data_selecionada() (+5 more)

### Community 37 - "gmail_conta.py"
Cohesion: 0.26
Nodes (15): GmailConexao, _access_token(), _cifrar(), _client_id(), _client_secret(), _decifrar(), enviar(), estado() (+7 more)

### Community 38 - "URLPublicaInvalida"
Cohesion: 0.10
Nodes (32): aluno_do_token(), ConviteIndisponivel, descartar(), enviar(), gerar_token(), _hash(), RuntimeError, Convite de acesso: como um cadastro criado pela administração vira uma conta.… (+24 more)

### Community 41 - ".listar_paginado"
Cohesion: 0.20
Nodes (6): Status como o painel deve LER, com o vencimento aplicado na própria consulta. A…, Carrega aluno e plano junto das mensalidades. O template do painel lê…, Lista completa (sem paginar). Mantida para relatórios e testes., Uma página de mensalidades, recortada pelo banco (LIMIT/OFFSET). O painel…, test_listar_filtrado_por_status_e_busca_de_aluno(), test_financeiro_pagina_no_banco_sem_carregar_tudo()

### Community 42 - "pagamento_polling.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 43 - "mercado_pago_conta.py"
Cohesion: 0.10
Nodes (35): access_token_vigente(), _agora(), ambiente_da_conexao(), _cifrar(), _client_id(), _client_secret(), ConexaoIlegivel, _decifrar() (+27 more)

### Community 44 - "logar_como_aluno"
Cohesion: 0.09
Nodes (46): logar_como_aluno(), _mockar_preferencia(), parametrize, Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala…, Um boleto pendente do Checkout Pro grava provider_payment_id, mas não é Pix:…, _resposta_preferencia(), test_abertura_json_navega_sem_redirecionar_post_externo(), test_admin_tambem_pode_abrir_checkout() (+38 more)

### Community 45 - "test_pix_rotas.py"
Cohesion: 0.21
Nodes (19): _assinar(), _resposta_consulta(), _resposta_criacao(), test_admin_tambem_pode_gerar_pix(), test_aluno_gera_pix_da_propria_mensalidade(), test_aluno_nao_acessa_mensalidade_de_outro_aluno(), test_falha_de_indisponibilidade_do_mp_retorna_503(), test_impede_cobranca_duplicada_em_chamadas_consecutivas() (+11 more)

### Community 46 - "PagamentoEvento"
Cohesion: 0.14
Nodes (8): Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda. O…, Primeiro dia não coberto por outra mensalidade do mesmo aluno., Define o período coberto por uma mensalidade que ainda não tem um (lançamento…, Abre o período de acesso no momento em que o pagamento é confirmado. Se a…, Reescreve os campos denormalizados do aluno a partir das mensalidades.…, Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.…, PagamentoEvento, Histórico de auditoria de uma mensalidade (nunca grava credenciais ou dados…

### Community 47 - "d9e2f6a14c80_contatos_academia_perfis_professores.py"
Cohesion: 0.83
Nodes (3): _campos_professor(), downgrade(), upgrade()

### Community 49 - "ProfessorDAO"
Cohesion: 0.17
Nodes (16): remover_professor(), ProfessorDAO, _foto(), pasta_fotos(), professor(), fixture, parametrize, test_admin_salva_perfil_sem_alterar_acesso() (+8 more)

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

### Community 56 - "ConfiguracaoInvalida"
Cohesion: 0.30
Nodes (11): _autorizacao_valida(), callback(), conectar(), desconectar(), limit, route, O state devolvido é o que ESTA sessão emitiu, há pouco tempo?, Só monta o state/PKCE na sessão e manda o administrador ao Mercado Pago. É um… (+3 more)

### Community 57 - "fila_email.py"
Cohesion: 0.06
Nodes (40): EmailPendente, espera_da_proxima_tentativa(), Fila de e-mails no banco. Aviso e cobrança coletivos saíam um a um dentro da…, contar_falhados(), contar_pendentes(), disparar(), enfileirar(), enfileirar_transacional() (+32 more)

### Community 58 - "test_migracao_cadastro_administrativo.py"
Cohesion: 0.40
Nodes (3): banco_antigo(), fixture, Verifica a migração em um banco isolado com o schema anterior e dados.

### Community 59 - "salvar_foto_perfil"
Cohesion: 0.10
Nodes (30): ArquivoInvalido, _conferir_dimensoes(), _detectar_tipo_imagem_real(), ImagemGrandeDemais, _pasta(), Exception, _raiz_uploads(), Armazenamento de arquivos enviados por usuários (fotos de perfil, comprovantes… (+22 more)

### Community 60 - "test_keep_alive.py"
Cohesion: 0.16
Nodes (7): ambiente_limpo(), fixture, parametrize, Garante que o keep-alive fica desligado por padrão e só pinga a própria origem., test_intervalo_fica_dentro_da_faixa(), test_nao_liga_com_valor_negativo(), test_ping_so_considera_200_como_sucesso()

### Community 61 - "Academia"
Cohesion: 0.14
Nodes (18): configuracoes(), _pagina(), route, editar_professor(), Academia, link_email(), Normalização de contatos profissionais antes de montar links públicos., validar_email() (+10 more)

### Community 62 - "mercado_pago.py"
Cohesion: 0.15
Nodes (22): _base_url_opcional(), base_url_publica(), criar_pagamento_pix(), criar_preferencia_checkout(), _erro_menciona(), _erro_menciona_expiracao(), _extrair_dados_pix(), _normalizar_pagamento() (+14 more)

### Community 63 - "test_arranque_seguranca.py"
Cohesion: 0.22
Nodes (14): _env_arranque(), Validações feitas por servidor.py no arranque (COOKIE_SECURE, TRUSTED_HOSTS,…, `python -m servicos.credenciais`: o hash sai entre aspas simples. O hash do…, Desenvolvimento local sem HTTPS (sem Caddy) não pode ficar travado., _rodar(), test_arranque_falha_com_cookie_secure_false_e_app_base_url_https(), test_arranque_falha_com_cookie_secure_invalido(), test_arranque_falha_sem_trusted_hosts() (+6 more)

### Community 64 - "Aluno"
Cohesion: 0.13
Nodes (8): Matrícula feita no balcão: sem login, sem senha e sem convite de acesso. Nasce…, Aluno, Se existe uma conta de acesso, e não se o aluno está em dia ou matriculado.…, Convite de acesso já enviado e ainda não usado (a validade é checada na rota)., Chave do estado da CONTA - nunca da situação financeira nem da matrícula., _dados_cadastro(), test_cadastro_exige_aceite_do_termo(), test_cadastro_registra_versao_e_horario_do_aceite()

### Community 66 - "autorizacao.py"
Cohesion: 0.14
Nodes (22): foto_professor(), pagina_login(), aluno_autorizado(), aluno_requerido(), _credencial_confere(), encerrar_sessao(), iniciar_sessao(), professor_autorizado() (+14 more)

### Community 67 - "servidor.py"
Cohesion: 0.12
Nodes (22): after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, context_processor, errorhandler, formatar_moeda(), Nome legível da forma de pagamento. Antes as telas usavam `|replace('_','…, Formata um valor em reais no padrão brasileiro: R$ 1.080,00. Usado como filtro… (+14 more)

### Community 69 - "pagina_cadastro"
Cohesion: 0.25
Nodes (14): _em_segundo_plano(), _enviar_em_segundo_plano(), pagina_cadastro(), Roda `tarefa` fora da requisição, para o tempo de resposta não revelar nada. Em…, E-mail COM token (recuperação, confirmação): não pode ir para a `fila_email`. A…, recuperar_senha(), cpf_valido(), data_nascimento_valida() (+6 more)

### Community 70 - "PlanoDAO"
Cohesion: 0.18
Nodes (13): atualizar_status_pagamento(), cadastrar_aluno(), cadastrar_pagamento(), detalhes_usuario(), painel_adm(), painel_financeiro(), Matrícula feita pela administração, sem conta de acesso. Pede só o que…, rotulo_status() (+5 more)

### Community 71 - "credenciais.py"
Cohesion: 0.20
Nodes (11): admin_configurado(), comparar_em_tempo_constante(), credencial_admin_confere(), gerar_hash_admin(), _main(), Credencial administrativa baseada exclusivamente em hash de senha. O…, Compara duas senhas em tempo constante, sem restrição de alfabeto. Codificar…, True quando existe usuário e hash da senha do administrador. (+3 more)

### Community 72 - "shot.mjs"
Cohesion: 0.29
Nodes (5): { chromium }, contextos, CREDS, jobs, require

### Community 73 - "Pagamento"
Cohesion: 0.25
Nodes (5): Decimal, Pagamento, _para_decimal(), Status a exibir, com o vencimento já aplicado. Uma cobrança `pendente` cujo…, cobranca()

### Community 74 - "usuario_bp.py"
Cohesion: 0.18
Nodes (19): _acesso_permitido_pagamento(), comprovante_mensalidade(), foto_perfil(), _pagamento_com_acesso_ou_404(), pagina_pagamento(), pagina_perfil(), _plano_do_formulario(), _pode_ver_foto() (+11 more)

### Community 76 - "Pagina"
Cohesion: 0.14
Nodes (5): Pagina, Uma fatia de resultados já recortada pelo banco, com o que a navegação precisa., Uma página existe mesmo quando está vazia. Sem isto, `__len__` fazia `{% if…, `__len__` fazia `{% if pagina %}` ser falso numa página sem itens, escondendo…, test_pagina_vazia_ainda_mostra_a_navegacao()

### Community 77 - "_parece_busca_por_cpf"
Cohesion: 0.17
Nodes (12): _parece_busca_por_cpf(), O termo é um CPF, ou um pedaço dele, e não um nome que por acaso tem número?, parametrize, Qualquer dígito no termo virava `CPF LIKE '%3%'` e devolvia a academia inteira., Rotas que custam hash de senha, processamento de imagem ou sondagem de token., Limites declarados por decorador NAQUELA rota. `resolve_limits` não serve aqui:…, Guarda do teste acima: uma rota sem limite precisa ser reprovada por ele., _tem_limite() (+4 more)

### Community 81 - "Contrato do redesign — SistemaEXTREMETEAM"
Cohesion: 0.09
Nodes (20): 0. Antes de escrever código, 1. Identidade visual (design tokens), 2. Logo oficial (usar SOMENTE a logo original), 3. Telas a implementar, 4. Regras e dados, 5. Forma de trabalhar, Painel administrativo (desktop, sidebar preta com o emblema do dragão), Prompt para o Claude Code — Redesign do SistemaEXTREMETEAM (+12 more)

### Community 82 - "_chave_da_conta"
Cohesion: 0.40
Nodes (5): _chave_da_conta(), Chave de limite por CONTA, caindo no IP só para quem não está autenticado. A…, Alunos atrás do mesmo IP (o Wi-Fi da academia) não dividem a cota., test_limite_de_upload_e_por_conta_e_nao_por_ip(), test_visitante_sem_sessao_ainda_e_limitado_por_ip()

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

### Community 89 - "adm_bp.py"
Cohesion: 0.17
Nodes (18): _chave_lote(), cobrar_inadimplentes(), cobrar_mensalidade(), enviar_aviso(), _esta_inadimplente(), _paragrafos_cobranca(), Situação de todos os alunos ativos com UMA consulta de mensalidades., Quem realmente deve receber cobrança: nem quem está com o plano ativo, nem quem… (+10 more)

### Community 90 - "Relatório de segurança — Sistema Extreme Team"
Cohesion: 0.29
Nodes (6): Controles verificados, Histórico de auditorias, Pendências não relacionadas a segurança, Relatório de segurança — Sistema Extreme Team, Situação atual (22/09/2026 — 2ª rodada), Validação executada em 22/09/2026

### Community 94 - "gmail_oauth_bp.py"
Cohesion: 0.57
Nodes (6): callback(), conectar(), desconectar(), limit, route, _voltar()

### Community 95 - "test_email_componentes.py"
Cohesion: 0.33
Nodes (7): E-mails: base com a logo oficial e componentes seguros para cliente de e-mail…, _render(), _sem_recursos_externos(), test_base_sem_url_publica_cai_para_o_nome_em_texto(), test_base_usa_a_logo_quando_ha_url_publica(), test_botao_do_email_usa_o_ouro_do_sistema(), test_cartao_de_resumo_com_badge()

### Community 96 - "test_perfil_e_foto.py"
Cohesion: 0.14
Nodes (18): TurmaDAO, Turma, Sonda: a data vem da query string e é convertida sem tratamento., test_data_invalida_na_turma_nao_derruba_a_rota(), test_area_do_aluno_renderiza_telas_independentes_do_menu(), test_escolher_plano_com_turma_cria_matricula(), test_plano_atual_continua_disponivel_para_gerar_cobranca(), test_turma_lotada_nao_vira_matricula_apos_pagamento() (+10 more)

### Community 98 - "test_layouts.py"
Cohesion: 0.29
Nodes (8): _conferir_head_comum(), parametrize, Layouts base (templates/layouts/) e toasts. Cada página estende o layout da sua…, test_area_do_aluno_carrega_o_layout(), test_flash_de_erro_vira_toast_que_nao_some_sozinho(), test_paginas_publicas_carregam_o_head_comum(), test_painel_admin_carrega_o_layout_admin(), test_toda_pagina_estende_um_layout()

### Community 99 - "conftest.py"
Cohesion: 0.27
Nodes (11): app(), client(), contexto_app(), limpar_banco(), logar_como_professor(), plano(), fixture, Substitui o provedor de e-mail em todos os módulos que o chamam. A suíte nunca… (+3 more)

### Community 100 - "erro_validacao_senha"
Cohesion: 0.20
Nodes (10): ativar_acesso(), Transforma um cadastro feito no balcão na conta do próprio aluno. Quem chega…, mascarar_email(), Mostra o bastante do e-mail para o dono se reconhecer, sem revelá-lo a…, _carregar_senhas_comuns(), erro_confirmacao_senha(), erro_validacao_senha(), Retorna uma mensagem quando a senha é curta, comum ou igual ao identificador. (+2 more)

### Community 102 - "Flask App Service (compose)"
Cohesion: 0.14
Nodes (14): Flask App Service (compose), Postgres DB Service (compose), postgres_data Volume, Flask, Flask-SQLAlchemy, Gunicorn, psycopg2-binary, python-dotenv (+6 more)

### Community 103 - "SolicitacaoMudancaPlano"
Cohesion: 0.20
Nodes (4): O que aconteceu numa tentativa de contratar/renovar/trocar de plano., ResultadoContratacao, Pedido de troca de plano agendado para a próxima renovação. Nunca altera o…, SolicitacaoMudancaPlano

### Community 104 - "Plano"
Cohesion: 0.24
Nodes (6): Plano, postgres_pix(), fixture, parametrize, Regressão com trava de linha real, opcional na suíte que usa SQLite. Execute…, test_duas_requisicoes_pix_reutilizam_uma_cobranca_postgres()

### Community 106 - "Etapa 1 — migrar páginas para os layouts (SEM mudar o visual)"
Cohesion: 0.29
Nodes (6): Conferência (agentes Claude), Divisão, Etapa 1 — migrar páginas para os layouts (SEM mudar o visual), O que já existe (não edite), Receita por página, Relatório (curto)

### Community 107 - "Etapas 4 a 6 — aluno, admin, professor (aplicar os componentes nas páginas)"
Cohesion: 0.29
Nodes (6): Agente A — área do aluno + pagamento, Agente B — admin, Antigravity — financeiro, turmas, professor, Etapas 4 a 6 — aluno, admin, professor (aplicar os componentes nas páginas), Orquestrador (Claude), Regras para todos

### Community 108 - "enviar_convite_acesso"
Cohesion: 0.33
Nodes (5): _aluno_do_cpf_ou_painel(), enviar_convite_acesso(), Aluno de uma rota administrativa, ou None (a rota redireciona ao painel)., Envia ao aluno o link de uso único que transforma o cadastro numa conta. O…, revogar_convite_acesso()

### Community 109 - "Etapa 2 — biblioteca de componentes"
Cohesion: 0.33
Nodes (5): Entregas e arquivos exclusivos, Etapa 2 — biblioteca de componentes, Ganchos de JS (Claude escreve `static/js/componentes.js`; markup e CSS usam EXATAMENTE isto), Macros (Agente A), cada uma no seu arquivo em `templates/components/`, Regras visuais (REDESIGN_CONTRATO.md seção 2 — leia)

### Community 110 - "Etapa 3 — home com os planos + termos"
Cohesion: 0.40
Nodes (4): Agente A — `templates/index.html` e `static/css/index.css`, Antigravity — `termos_de_servico.html`, `politica_privacidade.html`, `termos_responsabilidade.html` + `static/css/termos.css` (novo), Dados da home (Claude entrega em servidor.py — não edite), Etapa 3 — home com os planos + termos

### Community 113 - "test_pedido_publico_nao_invalida_convite_ainda_valido"
Cohesion: 0.40
Nodes (5): _convidar_cadastro_existente(), _convidar_cadastro_existente_por_id(), Cadastro administrativo que alguém tentou recriar pelo formulário público. Em…, Versão para thread de fundo: a sessão da requisição não vale fora dela., test_pedido_publico_nao_invalida_convite_ainda_valido()

### Community 115 - "test_comprovante_de_outro_aluno_com_arquivo_real_nao_vaza"
Cohesion: 0.50
Nodes (3): Versão forte da sonda de IDOR: o alvo TEM arquivo, então um 200 seria vazamento., test_comprovante_de_outro_aluno_com_arquivo_real_nao_vaza(), test_comprovante_em_analise_marca_situacao_do_aluno()

### Community 116 - "capturar_emails"
Cohesion: 0.67
Nodes (3): capturar_emails(), fixture, Intercepta o envio e devolve os e-mails que teriam saído, com os links.

## Knowledge Gaps
- **98 isolated node(s):** `modal`, `input_senha`, `icone_senha`, `formularioPlano`, `campoPreco` (+93 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PagamentoDAO` connect `PagamentoDAO` to `route`, `.listar_por_aluno`, `criar_pagamento`, `test_mudanca_plano.py`, `AlunoDAO`, `criar_aluno`, `MercadoPagoIndisponivel`, `logar_como_admin`, `checkout_bp.py`, `config.py`, `test_auditoria_seguranca.py`, `usuario_e_admin`, `MatriculaDAO`, `.listar_paginado`, `logar_como_aluno`, `test_pix_rotas.py`, `PagamentoEvento`, `test_seguranca.py`, `Aluno`, `test_retorno_ignora_status_aprovado_da_query_string`, `PlanoDAO`, `Pagamento`, `usuario_bp.py`, `adm_bp.py`, `test_perfil_e_foto.py`, `conftest.py`, `SolicitacaoMudancaPlano`, `test_comprovante_de_outro_aluno_com_arquivo_real_nao_vaza`?**
  _High betweenness centrality (0.158) - this node is a cross-community bridge._
- **Why does `Aluno` connect `Aluno` to `route`, `autorizacao.py`, `conftest.py`, `erro_validacao_senha`, `pagina_cadastro`, `PlanoDAO`, `AlunoDAO`, `URLPublicaInvalida`, `criar_aluno`, `usuario_bp.py`, `Plano`, `test_pedido_publico_nao_invalida_convite_ainda_valido`, `logar_como_admin`, `PagamentoDAO`, `test_seguranca.py`, `config.py`, `adm_bp.py`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Why does `logar_como_admin()` connect `logar_como_admin` to `test_home_planos.py`, `.listar_por_aluno`, `criar_pagamento`, `test_mudanca_plano.py`, `AlunoDAO`, `criar_aluno`, `test_mercado_pago_oauth.py`, `PagamentoDAO`, `MatriculaDAO`, `.listar_paginado`, `logar_como_aluno`, `test_pix_rotas.py`, `ProfessorDAO`, `test_seguranca.py`, `Academia`, `test_sessao_revogada.py`, `test_perfil_e_foto.py`, `test_layouts.py`, `conftest.py`, `test_pedido_publico_nao_invalida_convite_ainda_valido`, `test_trocar_a_credencial_do_admin_encerra_a_sessao_administrativa`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Are the 136 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 136 INFERRED edges - model-reasoned connections that need verification._
- **Are the 140 inferred relationships involving `criar_pagamento()` (e.g. with `PagamentoDAO` and `Pagamento`) actually correct?**
  _`criar_pagamento()` has 140 INFERRED edges - model-reasoned connections that need verification._
- **Are the 138 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 138 INFERRED edges - model-reasoned connections that need verification._
- **Are the 117 inferred relationships involving `logar_como_aluno()` (e.g. with `test_aluno_nao_alcanca_cobranca_de_outro_aluno()` and `test_checkout_recusa_cobranca_indisponivel()`) actually correct?**
  _`logar_como_aluno()` has 117 INFERRED edges - model-reasoned connections that need verification._