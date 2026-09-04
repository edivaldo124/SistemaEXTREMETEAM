"""Ponto de entrada WSGI usado pelo Gunicorn em producao."""

from servidor import app


__all__ = ["app"]
