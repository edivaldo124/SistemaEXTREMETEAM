# Relatório de segurança — Sistema Extreme Team

**Última atualização:** 04/10/2026 (rodada de limites de requisição)
**Escopo da rodada de 04/10/2026:** cobertura de rate limit em todas as rotas (limite padrão,
login, e-mails em massa, webhook do Mercado Pago, links com token, prontidão, escritas
autenticadas, cadastro público) e a política de memória do Redis que guarda os contadores.
**Escopo das rodadas anteriores:** aplicação Flask/Python completa (autenticação, autorização, acesso a dados,
injeção, XSS, CSRF, uploads, segredos, pagamentos, matrícula/turma, presença). Esta rodada
aprofundou especificamente áreas ainda não detalhadas nas anteriores: OAuth do Gmail e do
Mercado Pago (conexão da conta da academia), Checkout Pro, páginas públicas legais,
credenciais do administrador e armazenamento de arquivos.
**Método:** leitura direta do código-fonte atual (não apenas dos relatórios anteriores),
consulta ao grafo do projeto, `grep`/varredura de sinks, Bandit, `pip-audit` e testes locais.
Nenhum segredo foi lido ou exibido. Nenhum serviço externo ou ambiente de produção foi
atacado.

> Este arquivo é o **único relatório de segurança mantido no repositório**. Ele substitui e
> incorpora quatro análises anteriores (05/09, 12/09, 17/09 e 21/09/2026), cada uma revalidando
> a anterior lendo o código diretamente. Os arquivos antigos foram removidos; o histórico
> resumido de cada rodada está na seção **Histórico de auditorias** no fim deste documento.

## Situação atual (04/10/2026 — limites de requisição)

**Nenhum achado de segurança aberto.** Antes desta rodada, 62 das 85 rotas não tinham limite
algum: o `limiter` nascia com `default_limits=[]` e só a rota com decorador era contida. Os
nove pontos abaixo (SEC-10 a SEC-17 e SEC-19) foram corrigidos, cada um com teste que estoura
o limite e espera 429 (ou, no caso do webhook e do Redis, que verifica o comportamento). O
SEC-18 é só informativo e não foi implementado, porque a correção é de front-end.

Cobertura depois da rodada: das 85 rotas, **44 têm limite próprio, 40 ficam com o limite
padrão e 1 é isenta** (`/health`, healthcheck do Docker). Arquivos de `/static/` não passam
pelo limitador (o Flask-Limiter dispensa o endpoint `static`).

