---
version: alpha
name: Extreme-Team-design-system
description: Sistema visual da Extreme Team, academia de lutas e musculação. O preto puro é o palco da marca (cabeçalhos, barra lateral, hero, cartões de métrica) e o papel creme é a superfície de leitura. O dourado aparece só onde há ação ou estado ativo. Os títulos usam Bebas Neue em caixa alta e o resto do texto usa Inter. Os componentes seguem a estrutura do shadcn/ui com a marca por cima (prefixo .et-).

colors:
  # Palco escuro: o preto é #000 puro porque as logos oficiais têm fundo preto
  et-black: "#000000"
  et-black-soft: "#0A0A0A"
  et-surface-dark: "#161616"
  et-surface-dark-2: "#202020"
  ink-3: "#2C2E31"
  et-line-dark: "rgba(245,185,20,.22)"
  et-line-dark-strong: "rgba(245,185,20,.5)"
  # Ouro
  et-gold: "#F5B914"
  et-gold-light: "#FFE27A"
  et-gold-dark: "#B7790A"
  yellow-soft: "#FEF0BC"
  # Papel e superfícies claras
  et-cream: "#F6F1E6"
  paper-2: "#E3DED1"
  surface: "#FFFFFF"
  surface-2: "#F6F3EC"
  line: "#DFDACC"
  line-strong: "#C5BEAC"
  # Texto
  text: "#16181A"
  text-2: "#4C5155"
  text-3: "#63686D"
  text-on-dark: "#F4F1E8"
  text-on-dark-muted: "#A9ADB1"
  # Situações sobre o claro (trincas cor / fundo / tinta)
  green: "#1D6244"
  green-bg: "#DFEEE7"
  green-ink: "#14503A"
  red: "#A03325"
  red-bg: "#F7E1DD"
  red-ink: "#7C2C22"
  amber: "#8A6B00"
  amber-bg: "#FBEFC6"
  amber-ink: "#5F4A00"
  blue: "#1C4478"
  blue-bg: "#DDE6F5"
  blue-ink: "#1A3E6C"
  slate: "#4C5155"
  slate-bg: "#E4E2DC"
  slate-ink: "#41454A"
  # Situações sobre o escuro
  et-ok-ink-dark: "#7EDBA6"
  et-warn-ink-dark: "#FFD666"
  et-bad-ink-dark: "#FF9C99"
  et-info-ink-dark: "#A9C6F5"
  # Apoio decorativo: só nas formas do fundo, nunca para comunicar situação
  clay: "#B9541F"
  forest: "#1C4A38"

typography:
  display-hero:
    fontFamily: Bebas Neue, Barlow Condensed, Impact, sans-serif
    fontSize: 72px
    fontWeight: 400
    lineHeight: 0.92
    letterSpacing: 0.01em
    textTransform: uppercase
  display-h1:
    fontFamily: Bebas Neue, Barlow Condensed, Impact, sans-serif
    fontSize: 44px
    fontWeight: 400
    lineHeight: 1.02
    letterSpacing: -0.01em
    textTransform: uppercase
  display-h2:
    fontFamily: Bebas Neue, Barlow Condensed, Impact, sans-serif
    fontSize: 30px
    fontWeight: 400
    lineHeight: 1.1
    textTransform: uppercase
  display-metrica:
    fontFamily: Bebas Neue, Barlow Condensed, Impact, sans-serif
    fontSize: 52px
    fontWeight: 400
    lineHeight: 1
    letterSpacing: 0.02em
  display-preco:
    fontFamily: Bebas Neue, Barlow Condensed, Impact, sans-serif
    fontSize: 56px
    fontWeight: 400
    lineHeight: 0.95
    letterSpacing: 0.02em
  display-plano:
    fontFamily: Bebas Neue, Barlow Condensed, Impact, sans-serif
    fontSize: 28px
    fontWeight: 400
    lineHeight: 1
    letterSpacing: 0.03em
    textTransform: uppercase
  body-lg:
    fontFamily: Inter, Segoe UI, system-ui, sans-serif
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.55
  body:
    fontFamily: Inter, Segoe UI, system-ui, sans-serif
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.55
  body-md:
    fontFamily: Inter, Segoe UI, system-ui, sans-serif
    fontSize: 15px
    fontWeight: 400
    lineHeight: 1.5
  body-sm:
    fontFamily: Inter, Segoe UI, system-ui, sans-serif
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.6
  rotulo:
    fontFamily: Inter, Segoe UI, system-ui, sans-serif
    fontSize: 14px
    fontWeight: 600
    lineHeight: 1.4
  body-xs:
    fontFamily: Inter, Segoe UI, system-ui, sans-serif
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.5
  micro-caps:
    fontFamily: Inter, Segoe UI, system-ui, sans-serif
    fontSize: 12px
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: 0.08em
    textTransform: uppercase
  botao:
    fontFamily: Inter, Segoe UI, system-ui, sans-serif
    fontSize: 14px
    fontWeight: 600
    lineHeight: 1.2

rounded:
  selo: 6px
  control: 10px
  btn: 12px
  card: 18px
  card-mobile: 22px
  painel: 28px
  pill: 999px

spacing:
  sp-1: 4px
  sp-2: 8px
  sp-3: 12px
  sp-4: 16px
  sp-5: 20px
  sp-6: 24px
  sp-7: 32px
  sp-8: 40px
  sp-9: 48px
  sp-10: 64px
  sp-11: 80px

