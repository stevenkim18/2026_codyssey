# Mini Redis에서 3개 자료구조가 함께 동작하는 원리

## 1. 먼저 세 자료구조의 역할부터 정리

이번 Mini Redis에서는 크게 세 가지 자료구조를 사용한다.

```text
1. HashMap
2. Doubly Linked List
3. Min Heap
```

각각 담당하는 일이 다르다.

```text
HashMap
→ Key로 데이터를 빠르게 찾는다.

Doubly Linked List
→ 최근 사용 순서를 관리한다.

Min Heap
→ 가장 빨리 만료될 Key를 관리한다.
```

한눈에 보면:

```text
                   Mini Redis

                       │
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼

    HashMap       Doubly Linked      Min Heap
                     List

       │               │               │
       ▼               ▼               ▼

   Key 검색        LRU 순서        TTL 만료 순서
```

---

# 2. 같은 Key를 서로 다른 관점으로 관리한다

예를 들어 Redis에 다음 데이터가 있다고 하자.

```text
user:1 → Alice
user:2 → Bob
user:3 → Charlie
```

HashMap에서는:

```text
"user:1" → Alice
"user:2" → Bob
"user:3" → Charlie
```

형태로 바라본다.

하지만 LRU에서는 값 자체보다:

```text
누가 최근에 사용되었는가?
```

가 중요하다.

그래서:

```text
최근                              오래됨
 ↓                                   ↓

[user:3] ⇄ [user:1] ⇄ [user:2]
```

처럼 관리한다.

TTL에서는:

```text
누가 가장 빨리 만료되는가?
```

가 중요하다.

```text
(10:00:05, user:2)
(10:00:30, user:1)
(10:01:00, user:3)
```

같이 관리한다.

즉 같은 Redis Key라도 세 자료구조가 서로 다른 질문에 답한다.

---

# 3. HashMap이 답하는 질문

HashMap이 답하는 질문은:

> `"user:2"` 데이터가 어디 있지?

이다.

```text
"user:2"
    ↓
 Hash
    ↓
Bucket
    ↓
Entry
```

평균적으로:

```text
O(1)
```

에 찾을 수 있다.

---

# 4. Doubly Linked List가 답하는 질문

이중 연결 리스트가 답하는 질문은:

> 가장 최근에 사용된 Key는 무엇인가?

또는:

> 가장 오래 사용하지 않은 Key는 무엇인가?

이다.

예:

```text
head                              tail
 ↓                                  ↓

[user:3] ⇄ [user:1] ⇄ [user:2]

최근 사용                      가장 오래됨
```

메모리가 부족하면:

```text
tail
```

을 제거하면 된다.

즉 여기서는:

```text
user:2
```

가 LRU 대상이다.

---

# 5. Min Heap이 답하는 질문

Min Heap이 답하는 질문은:

> 가장 빨리 만료되는 Key는 무엇인가?

이다.

예:

```text
           (105, B)
           /      \
      (120, A)   (180, C)
```

가장 위:

```text
(105, B)
```

를 보면 B가 가장 먼저 만료된다는 것을 알 수 있다.

---

# 6. 하나의 Key를 실제로 어떻게 연결할까?

구현 방법은 여러 가지가 있지만 학습용으로 다음처럼 생각하면 이해하기 쉽다.

HashMap에 저장하는 Value를 단순 문자열 하나가 아니라:

```text
Entry
```

라는 객체로 만든다.

예:

```python
class RedisEntry:
    def __init__(self, value):
        self.value = value
        self.lru_node = None
        self.expire_at = None
```

그러면:

```text
HashMap

"user:1"
   ↓
┌─────────────────────┐
│ value = "Alice"     │
│ lru_node = Node(...)│
│ expire_at = 150     │
└─────────────────────┘
```

처럼 만들 수 있다.

이 방식의 장점은 특정 Key를 찾으면:

```text
Value
LRU Node
TTL 정보
```

를 같이 알 수 있다는 것이다.

---

# 7. 전체 구조

예를 들어 다음 상태라고 해보자.

```text
user:1 → Alice
user:2 → Bob
user:3 → Charlie
```

