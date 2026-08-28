#!/usr/bin/env bash

set -u
set -o pipefail

PATH=/usr/sbin:/usr/bin:/sbin:/bin

APP_PROCESS="agent-app-linux-arm64"
APP_PORT=15034
LOG_DIR="/var/log/agent-app"
LOG_FILE="${LOG_DIR}/monitor.log"

MAX_LOG_BYTES=$((10 * 1024 * 1024))
MAX_LOG_FILES=10

umask 007

exec 9>"${LOG_DIR}/monitor.lock"
if ! flock -n 9; then
    echo "[INFO] Another monitor is already running. Skipping."
    exit 0
fi

echo "====== SYSTEM MONITOR RESULT ======"
echo "[HEALTH CHECK]"

APP_PID="$(pgrep -f "${APP_PROCESS}" | head -n 1 || true)"
if [[ -z "${APP_PID}" ]]; then
    echo "Checking process '${APP_PROCESS}'... [FAIL]"
    exit 1
fi
echo "Checking process '${APP_PROCESS}'... [OK] (PID: ${APP_PID})"

if ss -ltnH | awk -v port=":${APP_PORT}" '$4 ~ (port "$") { found=1 } END { exit !found }'; then
    echo "Checking port ${APP_PORT}... [OK]"
else
    echo "Checking port ${APP_PORT}... [FAIL]"
    exit 1
fi

if sudo -n /usr/sbin/ufw status 2>/dev/null | grep -q '^Status: active$'; then
    echo "Firewall status... [OK]"
else
    echo "[WARNING] Firewall is inactive or cannot be checked."
fi

read -r _ u1 n1 s1 i1 io1 irq1 sirq1 st1 _ < /proc/stat
total1=$((u1 + n1 + s1 + i1 + io1 + irq1 + sirq1 + st1))
idle1=$((i1 + io1))

sleep 1

read -r _ u2 n2 s2 i2 io2 irq2 sirq2 st2 _ < /proc/stat
total2=$((u2 + n2 + s2 + i2 + io2 + irq2 + sirq2 + st2))
idle2=$((i2 + io2))

CPU_USAGE="$(awk -v total="$((total2 - total1))" -v idle="$((idle2 - idle1))" \
    'BEGIN { if (total <= 0) printf "0.0"; else printf "%.1f", (total - idle) * 100 / total }')"

MEM_USAGE="$(free -b | awk '/^Mem:/ { printf "%.1f", $3 * 100 / $2 }')"
DISK_USED="$(df -P / | awk 'NR == 2 { gsub(/%/, "", $5); print $5 }')"

echo "[RESOURCE MONITORING]"
printf 'CPU Usage : %s%%\n' "${CPU_USAGE}"
printf 'MEM Usage : %s%%\n' "${MEM_USAGE}"
printf 'DISK Used : %s%%\n' "${DISK_USED}"

if awk -v value="${CPU_USAGE}" 'BEGIN { exit !(value > 20) }'; then
    echo "[WARNING] CPU threshold exceeded (${CPU_USAGE}% > 20%)"
fi

if awk -v value="${MEM_USAGE}" 'BEGIN { exit !(value > 10) }'; then
    echo "[WARNING] MEM threshold exceeded (${MEM_USAGE}% > 10%)"
fi

if awk -v value="${DISK_USED}" 'BEGIN { exit !(value > 80) }'; then
    echo "[WARNING] DISK threshold exceeded (${DISK_USED}% > 80%)"
fi

touch "${LOG_FILE}"
chmod 660 "${LOG_FILE}"

if (( $(stat -c %s "${LOG_FILE}") >= MAX_LOG_BYTES )); then
    rm -f "${LOG_FILE}.$((MAX_LOG_FILES - 1))"

    for ((index = MAX_LOG_FILES - 2; index >= 1; index--)); do
        [[ -f "${LOG_FILE}.${index}" ]] && mv -f "${LOG_FILE}.${index}" "${LOG_FILE}.$((index + 1))"
    done

    mv -f "${LOG_FILE}" "${LOG_FILE}.1"
    : > "${LOG_FILE}"
    chmod 660 "${LOG_FILE}"
fi

LOG_LINE="[$(date '+%F %T')] PID:${APP_PID} CPU:${CPU_USAGE}% MEM:${MEM_USAGE}% DISK_USED:${DISK_USED}%"
printf '%s\n' "${LOG_LINE}" >> "${LOG_FILE}"

echo "[INFO] Log appended: ${LOG_FILE}"
