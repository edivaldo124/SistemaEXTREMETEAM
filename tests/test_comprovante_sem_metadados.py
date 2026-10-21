"""Comprovante em imagem é guardado sem os metadados da câmera (SEC-28, LGPD).

A foto de um comprovante em papel sai do celular com o GPS de onde foi tirada. Os
metadados saem direto dos bytes, sem decodificar a imagem: os pixels têm de continuar
exatamente os mesmos, e só a orientação volta, para a foto não chegar de lado.
"""

import io
import random
from io import BytesIO

import pytest
from PIL import ExifTags, Image, PngImagePlugin

from dao.financeiroDAO import PagamentoDAO
from servicos import armazenamento
from servicos.armazenamento import salvar_comprovante_manual

TRAILER = b'dados do fabricante: -23.5505,-46.6333'


@pytest.fixture(autouse=True)
def disco_temporario(monkeypatch, tmp_path):
    monkeypatch.delenv('SUPABASE_URL', raising=False)
    monkeypatch.delenv('SUPABASE_SECRET_KEY', raising=False)
    monkeypatch.setenv('UPLOAD_DIR', str(tmp_path))


def _pixels_aleatorios():
    # Ruído gera bytes FF no fluxo comprimido do JPEG, que precisam passar intactos.
    return Image.frombytes('RGB', (64, 48), random.Random(28).randbytes(64 * 48 * 3))


def _exif_do_celular(orientacao=6):
    exif = Image.Exif()
    exif[ExifTags.Base.Orientation] = orientacao
    exif[ExifTags.Base.Make] = 'Celular'
    exif[ExifTags.IFD.GPSInfo] = {ExifTags.GPS.GPSLatitudeRef: 'S', ExifTags.GPS.GPSLatitude: (23.0, 33.0, 1.0)}
    return exif


def _foto_jpeg(**opcoes):
    buffer = BytesIO()
    _pixels_aleatorios().save(buffer, format='JPEG', quality=95, **opcoes)
    return buffer.getvalue()


def _guardado(conteudo):
    nome = salvar_comprovante_manual(conteudo)
    return armazenamento.ler_arquivo(nome, subpasta='comprovantes')


def _pixels(conteudo):
    with Image.open(BytesIO(conteudo)) as imagem:
        return imagem.convert('RGB').tobytes()


def _exif(conteudo):
    with Image.open(BytesIO(conteudo)) as imagem:
        imagem.load()
        return dict(imagem.getexif())


def _chunks(png):
    tipos, i = [], 8
    while i < len(png):
        tamanho = int.from_bytes(png[i:i + 4], 'big')
        tipos.append(png[i + 4:i + 8].decode())
        i += 12 + tamanho
    return tipos


@pytest.mark.parametrize('progressivo', [False, True])
def test_foto_jpeg_perde_gps_xmp_e_comentario_e_mantem_os_pixels(progressivo):
    original = _foto_jpeg(
        progressive=progressivo, exif=_exif_do_celular(), comment=b'tirada na academia',
        xmp=b'<x:xmpmeta xmlns:x="adobe:ns:meta/"/>',
    ) + TRAILER

    gravado = _guardado(original)

    assert _exif(gravado) == {ExifTags.Base.Orientation: 6}
    for vestigio in (b'Celular', b'xmpmeta', b'academia', TRAILER):
        assert vestigio not in gravado
    assert _pixels(gravado) == _pixels(original)


def test_foto_jpeg_sem_rotacao_nao_ganha_exif():
    gravado = _guardado(_foto_jpeg(exif=_exif_do_celular(orientacao=1)))

    assert b'Exif' not in gravado
    assert _exif(gravado) == {}


def test_jpeg_sem_metadados_fica_identico():
    original = _foto_jpeg()

    assert _guardado(original) == original


def test_png_perde_texto_e_exif_e_mantem_os_pixels():
    texto = PngImagePlugin.PngInfo()
    texto.add_text('Location', 'Rua da Academia, 100')
    texto.add_itxt('XML:com.adobe.xmp', '<x:xmpmeta xmlns:x="adobe:ns:meta/"/>')
    buffer = BytesIO()
    _pixels_aleatorios().save(buffer, format='PNG', pnginfo=texto, exif=_exif_do_celular())
    original = buffer.getvalue()
    assert _chunks(original) == ['IHDR', 'tEXt', 'iTXt', 'eXIf', 'IDAT', 'IEND']

    gravado = _guardado(original)

    assert _chunks(gravado) == ['IHDR', 'eXIf', 'IDAT', 'IEND']
    with Image.open(BytesIO(gravado)) as imagem:
        imagem.verify()  # CRC do eXIf novo
    assert _exif(gravado) == {ExifTags.Base.Orientation: 6}
    assert b'Academia' not in gravado
    assert _pixels(gravado) == _pixels(original)


def test_png_sem_metadados_fica_identico():
    buffer = BytesIO()
    _pixels_aleatorios().save(buffer, format='PNG')
    original = buffer.getvalue()

    assert _guardado(original) == original


def test_admin_recebe_o_comprovante_enviado_sem_o_gps(client, criar_pagamento, logar_como_aluno):
    pagamento = criar_pagamento(status='pendente')
    logar_como_aluno(pagamento.aluno)
    original = _foto_jpeg(exif=_exif_do_celular())

    client.post(
        f'/perfil/mensalidade/{pagamento.id}/comprovante-manual',
        data={'comprovante': (io.BytesIO(original), 'comprovante.jpg', 'image/jpeg')},
        content_type='multipart/form-data',
    )

    nome = PagamentoDAO.buscar_por_id(pagamento.id).comprovante_manual_arquivo
    gravado = armazenamento.ler_arquivo(nome, subpasta='comprovantes')
    assert ExifTags.IFD.GPSInfo not in _exif(gravado)
    assert _pixels(gravado) == _pixels(original)
