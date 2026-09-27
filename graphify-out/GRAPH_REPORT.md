# Graph Report - SistemaEXTREMETEAM  (2026-09-25)

## Corpus Check
- 132 files · ~189,528 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1740 nodes · 4503 edges · 105 communities (87 shown, 18 thin omitted)
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 932 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c4ad3faa`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- route
- Aluno Profile Page
- .efetivar_mudancas_por_prazo
- .listar_por_aluno
- test_limites_pagamento.py
- criar_aluno
- PagamentoDAO
- test_regressao_auditoria.py
- SistemaEXTREMETEAM Project
- test_mercado_pago_servico.py
- test_mercado_pago_oauth.py
- ProfessorDAO
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
- adm_bp.py
- MatriculaDAO
- test_perfil_e_foto.py
- convites.py
- MercadoPagoIndisponivel
- pagamento_polling.test.cjs
- mercado_pago_conta.py
- logar_como_aluno
- criar_pagamento
- PagamentoEvento
- d9e2f6a14c80_contatos_academia_perfis_professores.py
- test_professor_perfil.py
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
- _png_bomba
- URLPublicaInvalida
- servidor.py
- test_retorno_ignora_status_aprovado_da_query_string
- pagina_cadastro
- test_um_envio_ainda_pendente_continua_sendo_recusado
- pagina_login
- shot.mjs
- test_jpeg_grande_e_aceito_porque_decodifica_em_escala_reduzida
- usuario_bp.py
- Pagina
- _parece_busca_por_cpf
- e4b7c2a91d35_cadastro_administrativo_e_convite_de_acesso.py
- a1f0c3e75b92_schema_inicial.py
- Contrato do redesign — SistemaEXTREMETEAM
- _chave_da_conta
- test_decodificacao_de_imagem_e_serializada_no_processo
- Skills Disponíveis
- test_a_suite_nunca_escreve_na_pasta_de_uploads_do_projeto
- test_sessao_sem_carimbo_de_credencial_e_recusada
- test_o_mesmo_aviso_pode_ser_enviado_de_novo_em_outro_dia
- Relatório de segurança — Sistema Extreme Team
- limit
- test_uma_falha_do_provedor_nao_queima_todas_as_tentativas
- Turma
- test_email_gmail.py
- .contratar_plano
- erro_validacao_senha
- test_limite_atingido_nao_mostra_login_a_quem_ja_entrou
- _FakePaymentResource

## God Nodes (most connected - your core abstractions)
1. `PagamentoDAO` - 198 edges
2. `criar_pagamento()` - 141 edges
3. `criar_aluno()` - 134 edges
4. `logar_como_admin()` - 113 edges
5. `logar_como_aluno()` - 113 edges
6. `AlunoDAO` - 84 edges
7. `Aluno` - 54 edges
8. `MercadoPagoIndisponivel` - 41 edges
9. `ProfessorDAO` - 36 edges
10. `_matricular()` - 36 edges

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

## Communities (105 total, 18 thin omitted)

### Community 0 - "route"
Cohesion: 0.16
Nodes (22): alterar_senha_perfil(), _aluno_da_sessao(), _aluno_por_token(), atualizar_dados_perfil(), cancelar_mudanca_plano(), confirmar_email(), confirmar_presenca(), enviar_comprovante_manual_aluno() (+14 more)

### Community 1 - "Aluno Profile Page"
Cohesion: 0.05
Nodes (38): abrirmodal(), fechar(), icone_senha, input_senha, modal, mostrarSenha(), campoDuracao, campoPreco (+30 more)

### Community 3 - ".listar_por_aluno"
Cohesion: 0.13
Nodes (27): test_escolher_plano_cria_mensalidade_e_redireciona_para_pix(), test_plano_invalido_nao_cria_mensalidade(), test_reenvio_da_contratacao_reutiliza_mensalidade(), test_valor_enviado_pelo_navegador_e_ignorado(), _pagar(), Vigência do plano: o que decide "Plano ativo" é o período pago, não o cadastro.…, Mensalidade paga cobrindo um período - o que de fato ativa o plano., Quem paga uma cobrança vencida há semanas tem de receber os 30 dias a partir da… (+19 more)

### Community 4 - "test_limites_pagamento.py"
Cohesion: 0.15
Nodes (15): consultar_mp(), fixture, parametrize, Limites de pagamento por conta, com o provedor inteiramente simulado., _sessao_aluno(), test_admin_limite_por_usuario_persiste_entre_sessoes(), test_alunos_no_mesmo_ip_tem_limites_separados(), test_anonimos_limitados_por_ip_sem_consultar_provedor() (+7 more)

### Community 5 - "criar_aluno"
Cohesion: 0.17
Nodes (29): Persistência dos pedidos de troca de plano agendados para a próxima renovação., SolicitacaoPlanoDAO, criar_aluno(), test_aluno_existente_continua_entrando_normalmente(), test_area_do_aluno_renderiza_telas_independentes_do_menu(), test_plano_atual_continua_disponivel_para_gerar_cobranca(), _agendar(), _pagar() (+21 more)

### Community 6 - "PagamentoDAO"
Cohesion: 0.10
Nodes (25): PagamentoDAO, Status como o painel deve LER, com o vencimento aplicado na própria consulta. A…, Carrega aluno e plano junto das mensalidades. O template do painel lê…, Lista completa (sem paginar). Mantida para relatórios e testes., Uma página de mensalidades, recortada pelo banco (LIMIT/OFFSET). O painel…, Totais do painel financeiro - sempre calculados no backend a partir do banco,…, True se já existe um Pix ou um checkout válido emitido para esta cobrança.…, True se a cobrança Pix já gerada para este pagamento ainda pode ser… (+17 more)

### Community 7 - "test_regressao_auditoria.py"
Cohesion: 0.06
Nodes (30): _contar_selects_em_alunos(), _credencial(), Regressões da auditoria de segurança, desempenho e confiabilidade. Cada caso…, Head-of-line blocking: a primeira linha falhando não pode impedir as seguintes.…, Uma linha `desistiu` nunca foi entregue: recusar o reenvio fazia a tela dizer…, Persistência não é retomada: alguém precisa acordar a fila quando o adiamento…, A conta de maior privilégio não pode ser a única isenta da revogação., Conferir a credencial do admin custava um scrypt em TODO login. São ~74 ms e… (+22 more)

### Community 9 - "test_mercado_pago_servico.py"
Cohesion: 0.09
Nodes (34): ambiente_mercado_pago(), Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, Diz se a integracao esta apontando para producao ou para o sandbox. Prioriza a…, validar_assinatura_webhook(), Hipótese: uma notificação capturada ontem pode ser reenviada hoje., `ts=nan` fazia a comparação da janela dar False e passava pela checagem de…, test_webhook_recusa_assinatura_antiga(), test_webhook_recusa_ts_nao_numerico_finito() (+26 more)

### Community 10 - "test_mercado_pago_oauth.py"
Cohesion: 0.05
Nodes (68): MercadoPagoConexao, Conta do Mercado Pago que a academia autorizou por OAuth. Uma linha só (a…, _agora(), _ajustar(), api_mp(), _conectar(), _dados_conexao(), oauth_env() (+60 more)

### Community 11 - "ProfessorDAO"
Cohesion: 0.12
Nodes (17): gerenciar_turmas(), remover_professor(), ProfessorDAO, Professor, Cadastrar Professor Form, logar_como_professor(), fixture, Hipótese: a foto continua acessível por URL depois de tirar a publicação. (+9 more)

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
Nodes (25): _acesso_permitido(), criar_pix_mensalidade(), _forma_pagamento_confirmada(), _pagamento_mp_mais_relevante(), _pagamento_ou_none(), _pix_expirado(), _processar_status_mp(), limitar_consulta_pagamento (+17 more)

### Community 18 - "logar_como_admin"
Cohesion: 0.06
Nodes (76): _convidar_cadastro_existente(), _convidar_cadastro_existente_por_id(), Cadastro administrativo que alguém tentou recriar pelo formulário público. Em…, Versão para thread de fundo: a sessão da requisição não vale fora dela., AlunoDAO, Matrícula feita no balcão: sem login, sem senha e sem convite de acesso. Nasce…, Uma página de alunos já cadastrados, recortada e filtrada pelo banco. O painel…, Aluno (+68 more)

### Community 19 - ".buscar_por_id"
Cohesion: 0.16
Nodes (26): _assinar(), _pagamento_mp(), _preparar_retorno(), Pix aberto e checkout concluído ao mesmo tempo: a consulta pelo…, test_retorno_com_aprovacao_confirmada_marca_pago(), test_retorno_com_mp_indisponivel_avisa_sem_mudar_status(), test_retorno_de_boleto_avisa_sobre_o_prazo(), test_retorno_de_sucesso_nao_marca_pago_sem_confirmacao() (+18 more)

### Community 20 - "checkout_bp.py"
Cohesion: 0.11
Nodes (24): abrir_checkout(), _acesso_permitido(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), limitar_consulta_pagamento, limitar_criacao_pagamento, route (+16 more)

### Community 21 - "pix.js"
Cohesion: 0.33
Nodes (14): abrirPix(), alvoDoRotulo(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), liberarBotao(), limparConteudoAnterior() (+6 more)

### Community 22 - "config.py"
Cohesion: 0.07
Nodes (34): _paginar(), Aplica LIMIT/OFFSET e conta o total numa consulta separada e barata. A contagem…, Decimal, Matricula, Pagamento, _para_decimal(), Status a exibir, com o vencimento já aplicado. Uma cobrança `pendente` cujo…, Plano (+26 more)

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
Nodes (45): _assinar(), _pagamento_mp(), _preparar_para_conciliacao(), parametrize, Auditoria de segurança: sondas escritas para TENTAR quebrar as regras. Nenhum…, Hipótese: a sessão de professor é aceita nas rotas financeiras do aluno., Hipótese: como o JS agora usa fetch, o POST perdeu a exigência de CSRF., Hipótese: as demais rotas de dinheiro aceitam POST sem token. (+37 more)

### Community 34 - "turma_bp.py"
Cohesion: 0.13
Nodes (26): _acesso_permitido(), cadastrar_professor(), desmatricular_aluno(), detalhe_turma(), editar_professor(), foto_professor(), matricular_aluno(), painel_professor() (+18 more)

### Community 35 - "adm_bp.py"
Cohesion: 0.08
Nodes (50): _aluno_do_cpf_ou_painel(), aprovar_aluno(), aprovar_comprovante_manual(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_aluno(), cadastrar_pagamento(), cadastrar_plano() (+42 more)

### Community 36 - "MatriculaDAO"
Cohesion: 0.19
Nodes (16): MatriculaDAO, Presenca, impressao_credencial(), Resumo curto e não reversível do hash da senha, guardado na sessão. Nunca é a…, Valor que representa a credencial administrativa em vigor, ou None se não há…, referencia_credencial_admin(), parametrize, test_aluno_confirma_sua_frequencia() (+8 more)

### Community 37 - "test_perfil_e_foto.py"
Cohesion: 0.43
Nodes (6): _imagem_jpeg_valida(), test_admin_acessa_foto_de_qualquer_aluno(), test_aluno_nao_acessa_foto_de_outro_aluno(), test_professor_ve_foto_de_aluno_da_propria_turma(), test_substituir_e_remover_foto(), test_upload_de_foto_valida()

### Community 38 - "convites.py"
Cohesion: 0.14
Nodes (20): solicitar_troca_email(), aluno_do_token(), ConviteIndisponivel, descartar(), enviar(), gerar_token(), _hash(), RuntimeError (+12 more)

### Community 41 - "MercadoPagoIndisponivel"
Cohesion: 0.17
Nodes (17): buscar_pagamento(), buscar_pagamentos_por_referencia(), cancelar_pagamento(), MercadoPagoIndisponivel, Consulta o pagamento diretamente na API do Mercado Pago - fonte de verdade de…, Lista os pagamentos que o Mercado Pago associa a uma external_reference. Usada…, Cancela uma cobranca Pix pendente no Mercado Pago. Best-effort: nunca lanca., Falha de transporte (timeout/DNS/conexao) ao falar com a API do Mercado Pago. (+9 more)

### Community 42 - "pagamento_polling.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 43 - "mercado_pago_conta.py"
Cohesion: 0.10
Nodes (35): access_token_vigente(), _agora(), ambiente_da_conexao(), _cifrar(), _client_id(), _client_secret(), ConexaoIlegivel, _decifrar() (+27 more)

### Community 44 - "logar_como_aluno"
Cohesion: 0.09
Nodes (44): logar_como_aluno(), _mockar_preferencia(), parametrize, Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala…, Um boleto pendente do Checkout Pro grava provider_payment_id, mas não é Pix:…, _resposta_preferencia(), test_abertura_json_navega_sem_redirecionar_post_externo(), test_admin_tambem_pode_abrir_checkout() (+36 more)

### Community 45 - "criar_pagamento"
Cohesion: 0.25
Nodes (21): criar_pagamento(), _assinar(), _resposta_consulta(), _resposta_criacao(), test_admin_tambem_pode_gerar_pix(), test_aluno_gera_pix_da_propria_mensalidade(), test_aluno_nao_acessa_mensalidade_de_outro_aluno(), test_falha_de_indisponibilidade_do_mp_retorna_503() (+13 more)

### Community 46 - "PagamentoEvento"
Cohesion: 0.11
Nodes (12): Primeiro dia não coberto por outra mensalidade do mesmo aluno., Define o período coberto por uma mensalidade que ainda não tem um (lançamento…, Abre o período de acesso no momento em que o pagamento é confirmado. Se a…, Reescreve os campos denormalizados do aluno a partir das mensalidades.…, forma_pagamento vem do que o Mercado Pago confirmou na consulta à API ('pix',…, Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.…, PagamentoEvento, Histórico de auditoria de uma mensalidade (nunca grava credenciais ou dados… (+4 more)

### Community 47 - "d9e2f6a14c80_contatos_academia_perfis_professores.py"
Cohesion: 0.83
Nodes (3): _campos_professor(), downgrade(), upgrade()

### Community 49 - "test_professor_perfil.py"
Cohesion: 0.22
Nodes (9): _foto(), pasta_fotos(), professor(), fixture, test_edicao_professor_tem_protecao_csrf(), test_falha_ao_salvar_preserva_foto_anterior(), test_publicar_e_retirar_foto_do_site(), test_substituir_remover_e_recusar_foto_falsa() (+1 more)

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

### Community 56 - "ConfiguracaoInvalida"
Cohesion: 0.27
Nodes (12): _autorizacao_valida(), callback(), conectar(), desconectar(), limit, route, O state devolvido é o que ESTA sessão emitiu, há pouco tempo?, Só monta o state/PKCE na sessão e manda o administrador ao Mercado Pago. É um… (+4 more)

### Community 57 - "fila_email.py"
Cohesion: 0.06
Nodes (40): EmailPendente, espera_da_proxima_tentativa(), Fila de e-mails no banco. Aviso e cobrança coletivos saíam um a um dentro da…, contar_falhados(), contar_pendentes(), disparar(), enfileirar(), enfileirar_transacional() (+32 more)

### Community 58 - "test_migracao_cadastro_administrativo.py"
Cohesion: 0.40
Nodes (3): banco_antigo(), fixture, Verifica a migração em um banco isolado com o schema anterior e dados.

### Community 59 - "salvar_foto_perfil"
Cohesion: 0.16
Nodes (20): ArquivoInvalido, caminho_arquivo(), _conferir_dimensoes(), _detectar_tipo_imagem_real(), ImagemGrandeDemais, _pasta(), Exception, _raiz_uploads() (+12 more)

### Community 60 - "test_keep_alive.py"
Cohesion: 0.16
Nodes (7): ambiente_limpo(), fixture, parametrize, Garante que o keep-alive fica desligado por padrão e só pinga a própria origem., test_intervalo_fica_dentro_da_faixa(), test_nao_liga_com_valor_negativo(), test_ping_so_considera_200_como_sucesso()

### Community 61 - "gmail_conta.py"
Cohesion: 0.09
Nodes (33): configuracoes(), _pagina(), route, Academia, GmailConexao, link_email(), Normalização de contatos profissionais antes de montar links públicos., validar_email() (+25 more)

### Community 62 - "mercado_pago.py"
Cohesion: 0.15
Nodes (22): _base_url_opcional(), base_url_publica(), criar_pagamento_pix(), criar_preferencia_checkout(), _erro_menciona(), _erro_menciona_expiracao(), _extrair_dados_pix(), _normalizar_pagamento() (+14 more)

### Community 63 - "test_arranque_seguranca.py"
Cohesion: 0.22
Nodes (14): _env_arranque(), Validações feitas por servidor.py no arranque (COOKIE_SECURE, TRUSTED_HOSTS,…, `python -m servicos.credenciais`: o hash sai entre aspas simples. O hash do…, Desenvolvimento local sem HTTPS (sem Caddy) não pode ficar travado., _rodar(), test_arranque_falha_com_cookie_secure_false_e_app_base_url_https(), test_arranque_falha_com_cookie_secure_invalido(), test_arranque_falha_sem_trusted_hosts() (+6 more)

### Community 64 - "_png_bomba"
Cohesion: 0.29
Nodes (7): _png_bomba(), Bomba de descompressão: arquivo minúsculo, imagem gigante. O PNG aqui tem 285…, PNG válido e altamente compressível: linhas zeradas, como uma bomba real., O teto de pixels vale para a FOTO, que é decodificada, não para o comprovante.…, test_comprovante_a4_escaneado_continua_sendo_aceito(), test_foto_de_perfil_mantem_o_teto_de_pixels(), test_png_com_pixels_demais_e_recusado_pelo_cabecalho()

### Community 66 - "URLPublicaInvalida"
Cohesion: 0.22
Nodes (13): iniciar(), _intervalo(), _laco(), _ligado(), parar(), _pingar(), Mantém a aplicação acordada em hospedagens que hibernam por inatividade. Uma…, Encerra o laço. Usado pelos testes; em produção a thread é daemon. (+5 more)

### Community 67 - "servidor.py"
Cohesion: 0.05
Nodes (48): admin_requerido, after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, callback(), conectar(), desconectar(), route (+40 more)

### Community 69 - "pagina_cadastro"
Cohesion: 0.25
Nodes (14): _em_segundo_plano(), _enviar_em_segundo_plano(), pagina_cadastro(), Roda `tarefa` fora da requisição, para o tempo de resposta não revelar nada. Em…, E-mail COM token (recuperação, confirmação): não pode ir para a `fila_email`. A…, recuperar_senha(), cpf_valido(), data_nascimento_valida() (+6 more)

### Community 71 - "pagina_login"
Cohesion: 0.12
Nodes (16): pagina_login(), iniciar_sessao(), Grava na sessão atual a credencial em vigor (login ou troca de senha bem-…, Dá um identificador à sessão recém-aberta, para o logout poder revogá-la.…, registrar_credencial(), admin_configurado(), comparar_em_tempo_constante(), credencial_admin_confere() (+8 more)

### Community 72 - "shot.mjs"
Cohesion: 0.29
Nodes (5): { chromium }, contextos, CREDS, jobs, require

### Community 74 - "usuario_bp.py"
Cohesion: 0.19
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

### Community 84 - "Skills Disponíveis"
Cohesion: 0.22
Nodes (8): Assistente e Automação (Antigravity), Ciências e Bioinformática (Plugins de Ciência), Dados e Google Cloud Platform (GCP), Desenvolvimento Mobile e Flutter/Dart, Desenvolvimento Web e Frontend, Firebase e Backend, GenAI e Machine Learning, Skills Disponíveis

### Community 90 - "Relatório de segurança — Sistema Extreme Team"
Cohesion: 0.29
Nodes (6): Controles verificados, Histórico de auditorias, Pendências não relacionadas a segurança, Relatório de segurança — Sistema Extreme Team, Situação atual (22/09/2026 — 2ª rodada), Validação executada em 22/09/2026

### Community 96 - "Turma"
Cohesion: 0.20
Nodes (11): cadastrar_turma(), remover_turma(), TurmaDAO, Turma, Cadastrar Turma Form, Sonda: a data vem da query string e é convertida sem tratamento., test_data_invalida_na_turma_nao_derruba_a_rota(), test_escolher_plano_com_turma_cria_matricula() (+3 more)

### Community 99 - ".contratar_plano"
Cohesion: 0.10
Nodes (12): O que aconteceu numa tentativa de contratar/renovar/trocar de plano., Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda. O…, Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, Com uma troca já agendada, só dois planos fazem sentido num pedido de…, A cobrança do período seguinte tem de nascer no plano que o aluno agendou.…, `pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -…, ResultadoContratacao (+4 more)

