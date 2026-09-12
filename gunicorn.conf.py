"""Hooks carregados pelo Gunicorn; nunca executados por flask db upgrade."""


def post_worker_init(worker):
    from servicos.consumidor_email import iniciar

    iniciar(worker.wsgi)


def worker_exit(server, worker):
    from servicos.consumidor_email import parar

    parar()

