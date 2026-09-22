# Mini Redis

해시맵, 이중 연결 리스트, 최소 힙을 직접 구현해 만든 CLI 기반 In-Memory Key-Value 저장소입니다. String 타입의 기본 명령, LRU 기반 메모리 제한, TTL 만료를 지원합니다.

## 실행 방법

Python 3.8 이상이 필요합니다.

```bash
cd submissions/3-1
python3 main.py
```

실행하면 아래처럼 명령을 입력하는 REPL 환경이 시작됩니다.

```text
mini-redis> SET user:1 "Alice Kim"
OK
mini-redis> GET user:1
"Alice Kim"
```

`exit` 또는 `quit`을 입력하면 종료합니다.

```text
mini-redis> quit
```

## 입력 규칙

- 명령어는 대소문자를 구분하지 않습니다. 예를 들어 `set`, `SET`, `Set` 모두 사용할 수 있습니다.
- 값에 공백이 없다면 그대로 입력합니다. 예: `SET name Alice`
- 값에 공백이 있다면 큰따옴표로 묶습니다. 예: `SET name "Alice Kim"`
- 키와 값은 문자열로 처리합니다.
- 각 명령은 Redis 스타일의 `OK`, `(nil)`, `(integer) N`, `(error) ...` 형식으로 결과를 출력합니다.

## 명령어 한눈에 보기

| 구분 | 명령 | 설명 |
| --- | --- | --- |
| String | `SET key value` | 키에 문자열 값 저장 |
| String | `GET key` | 키의 문자열 값 조회 |
| String | `DEL key` | 키 삭제 |
| String | `EXISTS key` | 키 존재 여부 확인 |
| String | `DBSIZE` | 저장된 키 개수 확인 |
| String | `KEYS` | 모든 키 목록 출력 |
| 메모리 | `CONFIG SET maxmemory bytes` | 최대 메모리 제한 설정 |
| 메모리 | `INFO memory` | 메모리 사용량과 eviction 정보 출력 |
| TTL | `EXPIRE key seconds` | 키의 유효기간 설정 |
| TTL | `TTL key` | 키의 남은 유효기간 확인 |

---

## String 명령어

### `SET key value`

키에 String 값을 저장하거나, 기존 값을 새 값으로 덮어씁니다.

```text
SET <key> <value>
```

```text
mini-redis> SET user:1 "Alice Kim"
OK
mini-redis> SET score 100
OK
```

| 상황 | 동작 |
| --- | --- |
| 새 키 | 키와 값을 저장하고 LRU에서 최근 사용 위치로 등록 |
| 기존 키 | 값을 덮어쓰고, 기존 TTL을 삭제한 뒤 LRU 최근 사용 위치로 이동 |
| 값에 공백 포함 | 큰따옴표로 묶어 입력. 예: `SET greeting "hello world"` |
| 단일 엔트리가 `maxmemory`보다 큼 | 저장하지 않고 OOM 오류 반환 |

성공하면 `OK`를 반환합니다. 값의 메모리 크기는 키와 값의 UTF-8 바이트 길이를 합산해 계산합니다.

### `GET key`

키의 값을 조회합니다.

```text
GET <key>
```

```text
mini-redis> GET user:1
"Alice Kim"
mini-redis> GET missing-key
(nil)
```

| 결과 | 의미 |
| --- | --- |
| `"value"` | 키가 존재하며 저장된 값을 반환 |
| `(nil)` | 키가 없거나 이미 TTL 만료됨 |

성공한 `GET`은 해당 키를 LRU의 최근 사용 위치로 이동합니다. 없는 키 또는 만료된 키를 조회할 때는 LRU 순서를 갱신하지 않습니다.

### `DEL key`

키를 삭제합니다.

```text
DEL <key>
```

```text
mini-redis> DEL user:1
(integer) 1
mini-redis> DEL user:1
(integer) 0
```

| 결과 | 의미 |
| --- | --- |
| `(integer) 1` | 존재하던 키를 삭제함 |
| `(integer) 0` | 삭제할 키가 없음 |

