# Graph Report - SistemaEXTREMETEAM  (2026-09-21)

## Corpus Check
- 132 files · ~194,006 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1758 nodes · 4509 edges · 100 communities (94 shown, 6 thin omitted)
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 926 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5ffc6e51`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- impressao_credencial
- Aluno Profile Page
- Aluno
- criar_aluno
- test_limites_pagamento.py
- test_mudanca_plano.py
- PagamentoDAO
- Reavaliação de segurança e desempenho — 12/09/2026
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
- test_checkout_rotas.py
- checkout_bp.py
- pix.js
- config.py
- env.py
- pagamento.js
- c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py
- varredura.mjs
- 896e70afc9c5_adiciona_foto_e_graduacao_do_aluno_.py
- test_auditoria_seguranca.py
- .buscar_por_id
- adm_bp.py
- MatriculaDAO
- test_regressao_auditoria.py
- convites.py
- Academia
- pagamento_polling.test.cjs
- mercado_pago_conta.py
- criar_pagamento
- test_pix_rotas.py
- PagamentoEvento
- d9e2f6a14c80_contatos_academia_perfis_professores.py
- conftest.py
- botao_ocupado.test.cjs
- test_seguranca.py
- checkout_abertura.test.cjs
- filtros_financeiro.js
- gunicorn.conf.py
- admin_requerido
- fila_email.py
- test_migracao_cadastro_administrativo.py
- salvar_foto_perfil
- test_keep_alive.py
- pagina_login
- MercadoPagoIndisponivel
- test_arranque_seguranca.py
- .contratar_plano
- ativar_acesso
- servidor.py
- turma_bp.py
- pagina_cadastro
- _png_bomba
- credenciais.py
- shot.mjs
- limites_pagamento.py
- usuario_bp.py
- Pagina
- _tem_limite
- e4b7c2a91d35_cadastro_administrativo_e_convite_de_acesso.py
- a1f0c3e75b92_schema_inicial.py
- Contrato do redesign — SistemaEXTREMETEAM
- _chave_da_conta
- Relatório de segurança — Sistema Extreme Team (17/09/2026)
- Atualização de 19/09/2026 — correções aplicadas e nova varredura
- Severidade BAIXA
- test_perfil_e_foto.py
- Relatório de segurança — Sistema Extreme Team
- Severidade MÉDIA
- Severidade ALTA
- URLPublicaInvalida
- _FakePaymentResource
- _convidar_cadastro_existente

## God Nodes (most connected - your core abstractions)
1. `PagamentoDAO` - 196 edges
2. `criar_pagamento()` - 141 edges
3. `criar_aluno()` - 131 edges
4. `logar_como_aluno()` - 112 edges
5. `logar_como_admin()` - 111 edges
6. `AlunoDAO` - 91 edges
7. `Aluno` - 59 edges
8. `MercadoPagoIndisponivel` - 41 edges
9. `Professor` - 37 edges
10. `ProfessorDAO` - 35 edges

## Surprising Connections (you probably didn't know these)
- `Histórico de Mensalidades Section` --shares_data_with--> `Pagamento`  [INFERRED]
  templates/pgUsuario.html → modelos/pagamento.py
- `Presença Form` --shares_data_with--> `Presenca`  [INFERRED]
  templates/turma.html → modelos/presenca.py
- `Aluno Detail/Admin Page` --shares_data_with--> `Matricula`  [INFERRED]
  templates/dt_aluno.html → modelos/matricula.py
- `Aluno Profile Page` --shares_data_with--> `Matricula`  [INFERRED]
  templates/pgUsuario.html → modelos/matricula.py
- `Aluno Mensalidade Launch Form` --shares_data_with--> `Pagamento`  [INFERRED]
  templates/dt_aluno.html → modelos/pagamento.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Shared Confirmation Modal Pattern** — templates_components_confirm_modal_dialog, templates_pgadm_page, templates_pgprofessor_page, templates_pgusuario_page, templates_turmas_page [EXTRACTED 1.00]
- **Mensalidade (Billing) Management Flow** — templates_dt_aluno_pagamento_form, templates_pgusuario_mensalidades_section, modelos_pagamento_pagamento, modelos_plano_plano [INFERRED 0.85]
- **Turma and Attendance Management Flow** — templates_turmas_turma_form, templates_turma_presenca_form, templates_pgprofessor_page, modelos_turma_turma [INFERRED 0.85]

## Communities (100 total, 6 thin omitted)

### Community 0 - "impressao_credencial"
Cohesion: 0.18
Nodes (14): impressao_credencial(), Resumo curto e não reversível do hash da senha, guardado na sessão. Nunca é a…, _foto(), pasta_fotos(), fixture, parametrize, test_admin_salva_perfil_sem_alterar_acesso(), test_apenas_admin_edita_perfil() (+6 more)

### Community 1 - "Aluno Profile Page"
Cohesion: 0.05
Nodes (34): abrirmodal(), fechar(), icone_senha, input_senha, modal, mostrarSenha(), campoDuracao, campoPreco (+26 more)

### Community 2 - "Aluno"
Cohesion: 0.13
Nodes (8): Aluno, Se existe uma conta de acesso, e não se o aluno está em dia ou matriculado.…, Convite de acesso já enviado e ainda não usado (a validade é checada na rota)., Chave do estado da CONTA - nunca da situação financeira nem da matrícula., _dados_cadastro(), test_cadastro_exige_aceite_do_termo(), test_cadastro_registra_versao_e_horario_do_aceite(), aluno()

### Community 3 - "criar_aluno"
Cohesion: 0.13
Nodes (35): Pagamento, Status a exibir, com o vencimento já aplicado. Uma cobrança `pendente` cujo…, criar_aluno(), test_escolher_plano_cria_mensalidade_e_redireciona_para_pix(), test_plano_invalido_nao_cria_mensalidade(), test_reenvio_da_contratacao_reutiliza_mensalidade(), test_valor_enviado_pelo_navegador_e_ignorado(), _pagar() (+27 more)

### Community 4 - "test_limites_pagamento.py"
Cohesion: 0.15
Nodes (16): consultar_mp(), fixture, parametrize, Limites de pagamento por conta, com o provedor inteiramente simulado., _sessao_admin(), _sessao_aluno(), test_admin_limite_por_usuario_persiste_entre_sessoes(), test_alunos_no_mesmo_ip_tem_limites_separados() (+8 more)

### Community 5 - "test_mudanca_plano.py"
Cohesion: 0.20
Nodes (22): Persistência dos pedidos de troca de plano agendados para a próxima renovação., SolicitacaoPlanoDAO, _agendar(), _pagar(), Mudança para um plano mais barato agendada para a próxima renovação. Regra…, O admin pode estornar/cancelar a mensalidade que sustentava a vigência depois…, test_admin_cancela_a_solicitacao(), test_aluno_cancela_a_solicitacao_antes_da_efetivacao() (+14 more)

### Community 6 - "PagamentoDAO"
Cohesion: 0.09
Nodes (26): PagamentoDAO, Carrega aluno e plano junto das mensalidades. O template do painel lê…, Lista completa (sem paginar). Mantida para relatórios e testes., Uma página de mensalidades, recortada pelo banco (LIMIT/OFFSET). O painel…, Totais do painel financeiro - sempre calculados no backend a partir do banco,…, True se já existe um Pix ou um checkout válido emitido para esta cobrança.…, True se a cobrança Pix já gerada para este pagamento ainda pode ser…, True se a preferência do Checkout Pro já criada pode ser reaproveitada. Só… (+18 more)

### Community 7 - "Reavaliação de segurança e desempenho — 12/09/2026"
Cohesion: 0.25
Nodes (5): Achados, Atualização de 19/09/2026, Medições locais, Reavaliação de segurança e desempenho — 12/09/2026, Validação e limites

### Community 9 - "test_mercado_pago_servico.py"
Cohesion: 0.11
Nodes (28): Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, validar_assinatura_webhook(), Hipótese: uma notificação capturada ontem pode ser reenviada hoje., `ts=nan` fazia a comparação da janela dar False e passava pela checagem de…, test_webhook_recusa_assinatura_antiga(), test_webhook_recusa_ts_nao_numerico_finito(), base_url(), _criar_preferencia() (+20 more)

### Community 10 - "test_mercado_pago_oauth.py"
Cohesion: 0.05
Nodes (68): MercadoPagoConexao, Conta do Mercado Pago que a academia autorizou por OAuth. Uma linha só (a…, _agora(), _ajustar(), api_mp(), _conectar(), _dados_conexao(), oauth_env() (+60 more)

### Community 11 - "Professor"
Cohesion: 0.13
Nodes (18): cadastrar_professor(), gerenciar_turmas(), remover_professor(), ProfessorDAO, Professor, Cadastrar Professor Form, logar_como_professor(), fixture (+10 more)

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
Cohesion: 0.07
Nodes (73): AlunoDAO, Uma página de alunos já cadastrados, recortada e filtrada pelo banco. O painel…, logar_como_admin(), capturar_emails(), _matricular(), fixture, parametrize, Cadastro de aluno pela administração, ativação de acesso e confirmação de… (+65 more)

### Community 19 - "test_checkout_rotas.py"
Cohesion: 0.19
Nodes (25): _assinar(), _pagamento_mp(), _preparar_retorno(), parametrize, Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala…, Pix aberto e checkout concluído ao mesmo tempo: a consulta pelo…, _resposta_preferencia(), test_json_nao_abre_destino_fora_do_checkout() (+17 more)

### Community 20 - "checkout_bp.py"
Cohesion: 0.11
Nodes (29): abrir_checkout(), _acesso_permitido(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), limitar_consulta_pagamento, limitar_criacao_pagamento, route (+21 more)

### Community 21 - "pix.js"
Cohesion: 0.33
Nodes (14): abrirPix(), alvoDoRotulo(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), liberarBotao(), limparConteudoAnterior() (+6 more)

### Community 22 - "config.py"
Cohesion: 0.18
Nodes (9): _paginar(), Aplica LIMIT/OFFSET e conta o total numa consulta separada e barata. A contagem…, Decimal, Matricula, _para_decimal(), postgres_pix(), fixture, Regressão com trava de linha real, opcional na suíte que usa SQLite. Execute… (+1 more)

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

### Community 34 - ".buscar_por_id"
Cohesion: 0.20
Nodes (12): Hipótese: se a resposta do MP trouxer um destino estranho, ele é salvo e…, test_url_hostil_do_mercado_pago_nao_e_persistida(), test_configuracao_ausente_falha_de_forma_explicita(), test_mercado_pago_indisponivel_nao_persiste_nada(), test_admin_aprova_comprovante_manual(), test_admin_rejeita_comprovante_manual_volta_para_pendente(), test_aluno_nao_acessa_arquivo_de_comprovante_de_outro(), test_aluno_nao_envia_comprovante_de_outro_aluno() (+4 more)

### Community 35 - "adm_bp.py"
Cohesion: 0.06
Nodes (59): _aluno_do_cpf_ou_painel(), aprovar_aluno(), aprovar_comprovante_manual(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_aluno(), cadastrar_pagamento(), cadastrar_plano() (+51 more)

### Community 36 - "MatriculaDAO"
Cohesion: 0.24
Nodes (10): MatriculaDAO, Presenca, Valor que representa a credencial administrativa em vigor, ou None se não há…, referencia_credencial_admin(), parametrize, test_aluno_confirma_sua_frequencia(), test_consulta_com_data_invalida_exibe_hoje_e_aviso(), test_data_invalida_nao_contorna_permissoes() (+2 more)

### Community 37 - "test_regressao_auditoria.py"
Cohesion: 0.04
Nodes (40): _contar_selects_em_alunos(), _credencial(), Regressões da auditoria de segurança, desempenho e confiabilidade. Cada caso…, Head-of-line blocking: a primeira linha falhando não pode impedir as seguintes.…, Uma linha `desistiu` nunca foi entregue: recusar o reenvio fazia a tela dizer…, A revivência vale só para o abandonado: clique duplo continua virando um envio., Trocar senha, e-mail ou foto são ações de quem JÁ está autenticado. Devolver o…, Persistência não é retomada: alguém precisa acordar a fila quando o adiamento… (+32 more)

### Community 38 - "convites.py"
Cohesion: 0.11
Nodes (19): aluno_do_token(), ConviteIndisponivel, descartar(), enviar(), gerar_token(), _hash(), RuntimeError, Convite de acesso: como um cadastro criado pela administração vira uma conta.… (+11 more)

### Community 41 - "Academia"
Cohesion: 0.13
Nodes (19): configuracoes(), _pagina(), route, editar_professor(), Academia, link_email(), Normalização de contatos profissionais antes de montar links públicos., validar_email() (+11 more)

### Community 42 - "pagamento_polling.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 43 - "mercado_pago_conta.py"
Cohesion: 0.10
Nodes (35): access_token_vigente(), _agora(), ambiente_da_conexao(), _cifrar(), _client_id(), _client_secret(), ConexaoIlegivel, _decifrar() (+27 more)

### Community 44 - "criar_pagamento"
Cohesion: 0.11
Nodes (40): criar_pagamento(), logar_como_aluno(), Hipótese: forjar ?status=approved na volta do MP quita a mensalidade., test_retorno_ignora_status_aprovado_da_query_string(), _mockar_preferencia(), Um boleto pendente do Checkout Pro grava provider_payment_id, mas não é Pix:…, test_abertura_json_navega_sem_redirecionar_post_externo(), test_admin_tambem_pode_abrir_checkout() (+32 more)

### Community 45 - "test_pix_rotas.py"
Cohesion: 0.23
Nodes (18): _assinar(), _resposta_consulta(), _resposta_criacao(), test_admin_tambem_pode_gerar_pix(), test_aluno_gera_pix_da_propria_mensalidade(), test_aluno_nao_acessa_mensalidade_de_outro_aluno(), test_impede_cobranca_duplicada_em_chamadas_consecutivas(), test_mensalidade_ja_paga_retorna_409() (+10 more)

### Community 46 - "PagamentoEvento"
Cohesion: 0.11
Nodes (12): Primeiro dia não coberto por outra mensalidade do mesmo aluno., Define o período coberto por uma mensalidade que ainda não tem um (lançamento…, Abre o período de acesso no momento em que o pagamento é confirmado. Se a…, Reescreve os campos denormalizados do aluno a partir das mensalidades.…, forma_pagamento vem do que o Mercado Pago confirmou na consulta à API ('pix',…, Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.…, PagamentoEvento, Histórico de auditoria de uma mensalidade (nunca grava credenciais ou dados… (+4 more)

### Community 47 - "d9e2f6a14c80_contatos_academia_perfis_professores.py"
Cohesion: 0.83
Nodes (3): _campos_professor(), downgrade(), upgrade()

### Community 49 - "conftest.py"
Cohesion: 0.27
Nodes (11): app(), client(), contexto_app(), limpar_banco(), logar_como_professor(), plano(), fixture, Substitui o provedor de e-mail em todos os módulos que o chamam. A suíte nunca… (+3 more)

### Community 50 - "botao_ocupado.test.cjs"
Cohesion: 0.18
Nodes (7): assert, criarElemento(), fs, montar(), path, test, vm

### Community 51 - "test_seguranca.py"
Cohesion: 0.09
Nodes (22): erro_validacao_senha(), Retorna uma mensagem quando a senha é curta, comum ou igual ao identificador., url_publica(), _cadastro_publico(), _imagem_jpeg(), _mensagem_da_resposta(), O ramo "par existe" não pode pagar a ida ao provedor dentro da requisição., Cadastro novo, CPF existente e e-mail existente respondem com a MESMA tela. (+14 more)

### Community 52 - "checkout_abertura.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 55 - "gunicorn.conf.py"
Cohesion: 0.25
Nodes (9): post_worker_init(), Hooks carregados pelo Gunicorn; nunca executados por flask db upgrade., worker_exit(), iniciar(), _laco(), parar(), Aciona a fila periodicamente durante a vida de um worker Gunicorn. Importar…, Inicia uma vez por processo, depois de carregar a aplicação e migrar o banco. (+1 more)

### Community 56 - "admin_requerido"
Cohesion: 0.25
Nodes (15): callback(), conectar(), desconectar(), route, _voltar(), _autorizacao_valida(), callback(), conectar() (+7 more)

### Community 57 - "fila_email.py"
Cohesion: 0.06
Nodes (40): EmailPendente, espera_da_proxima_tentativa(), Fila de e-mails no banco. Aviso e cobrança coletivos saíam um a um dentro da…, contar_falhados(), contar_pendentes(), disparar(), enfileirar(), enfileirar_transacional() (+32 more)

### Community 58 - "test_migracao_cadastro_administrativo.py"
Cohesion: 0.40
Nodes (3): banco_antigo(), fixture, Verifica a migração em um banco isolado com o schema anterior e dados.

### Community 59 - "salvar_foto_perfil"
Cohesion: 0.11
Nodes (26): ArquivoInvalido, caminho_arquivo(), _conferir_dimensoes(), _detectar_tipo_imagem_real(), ImagemGrandeDemais, _pasta(), Exception, _raiz_uploads() (+18 more)

### Community 60 - "test_keep_alive.py"
Cohesion: 0.16
Nodes (7): ambiente_limpo(), fixture, parametrize, Garante que o keep-alive fica desligado por padrão e só pinga a própria origem., test_intervalo_fica_dentro_da_faixa(), test_nao_liga_com_valor_negativo(), test_ping_so_considera_200_como_sucesso()

### Community 61 - "pagina_login"
Cohesion: 0.20
Nodes (8): pagina_login(), iniciar_sessao(), Grava na sessão atual a credencial em vigor (login ou troca de senha bem-…, Dá um identificador à sessão recém-aberta, para o logout poder revogá-la.…, registrar_credencial(), O `login` de um aluno pode ser o e-mail de outro; quem entra é decidido pela…, test_login_com_identificador_repetido_em_outra_coluna_nao_bloqueia_a_vitima(), test_login_nao_aceita_nome_do_aluno()

### Community 62 - "MercadoPagoIndisponivel"
Cohesion: 0.10
Nodes (35): _base_url_opcional(), base_url_publica(), buscar_pagamentos_por_referencia(), cancelar_pagamento(), criar_pagamento_pix(), criar_preferencia_checkout(), _erro_menciona(), _erro_menciona_expiracao() (+27 more)

### Community 63 - "test_arranque_seguranca.py"
Cohesion: 0.22
Nodes (14): _env_arranque(), Validações feitas por servidor.py no arranque (COOKIE_SECURE, TRUSTED_HOSTS,…, `python -m servicos.credenciais`: o hash sai entre aspas simples. O hash do…, Desenvolvimento local sem HTTPS (sem Caddy) não pode ficar travado., _rodar(), test_arranque_falha_com_cookie_secure_false_e_app_base_url_https(), test_arranque_falha_com_cookie_secure_invalido(), test_arranque_falha_sem_trusted_hosts() (+6 more)

### Community 64 - ".contratar_plano"
Cohesion: 0.09
Nodes (13): O que aconteceu numa tentativa de contratar/renovar/trocar de plano., Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda. O…, Aplica um pedido agendado cujo período de origem já terminou sem renovação.…, Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, Com uma troca já agendada, só dois planos fazem sentido num pedido de…, A cobrança do período seguinte tem de nascer no plano que o aluno agendou.…, `pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -… (+5 more)