전체 내부 구조를 단순화하면:

```text
HashMap
─────────────────────────────

"user:1"
   ↓
[value=Alice, lru_node=●, expire_at=130]

"user:2"
   ↓
[value=Bob, lru_node=●, expire_at=None]

"user:3"
   ↓
[value=Charlie, lru_node=●, expire_at=160]
```

LRU 리스트:

```text
최근                              오래됨
 ↓                                   ↓

[user:3] ⇄ [user:1] ⇄ [user:2]
```

TTL Heap:

```text
       (130, user:1)
              \
             (160, user:3)
```

각 자료구조는 서로 다른 목적을 가진다.

---

# 8. 가장 중요한 점

세 자료구조에 똑같은 내용을 복사해 넣는 것이 아니다.

예를 들어:

```text
HashMap
→ 실제 데이터와 관련 정보

Linked List
→ 순서

Heap
→ 만료 시간 순서
```

만 관리한다.

즉:

```text
HashMap = 검색
List    = 사용 순서
Heap    = 만료 순서
```

라고 기억하면 된다.

---

# 9. SET은 어떻게 동작할까?

사용자가:

```text
SET user:1 Alice
```

를 실행했다고 하자.

단순하게 보면 저장만 하면 될 것 같지만 실제로는 여러 작업이 필요하다.

전체 흐름:

```text
SET user:1 Alice

        ↓

기존 Key 존재 확인

        ↓

HashMap에 저장

        ↓

LRU 등록 / 갱신

        ↓

기존 TTL 제거

        ↓

used_memory 갱신

        ↓

maxmemory 초과 확인

        ↓

필요하면 LRU Eviction

        ↓

OK
```

하나씩 보자.

---

# 10. SET - HashMap

먼저:

```text
user:1
```

이 이미 존재하는지 확인한다.

```python
entry = store.get("user:1")
```

없다면 새로운 Entry를 만든다.

```text
HashMap

"user:1"
   ↓
[value = Alice]
```

---

# 11. SET - LRU

새로운 데이터는 방금 사용된 데이터다.

따라서 LRU 리스트의 가장 앞으로 넣는다.

기존:

```text
최근                  오래됨

[B] ⇄ [A]
```

새로운 C:

```text
[C] ⇄ [B] ⇄ [A]
 ↑
head
```

즉:

```python
node = lru.insert_front("user:1")
```

같은 동작을 한다.

---

# 12. 기존 Key를 SET하면?

현재:

```text
최근                     오래됨

[C] ⇄ [B] ⇄ [A]
```

여기서:

```text
SET A hello
```

가 들어왔다.

A는 이미 존재한다.

Value를 변경한 후:

```text
A는 방금 사용됨
```

이므로:

```text
[A] ⇄ [C] ⇄ [B]
```

로 이동한다.

즉:

```python
lru.move_to_front(a_node)
```

를 호출한다.

---

# 13. SET - TTL

이번 과제에서는 기존 Key를 SET으로 덮어쓰면 TTL이 초기화된다.

예:

```text
A → hello
TTL → 10초
```

인데:

```text
SET A world
```

를 실행했다.

그러면:

```text
A → world
TTL → 없음
```

이 되어야 한다.

즉 Entry의:

```python
entry.expire_at = None
```

같은 처리가 필요하다.

Heap에 예전 TTL 기록이 남을 수도 있지만 나중에 Lazy Deletion으로 무시할 수 있다.

---

# 14. SET - 메모리

SET으로 데이터가 들어오면:

```text
used_memory
```

도 바뀐다.

예:

```text
A → hello
```

라면:

```text
len("A".encode("utf-8"))
+
len("hello".encode("utf-8"))
```

만큼 증가한다.

그리고:

```text
used_memory > maxmemory?
```

를 확인한다.

---

# 15. maxmemory를 초과하면?

현재:

```text
maxmemory = 20
used_memory = 25
```

라고 하자.

그러면 데이터를 제거해야 한다.

LRU 리스트:

```text
최근                     오래됨

[C] ⇄ [B] ⇄ [A]
                      ↑
                     tail
```

A를 제거한다.

```text
[C] ⇄ [B]
```

