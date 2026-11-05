# Graph Report - SistemaEXTREMETEAM  (2026-11-04)

## Corpus Check
- 214 files · ~278,831 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3104 nodes · 7316 edges · 181 communities (167 shown, 14 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 1321 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `60b6d8a1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Aluno
- Componentes
- test_admin_segundo_fator.py
- Professor
- test_seo.py
- adm_bp.py
- turma_bp.py
- AlunoDAO
- planos.py
- route
- test_admin_mercado_pago.py
- financeiro.html — painel financeiro
- index.html (home pública)
- test_financeiro_dao.py
- test_regressao_auditoria.py
- fase3b.js
- test_auditoria_seguranca.py
- salvar_foto_perfil
- fila_email.py
- csrf_field.html
- armazenamento.py
- test_google_login.py
- pix_bp.py
- servidor.py
- PagamentoDAO
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
- seo.py
- PlanoDAO
- URLPublicaInvalida
- varredura.mjs
- test_pagamento_recusado.py
- MercadoPagoConexao
- avatar
- ConfiguracaoInvalida
- test_observabilidade.py
- test_analytics.py
- requirements.txt (dependências de produção)
- gmail_conta.py
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
- ProfessorDAO
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
- turnstile.py
- MatriculaDAO
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
- logar_como_admin
- salvar_comprovante_manual
- agendar.sh
- restaurar.sh
- Contrato do redesign — SistemaEXTREMETEAM
- conftest.py
- cinema.test.cjs
- compilerOptions
- pgUsuario.html (área do aluno)
- penetration-testing-with-strix/SKILL.md
- test_cinema.py
- SistemaEXTREMETEAM
- test_paginas_erro.py
- EmailPendente
- erro_validacao_senha
- Pagamento de mensalidade via Pix (Mercado Pago)
- usuario_bp.py
- cinema.py
- Skills Disponíveis
- criar_aluno
- cinema.js
- Etapa 1 — migrar páginas para os layouts (SEM mudar o visual)
- Etapas 4 a 6 — aluno, admin, professor (aplicar os componentes nas páginas)
- emblema.py
- Banco de dados e migrations
- Etapa 2 — biblioteca de componentes
- Cadastro de aluno pela administração e ativação de acesso
- Outras formas de pagamento (Checkout Pro)
- pagina_cadastro
- Etapa 3 — home com os planos + termos
- test_fontes_locais.py
- Biblioteca no Figma
- CLAUDE.md
- keep_alive.py
- Configuração de segurança
- ler_arquivo
- test_logs_sem_dado_pessoal.py
- auth.test.cjs
- credenciais.py
- .buscar_por_id
- pagina_login
- ci-security-scanning-with-strix/SKILL.md
- .totais_periodo
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
- gmail_oauth_bp.py
- test_email_gmail.py
- _convidar_cadastro_existente
- ResultadoContratacao
- .contar_cadastrados
- _ler_promocao
- limites_pagamento.py

## God Nodes (most connected - your core abstractions)
1. `PagamentoDAO` - 243 edges
2. `criar_aluno()` - 172 edges
3. `criar_pagamento()` - 172 edges
4. `logar_como_admin()` - 171 edges
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
- `test_refresh_token_fica_cifrado_no_banco()` --uses--> `GmailConexao`  [INFERRED]
  tests/test_email_gmail.py → modelos/gmail_conexao.py
- `Envio de comprovante manual (et-upload, até 4 MB)` --references--> `salvar_comprovante_manual()`  [EXTRACTED]
  templates/pagamento.html → servicos/armazenamento.py

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

## Communities (181 total, 14 thin omitted)

### Community 0 - "Aluno"
Cohesion: 0.08
Nodes (19): Matrícula feita no balcão: sem login, sem senha e sem convite de acesso. Nasce…, Aluno, Se existe uma conta de acesso, e não se o aluno está em dia ou matriculado.…, Convite de acesso já enviado e ainda não usado (a validade é checada na rota)., Chave do estado da CONTA - nunca da situação financeira nem da matrícula., test_cadastro_publico_recusa_confirmacao_diferente(), test_cadastro_publico_recusa_confirmacao_vazia(), parametrize (+11 more)

### Community 1 - "Componentes"
Cohesion: 0.05
Nodes (36): Altura de controle, Avisos flutuantes, Botões — `.et-botao` + variante (+ tamanho), Cartões e contêineres, Componentes, Contêiner e estrutura, Cores, Dados (+28 more)

### Community 2 - "test_admin_segundo_fator.py"
Cohesion: 0.20
Nodes (20): _codigo_agora(), _codigo_errado(), _destino(), _entrar_com_senha(), fixture, parametrize, Segundo fator do administrador (SEC-30). Com ADMIN_TOTP_SECRET definida, a…, segundo_fator() (+12 more)

### Community 3 - "Professor"
Cohesion: 0.17
Nodes (10): TurmaDAO, Professor, Turma, Sonda: a data vem da query string e é convertida sem tratamento., test_data_invalida_na_turma_nao_derruba_a_rota(), test_escolher_plano_com_turma_cria_matricula(), test_turma_lotada_nao_vira_matricula_apos_pagamento(), fixture (+2 more)

### Community 4 - "test_seo.py"
Cohesion: 0.10
Nodes (25): _head(), _json_ld(), parametrize, SEO técnico: robots.txt, sitemap, títulos, meta tags, noindex e JSON-LD da home., Nenhum campo do JSON-LD pode sair nulo, vazio ou só com espaços., _robots(), _sem_vazios(), test_area_do_admin_sai_do_indice() (+17 more)

### Community 5 - "adm_bp.py"
Cohesion: 0.09
Nodes (51): _aluno_do_cpf_ou_painel(), aprovar_aluno(), aprovar_comprovante_manual(), arquivar_plano(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_pagamento(), _chave_lote() (+43 more)

### Community 6 - "turma_bp.py"
Cohesion: 0.16
Nodes (17): _acesso_permitido(), cadastrar_professor(), cadastrar_turma(), desmatricular_aluno(), detalhe_turma(), editar_professor(), gerenciar_turmas(), matricular_aluno() (+9 more)

### Community 7 - "AlunoDAO"
Cohesion: 0.12
Nodes (44): AlunoDAO, _matricular(), parametrize, Cadastro de aluno pela administração, ativação de acesso e confirmação de…, test_admin_lanca_e_baixa_mensalidade_de_aluno_sem_acesso(), test_admin_matricula_aluno_sem_email_senha_nem_acesso(), test_admin_pode_deixar_cadastro_de_balcao_sem_usuario_e_sem_email(), test_admin_rejeita_status_financeiro_desconhecido() (+36 more)

### Community 8 - "planos.py"
Cohesion: 0.06
Nodes (42): cadeia_paga(), cartao_do_plano(), cobranca_a_pagar(), cobranca_em_decisao(), cobranca_pendente(), duracao_dias(), _duracao_por_extenso(), esta_inadimplente() (+34 more)

### Community 9 - "route"
Cohesion: 0.20
Nodes (20): alterar_senha_perfil(), _aluno_da_sessao(), _aluno_por_token(), atualizar_dados_perfil(), cancelar_mudanca_plano(), confirmar_email(), confirmar_presenca(), enviar_comprovante_manual_aluno() (+12 more)

### Community 10 - "test_admin_mercado_pago.py"
Cohesion: 0.18
Nodes (14): _aprovado_no_checkout(), Painel do admin com mensalidades do Mercado Pago: formas de pagamento,…, Cartão/boleto: a preferência existe, o webhook ainda não trouxe o payment_id., _so_com_checkout(), test_admin_muda_o_status_sem_perder_a_forma_do_mercado_pago(), test_admin_nao_grava_forma_inventada(), test_aprovar_comprovante_recusa_forma_inventada(), test_ficha_mantem_no_select_a_forma_confirmada_pelo_mercado_pago() (+6 more)

### Community 11 - "financeiro.html — painel financeiro"
Cohesion: 0.13
Nodes (14): ajustar(), aplicar(), Tom da mensagem por status do pagamento, badge(), Situações da mensalidade (pendente a reembolsado), email/base.html — layout dos e-mails, email/componentes.html — macros de e-mail, badge() — etiqueta de situação no e-mail (+6 more)

### Community 12 - "index.html (home pública)"
Cohesion: 0.13
Nodes (12): faq_estruturado(), Textos editáveis da página inicial: perguntas frequentes e prazos de…, JSON-LD FAQPage com exatamente as perguntas mostradas na página., cabecalho, entrarFixo, icone_senha, input_senha, modal (+4 more)

### Community 13 - "test_financeiro_dao.py"
Cohesion: 0.10
Nodes (17): Carrega aluno e plano junto das mensalidades. O template do painel lê…, Lista completa (sem paginar). Mantida para relatórios e testes., True se já existe um Pix ou um checkout válido emitido para esta cobrança.…, True se a cobrança Pix já gerada para este pagamento ainda pode ser…, True se a preferência do Checkout Pro já criada pode ser reaproveitada. Só…, provider_payment_id sozinho não basta: pagamentos do Checkout Pro…, test_listar_filtrado_por_status_e_busca_de_aluno(), test_marcar_pago_via_webhook_sincroniza_mensalidade_do_aluno() (+9 more)

### Community 14 - "test_regressao_auditoria.py"
Cohesion: 0.04
Nodes (40): _contar_selects_em_alunos(), _credencial(), Regressões da auditoria de segurança, desempenho e confiabilidade. Cada caso…, Head-of-line blocking: a primeira linha falhando não pode impedir as seguintes.…, Uma linha `desistiu` nunca foi entregue: recusar o reenvio fazia a tela dizer…, A revivência vale só para o abandonado: clique duplo continua virando um envio., Trocar senha, e-mail ou foto são ações de quem JÁ está autenticado. Devolver o…, Persistência não é retomada: alguém precisa acordar a fila quando o adiamento… (+32 more)

### Community 15 - "fase3b.js"
Cohesion: 0.06
Nodes (47): avisos, bind(), caixas, campos, col(), D(), estados, faixa (+39 more)

### Community 16 - "test_auditoria_seguranca.py"
Cohesion: 0.08
Nodes (37): _agora_mercado_pago(), _assinar(), _pagamento_mp(), _preparar_para_conciliacao(), parametrize, Auditoria de segurança: sondas escritas para TENTAR quebrar as regras. Nenhum…, Hipótese: as rotas de cobrança respondem sem sessão nenhuma., Hipótese: a sessão de professor é aceita nas rotas financeiras do aluno. (+29 more)

### Community 17 - "salvar_foto_perfil"
Cohesion: 0.18
Nodes (19): ArquivoInvalido, Exception, Valida, reprocessa e salva uma foto de perfil. Retorna o nome do arquivo…, Arquivo recusado por tipo, tamanho ou conteúdo não confiável., salvar_foto_perfil(), _jpeg(), Uploads no Supabase Storage (produção na Vercel), com o HTTP simulado., test_chave_secreta_nova_vai_so_no_apikey() (+11 more)

### Community 18 - "fila_email.py"
Cohesion: 0.10
Nodes (25): espera_da_proxima_tentativa(), Fila de e-mails no banco. Aviso e cobrança coletivos saíam um a um dentro da…, contar_falhados(), contar_pendentes(), disparar(), enfileirar(), enfileirar_transacional(), _entregar() (+17 more)

### Community 19 - "csrf_field.html"
Cohesion: 0.13
Nodes (20): Contato e localização da academia, ativar_acesso.html — ativar acesso pelo convite, cadastro.html — criar conta, cadastro_obrigado.html — cadastro recebido, Cadastro com PRG e resposta única, Aceite do Termo de Responsabilidade, Modal de login da home (#meuModal, POST /login), layouts/publico.html — layout das telas públicas (+12 more)

### Community 20 - "armazenamento.py"
Cohesion: 0.14
Nodes (21): ArmazenamentoIndisponivel, _exif_so_com_orientacao(), _gravar(), _jpeg_sem_metadados(), _nome_valido(), _orientacao(), _pasta(), _png_sem_metadados() (+13 more)

### Community 21 - "test_google_login.py"
Cohesion: 0.08
Nodes (24): Esquece a conta conectada. Devolve True se havia uma., remover_conexao(), fixture, Registra as chamadas e devolve as respostas configuradas por método., storage(), _StorageFalso, test_envia_pelo_gmail_com_o_refresh_token_da_conexao(), cliente_google() (+16 more)

### Community 22 - "pix_bp.py"
Cohesion: 0.06
Nodes (43): _chave_entrega_webhook(), _data_da_aprovacao(), _forma_pagamento_confirmada(), _instante_utc(), _iso_utc(), _liberar_entrega_webhook(), _mensalidade_da_referencia(), _pagamento_mp_mais_relevante() (+35 more)

### Community 23 - "servidor.py"
Cohesion: 0.10
Nodes (26): after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, route, robots(), sitemap(), errorhandler, Registra a sessão como encerrada: cópias antigas do cookie deixam de valer.… (+18 more)

### Community 24 - "PagamentoDAO"
Cohesion: 0.05
Nodes (65): criar_pix_mensalidade(), _processar_status_mp(), limitar_criacao_pagamento, Fonte unica de aprovacao, usada pelo webhook, pelo polling de status e pela…, _tratar_webhook(), PagamentoDAO, A recusa (criada em `criada_em`, UTC) é de antes da última nova tentativa? Sem…, Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.… (+57 more)

### Community 25 - "test_turnstile.py"
Cohesion: 0.15
Nodes (10): _cadastrar(), Turnstile da Cloudflare no cadastro público (SEC-36). O cadastro manda e-mail…, _Resposta, _Siteverify, test_cadastro_com_token_valido_segue_o_fluxo_de_sempre(), test_cadastro_sem_token_nao_cria_conta_nem_manda_email(), test_sem_turnstile_configurado_nada_carrega(), test_siteverify_fora_do_ar_recusa_o_cadastro() (+2 more)

### Community 26 - "mercado_pago_conta.py"
Cohesion: 0.10
Nodes (37): access_token_vigente(), _agora(), ambiente_da_conexao(), _cifrar(), _client_id(), _client_secret(), ConexaoIlegivel, _configuracao_do_aplicativo() (+29 more)

### Community 27 - "test_seguranca.py"
Cohesion: 0.08
Nodes (24): _cadastro_publico(), _imagem_jpeg(), _mensagem_da_resposta(), O `login` de um aluno pode ser o e-mail de outro; quem entra é decidido pela…, O ramo "par existe" não pode pagar a ida ao provedor dentro da requisição., Cadastro novo, CPF existente e e-mail existente respondem com a MESMA tela., Quem ainda controla a caixa antiga não pode assumir a conta depois da troca., test_cabecalhos_de_seguranca() (+16 more)

### Community 28 - "test_pix_rotas.py"
Cohesion: 0.19
Nodes (21): _agora_mercado_pago(), _assinar(), _resposta_consulta(), _resposta_criacao(), test_admin_tambem_pode_gerar_pix(), test_aluno_gera_pix_da_propria_mensalidade(), test_aluno_nao_acessa_mensalidade_de_outro_aluno(), test_falha_de_indisponibilidade_do_mp_retorna_503() (+13 more)

### Community 29 - "test_fila_email_concorrencia_postgres.py"
Cohesion: 0.18
Nodes (10): _enfileirar_em_transacao_propria(), postgres_fila(), fixture, Idempotência da fila de e-mail sob concorrência real, em PostgreSQL…, A recusa de uma chave repetida não pode desfazer o lote inteiro. Um…, A trava do lote precisa valer até o fim do lote. Comitar linha a linha…, Enfileira e comita numa sessão própria, como faria outra requisição., test_chave_duplicada_nao_descarta_os_outros_destinatarios_do_lote() (+2 more)

### Community 30 - "planilha_excel.py"
Cohesion: 0.30
Nodes (13): Nome legível da forma de pagamento. Antes as telas usavam `|replace('_','…, rotulo_forma_pagamento(), _aba_categorias(), _aba_entradas(), _aba_resumo(), _aba_saidas(), _cabecalho(), _escrever() (+5 more)

### Community 31 - "checkout_bp.py"
Cohesion: 0.11
Nodes (29): abrir_checkout(), _acesso_permitido(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), limitar_consulta_pagamento, limitar_criacao_pagamento, route (+21 more)

### Community 32 - "test_mudanca_plano.py"
Cohesion: 0.15
Nodes (27): cancelar_mudanca_plano_admin(), A administração pode cancelar um pedido de troca ainda não aplicado. Não existe…, Persistência dos pedidos de troca de plano agendados para a próxima renovação., Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, SolicitacaoPlanoDAO, _agendar(), _pagar(), plano_barato() (+19 more)

### Community 33 - "ui.html"
Cohesion: 0.10
Nodes (28): campoDuracao, campoPreco, formularioPlano, cartao_plano(), secao_planos(), estado_vazio(), interruptor(), metrica() (+20 more)

### Community 34 - "test_mercado_pago_servico.py"
Cohesion: 0.09
Nodes (35): buscar_pagamentos_por_referencia(), Lista os pagamentos que o Mercado Pago associa a uma external_reference. Usada…, Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, validar_assinatura_webhook(), Hipótese: uma notificação capturada ontem pode ser reenviada hoje., `ts=nan` fazia a comparação da janela dar False e passava pela checagem de…, test_webhook_recusa_assinatura_antiga(), test_webhook_recusa_ts_nao_numerico_finito() (+27 more)

### Community 35 - "test_limites_requisicao.py"
Cohesion: 0.12
Nodes (28): consultar_mp(), _estourar(), fixture, parametrize, Limites de requisição da rodada de 04/10/2026 (SEC-10 a SEC-17 e SEC-19). Cada…, Trocar de rede ou abrir outra sessão não devolve a cota de e-mails em massa., Faz `limite` requisições sem nenhum 429 e devolve a seguinte., Alunos no mesmo Wi-Fi não dividem o teto padrão, nem com o visitante anônimo. (+20 more)

### Community 36 - "Pagina"
Cohesion: 0.14
Nodes (5): Pagina, Uma fatia de resultados já recortada pelo banco, com o que a navegação precisa., Uma página existe mesmo quando está vazia. Sem isto, `__len__` fazia `{% if…, `__len__` fazia `{% if pagina %}` ser falso numa página sem itens, escondendo…, test_pagina_vazia_ainda_mostra_a_navegacao()

### Community 37 - "seo.py"
Cohesion: 0.18
Nodes (18): conteudo_robots(), conteudo_sitemap(), dados_estruturados_academia(), _dia(), _dias_da_linha(), _hora(), horarios_estruturados(), origem_publica() (+10 more)

### Community 38 - "PlanoDAO"
Cohesion: 0.08
Nodes (45): cadastrar_aluno(), editar_plano(), painel_adm(), Nome, preço, duração e promoção. Vale para as cobranças criadas daqui em…, Matrícula feita pela administração, sem conta de acesso. Pede só o que…, pagina_perfil(), _plano_do_formulario(), PlanoDAO (+37 more)

### Community 39 - "URLPublicaInvalida"
Cohesion: 0.11
Nodes (27): route, verificar_email_cadastro(), aluno_do_token(), ConviteIndisponivel, descartar(), enviar(), gerar_token(), _hash() (+19 more)

### Community 40 - "varredura.mjs"
Cohesion: 0.11
Nodes (23): aberto(), ACESSO, auditar(), { chromium }, CONF, confirmacoes(), crc, CREDS (+15 more)

### Community 41 - "test_pagamento_recusado.py"
Cohesion: 0.26
Nodes (21): _assinar(), _data_mp(), _eventos(), _mockar_mp(), _pagamento_mp(), _pix_criado(), Mensalidade recusada: a próxima tentativa do aluno a reabre, e a recusa antiga…, Mensalidade cujo cartão acabou de ser recusado no Checkout Pro. (+13 more)

### Community 42 - "MercadoPagoConexao"
Cohesion: 0.19
Nodes (10): MercadoPagoConexao, Conta do Mercado Pago que a academia autorizou por OAuth. Uma linha só (a…, postgres_mp(), fixture, Renovação do token OAuth com trava de linha real, opcional na suíte que usa…, _Resposta, test_dois_processos_perto_do_vencimento_gastam_o_refresh_token_uma_vez(), _migracao() (+2 more)

### Community 43 - "avatar"
Cohesion: 0.12
Nodes (16): avatar(), breadcrumb(), Biblioteca de componentes .et-* (componentes.css), Seção Nossa equipe (professores_publicos), Nosso método: criar conta, aguardar aprovação, contratar plano e treinar, Cadastros pendentes (aprovar ou recusar aluno), Tabela de alunos paginada com busca no servidor, pgProfessor.html (minhas turmas do professor) (+8 more)

### Community 44 - "ConfiguracaoInvalida"
Cohesion: 0.28
Nodes (12): _autorizacao_valida(), callback(), conectar(), desconectar(), limit, route, O state devolvido é o que ESTA sessão emitiu, há pouco tempo?, Só monta o state/PKCE na sessão e manda o administrador ao Mercado Pago. É um… (+4 more)

### Community 45 - "test_observabilidade.py"
Cohesion: 0.14
Nodes (20): before_breadcrumb(), before_send(), iniciar_sentry(), _limpar(), mascarar(), Rastreamento de erros opcional com Sentry. Sem `SENTRY_DSN`, nada é importado…, _evento(), fixture (+12 more)

### Community 46 - "test_analytics.py"
Cohesion: 0.14
Nodes (20): _carrega_analytics(), com_analytics(), _csp_com_google(), _evento(), fixture, parametrize, GA4 opcional (servicos/analytics.py): nada sem ANALYTICS_ID, nunca em área…, sem_analytics_por_padrao() (+12 more)

### Community 47 - "requirements.txt (dependências de produção)"
Cohesion: 0.12
Nodes (19): requirements.txt (dependências de produção), cryptography 50.0.1, requirements-dev.txt (requirements.txt + pytest + pip-audit), pip-audit 2.10.1, pytest, Flask 3.1.3, Flask-Limiter[redis] 4.1.1, Flask-Migrate 4.1.0 (+11 more)

### Community 48 - "gmail_conta.py"
Cohesion: 0.27
Nodes (15): GmailConexao, _access_token(), _cifrar(), _client_id(), _client_secret(), _decifrar(), enviar(), estado() (+7 more)

### Community 49 - "criar_pagamento"
Cohesion: 0.06
Nodes (70): criar_pagamento(), logar_como_aluno(), Hipótese: forjar ?status=approved na volta do MP quita a mensalidade., Hipótese: cada clique cria uma cobrança nova no Mercado Pago., Hipótese: dá para injetar o valor pelo corpo do POST., Verifica a trava antes da emissão e o reaproveitamento na próxima chamada.…, test_dois_cliques_reaproveitam_a_mesma_preferencia(), test_pix_exige_trava_e_reutiliza_a_cobranca() (+62 more)

### Community 50 - "test_planilha_economica.py"
Cohesion: 0.06
Nodes (59): 80', '80.5', '80,50' ou '1.234,56' -> Decimal. None se vazio; ValueError se…, _valor_em_reais(), alterar_despesa(), _ano_e_mes(), _ano_valido(), baixar_excel(), excluir_despesa(), _formulario_de() (+51 more)

### Community 51 - "analytics.js"
Cohesion: 0.14
Nodes (12): analytics_ativo(), id_analytics(), marcar_conversao_cadastro(), Google Analytics 4 opcional, só em página pública e só com consentimento. Sem…, Chamada no arranque: um ID malformado derruba a subida, como as demais…, Esta resposta pode carregar o GA4? Visitante, página pública indexável ou…, validar_configuracao(), apagarCookiesGa() (+4 more)

### Community 52 - "package.json"
Cohesion: 0.05
Nodes (38): dependencies, maath, react, react-dom, @react-three/drei, @react-three/fiber, scrolly-video, three (+30 more)

### Community 53 - "test_home_planos.py"
Cohesion: 0.14
Nodes (20): cadastrar_plano(), _ler_plano(), Nome, preço e duração do formulário de plano: `(campos, None)` ou `(None,…, Marca o plano em destaque da página inicial, desmarcando qualquer outro.…, Inclusive os arquivados: serve a quem olha o histórico (filtro do financeiro)., Planos da página inicial, prontos para `components/cartao_plano.html`. O preço…, vitrine_planos(), _plano() (+12 more)

### Community 54 - "Strix Cloud (managed, no local infra)"
Cohesion: 0.12
Nodes (15): 0. Credits & top-ups, 1. Register the target as an asset, 2. Launch a scan, 3. Wait for completion, 4. Read findings, 5. Export & report, 6. PR reviews, 7. Continuous testing (schedules & webhooks) (+7 more)

### Community 55 - "autorizacao.py"
Cohesion: 0.20
Nodes (16): _acesso_permitido(), foto_professor(), aluno_autorizado(), aluno_requerido(), _credencial_confere(), encerrar_sessao(), professor_autorizado(), Autorização das rotas protegidas. A sessão diz quem *afirmou* ser quem; quem… (+8 more)

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

### Community 66 - "ProfessorDAO"
Cohesion: 0.14
Nodes (21): remover_professor(), ProfessorDAO, logar_como_professor(), fixture, Hipótese: a foto continua acessível por URL depois de tirar a publicação., Hipótese: os contatos vazam na home antes de a publicação ser marcada., test_contatos_do_professor_so_aparecem_quando_publicados(), test_foto_do_professor_some_ao_despublicar() (+13 more)

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
Cohesion: 0.07
Nodes (28): chave_da_conta(), Chave de limite por CONTA, caindo no IP só para quem não está autenticado. A…, mensalidade_destaque(), _paginar(), Uma página de mensalidades, recortada pelo banco (LIMIT/OFFSET). O painel…, Escolhe a mensalidade mais relevante para o card 'Minha mensalidade': a mais…, Aplica LIMIT/OFFSET e conta o total numa consulta separada e barata. A contagem…, Decimal (+20 more)

### Community 73 - "analytics.test.cjs"
Cohesion: 0.18
Nodes (7): assert, CODIGO, Element, fs, path, test, vm

### Community 74 - "test_conversao_home.py"
Cohesion: 0.23
Nodes (10): _body_tag(), _html(), Conversão na home: perguntas frequentes, cadastro no hero e página de obrigado., test_cadastro_fica_no_hero(), test_home_mostra_as_perguntas_frequentes_em_details(), test_home_nao_tem_barra_fixa_de_cadastro(), test_json_ld_faq_repete_exatamente_as_perguntas_da_pagina(), test_pagina_de_obrigado_explica_os_proximos_passos_e_sai_do_indice() (+2 more)

### Community 75 - "_parece_busca_por_cpf"
Cohesion: 0.17
Nodes (12): _parece_busca_por_cpf(), O termo é um CPF, ou um pedaço dele, e não um nome que por acaso tem número?, parametrize, Qualquer dígito no termo virava `CPF LIKE '%3%'` e devolvia a academia inteira., Rotas que custam hash de senha, processamento de imagem ou sondagem de token., Limites declarados por decorador NAQUELA rota. `resolve_limits` não serve aqui:…, Guarda do teste acima: uma rota sem limite precisa ser reprovada por ele., _tem_limite() (+4 more)

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
Nodes (22): configuracoes(), _pagina(), route, O administrador foi ao Mercado Pago e a autorização não voltou para cá? O state…, tentativa_sem_retorno(), context_processor, Academia, link_email() (+14 more)

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

### Community 85 - "turnstile.py"
Cohesion: 0.27
Nodes (12): ativo_nesta_resposta(), _chave_site(), configurado(), hostnames_esperados(), Cloudflare Turnstile no cadastro público (SEC-36). O cadastro manda e-mail para…, Sites onde o widget pode ter sido resolvido, como a Cloudflare os informa., Chamada no arranque. `exigir` é verdadeiro em produção (endereço público em…, Para o template: a chave pública do widget, ou vazio quando o Turnstile está… (+4 more)

### Community 86 - "MatriculaDAO"
Cohesion: 0.22
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

### Community 93 - "google_login.py"
Cohesion: 0.33
Nodes (9): _autorizacao_valida(), callback(), login_google(), _novo_pkce(), limit, route, (code_verifier, code_challenge S256), como na conexão do Mercado Pago. O state…, O state devolvido é o que ESTA sessão emitiu, há pouco tempo? (+1 more)

### Community 95 - "d9e2f6a14c80_contatos_academia_perfis_professores.py"
Cohesion: 0.83
Nodes (3): _campos_professor(), downgrade(), upgrade()

### Community 97 - "vercel.json"
Cohesion: 0.50
Nodes (3): gru1, regions, $schema

### Community 98 - "mercado_pago.py"
Cohesion: 0.11
Nodes (30): _base_url_opcional(), base_url_publica(), cancelar_pagamento(), criar_pagamento_pix(), criar_preferencia_checkout(), _erro_menciona(), _erro_menciona_expiracao(), _extrair_dados_pix() (+22 more)

### Community 99 - "backup.sh"
Cohesion: 1.00
Nodes (3): registrar(), reter(), backup.sh script

### Community 114 - "capturar_emails"
Cohesion: 0.67
Nodes (3): capturar_emails(), fixture, Intercepta o envio e devolve os e-mails que teriam saído, com os links.

### Community 116 - "logar_como_admin"
Cohesion: 0.12
Nodes (26): logar_como_admin(), test_admin_nao_pode_apagar_o_usuario_de_uma_conta_ativa(), test_convite_recusado_para_quem_ja_tem_acesso(), test_consulta_com_data_valida_preserva_data_selecionada(), _preparar_state(), parametrize, test_aviso_de_autorizacao_vencida_aparece_uma_vez(), test_callback_avisa_quando_a_conta_muda() (+18 more)

### Community 117 - "salvar_comprovante_manual"
Cohesion: 0.14
Nodes (16): _conferir_dimensoes(), _detectar_tipo_imagem_real(), ImagemGrandeDemais, Imagem cujas DIMENSÕES declaradas passam do limite de pixels., Recusa pelo cabeçalho, antes de qualquer pixel ser decodificado. `Image.open`…, Confere o conteúdo de fato (decodificando com Pillow), não a extensão/Content-…, Valida e salva um comprovante manual (JPEG, PNG ou PDF). Imagens passam pelo…, salvar_comprovante_manual() (+8 more)

### Community 122 - "Contrato do redesign — SistemaEXTREMETEAM"
Cohesion: 0.09
Nodes (20): 0. Antes de escrever código, 1. Identidade visual (design tokens), 2. Logo oficial (usar SOMENTE a logo original), 3. Telas a implementar, 4. Regras e dados, 5. Forma de trabalhar, Painel administrativo (desktop, sidebar preta com o emblema do dragão), Prompt para o Claude Code — Redesign do SistemaEXTREMETEAM (+12 more)

### Community 123 - "conftest.py"
Cohesion: 0.27
Nodes (11): app(), client(), contexto_app(), limpar_banco(), logar_como_professor(), plano(), fixture, Substitui o provedor de e-mail em todos os módulos que o chamam. A suíte nunca… (+3 more)

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
Nodes (6): erro_interno(), csrf_ligado(), fixture, Página de erro (templates/erro.html) e os handlers de 404, 403, 500 e CSRF., test_404_para_quem_esta_logado_leva_a_area_dele(), test_500_mostra_a_pagina_de_erro()

### Community 131 - "EmailPendente"
Cohesion: 0.25
Nodes (5): EmailPendente, parametrize, Agendamento sem rede, threads reais ou esperas de relógio., test_nao_inicia_em_testes(), test_retomada_de_item_persistido_e_retentativa_sem_painel()

### Community 132 - "erro_validacao_senha"
Cohesion: 0.22
Nodes (9): ativar_acesso(), Transforma um cadastro feito no balcão na conta do próprio aluno. Quem chega…, _carregar_senhas_comuns(), Lista de senhas comuns recusadas (cerca de 3000; ASVS 5.0 6.2.4 e NIST 800-63B), erro_confirmacao_senha(), erro_validacao_senha(), Retorna uma mensagem quando a senha é curta, comum ou igual ao identificador., Retorna uma mensagem quando a confirmação não repete exatamente a senha. A… (+1 more)

### Community 133 - "Pagamento de mensalidade via Pix (Mercado Pago)"
Cohesion: 0.22
Nodes (9): Como obter credenciais de teste (modo manual, sem OAuth), Como testar localmente, Conectar a conta por OAuth (a academia não cria aplicativo), Instalar dependências, Pagamento de mensalidade via Pix (Mercado Pago), Produção, Trocando de credenciais de teste para produção, URL a cadastrar como webhook (+1 more)

### Community 134 - "usuario_bp.py"
Cohesion: 0.18
Nodes (17): _acesso_permitido_pagamento(), cadastro_obrigado(), _chave_ip_e_identificador(), comprovante_mensalidade(), foto_perfil(), _pagamento_com_acesso_ou_404(), pagina_pagamento(), pagina_termos_responsabilidade() (+9 more)

### Community 135 - "cinema.py"
Cohesion: 0.31
Nodes (8): _entradas(), modulo(), Arquivos do hero cinematográfico da página inicial. A cena 3D é compilada pelo…, {nome da entrada: arquivo}, lido uma vez: o build não muda com o servidor no ar., URL da entrada `nome` ('cena' ou 'video') do build, ou None se não foi…, URL do vídeo do hero, só se ele existir e a entrada que o toca estiver…, _tem_video(), video()

### Community 136 - "Skills Disponíveis"
Cohesion: 0.22
Nodes (8): Assistente e Automação (Antigravity), Ciências e Bioinformática (Plugins de Ciência), Dados e Google Cloud Platform (GCP), Desenvolvimento Mobile e Flutter/Dart, Desenvolvimento Web e Frontend, Firebase e Backend, GenAI e Machine Learning, Skills Disponíveis

### Community 137 - "criar_aluno"
Cohesion: 0.09
Nodes (27): criar_aluno(), test_aluno_existente_continua_entrando_normalmente(), test_area_do_aluno_renderiza_telas_independentes_do_menu(), test_plano_atual_continua_disponivel_para_gerar_cobranca(), test_busca_financeira_trata_curingas_como_texto(), test_painel_financeiro_busca_por_nome_do_aluno(), test_painel_financeiro_exige_admin(), test_painel_financeiro_filtra_por_status() (+19 more)

### Community 138 - "cinema.js"
Cohesion: 0.39
Nodes (7): anotar(), ativar(), carregarCena(), ehAppleMovel(), medir(), pedirMedida(), podeTer3D()

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

### Community 146 - "pagina_cadastro"
Cohesion: 0.16
Nodes (20): _cadastro_recebido(), _em_segundo_plano(), _enviar_em_segundo_plano(), pagina_cadastro(), Roda `tarefa` fora da requisição, para o tempo de resposta não revelar nada. Em…, E-mail COM token (recuperação, confirmação): não pode ir para a `fila_email`. A…, Post/Redirect/Get para a página de obrigado. Cadastro novo, CPF já cadastrado e…, recuperar_senha() (+12 more)

### Community 147 - "Etapa 3 — home com os planos + termos"
Cohesion: 0.40
Nodes (4): Agente A — `templates/index.html` e `static/css/index.css`, Antigravity — `termos_de_servico.html`, `politica_privacidade.html`, `termos_responsabilidade.html` + `static/css/termos.css` (novo), Dados da home (Claude entrega em servidor.py — não edite), Etapa 3 — home com os planos + termos

### Community 148 - "test_fontes_locais.py"
Cohesion: 0.25
Nodes (3): parametrize, Fontes servidas pelo próprio site (SEC-18). Com o Google Fonts, o navegador de…, test_csp_nao_libera_o_google_fonts()

### Community 149 - "Biblioteca no Figma"
Cohesion: 0.50
Nodes (3): Biblioteca no Figma, Falta (ordem de retomada), Limites do plano Starter que moldaram o arquivo

### Community 151 - "keep_alive.py"
Cohesion: 0.29
Nodes (9): iniciar(), _intervalo(), _laco(), _ligado(), parar(), _pingar(), Mantém a aplicação acordada em hospedagens que hibernam por inatividade. Uma…, Encerra o laço. Usado pelos testes; em produção a thread é daemon. (+1 more)

### Community 152 - "Configuração de segurança"
Cohesion: 0.40
Nodes (5): Configuração de segurança, Credencial do administrador, Publicar com um domínio próprio, Segundo fator do administrador (opcional, recomendado), Turnstile no cadastro público (obrigatório em produção)

### Community 155 - "ler_arquivo"
Cohesion: 0.28
Nodes (8): ler_arquivo(), Conteúdo de um arquivo já salvo, ou None se não existir, for inválido ou o…, parametrize, _Resposta, test_arquivo_que_o_bucket_nao_entrega_vira_none(), test_le_o_arquivo_do_bucket(), test_nome_invalido_nem_chega_no_bucket(), test_storage_fora_do_ar_na_leitura_vira_none()

### Community 157 - "auth.test.cjs"
Cohesion: 0.25
Nodes (6): assert, CODIGO, fs, path, test, vm

### Community 158 - "credenciais.py"
Cohesion: 0.09
Nodes (28): _primeiro_uso_do_codigo(), Cada código vale uma vez: quem o viu na tela de outra pessoa não entra com ele.…, verificar_codigo_admin(), admin_configurado(), codigo_totp(), comparar_em_tempo_constante(), credencial_admin_confere(), gerar_hash_admin() (+20 more)

### Community 159 - ".buscar_por_id"
Cohesion: 0.16
Nodes (39): _agora_mercado_pago(), _assinar(), _paga_pelo_mercado_pago(), _pagamento_mp(), _preparar_retorno(), Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala…, Pix aberto e checkout concluído ao mesmo tempo: a consulta pelo…, _ref_checkout() (+31 more)

### Community 160 - "pagina_login"
Cohesion: 0.32
Nodes (6): _abrir_sessao_admin(), pagina_login(), iniciar_sessao(), Grava na sessão atual a credencial em vigor (login ou troca de senha bem-…, Dá um identificador à sessão recém-aberta, para o logout poder revogá-la.…, registrar_credencial()

### Community 161 - "ci-security-scanning-with-strix/SKILL.md"
Cohesion: 0.29
Nodes (6): GitHub Actions, Option A — Self-hosted OSS CLI in the runner, Option B — Managed platform (no runner infra), Optional: upload findings to GitHub code scanning, Other CI systems, Set up Strix in CI/CD

### Community 162 - ".totais_periodo"
Cohesion: 0.29
Nodes (5): Status como o painel deve LER, com o vencimento aplicado na própria consulta. A…, Totais do painel financeiro - sempre calculados no backend a partir do banco,…, test_indicadores_e_tabela_concordam_na_primeira_abertura(), test_indicadores_saem_de_uma_consulta_de_agregacao(), test_totais_periodo_preserva_o_escopo_dos_filtros_de_data()

### Community 164 - "Find security vulnerabilities in code"
Cohesion: 0.29
Nodes (6): Complementary tooling, Find security vulnerabilities in code, Fix and verify, Read the results, Reviewing a pull request instead of the whole repo, Run it

### Community 165 - "test_mercado_pago_oauth.py"
Cohesion: 0.07
Nodes (53): MercadoPagoIndisponivel, Falha de transporte (timeout/DNS/conexao) ao falar com a API do Mercado Pago., _sdk(), _agora(), _ajustar(), api_mp(), _conectar(), _dados_conexao() (+45 more)

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

### Community 174 - "gmail_oauth_bp.py"
Cohesion: 0.62
Nodes (6): callback(), conectar(), desconectar(), limit, route, _voltar()

### Community 175 - "test_email_gmail.py"
Cohesion: 0.33
Nodes (3): aplicativo_google(), fixture, test_refresh_token_fica_cifrado_no_banco()

### Community 176 - "_convidar_cadastro_existente"
Cohesion: 0.50
Nodes (4): _convidar_cadastro_existente(), _convidar_cadastro_existente_por_id(), Cadastro administrativo que alguém tentou recriar pelo formulário público. Em…, Versão para thread de fundo: a sessão da requisição não vale fora dela.

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
- **Why does `PagamentoDAO` connect `PagamentoDAO` to `Aluno`, `Professor`, `adm_bp.py`, `usuario_bp.py`, `AlunoDAO`, `route`, `test_admin_mercado_pago.py`, `criar_aluno`, `test_financeiro_dao.py`, `test_regressao_auditoria.py`, `test_auditoria_seguranca.py`, `pix_bp.py`, `test_seguranca.py`, `test_pix_rotas.py`, `.buscar_por_id`, `checkout_bp.py`, `test_mudanca_plano.py`, `.totais_periodo`, `PlanoDAO`, `test_pagamento_recusado.py`, `criar_pagamento`, `config.py`, `MatriculaDAO`, `test_comprovante_sem_metadados.py`, `conftest.py`?**
  _High betweenness centrality (0.112) - this node is a cross-community bridge._
- **Why does `Vitrine de componentes (/_vitrine)` connect `ui.html` to `config.py`, `componentes.js`, `csrf_field.html`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Why does `criar_aluno()` connect `criar_aluno` to `Aluno`, `test_paginas_erro.py`, `Professor`, `test_seo.py`, `AlunoDAO`, `test_financeiro_dao.py`, `test_regressao_auditoria.py`, `test_auditoria_seguranca.py`, `test_google_login.py`, `PagamentoDAO`, `test_seguranca.py`, `test_pix_rotas.py`, `test_mudanca_plano.py`, `.totais_periodo`, `test_limites_requisicao.py`, `PlanoDAO`, `.listar_paginado`, `test_analytics.py`, `criar_pagamento`, `test_planilha_economica.py`, `test_home_planos.py`, `ProfessorDAO`, `_parece_busca_por_cpf`, `test_layouts.py`, `test_publicas_redesign.py`, `MatriculaDAO`, `logar_como_admin`, `conftest.py`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Are the 170 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 170 INFERRED edges - model-reasoned connections that need verification._
- **Are the 170 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 170 INFERRED edges - model-reasoned connections that need verification._
- **Are the 170 inferred relationships involving `criar_pagamento()` (e.g. with `PagamentoDAO` and `Pagamento`) actually correct?**
  _`criar_pagamento()` has 170 INFERRED edges - model-reasoned connections that need verification._