### Community 66 - "ativar_acesso"
Cohesion: 0.22
Nodes (8): ativar_acesso(), Transforma um cadastro feito no balcão na conta do próprio aluno. Quem chega…, mascarar_email(), Mostra o bastante do e-mail para o dono se reconhecer, sem revelá-lo a…, _carregar_senhas_comuns(), erro_confirmacao_senha(), Retorna uma mensagem quando a confirmação não repete exatamente a senha. A…, Lê a lista de senhas comuns (uma por linha; `#` abre comentário) para um…

### Community 67 - "servidor.py"
Cohesion: 0.05
Nodes (56): after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, Flask App Service (compose), Postgres DB Service (compose), postgres_data Volume, context_processor, errorhandler (+48 more)

### Community 68 - "turma_bp.py"
Cohesion: 0.14
Nodes (25): _acesso_permitido(), desmatricular_aluno(), detalhe_turma(), foto_professor(), matricular_aluno(), painel_professor(), route, registrar_presenca() (+17 more)

### Community 69 - "pagina_cadastro"
Cohesion: 0.21
Nodes (16): _em_segundo_plano(), _enviar_em_segundo_plano(), pagina_cadastro(), Roda `tarefa` fora da requisição, para o tempo de resposta não revelar nada. Em…, E-mail COM token (recuperação, confirmação): não pode ir para a `fila_email`. A…, recuperar_senha(), _parece_busca_por_cpf(), O termo é um CPF, ou um pedaço dele, e não um nome que por acaso tem número? (+8 more)

