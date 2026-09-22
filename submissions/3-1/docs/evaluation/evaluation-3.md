# 3-1 평가 항목 3 답변 가이드

이 문서는 `evaluations/evaluation3-1.md`의 **항목 3**에 답할 때 사용할 설명을 정리한 것이다. 설명은 현재 구현인 `mini_redis/store.py`, `mini_redis/linked_list.py`, `mini_redis/hash_map.py`, `mini_redis/min_heap.py`를 기준으로 한다.

## 먼저 한 번에 답하기

> LRU에는 키를 빠르게 찾는 해시맵과 최근 사용 순서를 빠르게 바꾸는 이중 연결 리스트가 모두 필요합니다. 해시맵은 `key -> CacheEntry`를 평균 O(1)에 찾고, `CacheEntry`가 기억한 `lru_node`를 이중 연결 리스트의 맨 앞으로 O(1)에 옮깁니다. 리스트의 맨 뒤는 항상 LRU이므로 메모리 초과 시 바로 축출할 수 있습니다. TTL은 가장 이른 만료 시각을 먼저 알아야 하므로 `(expire_at, key, version)`을 최소 힙에 넣습니다. 명령 시작 시 힙의 최솟값부터 만료된 키를 정리하고, `GET`은 살아 있는 키일 때만 값을 반환하면서 LRU 순서를 갱신합니다. 저장 뒤 `used_memory`가 `maxmemory`를 넘으면 LRU 키를 반복 삭제하고, 삭제한 바이트만큼 사용량을 줄이며 `evicted_keys`를 증가시킵니다.

---

## 1. LRU에서 해시맵과 이중 연결 리스트는 각각 무엇을 하는가?

### 역할 분담

| 자료구조 | 저장하는 내용 | LRU에서 맡는 일 |
| --- | --- | --- |
| `ChainedHashMap` (`_data`) | `key -> CacheEntry` | 문자열 키로 캐시 엔트리를 찾는다. |
| `DoublyLinkedList` (`_lru`) | `CacheEntry`를 담은 노드 | 최근 사용 순서를 유지한다. 앞은 MRU, 뒤는 LRU다. |
| `CacheEntry.lru_node` | 해당 엔트리가 들어 있는 LRU 노드 | 해시맵으로 찾은 엔트리에서 리스트 노드로 바로 이동하게 한다. |

```text
해시맵 _data
"user:1" -> CacheEntry(key="user:1", value="Alice", lru_node=노드 A)
"user:2" -> CacheEntry(key="user:2", value="Bob",   lru_node=노드 B)

LRU 이중 연결 리스트 _lru
MRU                                                     LRU
head <-> [노드 A: CacheEntry user:1] <-> [노드 B: CacheEntry user:2] <-> tail
```

해시맵만 사용하면 키로 값은 빠르게 찾을 수 있지만, 어떤 키가 가장 오래 사용되지 않았는지는 알 수 없다. 반대로 이중 연결 리스트만 사용하면 최근 사용 순서는 관리할 수 있지만, `GET user:1000`을 하려면 앞에서부터 키를 찾아 O(n)이 걸린다. 두 자료구조를 함께 써야 조회와 순서 갱신을 모두 빠르게 처리할 수 있다.

### 새 키·기존 키·삭제 시의 일관성

| 상황 | 해시맵 | LRU 리스트 |
| --- | --- | --- |
| 새 키 `SET` | 새 `CacheEntry`를 키에 연결한다. | 새 노드를 맨 앞(MRU)에 추가하고 그 노드를 `entry.lru_node`에 저장한다. |
| 기존 키 `SET` | 기존 엔트리의 값과 메모리 크기를 갱신한다. | 기존 `lru_node`를 맨 앞으로 이동한다. |
| 성공한 `GET` | 키로 엔트리를 찾는다. | 해당 `lru_node`를 맨 앞으로 이동한다. |
| `DEL`, TTL 만료, eviction | 키를 해시맵에서 제거한다. | 같은 엔트리의 `lru_node`도 제거한다. |

키를 삭제할 때 한쪽 자료구조에만 남기면 잘못된 LRU 후보가 생기거나, 이미 없는 키를 조회할 수 있다. 그래서 `_delete_key`은 해시맵, LRU 노드, TTL 상태, `used_memory`를 한 흐름에서 함께 정리한다.

---

## 2. O(1) LRU는 “조회 + 리스트 이동”으로 어떻게 달성하는가?

