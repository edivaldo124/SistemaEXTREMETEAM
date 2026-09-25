# Graph Report - SistemaEXTREMETEAM  (2026-09-24)

## Corpus Check
- 132 files · ~189,452 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1737 nodes · 4539 edges · 129 communities (107 shown, 22 thin omitted)
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 946 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `062ac873`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_professor_perfil.py
- index.js
- Aluno
- criar_aluno
- test_limites_pagamento.py
- test_mudanca_plano.py
- PagamentoDAO
- test_regressao_auditoria.py
- SistemaEXTREMETEAM Project
- test_mercado_pago_servico.py
- test_mercado_pago_oauth.py
- Professor
- test_migracao_checkout.py
- checkout.js
- CLAUDE.md
- planos.py
- pix_bp.py
- logar_como_admin
- .buscar_por_id
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
- impressao_credencial
- test_linha_com_defeito_nao_trava_a_fila_atras_dela
- convites.py
- Academia
- pagamento_polling.test.cjs
- MercadoPagoIndisponivel
- criar_pagamento
- test_pix_rotas.py
- PagamentoEvento
- d9e2f6a14c80_contatos_academia_perfis_professores.py
- _Resposta
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
- gmail_conta.py
- mercado_pago.py
- test_arranque_seguranca.py
- MercadoPagoConexao
- URLPublicaInvalida
- servidor.py
- autorizacao.py
- pagina_cadastro
- adm_bp.py
- pagina_login
- shot.mjs
- limites_pagamento.py
- usuario_bp.py
- Pagina
- _parece_busca_por_cpf
- e4b7c2a91d35_cadastro_administrativo_e_convite_de_acesso.py
- a1f0c3e75b92_schema_inicial.py
- Contrato do redesign — SistemaEXTREMETEAM
- _chave_da_conta
- Admin Dashboard Page
- Skills Disponíveis
- academia_bp.py
- test_sessao_revogada.py
- MatriculaDAO
- Relatório de segurança — Sistema Extreme Team
- admin_requerido
- test_admin_rejeita_valor_financeiro_invalido
- test_perfil_e_foto.py
- test_email_gmail.py
- AlunoDAO
- .contratar_plano
- erro_validacao_senha
- PlanoDAO
- Flask App Service (compose)
- theme.css
- test_retorno_ignora_status_aprovado_da_query_string
- enviar_convite_acesso
- test_financeiro_admin_painel.py
- Aluno Profile Page
- test_o_mesmo_aviso_pode_ser_enviado_de_novo_em_outro_dia
- _FakePaymentResource
- Aluno Detail/Admin Page
- _tem_limite
- pgAdm.js
- test_reenviar_um_aviso_que_desistiu_volta_a_enfileirar
- test_um_envio_ainda_pendente_continua_sendo_recusado
- test_retentativa_acontece_sem_ninguem_abrir_o_painel
- test_jpeg_grande_e_aceito_porque_decodifica_em_escala_reduzida
- test_decodificacao_de_imagem_e_serializada_no_processo
- test_a_suite_nunca_escreve_na_pasta_de_uploads_do_projeto
- test_trocar_a_credencial_do_admin_encerra_a_sessao_administrativa
- test_uma_falha_do_provedor_nao_queima_todas_as_tentativas
- extreme.css
- capturar_emails
- test_limite_atingido_nao_mostra_login_a_quem_ja_entrou
- test_sessao_sem_carimbo_de_credencial_e_recusada
- test_login_de_aluno_nao_paga_o_hash_do_admin

## God Nodes (most connected - your core abstractions)
1. `PagamentoDAO` - 202 edges
2. `criar_pagamento()` - 141 edges
3. `criar_aluno()` - 134 edges
4. `logar_como_aluno()` - 113 edges
5. `logar_como_admin()` - 113 edges
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

## Communities (129 total, 22 thin omitted)

### Community 0 - "test_professor_perfil.py"
Cohesion: 0.25
Nodes (9): _foto(), pasta_fotos(), professor(), fixture, test_edicao_professor_tem_protecao_csrf(), test_falha_ao_salvar_preserva_foto_anterior(), test_publicar_e_retirar_foto_do_site(), test_substituir_remover_e_recusar_foto_falsa() (+1 more)

### Community 1 - "index.js"
Cohesion: 0.24
Nodes (9): abrirmodal(), fechar(), icone_senha, input_senha, modal, mostrarSenha(), meuModal Login Modal, Home Page (+1 more)

