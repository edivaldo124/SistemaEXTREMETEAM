# Relatório de segurança — Sistema Extreme Team

**Última atualização:** 22/09/2026 (segunda rodada do dia)
**Escopo:** aplicação Flask/Python completa (autenticação, autorização, acesso a dados,
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

## Situação atual (22/09/2026 — 2ª rodada)

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
| OBS-01 | `/admin/gmail/conectar` e `/admin/gmail/callback` não tinham `@limiter.limit(...)`, diferente das rotas equivalentes do Mercado Pago (`10 per 15 minutes` / `20 per 15 minutes`) | Baixa (informativo) | **Corrigido nesta rodada** | `limiter` tem `default_limits=[]` ([config.py:11](../config.py#L11)), ou seja, sem decorator a rota ficava sem limite algum. Ambas as rotas já exigiam `@admin_requerido` e o `callback` só prossegue com um `state` HMAC válido gerado pela própria sessão, então o impacto prático era baixo — mas a inconsistência entre os dois fluxos OAuth valia corrigir por padronização. Adicionados os mesmos limites do fluxo do Mercado Pago em [gmail_oauth_bp.py:18-33](../blueprints/gmail_oauth_bp.py#L18-L33). |

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

Rodar a suíte **completa** (`pytest -q`, 632 testes) nesta rodada — as rodadas anteriores
sempre selecionaram um subconjunto de arquivos — revelou mais 4 falhas além da já conhecida,
todas investigadas individualmente até a causa raiz. Nenhuma é uma vulnerabilidade; todas são
dívida de teste:

- **`tests/test_seguranca.py::test_cadastro_publico_rejeita_cpf_invalido`**: a asserção final
  consulta `Aluno.query` fora de um contexto de aplicação Flask (`RuntimeError: Working
  outside of application context`). Já documentado desde 21/09.
- **`tests/test_email_gmail.py::test_envia_pelo_gmail_com_refresh_token` e
  `test_gmail_sem_credenciais_nao_chama_rede`**: chamam `email._enviar_via_gmail`, uma
  função que **não existe mais** em `servicos/email.py` (`AttributeError`). É um teste órfão
  do envio de e-mail por variável de ambiente (`GMAIL_REFRESH_TOKEN`), fluxo substituído
  pela conexão OAuth com o banco em `servicos/gmail_conta.py` (revisada e aprovada nesta
  rodada — ver **Controles verificados**). O arquivo de teste antigo não foi removido/
  atualizado junto com a migração.
- **`tests/test_mercado_pago_oauth.py::test_sem_chave_dedicada_a_cifra_deriva_da_secret_key`**:
  falha **só neste ambiente local**, porque o teste não limpa `MERCADO_PAGO_TOKEN_KEY` (não
  usa a fixture `oauth_env`, que faz `monkeypatch.delenv('MERCADO_PAGO_TOKEN_KEY', ...)`) e
  o `.env` local da máquina já tem essa variável definida — `load_dotenv()` ([servidor.py:13](../servidor.py#L13))
  não sobrescreve variável já presente no ambiente. Com a variável setada, `_fernet()` usa a
  chave dedicada e ignora a `SECRET_KEY` de propósito, então trocar `app.secret_key` no teste
  não muda nada. **Reproduzido isoladamente fora do pytest** (sem `MERCADO_PAGO_TOKEN_KEY`) que
  o comportamento real do produto está correto: derivar a chave da `SECRET_KEY` e depois trocar
  a `SECRET_KEY` de fato torna o token ilegível (`ConexaoIlegivel`), confirmando a garantia
  documentada em [mercado_pago_conta.py:87-88](../servicos/mercado_pago_conta.py#L87-L88). Falso
  negativo de teste, não falha de produto — mas vale adicionar a fixture `oauth_env` a este
  teste para não mascarar uma regressão real nesse caminho no futuro.
- **`tests/test_publicas_redesign.py::test_landing_page`**: espera o texto `'VÁ AO EXTREMO.'`
  no HTML da home, que não está mais lá — troca de copy na landing page sem atualizar o teste.
  Conteúdo de marketing, sem relação com segurança.

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
| 22/09/2026 (2ª rodada) | OAuth Gmail/Mercado Pago, Checkout Pro, upload de arquivos, páginas legais públicas, credencial do administrador, revalidação independente de SEC-01/03/05/06/07/09 | OBS-01 (rate limit ausente no OAuth do Gmail, baixa/informativo); `requirements.lock` confirmado commitado e já usado com `--require-hashes` no Dockerfile | Nenhum achado de segurança aberto; ver tabelas **Situação atual** acima. |

**Nenhuma injeção de SQL, XSS refletido/armazenado/DOM, path traversal, IDOR, SSRF ou
segredo exposto foi encontrado em nenhuma das rodadas.**
