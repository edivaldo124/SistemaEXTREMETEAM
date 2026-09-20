# Contrato do redesign — SistemaEXTREMETEAM

Documento de coordenação entre o orquestrador (Claude), o Copilot e o Antigravity.
A especificação-mãe é o [PROMPT_CLAUDE_CODE.md](PROMPT_CLAUDE_CODE.md) (escrito pelo dono do projeto):
**leia-o inteiro e siga-o.** Este arquivo só registra as adaptações já aprovadas e quem é dono de cada arquivo.
Escreva todo texto para o usuário em português do Brasil, frase normal (não caixa alta, salvo os títulos em Bebas Neue).

## 1. Adaptações aprovadas ao prompt-mãe

| Prompt-mãe diz | No repositório real | Decisão |
|---|---|---|
| Supabase (banco, auth, Storage, RLS) | Não existe. É Flask + SQLAlchemy + Postgres; sessão por cookie; uploads em disco (`servicos/armazenamento.py`) | Manter a stack. Ignore qualquer menção a Supabase. A "RLS" é a autorização no servidor (`servicos/autorizacao.py`: `admin_requerido`, `aluno_requerido`, `professor_ou_admin_requerido`). |
| `--et-black:#0A0A0A` | As logos têm fundo `#000` puro | `--et-black` é `#000`. Superfície com logo = `--et-black`. |
| Status `vencido` | No banco o estado se chama `atrasado` (promovido sozinho após o vencimento) | Não renomear no banco. A classe `.status-vencido` é alias de `.status-atrasado`; o rótulo exibido é "Vencido". |
| "Lembrar de mim" no login | Sessão expira em 30 min de propósito (endurecimento de segurança) | NÃO estender a sessão. Implementar como "Lembrar meu usuário neste aparelho": só o nome de usuário em `localStorage` (dentro de try/catch), nunca a senha. |
| Login/cadastro num card com ⇄ | `/login` e `/cadastrar` são rotas separadas (cadastro tem CPF, termos e validação no servidor) | Mantê-las separadas, com o mesmo card. O ⇄ navega entre elas com transição. |
| Gráficos | CSP `script-src 'self'`: sem CDN, sem Chart.js | SVG renderizado no servidor (Jinja), com tabela/legenda acessível. |
| Logo em alta / `logo-original/` | Não está no repositório | Usar só arquivos de `static/imagens/`. Sem SVG de logo inventado. Onde faltar arte grande, deixar `TODO` para trocar pelos originais. |

## 2. Contrato de design (já existe no repositório — não redefina)

- **Tokens**: `static/css/tokens.css` (`--et-*`). Carregado por `theme.css` via `@import`; todo template que já linka `theme.css` o recebe. Não crie cores hexadecimais soltas: use o token. Se faltar um token, peça (seção 5).
- **Componentes CSS**: `static/css/componentes.css` (`.et-metrica`, `.et-vazio`, `.et-anel`).
- **Macros Jinja**: `templates/components/ui.html` — `badge`, `metrica`, `estado_vazio`, `anel`.
  Uso: `{% from "components/ui.html" import badge, metrica, estado_vazio, anel with context %}`.