### 성공한 `GET`의 LRU 갱신

```text
GET user:1
  -> 해시맵에서 "user:1"의 CacheEntry를 평균 O(1)에 찾는다.
  -> entry.lru_node를 읽는다.
  -> move_to_front(entry.lru_node)를 호출한다.
  -> 이전·다음 노드의 연결만 바꿔 MRU 위치로 옮긴다.
```

예를 들어 아래 상태에서 `GET B`가 성공했다고 하자.

```text
조회 전: head <-> A <-> B <-> C <-> tail
                             ↑
                            LRU

GET B 후: head <-> B <-> A <-> C <-> tail
                                         ↑
                                        LRU
```

`B`를 찾기 위해 리스트를 다시 순회하지 않는 점이 핵심이다. 해시맵이 `CacheEntry`를 찾고, 그 엔트리가 이미 `lru_node`를 들고 있으므로 이중 연결 리스트는 `prev`, `next` 몇 개만 바꿔 O(1)에 이동한다.

### LRU 후보 찾기와 제거

리스트의 앞은 MRU, 뒤는 LRU로 약속했다.

```text
head <-> [최근 사용] <-> [오래 사용하지 않음] <-> tail
                                  ^
                           tail.prev, eviction 대상
```

따라서 메모리가 부족할 때 `_lru.last_node()`로 LRU 노드를 O(1)에 얻는다. 해당 노드의 `data`는 `CacheEntry`이므로 키를 알고 있고, `_delete_key(entry.key, evicted=True)`로 해시맵·LRU·TTL·메모리 정보를 함께 제거한다.

### 시간 복잡도에서 말할 점

| 작업 | 시간 복잡도 | 근거 |
| --- | --- | --- |
| 키로 `CacheEntry` 조회 | 평균 O(1) | 해시맵으로 해당 버킷을 찾는다. |
| 이미 찾은 노드의 MRU 이동 | O(1) | 이웃 노드의 연결만 바꾼다. |
| LRU 후보 찾기 | O(1) | `tail.prev`를 바로 읽는다. |
| LRU 노드 제거 | O(1) | 해당 노드를 이미 알고 있어 양옆 연결만 끊는다. |

엄밀히 말하면 문자열 키의 해시 계산은 키 길이에 비례하고, 충돌이 한 버킷에 몰리면 해시맵 조회는 최악 O(n)이다. 여기서 말하는 O(1)은 해시가 고르게 분산되고 로드 팩터가 관리된다는 일반적인 평균 시간 복잡도다.

---

## 3. TTL 관리에 최소 힙을 사용하는 이유는 무엇인가?

TTL은 “가장 오래 사용하지 않은 키”가 아니라 **가장 먼저 만료되는 키**를 찾아야 한다. TTL이 있는 모든 키를 매 명령마다 순회하면 다음 만료 키를 찾는 데 O(n)이 걸린다.

최소 힙은 가장 작은 값을 루트에 둔다. 이 구현은 TTL 티켓을 아래 형태로 저장한다.

```text
(expire_at, key, version)
```

| 값 | 의미 |
| --- | --- |
| `expire_at` | 키가 만료되는 단조 시각(`time.monotonic`) |
| `key` | 만료 여부를 다시 확인할 키 |
| `version` | 이 티켓이 현재 TTL 설정과 같은 버전인지 확인하는 번호 |

튜플의 첫 값인 `expire_at`이 우선 비교되므로, 힙의 루트에는 가장 이른 만료 시각의 티켓이 온다.

```text
힙의 루트
  -> 가장 작은 expire_at
  -> 가장 먼저 만료될 가능성이 있는 키
```

`peek()`은 루트만 확인하므로 O(1)이고, `push()`와 `pop()`은 힙 높이만큼 정리하므로 O(log n)이다. 따라서 모든 TTL 키를 매번 훑지 않고, 다음 만료 후보부터 확인할 수 있다.

### 만료 정리 흐름

모든 명령은 실행을 시작할 때 `_purge_expired()`를 호출한다.

```text
1. 최소 힙의 루트 티켓을 peek한다.
2. 힙이 비었거나 expire_at이 아직 미래면 종료한다.
3. expire_at이 현재 시각 이하이면 티켓을 pop한다.
4. 해시맵에서 그 key의 현재 CacheEntry를 찾는다.
5. 키가 이미 없으면 오래된 티켓이므로 무시한다.
6. ticket.version과 entry.ttl_version이 같고,
   entry.expire_at도 현재 시각 이하일 때만 실제 키를 삭제한다.
7. 다음 힙 루트도 만료됐는지 반복해서 확인한다.
```