### Community 2 - "Aluno"
Cohesion: 0.11
Nodes (10): Matrícula feita no balcão: sem login, sem senha e sem convite de acesso. Nasce…, Aluno, Se existe uma conta de acesso, e não se o aluno está em dia ou matriculado.…, Convite de acesso já enviado e ainda não usado (a validade é checada na rota)., Chave do estado da CONTA - nunca da situação financeira nem da matrícula., test_admin_lanca_e_baixa_mensalidade_de_aluno_sem_acesso(), test_cadastro_publico_com_cpf_sem_email_no_cadastro_nao_envia_nada(), _dados_cadastro() (+2 more)

### Community 3 - "criar_aluno"
Cohesion: 0.13
Nodes (35): criar_aluno(), test_aluno_existente_continua_entrando_normalmente(), test_escolher_plano_cria_mensalidade_e_redireciona_para_pix(), test_plano_invalido_nao_cria_mensalidade(), test_reenvio_da_contratacao_reutiliza_mensalidade(), test_valor_enviado_pelo_navegador_e_ignorado(), test_callback_de_aluno_nao_conecta_conta(), _pagar() (+27 more)

### Community 4 - "test_limites_pagamento.py"
Cohesion: 0.15
Nodes (15): consultar_mp(), fixture, parametrize, Limites de pagamento por conta, com o provedor inteiramente simulado., _sessao_aluno(), test_admin_limite_por_usuario_persiste_entre_sessoes(), test_alunos_no_mesmo_ip_tem_limites_separados(), test_anonimos_limitados_por_ip_sem_consultar_provedor() (+7 more)

### Community 5 - "test_mudanca_plano.py"
Cohesion: 0.20
Nodes (23): detalhes_usuario(), Persistência dos pedidos de troca de plano agendados para a próxima renovação., SolicitacaoPlanoDAO, _agendar(), _pagar(), Mudança para um plano mais barato agendada para a próxima renovação. Regra…, O admin pode estornar/cancelar a mensalidade que sustentava a vigência depois…, test_admin_cancela_a_solicitacao() (+15 more)

### Community 6 - "PagamentoDAO"
Cohesion: 0.09
Nodes (28): mensalidade_destaque(), PagamentoDAO, Status como o painel deve LER, com o vencimento aplicado na própria consulta. A…, Carrega aluno e plano junto das mensalidades. O template do painel lê…, Lista completa (sem paginar). Mantida para relatórios e testes., Uma página de mensalidades, recortada pelo banco (LIMIT/OFFSET). O painel…, Totais do painel financeiro - sempre calculados no backend a partir do banco,…, Escolhe a mensalidade mais relevante para o card 'Minha mensalidade': a mais… (+20 more)

### Community 7 - "test_regressao_auditoria.py"
Cohesion: 0.08
Nodes (21): _contar_selects_em_alunos(), _credencial(), Regressões da auditoria de segurança, desempenho e confiabilidade. Cada caso…, test_abrir_o_painel_financeiro_nao_grava_no_banco(), test_aluno_desativado_nao_ve_mais_a_propria_foto_pela_sessao_antiga(), test_aluno_troca_a_senha_para_uma_com_acentos(), test_aviso_coletivo_enfileira_em_vez_de_enviar_na_requisicao(), test_aviso_repetido_no_mesmo_dia_avisa_em_vez_de_comemorar() (+13 more)

### Community 9 - "test_mercado_pago_servico.py"
Cohesion: 0.10
Nodes (30): Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, validar_assinatura_webhook(), Hipótese: uma notificação capturada ontem pode ser reenviada hoje., `ts=nan` fazia a comparação da janela dar False e passava pela checagem de…, test_webhook_recusa_assinatura_antiga(), test_webhook_recusa_ts_nao_numerico_finito(), base_url(), _criar_preferencia() (+22 more)

### Community 10 - "test_mercado_pago_oauth.py"
Cohesion: 0.09
Nodes (32): _conectar(), _dados_conexao(), _preparar_state(), Grava uma conexão direto pelo serviço (precisa de app context)., test_ambiente_explicito_vence_a_conta_conectada(), test_ambiente_segue_o_live_mode_da_conta(), test_cada_conexao_iniciada_usa_state_novo(), test_callback_avisa_quando_a_conta_muda() (+24 more)

### Community 11 - "Professor"
Cohesion: 0.12
Nodes (19): remover_professor(), ProfessorDAO, Professor, logar_como_professor(), fixture, Hipótese: a foto continua acessível por URL depois de tirar a publicação., Hipótese: os contatos vazam na home antes de a publicação ser marcada., Sonda: a data vem da query string e é convertida sem tratamento. (+11 more)

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
Nodes (31): _acesso_permitido(), criar_pix_mensalidade(), _forma_pagamento_confirmada(), _pagamento_mp_mais_relevante(), _pagamento_ou_none(), _pix_expirado(), _processar_status_mp(), limitar_consulta_pagamento (+23 more)