- **Botões** (nomes existentes, não invente outros): `.button-primary` (gradiente dourado — uma por bloco), `.button-secondary`, `.btn` (compacto, linha de tabela), `.btn-principal` (aprovar), `.btn-remover` (recusar/excluir), `.btn-destaque`.
- **Badges**: `<span class="status status-<estado>">` com estados `pago`, `pendente`, `atrasado`/`vencido`, `em_analise`, `em_processamento`, `recusado`, `cancelado`, `reembolsado`; famílias `status-plano-*` e `status-acesso-*`.
- **Tipografia**: títulos e números grandes com `var(--et-font-display)` (Bebas Neue, só peso 400, só caixa alta). Texto, tabelas e formulários com Inter. Não peça `font-weight` de 700 em Bebas.
- **Variáveis antigas** (`--yellow`, `--paper`, `--ink`, `--surface`, `--line`, `--sp-*`, `--fs-*`, `--radius*`) continuam válidas como alias; código novo prefere `--et-*`.
- **Marca**: só as logos de `static/imagens/` (`logo-icon.png` = emblema quadrado 512 px; `logo-horizontal-{400,800,1200}.png` = logo horizontal, sempre com `srcset` e `sizes` reais; originais intactos em `static/imagens/marca/`; favicons `favicon-{32,180,192,512}.png`). As logos antigas (`logo-header*`, `logo-full*`, `logo.png`) foram removidas. Sempre sobre `--et-black`, sem borda nem sombra que revele o retângulo. Nunca redesenhar, nunca esticar (mantenha a proporção). `alt="Extreme Team"` quando for a única identificação; `alt=""` quando decorativa.
- **Cara do redesign** (evite os vícios de página gerada): sem "eyebrow" em caixa alta sobre todo título; sem numeração 01/02/03 onde o conteúdo não é sequência; sem fade-in em toda seção (movimento só onde responde a uma ação ou num único momento de entrada); gradiente dourado só no botão primário e no item ativo do menu; cartões escuros `--et-surface-dark` com borda `--et-line-dark`; raio: controle 10, botão 12, cartão 18.
- **Qualidade mínima**: responsivo de 360 a 1440 px sem rolagem horizontal; alvo de toque ≥ 44 px; foco de teclado visível; `prefers-reduced-motion` respeitado; contraste AA; valores `R$ 1.234,56` (filtro Jinja `|moeda`); datas `dd/mm/aaaa`; estados vazios escritos ("Nenhum pagamento pendente"), nunca dados inventados.

## 3. Restrições do servidor (a suíte de testes cobra isto)

- **CSP** (`servidor.py`): `script-src 'self' 'nonce-…'`, `script-src-attr 'none'` → **proibido** `onclick=`/`onchange=` e qualquer handler inline; scripts só como arquivo em `static/js/` (`<script src=… defer>`) ou inline com `nonce="{{ csp_nonce() }}"`. Sem `<script>` de CDN. `img-src 'self' data:`. Fontes só do Google Fonts. `<style>` e `style=""` inline são permitidos.
- **CSRF**: todo `<form method="post">` inclui `{% include "components/csrf_field.html" %}`.
- **Não quebre contratos que testes e JS usam**: rotas, `name=` de campos, `id=`, `data-*`, `aria-*` e textos visíveis que os testes procuram. Antes de renomear ou reescrever um texto/atributo, faça `grep -rn "<texto>" tests static/js`.
- Não toque em `.env`, `.env.local`, `.env.example`, `compose.yaml`, `Dockerfile`, `migrations/`, `servidor.py`, `blueprints/usuario_bp.py`, `blueprints/mercado_pago_oauth_bp.py`, `servicos/mercado_pago*.py`.
- Há trabalho **não commitado do dono** em `templates/cadastro.html`, `templates/admin_academia.html`, `static/css/admin_academia.css`, `blueprints/academia_bp.py`: leia o `git diff` desses arquivos antes de editá-los e preserve cada linha dele.

## 4. Quem é dono de quê (não edite arquivo de outro dono)