components:
  et-botao--principal:
    background: "linear-gradient(135deg, {colors.et-gold-light} 0%, {colors.et-gold} 48%, {colors.et-gold-dark} 100%)"
    borderColor: "{colors.et-gold-dark}"
    textColor: "{colors.et-black}"
    typography: "{typography.botao}"
    fontWeight: 700
    rounded: "{rounded.btn}"
    height: 48px
    padding: "0 {spacing.sp-5}"
  et-botao--secundario:
    backgroundColor: "{colors.surface-2}"
    textColor: "{colors.text}"
    typography: "{typography.botao}"
    rounded: "{rounded.btn}"
    height: 48px
  et-botao--contorno:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.line-strong}"
    textColor: "{colors.text}"
    typography: "{typography.botao}"
    rounded: "{rounded.btn}"
    height: 48px
  et-botao--contorno-no-escuro:
    backgroundColor: transparent
    borderColor: "{colors.et-line-dark-strong}"
    textColor: "{colors.text-on-dark}"
    hoverTextColor: "{colors.et-gold}"
    rounded: "{rounded.btn}"
  et-botao--fantasma:
    backgroundColor: transparent
    hoverBackground: "{colors.surface-2}"
    textColor: "{colors.text}"
    rounded: "{rounded.btn}"
  et-botao--confirmar:
    backgroundColor: "{colors.green-bg}"
    borderColor: "{colors.green}"
    textColor: "{colors.green-ink}"
    fontWeight: 700
    rounded: "{rounded.btn}"
  et-botao--perigo:
    backgroundColor: "{colors.red-bg}"
    textColor: "{colors.red-ink}"
    hoverBackground: "{colors.red}"
    rounded: "{rounded.btn}"
  et-botao--destrutivo:
    backgroundColor: "{colors.red}"
    textColor: "{colors.surface}"
    fontWeight: 700
    rounded: "{rounded.btn}"
  et-campo:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.line-strong}"
    focusBorderColor: "{colors.et-gold-dark}"
    focusRing: "0 0 0 3px rgba(245,185,20,.35)"
    textColor: "{colors.text}"
    typography: "{typography.body-md}"
    rounded: "{rounded.btn}"
    height: 48px
    padding: "0 {spacing.sp-4}"
  et-interruptor:
    trackColor: "{colors.paper-2}"
    trackBorder: "{colors.line-strong}"
    thumbColor: "{colors.surface}"
    thumbBorder: "{colors.text-3}"
    checkedTrackColor: "{colors.et-black}"
    checkedThumbColor: "{colors.et-gold}"
    rounded: "{rounded.pill}"
    width: 44px
    height: 24px
    rowHeight: 44px
  et-selo:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.line-strong}"
    typography: "{typography.micro-caps}"
    rounded: "{rounded.selo}"
    padding: "3px {spacing.sp-2}"
  et-aviso:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.line-strong}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.btn}"
    padding: "{spacing.sp-3} {spacing.sp-4}"
  et-cartao:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.line}"
    textColor: "{colors.text}"
    titleTypography: "{typography.display-h2}"
    rounded: "{rounded.painel}"
    padding: "clamp(20px, 3vw, 32px)"
    shadow: "0 1px 2px rgba(26,22,10,.05), 0 10px 26px -18px rgba(26,22,10,.35)"
  et-metrica:
    backgroundColor: "{colors.et-surface-dark}"
    borderColor: "{colors.et-line-dark}"
    textColor: "{colors.text-on-dark}"
    valueColor: "{colors.et-gold}"
    valueTypography: "{typography.display-metrica}"
    rounded: "{rounded.card}"
    padding: "{spacing.sp-5} {spacing.sp-6}"
  et-plano:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.line}"
    nameTypography: "{typography.display-plano}"
    priceTypography: "{typography.display-preco}"
    rounded: "{rounded.card}"
    padding: "{spacing.sp-6}"
  et-plano--destaque:
    backgroundColor: "{colors.et-surface-dark}"
    borderColor: "{colors.et-line-dark}"
    textColor: "{colors.text-on-dark}"
    priceColor: "{colors.et-gold}"
    rounded: "{rounded.card}"
    padding: "{spacing.sp-8} {spacing.sp-7}"
    shadow: "0 0 0 1px rgba(245,185,20,.22), 0 22px 60px -30px rgba(245,185,20,.35)"
  et-dialogo:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.line}"
    borderTop: "4px solid {colors.et-gold}"
    titleTypography: "{typography.display-h2}"
    rounded: "{rounded.painel}"
    padding: "{spacing.sp-7}"
    width: 480px
    backdrop: "rgba(0,0,0,.7) + blur(4px)"
  et-tabela:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.line}"
    headerBackground: "{colors.surface-2}"
    headerTextColor: "{colors.text-2}"
    headerTypography: "{typography.micro-caps}"
    bodyTypography: "{typography.body-sm}"
    cellPadding: "{spacing.sp-3} {spacing.sp-4}"
    rowHover: "{colors.surface-2}"
    rounded: "{rounded.card}"
  et-tabs-lista:
    trackBackground: "{colors.surface-2}"
    activeBackground: "{colors.surface}"
    textColor: "{colors.text-2}"
    activeTextColor: "{colors.text}"
    rounded: "{rounded.btn}"
    padding: 3px
  et-menu-lista:
    backgroundColor: "{colors.surface}"
    borderColor: "{colors.line}"
    itemRounded: "{rounded.control}"
    rounded: "{rounded.btn}"
    shadow: "0 2px 4px rgba(26,22,10,.06), 0 18px 40px -24px rgba(26,22,10,.45)"
  et-tooltip:
    backgroundColor: "{colors.et-black}"
    borderColor: "{colors.et-line-dark}"
    textColor: "{colors.text-on-dark}"
    typography: "{typography.body-xs}"
    rounded: "{rounded.control}"
  et-toast:
    backgroundColor: "{colors.et-surface-dark-2}"
    borderColor: "{colors.et-line-dark}"
    textColor: "{colors.text-on-dark}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.btn}"
  et-vazio:
    backgroundColor: "{colors.surface-2}"
    border: "1px dashed {colors.line-strong}"
    rounded: "{rounded.card}"
    padding: "{spacing.sp-6}"
  app-header:
    backgroundColor: "{colors.et-black}"
    borderColor: "{colors.ink-3}"
    textColor: "{colors.text-on-dark}"
    activeItemBackground: "{colors.et-gold}"
    activeItemText: "{colors.et-black}"
    rounded: "{rounded.painel}"
    padding: "{spacing.sp-3} {spacing.sp-5}"
  admin-header:
    backgroundColor: "{colors.et-black}"
    width: 236px
    rounded: "{rounded.painel}"
    padding: "{spacing.sp-6} {spacing.sp-5}"
  bottom-nav:
    backgroundColor: "rgba(10,10,10,.94)"
    backdropFilter: "blur(10px)"
    activeItemBackground: "{colors.et-gold}"
    activeItemText: "{colors.et-black}"
    rounded: "{rounded.painel}"
    itemHeight: 52px
