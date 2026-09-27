# Etapa 2 — biblioteca de componentes

Branch `componentes-front`. Três frentes em paralelo, cada uma com arquivos EXCLUSIVOS.
Nada de git que escreva, não suba servidor, não rode `graphify update`, não edite páginas (`templates/*.html`):
nesta etapa os componentes só aparecem na **vitrine** (`/_vitrine` da instância descartável, porta 4002).
Aplicar nas páginas é das etapas 3 a 6.

## Regras visuais (REDESIGN_CONTRATO.md seção 2 — leia)
- Só tokens `--et-*` (e os aliases `--sp-*`, `--fs-*`, `--ease`, `--dur-*` de theme.css). Nenhum hex solto.
- Títulos/números: `var(--et-font-display)` (Bebas Neue, peso 400, caixa alta). Resto: Inter.
- Raios: controle `--et-radius-control` (10), botão `--et-radius-btn` (12), cartão `--et-radius-card` (18).
- Gradiente dourado só no botão primário e item ativo do menu. Sem eyebrow em caixa alta, sem 01/02/03, sem fade-in.
- Foco visível (`outline:2px solid var(--et-gold); outline-offset:2px`), alvo de toque ≥ 44 px,
  `@media (prefers-reduced-motion:reduce)` desliga transições/animações do componente.
- Os componentes precisam funcionar sobre fundo CLARO (páginas do aluno/admin: `--surface`, `--ink`)
  e, onde fizer sentido, sobre o escuro (`--et-surface-dark`). Prefixo de classe: `.et-<nome>`.

## Ganchos de JS (Claude escreve `static/js/componentes.js`; markup e CSS usam EXATAMENTE isto)

**Tabs** (WAI-ARIA, setas/Home/End):
```html
<div class="et-tabs" data-tabs>
  <div class="et-tabs-lista" role="tablist" aria-label="Seções do aluno">
    <button type="button" role="tab" id="aba-dados" aria-controls="painel-dados" aria-selected="true">Dados</button>
    <button type="button" role="tab" id="aba-pag" aria-controls="painel-pag" aria-selected="false" tabindex="-1">Pagamentos</button>
  </div>
  <div class="et-tabs-painel" role="tabpanel" id="painel-dados" aria-labelledby="aba-dados" tabindex="0">...</div>
  <div class="et-tabs-painel" role="tabpanel" id="painel-pag" aria-labelledby="aba-pag" tabindex="0" hidden>...</div>
</div>
```
Estilo da aba ativa: `[aria-selected="true"]`.

**Menu de ações** (Esc fecha e devolve o foco; setas andam; clique fora fecha):
```html
<div class="et-menu" data-menu>
  <button type="button" class="et-menu-botao" aria-haspopup="menu" aria-expanded="false" aria-controls="menu-7" aria-label="Ações de Marina Souza">
    <svg ...três pontos...></svg>
  </button>
  <div class="et-menu-lista" role="menu" id="menu-7" hidden>
    <a role="menuitem" href="...">Ver detalhes</a>
    <form method="post" action="..." role="none">{% include "components/csrf_field.html" %}<button type="submit" role="menuitem" class="et-menu-perigo">Remover</button></form>
  </div>
</div>
```
Aberto: `[aria-expanded="true"]` no botão e a lista sem `hidden`. A lista abre alinhada à direita do botão.

**Tooltip**: `<button type="button" class="..." aria-label="Copiar código" data-tooltip>svg</button>`
(ou `<a ... aria-label data-tooltip>`). O JS cria `<span class="et-tooltip" role="tooltip">` como filho de `body`,
posicionado acima do elemento (abaixo se não couber) e com a classe `et-tooltip--visivel` quando aparece.

**Accordion**: HTML nativo, sem JS: `<details class="et-acordeao"><summary>Título</summary><div class="et-acordeao-corpo">...</div></details>`.
Vários em sequência formam o grupo. Seta indicadora via CSS (`details[open] > summary`).

**Botão com carregamento**: `<form ... data-enviando>` e no botão `data-texto-enviando="Enviando..."`.
No submit o JS põe `disabled`, `aria-busy="true"`, troca o texto e adiciona `.et-carregando` ao botão
(o CSS desenha um spinner antes do texto via `::before`).

**Tabela de dados**:
```html
<div class="et-tabela" data-tabela>
  <div class="et-tabela-ferramentas">
    <label class="et-tabela-busca"><span class="sr-only">Buscar alunos</span>
      <input type="search" placeholder="Buscar" data-tabela-busca></label>
  </div>
  <div class="et-tabela-rolagem" tabindex="0" role="region" aria-label="Alunos da turma">
    <table>
      <thead><tr>
        <th scope="col" aria-sort="none"><button type="button" data-ordenar="texto">Aluno</button></th>
        <th scope="col" aria-sort="none"><button type="button" data-ordenar="data">Vencimento</button></th>
        <th scope="col" aria-sort="none"><button type="button" data-ordenar="numero">Valor</button></th>
        <th scope="col">Ações</th>
      </tr></thead>
      <tbody>
        <tr><td>Marina</td><td data-valor="2026-10-04">04/10/2026</td><td data-valor="150.00">R$ 150,00</td><td>...</td></tr>
      </tbody>
    </table>
  </div>
  <p class="et-tabela-vazio" data-tabela-vazio hidden>Nenhum resultado para a busca.</p>
</div>
```
Cabeçalho fixo (`position:sticky` no `th` DENTRO de `.et-tabela-rolagem`, que tem `max-height` e `overflow:auto`),
rolagem horizontal no próprio contêiner no celular. Seta de ordenação via `th[aria-sort="ascending|descending"]`.
Busca/ordenação só em tabelas sem paginação; nas paginadas usa-se só o visual (sem `data-tabela-busca`/`data-ordenar`).

