# Graph Report - SistemaEXTREMETEAM  (2026-10-27)

## Corpus Check
- 216 files · ~281,470 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3082 nodes · 7215 edges · 179 communities (165 shown, 14 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 1301 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c0d88043`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Aluno
- Componentes
- test_admin_segundo_fator.py
- planos.py
- test_seo.py
- adm_bp.py
- turma_bp.py
- AlunoDAO
- SituacaoPlano
- route
- test_admin_mercado_pago.py
- financeiro.html — painel financeiro
- index.html (home pública)
- PagamentoDAO
- test_regressao_auditoria.py
- fase3b.js
- test_auditoria_seguranca.py
- test_limites_pagamento.py
- fila_email.py
- csrf_field.html
- salvar_foto_perfil
- gmail_conta.py
- pix_bp.py
- servidor.py
- criar_aluno
- test_turnstile.py
- mercado_pago_conta.py
- test_seguranca.py
- test_pix_rotas.py
- test_fila_email_concorrencia_postgres.py
- planilha_excel.py
- checkout_bp.py
- test_mudanca_plano.py
- ui.html
- test_mercado_pago_servico.py
- test_limites_requisicao.py
- Pagina
- cartao_do_plano
- PlanoDAO
- URLPublicaInvalida
- varredura.mjs
- test_pagamento_recusado.py
- test_mercado_pago_oauth_postgres.py
- avatar
- admin_requerido
- test_observabilidade.py
- test_analytics.py
- requirements.txt (dependências de produção)
- planilha_bp.py
- criar_pagamento
- test_planilha_economica.py
- analytics.js
- package.json
- test_home_planos.py
- Strix Cloud (managed, no local infra)
- autorizacao.py
- deslize.html
- Serviço app (Flask com Gunicorn na porta 5000)
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
- MercadoPagoIndisponivel
- _tem_limite
- test_email_componentes.py
- test_layouts.py
- test_migracao_checkout.py
- Academia
- checkout_abertura.test.cjs
- pagamento_polling.test.cjs
- test_publicas_redesign.py
- env.py
- armazenamento.py
- turnstile.py
- MatriculaDAO
- shot.mjs
- c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py
- cena.tsx
- test_comprovante_sem_metadados.py
- 896e70afc9c5_adiciona_foto_e_graduacao_do_aluno_.py
- test_migracao_cadastro_administrativo.py
- academia_bp.py
- a1f0c3e75b92_schema_inicial.py
- d9e2f6a14c80_contatos_academia_perfis_professores.py
- e4b7c2a91d35_cadastro_administrativo_e_convite_de_acesso.py
- vercel.json
- mercado_pago.py
- backup.sh
- capturar_emails
- gerar_imagem_og.py
- logar_como_admin
- _png_bomba
- agendar.sh
- restaurar.sh
- Contrato do redesign — SistemaEXTREMETEAM
- planilha.py
- cinema.test.cjs
- compilerOptions
- pgUsuario.html (área do aluno)
- penetration-testing-with-strix/SKILL.md
- test_cinema.py
- SistemaEXTREMETEAM
- test_paginas_erro.py
- EmailPendente
- verificar_email_cadastro
- Pagamento de mensalidade via Pix (Mercado Pago)
- formatar_competencia
- cinema.py
- Skills Disponíveis
- test_perfil_e_foto.py
- cinema.js
- Etapa 1 — migrar páginas para os layouts (SEM mudar o visual)
- Etapas 4 a 6 — aluno, admin, professor (aplicar os componentes nas páginas)
- emblema.py
- Banco de dados e migrations
- Etapa 2 — biblioteca de componentes
- Cadastro de aluno pela administração e ativação de acesso
- Outras formas de pagamento (Checkout Pro)
- usuario_bp.py
- Etapa 3 — home com os planos + termos
- test_fontes_locais.py
- Biblioteca no Figma
- CLAUDE.md
- home
- Configuração de segurança
- seo_bp.py
- test_logs_sem_dado_pessoal.py
- auth.test.cjs
- credenciais.py
- .buscar_por_id
- TransporteEmMemoria
- ci-security-scanning-with-strix/SKILL.md
- _Resposta
- _FakePaymentResource
- Find security vulnerabilities in code
- test_mercado_pago_oauth.py
- .listar_paginado
- Security-test an API
- Application security testing
- imagens.d.ts
- Fix Strix findings and verify
- Test against the OWASP Top 10
- Pentest a web application
- README.md
- cobranca_pendente
- test_financeiro_admin_painel.py
- test_migracao_conexao_mercado_pago.py
- .contar_cadastrados
- limites_pagamento.py

## God Nodes (most connected - your core abstractions)
1. `PagamentoDAO` - 230 edges
2. `criar_aluno()` - 172 edges
3. `logar_como_admin()` - 171 edges
4. `criar_pagamento()` - 164 edges
5. `logar_como_aluno()` - 137 edges
6. `AlunoDAO` - 93 edges
7. `Aluno` - 74 edges
8. `PlanoDAO` - 69 edges
9. `MercadoPagoIndisponivel` - 45 edges
10. `Professor` - 41 edges

## Surprising Connections (you probably didn't know these)
- `Vitrine de planos da home (secao_planos com vitrine_planos)` --references--> `cartao_do_plano()`  [INFERRED]
  templates/index.html → servicos/planos.py
- `test_limite_de_login_por_ip_e_identificador()` --uses--> `AlunoDAO`  [INFERRED]
  tests/test_seguranca.py → dao/usuarioDAO.py
- `contar_falhados()` --uses--> `EmailPendente`  [INFERRED]
  servicos/fila_email.py → modelos/email_pendente.py
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

## Communities (179 total, 14 thin omitted)

### Community 0 - "Aluno"
Cohesion: 0.08
Nodes (17): _convidar_cadastro_existente(), _convidar_cadastro_existente_por_id(), Cadastro administrativo que alguém tentou recriar pelo formulário público. Em…, Versão para thread de fundo: a sessão da requisição não vale fora dela., Matrícula feita no balcão: sem login, sem senha e sem convite de acesso. Nasce…, Aluno, Se existe uma conta de acesso, e não se o aluno está em dia ou matriculado.…, Convite de acesso já enviado e ainda não usado (a validade é checada na rota). (+9 more)

### Community 1 - "Componentes"
Cohesion: 0.05
Nodes (36): Altura de controle, Avisos flutuantes, Botões — `.et-botao` + variante (+ tamanho), Cartões e contêineres, Componentes, Contêiner e estrutura, Cores, Dados (+28 more)

### Community 2 - "test_admin_segundo_fator.py"
Cohesion: 0.20
Nodes (20): _codigo_agora(), _codigo_errado(), _destino(), _entrar_com_senha(), fixture, parametrize, Segundo fator do administrador (SEC-30). Com ADMIN_TOTP_SECRET definida, a…, segundo_fator() (+12 more)

### Community 3 - "planos.py"
Cohesion: 0.19
Nodes (17): cadeia_paga(), esta_inadimplente(), fim_periodo_comprometido(), inicio_proximo_periodo(), intervalo_vigencia(), periodo_para_nova_cobranca(), plano_do_ultimo_periodo(), Regras de vigência do plano do aluno. Uma mensalidade paga cobre um intervalo… (+9 more)

### Community 4 - "test_seo.py"
Cohesion: 0.07
Nodes (43): conteudo_robots(), conteudo_sitemap(), dados_estruturados_academia(), _dia(), _dias_da_linha(), _hora(), horarios_estruturados(), origem_publica() (+35 more)

### Community 5 - "adm_bp.py"
Cohesion: 0.08
Nodes (54): aprovar_aluno(), aprovar_comprovante_manual(), arquivar_plano(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_aluno(), cadastrar_pagamento(), cadastrar_plano() (+46 more)

### Community 6 - "turma_bp.py"
Cohesion: 0.14
Nodes (18): _acesso_permitido(), cadastrar_professor(), cadastrar_turma(), desmatricular_aluno(), detalhe_turma(), gerenciar_turmas(), matricular_aluno(), painel_professor() (+10 more)

### Community 7 - "AlunoDAO"
Cohesion: 0.11
Nodes (46): _aluno_do_cpf_ou_painel(), Aluno de uma rota administrativa, ou None (a rota redireciona ao painel)., remover_foto_aluno(), AlunoDAO, _matricular(), parametrize, Cadastro de aluno pela administração, ativação de acesso e confirmação de…, test_admin_lanca_e_baixa_mensalidade_de_aluno_sem_acesso() (+38 more)

### Community 8 - "SituacaoPlano"
Cohesion: 0.10
Nodes (8): Retrato completo da situação do plano do aluno em uma data. Objeto de leitura,…, Último dia de acesso já pago, somando as renovações antecipadas., Fim só do período em curso - o que a troca de plano tem de preservar., Renovação já paga que começa depois do período atual, quando existe., Existe uma cobrança que o aluno pode quitar agora., Pode antecipar o próximo período: só quando nada está em aberto nem em decisão…, Só faz sentido agendar a troca quando existe um período pago correndo: sem…, SituacaoPlano

### Community 9 - "route"
Cohesion: 0.11
Nodes (31): _abrir_sessao_admin(), _acesso_permitido_pagamento(), alterar_senha_perfil(), _aluno_da_sessao(), _aluno_por_token(), atualizar_dados_perfil(), cadastro_obrigado(), cancelar_mudanca_plano() (+23 more)

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
Cohesion: 0.06
Nodes (40): mensalidade_destaque(), PagamentoDAO, Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.…, Status como o painel deve LER, com o vencimento aplicado na própria consulta. A…, Carrega aluno e plano junto das mensalidades. O template do painel lê…, Lista completa (sem paginar). Mantida para relatórios e testes., Uma página de mensalidades, recortada pelo banco (LIMIT/OFFSET). O painel…, Totais do painel financeiro - sempre calculados no backend a partir do banco,… (+32 more)

### Community 14 - "test_regressao_auditoria.py"
Cohesion: 0.04
Nodes (48): _chave_lote(), Identidade de um aviso: o conteúdo MAIS o dia. Só o conteúdo não serve. Um…, _contar_selects_em_alunos(), _credencial(), Regressões da auditoria de segurança, desempenho e confiabilidade. Cada caso…, Head-of-line blocking: a primeira linha falhando não pode impedir as seguintes.…, Uma linha `desistiu` nunca foi entregue: recusar o reenvio fazia a tela dizer…, A revivência vale só para o abandonado: clique duplo continua virando um envio. (+40 more)

### Community 15 - "fase3b.js"
Cohesion: 0.06
Nodes (47): avisos, bind(), caixas, campos, col(), D(), estados, faixa (+39 more)

### Community 16 - "test_auditoria_seguranca.py"
Cohesion: 0.06
Nodes (49): _agora_mercado_pago(), _assinar(), logar_como_professor(), _pagamento_mp(), _preparar_para_conciliacao(), fixture, parametrize, Auditoria de segurança: sondas escritas para TENTAR quebrar as regras. Nenhum… (+41 more)

### Community 17 - "test_limites_pagamento.py"
Cohesion: 0.13
Nodes (18): Valor que representa a credencial administrativa em vigor, ou None se não há…, referencia_credencial_admin(), consultar_mp(), fixture, parametrize, Limites de pagamento por conta, com o provedor inteiramente simulado., _sessao_admin(), _sessao_aluno() (+10 more)

### Community 18 - "fila_email.py"
Cohesion: 0.10
Nodes (25): espera_da_proxima_tentativa(), Fila de e-mails no banco. Aviso e cobrança coletivos saíam um a um dentro da…, contar_falhados(), contar_pendentes(), disparar(), enfileirar(), enfileirar_transacional(), _entregar() (+17 more)

### Community 19 - "csrf_field.html"
Cohesion: 0.13
Nodes (20): Contato e localização da academia, ativar_acesso.html — ativar acesso pelo convite, cadastro.html — criar conta, cadastro_obrigado.html — cadastro recebido, Cadastro com PRG e resposta única, Aceite do Termo de Responsabilidade, Modal de login da home (#meuModal, POST /login), layouts/publico.html — layout das telas públicas (+12 more)

### Community 20 - "salvar_foto_perfil"
Cohesion: 0.10
Nodes (36): enviar_foto_aluno(), ArmazenamentoIndisponivel, _gravar(), ler_arquivo(), _nome_valido(), _pasta(), _raiz_uploads(), (URL base do bucket, cabeçalhos) do Supabase Storage, ou None para gravar em… (+28 more)

### Community 21 - "gmail_conta.py"
Cohesion: 0.06
Nodes (42): GmailConexao, _access_token(), _cifrar(), _client_id(), _client_secret(), _decifrar(), enviar(), estado() (+34 more)

### Community 22 - "pix_bp.py"
Cohesion: 0.07
Nodes (42): _acesso_permitido(), _chave_entrega_webhook(), criar_pix_mensalidade(), _data_da_aprovacao(), _forma_pagamento_confirmada(), _instante_utc(), _iso_utc(), _liberar_entrega_webhook() (+34 more)

### Community 23 - "servidor.py"
Cohesion: 0.14
Nodes (20): after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, context_processor, errorhandler, formatar_moeda(), Formata um valor em reais no padrão brasileiro: R$ 1.080,00. Usado como filtro…, acesso_negado() (+12 more)

### Community 24 - "criar_aluno"
Cohesion: 0.11
Nodes (39): Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, Com uma troca já agendada, só dois planos fazem sentido num pedido de…, A cobrança do período seguinte tem de nascer no plano que o aluno agendou.…, `pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -…, criar_aluno(), parametrize, test_admin_lanca_mensalidade_paga_no_cartao(), test_escolher_plano_cria_mensalidade_e_redireciona_para_pix() (+31 more)

### Community 25 - "test_turnstile.py"
Cohesion: 0.24
Nodes (9): _cadastrar(), parametrize, Turnstile da Cloudflare no cadastro público (SEC-36). O cadastro manda e-mail…, test_cadastro_com_token_valido_segue_o_fluxo_de_sempre(), test_cadastro_sem_token_nao_cria_conta_nem_manda_email(), test_sem_turnstile_configurado_nada_carrega(), test_siteverify_fora_do_ar_recusa_o_cadastro(), test_token_grande_demais_nem_chega_a_cloudflare() (+1 more)

### Community 26 - "mercado_pago_conta.py"
Cohesion: 0.10
Nodes (37): access_token_vigente(), _agora(), ambiente_da_conexao(), _cifrar(), _client_id(), _client_secret(), ConexaoIlegivel, _configuracao_do_aplicativo() (+29 more)

### Community 27 - "test_seguranca.py"
Cohesion: 0.07
Nodes (28): _carregar_senhas_comuns(), Lista de senhas comuns recusadas (cerca de 3000; ASVS 5.0 6.2.4 e NIST 800-63B), erro_validacao_senha(), Retorna uma mensagem quando a senha é curta, comum ou igual ao identificador., Lê a lista de senhas comuns (uma por linha; `#` abre comentário) para um…, _cadastro_publico(), _imagem_jpeg(), _mensagem_da_resposta() (+20 more)

### Community 28 - "test_pix_rotas.py"
Cohesion: 0.22
Nodes (19): _agora_mercado_pago(), _assinar(), _resposta_consulta(), _resposta_criacao(), test_admin_tambem_pode_gerar_pix(), test_aluno_gera_pix_da_propria_mensalidade(), test_falha_de_indisponibilidade_do_mp_retorna_503(), test_impede_cobranca_duplicada_em_chamadas_consecutivas() (+11 more)

### Community 29 - "test_fila_email_concorrencia_postgres.py"
Cohesion: 0.18
Nodes (10): _enfileirar_em_transacao_propria(), postgres_fila(), fixture, Idempotência da fila de e-mail sob concorrência real, em PostgreSQL…, A recusa de uma chave repetida não pode desfazer o lote inteiro. Um…, A trava do lote precisa valer até o fim do lote. Comitar linha a linha…, Enfileira e comita numa sessão própria, como faria outra requisição., test_chave_duplicada_nao_descarta_os_outros_destinatarios_do_lote() (+2 more)

### Community 30 - "planilha_excel.py"
Cohesion: 0.30
Nodes (13): Nome legível da forma de pagamento. Antes as telas usavam `|replace('_','…, rotulo_forma_pagamento(), _aba_categorias(), _aba_entradas(), _aba_resumo(), _aba_saidas(), _cabecalho(), _escrever() (+5 more)

### Community 31 - "checkout_bp.py"
Cohesion: 0.10
Nodes (31): abrir_checkout(), _acesso_permitido(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), limitar_consulta_pagamento, limitar_criacao_pagamento, route (+23 more)

### Community 32 - "test_mudanca_plano.py"
Cohesion: 0.14
Nodes (28): detalhes_usuario(), pagina_perfil(), Persistência dos pedidos de troca de plano agendados para a próxima renovação., Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, Aplica um pedido agendado cujo período de origem já terminou sem renovação.…, SolicitacaoPlanoDAO, _agendar(), _pagar() (+20 more)

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

### Community 37 - "cartao_do_plano"
Cohesion: 0.27
Nodes (10): cartao_do_plano(), duracao_dias(), _duracao_por_extenso(), _meses(), preco(), preco_cheio(), Duração em meses cheios para exibir e dividir o preço: 30→1, 90→3, 365→12., Campos de `components/cartao_plano.html` para um plano: os mesmos na home e na… (+2 more)

### Community 38 - "PlanoDAO"
Cohesion: 0.10
Nodes (39): PlanoDAO, Apaga um plano que nunca foi usado. True, None (não existe) ou False (em uso)., Os planos à venda: home, perfil do aluno e formulários de contratação., Planos que algum registro referencia: mensalidade, cadastro de aluno ou pedido…, Grava a edição do admin. Vale para as cobranças criadas daqui em diante: as…, Tira o plano de venda. Devolve `(plano, pedidos_cancelados)`, ou None. Pedidos…, _pagar(), _plano() (+31 more)

### Community 39 - "URLPublicaInvalida"
Cohesion: 0.09
Nodes (35): aluno_do_token(), ConviteIndisponivel, descartar(), enviar(), gerar_token(), _hash(), RuntimeError, Convite de acesso: como um cadastro criado pela administração vira uma conta.… (+27 more)

### Community 40 - "varredura.mjs"
Cohesion: 0.11
Nodes (23): aberto(), ACESSO, auditar(), { chromium }, CONF, confirmacoes(), crc, CREDS (+15 more)

### Community 41 - "test_pagamento_recusado.py"
Cohesion: 0.28
Nodes (20): _assinar(), _data_mp(), _eventos(), _mockar_mp(), _pagamento_mp(), _pix_criado(), Mensalidade recusada: a próxima tentativa do aluno a reabre, e a recusa antiga…, Mensalidade cujo cartão acabou de ser recusado no Checkout Pro. (+12 more)

### Community 42 - "test_mercado_pago_oauth_postgres.py"
Cohesion: 0.25
Nodes (5): postgres_mp(), fixture, Renovação do token OAuth com trava de linha real, opcional na suíte que usa…, _Resposta, test_dois_processos_perto_do_vencimento_gastam_o_refresh_token_uma_vez()

### Community 43 - "avatar"
Cohesion: 0.12
Nodes (16): avatar(), breadcrumb(), Biblioteca de componentes .et-* (componentes.css), Seção Nossa equipe (professores_publicos), Nosso método: criar conta, aguardar aprovação, contratar plano e treinar, Cadastros pendentes (aprovar ou recusar aluno), Tabela de alunos paginada com busca no servidor, pgProfessor.html (minhas turmas do professor) (+8 more)

### Community 44 - "admin_requerido"
Cohesion: 0.22
Nodes (18): callback(), conectar(), desconectar(), limit, route, _voltar(), _autorizacao_valida(), callback() (+10 more)

### Community 45 - "test_observabilidade.py"
Cohesion: 0.18
Nodes (18): before_breadcrumb(), before_send(), iniciar_sentry(), _limpar(), mascarar(), Rastreamento de erros opcional com Sentry. Sem `SENTRY_DSN`, nada é importado…, _evento(), fixture (+10 more)

### Community 46 - "test_analytics.py"
Cohesion: 0.14
Nodes (20): _carrega_analytics(), com_analytics(), _csp_com_google(), _evento(), fixture, parametrize, GA4 opcional (servicos/analytics.py): nada sem ANALYTICS_ID, nunca em área…, sem_analytics_por_padrao() (+12 more)

### Community 47 - "requirements.txt (dependências de produção)"
Cohesion: 0.12
Nodes (19): requirements.txt (dependências de produção), cryptography 50.0.1, requirements-dev.txt (requirements.txt + pytest + pip-audit), pip-audit 2.10.1, pytest, Flask 3.1.3, Flask-Limiter[redis] 4.1.1, Flask-Migrate 4.1.0 (+11 more)

### Community 48 - "planilha_bp.py"
Cohesion: 0.18
Nodes (21): 80', '80.5', '80,50' ou '1.234,56' -> Decimal. None se vazio; ValueError se…, _valor_em_reais(), alterar_despesa(), _ano_e_mes(), _ano_valido(), baixar_excel(), excluir_despesa(), _formulario_de() (+13 more)

### Community 49 - "criar_pagamento"
Cohesion: 0.10
Nodes (53): criar_pagamento(), logar_como_aluno(), Hipótese: forjar ?status=approved na volta do MP quita a mensalidade., test_retorno_ignora_status_aprovado_da_query_string(), _mockar_preferencia(), parametrize, Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala…, Um boleto pendente do Checkout Pro grava provider_payment_id, mas não é Pix:… (+45 more)

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
Nodes (15): foto_professor(), aluno_autorizado(), aluno_requerido(), _credencial_confere(), encerrar_sessao(), professor_autorizado(), Autorização das rotas protegidas. A sessão diz quem *afirmou* ser quem; quem…, A sessão foi emitida para a credencial que vale AGORA? Uma sessão sem carimbo é… (+7 more)

### Community 56 - "deslize.html"
Cohesion: 0.22
Nodes (8): Content Security Policy (csp_nonce), window.deslizarTela(), marcar(), listener de pagereveal, SECOES (ordem das seções do menu), sentidoEntre(), View Transitions API (@view-transition), anel()

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
Cohesion: 0.10
Nodes (21): remover_professor(), ProfessorDAO, Professor, Hipótese: a foto continua acessível por URL depois de tirar a publicação., Hipótese: os contatos vazam na home antes de a publicação ser marcada., test_contatos_do_professor_so_aparecem_quando_publicados(), test_foto_do_professor_some_ao_despublicar(), _foto() (+13 more)

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
Cohesion: 0.06
Nodes (38): _paginar(), O que aconteceu numa tentativa de contratar/renovar/trocar de plano., Aplica LIMIT/OFFSET e conta o total numa consulta separada e barata. A contagem…, ResultadoContratacao, Decimal, Matricula, Pagamento, _para_decimal() (+30 more)

### Community 73 - "analytics.test.cjs"
Cohesion: 0.18
Nodes (7): assert, CODIGO, Element, fs, path, test, vm

### Community 74 - "MercadoPagoIndisponivel"
Cohesion: 0.13
Nodes (21): buscar_pagamento(), buscar_pagamentos_por_referencia(), cancelar_pagamento(), MercadoPagoIndisponivel, Exception, Consulta o pagamento diretamente na API do Mercado Pago - fonte de verdade de…, Lista os pagamentos que o Mercado Pago associa a uma external_reference. Usada…, Cancela uma cobranca Pix pendente no Mercado Pago. Best-effort: nunca lanca. (+13 more)

### Community 75 - "_tem_limite"
Cohesion: 0.20
Nodes (10): parametrize, Qualquer dígito no termo virava `CPF LIKE '%3%'` e devolvia a academia inteira., Rotas que custam hash de senha, processamento de imagem ou sondagem de token., Limites declarados por decorador NAQUELA rota. `resolve_limits` não serve aqui:…, Guarda do teste acima: uma rota sem limite precisa ser reprovada por ele., _tem_limite(), test_busca_so_trata_como_cpf_o_que_parece_cpf(), test_o_detector_de_limite_realmente_discrimina() (+2 more)

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
Cohesion: 0.11
Nodes (20): Academia, parametrize, test_admin_salva_atualiza_e_limpa_contatos(), test_configuracoes_exigem_admin(), test_contatos_invalidos(), test_csrf_configuracoes(), test_erro_preserva_formulario_e_dados_salvos(), test_link_email_preserva_caracteres_do_endereco() (+12 more)

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

### Community 84 - "armazenamento.py"
Cohesion: 0.12
Nodes (28): ArquivoInvalido, _conferir_dimensoes(), _detectar_tipo_imagem_real(), _exif_so_com_orientacao(), ImagemGrandeDemais, _jpeg_sem_metadados(), _orientacao(), _png_sem_metadados() (+20 more)

### Community 85 - "turnstile.py"
Cohesion: 0.27
Nodes (12): ativo_nesta_resposta(), _chave_site(), configurado(), hostnames_esperados(), Cloudflare Turnstile no cadastro público (SEC-36). O cadastro manda e-mail para…, Sites onde o widget pode ter sido resolvido, como a Cloudflare os informa., Chamada no arranque. `exigir` é verdadeiro em produção (endereço público em…, Para o template: a chave pública do widget, ou vazio quando o Turnstile está… (+4 more)

### Community 86 - "MatriculaDAO"
Cohesion: 0.17
Nodes (17): MatriculaDAO, Presenca, impressao_credencial(), Resumo curto e não reversível do hash da senha, guardado na sessão. Nunca é a…, test_area_do_aluno_renderiza_telas_independentes_do_menu(), test_escolher_plano_com_turma_cria_matricula(), test_plano_atual_continua_disponivel_para_gerar_cobranca(), test_turma_lotada_nao_vira_matricula_apos_pagamento() (+9 more)

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

### Community 93 - "academia_bp.py"
Cohesion: 0.13
Nodes (22): configuracoes(), _pagina(), route, _autorizacao_valida(), callback(), login_google(), _novo_pkce(), limit (+14 more)

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

### Community 116 - "logar_como_admin"
Cohesion: 0.10
Nodes (25): logar_como_admin(), test_admin_nao_pode_apagar_o_usuario_de_uma_conta_ativa(), test_convite_recusado_para_quem_ja_tem_acesso(), parametrize, Data de nascimento: o mesmo seletor de data e a mesma regra no cadastro, na…, _salvar_ficha(), test_data_iso_aceita_aaaa_mm_dd_e_dd_mm_aaaa(), test_ficha_do_admin_grava_no_formato_do_seletor() (+17 more)

### Community 117 - "_png_bomba"
Cohesion: 0.29
Nodes (7): _png_bomba(), Bomba de descompressão: arquivo minúsculo, imagem gigante. O PNG aqui tem 285…, PNG válido e altamente compressível: linhas zeradas, como uma bomba real., O teto de pixels vale para a FOTO, que é decodificada, não para o comprovante.…, test_comprovante_a4_escaneado_continua_sendo_aceito(), test_foto_de_perfil_mantem_o_teto_de_pixels(), test_png_com_pixels_demais_e_recusado_pelo_cabecalho()

### Community 122 - "Contrato do redesign — SistemaEXTREMETEAM"
Cohesion: 0.09
Nodes (20): 0. Antes de escrever código, 1. Identidade visual (design tokens), 2. Logo oficial (usar SOMENTE a logo original), 3. Telas a implementar, 4. Regras e dados, 5. Forma de trabalhar, Painel administrativo (desktop, sidebar preta com o emblema do dragão), Prompt para o Claude Code — Redesign do SistemaEXTREMETEAM (+12 more)

### Community 123 - "planilha.py"
Cohesion: 0.14
Nodes (15): anos_disponiveis(), Categoria, data_da_entrada(), _decimal(), _entradas(), entradas_detalhadas(), limites_do_ano(), Mes (+7 more)

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
Cohesion: 0.13
Nodes (15): Comprovante manual (dinheiro/transferência), Configuração de e-mail, Contatos da academia e equipe, Erros no Sentry (opcional), Foto de perfil e comprovante manual (armazenamento de arquivos), Google Analytics 4 (opcional, com consentimento), `/health` e `/health/pronto`, Hero da página inicial (cena 3D) (+7 more)

### Community 130 - "test_paginas_erro.py"
Cohesion: 0.17
Nodes (5): csrf_ligado(), fixture, Página de erro (templates/erro.html) e os handlers de 404, 403, 500 e CSRF., test_404_para_quem_esta_logado_leva_a_area_dele(), test_500_mostra_a_pagina_de_erro()

### Community 131 - "EmailPendente"
Cohesion: 0.25
Nodes (5): EmailPendente, parametrize, Agendamento sem rede, threads reais ou esperas de relógio., test_nao_inicia_em_testes(), test_retomada_de_item_persistido_e_retentativa_sem_painel()

### Community 133 - "Pagamento de mensalidade via Pix (Mercado Pago)"
Cohesion: 0.22
Nodes (9): Como obter credenciais de teste (modo manual, sem OAuth), Como testar localmente, Conectar a conta por OAuth (a academia não cria aplicativo), Instalar dependências, Pagamento de mensalidade via Pix (Mercado Pago), Produção, Trocando de credenciais de teste para produção, URL a cadastrar como webhook (+1 more)

### Community 134 - "formatar_competencia"
Cohesion: 0.39
Nodes (8): comprovante_mensalidade(), _pagamento_com_acesso_ou_404(), pagina_pagamento(), Há alguém autorizado a ver mensalidades nesta sessão (admin ou aluno ativo)?, _sessao_financeira_valida(), ver_comprovante_manual(), formatar_competencia(), Converte 'AAAA-MM' em algo como 'Setembro de 2026'. Devolve o valor original se…

### Community 135 - "cinema.py"
Cohesion: 0.31
Nodes (8): _entradas(), modulo(), Arquivos do hero cinematográfico da página inicial. A cena 3D é compilada pelo…, {nome da entrada: arquivo}, lido uma vez: o build não muda com o servidor no ar., URL da entrada `nome` ('cena' ou 'video') do build, ou None se não foi…, URL do vídeo do hero, só se ele existir e a entrada que o toca estiver…, _tem_video(), video()

### Community 136 - "Skills Disponíveis"
Cohesion: 0.22
Nodes (8): Assistente e Automação (Antigravity), Ciências e Bioinformática (Plugins de Ciência), Dados e Google Cloud Platform (GCP), Desenvolvimento Mobile e Flutter/Dart, Desenvolvimento Web e Frontend, Firebase e Backend, GenAI e Machine Learning, Skills Disponíveis

### Community 137 - "test_perfil_e_foto.py"
Cohesion: 0.15
Nodes (12): Turma, test_consulta_com_data_invalida_exibe_hoje_e_aviso(), test_consulta_com_data_valida_preserva_data_selecionada(), _imagem_jpeg_valida(), test_admin_acessa_foto_de_qualquer_aluno(), test_aluno_nao_acessa_foto_de_outro_aluno(), test_aluno_ve_o_proprio_perfil(), test_substituir_e_remover_foto() (+4 more)

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

### Community 146 - "usuario_bp.py"
Cohesion: 0.12
Nodes (32): ativar_acesso(), _cadastro_recebido(), _chave_ip_e_identificador(), _em_segundo_plano(), _enviar_em_segundo_plano(), foto_perfil(), pagina_cadastro(), _pode_ver_foto() (+24 more)

### Community 147 - "Etapa 3 — home com os planos + termos"
Cohesion: 0.40
Nodes (4): Agente A — `templates/index.html` e `static/css/index.css`, Antigravity — `termos_de_servico.html`, `politica_privacidade.html`, `termos_responsabilidade.html` + `static/css/termos.css` (novo), Dados da home (Claude entrega em servidor.py — não edite), Etapa 3 — home com os planos + termos

### Community 148 - "test_fontes_locais.py"
Cohesion: 0.25
Nodes (3): parametrize, Fontes servidas pelo próprio site (SEC-18). Com o Google Fonts, o navegador de…, test_csp_nao_libera_o_google_fonts()

### Community 149 - "Biblioteca no Figma"
Cohesion: 0.50
Nodes (3): Biblioteca no Figma, Falta (ordem de retomada), Limites do plano Starter que moldaram o arquivo

### Community 151 - "home"
Cohesion: 0.25
Nodes (9): Registra a sessão como encerrada: cópias antigas do cookie deixam de valer.…, revogar_sessao_atual(), health(), health_pronto(), home(), logout(), exempt, limit (+1 more)

### Community 152 - "Configuração de segurança"
Cohesion: 0.40
Nodes (5): Configuração de segurança, Credencial do administrador, Publicar com um domínio próprio, Segundo fator do administrador (opcional, recomendado), Turnstile no cadastro público (obrigatório em produção)

### Community 155 - "seo_bp.py"
Cohesion: 0.67
Nodes (3): route, robots(), sitemap()

### Community 157 - "auth.test.cjs"
Cohesion: 0.25
Nodes (6): assert, CODIGO, fs, path, test, vm

### Community 158 - "credenciais.py"
Cohesion: 0.10
Nodes (26): pagina_login(), admin_configurado(), codigo_totp(), comparar_em_tempo_constante(), credencial_admin_confere(), gerar_hash_admin(), gerar_segredo_totp(), _main() (+18 more)

### Community 159 - ".buscar_por_id"
Cohesion: 0.15
Nodes (26): _agora_mercado_pago(), _assinar(), _pagamento_mp(), _preparar_retorno(), Pix aberto e checkout concluído ao mesmo tempo: a consulta pelo…, test_retorno_com_aprovacao_confirmada_marca_pago(), test_retorno_com_mp_indisponivel_avisa_sem_mudar_status(), test_retorno_de_boleto_avisa_sobre_o_prazo() (+18 more)

### Community 161 - "ci-security-scanning-with-strix/SKILL.md"
Cohesion: 0.29
Nodes (6): GitHub Actions, Option A — Self-hosted OSS CLI in the runner, Option B — Managed platform (no runner infra), Optional: upload findings to GitHub code scanning, Other CI systems, Set up Strix in CI/CD

### Community 162 - "_Resposta"
Cohesion: 0.25
Nodes (3): fixture, _Resposta, _Siteverify

### Community 164 - "Find security vulnerabilities in code"
Cohesion: 0.29
Nodes (6): Complementary tooling, Find security vulnerabilities in code, Fix and verify, Read the results, Reviewing a pull request instead of the whole repo, Run it

### Community 165 - "test_mercado_pago_oauth.py"
Cohesion: 0.08
Nodes (54): MercadoPagoConexao, Conta do Mercado Pago que a academia autorizou por OAuth. Uma linha só (a…, _agora(), _ajustar(), api_mp(), _conectar(), _dados_conexao(), oauth_env() (+46 more)

### Community 166 - ".listar_paginado"
Cohesion: 0.29
Nodes (6): Uma página de alunos já cadastrados, recortada e filtrada pelo banco. O painel…, O CPF é guardado formatado; digitar só os números precisa encontrar mesmo assim., test_busca_do_admin_encontra_o_aluno_pelo_cpf_so_com_digitos(), test_busca_por_nome_com_numero_nao_devolve_todo_mundo(), test_paginacao_do_admin_ignora_pendentes_como_a_tela_sempre_fez(), test_painel_admin_pagina_alunos_no_banco()

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

### Community 174 - "cobranca_pendente"
Cohesion: 0.33
Nodes (7): cobranca_a_pagar(), cobranca_em_decisao(), cobranca_pendente(), _ordenar_por_inicio(), Mensalidade com pagamento já enviado e aguardando decisão…, Mensalidade que ainda depende de uma ação do aluno., Qualquer cobrança que impeça abrir outra: a que aguarda decisão tem prioridade.

### Community 175 - "test_financeiro_admin_painel.py"
Cohesion: 0.33
Nodes (5): test_busca_financeira_trata_curingas_como_texto(), test_painel_financeiro_busca_por_nome_do_aluno(), test_painel_financeiro_exige_admin(), test_painel_financeiro_filtra_por_status(), test_painel_financeiro_mostra_totais_do_backend()

### Community 177 - "test_migracao_conexao_mercado_pago.py"
Cohesion: 0.83
Nodes (3): _migracao(), test_migracao_cria_a_tabela_igual_ao_modelo_e_e_reentrante(), test_migracao_encadeia_na_ultima_revisao_existente()

### Community 180 - "limites_pagamento.py"
Cohesion: 0.50
Nodes (3): chave_pagamento(), Orçamentos compartilhados das chamadas interativas ao provedor de pagamento., A mesma conta mantém seu limite entre sessões, rotas e mensalidades. Alunos que…

## Ambiguous Edges - Review These
- `botao_google.html` → `Integração com o Gmail (conta remetente da academia)`  [AMBIGUOUS]
  templates/politica_privacidade.html · relation: conceptually_related_to

## Knowledge Gaps
- **326 isolated node(s):** `name`, `private`, `version`, `description`, `type` (+321 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `botao_google.html` and `Integração com o Gmail (conta remetente da academia)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `PagamentoDAO` connect `PagamentoDAO` to `Aluno`, `adm_bp.py`, `formatar_competencia`, `AlunoDAO`, `route`, `test_admin_mercado_pago.py`, `test_regressao_auditoria.py`, `test_auditoria_seguranca.py`, `usuario_bp.py`, `pix_bp.py`, `criar_aluno`, `test_seguranca.py`, `test_pix_rotas.py`, `.buscar_por_id`, `test_mudanca_plano.py`, `checkout_bp.py`, `PlanoDAO`, `test_pagamento_recusado.py`, `test_financeiro_admin_painel.py`, `criar_pagamento`, `config.py`, `MatriculaDAO`, `test_comprovante_sem_metadados.py`?**
  _High betweenness centrality (0.098) - this node is a cross-community bridge._
- **Why does `Vitrine de componentes (/_vitrine)` connect `ui.html` to `config.py`, `componentes.js`, `csrf_field.html`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Why does `criar_aluno()` connect `criar_aluno` to `Aluno`, `test_paginas_erro.py`, `test_seo.py`, `AlunoDAO`, `test_perfil_e_foto.py`, `PagamentoDAO`, `test_regressao_auditoria.py`, `test_auditoria_seguranca.py`, `test_limites_pagamento.py`, `gmail_conta.py`, `test_seguranca.py`, `.buscar_por_id`, `test_mudanca_plano.py`, `test_limites_requisicao.py`, `test_mercado_pago_oauth.py`, `PlanoDAO`, `.listar_paginado`, `test_analytics.py`, `test_financeiro_admin_painel.py`, `criar_pagamento`, `test_planilha_economica.py`, `test_home_planos.py`, `config.py`, `_tem_limite`, `test_layouts.py`, `test_publicas_redesign.py`, `MatriculaDAO`, `logar_como_admin`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Are the 158 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 158 INFERRED edges - model-reasoned connections that need verification._
- **Are the 170 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 170 INFERRED edges - model-reasoned connections that need verification._
- **Are the 169 inferred relationships involving `logar_como_admin()` (e.g. with `test_admin_salva_atualiza_e_limpa_contatos()` and `test_csrf_configuracoes()`) actually correct?**
  _`logar_como_admin()` has 169 INFERRED edges - model-reasoned connections that need verification._