---

## Visão geral

A Extreme Team é uma academia de lutas e musculação, e este sistema é onde alunos, professores e administradores resolvem a rotina: cadastro, plano, mensalidade, Pix, turmas e presença. A marca é o dragão preto com o X dourado. O visual parte da própria arte: **preto puro como palco** e **dourado como sinal**.

São duas superfícies com papéis fixos:

- **O palco escuro** (`{colors.et-black}` e `{colors.et-surface-dark}`) carrega a identidade: cabeçalho, barra lateral do admin, hero da página inicial, login, cartões de métrica, plano em destaque, toasts e navegação inferior. A logo só aparece aqui.
- **O papel** (`{colors.et-cream}` com cartões `{colors.surface}` brancos) carrega o trabalho: tabelas, formulários, listas, detalhes. É onde a pessoa lê e preenche.

O dourado (`{colors.et-gold}`) não é decoração. Ele marca a ação principal do bloco (botão em gradiente), o item ativo da navegação (pastilha sólida), o foco de teclado, a borda de cima dos diálogos e os números que importam sobre o escuro (métricas, preço do plano em destaque). Fora disso, não aparece.

A tipografia tem duas vozes que não se misturam. **Bebas Neue** (só peso 400, só caixa alta) faz títulos e números grandes, com cara de cartaz de luta. **Inter** faz todo o resto: texto, rótulos, botões, tabelas, formulários.

Os componentes seguem a estrutura do shadcn/ui (Button, Input, Badge, Alert, Card, Dialog, Tabs, DropdownMenu, Tooltip, Accordion, DataTable, Toast), mas com a marca da academia no lugar do cinza neutro. Tudo vive com o prefixo `.et-` e nomes em português.

**Características principais:**
- Preto `#000` puro em toda superfície que leva logo: a arte oficial tem fundo preto e qualquer "quase preto" desenha um retângulo em volta dela.
- Um botão dourado em gradiente por bloco. As outras ações usam contorno, fantasma, secundário ou link.
- Títulos em Bebas Neue caixa alta, sem negrito (a fonte não tem; `font-synthesis-weight:none` impede o negrito falso).
- O fundo do papel tem quatro formas radiais em baixa opacidade (ouro, verde floresta, barro e preto), presas numa camada fixa. É a única textura do sistema.
- Cabeçalhos escuros flutuam arredondados sobre o papel, afastados das bordas (16 px no topo, 16–32 px nas laterais), em vez de colar na borda da tela.
- Movimento contido: uma entrada por tela, e o resto só se mexe quando a pessoa age.

## Cores

### Marca
- **Preto** (`{colors.et-black}` — `#000000`): palco da marca. Cabeçalho, barra lateral, hero, cartão de login, fundo do avatar, tooltip.
- **Preto suave** (`{colors.et-black-soft}` — `#0A0A0A`): fundo escuro sem logo por perto.
- **Superfície escura** (`{colors.et-surface-dark}` — `#161616`): cartões sobre o escuro (métrica, plano em destaque, diálogo escuro).
- **Superfície escura 2** (`{colors.et-surface-dark-2}` — `#202020`): toasts e aviso de cookies, que flutuam sobre qualquer fundo.
- **Ouro** (`{colors.et-gold}` — `#F5B914`): ação e estado ativo. Pastilha do item ativo, borda de cima do diálogo, valor de métrica, anel de progresso, letra do avatar.
- **Ouro claro → ouro → ouro escuro** (`#FFE27A` → `#F5B914` → `#B7790A`, 135°): o gradiente do botão principal. Não use em outro lugar.
- **Ouro escuro** (`{colors.et-gold-dark}` — `#B7790A`): o dourado que aparece sobre o claro. O `#F5B914` some no papel, então seta de ordenação, chevron aberto do acordeão, foco de campo e selo de destaque usam o escuro.
- **Linha dourada** (`{colors.et-line-dark}` — dourado a 22%; forte a 50%): borda de cartão e de botão de contorno sobre o escuro.