**Orquestrador (Claude)**
`tokens.css`, `componentes.css`, `theme.css`, `extreme.css`, `components/ui.html`, `components/admin_nav.html`, `js/admin_nav.js`, `components/detail_back_header.html`, `components/*modal*`, `js/modal*.js`, `js/comprovante*.js`,
`pgUsuario.html/.css/.js`, `planos.css`, `pagamento.html`, `pagamento.css/.js`, `pix.css/.js`, `comprovante.html/.css`, `checkout_*.html`,
`turmas.html/.css`, `turma.html`, `js/turma*.js`, `js/presenca_historico.js`, `pgProfessor.html`, `professor_editar.html/.css`,
`static/imagens/*` (exceto `hero-*` novos do Antigravity), favicons e `manifest.json`, `templates/email/*`,
e **todo componente de `templates/components/` que não aparece nas listas abaixo** (`plano_situacao.html`, `mensalidade_acao.html`, `paginacao.html`, `pix_dialog.html`, `presenca_modal.html`, `turma_detalhe_modal.html`, `confirm_modal.html`, `csrf_field.html`). Você pode *incluí-los*; para mudá-los, faça um pedido.

**Antigravity** — telas públicas (1, 2, 3, 4)
`index.html`, `login.html`, `cadastro.html`⚠, `recuperar.html`, `redefinir_senha.html`, `ativar_acesso.html`, `termos_responsabilidade.html`, `components/contatos_academia.html`,
`index.css`, `login.css`, `cadastro.css`⚠, `recuperar.css`, `contatos.css`, `js/index.js`, `js/senha_confirmacao.js`, e arquivos NOVOS que criar (`auth.css`, `js/auth.js`, `static/imagens/hero-*`).
Só front-end: nenhuma alteração em Python.

**Copilot** — painel admin (8, 9, 10, 11)
`pgAdm.html`, `dt_aluno.html`, `financeiro.html`, `admin_aluno_novo.html`, `admin_avisos.html`, `admin_academia.html`⚠,
`pgAdm.css`, `dt_aluno.css`, `financeiro.css`, `admin_academia.css`⚠, `js/pgAdm.js`, `js/filtros_financeiro.js`, `js/mensalidades_filtro.js`,
`blueprints/adm_bp.py` (rotas e contexto), `dao/*.py` (**só ACRESCENTAR funções novas**; não altere as existentes), e arquivos NOVOS: `admin_alunos.html`, `admin_relatorios.html`, `components/graficos.html`, `admin_paginas.css`, `tests/test_admin_*.py`.

⚠ = contém trabalho não commitado do dono (ver seção 3).

## 5. Regras de convivência (vários agentes, mesma árvore de trabalho, branch `redesign-et`)

1. Só edite arquivos do seu bloco. Precisa de mudança num arquivo de outro dono (token novo, macro, regra em `theme.css`/`extreme.css`)? **Não edite**: descreva no relatório em "Pedidos ao orquestrador" com o trecho exato.
2. **Nenhum comando git que escreva**: nada de `commit`, `add`, `checkout`, `switch`, `stash`, `reset`, `restore`, `clean`, `rebase`, `merge`, `push`. Só `git status/diff/log/show`.
3. **Não rode `graphify update`** (o orquestrador roda uma vez no fim). Para se orientar no código, use o grafo antes de sair lendo arquivos: `graphify query "<pergunta>"`, `graphify path "<A>" "<B>"`, `graphify explain "<conceito>"`.
4. Não suba o servidor, não abra portas, não toque no banco real. Teste só com pytest (SQLite descartável do `tests/conftest.py`): `env -u DATABASE_URL .venv/bin/python -m pytest -q <arquivos>`. Os helpers `criar_aluno`, `criar_pagamento`, `logar_como_aluno`, `logar_como_admin` estão em `tests/conftest.py`.
5. Linha de base da suíte completa antes de qualquer agente: **589 passed, 8 skipped** (≈113 s). Rode a suíte completa ao terminar. Não edite teste existente para "fazê-lo passar"; se uma mudança de texto é intencional e o teste precisa acompanhar, diga isso no relatório.
6. Leia e nunca imprima segredos. Nada de dados falsos em produção: números vêm do banco.
7. Comentários e nomes seguem o arquivo ao redor (português, explicando o *porquê*, sem enfeite).

## 6. Formato do relatório final (máx. ~400 palavras, em português)