그 후:

```text
used_memory
```

를 다시 계산한다.

아직 초과했다면:

```text
B
```

도 제거한다.

즉:

```text
while used_memory > maxmemory:
    LRU 제거
```

한다.

---

# 16. Eviction에서는 어떤 구조를 수정할까?

A가 LRU로 제거된다면:

```text
HashMap에서 A 삭제

LRU List에서 A 삭제

TTL 정보도 무효화

used_memory 감소

evicted_keys 증가
```

가 함께 일어나야 한다.

즉 하나의 Key 삭제가 여러 자료구조에 영향을 준다.

---

# 17. GET은 어떻게 동작할까?

사용자가:

```text
GET user:1
```

을 실행했다.

전체 흐름:

```text
GET user:1

     ↓

HashMap에서 찾기

     ↓

없음?
 ├─ YES → (nil)
 └─ NO

     ↓

TTL 확인

     ↓

만료됨?
 ├─ YES → 삭제 → (nil)
 └─ NO

     ↓

LRU 최신 위치로 이동

     ↓

Value 반환
```

---

# 18. GET - HashMap

먼저:

```python
entry = store.get("user:1")
```

한다.

평균:

```text
O(1)
```

이다.

Key가 없으면 바로:

```text
(nil)
```

을 반환한다.

---

# 19. GET - TTL 확인

Entry가 있다면 TTL을 확인한다.

예:

```text
expire_at = 100
current_time = 120
```

라면:

```text
120 >= 100
```

이므로 이미 만료되었다.

따라서:

```text
데이터 삭제
→ (nil)
```

이다.

중요:

```text
LRU 갱신하지 않음
```

이다.

---

# 20. GET 성공 시 LRU 갱신

현재:

```text
최근                     오래됨

[C] ⇄ [B] ⇄ [A]
```

사용자가:

```text
GET A
```

를 했다.

A를 성공적으로 가져왔으므로:

```text
[A] ⇄ [C] ⇄ [B]
```

로 바꾼다.

왜 이게 O(1)일까?

HashMap의 Entry가:

```text
A의 LRU Node
```

를 가지고 있기 때문이다.

```text
HashMap
"A"
 ↓
Entry
 ↓
lru_node
 ↓
[A]
```

따라서 리스트 전체를 검색하지 않아도 된다.

---

# 21. GET 전체 시간복잡도

평균적으로 생각하면:

```text
HashMap 조회
O(1)

+

expire_at 확인
O(1)

+

move_to_front
O(1)
```

따라서:

```text
평균 O(1)
```

에 가깝게 처리할 수 있다.

이 조합이 중요한 이유다.

---

# 22. EXPIRE는 어떻게 동작할까?

사용자:

```text
EXPIRE user:1 30
```

현재 시간이:

```text
100
```

이라고 하자.

먼저 HashMap에서:

```text
user:1
```

을 찾는다.

없으면:

```text
(integer) 0
```

이다.

있다면:

```text
expire_at = 100 + 30
          = 130
```

을 만든다.

---

# 23. EXPIRE - HashMap

Entry에 실제 TTL 정보를 기록한다.

```text
"user:1"
    ↓
Entry

value = Alice
expire_at = 130
```

즉:

```python
entry.expire_at = 130
```

이다.

---

# 24. EXPIRE - Min Heap

그리고 Heap에:

```text
(130, "user:1")
```

을 넣는다.

```text
       (130, user:1)
```

다른 TTL이 있다면:

```text
       (110, B)
       /      \
(130, user:1) (160, C)
```

같이 된다.

이제 Heap의 맨 위를 보면 가장 빨리 만료될 Key를 알 수 있다.

---

# 25. EXPIRE를 다시 호출하면?

현재:

```text
EXPIRE A 10
```

으로:

```text
expire_at = 110
```

이 등록되어 있다고 하자.

Heap:

```text
(110, A)
```

그런데 다시:

```text
EXPIRE A 100
```

을 실행했다.

Entry는:

```text
A.expire_at = 200
```

으로 바뀐다.

Heap에는:

```text
(110, A)
(200, A)
```

둘 다 남을 수 있다.

