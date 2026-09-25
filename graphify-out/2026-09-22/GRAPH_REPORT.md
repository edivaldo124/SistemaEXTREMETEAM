# Graph Report - SistemaEXTREMETEAM  (2026-09-22)

## Corpus Check
- 132 files · ~187,952 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1735 nodes · 4534 edges · 112 communities (99 shown, 13 thin omitted)
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 946 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5ffc6e51`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_professor_perfil.py
- Admin Dashboard Page
- Aluno
- .listar_por_aluno
- test_limites_pagamento.py
- test_mudanca_plano.py
- pagina_perfil
- criar_aluno
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
- adm_bp.py
- MatriculaDAO
- test_regressao_auditoria.py
- convites.py
- Academia
- pagamento_polling.test.cjs
- MercadoPagoIndisponivel
- logar_como_aluno
- criar_pagamento
- PagamentoDAO
- d9e2f6a14c80_contatos_academia_perfis_professores.py
- .totais_periodo
- botao_ocupado.test.cjs
- test_seguranca.py
- checkout_abertura.test.cjs
- filtros_financeiro.js
- gunicorn.conf.py
- mercado_pago_oauth_bp.py
- fila_email.py
- test_migracao_cadastro_administrativo.py
- salvar_foto_perfil
- test_keep_alive.py
- extreme.css
- mercado_pago.py
- test_arranque_seguranca.py
- ResultadoContratacao
- erro_validacao_senha
- servidor.py
- autorizacao.py
- pagina_cadastro
- _png_bomba
- pagina_login
- shot.mjs
- limites_pagamento.py
- usuario_bp.py
- index.js
- _tem_limite
- e4b7c2a91d35_cadastro_administrativo_e_convite_de_acesso.py
- a1f0c3e75b92_schema_inicial.py
- Contrato do redesign — SistemaEXTREMETEAM
- _chave_da_conta
- Pagamento
- Skills Disponíveis
- Aluno Detail/Admin Page
- Aluno Profile Page
- .listar_paginado
- Relatório de segurança — Sistema Extreme Team
- gmail_oauth_bp.py
- test_admin_rejeita_valor_financeiro_invalido
- test_perfil_e_foto.py
- test_email_gmail.py
- _enviar_em_segundo_plano
- ._conflita_com_agendamento
- Login Page
- capturar_emails
- keep_alive.py
- .bloquear_pendente_do_aluno
- test_retorno_ignora_status_aprovado_da_query_string
- test_sessao_sem_carimbo_de_credencial_e_recusada
- test_login_de_aluno_nao_paga_o_hash_do_admin
- _FakePaymentResource
- _convidar_cadastro_existente

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

## Communities (112 total, 13 thin omitted)

### Community 0 - "test_professor_perfil.py"
Cohesion: 0.17
Nodes (12): _foto(), pasta_fotos(), fixture, parametrize, test_admin_salva_perfil_sem_alterar_acesso(), test_apenas_admin_edita_perfil(), test_contato_invalido_nao_salva_nenhuma_alteracao(), test_edicao_professor_tem_protecao_csrf() (+4 more)

### Community 1 - "Admin Dashboard Page"
Cohesion: 0.16
Nodes (11): campoDuracao, campoPreco, formatadorDePreco, formularioPlano, Confirm Dialog Component, Admin Dashboard Page, Cadastrar Plano Form, Professor Turmas Page (+3 more)

### Community 2 - "Aluno"
Cohesion: 0.10
Nodes (11): Matrícula feita no balcão: sem login, sem senha e sem convite de acesso. Nasce…, Aluno, Se existe uma conta de acesso, e não se o aluno está em dia ou matriculado.…, Convite de acesso já enviado e ainda não usado (a validade é checada na rota)., Chave do estado da CONTA - nunca da situação financeira nem da matrícula., test_cadastro_publico_recusa_confirmacao_diferente(), test_cadastro_publico_recusa_confirmacao_vazia(), _dados_cadastro() (+3 more)

### Community 3 - ".listar_por_aluno"
Cohesion: 0.14
Nodes (28): Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, `pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -…, test_escolher_plano_cria_mensalidade_e_redireciona_para_pix(), test_plano_invalido_nao_cria_mensalidade(), test_reenvio_da_contratacao_reutiliza_mensalidade(), test_valor_enviado_pelo_navegador_e_ignorado(), _pagar(), Vigência do plano: o que decide "Plano ativo" é o período pago, não o cadastro.… (+20 more)

