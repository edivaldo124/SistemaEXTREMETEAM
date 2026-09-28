#!/bin/sh
# Um backup completo: banco (pg_dump, formato custom compactado) + uploads (comprovantes
# e fotos), com retenção de N diários e N semanais. Roda dentro do serviço `backup` do
# compose.yaml (postgres:17-alpine, mesma versão do banco); a conexão vem de
# PGHOST/PGUSER/PGPASSWORD/PGDATABASE. Também serve para rodar na mão:
#
#   docker compose exec backup sh /scripts/backup.sh
#
# Cada backup é uma pasta com banco.dump e uploads.tar.gz. Ela é montada com um nome
# provisório e só ganha o nome final depois que o dump foi relido com sucesso: uma
# pasta com nome de data está sempre completa.
set -eu

DESTINO=${BACKUP_DIR:-/backups}
UPLOADS=${UPLOADS_DIR:-/uploads}
DIARIOS=${BACKUP_DIARIOS:-7}
SEMANAIS=${BACKUP_SEMANAIS:-4}

# Comprovantes e fotos de alunos: só o dono do processo lê.
umask 077

registrar() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') backup: $*"
}

# Mantém só as N pastas mais novas (os nomes são datas, então a ordem alfabética é a
# cronológica). Pasta provisória de uma execução que falhou começa com "." e não conta.
reter() {
    pasta=$1
    manter=$2
    total=$(ls -1 "$pasta" | grep -c '^[0-9]' || true)
    excedente=$((total - manter))
    [ "$excedente" -gt 0 ] || return 0
    ls -1 "$pasta" | grep '^[0-9]' | sort | head -n "$excedente" | while read -r nome; do
        rm -rf "${pasta:?}/${nome:?}"
        registrar "removido $pasta/$nome (retenção de $manter)"
    done
}

mkdir -p "$DESTINO/diarios" "$DESTINO/semanais"
rm -rf "$DESTINO"/diarios/.parcial-*

carimbo=$(date +%Y-%m-%d_%H%M%S)
parcial="$DESTINO/diarios/.parcial-$carimbo"
mkdir "$parcial"

registrar "iniciando $carimbo (banco ${PGDATABASE:-?} em ${PGHOST:-?})"
pg_dump --format=custom --compress=9 --no-owner --no-privileges --file="$parcial/banco.dump"
# Um dump que o pg_restore não consegue listar não é backup.
pg_restore --list "$parcial/banco.dump" > /dev/null

if [ -d "$UPLOADS" ]; then
    tar -czf "$parcial/uploads.tar.gz" -C "$UPLOADS" .
else
    registrar "aviso: $UPLOADS não existe; backup só do banco"
fi

mv "$parcial" "$DESTINO/diarios/$carimbo"

# Semanal: o primeiro backup de cada semana ISO vira cópia semanal. Não depende de o
# serviço estar de pé num dia específico: se domingo passou em branco, a segunda conta.
semana=$(date +%G-S%V)
if [ ! -d "$DESTINO/semanais/$semana" ]; then
    cp -R "$DESTINO/diarios/$carimbo" "$DESTINO/semanais/.parcial-$semana"
    mv "$DESTINO/semanais/.parcial-$semana" "$DESTINO/semanais/$semana"
    registrar "cópia semanal $semana"
fi
rm -rf "$DESTINO"/semanais/.parcial-*

reter "$DESTINO/diarios" "$DIARIOS"
reter "$DESTINO/semanais" "$SEMANAIS"

date '+%Y-%m-%d %H:%M:%S' > "$DESTINO/ULTIMO_BACKUP_OK"
registrar "concluído: $DESTINO/diarios/$carimbo ($(du -sh "$DESTINO/diarios/$carimbo" | cut -f1))"