---

# 26. 왜 괜찮은가?

나중에 `(110, A)`가 만료될 때 확인한다.

```text
Heap 정보:
A → 110

HashMap Entry:
A → 200
```

둘이 다르다.

따라서:

```text
110은 오래된 정보
```

라고 판단해서 무시한다.

이게:

```text
Lazy Deletion
```

이다.

---

# 27. Min Heap과 HashMap이 함께 필요한 이유

Heap만 보면:

```text
(110, A)
```

가 있다.

하지만 이것이 **현재도 유효한 TTL인지 알 수 없다.**

그래서 HashMap의 Entry를 확인한다.

```text
HashMap
A → expire_at 200
```

비교:

```text
Heap:    110
현재값:  200
```

다르므로:

```text
무효
```

이다.

즉:

```text
Heap
→ 어떤 TTL이 가장 빠른가?

HashMap
→ 그 TTL이 현재도 유효한가?
```

를 담당한다.

---

# 28. TTL 명령은 어떻게 동작할까?

```text
TTL A
```

가 들어왔다.

먼저 HashMap에서 A를 찾는다.

없으면:

```text
(integer) -2
```

이다.

A가 있는데:

```text
expire_at = None
```

이라면:

```text
(integer) -1
```

이다.

TTL이 있다면:

```text
expire_at - current_time
```

을 계산한다.

예:

```text
expire_at = 130
current = 120
```

이면:

```text
10초
```

이다.

---

# 29. DEL은 어떻게 동작할까?

사용자가:

```text
DEL A
```

를 실행한다.

HashMap으로 A를 찾는다.

없으면:

```text
(integer) 0
```

이다.

있다면 세 군데를 정리해야 한다.

```text
HashMap
→ Entry 삭제

Linked List
→ A Node 삭제

TTL
→ A의 TTL 무효화
```

그리고:

```text
used_memory
```

도 감소시킨다.

---

# 30. DEL에서 Heap은 어떻게 삭제할까?

A가 Heap의 중간에 있다고 하자.

```text
       (100, B)
       /      \
   (150, A)  (120, C)
```

A를 바로 찾으려면 Heap 전체를 검색해야 한다.

```text
O(N)
```

이 될 수 있다.

그래서 굳이 바로 삭제하지 않아도 된다.

대신 HashMap에서:

```text
A 자체를 삭제
```

한다.

나중에 `(150, A)`가 Heap top으로 올라오면:

```text
HashMap에 A가 있나?
```

확인한다.

없다면:

```text
오래된 TTL 정보
→ 그냥 Heap에서 버림
```

한다.

이것도 Lazy Deletion이다.

---

# 31. 만료된 Key를 정리하는 과정

현재 시간이:

```text
150
```

이고 Heap이:

```text
       (100, A)
       /      \
   (120, B)  (200, C)
```

라면 Heap top:

```text
(100, A)
```

는 이미 만료되었다.

그래서:

```text
peek()

↓

expire_at <= now ?

↓

YES

↓

pop()
```

한다.

그리고 A의 Entry를 확인한다.

현재 TTL도 정말 100이라면:

```text
A 삭제
```

한다.

다시 Heap top 확인:

```text
(120, B)
```

역시 만료되었다.

삭제.

다음:

```text
(200, C)
```

는 아직 만료되지 않았다.

여기서 멈춘다.

---

# 32. 의사 코드로 보면

대략 이런 느낌이다.

```python
def cleanup_expired():
    while heap.size() > 0:
        expire_at, key = heap.peek()

        if expire_at > now():
            break

        heap.pop()

        entry = store.get(key)

        if entry is None:
            continue

        if entry.expire_at != expire_at:
            continue

        delete_key(key)
```

이 코드가 매우 중요한 이유는:

```text
HashMap + Heap
```

이 서로 협력하는 모습을 잘 보여주기 때문이다.

---

# 33. LRU Eviction 전체 흐름

이번에는 메모리 제한을 보자.

현재:

```text
maxmemory = 20
```

LRU:

```text
최근                     오래됨

[C] ⇄ [B] ⇄ [A]
```

새로운 D를 저장해서:

