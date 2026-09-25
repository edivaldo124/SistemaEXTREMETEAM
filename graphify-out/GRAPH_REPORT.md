# Graph Report - SistemaEXTREMETEAM  (2026-09-25)

## Corpus Check
- 132 files · ~189,528 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1738 nodes · 4540 edges · 105 communities (96 shown, 9 thin omitted)
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 946 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `062ac873`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_fila_email_concorrencia_postgres.py
- Aluno Profile Page
- .efetivar_mudancas_por_prazo
- .listar_por_aluno
- test_limites_pagamento.py
- test_mudanca_plano.py
- PagamentoDAO
- test_regressao_auditoria.py
- SistemaEXTREMETEAM Project
- MercadoPagoIndisponivel
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
- turma_bp.py
- adm_bp.py
- Presenca
- .buscar_por_id
- convites.py
- Academia
- pagamento_polling.test.cjs
- mercado_pago_conta.py
- criar_pagamento
- test_pix_rotas.py
- PagamentoEvento
- d9e2f6a14c80_contatos_academia_perfis_professores.py
- EmailPendente
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
- disparar
- URLPublicaInvalida
- servidor.py
- aluno_autorizado
- pagina_cadastro
- .bloquear_pendente_do_aluno
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
- Skills Disponíveis
- academia_bp.py
- test_sessao_revogada.py
- Relatório de segurança — Sistema Extreme Team
- admin_requerido
- MatriculaDAO
- test_email_gmail.py
- .listar_paginado
- SolicitacaoMudancaPlano
- erro_validacao_senha
- test_painel_financeiro_nao_varre_mensalidades_fora_do_filtro
- Flask App Service (compose)
- criar_aluno
- _FakePaymentResource

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

## Communities (105 total, 9 thin omitted)

### Community 0 - "test_fila_email_concorrencia_postgres.py"
Cohesion: 0.18
Nodes (10): _enfileirar_em_transacao_propria(), postgres_fila(), fixture, Idempotência da fila de e-mail sob concorrência real, em PostgreSQL…, A recusa de uma chave repetida não pode desfazer o lote inteiro. Um…, A trava do lote precisa valer até o fim do lote. Comitar linha a linha…, Enfileira e comita numa sessão própria, como faria outra requisição., test_chave_duplicada_nao_descarta_os_outros_destinatarios_do_lote() (+2 more)

### Community 1 - "Aluno Profile Page"
Cohesion: 0.05
Nodes (38): abrirmodal(), fechar(), icone_senha, input_senha, modal, mostrarSenha(), campoDuracao, campoPreco (+30 more)

