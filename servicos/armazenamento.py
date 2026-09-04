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
import uuid
from io import BytesIO

from PIL import Image, ImageOps

TAMANHO_MAX_FOTO = 5 * 1024 * 1024  # 5 MB, conforme RF de upload de perfil
TAMANHO_MAX_COMPROVANTE = 8 * 1024 * 1024  # 8 MB - PDFs escaneados costumam ser maiores
TAMANHO_AVATAR = 512  # px, quadrado

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


def _detectar_tipo_imagem_real(conteudo):
    """Confere o conteúdo de fato (decodificando com Pillow), não a extensão/Content-Type
    enviados pelo navegador - impede um arquivo malicioso disfarçado com extensão de imagem."""
    try:
        with Image.open(BytesIO(conteudo)) as imagem:
            imagem.verify()
        with Image.open(BytesIO(conteudo)) as imagem:
            formato = (imagem.format or '').upper()
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

    if _detectar_tipo_imagem_real(conteudo) not in _MIME_POR_FORMATO_PIL.values():
        raise ArquivoInvalido('Envie uma imagem JPEG, PNG ou WebP.')

    with Image.open(BytesIO(conteudo)) as imagem:
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
