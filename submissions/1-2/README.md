# 1-2. 컴퓨터가 갑자기 느려지거나 멈췄을 때 원인 찾아 고치기

Docker `linux/arm64` 환경에서 과제용 `agent-leak-app`의 OOM, CPU 과점유, Deadlock을 재현하고, 대상 프로세스 관제값과 애플리케이션 로그를 근거로 분석한 결과물이다.

## 구성

- `docker/Dockerfile`: Ubuntu 22.04 ARM64 실행 이미지
- `docker/compose.yaml`: `15034:15034` 포트와 케이스별 환경변수 설정
- `docker/app/agent-app-linux-arm64`: 과제용 ARM64 실행 바이너리
- `docker/monitor.sh`: 대상 프로세스의 PID, CPU, MEM, RSS, 상태, 포트를 수집하는 1회성 관제 스크립트
- `run_case.sh`: 장애 유형별 Before/After 실행과 증거 수집
- `reports/`: GitHub Issue 형식의 장애 분석 리포트
- `evidence/`: 실행별 원본 로그, 명령 출력, Docker 상태

ARM64 바이너리는 작업 폴더에 준비된 과제용 미션 바이너리를 `docker/app/` 아래에 포함했다. Docker Engine과 바이너리 모두 `linux/arm64`이며, 바이너리 디컴파일이나 리버스 엔지니어링은 수행하지 않았다.

## 실행 환경

이미지는 앱의 내부 `MEMORY_LIMIT` 최대값보다 높은 1GiB cgroup 한도를 사용한다. 따라서 OOM 실험에서는 Docker cgroup OOM Kill보다 앱의 `MemoryGuard` 또는 내부 정리 동작을 먼저 관찰할 수 있다.

컨테이너 내부 앱은 root가 아닌 `agent-admin`(uid=10001) 사용자로 실행된다.

~~~text
AGENT_HOME=/opt/agent
AGENT_PORT=15034
AGENT_UPLOAD_DIR=/opt/agent/upload_files
AGENT_KEY_PATH=/opt/agent/api_keys
AGENT_LOG_DIR=/var/log/agent-app
~~~

부트 시퀀스에서 6단계가 모두 `[OK]`이고 `Agent READY`가 출력되는 것을 각 실행 로그에서 확인했다. `secret.key`는 `agent_api_key_test` 값으로 포함했다.

## 재현 명령

저장소 루트에서 실행한다. 실행 결과는 `evidence/<case>/<phase>/<timestamp>/`에 저장된다.

~~~bash
cd submissions/1-2
chmod +x docker/monitor.sh run_case.sh

./run_case.sh oom before 128
./run_case.sh oom after 512

# 과제 계획표의 CPU 비교: 10 -> 100
CASE_TIMEOUT_SEC=40 ./run_case.sh cpu before 10
CASE_TIMEOUT_SEC=40 ./run_case.sh cpu after 100

./run_case.sh deadlock before true
./run_case.sh deadlock after false
~~~

CPU 케이스의 실제 바이너리 동작은 `CPU_MAX_OCCUPY=100`에서 `CPU Threshold Violated!`가 발생하고 `10`에서는 `Peak reached`/`Cooldown`으로 제한된다. 따라서 과제 계획표의 10 -> 100 비교와 함께, 우회 조치 검증인 100 -> 10 실행도 보관했다.

## 실행 결과 요약

| 장애 | 계획표 Before | 계획표 After | 관측 결과 |
| --- | --- | --- | --- |
| OOM | `MEMORY_LIMIT=128` | `512` | Before는 RSS 16.4 -> 141.5MB 후 `MemoryGuard` 종료, After는 525MB에서 정리 후 계속 실행 |
| CPU | `CPU_MAX_OCCUPY=10` | `100` | 10%는 안정적인 cooldown, 100%는 약 28초 후 CPU threshold 위반 |
| Deadlock | `MULTI_THREAD_ENABLE=true` | `false` | true는 두 락의 순환 대기, false는 Scheduler 완료 및 워커 진행 |

## 증거 수집 방식

각 실행에서 다음 자료를 함께 저장한다.

- `application.log`: 컨테이너 표준 출력과 표준 오류
- `app-log/`: 컨테이너 내부 `/var/log/agent-app` 파일
- `observations.log`: `monitor.sh`, `ps`, `top -H`, `ps -L`, `docker stats` 출력
- `container-inspect.json`: 종료 상태, 종료 코드, cgroup 메모리 한도, 실행 사용자
- `run-metadata.txt`: 케이스별 환경변수, ARM64 호스트와 바이너리 정보

`monitor.sh`는 시스템 전체 메모리가 아니라 대상 앱 프로세스와 자식 워커의 RSS를 기록한다. `docker stats`는 1GiB cgroup 안에서의 컨테이너 전체 사용량을 보조 자료로 사용한다.
캡처 PNG는 위 원본 로그와 명령 출력을 터미널 형태로 정리한 비교 화면이며, 각 화면 하단에 원본 실행 디렉터리를 표시한다.
UFW 정책은 컨테이너 내부에서 판단하지 않고, 앱의 `0.0.0.0:15034` LISTEN 상태와 프로세스·로그 증거에 집중했다.

## 주요 실행 증거

- [OOM Before/After 캡처](evidence/captures/oom-comparison.png)
- [CPU Before/After 캡처](evidence/captures/cpu-comparison.png)
- [Deadlock Before/After 캡처](evidence/captures/deadlock-comparison.png)
- [OOM Before 로그](evidence/oom/before/20260915-140016-61131/application.log) / [OOM After 로그](evidence/oom/after/20260915-140104-61678/application.log)
- [CPU 계획표 Before 로그](evidence/cpu/before/20260915-141452-66829/application.log) / [CPU 계획표 After 로그](evidence/cpu/after/20260915-141620-67680/application.log)
- [Deadlock Before 로그](evidence/deadlock/before/20260915-140644-64188/application.log) / [Deadlock After 로그](evidence/deadlock/after/20260915-141042-65094/application.log)
- CPU 우회 검증: [100% 실행](evidence/cpu/before/20260915-140355-62651/application.log), [10% 실행](evidence/cpu/after/20260915-140458-63304/application.log)

## 분석 리포트

- [OOM / Memory Leak](reports/oom.md)
- [CPU 과점유](reports/cpu.md)
- [Deadlock](reports/deadlock.md)
