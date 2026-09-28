"""Scripts de backup (tools/backup/): retenção, falha sem backup "pela metade" e a trava
da restauração. pg_dump/pg_restore são trocados por scripts falsos no PATH; a
restauração de verdade (pg_dump 17 -> banco descartável) está descrita no README."""

import os
import stat
import subprocess
import tarfile
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
BACKUP = RAIZ / 'tools/backup/backup.sh'
RESTAURAR = RAIZ / 'tools/backup/restaurar.sh'


def _executavel(caminho, conteudo):
    caminho.write_text(conteudo)
    caminho.chmod(caminho.stat().st_mode | stat.S_IXUSR)


@pytest.fixture
def ambiente(tmp_path):
    binarios = tmp_path / 'bin'
    binarios.mkdir()
    chamadas = tmp_path / 'chamadas.log'
    # pg_dump falso: grava um "dump" no --file pedido.
    _executavel(binarios / 'pg_dump', f"""#!/bin/sh
echo "pg_dump $*" >> {chamadas}
for arg in "$@"; do case "$arg" in --file=*) echo dump > "${{arg#--file=}}" ;; esac; done
""")
    _executavel(binarios / 'pg_restore', f"""#!/bin/sh
echo "pg_restore $*" >> {chamadas}
[ -z "${{PG_RESTORE_FALHA:-}}" ]
""")
    uploads = tmp_path / 'uploads'
    (uploads / 'comprovantes').mkdir(parents=True)
    (uploads / 'comprovantes' / 'pag-1.pdf').write_bytes(b'%PDF-comprovante')
    destino = tmp_path / 'backups'
    env = dict(
        os.environ, PATH=f'{binarios}:{os.environ["PATH"]}',
        BACKUP_DIR=str(destino), UPLOADS_DIR=str(uploads), PGDATABASE='academia', PGHOST='db',
    )
    env.pop('PG_RESTORE_FALHA', None)
    return {'env': env, 'destino': destino, 'chamadas': chamadas}


def _rodar(script, env, *args):
    return subprocess.run(['sh', str(script), *args], env=env, capture_output=True, text=True, timeout=30)


def test_backup_gera_dump_e_uploads_e_aplica_a_retencao(ambiente):
    destino = ambiente['destino']
    diarios, semanais = destino / 'diarios', destino / 'semanais'
    for dia in range(10, 18):
        (diarios / f'2026-09-{dia}_033000').mkdir(parents=True)
    for semana in range(30, 35):
        (semanais / f'2026-S{semana}').mkdir(parents=True)
    (diarios / '.parcial-2026-09-18_033000').mkdir()

    resultado = _rodar(BACKUP, ambiente['env'])
    assert resultado.returncode == 0, resultado.stderr

    nomes = sorted(p.name for p in diarios.iterdir())
    assert len(nomes) == 7
    assert nomes[0] == '2026-09-12_033000'
    assert not any(n.startswith('.parcial') for n in nomes)
    novo = diarios / nomes[-1]
    assert (novo / 'banco.dump').read_text() == 'dump\n'
    with tarfile.open(novo / 'uploads.tar.gz') as pacote:
        assert './comprovantes/pag-1.pdf' in pacote.getnames()

    assert len(list(semanais.iterdir())) == 4
    assert (destino / 'ULTIMO_BACKUP_OK').exists()
    # Só leitura para o dono: comprovantes e fotos de alunos.
    assert stat.S_IMODE((novo / 'banco.dump').stat().st_mode) == 0o600

    chamadas = ambiente['chamadas'].read_text()
    assert '--format=custom' in chamadas and '--compress=9' in chamadas
    assert 'pg_restore --list' in chamadas


def test_semanal_uma_vez_por_semana(ambiente):
    assert _rodar(BACKUP, ambiente['env']).returncode == 0
    assert _rodar(BACKUP, ambiente['env']).returncode == 0
    assert len(list((ambiente['destino'] / 'semanais').iterdir())) == 1


def test_dump_ilegivel_nao_vira_backup(ambiente):
    env = dict(ambiente['env'], PG_RESTORE_FALHA='1')
    resultado = _rodar(BACKUP, env)
    assert resultado.returncode != 0
    diarios = ambiente['destino'] / 'diarios'
    assert [p.name for p in diarios.iterdir() if not p.name.startswith('.')] == []
    assert not (ambiente['destino'] / 'ULTIMO_BACKUP_OK').exists()

    # A próxima execução boa limpa a pasta provisória da que falhou.
    assert _rodar(BACKUP, ambiente['env']).returncode == 0
    assert not any(p.name.startswith('.parcial') for p in diarios.iterdir())


def test_restaurar_recusa_o_banco_em_uso_sem_confirmacao(ambiente):
    assert _rodar(BACKUP, ambiente['env']).returncode == 0
    pasta = next((ambiente['destino'] / 'diarios').iterdir())
    antes = ambiente['chamadas'].read_text()

    resultado = _rodar(RESTAURAR, ambiente['env'], str(pasta), 'academia')
    assert resultado.returncode == 1
    assert 'CONFIRMAR=sim' in resultado.stderr
    assert ambiente['chamadas'].read_text() == antes


def test_restaurar_em_banco_descartavel_e_extrair_uploads(ambiente, tmp_path):
    assert _rodar(BACKUP, ambiente['env']).returncode == 0
    pasta = next((ambiente['destino'] / 'diarios').iterdir())
    destino_uploads = tmp_path / 'restaurados'

    resultado = _rodar(RESTAURAR, ambiente['env'], str(pasta), 'restauracao_teste', str(destino_uploads))
    assert resultado.returncode == 0, resultado.stderr
    chamadas = ambiente['chamadas'].read_text()
    assert '--dbname=restauracao_teste' in chamadas
    assert '--single-transaction' in chamadas and '--exit-on-error' in chamadas
    assert (destino_uploads / 'comprovantes' / 'pag-1.pdf').read_bytes() == b'%PDF-comprovante'


def test_restaurar_exige_os_argumentos(ambiente):
    resultado = _rodar(RESTAURAR, ambiente['env'])
    assert resultado.returncode == 2
    assert 'uso:' in resultado.stderr