### Community 4 - "test_limites_pagamento.py"
Cohesion: 0.15
Nodes (15): consultar_mp(), fixture, parametrize, Limites de pagamento por conta, com o provedor inteiramente simulado., _sessao_aluno(), test_admin_limite_por_usuario_persiste_entre_sessoes(), test_alunos_no_mesmo_ip_tem_limites_separados(), test_anonimos_limitados_por_ip_sem_consultar_provedor() (+7 more)

### Community 5 - "test_mudanca_plano.py"
Cohesion: 0.18
Nodes (23): detalhes_usuario(), Persistência dos pedidos de troca de plano agendados para a próxima renovação., SolicitacaoPlanoDAO, _agendar(), _pagar(), Mudança para um plano mais barato agendada para a próxima renovação. Regra…, O admin pode estornar/cancelar a mensalidade que sustentava a vigência depois…, test_admin_cancela_a_solicitacao() (+15 more)

### Community 6 - "pagina_perfil"
Cohesion: 0.14
Nodes (15): pagina_perfil(), _turma_do_formulario(), mensalidade_destaque(), Escolhe a mensalidade mais relevante para o card 'Minha mensalidade': a mais…, True se já existe um Pix ou um checkout válido emitido para esta cobrança.…, True se a cobrança Pix já gerada para este pagamento ainda pode ser…, provider_payment_id sozinho não basta: pagamentos do Checkout Pro…, test_mensalidade_destaque_prioriza_a_mais_proxima_de_vencer() (+7 more)

### Community 7 - "criar_aluno"
Cohesion: 0.08
Nodes (28): criar_aluno(), test_aluno_existente_continua_entrando_normalmente(), test_busca_financeira_trata_curingas_como_texto(), test_painel_financeiro_busca_por_nome_do_aluno(), test_painel_financeiro_exige_admin(), test_painel_financeiro_filtra_por_status(), test_painel_financeiro_mostra_totais_do_backend(), test_admin_pode_remover_o_plano_do_cadastro() (+20 more)

### Community 9 - "test_mercado_pago_servico.py"
Cohesion: 0.08
Nodes (39): ambiente_mercado_pago(), Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, Diz se a integracao esta apontando para producao ou para o sandbox. Prioriza a…, validar_assinatura_webhook(), Hipótese: uma notificação capturada ontem pode ser reenviada hoje., `ts=nan` fazia a comparação da janela dar False e passava pela checagem de…, test_webhook_recusa_assinatura_antiga(), test_webhook_recusa_ts_nao_numerico_finito() (+31 more)

