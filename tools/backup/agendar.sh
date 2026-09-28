#!/bin/sh
# Processo principal do serviço `backup`: dorme até BACKUP_HORA (fuso de TZ) e roda
# backup.sh, todo dia. Um laço em vez de cron porque o crond não repassa as variáveis
# do container (PGPASSWORD etc.) para o job. Falha num dia é registrada no log e o laço
# segue para o dia seguinte; a data do último sucesso fica em /backups/ULTIMO_BACKUP_OK.
set -u

HORA=${BACKUP_HORA:-03:30}
case "$HORA" in
    [0-2][0-9]:[0-5][0-9]) ;;
    *) echo "BACKUP_HORA deve estar no formato HH:MM (recebido: $HORA)" >&2; exit 1 ;;
esac

echo "$(date '+%Y-%m-%d %H:%M:%S') backup: agendado para $HORA todo dia (TZ=${TZ:-UTC})"
while true; do
    agora=$(date +%s)
    alvo=$(date -d "$HORA" +%s)
    [ "$alvo" -gt "$agora" ] || alvo=$((alvo + 86400))
    sleep $((alvo - agora))
    sh /scripts/backup.sh || echo "$(date '+%Y-%m-%d %H:%M:%S') backup: FALHOU (ver mensagens acima)" >&2
done
