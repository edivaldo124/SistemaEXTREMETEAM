"""Armazenamento de arquivos enviados por usuários (fotos de perfil, comprovantes manuais).

Guarda tudo em disco fora de `static/` (nunca fica público por URL direta - o acesso
sempre passa por uma rota Flask autenticada que confere permissão antes de servir o
arquivo). Local por padrão (bom para desenvolvimento); em produção o diretório
apontado por UPLOAD_DIR precisa estar num volume persistente (veja README/.env.example -
o container da aplicação não tem disco persistente por si só).

Nunca salva bytes de imagem em campos de texto do banco - só o nome gerado (UUID) fica
no banco, o conteúdo sempre vai para o disco.
"""
import os
import threading
import uuid
from io import BytesIO

from PIL import Image, ImageOps

# Uma decodificação de imagem por vez no processo.
#
# Medido: a aplicação ocupa 89 MB residentes em regime, num container de 192 MB - restam
# ~103 MB. Uma imagem de 8 MP sem escala reduzida custa ~92 MB e cabe; DUAS ao mesmo
# tempo, nas 2 threads do Gunicorn, passariam de 270 MB e derrubariam o processo por
# falta de memória (levando junto a requisição de todo mundo).
#
# Serializar é preferível a apertar mais o limite de pixels: o custo é esperar, e só
# quando duas pessoas enviam foto no mesmo instante - raro numa academia, e cada envio
# leva dezenas de milissegundos. Apertar o limite recusaria envios legítimos o tempo todo.
_UMA_IMAGEM_POR_VEZ = threading.Semaphore(1)

TAMANHO_MAX_FOTO = 5 * 1024 * 1024  # 5 MB, conforme RF de upload de perfil
TAMANHO_MAX_COMPROVANTE = 8 * 1024 * 1024  # 8 MB - PDFs escaneados costumam ser maiores
TAMANHO_AVATAR = 512  # px, quadrado

# Limites de PIXELS. É o número de pixels, não o tamanho do arquivo, que decide a
# memória usada: um PNG de 285 KB pode declarar 10000x10000 e custar, medido neste
# projeto, 1146 MB ao ser decodificado - num container de 192 MB. O padrão do Pillow
# (MAX_IMAGE_PIXELS) não protege: acima do limite ele apenas emite um aviso e decodifica
# assim mesmo, e só levanta erro passando do DOBRO.
#
# Custo medido, decodificando e reamostrando para o avatar de 512px:
#
#     formato        3 MP     9 MP    12 MP    24 MP    48 MP    100 MP
#     PNG/WebP      36 MB   105 MB   139 MB   277 MB   552 MB   1146 MB
#     JPEG                            12 MB             12 MB
#
# JPEG tem decodificação em escala reduzida (`draft()`), então o decodificador nunca
# monta a resolução cheia e o custo praticamente não cresce com a dimensão. PNG e WebP
# não têm equivalente e pagam o preço inteiro - por isso os dois limites são diferentes.
# Não é rigor arbitrário: é a memória que o container realmente tem.
#
# JPEG: 80 MP. `draft()` reduz em potências de 2 até 1/8, então o decodificador nunca
# monta mais que pixels/64 - 80 MP custam ~15 MB. Cobre qualquer câmera de consumo,
# inclusive os modos de 48 e 50 MP dos celulares.
MAX_PIXELS_JPEG = 80_000_000
# PNG/WebP: 8 MP custa ~92 MB no pior caso e continua folgado para uma foto de perfil
# (um print de tela cheia em 4K tem 8,3 MP; uma foto de celular chega como JPEG).
MAX_PIXELS_SEM_ESCALA = 8_000_000

# Formatos cujo decodificador aceita entregar a imagem já reduzida.
_FORMATOS_COM_ESCALA = ('JPEG', 'MPO')

_MIME_POR_FORMATO_PIL = {'JPEG': 'image/jpeg', 'PNG': 'image/png', 'WEBP': 'image/webp'}
_EXTENSAO_POR_MIME_IMAGEM = {'image/jpeg': 'jpg', 'image/png': 'png', 'image/webp': 'webp'}