### Community 10 - "test_mercado_pago_oauth.py"
Cohesion: 0.05
Nodes (70): MercadoPagoConexao, Conta do Mercado Pago que a academia autorizou por OAuth. Uma linha só (a…, Esquece a conta conectada. Devolve True se havia uma., remover_conexao(), _agora(), _ajustar(), api_mp(), _conectar() (+62 more)

### Community 11 - "Professor"
Cohesion: 0.11
Nodes (22): ProfessorDAO, TurmaDAO, Professor, Turma, logar_como_professor(), fixture, Hipótese: a foto continua acessível por URL depois de tirar a publicação., Hipótese: os contatos vazam na home antes de a publicação ser marcada. (+14 more)

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
Cohesion: 0.12
Nodes (27): _acesso_permitido(), criar_pix_mensalidade(), _forma_pagamento_confirmada(), _pagamento_ou_none(), _pix_expirado(), _processar_status_mp(), limitar_consulta_pagamento, limitar_criacao_pagamento (+19 more)

### Community 18 - "logar_como_admin"
Cohesion: 0.16
Nodes (43): AlunoDAO, logar_como_admin(), _matricular(), Cadastro de aluno pela administração, ativação de acesso e confirmação de…, test_admin_lanca_e_baixa_mensalidade_de_aluno_sem_acesso(), test_admin_matricula_aluno_sem_email_senha_nem_acesso(), test_admin_nao_pode_apagar_o_usuario_de_uma_conta_ativa(), test_admin_pode_deixar_cadastro_de_balcao_sem_usuario_e_sem_email() (+35 more)

### Community 19 - ".buscar_por_id"
Cohesion: 0.16
Nodes (26): _assinar(), _pagamento_mp(), _preparar_retorno(), Pix aberto e checkout concluído ao mesmo tempo: a consulta pelo…, test_retorno_com_aprovacao_confirmada_marca_pago(), test_retorno_com_mp_indisponivel_avisa_sem_mudar_status(), test_retorno_de_boleto_avisa_sobre_o_prazo(), test_retorno_de_sucesso_nao_marca_pago_sem_confirmacao() (+18 more)

### Community 20 - "checkout_bp.py"
Cohesion: 0.10
Nodes (28): abrir_checkout(), _acesso_permitido(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), limitar_consulta_pagamento, limitar_criacao_pagamento, route (+20 more)

### Community 21 - "pix.js"
Cohesion: 0.33
Nodes (14): abrirPix(), alvoDoRotulo(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), liberarBotao(), limparConteudoAnterior() (+6 more)

### Community 22 - "config.py"
Cohesion: 0.06
Nodes (32): Pagina, _paginar(), Uma fatia de resultados já recortada pelo banco, com o que a navegação precisa., Uma página existe mesmo quando está vazia. Sem isto, `__len__` fazia `{% if…, Aplica LIMIT/OFFSET e conta o total numa consulta separada e barata. A contagem…, Decimal, Matricula, _para_decimal() (+24 more)

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

### Community 34 - "turma_bp.py"
Cohesion: 0.20
Nodes (16): _acesso_permitido(), cadastrar_professor(), cadastrar_turma(), desmatricular_aluno(), detalhe_turma(), gerenciar_turmas(), matricular_aluno(), painel_professor() (+8 more)

### Community 35 - "adm_bp.py"
Cohesion: 0.07
Nodes (51): _aluno_do_cpf_ou_painel(), aprovar_aluno(), aprovar_comprovante_manual(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_aluno(), cadastrar_pagamento(), cadastrar_plano() (+43 more)

### Community 36 - "MatriculaDAO"
Cohesion: 0.19
Nodes (16): MatriculaDAO, Presenca, impressao_credencial(), Resumo curto e não reversível do hash da senha, guardado na sessão. Nunca é a…, Valor que representa a credencial administrativa em vigor, ou None se não há…, referencia_credencial_admin(), parametrize, test_aluno_confirma_sua_frequencia() (+8 more)

### Community 37 - "test_regressao_auditoria.py"
Cohesion: 0.07
Nodes (22): _contar_selects_em_alunos(), _credencial(), Regressões da auditoria de segurança, desempenho e confiabilidade. Cada caso…, Head-of-line blocking: a primeira linha falhando não pode impedir as seguintes.…, Uma linha `desistiu` nunca foi entregue: recusar o reenvio fazia a tela dizer…, A revivência vale só para o abandonado: clique duplo continua virando um envio., Persistência não é retomada: alguém precisa acordar a fila quando o adiamento…, O limite protege a memória, não pune a resolução: JPEG usa `draft()`. (+14 more)

### Community 38 - "convites.py"
Cohesion: 0.12
Nodes (24): solicitar_troca_email(), aluno_do_token(), ConviteIndisponivel, descartar(), enviar(), gerar_token(), _hash(), RuntimeError (+16 more)

### Community 41 - "Academia"
Cohesion: 0.13
Nodes (19): configuracoes(), _pagina(), route, editar_professor(), Academia, link_email(), Normalização de contatos profissionais antes de montar links públicos., validar_email() (+11 more)

### Community 42 - "pagamento_polling.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 43 - "MercadoPagoIndisponivel"
Cohesion: 0.11
Nodes (35): access_token_vigente(), _agora(), ambiente_da_conexao(), _cifrar(), _client_id(), _client_secret(), ConexaoIlegivel, _decifrar() (+27 more)

### Community 44 - "logar_como_aluno"
Cohesion: 0.10
Nodes (43): logar_como_aluno(), _mockar_preferencia(), parametrize, Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala…, Um boleto pendente do Checkout Pro grava provider_payment_id, mas não é Pix:…, _resposta_preferencia(), test_abertura_json_navega_sem_redirecionar_post_externo(), test_admin_tambem_pode_abrir_checkout() (+35 more)

### Community 45 - "criar_pagamento"
Cohesion: 0.25
Nodes (21): criar_pagamento(), _assinar(), _resposta_consulta(), _resposta_criacao(), test_admin_tambem_pode_gerar_pix(), test_aluno_gera_pix_da_propria_mensalidade(), test_aluno_nao_acessa_mensalidade_de_outro_aluno(), test_falha_de_indisponibilidade_do_mp_retorna_503() (+13 more)

### Community 46 - "PagamentoDAO"
Cohesion: 0.10
Nodes (18): PagamentoDAO, Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda. O…, Aplica um pedido agendado cujo período de origem já terminou sem renovação.…, Primeiro dia não coberto por outra mensalidade do mesmo aluno., Define o período coberto por uma mensalidade que ainda não tem um (lançamento…, Abre o período de acesso no momento em que o pagamento é confirmado. Se a…, Reescreve os campos denormalizados do aluno a partir das mensalidades.…, Solta a preferência atual para que a próxima tentativa crie uma nova. Nunca… (+10 more)

### Community 47 - "d9e2f6a14c80_contatos_academia_perfis_professores.py"
Cohesion: 0.83
Nodes (3): _campos_professor(), downgrade(), upgrade()

### Community 49 - ".totais_periodo"
Cohesion: 0.14
Nodes (10): Status como o painel deve LER, com o vencimento aplicado na própria consulta. A…, Carrega aluno e plano junto das mensalidades. O template do painel lê…, Lista completa (sem paginar). Mantida para relatórios e testes., Uma página de mensalidades, recortada pelo banco (LIMIT/OFFSET). O painel…, Totais do painel financeiro - sempre calculados no backend a partir do banco,…, test_listar_filtrado_por_status_e_busca_de_aluno(), test_financeiro_pagina_no_banco_sem_carregar_tudo(), test_indicadores_e_tabela_concordam_na_primeira_abertura() (+2 more)

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

### Community 56 - "mercado_pago_oauth_bp.py"
Cohesion: 0.36
Nodes (9): _autorizacao_valida(), callback(), conectar(), desconectar(), limit, route, O state devolvido é o que ESTA sessão emitiu, há pouco tempo?, Só monta o state/PKCE na sessão e manda o administrador ao Mercado Pago. É um… (+1 more)

### Community 57 - "fila_email.py"
Cohesion: 0.06
Nodes (40): EmailPendente, espera_da_proxima_tentativa(), Fila de e-mails no banco. Aviso e cobrança coletivos saíam um a um dentro da…, contar_falhados(), contar_pendentes(), disparar(), enfileirar(), enfileirar_transacional() (+32 more)

### Community 58 - "test_migracao_cadastro_administrativo.py"
Cohesion: 0.40
Nodes (3): banco_antigo(), fixture, Verifica a migração em um banco isolado com o schema anterior e dados.

### Community 59 - "salvar_foto_perfil"
Cohesion: 0.13
Nodes (25): enviar_comprovante_manual_aluno(), enviar_foto_perfil(), ArquivoInvalido, caminho_arquivo(), _conferir_dimensoes(), _detectar_tipo_imagem_real(), ImagemGrandeDemais, _pasta() (+17 more)

### Community 60 - "test_keep_alive.py"
Cohesion: 0.16
Nodes (7): ambiente_limpo(), fixture, parametrize, Garante que o keep-alive fica desligado por padrão e só pinga a própria origem., test_intervalo_fica_dentro_da_faixa(), test_nao_liga_com_valor_negativo(), test_ping_so_considera_200_como_sucesso()

### Community 61 - "extreme.css"
Cohesion: 0.22
Nodes (4): cadastro-form Registration Form, Cadastro (Registration) Page, Recuperar Senha Form, Recuperar Senha Page

### Community 62 - "mercado_pago.py"
Cohesion: 0.13
Nodes (27): _base_url_opcional(), base_url_publica(), buscar_pagamentos_por_referencia(), cancelar_pagamento(), criar_pagamento_pix(), criar_preferencia_checkout(), _erro_menciona(), _erro_menciona_expiracao() (+19 more)

### Community 63 - "test_arranque_seguranca.py"
Cohesion: 0.22
Nodes (14): _env_arranque(), Validações feitas por servidor.py no arranque (COOKIE_SECURE, TRUSTED_HOSTS,…, `python -m servicos.credenciais`: o hash sai entre aspas simples. O hash do…, Desenvolvimento local sem HTTPS (sem Caddy) não pode ficar travado., _rodar(), test_arranque_falha_com_cookie_secure_false_e_app_base_url_https(), test_arranque_falha_com_cookie_secure_invalido(), test_arranque_falha_sem_trusted_hosts() (+6 more)

### Community 66 - "erro_validacao_senha"
Cohesion: 0.16
Nodes (13): alterar_senha_perfil(), _aluno_por_token(), confirmar_email(), Descarta todo link pendente que ainda autorizaria assumir ou redirecionar a…, Localiza o aluno pelo hash do token, filtrando no banco por uma coluna indexada., redefinir_senha(), _revogar_tokens_de_conta(), Grava na sessão atual a credencial em vigor (login ou troca de senha bem-… (+5 more)

### Community 67 - "servidor.py"
Cohesion: 0.05
Nodes (56): after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, Flask App Service (compose), Postgres DB Service (compose), postgres_data Volume, context_processor, errorhandler (+48 more)

### Community 68 - "autorizacao.py"
Cohesion: 0.21
Nodes (15): foto_professor(), aluno_autorizado(), aluno_requerido(), _credencial_confere(), encerrar_sessao(), professor_autorizado(), Autorização das rotas protegidas. A sessão diz quem *afirmou* ser quem; quem…, A sessão foi emitida para a credencial que vale AGORA? Uma sessão sem carimbo é… (+7 more)

### Community 69 - "pagina_cadastro"
Cohesion: 0.17
Nodes (20): ativar_acesso(), atualizar_dados_perfil(), pagina_cadastro(), limit, Transforma um cadastro feito no balcão na conta do próprio aluno. Quem chega…, recuperar_senha(), _parece_busca_por_cpf(), O termo é um CPF, ou um pedaço dele, e não um nome que por acaso tem número? (+12 more)

### Community 70 - "_png_bomba"
Cohesion: 0.29
Nodes (7): _png_bomba(), Bomba de descompressão: arquivo minúsculo, imagem gigante. O PNG aqui tem 285…, PNG válido e altamente compressível: linhas zeradas, como uma bomba real., O teto de pixels vale para a FOTO, que é decodificada, não para o comprovante.…, test_comprovante_a4_escaneado_continua_sendo_aceito(), test_foto_de_perfil_mantem_o_teto_de_pixels(), test_png_com_pixels_demais_e_recusado_pelo_cabecalho()

### Community 71 - "pagina_login"
Cohesion: 0.15
Nodes (14): pagina_login(), iniciar_sessao(), Dá um identificador à sessão recém-aberta, para o logout poder revogá-la.…, admin_configurado(), comparar_em_tempo_constante(), credencial_admin_confere(), gerar_hash_admin(), _main() (+6 more)

### Community 72 - "shot.mjs"
Cohesion: 0.29
Nodes (5): { chromium }, contextos, CREDS, jobs, require

### Community 73 - "limites_pagamento.py"
Cohesion: 0.50
Nodes (3): chave_pagamento(), Orçamentos compartilhados das chamadas interativas ao provedor de pagamento., A mesma conta mantém seu limite entre sessões, rotas e mensalidades. Alunos que…

### Community 74 - "usuario_bp.py"
Cohesion: 0.18
Nodes (22): _acesso_permitido_pagamento(), _aluno_da_sessao(), cancelar_mudanca_plano(), comprovante_mensalidade(), confirmar_presenca(), foto_perfil(), _pagamento_com_acesso_ou_404(), pagina_pagamento() (+14 more)

### Community 76 - "index.js"
Cohesion: 0.27
Nodes (8): abrirmodal(), fechar(), icone_senha, input_senha, modal, mostrarSenha(), meuModal Login Modal, Home Page

### Community 77 - "_tem_limite"
Cohesion: 0.20
Nodes (10): parametrize, Qualquer dígito no termo virava `CPF LIKE '%3%'` e devolvia a academia inteira., Rotas que custam hash de senha, processamento de imagem ou sondagem de token., Limites declarados por decorador NAQUELA rota. `resolve_limits` não serve aqui:…, Guarda do teste acima: uma rota sem limite precisa ser reprovada por ele., _tem_limite(), test_busca_so_trata_como_cpf_o_que_parece_cpf(), test_o_detector_de_limite_realmente_discrimina() (+2 more)

### Community 81 - "Contrato do redesign — SistemaEXTREMETEAM"
Cohesion: 0.09
Nodes (20): 0. Antes de escrever código, 1. Identidade visual (design tokens), 2. Logo oficial (usar SOMENTE a logo original), 3. Telas a implementar, 4. Regras e dados, 5. Forma de trabalhar, Painel administrativo (desktop, sidebar preta com o emblema do dragão), Prompt para o Claude Code — Redesign do SistemaEXTREMETEAM (+12 more)

### Community 82 - "_chave_da_conta"
Cohesion: 0.40
Nodes (5): _chave_da_conta(), Chave de limite por CONTA, caindo no IP só para quem não está autenticado. A…, Alunos atrás do mesmo IP (o Wi-Fi da academia) não dividem a cota., test_limite_de_upload_e_por_conta_e_nao_por_ip(), test_visitante_sem_sessao_ainda_e_limitado_por_ip()

### Community 83 - "Pagamento"
Cohesion: 0.22
Nodes (7): Pagamento, Status a exibir, com o vencimento já aplicado. Uma cobrança `pendente` cujo…, parametrize, test_duas_requisicoes_pix_reutilizam_uma_cobranca_postgres(), Quem paga uma cobrança vencida há semanas tem de receber os 30 dias a partir da…, test_cobranca_antiga_quitada_hoje_abre_o_periodo_a_partir_de_hoje(), cobranca()

### Community 84 - "Skills Disponíveis"
Cohesion: 0.22
Nodes (8): Assistente e Automação (Antigravity), Ciências e Bioinformática (Plugins de Ciência), Dados e Google Cloud Platform (GCP), Desenvolvimento Mobile e Flutter/Dart, Desenvolvimento Web e Frontend, Firebase e Backend, GenAI e Machine Learning, Skills Disponíveis

### Community 85 - "Aluno Detail/Admin Page"
Cohesion: 0.22
Nodes (7): Aluno Mensalidade Launch Form, Aluno Detail/Admin Page, Aluno Profile Update Form, preencherValor() Inline Script, Matrícula Form, Turma Detail Page, Presença Form

### Community 86 - "Aluno Profile Page"
Cohesion: 0.22
Nodes (5): formatadorDePreco, gradePlanos, Histórico de Mensalidades Section, Aluno Profile Page, Planos Disponíveis Section

### Community 89 - ".listar_paginado"
Cohesion: 0.29
Nodes (6): Uma página de alunos já cadastrados, recortada e filtrada pelo banco. O painel…, O CPF é guardado formatado; digitar só os números precisa encontrar mesmo assim., test_busca_do_admin_encontra_o_aluno_pelo_cpf_so_com_digitos(), test_busca_por_nome_com_numero_nao_devolve_todo_mundo(), test_paginacao_do_admin_ignora_pendentes_como_a_tela_sempre_fez(), test_painel_admin_pagina_alunos_no_banco()

### Community 90 - "Relatório de segurança — Sistema Extreme Team"
Cohesion: 0.29
Nodes (6): Controles verificados, Histórico de auditorias, Pendências não relacionadas a segurança, Relatório de segurança — Sistema Extreme Team, Situação atual (22/09/2026), Validação executada em 22/09/2026

### Community 94 - "gmail_oauth_bp.py"
Cohesion: 0.67
Nodes (5): callback(), conectar(), desconectar(), route, _voltar()

### Community 95 - "test_admin_rejeita_valor_financeiro_invalido"
Cohesion: 0.33
Nodes (6): parametrize, test_admin_rejeita_valor_financeiro_invalido(), test_confirmacao_aceita_unicode(), test_matricula_valida_dados_no_servidor(), test_novos_formularios_exigem_csrf(), test_rotas_de_matricula_e_convite_sao_so_do_admin()

### Community 96 - "test_perfil_e_foto.py"
Cohesion: 0.39
Nodes (6): _imagem_jpeg_valida(), test_admin_acessa_foto_de_qualquer_aluno(), test_aluno_nao_acessa_foto_de_outro_aluno(), test_aluno_ve_o_proprio_perfil(), test_substituir_e_remover_foto(), test_upload_de_foto_valida()

### Community 98 - "_enviar_em_segundo_plano"
Cohesion: 0.50
Nodes (4): _em_segundo_plano(), _enviar_em_segundo_plano(), Roda `tarefa` fora da requisição, para o tempo de resposta não revelar nada. Em…, E-mail COM token (recuperação, confirmação): não pode ir para a `fila_email`. A…

### Community 100 - "Login Page"
Cohesion: 0.50
Nodes (3): login-form Login Form, Login Page, Password Toggle Inline Script

### Community 102 - "capturar_emails"
Cohesion: 0.67
Nodes (3): capturar_emails(), fixture, Intercepta o envio e devolve os e-mails que teriam saído, com os links.

### Community 103 - "keep_alive.py"
Cohesion: 0.29
Nodes (9): iniciar(), _intervalo(), _laco(), _ligado(), parar(), _pingar(), Mantém a aplicação acordada em hospedagens que hibernam por inatividade. Uma…, Encerra o laço. Usado pelos testes; em produção a thread é daemon. (+1 more)

### Community 112 - "_convidar_cadastro_existente"
Cohesion: 0.50
Nodes (4): _convidar_cadastro_existente(), _convidar_cadastro_existente_por_id(), Cadastro administrativo que alguém tentou recriar pelo formulário público. Em…, Versão para thread de fundo: a sessão da requisição não vale fora dela.

## Knowledge Gaps
- **83 isolated node(s):** `modal`, `input_senha`, `icone_senha`, `formularioPlano`, `campoPreco` (+78 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PagamentoDAO` connect `PagamentoDAO` to `Aluno`, `.listar_por_aluno`, `test_mudanca_plano.py`, `pagina_perfil`, `criar_aluno`, `Professor`, `pix_bp.py`, `logar_como_admin`, `.buscar_por_id`, `checkout_bp.py`, `config.py`, `test_auditoria_seguranca.py`, `adm_bp.py`, `MatriculaDAO`, `test_regressao_auditoria.py`, `logar_como_aluno`, `criar_pagamento`, `.totais_periodo`, `test_seguranca.py`, `salvar_foto_perfil`, `ResultadoContratacao`, `usuario_bp.py`, `Pagamento`, `test_admin_rejeita_valor_financeiro_invalido`, `._conflita_com_agendamento`, `test_retorno_ignora_status_aprovado_da_query_string`?**
  _High betweenness centrality (0.178) - this node is a cross-community bridge._
- **Why does `AlunoDAO` connect `logar_como_admin` to `test_perfil_e_foto.py`, `turma_bp.py`, `adm_bp.py`, `Aluno`, `pagina_cadastro`, `test_mudanca_plano.py`, `pagina_login`, `criar_aluno`, `test_regressao_auditoria.py`, `usuario_bp.py`, `PagamentoDAO`, `test_seguranca.py`, `config.py`, `.listar_paginado`, `test_admin_rejeita_valor_financeiro_invalido`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Why does `Aluno` connect `Aluno` to `erro_validacao_senha`, `adm_bp.py`, `autorizacao.py`, `pagina_cadastro`, `test_mudanca_plano.py`, `convites.py`, `criar_aluno`, `test_regressao_auditoria.py`, `usuario_bp.py`, `PagamentoDAO`, `_convidar_cadastro_existente`, `logar_como_admin`, `Pagamento`, `test_seguranca.py`, `config.py`, `test_admin_rejeita_valor_financeiro_invalido`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Are the 136 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 136 INFERRED edges - model-reasoned connections that need verification._
- **Are the 139 inferred relationships involving `criar_pagamento()` (e.g. with `PagamentoDAO` and `Pagamento`) actually correct?**
  _`criar_pagamento()` has 139 INFERRED edges - model-reasoned connections that need verification._
- **Are the 132 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 132 INFERRED edges - model-reasoned connections that need verification._
- **Are the 111 inferred relationships involving `logar_como_aluno()` (e.g. with `test_aluno_nao_alcanca_cobranca_de_outro_aluno()` and `test_checkout_recusa_cobranca_indisponivel()`) actually correct?**
  _`logar_como_aluno()` has 111 INFERRED edges - model-reasoned connections that need verification._