# Graph Report - SistemaEXTREMETEAM  (2026-11-04)

## Corpus Check
- 233 files · ~309,970 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3107 nodes · 7193 edges · 173 communities (159 shown, 14 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 1259 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3d5f0e6f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Aluno
- Componentes
- test_admin_segundo_fator.py
- planilha_bp.py
- test_seo.py
- adm_bp.py
- turma_bp.py
- logar_como_admin
- planos.py
- usuario_bp.py
- test_admin_mercado_pago.py
- financeiro.html — painel financeiro
- index.html (home pública)
- PagamentoDAO
- criar_aluno
- fase3b.js
- test_auditoria_seguranca.py
- planilha.py
- fila_email.py
- csrf_field.html
- armazenamento.py
- test_google_login.py
- pix_bp.py
- servidor.py
- .contratar_plano
- test_turnstile.py
- mercado_pago_conta.py
- test_seguranca.py
- test_pix_rotas.py
- EmailPendente
- planilha_excel.py
- checkout_bp.py
- test_mudanca_plano.py
- ui.html
- test_mercado_pago_servico.py
- test_limites_requisicao.py
- Pagina
- seo.py
- test_plano_arquivo_promocao.py
- convites.py
- varredura.mjs
- test_pagamento_recusado.py
- MercadoPagoConexao
- avatar
- mercado_pago_oauth_bp.py
- test_observabilidade.py
- test_analytics.py
- PlanoDAO
- gmail_conta.py
- criar_pagamento
- test_planilha_economica.py
- analytics.js
- package.json
- test_home_planos.py
- Strix Cloud (managed, no local infra)
- autorizacao.py
- deslize.html
- MercadoPagoIndisponivel
- test_prontidao.py
- pix.js
- test_arranque_seguranca.py
- dt_aluno.html — ficha do aluno (admin)
- test_keep_alive.py
- pagamento.js
- test_sessao_revogada.py
- Relatório de segurança — Sistema Extreme Team
- Professor
- componentes.js
- prontidao.py
- botao_ocupado.test.cjs
- test_backup_scripts.py
- gunicorn.conf.py
- config.py
- analytics.test.cjs
- test_conversao_home.py
- _parece_busca_por_cpf
- test_email_componentes.py
- test_layouts.py
- test_migracao_checkout.py
- Academia
- checkout_abertura.test.cjs
- pagamento_polling.test.cjs
- test_publicas_redesign.py
- env.py
- test_formatos_de_imagem.py
- _Resposta
- academia_bp.py
- shot.mjs
- c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py
- cena.tsx
- test_comprovante_sem_metadados.py
- 896e70afc9c5_adiciona_foto_e_graduacao_do_aluno_.py
- test_migracao_cadastro_administrativo.py
- google_login.py
- a1f0c3e75b92_schema_inicial.py
- d9e2f6a14c80_contatos_academia_perfis_professores.py
- e4b7c2a91d35_cadastro_administrativo_e_convite_de_acesso.py
- vercel.json
- mercado_pago.py
- backup.sh
- capturar_emails
- gerar_imagem_og.py
- _preparar_state
- salvar_foto_perfil
- agendar.sh
- restaurar.sh
- Contrato do redesign — SistemaEXTREMETEAM
- Plano
- cinema.test.cjs
- compilerOptions
- pgUsuario.html (área do aluno)
- penetration-testing-with-strix/SKILL.md
- test_cinema.py
- SistemaEXTREMETEAM
- test_paginas_erro.py
- _ajustar
- .remover
- seo_bp.py
- .checkout_ainda_valido
- cinema.py
- Skills Disponíveis
- .listar_por_aluno
- cinema.js
- Etapa 1 — migrar páginas para os layouts (SEM mudar o visual)
- Etapas 4 a 6 — aluno, admin, professor (aplicar os componentes nas páginas)
- emblema.py
- home
- Etapa 2 — biblioteca de componentes
- verificar_email_cadastro
- exempt
- formatacao.py
- Etapa 3 — home com os planos + termos
- test_fontes_locais.py
- Biblioteca no Figma
- CLAUDE.md
- URLPublicaInvalida
- test_armazenamento_storage.py
- test_logs_sem_dado_pessoal.py
- auth.test.cjs
- requirements.txt (dependências de produção)
- .buscar_por_id
- ci-security-scanning-with-strix/SKILL.md
- _FakePaymentResource
- Find security vulnerabilities in code
- test_mercado_pago_oauth.py
- Security-test an API
- Application security testing
- imagens.d.ts
- Fix Strix findings and verify
- Test against the OWASP Top 10
- Pentest a web application
- admin_requerido
- test_email_gmail.py
- .contar_cadastrados
- limites_pagamento.py

## God Nodes (most connected - your core abstractions)
1. `PagamentoDAO` - 235 edges
2. `logar_como_admin()` - 171 edges
3. `criar_aluno()` - 170 edges
4. `criar_pagamento()` - 170 edges
5. `logar_como_aluno()` - 137 edges
6. `AlunoDAO` - 80 edges
7. `PlanoDAO` - 62 edges
8. `Aluno` - 51 edges
9. `MercadoPagoIndisponivel` - 45 edges
10. `Professor` - 39 edges

## Surprising Connections (you probably didn't know these)
- `Vitrine de planos da home (secao_planos com vitrine_planos)` --references--> `cartao_do_plano()`  [INFERRED]
  templates/index.html → servicos/planos.py
- `contar_falhados()` --uses--> `EmailPendente`  [INFERRED]
  servicos/fila_email.py → modelos/email_pendente.py
- `test_refresh_token_fica_cifrado_no_banco()` --uses--> `GmailConexao`  [INFERRED]
  tests/test_email_gmail.py → modelos/gmail_conexao.py
- `Envio de comprovante manual (et-upload, até 4 MB)` --references--> `salvar_comprovante_manual()`  [EXTRACTED]
  templates/pagamento.html → servicos/armazenamento.py
- `Contratação e troca de plano (contratar, renovar, agendar_mudanca)` --references--> `cartao_do_plano()`  [EXTRACTED]
  templates/pgUsuario.html → servicos/planos.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Redesign multiagente em etapas (contrato, enunciados e vitrine)** — redesign_contrato, tools_redesign_tarefa_admin, tools_redesign_tarefa_etapa1_layouts, tools_redesign_tarefa_etapa2_componentes, tools_redesign_tarefa_etapa3_home_termos, tools_redesign_tarefa_etapas4a6, tools_redesign_vitrine_vitrine [EXTRACTED 1.00]
- **Modais nativos <dialog> com .et-dialogo** — templates_components_comprovante_modal, templates_components_confirm_modal, templates_components_pix_dialog, templates_components_presenca_modal, templates_components_turma_detalhe_modal [EXTRACTED 1.00]
- **Ciclo de vida do plano (admin cadastra, destaca e arquiva; home exibe; aluno contrata e renova)** — templates_pgadm_form_plano, templates_pgadm_ficha_plano, templates_index_vitrine_planos, templates_pgusuario_contratacao_plano, templates_pgusuario_regra_renovacao_plano [INFERRED 0.85]
- **Fluxo de pagamento da mensalidade na interface (Pix, comprovante, linha do tempo, situação do plano)** — templates_components_mensalidade_acao_acao, templates_components_pix_dialog, templates_components_comprovante_modal, templates_components_linha_tempo_linha_tempo_pagamento, templates_components_plano_situacao_cartao [INFERRED 0.85]
- **Envio de e-mails da academia (layout, fila e Gmail)** — templates_email_base, templates_email_componentes, templates_admin_avisos_fila_envio, templates_admin_avisos_cobranca_email, templates_admin_academia_conexao_gmail [INFERRED 0.85]
- **Exclusão só sem vínculos (plano em uso é arquivado; professor com turmas e turma com matrículas ou presenças não saem)** — templates_pgadm_ficha_plano, templates_turmas_professores, templates_turmas_turmas_academia [INFERRED 0.85]
- **Fluxo de convite e ativação de acesso do aluno** — templates_admin_aluno_novo_matricula_sem_acesso, templates_dt_aluno_convite_acesso, templates_email_base, templates_ativar_acesso [INFERRED 0.85]
- **Fluxo de presença (professor abre a turma, faz a chamada, aluno confirma a frequência)** — templates_pgprofessor, templates_turma_chamada_presenca, templates_pgusuario_turmas_presencas [INFERRED 0.85]
- **Fluxo de pagamento online pelo Mercado Pago** — templates_admin_academia_conexao_mercado_pago, templates_checkout_continuar, templates_checkout_retorno, templates_admin_academia_webhook_mercado_pago, templates_dt_aluno_sincronizacao_mercado_pago, templates_comprovante [INFERRED 0.85]
- **Cabeçalhos da área logada com o mesmo bloco site-brand** — templates_components_admin_nav, templates_components_cabecalho_professor, templates_components_detail_back_header [INFERRED 0.95]

## Communities (173 total, 14 thin omitted)

### Community 0 - "Aluno"
Cohesion: 0.08
Nodes (21): Matrícula feita no balcão: sem login, sem senha e sem convite de acesso. Nasce…, Aluno, Se existe uma conta de acesso, e não se o aluno está em dia ou matriculado.…, Convite de acesso já enviado e ainda não usado (a validade é checada na rota)., Chave do estado da CONTA - nunca da situação financeira nem da matrícula., data_iso(), A data em AAAA-MM-DD, o formato do <input type="date">, ou '' se não for uma…, test_cadastro_publico_recusa_confirmacao_diferente() (+13 more)

### Community 1 - "Componentes"
Cohesion: 0.05
Nodes (36): Altura de controle, Avisos flutuantes, Botões — `.et-botao` + variante (+ tamanho), Cartões e contêineres, Componentes, Contêiner e estrutura, Cores, Dados (+28 more)

### Community 2 - "test_admin_segundo_fator.py"
Cohesion: 0.20
Nodes (20): _codigo_agora(), _codigo_errado(), _destino(), _entrar_com_senha(), fixture, parametrize, Segundo fator do administrador (SEC-30). Com ADMIN_TOTP_SECRET definida, a…, segundo_fator() (+12 more)

### Community 3 - "planilha_bp.py"
Cohesion: 0.21
Nodes (19): alterar_despesa(), _ano_e_mes(), _ano_valido(), baixar_excel(), excluir_despesa(), _formulario_de(), lancar_despesa(), _ler_despesa() (+11 more)

### Community 4 - "test_seo.py"
Cohesion: 0.10
Nodes (26): _head(), _json_ld(), parametrize, SEO técnico: robots.txt, sitemap, títulos, meta tags, noindex e JSON-LD da home., Nenhum campo do JSON-LD pode sair nulo, vazio ou só com espaços., _robots(), _sem_vazios(), test_area_do_admin_sai_do_indice() (+18 more)

### Community 5 - "adm_bp.py"
Cohesion: 0.07
Nodes (60): _aluno_do_cpf_ou_painel(), aprovar_aluno(), aprovar_comprovante_manual(), arquivar_plano(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_aluno(), cadastrar_pagamento() (+52 more)

### Community 6 - "turma_bp.py"
Cohesion: 0.10
Nodes (28): _acesso_permitido(), cadastrar_turma(), desmatricular_aluno(), detalhe_turma(), matricular_aluno(), limit, registrar_presenca(), remover_turma() (+20 more)

### Community 7 - "logar_como_admin"
Cohesion: 0.14
Nodes (49): _convidar_cadastro_existente(), Cadastro administrativo que alguém tentou recriar pelo formulário público. Em…, AlunoDAO, logar_como_admin(), _matricular(), parametrize, Cadastro de aluno pela administração, ativação de acesso e confirmação de…, test_admin_lanca_e_baixa_mensalidade_de_aluno_sem_acesso() (+41 more)

### Community 8 - "planos.py"
Cohesion: 0.06
Nodes (42): cadeia_paga(), cartao_do_plano(), cobranca_a_pagar(), cobranca_em_decisao(), cobranca_pendente(), duracao_dias(), _duracao_por_extenso(), esta_inadimplente() (+34 more)

### Community 9 - "usuario_bp.py"
Cohesion: 0.11
Nodes (39): _acesso_permitido_pagamento(), alterar_senha_perfil(), _aluno_da_sessao(), _aluno_por_token(), atualizar_dados_perfil(), cadastro_obrigado(), cancelar_mudanca_plano(), _chave_ip_e_identificador() (+31 more)

### Community 10 - "test_admin_mercado_pago.py"
Cohesion: 0.18
Nodes (14): _aprovado_no_checkout(), Painel do admin com mensalidades do Mercado Pago: formas de pagamento,…, Cartão/boleto: a preferência existe, o webhook ainda não trouxe o payment_id., _so_com_checkout(), test_admin_muda_o_status_sem_perder_a_forma_do_mercado_pago(), test_admin_nao_grava_forma_inventada(), test_aprovar_comprovante_recusa_forma_inventada(), test_ficha_mantem_no_select_a_forma_confirmada_pelo_mercado_pago() (+6 more)

### Community 11 - "financeiro.html — painel financeiro"
Cohesion: 0.13
Nodes (14): ajustar(), aplicar(), Tom da mensagem por status do pagamento, badge(), Situações da mensalidade (pendente a reembolsado), email/base.html — layout dos e-mails, email/componentes.html — macros de e-mail, badge() — etiqueta de situação no e-mail (+6 more)

### Community 12 - "index.html (home pública)"
Cohesion: 0.13
Nodes (12): faq_estruturado(), Textos editáveis da página inicial: perguntas frequentes e prazos de…, JSON-LD FAQPage com exatamente as perguntas mostradas na página., cabecalho, entrarFixo, icone_senha, input_senha, modal (+4 more)

### Community 13 - "PagamentoDAO"
Cohesion: 0.08
Nodes (32): mensalidade_destaque(), PagamentoDAO, Status como o painel deve LER, com o vencimento aplicado na própria consulta. A…, Carrega aluno e plano junto das mensalidades. O template do painel lê…, Lista completa (sem paginar). Mantida para relatórios e testes., Uma página de mensalidades, recortada pelo banco (LIMIT/OFFSET). O painel…, Escolhe a mensalidade mais relevante para o card 'Minha mensalidade': a mais…, True se a cobrança Pix já gerada para este pagamento ainda pode ser… (+24 more)

### Community 14 - "criar_aluno"
Cohesion: 0.04
Nodes (61): Totais do painel financeiro - sempre calculados no backend a partir do banco,…, Uma página de alunos já cadastrados, recortada e filtrada pelo banco. O painel…, criar_aluno(), test_aluno_existente_continua_entrando_normalmente(), test_area_do_aluno_renderiza_telas_independentes_do_menu(), test_plano_atual_continua_disponivel_para_gerar_cobranca(), test_aluno_ve_o_proprio_perfil(), _contar_selects_em_alunos() (+53 more)

### Community 15 - "fase3b.js"
Cohesion: 0.06
Nodes (47): avisos, bind(), caixas, campos, col(), D(), estados, faixa (+39 more)

### Community 16 - "test_auditoria_seguranca.py"
Cohesion: 0.07
Nodes (42): _agora_mercado_pago(), _assinar(), logar_como_professor(), _pagamento_mp(), _preparar_para_conciliacao(), fixture, parametrize, Auditoria de segurança: sondas escritas para TENTAR quebrar as regras. Nenhum… (+34 more)

### Community 17 - "planilha.py"
Cohesion: 0.14
Nodes (15): anos_disponiveis(), Categoria, data_da_entrada(), _decimal(), _entradas(), entradas_detalhadas(), limites_do_ano(), Mes (+7 more)

### Community 18 - "fila_email.py"
Cohesion: 0.11
Nodes (24): espera_da_proxima_tentativa(), contar_falhados(), contar_pendentes(), disparar(), enfileirar(), enfileirar_transacional(), _entregar(), _laco() (+16 more)

### Community 19 - "csrf_field.html"
Cohesion: 0.13
Nodes (20): Contato e localização da academia, ativar_acesso.html — ativar acesso pelo convite, cadastro.html — criar conta, cadastro_obrigado.html — cadastro recebido, Cadastro com PRG e resposta única, Aceite do Termo de Responsabilidade, Modal de login da home (#meuModal, POST /login), layouts/publico.html — layout das telas públicas (+12 more)

### Community 20 - "armazenamento.py"
Cohesion: 0.13
Nodes (23): enviar_comprovante_manual_aluno(), _exif_so_com_orientacao(), _gravar(), _jpeg_sem_metadados(), _nome_valido(), _orientacao(), _pasta(), _png_sem_metadados() (+15 more)

### Community 21 - "test_google_login.py"
Cohesion: 0.08
Nodes (24): Esquece a conta conectada. Devolve True se havia uma., remover_conexao(), fixture, Registra as chamadas e devolve as respostas configuradas por método., storage(), _StorageFalso, test_envia_pelo_gmail_com_o_refresh_token_da_conexao(), cliente_google() (+16 more)

### Community 22 - "pix_bp.py"
Cohesion: 0.06
Nodes (50): _chave_entrega_webhook(), criar_pix_mensalidade(), _data_da_aprovacao(), _forma_pagamento_confirmada(), _instante_utc(), _iso_utc(), _liberar_entrega_webhook(), _mensalidade_da_referencia() (+42 more)

### Community 23 - "servidor.py"
Cohesion: 0.09
Nodes (27): after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, context_processor, errorhandler, Fila de e-mails no banco. Aviso e cobrança coletivos saíam um a um dentro da…, Registra a sessão como encerrada: cópias antigas do cookie deixam de valer.…, revogar_sessao_atual() (+19 more)

### Community 24 - ".contratar_plano"
Cohesion: 0.07
Nodes (19): Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.…, O que aconteceu numa tentativa de contratar/renovar/trocar de plano., Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda. O…, Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, Com uma troca já agendada, só dois planos fazem sentido num pedido de…, A cobrança do período seguinte tem de nascer no plano que o aluno agendou.…, `pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -… (+11 more)

### Community 25 - "test_turnstile.py"
Cohesion: 0.09
Nodes (24): ativo_nesta_resposta(), _chave_site(), configurado(), hostnames_esperados(), Cloudflare Turnstile no cadastro público (SEC-36). O cadastro manda e-mail para…, Sites onde o widget pode ter sido resolvido, como a Cloudflare os informa., Chamada no arranque. `exigir` é verdadeiro em produção (endereço público em…, Para o template: a chave pública do widget, ou vazio quando o Turnstile está… (+16 more)

### Community 26 - "mercado_pago_conta.py"
Cohesion: 0.10
Nodes (39): ConfiguracaoInvalida, access_token_vigente(), _agora(), ambiente_da_conexao(), _cifrar(), _client_id(), _client_secret(), ConexaoIlegivel (+31 more)

### Community 27 - "test_seguranca.py"
Cohesion: 0.07
Nodes (24): test_upload_de_arquivo_disfarcado_e_recusado(), _cadastro_publico(), _imagem_jpeg(), _mensagem_da_resposta(), O `login` de um aluno pode ser o e-mail de outro; quem entra é decidido pela…, O ramo "par existe" não pode pagar a ida ao provedor dentro da requisição., Cadastro novo, CPF existente e e-mail existente respondem com a MESMA tela., Quem ainda controla a caixa antiga não pode assumir a conta depois da troca. (+16 more)

### Community 28 - "test_pix_rotas.py"
Cohesion: 0.19
Nodes (21): _agora_mercado_pago(), _assinar(), _resposta_consulta(), _resposta_criacao(), test_admin_tambem_pode_gerar_pix(), test_aluno_gera_pix_da_propria_mensalidade(), test_aluno_nao_acessa_mensalidade_de_outro_aluno(), test_falha_de_indisponibilidade_do_mp_retorna_503() (+13 more)

### Community 29 - "EmailPendente"
Cohesion: 0.11
Nodes (15): EmailPendente, parametrize, Agendamento sem rede, threads reais ou esperas de relógio., test_nao_inicia_em_testes(), test_retomada_de_item_persistido_e_retentativa_sem_painel(), _enfileirar_em_transacao_propria(), postgres_fila(), fixture (+7 more)

### Community 30 - "planilha_excel.py"
Cohesion: 0.30
Nodes (13): Nome legível da forma de pagamento. Antes as telas usavam `|replace('_','…, rotulo_forma_pagamento(), _aba_categorias(), _aba_entradas(), _aba_resumo(), _aba_saidas(), _cabecalho(), _escrever() (+5 more)

### Community 31 - "checkout_bp.py"
Cohesion: 0.11
Nodes (28): abrir_checkout(), _acesso_permitido(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), limitar_consulta_pagamento, limitar_criacao_pagamento, route (+20 more)

### Community 32 - "test_mudanca_plano.py"
Cohesion: 0.13
Nodes (30): detalhes_usuario(), pagina_perfil(), _turma_do_formulario(), Persistência dos pedidos de troca de plano agendados para a próxima renovação., Aplica um pedido agendado cujo período de origem já terminou sem renovação.…, SolicitacaoPlanoDAO, _agendar(), _pagar() (+22 more)

### Community 33 - "ui.html"
Cohesion: 0.10
Nodes (28): campoDuracao, campoPreco, formularioPlano, cartao_plano(), secao_planos(), estado_vazio(), interruptor(), metrica() (+20 more)

### Community 34 - "test_mercado_pago_servico.py"
Cohesion: 0.11
Nodes (29): Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, validar_assinatura_webhook(), Hipótese: uma notificação capturada ontem pode ser reenviada hoje., `ts=nan` fazia a comparação da janela dar False e passava pela checagem de…, test_webhook_recusa_assinatura_antiga(), test_webhook_recusa_ts_nao_numerico_finito(), base_url(), _criar_preferencia() (+21 more)

### Community 35 - "test_limites_requisicao.py"
Cohesion: 0.12
Nodes (28): consultar_mp(), _estourar(), fixture, parametrize, Limites de requisição da rodada de 04/10/2026 (SEC-10 a SEC-17 e SEC-19). Cada…, Trocar de rede ou abrir outra sessão não devolve a cota de e-mails em massa., Faz `limite` requisições sem nenhum 429 e devolve a seguinte., Alunos no mesmo Wi-Fi não dividem o teto padrão, nem com o visitante anônimo. (+20 more)

### Community 36 - "Pagina"
Cohesion: 0.14
Nodes (5): Pagina, Uma fatia de resultados já recortada pelo banco, com o que a navegação precisa., Uma página existe mesmo quando está vazia. Sem isto, `__len__` fazia `{% if…, `__len__` fazia `{% if pagina %}` ser falso numa página sem itens, escondendo…, test_pagina_vazia_ainda_mostra_a_navegacao()

### Community 37 - "seo.py"
Cohesion: 0.23
Nodes (14): conteudo_robots(), conteudo_sitemap(), dados_estruturados_academia(), _dia(), _dias_da_linha(), _hora(), horarios_estruturados(), pagina_indexavel() (+6 more)

### Community 38 - "test_plano_arquivo_promocao.py"
Cohesion: 0.13
Nodes (26): Tira o plano de venda. Devolve `(plano, pedidos_cancelados)`, ou None. Pedidos…, Pagamento, _para_decimal(), Status a exibir, com o vencimento já aplicado. Uma cobrança `pendente` cujo…, _pagar(), _plano(), _promocao(), Plano fora de venda (arquivar/reativar/excluir), edição e promoção com período.… (+18 more)

### Community 39 - "convites.py"
Cohesion: 0.13
Nodes (22): solicitar_troca_email(), aluno_do_token(), ConviteIndisponivel, descartar(), enviar(), gerar_token(), _hash(), RuntimeError (+14 more)

### Community 40 - "varredura.mjs"
Cohesion: 0.11
Nodes (23): aberto(), ACESSO, auditar(), { chromium }, CONF, confirmacoes(), crc, CREDS (+15 more)

### Community 41 - "test_pagamento_recusado.py"
Cohesion: 0.28
Nodes (20): _assinar(), _data_mp(), _eventos(), _mockar_mp(), _pagamento_mp(), _pix_criado(), Mensalidade recusada: a próxima tentativa do aluno a reabre, e a recusa antiga…, Mensalidade cujo cartão acabou de ser recusado no Checkout Pro. (+12 more)

### Community 42 - "MercadoPagoConexao"
Cohesion: 0.16
Nodes (12): MercadoPagoConexao, Conta do Mercado Pago que a academia autorizou por OAuth. Uma linha só (a…, postgres_mp(), fixture, Renovação do token OAuth com trava de linha real, opcional na suíte que usa…, _Resposta, test_dois_processos_perto_do_vencimento_gastam_o_refresh_token_uma_vez(), test_desconectar_exige_token_csrf() (+4 more)

### Community 43 - "avatar"
Cohesion: 0.12
Nodes (16): avatar(), breadcrumb(), Biblioteca de componentes .et-* (componentes.css), Seção Nossa equipe (professores_publicos), Nosso método: criar conta, aguardar aprovação, contratar plano e treinar, Cadastros pendentes (aprovar ou recusar aluno), Tabela de alunos paginada com busca no servidor, pgProfessor.html (minhas turmas do professor) (+8 more)

### Community 44 - "mercado_pago_oauth_bp.py"
Cohesion: 0.38
Nodes (9): _autorizacao_valida(), callback(), conectar(), desconectar(), limit, route, O state devolvido é o que ESTA sessão emitiu, há pouco tempo?, Só monta o state/PKCE na sessão e manda o administrador ao Mercado Pago. É um… (+1 more)

### Community 45 - "test_observabilidade.py"
Cohesion: 0.14
Nodes (20): before_breadcrumb(), before_send(), iniciar_sentry(), _limpar(), mascarar(), Rastreamento de erros opcional com Sentry. Sem `SENTRY_DSN`, nada é importado…, _evento(), fixture (+12 more)

### Community 46 - "test_analytics.py"
Cohesion: 0.14
Nodes (20): _carrega_analytics(), com_analytics(), _csp_com_google(), _evento(), fixture, parametrize, GA4 opcional (servicos/analytics.py): nada sem ANALYTICS_ID, nunca em área…, sem_analytics_por_padrao() (+12 more)

### Community 47 - "PlanoDAO"
Cohesion: 0.17
Nodes (14): _plano_do_formulario(), PlanoDAO, Os planos à venda: home, perfil do aluno e formulários de contratação., Grava a edição do admin. Vale para as cobranças criadas daqui em diante: as…, parametrize, test_admin_cria_promocao(), test_admin_edita_nome_preco_e_duracao(), test_arquivar_exige_admin() (+6 more)

### Community 48 - "gmail_conta.py"
Cohesion: 0.27
Nodes (15): GmailConexao, _access_token(), _cifrar(), _client_id(), _client_secret(), _decifrar(), enviar(), estado() (+7 more)

### Community 49 - "criar_pagamento"
Cohesion: 0.06
Nodes (73): criar_pagamento(), logar_como_aluno(), Hipótese: forjar ?status=approved na volta do MP quita a mensalidade., Hipótese: cada clique cria uma cobrança nova no Mercado Pago., Hipótese: dá para injetar o valor pelo corpo do POST., Verifica a trava antes da emissão e o reaproveitamento na próxima chamada.…, test_dois_cliques_reaproveitam_a_mesma_preferencia(), test_pix_exige_trava_e_reutiliza_a_cobranca() (+65 more)

### Community 50 - "test_planilha_economica.py"
Cohesion: 0.13
Nodes (23): Despesa, Saídas de caixa lançadas pelo admin (aluguel, luz, salários...). As entradas da…, criar_despesa(), _form(), fixture, parametrize, Planilha econômica: fluxo de caixa, lançamento de despesas e download em Excel., test_ano_fora_do_intervalo_volta_ao_atual() (+15 more)

### Community 51 - "analytics.js"
Cohesion: 0.14
Nodes (12): analytics_ativo(), id_analytics(), marcar_conversao_cadastro(), Google Analytics 4 opcional, só em página pública e só com consentimento. Sem…, Chamada no arranque: um ID malformado derruba a subida, como as demais…, Esta resposta pode carregar o GA4? Visitante, página pública indexável ou…, validar_configuracao(), apagarCookiesGa() (+4 more)

### Community 52 - "package.json"
Cohesion: 0.05
Nodes (38): dependencies, maath, react, react-dom, @react-three/drei, @react-three/fiber, scrolly-video, three (+30 more)

### Community 53 - "test_home_planos.py"
Cohesion: 0.18
Nodes (17): Marca o plano em destaque da página inicial, desmarcando qualquer outro.…, Inclusive os arquivados: serve a quem olha o histórico (filtro do financeiro)., Planos da página inicial, prontos para `components/cartao_plano.html`. O preço…, vitrine_planos(), _plano(), _quatro_planos(), Planos na página inicial: cálculo (servicos/planos.vitrine_planos), destaque…, test_admin_destaca_e_tira_o_destaque() (+9 more)

### Community 54 - "Strix Cloud (managed, no local infra)"
Cohesion: 0.12
Nodes (15): 0. Credits & top-ups, 1. Register the target as an asset, 2. Launch a scan, 3. Wait for completion, 4. Read findings, 5. Export & report, 6. PR reviews, 7. Continuous testing (schedules & webhooks) (+7 more)

### Community 55 - "autorizacao.py"
Cohesion: 0.21
Nodes (15): _acesso_permitido(), aluno_autorizado(), aluno_requerido(), _credencial_confere(), encerrar_sessao(), professor_autorizado(), Autorização das rotas protegidas. A sessão diz quem *afirmou* ser quem; quem…, A sessão foi emitida para a credencial que vale AGORA? Uma sessão sem carimbo é… (+7 more)

### Community 56 - "deslize.html"
Cohesion: 0.22
Nodes (8): Content Security Policy (csp_nonce), window.deslizarTela(), marcar(), listener de pagereveal, SECOES (ordem das seções do menu), sentidoEntre(), View Transitions API (@view-transition), anel()

### Community 57 - "MercadoPagoIndisponivel"
Cohesion: 0.14
Nodes (20): buscar_pagamento(), buscar_pagamentos_por_referencia(), cancelar_pagamento(), MercadoPagoIndisponivel, Exception, Consulta o pagamento diretamente na API do Mercado Pago - fonte de verdade de…, Lista os pagamentos que o Mercado Pago associa a uma external_reference. Usada…, Cancela uma cobranca Pix pendente no Mercado Pago. Best-effort: nunca lanca. (+12 more)

### Community 58 - "test_prontidao.py"
Cohesion: 0.14
Nodes (5): banco_fora(), fixture, /health/pronto: 503 quando banco ou Redis caem, sem expor detalhe nem criar…, Cada chamada consulta banco e Redis: 60 por minuto bastam ao monitor externo., test_pronto_tem_limite_por_ip()

### Community 59 - "pix.js"
Cohesion: 0.33
Nodes (14): abrirPix(), alvoDoRotulo(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), liberarBotao(), limparConteudoAnterior() (+6 more)

### Community 60 - "test_arranque_seguranca.py"
Cohesion: 0.14
Nodes (25): _env_arranque(), _hosts_e_proxy(), parametrize, Validações feitas por servidor.py no arranque (COOKIE_SECURE, TRUSTED_HOSTS,…, Desenvolvimento local sem HTTPS (sem Caddy) não pode ficar travado., `python -m servicos.credenciais`: o hash sai entre aspas simples. O hash do…, _rodar(), test_arranque_aceita_redis_do_upstash_com_espaco_em_volta() (+17 more)

### Community 61 - "dt_aluno.html — ficha do aluno (admin)"
Cohesion: 0.11
Nodes (25): admin_academia.html — configurações da academia, Abas com memória (data-tabs-lembrar), Conexão OAuth do Gmail para envio de avisos, Conexão OAuth do Mercado Pago (PKCE), Webhook de pagamentos do Mercado Pago (MERCADO_PAGO_WEBHOOK_SECRET), admin_aluno_novo.html — matricular aluno, Matrícula sem acesso ao sistema, admin_avisos.html — avisos e cobranças por e-mail (+17 more)

### Community 62 - "test_keep_alive.py"
Cohesion: 0.16
Nodes (7): ambiente_limpo(), fixture, parametrize, Garante que o keep-alive fica desligado por padrão e só pinga a própria origem., test_intervalo_fica_dentro_da_faixa(), test_nao_liga_com_valor_negativo(), test_ping_so_considera_200_como_sucesso()

### Community 63 - "pagamento.js"
Cohesion: 0.47
Nodes (9): alvoDoRotulo(), consultarStatus(), gerarOuAtualizarPix(), iniciarPolling(), liberarBotao(), marcarOcupado(), mostrarEstado(), pararPolling() (+1 more)

### Community 64 - "test_sessao_revogada.py"
Cohesion: 0.24
Nodes (11): Sessões encerradas pelo logout. A sessão do Flask é um cookie assinado, sem…, SessaoRevogada, _cliente_com_cookie(), _entrar_como_admin(), `session.clear()` só limpava o navegador de quem saiu; a cópia do cookie seguia…, test_logout_apaga_revogacoes_vencidas(), test_logout_de_uma_sessao_nao_derruba_as_outras(), test_logout_revoga_a_copia_do_cookie_feita_antes() (+3 more)

### Community 65 - "Relatório de segurança — Sistema Extreme Team"
Cohesion: 0.15
Nodes (12): Controles verificados, Histórico de auditorias, O que foi feito nesta rodada, Pendências não relacionadas a segurança, Relatório de segurança — Sistema Extreme Team, Rodada anterior (22/09/2026 — 2ª rodada), Rodada de 04/10/2026 — limites de requisição, Situação atual (20/10/2026 — hero 3D, OWASP/DevSecOps e dependências) (+4 more)

### Community 66 - "Professor"
Cohesion: 0.07
Nodes (40): cadastrar_professor(), foto_professor(), gerenciar_turmas(), painel_professor(), route, remover_professor(), ProfessorDAO, Professor (+32 more)

### Community 67 - "componentes.js"
Cohesion: 0.15
Nodes (12): abrir(), agendarSaida(), fecharMenu(), fecharToast(), limpar(), mostrarErro(), prepararToast(), campo_copiavel() (+4 more)

### Community 68 - "prontidao.py"
Cohesion: 0.43
Nodes (6): banco_responde(), _consultar_banco(), Verificação de prontidão (/health/pronto): o banco e o Redis respondem agora?…, None quando o limite de requisições não usa Redis (memory:// em…, redis_responde(), verificar()

### Community 69 - "botao_ocupado.test.cjs"
Cohesion: 0.18
Nodes (7): assert, criarElemento(), fs, montar(), path, test, vm

### Community 70 - "test_backup_scripts.py"
Cohesion: 0.27
Nodes (11): ambiente(), _executavel(), fixture, Scripts de backup (tools/backup/): retenção, falha sem backup "pela metade" e a…, _rodar(), test_backup_gera_dump_e_uploads_e_aplica_a_retencao(), test_dump_ilegivel_nao_vira_backup(), test_restaurar_em_banco_descartavel_e_extrair_uploads() (+3 more)

### Community 71 - "gunicorn.conf.py"
Cohesion: 0.25
Nodes (9): post_worker_init(), Hooks carregados pelo Gunicorn; nunca executados por flask db upgrade., worker_exit(), iniciar(), _laco(), parar(), Aciona a fila periodicamente durante a vida de um worker Gunicorn. Importar…, Inicia uma vez por processo, depois de carregar a aplicação e migrar o banco. (+1 more)

### Community 72 - "config.py"
Cohesion: 0.10
Nodes (26): chave_da_conta(), Chave de limite por CONTA, caindo no IP só para quem não está autenticado. A…, _paginar(), Aplica LIMIT/OFFSET e conta o total numa consulta separada e barata. A contagem…, Decimal, Matricula, Pedido de troca de plano agendado para a próxima renovação. Nunca altera o…, SolicitacaoMudancaPlano (+18 more)

### Community 73 - "analytics.test.cjs"
Cohesion: 0.18
Nodes (7): assert, CODIGO, Element, fs, path, test, vm

### Community 74 - "test_conversao_home.py"
Cohesion: 0.23
Nodes (10): _body_tag(), _html(), Conversão na home: perguntas frequentes, cadastro no hero e página de obrigado., test_cadastro_fica_no_hero(), test_home_mostra_as_perguntas_frequentes_em_details(), test_home_nao_tem_barra_fixa_de_cadastro(), test_json_ld_faq_repete_exatamente_as_perguntas_da_pagina(), test_pagina_de_obrigado_explica_os_proximos_passos_e_sai_do_indice() (+2 more)

### Community 75 - "_parece_busca_por_cpf"
Cohesion: 0.18
Nodes (11): _parece_busca_por_cpf(), O termo é um CPF, ou um pedaço dele, e não um nome que por acaso tem número?, parametrize, Qualquer dígito no termo virava `CPF LIKE '%3%'` e devolvia a academia inteira., Rotas que custam hash de senha, processamento de imagem ou sondagem de token., Limites declarados por decorador NAQUELA rota. `resolve_limits` não serve aqui:…, Guarda do teste acima: uma rota sem limite precisa ser reprovada por ele., _tem_limite() (+3 more)

### Community 76 - "test_email_componentes.py"
Cohesion: 0.33
Nodes (7): E-mails: base com a logo oficial e componentes seguros para cliente de e-mail…, _render(), _sem_recursos_externos(), test_base_sem_url_publica_cai_para_o_nome_em_texto(), test_base_usa_a_logo_quando_ha_url_publica(), test_botao_do_email_usa_o_ouro_do_sistema(), test_cartao_de_resumo_com_badge()

### Community 77 - "test_layouts.py"
Cohesion: 0.29
Nodes (8): _conferir_head_comum(), parametrize, Layouts base (templates/layouts/) e toasts. Cada página estende o layout da sua…, test_area_do_aluno_carrega_o_layout(), test_flash_de_erro_vira_toast_que_nao_some_sozinho(), test_paginas_publicas_carregam_o_head_comum(), test_painel_admin_carrega_o_layout_admin(), test_toda_pagina_estende_um_layout()

### Community 78 - "test_migracao_checkout.py"
Cohesion: 0.31
Nodes (8): _colunas(), conexao(), migracao(), fixture, Exercita a migração dos campos do Checkout Pro de verdade (upgrade e…, _rodar(), test_downgrade_remove_exatamente_o_que_o_upgrade_criou(), test_upgrade_adiciona_as_colunas_e_preserva_linhas_antigas()

### Community 79 - "Academia"
Cohesion: 0.16
Nodes (11): Academia, link_email(), parametrize, test_admin_salva_atualiza_e_limpa_contatos(), test_configuracoes_exigem_admin(), test_contatos_invalidos(), test_csrf_configuracoes(), test_erro_preserva_formulario_e_dados_salvos() (+3 more)

### Community 80 - "checkout_abertura.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 81 - "pagamento_polling.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 82 - "test_publicas_redesign.py"
Cohesion: 0.20
Nodes (5): _cabecalho(), _entrar_fixo(), test_admin_logado_vai_da_home_para_o_painel(), test_aluno_logado_vai_da_home_direto_para_a_area_do_aluno(), test_visitante_tem_entrar_fixo_que_abre_o_mesmo_modal()

### Community 83 - "env.py"
Cohesion: 0.39
Nodes (7): get_engine(), get_engine_url(), get_metadata(), Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online()

### Community 84 - "test_formatos_de_imagem.py"
Cohesion: 0.26
Nodes (10): disco_temporario(), _imagem(), parsers_proibidos(), fixture, parametrize, Upload de foto e comprovante: o Pillow só interpreta JPEG, PNG e WebP. As…, Falha o teste se o parser de GIF ou TIFF for chamado., test_comprovante_em_outro_formato_e_recusado_sem_passar_pelo_parser() (+2 more)

### Community 85 - "_Resposta"
Cohesion: 0.15
Nodes (13): api_mp(), oauth_env(), fixture, Substitui POST /oauth/token. `respostas` é consumida em ordem; a última se…, A rota de checkout pede o token com a mensalidade travada na sessão dela., _Resposta, test_callback_com_aplicativo_recusado_aponta_as_credenciais(), test_callback_com_code_recusado_nao_grava() (+5 more)

### Community 86 - "academia_bp.py"
Cohesion: 0.32
Nodes (10): configuracoes(), _pagina(), route, O administrador foi ao Mercado Pago e a autorização não voltou para cá? O state…, tentativa_sem_retorno(), editar_professor(), Normalização de contatos profissionais antes de montar links públicos., validar_email() (+2 more)

### Community 87 - "shot.mjs"
Cohesion: 0.29
Nodes (5): { chromium }, contextos, CREDS, jobs, require

### Community 88 - "c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py"
Cohesion: 0.60
Nodes (5): _backfill_vigencia(), _colunas(), _criar_tabela_solicitacoes(), downgrade(), upgrade()

### Community 89 - "cena.tsx"
Cohesion: 0.09
Nodes (22): AmostraEmblema, amostrarEmblema(), amostras, Brasas(), BRONZE, Camera(), carregarEmblema(), Conjunto() (+14 more)

### Community 90 - "test_comprovante_sem_metadados.py"
Cohesion: 0.27
Nodes (17): _chunks(), disco_temporario(), _exif(), _exif_do_celular(), _foto_jpeg(), _guardado(), _pixels(), _pixels_aleatorios() (+9 more)

### Community 91 - "896e70afc9c5_adiciona_foto_e_graduacao_do_aluno_.py"
Cohesion: 0.60
Nodes (3): _e_decimal(), _faltantes(), upgrade()

### Community 92 - "test_migracao_cadastro_administrativo.py"
Cohesion: 0.40
Nodes (3): banco_antigo(), fixture, Verifica a migração em um banco isolado com o schema anterior e dados.

### Community 93 - "google_login.py"
Cohesion: 0.20
Nodes (15): _autorizacao_valida(), callback(), login_google(), _novo_pkce(), limit, route, (code_verifier, code_challenge S256), como na conexão do Mercado Pago. O state…, O state devolvido é o que ESTA sessão emitiu, há pouco tempo? (+7 more)

### Community 95 - "d9e2f6a14c80_contatos_academia_perfis_professores.py"
Cohesion: 0.83
Nodes (3): _campos_professor(), downgrade(), upgrade()

### Community 97 - "vercel.json"
Cohesion: 0.50
Nodes (3): gru1, regions, $schema

### Community 98 - "mercado_pago.py"
Cohesion: 0.12
Nodes (27): _base_url_opcional(), base_url_publica(), criar_pagamento_pix(), criar_preferencia_checkout(), _erro_menciona(), _erro_menciona_expiracao(), _extrair_dados_pix(), _normalizar_pagamento() (+19 more)

### Community 99 - "backup.sh"
Cohesion: 1.00
Nodes (3): registrar(), reter(), backup.sh script

### Community 114 - "capturar_emails"
Cohesion: 0.67
Nodes (3): capturar_emails(), fixture, Intercepta o envio e devolve os e-mails que teriam saído, com os links.

### Community 116 - "_preparar_state"
Cohesion: 0.15
Nodes (15): _preparar_state(), parametrize, test_aviso_de_autorizacao_vencida_aparece_uma_vez(), test_callback_avisa_quando_a_conta_muda(), test_callback_cancelado_no_mercado_pago_consome_o_state(), test_callback_com_erro_do_mercado_pago_que_nao_e_cancelamento(), test_callback_com_mercado_pago_fora_do_ar_nao_grava(), test_callback_com_resposta_incompleta_nao_grava() (+7 more)

### Community 117 - "salvar_foto_perfil"
Cohesion: 0.10
Nodes (25): ArquivoInvalido, _conferir_dimensoes(), _detectar_tipo_imagem_real(), ImagemGrandeDemais, Exception, Imagem cujas DIMENSÕES declaradas passam do limite de pixels., Recusa pelo cabeçalho, antes de qualquer pixel ser decodificado. `Image.open`…, Confere o conteúdo de fato (decodificando com Pillow), não a extensão/Content-… (+17 more)

### Community 122 - "Contrato do redesign — SistemaEXTREMETEAM"
Cohesion: 0.09
Nodes (20): 0. Antes de escrever código, 1. Identidade visual (design tokens), 2. Logo oficial (usar SOMENTE a logo original), 3. Telas a implementar, 4. Regras e dados, 5. Forma de trabalhar, Painel administrativo (desktop, sidebar preta com o emblema do dragão), Prompt para o Claude Code — Redesign do SistemaEXTREMETEAM (+12 more)

### Community 123 - "Plano"
Cohesion: 0.24
Nodes (4): Plano, Preço de uma cobrança criada em `hoje`., parametrize, test_duas_requisicoes_pix_reutilizam_uma_cobranca_postgres()

### Community 124 - "cinema.test.cjs"
Cohesion: 0.11
Nodes (10): assert, CODIGO, conferirAtiva(), Elemento, fs, ListaDeClasses, montar(), path (+2 more)

### Community 125 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, isolatedModules, jsx, lib, module, moduleResolution, noEmit, noUnusedLocals (+10 more)

### Community 126 - "pgUsuario.html (área do aluno)"
Cohesion: 0.10
Nodes (23): cancelarAberturas(), consultar(), finalizarAbertura(), parar(), mostrarTela(), trocarTela(), checkout_continuar.html — continuar no Mercado Pago, checkout_retorno.html — situação do pagamento (+15 more)

### Community 127 - "penetration-testing-with-strix/SKILL.md"
Cohesion: 0.18
Nodes (10): Exit codes (headless), Option A — Open-source CLI (self-hosted), Option B — Managed cloud (no local infra), Prerequisites, Reading results, Reporting & next steps, Run a Strix pentest, Running a scan (+2 more)

### Community 128 - "test_cinema.py"
Cohesion: 0.20
Nodes (10): _html(), Hero cinematográfico da home e profundidade (tilt) dos cartões. O hero guarda…, _secao_cinema(), test_cartoes_do_metodo_na_home_inclinam(), test_cena_aponta_para_a_entrada_compilada_com_hash(), test_hero_tem_cadastro_seta_para_os_planos_e_poster(), test_manchetes_ficam_no_html_e_so_a_primeira_e_visivel(), test_sem_build_a_home_fica_so_com_o_poster() (+2 more)

### Community 129 - "SistemaEXTREMETEAM"
Cohesion: 0.04
Nodes (47): Ativar o acesso depois, Backup automático (serviço `backup` do compose), Backup e restauração, Banco criado pela versão antiga, Banco de dados e migrations, Cadastro de aluno pela administração e ativação de acesso, Como obter credenciais de teste (modo manual, sem OAuth), Como testar localmente (+39 more)

### Community 130 - "test_paginas_erro.py"
Cohesion: 0.18
Nodes (4): csrf_ligado(), fixture, Página de erro (templates/erro.html) e os handlers de 404, 403, 500 e CSRF., test_404_para_quem_esta_logado_leva_a_area_dele()

### Community 131 - "_ajustar"
Cohesion: 0.43
Nodes (8): _agora(), _ajustar(), test_conexao_vencida_e_sem_renovacao_possivel_recusa(), test_erro_diferente_de_invalid_grant_nao_marca_reconexao(), test_falha_na_renovacao_com_token_vencido_levanta(), test_falha_passageira_na_renovacao_usa_o_token_ainda_valido(), test_renovacao_recusada_marca_reconexao_e_nao_insiste(), test_token_perto_de_vencer_e_renovado_uma_vez()

### Community 132 - ".remover"
Cohesion: 0.40
Nodes (3): Apaga um plano que nunca foi usado. True, None (não existe) ou False (em uso)., Planos que algum registro referencia: mensalidade, cadastro de aluno ou pedido…, test_plano_so_no_cadastro_do_aluno_tambem_conta_como_em_uso()

### Community 133 - "seo_bp.py"
Cohesion: 0.67
Nodes (3): route, robots(), sitemap()

### Community 135 - "cinema.py"
Cohesion: 0.31
Nodes (8): _entradas(), modulo(), Arquivos do hero cinematográfico da página inicial. A cena 3D é compilada pelo…, {nome da entrada: arquivo}, lido uma vez: o build não muda com o servidor no ar., URL da entrada `nome` ('cena' ou 'video') do build, ou None se não foi…, URL do vídeo do hero, só se ele existir e a entrada que o toca estiver…, _tem_video(), video()

### Community 136 - "Skills Disponíveis"
Cohesion: 0.22
Nodes (8): Assistente e Automação (Antigravity), Ciências e Bioinformática (Plugins de Ciência), Dados e Google Cloud Platform (GCP), Desenvolvimento Mobile e Flutter/Dart, Desenvolvimento Web e Frontend, Firebase e Backend, GenAI e Machine Learning, Skills Disponíveis

### Community 137 - ".listar_por_aluno"
Cohesion: 0.11
Nodes (32): parametrize, test_admin_lanca_mensalidade_paga_no_cartao(), _pagar(), plano_barato(), fixture, Vigência do plano: o que decide "Plano ativo" é o período pago, não o cadastro.…, Mensalidade paga cobrindo um período - o que de fato ativa o plano., Quem paga uma cobrança vencida há semanas tem de receber os 30 dias a partir da… (+24 more)

### Community 138 - "cinema.js"
Cohesion: 0.39
Nodes (7): anotar(), ativar(), carregarCena(), ehAppleMovel(), medir(), pedirMedida(), podeTer3D()

### Community 139 - "Etapa 1 — migrar páginas para os layouts (SEM mudar o visual)"
Cohesion: 0.29
Nodes (6): Conferência (agentes Claude), Divisão, Etapa 1 — migrar páginas para os layouts (SEM mudar o visual), O que já existe (não edite), Receita por página, Relatório (curto)

### Community 140 - "Etapas 4 a 6 — aluno, admin, professor (aplicar os componentes nas páginas)"
Cohesion: 0.29
Nodes (6): Agente A — área do aluno + pagamento, Agente B — admin, Antigravity — financeiro, turmas, professor, Etapas 4 a 6 — aluno, admin, professor (aplicar os componentes nas páginas), Orquestrador (Claude), Regras para todos

### Community 142 - "home"
Cohesion: 0.50
Nodes (4): exempt, health(), home(), route

### Community 143 - "Etapa 2 — biblioteca de componentes"
Cohesion: 0.33
Nodes (5): Entregas e arquivos exclusivos, Etapa 2 — biblioteca de componentes, Ganchos de JS (Claude escreve `static/js/componentes.js`; markup e CSS usam EXATAMENTE isto), Macros (Agente A), cada uma no seu arquivo em `templates/components/`, Regras visuais (REDESIGN_CONTRATO.md seção 2 — leia)

### Community 146 - "formatacao.py"
Cohesion: 0.09
Nodes (31): ativar_acesso(), _cadastro_recebido(), _convidar_cadastro_existente_por_id(), _em_segundo_plano(), _enviar_em_segundo_plano(), pagina_cadastro(), Roda `tarefa` fora da requisição, para o tempo de resposta não revelar nada. Em…, E-mail COM token (recuperação, confirmação): não pode ir para a `fila_email`. A… (+23 more)

### Community 147 - "Etapa 3 — home com os planos + termos"
Cohesion: 0.40
Nodes (4): Agente A — `templates/index.html` e `static/css/index.css`, Antigravity — `termos_de_servico.html`, `politica_privacidade.html`, `termos_responsabilidade.html` + `static/css/termos.css` (novo), Dados da home (Claude entrega em servidor.py — não edite), Etapa 3 — home com os planos + termos

### Community 148 - "test_fontes_locais.py"
Cohesion: 0.25
Nodes (3): parametrize, Fontes servidas pelo próprio site (SEC-18). Com o Google Fonts, o navegador de…, test_csp_nao_libera_o_google_fonts()

### Community 149 - "Biblioteca no Figma"
Cohesion: 0.50
Nodes (3): Biblioteca no Figma, Falta (ordem de retomada), Limites do plano Starter que moldaram o arquivo

### Community 151 - "URLPublicaInvalida"
Cohesion: 0.18
Nodes (16): iniciar(), _intervalo(), _laco(), _ligado(), parar(), _pingar(), Mantém a aplicação acordada em hospedagens que hibernam por inatividade. Uma…, Encerra o laço. Usado pelos testes; em produção a thread é daemon. (+8 more)

### Community 155 - "test_armazenamento_storage.py"
Cohesion: 0.18
Nodes (17): ArmazenamentoIndisponivel, ler_arquivo(), Conteúdo de um arquivo já salvo, ou None se não existir, for inválido ou o…, O arquivo era válido, mas o Storage não aceitou guardá-lo agora. Herda de…, _jpeg(), parametrize, Uploads no Supabase Storage (produção na Vercel), com o HTTP simulado., _Resposta (+9 more)

### Community 157 - "auth.test.cjs"
Cohesion: 0.25
Nodes (6): assert, CODIGO, fs, path, test, vm

### Community 158 - "requirements.txt (dependências de produção)"
Cohesion: 0.05
Nodes (53): compose.yaml (Docker Compose: db, rate-limit, app, backup, https), Serviço app (Flask com Gunicorn na porta 5000), Serviço backup (pg_dump diário, retenção 7 + 4), Serviço db (postgres:17-alpine), Serviço https (Caddy 2.9), Serviço rate-limit (redis:7-alpine, volatile-ttl, 64 MB), Dependabot (atualizações semanais de dependências), Atualização das imagens do compose (postgres, redis, caddy) (+45 more)

### Community 159 - ".buscar_por_id"
Cohesion: 0.17
Nodes (37): _agora_mercado_pago(), _assinar(), _paga_pelo_mercado_pago(), _pagamento_mp(), _preparar_retorno(), Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala…, Pix aberto e checkout concluído ao mesmo tempo: a consulta pelo…, _ref_checkout() (+29 more)

### Community 161 - "ci-security-scanning-with-strix/SKILL.md"
Cohesion: 0.29
Nodes (6): GitHub Actions, Option A — Self-hosted OSS CLI in the runner, Option B — Managed platform (no runner infra), Optional: upload findings to GitHub code scanning, Other CI systems, Set up Strix in CI/CD

### Community 164 - "Find security vulnerabilities in code"
Cohesion: 0.29
Nodes (6): Complementary tooling, Find security vulnerabilities in code, Fix and verify, Read the results, Reviewing a pull request instead of the whole repo, Run it

### Community 165 - "test_mercado_pago_oauth.py"
Cohesion: 0.09
Nodes (27): _conectar(), _dados_conexao(), Grava uma conexão direto pelo serviço (precisa de app context)., test_cada_conexao_iniciada_usa_state_novo(), test_callback_de_aluno_nao_conecta_conta(), test_callback_sem_conexao_iniciada_pela_sessao(), test_chave_dedicada_cifra_e_troca_de_chave_torna_ilegivel(), test_chave_dedicada_malformada_e_erro_de_configuracao() (+19 more)

### Community 167 - "Security-test an API"
Cohesion: 0.33
Nodes (5): 1. Gather what the agents need, 2. Run the scan, 3. Verify findings, 4. Fix, re-test, and keep it tested, Security-test an API

### Community 168 - "Application security testing"
Cohesion: 0.33
Nodes (5): 1. Map the assets, 2. Pick the right test per asset, 3. Consolidate into one plan, 4. Be honest about coverage, Application security testing

### Community 170 - "Fix Strix findings and verify"
Cohesion: 0.33
Nodes (5): 1. Triage, 2. Fix, 3. Verify by re-running Strix, 4. Report, Fix Strix findings and verify

### Community 171 - "Test against the OWASP Top 10"
Cohesion: 0.33
Nodes (5): Report honestly, Run it, Test against the OWASP Top 10, Then fix and re-test, What is and is not testable by an agent

### Community 172 - "Pentest a web application"
Cohesion: 0.33
Nodes (5): 1. Confirm authorization and scope, 2. Run the scan, 3. Review results, 4. Fix and verify, Pentest a web application

### Community 174 - "admin_requerido"
Cohesion: 0.61
Nodes (7): callback(), conectar(), desconectar(), limit, route, _voltar(), admin_requerido()

### Community 175 - "test_email_gmail.py"
Cohesion: 0.33
Nodes (3): aplicativo_google(), fixture, test_refresh_token_fica_cifrado_no_banco()

### Community 180 - "limites_pagamento.py"
Cohesion: 0.50
Nodes (3): chave_pagamento(), Orçamentos compartilhados das chamadas interativas ao provedor de pagamento., A mesma conta mantém seu limite entre sessões, rotas e mensalidades. Alunos que…

## Ambiguous Edges - Review These
- `botao_google.html` → `Integração com o Gmail (conta remetente da academia)`  [AMBIGUOUS]
  templates/politica_privacidade.html · relation: conceptually_related_to

## Knowledge Gaps
- **326 isolated node(s):** `Visão geral`, `Marca`, `Superfícies claras`, `Texto`, `Situações` (+321 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `botao_google.html` and `Integração com o Gmail (conta remetente da academia)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `PagamentoDAO` connect `PagamentoDAO` to `Aluno`, `adm_bp.py`, `.checkout_ainda_valido`, `turma_bp.py`, `logar_como_admin`, `.listar_por_aluno`, `test_admin_mercado_pago.py`, `criar_aluno`, `test_auditoria_seguranca.py`, `pix_bp.py`, `.contratar_plano`, `test_pix_rotas.py`, `.buscar_por_id`, `test_mudanca_plano.py`, `checkout_bp.py`, `test_plano_arquivo_promocao.py`, `test_pagamento_recusado.py`, `criar_pagamento`, `config.py`, `test_comprovante_sem_metadados.py`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Why does `Vitrine de componentes (/_vitrine)` connect `ui.html` to `config.py`, `componentes.js`, `csrf_field.html`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Why does `logar_como_admin()` connect `logar_como_admin` to `Aluno`, `test_admin_segundo_fator.py`, `planilha_bp.py`, `test_seo.py`, `turma_bp.py`, `.listar_por_aluno`, `test_admin_mercado_pago.py`, `PagamentoDAO`, `criar_aluno`, `test_google_login.py`, `test_seguranca.py`, `test_pix_rotas.py`, `test_mudanca_plano.py`, `test_mercado_pago_oauth.py`, `test_plano_arquivo_promocao.py`, `MercadoPagoConexao`, `test_analytics.py`, `PlanoDAO`, `criar_pagamento`, `test_planilha_economica.py`, `test_home_planos.py`, `test_sessao_revogada.py`, `Professor`, `config.py`, `test_layouts.py`, `Academia`, `test_publicas_redesign.py`, `_Resposta`, `_preparar_state`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Are the 165 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 165 INFERRED edges - model-reasoned connections that need verification._
- **Are the 169 inferred relationships involving `logar_como_admin()` (e.g. with `test_admin_salva_atualiza_e_limpa_contatos()` and `test_csrf_configuracoes()`) actually correct?**
  _`logar_como_admin()` has 169 INFERRED edges - model-reasoned connections that need verification._
- **Are the 168 inferred relationships involving `criar_aluno()` (e.g. with `test_admin_lanca_mensalidade_paga_no_cartao()` and `test_conversao_igual_para_cadastro_novo_e_cpf_ou_email_existentes()`) actually correct?**
  _`criar_aluno()` has 168 INFERRED edges - model-reasoned connections that need verification._