### Community 2 - ".efetivar_mudancas_por_prazo"
Cohesion: 0.22
Nodes (4): Aplica um pedido agendado cujo período de origem já terminou sem renovação.…, Primeiro dia não coberto por outra mensalidade do mesmo aluno., Define o período coberto por uma mensalidade que ainda não tem um (lançamento…, test_mudanca_vale_por_decurso_de_prazo_quando_o_plano_vence()

### Community 3 - ".listar_por_aluno"
Cohesion: 0.11
Nodes (33): Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, `pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -…, test_escolher_plano_cria_mensalidade_e_redireciona_para_pix(), test_plano_invalido_nao_cria_mensalidade(), test_reenvio_da_contratacao_reutiliza_mensalidade(), test_valor_enviado_pelo_navegador_e_ignorado(), _pagar(), plano_barato() (+25 more)

### Community 4 - "test_limites_pagamento.py"
Cohesion: 0.15
Nodes (16): consultar_mp(), fixture, parametrize, Limites de pagamento por conta, com o provedor inteiramente simulado., _sessao_admin(), _sessao_aluno(), test_admin_limite_por_usuario_persiste_entre_sessoes(), test_alunos_no_mesmo_ip_tem_limites_separados() (+8 more)

### Community 5 - "test_mudanca_plano.py"
Cohesion: 0.16
Nodes (26): detalhes_usuario(), Persistência dos pedidos de troca de plano agendados para a próxima renovação., SolicitacaoPlanoDAO, _agendar(), _pagar(), plano_barato(), fixture, Mudança para um plano mais barato agendada para a próxima renovação. Regra… (+18 more)

### Community 6 - "PagamentoDAO"
Cohesion: 0.09
Nodes (23): PagamentoDAO, Status como o painel deve LER, com o vencimento aplicado na própria consulta. A…, Carrega aluno e plano junto das mensalidades. O template do painel lê…, Lista completa (sem paginar). Mantida para relatórios e testes., Uma página de mensalidades, recortada pelo banco (LIMIT/OFFSET). O painel…, True se já existe um Pix ou um checkout válido emitido para esta cobrança.…, Com uma troca já agendada, só dois planos fazem sentido num pedido de…, A cobrança do período seguinte tem de nascer no plano que o aluno agendou.… (+15 more)

### Community 7 - "test_regressao_auditoria.py"
Cohesion: 0.05
Nodes (32): _contar_selects_em_alunos(), _credencial(), Regressões da auditoria de segurança, desempenho e confiabilidade. Cada caso…, Head-of-line blocking: a primeira linha falhando não pode impedir as seguintes.…, Uma linha `desistiu` nunca foi entregue: recusar o reenvio fazia a tela dizer…, A revivência vale só para o abandonado: clique duplo continua virando um envio., Persistência não é retomada: alguém precisa acordar a fila quando o adiamento…, O limite protege a memória, não pune a resolução: JPEG usa `draft()`. (+24 more)

### Community 9 - "MercadoPagoIndisponivel"
Cohesion: 0.08
Nodes (37): MercadoPagoIndisponivel, Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, Falha de transporte (timeout/DNS/conexao) ao falar com a API do Mercado Pago., validar_assinatura_webhook(), Hipótese: uma notificação capturada ontem pode ser reenviada hoje., `ts=nan` fazia a comparação da janela dar False e passava pela checagem de…, test_webhook_recusa_assinatura_antiga(), test_webhook_recusa_ts_nao_numerico_finito() (+29 more)

### Community 10 - "test_mercado_pago_oauth.py"
Cohesion: 0.05
Nodes (70): MercadoPagoConexao, Conta do Mercado Pago que a academia autorizou por OAuth. Uma linha só (a…, Esquece a conta conectada. Devolve True se havia uma., remover_conexao(), _agora(), _ajustar(), api_mp(), _conectar() (+62 more)

### Community 11 - "Professor"
Cohesion: 0.09
Nodes (31): remover_professor(), ProfessorDAO, Professor, aluno_requerido(), impressao_credencial(), Autorização das rotas protegidas. A sessão diz quem *afirmou* ser quem; quem…, Rotas da área do aluno: injeta o aluno já revalidado como primeiro argumento., Resumo curto e não reversível do hash da senha, guardado na sessão. Nunca é a… (+23 more)

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
Nodes (30): _acesso_permitido(), criar_pix_mensalidade(), _forma_pagamento_confirmada(), _pagamento_mp_mais_relevante(), _pagamento_ou_none(), _pix_expirado(), _processar_status_mp(), limitar_consulta_pagamento (+22 more)

### Community 18 - "logar_como_admin"
Cohesion: 0.07
Nodes (67): _convidar_cadastro_existente(), Cadastro administrativo que alguém tentou recriar pelo formulário público. Em…, AlunoDAO, Matrícula feita no balcão: sem login, sem senha e sem convite de acesso. Nasce…, Aluno, Se existe uma conta de acesso, e não se o aluno está em dia ou matriculado.…, Convite de acesso já enviado e ainda não usado (a validade é checada na rota)., Chave do estado da CONTA - nunca da situação financeira nem da matrícula. (+59 more)

### Community 19 - "test_checkout_rotas.py"
Cohesion: 0.21
Nodes (26): _assinar(), _pagamento_mp(), _preparar_retorno(), parametrize, Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala…, Pix aberto e checkout concluído ao mesmo tempo: a consulta pelo…, _resposta_preferencia(), test_configuracao_ausente_falha_de_forma_explicita() (+18 more)

### Community 20 - "checkout_bp.py"
Cohesion: 0.11
Nodes (26): abrir_checkout(), _acesso_permitido(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), limitar_consulta_pagamento, limitar_criacao_pagamento, route (+18 more)

### Community 21 - "pix.js"
Cohesion: 0.33
Nodes (14): abrirPix(), alvoDoRotulo(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), liberarBotao(), limparConteudoAnterior() (+6 more)

### Community 22 - "config.py"
Cohesion: 0.10
Nodes (25): _paginar(), Aplica LIMIT/OFFSET e conta o total numa consulta separada e barata. A contagem…, Decimal, Matricula, Pagamento, _para_decimal(), Status a exibir, com o vencimento já aplicado. Uma cobrança `pendente` cujo…, Plano (+17 more)

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
Cohesion: 0.15
Nodes (17): _acesso_permitido(), cadastrar_professor(), desmatricular_aluno(), detalhe_turma(), editar_professor(), foto_professor(), matricular_aluno(), painel_professor() (+9 more)

### Community 35 - "adm_bp.py"
Cohesion: 0.07
Nodes (52): _aluno_do_cpf_ou_painel(), aprovar_aluno(), aprovar_comprovante_manual(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_aluno(), cadastrar_pagamento(), cadastrar_plano() (+44 more)

### Community 36 - "Presenca"
Cohesion: 0.24
Nodes (9): Presenca, Valor que representa a credencial administrativa em vigor, ou None se não há…, referencia_credencial_admin(), parametrize, test_aluno_confirma_sua_frequencia(), test_consulta_com_data_invalida_exibe_hoje_e_aviso(), test_corrigir_falta_remove_confirmacao_anterior(), test_presenca_com_data_invalida_nao_grava() (+1 more)

### Community 37 - ".buscar_por_id"
Cohesion: 0.25
Nodes (8): _imagem_jpeg_valida(), test_admin_acessa_foto_de_qualquer_aluno(), test_aluno_nao_acessa_foto_de_outro_aluno(), test_substituir_e_remover_foto(), test_upload_de_arquivo_disfarcado_e_recusado(), test_upload_de_foto_valida(), test_perfil_dados_recusa_campo_maior_que_a_coluna(), test_perfil_email_recusa_endereco_invalido_ou_grande_demais()

### Community 38 - "convites.py"
Cohesion: 0.15
Nodes (18): aluno_do_token(), ConviteIndisponivel, descartar(), enviar(), gerar_token(), _hash(), RuntimeError, Convite de acesso: como um cadastro criado pela administração vira uma conta.… (+10 more)

### Community 41 - "Academia"
Cohesion: 0.20
Nodes (10): Academia, parametrize, test_admin_salva_atualiza_e_limpa_contatos(), test_configuracoes_exigem_admin(), test_contatos_invalidos(), test_csrf_configuracoes(), test_erro_preserva_formulario_e_dados_salvos(), test_link_email_preserva_caracteres_do_endereco() (+2 more)

### Community 42 - "pagamento_polling.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 43 - "mercado_pago_conta.py"
Cohesion: 0.11
Nodes (33): access_token_vigente(), _agora(), ambiente_da_conexao(), _cifrar(), _client_id(), _client_secret(), ConexaoIlegivel, _decifrar() (+25 more)

### Community 44 - "criar_pagamento"
Cohesion: 0.10
Nodes (46): criar_pagamento(), logar_como_aluno(), Hipótese: forjar ?status=approved na volta do MP quita a mensalidade., test_retorno_ignora_status_aprovado_da_query_string(), _mockar_preferencia(), Um boleto pendente do Checkout Pro grava provider_payment_id, mas não é Pix:…, test_abertura_json_navega_sem_redirecionar_post_externo(), test_admin_tambem_pode_abrir_checkout() (+38 more)

### Community 45 - "test_pix_rotas.py"
Cohesion: 0.20
Nodes (20): _assinar(), _resposta_consulta(), _resposta_criacao(), test_admin_tambem_pode_gerar_pix(), test_aluno_gera_pix_da_propria_mensalidade(), test_aluno_nao_acessa_mensalidade_de_outro_aluno(), test_falha_de_indisponibilidade_do_mp_retorna_503(), test_impede_cobranca_duplicada_em_chamadas_consecutivas() (+12 more)

### Community 46 - "PagamentoEvento"
Cohesion: 0.13
Nodes (9): Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda. O…, Abre o período de acesso no momento em que o pagamento é confirmado. Se a…, Reescreve os campos denormalizados do aluno a partir das mensalidades.…, forma_pagamento vem do que o Mercado Pago confirmou na consulta à API ('pix',…, Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.…, PagamentoEvento, Histórico de auditoria de uma mensalidade (nunca grava credenciais ou dados…, test_comprovante_em_analise_marca_situacao_do_aluno() (+1 more)

### Community 47 - "d9e2f6a14c80_contatos_academia_perfis_professores.py"
Cohesion: 0.83
Nodes (3): _campos_professor(), downgrade(), upgrade()

### Community 49 - "EmailPendente"
Cohesion: 0.25
Nodes (5): EmailPendente, parametrize, Agendamento sem rede, threads reais ou esperas de relógio., test_nao_inicia_em_testes(), test_retomada_de_item_persistido_e_retentativa_sem_painel()

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
Cohesion: 0.27
Nodes (12): _autorizacao_valida(), callback(), conectar(), desconectar(), limit, route, O state devolvido é o que ESTA sessão emitiu, há pouco tempo?, Só monta o state/PKCE na sessão e manda o administrador ao Mercado Pago. É um… (+4 more)

### Community 57 - "fila_email.py"
Cohesion: 0.13
Nodes (18): espera_da_proxima_tentativa(), Fila de e-mails no banco. Aviso e cobrança coletivos saíam um a um dentro da…, contar_falhados(), contar_pendentes(), enfileirar(), enfileirar_transacional(), _entregar(), listar_pendentes() (+10 more)

### Community 58 - "test_migracao_cadastro_administrativo.py"
Cohesion: 0.40
Nodes (3): banco_antigo(), fixture, Verifica a migração em um banco isolado com o schema anterior e dados.

### Community 59 - "salvar_foto_perfil"
Cohesion: 0.11
Nodes (30): enviar_comprovante_manual_aluno(), enviar_foto_perfil(), remover_foto_perfil(), ArquivoInvalido, caminho_arquivo(), _conferir_dimensoes(), _detectar_tipo_imagem_real(), ImagemGrandeDemais (+22 more)

### Community 60 - "test_keep_alive.py"
Cohesion: 0.16
Nodes (7): ambiente_limpo(), fixture, parametrize, Garante que o keep-alive fica desligado por padrão e só pinga a própria origem., test_intervalo_fica_dentro_da_faixa(), test_nao_liga_com_valor_negativo(), test_ping_so_considera_200_como_sucesso()

### Community 61 - "gmail_conta.py"
Cohesion: 0.26
Nodes (15): GmailConexao, _access_token(), _cifrar(), _client_id(), _client_secret(), _decifrar(), enviar(), estado() (+7 more)

### Community 62 - "mercado_pago.py"
Cohesion: 0.14
Nodes (26): _base_url_opcional(), base_url_publica(), buscar_pagamentos_por_referencia(), cancelar_pagamento(), criar_pagamento_pix(), criar_preferencia_checkout(), _erro_menciona(), _erro_menciona_expiracao() (+18 more)

### Community 63 - "test_arranque_seguranca.py"
Cohesion: 0.22
Nodes (14): _env_arranque(), Validações feitas por servidor.py no arranque (COOKIE_SECURE, TRUSTED_HOSTS,…, `python -m servicos.credenciais`: o hash sai entre aspas simples. O hash do…, Desenvolvimento local sem HTTPS (sem Caddy) não pode ficar travado., _rodar(), test_arranque_falha_com_cookie_secure_false_e_app_base_url_https(), test_arranque_falha_com_cookie_secure_invalido(), test_arranque_falha_sem_trusted_hosts() (+6 more)

### Community 64 - "disparar"
Cohesion: 0.29
Nodes (7): disparar(), _laco(), _liberar_e_retomar_se_preciso(), Drena a fila enquanto houver entrega acontecendo. Encerra na primeira passada…, Desregistra a thread e sobe outra se alguém pediu trabalho durante a queda. Sem…, Acorda o processamento em segundo plano, sem bloquear a requisição. Se a thread…, test_reaciona_fila_sem_requisicao_e_sobrevive_a_falha()

### Community 66 - "URLPublicaInvalida"
Cohesion: 0.22
Nodes (13): iniciar(), _intervalo(), _laco(), _ligado(), parar(), _pingar(), Mantém a aplicação acordada em hospedagens que hibernam por inatividade. Uma…, Encerra o laço. Usado pelos testes; em produção a thread é daemon. (+5 more)

### Community 67 - "servidor.py"
Cohesion: 0.11
Nodes (21): after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, context_processor, errorhandler, Registra a sessão como encerrada: cópias antigas do cookie deixam de valer.…, revogar_sessao_atual(), formatar_moeda() (+13 more)

### Community 68 - "aluno_autorizado"
Cohesion: 0.29
Nodes (7): aluno_autorizado(), _credencial_confere(), encerrar_sessao(), A sessão foi emitida para a credencial que vale AGORA? Uma sessão sem carimbo é…, Aluno da sessão, revalidado no banco, ou None se o acesso não vale mais., A sessão tem identificador e ele não foi revogado pelo logout? Sessão sem…, _sessao_ativa()

### Community 69 - "pagina_cadastro"
Cohesion: 0.19
Nodes (18): _convidar_cadastro_existente_por_id(), _em_segundo_plano(), _enviar_em_segundo_plano(), pagina_cadastro(), Roda `tarefa` fora da requisição, para o tempo de resposta não revelar nada. Em…, E-mail COM token (recuperação, confirmação): não pode ir para a `fila_email`. A…, Versão para thread de fundo: a sessão da requisição não vale fora dela., recuperar_senha() (+10 more)

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
Nodes (28): _acesso_permitido_pagamento(), _aluno_da_sessao(), atualizar_dados_perfil(), cancelar_mudanca_plano(), comprovante_mensalidade(), confirmar_presenca(), foto_perfil(), _pagamento_com_acesso_ou_404() (+20 more)

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

### Community 85 - "academia_bp.py"
Cohesion: 0.27
Nodes (8): configuracoes(), _pagina(), route, link_email(), Normalização de contatos profissionais antes de montar links públicos., validar_email(), validar_instagram(), validar_whatsapp()

### Community 86 - "test_sessao_revogada.py"
Cohesion: 0.24
Nodes (11): Sessões encerradas pelo logout. A sessão do Flask é um cookie assinado, sem…, SessaoRevogada, _cliente_com_cookie(), _entrar_como_admin(), `session.clear()` só limpava o navegador de quem saiu; a cópia do cookie seguia…, test_logout_apaga_revogacoes_vencidas(), test_logout_de_uma_sessao_nao_derruba_as_outras(), test_logout_revoga_a_copia_do_cookie_feita_antes() (+3 more)

### Community 90 - "Relatório de segurança — Sistema Extreme Team"
Cohesion: 0.29
Nodes (6): Controles verificados, Histórico de auditorias, Pendências não relacionadas a segurança, Relatório de segurança — Sistema Extreme Team, Situação atual (22/09/2026 — 2ª rodada), Validação executada em 22/09/2026

### Community 94 - "admin_requerido"
Cohesion: 0.35
Nodes (8): callback(), conectar(), desconectar(), limit, route, _voltar(), gerenciar_turmas(), admin_requerido()

### Community 96 - "MatriculaDAO"
Cohesion: 0.24
Nodes (10): cadastrar_turma(), MatriculaDAO, TurmaDAO, Turma, test_escolher_plano_com_turma_cria_matricula(), test_turma_lotada_nao_vira_matricula_apos_pagamento(), fixture, test_professor_nao_pode_matricular_aluno() (+2 more)

### Community 98 - ".listar_paginado"
Cohesion: 0.29
Nodes (6): Uma página de alunos já cadastrados, recortada e filtrada pelo banco. O painel…, O CPF é guardado formatado; digitar só os números precisa encontrar mesmo assim., test_busca_do_admin_encontra_o_aluno_pelo_cpf_so_com_digitos(), test_busca_por_nome_com_numero_nao_devolve_todo_mundo(), test_paginacao_do_admin_ignora_pendentes_como_a_tela_sempre_fez(), test_painel_admin_pagina_alunos_no_banco()

### Community 99 - "SolicitacaoMudancaPlano"
Cohesion: 0.22
Nodes (4): O que aconteceu numa tentativa de contratar/renovar/trocar de plano., ResultadoContratacao, Pedido de troca de plano agendado para a próxima renovação. Nunca altera o…, SolicitacaoMudancaPlano

### Community 100 - "erro_validacao_senha"
Cohesion: 0.15
Nodes (18): alterar_senha_perfil(), _aluno_por_token(), ativar_acesso(), confirmar_email(), limit, Descarta todo link pendente que ainda autorizaria assumir ou redirecionar a…, Localiza o aluno pelo hash do token, filtrando no banco por uma coluna indexada., Transforma um cadastro feito no balcão na conta do próprio aluno. Quem chega… (+10 more)

### Community 103 - "Flask App Service (compose)"
Cohesion: 0.22
Nodes (9): Flask App Service (compose), Postgres DB Service (compose), postgres_data Volume, Flask, Flask-SQLAlchemy, Gunicorn, psycopg2-binary, python-dotenv (+1 more)

### Community 108 - "criar_aluno"
Cohesion: 0.07
Nodes (31): Totais do painel financeiro - sempre calculados no backend a partir do banco,…, criar_aluno(), test_aluno_existente_continua_entrando_normalmente(), test_area_do_aluno_renderiza_telas_independentes_do_menu(), test_plano_atual_continua_disponivel_para_gerar_cobranca(), test_busca_financeira_trata_curingas_como_texto(), test_painel_financeiro_busca_por_nome_do_aluno(), test_painel_financeiro_exige_admin() (+23 more)

## Knowledge Gaps
- **83 isolated node(s):** `modal`, `input_senha`, `icone_senha`, `formularioPlano`, `campoPreco` (+78 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PagamentoDAO` connect `PagamentoDAO` to `.efetivar_mudancas_por_prazo`, `.listar_por_aluno`, `test_mudanca_plano.py`, `test_regressao_auditoria.py`, `pix_bp.py`, `logar_como_admin`, `test_checkout_rotas.py`, `checkout_bp.py`, `config.py`, `test_auditoria_seguranca.py`, `adm_bp.py`, `criar_pagamento`, `test_pix_rotas.py`, `PagamentoEvento`, `test_seguranca.py`, `salvar_foto_perfil`, `usuario_bp.py`, `MatriculaDAO`, `SolicitacaoMudancaPlano`, `criar_aluno`?**
  _High betweenness centrality (0.161) - this node is a cross-community bridge._
- **Why does `AlunoDAO` connect `logar_como_admin` to `MatriculaDAO`, `turma_bp.py`, `adm_bp.py`, `.listar_paginado`, `pagina_cadastro`, `test_mudanca_plano.py`, `pagina_login`, `PagamentoDAO`, `.buscar_por_id`, `usuario_bp.py`, `test_regressao_auditoria.py`, `criar_aluno`, `test_seguranca.py`, `config.py`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Why does `criar_aluno()` connect `criar_aluno` to `.efetivar_mudancas_por_prazo`, `.listar_por_aluno`, `test_limites_pagamento.py`, `test_mudanca_plano.py`, `PagamentoDAO`, `test_regressao_auditoria.py`, `test_mercado_pago_oauth.py`, `Professor`, `logar_como_admin`, `config.py`, `test_auditoria_seguranca.py`, `Presenca`, `.buscar_por_id`, `criar_pagamento`, `test_pix_rotas.py`, `test_seguranca.py`, `_parece_busca_por_cpf`, `_chave_da_conta`, `MatriculaDAO`, `.listar_paginado`, `test_painel_financeiro_nao_varre_mensalidades_fora_do_filtro`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Are the 136 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 136 INFERRED edges - model-reasoned connections that need verification._
- **Are the 139 inferred relationships involving `criar_pagamento()` (e.g. with `PagamentoDAO` and `Pagamento`) actually correct?**
  _`criar_pagamento()` has 139 INFERRED edges - model-reasoned connections that need verification._
- **Are the 132 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 132 INFERRED edges - model-reasoned connections that need verification._
- **Are the 111 inferred relationships involving `logar_como_aluno()` (e.g. with `test_aluno_nao_alcanca_cobranca_de_outro_aluno()` and `test_checkout_recusa_cobranca_indisponivel()`) actually correct?**
  _`logar_como_aluno()` has 111 INFERRED edges - model-reasoned connections that need verification._