**Upload com pré-visualização** (validação no cliente; o servidor continua validando):
```html
<div class="et-upload" data-upload data-tipos="image/jpeg,image/png,image/webp,application/pdf" data-max-mb="5">
  <label class="et-upload-alvo">
    <input type="file" name="comprovante" accept="image/jpeg,image/png,image/webp,application/pdf" class="sr-only">
    <span class="et-upload-titulo">Escolha o arquivo</span>
    <span class="et-upload-ajuda">JPG, PNG, WEBP ou PDF, até 5 MB.</span>
  </label>
  <div class="et-upload-previa" data-upload-previa hidden></div>   <!-- JS põe <img> ou <p class="et-upload-arquivo">nome.pdf · 1,2 MB</p> + botão "Trocar arquivo" -->
  <p class="et-upload-erro" data-upload-erro role="alert" hidden></p>
</div>
```
Com arquivo escolhido: classe `.et-upload--com-arquivo`. Arraste por cima: `.et-upload--arrastando`.

## Macros (Agente A), cada uma no seu arquivo em `templates/components/`

- `avatar.html` → `{% macro avatar(nome, foto_url='', tamanho='md') %}`: foto quando houver (`alt=""`, o nome está ao lado),
  senão as iniciais (primeiro + último nome, 2 letras) sobre fundo preto com letra dourada em Bebas. Tamanhos `sm` 32, `md` 44, `lg` 72.
- `linha_tempo.html` → `{% macro linha_tempo_pagamento(status) %}`: passos Aguardando pagamento → Em análise → Pago;
  `recusado` e `cancelado` terminam o fluxo no lugar de "Pago" com cor de erro/neutra; `atrasado` = Aguardando pagamento vencido;
  `em_processamento` = Em análise (rótulo "Processando"); `reembolsado` = Pago + passo "Reembolsado".
  Lista ordenada `<ol>` (é uma sequência de verdade), passo atual com `aria-current="step"`, estado em texto (não só cor).
- `breadcrumb.html` → `{% macro breadcrumb(itens) %}` com `itens = [('Painel', '/admin'), ('Alunos', None)]`:
  `<nav aria-label="Você está em"><ol>`, último item com `aria-current="page"`.
  E evolua `components/detail_back_header.html` para aceitar `voltar_href`/`voltar_texto` opcionais (padrão atual: `/perfil`, "Voltar para minha área") SEM mudar o que renderiza hoje sem as variáveis.
- `cartao_plano.html` → `{% macro cartao_plano(plano, destaque=false) %}` com `plano` = dict
  `{nome, preco_total, preco_mes, meses, duracao_texto ('3 meses'), economia (número ou none), url_matricula, texto_botao}`:
  nome, preço por mês grande em Bebas (`|moeda`), "R$ X no total por 3 meses", economia "Economia de R$ 40,00" quando houver,
  botão. `destaque=true`: cartão maior, fundo `--et-surface-dark`, texto claro, botão primário dourado, selo "Mais escolhido" NÃO —
  use "Recomendado", e a **borda brilhante** (`.et-borda-brilho`: `@property --et-angulo` + `conic-gradient` em máscara, girando ~6 s,
  parada e dourada fixa com reduced-motion). Demais: discretos, botão secundário. E `{% macro secao_planos(planos) %}`:
  grade em que o destaque fica ao centro no desktop e PRIMEIRO no celular (CSS `order`); sem planos → `estado_vazio`
  ("Os planos ainda não foram publicados." / "Fale com a academia para saber os valores.").

## Entregas e arquivos exclusivos

- **Agente A (Claude):** os 4 arquivos de macro acima + `components/detail_back_header.html`;
  CSS em `tools/redesign/etapa2/a.css`; exemplos em `tools/redesign/vitrine/_a.html` (cada macro em claro e,
  o cartão de plano, com 3 planos fictícios só na vitrine).
- **Antigravity:** CSS de tabs, menu de ações, tooltip, accordion, botão com carregamento, tabela de dados e upload em
  `tools/redesign/etapa2/b.css`; exemplos com o markup EXATO acima em `tools/redesign/vitrine/_b.html`.
- **Claude (orquestrador):** `static/js/componentes.js`, `templates/erro.html`, handlers em `servidor.py`, `tests/`,
  a vitrine (`tools/redesign/vitrine/vitrine.html` + rota em `tools/redesign/servir_visual.py`) e a junção de a.css/b.css em
  `static/css/componentes.css`.

A vitrine inclui `_a.html` e `_b.html` dentro de `{% block conteudo %}` de um layout com `componentes.css`;
escreva só o conteúdo (seções `<section class="vitrine-secao"><h2>Nome</h2>...</section>`), sem `<html>`/`<head>`.
Relatório: arquivos criados, desvios, dúvidas. Agente A: rode `env -u DATABASE_URL .venv/bin/python -m pytest -q -p no:cacheprovider -W ignore tests/test_layouts.py tests/test_checkout_rotas.py tests/test_comprovante_manual.py` (detail_back_header é usado nessas páginas) e cole a linha final.
