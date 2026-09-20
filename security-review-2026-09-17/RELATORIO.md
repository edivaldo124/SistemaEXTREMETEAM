# Relatório de segurança — Sistema Extreme Team (17/09/2026)

> **Atualizado em 19/09/2026.** Os achados A1–A4 e o housekeeping do `pip` foram corrigidos, e uma nova varredura
> encontrou e corrigiu S1 e S2. Veja a seção **"Atualização de 19/09/2026"** logo abaixo da introdução.
> O restante do texto descreve o estado do código em 17/09.

**Escopo:** aplicação Flask completa, incluindo o código não commitado no momento da
análise (repopulação do formulário de cadastro e Termo de Responsabilidade).
**Referência:** OWASP Top 10:2025, ASVS 5.0, checklist do skill `owasp-security`.
**Metodologia:** leitura direta do código-fonte atual (não apenas dos relatórios
anteriores), `grep` por padrões perigosos, `pip-audit` contra as dependências
instaladas. Nenhum segredo foi lido/exibido, nenhuma chamada real foi feita ao
Mercado Pago ou à Brevo, nenhum arquivo de produção foi tocado.

Este projeto já tinha dois relatórios de segurança no repositório:
[`security_best_practices_report.md`](../security_best_practices_report.md) (05/09) e
[`reauditoria_seguranca_desempenho_2026-09-12.md`](../reauditoria_seguranca_desempenho_2026-09-12.md)
(12/09). Esta análise **revalidou os dois** lendo o código atual (não confiou nos
textos anteriores) e comparou com os commits e as alterações não commitadas desde
então. Resultado: os 15 achados do relatório de 05/09 continuam corrigidos; o achado
médio do relatório de 12/09 **continua aberto**, reproduzido abaixo.

---

## Atualização de 19/09/2026 — correções aplicadas e nova varredura

As seções abaixo preservam a análise de 17/09 e descrevem o estado do código naquele dia.
Em 19/09/2026 os achados abertos foram corrigidos e o código foi revisado de novo. As
correções estão no working tree da branch `redesign-et` (ainda sem commit no momento desta
atualização).

### Correções dos achados de 17/09

| ID | Estado | O que foi feito |
|---|---|---|
| A1 | Corrigido | `/recuperar_senha` envia o e-mail numa thread própria (`_enviar_em_segundo_plano` em `blueprints/usuario_bp.py`), fora da requisição. **Difere da recomendação original** (usar `fila_email`): a fila grava o `link_url` em claro em `emails_pendentes`, e o token de recuperação hoje só existe como hash no banco. Sobra uma diferença de poucos milissegundos (o `commit` do token só ocorre no ramo "par existe"), **não medida**. |
| A2 | Corrigido | `/perfil/dados` ganhou `@limiter.limit('15 per hour', key_func=_chave_da_conta)`, igual a `/perfil/senha`. |
| A3 | Corrigido | `/perfil/dados` valida nome (150), login (50), telefone (20) e descrição (255) e trata `IntegrityError` no `commit`. O mesmo furo do telefone existia em `/cadastrar` e `/ativar-acesso`, e `/perfil/email` não validava o formato nem o tamanho do e-mail; os três foram fechados. |
| A4 | Corrigido para CPF e e-mail | Cadastro novo, CPF já existente e e-mail já existente devolvem a **mesma tela** (`MSG_CADASTRO_RECEBIDO`), sem criar conta e com o mesmo custo de hash de senha; o dono do e-mail recebe um aviso. **O nome de usuário continua com aviso explícito** ("já está em uso"), por decisão: quem escolhe um precisa saber para trocar, e não é dado pessoal. Correção de fato: o texto de 17/09 dizia que o CPF já devolvia a mesma mensagem nos dois casos, mas o ramo de CPF existente respondia diferente do cadastro novo. |
| pip local | Corrigido | `.venv` atualizado de 25.1.1 para 26.2.1. |

### Reforços em achados de 05/09 (F1–F15 seguem corrigidos)