1. Arquivos criados/alterados (lista).
2. Rotas novas e funções novas de DAO (se houver).
3. Testes: comando rodado e resultado (`N passed`), incluindo a suíte completa.
4. Decisões e desvios do prompt-mãe.
5. **Pedidos ao orquestrador** (tokens/macros/CSS de arquivos que não são seus).
6. O que ficou de fora e por quê.

---

## 7. Erros já cometidos neste redesign — não repita

Todos foram achados olhando o resultado no navegador, e **nenhum foi pego pelos testes** (a suíte passou o tempo todo). Testar não basta: abra a tela.

1. **Empilhar CSS novo sobre classes legadas.** O cartão de login manteve `brand-panel`, `form-panel`, `signup` no HTML e as regras antigas em `extreme.css`; a regra antiga (mais específica) pintou os links de escuro sobre o cartão escuro e eles ficaram invisíveis. Ao refazer uma tela: **tire as classes antigas do HTML e apague as regras antigas dos CSS**, não some por cima. Rode `grep -rn "<classe-antiga>" templates static` antes de dar por terminado.
2. **`overflow-x:hidden` em `html`/`body` quebra `position:sticky`** (o body vira contêiner de rolagem). Use `overflow-x:clip`. Ancestrais de um elemento `sticky` também não podem ter `overflow:hidden`/`auto`; use `clip`.
3. **Logo com placa preta sobre fundo que não é `#000`** desenha um retângulo (as logos são RGB, sem alfa). Sobre `--et-black` puro não aparece; sobre cartão `#161616` ou sobre brilho dourado, use `mix-blend-mode:lighten` na `<img>` (e `isolation:isolate` no contêiner se houver brilho atrás). Nunca `background`/`border-radius` na imagem da logo.
4. **`.campo + .campo { margin-top }` vaza para dentro de grades.** Escopar a margem ao contêiner que empilha (`form > .field + .field`); dentro de `grid`, use `gap`.
5. **Dois scripts fazendo a mesma coisa** (um inline e um em `auth.js` alternando "mostrar senha") se anulam. Antes de escrever JS, procure se já existe.
6. **Marca digitada em texto** ("EXTREME TEAM" em Bebas ao lado de um ícone) não é a logo oficial. Use as imagens.
7. **`path` de SVG com número faltando** gera erro de console: o script de captura (seção 8) lista erros de console de cada página — zere-os.
8. **`@import` duplicado** do mesmo CSS que o template já linka.
9. **Rótulos com traço + caixa alta sobre todo título, numeração 01/02/03 onde não há sequência e a mesma informação repetida em dois blocos** (ex.: "Comece/Mantenha/Supere" na faixa do hero E nos cartões logo abaixo) são vícios de página gerada. Cada informação aparece uma vez.

10. **Logo renderizada menor/maior que a resolução da imagem.** Uma logo horizontal foi espremida em 38×38 (regra global `.site-brand img`) e o emblema do hero foi reduzido para 536 px antes de ser ampliado no navegador. Regra: meça com `eval` (`naturalWidth` × largura renderizada); a ampliação (`renderizada/natural`) tem de ser ≤ 1,0; sirva 3 resoluções reais com `srcset`+`sizes` verdadeiros; nunca converta logo para WebP com perdas.

## 8. Como verificar visualmente (obrigatório antes de dizer "pronto")

Nunca use o navegador do MCP do Playwright: ele é compartilhado entre agentes e a aba muda sozinha. Use as ferramentas isoladas:

