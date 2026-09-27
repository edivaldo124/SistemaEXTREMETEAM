# Etapa 3 — home com os planos + termos

Branch `componentes-front`. Arquivos EXCLUSIVOS por frente; nada de git que escreva, não suba servidor,
não rode `graphify update`. Leia REDESIGN_CONTRATO.md seções 2 e 7 e `tools/redesign/TAREFA_ETAPA2_COMPONENTES.md`
(os componentes já existem em `templates/components/` e `static/css/componentes.css`; a vitrine de referência é
`tools/redesign/vitrine/`).

## Dados da home (Claude entrega em servidor.py — não edite)

A rota `/` passa `vitrine_planos`: lista em ordem de duração, cada item um dict com EXATAMENTE as chaves que
`components/cartao_plano.html` usa: `id`, `nome`, `preco_total`, `preco_mes`, `meses`, `duracao_texto` ("3 meses",
"1 ano"), `economia` (Decimal ou None, em relação ao plano de 30 dias), `recomendado` (bool — o admin marca um plano
"em destaque"; sem marcação, vale o de menor preço por mês), `url_matricula` ("/cadastrar" para visitante,
"/perfil#planos" para aluno logado) e `texto_botao` ("Matricular agora"). Lista vazia quando não há planos.
Continuam existindo `professores_publicos` e `academia`.

## Agente A — `templates/index.html` e `static/css/index.css`

- Seção de planos LOGO ABAIXO do hero e ANTES de "Nosso método", usando `secao_planos(vitrine_planos)` de
  `components/cartao_plano.html` (sem lista → o estado vazio da macro). Título da seção: `Planos` (h2) e uma frase:
  `Escolha por quanto tempo quer treinar. Quanto mais longo o plano, menor o valor por mês.`
- Em 1440×900 o topo dos cartões de plano precisa aparecer na primeira tela (sem rolar): encurte o hero
  (altura, espaçamentos, tamanho do emblema) sem trocar os textos nem o emblema. No celular o recomendado vem primeiro
  (a macro já faz). Os dois botões do hero continuam.
- Faixa "Comece / Mantenha / Supere": mantenha (o teste cobra os textos), mas ela não pode empurrar os planos para
  fora da primeira tela — pode ir para depois dos planos ou ficar mais baixa.
- Professores públicos: use `avatar(nome, foto_url, 'lg')` de `components/avatar.html` quando o professor NÃO tem foto
  (hoje é um `<span>` com a inicial); com foto, mantenha o retrato atual.
- Não mexa em mais nada: modal de login, links, `id`s, `data-*` e textos existentes ficam como estão
  (teste: `tests/test_publicas_redesign.py::test_landing_page` e `tests/test_layouts.py`). Apague CSS que ficar sem uso.
- Conferência: `env -u DATABASE_URL .venv/bin/python -m pytest -q -p no:cacheprovider -W ignore tests/test_publicas_redesign.py tests/test_layouts.py tests/test_home_planos.py`
  (o último é do Claude e pode ainda não existir — ignore se faltar). `test_landing_page` já falhava antes por procurar
  "VÁ AO EXTREMO." — o Claude atualiza esse teste; não o edite.

## Antigravity — `termos_de_servico.html`, `politica_privacidade.html`, `termos_responsabilidade.html` + `static/css/termos.css` (novo)

- Sumário no topo: `<nav class="termos-sumario" aria-label="Nesta página"><ol>` com um link âncora por seção
  (é uma sequência de verdade: as seções já são numeradas).
- Cada `<section>` vira `<details class="et-acordeao" id="secao-N" open><summary><h2>N. Título</h2></summary>
  <div class="et-acordeao-corpo">...texto...</div></details>` — **todas ABERTAS** por padrão (decisão do dono):
  o accordion só serve para recolher o que já foi lido. Texto legal INALTERADO, palavra por palavra.
- Tipografia de leitura: coluna de texto com no máximo ~70 caracteres (`max-width: 68ch`), `line-height` ~1.7,
  Inter no corpo, títulos em Bebas (`--et-font-display`, peso 400). Mantenha o `account-header` e a nota final.
- `static/css/termos.css` novo, só tokens, linkado nos 3 templates pelo bloco `estilos` (depois das folhas atuais).
  Apague do HTML classes que deixarem de ser usadas. Não edite `auth.css`/`cadastro.css` (outras telas usam).
- Links do sumário para uma seção fechada: o Claude faz o JS que abre o `<details>` ao navegar por âncora.
- Testes que cobram essas páginas: `tests/test_publicas_redesign.py` (test_termos_*, test_politica_*) e
  `tests/test_termos_responsabilidade.py` — preserve os textos que eles procuram.
- NÃO rode pytest, NÃO suba servidor: edite e devolva o resumo.