### Superfícies claras
- **Papel** (`{colors.et-cream}` — `#F6F1E6`): fundo de toda página.
- **Papel 2** (`{colors.paper-2}` — `#E3DED1`): realce sob o cursor em cabeçalho de tabela e área de upload.
- **Cartão** (`{colors.surface}` — `#FFFFFF`): painéis de seção, campos, tabelas, diálogos.
- **Faixa** (`{colors.surface-2}` — `#F6F3EC`): cabeçalho de tabela, trilho das abas, estado vazio, botão secundário, linha sob o cursor.
- **Linha** (`{colors.line}` — `#DFDACC`) e **linha forte** (`{colors.line-strong}` — `#C5BEAC`): bordas de cartão e de campo.

### Texto
- **Texto** (`{colors.text}` — `#16181A`): corpo e títulos no claro.
- **Texto 2** (`{colors.text-2}` — `#4C5155`): descrições, cabeçalho de tabela, ajuda de campo.
- **Texto 3** (`{colors.text-3}` — `#63686D`): placeholder e notas curtas ("Opcional"). Os três passam de 4.5:1 sobre o papel.
- **Sobre o escuro** (`{colors.text-on-dark}` — `#F4F1E8`; apagado `{colors.text-on-dark-muted}` — `#A9ADB1`).

### Situações
Cada situação tem uma trinca para o claro (cor de borda / fundo / tinta do texto) e uma versão para o escuro:

| Tom | Claro (fundo · tinta) | Escuro (tinta) | Situações |
|---|---|---|---|
| ok | `#DFEEE7` · `#14503A` | `#7EDBA6` | pago, plano ativo, acesso ativado |
| alerta | `#FBEFC6` · `#5F4A00` | `#FFD666` | pendente, em análise, aguardando análise, a pagar |
| perigo | `#F7E1DD` · `#7C2C22` | `#FF9C99` | vencido (`atrasado` no banco), recusado |
| info | `#DDE6F5` · `#1A3E6C` | `#A9C6F5` | em processamento, reembolsado, convite enviado |
| neutro | `#E4E2DC` · `#41454A` | — | cancelado, sem plano, acesso não ativado |

A cor nunca comunica sozinha: o selo sempre traz o nome da situação escrito.

### Decorativas
**Barro** (`#B9541F`) e **floresta** (`#1C4A38`) só existem nas formas abstratas do fundo. Nunca indicam situação.

## Tipografia

### Famílias
1. **Bebas Neue** (Google Fonts) para títulos e números grandes. Só existe em peso 400 e só faz sentido em caixa alta. Substitutos: Barlow Condensed, Impact.
2. **Inter** (Google Fonts), pesos 400, 500, 600 e 700, para todo o resto. Substitutos: Segoe UI, system-ui.

### Hierarquia

| Token | Tamanho | Peso | Altura de linha | Uso |
|---|---|---|---|---|
| `{typography.display-hero}` | clamp(48px, 5vw, 72px); 38–52px no celular | 400 | 0.92 | Título do hero ("DESPERTE SUA FORÇA. VÁ AO EXTREMO."). O trecho em `<em>` fica dourado. |
| `{typography.display-h1}` | clamp(32px, 3.6vw, 44px) | 400 | 1.02 | Título de página (`.page-title`). |
| `{typography.display-h2}` | clamp(24px, 2.6vw, 30px) | 400 | 1.1 | Título de cartão de seção e de diálogo. |
| `{typography.display-metrica}` | clamp(38px, 4.4vw, 52px) | 400 | 1 | Valor de métrica, em dourado, com algarismos tabulares. |
| `{typography.display-preco}` | clamp(44px, 5vw, 56px) | 400 | 0.95 | Preço por mês no cartão de plano. |
| `{typography.display-plano}` | 28px | 400 | 1 | Nome do plano. |
| `{typography.body-lg}` | 18px | 400 | 1.55 | Texto de abertura. |
| `{typography.body}` | 16px | 400 | 1.55 | Corpo padrão. |
| `{typography.body-md}` | 15px | 400 | 1.5 | Valor digitado em campo; título do acordeão (600). |
| `{typography.body-sm}` | 14px | 400 | 1.6 | Descrição de cartão, células de tabela, avisos, toasts. |
| `{typography.rotulo}` | 14px | 600 | 1.4 | Rótulo de campo. |
| `{typography.botao}` | 14px | 600 (principal: 700, +0.02em) | 1.2 | Botões. Pequeno: 13px; grande: 15px. |
| `{typography.body-xs}` | 13px | 400 | 1.5 | Ajuda de campo, erro de campo (600), tooltip (500). |
| `{typography.micro-caps}` | 12px | 700 | 1.4 | Cabeçalho de tabela (+0.08em), selo de situação (+0.04em), eyebrow (+0.1em). |