### Community 70 - "_png_bomba"
Cohesion: 0.29
Nodes (7): _png_bomba(), Bomba de descompressão: arquivo minúsculo, imagem gigante. O PNG aqui tem 285…, PNG válido e altamente compressível: linhas zeradas, como uma bomba real., O teto de pixels vale para a FOTO, que é decodificada, não para o comprovante.…, test_comprovante_a4_escaneado_continua_sendo_aceito(), test_foto_de_perfil_mantem_o_teto_de_pixels(), test_png_com_pixels_demais_e_recusado_pelo_cabecalho()

### Community 71 - "credenciais.py"
Cohesion: 0.20
Nodes (11): admin_configurado(), comparar_em_tempo_constante(), credencial_admin_confere(), gerar_hash_admin(), _main(), Credencial administrativa baseada exclusivamente em hash de senha. O…, Compara duas senhas em tempo constante, sem restrição de alfabeto. Codificar…, True quando existe usuário e hash da senha do administrador. (+3 more)

### Community 72 - "shot.mjs"
Cohesion: 0.29
Nodes (5): { chromium }, contextos, CREDS, jobs, require

### Community 73 - "limites_pagamento.py"
Cohesion: 0.50
Nodes (3): chave_pagamento(), Orçamentos compartilhados das chamadas interativas ao provedor de pagamento., A mesma conta mantém seu limite entre sessões, rotas e mensalidades. Alunos que…

