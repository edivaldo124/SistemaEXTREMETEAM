# Etapas 4 a 6 — aluno, admin, professor (aplicar os componentes nas páginas)

Branch `componentes-front`. Três frentes em paralelo + orquestrador. Leia antes, inteiros:
REDESIGN_CONTRATO.md seções 2, 3 e 7; `tools/redesign/TAREFA_ETAPA2_COMPONENTES.md` (ganchos de JS e macros);
`templates/components/{avatar,linha_tempo,breadcrumb,cartao_plano,ui}.html`; `static/css/componentes.css`;
`static/js/componentes.js`. Exemplos vivos: `tools/redesign/vitrine/_a.html` e `_b.html`.

## Regras para todos
- Só os arquivos da SUA lista. Precisa de algo fora dela (token, regra global, macro)? Não edite: peça no relatório.
- Nada de git que escreva, não suba servidor, não rode `graphify update`.
- Preserve rotas, `name=`, `id=`, `data-*` usados por JS e testes, textos que testes procuram
  (`grep -rn "<texto>" tests static/js` antes de mudar). CSRF em todo POST. Nenhum handler inline.
- Ao trocar markup antigo por componente, APAGUE a classe antiga do HTML e a regra antiga do CSS da sua lista
  (grep antes de encerrar). Sem eyebrow novo, sem 01/02/03, sem fade-in; gradiente só no botão primário.
- Tabela: busca/ordenação no cliente (`data-tabela-busca`, `data-ordenar`) SÓ em tabelas sem paginação;
  as paginadas (`components/paginacao.html`) ficam só com o visual `.et-tabela` e os filtros de servidor que já existem.
- Botão com carregamento (`data-enviando`): só em formulários que NÃO têm JS próprio de envio
  (pagamento.js, pix.js, checkout.js e comprovante.js já tratam os deles — não duplique, erro 5 da seção 7).
- Menu de ações por linha: ações destrutivas continuam passando pelo `confirm_modal` (`data-confirm-modal` no form).
- Não crie números/estatísticas/depoimentos: só dados que a rota já entrega.
- Conferência (agentes Claude): `env -u DATABASE_URL .venv/bin/python -m pytest -q -p no:cacheprovider -W ignore <arquivos das suas rotas> tests/test_layouts.py`.
  Linha de base da suíte: 5 failed (test_email_gmail ×2, test_mercado_pago_oauth cifra, test_pix_rotas webhook,
  test_seguranca CPF) — nenhum outro pode falhar. Não edite testes existentes; se um texto precisa mudar, anote.
- Conferência visual (agentes Claude): a instância descartável JÁ está rodando em http://localhost:4002 (não suba outra,
  não pare). Use `SAIDA=<scratchpad>/<seu-nome> node tools/redesign/shot.mjs jobs.json` (perfis anon/aluno/admin/prof;
  formato em REDESIGN_CONTRATO.md seção 8). 1440 e 390 px de cada página sua; overflowX 0; console sem erro
  (exceto o 502 do Pix em /perfil/pagamento, que é falta de rede). Olhe os PNGs e corrija antes de encerrar.
  O scratchpad é /tmp/claude-1000/-home-edivaldo-PycharmProjects-SistemaEXTREMETEAM/8999844d-c27b-4e4a-a222-fe04676cb873/scratchpad.

## Agente A — área do aluno + pagamento
Arquivos: `templates/pgUsuario.html`, `pagamento.html`, `comprovante.html`, `checkout_continuar.html`, `checkout_retorno.html`,
`templates/components/{plano_situacao,mensalidade_acao,cartao_plano,linha_tempo,avatar}.html`,
`static/css/{pgUsuario,planos,pagamento,comprovante}.css`, `static/js/{pgUsuario,pagamento,checkout,comprovante,mensalidades_filtro}.js`.
- pgUsuario: avatar do aluno; cartões de plano com o MESMO componente da home (`cartao_plano`). Os botões de contratar/
  renovar/agendar são formulários POST com `plano`/`acao` — estenda a macro com um slot (`{% call %}`/`caller()`) para a
  ação, sem quebrar o uso da home; linha do tempo da mensalidade atual; tabela de mensalidades `.et-tabela`
  (sem paginação → busca/ordenação liberadas se fizer sentido); as telas por hash/bottom-nav continuam como estão.