### Princípios
- **Bebas para chamar, Inter para ler.** Bebas nunca carrega parágrafo, rótulo ou botão.
- **Nunca peça `font-weight` 600/700 em Bebas.** Não existe; o navegador inventaria um negrito borrado.
- **Valores monetários, datas e contagens usam `font-variant-numeric: tabular-nums`**, para alinhar em coluna.
- **Texto da interface em português do Brasil, em frase normal.** A caixa alta fica para os títulos em Bebas, o cabeçalho de tabela e o selo de situação.
- **Formato:** `R$ 1.234,56` (filtro Jinja `|moeda`) e `dd/mm/aaaa`, fuso America/Fortaleza.

## Layout

### Espaçamento
- **Base de 4 px:** `{spacing.sp-1}` 4 · `sp-2` 8 · `sp-3` 12 · `sp-4` 16 · `sp-5` 20 · `sp-6` 24 · `sp-7` 32 · `sp-8` 40 · `sp-9` 48 · `sp-10` 64 · `sp-11` 80.
- **Cartão de seção:** padding `clamp(20px, 3vw, 32px)`; cabeça com 24 px abaixo e linha divisória.
- **Diálogo:** 32 px (24/20 px no celular).
- **A margem entre cartões é da página, não do cartão.** Dentro de grade, use `gap`, nunca `.a + .a { margin-top }`.

### Altura de controle
- Padrão 48 px, pequeno 40 px, grande 54 px.
- Até 1023 px, todo controle pequeno sobe para **44 px**, o alvo mínimo de toque.

### Contêiner e estrutura
- **Admin:** grade com barra lateral escura de 236 px fixa (`position: sticky`) e conteúdo de até 1240 px.
- **Área do aluno:** conteúdo de até 1100 px, cabeçalho escuro flutuante e, até 720 px, navegação inferior.
- **Público:** cabeçalho e hero formam um palco preto contínuo; o resto da página fica sobre o papel.
- Todas as telas estendem um layout de `templates/layouts/` (`base` → `publico` / `aluno` / `admin` / `professor`).

### Responsivo

| Faixa | Largura | O que muda |
|---|---|---|
| Celular pequeno | ≤ 480px | Rodapé do diálogo empilha os botões em largura total, com a ação principal em cima. |
| Celular | ≤ 640px | Tabelas viram lista; o diálogo vira folha que sobe de baixo, com alça; até 540 px, o cartão de seção usa raio de 22 px. |
| Celular largo | ≤ 720px | Aparece a navegação inferior da área do aluno. |
| Tablet | ≤ 768px | Aparece a barra de CTA fixa no pé da página pública. |
| Tablet largo | ≤ 1023px | Alvos de toque de 44 px; a barra lateral do admin vira barra de topo com as seções roláveis na horizontal. |
| Desktop | ≥ 1024px | Barra lateral fixa; planos numa linha só, com o destaque no meio. |

Tudo funciona de 360 a 1440 px **sem rolagem horizontal**. Para cortar sobra lateral, use `overflow-x: clip` em `html`/`body`: `hidden` transforma o body em contêiner de rolagem e quebra todo `position: sticky`.

## Elevação e profundidade

| Nível | Sombra | Uso |
|---|---|---|
| 0 — plano | nenhuma | Tabela, campo, cartão de plano comum. |
| 1 — cartão | `0 1px 2px rgba(26,22,10,.05), 0 10px 26px -18px rgba(26,22,10,.35)` | Cartão de seção, cabeçalho flutuante. |
| 2 — elevado | `0 2px 4px rgba(26,22,10,.06), 0 18px 40px -24px rgba(26,22,10,.45)` | Menu de ações, barra lateral do admin. |
| 3 — diálogo | `0 30px 70px -20px rgba(0,0,0,.55)` + fundo `rgba(0,0,0,.7)` com `blur(4px)` | Diálogos. |
| Escuro | `0 18px 40px -22px rgba(0,0,0,.8)` | Métrica, toast, tooltip, CTA fixo. |
| Brilho dourado | `0 0 0 1px` dourado 22% + `0 22px 60px -30px rgba(245,185,20,.35)` | Só o plano em destaque. |

As sombras do claro são curtas e com tom quente (`rgba(26,22,10,…)`), nunca cinza puro.

### Profundidade decorativa
- **Formas do fundo:** quatro gradientes radiais fixos atrás do papel (ouro 20% no canto superior direito, floresta 13% no superior esquerdo, barro 11% no inferior esquerdo, preto 7% no inferior direito).
- **Borda brilhante** (`.et-borda-brilho`): um arco dourado gira pela borda do plano em destaque a cada 6 s. Com `prefers-reduced-motion`, a borda fica dourada e parada.
- **Vidro escuro:** navegação inferior e CTA fixo em `rgba(10,10,10,.94)` com `backdrop-filter: blur(10px)`.

## Formas

### Raios

| Token | Valor | Uso |
|---|---|---|
| `{rounded.selo}` | 6px | Selo, caixa de seleção. |
| `{rounded.control}` | 10px | Item de menu, tooltip, área de foco do breadcrumb. |
| `{rounded.btn}` | 12px | Botão, campo, aviso, trilho das abas, menu, toast. |
| `{rounded.card}` | 18px | Métrica, plano, tabela, estado vazio, upload, CTA fixo. |
| `{rounded.card-mobile}` | 22px | Cartão de seção até 540 px. |
| `{rounded.painel}` | 28px | Cartão de seção, diálogo, cabeçalho flutuante, barra lateral, navegação inferior. |
| `{rounded.pill}` | 999px | Item ativo do cabeçalho, botões de sair/voltar/entrar (`.et-botao--pilula`), ícone do diálogo de alerta. |