삭제 시 데이터뿐 아니라 LRU 노드, TTL 정보, `used_memory`도 함께 정리합니다.

### `EXISTS key`

키가 현재 존재하는지 확인합니다.

```text
EXISTS <key>
```

```text
mini-redis> EXISTS user:1
(integer) 1
mini-redis> EXISTS missing-key
(integer) 0
```

| 결과 | 의미 |
| --- | --- |
| `(integer) 1` | 키가 존재하고 아직 만료되지 않음 |
| `(integer) 0` | 키가 없거나 이미 TTL 만료됨 |

`EXISTS`는 단순한 존재 확인이므로 LRU 사용 순서를 바꾸지 않습니다.

### `DBSIZE`

현재 저장된 살아 있는 키의 개수를 반환합니다.

```text
DBSIZE
```

```text
mini-redis> DBSIZE
(integer) 2
```

TTL이 만료된 키는 먼저 정리되므로 개수에 포함되지 않습니다.

### `KEYS`

현재 저장된 살아 있는 모든 키를 출력합니다. 패턴 검색은 지원하지 않습니다.

```text
KEYS
```

```text
mini-redis> KEYS
1. "score"
2. "user:1"
```

저장된 키가 없으면 다음을 출력합니다.

```text
(empty array)
```

키 목록의 순서는 해시맵 버킷 순서이므로 정렬 순서나 LRU 순서를 보장하지 않습니다.

---

## 메모리 관리 명령어

### `CONFIG SET maxmemory bytes`

저장소가 사용할 수 있는 최대 메모리를 바이트 단위로 설정합니다.

```text
CONFIG SET maxmemory <bytes>
```

```text
mini-redis> CONFIG SET maxmemory 30
OK
mini-redis> CONFIG SET maxmemory 0
OK
```

| 입력 | 동작 |
| --- | --- |
| 0 이상의 정수 | 최대 메모리 설정 |
| `0` | 메모리 제한 없음 |
| 음수 또는 정수가 아닌 값 | `(error) ERR value is not an integer or out of range` |

`maxmemory`가 0보다 크고 저장 후 `used_memory`가 제한을 넘으면, 가장 오래 사용하지 않은 키(LRU)부터 제거해 제한 이하가 될 때까지 반복합니다. 더 작은 제한으로 다시 설정했을 때도 즉시 LRU eviction을 수행합니다.

### `INFO memory`

현재 메모리 상태를 출력합니다.

```text
INFO memory
```

```text
mini-redis> CONFIG SET maxmemory 30
OK
mini-redis> SET user:1 Alice
OK
mini-redis> INFO memory
used_memory:11
maxmemory:30
evicted_keys:0
```

| 항목 | 의미 |
| --- | --- |
| `used_memory` | 살아 있는 모든 키와 값의 UTF-8 바이트 길이 합계 |
| `maxmemory` | 설정된 최대 메모리. 0은 무제한 |
| `evicted_keys` | 메모리 초과로 자동 제거된 키의 누적 개수 |

노드, 포인터, 버킷 같은 자료구조의 메모리 오버헤드는 `used_memory` 계산에서 제외합니다. 수동 `DEL`이나 TTL 만료 삭제는 `evicted_keys`에 포함하지 않습니다.

### LRU란?

LRU(Least Recently Used)는 **가장 오래 사용하지 않은 데이터부터 제거하는 캐시 정책**입니다. 메모리가 가득 찼을 때 최근에 조회하거나 저장한 키는 남기고, 오랫동안 사용하지 않은 키를 먼저 제거해 자주 쓰는 데이터를 더 오래 유지합니다.

이 Mini Redis에서는 다음 규칙으로 LRU 순서를 관리합니다.

- 새 키를 `SET`하면 최근 사용(MRU) 위치가 됩니다.
- 이미 존재하는 키를 `SET`하거나 성공적으로 `GET`하면 최근 사용 위치로 이동합니다.
- `maxmemory`를 초과하면 가장 오래 사용하지 않은(LRU) 키부터 자동 제거합니다.