이 구현은 별도 백그라운드 타이머가 아니라 **명령을 처리할 때** 만료된 키를 정리한다. 또한 `_live_entry(key)`가 특정 키를 조회할 때 만료 시각을 한 번 더 검사하므로, 만료된 키가 값으로 반환되거나 LRU의 MRU 위치로 이동하지 않는다.

### `version`을 함께 넣는 이유: lazy deletion

같은 키에 `EXPIRE`를 다시 설정하거나 `SET`으로 값을 덮어쓰면 이전 TTL 티켓은 힙 중간에 남아 있을 수 있다. 힙 중간의 특정 티켓을 즉시 찾아 제거하면 O(n)이 될 수 있으므로, 이 구현은 이전 티켓을 나중에 꺼낼 때만 검사한다.

```text
EXPIRE session 10  -> (10, "session", 1)
EXPIRE session 60  -> (60, "session", 2)

10초 시점:
첫 티켓의 version 1 != 현재 entry.ttl_version 2
-> 오래된 티켓이므로 키를 삭제하지 않고 무시한다.
```

이 방식 덕분에 힙은 가장 이른 후보를 빠르게 제공하고, 실제 삭제 여부는 최신 `CacheEntry` 상태가 결정한다.

---

## 4. 메모리 초과 시 eviction은 어떤 순서로 동작하는가?

### `used_memory`의 계산과 갱신

이 구현의 엔트리 메모리 크기는 키와 값의 UTF-8 바이트 길이 합이다.

```text
memory_size = len(key.encode("utf-8")) + len(value.encode("utf-8"))
```

즉, 현재 `used_memory`에는 문자열 키와 값의 바이트만 포함하며, `CacheEntry`, 해시맵 버킷, 연결 리스트 노드, TTL 힙 같은 자료구조 자체의 오버헤드는 포함하지 않는다.

| `SET` 상황 | `used_memory` 갱신 |
| --- | --- |
| 새 키 | 새 엔트리의 `memory_size`를 더한다. |
| 기존 키의 값 갱신 | 이전 `memory_size`를 빼고, 새 `memory_size`를 더한다. |
| `DEL`, TTL 만료, eviction | 삭제되는 엔트리의 `memory_size`를 뺀다. |

### 저장 뒤의 eviction 흐름

```text
SET key value
  -> key + value의 UTF-8 바이트 수를 계산한다.
  -> 새 키를 MRU에 추가하거나, 기존 키의 값을 갱신하고 MRU로 옮긴다.
  -> used_memory를 새 상태로 갱신한다.
  -> maxmemory > 0 이고 used_memory > maxmemory 이면 반복한다.
       1. tail.prev에서 LRU 노드를 찾는다.
       2. 그 노드의 CacheEntry와 key를 얻는다.
       3. 해시맵에서 키를 제거한다.
       4. LRU 리스트에서 노드를 제거한다.
       5. TTL 상태를 무효화한다.
       6. entry.memory_size만큼 used_memory를 줄인다.
       7. evicted_keys를 1 증가한다.
  -> used_memory <= maxmemory가 되면 종료한다.
```

여러 키를 제거해야 제한 아래로 내려갈 수 있으므로, `_evict_until_within_limit()`은 한 번이 아니라 `while`로 반복한다. `CONFIG SET maxmemory <값>`으로 이미 사용 중인 메모리보다 작은 제한을 설정한 경우에도 같은 eviction 흐름이 즉시 실행된다.

### OOM과 eviction의 구분

새로 넣으려는 **하나의 엔트리 자체가** `maxmemory`보다 크면, 다른 키를 모두 지워도 저장할 수 없다. 이 경우 구현은 기존 상태를 바꾸지 않고 OOM 오류를 반환한다.

```text
maxmemory > 0 and new_entry_memory_size > maxmemory
  -> (error) OOM command not allowed when used_memory > 'maxmemory'
```

반면 새 엔트리 자체는 들어갈 수 있지만 전체 합이 제한을 넘는 경우에는 LRU eviction을 수행한다. `evicted_keys`는 이 자동 축출에서만 증가하며, 사용자의 `DEL`이나 TTL 만료에 의한 삭제는 증가시키지 않는다.