### Community 74 - "usuario_bp.py"
Cohesion: 0.12
Nodes (40): _acesso_permitido_pagamento(), alterar_senha_perfil(), _aluno_da_sessao(), _aluno_por_token(), atualizar_dados_perfil(), cancelar_mudanca_plano(), comprovante_mensalidade(), confirmar_email() (+32 more)

### Community 76 - "Pagina"
Cohesion: 0.14
Nodes (5): Pagina, Uma fatia de resultados já recortada pelo banco, com o que a navegação precisa., Uma página existe mesmo quando está vazia. Sem isto, `__len__` fazia `{% if…, `__len__` fazia `{% if pagina %}` ser falso numa página sem itens, escondendo…, test_pagina_vazia_ainda_mostra_a_navegacao()

### Community 77 - "_tem_limite"
Cohesion: 0.20
Nodes (10): parametrize, Qualquer dígito no termo virava `CPF LIKE '%3%'` e devolvia a academia inteira., Rotas que custam hash de senha, processamento de imagem ou sondagem de token., Limites declarados por decorador NAQUELA rota. `resolve_limits` não serve aqui:…, Guarda do teste acima: uma rota sem limite precisa ser reprovada por ele., _tem_limite(), test_busca_so_trata_como_cpf_o_que_parece_cpf(), test_o_detector_de_limite_realmente_discrimina() (+2 more)

### Community 81 - "Contrato do redesign — SistemaEXTREMETEAM"
Cohesion: 0.09
Nodes (20): 0. Antes de escrever código, 1. Identidade visual (design tokens), 2. Logo oficial (usar SOMENTE a logo original), 3. Telas a implementar, 4. Regras e dados, 5. Forma de trabalhar, Painel administrativo (desktop, sidebar preta com o emblema do dragão), Prompt para o Claude Code — Redesign do SistemaEXTREMETEAM (+12 more)

### Community 82 - "_chave_da_conta"
Cohesion: 0.40
Nodes (5): _chave_da_conta(), Chave de limite por CONTA, caindo no IP só para quem não está autenticado. A…, Alunos atrás do mesmo IP (o Wi-Fi da academia) não dividem a cota., test_limite_de_upload_e_por_conta_e_nao_por_ip(), test_visitante_sem_sessao_ainda_e_limitado_por_ip()

### Community 83 - "Relatório de segurança — Sistema Extreme Team (17/09/2026)"
Cohesion: 0.20
Nodes (10): A1 — `/recuperar_senha` revela por tempo de resposta se o CPF+e-mail existe (Média, CORRIGIDA em 19/09/2026), A2 — `/perfil/dados` sem limite de tentativas na senha atual (Baixa–Média, CORRIGIDA em 19/09/2026), A3 — `/perfil/dados` não valida tamanho de `nome`/`login`/`descricao` (Baixa, CORRIGIDA em 19/09/2026), A4 — Enumeração de usuário/e-mail no cadastro público (Baixa / informativa, CORRIGIDA em 19/09/2026 para CPF e e-mail), Housekeeping: `pip` desatualizado no ambiente virtual local (CORRIGIDO em 19/09/2026: pip 26.2.1), Ordem de correção sugerida (executada em 19/09/2026, ver a seção de atualização), Relatório de segurança — Sistema Extreme Team (17/09/2026), Situação dos 15 achados do relatório de 05/09 (revalidados hoje, código lido diretamente) (+2 more)

### Community 90 - "Atualização de 19/09/2026 — correções aplicadas e nova varredura"
Cohesion: 0.25
Nodes (8): Atualização de 19/09/2026 — correções aplicadas e nova varredura, Correções dos achados de 17/09, Nova varredura independente (19/09) — S1 e S2, Não alterado (decisão ou baixo valor), Reauditoria de 12/09 (itens de desempenho), Reforços em achados de 05/09 (F1–F15 seguem corrigidos), Revisão do fluxo OAuth do Mercado Pago (código novo da branch), Validação e implantação

### Community 94 - "Severidade BAIXA"
Cohesion: 0.29
Nodes (7): F10 — Redirecionamento aberto via `Referer`, F11 — `/logout` aceita GET, F12 — Enumeração de usuários por tempo de resposta, F13 — Senha mínima de 6 caracteres, sem outros critérios, F14 — Webhook sem verificação de recência do timestamp, F15 — Curinga de `LIKE` no filtro do financeiro, Severidade BAIXA

### Community 96 - "test_perfil_e_foto.py"
Cohesion: 0.16
Nodes (11): cadastrar_turma(), remover_turma(), TurmaDAO, Turma, Cadastrar Turma Form, test_area_do_aluno_renderiza_telas_independentes_do_menu(), test_escolher_plano_com_turma_cria_matricula(), test_plano_atual_continua_disponivel_para_gerar_cobranca() (+3 more)

### Community 97 - "Relatório de segurança — Sistema Extreme Team"
Cohesion: 0.33
Nodes (6): A verificar em execução, Atualização após as correções, Ordem de correção sugerida, Relatório de segurança — Sistema Extreme Team, Sumário executivo, Verificado e correto

### Community 98 - "Severidade MÉDIA"
Cohesion: 0.33
Nodes (6): F5 — Sem limite de tamanho de requisição: negação de serviço por memória, F6 — Comprovante em PDF servido inline, F7 — Nenhum cabeçalho de segurança HTTP, F8 — Autenticação aceita campo não único e editável pelo usuário, F9 — Confiança em proxy não configurada, Severidade MÉDIA

### Community 99 - "Severidade ALTA"
Cohesion: 0.40
Nodes (5): F1 — Aluno consegue desviar a ficha administrativa de outro aluno, F2 — Ausência de proteção CSRF em 46 de 49 formulários, F3 — Sem limite de tentativas: força bruta na senha do administrador, F4 — Link de recuperação de senha montado a partir do cabeçalho `Host`, Severidade ALTA

### Community 103 - "URLPublicaInvalida"
Cohesion: 0.22
Nodes (13): iniciar(), _intervalo(), _laco(), _ligado(), parar(), _pingar(), Mantém a aplicação acordada em hospedagens que hibernam por inatividade. Uma…, Encerra o laço. Usado pelos testes; em produção a thread é daemon. (+5 more)

### Community 112 - "_convidar_cadastro_existente"
Cohesion: 0.50
Nodes (4): _convidar_cadastro_existente(), _convidar_cadastro_existente_por_id(), Cadastro administrativo que alguém tentou recriar pelo formulário público. Em…, Versão para thread de fundo: a sessão da requisição não vale fora dela.

## Knowledge Gaps
- **112 isolated node(s):** `modal`, `input_senha`, `icone_senha`, `formularioPlano`, `campoPreco` (+107 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PagamentoDAO` connect `PagamentoDAO` to `Aluno`, `criar_aluno`, `test_mudanca_plano.py`, `pix_bp.py`, `logar_como_admin`, `test_checkout_rotas.py`, `checkout_bp.py`, `config.py`, `test_auditoria_seguranca.py`, `.buscar_por_id`, `adm_bp.py`, `test_regressao_auditoria.py`, `criar_pagamento`, `test_pix_rotas.py`, `PagamentoEvento`, `conftest.py`, `test_seguranca.py`, `.contratar_plano`, `usuario_bp.py`, `test_perfil_e_foto.py`?**
  _High betweenness centrality (0.157) - this node is a cross-community bridge._
