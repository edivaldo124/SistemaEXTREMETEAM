FROM python:3.11.16-slim-bookworm AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /build
COPY requirements.txt .
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip setuptools wheel \
    && /opt/venv/bin/pip install -r requirements.txt

FROM python:3.11.16-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system academia \
    && useradd --system --gid academia --home-dir /app academia

WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY --chown=academia:academia . .
# Fica vazio na imagem - o conteudo real mora no volume "uploads_data" montado
# aqui pelo compose.yaml. Precisa existir com este dono antes do volume ser
# montado, senao o Docker inicializa o volume como root e o processo (que roda
# como "academia") nao consegue escrever fotos/comprovantes.
RUN mkdir -p /app/uploads && chown academia:academia /app/uploads

USER academia
EXPOSE 5000

# O plano gratuito do Render não oferece Shell/Pre-Deploy Command. Aplicar as
# migrations antes do Gunicorn mantém o schema compatível em cada publicação;
# `flask db upgrade` é idempotente quando o banco já está na revisão mais nova.
CMD ["sh", "-c", "flask --app servidor db upgrade && exec gunicorn --bind 0.0.0.0:5000 --workers 1 --threads 2 --timeout 60 servidor:app"]
