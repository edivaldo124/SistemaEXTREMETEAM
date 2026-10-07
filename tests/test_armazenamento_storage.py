"""Uploads no Supabase Storage (produção na Vercel), com o HTTP simulado."""
import io

import pytest
import requests
from PIL import Image

from servicos import armazenamento
from servicos.armazenamento import (
    ArmazenamentoIndisponivel,
    ArquivoInvalido,
    TAMANHO_MAX_FOTO,
    ler_arquivo,
    remover_arquivo,
    salvar_comprovante_manual,
    salvar_foto_perfil,
)

URL = 'https://projeto.supabase.co'
BASE = f'{URL}/storage/v1/object/uploads'


class _Resposta:
    def __init__(self, status_code, content=b'', text=''):
        self.status_code = status_code
        self.content = content
        self.text = text
        self.ok = 200 <= status_code < 300


class _StorageFalso:
    """Registra as chamadas e devolve as respostas configuradas por método."""

    def __init__(self):
        self.chamadas = []
        self.respostas = {'post': _Resposta(200), 'get': _Resposta(200), 'delete': _Resposta(200)}
        self.erro = None

    def _chamar(self, metodo, url, **kwargs):
        self.chamadas.append((metodo, url, kwargs))
        if self.erro:
            raise self.erro
        return self.respostas[metodo]

    def post(self, url, **kwargs):
        return self._chamar('post', url, **kwargs)

    def get(self, url, **kwargs):
        return self._chamar('get', url, **kwargs)

    def delete(self, url, **kwargs):
        return self._chamar('delete', url, **kwargs)


@pytest.fixture
def storage(monkeypatch, tmp_path):
    falso = _StorageFalso()
    monkeypatch.setattr(armazenamento.requests, 'post', falso.post)
    monkeypatch.setattr(armazenamento.requests, 'get', falso.get)
    monkeypatch.setattr(armazenamento.requests, 'delete', falso.delete)
    monkeypatch.setenv('SUPABASE_URL', URL + '/')
    monkeypatch.setenv('SUPABASE_SECRET_KEY', 'sb_secret_chave-de-teste')
    monkeypatch.setenv('UPLOAD_DIR', str(tmp_path))
    falso.disco = tmp_path
    return falso


def _jpeg():
    arquivo = io.BytesIO()
    Image.new('RGB', (300, 200), (30, 80, 120)).save(arquivo, 'JPEG')
    return arquivo.getvalue()


def test_foto_vai_para_o_bucket_e_nao_para_o_disco(storage):
    nome = salvar_foto_perfil(_jpeg())

    metodo, url, kwargs = storage.chamadas[0]
    assert (metodo, url) == ('post', f'{BASE}/fotos/{nome}')
    assert kwargs['headers']['Content-Type'] == 'image/jpeg'
    assert kwargs['headers']['x-upsert'] == 'false'
    assert kwargs['data'][:3] == b'\xff\xd8\xff'
    assert kwargs['timeout'] == armazenamento.TIMEOUT_STORAGE
    assert not any(storage.disco.rglob('*.jpg'))


def test_chave_secreta_nova_vai_so_no_apikey(storage):
    salvar_foto_perfil(_jpeg())

    cabecalhos = storage.chamadas[0][2]['headers']
    assert cabecalhos['apikey'] == 'sb_secret_chave-de-teste'
    assert 'Authorization' not in cabecalhos


def test_service_role_antiga_vai_tambem_no_authorization(storage, monkeypatch):
    monkeypatch.setenv('SUPABASE_SECRET_KEY', 'eyJ.jwt.antigo')
    salvar_foto_perfil(_jpeg())

    cabecalhos = storage.chamadas[0][2]['headers']
    assert cabecalhos['apikey'] == 'eyJ.jwt.antigo'
    assert cabecalhos['Authorization'] == 'Bearer eyJ.jwt.antigo'


def test_comprovante_pdf_vai_com_o_tipo_certo(storage):
    nome = salvar_comprovante_manual(b'%PDF-1.4 conteudo')

    metodo, url, kwargs = storage.chamadas[0]
    assert url == f'{BASE}/comprovantes/{nome}'
    assert nome.endswith('.pdf')
    assert kwargs['headers']['Content-Type'] == 'application/pdf'


@pytest.mark.parametrize('falha', [_Resposta(500, text='erro interno'), requests.ConnectionError('fora do ar')])
def test_falha_do_storage_vira_mensagem_para_a_pessoa(storage, falha):
    if isinstance(falha, Exception):
        storage.erro = falha
    else:
        storage.respostas['post'] = falha

    with pytest.raises(ArmazenamentoIndisponivel) as erro:
        salvar_foto_perfil(_jpeg())

    # As rotas só tratam ArquivoInvalido: a falha precisa cair no mesmo `except`.
    assert isinstance(erro.value, ArquivoInvalido)
    assert 'Tente de novo' in str(erro.value)


def test_le_o_arquivo_do_bucket(storage):
    storage.respostas['get'] = _Resposta(200, content=b'bytes-da-foto')

    assert ler_arquivo('abc.jpg', subpasta='fotos') == b'bytes-da-foto'
    assert storage.chamadas[0][:2] == ('get', f'{BASE}/fotos/abc.jpg')


@pytest.mark.parametrize('status', [400, 404, 500])
def test_arquivo_que_o_bucket_nao_entrega_vira_none(storage, status):
    storage.respostas['get'] = _Resposta(status)

    assert ler_arquivo('abc.jpg', subpasta='fotos') is None


def test_storage_fora_do_ar_na_leitura_vira_none(storage):
    storage.erro = requests.Timeout('demorou')

    assert ler_arquivo('abc.jpg', subpasta='fotos') is None


@pytest.mark.parametrize('nome', ['', None, '../segredo.jpg', 'a/b.jpg', 'a\\b.jpg'])
def test_nome_invalido_nem_chega_no_bucket(storage, nome):
    assert ler_arquivo(nome, subpasta='fotos') is None
    remover_arquivo(nome, subpasta='fotos')
    assert storage.chamadas == []


def test_remover_apaga_do_bucket_e_engole_falha(storage):
    remover_arquivo('abc.jpg', subpasta='fotos')
    assert storage.chamadas[0][:2] == ('delete', f'{BASE}/fotos/abc.jpg')

    storage.erro = requests.ConnectionError('fora do ar')
    remover_arquivo('abc.jpg', subpasta='fotos')


def test_sem_as_variaveis_continua_gravando_em_disco(storage, monkeypatch):
    monkeypatch.delenv('SUPABASE_SECRET_KEY')

    nome = salvar_foto_perfil(_jpeg())

    assert storage.chamadas == []
    assert (storage.disco / 'fotos' / nome).is_file()
    assert ler_arquivo(nome, subpasta='fotos')[:3] == b'\xff\xd8\xff'
    remover_arquivo(nome, subpasta='fotos')
    assert not (storage.disco / 'fotos' / nome).exists()


def test_limite_cabe_no_corpo_aceito_pela_vercel(storage):
    # A Vercel recusa requisição acima de 4,5 MB antes de chegar no app.
    assert TAMANHO_MAX_FOTO <= 4 * 1024 * 1024
    with pytest.raises(ArquivoInvalido, match='4 MB'):
        salvar_foto_perfil(b'\xff' * (TAMANHO_MAX_FOTO + 1))
    assert storage.chamadas == []
