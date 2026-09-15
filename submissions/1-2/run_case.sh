#!/usr/bin/env bash

set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
DOCKER_DIR="$SCRIPT_DIR/docker"
COMPOSE_FILE="$DOCKER_DIR/compose.yaml"
PROJECT_NAME="codyssey-subject1-2"
APP_PROCESS="agent-app-linux-arm64"
MONITOR_PATH="/opt/agent/bin/monitor.sh"
INTERVAL_SEC="${MONITOR_INTERVAL_SEC:-5}"

usage() {
    cat <<'EOF'
사용법:
  ./run_case.sh oom before|after MEMORY_LIMIT
  ./run_case.sh cpu before|after CPU_MAX_OCCUPY
  ./run_case.sh deadlock before|after true|false

예시:
  ./run_case.sh oom before 128
  ./run_case.sh oom after 512
  ./run_case.sh cpu before 100
  ./run_case.sh cpu after 10
  ./run_case.sh deadlock before true
  ./run_case.sh deadlock after false

환경변수:
  CASE_TIMEOUT_SEC       OOM/CPU 관찰 최대 시간 (기본값: 300초)
  DEADLOCK_TIMEOUT_SEC   Deadlock 관찰 시간 (기본값: 60초)
  MONITOR_INTERVAL_SEC   관제 주기 (기본값: 5초)
EOF
}

if (( $# != 3 )); then
    usage >&2
    exit 2
fi

case_name="$1"
phase="$2"
value="$3"

case "$case_name" in
    oom|cpu|deadlock) ;;
    *)
        echo "지원하지 않는 case: $case_name" >&2
        usage >&2
        exit 2
        ;;
esac

case "$phase" in
    before|after) ;;
    *)
        echo "phase는 before 또는 after여야 합니다: $phase" >&2
        exit 2
        ;;
esac

memory_limit=512
cpu_max_occupy=10
multi_thread_enable=false

is_integer() {
    [[ "$1" =~ ^[0-9]+$ ]]
}

case "$case_name" in
    oom)
        if ! is_integer "$value" || (( value < 50 || value > 512 )); then
            echo "MEMORY_LIMIT은 50~512 사이의 정수여야 합니다: $value" >&2
            exit 2
        fi
        memory_limit="$value"
        ;;
    cpu)
        if ! is_integer "$value" || (( value < 10 || value > 100 )); then
            echo "CPU_MAX_OCCUPY는 10~100 사이의 정수여야 합니다: $value" >&2
            exit 2
        fi
        cpu_max_occupy="$value"
        ;;
    deadlock)
        if [[ "$value" != true && "$value" != false ]]; then
            echo "MULTI_THREAD_ENABLE은 true 또는 false여야 합니다: $value" >&2
            exit 2
        fi
        multi_thread_enable="$value"
        ;;
esac

case "$case_name" in
    deadlock) max_seconds="${DEADLOCK_TIMEOUT_SEC:-60}" ;;
    *) max_seconds="${CASE_TIMEOUT_SEC:-300}" ;;
esac

if ! is_integer "$INTERVAL_SEC" || (( INTERVAL_SEC < 1 )); then
    echo "MONITOR_INTERVAL_SEC는 1 이상의 정수여야 합니다: $INTERVAL_SEC" >&2
    exit 2
fi

if ! is_integer "$max_seconds" || (( max_seconds < 1 )); then
    echo "관찰 시간은 1 이상의 정수여야 합니다: $max_seconds" >&2
    exit 2
fi

run_id="$(date '+%Y%m%d-%H%M%S')-$$"
out_dir="$SCRIPT_DIR/evidence/$case_name/$phase/$run_id"
mkdir -p "$out_dir/app-log"

container_name="codyssey-agent-${case_name}-${phase}-${run_id}"
observation_file="$out_dir/observations.log"
cleanup_started=false

compose() {
    docker compose \
        --project-name "$PROJECT_NAME" \
        --project-directory "$DOCKER_DIR" \
        --file "$COMPOSE_FILE" \
        "$@"
}

is_running() {
    local state
    state="$(docker inspect -f '{{.State.Running}}' "$container_name" 2>/dev/null || true)"
    [[ "$state" == true ]]
}

app_pid() {
    docker exec "$container_name" ps -eo pid=,args= 2>/dev/null \
        | awk -v target="/opt/agent/$APP_PROCESS" '$2 == target { print $1 }' \
        || true
}