Chaves usadas: `chave_da_conta` ([config.py:10-24](../config.py#L10-L24)) devolve
`aluno:<id>`, `professor:<id>` ou `admin` quando há sessão, e `ip:<endereço>` quando não há,
para alunos no mesmo Wi-Fi da academia não dividirem cota. Os limites declarados sem
`key_func` continuam por IP (`get_remote_address`).

| ID | Achado | Severidade | Status | Evidência |
|---|---|---|---|---|
| SEC-10 | Sem limite padrão: 62 das 85 rotas sem limite nenhum (`default_limits=[]`) | Média | **Corrigido** | [config.py:30-36](../config.py#L30-L36): `Limit('300 per minute;3000 per hour', key_function=chave_da_conta)` vale para toda rota sem decorador (um decorador na rota substitui o padrão, e um limite só de `POST` deixa o `GET` no padrão). `/health` ganhou `@limiter.exempt` ([servidor.py:342-345](../servidor.py#L342-L345)). Testes: `test_limite_padrao_tem_teto_por_minuto_e_por_hora_por_conta`, `test_limite_padrao_alcanca_rota_sem_limite_proprio` (301ª requisição → 429), `test_limite_padrao_e_por_conta_e_cai_no_ip_sem_sessao` e `test_health_e_static_ficam_fora_do_limite_padrao` (320 requisições sem 429), em `tests/test_limites_requisicao.py`. |
| SEC-11 | Login sem teto por conta: as chaves eram IP e IP+usuário, então um ataque vindo de muitos IPs contra a mesma conta não tinha limite | Média | **Corrigido**, com risco residual | [usuario_bp.py:132-141](../blueprints/usuario_bp.py#L132-L141): `10 per hour` no `POST` com chave `usuario:<sha256 do login sem espaços e em minúsculas>`, somado aos limites que já existiam (`20 per minute` por IP e `5 per 15 minutes` por IP+usuário). **Risco residual:** quem souber um login, inclusive o do admin, consegue bloquear a entrada dessa conta por até 1 hora com 10 tentativas erradas, de qualquer IP. É a troca inerente a um teto por conta; o contador conta todo `POST`, inclusive login certo. Teste: `test_login_tem_teto_por_usuario_mesmo_vindo_de_muitos_ips` (11 IPs diferentes; caixa e espaços não abrem cota nova). |
| SEC-12 | E-mails em massa sem limite no painel do admin | Média (condicional: exige sessão de admin) | **Corrigido** | Por conta de admin: aviso `POST` 10/h ([adm_bp.py:936-938](../blueprints/adm_bp.py#L936-L938)), cobrança dos inadimplentes 5/h ([adm_bp.py:1023](../blueprints/adm_bp.py#L1023)), cobrança individual 30/h ([adm_bp.py:1074](../blueprints/adm_bp.py#L1074)) e convite 30/h ([adm_bp.py:470](../blueprints/adm_bp.py#L470)). A chave de idempotência por dia já impedia a cobrança em lote repetida, mas um aviso com texto diferente a cada envio ia para todos os alunos sem teto, e a cobrança individual chama `enviar_email` direto a cada clique. Com uma sessão de admin roubada, isso transformava o Gmail da academia em disparador. Testes: `test_escritas_do_admin_tem_limite` (4 casos), `test_limite_do_admin_segue_a_conta_e_nao_o_ip` e `test_tela_de_avisos_continua_abrindo_depois_do_limite_de_envio`. |
| SEC-13 | Webhook do Mercado Pago sem limite e sem recusa de repetição: uma notificação assinada e capturada valia pelos 300 s da janela de recência, e cada reenvio custava uma consulta à API do Mercado Pago | Baixa | **Corrigido** | `120 per minute` por IP ([pix_bp.py:441-444](../blueprints/pix_bp.py#L441-L444)). Depois de validar a assinatura, `limiter.storage.incr` grava a marca de `x-request-id` + `data.id` (sha256) por 300 s; a repetição recebe 200 sem reprocessar ([pix_bp.py:408-438](../blueprints/pix_bp.py#L408-L438) e [pix_bp.py:463-475](../blueprints/pix_bp.py#L463-L475)). A marca é liberada quando o processamento falha do nosso lado (resposta 5xx ou exceção), para o reenvio do Mercado Pago ser processado. Se o storage cair, a notificação segue e o fato vai para o log: a assinatura já foi validada e o processamento é idempotente. Assinatura inválida não gasta a marca. Testes: `test_webhook_tem_limite_por_ip`, `test_webhook_repetido_responde_200_sem_reprocessar`, `test_webhook_com_assinatura_invalida_nao_queima_o_request_id`, `test_webhook_que_falhou_do_nosso_lado_e_reprocessado_no_reenvio` e `test_webhook_segue_se_o_storage_do_limitador_cair`. |
| SEC-14 | `/cadastro/verificar/<token>` sem limite, ao contrário das rotas irmãs com token | Baixa (o token tem 256 bits; defesa em profundidade) | **Corrigido** | `30 per hour` por IP, igual a `confirmar_email`, `ativar_acesso` e `redefinir_senha` ([usuario_bp.py:1222-1225](../blueprints/usuario_bp.py#L1222-L1225)). Teste: `test_link_de_verificacao_do_cadastro_tem_limite`. |
| SEC-15 | `/health/pronto` isento de limite, consultando banco e Redis a cada chamada pública | Baixa | **Corrigido** | `@limiter.exempt` virou `60 per minute` por IP ([servidor.py:348-353](../servidor.py#L348-L353)); foi escolhida a opção sem token. Isso reverte de propósito a isenção criada no commit `0e5b399`. O healthcheck do Docker usa `/health`, que segue isento. Teste: `tests/test_prontidao.py::test_pronto_tem_limite_por_ip`, que substitui o teste que exigia a isenção. |
| SEC-16 | Escritas autenticadas sem limite | Baixa (todas exigem sessão válida) | **Corrigido** | Por conta: `confirmar_presenca` 30/h ([usuario_bp.py:530](../blueprints/usuario_bp.py#L530)), `cancelar_mudanca_plano` 10/h ([usuario_bp.py:544](../blueprints/usuario_bp.py#L544)), `remover_foto_perfil` 20/h ([usuario_bp.py:1066](../blueprints/usuario_bp.py#L1066)), `continuar_checkout` com `limitar_consulta_pagamento` ([checkout_bp.py:186](../blueprints/checkout_bp.py#L186)), desconectar Gmail e Mercado Pago 10 a cada 15 min ([gmail_oauth_bp.py:57](../blueprints/gmail_oauth_bp.py#L57), [mercado_pago_oauth_bp.py:174](../blueprints/mercado_pago_oauth_bp.py#L174)), `enviar_foto_aluno` e `cadastrar_aluno` (`POST`) 30/h ([adm_bp.py:595](../blueprints/adm_bp.py#L595), [adm_bp.py:370](../blueprints/adm_bp.py#L370)), escritas financeiras do admin 60/h ([adm_bp.py:644](../blueprints/adm_bp.py#L644), [718](../blueprints/adm_bp.py#L718), [747](../blueprints/adm_bp.py#L747), [777](../blueprints/adm_bp.py#L777)), `matricular_aluno` e `registrar_presenca` 60/h ([turma_bp.py:257](../blueprints/turma_bp.py#L257), [turma_bp.py:294](../blueprints/turma_bp.py#L294)). `logout` 60/min por IP ([servidor.py:363-364](../servidor.py#L363-L364)). Testes: `test_escritas_do_admin_tem_limite` (10 casos), `test_escritas_do_aluno_tem_limite` (4 casos), `test_limite_das_escritas_do_aluno_e_por_conta` e `test_logout_tem_limite_por_ip`. |
| SEC-17 | Cadastro público com 5/h por IP bloqueava cadastros legítimos: a academia inteira sai por um IP só | Baixa (disponibilidade) | **Corrigido** | `20 per hour` por IP ([usuario_bp.py:242-245](../blueprints/usuario_bp.py#L242-L245)). Mantido o `3 per hour` cuja chave é IP + hash do CPF (já era assim; não é um teto só por CPF). Testes: `test_cadastro_publico_aceita_20_por_hora_do_mesmo_ip` e `test_cadastro_publico_mantem_3_por_hora_por_cpf`. |
| SEC-18 | Fontes carregadas do Google Fonts: o `@import` em [static/css/theme.css:7](../static/css/theme.css#L7) (liberado na CSP em `style-src`/`font-src` de `servidor.py`) faz o navegador de todo visitante, inclusive em páginas públicas e sem consentimento, enviar o IP ao Google | Informativo (LGPD) | **Não implementado** (fora do escopo: front-end) | A política de privacidade (`templates/politica_privacidade.html`) cita o Google só no contexto do Gmail da academia, não das fontes. Caminhos possíveis: servir Bebas Neue e Inter (licença OFL) de `static/` e tirar `fonts.googleapis.com`/`fonts.gstatic.com` da CSP, ou declarar o compartilhamento na política de privacidade. |
| SEC-19 | Redis do rate limit com `allkeys-lru` e 32 MB: sob pressão de memória ele apagava contadores ainda em uso, e quem estava bloqueado voltava a ter cota inteira justamente sob carga | Média (condicional: só com o Redis cheio) | **Corrigido** | [compose.yaml:22-32](../compose.yaml#L22-L32): `--maxmemory-policy volatile-ttl` e `--maxmemory 64mb`. Todas as chaves do Flask-Limiter e a marca do webhook têm TTL, então `volatile-ttl` descarta primeiro a mais perto de expirar. O `mem_limit` do container subiu de 48m para 96m; com 64 MB de dados num container de 48 MB, o processo seria morto por falta de memória. Teste: `test_redis_do_rate_limit_nao_apaga_contadores_sob_carga`. |

## Rodada anterior (22/09/2026 — 2ª rodada)

**Nenhum achado de segurança aberto.** Os 9 pontos de atenção da varredura de 21/09/2026
seguem corrigidos (revalidados de novo, com leitura direta do código de
`matricular_com_lotacao`, `efetivar_turma_da_cobranca`, `registrar_lote`, o arranque de
`servidor.py` e o `UniqueConstraint` de `Matricula`, não apenas repetindo a rodada anterior).
Esta rodada também cobriu OAuth do Gmail/Mercado Pago, Checkout Pro, upload de comprovantes/
fotos, páginas legais públicas e a credencial do administrador — nenhuma injeção, IDOR, SSRF,
open redirect ou exposição de segredo encontrada nesses fluxos. Um ponto novo de baixa
severidade foi identificado e já corrigido nesta mesma rodada (OBS-01), e a pendência não
relacionada a segurança do `requirements.lock` foi resolvida.

| ID | Achado | Severidade | Status | Evidência |
|---|---|---|---|---|
| OBS-01 | `/admin/gmail/conectar` e `/admin/gmail/callback` não tinham `@limiter.limit(...)`, diferente das rotas equivalentes do Mercado Pago (`10 per 15 minutes` / `20 per 15 minutes`) | Baixa (informativo) | **Corrigido nesta rodada** | Em 22/09, `limiter` tinha `default_limits=[]` (desde 04/10 há limite padrão; ver SEC-10), ou seja, sem decorator a rota ficava sem limite algum. Ambas as rotas já exigiam `@admin_requerido` e o `callback` só prossegue com um `state` HMAC válido gerado pela própria sessão, então o impacto prático era baixo — mas a inconsistência entre os dois fluxos OAuth valia corrigir por padronização. Adicionados os mesmos limites do fluxo do Mercado Pago em [gmail_oauth_bp.py:18-33](../blueprints/gmail_oauth_bp.py#L18-L33). |

| ID | Achado | Severidade original | Status em 22/09 | Evidência |
|---|---|---|---|---|
| SEC-01 | Matrícula criada antes da confirmação do pagamento | Média | **Corrigido** | `turma_id` fica pendurado na cobrança (`Pagamento.turma_id`), inclusive quando escolhido pelo aluno via `_turma_do_formulario` em [usuario_bp.py:430-435](../blueprints/usuario_bp.py#L430-L435) (valida a turma contra o banco antes de aceitar o id); a `Matricula` só é criada em [`efetivar_turma_da_cobranca`](../dao/financeiroDAO.py#L729-L742), chamada por [`atualizar_status`](../dao/financeiroDAO.py#L715-L718) apenas quando `status == 'pago'`. Turma lotada gera evento `matricula_sem_vaga` em vez de estourar o limite. |
| SEC-02 | Professor recebe lista global de alunos ativos | Média (condicional) | **Não reproduz** | `alunos_disponiveis` só é montada `if eh_admin` em [turma_bp.py:242](../blueprints/turma_bp.py#L242); o template gate a mesma condição em [turma.html:60](../templates/turma.html#L60); a rota de matrícula usa `@admin_requerido` ([turma_bp.py:257](../blueprints/turma_bp.py#L257)), não decorator de professor. |
| SEC-03 | Verificação de lotação sujeita a corrida concorrente | Média | **Corrigido** | [`matricular_com_lotacao`](../dao/matriculaDAO.py#L21-L37) usa `.with_for_update()` na turma e checa a contagem dentro da mesma transação antes do insert. |
| SEC-04 | Estados e valores financeiros sem validação de domínio | Média | **Corrigido** | `Decimal` + `is_finite()` + limites de valor/duração + allowlist `STATUS_VALIDOS`/`FORMAS_PAGAMENTO_VALIDAS` em [adm_bp.py:148-155](../blueprints/adm_bp.py#L148-L155), [adm_bp.py:498-511](../blueprints/adm_bp.py#L498-L511) e [adm_bp.py:560-564](../blueprints/adm_bp.py#L560-L564). |
| SEC-05 | Confirmação de frequência não invalidada ao corrigir presença | Baixa | **Corrigido** | [`registrar_lote`](../dao/presencaDAO.py#L15-L23) zera `confirmada_aluno`/`confirmada_em` quando `presente` vira falso. |
| SEC-06 | `SECRET_KEY` sem requisito mínimo de força | Média (condicional) | **Corrigido** | [servidor.py:33-34](../servidor.py#L33-L34) exige `len(app.secret_key) >= 32`. |
| SEC-07 | Rate limiting com fallback em memória | Média (condicional) | **Corrigido** | [servidor.py:49-52](../servidor.py#L49-L52) falha no arranque se `APP_BASE_URL` for HTTPS e `RATELIMIT_STORAGE_URI` continuar `memory://`. |
| SEC-08 | Logs registram e-mails completos | Baixa | **Corrigido** | [`_destinatario_log`](../servicos/email.py#L15-L20) mascara (`ab***@dominio`) e é usado em todos os `logger.warning`/`logger.exception` com destinatário. |
| SEC-09 | Dependências sem lockfile/hash transitivo | Baixa | **Corrigido** | `requirements.lock` está commitado (`git ls-files` confirma) e o `Dockerfile` agora copia `requirements.lock` e instala com `pip install --require-hashes -r requirements.lock` ([Dockerfile diff em 062ac87](../Dockerfile)), em vez de `requirements.txt` sem hash. A pendência de commit que constava na rodada anterior já não existe. |

### Pendências não relacionadas a segurança

**Resolvida em 04/10/2026:**
`tests/test_checkout_rotas.py::test_webhook_encontra_mensalidade_por_referencia_do_checkout`
falhava: o pagamento virava `pago`, mas `aluno.mensalidade` ficava `Pendente`. **Era bug do
teste, não do código.** O duplo do Mercado Pago devolve `date_approved` fixo em `2026-09-04`. O código
abre a vigência a partir da data de aprovação (`abrir_vigencia` → `garantir_vigencia`, em
`dao/financeiroDAO.py`): 04/09 + 30 dias - 1 = 03/10. Desde 04/10, `vigencia_ativa` não acha
período que cubra hoje, `situacao_plano` cai em `vencido` e `_sincronizar_situacao` grava
`Pendente`. Rodando o mesmo teste com `date.today()` simulado: passa em 03/10 e falha em 04/10.
A regra (período conta da data em que o aluno pagou) está certa. Correção: os duplos de
`tests/test_checkout_rotas.py` e `tests/test_auditoria_seguranca.py` (que tinha a mesma data
fixa) passam a gerar `date_approved` a partir de agora, no fuso do Mercado Pago, como já
faziam `test_pix_rotas.py` e `test_pagamento_recusado.py`. O código não foi alterado.

**Resolvidas em 27/09/2026:**

**Todas resolvidas (27/09/2026).** A 2ª rodada de 22/09 encontrou 4 falhas de teste na suíte
completa, todas dívida de teste e nenhuma vulnerabilidade. Revalidadas uma a uma em 27/09:

| Teste | Causa em 22/09 | Situação em 27/09 |
|---|---|---|
| `test_seguranca.py::test_cadastro_publico_rejeita_cpf_invalido` | `Aluno.query` fora do contexto de aplicação | Passa; o teste usa a fixture `contexto_app`, que abre o contexto de aplicação. |
| `test_email_gmail.py` (2 testes) | Chamavam `email._enviar_via_gmail`, que deixou de existir com a conexão OAuth | Arquivo reescrito para `servicos/gmail_conta.py` (commits `795bb2b` e `56e5d9c`); nenhuma referência à função antiga. |
| `test_mercado_pago_oauth.py::test_sem_chave_dedicada_a_cifra_deriva_da_secret_key` | `MERCADO_PAGO_TOKEN_KEY` do `.env` local vazava para o teste | Passa; o `tests/conftest.py` zera essa e as demais variáveis de integração antes de importar o app. |
| `test_publicas_redesign.py::test_landing_page` | Esperava o texto antigo da home (`VÁ AO EXTREMO.`) | Passa; o teste acompanha o texto atual. |

Resultado da suíte completa em 27/09/2026: `pytest -q` → **740 passaram, 0 falharam, 0
pulados**, com os 8 testes `*_postgres.py` executados contra um PostgreSQL 17 local descartável
(`TEST_POSTGRES_URL` com socket em `/tmp/`, exigência dos próprios testes). Sem essa variável,
os mesmos 8 aparecem como pulados e o restante continua verde (732 passaram).

## Controles verificados

- `CSRFProtect` inicializado e aplicado globalmente; única exceção é o webhook assinado do
  Mercado Pago em [pix_bp.py:328-329](../blueprints/pix_bp.py#L328-L329).
- Cookies com `HttpOnly`, `SameSite=Lax`, `Secure` configurável e lifetime limitado.
- Login limpa a sessão; sessões têm identificador e credencial revalidada; logout registra
  revogação no banco (`sessoes_revogadas`).
- Aluno, professor e administrador são revalidados no banco antes de acessar suas áreas.
- Acesso de professor à turma verifica o `professor_id` da turma.
- Pagamentos, comprovantes, fotos e presença do aluno têm verificação de propriedade.
- Webhook do Mercado Pago valida assinatura HMAC-SHA256 em tempo constante, janela de
  recência de 300s (com proteção explícita contra `ts=nan`) e reconsulta a API — nunca
  confia no status recebido no corpo do webhook ([mercado_pago.py:412-450](../servicos/mercado_pago.py#L412-L450)).
- Checkout Pro: valor cobrado sempre lido do banco (nunca do navegador), `back_urls`
  construídas com `url_publica()` (nunca com o `Host` da requisição), destino do checkout
  restrito por allowlist de host (`url_checkout_permitida`, só aceita
  `www.mercadopago.com.br`/`sandbox.mercadopago.com.br` em HTTPS) e retorno do checkout
  ignora por completo a query string, reconsultando a API — ver [checkout_bp.py](../blueprints/checkout_bp.py) e [mercado_pago.py:49-57](../servicos/mercado_pago.py#L49-L57).
- OAuth do Gmail e do Mercado Pago (conexão da conta da academia): `state` aleatório
  (32+ bytes), comparado com `hmac.compare_digest`, validade curta (600s/10min), PKCE
  (S256) no fluxo do Mercado Pago, `redirect_uri` sempre derivada de `APP_BASE_URL` (nunca
  do `Host` da requisição — `servicos/urls.py` rejeita valor com espaço, userinfo, path,
  query ou fragmento). Refresh/access tokens cifrados com Fernet (chave derivada via HKDF
  da `SECRET_KEY`, ou de `MERCADO_PAGO_TOKEN_KEY` dedicada) e nunca logados nem devolvidos
  à tela — ver [gmail_conta.py](../servicos/gmail_conta.py), [mercado_pago_conta.py](../servicos/mercado_pago_conta.py).
- Renovação do token do Mercado Pago usa `with_for_update()` na linha da conexão para
  serializar processos concorrentes e não gastar duas vezes o mesmo `refresh_token` de uso
  único ([mercado_pago_conta.py:317-353](../servicos/mercado_pago_conta.py#L317-L353)).
- Credencial do administrador: usuário comparado em tempo constante antes da senha, senha
  sempre via `check_password_hash` (nunca texto puro no ambiente) — ver [credenciais.py](../servicos/credenciais.py).
- SQLAlchemy/ORM em todos os acessos revisados; nenhum sink de SQL injection confirmado.
- Curingas de `LIKE` escapados (`%`, `_`, `\`) em `financeiroDAO.py` e `usuarioDAO.py`.
- Uploads armazenados fora de `static/`, nome gerado por UUID, validação de conteúdo real
  (não apenas extensão/Content-Type) e limite de pixels.
- Jinja com autoescape; nenhum `|safe`, `render_template_string`, `innerHTML`, `eval` ou
  `document.write` em caminho explorável.
- Cabeçalhos de segurança (`CSP` com nonce, `X-Content-Type-Options`, `X-Frame-Options`,
  `Referrer-Policy`, `Permissions-Policy`, HSTS condicional) aplicados a toda resposta.
- Páginas autenticadas saem com `Cache-Control: no-store`.
- `pip-audit` sem vulnerabilidades conhecidas nas dependências declaradas.
- Bandit: 1 alerta médio (`app.run(host="0.0.0.0")`, protegido por `if __name__ == '__main__'`;
  produção usa Gunicorn) e alertas baixos, todos falsos positivos de constantes/`None`.

## Validação executada em 04/10/2026

- Linha de base antes das mudanças: `pytest -q` → 895 passaram, 1 falhou (o teste de data fixa
  descrito em **Pendências**), 8 pulados.
- Depois das mudanças de rate limit: `pytest -q` → 932 passaram, 1 falhou (o mesmo), 8 pulados.
- Depois de corrigir a data fixa dos testes: `pytest -q` → **933 passaram, 0 falharam, 8
  pulados**. Os 8 pulados são os `*_postgres.py`, sem `TEST_POSTGRES_URL` nesta máquina.
- Prova de que os testes novos detectam a falta da proteção: os 46 testes de
  `tests/test_limites_requisicao.py` e `tests/test_prontidao.py` rodados contra o `HEAD` sem as
  mudanças (worktree descartável): 33 falharam. Os 13 que passam lá cobrem comportamento que já
  existia e precisa continuar valendo: as isenções de `/health` e `/static/`, o `3 per hour` por
  IP+CPF, assinatura inválida e reprocessamento depois de 503 no webhook, e os testes antigos de
  prontidão.
- Contagem de cobertura feita com o `url_map` e o `limit_manager` do próprio app: 85 rotas, 44
  com limite próprio, 40 só com o padrão, 1 isenta.
- Nenhuma requisição foi enviada a Mercado Pago, Gmail, Redis ou PostgreSQL de produção.

## Validação executada em 22/09/2026

**1ª rodada:**
- `pytest -q tests/test_contratacao_plano.py tests/test_datas_turma.py tests/test_seguranca.py
  tests/test_cadastro_administrativo.py tests/test_arranque_seguranca.py`: **127 passaram, 1
  falhou** (bug de teste descrito acima, não vulnerabilidade).
- Bandit sobre o projeto (excluindo testes/venv/graphify-out): mesma distribuição de alertas
  do relatório anterior (1 médio esperado, restante baixo/falso positivo).

**2ª rodada (esta atualização):**
- `pytest -q tests/test_seguranca.py tests/test_auditoria_seguranca.py
  tests/test_arranque_seguranca.py tests/test_regressao_auditoria.py
  tests/test_checkout_rotas.py`: 246 passaram, 1 falhou (mesmo bug de teste conhecido).
- `pytest -q` (suíte **completa**, 632 testes): **623 passaram, 5 falharam, 8 pulados** —
  as 4 falhas além da já conhecida foram investigadas e são dívida de teste, não segurança
  (ver **Pendências não relacionadas a segurança**); confirmado que nenhuma delas é causada
  pela correção do OBS-01 (mesmo resultado com e sem a mudança, via `git stash`).
- Bandit (`bandit -r .` excluindo testes/venv/graphify-out/tools): 1 médio (f-string em
  `migrations/versions/c7a4e1b93d20_...py:108` — os dois valores possíveis vêm só de
  `bind.dialect.name`, nunca de entrada do usuário; migração de banco executada uma vez no
  deploy — falso positivo confirmado lendo o arquivo) + 7 baixos (nomes de constante como
  `TOKEN_URL`/`SEND_URL` reconhecidos como "possível senha hardcoded" — falsos positivos).
- `pip-audit -r requirements.txt`: **sem vulnerabilidades conhecidas**.
- `git ls-files | grep requirements` confirma `requirements.lock` versionado.
- Nenhuma requisição foi enviada a Mercado Pago, Gmail, Redis ou PostgreSQL de produção.

## Histórico de auditorias

Resumo das rodadas anteriores — os arquivos originais foram removidos do repositório em
22/09/2026 para manter um único relatório vivo; o conteúdo relevante de cada um foi
revalidado e está refletido nas seções acima.

| Data | Escopo | Achados | Resultado |
|---|---|---|---|
| 05/09/2026 | Auditoria inicial completa (autenticação, autorização, CSRF, XSS, uploads, segredos) | 15 achados (F1–F15) | Todos corrigidos e revalidados nas rodadas seguintes. |
| 12/09/2026 | Reauditoria de segurança/desempenho | 1 achado médio (tempo de resposta em `/recuperar_senha`) + itens de desempenho | Achado de segurança corrigido em 19/09 (ver A1 abaixo); itens de desempenho tratados parcialmente por desenho. |
| 17/09/2026 (atualizado 19/09) | Revalidação de F1–F15 + novos achados A1–A4 + varredura independente S1–S2 + fluxo OAuth do Mercado Pago | A1–A4 (recuperação de senha vazando tempo, `/perfil/dados` sem limite de tentativas nem validação de tamanho, enumeração de usuário/e-mail) e S1–S2 (logout não revogava sessão, páginas autenticadas sem `Cache-Control`) | Todos corrigidos em 19/09/2026. |
| 21/09/2026 | Foco nos fluxos recentes de matrícula, turma, presença e permissões de professor | SEC-01 a SEC-09 (0 alto, 6 médio, 3 baixo) | Todos confirmados corrigidos (ou não reprodutíveis) em 22/09/2026 — ver tabela **Situação atual** acima. |
| 04/10/2026 | Rate limit em todas as rotas, webhook do Mercado Pago (repetição de notificação), prontidão, política de memória do Redis | SEC-10 a SEC-17 e SEC-19 (0 alto, 4 médio, 5 baixo) + SEC-18 informativo (Google Fonts/LGPD) | SEC-10 a SEC-17 e SEC-19 corrigidos com teste; SEC-18 registrado sem implementar (front-end). |
| 22/09/2026 (2ª rodada) | OAuth Gmail/Mercado Pago, Checkout Pro, upload de arquivos, páginas legais públicas, credencial do administrador, revalidação independente de SEC-01/03/05/06/07/09 | OBS-01 (rate limit ausente no OAuth do Gmail, baixa/informativo); `requirements.lock` confirmado commitado e já usado com `--require-hashes` no Dockerfile | Nenhum achado de segurança aberto; ver tabelas **Situação atual** acima. |

**Nenhuma injeção de SQL, XSS refletido/armazenado/DOM, path traversal, IDOR, SSRF ou
segredo exposto foi encontrado em nenhuma das rodadas.**