### 간단한 예시

`maxmemory`가 8바이트이고, 각 키와 값의 바이트 수가 다음과 같다고 하자.

| 키 / 값 | 엔트리 바이트 |
| --- | ---: |
| `a` / `11` | 3 |
| `b` / `22` | 3 |
| `c` / `333` | 4 |

```text
SET a 11, SET b 22 뒤: used_memory = 6
GET a 뒤:               LRU 순서는 a(MRU) -> b(LRU)
SET c 333 뒤:           used_memory = 10, c(MRU) -> a -> b(LRU)
eviction 뒤:            b 제거, used_memory = 7, evicted_keys = 1
```

`GET a`가 `a`를 MRU로 옮겼기 때문에, 같은 상황에서 `b`가 정확히 제거된다.

---

## 5. `GET` 명령어는 어떤 순서로 동작하는가?

### 전체 흐름

`GET`은 단순히 해시맵에서 값만 꺼내지 않는다. 만료 여부와 LRU 순서를 함께 관리한다.

```text
GET key
  1. execute() 시작 시 _purge_expired()로, 힙에서 기한이 지난 TTL을 먼저 정리한다.
  2. 인자 수가 하나인지 확인한다.
  3. _live_entry(key)로 해시맵에서 엔트리를 찾는다.
  4. 엔트리가 없으면 (nil)을 반환한다.
  5. 엔트리가 있지만 expire_at <= 현재 시각이면 _delete_key(key)로 실제 삭제하고 (nil)을 반환한다.
  6. 살아 있는 엔트리면 _touch(entry)로 lru_node를 MRU 위치로 옮긴다.
  7. 값을 출력용으로 이스케이프해 큰따옴표로 감싸 반환한다.
```

소스 코드의 실제 실행 순서에서는 6단계의 LRU 갱신 뒤에 문자열을 만들어 반환한다. 의미상으로는 **성공한 조회의 결과를 반환하는 경로에서만 LRU를 갱신한다**고 이해하면 된다.

### 상태별 결과

| 키 상태 | TTL 처리 | 반환값 | LRU 갱신 |
| --- | --- | --- | --- |
| 키가 없음 | 삭제할 것이 없다. | `(nil)` | 하지 않는다. |
| 만료됨 | 해시맵·LRU·TTL·메모리 상태에서 삭제한다. | `(nil)` | 하지 않는다. |
| TTL이 없거나 아직 유효함 | 그대로 유지한다. | 저장된 값을 큰따옴표로 감싸 반환한다. | 해당 노드를 MRU로 이동한다. |

만료된 키를 먼저 삭제하고 `(nil)`로 처리하는 이유는, 이미 유효기간이 끝난 데이터가 반환되거나 “방금 사용했다”는 이유로 LRU 목록의 앞으로 이동하는 일을 막기 위해서다.

---

## 평가에서 확인할 핵심 표현

| 질문 | 핵심 답변 |
| --- | --- |
| 왜 LRU에 해시맵과 리스트가 둘 다 필요한가? | 해시맵은 키 조회, 이중 연결 리스트는 사용 순서와 O(1) 노드 이동·제거를 담당한다. 한 구조만으로는 두 일을 모두 빠르게 할 수 없다. |
| O(1) LRU의 핵심은 무엇인가? | 해시맵으로 `CacheEntry`를 찾고, 엔트리가 가진 `lru_node`를 리스트 맨 앞으로 옮기는 것이다. |
| TTL에 왜 최소 힙을 쓰는가? | 가장 이른 만료 시각을 `peek()`으로 O(1)에 확인해 모든 TTL 키를 매번 순회하지 않기 위해서다. |
| eviction 때 무엇이 바뀌는가? | LRU 키가 해시맵과 리스트에서 제거되고 TTL이 무효화되며, `used_memory`는 줄고 `evicted_keys`는 1 증가한다. |
| `GET`은 언제 LRU를 갱신하는가? | 키가 존재하고 만료되지 않아 값을 성공적으로 반환하는 경우에만 갱신한다. |

### 한 문장으로 정리

> Mini Redis는 해시맵으로 키를 찾고 이중 연결 리스트로 사용 순서를 관리해 LRU를 평균 O(1)에 갱신하며, 최소 힙으로 가장 빠른 TTL 만료를 확인하고, 메모리 제한을 넘으면 LRU 키를 제거해 사용량을 제한한다.
