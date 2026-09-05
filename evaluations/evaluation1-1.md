# 평가 문항

## 항목 1

- SSH 포트가 20022로 변경되었고, Root 원격 접속이 차단되었는가?
  - 확인 명령:
    ```bash
    sudo sshd -T | grep -E '^(port|permitrootlogin)'
    sudo ss -tulnp | grep sshd
    ```
  - `port 20022`, `permitrootlogin no`, 그리고 `20022` 포트의 `LISTEN` 상태를 확인한다.
- 방화벽이 활성화되어 있고(택1: UFW 또는 firewalld), 20022/tcp와 15034/tcp만 허용되는가?
  - UFW 사용 시 확인 명령:
    ```bash
    sudo ufw status numbered
    sudo ufw status verbose
    ```
  - `status numbered`에서 UFW가 `active`이고 `20022/tcp`, `15034/tcp` 외 추가 인바운드 허용 규칙이 없는지 확인한다. `status verbose`에서는 기본 인바운드 정책이 `deny`인지 확인한다.
- agent-admin/dev/test 계정과 agent-common/core 그룹이 요구 사항대로 구성되어 있는가?
  - 계정·그룹 및 권한 확인 명령:
    ```bash
    id agent-admin
    id agent-dev
    id agent-test

    sudo stat -c '%U:%G %a %n' \
      /home/agent-admin/agent-app/bin/monitor.sh \
      /var/log/agent-app \
      /var/log/agent-app/monitor.log

    sudo getfacl -p \
      /home/agent-admin/agent-app/upload_files \
      /home/agent-admin/agent-app/api_keys \
      /var/log/agent-app
    ```
  - `agent-admin`, `agent-dev`는 `agent-common`, `agent-core`에, `agent-test`는 `agent-common`에만 속해야 한다. `monitor.sh`는 `agent-dev:agent-core 750`이어야 한다.
  - 실제 접근 정책은 다음처럼 파일을 변경하지 않고 확인한다.
    ```bash
    if sudo -u agent-test test -w /home/agent-admin/agent-app/upload_files; then
      echo '[OK] agent-test can write upload_files'
    else
      echo '[FAIL] agent-test cannot write upload_files'
    fi

    if sudo -u agent-test test -r /home/agent-admin/agent-app/api_keys/t_secret.key; then
      echo '[FAIL] agent-test can read key'
    else
      echo '[OK] agent-test cannot read key'
    fi
    ```
- 앱이 Boot Sequence 5단계 [OK]를 통과하고 “Agent READY”가 출력되는가?
  - `agent-admin`으로 앱을 실행해 다음 출력을 확인한다.
    ```bash
    sudo -iu agent-admin
    source ~/.profile
    cd "$AGENT_HOME"
    ./agent-app-linux-arm64
    ```
  - 5단계 모두 `[OK]`이고 마지막에 `Agent READY`가 출력되어야 한다. 앱은 종료하지 않고 유지한 채, 다른 터미널에서 포트도 확인한다.
    ```bash
    sudo ss -ltnp | grep ':15034'
    ```
- monitor.sh가 프로세스/포트 상태를 점검하고, 비정상 상태에서 exit 1로 종료되는가?
  - 앱이 실행 중일 때 정상 Health Check를 확인한다.
    ```bash
    sudo -u agent-admin /home/agent-admin/agent-app/bin/monitor.sh
    echo "exit code: $?"
    ```
  - 프로세스와 포트가 모두 `[OK]`이고 종료 코드는 `0`이어야 한다.
  - 비정상 종료는 앱 실행 터미널에서 `Ctrl+C`로 앱을 잠시 종료한 뒤 같은 명령을 실행해 확인한다. 프로세스 `[FAIL]`과 종료 코드 `1`을 확인한 후 앱을 다시 실행한다.
- /var/log/agent-app/monitor.log가 지정 포맷으로 누적 기록되는가?
  - 앱이 실행 중일 때, 수동 실행 전후의 로그 줄 수와 마지막 행을 비교한다.
    ```bash
    sudo wc -l /var/log/agent-app/monitor.log
    sudo -u agent-admin /home/agent-admin/agent-app/bin/monitor.sh
    sudo wc -l /var/log/agent-app/monitor.log
    sudo tail -n 1 /var/log/agent-app/monitor.log
    ```
  - 실행 뒤 로그가 한 줄 이상 늘어나고, 마지막 행이 `[YYYY-MM-DD HH:MM:SS] PID:... CPU:...% MEM:...% DISK_USED:...%` 형식이어야 한다.