- **F3:** falha de login agora é registrada com IP e resumo SHA-256 do identificador, nunca o valor digitado.
- **F8:** `nome` já não autenticava, mas o aluno podia gravar como `login` o e-mail ou o CPF de outra pessoa e, com `.first()`, ficar "na frente" da vítima no login. `AlunoDAO.autenticar` agora confere a senha nos até 3 candidatos.
- **F12:** o mesmo problema de tempo do login existia na recuperação de senha (ver A1).
- **F13:** a lista de senhas comuns tinha 8 entradas. Agora `servicos/senhas_comuns.txt` traz as 3000 mais comuns com 8 ou mais caracteres (ASVS 5.0 6.2.4), carregada no import; sem o arquivo o app não sobe.

### Nova varredura independente (19/09) — S1 e S2

Um subagente fez uma varredura guiada pelos checklists OWASP Top 10:2025 e ASVS 5.0, com testes dinâmicos em memória (matriz papel × rota, IDOR, SQL, XSS, OAuth, pagamentos, uploads, infraestrutura). **Nenhum achado de severidade Alta ou Média.** Dois de severidade Baixa, ambos exigindo posse do cookie ou acesso ao navegador da vítima:

| ID | Estado | Achado e correção |
|---|---|---|
| S1 | Corrigido | **`/logout` não revogava a sessão.** O cookie é assinado e sem estado; `session.clear()` limpava só o navegador de quem saiu, e uma cópia feita antes continuava aceita (reproduzido: `GET /admin` devolveu 200 após o logout) e, renovada a cada requisição, não expirava. Agora cada login grava um identificador aleatório (`sid`) no cookie e o logout o registra em `sessoes_revogadas` (`modelos/sessao_revogada.py`, migration `b5d9c3e71a26`). As verificações de admin, professor e aluno em `servicos/autorizacao.py` recusam `sid` revogado ou ausente. |
| S2 | Corrigido | **Páginas autenticadas sem `Cache-Control`.** O botão "Voltar" após o logout podia reexibir CPF e financeiro. Toda resposta a quem está autenticado sai com `Cache-Control: no-store` (exceto `/static`; a política própria das fotos é preservada). |

Observações menores da varredura, também corrigidas: `ts=nan` no cabeçalho do webhook passava pela janela de recência (agora `math.isfinite`); confirmar a troca de e-mail agora descarta links de recuperação e convite enviados ao endereço antigo; `.dockerignore` exclui `tools/`, os relatórios e os `.md` de trabalho da imagem.

### Revisão do fluxo OAuth do Mercado Pago (código novo da branch)

Sem achados. `state` aleatório com `compare_digest` e validade de 10 minutos, consumido uma vez; PKCE S256; `redirect_uri` vinda de `APP_BASE_URL`; tokens cifrados com Fernet e sem log; refresh sob trava de linha; rotas atrás de `@admin_requerido`, com CSRF no `desconectar`.

### Reauditoria de 12/09 (itens de desempenho)

