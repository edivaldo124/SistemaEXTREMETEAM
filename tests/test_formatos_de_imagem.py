"""Upload de foto e comprovante: o Pillow só interpreta JPEG, PNG e WebP.

As falhas conhecidas do Pillow 12.3 (GIF que pede gigabytes de memória, TIFF e EPS) ficam
nos decodificadores desses outros formatos. O arquivo de um aluno não pode chegar a eles:
tem que ser recusado antes de qualquer parser rodar.
"""

from io import BytesIO

import pytest
from PIL import GifImagePlugin, Image, TiffImagePlugin

from servicos import armazenamento
from servicos.armazenamento import ArquivoInvalido, salvar_comprovante_manual, salvar_foto_perfil


def _imagem(formato, **opcoes):
    buffer = BytesIO()
    Image.new('RGB', (16, 16), 'gold').save(buffer, format=formato, **opcoes)
    return buffer.getvalue()


@pytest.fixture
def parsers_proibidos(monkeypatch):
    """Falha o teste se o parser de GIF ou TIFF for chamado."""
    chamados = []

    def proibido(nome):
        def _abrir(self):
            chamados.append(nome)
            raise AssertionError(f'o parser de {nome} não devia rodar')
        return _abrir

    monkeypatch.setattr(GifImagePlugin.GifImageFile, '_open', proibido('GIF'))
    monkeypatch.setattr(TiffImagePlugin.TiffImageFile, '_open', proibido('TIFF'))
    return chamados


@pytest.fixture(autouse=True)
def disco_temporario(monkeypatch, tmp_path):
    monkeypatch.delenv('SUPABASE_URL', raising=False)
    monkeypatch.delenv('SUPABASE_SECRET_KEY', raising=False)
    monkeypatch.setenv('UPLOAD_DIR', str(tmp_path))


@pytest.mark.parametrize('formato', ['GIF', 'TIFF'])
def test_foto_em_outro_formato_e_recusada_sem_passar_pelo_parser(parsers_proibidos, formato):
    with pytest.raises(ArquivoInvalido, match='JPEG, PNG ou WebP'):
        salvar_foto_perfil(_imagem(formato))
    assert parsers_proibidos == []


@pytest.mark.parametrize('formato', ['GIF', 'TIFF'])
def test_comprovante_em_outro_formato_e_recusado_sem_passar_pelo_parser(parsers_proibidos, formato):
    with pytest.raises(ArquivoInvalido, match='JPEG, PNG ou PDF'):
        salvar_comprovante_manual(_imagem(formato))
    assert parsers_proibidos == []


@pytest.mark.parametrize('formato,opcoes', [('JPEG', {}), ('PNG', {}), ('WEBP', {'quality': 80})])
def test_formatos_aceitos_continuam_funcionando(formato, opcoes):
    nome = salvar_foto_perfil(_imagem(formato, **opcoes))
    assert nome.endswith('.jpg')


def test_lista_de_formatos_e_a_mesma_dos_tipos_aceitos():
    assert set(armazenamento._FORMATOS_ACEITOS) == set(armazenamento._MIME_POR_FORMATO_PIL)