```text
used_memory = 25
```

가 됐다.

그러면:

```text
tail
 ↓
A
```

를 제거한다.

---

# 34. LRU Eviction에서 HashMap이 필요한 이유

Linked List에서 A를 찾을 필요는 없다.

tail이 이미 A다.

```text
tail → A
```

A의 Key를 얻으면:

```text
"A"
```

를 HashMap에서 삭제한다.

```python
store.remove("A")
```

그리고:

```text
used_memory 감소
evicted_keys += 1
```

한다.

아직 메모리가 넘치면 다음 tail을 제거한다.

---

# 35. 즉 HashMap과 Linked List는 서로 연결되어 있다

검색 방향:

```text
Key
 ↓
HashMap
 ↓
Entry
 ↓
LRU Node
```

Eviction 방향:

```text
tail Node
 ↓
Key
 ↓
HashMap에서 삭제
```

양쪽 방향으로 연결이 가능하면 편하다.

그래서 LRU Node에도 Key를 저장할 수 있다.

```python
class LRUNode:
    def __init__(self, key):
        self.key = key
        self.prev = None
        self.next = None
```

---

# 36. 실제 예제로 세 자료구조를 따라가 보자

처음:

```text
HashMap: 비어 있음
LRU:     비어 있음
Heap:    비어 있음
```

---

# 37. 명령 1

```text
SET A apple
```

HashMap:

```text
A → apple
```

LRU:

```text
[A]
```

Heap:

```text
비어 있음
```

TTL이 없기 때문이다.

---

# 38. 명령 2

```text
SET B banana
```

HashMap:

```text
A → apple
B → banana
```

LRU:

```text
[B] ⇄ [A]
 ↑       ↑
최근    오래됨
```

Heap:

```text
비어 있음
```

---

# 39. 명령 3

```text
GET A
```

HashMap으로 A를 찾는다.

```text
A → apple
```

A 조회 성공.

따라서 LRU 갱신:

기존:

```text
[B] ⇄ [A]
```

변경:

```text
[A] ⇄ [B]
```

Heap은 바뀌지 않는다.

---

# 40. 명령 4

현재 시간이 100이라고 하자.

```text
EXPIRE A 30
```

HashMap Entry:

```text
A
value = apple
expire_at = 130
```

LRU:

```text
[A] ⇄ [B]
```

EXPIRE 자체가 이번 요구사항에서는 LRU 갱신 대상이라고 명시되어 있지 않으므로 그대로 둬도 된다.

Heap:

```text
(130, A)
```

---

# 41. 명령 5

```text
SET C cherry
```

HashMap:

```text
A → apple
B → banana
C → cherry
```

LRU:

```text
[C] ⇄ [A] ⇄ [B]
```

Heap:

```text
(130, A)
```

---

# 42. 명령 6

메모리가 부족해졌다.

가장 오래 사용하지 않은 것은:

```text
B
```

이다.

LRU:

```text
[C] ⇄ [A] ⇄ [B]
               ↑
             삭제
```

HashMap에서도:

```text
B 삭제
```

한다.

결과:

```text
HashMap

A → apple
C → cherry
```

LRU:

```text
[C] ⇄ [A]
```

Heap:

```text
(130, A)
```

`evicted_keys`는 1 증가한다.

---

# 43. 명령 7

현재 시간이 140이 됐다.

```text
GET A
```

HashMap에서 A를 찾는다.

A는 존재한다.

하지만:

```text
expire_at = 130
now = 140
```

이미 만료됐다.

따라서 A를 삭제한다.

HashMap:

```text
C → cherry
```

LRU:

```text
[C]
```

Heap의 `(130, A)`도 정리된다.

결과:

```text
(nil)
```

이다.

중요:

```text
A를 LRU 앞으로 이동시키지 않는다.
```

---

# 44. 각 자료구조는 혼자서는 부족하다

## HashMap만 사용한다면

```text
Key → Value
```

는 잘 찾는다.

하지만:

> 누가 가장 오래 사용되지 않았지?

를 빠르게 알 수 없다.

---

## Linked List만 사용한다면

최근 사용 순서는 잘 관리한다.