- **Avisos carregam a base inteira (#3), parcial:** `AlunoDAO.listar_ativos()` filtra no SQL e o aviso "para todos" não carrega mais as mensalidades. O aviso "para inadimplentes" e a tela de avisos ainda carregam as mensalidades dos ativos, porque a situação depende das regras de plano em Python.
- **E-mails síncronos (#4), parcial:** aprovação e recusa de cadastro, cadastro recebido, aviso ao administrador, senha alterada, acesso ativado e aviso de troca de e-mail saem pela fila durável (`fila_email.enfileirar_transacional`). Continuam síncronos de propósito: `convites.enviar` (o token só é gravado depois da entrega), a cobrança individual (a mensagem da tela depende do resultado) e os e-mails com token (thread própria, ver A1).

### Não alterado (decisão ou baixo valor)

- `SECRET_KEY` aceita qualquer valor não vazio. Sem o carimbo de credencial não há exploração direta; uma checagem de tamanho no arranque poderia derrubar um `.env` que eu não pude ler.
- `datanascimento` é gravado sem validação de formato, e algumas rotas de admin devolvem 500 com entrada malformada. Não há caminho de exploração.
- O tempo de resposta do login revela o nome do usuário admin (documentado como aceito em `servicos/credenciais.py`).
- Sessão assinada sem estado: além do S1, o cookie continua válido até expirar (30 min, renovados a cada requisição) ou até a senha mudar.

### Validação e implantação

- `pytest -q`: **613 aprovados, 8 ignorados** (exigem `TEST_POSTGRES_URL`; a migration nova e a revogação de sessão foram testadas em SQLite, não em PostgreSQL).
- `pip-audit -r requirements.txt`: nenhuma vulnerabilidade conhecida.
- **Ao publicar:** rodar `flask db upgrade` (o Dockerfile já faz antes do Gunicorn) para criar `sessoes_revogadas`; quem estiver logado precisa entrar de novo uma única vez.

---

## Sumário

| ID | Severidade | Situação | Resumo |
|---|---|---|---|
| A1 | **Média** | **Corrigido em 19/09** (envio fora da requisição) | `/recuperar_senha` revela por tempo de resposta se o par CPF+e-mail existe |
| A2 | Baixa–Média | **Corrigido em 19/09** | `/perfil/dados` confere a senha atual sem nenhum limite de tentativas |
| A3 | Baixa | **Corrigido em 19/09** | `/perfil/dados` não valida tamanho de `nome`/`login`/`descricao` antes de gravar |
| A4 | Baixa / informativo | **Corrigido em 19/09** para CPF e e-mail (usuário mantém aviso, por decisão) | `/cadastrar` diferencia "usuário já cadastrado" de "e-mail já cadastrado" (enumeração) |
| — | Baixa / housekeeping | **Corrigido em 19/09** (pip 26.2.1) | `pip` do ambiente virtual local em 25.1.1 (atual: 26.2.1) |
| F1–F15 | — | **Confirmado corrigido** | Revalidados linha a linha nesta análise (ver seção própria); F3, F8, F12 e F13 ganharam reforços em 19/09 |
| S1 | Baixa | **Novo em 19/09, corrigido** | `/logout` não revogava a sessão: cópia do cookie seguia válida |
| S2 | Baixa | **Novo em 19/09, corrigido** | Páginas autenticadas sem `Cache-Control: no-store` |

Nenhuma injeção de SQL, XSS refletido/armazenado/DOM, path traversal, IDOR ou segredo
exposto foi encontrado no código atual (ver "Verificado e correto").

---

## A1 — `/recuperar_senha` revela por tempo de resposta se o CPF+e-mail existe (Média, CORRIGIDA em 19/09/2026)

**Status:** identificada no relatório de 12/09 com medição reproduzível; **revalidada
hoje lendo `blueprints/usuario_bp.py:731-772` — o código não mudou nesse trecho.**

```python
# blueprints/usuario_bp.py:742-768
aluno = Aluno.query.filter(Aluno.cpf.in_(variantes_cpf(cpf)), Aluno.email == email).first()

if aluno and aluno.acesso_ativado:
    token = secrets.token_urlsafe(32)
    ...
    db.session.commit()
    enviar_email(...)          # chamada HTTP síncrona à API da Brevo (timeout=10s)

return render_template("login.html", msg=MSG_RECUPERACAO_ENVIADA)   # mesma mensagem sempre
```

`servicos/email.py:52` faz um `requests.post` síncrono para `api.brevo.com` só quando
o par existe e a conta está ativada. A mensagem devolvida é idêntica nos dois casos,
mas o **tempo não**: o relatório de 12/09 mediu 11,6 ms para um par inexistente contra
206,1 ms para um par existente, com o provedor de e-mail simulado em 200 ms de latência
— consistente com uma chamada de rede real acontecendo só no caminho "existe".

**Impacto:** um atacante consegue testar pares CPF+e-mail e inferir quais já têm
cadastro com acesso ativado, sem que a resposta HTTP diferencie os casos. Os limites já
aplicados (`10 per hour` e `3 per hour` por IP+CPF, linhas 732-736) reduzem a
velocidade de exploração, mas não eliminam o canal.

**Correção recomendada:** a própria aplicação já tem a peça que falta — a fila
persistente de e-mail (`servicos/fila_email.py`), hoje usada em avisos e cobranças.
Trocar a chamada síncrona por `fila_email.enfileirar(...)` faz o `enviar_email` sair da
requisição HTTP nos dois ramos (existe ou não), igualando o tempo de resposta. O mesmo
vale para os e-mails síncronos do `/cadastrar` e do `/ativar-acesso`, que hoje não
vazam informação por não terem um "ramo curto" equivalente, mas ficariam mais robustos
na mesma limpeza.

---

## A2 — `/perfil/dados` sem limite de tentativas na senha atual (Baixa–Média, CORRIGIDA em 19/09/2026)

**Local:** [`blueprints/usuario_bp.py:456-490`](../blueprints/usuario_bp.py#L456-L490)

```python
@auth_bp.route("/perfil/dados", methods=["POST"])
def atualizar_dados_perfil():
    aluno = _aluno_da_sessao()
    ...
    senha_atual = request.form.get("senha_atual") or ""
    if not aluno.verificar_senha(senha_atual):
        flash('Senha atual incorreta. Nenhum dado foi alterado.', 'erro')
        return redirect('/perfil')
```

As duas rotas irmãs que também exigem a senha atual têm limite explícito:
`/perfil/senha` usa `@limiter.limit('15 per hour', key_func=_chave_da_conta)`
(linha 496) e `/perfil/email` usa `@limiter.limit('10 per hour', key_func=_chave_da_conta)`
(linha 544). `/perfil/dados` não tem decorator nenhum de `limiter`.

**Impacto:** quem já possui uma sessão autenticada válida para a conta (cookie
roubado, dispositivo compartilhado, sessão deixada aberta) mas não sabe a senha pode
tentar `senha_atual` indefinidamente contra esta rota, sem o teto que as rotas
equivalentes aplicam. O custo do hash (scrypt) desacelera cada tentativa, mas não
substitui um limite explícito — é exatamente o raciocínio já usado no resto do projeto
para justificar F3 e os `@limiter.limit` das rotas vizinhas.

**Correção recomendada:** aplicar o mesmo `@limiter.limit('15 per hour', key_func=_chave_da_conta)`
já usado em `/perfil/senha`.

---

## A3 — `/perfil/dados` não valida tamanho de `nome`/`login`/`descricao` (Baixa, CORRIGIDA em 19/09/2026)

**Local:** [`blueprints/usuario_bp.py:456-484`](../blueprints/usuario_bp.py#L456-L484)

O cadastro público (`/cadastrar`) valida explicitamente
`len(login) > 50 or len(nome) > 150 or len(descricao) > 255` (linha 218) antes de
gravar, batendo com as colunas `db.String(50)`, `db.String(150)` e `db.String(255)` de
`modelos/usuario.py`. A edição de perfil (`/perfil/dados`) não repete nenhuma dessas
checagens:

```python
nome = (request.form.get("nome") or "").strip()
login = (request.form.get("login") or "").strip()
...
descricao = (request.form.get("descricao") or "").strip()
...
aluno.nome = nome
aluno.login = login
aluno.telefone = telefone
aluno.descricao = descricao
db.session.commit()          # sem try/except
```

**Impacto:** em PostgreSQL (o banco de produção declarado nos dois relatórios
anteriores), gravar um valor além do limite da coluna `VARCHAR` levanta
`sqlalchemy.exc.DataError`, sem `try/except` ao redor do `commit()`. O resultado é um
erro 500 não tratado para uma ação do próprio aluno autenticado — não é um caminho de
comprometimento, mas contraria o item "Input length limits enforced" do checklist e é
inconsistente com o próprio cadastro, que já faz essa validação.

**Correção recomendada:** repetir a mesma checagem de tamanho usada em `/cadastrar`
antes de atribuir os campos.

---

## A4 — Enumeração de usuário/e-mail no cadastro público (Baixa / informativa, CORRIGIDA em 19/09/2026 para CPF e e-mail)

**Local:** [`blueprints/usuario_bp.py:245-249`](../blueprints/usuario_bp.py#L245-L249)

```python
if Aluno.query.filter_by(login=login).first():
    return render_template("cadastro.html", erro="Erro: Este usuário já está cadastrado!", ...)
if Aluno.query.filter_by(email=email).first():
    return render_template("cadastro.html", erro="Erro: Este e-mail já está cadastrado!", ...)
```

Um visitante sem conta consegue testar nomes de usuário e e-mails e descobrir, pela
mensagem, quais já existem na base. Isso é diferente da checagem por CPF logo acima
(linha 240-243), que devolve a mesma mensagem genérica nos dois casos por desenho — o
próprio código comenta que "CPF já cadastrado nunca devolve o nome, o e-mail nem a
situação de quem está na base" (linha 159-160). O mesmo cuidado não foi estendido a
login/e-mail.

**Impacto:** baixo — não expõe CPF, senha nem dado financeiro, e a rota já tem limite
de `5 per hour` (e `3 per hour` por IP+CPF). É, ainda assim, um canal de enumeração de
e-mails/usuários que o próprio código trata como risco relevante um parágrafo acima.

**Correção recomendada (opcional):** unificar as duas mensagens numa única genérica
("Não foi possível concluir o cadastro com os dados informados"), deixando o aluno
saber que algo colidiu sem dizer qual campo.

---

## Housekeeping: `pip` desatualizado no ambiente virtual local (CORRIGIDO em 19/09/2026: pip 26.2.1)

Identificado em 12/09, ainda presente: `.venv/bin/pip --version` reporta `25.1.1`
(atual: `26.2.1`). É a ferramenta de instalação do ambiente de desenvolvimento, não uma
dependência da aplicação em execução — impacto de segurança direto é baixo — mas como
já tinha sido sinalizado e continua pendente, fica registrado aqui. `pip-audit -r
requirements.txt` (executado agora) **não encontrou vulnerabilidades conhecidas** nas
dependências da aplicação.

---

## Situação dos 15 achados do relatório de 05/09 (revalidados hoje, código lido diretamente)

| ID | Achado original | Verificação feita agora |
|---|---|---|
| F1 | Aluno desviava ficha administrativa de outro aluno | `dao/usuarioDAO.py:154-157` (`buscar_por_cpf`) filtra só por CPF; usado nas 5 rotas de `adm_bp.py`. **Confirmado corrigido.** |
| F2 | CSRF ausente em 46/49 formulários | `CSRFProtect` global em `servidor.py:121`/`config.py:10`; todos os `<form method="POST">` sem token literal incluem `components/csrf_field.html` (verificado nos 6 casos que o grep isolou). **Confirmado corrigido.** |
| F3 | Sem limite de tentativas no login/admin | `@limiter.limit('5 per 15 minutes', ...)` em `/login` (`usuario_bp.py:105-108`). **Confirmado corrigido** (ver A2 para uma lacuna correlata numa rota diferente). |
| F4 | Link de recuperação a partir do `Host` | `servicos/urls.py` monta tudo a partir de `APP_BASE_URL`, validada e nunca do request; `TRUSTED_HOSTS` obrigatório em `servidor.py:71-78`. **Confirmado corrigido.** |
| F5 | Sem limite de tamanho de requisição | `MAX_CONTENT_LENGTH`, `MAX_FORM_MEMORY_SIZE`, `MAX_FORM_PARTS` em `servidor.py:65-67`. **Confirmado corrigido.** |
| F6 | Comprovante PDF servido inline | `usuario_bp.py:1043-1049` usa `CONTENT_TYPE_POR_EXTENSAO` e `as_attachment=(extensao == 'pdf')`. **Confirmado corrigido.** |
| F7 | Nenhum cabeçalho de segurança | `servidor.py:143-162`: CSP com nonce, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`, HSTS condicional. **Confirmado corrigido** (e mais completo que a correção original sugerida — CSP não usa mais `unsafe-inline` em script). |
| F8 | Login aceitava `nome` (não único) | `dao/usuarioDAO.py:106-117` (`autenticar`) usa só `login`, `email`, `cpf`. **Confirmado corrigido.** |
| F9 | `ProxyFix` ausente | `servidor.py:81-93`, condicionado a `TRUST_PROXY_COUNT`. **Confirmado corrigido.** |
| F10 | Redirect aberto via `Referer` no Pix | `blueprints/pix_bp.py` não usa mais `request.referrer` em nenhum ponto — todos os redirects são para destinos fixos. **Confirmado corrigido.** |
| F11 | `/logout` aceitava GET | `servidor.py:227` — só `POST`. **Confirmado corrigido.** |
| F12 | Enumeração por tempo no login | `dao/usuarioDAO.py:119-121` compara contra `_HASH_DESCARTAVEL` quando a conta não existe. **Confirmado corrigido** (mas ver A1 para o mesmo problema em outra rota, ainda aberto). |
| F13 | Senha mínima de 6, sem outros critérios | `servicos/senhas.py`: mínimo 8, lista de senhas comuns, veto a repetir usuário/e-mail/CPF; aplicado também no cadastro (`usuario_bp.py:221`). **Confirmado corrigido.** |
| F14 | Webhook sem checar recência do `ts` | `servicos/mercado_pago.py:399-434` (`validar_assinatura_webhook`) recusa `ts` fora de `tolerancia_segundos=300`. **Confirmado corrigido.** |
| F15 | Curinga de `LIKE` sem escape | `dao/financeiroDAO.py:1017-1018` e `dao/usuarioDAO.py:63-64` escapam `%`, `_`, `\`. **Confirmado corrigido.** |

---

## Verificado e correto (confirmado nesta análise, não apenas herdado do relatório anterior)

- **Injeção de SQL:** nenhuma ocorrência de `text()`/`.execute()` com string interpolada
  fora de testes e migrations (que não recebem entrada de usuário). Todo acesso a dados
  passa pelo ORM parametrizado.
- **XSS:** nenhuma ocorrência de `|safe`, `Markup(`, `render_template_string`,
  `innerHTML`, `document.write` ou `eval` em `templates/` ou `static/js/`. O novo campo
  `dados.*` (repopulação do formulário de cadastro, código ainda não commitado) é
  interpolado com `{{ }}` normal — o autoescape do Jinja cobre o contexto de atributo
  HTML (`value="{{ dados.nome }}"`), então não introduz XSS refletido.
  <br>Recomendação de código, não de segurança: mover `dados_formulario` para um
  `dataclass`/`TypedDict` deixaria explícito quais chaves o template espera, mas isso é
  estilo, não uma falha.
- **Uploads:** validação por conteúdo real (`Pillow.verify()` + regravação da imagem),
  nunca por extensão/Content-Type do navegador; nomes gerados por UUID; limite de
  pixels calibrado à memória do container (`servicos/armazenamento.py`).
- **Pagamentos (Pix e Checkout Pro):** valor sempre lido do banco, nunca do formulário
  ou da URL de retorno (`checkout_bp.py:138-139`, `pix_bp.py:222-229`); webhook
  reconcilia `external_reference`, `currency_id` e `transaction_amount` contra o que
  está persistido antes de dar baixa (`pix_bp.py:399-435`); nunca confia no corpo do
  webhook, sempre reconsulta a API do Mercado Pago.
- **Posse de recursos (IDOR):** `_acesso_permitido` (`pix_bp.py`, `checkout_bp.py`),
  `_pagamento_com_acesso_ou_404` e `_pode_ver_foto` (`usuario_bp.py`) checam
  `aluno.id == pagamento.aluno_id`/`aluno_id` em toda rota financeira e de foto,
  revalidando a sessão no banco a cada requisição via `servicos/autorizacao.py`.
- **Segredos:** `.env` fora do controle de versão; nenhuma chave em `dao/`,
  `blueprints/`, `servicos/`, `modelos/`; `ADMIN_PASSWORD_HASH` é hash (não senha em
  texto puro) desde a última correção — reforça F3 além do que o relatório original
  pedia.
- **Dependências:** `pip-audit -r requirements.txt` sem vulnerabilidades conhecidas
  nesta execução.

---

## Ordem de correção sugerida (executada em 19/09/2026, ver a seção de atualização)

1. **A1** — mover `/recuperar_senha` (e, por consistência, `/cadastrar` e
   `/ativar-acesso`) para `fila_email.enfileirar`, igualando o tempo de resposta.
2. **A2** — copiar o `@limiter.limit` de `/perfil/senha` para `/perfil/dados`.
3. **A3** — repetir a validação de tamanho do `/cadastrar` em `/perfil/dados`.
4. **A4** — opcional; só vale a pena se a equipe decidir que enumeração de login/e-mail
   é um risco a fechar agora.
