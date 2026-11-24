<p align="center">
  <img src="static/imagens/logo-horizontal-800.png" alt="Extreme Team" width="420">
</p>

# Extreme Team: sistema de gestão de academia

Sistema web feito para o centro de treinamento Extreme Team. Ele junta num lugar só o que a academia fazia no caderno e no WhatsApp: cadastro de alunos, turmas, presença, mensalidades e pagamentos.

## O que o sistema faz

**Para o aluno**
- Cadastro com aprovação da academia e ativação de acesso por convite
- Área do aluno com plano, turmas, horários e perfil dos professores
- Pagamento da mensalidade por **Pix** ou pelo **Checkout Pro do Mercado Pago** (cartão, boleto e saldo)
- Envio de comprovante para pagamento em dinheiro ou transferência

**Para a administração**
- Matrícula no balcão, sem exigir e-mail nem senha do aluno
- Turmas, presença, planos e professores
- Painel financeiro com recebido, pendente, vencido e lista de inadimplentes, com filtros
- Conexão da conta do Mercado Pago por OAuth (a academia não copia token nenhum)
- Envio de e-mails pela Gmail API, com fila no banco

**Página inicial**
- Hero com cena 3D (React Three Fiber) que acompanha a rolagem, com versão leve para celular e imagem estática para quem pede menos movimento

## Tecnologias

| Camada | Ferramentas |
|---|---|
| Back-end | Python, Flask, SQLAlchemy, Flask-Migrate (Alembic), Gunicorn |
| Banco | PostgreSQL (Supabase), Redis para limite de requisições |
| Front-end | HTML, CSS e JavaScript; React Three Fiber + Vite só na cena 3D |
| Pagamentos | Mercado Pago: Pix, Checkout Pro, webhooks assinados, OAuth com PKCE |
| Infra | Docker, Docker Compose, Caddy (HTTPS), backup diário com retenção |
| Qualidade | pytest, testes de JavaScript no Node, Dependabot, pip-audit |

## Cuidados de segurança

- Senha do administrador guardada só como hash e segundo fator (TOTP) opcional
- Tokens do Mercado Pago e do Gmail cifrados no banco
- Pagamento só é confirmado depois de conferir valor, moeda e referência na API do Mercado Pago
- Limite de requisições no login e nos pagamentos, Cloudflare Turnstile no cadastro público
- Uploads validados pelo conteúdo real do arquivo, com os metadados da câmera removidos
- Google Analytics só depois do consentimento (LGPD)

## Rodando localmente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env      # preencha DATABASE_URL, SECRET_KEY, ADMIN_USER e ADMIN_PASSWORD_HASH
flask --app servidor db upgrade
python servidor.py        # http://localhost:4000
```

Ou com Docker: `docker compose up --build`.

Testes: `pytest` e `node --test tests/js/*.test.cjs`.

O guia completo de instalação, configuração, pagamentos, backup e publicação está em **[docs/OPERACAO.md](docs/OPERACAO.md)**.

---

Desenvolvido por [Edivaldo Roberto](https://github.com/edivaldo124).
