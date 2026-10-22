# Graph Report - SistemaEXTREMETEAM  (2026-10-07)

## Corpus Check
- 184 files · ~241,778 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2509 nodes · 6061 edges · 157 communities (142 shown, 15 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 1111 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5f93d678`
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
- fase3b.js
- test_analytics.py
- test_migracao_checkout.py
- checkout.js
- CLAUDE.md
- test_home_planos.py
- test_mercado_pago_oauth_postgres.py
- logar_como_admin
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
- MatriculaDAO
- test_limites_requisicao.py
- seo.py
- gmail_conta.py
- PagamentoEvento
- Academia
- pagamento_polling.test.cjs
- mercado_pago_conta.py
- ConfiguracaoInvalida
- test_pix_rotas.py
- test_planilha_economica.py
- d9e2f6a14c80_contatos_academia_perfis_professores.py
- ProfessorDAO
- botao_ocupado.test.cjs
- test_seguranca.py
- checkout_abertura.test.cjs
- filtros_financeiro.js
- gunicorn.conf.py
- PagamentoDAO
- fila_email.py
- test_migracao_cadastro_administrativo.py
- salvar_comprovante_manual
- test_keep_alive.py
- test_google_login.py
- MercadoPagoIndisponivel
- test_arranque_seguranca.py
- Aluno
- salvar_foto_perfil
- servidor.py
- formatar_competencia
- .buscar_por_id
- credenciais.py
- shot.mjs
- Componentes
- convites.py
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
- test_checkout_rotas.py
- armazenamento.py
- test_layouts.py
- Plano
- usuario_bp.py
- Flask App Service (compose)
- Professor
- test_plano_arquivo_promocao.py
- Etapa 1 — migrar páginas para os layouts (SEM mudar o visual)
- Etapas 4 a 6 — aluno, admin, professor (aplicar os componentes nas páginas)
- seo_bp.py
- Etapa 2 — biblioteca de componentes
- Etapa 3 — home com os planos + termos
- test_prontidao.py
- test_perfil_e_foto.py
- keep_alive.py
- test_observabilidade.py
- .contratar_plano
- analytics.py
- test_backup_scripts.py
- autorizacao.py
- gerar_imagem_og.py
- _tem_limite
- detalhes_usuario
- formatacao.py
- PlanoDAO
- impressao_credencial
- usuario_e_admin
- revogar_sessao_atual
- _json_ld
- AlunoDAO
- test_conversao_home.py
- test_financeiro_admin_painel.py
- prontidao.py
- _valor_em_reais
- ativar_acesso
- _convidar_cadastro_existente_por_id
- backup.sh
- vercel.json
- Biblioteca no Figma
- _FakePaymentResource
- conteudo_home.py
- api_mp
- agendar.sh
- restaurar.sh
- verificar_email_cadastro
- adm_bp.py
- _enviar_em_segundo_plano
- adicionar_cabecalhos_de_seguranca
- test_limites_pagamento.py
- _cadastro_recebido
- Exception
- exempt

## God Nodes (most connected - your core abstractions)
1. `PagamentoDAO` - 211 edges
2. `logar_como_admin()` - 166 edges
3. `criar_aluno()` - 164 edges
4. `criar_pagamento()` - 161 edges
5. `logar_como_aluno()` - 136 edges
6. `AlunoDAO` - 84 edges
7. `PlanoDAO` - 62 edges
8. `Aluno` - 52 edges
9. `MercadoPagoIndisponivel` - 45 edges
10. `Pagamento` - 40 edges

## Surprising Connections (you probably didn't know these)
- `Presença Form` --shares_data_with--> `Presenca`  [INFERRED]
  templates/turma.html → modelos/presenca.py
- `Histórico de Mensalidades Section` --shares_data_with--> `Pagamento`  [INFERRED]
  templates/pgUsuario.html → modelos/pagamento.py
- `Cadastrar Plano Form` --shares_data_with--> `Plano`  [INFERRED]
  templates/pgAdm.html → modelos/plano.py
- `Planos Disponíveis Section` --shares_data_with--> `Plano`  [INFERRED]
  templates/pgUsuario.html → modelos/plano.py
- `Cadastrar Professor Form` --shares_data_with--> `Professor`  [INFERRED]
  templates/turmas.html → modelos/professor.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Shared Confirmation Modal Pattern** — templates_components_confirm_modal_dialog, templates_pgadm_page, templates_pgprofessor_page, templates_pgusuario_page, templates_turmas_page [EXTRACTED 1.00]
- **Mensalidade (Billing) Management Flow** — templates_dt_aluno_pagamento_form, templates_pgusuario_mensalidades_section, modelos_pagamento_pagamento, modelos_plano_plano [INFERRED 0.85]
- **Turma and Attendance Management Flow** — templates_turmas_turma_form, templates_turma_presenca_form, templates_pgprofessor_page, modelos_turma_turma [INFERRED 0.85]

## Communities (157 total, 15 thin omitted)

### Community 0 - "criar_pagamento"
Cohesion: 0.09
Nodes (49): criar_pagamento(), logar_como_aluno(), Hipótese: forjar ?status=approved na volta do MP quita a mensalidade., Hipótese: dá para injetar o valor pelo corpo do POST., Versão forte da sonda de IDOR: o alvo TEM arquivo, então um 200 seria vazamento., test_comprovante_de_outro_aluno_com_arquivo_real_nao_vaza(), test_retorno_ignora_status_aprovado_da_query_string(), test_valor_cobrado_vem_do_banco_e_nao_do_navegador() (+41 more)

### Community 1 - "extreme.css"
Cohesion: 0.05
Nodes (37): abrirmodal(), fechar(), icone_senha, input_senha, modal, mostrarSenha(), campoDuracao, campoPreco (+29 more)

### Community 2 - "planos.py"
Cohesion: 0.06
Nodes (42): cadeia_paga(), cartao_do_plano(), cobranca_a_pagar(), cobranca_em_decisao(), cobranca_pendente(), duracao_dias(), _duracao_por_extenso(), esta_inadimplente() (+34 more)

### Community 3 - "criar_aluno"
Cohesion: 0.13
Nodes (36): criar_aluno(), parametrize, test_admin_lanca_mensalidade_paga_no_cartao(), test_aluno_existente_continua_entrando_normalmente(), test_escolher_plano_cria_mensalidade_e_redireciona_para_pix(), test_plano_invalido_nao_cria_mensalidade(), test_reenvio_da_contratacao_reutiliza_mensalidade(), test_valor_enviado_pelo_navegador_e_ignorado() (+28 more)

### Community 4 - "test_pagamento_recusado.py"
Cohesion: 0.23
Nodes (22): test_polling_usa_consultas_curtas_sem_retentativas(), test_retorno_checkout_usa_consulta_curta_sem_retentativas(), _assinar(), _data_mp(), _eventos(), _mockar_mp(), _pagamento_mp(), _pix_criado() (+14 more)

### Community 5 - "test_mudanca_plano.py"
Cohesion: 0.18
Nodes (24): Persistência dos pedidos de troca de plano agendados para a próxima renovação., SolicitacaoPlanoDAO, _agendar(), _pagar(), plano_barato(), fixture, Mudança para um plano mais barato agendada para a próxima renovação. Regra…, O admin pode estornar/cancelar a mensalidade que sustentava a vigência depois… (+16 more)

### Community 6 - "pix_bp.py"
Cohesion: 0.07
Nodes (42): _acesso_permitido(), _chave_entrega_webhook(), criar_pix_mensalidade(), _data_da_aprovacao(), _forma_pagamento_confirmada(), _instante_utc(), _iso_utc(), _liberar_entrega_webhook() (+34 more)

### Community 7 - "test_regressao_auditoria.py"
Cohesion: 0.04
Nodes (42): _contar_selects_em_alunos(), _credencial(), Regressões da auditoria de segurança, desempenho e confiabilidade. Cada caso…, Head-of-line blocking: a primeira linha falhando não pode impedir as seguintes.…, Uma linha `desistiu` nunca foi entregue: recusar o reenvio fazia a tela dizer…, A revivência vale só para o abandonado: clique duplo continua virando um envio., Trocar senha, e-mail ou foto são ações de quem JÁ está autenticado. Devolver o…, Persistência não é retomada: alguém precisa acordar a fila quando o adiamento… (+34 more)

### Community 9 - "test_mercado_pago_servico.py"
Cohesion: 0.10
Nodes (31): Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, validar_assinatura_webhook(), Hipótese: uma notificação capturada ontem pode ser reenviada hoje., `ts=nan` fazia a comparação da janela dar False e passava pela checagem de…, test_webhook_recusa_assinatura_antiga(), test_webhook_recusa_ts_nao_numerico_finito(), base_url(), _criar_preferencia() (+23 more)

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
Cohesion: 0.19
Nodes (16): Marca o plano em destaque da página inicial, desmarcando qualquer outro.…, Inclusive os arquivados: serve a quem olha o histórico (filtro do financeiro)., Planos da página inicial, prontos para `components/cartao_plano.html`. O preço…, vitrine_planos(), _plano(), _quatro_planos(), Planos na página inicial: cálculo (servicos/planos.vitrine_planos), destaque…, test_admin_pode_criar_plano_ja_em_destaque() (+8 more)

### Community 17 - "test_mercado_pago_oauth_postgres.py"
Cohesion: 0.18
Nodes (8): postgres_mp(), fixture, Renovação do token OAuth com trava de linha real, opcional na suíte que usa…, _Resposta, test_dois_processos_perto_do_vencimento_gastam_o_refresh_token_uma_vez(), _migracao(), test_migracao_cria_a_tabela_igual_ao_modelo_e_e_reentrante(), test_migracao_encadeia_na_ultima_revisao_existente()

### Community 18 - "logar_como_admin"
Cohesion: 0.10
Nodes (56): _convidar_cadastro_existente(), Cadastro administrativo que alguém tentou recriar pelo formulário público. Em…, erro_confirmacao_senha(), Retorna uma mensagem quando a confirmação não repete exatamente a senha. A…, logar_como_admin(), _matricular(), parametrize, Cadastro de aluno pela administração, ativação de acesso e confirmação de… (+48 more)

### Community 19 - "test_mercado_pago_oauth.py"
Cohesion: 0.07
Nodes (58): MercadoPagoConexao, Conta do Mercado Pago que a academia autorizou por OAuth. Uma linha só (a…, _agora(), _ajustar(), _conectar(), _dados_conexao(), _preparar_state(), parametrize (+50 more)

### Community 20 - "checkout_bp.py"
Cohesion: 0.08
Nodes (32): abrir_checkout(), _acesso_permitido(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), limitar_consulta_pagamento, limitar_criacao_pagamento, route (+24 more)

### Community 21 - "pix.js"
Cohesion: 0.33
Nodes (14): abrirPix(), alvoDoRotulo(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), liberarBotao(), limparConteudoAnterior() (+6 more)

### Community 22 - "config.py"
Cohesion: 0.13
Nodes (15): _paginar(), Aplica LIMIT/OFFSET e conta o total numa consulta separada e barata. A contagem…, Decimal, Matricula, _para_decimal(), Pedido de troca de plano agendado para a próxima renovação. Nunca altera o…, SolicitacaoMudancaPlano, postgres_pix() (+7 more)

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
Nodes (42): _agora_mercado_pago(), _assinar(), logar_como_professor(), _pagamento_mp(), _preparar_para_conciliacao(), fixture, parametrize, Auditoria de segurança: sondas escritas para TENTAR quebrar as regras. Nenhum… (+34 more)

### Community 34 - "MatriculaDAO"
Cohesion: 0.22
Nodes (12): MatriculaDAO, TurmaDAO, Turma, Sonda: a data vem da query string e é convertida sem tratamento., test_data_invalida_na_turma_nao_derruba_a_rota(), test_area_do_aluno_renderiza_telas_independentes_do_menu(), test_escolher_plano_com_turma_cria_matricula(), test_plano_atual_continua_disponivel_para_gerar_cobranca() (+4 more)

### Community 35 - "test_limites_requisicao.py"
Cohesion: 0.12
Nodes (28): consultar_mp(), _estourar(), fixture, parametrize, Limites de requisição da rodada de 04/10/2026 (SEC-10 a SEC-17 e SEC-19). Cada…, Trocar de rede ou abrir outra sessão não devolve a cota de e-mails em massa., Faz `limite` requisições sem nenhum 429 e devolve a seguinte., Alunos no mesmo Wi-Fi não dividem o teto padrão, nem com o visitante anônimo. (+20 more)

### Community 36 - "seo.py"
Cohesion: 0.18
Nodes (18): conteudo_robots(), conteudo_sitemap(), dados_estruturados_academia(), _dia(), _dias_da_linha(), _hora(), horarios_estruturados(), origem_publica() (+10 more)

### Community 37 - "gmail_conta.py"
Cohesion: 0.17
Nodes (18): GmailConexao, _access_token(), _cifrar(), _client_id(), _client_secret(), _decifrar(), enviar(), estado() (+10 more)

### Community 38 - "PagamentoEvento"
Cohesion: 0.10
Nodes (12): Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.…, Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda. O…, Primeiro dia não coberto por outra mensalidade do mesmo aluno., Define o período coberto por uma mensalidade que ainda não tem um (lançamento…, Abre o período de acesso no momento em que o pagamento é confirmado. Se a…, Reescreve os campos denormalizados do aluno a partir das mensalidades.…, forma_pagamento vem do que o Mercado Pago confirmou na consulta à API ('pix',…, Uma recusa encerra aquela tentativa, não a mensalidade. Quando o aluno gera um… (+4 more)

### Community 41 - "Academia"
Cohesion: 0.16
Nodes (11): Academia, link_email(), parametrize, test_admin_salva_atualiza_e_limpa_contatos(), test_configuracoes_exigem_admin(), test_contatos_invalidos(), test_csrf_configuracoes(), test_erro_preserva_formulario_e_dados_salvos() (+3 more)

### Community 42 - "pagamento_polling.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 43 - "mercado_pago_conta.py"
Cohesion: 0.11
Nodes (35): access_token_vigente(), _agora(), ambiente_da_conexao(), _cifrar(), _client_id(), _client_secret(), ConexaoIlegivel, _decifrar() (+27 more)

### Community 44 - "ConfiguracaoInvalida"
Cohesion: 0.10
Nodes (34): configuracoes(), _pagina(), route, callback(), login_google(), limit, route, redirect_uri() (+26 more)

### Community 45 - "test_pix_rotas.py"
Cohesion: 0.20
Nodes (20): _agora_mercado_pago(), _assinar(), _resposta_consulta(), _resposta_criacao(), test_admin_tambem_pode_gerar_pix(), test_aluno_gera_pix_da_propria_mensalidade(), test_aluno_nao_acessa_mensalidade_de_outro_aluno(), test_falha_de_indisponibilidade_do_mp_retorna_503() (+12 more)

### Community 46 - "test_planilha_economica.py"
Cohesion: 0.05
Nodes (66): callback(), conectar(), desconectar(), limit, route, _voltar(), alterar_despesa(), _ano_e_mes() (+58 more)

### Community 47 - "d9e2f6a14c80_contatos_academia_perfis_professores.py"
Cohesion: 0.83
Nodes (3): _campos_professor(), downgrade(), upgrade()

### Community 49 - "ProfessorDAO"
Cohesion: 0.17
Nodes (15): ProfessorDAO, _foto(), pasta_fotos(), professor(), fixture, parametrize, test_admin_salva_perfil_sem_alterar_acesso(), test_apenas_admin_edita_perfil() (+7 more)

### Community 50 - "botao_ocupado.test.cjs"
Cohesion: 0.18
Nodes (7): assert, criarElemento(), fs, montar(), path, test, vm

### Community 51 - "test_seguranca.py"
Cohesion: 0.08
Nodes (24): _carregar_senhas_comuns(), erro_validacao_senha(), Retorna uma mensagem quando a senha é curta, comum ou igual ao identificador., Lê a lista de senhas comuns (uma por linha; `#` abre comentário) para um…, _cadastro_publico(), _imagem_jpeg(), _mensagem_da_resposta(), O ramo "par existe" não pode pagar a ida ao provedor dentro da requisição. (+16 more)

### Community 52 - "checkout_abertura.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 55 - "gunicorn.conf.py"
Cohesion: 0.25
Nodes (9): post_worker_init(), Hooks carregados pelo Gunicorn; nunca executados por flask db upgrade., worker_exit(), iniciar(), _laco(), parar(), Aciona a fila periodicamente durante a vida de um worker Gunicorn. Importar…, Inicia uma vez por processo, depois de carregar a aplicação e migrar o banco. (+1 more)

### Community 56 - "PagamentoDAO"
Cohesion: 0.09
Nodes (28): mensalidade_destaque(), PagamentoDAO, Status como o painel deve LER, com o vencimento aplicado na própria consulta. A…, Carrega aluno e plano junto das mensalidades. O template do painel lê…, Lista completa (sem paginar). Mantida para relatórios e testes., Uma página de mensalidades, recortada pelo banco (LIMIT/OFFSET). O painel…, Totais do painel financeiro - sempre calculados no backend a partir do banco,…, Escolhe a mensalidade mais relevante para o card 'Minha mensalidade': a mais… (+20 more)

### Community 57 - "fila_email.py"
Cohesion: 0.06
Nodes (40): EmailPendente, espera_da_proxima_tentativa(), Fila de e-mails no banco. Aviso e cobrança coletivos saíam um a um dentro da…, contar_falhados(), contar_pendentes(), disparar(), enfileirar(), enfileirar_transacional() (+32 more)

### Community 58 - "test_migracao_cadastro_administrativo.py"
Cohesion: 0.40
Nodes (3): banco_antigo(), fixture, Verifica a migração em um banco isolado com o schema anterior e dados.

### Community 59 - "salvar_comprovante_manual"
Cohesion: 0.14
Nodes (16): _conferir_dimensoes(), _detectar_tipo_imagem_real(), ImagemGrandeDemais, Imagem cujas DIMENSÕES declaradas passam do limite de pixels., Recusa pelo cabeçalho, antes de qualquer pixel ser decodificado. `Image.open`…, Confere o conteúdo de fato (decodificando com Pillow), não a extensão/Content-…, Valida e salva um comprovante manual (JPEG, PNG ou PDF). Imagens passam pelo…, salvar_comprovante_manual() (+8 more)

### Community 60 - "test_keep_alive.py"
Cohesion: 0.16
Nodes (7): ambiente_limpo(), fixture, parametrize, Garante que o keep-alive fica desligado por padrão e só pinga a própria origem., test_intervalo_fica_dentro_da_faixa(), test_nao_liga_com_valor_negativo(), test_ping_so_considera_200_como_sucesso()

### Community 61 - "test_google_login.py"
Cohesion: 0.10
Nodes (20): Esquece a conta conectada. Devolve True se havia uma., remover_conexao(), fixture, Registra as chamadas e devolve as respostas configuradas por método., storage(), _StorageFalso, test_envia_pelo_gmail_com_o_refresh_token_da_conexao(), cliente_google() (+12 more)

### Community 62 - "MercadoPagoIndisponivel"
Cohesion: 0.08
Nodes (44): _base_url_opcional(), buscar_pagamento(), buscar_pagamentos_por_referencia(), cancelar_pagamento(), criar_pagamento_pix(), criar_preferencia_checkout(), _erro_menciona(), _erro_menciona_expiracao() (+36 more)

### Community 63 - "test_arranque_seguranca.py"
Cohesion: 0.22
Nodes (14): _env_arranque(), Validações feitas por servidor.py no arranque (COOKIE_SECURE, TRUSTED_HOSTS,…, `python -m servicos.credenciais`: o hash sai entre aspas simples. O hash do…, Desenvolvimento local sem HTTPS (sem Caddy) não pode ficar travado., _rodar(), test_arranque_falha_com_cookie_secure_false_e_app_base_url_https(), test_arranque_falha_com_cookie_secure_invalido(), test_arranque_falha_sem_trusted_hosts() (+6 more)

### Community 64 - "Aluno"
Cohesion: 0.10
Nodes (12): Aluno, Se existe uma conta de acesso, e não se o aluno está em dia ou matriculado.…, Convite de acesso já enviado e ainda não usado (a validade é checada na rota)., Chave do estado da CONTA - nunca da situação financeira nem da matrícula., capturar_emails(), fixture, Intercepta o envio e devolve os e-mails que teriam saído, com os links., test_cadastro_publico_com_cpf_de_cadastro_administrativo_nao_duplica() (+4 more)

### Community 66 - "salvar_foto_perfil"
Cohesion: 0.13
Nodes (24): Exception, ArquivoInvalido, Valida, reprocessa e salva uma foto de perfil. Retorna o nome do arquivo…, Arquivo recusado por tipo, tamanho ou conteúdo não confiável., salvar_foto_perfil(), _jpeg(), parametrize, Uploads no Supabase Storage (produção na Vercel), com o HTTP simulado. (+16 more)

### Community 67 - "servidor.py"
Cohesion: 0.16
Nodes (17): Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, context_processor, errorhandler, formatar_moeda(), Formata um valor em reais no padrão brasileiro: R$ 1.080,00. Usado como filtro…, acesso_negado(), contatos_da_academia() (+9 more)

### Community 69 - "formatar_competencia"
Cohesion: 0.25
Nodes (15): formatar_competencia(), Nome legível da forma de pagamento. Antes as telas usavam `|replace('_','…, Converte 'AAAA-MM' em algo como 'Setembro de 2026'. Devolve o valor original se…, rotulo_forma_pagamento(), _aba_categorias(), _aba_entradas(), _aba_resumo(), _aba_saidas() (+7 more)

### Community 70 - ".buscar_por_id"
Cohesion: 0.14
Nodes (19): _aprovado_no_checkout(), Painel do admin com mensalidades do Mercado Pago: formas de pagamento,…, Cartão/boleto: a preferência existe, o webhook ainda não trouxe o payment_id., _so_com_checkout(), test_admin_muda_o_status_sem_perder_a_forma_do_mercado_pago(), test_admin_nao_grava_forma_inventada(), test_aprovar_comprovante_recusa_forma_inventada(), test_ficha_mantem_no_select_a_forma_confirmada_pelo_mercado_pago() (+11 more)

### Community 71 - "credenciais.py"
Cohesion: 0.20
Nodes (11): admin_configurado(), comparar_em_tempo_constante(), credencial_admin_confere(), gerar_hash_admin(), _main(), Credencial administrativa baseada exclusivamente em hash de senha. O…, Compara duas senhas em tempo constante, sem restrição de alfabeto. Codificar…, True quando existe usuário e hash da senha do administrador. (+3 more)

### Community 72 - "shot.mjs"
Cohesion: 0.29
Nodes (5): { chromium }, contextos, CREDS, jobs, require

### Community 73 - "Componentes"
Cohesion: 0.05
Nodes (36): Altura de controle, Avisos flutuantes, Botões — `.et-botao` + variante (+ tamanho), Cartões e contêineres, Componentes, Contêiner e estrutura, Cores, Dados (+28 more)

### Community 74 - "convites.py"
Cohesion: 0.14
Nodes (23): aluno_do_token(), ConviteIndisponivel, descartar(), enviar(), gerar_token(), _hash(), RuntimeError, Convite de acesso: como um cadastro criado pela administração vira uma conta.… (+15 more)

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
Cohesion: 0.22
Nodes (8): Controles verificados, Histórico de auditorias, Pendências não relacionadas a segurança, Relatório de segurança — Sistema Extreme Team, Rodada anterior (22/09/2026 — 2ª rodada), Situação atual (04/10/2026 — limites de requisição), Validação executada em 04/10/2026, Validação executada em 22/09/2026

### Community 94 - "test_seo.py"
Cohesion: 0.13
Nodes (18): _head(), parametrize, SEO técnico: robots.txt, sitemap, títulos, meta tags, noindex e JSON-LD da home., _robots(), test_area_do_admin_sai_do_indice(), test_area_do_aluno_sai_do_indice(), test_area_do_professor_sai_do_indice(), test_canonical_ignora_query_string() (+10 more)

### Community 95 - "test_email_componentes.py"
Cohesion: 0.33
Nodes (7): E-mails: base com a logo oficial e componentes seguros para cliente de e-mail…, _render(), _sem_recursos_externos(), test_base_sem_url_publica_cai_para_o_nome_em_texto(), test_base_usa_a_logo_quando_ha_url_publica(), test_botao_do_email_usa_o_ouro_do_sistema(), test_cartao_de_resumo_com_badge()

### Community 96 - "test_checkout_rotas.py"
Cohesion: 0.17
Nodes (27): _agora_mercado_pago(), _assinar(), _pagamento_mp(), _preparar_retorno(), parametrize, Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala…, Pix aberto e checkout concluído ao mesmo tempo: a consulta pelo…, _resposta_preferencia() (+19 more)

### Community 97 - "armazenamento.py"
Cohesion: 0.17
Nodes (18): ArmazenamentoIndisponivel, _gravar(), ler_arquivo(), _nome_valido(), _pasta(), _raiz_uploads(), Armazenamento de arquivos enviados por usuários (fotos de perfil, comprovantes…, (URL base do bucket, cabeçalhos) do Supabase Storage, ou None para gravar em… (+10 more)

### Community 98 - "test_layouts.py"
Cohesion: 0.29
Nodes (8): _conferir_head_comum(), parametrize, Layouts base (templates/layouts/) e toasts. Cada página estende o layout da sua…, test_area_do_aluno_carrega_o_layout(), test_flash_de_erro_vira_toast_que_nao_some_sozinho(), test_paginas_publicas_carregam_o_head_comum(), test_painel_admin_carrega_o_layout_admin(), test_toda_pagina_estende_um_layout()

### Community 99 - "Plano"
Cohesion: 0.18
Nodes (6): Plano, Preço de uma cobrança criada em `hoje`., parametrize, test_duas_requisicoes_pix_reutilizam_uma_cobranca_postgres(), Abrir o painel filtrado por um plano não pode tocar as mensalidades dos outros., test_painel_financeiro_nao_varre_mensalidades_fora_do_filtro()

### Community 100 - "usuario_bp.py"
Cohesion: 0.11
Nodes (41): _acesso_permitido_pagamento(), alterar_senha_perfil(), _aluno_da_sessao(), _aluno_por_token(), atualizar_dados_perfil(), cadastro_obrigado(), cancelar_mudanca_plano(), _chave_ip_e_identificador() (+33 more)

### Community 102 - "Flask App Service (compose)"
Cohesion: 0.18
Nodes (11): Flask App Service (compose), Postgres DB Service (compose), postgres_data Volume, exempt, Flask, Flask-SQLAlchemy, Gunicorn, psycopg2-binary (+3 more)

### Community 103 - "Professor"
Cohesion: 0.20
Nodes (5): Professor, Hipótese: a foto continua acessível por URL depois de tirar a publicação., Hipótese: os contatos vazam na home antes de a publicação ser marcada., test_contatos_do_professor_so_aparecem_quando_publicados(), test_foto_do_professor_some_ao_despublicar()

### Community 104 - "test_plano_arquivo_promocao.py"
Cohesion: 0.16
Nodes (23): Tira o plano de venda. Devolve `(plano, pedidos_cancelados)`, ou None. Pedidos…, Pagamento, Status a exibir, com o vencimento já aplicado. Uma cobrança `pendente` cujo…, _pagar(), _plano(), _promocao(), Plano fora de venda (arquivar/reativar/excluir), edição e promoção com período.…, test_admin_nao_lanca_mensalidade_nova_em_plano_arquivado() (+15 more)

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
Cohesion: 0.31
Nodes (6): _imagem_jpeg_valida(), test_admin_acessa_foto_de_qualquer_aluno(), test_aluno_nao_acessa_foto_de_outro_aluno(), test_aluno_ve_o_proprio_perfil(), test_substituir_e_remover_foto(), test_upload_de_foto_valida()

### Community 115 - "keep_alive.py"
Cohesion: 0.29
Nodes (9): iniciar(), _intervalo(), _laco(), _ligado(), parar(), _pingar(), Mantém a aplicação acordada em hospedagens que hibernam por inatividade. Uma…, Encerra o laço. Usado pelos testes; em produção a thread é daemon. (+1 more)

### Community 116 - "test_observabilidade.py"
Cohesion: 0.14
Nodes (20): before_breadcrumb(), before_send(), iniciar_sentry(), _limpar(), mascarar(), Rastreamento de erros opcional com Sentry. Sem `SENTRY_DSN`, nada é importado…, _evento(), fixture (+12 more)

### Community 117 - ".contratar_plano"
Cohesion: 0.10
Nodes (12): O que aconteceu numa tentativa de contratar/renovar/trocar de plano., Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, Aplica um pedido agendado cujo período de origem já terminou sem renovação.…, Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, Com uma troca já agendada, só dois planos fazem sentido num pedido de…, A cobrança do período seguinte tem de nascer no plano que o aluno agendou.…, `pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -…, ResultadoContratacao (+4 more)

### Community 118 - "analytics.py"
Cohesion: 0.28
Nodes (7): analytics_ativo(), id_analytics(), marcar_conversao_cadastro(), Google Analytics 4 opcional, só em página pública e só com consentimento. Sem…, Chamada no arranque: um ID malformado derruba a subida, como as demais…, Esta resposta pode carregar o GA4? Visitante, página pública indexável ou…, validar_configuracao()

### Community 119 - "test_backup_scripts.py"
Cohesion: 0.27
Nodes (11): ambiente(), _executavel(), fixture, Scripts de backup (tools/backup/): retenção, falha sem backup "pela metade" e a…, _rodar(), test_backup_gera_dump_e_uploads_e_aplica_a_retencao(), test_dump_ilegivel_nao_vira_backup(), test_restaurar_em_banco_descartavel_e_extrair_uploads() (+3 more)

### Community 120 - "autorizacao.py"
Cohesion: 0.11
Nodes (31): admin_requerido, _acesso_permitido(), cadastrar_professor(), cadastrar_turma(), desmatricular_aluno(), detalhe_turma(), foto_professor(), gerenciar_turmas() (+23 more)

### Community 122 - "_tem_limite"
Cohesion: 0.20
Nodes (10): parametrize, Qualquer dígito no termo virava `CPF LIKE '%3%'` e devolvia a academia inteira., Rotas que custam hash de senha, processamento de imagem ou sondagem de token., Limites declarados por decorador NAQUELA rota. `resolve_limits` não serve aqui:…, Guarda do teste acima: uma rota sem limite precisa ser reprovada por ele., _tem_limite(), test_busca_so_trata_como_cpf_o_que_parece_cpf(), test_o_detector_de_limite_realmente_discrimina() (+2 more)

### Community 123 - "detalhes_usuario"
Cohesion: 0.25
Nodes (7): atualizar_status_pagamento(), cadastrar_pagamento(), detalhes_usuario(), painel_financeiro(), forma_pagamento_aceita(), Vazio, uma forma do painel ou a que a mensalidade já tem. Sem a última opção,…, rotulo_status()

### Community 124 - "formatacao.py"
Cohesion: 0.15
Nodes (19): cadastrar_aluno(), Matrícula feita pela administração, sem conta de acesso. Pede só o que…, pagina_cadastro(), _parece_busca_por_cpf(), Matrícula feita no balcão: sem login, sem senha e sem convite de acesso. Nasce…, O termo é um CPF, ou um pedaço dele, e não um nome que por acaso tem número?, email_valido(), Validação sintática básica, compartilhada pelos formulários do cadastro. (+11 more)

### Community 125 - "PlanoDAO"
Cohesion: 0.15
Nodes (17): PlanoDAO, Apaga um plano que nunca foi usado. True, None (não existe) ou False (em uso)., Os planos à venda: home, perfil do aluno e formulários de contratação., Planos que algum registro referencia: mensalidade, cadastro de aluno ou pedido…, Grava a edição do admin. Vale para as cobranças criadas daqui em diante: as…, test_admin_destaca_e_tira_o_destaque(), parametrize, test_admin_cria_promocao() (+9 more)

### Community 126 - "impressao_credencial"
Cohesion: 0.14
Nodes (17): PresencaDAO, Presenca, impressao_credencial(), Resumo curto e não reversível do hash da senha, guardado na sessão. Nunca é a…, Valor que representa a credencial administrativa em vigor, ou None se não há…, referencia_credencial_admin(), parametrize, test_aluno_confirma_sua_frequencia() (+9 more)

### Community 127 - "usuario_e_admin"
Cohesion: 0.11
Nodes (26): _aluno_do_cpf_ou_painel(), aprovar_aluno(), arquivar_plano(), cadastrar_plano(), cancelar_mudanca_plano_admin(), destacar_plano(), editar_plano(), enviar_convite_acesso() (+18 more)

### Community 128 - "revogar_sessao_atual"
Cohesion: 0.33
Nodes (7): Registra a sessão como encerrada: cópias antigas do cookie deixam de valer.…, revogar_sessao_atual(), health_pronto(), home(), logout(), limit, route

### Community 130 - "_json_ld"
Cohesion: 0.38
Nodes (7): _json_ld(), Nenhum campo do JSON-LD pode sair nulo, vazio ou só com espaços., _sem_vazios(), test_json_ld_completo_a_partir_da_academia(), test_json_ld_nao_deixa_texto_do_painel_fechar_o_script(), test_json_ld_omite_campos_vazios(), test_json_ld_sem_dados_da_academia_so_tem_o_basico()

### Community 131 - "AlunoDAO"
Cohesion: 0.13
Nodes (17): ativar_aluno(), desativar_aluno(), painel_adm(), remover_usuario(), AlunoDAO, Quantos alunos a academia tem, sem filtro de busca. O card do topo do painel é…, Uma página de alunos já cadastrados, recortada e filtrada pelo banco. O painel…, Aluno Management Table (+9 more)

### Community 133 - "test_conversao_home.py"
Cohesion: 0.19
Nodes (14): _body_tag(), _html(), parametrize, Conversão na home: perguntas frequentes, CTA fixo no celular e página de…, test_admin_logado_nao_ve_o_cta_fixo(), test_aluno_logado_nao_ve_o_cta_fixo(), test_cta_fixo_fica_so_na_home(), test_cta_fixo_sem_whatsapp_so_tem_o_cadastro() (+6 more)

### Community 134 - "test_financeiro_admin_painel.py"
Cohesion: 0.33
Nodes (5): test_busca_financeira_trata_curingas_como_texto(), test_painel_financeiro_busca_por_nome_do_aluno(), test_painel_financeiro_exige_admin(), test_painel_financeiro_filtra_por_status(), test_painel_financeiro_mostra_totais_do_backend()

### Community 135 - "prontidao.py"
Cohesion: 0.43
Nodes (6): banco_responde(), _consultar_banco(), Verificação de prontidão (/health/pronto): o banco e o Redis respondem agora?…, None quando o limite de requisições não usa Redis (memory:// em…, redis_responde(), verificar()

### Community 136 - "_valor_em_reais"
Cohesion: 0.50
Nodes (4): _ler_promocao(), 80', '80.5', '80,50' ou '1.234,56' -> Decimal. None se vazio; ValueError se…, Preço promocional e período: `(campos, None)` ou `(None, erro)`. Os três campos…, _valor_em_reais()

### Community 137 - "ativar_acesso"
Cohesion: 0.50
Nodes (4): ativar_acesso(), Transforma um cadastro feito no balcão na conta do próprio aluno. Quem chega…, mascarar_email(), Mostra o bastante do e-mail para o dono se reconhecer, sem revelá-lo a…

### Community 140 - "backup.sh"
Cohesion: 1.00
Nodes (3): registrar(), reter(), backup.sh script

### Community 141 - "vercel.json"
Cohesion: 0.50
Nodes (3): gru1, regions, $schema

### Community 143 - "Biblioteca no Figma"
Cohesion: 0.50
Nodes (3): Biblioteca no Figma, Falta (ordem de retomada), Limites do plano Starter que moldaram o arquivo

### Community 145 - "conteudo_home.py"
Cohesion: 0.50
Nodes (3): faq_estruturado(), Textos editáveis da página inicial: perguntas frequentes e prazos de…, JSON-LD FAQPage com exatamente as perguntas mostradas na página.

### Community 146 - "api_mp"
Cohesion: 0.50
Nodes (4): api_mp(), oauth_env(), fixture, Substitui POST /oauth/token. `respostas` é consumida em ordem; a última se…

### Community 150 - "adm_bp.py"
Cohesion: 0.17
Nodes (20): aprovar_comprovante_manual(), _chave_lote(), cobrar_inadimplentes(), cobrar_mensalidade(), _data_do_form(), enviar_aviso(), _esta_inadimplente(), _paragrafos_cobranca() (+12 more)

### Community 151 - "_enviar_em_segundo_plano"
Cohesion: 0.50
Nodes (4): _em_segundo_plano(), _enviar_em_segundo_plano(), E-mail COM token (recuperação, confirmação): não pode ir para a `fila_email`. A…, Roda `tarefa` fora da requisição, para o tempo de resposta não revelar nada. Em…

### Community 153 - "test_limites_pagamento.py"
Cohesion: 0.15
Nodes (15): consultar_mp(), fixture, parametrize, Limites de pagamento por conta, com o provedor inteiramente simulado., _sessao_aluno(), test_admin_limite_por_usuario_persiste_entre_sessoes(), test_alunos_no_mesmo_ip_tem_limites_separados(), test_anonimos_limitados_por_ip_sem_consultar_provedor() (+7 more)

## Knowledge Gaps
- **168 isolated node(s):** `icone_senha`, `input_senha`, `modal`, `campoDuracao`, `campoPreco` (+163 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PagamentoDAO` connect `PagamentoDAO` to `criar_pagamento`, `criar_aluno`, `test_pagamento_recusado.py`, `test_mudanca_plano.py`, `pix_bp.py`, `AlunoDAO`, `test_financeiro_admin_painel.py`, `test_regressao_auditoria.py`, `logar_como_admin`, `checkout_bp.py`, `adm_bp.py`, `config.py`, `test_auditoria_seguranca.py`, `MatriculaDAO`, `PagamentoEvento`, `test_pix_rotas.py`, `test_seguranca.py`, `Aluno`, `.buscar_por_id`, `test_checkout_rotas.py`, `test_plano_arquivo_promocao.py`, `.contratar_plano`, `detalhes_usuario`, `formatacao.py`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Why does `logar_como_admin()` connect `logar_como_admin` to `criar_pagamento`, `criar_aluno`, `AlunoDAO`, `test_conversao_home.py`, `test_financeiro_admin_painel.py`, `test_mudanca_plano.py`, `test_regressao_auditoria.py`, `test_analytics.py`, `test_home_planos.py`, `test_mercado_pago_oauth.py`, `test_limites_pagamento.py`, `MatriculaDAO`, `Academia`, `test_pix_rotas.py`, `test_planilha_economica.py`, `ProfessorDAO`, `test_seguranca.py`, `PagamentoDAO`, `test_google_login.py`, `Aluno`, `.buscar_por_id`, `conftest.py`, `test_sessao_revogada.py`, `test_seo.py`, `test_layouts.py`, `Plano`, `test_plano_arquivo_promocao.py`, `test_perfil_e_foto.py`, `PlanoDAO`, `impressao_credencial`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Why does `criar_aluno()` connect `criar_aluno` to `criar_pagamento`, `AlunoDAO`, `test_conversao_home.py`, `test_financeiro_admin_painel.py`, `test_mudanca_plano.py`, `test_regressao_auditoria.py`, `test_analytics.py`, `test_home_planos.py`, `logar_como_admin`, `test_mercado_pago_oauth.py`, `test_limites_pagamento.py`, `test_auditoria_seguranca.py`, `MatriculaDAO`, `test_limites_requisicao.py`, `test_pix_rotas.py`, `test_planilha_economica.py`, `test_seguranca.py`, `PagamentoDAO`, `test_google_login.py`, `conftest.py`, `test_paginas_erro.py`, `test_seo.py`, `test_layouts.py`, `Plano`, `test_plano_arquivo_promocao.py`, `test_perfil_e_foto.py`, `.contratar_plano`, `_tem_limite`, `formatacao.py`, `PlanoDAO`, `impressao_credencial`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Are the 143 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 143 INFERRED edges - model-reasoned connections that need verification._
- **Are the 164 inferred relationships involving `logar_como_admin()` (e.g. with `test_admin_salva_atualiza_e_limpa_contatos()` and `test_csrf_configuracoes()`) actually correct?**
  _`logar_como_admin()` has 164 INFERRED edges - model-reasoned connections that need verification._
- **Are the 162 inferred relationships involving `criar_aluno()` (e.g. with `test_admin_lanca_mensalidade_paga_no_cartao()` and `test_conversao_igual_para_cadastro_novo_e_cpf_ou_email_existentes()`) actually correct?**
  _`criar_aluno()` has 162 INFERRED edges - model-reasoned connections that need verification._
- **Are the 159 inferred relationships involving `criar_pagamento()` (e.g. with `_so_com_checkout()` and `test_admin_muda_o_status_sem_perder_a_forma_do_mercado_pago()`) actually correct?**
  _`criar_pagamento()` has 159 INFERRED edges - model-reasoned connections that need verification._