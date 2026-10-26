# Relatório de segurança — Sistema Extreme Team

**Última atualização:** 23/10/2026 (fechados os abertos SEC-27, SEC-29 e SEC-30, Pillow 13 do
SEC-20 e os novos SEC-33, SEC-34 e SEC-35; em 22/10, SEC-31 e SEC-32: login com Google sem conta de
acesso e CPF guardado no aparelho; antes, SEC-28: comprovante sem metadados da câmera), sobre a rodada de
20/10/2026 (hero 3D da home, revisão OWASP Top 10:2025 +
DevSecOps e dependências)
**Escopo da rodada de 20/10/2026:** o código que entrou depois de 04/10 (uploads no Supabase
Storage, planilha econômica, login com Google, ajustes da Vercel), a superfície nova do front
(hero cinematográfico e a cena 3D em `front/`), cadeia de dependências (`pip-audit`, `npm
audit`, lock com hashes) e as categorias do OWASP Top 10:2025 menos cobertas antes (A03
cadeia de suprimentos, A09 logs, A10 condições excepcionais), com o checklist DevSecOps
Flask/PostgreSQL/Docker/Vercel.
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

## Situação atual (20/10/2026 — hero 3D, OWASP/DevSecOps e dependências)

**Corrigidos nesta rodada:** 8 achados novos (SEC-20 a SEC-26 e, em 21/10, o SEC-28) e o
SEC-18, que estava aberto desde 04/10. **Abertos, todos dependentes de decisão ou configuração
do dono:** 3 (SEC-27, SEC-29 e SEC-30). Nenhum achado crítico ou alto: o mais sério (SEC-20) exigia uma conta de aluno
aprovada e derrubava só a instância que recebeu o arquivo.

### O que foi feito nesta rodada

**Front-end** (pedido do dono: "melhorar todo o sistema, principalmente o front", com as skills
de vídeo na rolagem, 3D em React, OWASP e DevSecOps):

- **Hero cinematográfico da home** (padrão Framerate): pista de 400svh com quatro manchetes que
  trocam com a rolagem, medidor de 00 a 100, loader só na primeira visita da aba e seta para os
  planos. Os textos ficam no HTML (SEO e leitor de tela; um único `<h1>`). Arquivos:
  `templates/index.html`, `static/js/cinema.js`, `static/css/cinema.css`. O hero antigo saiu
  (216 linhas de CSS apagadas de `index.css` e `.hero` tirado do `theme.css`).
- **Cena 3D (nível 2)**: núcleo de metal dourado líquido com brasas, ilha React Three Fiber em
  `front/`, compilada pelo Vite para `static/dist/cinema` (316 KB gzip). É baixada só depois
  que a página carregou e nunca com "reduzir movimento", economia de dados, conexão 2G,
  aparelho com menos de 4 GB ou sem GPU; nesses casos fica um pôster de 32 KB (20 KB no
  celular). Fora da tela, a cena para de desenhar.
- **Vídeo opcional**: um MP4 em `static/video/cinema.mp4` substitui a cena e avança com a
  rolagem (scrolly-video). Testado com um vídeo sintético (os quadros mudam com a rolagem, sem
  erro de console nem de CSP) e removido depois.
- **3D nível 1 no sistema**: tilt em CSS (`.et-tilt`) nos cartões de plano (home e área do
  aluno), de métrica (painéis do admin) e do método; só com mouse e sem "reduzir movimento".
- **Fontes servidas pelo próprio site** (SEC-18, abaixo).
- Conferência no navegador (GPU real): 1440×900 e 390×844, nos progressos 0, 30, 55, 85 e 100%,
  com movimento reduzido e sem JS; sem rolagem lateral, sem erro de console, cena pronta em
  0,7–1,2 s. `DESIGN.md` e `README.md` registram a exceção da ilha React e o movimento do hero.

**Segurança**: tabela abaixo. Também foram corrigidas 13 falhas antigas dos testes de JS
(`tests/js/botao_ocupado.test.cjs` e `tests/js/pagamento_polling.test.cjs`): o DOM falso não
tinha `classList.replace`, que o `pix.js` passou a usar. Era dívida de teste, não bug.