하지만:

```text
GET user:123
```

에서 `user:123` Node를 찾으려면:

```text
O(N)
```

검색이 필요하다.

---

## Heap만 사용한다면

가장 빠른 TTL은 잘 찾는다.

하지만:

> user:123의 현재 Value는?

을 빠르게 찾는 구조는 아니다.

---

# 45. 그래서 조합한다

```text
HashMap
+
Doubly Linked List
+
Min Heap
```

세 개를 사용한다.

각자가 자신이 잘하는 문제만 해결한다.

```text
HashMap
→ 검색

Linked List
→ 순서

Heap
→ 최소값
```

이게 자료구조를 공부할 때 가장 중요한 관점이다.

---

# 46. SET을 다시 한 번 정리

```text
SET key value

        ↓

[HashMap]
기존 Key 검색

        ↓

기존 Key라면
기존 메모리 사용량 제거

        ↓

Value 저장

        ↓

TTL 초기화

        ↓

[Linked List]
새 Key → insert_front
기존 Key → move_to_front

        ↓

used_memory 증가

        ↓

maxmemory 확인

        ↓

초과하면
tail부터 Eviction
```

---

# 47. GET 다시 정리

```text
GET key

    ↓

[HashMap]
Key 검색

    ↓

없음 → (nil)

    ↓

TTL 확인

    ↓

만료됨 → 전체 삭제 → (nil)

    ↓

[Linked List]
move_to_front

    ↓

Value 반환
```

---

# 48. EXPIRE 다시 정리

```text
EXPIRE key seconds

       ↓

[HashMap]
Key 검색

       ↓

없음 → 0

       ↓

expire_at 계산

       ↓

HashMap Entry에
expire_at 저장

       ↓

[Min Heap]
(expire_at, key)
push

       ↓

1 반환
```

---

# 49. DEL 다시 정리

```text
DEL key

    ↓

[HashMap]
Key 검색

    ↓

없음 → 0

    ↓

used_memory 감소

    ↓

[Doubly Linked List]
Node 제거

    ↓

HashMap Entry 삭제

    ↓

TTL 정보 무효화

    ↓

1 반환
```

Heap에 남은 오래된 정보는 Lazy Deletion으로 나중에 제거할 수 있다.

---

# 50. TTL 만료 정리

```text
Min Heap

peek
 ↓
가장 빠른 expire_at

 ↓

현재 시간보다 작거나 같음?

 ├─ NO
 │   └─ 종료
 │
 └─ YES
      ↓
     pop
      ↓
  HashMap 확인
      ↓
 Entry가 없음?
 → 오래된 정보, 무시

 expire_at이 다름?
 → 오래된 정보, 무시

 expire_at이 같음?
 → 실제 만료
      ↓
 HashMap / LRU에서 삭제
```

---

# 51. 세 자료구조의 시간복잡도 연결

GET 성공을 보자.

```text
HashMap get
평균 O(1)

+

Linked List move_to_front
O(1)
```

따라서 평균:

```text
O(1)
```

이다.

TTL 추가:

```text
Heap push
O(log N)
```

Eviction:

```text
Linked List remove_back
O(1)

+

HashMap remove
평균 O(1)
```

이런 식으로 각 기능의 성능을 계산할 수 있다.

---

# 52. 핵심 시간복잡도 표

| 기능 | 핵심 자료구조 | 일반적인 복잡도 |
|---|---|---:|
| Key 검색 | HashMap | 평균 O(1) |
| Key 저장 | HashMap | 평균 O(1) |
| LRU 갱신 | Doubly Linked List | O(1) |
| 가장 오래된 Key 찾기 | tail | O(1) |
| LRU 삭제 | Linked List + HashMap | 평균 O(1) |
| 가장 빠른 TTL 확인 | Min Heap | O(1) |
| TTL 추가 | Min Heap | O(log N) |
| TTL pop | Min Heap | O(log N) |

---

# 53. 이 과제의 중요한 설계 포인트

이 과제는 사실:

```text
자료구조 3개를 구현해라
```

가 핵심이 아니다.

더 중요한 것은:

```text
하나의 문제를
여러 자료구조의 장점을 조합해서
효율적으로 해결한다.
```

는 것이다.

예를 들어 LRU 하나만 보더라도:

```text
HashMap
→ Node를 찾는다.

Doubly Linked List
→ Node 순서를 바꾼다.
```

둘을 조합해야 한다.

TTL 역시:

```text
HashMap
→ Key의 현재 TTL을 확인한다.

Min Heap
→ 가장 빠른 TTL을 찾는다.
```

조합해서 해결한다.

---

# 54. 세 자료구조의 관계를 한 장으로 표현하면

```text
                        Key
                         │
                         ▼
                  ┌─────────────┐
                  │   HashMap   │
                  └──────┬──────┘
                         │
                         ▼
                    RedisEntry
               ┌─────────┼─────────┐
               │         │         │
               ▼         ▼         ▼
             Value   LRU Node   expire_at
                         │         │
                         ▼         ▼

                  Doubly Linked   Min Heap
                      List

                  최근 ⇄ 오래됨   최소 만료시간
```

---

# 55. 질문별로 어떤 자료구조를 볼까?

## "A라는 Key가 있나요?"

```text
HashMap
```

---

## "A의 Value가 무엇인가요?"

```text
HashMap
```

---

## "A를 방금 사용했어요."

```text
Doubly Linked List
```

에서 A를 앞으로 이동한다.

---

## "메모리가 부족해요. 뭘 지우죠?"

```text
Doubly Linked List의 tail
```

을 본다.

---

## "가장 빨리 만료되는 Key가 뭔가요?"

```text
Min Heap
```

을 본다.

---

## "이 Heap의 TTL 정보가 아직 유효한가요?"

```text
HashMap Entry의 expire_at
```

을 확인한다.

---

# 56. 발표할 때 이렇게 설명하면 된다

> Mini Redis에서는 HashMap, 이중 연결 리스트, 최소 힙 세 가지 자료구조를 서로 다른 목적으로 조합합니다.
>
> HashMap은 Key를 이용해 데이터를 평균 O(1)에 찾는 역할을 합니다.
>
> 이중 연결 리스트는 Key들의 최근 사용 순서를 관리합니다. 가장 최근 사용된 Key를 head에 두고 가장 오래 사용하지 않은 Key를 tail에 두기 때문에, GET이나 SET이 성공했을 때 해당 노드를 O(1)에 앞으로 이동시킬 수 있고 메모리가 부족할 때 tail을 O(1)에 제거할 수 있습니다.
>
> 최소 힙은 TTL 관리에 사용합니다. `(expire_at, key)`를 저장해서 가장 빠른 만료 시간을 O(1)에 확인하고, TTL 추가나 제거는 O(log N)에 처리합니다.
>
> 예를 들어 GET 명령이 들어오면 HashMap으로 Key를 찾고, TTL이 만료되지 않았는지 확인한 뒤, 성공한 경우 이중 연결 리스트의 해당 노드를 앞으로 이동시킵니다.
>
> EXPIRE 명령에서는 HashMap의 Entry에 실제 만료 시간을 기록하고 Min Heap에도 `(expire_at, key)`를 추가합니다.
>
> 결국 HashMap은 검색, Linked List는 사용 순서, Min Heap은 만료 순서를 담당한다고 정리할 수 있습니다.

---

# 57. 정말 핵심만 기억하면

```text
HashMap
"어디 있어?"

Doubly Linked List
"누가 가장 최근 / 오래됐어?"

Min Heap
"누가 가장 빨리 만료돼?"
```

이 세 문장으로 기억하면 된다.

그리고 Mini Redis는 이 세 질문을 조합해서:

```text
SET
GET
DEL
EXPIRE
TTL
LRU Eviction
```

을 구현하는 프로그램이다.

---

# 58. 한 문장으로 정리

> Mini Redis는 HashMap으로 Key를 빠르게 찾고, 이중 연결 리스트로 최근 사용 순서를 관리하며, 최소 힙으로 만료 시간 순서를 관리하고, 하나의 명령이 실행될 때 이 세 자료구조의 상태를 일관되게 함께 변경하는 방식으로 동작한다.