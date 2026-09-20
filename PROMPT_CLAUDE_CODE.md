# Prompt para o Claude Code — Redesign do SistemaEXTREMETEAM

> Antes de colar: copie a pasta `logo-original/` para dentro do projeto (ex.: `static/img/brand/` ou `public/brand/`, conforme a estrutura) e anexe as 3 imagens de referência das telas na conversa do Claude Code.

---

Você vai redesenhar e completar o front-end do **SistemaEXTREMETEAM**, um sistema web de gestão para a academia de lutas e musculação **Extreme Team**. As 3 imagens anexadas são a referência visual oficial; siga-as o mais fielmente possível em layout, hierarquia e cores.

## 0. Antes de escrever código
1. Explore o repositório inteiro e me diga: framework/linguagem usados, estrutura de pastas, como as rotas/templates estão organizados, como é feita a autenticação e quais tabelas já existem no Supabase.
2. **Mantenha a stack atual.** Não troque framework nem banco. As integrações existentes devem continuar funcionando: **Supabase** (banco/auth), **Brevo** (e-mails) e **Mercado Pago** (pagamentos/PIX).
3. Não exponha nem altere segredos do `.env`. Não faça commit de chaves.
4. Me apresente um plano curto (arquivos que vai criar/alterar e ordem) e espere meu OK antes de implementar.

## 1. Identidade visual (design tokens)
Crie um arquivo central de tokens (CSS custom properties) e use-o em todas as telas.

| Token | Valor | Uso |
|---|---|---|
| `--et-black` | `#0A0A0A` | fundos escuros, sidebar, header |
| `--et-surface-dark` | `#161616` | cards no tema escuro |
| `--et-gold` | `#F5B914` | cor principal, botões primários, item ativo do menu |
| `--et-gold-light` | `#FFE27A` | início do gradiente dourado |
| `--et-gold-dark` | `#B7790A` | fim do gradiente, bordas |
| `--et-green` | `#1F5A3A` | detalhes decorativos, status "Pago/Ativo" (`#22A45D`) |
| `--et-orange` | `#FF8A1F` | detalhes decorativos, alertas |
| `--et-cream` | `#F6F1E6` | fundo claro das páginas |
| `--et-danger` | `#E53935` | "Vencido", "Recusar", "Inativo" |
| `--et-warning` | `#F2A900` | "Pendente", "Em análise" |

- **Tipografia:** títulos e números grandes em **Bebas Neue** (Google Fonts), textos e tabelas em **Inter**. Títulos em caixa alta, como nas referências.
- **Botão primário:** gradiente dourado (`--et-gold-light` → `--et-gold` → `--et-gold-dark`), texto preto, cantos arredondados de 10–12px. **Secundário:** contorno dourado, fundo transparente.
- **Cards escuros:** fundo `--et-surface-dark`, borda 1px dourada com baixa opacidade, leve efeito vidro (backdrop-filter) nas telas de login.
- **Badges de status:** Pago/Ativo = verde, Pendente/Em análise = amarelo, Vencido/Inativo/Recusado = vermelho.
- Responsivo de verdade: desktop, tablet e celular. Foco de teclado visível e contraste acessível.

## 2. Logo oficial (usar SOMENTE a logo original)
A logo da academia é o **dragão preto com o X dourado** dos arquivos da pasta `logo-original/`. Não crie, não redesenhe e não gere outra logo por código (nada de SVG inventado, ícone genérico ou texto estilizado no lugar dela).
- `logo-original/logo-extreme-team-horizontal.png` → "CENTRO DE TREINAMENTO EXTREME TEAM" + dragão. Use no header da página inicial, no rodapé e nos e-mails do Brevo.
- `logo-original/emblema-dragao.png` → só o dragão com o X. Use no topo da sidebar do painel, no card de login, no header da área do aluno, na tela de carregamento e como favicon.
- As duas imagens têm fundo preto: use-as sempre sobre fundo escuro (`--et-black`), sem bordas ou sombras que revelem o retângulo. No painel com conteúdo claro, a sidebar continua preta, então a logo fica sobre ela.
- Gere a partir de `emblema-dragao.png` os favicons (32, 180, 192 e 512 px, recorte quadrado centralizado) e o `manifest.json`.
- Mantenha a proporção original; nunca estique a imagem. Coloque `alt="Extreme Team"`.
- Onde as telas de referência mostram o dragão grande (hero da página inicial, fundo do login), use `hero-dragao.webp` e `fundo-academia.webp` se existirem na pasta; se não existirem, use o próprio `emblema-dragao.png` grande com um brilho dourado suave atrás e deixe um `TODO` para trocar depois.

