# ProjetoWeb
# Sistema-academia
# SistemaEXTREMETEAM

Sistema de gestão para academia (Extreme Team): cadastro e aprovação de alunos, planos, turmas, presença, mensalidades, pagamento de mensalidade via Pix e Checkout Pro (Mercado Pago), foto de perfil, comprovante manual e painel financeiro do admin.

## Instalação local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt   # inclui requirements.txt + pytest
cp .env.example .env
```

Edite o `.env` e preencha pelo menos: `DATABASE_URL`, `SECRET_KEY`, `ADMIN_USER`, `ADMIN_PASSWORD`. O arquivo `.env` nunca deve ser commitado (já está no `.gitignore`).

## Banco de dados e migrations

O projeto usa Flask-SQLAlchemy + Flask-Migrate (Alembic). Em uma base nova, `python servidor.py` já cria as tabelas automaticamente (`db.create_all()`). Para aplicar mudanças de schema em uma base **já existente** (como os campos de pagamento via Pix), use as migrations:

```bash
export FLASK_APP=servidor.py
flask db upgrade
```

**Atenção:** o `DATABASE_URL` de desenvolvimento local aponta para um Postgres local. Em produção, `DATABASE_URL` aponta para o banco real da academia, com dados de alunos — nunca rode testes automatizados apontando para ele, e sempre revise (`flask db upgrade --sql` ou leitura manual do arquivo em `migrations/versions/`) uma migration nova antes de aplicá-la em produção.

## Rodando

```bash
python servidor.py            # dev, http://localhost:4000
# ou
docker compose up --build     # app + Caddy (HTTPS)
```

## Testes

```bash
pip install -r requirements-dev.txt
pytest
```

Os testes forçam um banco SQLite temporário isolado (configurado em `tests/conftest.py`) e nunca chamam a API real do Mercado Pago: o SDK é mockado. A configuração de teste substitui qualquer `DATABASE_URL` presente no shell para impedir acesso acidental ao banco real.

A regressão de concorrência do Pix exige PostgreSQL, pois SQLite não aplica `SELECT FOR UPDATE`. Para executá-la, informe `TEST_POSTGRES_URL` de um PostgreSQL **local de teste** e rode `pytest tests/test_pix_concorrencia_postgres.py`. Cada caso cria e remove seu próprio schema temporário, usa duas conexões simultâneas e simula o Mercado Pago. Sem essa variável, esses casos aparecem como ignorados (`skipped`).

## Configuração de segurança

- `APP_BASE_URL` define a origem usada em links de recuperação, confirmação de e-mail e retornos de pagamento. Ela não é derivada do cabeçalho `Host`.
- `TRUSTED_HOSTS` contém os hosts aceitos, separados por vírgula. Em produção, informe o domínio público real.
- `TRUST_PROXY_COUNT` informa quantos proxies confiáveis existem à frente do Flask. O `compose.yaml` usa `1` por causa do Caddy; uma execução local direta usa `0`.
- `RATELIMIT_STORAGE_URI` deve apontar para Redis em produção para compartilhar os limites de autenticação e pagamentos entre processos. O Docker Compose já inclui esse serviço; no Render, configure a URI do serviço Redis usado pela aplicação. `memory://` mantém contadores apenas dentro de cada processo.
- Pagamentos têm limites por conta, preservados entre sessões: Pix e Checkout compartilham 10 tentativas de abertura por minuto; status, retorno do Checkout e sincronização administrativa compartilham 30 consultas por minuto. Ao atingir o limite, a aplicação responde `429` com `Retry-After: 60` antes de chamar o provedor.
- Requisições acima de 10 MB são recusadas pelo Flask e pelo Caddy. PDFs enviados como comprovante são entregues como download.

## Keep-alive (hospedagem que hiberna)

No plano gratuito do Render o serviço é derrubado depois de ~15 minutos sem nenhuma requisição de entrada, e a volta custa quase um minuto de espera para o primeiro visitante. Com `KEEP_ALIVE=true`, a aplicação sobe uma thread daemon que faz um GET no próprio `/health` a cada `KEEP_ALIVE_INTERVALO` segundos (padrão 600, aceito entre 60 e 840), tentando reduzir os períodos sem tráfego. Se o ping falhar ou retornar um status diferente de 200, tenta novamente após 60 segundos. Isso não garante que o serviço nunca hiberne ou reinicie.