### Community 18 - "logar_como_admin"
Cohesion: 0.15
Nodes (42): _convidar_cadastro_existente(), Cadastro administrativo que alguém tentou recriar pelo formulário público. Em…, logar_como_admin(), _matricular(), Cadastro de aluno pela administração, ativação de acesso e confirmação de…, test_admin_matricula_aluno_sem_email_senha_nem_acesso(), test_admin_nao_pode_apagar_o_usuario_de_uma_conta_ativa(), test_admin_pode_deixar_cadastro_de_balcao_sem_usuario_e_sem_email() (+34 more)

### Community 19 - ".buscar_por_id"
Cohesion: 0.15
Nodes (27): _assinar(), _pagamento_mp(), _preparar_retorno(), Pix aberto e checkout concluído ao mesmo tempo: a consulta pelo…, test_mercado_pago_indisponivel_nao_persiste_nada(), test_retorno_com_aprovacao_confirmada_marca_pago(), test_retorno_com_mp_indisponivel_avisa_sem_mudar_status(), test_retorno_de_boleto_avisa_sobre_o_prazo() (+19 more)

### Community 20 - "checkout_bp.py"
Cohesion: 0.11
Nodes (27): abrir_checkout(), _acesso_permitido(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), limitar_consulta_pagamento, limitar_criacao_pagamento, route (+19 more)

### Community 21 - "pix.js"
Cohesion: 0.33
Nodes (14): abrirPix(), alvoDoRotulo(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), liberarBotao(), limparConteudoAnterior() (+6 more)

### Community 22 - "config.py"
Cohesion: 0.08
Nodes (32): _paginar(), Aplica LIMIT/OFFSET e conta o total numa consulta separada e barata. A contagem…, Decimal, Matricula, Pagamento, _para_decimal(), Status a exibir, com o vencimento já aplicado. Uma cobrança `pendente` cujo…, Plano (+24 more)

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
Nodes (43): _assinar(), _pagamento_mp(), _preparar_para_conciliacao(), parametrize, Auditoria de segurança: sondas escritas para TENTAR quebrar as regras. Nenhum…, Hipótese: a sessão de professor é aceita nas rotas financeiras do aluno., Hipótese: como o JS agora usa fetch, o POST perdeu a exigência de CSRF., Hipótese: as demais rotas de dinheiro aceitam POST sem token. (+35 more)

### Community 34 - "turma_bp.py"
Cohesion: 0.17
Nodes (15): _acesso_permitido(), cadastrar_professor(), cadastrar_turma(), desmatricular_aluno(), detalhe_turma(), gerenciar_turmas(), matricular_aluno(), painel_professor() (+7 more)

### Community 35 - "usuario_e_admin"
Cohesion: 0.16
Nodes (19): aprovar_aluno(), aprovar_comprovante_manual(), ativar_aluno(), atualizar_status_pagamento(), cancelar_mudanca_plano_admin(), _data_do_form(), desativar_aluno(), enviar_foto_aluno() (+11 more)

### Community 36 - "impressao_credencial"
Cohesion: 0.22
Nodes (15): Presenca, impressao_credencial(), Resumo curto e não reversível do hash da senha, guardado na sessão. Nunca é a…, Valor que representa a credencial administrativa em vigor, ou None se não há…, referencia_credencial_admin(), parametrize, test_aluno_confirma_sua_frequencia(), test_consulta_com_data_invalida_exibe_hoje_e_aviso() (+7 more)

### Community 38 - "convites.py"
Cohesion: 0.15
Nodes (18): aluno_do_token(), ConviteIndisponivel, descartar(), enviar(), gerar_token(), _hash(), RuntimeError, Convite de acesso: como um cadastro criado pela administração vira uma conta.… (+10 more)

### Community 41 - "Academia"
Cohesion: 0.16
Nodes (11): Academia, link_email(), parametrize, test_admin_salva_atualiza_e_limpa_contatos(), test_configuracoes_exigem_admin(), test_contatos_invalidos(), test_csrf_configuracoes(), test_erro_preserva_formulario_e_dados_salvos() (+3 more)

