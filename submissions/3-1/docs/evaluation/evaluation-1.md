# 3-1 평가 항목 1 시연·답변 가이드

이 문서는 `evaluations/evaluation3-1.md`의 **항목 1**을 실제 CLI에서 재현하고, 각 결과를 평가자에게 어떻게 설명할지 정리한 가이드다. 평가에서는 내부 구조를 길게 설명하기보다 **명령 입력 → 출력 확인 → 그 출력이 의미하는 규칙 한 문장** 순서로 진행한다.

## 0. 시연 준비

터미널을 열고 아래 위치에서 프로그램을 실행한다.

```bash
cd /Users/seungwookim/Code/edu/Codyssey/2026_codyssey/submissions/3-1
python3 main.py
```

정상적으로 실행되면 아래 프롬프트가 보인다.

```text
mini-redis>
```

각 절은 **새 REPL에서 시작**하는 것을 권장한다. 앞 절의 키, `maxmemory`, `evicted_keys` 값이 다음 절의 결과에 영향을 주지 않기 때문이다. 한 절이 끝나면 `quit`을 입력하고 `python3 main.py`를 다시 실행한다.

시연 전에 다음 두 가지를 알고 있으면 좋다.

- `KEYS`의 출력 순서는 해시맵 버킷 순서이므로 고정되지 않는다. 키가 있는지 여부만 확인하고, 이 순서로 LRU 순서를 설명하지 않는다.
- `TTL`은 남은 시간을 정수로 내림해 출력하므로, `EXPIRE key 5` 직후에도 보통 `4`가 나온다. 시연에서는 정확한 숫자보다 **양수로 줄어든다**는 성질과 만료 뒤의 `-2`를 확인한다.

---

## 1. String 타입 기본 동작

### 평가 질문

> `SET`, `GET`, `DEL`, `EXISTS`, `DBSIZE`, `KEYS` 명령어가 모두 정상 동작하는가?

### 시작할 때 말할 문장

> 먼저 하나의 String 키를 저장한 뒤 조회·존재 확인·전체 개수·전체 키 목록을 확인하겠습니다. 그 다음 삭제하고, 삭제된 키가 없는 키처럼 처리되는지도 확인하겠습니다.

### 입력 순서와 기대 결과

아래 명령을 한 줄씩 입력한다.

```text
mini-redis> SET user:1 "Alice Kim"
OK
mini-redis> GET user:1
"Alice Kim"
mini-redis> EXISTS user:1
(integer) 1
mini-redis> DBSIZE
(integer) 1
mini-redis> KEYS
1. "user:1"
mini-redis> DEL user:1
(integer) 1
mini-redis> GET user:1
(nil)
mini-redis> EXISTS user:1
(integer) 0
mini-redis> DBSIZE
(integer) 0
mini-redis> KEYS
(empty array)
```

### 출력마다 할 설명

| 확인 지점 | 짧게 설명할 내용 |
| --- | --- |
| `SET` → `OK` | `user:1`에 공백을 포함한 String 값이 저장됐습니다. CLI는 큰따옴표로 묶인 값을 하나의 인자로 처리합니다. |
| `GET` → `"Alice Kim"` | 저장한 값이 그대로 반환됐습니다. 존재하는 키를 성공적으로 조회했으므로 이 키는 최근 사용한 키로도 갱신됩니다. |
| `EXISTS` → `1` | 저장 직후 키가 존재함을 정수 응답으로 확인했습니다. |
| `DBSIZE` → `1` | 현재 살아 있는 키가 하나임을 확인했습니다. |
| `KEYS` → `user:1` | 전체 키 목록에 저장한 키가 포함됩니다. 키가 여러 개라면 순서는 고정하지 않습니다. |
| `DEL` → `1` | 실제로 존재하던 키 하나를 삭제했다는 뜻입니다. |
| 이후 `GET`/`EXISTS`/`DBSIZE`/`KEYS` | 삭제 뒤에는 조회 결과가 `(nil)`이고, 존재 여부와 전체 개수도 0이며, 키 목록도 비어 있습니다. 따라서 삭제 상태가 모든 조회 명령에 일관되게 반영됩니다. |

### 코드와 연결해서 한 문장으로 답하기

> 모든 키 기반 명령은 먼저 살아 있는 엔트리를 확인합니다. 따라서 저장된 키는 정상 처리되고, 삭제되었거나 만료된 키는 같은 방식으로 없는 키처럼 응답합니다.

---

## 2. maxmemory 초과 시 LRU 자동 제거

### 평가 질문

> `maxmemory` 설정 후 제한 초과 시 가장 오래된 키가 자동 제거되는가?

### 시작할 때 말할 문장

> 이번에는 8바이트로 제한을 건 뒤, 어떤 키가 가장 오래 사용되지 않았는지를 `GET`으로 의도적으로 바꾸고, 제한을 넘는 새 키를 넣어 그 키가 제거되는지 확인하겠습니다.

### 입력 순서와 기대 결과