## 3. Telas a implementar

### Públicas
1. **Página inicial (landing)** — header com logo horizontal, links "A academia", "Nosso método", "Professores", "Contato" e botão "Área do aluno". Hero: "DESPERTE SUA FORÇA. VÁ AO EXTREMO.", subtítulo, botões "Criar minha conta" e "Já sou aluno", imagem do dragão à direita. Faixa com 3 etapas: Comece / Mantenha / Supere.
2. **Login / Criar conta (desktop)** — card dividido em dois painéis com botão circular dourado de alternar (⇄) entre Login e Cadastro, com animação de troca. Campos Usuário e Senha (mostrar/ocultar), "Lembrar de mim", "Esqueci minha senha".
3. **Login (mobile)** — card único com abas "Entrar | Criar conta".
4. **Recuperar senha** — envio de link pelo Brevo.

### Área do aluno (mobile-first, com barra de navegação inferior)
5. **Visão geral** — "Olá, {nome}", cards: Plano atual, Status financeiro, Presenças no mês (com anel de progresso). Card da mensalidade do mês com valor, badge de status e botão "Pagar agora".
6. **Pagamento PIX** — resumo do plano e vencimento, QR Code e "PIX copia e cola" gerados pelo **Mercado Pago**, botão "Copiar código", status "Aguardando pagamento" com atualização automática (webhook do Mercado Pago ou polling), "Outras formas de pagamento" e "Enviar comprovante" (upload para o Supabase Storage, gera status "Em análise").
7. **Turmas**, **Mensalidades** (histórico), **Planos**, **Meus dados** — abas da barra inferior.

### Painel administrativo (desktop, sidebar preta com o emblema do dragão)
Menu: Painel, Alunos, Turmas, Financeiro, Planos, Avisos, Relatórios, Academia/Configurações, Sair.
8. **Painel** — cards: Alunos ativos, Receita do mês, Pagamentos pendentes, Presença hoje, Aguardando aprovação. Lista "Cadastros pendentes" com Aprovar/Recusar. Tabela "Planos da academia" + "Cadastrar plano". Gráfico de barras "Receita dos últimos 6 meses" e linha "Total de alunos".
9. **Alunos** — busca por nome/e-mail/telefone, filtros por plano e status, tabela com "Ver perfil".
10. **Perfil do aluno** — foto, badges de status e plano, dados pessoais, turmas, situação do plano e **Controle de mensalidades** (Atualizar, Aprovar comprovante, Rejeitar) + "Enviar cobrança por e-mail" (Brevo). Botão "Editar cadastro".
11. **Financeiro** — cards: Recebido no período, Pendente, Vencido, Em análise, Alunos inadimplentes. Filtros: período, turma, plano, método, situação, aluno. Tabela com "Ver detalhes" e destaque "Revisar comprovante" para itens em análise.
12. **Turmas e presença (professor)** — "Minhas turmas" com dias/horário/ocupação e "Registrar presença". Tela de chamada por data com checkboxes e "Salvar presença".

## 4. Regras e dados
- Perfis de acesso: **aluno**, **professor**, **administrador**. Proteja as rotas de cada perfil no servidor, não só no front. Use RLS do Supabase onde fizer sentido.
- Novo cadastro entra como "aguardando aprovação" até o admin aprovar.
- Mensalidade: status `pendente`, `em_analise`, `pago`, `vencido`. Vira `vencido` automaticamente após o vencimento.
- Reaproveite as tabelas existentes; se faltar algo (planos, turmas, matrículas em turmas, presenças, mensalidades, comprovantes, avisos), crie **migrations SQL** separadas e me mostre antes de aplicar.
- Valores monetários no formato `R$ 1.234,56` e datas em `dd/mm/aaaa`, fuso America/Fortaleza.

## 5. Forma de trabalhar
- Implemente em etapas, nesta ordem: tokens + componentes base → login/cadastro → área do aluno → PIX → painel admin → financeiro → turmas/presença → landing.
- Ao fim de cada etapa: rode o projeto, verifique erros, e me diga o que mudou e como testar.
- Componentes reutilizáveis: botão, card de métrica, badge de status, tabela com filtros, sidebar, barra inferior mobile.
- Não use dados falsos em produção: os números das imagens são só exemplo. Use dados reais do banco e estados vazios bem escritos ("Nenhum pagamento pendente").
