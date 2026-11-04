# Graph Report - SistemaEXTREMETEAM  (2026-10-24)

## Corpus Check
- 214 files · ~278,831 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3046 nodes · 7122 edges · 177 communities (161 shown, 16 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 1289 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c0d88043`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Aluno
- Componentes
- test_admin_segundo_fator.py
- logar_como_admin
- test_seo.py
- adm_bp.py
- test_mercado_pago_oauth_postgres.py
- AlunoDAO
- planos.py
- usuario_bp.py
- SituacaoPlano
- turma_bp.py
- index.html (home pública)
- PagamentoDAO
- test_regressao_auditoria.py
- fase3b.js
- test_auditoria_seguranca.py
- armazenamento.py
- fila_email.py
- csrf_field.html
- salvar_foto_perfil
- dt_aluno.html — ficha do aluno (admin)
- pix_bp.py
- servidor.py
- criar_aluno
- _tem_limite
- mercado_pago_conta.py
- test_seguranca.py
- test_pix_rotas.py
- financeiroDAO.py
- planilha_excel.py
- checkout_bp.py
- test_mudanca_plano.py
- ui.html
- test_mercado_pago_servico.py
- test_limites_requisicao.py
- Pagina
- google_login.py
- PlanoDAO
- convites.py
- varredura.mjs
- test_pagamento_recusado.py
- config.py
- avatar
- autorizacao.py
- test_observabilidade.py
- test_analytics.py
- requirements.txt (dependências de produção)
- .buscar_por_id
- criar_pagamento
- test_home_planos.py
- analytics.js
- package.json
- seo.py
- Strix Cloud (managed, no local infra)
- MercadoPagoIndisponivel
- deslize.html
- Serviço app (Flask com Gunicorn na porta 5000)
- test_prontidao.py
- pix.js
- test_arranque_seguranca.py
- exempt
- test_keep_alive.py
- Professor
- test_sessao_revogada.py
- Relatório de segurança — Sistema Extreme Team
- academia_bp.py
- componentes.js
- prontidao.py
- botao_ocupado.test.cjs
- test_backup_scripts.py
- gunicorn.conf.py
- Plano
- analytics.test.cjs
- pagamento.js
- test_perfil_e_foto.py
- test_email_componentes.py
- test_layouts.py
- test_migracao_checkout.py
- test_limites_pagamento.py
- checkout_abertura.test.cjs
- pagamento_polling.test.cjs
- test_publicas_redesign.py
- env.py
- test_formatos_de_imagem.py
- gmail_conta.py
- impressao_credencial
- shot.mjs
- c7a4e1b93d20_vigencia_do_plano_e_mudanca_agendada.py
- cena.tsx
- test_comprovante_sem_metadados.py
- 896e70afc9c5_adiciona_foto_e_graduacao_do_aluno_.py
- test_migracao_cadastro_administrativo.py
- ConfiguracaoInvalida
- a1f0c3e75b92_schema_inicial.py
- d9e2f6a14c80_contatos_academia_perfis_professores.py
- e4b7c2a91d35_cadastro_administrativo_e_convite_de_acesso.py
- vercel.json
- mercado_pago.py
- backup.sh
- parametrize
- gerar_imagem_og.py
- test_financeiro_admin_painel.py
- _png_bomba
- agendar.sh
- restaurar.sh
- Contrato do redesign — SistemaEXTREMETEAM
- test_planilha_economica.py
- cinema.test.cjs
- compilerOptions
- pgUsuario.html (área do aluno)
- penetration-testing-with-strix/SKILL.md
- test_cinema.py
- SistemaEXTREMETEAM
- test_paginas_erro.py
- MatriculaDAO
- financeiro.html — painel financeiro
- Pagamento de mensalidade via Pix (Mercado Pago)
- test_google_login.py
- cinema.py
- Skills Disponíveis
- cartao_do_plano
- cinema.js
- Etapa 1 — migrar páginas para os layouts (SEM mudar o visual)
- Etapas 4 a 6 — aluno, admin, professor (aplicar os componentes nas páginas)
- emblema.py
- Banco de dados e migrations
- Etapa 2 — biblioteca de componentes
- Cadastro de aluno pela administração e ativação de acesso
- Outras formas de pagamento (Checkout Pro)
- formatacao.py
- Etapa 3 — home com os planos + termos
- test_fontes_locais.py
- Biblioteca no Figma
- CLAUDE.md
- gmail_oauth_bp.py
- Configuração de segurança
- test_email_gmail.py
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
- .listar_paginado
- Security-test an API
- Application security testing
- imagens.d.ts
- Fix Strix findings and verify
- Test against the OWASP Top 10
- Pentest a web application
- .contar_cadastrados
- limit
- route
- parametrize

## God Nodes (most connected - your core abstractions)
1. `PagamentoDAO` - 230 edges
2. `criar_aluno()` - 172 edges
3. `logar_como_admin()` - 171 edges
4. `criar_pagamento()` - 164 edges
5. `logar_como_aluno()` - 137 edges
6. `AlunoDAO` - 93 edges
7. `Aluno` - 67 edges
8. `PlanoDAO` - 67 edges
9. `MercadoPagoIndisponivel` - 45 edges
10. `Pagamento` - 40 edges

## Surprising Connections (you probably didn't know these)
- `Vitrine de planos da home (secao_planos com vitrine_planos)` --references--> `cartao_do_plano()`  [INFERRED]
  templates/index.html → servicos/planos.py
- `test_cadastro_publico_recusa_confirmacao_diferente()` --uses--> `Aluno`  [INFERRED]
  tests/test_cadastro_administrativo.py → modelos/usuario.py
- `test_cadastro_publico_recusa_confirmacao_vazia()` --uses--> `Aluno`  [INFERRED]
  tests/test_cadastro_administrativo.py → modelos/usuario.py
- `test_refresh_token_fica_cifrado_no_banco()` --uses--> `GmailConexao`  [INFERRED]
  tests/test_email_gmail.py → modelos/gmail_conexao.py
- `test_limite_de_login_por_ip_e_identificador()` --uses--> `AlunoDAO`  [INFERRED]
  tests/test_seguranca.py → dao/usuarioDAO.py

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

## Communities (177 total, 16 thin omitted)

### Community 0 - "Aluno"
Cohesion: 0.09
Nodes (17): Matrícula feita no balcão: sem login, sem senha e sem convite de acesso. Nasce…, Aluno, Se existe uma conta de acesso, e não se o aluno está em dia ou matriculado.…, Convite de acesso já enviado e ainda não usado (a validade é checada na rota)., Chave do estado da CONTA - nunca da situação financeira nem da matrícula., parametrize, Data de nascimento: o mesmo seletor de data e a mesma regra no cadastro, na…, _salvar_ficha() (+9 more)

### Community 1 - "Componentes"
Cohesion: 0.05
Nodes (36): Altura de controle, Avisos flutuantes, Botões — `.et-botao` + variante (+ tamanho), Cartões e contêineres, Componentes, Contêiner e estrutura, Cores, Dados (+28 more)

### Community 2 - "test_admin_segundo_fator.py"
Cohesion: 0.20
Nodes (20): _codigo_agora(), _codigo_errado(), _destino(), _entrar_com_senha(), fixture, parametrize, Segundo fator do administrador (SEC-30). Com ADMIN_TOTP_SECRET definida, a…, segundo_fator() (+12 more)

### Community 3 - "logar_como_admin"
Cohesion: 0.07
Nodes (69): MercadoPagoConexao, Conta do Mercado Pago que a academia autorizou por OAuth. Uma linha só (a…, logar_como_admin(), _agora(), _ajustar(), api_mp(), _conectar(), _dados_conexao() (+61 more)

### Community 4 - "test_seo.py"
Cohesion: 0.10
Nodes (25): _head(), _json_ld(), parametrize, SEO técnico: robots.txt, sitemap, títulos, meta tags, noindex e JSON-LD da home., Nenhum campo do JSON-LD pode sair nulo, vazio ou só com espaços., _robots(), _sem_vazios(), test_area_do_admin_sai_do_indice() (+17 more)

### Community 5 - "adm_bp.py"
Cohesion: 0.09
Nodes (48): _aluno_do_cpf_ou_painel(), aprovar_aluno(), aprovar_comprovante_manual(), arquivar_plano(), ativar_aluno(), atualizar_status_pagamento(), cadastrar_pagamento(), _chave_lote() (+40 more)

### Community 6 - "test_mercado_pago_oauth_postgres.py"
Cohesion: 0.18
Nodes (8): postgres_mp(), fixture, Renovação do token OAuth com trava de linha real, opcional na suíte que usa…, _Resposta, test_dois_processos_perto_do_vencimento_gastam_o_refresh_token_uma_vez(), _migracao(), test_migracao_cria_a_tabela_igual_ao_modelo_e_e_reentrante(), test_migracao_encadeia_na_ultima_revisao_existente()

### Community 7 - "AlunoDAO"
Cohesion: 0.10
Nodes (47): remover_foto_aluno(), _convidar_cadastro_existente(), Cadastro administrativo que alguém tentou recriar pelo formulário público. Em…, AlunoDAO, _matricular(), Cadastro de aluno pela administração, ativação de acesso e confirmação de…, test_admin_lanca_e_baixa_mensalidade_de_aluno_sem_acesso(), test_admin_matricula_aluno_sem_email_senha_nem_acesso() (+39 more)

### Community 8 - "planos.py"
Cohesion: 0.14
Nodes (24): cadeia_paga(), cobranca_a_pagar(), cobranca_em_decisao(), cobranca_pendente(), esta_inadimplente(), fim_periodo_comprometido(), inicio_proximo_periodo(), intervalo_vigencia() (+16 more)

### Community 9 - "usuario_bp.py"
Cohesion: 0.11
Nodes (42): _acesso_permitido_pagamento(), alterar_senha_perfil(), _aluno_da_sessao(), _aluno_por_token(), atualizar_dados_perfil(), cadastro_obrigado(), cancelar_mudanca_plano(), _chave_ip_e_identificador() (+34 more)

### Community 10 - "SituacaoPlano"
Cohesion: 0.10
Nodes (8): Retrato completo da situação do plano do aluno em uma data. Objeto de leitura,…, Último dia de acesso já pago, somando as renovações antecipadas., Fim só do período em curso - o que a troca de plano tem de preservar., Renovação já paga que começa depois do período atual, quando existe., Existe uma cobrança que o aluno pode quitar agora., Pode antecipar o próximo período: só quando nada está em aberto nem em decisão…, Só faz sentido agendar a troca quando existe um período pago correndo: sem…, SituacaoPlano

### Community 11 - "turma_bp.py"
Cohesion: 0.17
Nodes (19): _acesso_permitido(), cadastrar_professor(), cadastrar_turma(), desmatricular_aluno(), detalhe_turma(), editar_professor(), gerenciar_turmas(), matricular_aluno() (+11 more)

### Community 12 - "index.html (home pública)"
Cohesion: 0.13
Nodes (12): faq_estruturado(), Textos editáveis da página inicial: perguntas frequentes e prazos de…, JSON-LD FAQPage com exatamente as perguntas mostradas na página., cabecalho, entrarFixo, icone_senha, input_senha, modal (+4 more)

### Community 13 - "PagamentoDAO"
Cohesion: 0.05
Nodes (44): mensalidade_destaque(), PagamentoDAO, Lançamento manual de recebimento (dinheiro/transferência) feito pelo admin.…, Status como o painel deve LER, com o vencimento aplicado na própria consulta. A…, Carrega aluno e plano junto das mensalidades. O template do painel lê…, Lista completa (sem paginar). Mantida para relatórios e testes., Uma página de mensalidades, recortada pelo banco (LIMIT/OFFSET). O painel…, Totais do painel financeiro - sempre calculados no backend a partir do banco,… (+36 more)

### Community 14 - "test_regressao_auditoria.py"
Cohesion: 0.04
Nodes (47): _contar_selects_em_alunos(), _credencial(), Regressões da auditoria de segurança, desempenho e confiabilidade. Cada caso…, Head-of-line blocking: a primeira linha falhando não pode impedir as seguintes.…, Uma linha `desistiu` nunca foi entregue: recusar o reenvio fazia a tela dizer…, A revivência vale só para o abandonado: clique duplo continua virando um envio., Trocar senha, e-mail ou foto são ações de quem JÁ está autenticado. Devolver o…, Persistência não é retomada: alguém precisa acordar a fila quando o adiamento… (+39 more)

### Community 15 - "fase3b.js"
Cohesion: 0.06
Nodes (47): avisos, bind(), caixas, campos, col(), D(), estados, faixa (+39 more)

### Community 16 - "test_auditoria_seguranca.py"
Cohesion: 0.06
Nodes (47): _agora_mercado_pago(), _assinar(), _pagamento_mp(), _preparar_para_conciliacao(), parametrize, Auditoria de segurança: sondas escritas para TENTAR quebrar as regras. Nenhum…, Hipótese: as rotas de cobrança respondem sem sessão nenhuma., Hipótese: a sessão de professor é aceita nas rotas financeiras do aluno. (+39 more)

### Community 17 - "armazenamento.py"
Cohesion: 0.12
Nodes (26): ArquivoInvalido, _conferir_dimensoes(), _detectar_tipo_imagem_real(), _exif_so_com_orientacao(), _gravar(), ImagemGrandeDemais, _jpeg_sem_metadados(), _orientacao() (+18 more)

### Community 18 - "fila_email.py"
Cohesion: 0.06
Nodes (40): EmailPendente, espera_da_proxima_tentativa(), Fila de e-mails no banco. Aviso e cobrança coletivos saíam um a um dentro da…, contar_falhados(), contar_pendentes(), disparar(), enfileirar(), enfileirar_transacional() (+32 more)

### Community 19 - "csrf_field.html"
Cohesion: 0.13
Nodes (20): Contato e localização da academia, ativar_acesso.html — ativar acesso pelo convite, cadastro.html — criar conta, cadastro_obrigado.html — cadastro recebido, Cadastro com PRG e resposta única, Aceite do Termo de Responsabilidade, Modal de login da home (#meuModal, POST /login), layouts/publico.html — layout das telas públicas (+12 more)

### Community 20 - "salvar_foto_perfil"
Cohesion: 0.14
Nodes (26): ArmazenamentoIndisponivel, ler_arquivo(), _nome_valido(), O nome sempre é o UUID gerado por esta camada, nunca um valor vindo da…, Valida, reprocessa e salva uma foto de perfil. Retorna o nome do arquivo…, Conteúdo de um arquivo já salvo, ou None se não existir, for inválido ou o…, Melhor esforço: um arquivo que sobra não quebra nada, então falha só vai para o…, O arquivo era válido, mas o Storage não aceitou guardá-lo agora. Herda de… (+18 more)

### Community 21 - "dt_aluno.html — ficha do aluno (admin)"
Cohesion: 0.11
Nodes (25): admin_academia.html — configurações da academia, Abas com memória (data-tabs-lembrar), Conexão OAuth do Gmail para envio de avisos, Conexão OAuth do Mercado Pago (PKCE), Webhook de pagamentos do Mercado Pago (MERCADO_PAGO_WEBHOOK_SECRET), admin_aluno_novo.html — matricular aluno, Matrícula sem acesso ao sistema, admin_avisos.html — avisos e cobranças por e-mail (+17 more)

### Community 22 - "pix_bp.py"
Cohesion: 0.07
Nodes (46): _acesso_permitido(), _chave_entrega_webhook(), criar_pix_mensalidade(), _data_da_aprovacao(), _forma_pagamento_confirmada(), _instante_utc(), _iso_utc(), _liberar_entrega_webhook() (+38 more)

### Community 23 - "servidor.py"
Cohesion: 0.08
Nodes (35): after_request, Ponto de entrada WSGI usado pelo Gunicorn em producao., before_request, route, robots(), sitemap(), context_processor, errorhandler (+27 more)

### Community 24 - "criar_aluno"
Cohesion: 0.13
Nodes (36): Único caminho pelo qual o aluno contrata, renova ou agenda a troca de plano.…, `pendente` vira `atrasado` depois do vencimento. Não altera nada além disso -…, criar_aluno(), parametrize, test_admin_lanca_mensalidade_paga_no_cartao(), test_escolher_plano_cria_mensalidade_e_redireciona_para_pix(), test_plano_invalido_nao_cria_mensalidade(), test_reenvio_da_contratacao_reutiliza_mensalidade() (+28 more)

### Community 25 - "_tem_limite"
Cohesion: 0.20
Nodes (10): parametrize, Qualquer dígito no termo virava `CPF LIKE '%3%'` e devolvia a academia inteira., Rotas que custam hash de senha, processamento de imagem ou sondagem de token., Limites declarados por decorador NAQUELA rota. `resolve_limits` não serve aqui:…, Guarda do teste acima: uma rota sem limite precisa ser reprovada por ele., _tem_limite(), test_busca_so_trata_como_cpf_o_que_parece_cpf(), test_o_detector_de_limite_realmente_discrimina() (+2 more)

### Community 26 - "mercado_pago_conta.py"
Cohesion: 0.10
Nodes (37): access_token_vigente(), _agora(), ambiente_da_conexao(), _cifrar(), _client_id(), _client_secret(), ConexaoIlegivel, _configuracao_do_aplicativo() (+29 more)

### Community 27 - "test_seguranca.py"
Cohesion: 0.07
Nodes (27): _carregar_senhas_comuns(), Lista de senhas comuns recusadas (cerca de 3000; ASVS 5.0 6.2.4 e NIST 800-63B), erro_validacao_senha(), Retorna uma mensagem quando a senha é curta, comum ou igual ao identificador., Lê a lista de senhas comuns (uma por linha; `#` abre comentário) para um…, _cadastro_publico(), _imagem_jpeg(), _mensagem_da_resposta() (+19 more)

### Community 28 - "test_pix_rotas.py"
Cohesion: 0.22
Nodes (19): _agora_mercado_pago(), _assinar(), _resposta_consulta(), _resposta_criacao(), test_admin_tambem_pode_gerar_pix(), test_aluno_gera_pix_da_propria_mensalidade(), test_aluno_nao_acessa_mensalidade_de_outro_aluno(), test_impede_cobranca_duplicada_em_chamadas_consecutivas() (+11 more)

### Community 29 - "financeiroDAO.py"
Cohesion: 0.14
Nodes (8): _paginar(), O que aconteceu numa tentativa de contratar/renovar/trocar de plano., Aplica LIMIT/OFFSET e conta o total numa consulta separada e barata. A contagem…, ResultadoContratacao, Decimal, _para_decimal(), Pedido de troca de plano agendado para a próxima renovação. Nunca altera o…, SolicitacaoMudancaPlano

### Community 30 - "planilha_excel.py"
Cohesion: 0.30
Nodes (13): Nome legível da forma de pagamento. Antes as telas usavam `|replace('_','…, rotulo_forma_pagamento(), _aba_categorias(), _aba_entradas(), _aba_resumo(), _aba_saidas(), _cabecalho(), _escrever() (+5 more)

### Community 31 - "checkout_bp.py"
Cohesion: 0.09
Nodes (28): abrir_checkout(), _acesso_permitido(), _checkout_pronto(), continuar_checkout(), _erro_abertura(), limitar_consulta_pagamento, limitar_criacao_pagamento, route (+20 more)

### Community 32 - "test_mudanca_plano.py"
Cohesion: 0.15
Nodes (27): cancelar_mudanca_plano_admin(), A administração pode cancelar um pedido de troca ainda não aplicado. Não existe…, Persistência dos pedidos de troca de plano agendados para a próxima renovação., Mesma trava de linha usada nas mensalidades: dois cliques simultâneos em…, SolicitacaoPlanoDAO, _agendar(), _pagar(), Mudança para um plano mais barato agendada para a próxima renovação. Regra… (+19 more)

### Community 33 - "ui.html"
Cohesion: 0.10
Nodes (28): campoDuracao, campoPreco, formularioPlano, cartao_plano(), secao_planos(), estado_vazio(), interruptor(), metrica() (+20 more)

### Community 34 - "test_mercado_pago_servico.py"
Cohesion: 0.08
Nodes (37): ambiente_mercado_pago(), Valida a assinatura HMAC-SHA256 do webhook do Mercado Pago. Nunca lanca -…, Diz se a integracao esta apontando para producao ou para o sandbox. Prioriza a…, validar_assinatura_webhook(), Hipótese: uma notificação capturada ontem pode ser reenviada hoje., `ts=nan` fazia a comparação da janela dar False e passava pela checagem de…, test_webhook_recusa_assinatura_antiga(), test_webhook_recusa_ts_nao_numerico_finito() (+29 more)

### Community 35 - "test_limites_requisicao.py"
Cohesion: 0.12
Nodes (28): consultar_mp(), _estourar(), fixture, parametrize, Limites de requisição da rodada de 04/10/2026 (SEC-10 a SEC-17 e SEC-19). Cada…, Trocar de rede ou abrir outra sessão não devolve a cota de e-mails em massa., Faz `limite` requisições sem nenhum 429 e devolve a seguinte., Alunos no mesmo Wi-Fi não dividem o teto padrão, nem com o visitante anônimo. (+20 more)

### Community 36 - "Pagina"
Cohesion: 0.14
Nodes (5): Pagina, Uma fatia de resultados já recortada pelo banco, com o que a navegação precisa., Uma página existe mesmo quando está vazia. Sem isto, `__len__` fazia `{% if…, `__len__` fazia `{% if pagina %}` ser falso numa página sem itens, escondendo…, test_pagina_vazia_ainda_mostra_a_navegacao()

### Community 37 - "google_login.py"
Cohesion: 0.22
Nodes (15): _autorizacao_valida(), callback(), login_google(), _novo_pkce(), limit, route, (code_verifier, code_challenge S256), como na conexão do Mercado Pago. O state…, O state devolvido é o que ESTA sessão emitiu, há pouco tempo? (+7 more)

### Community 38 - "PlanoDAO"
Cohesion: 0.07
Nodes (54): cadastrar_aluno(), cadastrar_plano(), editar_plano(), _ler_plano(), painel_adm(), Nome, preço e duração do formulário de plano: `(campos, None)` ou `(None,…, Nome, preço, duração e promoção. Vale para as cobranças criadas daqui em…, Matrícula feita pela administração, sem conta de acesso. Pede só o que… (+46 more)

### Community 39 - "convites.py"
Cohesion: 0.11
Nodes (24): route, verificar_email_cadastro(), aluno_do_token(), ConviteIndisponivel, descartar(), enviar(), gerar_token(), _hash() (+16 more)

### Community 40 - "varredura.mjs"
Cohesion: 0.11
Nodes (23): aberto(), ACESSO, auditar(), { chromium }, CONF, confirmacoes(), crc, CREDS (+15 more)

### Community 41 - "test_pagamento_recusado.py"
Cohesion: 0.28
Nodes (20): _assinar(), _data_mp(), _eventos(), _mockar_mp(), _pagamento_mp(), _pix_criado(), Mensalidade recusada: a próxima tentativa do aluno a reabre, e a recusa antiga…, Mensalidade cujo cartão acabou de ser recusado no Checkout Pro. (+12 more)

### Community 42 - "config.py"
Cohesion: 0.17
Nodes (10): chave_da_conta(), Chave de limite por CONTA, caindo no IP só para quem não está autenticado. A…, Matricula, postgres_pix(), fixture, Regressão com trava de linha real, opcional na suíte que usa SQLite. Execute…, route, Instância descartável para conferir o redesign no navegador (porta 4002).… (+2 more)

### Community 43 - "avatar"
Cohesion: 0.12
Nodes (16): avatar(), breadcrumb(), Biblioteca de componentes .et-* (componentes.css), Seção Nossa equipe (professores_publicos), Nosso método: criar conta, aguardar aprovação, contratar plano e treinar, Cadastros pendentes (aprovar ou recusar aluno), Tabela de alunos paginada com busca no servidor, pgProfessor.html (minhas turmas do professor) (+8 more)

### Community 44 - "autorizacao.py"
Cohesion: 0.21
Nodes (15): foto_professor(), aluno_autorizado(), aluno_requerido(), _credencial_confere(), encerrar_sessao(), professor_autorizado(), Autorização das rotas protegidas. A sessão diz quem *afirmou* ser quem; quem…, A sessão foi emitida para a credencial que vale AGORA? Uma sessão sem carimbo é… (+7 more)

### Community 45 - "test_observabilidade.py"
Cohesion: 0.14
Nodes (20): before_breadcrumb(), before_send(), iniciar_sentry(), _limpar(), mascarar(), Rastreamento de erros opcional com Sentry. Sem `SENTRY_DSN`, nada é importado…, _evento(), fixture (+12 more)

### Community 46 - "test_analytics.py"
Cohesion: 0.14
Nodes (20): _carrega_analytics(), com_analytics(), _csp_com_google(), _evento(), fixture, parametrize, GA4 opcional (servicos/analytics.py): nada sem ANALYTICS_ID, nunca em área…, sem_analytics_por_padrao() (+12 more)

### Community 47 - "requirements.txt (dependências de produção)"
Cohesion: 0.14
Nodes (16): requirements.txt (dependências de produção), cryptography 50.0.1, Flask 3.1.3, Flask-Limiter[redis] 4.1.1, Flask-Migrate 4.1.0, Flask-SQLAlchemy 3.1.1, Flask-WTF 1.2.2, gunicorn 23.0.0 (+8 more)

### Community 48 - ".buscar_por_id"
Cohesion: 0.15
Nodes (26): _agora_mercado_pago(), _assinar(), _pagamento_mp(), _preparar_retorno(), Pix aberto e checkout concluído ao mesmo tempo: a consulta pelo…, test_retorno_com_aprovacao_confirmada_marca_pago(), test_retorno_com_mp_indisponivel_avisa_sem_mudar_status(), test_retorno_de_boleto_avisa_sobre_o_prazo() (+18 more)

### Community 49 - "criar_pagamento"
Cohesion: 0.10
Nodes (53): criar_pagamento(), logar_como_aluno(), Hipótese: forjar ?status=approved na volta do MP quita a mensalidade., test_retorno_ignora_status_aprovado_da_query_string(), _mockar_preferencia(), parametrize, Rotas do Checkout Pro ("outras formas de pagamento"). Nenhum teste aqui fala…, Um boleto pendente do Checkout Pro grava provider_payment_id, mas não é Pix:… (+45 more)

### Community 50 - "test_home_planos.py"
Cohesion: 0.20
Nodes (16): Inclusive os arquivados: serve a quem olha o histórico (filtro do financeiro)., Planos da página inicial, prontos para `components/cartao_plano.html`. O preço…, vitrine_planos(), _plano(), _quatro_planos(), Planos na página inicial: cálculo (servicos/planos.vitrine_planos), destaque…, test_admin_destaca_e_tira_o_destaque(), test_admin_pode_criar_plano_ja_em_destaque() (+8 more)

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

### Community 55 - "MercadoPagoIndisponivel"
Cohesion: 0.21
Nodes (13): buscar_pagamentos_por_referencia(), MercadoPagoIndisponivel, Exception, Lista os pagamentos que o Mercado Pago associa a uma external_reference. Usada…, Falha de transporte (timeout/DNS/conexao) ao falar com a API do Mercado Pago., _sdk(), test_conexao_ilegivel_e_tratada_como_mercado_pago_indisponivel(), test_sdk_do_servico_usa_o_token_da_conexao() (+5 more)

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
Cohesion: 0.16
Nodes (21): parametrize, _env_arranque(), _hosts_e_proxy(), Validações feitas por servidor.py no arranque (COOKIE_SECURE, TRUSTED_HOSTS,…, Desenvolvimento local sem HTTPS (sem Caddy) não pode ficar travado., `python -m servicos.credenciais`: o hash sai entre aspas simples. O hash do…, _rodar(), test_arranque_aceita_redis_do_upstash_com_espaco_em_volta() (+13 more)

### Community 62 - "test_keep_alive.py"
Cohesion: 0.16
Nodes (7): ambiente_limpo(), fixture, parametrize, Garante que o keep-alive fica desligado por padrão e só pinga a própria origem., test_intervalo_fica_dentro_da_faixa(), test_nao_liga_com_valor_negativo(), test_ping_so_considera_200_como_sucesso()

### Community 63 - "Professor"
Cohesion: 0.09
Nodes (27): ProfessorDAO, Professor, logar_como_professor(), fixture, Hipótese: a foto continua acessível por URL depois de tirar a publicação., Hipótese: os contatos vazam na home antes de a publicação ser marcada., Sonda: a data vem da query string e é convertida sem tratamento., test_contatos_do_professor_so_aparecem_quando_publicados() (+19 more)

### Community 64 - "test_sessao_revogada.py"
Cohesion: 0.24
Nodes (11): Sessões encerradas pelo logout. A sessão do Flask é um cookie assinado, sem…, SessaoRevogada, _cliente_com_cookie(), _entrar_como_admin(), `session.clear()` só limpava o navegador de quem saiu; a cópia do cookie seguia…, test_logout_apaga_revogacoes_vencidas(), test_logout_de_uma_sessao_nao_derruba_as_outras(), test_logout_revoga_a_copia_do_cookie_feita_antes() (+3 more)

### Community 65 - "Relatório de segurança — Sistema Extreme Team"
Cohesion: 0.15
Nodes (12): Controles verificados, Histórico de auditorias, O que foi feito nesta rodada, Pendências não relacionadas a segurança, Relatório de segurança — Sistema Extreme Team, Rodada anterior (22/09/2026 — 2ª rodada), Rodada de 04/10/2026 — limites de requisição, Situação atual (20/10/2026 — hero 3D, OWASP/DevSecOps e dependências) (+4 more)

### Community 66 - "academia_bp.py"
Cohesion: 0.12
Nodes (20): configuracoes(), _pagina(), route, O administrador foi ao Mercado Pago e a autorização não voltou para cá? O state…, tentativa_sem_retorno(), Academia, link_email(), Normalização de contatos profissionais antes de montar links públicos. (+12 more)

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

### Community 72 - "Plano"
Cohesion: 0.12
Nodes (17): Plano, Preço de uma cobrança criada em `hoje`., app(), client(), contexto_app(), limpar_banco(), logar_como_professor(), plano() (+9 more)

### Community 73 - "analytics.test.cjs"
Cohesion: 0.18
Nodes (7): assert, CODIGO, Element, fs, path, test, vm

### Community 74 - "pagamento.js"
Cohesion: 0.47
Nodes (9): alvoDoRotulo(), consultarStatus(), gerarOuAtualizarPix(), iniciarPolling(), liberarBotao(), marcarOcupado(), mostrarEstado(), pararPolling() (+1 more)

### Community 75 - "test_perfil_e_foto.py"
Cohesion: 0.18
Nodes (11): Turma, _imagem_jpeg_valida(), test_admin_acessa_foto_de_qualquer_aluno(), test_aluno_nao_acessa_foto_de_outro_aluno(), test_aluno_ve_o_proprio_perfil(), test_professor_ve_foto_de_aluno_da_propria_turma(), test_substituir_e_remover_foto(), test_upload_de_arquivo_disfarcado_e_recusado() (+3 more)

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
Nodes (5): _cabecalho(), _entrar_fixo(), test_admin_logado_vai_da_home_para_o_painel(), test_aluno_logado_vai_da_home_direto_para_a_area_do_aluno(), test_visitante_tem_entrar_fixo_que_abre_o_mesmo_modal()

### Community 83 - "env.py"
Cohesion: 0.39
Nodes (7): get_engine(), get_engine_url(), get_metadata(), Run migrations in 'offline' mode. This configures the context with just a URL…, Run migrations in 'online' mode. In this scenario we need to create an Engine…, run_migrations_offline(), run_migrations_online()

### Community 84 - "test_formatos_de_imagem.py"
Cohesion: 0.26
Nodes (10): disco_temporario(), _imagem(), parsers_proibidos(), fixture, parametrize, Upload de foto e comprovante: o Pillow só interpreta JPEG, PNG e WebP. As…, Falha o teste se o parser de GIF ou TIFF for chamado., test_comprovante_em_outro_formato_e_recusado_sem_passar_pelo_parser() (+2 more)

### Community 85 - "gmail_conta.py"
Cohesion: 0.27
Nodes (15): GmailConexao, _access_token(), _cifrar(), _client_id(), _client_secret(), _decifrar(), enviar(), estado() (+7 more)

### Community 86 - "impressao_credencial"
Cohesion: 0.22
Nodes (15): Presenca, impressao_credencial(), Resumo curto e não reversível do hash da senha, guardado na sessão. Nunca é a…, Valor que representa a credencial administrativa em vigor, ou None se não há…, referencia_credencial_admin(), parametrize, test_aluno_confirma_sua_frequencia(), test_consulta_com_data_invalida_exibe_hoje_e_aviso() (+7 more)

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

### Community 93 - "ConfiguracaoInvalida"
Cohesion: 0.32
Nodes (11): _autorizacao_valida(), callback(), conectar(), desconectar(), limit, route, O state devolvido é o que ESTA sessão emitiu, há pouco tempo?, Só monta o state/PKCE na sessão e manda o administrador ao Mercado Pago. É um… (+3 more)

### Community 95 - "d9e2f6a14c80_contatos_academia_perfis_professores.py"
Cohesion: 0.83
Nodes (3): _campos_professor(), downgrade(), upgrade()

### Community 97 - "vercel.json"
Cohesion: 0.50
Nodes (3): gru1, regions, $schema

### Community 98 - "mercado_pago.py"
Cohesion: 0.08
Nodes (40): iniciar(), _intervalo(), _laco(), _ligado(), parar(), _pingar(), Mantém a aplicação acordada em hospedagens que hibernam por inatividade. Uma…, Encerra o laço. Usado pelos testes; em produção a thread é daemon. (+32 more)

### Community 99 - "backup.sh"
Cohesion: 1.00
Nodes (3): registrar(), reter(), backup.sh script

### Community 114 - "parametrize"
Cohesion: 0.21
Nodes (8): capturar_emails(), fixture, parametrize, Intercepta o envio e devolve os e-mails que teriam saído, com os links., test_confirmacao_aceita_unicode(), test_matricula_valida_dados_no_servidor(), test_novos_formularios_exigem_csrf(), test_rotas_de_matricula_e_convite_sao_so_do_admin()

### Community 116 - "test_financeiro_admin_painel.py"
Cohesion: 0.33
Nodes (5): test_busca_financeira_trata_curingas_como_texto(), test_painel_financeiro_busca_por_nome_do_aluno(), test_painel_financeiro_exige_admin(), test_painel_financeiro_filtra_por_status(), test_painel_financeiro_mostra_totais_do_backend()

### Community 117 - "_png_bomba"
Cohesion: 0.29
Nodes (7): _png_bomba(), Bomba de descompressão: arquivo minúsculo, imagem gigante. O PNG aqui tem 285…, PNG válido e altamente compressível: linhas zeradas, como uma bomba real., O teto de pixels vale para a FOTO, que é decodificada, não para o comprovante.…, test_comprovante_a4_escaneado_continua_sendo_aceito(), test_foto_de_perfil_mantem_o_teto_de_pixels(), test_png_com_pixels_demais_e_recusado_pelo_cabecalho()

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
Cohesion: 0.18
Nodes (4): csrf_ligado(), fixture, Página de erro (templates/erro.html) e os handlers de 404, 403, 500 e CSRF., test_404_para_quem_esta_logado_leva_a_area_dele()

### Community 131 - "MatriculaDAO"
Cohesion: 0.27
Nodes (5): MatriculaDAO, test_escolher_plano_com_turma_cria_matricula(), test_turma_lotada_nao_vira_matricula_apos_pagamento(), fixture, turma()

### Community 132 - "financeiro.html — painel financeiro"
Cohesion: 0.13
Nodes (14): ajustar(), aplicar(), Tom da mensagem por status do pagamento, badge(), Situações da mensalidade (pendente a reembolsado), email/base.html — layout dos e-mails, email/componentes.html — macros de e-mail, badge() — etiqueta de situação no e-mail (+6 more)

### Community 133 - "Pagamento de mensalidade via Pix (Mercado Pago)"
Cohesion: 0.22
Nodes (9): Como obter credenciais de teste (modo manual, sem OAuth), Como testar localmente, Conectar a conta por OAuth (a academia não cria aplicativo), Instalar dependências, Pagamento de mensalidade via Pix (Mercado Pago), Produção, Trocando de credenciais de teste para produção, URL a cadastrar como webhook (+1 more)

### Community 134 - "test_google_login.py"
Cohesion: 0.08
Nodes (24): Esquece a conta conectada. Devolve True se havia uma., remover_conexao(), fixture, Registra as chamadas e devolve as respostas configuradas por método., storage(), _StorageFalso, test_envia_pelo_gmail_com_o_refresh_token_da_conexao(), cliente_google() (+16 more)

### Community 135 - "cinema.py"
Cohesion: 0.31
Nodes (8): _entradas(), modulo(), Arquivos do hero cinematográfico da página inicial. A cena 3D é compilada pelo…, {nome da entrada: arquivo}, lido uma vez: o build não muda com o servidor no ar., URL da entrada `nome` ('cena' ou 'video') do build, ou None se não foi…, URL do vídeo do hero, só se ele existir e a entrada que o toca estiver…, _tem_video(), video()

### Community 136 - "Skills Disponíveis"
Cohesion: 0.22
Nodes (8): Assistente e Automação (Antigravity), Ciências e Bioinformática (Plugins de Ciência), Dados e Google Cloud Platform (GCP), Desenvolvimento Mobile e Flutter/Dart, Desenvolvimento Web e Frontend, Firebase e Backend, GenAI e Machine Learning, Skills Disponíveis

### Community 137 - "cartao_do_plano"
Cohesion: 0.27
Nodes (10): cartao_do_plano(), duracao_dias(), _duracao_por_extenso(), _meses(), preco(), preco_cheio(), Duração em meses cheios para exibir e dividir o preço: 30→1, 90→3, 365→12., Campos de `components/cartao_plano.html` para um plano: os mesmos na home e na… (+2 more)

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

### Community 146 - "formatacao.py"
Cohesion: 0.12
Nodes (26): ativar_acesso(), _cadastro_recebido(), _convidar_cadastro_existente_por_id(), _em_segundo_plano(), _enviar_em_segundo_plano(), pagina_cadastro(), Roda `tarefa` fora da requisição, para o tempo de resposta não revelar nada. Em…, E-mail COM token (recuperação, confirmação): não pode ir para a `fila_email`. A… (+18 more)

### Community 147 - "Etapa 3 — home com os planos + termos"
Cohesion: 0.40
Nodes (4): Agente A — `templates/index.html` e `static/css/index.css`, Antigravity — `termos_de_servico.html`, `politica_privacidade.html`, `termos_responsabilidade.html` + `static/css/termos.css` (novo), Dados da home (Claude entrega em servidor.py — não edite), Etapa 3 — home com os planos + termos

### Community 148 - "test_fontes_locais.py"
Cohesion: 0.25
Nodes (3): parametrize, Fontes servidas pelo próprio site (SEC-18). Com o Google Fonts, o navegador de…, test_csp_nao_libera_o_google_fonts()

### Community 149 - "Biblioteca no Figma"
Cohesion: 0.50
Nodes (3): Biblioteca no Figma, Falta (ordem de retomada), Limites do plano Starter que moldaram o arquivo

### Community 151 - "gmail_oauth_bp.py"
Cohesion: 0.62
Nodes (6): callback(), conectar(), desconectar(), limit, route, _voltar()

### Community 152 - "Configuração de segurança"
Cohesion: 0.50
Nodes (4): Configuração de segurança, Credencial do administrador, Publicar com um domínio próprio, Segundo fator do administrador (opcional, recomendado)

### Community 155 - "test_email_gmail.py"
Cohesion: 0.33
Nodes (3): aplicativo_google(), fixture, test_refresh_token_fica_cifrado_no_banco()

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
Cohesion: 0.23
Nodes (10): _body_tag(), _html(), Conversão na home: perguntas frequentes, cadastro no hero e página de obrigado., test_cadastro_fica_no_hero(), test_home_mostra_as_perguntas_frequentes_em_details(), test_home_nao_tem_barra_fixa_de_cadastro(), test_json_ld_faq_repete_exatamente_as_perguntas_da_pagina(), test_pagina_de_obrigado_explica_os_proximos_passos_e_sai_do_indice() (+2 more)

### Community 164 - "Find security vulnerabilities in code"
Cohesion: 0.29
Nodes (6): Complementary tooling, Find security vulnerabilities in code, Fix and verify, Read the results, Reviewing a pull request instead of the whole repo, Run it

### Community 165 - "requirements-dev.txt (requirements.txt + pytest + pip-audit)"
Cohesion: 0.67
Nodes (3): requirements-dev.txt (requirements.txt + pytest + pip-audit), pip-audit 2.10.1, pytest

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

## Ambiguous Edges - Review These
- `botao_google.html` → `Integração com o Gmail (conta remetente da academia)`  [AMBIGUOUS]
  templates/politica_privacidade.html · relation: conceptually_related_to

## Knowledge Gaps
- **325 isolated node(s):** `Visão geral`, `Marca`, `Superfícies claras`, `Texto`, `Situações` (+320 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `botao_google.html` and `Integração com o Gmail (conta remetente da academia)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `PagamentoDAO` connect `PagamentoDAO` to `Aluno`, `MatriculaDAO`, `adm_bp.py`, `AlunoDAO`, `usuario_bp.py`, `test_regressao_auditoria.py`, `test_auditoria_seguranca.py`, `pix_bp.py`, `criar_aluno`, `test_seguranca.py`, `test_pix_rotas.py`, `financeiroDAO.py`, `test_admin_mercado_pago.py`, `test_mudanca_plano.py`, `checkout_bp.py`, `PlanoDAO`, `test_pagamento_recusado.py`, `config.py`, `.buscar_por_id`, `criar_pagamento`, `Professor`, `Plano`, `test_comprovante_sem_metadados.py`, `test_financeiro_admin_painel.py`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Why does `logar_como_admin()` connect `logar_como_admin` to `Aluno`, `test_admin_segundo_fator.py`, `test_seo.py`, `test_google_login.py`, `AlunoDAO`, `PagamentoDAO`, `test_regressao_auditoria.py`, `criar_aluno`, `test_seguranca.py`, `test_pix_rotas.py`, `test_admin_mercado_pago.py`, `test_mudanca_plano.py`, `PlanoDAO`, `.listar_paginado`, `test_analytics.py`, `.buscar_por_id`, `criar_pagamento`, `test_home_planos.py`, `Professor`, `test_sessao_revogada.py`, `academia_bp.py`, `Plano`, `test_perfil_e_foto.py`, `test_layouts.py`, `test_limites_pagamento.py`, `test_publicas_redesign.py`, `impressao_credencial`, `parametrize`, `test_financeiro_admin_painel.py`, `test_planilha_economica.py`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Why does `Vitrine de componentes (/_vitrine)` connect `ui.html` to `componentes.js`, `csrf_field.html`, `config.py`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Are the 158 inferred relationships involving `PagamentoDAO` (e.g. with `aprovar_comprovante_manual()` and `atualizar_status_pagamento()`) actually correct?**
  _`PagamentoDAO` has 158 INFERRED edges - model-reasoned connections that need verification._
- **Are the 170 inferred relationships involving `criar_aluno()` (e.g. with `AlunoDAO` and `Aluno`) actually correct?**
  _`criar_aluno()` has 170 INFERRED edges - model-reasoned connections that need verification._
- **Are the 169 inferred relationships involving `logar_como_admin()` (e.g. with `test_admin_salva_atualiza_e_limpa_contatos()` and `test_csrf_configuracoes()`) actually correct?**
  _`logar_como_admin()` has 169 INFERRED edges - model-reasoned connections that need verification._