capture_snapshot() {
    local label="$1"
    local pid

    {
        printf '\n=== %s ===\n' "$label"
        date '+%Y-%m-%dT%H:%M:%S%z'
        echo '--- identity ---'
        docker exec "$container_name" id 2>&1 || true
        echo '--- monitor.sh ---'
        docker exec "$container_name" "$MONITOR_PATH" 2>&1 || true
        echo '--- ps -ef ---'
        docker exec "$container_name" ps -ef 2>&1 || true
        pid="$(app_pid)"
        for one_pid in $pid; do
            echo "--- ps process PID=$one_pid ---"
            docker exec "$container_name" ps -p "$one_pid" -o pid,ppid,etime,pcpu,pmem,rss,vsz,stat,cmd 2>&1 || true
            echo "--- top -H PID=$one_pid ---"
            docker exec "$container_name" top -H -b -n 1 -p "$one_pid" 2>&1 || true
            echo "--- ps -L PID=$one_pid ---"
            docker exec "$container_name" ps -L -p "$one_pid" -o pid,tid,stat,pcpu,pmem,wchan:32,comm 2>&1 || true
        done
        echo '--- docker stats ---'
        docker stats --no-stream --format 'NAME={{.Name}} CPU={{.CPUPerc}} MEM={{.MemUsage}} MEM_PERC={{.MemPerc}} PIDS={{.PIDs}}' "$container_name" 2>&1 || true
    } >> "$observation_file" 2>&1
}

collect_artifacts() {
    if ! docker inspect "$container_name" > "$out_dir/container-inspect.json" 2>/dev/null; then
        return 0
    fi

    docker logs --timestamps "$container_name" > "$out_dir/application.log" 2>&1 || true
    docker cp "$container_name:/var/log/agent-app/." "$out_dir/app-log" > "$out_dir/docker-cp.log" 2>&1 || true
}

cleanup() {
    if [[ "$cleanup_started" == true ]]; then
        return 0
    fi
    cleanup_started=true

    collect_artifacts

    if docker inspect "$container_name" >/dev/null 2>&1; then
        docker rm -f "$container_name" > "$out_dir/container-remove.log" 2>&1 || true
    fi
}

trap cleanup EXIT

{
    echo "case=$case_name"
    echo "phase=$phase"
    echo "requested_value=$value"
    echo "MEMORY_LIMIT=$memory_limit"
    echo "CPU_MAX_OCCUPY=$cpu_max_occupy"
    echo "MULTI_THREAD_ENABLE=$multi_thread_enable"
    echo "max_seconds=$max_seconds"
    echo "monitor_interval_sec=$INTERVAL_SEC"
    echo "host_architecture=$(uname -m)"
    echo "docker_server=$(docker info --format '{{.ServerVersion}} {{.Architecture}}' 2>/dev/null || true)"
    echo "binary=$(file "$DOCKER_DIR/app/$APP_PROCESS")"
} > "$out_dir/run-metadata.txt"

echo "[1/5] Docker 이미지 빌드 중..."
if ! compose build agent > "$out_dir/docker-build.log" 2>&1; then
    echo "Docker 이미지 빌드에 실패했습니다. $out_dir/docker-build.log를 확인하세요." >&2
    exit 1
fi

echo "[2/5] 컨테이너 실행 중..."
if ! compose run \
    --detach \
    --no-tty \
    --no-deps \
    --name "$container_name" \
    --service-ports \
    --env "MEMORY_LIMIT=$memory_limit" \
    --env "CPU_MAX_OCCUPY=$cpu_max_occupy" \
    --env "MULTI_THREAD_ENABLE=$multi_thread_enable" \
    agent > "$out_dir/container-id.txt" 2> "$out_dir/container-start.stderr"; then
    echo "컨테이너 실행에 실패했습니다. $out_dir/container-start.stderr를 확인하세요." >&2
    exit 1
fi

echo "[3/5] Boot Sequence와 PID 대기 중..."
for _ in {1..30}; do
    if ! is_running; then
        break
    fi
    if [[ -n "$(app_pid)" ]]; then
        break
    fi
    sleep 1
done

capture_snapshot 'initial'

echo "[4/5] ${max_seconds}초 동안 ${INTERVAL_SEC}초 간격으로 관제 중..."
elapsed=0
while is_running && (( elapsed <= max_seconds )); do
    if (( elapsed > 0 )); then
        capture_snapshot "t+${elapsed}s"
    fi
    sleep "$INTERVAL_SEC"
    elapsed=$((elapsed + INTERVAL_SEC))
done

if is_running; then
    capture_snapshot "final-before-stop-t+${elapsed}s"
    echo "[INFO] 관찰 시간이 끝나 컨테이너를 정리합니다."
    docker stop --timeout 2 "$container_name" > "$out_dir/container-stop.log" 2>&1 || true
    if is_running; then
        docker kill "$container_name" > "$out_dir/container-kill.log" 2>&1 || true
    fi
else
    capture_snapshot 'final-after-process-exit'
fi

echo "[5/5] 증거 파일 저장 완료: $out_dir"