CONTENT_TYPE_POR_EXTENSAO = {
    'jpg': 'image/jpeg',
    'png': 'image/png',
    'webp': 'image/webp',
    'pdf': 'application/pdf',
}


class ArquivoInvalido(Exception):
    """Arquivo recusado por tipo, tamanho ou conteúdo não confiável."""


def _raiz_uploads():
    raiz = os.environ.get('UPLOAD_DIR', 'uploads')
    os.makedirs(raiz, exist_ok=True)
    return raiz


def _pasta(subpasta):
    caminho = os.path.join(_raiz_uploads(), subpasta)
    os.makedirs(caminho, exist_ok=True)
    return caminho


class ImagemGrandeDemais(ArquivoInvalido):
    """Imagem cujas DIMENSÕES declaradas passam do limite de pixels."""


def _conferir_dimensoes(imagem):
    """Recusa pelo cabeçalho, antes de qualquer pixel ser decodificado.

    `Image.open` lê só o cabeçalho: `size` e `format` já estão disponíveis aqui, e
    desistir neste ponto é o que evita a alocação. Depois de `load()`/`convert()` a
    memória já foi pedida ao sistema.
    """
    largura, altura = imagem.size
    tem_escala = (imagem.format or '').upper() in _FORMATOS_COM_ESCALA
    limite = MAX_PIXELS_JPEG if tem_escala else MAX_PIXELS_SEM_ESCALA

    if largura * altura > limite:
        megapixels = limite // 1_000_000
        if tem_escala:
            detalhe = f'Envie uma foto de até {megapixels} megapixels.'
        else:
            detalhe = (
                f'Para PNG e WebP o limite é de {megapixels} megapixels. '
                'Uma foto em JPEG pode ser bem maior.'
            )
        raise ImagemGrandeDemais(f'A imagem tem dimensões grandes demais. {detalhe}')


def _detectar_tipo_imagem_real(conteudo, *, limitar_dimensoes=False):
    """Confere o conteúdo de fato (decodificando com Pillow), não a extensão/Content-Type
    enviados pelo navegador - impede um arquivo malicioso disfarçado com extensão de imagem.

    `limitar_dimensoes` só é ligado por quem vai DECODIFICAR os pixels depois. O
    comprovante manual não decodifica nada - ele é guardado como veio - então aplicar ali
    o teto pensado para o avatar recusava um documento legítimo: um A4 escaneado a
    300 dpi tem 8,7 MP e cabe folgado nos 8 MB permitidos ao arquivo.

    `verify()` lê o arquivo para conferir a integridade sem alocar o buffer de pixels,
    então o caminho sem limite continua preso ao tamanho do arquivo.

    Levanta ImagemGrandeDemais para a bomba de descompressão; devolve None para
    qualquer outro arquivo que não seja uma imagem válida.
    """
    try:
        with Image.open(BytesIO(conteudo)) as imagem:
            if limitar_dimensoes:
                _conferir_dimensoes(imagem)
            imagem.verify()
        with Image.open(BytesIO(conteudo)) as imagem:
            formato = (imagem.format or '').upper()
    except ImagemGrandeDemais:
        raise
    except Exception:
        return None
    return _MIME_POR_FORMATO_PIL.get(formato)