### Community 42 - "pagamento_polling.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 43 - "MercadoPagoIndisponivel"
Cohesion: 0.11
Nodes (36): access_token_vigente(), _agora(), ambiente_da_conexao(), _cifrar(), _client_id(), _client_secret(), ConexaoIlegivel, _decifrar() (+28 more)

### Community 44 - "criar_pagamento"
Cohesion: 0.11
Nodes (48): criar_pagamento(), logar_como_aluno(), _mockar_preferencia(), parametrize, Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala…, Um boleto pendente do Checkout Pro grava provider_payment_id, mas não é Pix:…, _resposta_preferencia(), test_abertura_json_navega_sem_redirecionar_post_externo() (+40 more)

### Community 45 - "test_pix_rotas.py"
Cohesion: 0.27
Nodes (16): _assinar(), _resposta_consulta(), _resposta_criacao(), test_admin_tambem_pode_gerar_pix(), test_aluno_gera_pix_da_propria_mensalidade(), test_impede_cobranca_duplicada_em_chamadas_consecutivas(), test_reutiliza_cobranca_pendente_valida(), test_sem_sessao_retorna_401() (+8 more)

### Community 46 - "PagamentoEvento"
Cohesion: 0.11
Nodes (13): cadastrar_pagamento(), Primeiro dia não coberto por outra mensalidade do mesmo aluno., Define o período coberto por uma mensalidade que ainda não tem um (lançamento…, Abre o período de acesso no momento em que o pagamento é confirmado. Se a…, Reescreve os campos denormalizados do aluno a partir das mensalidades.…, forma_pagamento vem do que o Mercado Pago confirmou na consulta à API ('pix',…, Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.…, PagamentoEvento (+5 more)

### Community 47 - "d9e2f6a14c80_contatos_academia_perfis_professores.py"
Cohesion: 0.83
Nodes (3): _campos_professor(), downgrade(), upgrade()

### Community 49 - "_Resposta"
Cohesion: 0.15
Nodes (20): _agora(), _ajustar(), api_mp(), oauth_env(), fixture, Substitui POST /oauth/token. `respostas` é consumida em ordem; a última se…, A rota de checkout pede o token com a mensalidade travada na sessão dela., _Resposta (+12 more)

### Community 50 - "botao_ocupado.test.cjs"
Cohesion: 0.18
Nodes (7): assert, criarElemento(), fs, montar(), path, test, vm

### Community 51 - "test_seguranca.py"
Cohesion: 0.08
Nodes (23): _cadastro_publico(), _imagem_jpeg(), _mensagem_da_resposta(), O `login` de um aluno pode ser o e-mail de outro; quem entra é decidido pela…, O ramo "par existe" não pode pagar a ida ao provedor dentro da requisição., Cadastro novo, CPF existente e e-mail existente respondem com a MESMA tela., Quem ainda controla a caixa antiga não pode assumir a conta depois da troca., test_cabecalhos_de_seguranca() (+15 more)

### Community 52 - "checkout_abertura.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 55 - "gunicorn.conf.py"
Cohesion: 0.25
Nodes (9): post_worker_init(), Hooks carregados pelo Gunicorn; nunca executados por flask db upgrade., worker_exit(), iniciar(), _laco(), parar(), Aciona a fila periodicamente durante a vida de um worker Gunicorn. Importar…, Inicia uma vez por processo, depois de carregar a aplicação e migrar o banco. (+1 more)

### Community 56 - "ConfiguracaoInvalida"
Cohesion: 0.24
Nodes (13): _autorizacao_valida(), callback(), conectar(), desconectar(), limit, route, O state devolvido é o que ESTA sessão emitiu, há pouco tempo?, Só monta o state/PKCE na sessão e manda o administrador ao Mercado Pago. É um… (+5 more)

### Community 57 - "fila_email.py"
Cohesion: 0.06
Nodes (40): EmailPendente, espera_da_proxima_tentativa(), Fila de e-mails no banco. Aviso e cobrança coletivos saíam um a um dentro da…, contar_falhados(), contar_pendentes(), disparar(), enfileirar(), enfileirar_transacional() (+32 more)

### Community 58 - "test_migracao_cadastro_administrativo.py"
Cohesion: 0.40
Nodes (3): banco_antigo(), fixture, Verifica a migração em um banco isolado com o schema anterior e dados.

### Community 59 - "salvar_foto_perfil"
Cohesion: 0.13
Nodes (25): enviar_comprovante_manual_aluno(), ArquivoInvalido, _conferir_dimensoes(), _detectar_tipo_imagem_real(), ImagemGrandeDemais, _pasta(), Exception, _raiz_uploads() (+17 more)

### Community 60 - "test_keep_alive.py"
Cohesion: 0.16
Nodes (7): ambiente_limpo(), fixture, parametrize, Garante que o keep-alive fica desligado por padrão e só pinga a própria origem., test_intervalo_fica_dentro_da_faixa(), test_nao_liga_com_valor_negativo(), test_ping_so_considera_200_como_sucesso()

### Community 61 - "gmail_conta.py"
Cohesion: 0.26
Nodes (15): GmailConexao, _access_token(), _cifrar(), _client_id(), _client_secret(), _decifrar(), enviar(), estado() (+7 more)

### Community 62 - "mercado_pago.py"
Cohesion: 0.12
Nodes (29): _base_url_opcional(), base_url_publica(), buscar_pagamentos_por_referencia(), cancelar_pagamento(), criar_pagamento_pix(), criar_preferencia_checkout(), _erro_menciona(), _erro_menciona_expiracao() (+21 more)

### Community 63 - "test_arranque_seguranca.py"
Cohesion: 0.22
Nodes (14): _env_arranque(), Validações feitas por servidor.py no arranque (COOKIE_SECURE, TRUSTED_HOSTS,…, `python -m servicos.credenciais`: o hash sai entre aspas simples. O hash do…, Desenvolvimento local sem HTTPS (sem Caddy) não pode ficar travado., _rodar(), test_arranque_falha_com_cookie_secure_false_e_app_base_url_https(), test_arranque_falha_com_cookie_secure_invalido(), test_arranque_falha_sem_trusted_hosts() (+6 more)

### Community 64 - "MercadoPagoConexao"
Cohesion: 0.13
Nodes (16): MercadoPagoConexao, Conta do Mercado Pago que a academia autorizou por OAuth. Uma linha só (a…, Esquece a conta conectada. Devolve True se havia uma., remover_conexao(), postgres_mp(), fixture, Renovação do token OAuth com trava de linha real, opcional na suíte que usa…, _Resposta (+8 more)

### Community 66 - "URLPublicaInvalida"
Cohesion: 0.22
Nodes (13): iniciar(), _intervalo(), _laco(), _ligado(), parar(), _pingar(), Mantém a aplicação acordada em hospedagens que hibernam por inatividade. Uma…, Encerra o laço. Usado pelos testes; em produção a thread é daemon. (+5 more)

### Community 67 - "servidor.py"
Cohesion: 0.11
Nodes (21): after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, context_processor, errorhandler, Registra a sessão como encerrada: cópias antigas do cookie deixam de valer.…, revogar_sessao_atual(), formatar_moeda() (+13 more)

### Community 68 - "autorizacao.py"
Cohesion: 0.21
Nodes (15): foto_professor(), aluno_autorizado(), aluno_requerido(), _credencial_confere(), encerrar_sessao(), professor_autorizado(), Autorização das rotas protegidas. A sessão diz quem *afirmou* ser quem; quem…, A sessão foi emitida para a credencial que vale AGORA? Uma sessão sem carimbo é… (+7 more)

### Community 69 - "pagina_cadastro"
Cohesion: 0.19
Nodes (18): _convidar_cadastro_existente_por_id(), _em_segundo_plano(), _enviar_em_segundo_plano(), pagina_cadastro(), Roda `tarefa` fora da requisição, para o tempo de resposta não revelar nada. Em…, E-mail COM token (recuperação, confirmação): não pode ir para a `fila_email`. A…, Versão para thread de fundo: a sessão da requisição não vale fora dela., recuperar_senha() (+10 more)

### Community 70 - "adm_bp.py"
Cohesion: 0.20
Nodes (16): _chave_lote(), cobrar_inadimplentes(), cobrar_mensalidade(), enviar_aviso(), _esta_inadimplente(), _paragrafos_cobranca(), Situação de todos os alunos ativos com UMA consulta de mensalidades., Quem realmente deve receber cobrança: nem quem está com o plano ativo, nem quem… (+8 more)

### Community 71 - "pagina_login"
Cohesion: 0.12
Nodes (16): pagina_login(), iniciar_sessao(), Grava na sessão atual a credencial em vigor (login ou troca de senha bem-…, Dá um identificador à sessão recém-aberta, para o logout poder revogá-la.…, registrar_credencial(), admin_configurado(), comparar_em_tempo_constante(), credencial_admin_confere() (+8 more)

### Community 72 - "shot.mjs"
Cohesion: 0.29
Nodes (5): { chromium }, contextos, CREDS, jobs, require

### Community 73 - "limites_pagamento.py"
Cohesion: 0.50
Nodes (3): chave_pagamento(), Orçamentos compartilhados das chamadas interativas ao provedor de pagamento., A mesma conta mantém seu limite entre sessões, rotas e mensalidades. Alunos que…

### Community 74 - "usuario_bp.py"
Cohesion: 0.15
Nodes (29): _acesso_permitido_pagamento(), _aluno_da_sessao(), atualizar_dados_perfil(), cancelar_mudanca_plano(), comprovante_mensalidade(), confirmar_presenca(), enviar_foto_perfil(), foto_perfil() (+21 more)

### Community 76 - "Pagina"
Cohesion: 0.14
Nodes (5): Pagina, Uma fatia de resultados já recortada pelo banco, com o que a navegação precisa., Uma página existe mesmo quando está vazia. Sem isto, `__len__` fazia `{% if…, `__len__` fazia `{% if pagina %}` ser falso numa página sem itens, escondendo…, test_pagina_vazia_ainda_mostra_a_navegacao()

### Community 77 - "_parece_busca_por_cpf"
Cohesion: 0.33
Nodes (6): _parece_busca_por_cpf(), O termo é um CPF, ou um pedaço dele, e não um nome que por acaso tem número?, parametrize, Qualquer dígito no termo virava `CPF LIKE '%3%'` e devolvia a academia inteira., test_busca_so_trata_como_cpf_o_que_parece_cpf(), test_sessao_aberta_perde_o_perfil_quando_a_conta_deixa_de_valer()

### Community 81 - "Contrato do redesign — SistemaEXTREMETEAM"
Cohesion: 0.09
Nodes (20): 0. Antes de escrever código, 1. Identidade visual (design tokens), 2. Logo oficial (usar SOMENTE a logo original), 3. Telas a implementar, 4. Regras e dados, 5. Forma de trabalhar, Painel administrativo (desktop, sidebar preta com o emblema do dragão), Prompt para o Claude Code — Redesign do SistemaEXTREMETEAM (+12 more)

### Community 82 - "_chave_da_conta"
Cohesion: 0.40
Nodes (5): _chave_da_conta(), Chave de limite por CONTA, caindo no IP só para quem não está autenticado. A…, Alunos atrás do mesmo IP (o Wi-Fi da academia) não dividem a cota., test_limite_de_upload_e_por_conta_e_nao_por_ip(), test_visitante_sem_sessao_ainda_e_limitado_por_ip()

### Community 83 - "Admin Dashboard Page"
Cohesion: 0.29
Nodes (6): Confirm Dialog Component, Admin Dashboard Page, Cadastrar Plano Form, Professor Turmas Page, Turmas Admin Page, Cadastrar Professor Form

### Community 84 - "Skills Disponíveis"
Cohesion: 0.22
Nodes (8): Assistente e Automação (Antigravity), Ciências e Bioinformática (Plugins de Ciência), Dados e Google Cloud Platform (GCP), Desenvolvimento Mobile e Flutter/Dart, Desenvolvimento Web e Frontend, Firebase e Backend, GenAI e Machine Learning, Skills Disponíveis

### Community 85 - "academia_bp.py"
Cohesion: 0.40
Nodes (8): configuracoes(), _pagina(), route, editar_professor(), Normalização de contatos profissionais antes de montar links públicos., validar_email(), validar_instagram(), validar_whatsapp()

### Community 86 - "test_sessao_revogada.py"
Cohesion: 0.24
Nodes (11): Sessões encerradas pelo logout. A sessão do Flask é um cookie assinado, sem…, SessaoRevogada, _cliente_com_cookie(), _entrar_como_admin(), `session.clear()` só limpava o navegador de quem saiu; a cópia do cookie seguia…, test_logout_apaga_revogacoes_vencidas(), test_logout_de_uma_sessao_nao_derruba_as_outras(), test_logout_revoga_a_copia_do_cookie_feita_antes() (+3 more)

### Community 89 - "MatriculaDAO"
Cohesion: 0.36
Nodes (4): MatriculaDAO, test_escolher_plano_com_turma_cria_matricula(), test_turma_lotada_nao_vira_matricula_apos_pagamento(), test_professor_ve_foto_de_aluno_da_propria_turma()

### Community 90 - "Relatório de segurança — Sistema Extreme Team"
Cohesion: 0.29
Nodes (6): Controles verificados, Histórico de auditorias, Pendências não relacionadas a segurança, Relatório de segurança — Sistema Extreme Team, Situação atual (22/09/2026 — 2ª rodada), Validação executada em 22/09/2026

### Community 94 - "admin_requerido"
Cohesion: 0.57
Nodes (7): callback(), conectar(), desconectar(), limit, route, _voltar(), admin_requerido()

### Community 95 - "test_admin_rejeita_valor_financeiro_invalido"
Cohesion: 0.33
Nodes (6): parametrize, test_admin_rejeita_valor_financeiro_invalido(), test_confirmacao_aceita_unicode(), test_matricula_valida_dados_no_servidor(), test_novos_formularios_exigem_csrf(), test_rotas_de_matricula_e_convite_sao_so_do_admin()

### Community 96 - "test_perfil_e_foto.py"
Cohesion: 0.18
Nodes (10): Turma, Cadastrar Turma Form, test_area_do_aluno_renderiza_telas_independentes_do_menu(), test_plano_atual_continua_disponivel_para_gerar_cobranca(), _imagem_jpeg_valida(), test_admin_acessa_foto_de_qualquer_aluno(), test_aluno_nao_acessa_foto_de_outro_aluno(), test_aluno_ve_o_proprio_perfil() (+2 more)

### Community 98 - "AlunoDAO"
Cohesion: 0.18
Nodes (11): AlunoDAO, Uma página de alunos já cadastrados, recortada e filtrada pelo banco. O painel…, test_upload_de_arquivo_disfarcado_e_recusado(), O CPF é guardado formatado; digitar só os números precisa encontrar mesmo assim., test_busca_do_admin_encontra_o_aluno_pelo_cpf_so_com_digitos(), test_busca_por_nome_com_numero_nao_devolve_todo_mundo(), test_paginacao_do_admin_ignora_pendentes_como_a_tela_sempre_fez(), test_painel_admin_pagina_alunos_no_banco() (+3 more)

### Community 99 - ".contratar_plano"
Cohesion: 0.10
Nodes (11): O que aconteceu numa tentativa de contratar/renovar/trocar de plano., Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda. O…, Aplica um pedido agendado cujo período de origem já terminou sem renovação.…, Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, Com uma troca já agendada, só dois planos fazem sentido num pedido de…, A cobrança do período seguinte tem de nascer no plano que o aluno agendou.…, `pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -… (+3 more)

### Community 100 - "erro_validacao_senha"
Cohesion: 0.15
Nodes (18): alterar_senha_perfil(), _aluno_por_token(), ativar_acesso(), confirmar_email(), limit, Descarta todo link pendente que ainda autorizaria assumir ou redirecionar a…, Localiza o aluno pelo hash do token, filtrando no banco por uma coluna indexada., Transforma um cadastro feito no balcão na conta do próprio aluno. Quem chega… (+10 more)

### Community 102 - "PlanoDAO"
Cohesion: 0.18
Nodes (10): cadastrar_aluno(), cadastrar_plano(), painel_adm(), Matrícula feita pela administração, sem conta de acesso. Pede só o que…, remover_plano(), _plano_do_formulario(), PlanoDAO, Quantos alunos a academia tem, sem filtro de busca. O card do topo do painel é… (+2 more)

### Community 103 - "Flask App Service (compose)"
Cohesion: 0.22
Nodes (9): Flask App Service (compose), Postgres DB Service (compose), postgres_data Volume, Flask, Flask-SQLAlchemy, Gunicorn, psycopg2-binary, python-dotenv (+1 more)

### Community 104 - "theme.css"
Cohesion: 0.22
Nodes (4): cadastro-form Registration Form, Cadastro (Registration) Page, Recuperar Senha Form, Recuperar Senha Page

### Community 107 - "enviar_convite_acesso"
Cohesion: 0.33
Nodes (5): _aluno_do_cpf_ou_painel(), enviar_convite_acesso(), Aluno de uma rota administrativa, ou None (a rota redireciona ao painel)., Envia ao aluno o link de uso único que transforma o cadastro numa conta. O…, revogar_convite_acesso()

### Community 108 - "test_financeiro_admin_painel.py"
Cohesion: 0.33
Nodes (5): test_busca_financeira_trata_curingas_como_texto(), test_painel_financeiro_busca_por_nome_do_aluno(), test_painel_financeiro_exige_admin(), test_painel_financeiro_filtra_por_status(), test_painel_financeiro_mostra_totais_do_backend()

### Community 109 - "Aluno Profile Page"
Cohesion: 0.22
Nodes (7): formatadorDePreco, gradePlanos, mostrarTela(), trocarTela(), Histórico de Mensalidades Section, Aluno Profile Page, Planos Disponíveis Section

### Community 112 - "Aluno Detail/Admin Page"
Cohesion: 0.22
Nodes (7): Aluno Mensalidade Launch Form, Aluno Detail/Admin Page, Aluno Profile Update Form, preencherValor() Inline Script, Matrícula Form, Turma Detail Page, Presença Form

### Community 113 - "_tem_limite"
Cohesion: 0.33
Nodes (6): Rotas que custam hash de senha, processamento de imagem ou sondagem de token., Limites declarados por decorador NAQUELA rota. `resolve_limits` não serve aqui:…, Guarda do teste acima: uma rota sem limite precisa ser reprovada por ele., _tem_limite(), test_o_detector_de_limite_realmente_discrimina(), test_rotas_caras_tem_limite_de_requisicoes()

### Community 115 - "pgAdm.js"
Cohesion: 0.40
Nodes (4): campoDuracao, campoPreco, formatadorDePreco, formularioPlano

### Community 125 - "capturar_emails"
Cohesion: 0.67
Nodes (3): capturar_emails(), fixture, Intercepta o envio e devolve os e-mails que teriam saído, com os links.

## Knowledge Gaps
- **83 isolated node(s):** `modal`, `input_senha`, `icone_senha`, `formularioPlano`, `campoPreco` (+78 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **22 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PagamentoDAO` connect `PagamentoDAO` to `Aluno`, `criar_aluno`, `test_mudanca_plano.py`, `test_regressao_auditoria.py`, `pix_bp.py`, `logar_como_admin`, `.buscar_por_id`, `checkout_bp.py`, `config.py`, `test_auditoria_seguranca.py`, `usuario_e_admin`, `criar_pagamento`, `test_pix_rotas.py`, `PagamentoEvento`, `test_seguranca.py`, `salvar_foto_perfil`, `adm_bp.py`, `usuario_bp.py`, `MatriculaDAO`, `test_admin_rejeita_valor_financeiro_invalido`, `test_perfil_e_foto.py`, `AlunoDAO`, `.contratar_plano`, `PlanoDAO`, `test_retorno_ignora_status_aprovado_da_query_string`, `test_financeiro_admin_painel.py`?**
  _High betweenness centrality (0.160) - this node is a cross-community bridge._
- **Why does `AlunoDAO` connect `AlunoDAO` to `Aluno`, `criar_aluno`, `test_mudanca_plano.py`, `PagamentoDAO`, `test_regressao_auditoria.py`, `logar_como_admin`, `config.py`, `turma_bp.py`, `usuario_e_admin`, `PagamentoEvento`, `test_seguranca.py`, `pagina_cadastro`, `adm_bp.py`, `pagina_login`, `usuario_bp.py`, `test_admin_rejeita_valor_financeiro_invalido`, `test_perfil_e_foto.py`, `PlanoDAO`, `enviar_convite_acesso`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `criar_aluno()` connect `criar_aluno` to `test_login_de_aluno_nao_paga_o_hash_do_admin`, `Aluno`, `test_limites_pagamento.py`, `test_mudanca_plano.py`, `PagamentoDAO`, `test_regressao_auditoria.py`, `Professor`, `logar_como_admin`, `.buscar_por_id`, `config.py`, `test_auditoria_seguranca.py`, `impressao_credencial`, `criar_pagamento`, `PagamentoEvento`, `test_seguranca.py`, `_parece_busca_por_cpf`, `_chave_da_conta`, `MatriculaDAO`, `test_admin_rejeita_valor_financeiro_invalido`, `test_perfil_e_foto.py`, `AlunoDAO`, `.contratar_plano`, `PlanoDAO`, `test_financeiro_admin_painel.py`, `test_limite_atingido_nao_mostra_login_a_quem_ja_entrou`, `test_sessao_sem_carimbo_de_credencial_e_recusada`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Are the 136 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 136 INFERRED edges - model-reasoned connections that need verification._
- **Are the 139 inferred relationships involving `criar_pagamento()` (e.g. with `PagamentoDAO` and `Pagamento`) actually correct?**
  _`criar_pagamento()` has 139 INFERRED edges - model-reasoned connections that need verification._
- **Are the 132 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 132 INFERRED edges - model-reasoned connections that need verification._
- **Are the 111 inferred relationships involving `logar_como_aluno()` (e.g. with `test_aluno_nao_alcanca_cobranca_de_outro_aluno()` and `test_checkout_recusa_cobranca_indisponivel()`) actually correct?**
  _`logar_como_aluno()` has 111 INFERRED edges - model-reasoned connections that need verification._