- pagamento: resumo do plano em cartão; linha do tempo com o status real; "Copiar código" do Pix confirma com
  `window.etToast('Código Pix copiado.', 'sucesso')` (procure a cópia em pix.js/pagamento.js — pix.js NÃO é seu:
  se a cópia estiver lá, peça no relatório); corrija a caixa vermelha vazia que aparece abaixo de
  "Ir para outras formas de pagamento" (existia antes do redesign).
- comprovante: upload com pré-visualização (`data-upload`, tipos/limite = os que o servidor aceita: confira na rota),
  linha do tempo.
- checkout_continuar / checkout_retorno: linha do tempo com o status real e estado claro de sucesso/pendente/falha com
  o próximo passo (texto já existente; não invente status).

## Agente B — admin
Arquivos: `templates/pgAdm.html`, `dt_aluno.html`, `admin_aluno_novo.html`, `admin_avisos.html`, `admin_academia.html`,
`templates/components/admin_nav.html`, `static/js/admin_nav.js`, `static/css/{pgAdm,dt_aluno,admin_academia}.css`,
`static/js/pgAdm.js`, e em `static/css/extreme.css` SOMENTE o bloco da barra lateral do admin.
ATENÇÃO: `pgAdm.css` e `dt_aluno.css` também são usados por financeiro/turmas/turma/professor (frente Antigravity):
mudanças nelas não podem quebrar essas páginas — prefira seletores escopados pela página.
- pgAdm: métricas com `metrica()` (et-metrica) no lugar dos cards atuais; tabela de alunos `.et-tabela` (paginada: só
  visual) com avatar e menu de ações por linha; planos continuam com o destaque (etapa 3).
- dt_aluno: `breadcrumb` (Painel › nome do aluno), avatar, tabs (Dados / Pagamentos / Presenças / Turmas) sobre os
  blocos que já existem, tabelas, menu de ações.
- admin_aluno_novo: breadcrumb + botão com carregamento. admin_avisos: tabela ou lista + menu de ações + confirm_modal.
- admin_academia: tabs ou accordion por grupo de configuração (fieldsets existentes).
- Barra do admin no celular: hoje "Financeiro" fica cortado atrás de "Sair" (390 px). Corrija.

## Antigravity — financeiro, turmas, professor
Arquivos: `templates/financeiro.html`, `turmas.html`, `turma.html`, `pgProfessor.html`, `professor_editar.html`,
`static/css/{financeiro,turmas,professor_editar}.css`, `static/js/{filtros_financeiro,turma}.js`.
NÃO edite `pgAdm.css`, `dt_aluno.css`, `modal.css`, `pix.css` (compartilhadas): estilos novos vão nas SUAS folhas.
- financeiro: tabela `.et-tabela` (paginada: só visual) com os filtros existentes, badges, menu de ações por linha.
- turmas / turma: tabela, avatar dos alunos, menu de ações, breadcrumb (Turmas › nome da turma) no admin.
- pgProfessor: tabela de turmas/alunos, avatar. professor_editar: upload da foto com pré-visualização (`data-upload`,
  tipos e tamanho que a rota aceita) + botão com carregamento.
- NÃO rode pytest, NÃO suba servidor, NÃO fique aguardando nada: edite e devolva o resumo com a lista de arquivos.

## Orquestrador (Claude)
E-mails (`templates/email/`), testes novos, `theme.css`/`componentes.css`/`modal.css`/`pix.css`, verificação completa
e a junção.
