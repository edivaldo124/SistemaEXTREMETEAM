# Graph Report - SistemaEXTREMETEAM  (2026-10-23)

## Corpus Check
- 214 files · ~278,893 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3047 nodes · 7154 edges · 178 communities (164 shown, 14 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 1296 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f7ae2bc1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Aluno
- Componentes
- test_admin_segundo_fator.py
- test_mercado_pago_oauth.py
- test_seo.py
- usuario_e_admin
- test_mercado_pago_oauth_postgres.py
- logar_como_admin
- planos.py
- route
- PlanoDAO
- turma_bp.py
- index.html (home pública)
- PagamentoDAO
- criar_aluno
- fase3b.js
- criar_pagamento
- armazenamento.py
- fila_email.py
- csrf_field.html
- salvar_foto_perfil
- dt_aluno.html — ficha do aluno (admin)
- pix_bp.py
- servidor.py
- .listar_por_aluno
- pgUsuario.html (área do aluno)
- mercado_pago_conta.py
- test_seguranca.py
- test_pix_rotas.py
- test_auditoria_seguranca.py
- planilha_excel.py
- checkout_bp.py
- test_mudanca_plano.py
- avatar
- test_mercado_pago_servico.py
- test_limites_requisicao.py
- Pagina
- academia_bp.py
- test_home_planos.py
- URLPublicaInvalida
- varredura.mjs
- test_pagamento_recusado.py
- PagamentoEvento
- layouts/admin.html — layout do painel administrativo
- autorizacao.py
- test_observabilidade.py
- test_analytics.py
- requirements.txt (dependências de produção)
- .buscar_por_id
- logar_como_aluno
- adm_bp.py
- analytics.js
- package.json
- seo.py
- Strix Cloud (managed, no local infra)
- admin_nav.html
- Serviço app (Flask com Gunicorn na porta 5000)
- test_prontidao.py
- pix.js
- test_arranque_seguranca.py
- revogar_sessao_atual
- test_keep_alive.py
- ProfessorDAO
- test_sessao_revogada.py
- Relatório de segurança — Sistema Extreme Team
- Academia
- componentes.js
- prontidao.py
- botao_ocupado.test.cjs
- test_backup_scripts.py
- gunicorn.conf.py
- config.py
- analytics.test.cjs
- pagamento.js
- test_perfil_e_foto.py
- test_email_componentes.py
- test_layouts.py
- test_migracao_checkout.py
- mercado_pago_oauth_bp.py
- checkout_abertura.test.cjs
- pagamento_polling.test.cjs
- test_publicas_redesign.py
- env.py
- test_formatos_de_imagem.py
- Plano
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
- conftest.py
- ImagemGrandeDemais
- agendar.sh
- restaurar.sh
- Contrato do redesign — SistemaEXTREMETEAM
- test_planilha_economica.py
- cinema.test.cjs
- compilerOptions
- pagamento.html (pagar mensalidade)
- penetration-testing-with-strix/SKILL.md
- test_cinema.py
- SistemaEXTREMETEAM
- test_paginas_erro.py
- test_aprovacao_incoerente_nao_quita_mensalidade
- financeiro.html — painel financeiro
- Pagamento de mensalidade via Pix (Mercado Pago)
- gmail_conta.py
- cinema.py
- Skills Disponíveis
- TransporteEmMemoria
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
- google_login.py
- Configuração de segurança
- test_data_nascimento.py
- test_logs_sem_dado_pessoal.py
- auth.test.cjs
- credenciais.py
- test_admin_mercado_pago.py
- README.md
- ci-security-scanning-with-strix/SKILL.md
- test_conversao_home.py
- _FakePaymentResource
- Find security vulnerabilities in code
- requirements-dev.txt (requirements.txt + pytest + pip-audit)
- painel_adm
- Security-test an API
- Application security testing
- imagens.d.ts
- Fix Strix findings and verify
- Test against the OWASP Top 10
- Pentest a web application
- gmail_oauth_bp.py
- pagina_login
- _pagamento_com_acesso_ou_404
- limites_pagamento.py
- .status_efetivo
- test_trocar_a_credencial_do_admin_encerra_a_sessao_administrativa

## God Nodes (most connected - your core abstractions)
1. `PagamentoDAO` - 230 edges
2. `criar_aluno()` - 173 edges
3. `logar_como_admin()` - 172 edges
4. `criar_pagamento()` - 164 edges
5. `logar_como_aluno()` - 138 edges
6. `AlunoDAO` - 93 edges
7. `PlanoDAO` - 69 edges
8. `Aluno` - 67 edges
9. `MercadoPagoIndisponivel` - 45 edges
10. `Professor` - 43 edges

## Surprising Connections (you probably didn't know these)
- `Vitrine de planos da home (secao_planos com vitrine_planos)` --references--> `cartao_do_plano()`  [INFERRED]
  templates/index.html → servicos/planos.py
- `test_limite_de_login_por_ip_e_identificador()` --uses--> `AlunoDAO`  [INFERRED]
  tests/test_seguranca.py → dao/usuarioDAO.py
- `Envio de comprovante manual (et-upload, até 4 MB)` --references--> `salvar_comprovante_manual()`  [EXTRACTED]
  templates/pagamento.html → servicos/armazenamento.py
- `Contratação e troca de plano (contratar, renovar, agendar_mudanca)` --references--> `cartao_do_plano()`  [EXTRACTED]
  templates/pgUsuario.html → servicos/planos.py
- `_pagina()` --uses--> `ConfiguracaoInvalida`  [INFERRED]
  blueprints/academia_bp.py → servicos/mercado_pago.py

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

## Communities (178 total, 14 thin omitted)

### Community 0 - "Aluno"
Cohesion: 0.08
Nodes (17): cadastrar_aluno(), Matrícula feita pela administração, sem conta de acesso. Pede só o que…, _convidar_cadastro_existente(), _convidar_cadastro_existente_por_id(), Cadastro administrativo que alguém tentou recriar pelo formulário público. Em…, Versão para thread de fundo: a sessão da requisição não vale fora dela., Matrícula feita no balcão: sem login, sem senha e sem convite de acesso. Nasce…, Aluno (+9 more)

### Community 1 - "Componentes"
Cohesion: 0.05
Nodes (36): Altura de controle, Avisos flutuantes, Botões — `.et-botao` + variante (+ tamanho), Cartões e contêineres, Componentes, Contêiner e estrutura, Cores, Dados (+28 more)

### Community 2 - "test_admin_segundo_fator.py"
Cohesion: 0.20
Nodes (20): _codigo_agora(), _codigo_errado(), _destino(), _entrar_com_senha(), fixture, parametrize, Segundo fator do administrador (SEC-30). Com ADMIN_TOTP_SECRET definida, a…, segundo_fator() (+12 more)

### Community 3 - "test_mercado_pago_oauth.py"
Cohesion: 0.06
Nodes (69): MercadoPagoConexao, Conta do Mercado Pago que a academia autorizou por OAuth. Uma linha só (a…, _agora(), _ajustar(), api_mp(), _conectar(), _dados_conexao(), oauth_env() (+61 more)

### Community 4 - "test_seo.py"
Cohesion: 0.10
Nodes (25): _head(), _json_ld(), parametrize, SEO técnico: robots.txt, sitemap, títulos, meta tags, noindex e JSON-LD da home., Nenhum campo do JSON-LD pode sair nulo, vazio ou só com espaços., _robots(), _sem_vazios(), test_area_do_admin_sai_do_indice() (+17 more)

### Community 5 - "usuario_e_admin"
Cohesion: 0.12
Nodes (23): _aluno_do_cpf_ou_painel(), aprovar_aluno(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_pagamento(), cancelar_mudanca_plano_admin(), desativar_aluno(), enviar_convite_acesso() (+15 more)

### Community 6 - "test_mercado_pago_oauth_postgres.py"
Cohesion: 0.18
Nodes (8): postgres_mp(), fixture, Renovação do token OAuth com trava de linha real, opcional na suíte que usa…, _Resposta, test_dois_processos_perto_do_vencimento_gastam_o_refresh_token_uma_vez(), _migracao(), test_migracao_cria_a_tabela_igual_ao_modelo_e_e_reentrante(), test_migracao_encadeia_na_ultima_revisao_existente()

### Community 7 - "logar_como_admin"
Cohesion: 0.12
Nodes (51): remover_foto_aluno(), AlunoDAO, logar_como_admin(), _matricular(), parametrize, Cadastro de aluno pela administração, ativação de acesso e confirmação de…, test_admin_lanca_e_baixa_mensalidade_de_aluno_sem_acesso(), test_admin_matricula_aluno_sem_email_senha_nem_acesso() (+43 more)

### Community 8 - "planos.py"
Cohesion: 0.06
Nodes (42): cadeia_paga(), cartao_do_plano(), cobranca_a_pagar(), cobranca_em_decisao(), cobranca_pendente(), duracao_dias(), _duracao_por_extenso(), esta_inadimplente() (+34 more)

### Community 9 - "route"
Cohesion: 0.14
Nodes (25): alterar_senha_perfil(), _aluno_da_sessao(), _aluno_por_token(), atualizar_dados_perfil(), cadastro_obrigado(), cancelar_mudanca_plano(), confirmar_email(), confirmar_presenca() (+17 more)

### Community 10 - "PlanoDAO"
Cohesion: 0.11
Nodes (41): arquivar_plano(), reativar_plano(), _plano_do_formulario(), PlanoDAO, Os planos à venda: home, perfil do aluno e formulários de contratação., Grava a edição do admin. Vale para as cobranças criadas daqui em diante: as…, Tira o plano de venda. Devolve `(plano, pedidos_cancelados)`, ou None. Pedidos…, Pagamento (+33 more)

### Community 11 - "turma_bp.py"
Cohesion: 0.17
Nodes (17): _acesso_permitido(), cadastrar_professor(), cadastrar_turma(), desmatricular_aluno(), detalhe_turma(), editar_professor(), gerenciar_turmas(), matricular_aluno() (+9 more)

### Community 12 - "index.html (home pública)"
Cohesion: 0.11
Nodes (14): faq_estruturado(), Textos editáveis da página inicial: perguntas frequentes e prazos de…, JSON-LD FAQPage com exatamente as perguntas mostradas na página., cabecalho, entrarFixo, icone_senha, input_senha, modal (+6 more)

### Community 13 - "PagamentoDAO"
Cohesion: 0.07
Nodes (36): criar_pix_mensalidade(), limitar_criacao_pagamento, _tratar_webhook(), mensalidade_destaque(), PagamentoDAO, Status como o painel deve LER, com o vencimento aplicado na própria consulta. A…, Carrega aluno e plano junto das mensalidades. O template do painel lê…, Lista completa (sem paginar). Mantida para relatórios e testes. (+28 more)

### Community 14 - "criar_aluno"
Cohesion: 0.04
Nodes (70): _parece_busca_por_cpf(), O termo é um CPF, ou um pedaço dele, e não um nome que por acaso tem número?, Uma página de alunos já cadastrados, recortada e filtrada pelo banco. O painel…, criar_aluno(), test_aluno_existente_continua_entrando_normalmente(), test_area_do_aluno_renderiza_telas_independentes_do_menu(), test_escolher_plano_cria_mensalidade_e_redireciona_para_pix(), test_plano_atual_continua_disponivel_para_gerar_cobranca() (+62 more)

### Community 15 - "fase3b.js"
Cohesion: 0.06
Nodes (47): avisos, bind(), caixas, campos, col(), D(), estados, faixa (+39 more)

### Community 16 - "criar_pagamento"
Cohesion: 0.07
Nodes (38): criar_pagamento(), parametrize, Hipótese: as rotas de cobrança respondem sem sessão nenhuma., Hipótese: dá para abrir um checkout novo sobre uma cobrança já resolvida., Hipótese: se a resposta do MP trouxer um destino estranho, ele é salvo e…, Hipótese: cada clique cria uma cobrança nova no Mercado Pago., Hipótese: dá para injetar o valor pelo corpo do POST., Verifica a trava antes da emissão e o reaproveitamento na próxima chamada.… (+30 more)

### Community 17 - "armazenamento.py"
Cohesion: 0.15
Nodes (21): ArmazenamentoIndisponivel, ArquivoInvalido, _exif_so_com_orientacao(), _gravar(), _jpeg_sem_metadados(), _orientacao(), _pasta(), _png_sem_metadados() (+13 more)

### Community 18 - "fila_email.py"
Cohesion: 0.06
Nodes (40): EmailPendente, espera_da_proxima_tentativa(), Fila de e-mails no banco. Aviso e cobrança coletivos saíam um a um dentro da…, contar_falhados(), contar_pendentes(), disparar(), enfileirar(), enfileirar_transacional() (+32 more)

### Community 19 - "csrf_field.html"
Cohesion: 0.12
Nodes (21): Contato e localização da academia, ativar_acesso.html — ativar acesso pelo convite, cadastro.html — criar conta, cadastro_obrigado.html — cadastro recebido, Cadastro com PRG e resposta única, Aceite do Termo de Responsabilidade, Modal de login da home (#meuModal, POST /login), layouts/publico.html — layout das telas públicas (+13 more)

### Community 20 - "salvar_foto_perfil"
Cohesion: 0.11
Nodes (30): enviar_foto_aluno(), ler_arquivo(), _nome_valido(), (URL base do bucket, cabeçalhos) do Supabase Storage, ou None para gravar em…, O nome sempre é o UUID gerado por esta camada, nunca um valor vindo da…, Valida, reprocessa e salva uma foto de perfil. Retorna o nome do arquivo…, Conteúdo de um arquivo já salvo, ou None se não existir, for inválido ou o…, Melhor esforço: um arquivo que sobra não quebra nada, então falha só vai para o… (+22 more)

### Community 21 - "dt_aluno.html — ficha do aluno (admin)"
Cohesion: 0.16
Nodes (19): Conexão OAuth do Gmail para envio de avisos, admin_aluno_novo.html — matricular aluno, Matrícula sem acesso ao sistema, admin_avisos.html — avisos e cobranças por e-mail, Cobrança de mensalidades por e-mail, Fila de envio de e-mails (até 5 tentativas), Nonce de CSP em scripts inline (csp_nonce), admin_plano_editar.html — editar plano (+11 more)

### Community 22 - "pix_bp.py"
Cohesion: 0.08
Nodes (39): _data_do_form(), painel_financeiro(), _chave_entrega_webhook(), _data_da_aprovacao(), _forma_pagamento_confirmada(), _instante_utc(), _iso_utc(), _liberar_entrega_webhook() (+31 more)

### Community 23 - "servidor.py"
Cohesion: 0.14
Nodes (20): after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, context_processor, errorhandler, formatar_moeda(), Formata um valor em reais no padrão brasileiro: R$ 1.080,00. Usado como filtro…, acesso_negado() (+12 more)

### Community 24 - ".listar_por_aluno"
Cohesion: 0.08
Nodes (36): O que aconteceu numa tentativa de contratar/renovar/trocar de plano., Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, Com uma troca já agendada, só dois planos fazem sentido num pedido de…, A cobrança do período seguinte tem de nascer no plano que o aluno agendou.…, `pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -…, ResultadoContratacao, parametrize, test_admin_lanca_mensalidade_paga_no_cartao() (+28 more)

### Community 25 - "pgUsuario.html (área do aluno)"
Cohesion: 0.16
Nodes (4): mostrarTela(), trocarTela(), pgUsuario.html (área do aluno), Navegação por telas da área do aluno (data-menu-screen, bottom-nav)

### Community 26 - "mercado_pago_conta.py"
Cohesion: 0.09
Nodes (43): base_url_publica(), ConfiguracaoInvalida, access_token_vigente(), _agora(), ambiente_da_conexao(), _cifrar(), _client_id(), _client_secret() (+35 more)

### Community 27 - "test_seguranca.py"
Cohesion: 0.07
Nodes (28): _carregar_senhas_comuns(), Lista de senhas comuns recusadas (cerca de 3000; ASVS 5.0 6.2.4 e NIST 800-63B), erro_validacao_senha(), Retorna uma mensagem quando a senha é curta, comum ou igual ao identificador., Lê a lista de senhas comuns (uma por linha; `#` abre comentário) para um…, test_upload_de_arquivo_disfarcado_e_recusado(), _cadastro_publico(), _imagem_jpeg() (+20 more)

### Community 28 - "test_pix_rotas.py"
Cohesion: 0.20
Nodes (20): _agora_mercado_pago(), _assinar(), _resposta_consulta(), _resposta_criacao(), test_admin_tambem_pode_gerar_pix(), test_aluno_gera_pix_da_propria_mensalidade(), test_aluno_nao_acessa_mensalidade_de_outro_aluno(), test_falha_de_indisponibilidade_do_mp_retorna_503() (+12 more)

### Community 29 - "test_auditoria_seguranca.py"
Cohesion: 0.09
Nodes (20): Professor, logar_como_professor(), fixture, Auditoria de segurança: sondas escritas para TENTAR quebrar as regras. Nenhum…, Hipótese: a sessão de professor é aceita nas rotas financeiras do aluno., Hipótese: como o JS agora usa fetch, o POST perdeu a exigência de CSRF., Hipótese: as demais rotas de dinheiro aceitam POST sem token., O webhook precisa ser isento de CSRF (vem de fora); a assinatura é a barreira. (+12 more)

### Community 30 - "planilha_excel.py"
Cohesion: 0.30
Nodes (13): Nome legível da forma de pagamento. Antes as telas usavam `|replace('_','…, rotulo_forma_pagamento(), _aba_categorias(), _aba_entradas(), _aba_resumo(), _aba_saidas(), _cabecalho(), _escrever() (+5 more)

### Community 31 - "checkout_bp.py"
Cohesion: 0.11
Nodes (28): abrir_checkout(), _acesso_permitido(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), limitar_consulta_pagamento, limitar_criacao_pagamento, route (+20 more)

### Community 32 - "test_mudanca_plano.py"
Cohesion: 0.14
Nodes (29): detalhes_usuario(), Persistência dos pedidos de troca de plano agendados para a próxima renovação., Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, Aplica um pedido agendado cujo período de origem já terminou sem renovação.…, SolicitacaoPlanoDAO, _agendar(), _pagar(), plano_barato() (+21 more)

### Community 33 - "avatar"
Cohesion: 0.12
Nodes (25): avatar(), breadcrumb(), cartao_plano(), secao_planos(), interruptor(), shadcn/ui, Seção Nossa equipe (professores_publicos), Nosso método: criar conta, aguardar aprovação, contratar plano e treinar (+17 more)

### Community 34 - "test_mercado_pago_servico.py"
Cohesion: 0.10
Nodes (31): Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, validar_assinatura_webhook(), Hipótese: uma notificação capturada ontem pode ser reenviada hoje., `ts=nan` fazia a comparação da janela dar False e passava pela checagem de…, test_webhook_recusa_assinatura_antiga(), test_webhook_recusa_ts_nao_numerico_finito(), base_url(), _criar_preferencia() (+23 more)

### Community 35 - "test_limites_requisicao.py"
Cohesion: 0.12
Nodes (28): consultar_mp(), _estourar(), fixture, parametrize, Limites de requisição da rodada de 04/10/2026 (SEC-10 a SEC-17 e SEC-19). Cada…, Trocar de rede ou abrir outra sessão não devolve a cota de e-mails em massa., Faz `limite` requisições sem nenhum 429 e devolve a seguinte., Alunos no mesmo Wi-Fi não dividem o teto padrão, nem com o visitante anônimo. (+20 more)

### Community 36 - "Pagina"
Cohesion: 0.14
Nodes (5): Pagina, Uma fatia de resultados já recortada pelo banco, com o que a navegação precisa., Uma página existe mesmo quando está vazia. Sem isto, `__len__` fazia `{% if…, `__len__` fazia `{% if pagina %}` ser falso numa página sem itens, escondendo…, test_pagina_vazia_ainda_mostra_a_navegacao()

### Community 37 - "academia_bp.py"
Cohesion: 0.23
Nodes (10): configuracoes(), _pagina(), route, O administrador foi ao Mercado Pago e a autorização não voltou para cá? O state…, tentativa_sem_retorno(), link_email(), Normalização de contatos profissionais antes de montar links públicos., validar_email() (+2 more)

### Community 38 - "test_home_planos.py"
Cohesion: 0.15
Nodes (19): destacar_plano(), Escolhe o plano que a página inicial mostra em destaque (só um por vez)., Marca o plano em destaque da página inicial, desmarcando qualquer outro.…, Inclusive os arquivados: serve a quem olha o histórico (filtro do financeiro)., Planos da página inicial, prontos para `components/cartao_plano.html`. O preço…, vitrine_planos(), _plano(), _quatro_planos() (+11 more)

### Community 39 - "URLPublicaInvalida"
Cohesion: 0.08
Nodes (41): _enviar_em_segundo_plano(), E-mail COM token (recuperação, confirmação): não pode ir para a `fila_email`. A…, recuperar_senha(), solicitar_troca_email(), verificar_email_cadastro(), route, verificar_email_cadastro(), aluno_do_token() (+33 more)

### Community 40 - "varredura.mjs"
Cohesion: 0.11
Nodes (23): aberto(), ACESSO, auditar(), { chromium }, CONF, confirmacoes(), crc, CREDS (+15 more)

### Community 41 - "test_pagamento_recusado.py"
Cohesion: 0.28
Nodes (20): _assinar(), _data_mp(), _eventos(), _mockar_mp(), _pagamento_mp(), _pix_criado(), Mensalidade recusada: a próxima tentativa do aluno a reabre, e a recusa antiga…, Mensalidade cujo cartão acabou de ser recusado no Checkout Pro. (+12 more)

### Community 42 - "PagamentoEvento"
Cohesion: 0.09
Nodes (17): aprovar_comprovante_manual(), _processar_status_mp(), Fonte unica de aprovacao, usada pelo webhook, pelo polling de status e pela…, A recusa (criada em `criada_em`, UTC) é de antes da última nova tentativa? Sem…, Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.…, Troca o plano de uma cobrança ainda não paga em vez de abrir uma segunda. O…, Primeiro dia não coberto por outra mensalidade do mesmo aluno., Define o período coberto por uma mensalidade que ainda não tem um (lançamento… (+9 more)

### Community 43 - "layouts/admin.html — layout do painel administrativo"
Cohesion: 0.10
Nodes (23): campoDuracao, campoPreco, formularioPlano, Protocolo data-confirm-modal, estado_vazio(), metrica(), erro.html — página de erro, Próximo passo conforme a área do usuário (+15 more)

### Community 44 - "autorizacao.py"
Cohesion: 0.20
Nodes (16): _acesso_permitido(), foto_professor(), aluno_autorizado(), aluno_requerido(), _credencial_confere(), encerrar_sessao(), professor_autorizado(), Autorização das rotas protegidas. A sessão diz quem *afirmou* ser quem; quem… (+8 more)

### Community 45 - "test_observabilidade.py"
Cohesion: 0.18
Nodes (18): before_breadcrumb(), before_send(), iniciar_sentry(), _limpar(), mascarar(), Rastreamento de erros opcional com Sentry. Sem `SENTRY_DSN`, nada é importado…, _evento(), fixture (+10 more)

### Community 46 - "test_analytics.py"
Cohesion: 0.14
Nodes (20): _carrega_analytics(), com_analytics(), _csp_com_google(), _evento(), fixture, parametrize, GA4 opcional (servicos/analytics.py): nada sem ANALYTICS_ID, nunca em área…, sem_analytics_por_padrao() (+12 more)

### Community 47 - "requirements.txt (dependências de produção)"
Cohesion: 0.14
Nodes (16): requirements.txt (dependências de produção), cryptography 50.0.1, Flask 3.1.3, Flask-Limiter[redis] 4.1.1, Flask-Migrate 4.1.0, Flask-SQLAlchemy 3.1.1, Flask-WTF 1.2.2, gunicorn 23.0.0 (+8 more)

### Community 48 - ".buscar_por_id"
Cohesion: 0.13
Nodes (29): _agora_mercado_pago(), _assinar(), _pagamento_mp(), _preparar_retorno(), Pix aberto e checkout concluído ao mesmo tempo: a consulta pelo…, test_configuracao_ausente_falha_de_forma_explicita(), test_mercado_pago_indisponivel_nao_persiste_nada(), test_retorno_com_aprovacao_confirmada_marca_pago() (+21 more)

### Community 49 - "logar_como_aluno"
Cohesion: 0.09
Nodes (46): logar_como_aluno(), Hipótese: forjar ?status=approved na volta do MP quita a mensalidade., test_retorno_ignora_status_aprovado_da_query_string(), _mockar_preferencia(), parametrize, Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala…, Um boleto pendente do Checkout Pro grava provider_payment_id, mas não é Pix:…, _resposta_preferencia() (+38 more)

### Community 50 - "adm_bp.py"
Cohesion: 0.13
Nodes (24): _chave_lote(), cobrar_inadimplentes(), cobrar_mensalidade(), editar_plano(), enviar_aviso(), _esta_inadimplente(), _ler_plano(), _ler_promocao() (+16 more)

### Community 51 - "analytics.js"
Cohesion: 0.14
Nodes (12): analytics_ativo(), id_analytics(), marcar_conversao_cadastro(), Google Analytics 4 opcional, só em página pública e só com consentimento. Sem…, Chamada no arranque: um ID malformado derruba a subida, como as demais…, Esta resposta pode carregar o GA4? Visitante, página pública indexável ou…, validar_configuracao(), apagarCookiesGa() (+4 more)

### Community 52 - "package.json"
Cohesion: 0.05
Nodes (38): dependencies, maath, react, react-dom, @react-three/drei, @react-three/fiber, scrolly-video, three (+30 more)

### Community 53 - "seo.py"
Cohesion: 0.18
Nodes (18): conteudo_robots(), conteudo_sitemap(), dados_estruturados_academia(), _dia(), _dias_da_linha(), _hora(), horarios_estruturados(), origem_publica() (+10 more)

### Community 54 - "Strix Cloud (managed, no local infra)"
Cohesion: 0.12
Nodes (15): 0. Credits & top-ups, 1. Register the target as an asset, 2. Launch a scan, 3. Wait for completion, 4. Read findings, 5. Export & report, 6. PR reviews, 7. Continuous testing (schedules & webhooks) (+7 more)

### Community 56 - "admin_nav.html"
Cohesion: 0.15
Nodes (9): Abas com memória (data-tabs-lembrar), Content Security Policy (csp_nonce), window.deslizarTela(), marcar(), listener de pagereveal, SECOES (ordem das seções do menu), sentidoEntre(), View Transitions API (@view-transition) (+1 more)

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
Cohesion: 0.16
Nodes (21): _env_arranque(), _hosts_e_proxy(), parametrize, Validações feitas por servidor.py no arranque (COOKIE_SECURE, TRUSTED_HOSTS,…, Desenvolvimento local sem HTTPS (sem Caddy) não pode ficar travado., `python -m servicos.credenciais`: o hash sai entre aspas simples. O hash do…, _rodar(), test_arranque_aceita_redis_do_upstash_com_espaco_em_volta() (+13 more)

### Community 61 - "revogar_sessao_atual"
Cohesion: 0.29
Nodes (8): Registra a sessão como encerrada: cópias antigas do cookie deixam de valer.…, revogar_sessao_atual(), health(), health_pronto(), logout(), exempt, limit, route

### Community 62 - "test_keep_alive.py"
Cohesion: 0.16
Nodes (7): ambiente_limpo(), fixture, parametrize, Garante que o keep-alive fica desligado por padrão e só pinga a própria origem., test_intervalo_fica_dentro_da_faixa(), test_nao_liga_com_valor_negativo(), test_ping_so_considera_200_como_sucesso()

### Community 63 - "ProfessorDAO"
Cohesion: 0.21
Nodes (14): remover_professor(), ProfessorDAO, _foto(), pasta_fotos(), professor(), fixture, parametrize, test_admin_salva_perfil_sem_alterar_acesso() (+6 more)

### Community 64 - "test_sessao_revogada.py"
Cohesion: 0.24
Nodes (11): Sessões encerradas pelo logout. A sessão do Flask é um cookie assinado, sem…, SessaoRevogada, _cliente_com_cookie(), _entrar_como_admin(), `session.clear()` só limpava o navegador de quem saiu; a cópia do cookie seguia…, test_logout_apaga_revogacoes_vencidas(), test_logout_de_uma_sessao_nao_derruba_as_outras(), test_logout_revoga_a_copia_do_cookie_feita_antes() (+3 more)

### Community 65 - "Relatório de segurança — Sistema Extreme Team"
Cohesion: 0.15
Nodes (12): Controles verificados, Histórico de auditorias, O que foi feito nesta rodada, Pendências não relacionadas a segurança, Relatório de segurança — Sistema Extreme Team, Rodada anterior (22/09/2026 — 2ª rodada), Rodada de 04/10/2026 — limites de requisição, Situação atual (20/10/2026 — hero 3D, OWASP/DevSecOps e dependências) (+4 more)

### Community 66 - "Academia"
Cohesion: 0.20
Nodes (10): Academia, parametrize, test_admin_salva_atualiza_e_limpa_contatos(), test_configuracoes_exigem_admin(), test_contatos_invalidos(), test_csrf_configuracoes(), test_erro_preserva_formulario_e_dados_salvos(), test_link_email_preserva_caracteres_do_endereco() (+2 more)

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
Cohesion: 0.13
Nodes (14): _paginar(), Aplica LIMIT/OFFSET e conta o total numa consulta separada e barata. A contagem…, Decimal, Matricula, _para_decimal(), Pedido de troca de plano agendado para a próxima renovação. Nunca altera o…, SolicitacaoMudancaPlano, postgres_pix() (+6 more)

### Community 73 - "analytics.test.cjs"
Cohesion: 0.18
Nodes (7): assert, CODIGO, Element, fs, path, test, vm

### Community 74 - "pagamento.js"
Cohesion: 0.35
Nodes (10): alvoDoRotulo(), consultarStatus(), gerarOuAtualizarPix(), iniciarPolling(), liberarBotao(), marcarOcupado(), mostrarEstado(), pararPolling() (+2 more)

### Community 75 - "test_perfil_e_foto.py"
Cohesion: 0.17
Nodes (16): pagina_perfil(), _turma_do_formulario(), TurmaDAO, Turma, Sonda: a data vem da query string e é convertida sem tratamento., test_data_invalida_na_turma_nao_derruba_a_rota(), test_escolher_plano_com_turma_cria_matricula(), test_turma_lotada_nao_vira_matricula_apos_pagamento() (+8 more)

### Community 76 - "test_email_componentes.py"
Cohesion: 0.33
Nodes (7): E-mails: base com a logo oficial e componentes seguros para cliente de e-mail…, _render(), _sem_recursos_externos(), test_base_sem_url_publica_cai_para_o_nome_em_texto(), test_base_usa_a_logo_quando_ha_url_publica(), test_botao_do_email_usa_o_ouro_do_sistema(), test_cartao_de_resumo_com_badge()

### Community 77 - "test_layouts.py"
Cohesion: 0.29
Nodes (8): _conferir_head_comum(), parametrize, Layouts base (templates/layouts/) e toasts. Cada página estende o layout da sua…, test_area_do_aluno_carrega_o_layout(), test_flash_de_erro_vira_toast_que_nao_some_sozinho(), test_paginas_publicas_carregam_o_head_comum(), test_painel_admin_carrega_o_layout_admin(), test_toda_pagina_estende_um_layout()

### Community 78 - "test_migracao_checkout.py"
Cohesion: 0.31
Nodes (8): _colunas(), conexao(), migracao(), fixture, Exercita a migração dos campos do Checkout Pro de verdade (upgrade e…, _rodar(), test_downgrade_remove_exatamente_o_que_o_upgrade_criou(), test_upgrade_adiciona_as_colunas_e_preserva_linhas_antigas()

### Community 79 - "mercado_pago_oauth_bp.py"
Cohesion: 0.38
Nodes (9): _autorizacao_valida(), callback(), conectar(), desconectar(), limit, route, O state devolvido é o que ESTA sessão emitiu, há pouco tempo?, Só monta o state/PKCE na sessão e manda o administrador ao Mercado Pago. É um… (+1 more)

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

### Community 85 - "Plano"
Cohesion: 0.18
Nodes (7): cadastrar_plano(), Plano, Preço de uma cobrança criada em `hoje`., parametrize, test_duas_requisicoes_pix_reutilizam_uma_cobranca_postgres(), Abrir o painel filtrado por um plano não pode tocar as mensalidades dos outros., test_painel_financeiro_nao_varre_mensalidades_fora_do_filtro()

### Community 86 - "MatriculaDAO"
Cohesion: 0.23
Nodes (15): MatriculaDAO, Presenca, impressao_credencial(), Resumo curto e não reversível do hash da senha, guardado na sessão. Nunca é a…, Valor que representa a credencial administrativa em vigor, ou None se não há…, referencia_credencial_admin(), parametrize, test_aluno_confirma_sua_frequencia() (+7 more)

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
Cohesion: 0.09
Nodes (40): _base_url_opcional(), buscar_pagamento(), buscar_pagamentos_por_referencia(), cancelar_pagamento(), criar_pagamento_pix(), criar_preferencia_checkout(), _erro_menciona(), _erro_menciona_expiracao() (+32 more)

### Community 99 - "backup.sh"
Cohesion: 1.00
Nodes (3): registrar(), reter(), backup.sh script

### Community 114 - "capturar_emails"
Cohesion: 0.67
Nodes (3): capturar_emails(), fixture, Intercepta o envio e devolve os e-mails que teriam saído, com os links.

### Community 116 - "conftest.py"
Cohesion: 0.27
Nodes (11): app(), client(), contexto_app(), limpar_banco(), logar_como_professor(), plano(), fixture, Substitui o provedor de e-mail em todos os módulos que o chamam. A suíte nunca… (+3 more)

### Community 117 - "ImagemGrandeDemais"
Cohesion: 0.17
Nodes (13): _conferir_dimensoes(), _detectar_tipo_imagem_real(), ImagemGrandeDemais, Imagem cujas DIMENSÕES declaradas passam do limite de pixels., Recusa pelo cabeçalho, antes de qualquer pixel ser decodificado. `Image.open`…, Confere o conteúdo de fato (decodificando com Pillow), não a extensão/Content-…, _png_bomba(), Bomba de descompressão: arquivo minúsculo, imagem gigante. O PNG aqui tem 285… (+5 more)

### Community 122 - "Contrato do redesign — SistemaEXTREMETEAM"
Cohesion: 0.09
Nodes (20): 0. Antes de escrever código, 1. Identidade visual (design tokens), 2. Logo oficial (usar SOMENTE a logo original), 3. Telas a implementar, 4. Regras e dados, 5. Forma de trabalhar, Painel administrativo (desktop, sidebar preta com o emblema do dragão), Prompt para o Claude Code — Redesign do SistemaEXTREMETEAM (+12 more)

### Community 123 - "test_planilha_economica.py"
Cohesion: 0.06
Nodes (59): 80', '80.5', '80,50' ou '1.234,56' -> Decimal. None se vazio; ValueError se…, _valor_em_reais(), alterar_despesa(), _ano_e_mes(), _ano_valido(), baixar_excel(), excluir_despesa(), _formulario_de() (+51 more)

### Community 124 - "cinema.test.cjs"
Cohesion: 0.11
Nodes (10): assert, CODIGO, conferirAtiva(), Elemento, fs, ListaDeClasses, montar(), path (+2 more)

### Community 125 - "compilerOptions"
Cohesion: 0.11
Nodes (18): compilerOptions, isolatedModules, jsx, lib, module, moduleResolution, noEmit, noUnusedLocals (+10 more)

### Community 126 - "pagamento.html (pagar mensalidade)"
Cohesion: 0.15
Nodes (17): cancelarAberturas(), consultar(), finalizarAbertura(), parar(), admin_academia.html — configurações da academia, Conexão OAuth do Mercado Pago (PKCE), Webhook de pagamentos do Mercado Pago (MERCADO_PAGO_WEBHOOK_SECRET), checkout_continuar.html — continuar no Mercado Pago (+9 more)

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

### Community 131 - "test_aprovacao_incoerente_nao_quita_mensalidade"
Cohesion: 0.23
Nodes (12): _agora_mercado_pago(), _assinar(), _pagamento_mp(), _preparar_para_conciliacao(), Hipótese: uma resposta 'approved' incoerente quita a mensalidade mesmo assim., Contraprova: com tudo batendo, a baixa acontece., Hipótese: assinatura válida basta para quitar, mesmo com valor errado., Reenvio da mesma notificação não pode gerar segunda baixa nem novo evento. (+4 more)

### Community 132 - "financeiro.html — painel financeiro"
Cohesion: 0.14
Nodes (13): ajustar(), aplicar(), Tom da mensagem por status do pagamento, acao() (ações da mensalidade), cartao() (situação do plano), badge(), Situações da mensalidade (pendente a reembolsado), badge() — etiqueta de situação no e-mail (+5 more)

### Community 133 - "Pagamento de mensalidade via Pix (Mercado Pago)"
Cohesion: 0.22
Nodes (9): Como obter credenciais de teste (modo manual, sem OAuth), Como testar localmente, Conectar a conta por OAuth (a academia não cria aplicativo), Instalar dependências, Pagamento de mensalidade via Pix (Mercado Pago), Produção, Trocando de credenciais de teste para produção, URL a cadastrar como webhook (+1 more)

### Community 134 - "gmail_conta.py"
Cohesion: 0.06
Nodes (42): GmailConexao, _access_token(), _cifrar(), _client_id(), _client_secret(), _decifrar(), enviar(), estado() (+34 more)

### Community 135 - "cinema.py"
Cohesion: 0.31
Nodes (8): _entradas(), modulo(), Arquivos do hero cinematográfico da página inicial. A cena 3D é compilada pelo…, {nome da entrada: arquivo}, lido uma vez: o build não muda com o servidor no ar., URL da entrada `nome` ('cena' ou 'video') do build, ou None se não foi…, URL do vídeo do hero, só se ele existir e a entrada que o toca estiver…, _tem_video(), video()

### Community 136 - "Skills Disponíveis"
Cohesion: 0.22
Nodes (8): Assistente e Automação (Antigravity), Ciências e Bioinformática (Plugins de Ciência), Dados e Google Cloud Platform (GCP), Desenvolvimento Mobile e Flutter/Dart, Desenvolvimento Web e Frontend, Firebase e Backend, GenAI e Machine Learning, Skills Disponíveis

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
Cohesion: 0.16
Nodes (24): ativar_acesso(), _cadastro_recebido(), _chave_ip_e_identificador(), _em_segundo_plano(), foto_perfil(), pagina_cadastro(), _pode_ver_foto(), _professor_pode_ver_aluno() (+16 more)

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
Cohesion: 0.27
Nodes (11): _autorizacao_valida(), callback(), login_google(), _novo_pkce(), limit, route, (code_verifier, code_challenge S256), como na conexão do Mercado Pago. O state…, O state devolvido é o que ESTA sessão emitiu, há pouco tempo? (+3 more)

### Community 152 - "Configuração de segurança"
Cohesion: 0.50
Nodes (4): Configuração de segurança, Credencial do administrador, Publicar com um domínio próprio, Segundo fator do administrador (opcional, recomendado)

### Community 155 - "test_data_nascimento.py"
Cohesion: 0.29
Nodes (10): data_iso(), A data em AAAA-MM-DD, o formato do <input type="date">, ou '' se não for uma…, parametrize, Data de nascimento: o mesmo seletor de data e a mesma regra no cadastro, na…, _salvar_ficha(), test_data_iso_aceita_aaaa_mm_dd_e_dd_mm_aaaa(), test_ficha_do_admin_grava_no_formato_do_seletor(), test_ficha_do_admin_recusa_data_invalida_ou_futura() (+2 more)

### Community 157 - "auth.test.cjs"
Cohesion: 0.25
Nodes (6): assert, CODIGO, fs, path, test, vm

### Community 158 - "credenciais.py"
Cohesion: 0.10
Nodes (25): admin_configurado(), codigo_totp(), comparar_em_tempo_constante(), credencial_admin_confere(), gerar_hash_admin(), gerar_segredo_totp(), _main(), _main_totp() (+17 more)

### Community 159 - "test_admin_mercado_pago.py"
Cohesion: 0.18
Nodes (14): _aprovado_no_checkout(), Painel do admin com mensalidades do Mercado Pago: formas de pagamento,…, Cartão/boleto: a preferência existe, o webhook ainda não trouxe o payment_id., _so_com_checkout(), test_admin_muda_o_status_sem_perder_a_forma_do_mercado_pago(), test_admin_nao_grava_forma_inventada(), test_aprovar_comprovante_recusa_forma_inventada(), test_ficha_mantem_no_select_a_forma_confirmada_pelo_mercado_pago() (+6 more)

### Community 161 - "ci-security-scanning-with-strix/SKILL.md"
Cohesion: 0.29
Nodes (6): GitHub Actions, Option A — Self-hosted OSS CLI in the runner, Option B — Managed platform (no runner infra), Optional: upload findings to GitHub code scanning, Other CI systems, Set up Strix in CI/CD

### Community 162 - "test_conversao_home.py"
Cohesion: 0.19
Nodes (14): _body_tag(), _html(), parametrize, Conversão na home: perguntas frequentes, CTA fixo no celular e página de…, test_admin_logado_nao_ve_o_cta_fixo(), test_aluno_logado_nao_ve_o_cta_fixo(), test_cta_fixo_fica_so_na_home(), test_cta_fixo_sem_whatsapp_so_tem_o_cadastro() (+6 more)

### Community 164 - "Find security vulnerabilities in code"
Cohesion: 0.29
Nodes (6): Complementary tooling, Find security vulnerabilities in code, Fix and verify, Read the results, Reviewing a pull request instead of the whole repo, Run it

### Community 165 - "requirements-dev.txt (requirements.txt + pytest + pip-audit)"
Cohesion: 0.67
Nodes (3): requirements-dev.txt (requirements.txt + pytest + pip-audit), pip-audit 2.10.1, pytest

### Community 166 - "painel_adm"
Cohesion: 0.22
Nodes (5): painel_adm(), Apaga um plano que nunca foi usado. True, None (não existe) ou False (em uso)., Planos que algum registro referencia: mensalidade, cadastro de aluno ou pedido…, Quantos alunos a academia tem, sem filtro de busca. O card do topo do painel é…, test_plano_so_no_cadastro_do_aluno_tambem_conta_como_em_uso()

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

### Community 173 - "gmail_oauth_bp.py"
Cohesion: 0.42
Nodes (8): callback(), conectar(), desconectar(), limit, route, _voltar(), chave_da_conta(), Chave de limite por CONTA, caindo no IP só para quem não está autenticado. A…

### Community 174 - "pagina_login"
Cohesion: 0.25
Nodes (7): _abrir_sessao_admin(), pagina_login(), Grava na sessão atual a credencial em vigor (login ou troca de senha bem-…, registrar_credencial(), O `login` de um aluno pode ser o e-mail de outro; quem entra é decidido pela…, test_login_com_identificador_repetido_em_outra_coluna_nao_bloqueia_a_vitima(), test_login_nao_aceita_nome_do_aluno()

### Community 175 - "_pagamento_com_acesso_ou_404"
Cohesion: 0.43
Nodes (7): _acesso_permitido_pagamento(), comprovante_mensalidade(), _pagamento_com_acesso_ou_404(), pagina_pagamento(), Há alguém autorizado a ver mensalidades nesta sessão (admin ou aluno ativo)?, _sessao_financeira_valida(), ver_comprovante_manual()

### Community 176 - "limites_pagamento.py"
Cohesion: 0.50
Nodes (3): chave_pagamento(), Orçamentos compartilhados das chamadas interativas ao provedor de pagamento., A mesma conta mantém seu limite entre sessões, rotas e mensalidades. Alunos que…

## Ambiguous Edges - Review These
- `botao_google.html` → `Integração com o Gmail (conta remetente da academia)`  [AMBIGUOUS]
  templates/politica_privacidade.html · relation: conceptually_related_to

## Knowledge Gaps
- **324 isolated node(s):** `name`, `private`, `version`, `description`, `type` (+319 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `botao_google.html` and `Integração com o Gmail (conta remetente da academia)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `PagamentoDAO` connect `PagamentoDAO` to `Aluno`, `test_aprovacao_incoerente_nao_quita_mensalidade`, `usuario_e_admin`, `logar_como_admin`, `route`, `PlanoDAO`, `criar_aluno`, `criar_pagamento`, `usuario_bp.py`, `pix_bp.py`, `.listar_por_aluno`, `test_seguranca.py`, `test_pix_rotas.py`, `test_auditoria_seguranca.py`, `checkout_bp.py`, `test_mudanca_plano.py`, `test_admin_mercado_pago.py`, `test_pagamento_recusado.py`, `PagamentoEvento`, `_pagamento_com_acesso_ou_404`, `.buscar_por_id`, `logar_como_aluno`, `adm_bp.py`, `config.py`, `test_perfil_e_foto.py`, `MatriculaDAO`, `test_comprovante_sem_metadados.py`, `conftest.py`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Why does `Vitrine de componentes (/_vitrine)` connect `csrf_field.html` to `config.py`, `avatar`, `componentes.js`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Why does `logar_como_admin()` connect `logar_como_admin` to `test_admin_segundo_fator.py`, `test_mercado_pago_oauth.py`, `test_seo.py`, `gmail_conta.py`, `PlanoDAO`, `PagamentoDAO`, `criar_aluno`, `criar_pagamento`, `.listar_por_aluno`, `test_data_nascimento.py`, `test_pix_rotas.py`, `test_seguranca.py`, `test_admin_mercado_pago.py`, `test_mudanca_plano.py`, `test_conversao_home.py`, `test_home_planos.py`, `test_analytics.py`, `.buscar_por_id`, `logar_como_aluno`, `test_trocar_a_credencial_do_admin_encerra_a_sessao_administrativa`, `ProfessorDAO`, `test_sessao_revogada.py`, `Academia`, `test_perfil_e_foto.py`, `test_layouts.py`, `test_publicas_redesign.py`, `Plano`, `MatriculaDAO`, `conftest.py`, `test_planilha_economica.py`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 158 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 158 INFERRED edges - model-reasoned connections that need verification._
- **Are the 171 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 171 INFERRED edges - model-reasoned connections that need verification._
- **Are the 170 inferred relationships involving `logar_como_admin()` (e.g. with `test_admin_salva_atualiza_e_limpa_contatos()` and `test_csrf_configuracoes()`) actually correct?**
  _`logar_como_admin()` has 170 INFERRED edges - model-reasoned connections that need verification._