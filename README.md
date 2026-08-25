# ProjetoWeb
# Sistema-academia
# SistemaEXTREMETEAM

Sistema de gestão para academia (Extreme Team): cadastro e aprovação de alunos, planos, turmas, presença, mensalidades e pagamento de mensalidade via Pix (Mercado Pago).

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
```

- `MERCADO_PAGO_ACCESS_TOKEN`: Access Token da conta Mercado Pago (teste ou produção). **Nunca** commitar o valor real; `.env.example` traz só um placeholder.
- `MERCADO_PAGO_WEBHOOK_SECRET`: assinatura secreta do webhook, gerada no painel do Mercado Pago.
- `APP_BASE_URL`: URL pública (HTTPS) onde a aplicação está publicada.

Se estiver rodando via `docker compose`, essas 3 variáveis já são repassadas ao container pelo `compose.yaml` (a partir do `.env`).

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

### Trocando de credenciais de teste para produção

Basta substituir `MERCADO_PAGO_ACCESS_TOKEN` e `MERCADO_PAGO_WEBHOOK_SECRET` no `.env` de produção pelos valores de produção, e recadastrar a URL do webhook (se o domínio mudou). **A conta e as credenciais de produção do Mercado Pago devem pertencer ao dono da academia** — nunca use uma conta de terceiros para receber os pagamentos reais dos alunos.