### Community 100 - "erro_validacao_senha"
Cohesion: 0.20
Nodes (10): ativar_acesso(), Transforma um cadastro feito no balcão na conta do próprio aluno. Quem chega…, mascarar_email(), Mostra o bastante do e-mail para o dono se reconhecer, sem revelá-lo a…, _carregar_senhas_comuns(), erro_confirmacao_senha(), erro_validacao_senha(), Retorna uma mensagem quando a senha é curta, comum ou igual ao identificador. (+2 more)

## Knowledge Gaps
- **83 isolated node(s):** `Pendências não relacionadas a segurança`, `Controles verificados`, `Validação executada em 22/09/2026`, `Histórico de auditorias`, `gradePlanos` (+78 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PagamentoDAO` connect `PagamentoDAO` to `route`, `.efetivar_mudancas_por_prazo`, `.listar_por_aluno`, `criar_aluno`, `test_regressao_auditoria.py`, `pix_bp.py`, `logar_como_admin`, `.buscar_por_id`, `checkout_bp.py`, `config.py`, `test_auditoria_seguranca.py`, `adm_bp.py`, `MatriculaDAO`, `logar_como_aluno`, `criar_pagamento`, `PagamentoEvento`, `test_retorno_ignora_status_aprovado_da_query_string`, `usuario_bp.py`, `Turma`, `.contratar_plano`?**
  _High betweenness centrality (0.147) - this node is a cross-community bridge._
- **Why does `logar_como_admin()` connect `logar_como_admin` to `Turma`, `.listar_por_aluno`, `MatriculaDAO`, `test_limites_pagamento.py`, `criar_aluno`, `test_perfil_e_foto.py`, `test_regressao_auditoria.py`, `PagamentoDAO`, `test_mercado_pago_oauth.py`, `ProfessorDAO`, `logar_como_aluno`, `criar_pagamento`, `test_professor_perfil.py`, `servidor.py`, `.buscar_por_id`, `test_seguranca.py`, `config.py`, `gmail_conta.py`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Why does `AlunoDAO` connect `logar_como_admin` to `turma_bp.py`, `adm_bp.py`, `pagina_cadastro`, `PagamentoDAO`, `pagina_login`, `criar_aluno`, `test_perfil_e_foto.py`, `usuario_bp.py`, `test_regressao_auditoria.py`, `test_seguranca.py`, `config.py`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Are the 134 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 134 INFERRED edges - model-reasoned connections that need verification._
- **Are the 139 inferred relationships involving `criar_pagamento()` (e.g. with `PagamentoDAO` and `Pagamento`) actually correct?**
  _`criar_pagamento()` has 139 INFERRED edges - model-reasoned connections that need verification._
- **Are the 132 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 132 INFERRED edges - model-reasoned connections that need verification._
- **Are the 111 inferred relationships involving `logar_como_admin()` (e.g. with `test_admin_salva_atualiza_e_limpa_contatos()` and `test_csrf_configuracoes()`) actually correct?**
  _`logar_como_admin()` has 111 INFERRED edges - model-reasoned connections that need verification._