A regra é **controle < botão < cartão < painel**. O botão não vira pílula por padrão: ele parece controle, não pastilha.

### Marca e imagens
- **Só as logos oficiais** de `static/imagens/`: `logo-icon.png` (emblema do dragão) e `logo-horizontal-{400,800,1200}.png`, sempre com `srcset` e `sizes` reais.
- **Sempre sobre `#000` puro.** Sobre `#161616` ou sobre brilho dourado, use `mix-blend-mode: lighten` na `<img>` (e `isolation: isolate` no contêiner). Nunca ponha `background`, `border-radius`, borda ou sombra na imagem da logo.
- Nunca estique; a imagem não pode ser renderizada maior que a resolução natural dela.
- `alt="Extreme Team"` quando a logo é a única identificação; `alt=""` quando é decorativa.
- **Avatar:** círculo preto com as iniciais em Bebas dourado e contorno dourado fraco (32 / 44 / 72 px).
- **Ícones:** Lucide (o conjunto do shadcn), traço de 1,7–2 px, `stroke: currentColor`, 16–22 px.

## Componentes

Todos ficam em `static/css/componentes.css`, usam só tokens e têm a classe `.et-*`. O comportamento fica em `static/js/componentes.js`, ligado por atributos `data-*`.

### Botões — `.et-botao` + variante (+ tamanho)
É o único botão do sistema. Não crie regra de botão por página, só de layout (largura, margem).

- **`--principal`:** gradiente dourado, borda `{colors.et-gold-dark}`, texto preto 700. No hover ganha brilho e um halo dourado. **Um por bloco.**
- **`--secundario`:** fundo `{colors.surface-2}`, texto escuro.
- **`--contorno`:** fundo branco, borda `{colors.line-strong}`. É o botão de ação em linha de tabela e o "Cancelar" dos diálogos.
- **`--fantasma`:** sem fundo; o fundo aparece no hover. Usado em botões de ícone, como o gatilho de menu e o fechar.
- **`--link`:** texto com sublinhado que aparece no hover.
- **`--confirmar`:** verde suave, para aprovar um cadastro sem gastar o dourado.
- **`--perigo`:** vermelho suave, que fica sólido no hover. Para recusar ou excluir em linha de tabela.
- **`--destrutivo`:** vermelho sólido. Só para a confirmação final dentro do diálogo.
- **Tamanhos:** `--pequeno` (40 px, 13 px), `--grande` (54 px, 15 px), `--icone` (quadrado). **Forma:** `--pilula`. **Largura:** `--largo` (100%).
- **No escuro** (`.et-escuro` ou cabeçalhos), contorno, fantasma, secundário e link passam a texto claro com borda dourada a 50%, e o dourado aparece no hover.
- **Carregando** (`.et-carregando`): ganha um anel girando antes do rótulo e para de responder a cliques.

### Formulários
- **`.et-campo`** vai direto no `<input>`, `<select>` ou `<textarea>`. Tem 48 px, fundo branco, borda `{colors.line-strong}` e raio de 12 px. No foco, a borda fica ouro escuro com um halo dourado de 3 px; no foco por teclado, aparece o anel completo. Quando inválido (`aria-invalid="true"`), a borda e o halo ficam vermelhos. `--bloqueado` deixa o campo não editável e com fundo de faixa; `--pequeno` serve a barras de ferramentas. O select usa o chevron do Lucide.
- **Rótulo** (`.field label`): 14 px, peso 600, com 8 px até o campo. Notas como "Opcional" vão em `<small>` alinhado à direita, em `{colors.text-3}`.
- **Ajuda** (`.field-hint`): 13 px em `{colors.text-2}`. **Erro** (`.field-erro`): 13 px, peso 600, em `{colors.red-ink}`, escrito ao lado do campo e não no topo do formulário.
- **`.et-caixa`** (checkbox e radio): 20 px, raio de 6 px, marcada em preto com sinal branco. No escuro, fica dourada com sinal preto. O tamanho e a cor vêm de `--caixa-*`.
- **`.et-interruptor`** (Switch): checkbox nativo com `role="switch"` para uma configuração que liga e desliga (destacar plano, exibir contato no site, publicar perfil, lançar a primeira mensalidade). Trilho de 44 × 24 px: desligado em `{colors.paper-2}` com polegar branco contornado; ligado em preto com polegar dourado. No escuro, o trilho ligado fica dourado e o polegar preto (`--interruptor-*`). Sempre dentro de `.et-interruptor-linha`, um `<label>` de 44 px de altura em que a linha inteira é o alvo de toque, com o interruptor antes do rótulo. Use a macro `interruptor()` de `ui.html`: o nome acessível é só o rótulo, e a ajuda vira descrição. A caixa continua para aceite (termos), "lembrar meu usuário", ação ao salvar ("remover foto atual") e chamada de presença.
- **`.et-upload`**: área tracejada de 140 px que fica dourada ao arrastar, com pré-visualização e erro em vermelho suave.
- **`.et-copiavel`**: campo somente leitura com botão de copiar ao lado (o "Pix copia e cola").