```bash
# 1) sobe uma instância descartável (SQLite temporário, sem rede) em http://localhost:4002
.venv/bin/python tools/redesign/servir_visual.py &        # logins: admin/admin-visual-123, aluno1/senha123, prof/prof12345
# 2) capturas + medições (uma execução do navegador, vários perfis/tamanhos)
SAIDA=/tmp/redesign-shots node tools/redesign/shot.mjs jobs.json
```
`jobs.json` = lista de `{perfil:'anon|admin|aluno|prof', w, h, path, out, full, cliques:[seletores], eval:'() => ...'}`. O script imprime, por captura: status, `overflowX` (deve ser **0** em 360–1440 px), **erros de console (devem ser `[]`)** e o resultado do seu `eval` (use-o para medir alinhamento, tamanhos e cores computadas em vez de "achar"). **Olhe cada PNG** (desktop 1440 e celular 390) e critique como um designer antes de encerrar. A instância recarrega templates sozinha; CSS/JS é só recarregar. Pare o servidor no fim (`pkill -f servir_visual.py`).

Requer Playwright/Chromium já instalados em `~/.cache/ms-playwright` e em `~/.npm/_npx/*/node_modules/playwright` (ajuste o caminho no topo de `shot.mjs` se mudar).

## 9. Estado do trabalho (atualize ao terminar cada bloco)

Branch `redesign-et`. Suíte: **594 passed, 8 skipped** (linha de base 589 + 5 testes de telas públicas).

**Feito e verificado no navegador:** tokens (`tokens.css`), componentes (`componentes.css`, `components/ui.html`), tipografia Bebas Neue/Inter e botão dourado em gradiente via `theme.css`; troca das logos pelas oficiais (originais em `static/imagens/marca/`; derivadas geradas nos nomes antigos `logo-icon.png`, `logo-header*.png`, `hero-emblema.webp` e novos `favicon-{32,180,192,512}.png`); telas de auth (login, cadastro, recuperar, redefinir, ativar) refeitas — marca com emblema oficial, ⇄ dourado, abas no celular, "lembrar meu usuário".

**Landing (`index.html`/`index.css`/`extreme.css`) refeita e verificada** (1920, 1440 e 390 px; overflowX 0; sem erro de console): cabeçalho e hero viram um palco preto contínuo, logo horizontal oficial a 196×88 px (antes 38×38 por causa de `.site-brand img` em `theme.css`), emblema do hero em recorte nativo 795×859 sem perdas com `mix-blend-mode:lighten` (sem retângulo), "Nosso método" volta a ser o passo a passo real (Crie sua conta / Escolha seu plano / Treine e acompanhe) e a faixa Comece/Mantenha/Supere fica só no hero; o bloco legado `home:` de `extreme.css` foi apagado. Pendente na landing: trocar o emblema do hero pelo `hero-dragao.webp` oficial (o arquivo `emblema-dragao.png` enviado tem só 1005×1185 e já vem com compressão/blur na fonte, então a nitidez máxima possível hoje é a de um recorte nativo).
**Em aberto — restante do plano:** shell admin (sidebar preta, `admin_nav.html`), painel/alunos/relatórios/financeiro/perfil (fatia do Copilot, ainda sem dono), área do aluno, Pix, turmas/presença, favicons+`manifest.json` ligados nos templates, logo horizontal nos e-mails (`templates/email/base.html`), limpeza de `static/imagens` (logos antigas duplicadas) e da pasta `.playwright-mcp/` na raiz.
**Copilot:** o plugin está quebrado (falta `@github/copilot-sdk`; o `setup` reporta "pronto" mesmo assim). Nada foi executado por ele.

**Reatribuição (19/09/2026):** com o Copilot indisponível, a fatia "painel admin" (seção 4) passou ao Antigravity (2º job), e o enunciado detalhado está em `tools/redesign/TAREFA_ADMIN.md`. Nessa fatia entram também `components/admin_nav.html`, `js/admin_nav.js` e, em `extreme.css`, SOMENTE o bloco "administração: barra lateral" (sidebar preta com o emblema; itens Painel, Alunos, Turmas, Financeiro, Planos, Avisos, Relatórios, Academia, Sair). O resto do `extreme.css`/`theme.css` continua do orquestrador. Área do aluno, Pix, turmas/presença e a landing continuam com o orquestrador.