```text
mini-redis> CONFIG SET maxmemory 8
OK
mini-redis> SET a 11
OK
mini-redis> SET b 22
OK
mini-redis> GET a
"11"
mini-redis> SET c 333
OK
mini-redis> GET b
(nil)
mini-redis> GET a
"11"
mini-redis> GET c
"333"
mini-redis> INFO memory
used_memory:7
maxmemory:8
evicted_keys:1
```

### 이 순서가 LRU를 재현하는 이유

키와 값의 UTF-8 바이트 수를 더하면 각 엔트리 크기는 다음과 같다.

| 키 | 키 바이트 | 값 바이트 | 엔트리 바이트 |
| --- | ---: | ---: | ---: |
| `a` / `11` | 1 | 2 | 3 |
| `b` / `22` | 1 | 2 | 3 |
| `c` / `333` | 1 | 3 | 4 |

LRU의 앞은 가장 최근 사용(MRU), 뒤는 가장 오래 사용(LRU)이다.

```text
SET a, SET b 뒤:  b (MRU) -> a (LRU)
GET a 뒤:         a (MRU) -> b (LRU)
SET c 직후:        c (MRU) -> a -> b (LRU), 사용량 10바이트
자동 제거 뒤:      c (MRU) -> a, 사용량 7바이트
```

`SET c 333` 뒤의 총 사용량은 `3 + 3 + 4 = 10`바이트라 제한 8을 넘는다. 직전에 `GET a`를 했기 때문에 `b`가 LRU이며, 그래서 `GET b`가 `(nil)`이 된다. `a`나 `c`가 아니라 **정확히 `b`가 사라지는 것**이 LRU 자동 제거의 증거다.

### 평가자에게 할 핵심 설명

> `GET a`가 성공하면서 `a`가 최근 사용 위치로 이동했고, 그 결과 `b`가 가장 오래된 키가 됐습니다. 새 키 `c`를 저장해 10바이트가 되자 제한 이하가 될 때까지 LRU인 `b`를 자동 삭제했고, 수동 `DEL` 없이 `GET b`가 `(nil)`이 된 것으로 확인했습니다.

`KEYS`를 추가로 입력해 `a`, `c`만 남았음을 보일 수 있다. 단, `KEYS`의 나열 순서는 LRU 순서가 아니므로 순서 자체를 근거로 삼지 않는다.

---

## 3. `INFO memory`의 메모리 정보

### 평가 질문

> `INFO memory`에서 `used_memory`, `maxmemory`, `evicted_keys`가 규칙에 맞게 출력되는가?

### 재현 방법

바로 앞의 LRU 시연 마지막 상태에서 다음 결과를 이미 확인할 수 있다.

```text
mini-redis> INFO memory
used_memory:7
maxmemory:8
evicted_keys:1
```

### 평가자에게 할 핵심 설명

> `used_memory`는 자료구조 자체의 오버헤드를 빼고 키와 값의 UTF-8 바이트 길이만 합산합니다. 남아 있는 `a`는 `1 + 2 = 3`바이트, `c`는 `1 + 3 = 4`바이트이므로 합계가 7입니다. `maxmemory`는 제가 설정한 8이고, 자동 LRU 제거가 한 번 발생했으므로 `evicted_keys`는 1입니다.

추가로 꼭 구분해서 말한다.

- `evicted_keys`는 메모리 초과로 자동 축출한 횟수다.
- 사용자가 실행한 `DEL`이나 TTL 만료로 인한 삭제는 이 카운터를 증가시키지 않는다.
- `CONFIG SET maxmemory 0`은 메모리 제한이 없다는 뜻이다.

---

## 4. TTL 설정·조회와 만료 키 제거

### 평가 질문

> `EXPIRE`/`TTL` 규칙이 동작하며 만료된 키가 적절히 제거되는가?

### `EXPIRE` 명령어 사용법

`EXPIRE`는 이미 저장된 키에 **유효기간(TTL, Time To Live)** 을 설정하는 명령어다. 지정한 시간이 지나면 해당 키는 만료되어 없는 키처럼 처리된다.

```text
EXPIRE <key> <seconds>
```

| 입력 요소 | 의미 | 예시 |
| --- | --- | --- |
| `<key>` | TTL을 설정할, 이미 존재하는 키 | `session` |
| `<seconds>` | 지금부터 만료될 때까지의 초 단위 정수 | `5` |

예를 들어 아래 명령은 `session` 키를 지금부터 5초 동안만 유지한다.

```text
mini-redis> SET session active
OK
mini-redis> EXPIRE session 5
(integer) 1
```

반환값은 다음처럼 읽으면 된다.

| 상황 | 결과 | 의미 |
| --- | --- | --- |
| 키가 존재하고 `seconds > 0` | `(integer) 1` | TTL 설정 성공 |
| 키가 없음 | `(integer) 0` | 설정할 대상이 없음 |
| 키가 존재하고 `seconds <= 0` | `(integer) 1` | 즉시 만료 처리로 키를 삭제함 |
| `seconds`가 정수가 아님 | `(error) ERR value is not an integer or out of range` | 초 단위 정수만 허용 |