- cron 매분 실행으로 monitor.log가 자동 증가하는가?
  - cron 서비스·등록 규칙·현재 로그를 순서대로 확인한다.
    ```bash
    sudo systemctl is-active cron
    sudo crontab -u agent-admin -l
    sudo tail -n 3 /var/log/agent-app/monitor.log
    ```
  - `cron`은 `active`여야 하며, crontab에는 다음 규칙이 있어야 한다.
    ```cron
    * * * * * /home/agent-admin/agent-app/bin/monitor.sh >/dev/null 2>&1
    ```
  - 앱을 실행한 채 1~2분 후 다시 `sudo tail -n 5 /var/log/agent-app/monitor.log`를 실행해, 새 시각의 로그 행이 자동으로 추가됐는지 확인한다.
- monitor.log 용량 관리(10MB/10개)가 설정되어 있고 동작을 설명할 수 있는가?
  - 우선 용량 한계와 회전 로직을 코드에서 확인한다.
    ```bash
    grep -nE 'MAX_LOG_(BYTES|FILES)|stat -c %s|rm -f|mv -f' \
      /home/agent-admin/agent-app/bin/monitor.sh
    ```
  - 실제 회전은 운영 로그를 채우지 않고, `LOG_DIR`만 별도 임시 디렉터리로 바꾼 사본에서 확인한다. 앱은 실행 상태여야 한다.
    ```bash
    TEST_DIR=/tmp/agent-monitor-rotation-test

    sudo install -d -o agent-admin -g agent-core -m 2770 "$TEST_DIR"
    sudo install -o agent-admin -g agent-core -m 750 \
      /home/agent-admin/agent-app/bin/monitor.sh "$TEST_DIR/monitor.sh"
    sudo sed -i 's|^LOG_DIR=.*|LOG_DIR="/tmp/agent-monitor-rotation-test"|' \
      "$TEST_DIR/monitor.sh"
    sudo chown agent-admin:agent-core "$TEST_DIR/monitor.sh"
    sudo chmod 750 "$TEST_DIR/monitor.sh"

    sudo -u agent-admin truncate -s 10485760 "$TEST_DIR/monitor.log"
    for index in $(seq 1 9); do
      sudo -u agent-admin touch "$TEST_DIR/monitor.log.$index"
    done

    sudo -u agent-admin "$TEST_DIR/monitor.sh"
    sudo find "$TEST_DIR" -maxdepth 1 -type f -name 'monitor.log*' -printf '%f\n' | sort
    ```
  - 실행 뒤 새 `monitor.log`와 과거 `.1`~`.9`가 남아 최대 10개여야 한다. 가장 오래된 기존 `.9`는 제거되고, 나머지 파일은 한 번호씩 뒤로 이동한다.

## 항목 2

- monitor.sh에서 프로세스 식별(pgrep/ps 등)과 포트 확인(ss/netstat 등)에 사용한 명령과 선택 이유를 설명할 수 있는가?
- CPU/MEM/DISK 값을 어떤 방식으로 추출/파싱했고, 로그 포맷을 왜 그 형태로 고정했는지 설명할 수 있는가?
- 소유자(agent-dev)와 실행자(agent-admin, cron) 권한 정책을 어떻게 만족시켰는지(소유/그룹/권한) 설명할 수 있는가?
- 용량 기반 로그 관리(10MB/10개)를 어떤 방식(logrotate/스크립트)으로 구현했는지 설명할 수 있는가?

## 항목 3

- SSH 포트 변경과 Root 접속 차단이 왜 보안에 효과적인지 위협 모델 관점에서 설명할 수 있는가?
- api_keys와 로그 디렉토리를 agent-core로 제한한 이유를 “최소 권한 원칙”으로 설명할 수 있는가?
- “경고는 출력하되 종료하지 않는 항목”(방화벽 비활성/임계치 초과)을 분리한 운영상의 이유를 설명할 수 있는가?
- 리다이렉션 기호 `>`와 `>>` 차이를 설명하고, 로그 누적에 `>>`가 필요한 이유를 설명할 수 있는가?

## 항목 4

- 모니터링 대상이 웹 서버(Nginx 등)로 바뀐다면, monitor.sh에서 바꿔야 할 핵심 포인트(프로세스/포트/로그/임계값)를 설명할 수 있는가?
- “프로세스는 살아있는 데 포트가 안 열리는 상황”을 발견했다면, 원인 후보와 확인 순서를 설명할 수 있는가?
- 로그가 급증해 디스크가 가득 찰 위험이 있다면, 운영자가 취할 대응(단기/중기)을 설명할 수 있는가?