즉, LRU는 데이터를 찾는 기능이 아니라 **메모리가 부족할 때 어떤 키를 지울지 결정하는 기준**입니다.

### LRU 동작 예시

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
mini-redis> INFO memory
used_memory:7
maxmemory:8
evicted_keys:1
```

`a`와 `b`는 각각 3바이트, `c`는 4바이트입니다. `GET a`로 `a`를 최근 사용 키로 만든 뒤 `c`를 저장하면 총 10바이트가 됩니다. 이때 가장 오래된 `b`가 자동 제거되어 최종 사용량은 7바이트가 됩니다.

---

## TTL 명령어

TTL(Time To Live)은 키마다 설정하는 **유효기간**입니다. `EXPIRE`로 "지금부터 몇 초 뒤에 만료할지"를 정하면, 그 시간이 지난 키는 더 이상 조회할 수 없습니다.

예를 들어 로그인 세션에 3,600초 TTL을 설정하면, 마지막 사용 여부와 관계없이 1시간이 지나면 만료됩니다. 이 점이 사용 빈도·순서를 기준으로 제거하는 LRU와의 차이입니다.

| 구분 | LRU | TTL |
| --- | --- | --- |
| 제거 기준 | 메모리 부족 시, 가장 오래 사용하지 않은 키 | 설정한 만료 시각 도달 |
| 제거 시점 | `maxmemory` 초과 시 | TTL 시간이 지난 뒤 다음 명령 처리 시 |
| 대표 용도 | 제한된 메모리에서 캐시 유지 | 세션, 인증 코드, 임시 데이터의 자동 만료 |

만료된 키는 다음 명령을 처리하기 전에 정리되며, 이후에는 없는 키와 같은 응답을 받습니다.

### `EXPIRE key seconds`

이미 존재하는 키에 초 단위 TTL을 설정합니다.

```text
EXPIRE <key> <seconds>
```

```text
mini-redis> SET session active
OK
mini-redis> EXPIRE session 10
(integer) 1
```

| 상황 | 결과 | 의미 |
| --- | --- | --- |
| 키가 존재하고 `seconds > 0` | `(integer) 1` | TTL 설정 성공 |
| 키가 없음 | `(integer) 0` | TTL을 설정할 대상이 없음 |
| 키가 존재하고 `seconds <= 0` | `(integer) 1` | 즉시 만료 처리로 키 삭제 |
| `seconds`가 정수가 아님 | `(error) ERR value is not an integer or out of range` | 초 단위 정수만 허용 |

`EXPIRE`는 키를 새로 만드는 명령이 아닙니다. 먼저 `SET` 등으로 키를 저장해야 합니다.

### `TTL key`

키에 설정된 TTL의 남은 시간을 초 단위 정수로 반환합니다.

```text
TTL <key>
```

```text
mini-redis> TTL session
(integer) 9
```

| 결과 | 의미 |
| --- | --- |
| `(integer) N` | N초가 남아 있음 |
| `(integer) -1` | 키는 존재하지만 TTL이 설정되지 않음 |
| `(integer) -2` | 키가 없거나 이미 만료됨 |

남은 시간은 정수로 내림해 출력합니다. 따라서 `EXPIRE session 10` 직후의 `TTL session`도 보통 `9`가 출력됩니다.

### TTL 만료 예시

```text
mini-redis> SET session active
OK
mini-redis> EXPIRE session 3
(integer) 1
mini-redis> TTL session
(integer) 2