`EXPIRE`는 키를 새로 만드는 명령이 아니다. 따라서 먼저 `SET` 등으로 키를 저장해야 하며, 설정 뒤에는 `TTL <key>`로 남은 시간을 확인한다.

### 시작할 때 말할 문장

> TTL이 없는 키, 없는 키에 TTL을 설정하는 경우, 정상적으로 만료되는 키를 차례로 보이겠습니다. 만료 시간이 지난 뒤에는 다음 명령 처리 전에 키를 정리하므로 없는 키와 같은 응답이 나와야 합니다.

### 4-1. 기본 TTL과 실제 만료 재현

새 REPL에서 아래를 한 줄씩 입력한다.

```text
mini-redis> SET permanent value
OK
mini-redis> TTL permanent
(integer) -1
mini-redis> EXPIRE missing 5
(integer) 0
mini-redis> SET session active
OK
mini-redis> EXPIRE session 5
(integer) 1
mini-redis> TTL session
(integer) N
```

여기서 `N`은 남은 초다. 입력 직후에는 보통 `4`가 보이며, 입력·설명에 걸린 시간에 따라 `0`부터 `4` 사이의 값이 될 수 있다. 양수 TTL을 설정한 직후에는 **정확히 5가 아니어도 정상**이다. 구현이 소수점 남은 시간을 정수로 내림하기 때문이다.

이제 **6초 이상 기다린 뒤** 아래를 입력한다.

```text
mini-redis> GET session
(nil)
mini-redis> TTL session
(integer) -2
mini-redis> EXISTS session
(integer) 0
mini-redis> DBSIZE
(integer) 1
```

`permanent`만 남았으므로 `DBSIZE`는 1이다. `GET session`을 먼저 실행한 이유는, 만료된 키가 조회 시 실제 삭제되고 `(nil)`로 처리되는 모습을 가장 직관적으로 보이기 위해서다.

### 4-2. TTL 엣지 규칙도 짧게 확인하기

시간이 허락하면 바로 이어서 아래 두 규칙도 시연한다.

```text
mini-redis> SET immediate x
OK
mini-redis> EXPIRE immediate 0
(integer) 1
mini-redis> TTL immediate
(integer) -2

mini-redis> SET refresh old
OK
mini-redis> EXPIRE refresh 10
(integer) 1
mini-redis> SET refresh new
OK
mini-redis> TTL refresh
(integer) -1
```

- `EXPIRE immediate 0`은 존재하는 키를 즉시 삭제하므로 성공 응답 `1` 뒤에 TTL은 `-2`가 된다.
- `SET refresh new`는 기존 TTL을 초기화한다. 그래서 `refresh`는 존재하지만 TTL이 없는 상태인 `-1`이 된다.

### 평가자에게 할 핵심 설명

> `TTL`의 `-1`은 키는 있지만 만료 시간이 없다는 뜻이고, `-2`는 키가 없거나 이미 만료됐다는 뜻입니다. 만료 시각은 최소 힙으로 관리하며, 명령을 처리하기 전에 만료 티켓을 확인해 실제 데이터·LRU·메모리 사용량까지 함께 정리합니다. 따라서 만료된 `session`은 `GET`에서 값을 반환하거나 LRU를 갱신하지 않고 `(nil)`이 됩니다.

---

## 5. 표준 형식의 에러 처리

### 평가 질문

> 잘못된 명령, 인자 개수, 정수 오류, OOM이 표준 형식으로 출력되는가?

### 시작할 때 말할 문장

> 마지막으로 오류 종류별로 한 번씩 입력해, 오류가 예외로 종료되지 않고 Redis 스타일 문자열로 일관되게 출력되는지 확인하겠습니다.

### 입력 순서와 기대 결과

새 REPL에서 아래를 입력한다.

```text
mini-redis> HELLO
(error) ERR unknown command 'HELLO'
mini-redis> GET
(error) ERR wrong number of arguments for 'GET' command
mini-redis> CONFIG SET maxmemory abc
(error) ERR value is not an integer or out of range
mini-redis> CONFIG SET maxmemory 3
OK
mini-redis> SET a 123
(error) OOM command not allowed when used_memory > 'maxmemory'
mini-redis> INFO memory
used_memory:0
maxmemory:3
evicted_keys:0
```

### OOM까지 설명하는 방법

`SET a 123`의 크기는 키 `a` 1바이트와 값 `123` 3바이트를 합쳐 4바이트다. 설정한 제한은 3바이트이므로 **이 엔트리 하나만으로도 제한을 넘는다**. 이 경우에는 다른 키를 축출해도 저장할 수 없으므로 저장하지 않고 OOM 오류를 반환한다. 마지막 `INFO memory`의 `used_memory:0`은 실패한 데이터가 저장되지 않았음을 확인해 준다.

### 평가자에게 할 핵심 설명

> 오류는 네 종류 모두 `(error) ERR ...` 또는 `(error) OOM ...` 형식으로 반환됩니다. 특히 OOM은 단일 엔트리가 제한보다 큰 경우 기존 상태를 바꾸지 않고 거절하므로, 잘못된 저장으로 메모리 제한 규칙이 깨지지 않습니다.


