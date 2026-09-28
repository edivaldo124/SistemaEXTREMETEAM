#!/bin/sh
# Restaura um backup gerado por backup.sh.
#
#   sh restaurar.sh <pasta-do-backup> <banco-destino> [pasta-dos-uploads]
#
# <banco-destino> é obrigatório e explícito. Restaurar por cima do banco em uso
# (o mesmo nome de PGDATABASE) apaga os dados atuais, então exige CONFIRMAR=sim.
# O caminho seguro é sempre restaurar primeiro num banco descartável e conferir.
# Com [pasta-dos-uploads], extrai uploads.tar.gz ali (os arquivos com o mesmo nome
# são sobrescritos; os demais ficam).
set -eu

if [ $# -lt 2 ]; then
    echo "uso: $0 <pasta-do-backup> <banco-destino> [pasta-dos-uploads]" >&2
    exit 2
fi
ORIGEM=$1
BANCO=$2
UPLOADS_DESTINO=${3:-}

[ -f "$ORIGEM/banco.dump" ] || { echo "não achei $ORIGEM/banco.dump" >&2; exit 1; }

if [ "$BANCO" = "${PGDATABASE:-}" ] && [ "${CONFIRMAR:-}" != "sim" ]; then
    echo "O destino \"$BANCO\" é o banco em uso: a restauração apaga os dados atuais." >&2
    echo "Pare o app antes (docker compose stop app) e rode de novo com CONFIRMAR=sim." >&2
    exit 1
fi

pg_restore --list "$ORIGEM/banco.dump" > /dev/null
echo "restaurando $ORIGEM/banco.dump em \"$BANCO\"..."
# Uma transação só: ou restaura tudo, ou o banco fica como estava.
pg_restore --dbname="$BANCO" --clean --if-exists --no-owner --no-privileges \
    --single-transaction --exit-on-error "$ORIGEM/banco.dump"
echo "banco restaurado."

if [ -n "$UPLOADS_DESTINO" ]; then
    [ -f "$ORIGEM/uploads.tar.gz" ] || { echo "este backup não tem uploads.tar.gz" >&2; exit 1; }
    mkdir -p "$UPLOADS_DESTINO"
    tar -xzf "$ORIGEM/uploads.tar.gz" -C "$UPLOADS_DESTINO"
    echo "uploads extraídos em $UPLOADS_DESTINO."
fi