# 4초 이상 기다린 뒤
mini-redis> GET session
(nil)
mini-redis> TTL session
(integer) -2
```

TTL을 다시 설정하거나 `SET`으로 기존 키를 덮어쓰면 이전 TTL 기록은 무효화됩니다. 최소 힙에는 이전 만료 기록이 남을 수 있지만, 버전 값을 비교하는 lazy deletion 방식으로 오래된 기록을 안전하게 무시합니다.

---

## 오류 형식

| 상황 | 예시 입력 | 출력 |
| --- | --- | --- |
| 알 수 없는 명령 | `HELLO` | `(error) ERR unknown command 'HELLO'` |
| 인자 개수 오류 | `GET` | `(error) ERR wrong number of arguments for 'GET' command` |
| 정수 파싱 오류 | `CONFIG SET maxmemory abc` | `(error) ERR value is not an integer or out of range` |
| 인용 문자열 오류 | `SET name "Alice` | `(error) ERR invalid quoted string` |
| 단일 엔트리가 메모리 제한 초과 | `CONFIG SET maxmemory 3` 후 `SET a 123` | `(error) OOM command not allowed when used_memory > 'maxmemory'` |

OOM은 키와 값 하나의 크기 자체가 `maxmemory`보다 큰 경우에 발생합니다. 이 경우 저장은 수행되지 않으며, 기존 키나 메모리 사용량은 바뀌지 않습니다.

## 세 자료구조의 관계

하나의 키는 해시맵에서 `CacheEntry`를 찾는 것으로 시작합니다. 아래 그림에서 `CacheEntry`는 흔히 RedisEntry라고 부르는 "키 하나의 실제 데이터와 메타데이터"이며, 이 코드에서는 `CacheEntry`라는 이름을 사용합니다.

```text
                              Key
                               │
                               ▼
                    ┌──────────────────┐
                    │ ChainedHashMap   │
                    └────────┬─────────┘
                             │ key → CacheEntry
                             ▼
                         CacheEntry
                   ┌─────────┼──────────┐
                   │         │          │
                   ▼         ▼          ▼
                value    lru_node   expire_at
                                     ttl_version
                              │          │
                              ▼          ▼
                   DoublyLinkedList    MinHeap
                    최근(MRU) ⇄ 오래됨(LRU)  최소 만료 시각

                              MinHeap에는
                   (expire_at, key, version) 티켓을 저장
```

- **해시맵**은 `key → CacheEntry`를 빠르게 찾아 `GET`, `SET`, `DEL`의 시작점이 됩니다.
- **이중 연결 리스트**는 `CacheEntry.lru_node`를 통해 최근 사용 순서를 유지합니다. 맨 앞은 가장 최근에 사용한 키이고, 맨 뒤는 메모리 부족 시 먼저 제거할 LRU 키입니다.
- **최소 힙**은 `EXPIRE`가 만든 만료 기록을 보관합니다. 맨 위에는 가장 빨리 만료될 키가 있으므로, 만료 여부를 빠르게 확인할 수 있습니다.

즉, `GET`은 **해시맵으로 찾고 → 이중 연결 리스트에서 최근 사용 위치로 옮기며**, TTL 정리는 **최소 힙에서 가장 이른 만료 시각을 확인**합니다. 메모리 초과 시에는 이중 연결 리스트의 마지막 키를 가져와 해시맵에서 삭제합니다.

## 내부 구성

| 파일 | 역할 |
| --- | --- |
| [`mini_redis/hash_map.py`](mini_redis/hash_map.py) | 직접 구현한 DJB2 계열 해시 함수와 체이닝 해시맵 |
| [`mini_redis/linked_list.py`](mini_redis/linked_list.py) | LRU와 해시 충돌 체이닝에 사용하는 이중 연결 리스트 |
| [`mini_redis/min_heap.py`](mini_redis/min_heap.py) | 가장 빠른 TTL 만료 시각을 찾는 최소 힙 |
| [`mini_redis/store.py`](mini_redis/store.py) | 명령 처리, LRU eviction, TTL 및 메모리 상태 관리 |
| [`mini_redis/cli.py`](mini_redis/cli.py) | `shlex` 기반 명령 파싱과 REPL 출력 |

평가 시 명령별 시연과 설명은 [`docs/evaluation/evaluation-1.md`](docs/evaluation/evaluation-1.md)에서 확인할 수 있습니다.