def salvar_foto_perfil(conteudo, *, subpasta='fotos'):
    """Valida, reprocessa e salva uma foto de perfil. Retorna o nome do arquivo gerado.

    O reprocessamento (decodificar com Pillow e regravar do zero como JPEG) descarta
    qualquer metadado EXIF e qualquer payload que não seja realmente uma imagem válida -
    a extensão/Content-Type enviados pelo navegador nunca são usados para decidir.
    """
    if not conteudo:
        raise ArquivoInvalido('Nenhum arquivo enviado.')
    if len(conteudo) > TAMANHO_MAX_FOTO:
        raise ArquivoInvalido('A imagem deve ter no máximo 5 MB.')

    if _detectar_tipo_imagem_real(conteudo, limitar_dimensoes=True) not in _MIME_POR_FORMATO_PIL.values():
        raise ArquivoInvalido('Envie uma imagem JPEG, PNG ou WebP.')

    with _UMA_IMAGEM_POR_VEZ, Image.open(BytesIO(conteudo)) as imagem:
        # Segunda conferência: `_detectar_tipo_imagem_real` abriu outra instância, e é
        # esta que vai de fato decodificar os pixels.
        _conferir_dimensoes(imagem)

        # Decodificação reduzida (JPEG): o decodificador já entrega a imagem numa
        # escala menor, em vez de montar a resolução cheia para depois reduzir a 512px.
        # O resultado final é o mesmo avatar, por uma fração da memória. Em formatos
        # sem esse recurso (PNG, WebP) a chamada simplesmente não faz nada.
        imagem.draft('RGB', (TAMANHO_AVATAR, TAMANHO_AVATAR))

        imagem = ImageOps.exif_transpose(imagem)
        imagem = imagem.convert('RGB')

        lado = min(imagem.width, imagem.height)
        esquerda = (imagem.width - lado) // 2
        topo = (imagem.height - lado) // 2
        imagem = imagem.crop((esquerda, topo, esquerda + lado, topo + lado))
        imagem = imagem.resize((TAMANHO_AVATAR, TAMANHO_AVATAR), Image.LANCZOS)

        buffer = BytesIO()
        imagem.save(buffer, format='JPEG', quality=88, optimize=True)

    nome_arquivo = f'{uuid.uuid4().hex}.jpg'
    with open(os.path.join(_pasta(subpasta), nome_arquivo), 'wb') as destino:
        destino.write(buffer.getvalue())
    return nome_arquivo


def salvar_comprovante_manual(conteudo, *, subpasta='comprovantes'):
    """Valida e salva um comprovante manual (JPEG, PNG ou PDF).

    Imagens passam pelo mesmo Pillow.verify() da foto de perfil. PDFs não são
    reprocessados (não executamos/renderizamos o conteúdo em nenhum momento -
    só guardamos os bytes e os servimos depois com o Content-Type correto para
    download/visualização), mas têm a assinatura binária conferida.
    """
    if not conteudo:
        raise ArquivoInvalido('Nenhum arquivo enviado.')
    if len(conteudo) > TAMANHO_MAX_COMPROVANTE:
        raise ArquivoInvalido('O arquivo deve ter no máximo 8 MB.')

    if conteudo[:5] == b'%PDF-':
        extensao = 'pdf'
    else:
        tipo_real = _detectar_tipo_imagem_real(conteudo)
        if tipo_real not in ('image/jpeg', 'image/png'):
            raise ArquivoInvalido('Envie um arquivo JPEG, PNG ou PDF.')
        extensao = _EXTENSAO_POR_MIME_IMAGEM[tipo_real]

    nome_arquivo = f'{uuid.uuid4().hex}.{extensao}'
    with open(os.path.join(_pasta(subpasta), nome_arquivo), 'wb') as destino:
        destino.write(conteudo)
    return nome_arquivo


def caminho_arquivo(nome_arquivo, *, subpasta):
    """Resolve o caminho em disco de um arquivo já salvo, ou None se não existir/for inválido.

    Rejeita qualquer nome com separador de caminho - o nome sempre deve ser o UUID
    gerado por esta camada, nunca um valor vindo direto de uma requisição.
    """
    if not nome_arquivo or '/' in nome_arquivo or '\\' in nome_arquivo or '..' in nome_arquivo:
        return None
    caminho = os.path.join(_pasta(subpasta), nome_arquivo)
    return caminho if os.path.isfile(caminho) else None


def remover_arquivo(nome_arquivo, *, subpasta):
    caminho = caminho_arquivo(nome_arquivo, subpasta=subpasta)
    if not caminho:
        return
    try:
        os.remove(caminho)
    except OSError:
        pass
