"""Arquivos do hero cinematográfico da página inicial.

A cena 3D é compilada pelo Vite a partir de `front/` para `static/dist/cinema`, com o
hash do conteúdo no nome de cada arquivo (o Flask não versiona estáticos, e um nome
fixo deixaria o navegador com a versão velha em cache). O manifest diz qual arquivo é
cada entrada. Sem o manifest, a home fica com o pôster estático e nada quebra.

O vídeo é opcional: um MP4 em `static/video/cinema.mp4` substitui a cena 3D e avança
com a rolagem (README, seção "Hero da página inicial").
"""

import json
from functools import lru_cache
from pathlib import Path

from flask import current_app, url_for

PASTA_DIST = 'dist/cinema'
VIDEO = 'video/cinema.mp4'


@lru_cache(maxsize=4)
def _entradas(pasta_static):
    """{nome da entrada: arquivo}, lido uma vez: o build não muda com o servidor no ar."""
    try:
        manifest = json.loads((Path(pasta_static) / PASTA_DIST / 'manifest.json').read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return {}
    return {
        item['name']: item['file']
        for item in manifest.values()
        if isinstance(item, dict) and item.get('isEntry') and item.get('name') and item.get('file')
    }


@lru_cache(maxsize=4)
def _tem_video(pasta_static):
    return (Path(pasta_static) / VIDEO).is_file()


def modulo(nome):
    """URL da entrada `nome` ('cena' ou 'video') do build, ou None se não foi compilada."""
    arquivo = _entradas(current_app.static_folder).get(nome)
    return url_for('static', filename=f'{PASTA_DIST}/{arquivo}') if arquivo else None


def video():
    """URL do vídeo do hero, só se ele existir e a entrada que o toca estiver compilada."""
    if not modulo('video') or not _tem_video(current_app.static_folder):
        return None
    return url_for('static', filename=VIDEO)
