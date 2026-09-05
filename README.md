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

Os testes usam um banco SQLite temporário isolado (configurado em `tests/conftest.py`) e nunca chamam a API real do Mercado Pago — o SDK é mockado. **Nunca rode `pytest` num shell/container onde o `DATABASE_URL` real (Postgres de produção) já esteja exportado como variável de ambiente.**

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

1. `POST /perfil/mensalidade/<id>/checkout` — cria (ou reaproveita) uma preferência do Checkout Pro e responde `303` para a URL do Mercado Pago.
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

- O processamento do webhook é **síncrono** — o projeto não tem fila nem worker. Para não estourar o tempo de entrega do Mercado Pago, a consulta feita dentro do webhook usa timeout curto (5s) e sem retry. Se o Mercado Pago não responder a tempo, o endpoint devolve `503` e a notificação é reenviada por eles; a tela de retorno e o polling de status também reconferem o pagamento.
- Não há assinatura recorrente (`preapproval`): cada mensalidade é uma cobrança avulsa.

## Foto de perfil e comprovante manual (armazenamento de arquivos)

Fotos de perfil e comprovantes manuais (`servicos/armazenamento.py`) ficam fora de `static/` e só são servidos por rotas autenticadas (`/perfil/foto/<id>`, `/perfil/mensalidade/<id>/comprovante-manual/arquivo`) que conferem permissão a cada request - não há URL pública direta para esses arquivos.

- **Local (dev)**: gravado em `UPLOAD_DIR` (padrão `uploads/`, relativo à raiz do projeto). Já está no `.gitignore`.
- **Docker/produção**: o filesystem do container `app` é descartado a cada rebuild/deploy. Por isso o `compose.yaml` monta um volume nomeado (`uploads_data:/app/uploads`) e fixa `UPLOAD_DIR=/app/uploads` - **isso é obrigatório**: sem esse volume, toda foto e comprovante enviado se perde no próximo `docker compose up --build`. Se um dia migrar para object storage (S3, R2, etc.), troque a implementação de `servicos/armazenamento.py` sem precisar mexer nas rotas que a usam.

Upload de foto: valida o tipo real do arquivo decodificando com Pillow (nunca confia na extensão/Content-Type enviados pelo navegador), recorta em quadrado, remove EXIF e regrava do zero como JPEG antes de salvar com nome aleatório (UUID). Comprovante manual aceita JPEG/PNG/PDF; PDFs não são reprocessados (não são executados nem renderizados pelo servidor), só têm a assinatura binária conferida.

## Painel financeiro do admin

`/admin/financeiro` (link no cabeçalho do painel admin) mostra total recebido/pendente/vencido/em análise e alunos inadimplentes - todos calculados no backend (`PagamentoDAO.totais_periodo`), nunca somados em JavaScript. Filtros por período, turma, plano, forma de pagamento, situação e nome do aluno.

## Comprovante manual (dinheiro/transferência)

O aluno pode enviar um comprovante (JPEG/PNG/PDF) numa mensalidade pendente/vencida/recusada pela tela de pagamento (`/perfil/pagamento/<id>`). O envio sozinho **nunca** marca como pago - a mensalidade fica "Em análise" até um admin aprovar ou rejeitar em `/admin/usuario/<cpf>` (aprovar marca como paga; rejeitar devolve para pendente/vencida). Toda decisão fica registrada em `pagamentos_eventos` com quem decidiu, quando e a observação.
