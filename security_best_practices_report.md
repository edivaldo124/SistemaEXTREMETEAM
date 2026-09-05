# Relatório de segurança — Sistema Extreme Team

**Data:** 05/09/2026
**Escopo:** aplicação Flask completa (autenticação, autorização, acesso a dados, injeção, XSS, CSRF, uploads, segredos)
**Stack na análise original:** Python 3.11 · Flask 3.1.0 · Werkzeug 3.1.8 · SQLAlchemy 2.0.36 · Jinja2 3.1.6 · PostgreSQL · JavaScript sem framework
**Referências aplicadas:** `python-flask-web-server-security.md`, `javascript-general-web-frontend-security.md`

> Condição da análise original: nenhum arquivo foi alterado, nenhum valor de segredo foi lido ou exibido e nenhum teste foi disparado contra serviços externos (Mercado Pago, Brevo).

## Atualização após as correções

As seções detalhadas abaixo preservam a análise original e descrevem o estado anterior do código. Em 05/09/2026, as correções foram implementadas e validadas localmente sem acessar dados de produção nem chamar Mercado Pago ou Brevo.

| ID | Estado atual | Correção e evidência |
|---|---|---|
| F1 | Corrigido | Rotas administrativas buscam somente por CPF e usam as variantes formatada e numérica. Teste de regressão cobre consulta, edição, foto, cobrança e pagamento diante de colisões em nome e observações. |
| F2 | Corrigido | `CSRFProtect` foi ativado globalmente. Os 52 formulários POST enviam token, as requisições JavaScript usam `X-CSRFToken` e somente o webhook assinado possui exceção específica. |
| F3 | Corrigido | Login, recuperação e cadastro possuem limites. As chaves combinam IP e identificador com hash; o Docker Compose usa Redis compartilhado. |
| F4 | Corrigido | Links externos usam exclusivamente `APP_BASE_URL`; `TRUSTED_HOSTS` valida o host recebido. Host manipulável não participa da URL enviada. |
| F5 | Corrigido | Flask limita corpo a 10 MB, campos multipart a 512 KB e formulários a 100 partes. O Caddy também limita o corpo a 10 MB. |
| F6 | Corrigido | PDFs de comprovante usam tipo fixo e `Content-Disposition: attachment`. |
| F7 | Corrigido | Respostas incluem CSP com nonce, bloqueio de handlers inline, `nosniff`, proteção contra iframe, política de referência e permissões restritas. |
| F8 | Corrigido | Nome foi removido dos identificadores de login. Permanecem login, e-mail e CPF, que são únicos. |
| F9 | Corrigido por configuração | `ProxyFix` só é ativado por `TRUST_PROXY_COUNT`; o Compose informa exatamente um proxy, o Caddy. Outros ambientes precisam informar sua própria topologia. |
| F10 | Corrigido | Redirecionamentos após ações administrativas usam destino interno fixo. |
| F11 | Corrigido | Logout aceita somente POST, possui CSRF e continua usando confirmação visual. |
| F12 | Corrigido | Contas inexistentes executam uma verificação de hash descartável para reduzir diferença observável de tempo. |
| F13 | Corrigido | Senhas novas exigem no mínimo oito caracteres e recusam opções comuns ou iguais aos identificadores da conta. |
| F14 | Corrigido | Assinaturas de webhook fora da janela de cinco minutos são recusadas; segundos e milissegundos são aceitos. |
| F15 | Corrigido | `%`, `_` e `\\` são escapados no filtro `ILIKE` e passam a ser tratados como texto. |

Validação executada:

- `pytest -q`: **199 testes aprovados**.
- `pip-audit -r requirements.txt`: **nenhuma vulnerabilidade conhecida encontrada** após atualizar Flask para 3.1.3, Pillow para 12.3.0 e python-dotenv para 1.2.2.
- `pip check`: nenhuma dependência quebrada.
- `compileall`: módulos Python compilados sem erro.
- `docker compose config --quiet`: configuração válida.
- Verificação estrutural: 52 formulários POST e 52 inclusões do campo CSRF; nenhum handler HTML `onclick`, `onchange`, `onsubmit`, `onload` ou `onerror` permaneceu.

Pendências de implantação: confirmar volume persistente de uploads e os valores efetivos de `COOKIE_SECURE`, `TRUSTED_HOSTS`, `TRUST_PROXY_COUNT`, `APP_BASE_URL` e `RATELIMIT_STORAGE_URI` no ambiente publicado. Essas verificações dependem da infraestrutura e não podem ser concluídas pela análise local.

---

## Sumário executivo