### Selos e avisos
- **`.et-selo`** é o badge: 12 px, peso 600, raio de 6 px. Os tons são `--ok`, `--alerta`, `--perigo`, `--info`, `--neutro` e `--destaque` (contorno ouro escuro). Para situação de mensalidade, plano ou acesso, use `et-selo--situacao` (caixa alta com ponto colorido) + `data-situacao="<estado>"`. O mapa estado → tom fica só no CSS, e o JS só troca o atributo.
- **`.et-aviso`** é o alerta (`role="alert"`): raio de 12 px, 14 px, com os mesmos tons. Um `<svg>` como primeiro filho vira o ícone na margem esquerda. Dentro de `.auth-shell` e `.et-escuro`, usa as versões escuras.

### Cartões e contêineres
- **`.et-cartao`** é o painel claro de cada seção: fundo branco, borda `{colors.line}`, raio de 28 px e sombra nível 1. A cabeça (`.et-cartao-cabeca`) tem título em Bebas, descrição em 14 px e uma ação opcional à direita (`.et-cartao-acao`), separadas do conteúdo por uma linha.
- **`.et-metrica`** é o cartão escuro que ancora o painel do admin e a área do aluno: rótulo apagado, valor grande em Bebas dourado e detalhe em 13 px. As variantes `--ok`, `--alerta` e `--perigo` trocam a cor do valor.
- **`.et-plano`** é claro e discreto. O **`.et-plano--destaque`** é escuro, maior, com preço dourado, selo, brilho dourado e borda que gira. Na grade (`.et-planos`), o destaque fica no topo no celular, ocupa a linha inteira no tablet e fica no meio da linha no desktop.
- **`.et-vazio`** é o estado vazio: faixa com borda tracejada, título 700 e texto escrito ("Nenhum pagamento pendente"), nunca dado inventado.
- **`.et-anel`** é o anel de progresso de 104 px (presenças no mês): trilho dourado fraco, arco dourado e número em Bebas no centro.
- **`.et-linha-tempo`**: passos com marca circular, vertical no celular e horizontal a partir de 560 px. O estado de cada passo vem escrito, e a cor só reforça.

### Diálogos — `<dialog class="et-dialogo">`
- Usa o `<dialog>` nativo: foco preso, Esc e fundo inerte vêm do navegador.
- Fundo branco, raio de 28 px, **borda de cima dourada de 4 px** (vermelha com `data-variant="danger"`), largura padrão de 480 px (`--dialogo-largura`).
- Cabeça com título em Bebas e descrição em 14 px. O ícone do alerta fica num círculo âmbar (vermelho quando a ação é destrutiva).
- O rodapé alinha os botões à direita: a ação que a pessoa veio fazer fica na ponta e o "Cancelar" (contorno) logo antes dela.
- Entra crescendo de 96% em 240 ms e sai em 180 ms. Até 640 px, vira **folha que sobe de baixo**, com alça.
- `--escuro` é a variante do login: fundo `{colors.et-surface-dark}` com borda dourada.

### Navegação
- **Cabeçalho do aluno e do professor** (`.app-header`): faixa preta arredondada (28 px) flutuando afastada das bordas. Os links são claros e apagados e ficam dourados no hover; o item ativo é uma **pastilha dourada sólida com texto preto** e `aria-current="page"`. Sair, voltar e entrar são `.et-botao` pequenos em pílula.
- **Barra lateral do admin** (`.admin-header`): coluna preta de 236 px, fixa, com o emblema no topo e um selo dourado discreto no rodapé. Até 1023 px, vira barra de topo com as seções roláveis na horizontal, com degradê só do lado que ainda tem seção escondida.
- **Navegação inferior** (`.bottom-nav`, área do aluno até 720 px): barra de vidro escuro flutuando a 12 px do fim, acima da área segura do iPhone. Os itens têm 52 px, ícone de 22 px e rótulo de 11 px; o ativo fica em dourado sólido.
- **Abas** (`.et-tabs`): controle segmentado sobre um trilho `{colors.surface-2}`; a aba ativa é uma pastilha branca com sombra leve. Setas, Home e End funcionam pelo `componentes.js`.
- **Menu de ações** (`.et-menu`): o gatilho é um botão fantasma de ícone. A lista branca entra com zoom; o item perigoso fica em vermelho e grupos são separados por `<hr>`.
- **Breadcrumb**: herda a cor do contêiner, usa barra como separador e tem link sublinhado com alvo de 44 px.

### Dados
- **`.et-tabela`**: contêiner branco com raio de 18 px, ferramentas no topo (busca até 320 px) e rolagem com cabeçalho fixo. O cabeçalho usa faixa `{colors.surface-2}` com 12 px, peso 700 e caixa alta. A ordenação (`th[aria-sort]`) usa setas do Lucide, apagadas até a coluna ser escolhida e em ouro escuro quando ativas. As células têm 14 px e a linha sob o cursor fica em `{colors.surface-2}`. Busca e ordenação só existem em tabela sem paginação.
- **Lista no celular** (`.table-stack` no `.et-tabela-rolagem`, toda tabela tem): até 640 px, cada linha vira um cartão com rótulo (`data-label`) e valor, a moldura do componente sai e a lista cresce com a página. **Cartão compacto:** a célula `.celula-titulo` (quem ou o quê da linha: aluno, turma, professor, competência) vira a cabeça do cartão, sem rótulo e em 600, e o menu ⋮ da `.celula-menu` fica no canto dela. Ações com vários botões ficam em `.acao-cell`, empilhadas no pé.
- **Gráficos**: SVG gerado no servidor (Jinja), com tabela ou legenda acessível. Sem biblioteca de gráfico.