- O destino do ping é sempre `APP_BASE_URL` + `/health`, nunca o cabeçalho `Host` da requisição. Sem `APP_BASE_URL` válida o keep-alive não sobe e só registra um aviso no log.
- Deixe `KEEP_ALIVE=false` em desenvolvimento e no `docker compose` — nada hiberna nesses ambientes.
- O plano gratuito do Render dá 750 horas de instância por mês por workspace, e o mês tem ~730 horas. Um serviço acordado o tempo todo cabe na cota; dois não.
- A thread morre junto com o processo, então isto não acorda um serviço que já hibernou ou caiu. Para isso é preciso um monitor externo (UptimeRobot, cron-job.org) apontando para `/health`.

No painel do Render, configure em **Environment** (o `.env.example` local não configura o serviço):

```env
KEEP_ALIVE=true
APP_BASE_URL=https://seu-servico.onrender.com
KEEP_ALIVE_INTERVALO=600
```

Use a origem HTTPS real do serviço, sem caminho. Salve e faça o deploy para aplicar.
Nos logs, procure `Keep-alive falhou`, `Keep-alive recebeu HTTP` ou `Keep-alive desligado`.
O Render documenta a hibernação após 15 minutos sem tráfego de entrada e a possibilidade
de reiniciar instâncias gratuitas: https://render.com/docs/free.

## Pagamento de mensalidade via Pix (Mercado Pago)

### Instalar dependências

Já incluído em `requirements.txt` (`mercadopago`, `Flask-Migrate`). Basta `pip install -r requirements.txt`.

### Variáveis de ambiente

No `.env`:

```env
MERCADO_PAGO_ACCESS_TOKEN=
MERCADO_PAGO_WEBHOOK_SECRET=
APP_BASE_URL=
MERCADO_PAGO_AMBIENTE=
```

- `MERCADO_PAGO_ACCESS_TOKEN`: Access Token da conta Mercado Pago (teste ou produção). **Nunca** commitar o valor real; `.env.example` traz só um placeholder.
- `MERCADO_PAGO_WEBHOOK_SECRET`: assinatura secreta do webhook, gerada no painel do Mercado Pago.
- `APP_BASE_URL`: URL pública (HTTPS) onde a aplicação está publicada. **Obrigatória** para o Checkout Pro (monta as URLs de retorno e de notificação); sem ela, a ação "Outras formas de pagamento" falha de forma explícita, e o Pix direto continua funcionando.
- `MERCADO_PAGO_AMBIENTE` (opcional): `producao` ou `sandbox`. Decide se o aluno é mandado para o `init_point` real ou para o `sandbox_init_point` do Checkout Pro. **Se não for definida**, o ambiente é deduzido do prefixo público do access token (`TEST-` = sandbox, qualquer outro = produção) — o token em si nunca é lido além do prefixo, nem registrado em log.

Se estiver rodando via `docker compose`, essas variáveis já são repassadas ao container pelo `compose.yaml` (a partir do `.env`).

### Como obter credenciais de teste