O projeto tem uma base de segurança **melhor que a média** para o seu porte. Vários pontos que costumam falhar foram verificados: não foram encontrados caminhos de injeção SQL ou XSS na análise realizada; os uploads são validados por conteúdo; a recuperação de senha usa token com hash e expiração; o webhook do Mercado Pago valida assinatura HMAC e não confia no corpo recebido; e não foi encontrado segredo versionado.

Os problemas se concentram em **três frentes**:

1. **Confusão de registro na área administrativa** (F1). Um aluno comum consegue fazer o painel do administrador abrir e alterar a ficha errada, incluindo lançamento de mensalidades. É o achado mais grave e o de correção mais simples.
2. **Ausência de proteções transversais**: CSRF em 46 de 49 formulários, nenhum limite de tentativas de login, nenhum limite de tamanho de requisição, nenhum cabeçalho de segurança.
3. **Confiança no cabeçalho `Host`** para montar o link de recuperação de senha, o que abre caminho para roubo de conta se a aplicação for exposta sem validação de host.

**Contagem original:** 0 críticos · 4 altos · 5 médios · 6 baixos · 3 pontos a verificar em execução. Os 15 achados de código estão corrigidos; permanecem as verificações de implantação descritas acima.

| Severidade | IDs |
|---|---|
| Crítico | — |
| Alto | F1, F2, F3, F4 |
| Médio | F5, F6, F7, F8, F9 |
| Baixo | F10, F11, F12, F13, F14, F15 |
| Verificar em runtime | V1, V2, V3 |

---

## Severidade ALTA