| ID | Achado | Severidade | Status | Evidência |
|---|---|---|---|---|
| SEC-20 | Pillow 12.3.0 com 8 CVEs. Uma alcançável: o `Image.open()` do upload tentava **todos** os formatos antes de recusar, então um GIF de ~60 bytes (CVE-2026-112400) enviado como foto ou comprovante por qualquer aluno aprovado fazia o Pillow pedir gigabytes de memória e derrubava a instância (A03 + A06, negação de serviço). As outras 7 estão em código que o sistema não usa (append em PDF, `ImageMorph`, salvar TIFF, EPS) ou em formatos recusados antes de decodificar | Média | **Corrigido** (mitigado em 20/10; Pillow 13.0.0 aplicado em 23/10) | [armazenamento.py:81](../servicos/armazenamento.py#L81): `_FORMATOS_ACEITOS = ('JPEG', 'PNG', 'WEBP')`, passado como `formats=` nos três `Image.open` ([203](../servicos/armazenamento.py#L203), [207](../servicos/armazenamento.py#L207), [231](../servicos/armazenamento.py#L231)). GIF, TIFF, EPS e PPM nunca chegam a um parser, e a próxima falha desses decodificadores também fica fora de alcance. Em 23/10 entrou o Pillow 13.0.0, que corrige as 8 ([requirements.lock:611](../requirements.lock#L611)): os 46 testes de imagem e a suíte inteira passam, e o lock instala com `--require-hashes` no Python 3.11 do Dockerfile. Testes: `tests/test_formatos_de_imagem.py` (8; falham se o parser de GIF ou TIFF rodar). |
| SEC-21 | `certifi` 2026.7.22 confiava na raiz `emSign ECC Root CA - G3`, cujos intermediários tiveram chave privada comprometida (PYSEC-2026-4320): alguém no caminho de rede do servidor poderia se passar pelo Mercado Pago, pelo Google ou pelo Supabase nas chamadas HTTPS do backend | Média (condicional: exige atacante no caminho de rede) | **Corrigido** | [requirements.lock:17](../requirements.lock#L17): `certifi==2026.10.19` desde 23/10 (era .18, sem a raiz, mas o `pip-audit` aponta a .19 como correção; com ela o `pip-audit` sai limpo, o que a CI do SEC-29 exige). A .23, publicada no próprio dia 23/10, ficou de fora de propósito: pacote do dia ainda não teve tempo de ser examinado por ninguém. Na Vercel o `requirements.txt` não fixa `certifi`, então cada deploy já pega a versão mais nova. |
| SEC-22 | Werkzeug 3.1.8: `safe_join` aceitava nomes de dispositivo do Windows (PYSEC-2026-4312) | Informativo (só em servidor Windows; o sistema roda em Linux) | **Corrigido** | [requirements.lock:868](../requirements.lock#L868): `werkzeug==3.1.9`. Lock regenerado com `--upgrade-package` só para Werkzeug e certifi (as demais versões ficaram iguais) e conferido com `docker build --target builder` (`--require-hashes` instala). |
| SEC-23 | Login com Google sem PKCE, `state` comparado com `!=` e sem validade (A07). As boas práticas de OAuth (RFC 9700) pedem PKCE também para cliente confidencial, contra injeção de código de autorização vazado | Baixa (defesa em profundidade: o cliente é confidencial e o `state` já era conferido) | **Corrigido** | Mesmo padrão do OAuth do Mercado Pago: [google_login.py:30](../blueprints/google_login.py#L30) (`code_verifier` de 86 caracteres e desafio S256), [google_login.py:43](../blueprints/google_login.py#L43) (`hmac.compare_digest` e validade de 10 min), [google_login.py:117](../blueprints/google_login.py#L117) (`code_verifier` na troca do code). Testes novos em `tests/test_google_login.py`: desafio = SHA-256 do verificador da sessão, verificador enviado na troca, sessão sem PKCE e `state` vencido recusados sem chamar o Google. |
| SEC-24 | O login com Google pedia o escopo `profile` (nome e foto), que o código nunca usa | Baixa (LGPD, minimização) | **Corrigido** | [google_login.py:85](../blueprints/google_login.py#L85): `scope='openid email'`, que já traz `email` e `email_verified`. Teste em `tests/test_google_login.py`. |
| SEC-25 | E-mail completo no log quando o link de verificação do cadastro não pode ser montado (A09; LGPD). O SEC-08 tinha mascarado os logs do serviço de e-mail, mas esta linha ficou de fora | Baixa | **Corrigido** | [usuario_bp.py:370](../blueprints/usuario_bp.py#L370) usa `mascarar_email`. Teste: `tests/test_logs_sem_dado_pessoal.py`. |
| SEC-18 | Fontes do Google Fonts: o navegador de todo visitante mandava o IP ao Google, na home e antes de qualquer consentimento (LGPD) | Informativo (LGPD) | **Corrigido** (estava aberto desde 04/10) | Bebas Neue e Inter (Fontsource 5.3.0, licença OFL em `static/fonts/LICENCA-*.txt`) servidas de `static/fonts`, declaradas em `static/css/fontes.css`; CSP sem `fonts.googleapis.com`/`fonts.gstatic.com` ([servidor.py:205-206](../servidor.py#L205-L206): `style-src 'self' 'unsafe-inline'`, `font-src 'self'`); `preload` das duas fontes de toda tela no `base.html`. No navegador: só o subconjunto latino de cada peso usado é baixado, **zero requisições externas**, renderização idêntica. Testes: `tests/test_fontes_locais.py` (8). |
| SEC-26 | A política de privacidade diz que "alunos e professores não conectam contas do Google", mas existe "Entrar com o Google", que recebe o e-mail do aluno (transparência, LGPD art. 9º; o Google também exige que a política descreva o uso dos dados do login) | Média | **Corrigido** (texto aplicado a pedido do dono em 20/10; validar com quem cuida da parte jurídica) | `templates/politica_privacidade.html`: a seção 2 virou "Contas do Google (Gmail e login)", a frase passou a "não conectam contas do Google para o envio de e-mails" e entrou o parágrafo *"**Entrar com o Google (alunos):** quem já tem cadastro pode entrar com a conta do Google que usa o mesmo e-mail. O Google informa ao sistema apenas o endereço de e-mail e se ele foi confirmado; o sistema não recebe a senha do Google, não guarda nenhum token do Google e não acessa e-mails, contatos ou arquivos. O e-mail serve só para encontrar o cadastro existente; nenhum cadastro é criado a partir do Google."* Política com data de 20/10/2026. Teste: `test_politica_de_privacidade_descreve_o_login_com_google`. |
| SEC-27 | Na Vercel, o valor certo de `TRUST_PROXY_COUNT` não está documentado (o README cobre só o Caddy do compose). Se o Flask não enxergar o IP real do visitante, **todo limite por IP vira limite global**: 20 senhas erradas por minuto, vindas de qualquer pessoa, bloqueariam o login de todo mundo (A04/A06) | Média (condicional: depende da configuração de produção, que não é visível daqui) | **Corrigido em 23/10/2026**, no código | Não depende mais do valor oculto da variável: com `VERCEL=1` (variável de sistema da plataforma), o `ProxyFix` confia em exatamente um salto ([servidor.py:137](../servidor.py#L137)). É o valor certo pela documentação de request headers da Vercel: ela *sobrescreve* o `X-Forwarded-For` com o IP público de quem fez a requisição e não repassa IPs de fora, então o cliente não consegue forjar o cabeçalho. Teste: `test_na_vercel_aceita_os_enderecos_do_projeto_e_um_proxy` (sobe o servidor com `TRUST_PROXY_COUNT=0` e `VERCEL=1` e confere `x_for == 1`; falha no código anterior). |
| SEC-28 | Comprovante em imagem guardado como enviado, com os metadados EXIF (podem incluir a localização de onde a foto foi tirada) | Baixa (LGPD) | **Corrigido** (21/10, a pedido do dono) | Os metadados saem direto dos bytes, sem decodificar a imagem, então o comprovante continua sem teto de pixels e com os mesmos pixels: [armazenamento.py:301](../servicos/armazenamento.py#L301) (JPEG: saem EXIF, XMP, IPTC, comentários e o que vem depois do fim da imagem; ficam JFIF, perfil de cor e Adobe) e [361](../servicos/armazenamento.py#L361) (PNG: saem `tEXt`, `zTXt`, `iTXt`, `eXIf`, `tIME` e chunks particulares). Só a orientação volta, num EXIF de uma tag, para a foto não chegar de lado ao administrador. Regravar a imagem foi descartado: decodificar um JPEG de 48 MP sem `draft()` passaria da memória do container. PDF segue guardado como veio. Testes: `tests/test_comprovante_sem_metadados.py` (7). |
| SEC-29 | Sem pipeline de CI: testes, `pip-audit`, `npm audit` e Bandit só rodam à mão, e nada impede o deploy de código com dependência vulnerável (A03/A08) | Baixa (processo) | **Corrigido em 23/10/2026** | [.github/workflows/ci.yml](../.github/workflows/ci.yml), em todo push na `main` e em todo PR, com o token só de leitura e as actions fixadas pelo SHA (o Dependabot atualiza). Job de testes: instala pelo lock com `--require-hashes` no Python 3.11, roda `pytest -q` e `node --test tests/js/*.test.cjs`. Job de auditoria: `pip-audit` no lock, `bandit -ll` (barra severidade média ou alta; os 9 achados de severidade baixa de hoje são falsos positivos, listados no próprio workflow) e `npm audit --omit=dev` em `front/`. Conferido antes: as três auditorias saem limpas, e o job de testes rodou num container `python:3.11.16-slim-bookworm` limpo. Essa simulação achou um furo, o PyYAML que `tests/test_limites_requisicao.py` importa e que só existia no venv local: entrou na CI e no `requirements-dev.txt`, agora com versões fixas. |
| SEC-30 | Conta de administrador sem segundo fator (ASVS 5.0, 6.3.3, nível 2). Ela acessa CPF, financeiro e a conta do Mercado Pago | Média | **Corrigido em 23/10/2026** (vale quando o dono definir `ADMIN_TOTP_SECRET`) | TOTP da RFC 6238 feito com a biblioteca padrão, sem dependência nova ([credenciais.py:125](../servicos/credenciais.py#L125), conferido contra os vetores do apêndice B da RFC). Com a variável, a senha certa só leva a `/login/verificacao` ([usuario_bp.py:247](../blueprints/usuario_bp.py#L247)), e a sessão de admin abre com o código: 6 dígitos, tolerância de um passo para relógio fora, uso único pelo storage do limitador ([usuario_bp.py:226](../blueprints/usuario_bp.py#L226)), 5 minutos para digitar, 5 tentativas por 15 min por IP e 10 por hora no total. Ligar, trocar ou desligar o segredo encerra as sessões de admin abertas, porque um resumo dele entra no carimbo da sessão ([credenciais.py:72](../servicos/credenciais.py#L72)). A aplicação recusa subir com segredo ilegível ou menor que 128 bits. Recuperação: apagar a variável no painel. Cadastro no app: `python -m servicos.credenciais totp` (README). Testes: `tests/test_admin_segundo_fator.py` (21) e `test_arranque_falha_com_segundo_fator_ilegivel`. Risco residual, igual ao do SEC-11: quem souber a senha consegue travar a etapa do código por até 1 hora. |
| SEC-31 | Login com Google aceitava aluno sem conta de acesso (sem senha). O login por senha só entra quem tem `senha_hash` (`AlunoDAO.autenticar`), mas o Google casava só pelo e-mail: quem a administração cadastrou e ainda não ativou o acesso entrava sem criar a senha nem aceitar o Termo de Responsabilidade do convite (A07; LGPD, aceite) | Média | **Corrigido em 22/10/2026**, com teste | [google_login.py:152](../blueprints/google_login.py#L152): a checagem `acesso_ativado` vem depois de achar o aluno e antes de abrir a sessão. Quem não tem senha vê o aviso para usar o link de ativação ou pedir um convite novo à administração. Teste: `test_aluno_sem_senha_nao_entra_pelo_google` em `tests/test_google_login.py`, que falha no código anterior. |
| SEC-32 | "Lembrar meu usuário" gravava o que fosse digitado no `localStorage`. Como o CPF também faz login, ele ficava em texto puro no aparelho, legível por qualquer script da origem (LGPD, minimização) | Baixa | **Corrigido em 22/10/2026**, com teste | [auth.js:8](../static/js/auth.js#L8) (`lembravel()`): CPF com ou sem máscara não é guardado, e um CPF já guardado sai do aparelho na próxima vez que a tela abre ([auth.js:17](../static/js/auth.js#L17)). Usuário e e-mail continuam lembrados. O modal de login da home tinha uma cópia própria dessa lógica em `index.js`, sem a regra: a cópia saiu e a home passou a carregar o `auth.js`. Testes: `tests/js/auth.test.cjs` (5, um deles com os ids do modal; os de CPF falham no código anterior). |
| SEC-33 | Login com Google limitado a 10 tentativas a cada 15 minutos por IP. A academia inteira sai pelo mesmo Wi-Fi (o motivo do SEC-17), então a partir do 11º aluno ninguém mais entrava pelo Google ali (A06, disponibilidade) | Baixa | **Corrigido em 23/10/2026**, com teste | 30 a cada 15 minutos por IP no início e na volta do Google ([google_login.py:64](../blueprints/google_login.py#L64)). Força bruta ali não rende nada: a volta só vale com o `state` e o PKCE da própria sessão, e a senha é do Google. Teste: `test_login_com_google_aguenta_o_wifi_da_academia` (30 passam, a 31ª recebe 429; falha no código anterior). |
| SEC-34 | Produção fora do ar: `https://sistema-extremeteam.vercel.app` respondia **400** em toda rota (conferido em 23/10 com uma requisição de leitura a `/health`), porque `TRUSTED_HOSTS` não lista esse host e o domínio `.com.br` não resolve no DNS. Ninguém conseguia abrir o site nem entrar (A02, configuração) | Média (disponibilidade) | **Corrigido em 23/10/2026** e publicado no mesmo dia (commit `f7ae2bc`): `/health` passou a responder 200 | Com `VERCEL=1`, entram na lista os endereços que a própria Vercel informa, sem `https://`: `VERCEL_PROJECT_PRODUCTION_URL`, `VERCEL_URL` e `VERCEL_BRANCH_URL` ([servidor.py:118](../servidor.py#L118)). A Vercel só entrega à função requisições de hosts ligados ao projeto, e host de fora continua recusado. Depende da opção "Automatically expose System Environment Variables", ligada por padrão em projeto novo. Testes: `test_na_vercel_aceita_os_enderecos_do_projeto_e_um_proxy` (falha no código anterior) e `test_fora_da_vercel_os_hosts_e_o_proxy_seguem_o_ambiente`. |
| SEC-35 | Com o 400 resolvido, a produção passou a responder **500** na home, no `/login` e no `/login/verificacao` (o `/health` seguiu 200 por não passar pelo limite). Os logs da Vercel mostram `UnicodeError: label empty or too long` no codec idna: o host de `RATELIMIT_STORAGE_URI` está malformado (um rótulo vazio ou com 64+ caracteres) e o Flask-Limiter só percebe na primeira requisição. O erro existia desde 07/10, escondido pelo 400. Além disso, o valor validado no arranque tinha os espaços removidos, mas o Flask-Limiter recebia o valor cru (A02, configuração; A10, falha sem diagnóstico) | Média (disponibilidade) | **Corrigido no código em 23/10/2026**; falta o dono corrigir a variável na Vercel | O arranque falha com mensagem que nomeia a variável quando o host ou a porta não passam pelo `urlsplit` e pelo codec idna ([servidor.py:67](../servidor.py#L67)), e o `from None` esconde o erro original, que repete pedaços da senha. O Flask-Limiter recebe o mesmo valor já sem espaços. O valor da variável não foi lido: está como Secret na Vercel. Testes: `test_arranque_falha_com_redis_de_host_malformado` (4 casos) e `test_arranque_aceita_redis_do_upstash_com_espaco_em_volta`, todos falham no código anterior. |
| SEC-36 | Webhook ignorava toda notificação do pagamento que já tinha quitado a mensalidade. Estorno e chargeback chegam com esse mesmo `data.id`, então uma mensalidade estornada ou contestada no Mercado Pago seguia "paga" e com acesso liberado (A04, regra de negócio de pagamento) | Média | **Corrigido em 26/10/2026**, com teste | O atalho saiu de `_tratar_webhook` ([pix_bp.py](../blueprints/pix_bp.py)): a repetição da mesma entrega já para em `_primeira_entrega_webhook`, e `_processar_status_mp` não aprova duas vezes. Testes: `test_reembolso_do_pagamento_que_quitou_continua_reembolsando` (falha no código anterior) e `test_webhook_repetido_e_idempotente`, atualizado. |
| SEC-37 | Cobrança substituída não quitava a mensalidade: um Pix ou checkout novo sobrescreve a referência gravada, e o boleto de um checkout anterior (ou um Pix antigo cujo cancelamento falhou) pago depois chegava como "não corresponde a nenhuma mensalidade". O dinheiro entrava e a mensalidade ficava em aberto | Média (financeiro) | **Corrigido em 26/10/2026**, com teste | Referência lida da API (nunca da URL ou do corpo) no formato exato que o servidor gera, `mensalidade-<id>-` + 11 caracteres ou `checkout-<id>-` + 22, leva à mensalidade se ela tem cobrança do Mercado Pago; valor e moeda continuam conferidos. Referência de outro sistema com padrão parecido é ignorada. Testes em `tests/test_checkout_rotas.py` (boleto e Pix antigos, valor errado, outro sistema, outra mensalidade). |
| SEC-38 | Pagamento em duplicidade: o estorno da cobrança duplicada marcava a mensalidade como reembolsada (e bloqueava o aluno) mesmo com o outro pagamento valendo, inclusive quando ela tinha sido paga por comprovante; e o segundo pagamento aprovado não deixava rastro. Um pagamento antigo aprovado também reabria mensalidade cancelada | Média (financeiro) | **Corrigido em 26/10/2026**, com teste | `_processar_status_mp` só aplica estorno ao pagamento que quitou pelo Mercado Pago (`_quitada_por`); os outros viram eventos `pagamento_duplicado`, `duplicado_reembolsado` e `pagamento_em_cobranca_fechada` no histórico da mensalidade, para o admin devolver ou reabrir. O webhook trava a linha da mensalidade (`bloquear_para_atualizacao`) antes de decidir. Testes em `tests/test_checkout_rotas.py`. |

**Cadeia de dependências do front (nova):** versões fixas e com mais de 14 dias de publicação
(React 19.3.0, three 0.186.1, R3F 9.8.1, drei 10.7.9, Vite 8.3.3, scrolly-video 0.0.24),
`package-lock.json` versionado, instalação com `npm ci --ignore-scripts` (nenhum pacote roda
script de instalação), `npm audit` sem vulnerabilidades. O Dependabot ganhou a entrada `npm`
para `front/` ([.github/dependabot.yml](../.github/dependabot.yml)). O build não busca nada fora
do site (teste `test_build_nao_busca_nada_fora_do_site`), e a iluminação da cena é gerada no
navegador em vez de baixar um HDRI de CDN, que a CSP bloquearia.

**Descartados depois de conferir:** "Voltar" de `turma.html` levando o admin a `/professor` (o
layout do admin não desenha esse cabeçalho; o admin recebe a navegação e o breadcrumb dele);
`innerHTML` do `componentes.js` (só SVG constante); SQL em texto no `prontidao.py` (constante);
alertas baixos do Bandit (URLs de endpoint de token tidas como senha, comparações com `None`, o
prefixo `TEST-` e o `escape` usado para **gerar** o sitemap XML).

## Rodada de 04/10/2026 — limites de requisição

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
| SEC-18 | Fontes carregadas do Google Fonts: o `@import` em [static/css/theme.css:7](../static/css/theme.css#L7) (liberado na CSP em `style-src`/`font-src` de `servidor.py`) faz o navegador de todo visitante, inclusive em páginas públicas e sem consentimento, enviar o IP ao Google | Informativo (LGPD) | **Corrigido em 20/10/2026** (ver a rodada de 20/10); em 04/10 ficou sem implementar por ser front-end | A política de privacidade (`templates/politica_privacidade.html`) cita o Google só no contexto do Gmail da academia, não das fontes. Caminhos possíveis: servir Bebas Neue e Inter (licença OFL) de `static/` e tirar `fonts.googleapis.com`/`fonts.gstatic.com` da CSP, ou declarar o compartilhamento na política de privacidade. |
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
- `pip-audit` sem vulnerabilidades conhecidas nas dependências declaradas (04/10). Em 20/10
  apareceram 10 (Pillow, certifi, Werkzeug): ver SEC-20 a SEC-22.
- Bandit: 1 alerta médio (`app.run(host="0.0.0.0")`, protegido por `if __name__ == '__main__'`;
  produção usa Gunicorn) e alertas baixos, todos falsos positivos de constantes/`None`.

**Conferido em 20/10/2026, no código novo desde 04/10 e no hero:**

- Upload no Supabase Storage: nome sempre UUID gerado no servidor (leitura recusa `/`, `\` e
  `..`), bucket privado acessado só pela chave secreta do servidor, tipo real conferido pelo
  conteúdo, foto regravada sem metadados, teto de pixels contra bomba de descompressão e,
  agora, só os decodificadores de JPEG, PNG e WebP (SEC-20).
- Comprovante: dono conferido, `Content-Type` tirado da extensão gerada pelo servidor e PDF
  entregue como download (`as_attachment`), nunca inline no domínio do sistema.
- Planilha econômica: todas as rotas com `@admin_requerido` e limite por conta; data,
  categoria (lista fechada), descrição (tamanho) e valor validados; o Excel grava todo texto
  como texto, então um aluno cadastrado com o nome `=HYPERLINK(...)` não vira fórmula (teste
  `test_planilha_economica.py`).
- Login com Google: `state` aleatório de 32 bytes, PKCE S256, validade de 10 min,
  `email_verified` obrigatório, só conta já existente e aprovada, sessão nova
  (`session.clear()` + `iniciar_sessao()`), credencial carimbada e escopo mínimo.
- Erros: toda exceção cai no handler de 500, que faz `rollback` e responde sem detalhe interno;
  401/403/404/413/429 com mensagens genéricas (A10, falha fechada).
- Hero da home: nenhuma rota nova; os módulos da cena vêm do `manifest.json` gerado no build
  (nunca de dado do visitante) e são importados do próprio domínio; o único script inline é
  estático e leva o nonce da resposta (teste `test_scripts_da_home_sao_do_proprio_site_ou_tem_nonce`);
  a CSP ficou **mais restrita** (sem os domínios de fonte do Google).

## Validação executada em 21/10/2026 (SEC-28)

- `pytest -q` → **1028 passaram, 0 falharam, 8 pulados**; `node --test tests/js/*.test.cjs` →
  **62 passaram, 0 falharam**.
- `tests/test_comprovante_sem_metadados.py` (7): 5 falham com o código anterior; os outros 2
  conferem que um arquivo sem metadados é guardado byte a byte igual.
- 2935 JPEG e PNG reais (de `static/` e de `/usr/share`) passaram pela limpeza: nenhum
  recusado, todos com os mesmos pixels, 781 ficaram menores (tinham metadados).
- Custo medido num JPEG de 3,4 MB cheio de bytes `FF`: ~10 ms e pico de ~2× o tamanho do
  arquivo; nenhum pixel decodificado.

## Validação executada em 20/10/2026

- Linha de base antes das mudanças: suíte Python verde; testes de JS com 13 falhas antigas
  (DOM falso sem `classList.replace`), as mesmas antes e depois desta rodada até serem corrigidas.
- Final: `pytest -q` → **1021 passaram, 0 falharam, 8 pulados** (os `*_postgres.py`, sem
  `TEST_POSTGRES_URL` nesta máquina); `node --test tests/js/*.test.cjs` → **62 passaram, 0
  falharam**.
- Testes novos: `tests/test_cinema.py` (13), `tests/js/cinema.test.cjs` (6),
  `tests/test_formatos_de_imagem.py` (8), `tests/test_fontes_locais.py` (8),
  `tests/test_logs_sem_dado_pessoal.py` (1) e 5 casos novos em `tests/test_google_login.py`.
- `pip-audit -r requirements.lock`: antes, 10 vulnerabilidades em 3 pacotes; depois, as 8 do
  Pillow (fora de alcance pelo SEC-20, atualização pendente) e o aviso da `certifi` 2026.10.18
  explicado no SEC-21. `npm audit` em `front/`: 0.
- `docker build --target builder .`: o lock novo instala com `--require-hashes` no Python 3.11
  da imagem.
- Bandit sobre `blueprints servicos dao modelos servidor.py config.py`: só alertas baixos,
  todos falsos positivos (ver "Descartados depois de conferir").
- Navegador (Playwright, GPU real, instância descartável `tools/redesign/servir_visual.py`):
  hero em 1440×900 e 390×844, movimento reduzido e sem JS; fontes carregadas só de
  `/static/fonts` com zero requisições externas; caminho do vídeo com um MP4 sintético.
- Nenhuma requisição foi enviada a Mercado Pago, Google, Supabase, Redis ou banco de produção.

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
| 20/10/2026 | Código novo desde 04/10 (Storage, planilha, login com Google, Vercel), hero 3D e `front/`, dependências (pip-audit, npm audit, lock), OWASP Top 10:2025 (A03, A09, A10) e checklist DevSecOps | SEC-20 a SEC-30 + SEC-18 (0 alto; 5 médio, 5 baixo, 2 informativo) | SEC-18 e SEC-20 a SEC-26 corrigidos com teste (o texto da política, a validar juridicamente); SEC-28 corrigido com teste em 21/10, a pedido do dono; SEC-27 (configuração da Vercel), SEC-29 e SEC-30 (recomendações) dependem do dono. |
| 22/10/2026 | Login (senha e Google), lembrar usuário e cena 3D do hero em aparelho com pouca memória | SEC-31 e SEC-32 (0 alto; 1 médio, 1 baixo) | Corrigidos com teste, sem mudar o login por senha. Hero: aparelho com menos de 4 GB passa a receber a cena leve (60 brasas, pixel 1x) em vez do pôster. A ficha do aluno no admin passou a validar a data de nascimento (gravava qualquer texto). Os dois últimos itens não são achados de segurança. |
| 23/10/2026 | Pendências abertas (SEC-27, SEC-29, SEC-30), atualização do Pillow (SEC-20), limite do login com Google e a produção na Vercel, com as skills owasp-security, devsecops-flask-review e vercel:env-vars | SEC-33 e SEC-34 (0 alto; 1 médio, 1 baixo) | Tudo corrigido com teste. Nenhum achado aberto no código: o SEC-30 vale quando o dono definir `ADMIN_TOTP_SECRET`, e a correção do SEC-34 só chega à produção depois de publicada. |
| 23/10/2026 (tarde) | Produção depois do deploy de `f7ae2bc`, com leitura dos logs de erro da Vercel | SEC-35 (0 alto; 1 médio) | Checagem no arranque com teste; a variável `RATELIMIT_STORAGE_URI` fica com o dono. |
| 22/09/2026 (2ª rodada) | OAuth Gmail/Mercado Pago, Checkout Pro, upload de arquivos, páginas legais públicas, credencial do administrador, revalidação independente de SEC-01/03/05/06/07/09 | OBS-01 (rate limit ausente no OAuth do Gmail, baixa/informativo); `requirements.lock` confirmado commitado e já usado com `--require-hashes` no Dockerfile | Nenhum achado de segurança aberto; ver tabelas **Situação atual** acima. |

**Nenhuma injeção de SQL, XSS refletido/armazenado/DOM, path traversal, IDOR, SSRF ou
segredo exposto foi encontrado em nenhuma das rodadas.**