1. Acesse [Suas integrações → Credenciais](https://www.mercadopago.com.br/developers/pt/docs/your-integrations/credentials) no painel de desenvolvedores do Mercado Pago.
2. Crie (ou use) uma aplicação e copie o **Access Token de teste**.
3. Use também um [usuário de teste comprador](https://www.mercadopago.com.br/developers) para simular o pagamento do Pix gerado.

Nunca use credenciais de produção durante o desenvolvimento — os testes automatizados e o fluxo local devem usar sempre credenciais de teste.

### URL a cadastrar como webhook

No painel do Mercado Pago (Suas integrações → Webhooks → Configurar notificações), cadastre:

```
{APP_BASE_URL}/api/webhooks/mercado-pago
```

Por exemplo, `https://academiaextremeteam.com.br/api/webhooks/mercado-pago`. Essa URL **precisa** responder em HTTPS público e válido — o `Caddyfile` deste projeto usa `tls internal` (certificado local) enquanto não houver um domínio real configurado, e o Mercado Pago não consegue entregar webhooks para esse certificado. Até lá, teste o webhook com um túnel (ex.: `ngrok http 4000`) apontando o Mercado Pago para a URL do túnel, ou use o botão "Simular notificação" do painel do Mercado Pago.

### Como testar localmente

1. Configure `MERCADO_PAGO_ACCESS_TOKEN` de teste no `.env`.
2. Rode a aplicação (`python servidor.py`).
3. Faça login como aluno, acesse "Mensalidades" e clique em "Pagar com Pix" numa mensalidade pendente.
4. Sem HTTPS público, o webhook não chega automaticamente — a própria tela já consulta `GET /api/mensalidades/<id>/status` periodicamente, que também confirma o pagamento direto na API do Mercado Pago como rede de segurança.
5. Para validar a assinatura do webhook de verdade, use um túnel público (ngrok/cloudflared) + a opção "Simular notificação" do painel do Mercado Pago, e confira nos logs da aplicação se a assinatura foi validada.

### Produção

1. Configure um domínio real e HTTPS válido (edite o `Caddyfile`, trocando `tls internal` pelo domínio).
2. Cadastre a URL do webhook em produção (`https://SEU_DOMINIO/api/webhooks/mercado-pago`).
3. Rode `flask db upgrade` contra o banco de produção (com backup/atenção — ver seção de migrations acima).
4. Configure `MERCADO_PAGO_ACCESS_TOKEN`, `MERCADO_PAGO_WEBHOOK_SECRET` e `APP_BASE_URL` de produção no `.env` do servidor (nunca no repositório).

No deploy por Docker, o `CMD` da imagem executa `flask --app servidor db upgrade`
antes de iniciar o Gunicorn. Isso também atende planos do Render sem Shell ou
Pre-Deploy Command. Se uma migração falhar, a nova versão não inicia e o motivo fica
registrado nos logs do deploy, evitando executar código novo sobre um schema antigo.

### Trocando de credenciais de teste para produção

Basta substituir `MERCADO_PAGO_ACCESS_TOKEN` e `MERCADO_PAGO_WEBHOOK_SECRET` no `.env` de produção pelos valores de produção, e recadastrar a URL do webhook (se o domínio mudou). **A conta e as credenciais de produção do Mercado Pago devem pertencer ao dono da academia** — nunca use uma conta de terceiros para receber os pagamentos reais dos alunos.

## Outras formas de pagamento (Checkout Pro)

Além do Pix direto, a mensalidade pendente oferece **"Outras formas de pagamento"**: cartão de crédito/débito, boleto, saldo Mercado Pago e o que mais estiver habilitado na conta. O aluno é levado ao checkout hospedado pelo Mercado Pago e volta para o sistema ao final.

Nenhum dado de cartão passa pelo servidor da academia — número, validade e CVV são digitados dentro do ambiente do Mercado Pago (escopo PCI mínimo). Por isso não existe formulário de cartão próprio no projeto.

### Fluxo

1. `POST /perfil/mensalidade/<id>/checkout` — cria (ou reaproveita) uma preferência do Checkout Pro. Com `Accept: application/json`, responde com `url_checkout` e o navegador abre o Mercado Pago por GET. Isso evita que o Chrome bloqueie um redirecionamento externo de formulário pela CSP `form-action 'self'`. Sem JavaScript, responde `303` para uma página interna com o link de continuação. Falhas e timeout liberam o botão para nova tentativa.
2. O aluno escolhe o meio de pagamento no Mercado Pago.
3. `GET /perfil/mensalidade/<id>/retorno-checkout` — volta para o sistema. Essa tela **ignora** `status`, `payment_id` e `external_reference` da query string: ela consulta a API do Mercado Pago pela referência que o próprio servidor gravou e só então mostra o estado.
4. `POST /api/webhooks/mercado-pago` — mesmo endpoint do Pix. Valida a assinatura, consulta o pagamento na API e reencontra a mensalidade pela referência confirmada.

A mensalidade só vira `pago` quando a API do Mercado Pago responde `approved` **e** external_reference, valor e moeda (BRL) batem com o que está no banco. Boleto pode levar até 3 dias úteis para compensar — nesse intervalo a tela mostra "Aguardando confirmação", nunca "aprovado".

### Reuso de preferência

A preferência criada é reaproveitada em cliques repetidos enquanto continuar válida (mensalidade em aberto, dentro da validade de 60 min, mesmo ambiente e **mesmo valor**). Se o admin alterar o valor da mensalidade, a preferência antiga é descartada e uma nova é criada — do contrário o aluno pagaria a quantia antiga e a conferência barraria o crédito.

### Passos manuais no painel do Mercado Pago

1. **Suas integrações → sua aplicação → Formas de pagamento**: habilite cartão de crédito, cartão de débito, boleto e saldo em conta. O que estiver desabilitado lá simplesmente não aparece no checkout — o código não filtra meios de pagamento.
2. **Configurações → Webhooks**: a mesma URL do Pix (`{APP_BASE_URL}/api/webhooks/mercado-pago`) já cobre o Checkout Pro. Garanta que o tópico **Pagamentos** esteja marcado.
3. A conta precisa estar apta a receber (dados bancários e verificação concluídos) para que boleto e cartão apareçam.

### Limitações conhecidas

- A abertura do Checkout Pro usa timeout de até 6 segundos por chamada, sem novas tentativas automáticas; o fallback sem `auto_return` aproveita apenas o tempo restante. Consultas interativas de status usam 3 segundos por chamada, sem retentativas. Esses limites se aplicam ao transporte com a API; não são uma garantia do tempo total de carregamento da página hospedada no Mercado Pago.
- O processamento do webhook é **síncrono** — o projeto não tem fila nem worker. Para não estourar o tempo de entrega do Mercado Pago, a consulta feita dentro do webhook usa timeout curto (5s) e sem retry. Se o Mercado Pago não responder a tempo, o endpoint devolve `503` e a notificação é reenviada por eles; a tela de retorno e o polling de status também reconferem o pagamento.
- Não há assinatura recorrente (`preapproval`): cada mensalidade é uma cobrança avulsa.

## Foto de perfil e comprovante manual (armazenamento de arquivos)

Fotos de alunos e comprovantes manuais (`servicos/armazenamento.py`) ficam fora de `static/` e só são servidos por rotas autenticadas (`/perfil/foto/<id>`, `/perfil/mensalidade/<id>/comprovante-manual/arquivo`) que conferem permissão a cada request. Fotos profissionais ficam em `UPLOAD_DIR/professores` e são servidas por `/professores/<id>/foto`: o acesso público depende da opção de publicar o perfil; quando privado, só o administrador e o próprio professor podem acessar.

- **Local (dev)**: gravado em `UPLOAD_DIR` (padrão `uploads/`, relativo à raiz do projeto). Já está no `.gitignore`.
- **Docker/produção**: o filesystem do container `app` é descartado a cada rebuild/deploy. Por isso o `compose.yaml` monta um volume nomeado (`uploads_data:/app/uploads`) e fixa `UPLOAD_DIR=/app/uploads` - **isso é obrigatório**: sem esse volume, toda foto e comprovante enviado se perde no próximo `docker compose up --build`. Se um dia migrar para object storage (S3, R2, etc.), troque a implementação de `servicos/armazenamento.py` sem precisar mexer nas rotas que a usam.

Upload de foto: valida o tipo real do arquivo decodificando com Pillow (nunca confia na extensão/Content-Type enviados pelo navegador), recorta em quadrado, remove EXIF e regrava do zero como JPEG antes de salvar com nome aleatório (UUID). Comprovante manual aceita JPEG/PNG/PDF; PDFs não são reprocessados (não são executados nem renderizados pelo servidor), só têm a assinatura binária conferida.

## Painel financeiro do admin

`/admin/financeiro` (link no cabeçalho do painel admin) mostra total recebido/pendente/vencido/em análise e alunos inadimplentes - todos calculados no backend (`PagamentoDAO.totais_periodo`), nunca somados em JavaScript. Filtros por período, turma, plano, forma de pagamento, situação e nome do aluno.

## Comprovante manual (dinheiro/transferência)

O aluno pode enviar um comprovante (JPEG/PNG/PDF) numa mensalidade pendente/vencida/recusada pela tela de pagamento (`/perfil/pagamento/<id>`). O envio sozinho **nunca** marca como pago - a mensalidade fica "Em análise" até um admin aprovar ou rejeitar em `/admin/usuario/<cpf>` (aprovar marca como paga; rejeitar devolve para pendente/vencida). Toda decisão fica registrada em `pagamentos_eventos` com quem decidiu, quando e a observação.


## Contatos da academia e equipe

- **Administração → Academia** (`/admin/academia`): editar Instagram, e-mail de atendimento, WhatsApp, endereço completo, complemento e horários. Ao salvar, os campos preenchidos aparecem na página inicial e os canais ficam acessíveis no rodapé da área do aluno. O botão **Como chegar** abre o endereço no Google Maps. Apagar um campo retira aquela informação do site.
- **Administração → Turmas → Professores → Editar perfil**: definir nome de apresentação, modalidades, biografia, formação/graduações, foto e contatos profissionais. O nome de apresentação pode ser diferente do nome cadastrado; login e senha permanecem separados.
- Cada professor começa com **Exibir perfil do professor no site** desativado. Ao publicar, a equipe da página inicial mostra a apresentação; e-mail, Instagram e WhatsApp só aparecem se a opção individual também estiver marcada. Desmarcar a publicação retira o perfil e o acesso público à foto. O aluno encontra o link **Conhecer professor** em suas turmas, junto dos dias e horários existentes.
- Nesta versão, apenas o administrador edita essas informações. Não há envio de mensagens ao preencher os contatos.

A migração `d9e2f6a14c80` cria a configuração única da academia e acrescenta campos opcionais aos professores existentes, com publicação e contatos ocultos inicialmente. Execute `flask --app servidor db upgrade` antes de iniciar a nova versão fora do Docker; a imagem Docker já executa esse comando no início. Fotos de professores utilizam o mesmo volume persistente das demais imagens.


## Cadastro de aluno pela administração e ativação de acesso

O cadastro de um aluno e a conta de acesso dele são coisas separadas. A academia atende muita gente que não vai usar o sistema, então a matrícula não exige e-mail, usuário nem senha.

### Matricular no balcão

**Administração → Painel → Matricular aluno** (`/admin/alunos/novo`). Pede nome, CPF e data de nascimento; telefone, e-mail, graduação, observações e plano são opcionais. A opção **Já lançar a primeira mensalidade deste plano** reaproveita a mesma regra de contratação usada pelo aluno (`PagamentoDAO.contratar_plano`), que revalida tudo contra o banco e reutiliza uma cobrança aberta em vez de criar outra.

O aluno nasce com `status_cadastro='aprovado'` e `ativo=True` (quem cadastrou já é a administração), e sem conta: `login` e `senha_hash` ficam em NULL; `email` também fica em NULL quando não informado. Mensalidades, pagamentos, vencimentos e pendências funcionam desde o primeiro minuto em `/admin/usuario/<cpf>`.

Três situações diferentes aparecem separadas nas telas e nunca se misturam:

| Situação | Onde vive | Valores |
|---|---|---|
| Acesso | conta | Acesso ativado · Convite enviado · Acesso não ativado |
| Academia | matrícula | Ativo · Inativo · cadastro pendente/aprovado/recusado |
| Financeira | mensalidades | derivada de `situacao_plano`, nunca escrita à mão |

### Ativar o acesso depois

Em **`/admin/usuario/<cpf>` → Acesso ao sistema**, o administrador envia um convite para o e-mail do cadastro. O convite é um token de 32 bytes que existe só dentro do e-mail: o banco guarda apenas o SHA-256 dele, ele vale 7 dias e queima no primeiro uso. O aluno abre `/ativar-acesso/<token>`, escolhe usuário e senha e passa a entrar no **mesmo cadastro**, com plano, mensalidades e histórico intactos.

Regras que sustentam isso:

- CPF, nome ou data de nascimento **nunca** vinculam uma conta. Só o token, entregue num canal que a administração registrou, ativa o acesso.
- A tela de ativação mostra apenas o primeiro nome e o e-mail mascarado. CPF, telefone, plano e valores só aparecem depois do login.
- Quem tenta se cadastrar pelo formulário público com um CPF já existente não cria um segundo aluno: o convite vai para o e-mail **do cadastro**, nunca para o digitado, e a resposta não revela nada sobre quem está na base.
- Aluno sem e-mail continua sendo gerenciado normalmente. O convite simplesmente não é oferecido, e os painéis de aviso mostram quantos alunos precisam ser avisados no balcão.
- Um aluno sem senha não autentica por nenhum caminho, nem informando o CPF. A recuperação de senha só atende contas já ativadas.
- A troca do e-mail no cadastro invalida os links anteriores de convite e recuperação. Pedidos públicos repetidos preservam um convite ainda válido; a administração pode reenviar ou revogar.
- O uso único do convite é validado no banco durante a gravação, inclusive quando duas ativações chegam simultaneamente.

### Confirmar senha

O cadastro público e a ativação de acesso pedem **Confirmar senha**. A comparação é feita no navegador (aviso imediato no campo, `aria-invalid` e bloqueio do envio) e refeita no servidor com `hmac.compare_digest`, em `servicos/senhas.erro_confirmacao_senha`. As regras de força de senha existentes continuam valendo. A confirmação não é gravada em coluna nenhuma nem registrada em log.

### Migração e configuração

A migração `e4b7c2a91d35` torna `login`, `email` e `senha_hash` opcionais e acrescenta as três colunas de convite. Ela é aditiva: alunos existentes mantêm os três campos preenchidos e seguem com o acesso ativado. O `downgrade` se recusa a rodar enquanto houver cadastro sem conta, em vez de apagar esses alunos.

```bash
flask --app servidor db upgrade
```

Nenhuma variável de ambiente nova. O envio do convite usa a configuração de e-mail que já existe (`BREVO_API_KEY`, `BREVO_SENDER_EMAIL`) e `APP_BASE_URL` para montar o link; sem elas o convite não é gravado e o painel avisa que o envio falhou.