### Avisos flutuantes
- **Toast** (`.et-toast`): escuro em qualquer tela, com ícone na cor do tom e fechar como botão fantasma. Fica no canto superior direito no desktop e embaixo no celular, acima da navegação inferior.
- **Tooltip** (`.et-tooltip`): preto com texto claro de 13 px e entrada com zoom. É criado pelo JS e sempre acompanhado de `aria-label`.
- **CTA fixo** (`.et-cta-fixo`): barra de conversão de vidro escuro no pé da página pública, até 768 px.
- **Aviso de cookies** (`.et-consentimento`): cartão escuro no pé da tela em que "recusar" tem o mesmo peso de "aceitar".

### Foco
Todo elemento focável mostra um anel de dois tons: `outline` de 2 px em `--focus-ink` (preto no claro, dourado no escuro) com 2 px de afastamento, mais um halo dourado de 5 px. Bloco escuro novo ganha a classe `.et-escuro` para inverter o anel e as cores dos botões.

### Movimento
- **Curvas:** entrada `cubic-bezier(.22,1,.36,1)`, saída `cubic-bezier(.4,0,1,1)`.
- **Durações:** 180 ms (resposta ao toque), 280 ms (mudança de estado), 420 ms (entrada de tela). Nada passa de meio segundo nem se repete, exceto a borda do plano em destaque.
- **Uma entrada por tela** (`.entra`, subindo 10 px no bloco de abertura). O resto só se mexe quando a pessoa age.
- **Deslize entre telas** por View Transitions: cabeçalho, navegação inferior e item ativo têm nome próprio e deslizam juntos.
- `prefers-reduced-motion: reduce` desliga zoom, deslize e giro, deixando no máximo um esmaecimento curto.

## O que fazer e o que evitar

### Faça
- Use **só tokens**: `--et-*` em código novo (os aliases `--paper`, `--ink`, `--surface`, `--line`, `--sp-*`, `--fs-*` continuam valendo). Se faltar um token, crie-o em `tokens.css`; não escreva hexadecimal solto.
- Ponha **um** `.et-botao--principal` por bloco. A segunda ação é contorno, secundário ou link.
- Use `{colors.et-gold-dark}` para dourado sobre o papel, e `{colors.et-gold}` só sobre o escuro ou como fundo de pastilha.
- Escreva a situação no selo ("Pago", "Vencido"), não só a cor.
- Garanta alvo de toque ≥ 44 px, foco visível, contraste AA e `prefers-reduced-motion` respeitado.
- Escreva os estados vazios em frase completa e use dados reais do banco.
- Ao refazer uma tela, **apague as classes antigas do HTML e as regras antigas do CSS**, em vez de empilhar regra nova por cima. Antes de dar por pronto, rode `grep -rn "<classe-antiga>" templates static`.
- Abra a tela no navegador (1440 e 390 px) antes de dar por pronto. A suíte de testes não vê CSS.

### Evite
- Gradiente dourado fora do botão principal; dourado como enfeite de título, borda de cartão claro ou fundo de seção.
- `font-weight` acima de 400 em Bebas Neue, Bebas em parágrafo ou botão, e Inter em caixa alta fora de cabeçalho de tabela e selo.
- Logo redesenhada em SVG, marca digitada em texto ("EXTREME TEAM" em Bebas no lugar da imagem), logo esticada ou com fundo que revela o retângulo.
- Eyebrow em caixa alta sobre todo título, numeração 01/02/03 onde não há sequência, a mesma informação repetida em dois blocos e fade-in em toda seção. São vícios de página gerada.
- Barro e floresta para indicar situação; cinza neutro do shadcn no lugar das cores da marca.
- `overflow-x: hidden` em `html`/`body` (use `clip`) e `.a + .a { margin-top }` dentro de grade (use `gap`).
- Handlers inline (`onclick=`) e `<script>` de CDN: a CSP proíbe. O JS vai em arquivo em `static/js/` ou inline com `nonce`.

## Onde isso vive no código

| Peça | Arquivo |
|---|---|
| Tokens (fonte única) | `static/css/tokens.css` |
| Aliases, base, campos, foco, movimento, navegação inferior | `static/css/theme.css` (importa `tokens.css` e `componentes.css`) |
| Componentes `.et-*` | `static/css/componentes.css` |
| Cabeçalhos e barra lateral do admin | `static/css/extreme.css` (carregado por último) |
| Comportamento (abas, menu, tooltip, tabela, upload, toast) | `static/js/componentes.js` |
| Macros Jinja | `templates/components/` (`ui.html`, `avatar.html`, `cartao_plano.html`, `linha_tempo.html`, `breadcrumb.html`, `toasts.html`…) |
| Layouts | `templates/layouts/` |
| Logos e favicons | `static/imagens/` (originais intactos em `static/imagens/marca/`) |

A stack é Flask + Jinja, sem build de front-end, sem Tailwind e sem React. Componentes do shadcn/ui entram **portados** para `.et-*`, nunca via `npx shadcn add`.
