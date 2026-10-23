# Graph Report - SistemaEXTREMETEAM  (2026-10-22)

## Corpus Check
- 212 files · ~274,642 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2985 nodes · 7021 edges · 170 communities (156 shown, 14 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 1286 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7a28c63b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Aluno
- Componentes
- ResultadoContratacao
- test_mercado_pago_oauth.py
- test_seo.py
- adm_bp.py
- .buscar_por_id
- logar_como_admin
- planos.py
- usuario_bp.py
- PlanoDAO
- test_planilha_economica.py
- index.html (home pública)
- gmail_conta.py
- test_regressao_auditoria.py
- fase3b.js
- test_auditoria_seguranca.py
- financeiro.html — painel financeiro
- fila_email.py
- csrf_field.html
- financeiroDAO.py
- dt_aluno.html — ficha do aluno (admin)
- pix_bp.py
- servidor.py
- criar_aluno
- pgUsuario.html (área do aluno)
- mercado_pago_conta.py
- test_seguranca.py
- test_pix_rotas.py
- Plano
- planilha_excel.py
- checkout_bp.py
- test_mudanca_plano.py
- avatar
- test_mercado_pago_servico.py
- test_limites_requisicao.py
- Pagina
- PagamentoDAO
- seo.py
- URLPublicaInvalida
- varredura.mjs
- test_pagamento_recusado.py
- README.md
- ui.html
- turma_bp.py
- test_observabilidade.py
- test_analytics.py
- requirements.txt (dependências de produção)
- admin_requerido
- criar_pagamento
- pagina_cadastro
- analytics.js
- package.json
- Academia
- Strix Cloud (managed, no local infra)
- salvar_foto_perfil
- layouts/admin.html — layout do painel administrativo
- Serviço app (Flask com Gunicorn na porta 5000)
- test_prontidao.py
- pix.js
- test_arranque_seguranca.py
- revogar_sessao_atual
- test_keep_alive.py
- planilha_bp.py
- test_sessao_revogada.py
- Relatório de segurança — Sistema Extreme Team
- armazenamento.py
- componentes.js
- prontidao.py
- botao_ocupado.test.cjs
- test_backup_scripts.py
- gunicorn.conf.py
- .totais_periodo
- analytics.test.cjs
- pagamento.js
- admin_nav.html
- test_email_componentes.py
- test_layouts.py
- test_migracao_checkout.py
- test_limites_pagamento.py
- checkout_abertura.test.cjs
- pagamento_polling.test.cjs
- test_publicas_redesign.py
- env.py
- test_formatos_de_imagem.py
- _png_bomba
- MatriculaDAO
- shot.mjs
- c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py
- cena.tsx
- test_comprovante_sem_metadados.py
- 896e70afc9c5_adiciona_foto_e_graduacao_do_aluno_.py
- test_migracao_cadastro_administrativo.py
- seo_bp.py
- a1f0c3e75b92_schema_inicial.py
- d9e2f6a14c80_contatos_academia_perfis_professores.py
- e4b7c2a91d35_cadastro_administrativo_e_convite_de_acesso.py
- vercel.json
- MercadoPagoIndisponivel
- backup.sh
- capturar_emails
- gerar_imagem_og.py
- config.py
- test_perfil_e_foto.py
- agendar.sh
- restaurar.sh
- Contrato do redesign — SistemaEXTREMETEAM
- planilha.py
- cinema.test.cjs
- compilerOptions
- .contar_cadastrados
- penetration-testing-with-strix/SKILL.md
- test_cinema.py
- SistemaEXTREMETEAM
- test_paginas_erro.py
- test_mercado_pago_oauth_postgres.py
- test_email_gmail.py
- Pagamento de mensalidade via Pix (Mercado Pago)
- test_google_login.py
- cinema.py
- Skills Disponíveis
- test_migracao_conexao_mercado_pago.py
- cinema.js
- Etapa 1 — migrar páginas para os layouts (SEM mudar o visual)
- Etapas 4 a 6 — aluno, admin, professor (aplicar os componentes nas páginas)
- emblema.py
- Banco de dados e migrations
- Etapa 2 — biblioteca de componentes
- Cadastro de aluno pela administração e ativação de acesso
- Outras formas de pagamento (Checkout Pro)
- TransporteEmMemoria
- Etapa 3 — home com os planos + termos
- test_fontes_locais.py
- Biblioteca no Figma
- CLAUDE.md
- google_login.py
- Professor
- test_logs_sem_dado_pessoal.py
- auth.test.cjs
- credenciais.py
- test_admin_mercado_pago.py
- keep_alive.py
- ci-security-scanning-with-strix/SKILL.md
- test_conversao_home.py
- _FakePaymentResource
- Find security vulnerabilities in code
- Security-test an API
- Application security testing
- imagens.d.ts
- Fix Strix findings and verify
- Test against the OWASP Top 10
- Pentest a web application

## God Nodes (most connected - your core abstractions)
1. `PagamentoDAO` - 230 edges
2. `criar_aluno()` - 170 edges
3. `logar_como_admin()` - 167 edges
4. `criar_pagamento()` - 164 edges
5. `logar_como_aluno()` - 138 edges
6. `AlunoDAO` - 93 edges
7. `PlanoDAO` - 69 edges
8. `Aluno` - 64 edges
9. `MercadoPagoIndisponivel` - 45 edges
10. `Professor` - 43 edges

## Surprising Connections (you probably didn't know these)
- `Vitrine de planos da home (secao_planos com vitrine_planos)` --references--> `cartao_do_plano()`  [INFERRED]
  templates/index.html → servicos/planos.py
- `test_limite_de_login_por_ip_e_identificador()` --uses--> `AlunoDAO`  [INFERRED]
  tests/test_seguranca.py → dao/usuarioDAO.py
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

## Communities (170 total, 14 thin omitted)

### Community 0 - "Aluno"
Cohesion: 0.08
Nodes (15): _convidar_cadastro_existente(), _convidar_cadastro_existente_por_id(), Cadastro administrativo que alguém tentou recriar pelo formulário público. Em…, Versão para thread de fundo: a sessão da requisição não vale fora dela., Matrícula feita no balcão: sem login, sem senha e sem convite de acesso. Nasce…, Aluno, Se existe uma conta de acesso, e não se o aluno está em dia ou matriculado.…, Convite de acesso já enviado e ainda não usado (a validade é checada na rota). (+7 more)

### Community 1 - "Componentes"
Cohesion: 0.05
Nodes (36): Altura de controle, Avisos flutuantes, Botões — `.et-botao` + variante (+ tamanho), Cartões e contêineres, Componentes, Contêiner e estrutura, Cores, Dados (+28 more)

### Community 3 - "test_mercado_pago_oauth.py"
Cohesion: 0.08
Nodes (58): MercadoPagoConexao, Conta do Mercado Pago que a academia autorizou por OAuth. Uma linha só (a…, _agora(), _ajustar(), api_mp(), _conectar(), _dados_conexao(), oauth_env() (+50 more)

### Community 4 - "test_seo.py"
Cohesion: 0.10
Nodes (25): _head(), _json_ld(), parametrize, SEO técnico: robots.txt, sitemap, títulos, meta tags, noindex e JSON-LD da home., Nenhum campo do JSON-LD pode sair nulo, vazio ou só com espaços., _robots(), _sem_vazios(), test_area_do_admin_sai_do_indice() (+17 more)

### Community 5 - "adm_bp.py"
Cohesion: 0.08
Nodes (55): _aluno_do_cpf_ou_painel(), aprovar_aluno(), aprovar_comprovante_manual(), arquivar_plano(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_plano(), cancelar_mudanca_plano_admin() (+47 more)

### Community 6 - ".buscar_por_id"
Cohesion: 0.19
Nodes (27): Hipótese: forjar ?status=approved na volta do MP quita a mensalidade., test_retorno_ignora_status_aprovado_da_query_string(), _agora_mercado_pago(), _assinar(), _pagamento_mp(), _preparar_retorno(), Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala…, Pix aberto e checkout concluído ao mesmo tempo: a consulta pelo… (+19 more)

### Community 7 - "logar_como_admin"
Cohesion: 0.09
Nodes (62): AlunoDAO, logar_como_admin(), _matricular(), parametrize, Cadastro de aluno pela administração, ativação de acesso e confirmação de…, test_admin_lanca_e_baixa_mensalidade_de_aluno_sem_acesso(), test_admin_matricula_aluno_sem_email_senha_nem_acesso(), test_admin_nao_pode_apagar_o_usuario_de_uma_conta_ativa() (+54 more)

### Community 8 - "planos.py"
Cohesion: 0.06
Nodes (42): cadeia_paga(), cartao_do_plano(), cobranca_a_pagar(), cobranca_em_decisao(), cobranca_pendente(), duracao_dias(), _duracao_por_extenso(), esta_inadimplente() (+34 more)

### Community 9 - "usuario_bp.py"
Cohesion: 0.13
Nodes (38): _acesso_permitido_pagamento(), alterar_senha_perfil(), _aluno_da_sessao(), _aluno_por_token(), atualizar_dados_perfil(), cadastro_obrigado(), cancelar_mudanca_plano(), _chave_ip_e_identificador() (+30 more)

### Community 10 - "PlanoDAO"
Cohesion: 0.08
Nodes (37): editar_plano(), painel_adm(), Nome, preço, duração e promoção. Vale para as cobranças criadas daqui em…, PlanoDAO, Apaga um plano que nunca foi usado. True, None (não existe) ou False (em uso)., Marca o plano em destaque da página inicial, desmarcando qualquer outro.…, Inclusive os arquivados: serve a quem olha o histórico (filtro do financeiro)., Os planos à venda: home, perfil do aluno e formulários de contratação. (+29 more)

### Community 11 - "test_planilha_economica.py"
Cohesion: 0.15
Nodes (21): criar_despesa(), _form(), fixture, parametrize, Planilha econômica: fluxo de caixa, lançamento de despesas e download em Excel., test_ano_fora_do_intervalo_volta_ao_atual(), test_ano_sem_movimento_mostra_estado_vazio(), test_anos_disponiveis_vao_do_primeiro_movimento_ate_hoje() (+13 more)

### Community 12 - "index.html (home pública)"
Cohesion: 0.11
Nodes (13): faq_estruturado(), Textos editáveis da página inicial: perguntas frequentes e prazos de…, JSON-LD FAQPage com exatamente as perguntas mostradas na página., icone_senha, input_senha, modal, academia (contatos e endereço da academia), index.html (home pública) (+5 more)

### Community 13 - "gmail_conta.py"
Cohesion: 0.27
Nodes (15): GmailConexao, _access_token(), _cifrar(), _client_id(), _client_secret(), _decifrar(), enviar(), estado() (+7 more)

### Community 14 - "test_regressao_auditoria.py"
Cohesion: 0.03
Nodes (60): _parece_busca_por_cpf(), O termo é um CPF, ou um pedaço dele, e não um nome que por acaso tem número?, Uma página de alunos já cadastrados, recortada e filtrada pelo banco. O painel…, _contar_selects_em_alunos(), _credencial(), parametrize, Regressões da auditoria de segurança, desempenho e confiabilidade. Cada caso…, Head-of-line blocking: a primeira linha falhando não pode impedir as seguintes.… (+52 more)

### Community 15 - "fase3b.js"
Cohesion: 0.06
Nodes (47): avisos, bind(), caixas, campos, col(), D(), estados, faixa (+39 more)

### Community 16 - "test_auditoria_seguranca.py"
Cohesion: 0.06
Nodes (45): _agora_mercado_pago(), _assinar(), _pagamento_mp(), _preparar_para_conciliacao(), parametrize, Auditoria de segurança: sondas escritas para TENTAR quebrar as regras. Nenhum…, Hipótese: as rotas de cobrança respondem sem sessão nenhuma., Hipótese: a sessão de professor é aceita nas rotas financeiras do aluno. (+37 more)

### Community 17 - "financeiro.html — painel financeiro"
Cohesion: 0.11
Nodes (20): ajustar(), aplicar(), admin_academia.html — configurações da academia, Conexão OAuth do Mercado Pago (PKCE), Webhook de pagamentos do Mercado Pago (MERCADO_PAGO_WEBHOOK_SECRET), checkout_continuar.html — continuar no Mercado Pago, checkout_retorno.html — situação do pagamento, Tom da mensagem por status do pagamento (+12 more)

### Community 18 - "fila_email.py"
Cohesion: 0.06
Nodes (40): EmailPendente, espera_da_proxima_tentativa(), Fila de e-mails no banco. Aviso e cobrança coletivos saíam um a um dentro da…, contar_falhados(), contar_pendentes(), disparar(), enfileirar(), enfileirar_transacional() (+32 more)

### Community 19 - "csrf_field.html"
Cohesion: 0.12
Nodes (22): Contato e localização da academia, ativar_acesso.html — ativar acesso pelo convite, cadastro.html — criar conta, cadastro_obrigado.html — cadastro recebido, Cadastro com PRG e resposta única, Aceite do Termo de Responsabilidade, Modal de login da home (#meuModal, POST /login), layouts/publico.html — layout das telas públicas (+14 more)

### Community 20 - "financeiroDAO.py"
Cohesion: 0.09
Nodes (34): Tira o plano de venda. Devolve `(plano, pedidos_cancelados)`, ou None. Pedidos…, Decimal, Pagamento, _para_decimal(), Status a exibir, com o vencimento já aplicado. Uma cobrança `pendente` cujo…, Pedido de troca de plano agendado para a próxima renovação. Nunca altera o…, SolicitacaoMudancaPlano, postgres_pix() (+26 more)

### Community 21 - "dt_aluno.html — ficha do aluno (admin)"
Cohesion: 0.14
Nodes (21): Conexão OAuth do Gmail para envio de avisos, admin_aluno_novo.html — matricular aluno, Matrícula sem acesso ao sistema, admin_avisos.html — avisos e cobranças por e-mail, Cobrança de mensalidades por e-mail, Fila de envio de e-mails (até 5 tentativas), Nonce de CSP em scripts inline (csp_nonce), admin_plano_editar.html — editar plano (+13 more)

### Community 22 - "pix_bp.py"
Cohesion: 0.07
Nodes (42): _acesso_permitido(), _chave_entrega_webhook(), criar_pix_mensalidade(), _data_da_aprovacao(), _forma_pagamento_confirmada(), _instante_utc(), _iso_utc(), _liberar_entrega_webhook() (+34 more)

### Community 23 - "servidor.py"
Cohesion: 0.14
Nodes (20): after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, context_processor, errorhandler, formatar_moeda(), Formata um valor em reais no padrão brasileiro: R$ 1.080,00. Usado como filtro…, acesso_negado() (+12 more)

### Community 24 - "criar_aluno"
Cohesion: 0.13
Nodes (36): Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, `pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -…, criar_aluno(), parametrize, test_admin_lanca_mensalidade_paga_no_cartao(), test_escolher_plano_cria_mensalidade_e_redireciona_para_pix(), test_plano_invalido_nao_cria_mensalidade(), test_reenvio_da_contratacao_reutiliza_mensalidade() (+28 more)

### Community 25 - "pgUsuario.html (área do aluno)"
Cohesion: 0.15
Nodes (6): mostrarTela(), trocarTela(), pgUsuario.html (área do aluno), Histórico de mensalidades (filtro e ordenação no navegador), Navegação por telas da área do aluno (data-menu-screen, bottom-nav), Turmas e presenças do aluno (confirmar frequência)

### Community 26 - "mercado_pago_conta.py"
Cohesion: 0.10
Nodes (39): ConfiguracaoInvalida, access_token_vigente(), _agora(), ambiente_da_conexao(), _cifrar(), _client_id(), _client_secret(), ConexaoIlegivel (+31 more)

### Community 27 - "test_seguranca.py"
Cohesion: 0.07
Nodes (24): test_upload_de_arquivo_disfarcado_e_recusado(), _cadastro_publico(), _imagem_jpeg(), _mensagem_da_resposta(), O `login` de um aluno pode ser o e-mail de outro; quem entra é decidido pela…, O ramo "par existe" não pode pagar a ida ao provedor dentro da requisição., Cadastro novo, CPF existente e e-mail existente respondem com a MESMA tela., Quem ainda controla a caixa antiga não pode assumir a conta depois da troca. (+16 more)

### Community 28 - "test_pix_rotas.py"
Cohesion: 0.19
Nodes (21): _agora_mercado_pago(), _assinar(), _resposta_consulta(), _resposta_criacao(), test_admin_tambem_pode_gerar_pix(), test_aluno_gera_pix_da_propria_mensalidade(), test_aluno_nao_acessa_mensalidade_de_outro_aluno(), test_falha_de_indisponibilidade_do_mp_retorna_503() (+13 more)

### Community 29 - "Plano"
Cohesion: 0.11
Nodes (19): Plano, Preço de uma cobrança criada em `hoje`., app(), client(), contexto_app(), limpar_banco(), logar_como_professor(), plano() (+11 more)

### Community 30 - "planilha_excel.py"
Cohesion: 0.30
Nodes (13): Nome legível da forma de pagamento. Antes as telas usavam `|replace('_','…, rotulo_forma_pagamento(), _aba_categorias(), _aba_entradas(), _aba_resumo(), _aba_saidas(), _cabecalho(), _escrever() (+5 more)

### Community 31 - "checkout_bp.py"
Cohesion: 0.12
Nodes (23): abrir_checkout(), _acesso_permitido(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), limitar_consulta_pagamento, limitar_criacao_pagamento, route (+15 more)

### Community 32 - "test_mudanca_plano.py"
Cohesion: 0.18
Nodes (25): Persistência dos pedidos de troca de plano agendados para a próxima renovação., Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, SolicitacaoPlanoDAO, _agendar(), _pagar(), Mudança para um plano mais barato agendada para a próxima renovação. Regra…, O admin pode estornar/cancelar a mensalidade que sustentava a vigência depois…, test_admin_cancela_a_solicitacao() (+17 more)

### Community 33 - "avatar"
Cohesion: 0.23
Nodes (13): avatar(), breadcrumb(), Biblioteca de componentes .et-* (componentes.css), Seção Nossa equipe (professores_publicos), Tabela de alunos paginada com busca no servidor, pgProfessor.html (minhas turmas do professor), professor_editar.html (perfil do professor), turma.html (detalhe da turma) (+5 more)

### Community 34 - "test_mercado_pago_servico.py"
Cohesion: 0.09
Nodes (35): ambiente_mercado_pago(), Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, Diz se a integracao esta apontando para producao ou para o sandbox. Prioriza a…, validar_assinatura_webhook(), Hipótese: uma notificação capturada ontem pode ser reenviada hoje., `ts=nan` fazia a comparação da janela dar False e passava pela checagem de…, test_webhook_recusa_assinatura_antiga(), test_webhook_recusa_ts_nao_numerico_finito() (+27 more)

### Community 35 - "test_limites_requisicao.py"
Cohesion: 0.12
Nodes (28): consultar_mp(), _estourar(), fixture, parametrize, Limites de requisição da rodada de 04/10/2026 (SEC-10 a SEC-17 e SEC-19). Cada…, Trocar de rede ou abrir outra sessão não devolve a cota de e-mails em massa., Faz `limite` requisições sem nenhum 429 e devolve a seguinte., Alunos no mesmo Wi-Fi não dividem o teto padrão, nem com o visitante anônimo. (+20 more)

### Community 36 - "Pagina"
Cohesion: 0.14
Nodes (5): Pagina, Uma fatia de resultados já recortada pelo banco, com o que a navegação precisa., Uma página existe mesmo quando está vazia. Sem isto, `__len__` fazia `{% if…, `__len__` fazia `{% if pagina %}` ser falso numa página sem itens, escondendo…, test_pagina_vazia_ainda_mostra_a_navegacao()

### Community 37 - "PagamentoDAO"
Cohesion: 0.05
Nodes (39): cadastrar_pagamento(), forma_pagamento_aceita(), mensalidade_destaque(), PagamentoDAO, Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.…, Vazio, uma forma do painel ou a que a mensalidade já tem. Sem a última opção,…, Escolhe a mensalidade mais relevante para o card 'Minha mensalidade': a mais…, True se já existe um Pix ou um checkout válido emitido para esta cobrança.… (+31 more)

### Community 38 - "seo.py"
Cohesion: 0.18
Nodes (18): conteudo_robots(), conteudo_sitemap(), dados_estruturados_academia(), _dia(), _dias_da_linha(), _hora(), horarios_estruturados(), origem_publica() (+10 more)

### Community 39 - "URLPublicaInvalida"
Cohesion: 0.10
Nodes (29): _enviar_em_segundo_plano(), E-mail COM token (recuperação, confirmação): não pode ir para a `fila_email`. A…, recuperar_senha(), solicitar_troca_email(), route, verificar_email_cadastro(), aluno_do_token(), ConviteIndisponivel (+21 more)

### Community 40 - "varredura.mjs"
Cohesion: 0.11
Nodes (23): aberto(), ACESSO, auditar(), { chromium }, CONF, confirmacoes(), crc, CREDS (+15 more)

### Community 41 - "test_pagamento_recusado.py"
Cohesion: 0.28
Nodes (20): _assinar(), _data_mp(), _eventos(), _mockar_mp(), _pagamento_mp(), _pix_criado(), Mensalidade recusada: a próxima tentativa do aluno a reabre, e a recusa antiga…, Mensalidade cujo cartão acabou de ser recusado no Checkout Pro. (+12 more)

### Community 43 - "ui.html"
Cohesion: 0.10
Nodes (26): campoDuracao, campoPreco, formularioPlano, cartao_plano(), secao_planos(), estado_vazio(), interruptor(), metrica() (+18 more)

### Community 44 - "turma_bp.py"
Cohesion: 0.12
Nodes (27): _acesso_permitido(), desmatricular_aluno(), detalhe_turma(), foto_professor(), matricular_aluno(), painel_professor(), limit, route (+19 more)

### Community 45 - "test_observabilidade.py"
Cohesion: 0.18
Nodes (18): before_breadcrumb(), before_send(), iniciar_sentry(), _limpar(), mascarar(), Rastreamento de erros opcional com Sentry. Sem `SENTRY_DSN`, nada é importado…, _evento(), fixture (+10 more)

### Community 46 - "test_analytics.py"
Cohesion: 0.14
Nodes (20): _carrega_analytics(), com_analytics(), _csp_com_google(), _evento(), fixture, parametrize, GA4 opcional (servicos/analytics.py): nada sem ANALYTICS_ID, nunca em área…, sem_analytics_por_padrao() (+12 more)

### Community 47 - "requirements.txt (dependências de produção)"
Cohesion: 0.12
Nodes (19): requirements.txt (dependências de produção), cryptography 50.0.1, requirements-dev.txt (requirements.txt + pytest + pip-audit), pip-audit 2.10.1, pytest, Flask 3.1.3, Flask-Limiter[redis] 4.1.1, Flask-Migrate 4.1.0 (+11 more)

### Community 48 - "admin_requerido"
Cohesion: 0.22
Nodes (18): callback(), conectar(), desconectar(), limit, route, _voltar(), _autorizacao_valida(), callback() (+10 more)

### Community 49 - "criar_pagamento"
Cohesion: 0.08
Nodes (55): criar_pagamento(), logar_como_aluno(), _mockar_preferencia(), parametrize, Um boleto pendente do Checkout Pro grava provider_payment_id, mas não é Pix:…, _resposta_preferencia(), test_abertura_json_navega_sem_redirecionar_post_externo(), test_admin_tambem_pode_abrir_checkout() (+47 more)

### Community 50 - "pagina_cadastro"
Cohesion: 0.10
Nodes (29): cadastrar_aluno(), Matrícula feita pela administração, sem conta de acesso. Pede só o que…, ativar_acesso(), _cadastro_recebido(), _em_segundo_plano(), pagina_cadastro(), Post/Redirect/Get para a página de obrigado. Cadastro novo, CPF já cadastrado e…, Transforma um cadastro feito no balcão na conta do próprio aluno. Quem chega… (+21 more)

### Community 51 - "analytics.js"
Cohesion: 0.14
Nodes (12): analytics_ativo(), id_analytics(), marcar_conversao_cadastro(), Google Analytics 4 opcional, só em página pública e só com consentimento. Sem…, Chamada no arranque: um ID malformado derruba a subida, como as demais…, Esta resposta pode carregar o GA4? Visitante, página pública indexável ou…, validar_configuracao(), apagarCookiesGa() (+4 more)

### Community 52 - "package.json"
Cohesion: 0.05
Nodes (38): dependencies, maath, react, react-dom, @react-three/drei, @react-three/fiber, scrolly-video, three (+30 more)

### Community 53 - "Academia"
Cohesion: 0.12
Nodes (21): configuracoes(), _pagina(), route, O administrador foi ao Mercado Pago e a autorização não voltou para cá? O state…, tentativa_sem_retorno(), editar_professor(), Academia, link_email() (+13 more)

### Community 54 - "Strix Cloud (managed, no local infra)"
Cohesion: 0.12
Nodes (15): 0. Credits & top-ups, 1. Register the target as an asset, 2. Launch a scan, 3. Wait for completion, 4. Read findings, 5. Export & report, 6. PR reviews, 7. Continuous testing (schedules & webhooks) (+7 more)

### Community 55 - "salvar_foto_perfil"
Cohesion: 0.10
Nodes (31): ArmazenamentoIndisponivel, ler_arquivo(), _nome_valido(), O nome sempre é o UUID gerado por esta camada, nunca um valor vindo da…, Valida, reprocessa e salva uma foto de perfil. Retorna o nome do arquivo…, Conteúdo de um arquivo já salvo, ou None se não existir, for inválido ou o…, Melhor esforço: um arquivo que sobra não quebra nada, então falha só vai para o…, O arquivo era válido, mas o Storage não aceitou guardá-lo agora. Herda de… (+23 more)

### Community 56 - "layouts/admin.html — layout do painel administrativo"
Cohesion: 0.23
Nodes (9): Protocolo data-confirm-modal, layouts/admin.html — layout do painel administrativo, Diálogo de confirmação central (form[data-confirm-modal]), layouts/base.html — esqueleto comum das páginas, Layouts por área sobre o esqueleto base, Ordem de carregamento no head, Política de SEO por layout (título, descrição, robots), Proteção CSRF (meta csrf-token + csrf_field) (+1 more)

### Community 57 - "Serviço app (Flask com Gunicorn na porta 5000)"
Cohesion: 0.44
Nodes (9): compose.yaml (Docker Compose: db, rate-limit, app, backup, https), Serviço app (Flask com Gunicorn na porta 5000), Serviço backup (pg_dump diário, retenção 7 + 4), Serviço db (postgres:17-alpine), Serviço https (Caddy 2.9), Serviço rate-limit (redis:7-alpine, volatile-ttl, 64 MB), Dependabot (atualizações semanais de dependências), Atualização das imagens do compose (postgres, redis, caddy) (+1 more)

### Community 58 - "test_prontidao.py"
Cohesion: 0.14
Nodes (5): banco_fora(), fixture, /health/pronto: 503 quando banco ou Redis caem, sem expor detalhe nem criar…, Cada chamada consulta banco e Redis: 60 por minuto bastam ao monitor externo., test_pronto_tem_limite_por_ip()

### Community 59 - "pix.js"
Cohesion: 0.33
Nodes (14): abrirPix(), alvoDoRotulo(), atualizarStatusTexto(), fecharDialog(), iniciarPolling(), lerJson(), liberarBotao(), limparConteudoAnterior() (+6 more)

### Community 60 - "test_arranque_seguranca.py"
Cohesion: 0.22
Nodes (14): _env_arranque(), Validações feitas por servidor.py no arranque (COOKIE_SECURE, TRUSTED_HOSTS,…, `python -m servicos.credenciais`: o hash sai entre aspas simples. O hash do…, Desenvolvimento local sem HTTPS (sem Caddy) não pode ficar travado., _rodar(), test_arranque_falha_com_cookie_secure_false_e_app_base_url_https(), test_arranque_falha_com_cookie_secure_invalido(), test_arranque_falha_sem_trusted_hosts() (+6 more)

### Community 61 - "revogar_sessao_atual"
Cohesion: 0.29
Nodes (8): Registra a sessão como encerrada: cópias antigas do cookie deixam de valer.…, revogar_sessao_atual(), health(), health_pronto(), logout(), exempt, limit, route

### Community 62 - "test_keep_alive.py"
Cohesion: 0.16
Nodes (7): ambiente_limpo(), fixture, parametrize, Garante que o keep-alive fica desligado por padrão e só pinga a própria origem., test_intervalo_fica_dentro_da_faixa(), test_nao_liga_com_valor_negativo(), test_ping_so_considera_200_como_sucesso()

### Community 63 - "planilha_bp.py"
Cohesion: 0.16
Nodes (23): _ler_promocao(), 80', '80.5', '80,50' ou '1.234,56' -> Decimal. None se vazio; ValueError se…, Preço promocional e período: `(campos, None)` ou `(None, erro)`. Os três campos…, _valor_em_reais(), alterar_despesa(), _ano_e_mes(), _ano_valido(), baixar_excel() (+15 more)

### Community 64 - "test_sessao_revogada.py"
Cohesion: 0.24
Nodes (11): Sessões encerradas pelo logout. A sessão do Flask é um cookie assinado, sem…, SessaoRevogada, _cliente_com_cookie(), _entrar_como_admin(), `session.clear()` só limpava o navegador de quem saiu; a cópia do cookie seguia…, test_logout_apaga_revogacoes_vencidas(), test_logout_de_uma_sessao_nao_derruba_as_outras(), test_logout_revoga_a_copia_do_cookie_feita_antes() (+3 more)

### Community 65 - "Relatório de segurança — Sistema Extreme Team"
Cohesion: 0.15
Nodes (12): Controles verificados, Histórico de auditorias, O que foi feito nesta rodada, Pendências não relacionadas a segurança, Relatório de segurança — Sistema Extreme Team, Rodada anterior (22/09/2026 — 2ª rodada), Rodada de 04/10/2026 — limites de requisição, Situação atual (20/10/2026 — hero 3D, OWASP/DevSecOps e dependências) (+4 more)

### Community 66 - "armazenamento.py"
Cohesion: 0.12
Nodes (26): ArquivoInvalido, _conferir_dimensoes(), _detectar_tipo_imagem_real(), _exif_so_com_orientacao(), _gravar(), ImagemGrandeDemais, _jpeg_sem_metadados(), _orientacao() (+18 more)

### Community 67 - "componentes.js"
Cohesion: 0.22
Nodes (7): abrir(), agendarSaida(), fecharMenu(), fecharToast(), limpar(), mostrarErro(), prepararToast()

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

### Community 72 - ".totais_periodo"
Cohesion: 0.13
Nodes (11): _paginar(), Status como o painel deve LER, com o vencimento aplicado na própria consulta. A…, Carrega aluno e plano junto das mensalidades. O template do painel lê…, Lista completa (sem paginar). Mantida para relatórios e testes., Uma página de mensalidades, recortada pelo banco (LIMIT/OFFSET). O painel…, Totais do painel financeiro - sempre calculados no backend a partir do banco,…, Aplica LIMIT/OFFSET e conta o total numa consulta separada e barata. A contagem…, test_financeiro_pagina_no_banco_sem_carregar_tudo() (+3 more)

### Community 73 - "analytics.test.cjs"
Cohesion: 0.18
Nodes (7): assert, CODIGO, Element, fs, path, test, vm

### Community 74 - "pagamento.js"
Cohesion: 0.16
Nodes (19): cancelarAberturas(), consultar(), finalizarAbertura(), parar(), alvoDoRotulo(), consultarStatus(), gerarOuAtualizarPix(), iniciarPolling() (+11 more)

### Community 75 - "admin_nav.html"
Cohesion: 0.15
Nodes (9): Abas com memória (data-tabs-lembrar), Content Security Policy (csp_nonce), window.deslizarTela(), marcar(), listener de pagereveal, SECOES (ordem das seções do menu), sentidoEntre(), View Transitions API (@view-transition) (+1 more)

### Community 76 - "test_email_componentes.py"
Cohesion: 0.33
Nodes (7): E-mails: base com a logo oficial e componentes seguros para cliente de e-mail…, _render(), _sem_recursos_externos(), test_base_sem_url_publica_cai_para_o_nome_em_texto(), test_base_usa_a_logo_quando_ha_url_publica(), test_botao_do_email_usa_o_ouro_do_sistema(), test_cartao_de_resumo_com_badge()

### Community 77 - "test_layouts.py"
Cohesion: 0.29
Nodes (8): _conferir_head_comum(), parametrize, Layouts base (templates/layouts/) e toasts. Cada página estende o layout da sua…, test_area_do_aluno_carrega_o_layout(), test_flash_de_erro_vira_toast_que_nao_some_sozinho(), test_paginas_publicas_carregam_o_head_comum(), test_painel_admin_carrega_o_layout_admin(), test_toda_pagina_estende_um_layout()

### Community 78 - "test_migracao_checkout.py"
Cohesion: 0.31
Nodes (8): _colunas(), conexao(), migracao(), fixture, Exercita a migração dos campos do Checkout Pro de verdade (upgrade e…, _rodar(), test_downgrade_remove_exatamente_o_que_o_upgrade_criou(), test_upgrade_adiciona_as_colunas_e_preserva_linhas_antigas()

### Community 79 - "test_limites_pagamento.py"
Cohesion: 0.15
Nodes (15): consultar_mp(), fixture, parametrize, Limites de pagamento por conta, com o provedor inteiramente simulado., _sessao_aluno(), test_admin_limite_por_usuario_persiste_entre_sessoes(), test_alunos_no_mesmo_ip_tem_limites_separados(), test_anonimos_limitados_por_ip_sem_consultar_provedor() (+7 more)

### Community 80 - "checkout_abertura.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 81 - "pagamento_polling.test.cjs"
Cohesion: 0.22
Nodes (6): assert, criarPagina(), fs, path, test, vm

### Community 82 - "test_publicas_redesign.py"
Cohesion: 0.20
Nodes (3): _cabecalho(), test_admin_logado_vai_da_home_para_o_painel(), test_aluno_logado_vai_da_home_direto_para_a_area_do_aluno()

### Community 83 - "env.py"
Cohesion: 0.39
Nodes (7): get_engine(), get_engine_url(), get_metadata(), Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online()

### Community 84 - "test_formatos_de_imagem.py"
Cohesion: 0.26
Nodes (10): disco_temporario(), _imagem(), parsers_proibidos(), fixture, parametrize, Upload de foto e comprovante: o Pillow só interpreta JPEG, PNG e WebP. As…, Falha o teste se o parser de GIF ou TIFF for chamado., test_comprovante_em_outro_formato_e_recusado_sem_passar_pelo_parser() (+2 more)

### Community 85 - "_png_bomba"
Cohesion: 0.29
Nodes (7): _png_bomba(), Bomba de descompressão: arquivo minúsculo, imagem gigante. O PNG aqui tem 285…, PNG válido e altamente compressível: linhas zeradas, como uma bomba real., O teto de pixels vale para a FOTO, que é decodificada, não para o comprovante.…, test_comprovante_a4_escaneado_continua_sendo_aceito(), test_foto_de_perfil_mantem_o_teto_de_pixels(), test_png_com_pixels_demais_e_recusado_pelo_cabecalho()

### Community 86 - "MatriculaDAO"
Cohesion: 0.14
Nodes (21): pagina_login(), MatriculaDAO, Matricula, Presenca, impressao_credencial(), iniciar_sessao(), Grava na sessão atual a credencial em vigor (login ou troca de senha bem-…, Dá um identificador à sessão recém-aberta, para o logout poder revogá-la.… (+13 more)

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

### Community 93 - "seo_bp.py"
Cohesion: 0.67
Nodes (3): route, robots(), sitemap()

### Community 95 - "d9e2f6a14c80_contatos_academia_perfis_professores.py"
Cohesion: 0.83
Nodes (3): _campos_professor(), downgrade(), upgrade()

### Community 97 - "vercel.json"
Cohesion: 0.50
Nodes (3): gru1, regions, $schema

### Community 98 - "MercadoPagoIndisponivel"
Cohesion: 0.08
Nodes (46): _base_url_opcional(), base_url_publica(), buscar_pagamento(), buscar_pagamentos_por_referencia(), cancelar_pagamento(), criar_pagamento_pix(), criar_preferencia_checkout(), _erro_menciona() (+38 more)

### Community 99 - "backup.sh"
Cohesion: 1.00
Nodes (3): registrar(), reter(), backup.sh script

### Community 114 - "capturar_emails"
Cohesion: 0.67
Nodes (3): capturar_emails(), fixture, Intercepta o envio e devolve os e-mails que teriam saído, com os links.

### Community 116 - "config.py"
Cohesion: 0.15
Nodes (15): cadastrar_turma(), TurmaDAO, Turma, Sonda: a data vem da query string e é convertida sem tratamento., test_data_invalida_na_turma_nao_derruba_a_rota(), test_area_do_aluno_renderiza_telas_independentes_do_menu(), test_escolher_plano_com_turma_cria_matricula(), test_plano_atual_continua_disponivel_para_gerar_cobranca() (+7 more)

### Community 117 - "test_perfil_e_foto.py"
Cohesion: 0.36
Nodes (7): _imagem_jpeg_valida(), test_admin_acessa_foto_de_qualquer_aluno(), test_aluno_nao_acessa_foto_de_outro_aluno(), test_aluno_ve_o_proprio_perfil(), test_professor_ve_foto_de_aluno_da_propria_turma(), test_substituir_e_remover_foto(), test_upload_de_foto_valida()

### Community 122 - "Contrato do redesign — SistemaEXTREMETEAM"
Cohesion: 0.09
Nodes (20): 0. Antes de escrever código, 1. Identidade visual (design tokens), 2. Logo oficial (usar SOMENTE a logo original), 3. Telas a implementar, 4. Regras e dados, 5. Forma de trabalhar, Painel administrativo (desktop, sidebar preta com o emblema do dragão), Prompt para o Claude Code — Redesign do SistemaEXTREMETEAM (+12 more)

### Community 123 - "planilha.py"
Cohesion: 0.12
Nodes (17): Despesa, Saídas de caixa lançadas pelo admin (aluguel, luz, salários...). As entradas da…, anos_disponiveis(), Categoria, data_da_entrada(), _decimal(), _entradas(), entradas_detalhadas() (+9 more)

### Community 124 - "cinema.test.cjs"
Cohesion: 0.11
Nodes (10): assert, CODIGO, conferirAtiva(), Elemento, fs, ListaDeClasses, montar(), path (+2 more)

### Community 125 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, isolatedModules, jsx, lib, module, moduleResolution, noEmit, noUnusedLocals (+10 more)

### Community 127 - "penetration-testing-with-strix/SKILL.md"
Cohesion: 0.18
Nodes (10): Exit codes (headless), Option A — Open-source CLI (self-hosted), Option B — Managed cloud (no local infra), Prerequisites, Reading results, Reporting & next steps, Run a Strix pentest, Running a scan (+2 more)

### Community 128 - "test_cinema.py"
Cohesion: 0.20
Nodes (10): _html(), Hero cinematográfico da home e profundidade (tilt) dos cartões. O hero guarda…, _secao_cinema(), test_cartoes_do_metodo_na_home_inclinam(), test_cena_aponta_para_a_entrada_compilada_com_hash(), test_hero_tem_cadastro_seta_para_os_planos_e_poster(), test_manchetes_ficam_no_html_e_so_a_primeira_e_visivel(), test_sem_build_a_home_fica_so_com_o_poster() (+2 more)

### Community 129 - "SistemaEXTREMETEAM"
Cohesion: 0.11
Nodes (18): Comprovante manual (dinheiro/transferência), Configuração de e-mail, Configuração de segurança, Contatos da academia e equipe, Credencial do administrador, Erros no Sentry (opcional), Foto de perfil e comprovante manual (armazenamento de arquivos), Google Analytics 4 (opcional, com consentimento) (+10 more)

### Community 130 - "test_paginas_erro.py"
Cohesion: 0.17
Nodes (5): csrf_ligado(), fixture, Página de erro (templates/erro.html) e os handlers de 404, 403, 500 e CSRF., test_404_para_quem_esta_logado_leva_a_area_dele(), test_500_mostra_a_pagina_de_erro()

### Community 131 - "test_mercado_pago_oauth_postgres.py"
Cohesion: 0.25
Nodes (5): postgres_mp(), fixture, Renovação do token OAuth com trava de linha real, opcional na suíte que usa…, _Resposta, test_dois_processos_perto_do_vencimento_gastam_o_refresh_token_uma_vez()

### Community 132 - "test_email_gmail.py"
Cohesion: 0.29
Nodes (4): aplicativo_google(), fixture, test_envia_pelo_gmail_com_o_refresh_token_da_conexao(), test_refresh_token_fica_cifrado_no_banco()

### Community 133 - "Pagamento de mensalidade via Pix (Mercado Pago)"
Cohesion: 0.22
Nodes (9): Como obter credenciais de teste (modo manual, sem OAuth), Como testar localmente, Conectar a conta por OAuth (a academia não cria aplicativo), Instalar dependências, Pagamento de mensalidade via Pix (Mercado Pago), Produção, Trocando de credenciais de teste para produção, URL a cadastrar como webhook (+1 more)

### Community 134 - "test_google_login.py"
Cohesion: 0.09
Nodes (23): Esquece a conta conectada. Devolve True se havia uma., remover_conexao(), fixture, Registra as chamadas e devolve as respostas configuradas por método., storage(), _StorageFalso, cliente_google(), google() (+15 more)

### Community 135 - "cinema.py"
Cohesion: 0.31
Nodes (8): _entradas(), modulo(), Arquivos do hero cinematográfico da página inicial. A cena 3D é compilada pelo…, {nome da entrada: arquivo}, lido uma vez: o build não muda com o servidor no ar., URL da entrada `nome` ('cena' ou 'video') do build, ou None se não foi…, URL do vídeo do hero, só se ele existir e a entrada que o toca estiver…, _tem_video(), video()

### Community 136 - "Skills Disponíveis"
Cohesion: 0.22
Nodes (8): Assistente e Automação (Antigravity), Ciências e Bioinformática (Plugins de Ciência), Dados e Google Cloud Platform (GCP), Desenvolvimento Mobile e Flutter/Dart, Desenvolvimento Web e Frontend, Firebase e Backend, GenAI e Machine Learning, Skills Disponíveis

### Community 137 - "test_migracao_conexao_mercado_pago.py"
Cohesion: 0.83
Nodes (3): _migracao(), test_migracao_cria_a_tabela_igual_ao_modelo_e_e_reentrante(), test_migracao_encadeia_na_ultima_revisao_existente()

### Community 138 - "cinema.js"
Cohesion: 0.43
Nodes (5): ativar(), carregarCena(), medir(), pedirMedida(), podeTer3D()

### Community 139 - "Etapa 1 — migrar páginas para os layouts (SEM mudar o visual)"
Cohesion: 0.29
Nodes (6): Conferência (agentes Claude), Divisão, Etapa 1 — migrar páginas para os layouts (SEM mudar o visual), O que já existe (não edite), Receita por página, Relatório (curto)

### Community 140 - "Etapas 4 a 6 — aluno, admin, professor (aplicar os componentes nas páginas)"
Cohesion: 0.29
Nodes (6): Agente A — área do aluno + pagamento, Agente B — admin, Antigravity — financeiro, turmas, professor, Etapas 4 a 6 — aluno, admin, professor (aplicar os componentes nas páginas), Orquestrador (Claude), Regras para todos

### Community 142 - "Banco de dados e migrations"
Cohesion: 0.33
Nodes (6): Backup automático (serviço `backup` do compose), Backup e restauração, Banco criado pela versão antiga, Banco de dados e migrations, Produção no Supabase, Restauração

### Community 143 - "Etapa 2 — biblioteca de componentes"
Cohesion: 0.33
Nodes (5): Entregas e arquivos exclusivos, Etapa 2 — biblioteca de componentes, Ganchos de JS (Claude escreve `static/js/componentes.js`; markup e CSS usam EXATAMENTE isto), Macros (Agente A), cada uma no seu arquivo em `templates/components/`, Regras visuais (REDESIGN_CONTRATO.md seção 2 — leia)

### Community 144 - "Cadastro de aluno pela administração e ativação de acesso"
Cohesion: 0.40
Nodes (5): Ativar o acesso depois, Cadastro de aluno pela administração e ativação de acesso, Confirmar senha, Matricular no balcão, Migração e configuração

### Community 145 - "Outras formas de pagamento (Checkout Pro)"
Cohesion: 0.40
Nodes (5): Fluxo, Limitações conhecidas, Outras formas de pagamento (Checkout Pro), Passos manuais no painel do Mercado Pago, Reuso de preferência

### Community 147 - "Etapa 3 — home com os planos + termos"
Cohesion: 0.40
Nodes (4): Agente A — `templates/index.html` e `static/css/index.css`, Antigravity — `termos_de_servico.html`, `politica_privacidade.html`, `termos_responsabilidade.html` + `static/css/termos.css` (novo), Dados da home (Claude entrega em servidor.py — não edite), Etapa 3 — home com os planos + termos

### Community 148 - "test_fontes_locais.py"
Cohesion: 0.25
Nodes (3): parametrize, Fontes servidas pelo próprio site (SEC-18). Com o Google Fonts, o navegador de…, test_csp_nao_libera_o_google_fonts()

### Community 149 - "Biblioteca no Figma"
Cohesion: 0.50
Nodes (3): Biblioteca no Figma, Falta (ordem de retomada), Limites do plano Starter que moldaram o arquivo

### Community 151 - "google_login.py"
Cohesion: 0.33
Nodes (9): _autorizacao_valida(), callback(), login_google(), _novo_pkce(), limit, route, (code_verifier, code_challenge S256), como na conexão do Mercado Pago. O state…, O state devolvido é o que ESTA sessão emitiu, há pouco tempo? (+1 more)

### Community 152 - "Professor"
Cohesion: 0.09
Nodes (26): cadastrar_professor(), gerenciar_turmas(), remover_professor(), ProfessorDAO, Professor, logar_como_professor(), fixture, Hipótese: a foto continua acessível por URL depois de tirar a publicação. (+18 more)

### Community 157 - "auth.test.cjs"
Cohesion: 0.25
Nodes (6): assert, CODIGO, fs, path, test, vm

### Community 158 - "credenciais.py"
Cohesion: 0.20
Nodes (11): admin_configurado(), comparar_em_tempo_constante(), credencial_admin_confere(), gerar_hash_admin(), _main(), Credencial administrativa baseada exclusivamente em hash de senha. O…, Compara duas senhas em tempo constante, sem restrição de alfabeto. Codificar…, True quando existe usuário e hash da senha do administrador. (+3 more)

### Community 159 - "test_admin_mercado_pago.py"
Cohesion: 0.18
Nodes (14): _aprovado_no_checkout(), Painel do admin com mensalidades do Mercado Pago: formas de pagamento,…, Cartão/boleto: a preferência existe, o webhook ainda não trouxe o payment_id., _so_com_checkout(), test_admin_muda_o_status_sem_perder_a_forma_do_mercado_pago(), test_admin_nao_grava_forma_inventada(), test_aprovar_comprovante_recusa_forma_inventada(), test_ficha_mantem_no_select_a_forma_confirmada_pelo_mercado_pago() (+6 more)

### Community 160 - "keep_alive.py"
Cohesion: 0.29
Nodes (9): iniciar(), _intervalo(), _laco(), _ligado(), parar(), _pingar(), Mantém a aplicação acordada em hospedagens que hibernam por inatividade. Uma…, Encerra o laço. Usado pelos testes; em produção a thread é daemon. (+1 more)

### Community 161 - "ci-security-scanning-with-strix/SKILL.md"
Cohesion: 0.29
Nodes (6): GitHub Actions, Option A — Self-hosted OSS CLI in the runner, Option B — Managed platform (no runner infra), Optional: upload findings to GitHub code scanning, Other CI systems, Set up Strix in CI/CD

### Community 162 - "test_conversao_home.py"
Cohesion: 0.19
Nodes (14): _body_tag(), _html(), parametrize, Conversão na home: perguntas frequentes, CTA fixo no celular e página de…, test_admin_logado_nao_ve_o_cta_fixo(), test_aluno_logado_nao_ve_o_cta_fixo(), test_cta_fixo_fica_so_na_home(), test_cta_fixo_sem_whatsapp_so_tem_o_cadastro() (+6 more)

### Community 164 - "Find security vulnerabilities in code"
Cohesion: 0.29
Nodes (6): Complementary tooling, Find security vulnerabilities in code, Fix and verify, Read the results, Reviewing a pull request instead of the whole repo, Run it

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

## Ambiguous Edges - Review These
- `botao_google.html` → `Integração com o Gmail (conta remetente da academia)`  [AMBIGUOUS]
  templates/politica_privacidade.html · relation: conceptually_related_to

## Knowledge Gaps
- **322 isolated node(s):** `name`, `private`, `version`, `description`, `type` (+317 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `botao_google.html` and `Integração com o Gmail (conta remetente da academia)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `PagamentoDAO` connect `PagamentoDAO` to `Aluno`, `adm_bp.py`, `.buscar_por_id`, `logar_como_admin`, `usuario_bp.py`, `test_regressao_auditoria.py`, `test_auditoria_seguranca.py`, `financeiroDAO.py`, `pix_bp.py`, `criar_aluno`, `test_seguranca.py`, `test_pix_rotas.py`, `Plano`, `test_admin_mercado_pago.py`, `test_mudanca_plano.py`, `checkout_bp.py`, `test_pagamento_recusado.py`, `criar_pagamento`, `pagina_cadastro`, `.totais_periodo`, `MatriculaDAO`, `test_comprovante_sem_metadados.py`, `config.py`?**
  _High betweenness centrality (0.108) - this node is a cross-community bridge._
- **Why does `Vitrine de componentes (/_vitrine)` connect `csrf_field.html` to `layouts/admin.html — layout do painel administrativo`, `ui.html`, `config.py`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Why does `AlunoDAO` connect `logar_como_admin` to `Aluno`, `PagamentoDAO`, `adm_bp.py`, `usuario_bp.py`, `PlanoDAO`, `turma_bp.py`, `test_regressao_auditoria.py`, `pagina_cadastro`, `config.py`, `test_perfil_e_foto.py`, `MatriculaDAO`, `criar_aluno`, `test_seguranca.py`, `Plano`, `.contar_cadastrados`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Are the 158 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 158 INFERRED edges - model-reasoned connections that need verification._
- **Are the 168 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 168 INFERRED edges - model-reasoned connections that need verification._
- **Are the 165 inferred relationships involving `logar_como_admin()` (e.g. with `test_admin_salva_atualiza_e_limpa_contatos()` and `test_csrf_configuracoes()`) actually correct?**
  _`logar_como_admin()` has 165 INFERRED edges - model-reasoned connections that need verification._