#!/usr/bin/env bash

set -Eeuo pipefail

PATH=/usr/sbin:/usr/bin:/sbin:/bin

APP_PROCESS="${APP_PROCESS:-agent-app-linux-arm64}"
APP_PORT="${AGENT_PORT:-15034}"
LOG_DIR="${AGENT_LOG_DIR:-/var/log/agent-app}"
LOG_FILE="${MONITOR_LOG_FILE:-${LOG_DIR}/monitor.log}"

mkdir -p "$LOG_DIR"

timestamp="$(date '+%F %T')"
target_path="/opt/agent/$APP_PROCESS"
pid_list="$(ps -eo pid=,args= | awk -v target="$target_path" '$2 == target { print $1 }')"

if [[ -z "$pid_list" ]]; then
    echo "[$timestamp] PROCESS:$APP_PROCESS STATUS:NOT_FOUND"
    exit 1
fi

if ! ss -ltnH | awk -v port="$APP_PORT" '$4 ~ (":" port "$") { found=1 } END { exit(found ? 0 : 1) }'; then
    echo "[$timestamp] PROCESS:$APP_PROCESS PIDS:$pid_list PORT:$APP_PORT STATUS:NOT_LISTENING"
    exit 1
fi

record_count=0
for pid in $pid_list; do
    process_line="$(ps -p "$pid" -o pid=,ppid=,etime=,pcpu=,pmem=,rss=,vsz=,stat=,comm= | sed 's/^[[:space:]]*//')"

    if [[ -z "$process_line" ]]; then
        continue
    fi

    read -r _ ppid etime cpu mem rss_kb vsz_kb stat command <<< "$process_line"
    rss_mb="$(awk -v value="$rss_kb" 'BEGIN { printf "%.1f", value / 1024 }')"
    record="[$timestamp] PROCESS:$APP_PROCESS PID:$pid PPID:$ppid ETIME:$etime CPU:${cpu}% MEM:${mem}% RSS:${rss_mb}MB RSS_KB:${rss_kb} VSZ_KB:${vsz_kb} STAT:$stat PORT:$APP_PORT"
    printf '%s\n' "$record"
    printf '%s\n' "$record" >> "$LOG_FILE"
    record_count=$((record_count + 1))
done

if (( record_count == 0 )); then
    echo "[$timestamp] PROCESS:$APP_PROCESS PIDS:$pid_list STATUS:PS_FAILED"
    exit 1
fi