### F1 — Aluno consegue desviar a ficha administrativa de outro aluno
**Status:** Vulnerabilidade **confirmada** (leitura de código; não explorada)
**Gravidade:** Alta
**Local:** [dao/usuarioDAO.py:60-64](dao/usuarioDAO.py#L60-L64), consumida por [adm_bp.py:176](blueprints/adm_bp.py#L176), [226](blueprints/adm_bp.py#L226), [256](blueprints/adm_bp.py#L256), [274](blueprints/adm_bp.py#L274), [577](blueprints/adm_bp.py#L577)

**Evidência**

```python
# dao/usuarioDAO.py:59-64
@staticmethod
def buscar_por_usuario(usuario):
    # Busca o perfil pelo nome, email ou cpf que está salvo na sessão
    return Aluno.query.filter(
        (Aluno.nome == usuario) |(Aluno.login == usuario)| (Aluno.email == usuario) | (Aluno.descricao == usuario)| (Aluno.cpf == usuario)
    ).first()
```

A rota administrativa recebe um CPF, mas a consulta casa contra **cinco** colunas e devolve `.first()` **sem `ORDER BY`**. Duas dessas colunas não têm restrição de unicidade e são editáveis pelo próprio aluno:

```python
# modelos/usuario.py:9,17
nome      = db.Column(db.String(150), nullable=False)   # sem unique
descricao = db.Column(db.String(255), nullable=True)    # sem unique

# blueprints/usuario_bp.py:330,333 — o aluno edita os dois em /perfil/dados
aluno.nome = nome
aluno.descricao = descricao
```

**Impacto**

O aluno A abre "Meus dados" e grava no campo *Observações de saúde* o CPF do aluno B. Quando o administrador clica em "Ver perfil" de B no painel (`/admin/usuario/{{ u.cpf }}`, [pgAdm.html:231](templates/pgAdm.html#L231)), a consulta casa com os dois registros e o banco pode devolver o de A. A partir daí, todas as rotas que reusam essa busca operam no registro errado:

- `POST /admin/usuario/<cpf>` altera dados cadastrais do aluno errado
- `POST /admin/usuario/<cpf>/pagamentos` **lança uma mensalidade paga na conta errada** (fraude financeira: A ganha um plano que B pagou)
- `POST /admin/usuario/<cpf>/foto` e `/foto/remover` trocam a foto do aluno errado
- `POST /admin/usuario/<cpf>/cobrar` envia cobrança ao aluno errado

Não exige privilégio nenhum além de uma conta de aluno aprovada. A não determinação vem do plano de execução do PostgreSQL, então o efeito é intermitente, o que torna o diagnóstico ainda mais difícil para a equipe.

**Correção recomendada**

A rota passa um CPF; a busca deve ser por CPF e nada mais. O helper `variantes_cpf` já existe em `servicos/formatacao.py` para cobrir as duas grafias (com e sem pontuação):

```python
@staticmethod
def buscar_por_cpf(cpf):
    # Busca só pela coluna com restrição de unicidade. Casar contra nome ou
    # descricao permitia que um aluno colidisse de propósito com o CPF de outro.
    return Aluno.query.filter(Aluno.cpf.in_(variantes_cpf(cpf))).first()
```

Trocar as 5 chamadas em `adm_bp.py` para o novo método e remover `buscar_por_usuario`.

**Mitigação imediata (se a correção demorar)**
Remover `Aluno.descricao` e `Aluno.nome` do `OR` já elimina a parte controlável pelo atacante.

---

### F2 — Ausência de proteção CSRF em 46 de 49 formulários
**Status:** Vulnerabilidade **confirmada**, com mitigação parcial relevante
**Gravidade:** Alta (rebaixada na prática por `SameSite=Lax`)
**Local:** todos os `POST` fora de [adm_bp.py:134-138](blueprints/adm_bp.py#L134-L138) e [adm_bp.py:504-507](blueprints/adm_bp.py#L504-L507)

**Evidência**

A aplicação autentica por cookie de sessão. Apenas 3 dos 49 formulários carregam token anti-CSRF:

| Ação protegida | Token |
|---|---|
| `POST /admin/remover/<aluno_id>` | `token_exclusao` |
| `POST /admin/avisos` | `token_aviso` |
| `POST /admin/avisos/cobranca` | `token_aviso` |

Os tokens existentes estão **bem implementados** (presos à sessão, comparados com `hmac.compare_digest`, rotacionados após uso). O problema é a cobertura. Ficam sem token, entre outros:

- `POST /perfil/dados`, `/perfil/senha`, `/perfil/email` (troca de senha e de e-mail)
- `POST /perfil` (contratação e troca de plano)
- `POST /admin/aluno/<id>/aprovar|recusar|ativar|desativar`
- `POST /admin/pagamentos/<id>/status` e `/comprovante-manual/aprovar|rejeitar`
- `POST /admin/turmas/cadastrar`, `/admin/professores`
- `POST /api/mensalidades/<id>/pix`

Não há Flask-WTF nem middleware global (`grep -rn "csrf" --include="*.py"` não retorna nada).

**Impacto**

Um site de terceiros consegue disparar ações em nome de um usuário autenticado: trocar a senha de um aluno, aprovar um cadastro, marcar uma mensalidade como paga. A defesa hoje é exclusivamente o `SESSION_COOKIE_SAMESITE='Lax'` de [servidor.py:23](servidor.py#L23), que impede o navegador de anexar o cookie em POST cross-site. Isso cobre navegadores modernos, mas não cobre:

- navegadores antigos sem enforcement de `SameSite`
- ataques a partir de um subdomínio comprometido (mesmo site para efeito de `SameSite`)
- qualquer futura mudança para `SameSite=None`

A referência do Flask é explícita: `SameSite` é defesa em profundidade e não substitui token.

**Correção recomendada**

Adotar `Flask-WTF` com `CSRFProtect(app)`, que protege todos os `POST` de uma vez e expõe `{{ csrf_token() }}` para os templates. Como já existem 49 formulários, a alternativa de menor esforço é um `before_request` global que valide um token de sessão em toda requisição não idempotente, reaproveitando exatamente o padrão já usado no `token_exclusao`.

Para os endpoints JSON (`/api/mensalidades/...`), exigir um cabeçalho customizado (ex.: `X-Requested-With`) é suficiente e barato, já que o `fetch` do próprio front já pode enviá-lo.

---

### F3 — Sem limite de tentativas: força bruta na senha do administrador
**Status:** Vulnerabilidade **confirmada**
**Gravidade:** Alta
**Local:** [blueprints/usuario_bp.py:57-101](blueprints/usuario_bp.py#L57-L101)

**Evidência**

```python
# usuario_bp.py:63-71
admin_user = os.environ.get('ADMIN_USER')
admin_password = os.environ.get('ADMIN_PASSWORD')
if admin_user and admin_password and login == admin_user and hmac.compare_digest(senha, admin_password):
    session.clear()
    session['usuario'] = admin_user
    session['tipo_usuario'] = "admin"
```

Não há contagem de tentativas, atraso progressivo, CAPTCHA ou bloqueio temporário em nenhum ponto da aplicação. Uma varredura por `limiter|ratelimit|tentativas|throttle|lockout` em todo o código Python não retorna nada.

**Impacto**

O administrador é uma **credencial estática única**, sem MFA, sem rotação e sem trilha de auditoria por pessoa. Um atacante pode testar senhas indefinidamente contra `/login`. Acertar essa senha entrega o sistema inteiro: dados pessoais de todos os alunos (nome, CPF, e-mail, telefone, data de nascimento, observações de saúde), o histórico financeiro completo e a capacidade de enviar e-mail em massa em nome da academia.

O mesmo vale para `/recuperar_senha`, que pode ser usado para disparar e-mails em volume.

**Correção recomendada**

1. Limitar tentativas por IP e por login (`Flask-Limiter` é a opção direta): por exemplo 5 tentativas / 15 min em `/login` e 3 / hora em `/recuperar_senha`.
2. Registrar em log as falhas de autenticação de admin (hoje não há log algum de tentativa malsucedida).
3. Migrar o administrador para um registro em banco com senha em hash, permitindo mais de um admin e trilha de auditoria por pessoa. A senha em variável de ambiente é aceitável para um sistema pequeno, mas amarra a rotação a um redeploy.

---

### F4 — Link de recuperação de senha montado a partir do cabeçalho `Host`
**Status:** Vulnerabilidade **confirmada** no código; explorabilidade **depende do deploy**
**Gravidade:** Alta
**Local:** [blueprints/usuario_bp.py:489](blueprints/usuario_bp.py#L489) (também [420](blueprints/usuario_bp.py#L420) e [158](blueprints/usuario_bp.py#L158))

**Evidência**

```python
# usuario_bp.py:489
link_url=url_for('auth.redefinir_senha', token=token, _external=True),
```

`_external=True` monta a URL absoluta a partir do `Host` da requisição, porque **não há `SERVER_NAME` nem `TRUSTED_HOSTS` configurados** (confirmado: nenhuma ocorrência em `servidor.py` ou `config.py`). A aplicação já tem a variável `APP_BASE_URL` no `.env`, mas ela só é usada em [servicos/mercado_pago.py:95](servicos/mercado_pago.py#L95), não nos e-mails.

**Impacto**

Um atacante envia `POST /recuperar_senha` com o CPF e e-mail da vítima e o cabeçalho `Host: atacante.com`. A vítima recebe, no seu próprio e-mail, uma mensagem legítima da Extreme Team contendo `https://atacante.com/recuperar_senha/<token>`. Ao clicar, o token de redefinição vai para o servidor do atacante, que o usa em seguida no domínio real. **Isso é tomada de conta completa**, e o mesmo caminho serve para o token de confirmação de troca de e-mail (linha 420).

**Nota honesta sobre explorabilidade:** o [Caddyfile:9](Caddyfile#L9) declara um bloco de site para hosts nomeados (`localhost, 127.0.0.1, 10.0.0.105`), e o Caddy recusa `Host` desconhecido. **Nesse deploy específico, o ataque é bloqueado no proxy.** O risco é real para o cenário de deploy documentado no README (Render, com Gunicorn recebendo direto do proxy da plataforma) e para qualquer futura mudança no Caddyfile. É uma defesa que hoje mora inteiramente na infraestrutura, não no código.

**Correção recomendada**

Montar os links de e-mail a partir de `APP_BASE_URL`, que é uma configuração do servidor e não um dado da requisição:

```python
base = (os.environ.get('APP_BASE_URL') or '').rstrip('/')
link_url = f"{base}{url_for('auth.redefinir_senha', token=token)}"
```

E, como defesa em profundidade, definir `TRUSTED_HOSTS` em produção.

---

## Severidade MÉDIA

### F5 — Sem limite de tamanho de requisição: negação de serviço por memória
**Status:** Vulnerabilidade **confirmada**
**Gravidade:** Média
**Local:** [servidor.py:20-26](servidor.py#L20-L26) (ausência), [usuario_bp.py:592](blueprints/usuario_bp.py#L592), [usuario_bp.py:717](blueprints/usuario_bp.py#L717), [adm_bp.py:237](blueprints/adm_bp.py#L237)

**Evidência**

`MAX_CONTENT_LENGTH`, `MAX_FORM_MEMORY_SIZE` e `MAX_FORM_PARTS` não estão definidos em lugar nenhum. O [Caddyfile](Caddyfile) também não define `request_body max_size`. Os três handlers de upload leem o corpo inteiro para a memória **antes** de conferir o tamanho:

```python
# usuario_bp.py:592
nome_arquivo = salvar_foto_perfil(arquivo.read())   # lê tudo primeiro

# servicos/armazenamento.py:71 — o limite só é checado depois
if len(conteudo) > TAMANHO_MAX_FOTO:
    raise ArquivoInvalido('A imagem deve ter no máximo 5 MB.')
```

**Impacto**

Um aluno autenticado envia um arquivo de vários GB. O Gunicorn roda com `--workers 1 --threads 2` ([Dockerfile:39](Dockerfile#L39)), então poucas requisições simultâneas esgotam a memória do container e derrubam o sistema para todo mundo. O limite de 5 MB documentado na interface não é aplicado antes da alocação.

**Correção recomendada**

```python
app.config.update(
    MAX_CONTENT_LENGTH=10 * 1024 * 1024,   # teto global, acima do maior upload (8 MB)
    MAX_FORM_MEMORY_SIZE=512 * 1024,       # campos de texto de formulário
)
```

O Flask passa a rejeitar com `413` antes de bufferizar. Vale acrescentar `request_body { max_size 10MB }` no Caddyfile como segunda barreira, e um `errorhandler(413)` para exibir a mensagem em português já usada nos formulários.

---

### F6 — Comprovante em PDF servido inline
**Status:** Vulnerabilidade **confirmada** (risco moderado)
**Gravidade:** Média
**Local:** [blueprints/usuario_bp.py:744](blueprints/usuario_bp.py#L744)

**Evidência**

```python
return send_file(caminho, max_age=0, as_attachment=False)
```

Diferente da foto de perfil ([linha 577](blueprints/usuario_bp.py#L577)), que fixa `mimetype='image/jpeg'`, aqui o tipo é adivinhado pela extensão e o arquivo é renderizado **dentro da página**. PDFs são aceitos sem reprocessamento — e corretamente, já que reprocessar PDF é arriscado — mas apenas com checagem da assinatura binária:

```python
# servicos/armazenamento.py:109-110
if conteudo[:5] == b'%PDF-':
    extensao = 'pdf'
```

Um arquivo pode começar com `%PDF-` e conter qualquer coisa depois.

Observação: o módulo já define `CONTENT_TYPE_POR_EXTENSAO` ([armazenamento.py:25-30](servicos/armazenamento.py#L25-L30)) com o mapa correto, mas **essa constante nunca é usada em lugar nenhum** — sinal de que a intenção de fixar o Content-Type existia e ficou pelo caminho.

**Impacto**

Um aluno envia um PDF malicioso como comprovante. O administrador o abre no navegador, na origem da aplicação. PDFs suportam JavaScript e ações de formulário; o visualizador embutido do navegador é sandboxed, mas o vetor é real para phishing convincente (o documento aparece sob o domínio legítimo) e para exploração de falhas do próprio visualizador. Sem `X-Content-Type-Options: nosniff` (ver F7), há também espaço para sniffing de conteúdo.

**Correção recomendada**

Usar a constante que já existe e forçar download para PDF:

```python
extensao = caminho.rsplit('.', 1)[-1].lower()
content_type = CONTENT_TYPE_POR_EXTENSAO.get(extensao, 'application/octet-stream')
# PDF é formato ativo: entregar como anexo em vez de renderizar na nossa origem.
return send_file(
    caminho, mimetype=content_type, max_age=0,
    as_attachment=(extensao == 'pdf'),
    download_name=f'comprovante-{pagamento.id}.{extensao}',
)
```

Isso muda o comportamento do botão "Ver arquivo enviado" para PDFs (baixa em vez de abrir). Vale combinar com a equipe antes de aplicar.

---

### F7 — Nenhum cabeçalho de segurança HTTP
**Status:** **Confirmado** (ausência total, app e proxy)
**Gravidade:** Média
**Local:** [servidor.py](servidor.py) (sem `after_request`), [Caddyfile](Caddyfile) (sem bloco `header`)

**Evidência**

Busca por `after_request`, `Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options` e `Talisman` em todo o código Python: nenhuma ocorrência. O Caddyfile tem apenas `reverse_proxy` e o redirecionamento de porta 80.

**Impacto**

- Sem `Content-Security-Policy`: qualquer XSS futuro tem execução irrestrita. Hoje não há XSS (verificado, ver seção "Verificado e correto"), mas o CSP é a rede de proteção para quando um for introduzido.
- Sem `X-Frame-Options` / `frame-ancestors`: a aplicação pode ser embutida em iframe por terceiros (clickjacking). Ações destrutivas de admin em um clique são alvo natural.
- Sem `X-Content-Type-Options: nosniff`: navegadores podem inferir tipo de conteúdo, o que interage mal com F6.

**Correção recomendada**

Um `after_request` central em `servidor.py`. O CSP precisa liberar `fonts.googleapis.com` e `fonts.gstatic.com` (usados em `theme.css`) e `unsafe-inline` para estilo, já que há `<style>`/atributos inline no template de e-mail e scripts inline em `admin_avisos.html` e `dt_aluno.html`:

```python
@app.after_request
def cabecalhos_de_seguranca(resposta):
    resposta.headers.setdefault('X-Content-Type-Options', 'nosniff')
    resposta.headers.setdefault('X-Frame-Options', 'SAMEORIGIN')
    resposta.headers.setdefault('Referrer-Policy', 'same-origin')
    resposta.headers.setdefault('Content-Security-Policy', (
        "default-src 'self'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data:; "
        "script-src 'self' 'unsafe-inline'; "
        "frame-ancestors 'self'; base-uri 'self'; form-action 'self'"
    ))
    return resposta
```

Passo seguinte recomendado: mover os dois scripts inline para arquivos `.js` e remover `'unsafe-inline'` de `script-src`, que é o que dá valor real ao CSP.

---

### F8 — Autenticação aceita campo não único e editável pelo usuário
**Status:** Vulnerabilidade **confirmada** (impacto de disponibilidade)
**Gravidade:** Média
**Local:** [dao/usuarioDAO.py:41-53](dao/usuarioDAO.py#L41-L53)

**Evidência**

```python
aluno = Aluno.query.filter(
    (Aluno.nome == usuario) |      # <- sem unique, editável pelo aluno
    (Aluno.login == usuario) |
    (Aluno.email == usuario) |
    (Aluno.cpf.in_(cpfs_possiveis))
).first()
```

`nome` não tem restrição de unicidade ([modelos/usuario.py:9](modelos/usuario.py#L9)) e é editável em `/perfil/dados`.

**Impacto**

Não permite tomada de conta: o atacante ainda precisa da senha da vítima. Mas o aluno A pode alterar o próprio `nome` para o `login` da vítima B. A partir daí, o `.first()` sem ordenação pode devolver o registro de A quando B tenta entrar, e a autenticação de B **falha com a senha correta** — negação de serviço direcionada e muito difícil de diagnosticar pelo suporte.

**Correção recomendada**

Autenticar apenas por identificadores únicos (`login`, `email`, `cpf`) e remover `Aluno.nome` do `OR`. Se o login por nome for um requisito de produto, então `nome` precisa de restrição `unique` no banco e validação no cadastro.

---

### F9 — Confiança em proxy não configurada
**Status:** **Suspeita** — depende do deploy
**Gravidade:** Média
**Local:** [servidor.py](servidor.py) (sem `ProxyFix`), [Caddyfile:11](Caddyfile#L11)

**Evidência**

A aplicação roda atrás do Caddy (`reverse_proxy app:5000`), mas `ProxyFix` do Werkzeug não é aplicado e `TRUSTED_HOSTS` não é definido.

**Impacto**

`request.scheme` vê `http` mesmo quando o cliente usou HTTPS, o que pode gerar links `http://` em e-mails (interagindo com F4) e afeta qualquer lógica futura baseada em `request.remote_addr` — inclusive o rate limiting recomendado em F3, que sem `ProxyFix` limitaria pelo IP do proxy e não pelo IP real do cliente, tornando o controle inútil ou bloqueando todo mundo de uma vez.

**Correção recomendada**

```python
from werkzeug.middleware.proxy_fix import ProxyFix
# 1 proxy à frente (Caddy). Contar errado permitiria forjar X-Forwarded-For.
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
```

Aplicar **junto** com `TRUSTED_HOSTS`, nunca isolado: confiar em `X-Forwarded-Host` sem validar host é trocar um problema por outro.

---

## Severidade BAIXA

### F10 — Redirecionamento aberto via `Referer`
**Status:** **Confirmado**
**Local:** [blueprints/pix_bp.py:278](blueprints/pix_bp.py#L278), [284](blueprints/pix_bp.py#L284), [288](blueprints/pix_bp.py#L288), [297](blueprints/pix_bp.py#L297)

```python
return redirect(request.referrer or '/admin/financeiro')
```

`request.referrer` vem do cabeçalho `Referer`, controlado pelo cliente. Explorabilidade é baixa (rota `POST`, exige sessão de admin, e o `SameSite=Lax` dificulta o disparo cross-site), mas é um redirecionamento não validado. **Correção:** validar que o destino é relativo, ou usar `url_for('admin_blueprint.painel_financeiro')` como destino fixo.

### F11 — `/logout` aceita GET
**Status:** **Confirmado**
**Local:** [servidor.py:64-67](servidor.py#L64-L67)

Ação que altera estado (limpa a sessão) exposta em `GET`. Qualquer página consegue deslogar o usuário com `<img src="https://.../logout">`. Impacto é apenas incômodo. **Correção:** aceitar somente `POST` e usar um formulário nos templates. Os três links de logout já passam pelo modal de confirmação, então a mudança é pequena.

### F12 — Enumeração de usuários por tempo de resposta
**Status:** **Confirmado**
**Local:** [dao/usuarioDAO.py:51](dao/usuarioDAO.py#L51), [dao/professorDAO.py:24](dao/professorDAO.py#L24)

```python
if aluno and aluno.verificar_senha(senha):
```

Quando o login não existe, `verificar_senha` (scrypt, deliberadamente lento) não é executado, e a resposta volta muito mais rápido. Isso permite descobrir quais logins/e-mails/CPFs existem na base. Note que o fluxo de **recuperação de senha já trata isso corretamente** ([usuario_bp.py:473-474](blueprints/usuario_bp.py#L473-L474), com resposta idêntica nos dois casos) — a inconsistência está só no login. **Correção:** comparar contra um hash descartável quando o usuário não existir, para igualar o tempo.

### F13 — Senha mínima de 6 caracteres, sem outros critérios
**Status:** **Confirmado** (decisão de produto)
**Local:** [blueprints/usuario_bp.py:357](blueprints/usuario_bp.py#L357), [514](blueprints/usuario_bp.py#L514)

Não há verificação de comprimento no **cadastro** ([linha 116](blueprints/usuario_bp.py#L116) checa apenas se não está vazia), só na troca e na redefinição. Combinado com F3 (sem limite de tentativas), senhas fracas ficam viáveis de adivinhar. **Correção:** mínimo de 8 caracteres, aplicado também no cadastro, e checagem contra uma lista de senhas comuns.

### F14 — Webhook sem verificação de recência do timestamp
**Status:** **Confirmado** (impacto residual)
**Local:** [servicos/mercado_pago.py:395-406](servicos/mercado_pago.py#L395-L406)

O `ts` da assinatura entra no manifesto HMAC mas **nunca é comparado com a hora atual**, então uma notificação capturada continua válida para sempre. O impacto é pequeno porque `_processar_status_mp` reconsulta a API do Mercado Pago e é idempotente ([pix_bp.py:326-327](blueprints/pix_bp.py#L326-L327)) — o replay não consegue forçar uma aprovação falsa. **Correção:** rejeitar assinaturas com `ts` mais antigo que ~5 minutos.

### F15 — Curinga de `LIKE` no filtro do financeiro
**Status:** **Confirmado** — e **não é injeção SQL**
**Local:** [dao/financeiroDAO.py:900](dao/financeiroDAO.py#L900)

```python
consulta = consulta.filter(Aluno.nome.ilike(f'%{busca_aluno}%'))
```

A f-string monta o **padrão**, não o SQL: o SQLAlchemy parametriza o valor normalmente. Um administrador que digite `%` ou `_` obtém comportamento de curinga, e um padrão patológico pode ficar lento numa base grande. É higiene, não vulnerabilidade. **Correção (opcional):** escapar `%`, `_` e `\` e usar `ilike(padrao, escape='\\')`.

---

## Verificado e correto

Estes pontos foram auditados especificamente e **não** apresentaram problema. Registro-os porque são exatamente onde este tipo de aplicação costuma falhar:

| Área | Constatação |
|---|---|
| **Injeção SQL** | Não encontrada na análise realizada. Tudo passa pelo ORM parametrizado; não foi encontrado `text()`, `execute()` com string ou concatenação de SQL em `dao/`, `blueprints/`, `servicos/` ou `modelos/`. |
| **XSS em templates** | Não encontrada na análise realizada. Não houve ocorrência de `\|safe`, `Markup(` ou `render_template_string`; o autoescape do Jinja está ativo e os atributos com expressão estão entre aspas. |
| **XSS no DOM** | Não encontrada na análise realizada. Não houve `innerHTML`, `document.write`, `eval` ou `new Function`; o texto dinâmico usa `textContent`. |
| **Cobertura de autorização** | Auditado por AST rota a rota: **todas** as 44 rotas autenticadas verificam sessão. As 5 sem checagem são as públicas por definição (login, cadastro, recuperação, redefinição) e o webhook (que valida HMAC). |
| **Acesso a dados de outros usuários (IDOR)** | Verificações de posse consistentes e corretas: `pagamento.aluno_id != aluno.id` → 404; `solicitacao.aluno_id != aluno.id` → 404; `_pode_ver_foto` cobre inclusive o caso do professor, restringindo-o aos alunos das próprias turmas. **A exceção é F1**, que não é IDOR de sessão e sim colisão de consulta. |
| **Uploads** | Validação por **conteúdo**, não por extensão: `Pillow.verify()` e regravação completa da imagem, descartando EXIF e qualquer payload embutido. Nome de arquivo gerado por UUID no servidor (o nome enviado nunca é usado). Armazenamento fora de `static/`, servido por rota autenticada. `caminho_arquivo` bloqueia `/`, `\` e `..`. Ressalvas em F5 e F6. |
| **Path traversal** | Não encontrado na análise realizada. Nenhum `send_file` recebe caminho controlado diretamente pelo usuário. |
| **Segredos** | `.env` está no `.gitignore` e **nunca esteve no histórico do Git** (verificado com `git log --all`). `.env.example` só tem placeholders. O `compose.yaml` usa `${VAR:?}`, falhando cedo se faltar. Segredos de teste em `conftest.py` estão claramente rotulados como falsos. |
| **Hash de senha** | `werkzeug.security.generate_password_hash` (scrypt por padrão no Werkzeug 3.x), com salt automático. |
| **Fixação de sessão** | `session.clear()` antes de popular a sessão nos três caminhos de login ([usuario_bp.py:67](blueprints/usuario_bp.py#L67), [75](blueprints/usuario_bp.py#L75), [91](blueprints/usuario_bp.py#L91)). |
| **Conteúdo da sessão** | Somente identificadores (`login`, `id`, `tipo_usuario`, tokens anti-CSRF). Nenhum segredo no cookie assinado. |
| **Recuperação de senha** | Token de 32 bytes de `secrets`, **guardado como SHA-256**, uso único, expiração de 30 min, comparação com `hmac.compare_digest`, resposta idêntica para conta existente ou não. Ressalva apenas em F4. |
| **Webhook Mercado Pago** | Assinatura HMAC-SHA256 validada com `compare_digest`; **nunca confia no corpo recebido**, sempre reconsulta a API; idempotente para notificações repetidas. Ressalva apenas em F14. |
| **Cookies de sessão** | `HttpOnly=True`, `SameSite='Lax'`, `Secure` controlado por `COOKIE_SECURE` (padrão desligado para desenvolvimento em HTTP, ligado no `.env` de produção) — exatamente o padrão recomendado. Sessão de 30 min com renovação. |
| **Debug / servidor de desenvolvimento** | `app.run()` está sob `if __name__ == '__main__'`; o container usa Gunicorn ([Dockerfile:39](Dockerfile#L39)). Nenhum `debug=True` no código. |
| **CORS** | Não habilitado — correto, já que não há consumo cross-origin. |
| **Container** | Imagem multi-stage, roda como usuário não-root (`academia`), sem pacotes de build na imagem final. |

---

## A verificar em execução

Pontos que a análise estática não fecha sozinha:

- **V1 — Volume de uploads em produção.** `UPLOAD_DIR` precisa apontar para volume persistente e **fora** de qualquer raiz servida estaticamente. O `compose.yaml` faz isso; confirmar que o deploy no Render também faz, ou os comprovantes se perdem a cada publicação.
- **V2 — `COOKIE_SECURE` em produção.** O `.env` local define `COOKIE_SECURE` duas vezes, com valores diferentes (`false` e depois `true`). O último vence, mas a duplicidade é frágil. Confirmar o valor efetivo no ambiente publicado.
- **V3 — Higiene de dependências.** As versões estão atuais (Flask 3.1.0, Werkzeug 3.1.8, Jinja2 3.1.6, Pillow 11.1.0). Não afirmo CVE específica sem consultar um banco de avisos. Recomendo `pip-audit` no CI: **Pillow é a dependência mais sensível aqui**, porque processa imagens enviadas por usuários não confiáveis.

---

## Ordem de correção sugerida

1. **F1** — uma linha de consulta; corrige fraude financeira e confusão de cadastro.
2. **F3** — rate limiting; a credencial única de admin está exposta a força bruta hoje.
3. **F5** e **F7** — configuração central, sem risco de regressão, alta relação benefício/esforço.
4. **F4** — trocar 3 chamadas `_external=True` por `APP_BASE_URL`.
5. **F2** — o maior esforço (49 formulários); vale planejar com `Flask-WTF`.
6. **F8**, **F6**, **F9** e os itens de severidade baixa.

Antes de aplicar F2 e F6, vale alinhar com a equipe: são as duas mudanças com potencial de afetar fluxos existentes (todo formulário precisa passar a enviar token; o botão de comprovante PDF passa a baixar em vez de abrir).
