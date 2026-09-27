# Etapa 1 — migrar páginas para os layouts (SEM mudar o visual)

Branch `componentes-front`. Três agentes em paralelo, cada um com arquivos EXCLUSIVOS (lista no fim).
Não edite nada fora da sua lista. Nada de git que escreva (commit/add/checkout/stash/restore...).
Não suba servidor, não rode `graphify update`. O orquestrador faz as capturas e a suíte completa.

## O que já existe (não edite)

- `templates/layouts/base.html` — `<head>` comum. Blocos:
  `titulo` · `deslize` · `scripts` (scripts do `<head>`, com defer) · `estilos` (folhas da página, entre
  theme.css e extreme.css) · `estilos_finais` (folhas que vinham DEPOIS de extreme.css) ·
  `atributos_body` (ex.: `{% block atributos_body %} class="auth-page"{% endblock %}`, com o espaço inicial) ·
  `pular` / `alvo_pular` / `texto_pular` (skip link; padrão `#conteudo` "Ir para o conteúdo") ·
  `corpo` · `fim_corpo` (modais incluídos + scripts que ficavam no fim do `<body>`).
  O base já põe: meta csrf-token, viewport, theme-color, favicons, `components/deslize.html`,
  `js/componentes.js`, `css/theme.css`, `css/extreme.css` e `components/toasts.html`.
- `layouts/publico.html` — sem deslize; blocos `cabecalho` (padrão: `components/cabecalho_publico.html`),
  `conteudo`, `rodape` (padrão: `components/rodape_publico.html`).
- `layouts/aluno.html` — blocos `cabecalho` (padrão: `components/detail_back_header.html`), `conteudo`, `rodape`.
- `layouts/admin.html` — body `admin-shell` + `components/admin_nav.html` + bloco `conteudo`.
  O item ativo do menu: `{% set secao_ativa = '...' %}` logo abaixo do `extends`, fora de bloco.
- `layouts/professor.html` — bloco `cabecalho` (padrão: `components/cabecalho_professor.html`) + `conteudo`.
- Exemplos prontos: `templates/index.html` (público) e `templates/pgAdm.html` (admin). Copie o formato.

## Receita por página

1. Primeira linha: `{% extends "layouts/<area>.html" %}`. `{% import %}` que existiam no topo continuam no topo (depois do extends).
2. `{% block titulo %}` com o texto EXATO do `<title>` atual.
3. Scripts que estavam no `<head>` → `{% block scripts %}` na mesma ordem. Folhas da página → `{% block estilos %}`
   na mesma ordem; se alguma vinha depois de `extreme.css`, ela vai para `{% block estilos_finais %}`.
   NÃO repita theme.css, extreme.css, deslize, favicon, metas: o base já tem (teste cobra que aparecem 1 vez).
4. `class` do `<body>` diferente do padrão do layout → `atributos_body`. Skip link diferente → `alvo_pular`/`texto_pular`.
   Página sem skip link (ex.: comprovante) → ponha `id="conteudo"` no `<main>` e use o padrão.
5. Cabeçalho próprio da página → sobrescreva `{% block cabecalho %}` com ele. Página que não tinha cabeçalho/rodapé
   do layout (telas de acesso = cartão sozinho) → `{% block cabecalho %}{% endblock %}` e `{% block rodape %}{% endblock %}`.
6. `<main>...</main>` (e `<footer>` da página, se houver) → `{% block conteudo %}` (ou `rodape`).
7. Tudo que estava entre `</main>`/`</footer>` e `</body>` (modais incluídos, `<script>` do fim) → `{% block fim_corpo %}`, mesma ordem.
8. APAGUE o bloco `{% with mensagens = get_flashed_messages(...) %} ... {% endwith %}` (ou o `{% for ... in get_flashed_messages %}`):
   o toast do layout mostra os flashes. O teste cobra que `get_flashed_messages` não aparece mais na página.
9. Preserve TODO `id=`, `name=`, `data-*`, `aria-*`, classes e textos do conteúdo. Nada de redesign nesta etapa.
   Antes de mudar qualquer atributo, `grep -rn "<atributo>" tests static/js`.
10. `turma.html` serve admin e professor: `{% extends "layouts/admin.html" if eh_admin else "layouts/professor.html" %}`
    e sobrescreva `cabecalho` com o `detail-header` que a página já tem no ramo do professor (confira o `if` atual).

## Conferência (agentes Claude)

`env -u DATABASE_URL .venv/bin/python -m pytest -q -p no:cacheprovider -W ignore tests/test_layouts.py -k "<suas páginas>"`
e os testes das rotas das suas páginas (`grep -ln "<rota>" tests/*.py`). Linha de base da suíte completa antes da etapa:
6 failed (já existiam: test_email_gmail ×2, test_mercado_pago_oauth, test_pix_rotas webhook, test_publicas_redesign landing,
test_seguranca cadastro CPF), 623 passed, 8 skipped. Nenhum teste que passava pode passar a falhar.
Não edite testes existentes. Se um teste existente procura o markup antigo do flash (`class="msg msg-...`), NÃO altere
o teste: anote no relatório com o nome do teste.

## Relatório (curto)
Arquivos alterados · resultado literal do pytest que você rodou · qualquer desvio (ordem de CSS que mudou, teste
existente afetado, dúvida).

## Divisão

- **Antigravity (públicas):** `login.html`, `cadastro.html`, `recuperar.html`, `redefinir_senha.html`, `ativar_acesso.html`,
  `termos_de_servico.html`, `politica_privacidade.html`, `termos_responsabilidade.html` → `layouts/publico.html`
  com `cabecalho` e `rodape` VAZIOS (o `<footer>` e o `account-header` que cada uma já tem ficam dentro de `conteudo`).
- **Agente A (aluno + professor):** `pgUsuario.html` (cabeçalho próprio + `rodape` com o `app-footer`), `pagamento.html`,
  `comprovante.html`, `checkout_continuar.html`, `checkout_retorno.html` → `layouts/aluno.html`;
  `pgProfessor.html` → `layouts/professor.html` (o cabeçalho dele já virou `components/cabecalho_professor.html`).
- **Agente B (admin):** `admin_academia.html`, `admin_aluno_novo.html`, `admin_avisos.html`, `dt_aluno.html`,
  `financeiro.html`, `turmas.html`, `turma.html`, `professor_editar.html` → `layouts/admin.html`
  (`turma.html` conforme o passo 10).
