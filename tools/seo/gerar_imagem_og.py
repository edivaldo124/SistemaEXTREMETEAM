"""Gera static/imagens/og-extreme-team.jpg (1200x630) a partir da logo oficial.

A prévia de link (WhatsApp, Instagram, Facebook, X) recorta imagens fora de 1,91:1.
A logo horizontal oficial tem fundo preto, então ela é centralizada numa tela preta do
tamanho certo, sem redesenhar nada da marca. Rode de novo se a logo mudar:

    python tools/seo/gerar_imagem_og.py
"""

from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parents[2]
ORIGEM = RAIZ / 'static/imagens/marca/logo-extreme-team-horizontal.png'
DESTINO = RAIZ / 'static/imagens/og-extreme-team.jpg'
LARGURA, ALTURA = 1200, 630
# Margem para a logo não encostar na borda quando a rede social arredonda ou recorta.
ESPACO_UTIL = (1000, 520)


def gerar():
    logo = Image.open(ORIGEM).convert('RGB')
    logo.thumbnail(ESPACO_UTIL, Image.Resampling.LANCZOS)
    tela = Image.new('RGB', (LARGURA, ALTURA), (0, 0, 0))
    tela.paste(logo, ((LARGURA - logo.width) // 2, (ALTURA - logo.height) // 2))
    tela.save(DESTINO, 'JPEG', quality=88, optimize=True, progressive=True)
    return DESTINO


if __name__ == '__main__':
    print(gerar())