- **Why does `AlunoDAO` connect `logar_como_admin` to `test_perfil_e_foto.py`, `Aluno`, `adm_bp.py`, `turma_bp.py`, `pagina_cadastro`, `PagamentoDAO`, `criar_aluno`, `test_regressao_auditoria.py`, `usuario_bp.py`, `conftest.py`, `test_seguranca.py`, `config.py`, `pagina_login`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Why does `logar_como_admin()` connect `logar_como_admin` to `impressao_credencial`, `.buscar_por_id`, `criar_aluno`, `MatriculaDAO`, `test_limites_pagamento.py`, `test_mudanca_plano.py`, `test_regressao_auditoria.py`, `PagamentoDAO`, `Academia`, `test_mercado_pago_oauth.py`, `Professor`, `criar_pagamento`, `test_pix_rotas.py`, `conftest.py`, `adm_bp.py`, `test_seguranca.py`, `servidor.py`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Are the 131 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 131 INFERRED edges - model-reasoned connections that need verification._
- **Are the 139 inferred relationships involving `criar_pagamento()` (e.g. with `PagamentoDAO` and `Pagamento`) actually correct?**
  _`criar_pagamento()` has 139 INFERRED edges - model-reasoned connections that need verification._
- **Are the 129 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 129 INFERRED edges - model-reasoned connections that need verification._
- **Are the 110 inferred relationships involving `logar_como_aluno()` (e.g. with `test_aluno_nao_alcanca_cobranca_de_outro_aluno()` and `test_checkout_recusa_cobranca_indisponivel()`) actually correct?**
  _`logar_como_aluno()` has 110 INFERRED edges - model-reasoned connections that need verification._