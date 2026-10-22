"""Gera front/src/emblema.webp, a imagem de onde a cena do hero sorteia as brasas.

Parte do emblema oficial (static/imagens/marca/emblema-dragao.png, sobre preto puro):
recorta, reduz e deixa transparente o que é fundo. A cena só põe brasa em pixel opaco,
com a cor dele.

Uso, na raiz do projeto: .venv/bin/python front/scripts/emblema.py
"""
from pathlib import Path

from PIL import Image, ImageOps

RAIZ = Path(__file__).resolve().parents[2]
ORIGEM = RAIZ / 'static/imagens/marca/emblema-dragao.png'
DESTINO = RAIZ / 'front/src/emblema.webp'

# Resolução da amostragem: ~79 mil pixels opacos, o triplo das brasas do desktop.
LARGURA = 360
# O fundo do emblema é preto puro (0). O dragão, mesmo nas escamas escuras, passa de 3.
LIMIAR_FUNDO = 3


def main():
    imagem = Image.open(ORIGEM).convert('RGB')
    mascara = ImageOps.grayscale(imagem).point(lambda valor: 255 if valor > LIMIAR_FUNDO else 0)
    caixa = mascara.getbbox()
    imagem, mascara = imagem.crop(caixa), mascara.crop(caixa)

    tamanho = (LARGURA, round(LARGURA * imagem.height / imagem.width))
    imagem = imagem.resize(tamanho, Image.LANCZOS)
    # Reduzida, a máscara ganha meio-tom na borda; o corte em 128 tira os pontos soltos.
    mascara = mascara.resize(tamanho, Image.LANCZOS).point(lambda valor: 255 if valor >= 128 else 0)
    imagem.putalpha(mascara)
    imagem.save(DESTINO, 'WEBP', quality=86, method=6)
    print(f'{DESTINO.relative_to(RAIZ)}: {tamanho[0]}x{tamanho[1]}, {DESTINO.stat().st_size // 1024} KB')


if __name__ == '__main__':
    main()
