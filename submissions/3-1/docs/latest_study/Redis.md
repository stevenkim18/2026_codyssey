# Mini Redis 과제를 위한 Redis 핵심 개념 정리

# 1. Redis란?

Redis는 데이터를 메모리에 저장하는 **In-Memory Key-Value 데이터 저장소**다.

가장 단순하게 생각하면 다음과 같다.

```text
Key          Value

"name"   →   "Alice"
"age"    →   "20"
"city"   →   "Seoul"
```

사용자는 Key를 이용해 데이터를 저장하거나 조회한다.

예:

```text
SET name Alice
GET name
```

결과:

```text
"Alice"
```

즉 Redis의 가장 기본적인 사고방식은:

```text
Key → Value
```

이다.

이번 Mini Redis 과제도 바로 이 구조를 직접 구현하는 것이다.

---

# 2. Redis는 데이터베이스인가?

그렇다.

다만 MySQL이나 PostgreSQL 같은 관계형 데이터베이스와는 성격이 많이 다르다.

관계형 데이터베이스는 일반적으로:

```text
users 테이블

id | name   | age
---|--------|----
1  | Alice  | 20
2  | Bob    | 25
```

처럼 테이블과 행을 중심으로 데이터를 관리한다.

Redis는 기본적으로:

```text
user:1:name → Alice
user:2:name → Bob
```

처럼 Key를 이용한다.

그래서 Redis를 흔히:

```text
Key-Value Store
```

라고 부른다.

---

# 3. Redis가 빠른 가장 큰 이유: In-Memory

Redis의 중요한 특징 중 하나가:

```text
In-Memory
```

다.

즉 데이터를 주로 **RAM에 저장하고 처리한다.**

일반적인 저장장치는 크게:

```text
CPU
 ↓
RAM
 ↓
SSD / HDD
```

정도로 생각할 수 있다.

RAM은 SSD나 HDD보다 데이터 접근 속도가 매우 빠르다.

Redis는 데이터를 메모리에 올려놓고 처리하기 때문에 빠른 응답이 가능하다.

---

# 4. 그렇다고 "메모리를 써서만" 빠른 것은 아니다

Redis가 빠른 이유를:

> RAM을 쓰기 때문입니다.

라고만 설명하면 충분하지 않다.

Redis는 동시에 적절한 자료구조를 사용한다.

예를 들어 Key를 찾을 때:

```text
Key
 ↓
Hash Table
 ↓
Value
```

형태로 빠르게 접근할 수 있다.

이번 과제에서도:

```text
HashMap
Doubly Linked List
Min Heap
```

을 직접 구현하는 이유가 여기에 있다.

Mini Redis 관점에서는:

```text
HashMap
→ 데이터를 빠르게 찾는다.

Doubly Linked List
→ LRU 순서를 빠르게 관리한다.

Min Heap
→ TTL 만료 시간을 빠르게 관리한다.
```

라고 이해하면 된다.

---

# 5. Redis의 가장 기본적인 명령어 SET과 GET

Redis의 가장 기본적인 명령은:

```text
SET
GET
```

이다.

## SET

```text
SET name Alice
```

의 의미:

```text
"name"이라는 Key에
"Alice"라는 Value를 저장한다.
```

내부적으로 단순화하면:

```text
HashMap.put("name", "Alice")
```

와 비슷하게 생각할 수 있다.

---

## GET

```text
GET name
```

의 의미:

```text
"name"이라는 Key의 Value를 가져온다.
```

내부적으로:

```text
HashMap.get("name")
```

와 비슷하다.

결과:

```text
"Alice"
```

Key가 없다면:

```text
(nil)
```

을 반환한다.

---

# 6. Key란 무엇인가?

Redis에서는 모든 데이터를 Key를 이용해서 찾는다.

예:

```text
"user:1"
"user:2"
"session:abc123"
"product:100"
```

실제 서비스에서는 `:`을 이용해서 Key를 구분하는 경우가 많다.

예:

```text
user:1:name
user:1:email
user:2:name
```

`:` 자체가 특별한 문법은 아니다.

사람이 Key를 보기 좋게 정리하기 위한 관습이라고 생각하면 된다.

---

# 7. Value란 무엇인가?

이번 과제에서는 Redis의 여러 데이터 타입 중:

```text
String
```

만 구현한다.

예:

```text
SET name Alice
SET age 30
SET message "Hello World"
```

이번 Mini Redis에서는 사실상:

```text
Key → String Value
```

만 지원한다.

---

# 8. 실제 Redis에는 여러 자료형이 있다

실제 Redis는 String만 지원하는 것이 아니다.

대표적으로:

```text
String
List
Set
Hash
Sorted Set
Stream
```

등이 있다.

예를 들어:

```text
String
name → Alice
```

```text
List
queue → [A, B, C]
```

```text
Set
tags → {python, redis, database}
```

같은 구조를 지원한다.

하지만 이번 과제에서는:

```text
String만 구현
```

하면 된다.

따라서 Redis 전체를 구현하는 것이 아니라 **Redis의 핵심 원리를 작게 재현하는 것**이다.

---

# 9. DEL

Redis에서는 Key를 삭제할 수 있다.

```text
DEL name
```

성공하면:

```text
(integer) 1
```

Key가 존재하지 않으면:

```text
(integer) 0
```

을 반환한다.

이번 과제에서는 DEL을 단순히 HashMap에서만 삭제하면 안 된다.

왜냐하면 같은 Key 정보가 여러 구조에 들어 있기 때문이다.

```text
HashMap
LRU Linked List
TTL 구조
```

따라서 Key를 삭제한다는 것은:

```text
데이터 삭제
+
LRU 정보 삭제
+
TTL 정보 삭제
```

를 의미한다.

---

# 10. EXISTS

특정 Key가 존재하는지 확인한다.

```text
EXISTS name
```

존재하면:

```text
(integer) 1
```

없으면:

```text
(integer) 0
```

이다.

내부적으로는:

```text
HashMap.contains("name")
```

과 비슷하게 생각할 수 있다.

---

# 11. DBSIZE

현재 Redis에 저장된 Key 개수를 반환한다.

예:

```text
SET a 1
SET b 2
SET c 3
```

그 후:

```text
DBSIZE
```

결과:

```text
(integer) 3
```

이번 구현에서는 HashMap의:

```python
size()
```

와 연결할 수 있다.

---

# 12. KEYS

현재 저장된 Key들을 확인한다.

예:

```text
KEYS
```

결과:

```text
1. "user:1"
2. "user:2"
3. "name"
```

이번 과제에서는 패턴 검색까지 구현하지 않는다.

실제 Redis의 `KEYS`는 패턴을 사용할 수 있지만 이번에는:

```text
모든 Key 반환
```

정도로만 구현한다.

---

# 13. Redis와 메모리

Redis는 데이터를 메모리에 저장하기 때문에 중요한 문제가 하나 있다.

메모리는 무한하지 않다.

예를 들어 Redis가 사용할 수 있는 메모리가:

```text
100MB
```

라고 하자.

계속 데이터를 저장하면:

```text
20MB
50MB
80MB
100MB
120MB
```

언젠가는 제한을 넘을 수 있다.

그래서 Redis에서는:

```text
maxmemory
```

라는 개념이 중요하다.

---

# 14. maxmemory

`maxmemory`는 Redis가 사용할 수 있는 최대 메모리 양이다.

이번 과제에서는:

```text
CONFIG SET maxmemory 100
```

처럼 설정한다.

의미:

```text
최대 100바이트까지만 저장하겠다.
```

이번 과제에서는:

```text
maxmemory = 0
```

이면:

```text
메모리 제한 없음
```

으로 취급한다.

---

# 15. used_memory

현재 Redis가 얼마나 많은 메모리를 사용하고 있는지를 나타낸다.

이번 과제에서는 실제 Python 객체의 메모리 크기를 계산하지 않는다.

공식이 주어져 있다.

```text
used_memory
=
모든 Key와 Value의 UTF-8 바이트 길이의 합
```

예:

```text
name → Alice
```

영문 ASCII 문자는 UTF-8에서 일반적으로 한 글자당 1바이트다.

```text
"name" = 4 bytes
"Alice" = 5 bytes
```

따라서:

```text
4 + 5 = 9 bytes
```

이다.

---

# 16. 왜 len(string)이 아니라 UTF-8 바이트 길이인가?

영어만 있다면:

```python
len("Alice")
```

와 바이트 수가 같을 수 있다.

하지만 한글은 다르다.

예:

```text
"가"
```

Python 문자열 길이는:

```python
len("가")
```

결과:

```text
1
```

이지만 UTF-8에서는 3바이트를 사용한다.

그래서 이번 과제에서는:

```python
len(text.encode("utf-8"))
```

형태로 계산하는 것이 정확하다.

예:

```python
len("안녕".encode("utf-8"))
```

결과:

```text
6
```

이다.

---

# 17. INFO memory

현재 메모리 상태를 확인하는 명령이다.

예:

```text
INFO memory
```

결과:

```text
used_memory:22
maxmemory:30
evicted_keys:1
```

각 의미는:

```text
used_memory
→ 현재 데이터가 사용하는 메모리

maxmemory
→ 설정된 최대 메모리

evicted_keys
→ 메모리가 부족해서 자동으로 제거된 Key 개수
```

이다.

---

# 18. Eviction이란?

Eviction은:

```text
메모리가 부족할 때 기존 데이터를 자동으로 제거하는 것
```

이다.

예:

```text
maxmemory = 30
```

인데 새로운 데이터를 저장한 뒤:

```text
used_memory = 38
```

이 됐다.

그러면 일부 데이터를 제거해야 한다.

어떤 데이터를 제거할 것인가?

이번 과제에서는:

```text
LRU
```

정책을 사용한다.

---

# 19. LRU란?

LRU는:

```text
Least Recently Used
```

의 약자다.

뜻은:

```text
가장 오랫동안 사용하지 않은 데이터
```

이다.

예:

```text
최근 사용                     오래됨
   ↓                            ↓

C → B → A
```

라면 A가 가장 오래 사용되지 않았다.

메모리가 부족하면:

```text
A 삭제
```

한다.

---

# 20. 왜 LRU를 사용할까?

캐시에는 이런 특징이 있다.

최근에 사용한 데이터는 다시 사용할 가능성이 높고,

오랫동안 사용하지 않은 데이터는 앞으로도 사용될 가능성이 상대적으로 낮다고 가정한다.

따라서:

```text
최근 데이터 유지
오래된 데이터 제거
```

라는 전략을 사용할 수 있다.

이것이 LRU의 기본 아이디어다.

---

# 21. LRU와 GET

중요한 점은 GET도 LRU 순서를 변경한다는 것이다.

현재:

```text
최근                         오래됨

C ⇄ B ⇄ A
```

사용자가:

```text
GET A
```

를 실행한다.

A는 방금 사용된 데이터가 된다.

따라서:

```text
A ⇄ C ⇄ B
```

로 변경된다.

즉 GET은 단순한 조회만 하는 것이 아니다.

이번 과제에서는:

```text
GET 성공
→ LRU 갱신
```

도 수행해야 한다.

---

# 22. SET과 LRU

SET도 해당 Key를 최근 사용된 데이터로 만든다.

예:

```text
SET user:1 Alice
```

하면:

```text
user:1
```

이 LRU 리스트 맨 앞에 들어간다고 생각할 수 있다.

기존 Key를 덮어쓰는 경우에도 최근 사용된 데이터가 된다.

---

# 23. HashMap + Doubly Linked List를 사용하는 이유

LRU를 구현하려면 두 가지 문제를 해결해야 한다.

### 문제 1

특정 Key를 빠르게 찾아야 한다.

```text
GET user:100
```

→ HashMap

평균:

```text
O(1)
```

---

### 문제 2

찾은 데이터를 최근 위치로 빠르게 이동해야 한다.

```text
[user:3] ⇄ [user:2] ⇄ [user:100]
```

를:

```text
[user:100] ⇄ [user:3] ⇄ [user:2]
```

로 변경해야 한다.

→ Doubly Linked List

```text
O(1)
```

따라서:

```text
HashMap
+
Doubly Linked List
```

조합이 LRU에 잘 맞는다.

---

# 24. Eviction 흐름

이번 과제에서 `SET`을 실행했다고 하자.

```text
SET A 12345
```

전체 흐름은 대략 다음과 같다.

```text
SET 실행

↓ 데이터 저장

used_memory 증가

↓

maxmemory 초과?

        아니오
          ↓
          OK

        예
          ↓
      LRU Key 찾기
          ↓
        삭제
          ↓
 used_memory 감소
          ↓
아직 maxmemory 초과?
          ↓
      반복
```

즉:

```text
used_memory <= maxmemory
```

가 될 때까지 LRU Key를 계속 제거한다.

---

# 25. evicted_keys

메모리 부족 때문에 자동으로 삭제된 Key 수를 기록한다.

예:

```text
A
B
C
```

세 개가 있었다.

새로운 데이터를 저장하면서 A와 B가 LRU 정책으로 제거되었다.

그러면:

```text
evicted_keys += 2
```

가 된다.

중요한 점:

사용자가 직접:

```text
DEL A
```

한 것은 eviction이 아니다.

따라서 `evicted_keys`를 증가시키지 않는다.

---

# 26. OOM

OOM은:

```text
Out Of Memory
```

의 약자다.

이번 과제에서는 하나의 Key-Value 자체가 `maxmemory`보다 큰 경우 저장할 수 없다.

예:

```text
maxmemory = 10
```

인데:

```text
"username" + "Alexander"
```

가 10바이트를 넘는다고 하자.

기존 데이터를 모두 삭제하더라도 이 데이터 하나 자체가 들어가지 않는다.

따라서:

```text
(error) OOM command not allowed ...
```

형태의 에러를 반환한다.

---

# 27. TTL이란?

TTL은:

```text
Time To Live
```

의 약자다.

뜻은:

```text
이 데이터가 앞으로 얼마나 더 살아 있을 것인가
```

이다.

Redis에서는 Key에 유효기간을 설정할 수 있다.

예:

```text
SET verification_code 123456
EXPIRE verification_code 60
```

의 의미:

```text
verification_code를 60초 뒤에 만료시킨다.
```

이다.

---

# 28. TTL은 어디에 사용할까?

대표적인 예가:

### 인증번호

```text
SMS 인증번호
→ 3분 후 만료
```

### 로그인 세션

```text
session
→ 일정 시간 후 만료
```

### Cache

```text
API 결과
→ 5분 동안만 사용
```

### 임시 데이터

```text
password-reset-token
→ 30분 후 삭제
```

등이다.

---

# 29. EXPIRE

Key에 만료 시간을 지정한다.

예:

```text
EXPIRE name 10
```

의 의미:

```text
name Key를 10초 후 만료시킨다.
```

성공:

```text
(integer) 1
```

Key가 없으면:

```text
(integer) 0
```

이다.

---

# 30. 실제로는 "10초"를 어떻게 저장할까?

단순히:

```text
10
```

만 저장하면 시간이 지나면서 계속 값을 줄여야 한다.

그보다는:

```text
expire_at
```

이라는 절대 시간을 저장하는 것이 편하다.

예:

현재 시간이:

```text
1000초
```

라고 하자.

```text
EXPIRE A 10
```

이라면:

```text
expire_at = 1000 + 10
          = 1010
```

을 저장한다.

그리고 나중에 현재 시간이:

```text
1007
```

이면:

```text
1010 - 1007
= 3초
```

남았다고 계산한다.

---

# 31. TTL 명령

```text
TTL key
```

는 남은 시간을 반환한다.

예:

```text
TTL session
```

결과:

```text
(integer) 35
```

이면 약 35초 남았다는 뜻이다.

---

# 32. TTL의 특별한 반환 값

Redis 스타일에서는 특별한 값을 사용한다.

## -2

```text
(integer) -2
```

Key 자체가 없다.

---

## -1

```text
(integer) -1
```

Key는 있지만 만료 시간이 없다.

---

## 0 이상

```text
(integer) 10
```

약 10초 남았다.

따라서:

```text
-2 → Key 없음

-1 → Key 있음, TTL 없음

0 이상 → TTL 존재
```

라고 기억하면 된다.

---

# 33. 만료된 Key는 언제 삭제할까?

이것이 재미있는 부분이다.

모든 Key에 대해:

```text
매 순간
"얘 만료됐나?"
```

확인하는 것은 비효율적이다.

그래서 이번 과제에서는:

```text
Key를 조회할 때 만료 여부 확인
```

하는 방식을 사용한다.

예:

```text
GET A
```

가 들어왔는데 A의 만료 시간이 이미 지났다.

그러면:

```text
A 삭제
→ (nil)
```

로 처리한다.

이것을 넓은 의미로:

```text
Lazy Expiration
```

방식이라고 이해할 수 있다.

즉:

> 필요할 때 확인하고 정리한다.

---

# 34. 만료된 Key와 LRU

중요한 엣지 케이스다.

현재:

```text
A가 TTL 만료됨
```

그런데:

```text
GET A
```

가 들어왔다.

처리:

```text
1. TTL 확인
2. 이미 만료됨
3. A 삭제
4. (nil) 반환
```

여기서 A는 성공적으로 조회된 것이 아니다.

따라서:

```text
LRU 갱신 X
```

이다.

---

# 35. 왜 TTL 관리에 Min Heap을 사용할까?

여러 Key가 있다고 하자.

```text
A → 15:00:20
B → 15:00:05
C → 15:00:30
D → 15:00:10
```

우리가 알고 싶은 것은:

> 가장 먼저 만료되는 Key가 무엇인가?

이다.

여기서는:

```text
B → 15:00:05
```

다.

Min Heap은 가장 작은 값을 빠르게 확인하기 좋다.

그래서:

```text
(expire_at, key)
```

형태로 Heap에 넣는다.

예:

```text
(1005, "B")
(1010, "D")
(1020, "A")
(1030, "C")
```

Heap의 맨 위에는 가장 빠른 만료 시간이 온다.

---

# 36. Min Heap과 TTL

구조를 단순화하면:

```text
       (1005, B)
       /       \
 (1010, D)   (1020, A)
 /
(1030, C)
```

`peek()`을 하면:

```text
(1005, B)
```

를 바로 볼 수 있다.

즉:

```text
가장 빨리 만료될 Key
```

를 빠르게 찾을 수 있다.

---

# 37. TTL의 Lazy Deletion

TTL 구현에서 또 하나 알아두면 좋은 개념이:

```text
Lazy Deletion
```

이다.

예를 들어:

```text
EXPIRE A 10
```

을 설정했다.

Heap:

```text
(1010, A)
```

그런데 잠시 뒤 다시:

```text
EXPIRE A 100
```

을 설정한다.

새로운 만료 시간:

```text
1100
```

Heap에:

```text
(1010, A)
(1100, A)
```

두 개가 존재할 수도 있다.

오래된:

```text
(1010, A)
```

를 Heap 중간에서 직접 찾아서 삭제하는 것은 복잡하다.

따라서 그냥 두고,

나중에 `(1010, A)`가 Heap 맨 위로 올라왔을 때:

```text
현재 A의 실제 expire_at이 1010인가?
```

확인한다.

아니라면:

```text
오래된 정보이므로 무시
```

한다.

이런 전략이 Lazy Deletion이다.

이번 과제에서도 선택할 수 있는 좋은 구현 방법이다.

---

# 38. SET을 하면 기존 TTL이 사라진다

이번 과제에서 중요한 규칙이다.

현재:

```text
SET A hello
EXPIRE A 10
```

A는 10초 뒤 만료된다.

그런데:

```text
SET A world
```

를 다시 실행했다.

그러면 기존 TTL을 초기화한다.

즉:

```text
A → world
TTL 없음
```

이 된다.

따라서:

```text
TTL A
```

결과는:

```text
(integer) -1
```

이어야 한다.

---

# 39. EXPIRE 0 또는 음수

예:

```text
EXPIRE A 0
```

또는:

```text
EXPIRE A -10
```

이번 과제에서는:

```text
즉시 만료
```

로 처리할 수 있다.

즉 A가 존재한다면 바로 삭제한다.

결과:

```text
(integer) 1
```

그리고 이후:

```text
GET A
```

결과:

```text
(nil)
```

이다.

---

# 40. TTL과 DEL

Key를 DEL하면:

```text
데이터만 제거
```

하는 것이 아니다.

TTL 관리 정보도 함께 제거되어야 한다.

개념적으로:

```text
DEL A

↓

HashMap에서 A 제거

LRU List에서 A 제거

TTL 관리에서도 A 제거
```

가 필요하다.

---

# 41. Redis에서 "만료"와 "Eviction"은 다르다

매우 중요한 구분이다.

## Expiration

TTL 시간이 끝나서 데이터가 삭제됨.

```text
EXPIRE A 10
→ 10초 뒤 삭제
```

---

## Eviction

메모리가 부족해서 정책에 의해 삭제됨.

```text
maxmemory 초과
→ LRU 데이터 삭제
```

둘 다 결과적으로 Key가 없어지지만 **삭제 이유가 다르다.**

---

# 42. DEL / Expiration / Eviction 비교

| 상황 | 삭제 이유 |
|---|---|
| DEL | 사용자가 직접 삭제 |
| Expiration | TTL 만료 |
| Eviction | 메모리 부족 |
| SET overwrite | 기존 Value 교체 |

특히:

```text
evicted_keys
```

는 Eviction으로 삭제된 경우만 증가시킨다.

---

# 43. Redis CLI란?

CLI는:

```text
Command Line Interface
```

의 약자다.

터미널에서 명령어를 입력해서 Redis와 상호작용하는 방식이다.

예:

```text
mini-redis> SET name Alice
OK

mini-redis> GET name
"Alice"

mini-redis> DEL name
(integer) 1
```

이번 과제에서는 실제 Redis 서버를 만드는 것이 아니라:

```text
터미널
↓
명령어 입력
↓
Python 프로그램
↓
결과 출력
```

구조만 만든다.

---

# 44. REPL이란?

이번 CLI는 REPL 형태로 동작한다.

REPL:

```text
Read
Eval
Print
Loop
```

각 의미:

```text
Read
→ 사용자 입력 읽기

Eval
→ 명령 실행

Print
→ 결과 출력

Loop
→ 다시 입력 받기
```

예:

```text
mini-redis> GET name
```

프로그램:

```text
Read
"GET name"

Eval
GET 실행

Print
"Alice"

Loop
다시 mini-redis> 출력
```

이 과정을 반복한다.

---

# 45. 명령어 파싱

사용자 입력:

```text
SET name Alice
```

를 프로그램은 다음과 같이 해석해야 한다.

```text
command = SET
key = name
value = Alice
```

개념적으로:

```python
["SET", "name", "Alice"]
```

형태로 나눌 수 있다.

그 후:

```text
SET이면 set 함수 실행
GET이면 get 함수 실행
DEL이면 delete 함수 실행
```

하는 것이다.

---

# 46. 따옴표가 왜 문제일까?

다음 입력은 간단하다.

```text
SET name Alice
```

공백으로 나누면:

```text
SET
name
Alice
```

가 된다.

하지만:

```text
SET message "Hello World"
```

를 단순하게 공백으로 나누면:

```text
SET
message
"Hello
World"
```

가 되어버린다.

그래서 따옴표 입력을 지원하려면:

```text
"Hello World"
```

를 하나의 값으로 인식해야 한다.

Python에서는 `shlex` 같은 파싱 방법을 사용할 수도 있지만, 과제의 라이브러리 제한 범위를 확인하고 사용하는 것이 좋다.

---

# 47. Redis 스타일 응답

이번 과제에서는 출력도 Redis 느낌으로 만든다.

성공:

```text
OK
```

값 없음:

```text
(nil)
```

숫자:

```text
(integer) 1
```

에러:

```text
(error) ERR ...
```

이런 형식을 통해 CLI 사용자가 결과 유형을 쉽게 알 수 있다.

---

# 48. 잘못된 명령

사용자가:

```text
HELLO
```

처럼 지원하지 않는 명령을 입력한다.

그러면:

```text
(error) ERR unknown command 'HELLO'
```

처럼 출력한다.

즉 프로그램은:

```text
지원하는 명령인지 확인
```

해야 한다.

---

# 49. 인자 개수 오류

사용자가:

```text
GET
```

만 입력했다.

GET에는 Key가 필요하다.

정상:

```text
GET name
```

따라서:

```text
(error) ERR wrong number of arguments for 'GET' command
```

를 반환해야 한다.

---

# 50. 정수 파싱 오류

예:

```text
CONFIG SET maxmemory abc
```

`maxmemory`에는 정수가 와야 한다.

따라서:

```text
(error) ERR value is not an integer or out of range
```

을 반환한다.

비슷하게:

```text
EXPIRE key abc
```

도 에러다.

---

# 51. Redis에서 캐시란?

이 과제를 이해하려면 Redis가 왜 캐시에 많이 쓰이는지도 알아두면 좋다.

예를 들어 웹 서버가 데이터베이스에서 사용자 정보를 가져오는 데:

```text
100ms
```

가 걸린다고 하자.

매 요청마다 DB를 조회하면 비효율적일 수 있다.

그래서:

```text
요청
 ↓
Redis 확인
 ↓
있음 → 바로 반환

없음
 ↓
DB 조회
 ↓
Redis 저장
 ↓
반환
```

하는 방식을 사용할 수 있다.

이런 Redis의 용도가:

```text
Cache
```

다.

---

# 52. 캐시와 TTL

캐시 데이터는 영원히 유지하면 문제가 생길 수 있다.

DB에서는:

```text
name = Steven
```

으로 변경됐는데 Redis에는:

```text
name = Alice
```

가 남아있을 수 있다.

그래서:

```text
SET cache:user:1 Alice
EXPIRE cache:user:1 300
```

처럼 5분 뒤 자동 삭제하도록 만들 수 있다.

이것이 TTL과 Cache가 자주 함께 등장하는 이유다.

---

# 53. 캐시와 LRU

캐시에는 수많은 데이터가 들어올 수 있다.

하지만 메모리는 제한되어 있다.

따라서:

```text
최근에 사용되는 데이터는 남기고
오랫동안 사용되지 않은 데이터는 제거
```

할 필요가 있다.

여기서 LRU가 등장한다.

즉:

```text
Cache
    ↓
Memory 제한
    ↓
Eviction 필요
    ↓
LRU
```

라는 관계가 있다.

---

# 54. Mini Redis 전체 구조

이번 과제를 구조적으로 보면 다음과 같다.

```text
                    사용자

                      │
                      ▼

                  CLI / REPL

                      │
                      ▼

                  MiniRedis

          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼

       HashMap       LRU         TTL

          │           │           │
          ▼           ▼           ▼

       Key/Value   Doubly       Min Heap
                  Linked List
```

---

# 55. HashMap의 역할

```text
SET
GET
DEL
EXISTS
DBSIZE
KEYS
```

의 기반이다.

주요 역할:

```text
Key → Value 빠른 검색
```

---

# 56. Doubly Linked List의 역할

```text
최근 사용 순서
```

를 기록한다.

예:

```text
가장 최근                   가장 오래됨

C ⇄ A ⇄ B
```

메모리가 부족하면:

```text
tail의 B 제거
```

한다.

---

# 57. Min Heap의 역할

TTL을 관리한다.

예:

```text
(1005, A)
(1010, B)
(1030, C)
```

중 가장 먼저 만료되는:

```text
(1005, A)
```

를 빠르게 찾는다.

---

# 58. SET 하나에도 여러 일이 일어난다

겉으로는:

```text
SET name Alice
```

한 줄이다.

하지만 내부적으로는 여러 작업이 필요하다.

```text
SET name Alice

      ↓

기존 Key 존재 확인

      ↓

기존 TTL 제거

      ↓

used_memory 계산

      ↓

HashMap에 저장

      ↓

LRU 최근 위치로 이동

      ↓

maxmemory 확인

      ↓

필요하면 LRU eviction

      ↓

OK
```

이런 관점으로 보면 이번 과제가 왜 여러 자료구조를 요구하는지 이해하기 쉽다.

---

# 59. GET 하나에도 여러 일이 일어난다

```text
GET name
```

도 단순하지 않다.

```text
GET name

   ↓

Key 존재?

   ↓

TTL 확인

   ↓

만료됨?
 ├─ YES → 삭제 → (nil)
 │
 └─ NO
      ↓
    Value 조회
      ↓
   LRU 갱신
      ↓
   "Alice"
```

이다.

---

# 60. DEL 하나에도 여러 일이 일어난다

```text
DEL name

   ↓

Key 존재 확인

   ↓

HashMap 삭제

   ↓

used_memory 감소

   ↓

LRU 삭제

   ↓

TTL 삭제

   ↓

(integer) 1
```

이다.

이처럼 Redis 명령 하나가 여러 자료구조의 상태를 동시에 변경할 수 있다.

---

# 61. 이 과제에서 중요한 "상태의 일관성"

매우 중요한 개념이다.

예를 들어 HashMap에서는 A를 삭제했는데:

```text
LRU 리스트에는 A가 남아 있음
```

이면 문제가 생긴다.

또는:

```text
HashMap에는 A가 없는데
TTL Heap에는 A가 존재
```

할 수도 있다.

따라서 Redis 내부에서는 여러 자료구조의 상태가 서로 맞아야 한다.

이를 일반적으로:

```text
Consistency
```

즉 일관성이라고 이해할 수 있다.

---

# 62. Mini Redis와 실제 Redis의 차이

이번 프로젝트를 하면서 중요한 점은:

> 내가 실제 Redis를 완전히 구현하고 있는 것은 아니다.

라는 것이다.

이번 Mini Redis는 학습을 위한 단순화 버전이다.

구현하는 것:

```text
String
SET / GET / DEL
EXISTS
DBSIZE
KEYS

maxmemory
LRU

EXPIRE
TTL

CLI
```

구현하지 않는 것:

```text
네트워크 서버
TCP
Redis protocol 전체
Persistence
Replication
Cluster
Transactions
Lua
Pub/Sub 기본 과제
List
Set
Hash
Sorted Set
Stream
동시성
```

이다.

---

# 63. Persistence란?

이번 과제에서는 구현하지 않지만 알아두면 좋다.

Redis가 메모리만 사용한다면 프로그램이 종료되었을 때 데이터가 사라질 수 있다.

실제 Redis는 필요에 따라 디스크에 데이터를 저장하는 기능도 제공한다.

이것을:

```text
Persistence
```

라고 한다.

대표적인 방식으로 Redis에는:

```text
RDB
AOF
```

같은 영속화 개념이 있다.

하지만 이번 Mini Redis에서는:

```text
프로그램 종료
→ 데이터 전부 사라짐
```

이어도 정상이다.

---

# 64. Redis를 캐시라고만 생각하면 안 된다

Redis는 캐시로 매우 많이 사용되지만 캐시만을 위한 프로그램은 아니다.

대표적으로:

```text
Cache
Session Store
Rate Limiting
Message Broker
Leaderboard
Queue
Pub/Sub
```

등에도 활용된다.

하지만 이번 과제에서 집중하는 것은:

```text
In-Memory Key-Value Store
+
TTL
+
Memory Eviction
```

이다.

---

# 65. 중요한 용어 관계 정리

```text
Redis
│
├─ In-Memory
│    └─ RAM에 데이터 저장
│
├─ Key-Value
│    └─ Key로 Value 검색
│
├─ Hash Table
│    └─ Key 빠른 조회
│
├─ TTL
│    └─ 일정 시간 후 만료
│
├─ maxmemory
│    └─ 메모리 제한
│
├─ Eviction
│    └─ 메모리 부족 시 데이터 제거
│
└─ LRU
     └─ 오래 사용하지 않은 데이터 우선 제거
```

---

# 66. 가장 많이 헷갈리는 개념

## TTL과 LRU

완전히 다른 개념이다.

```text
TTL
→ 시간이 지나서 삭제
```

```text
LRU
→ 메모리가 부족해서 삭제
```

---

## Expiration과 Eviction

```text
Expiration
→ TTL에 의한 만료
```

```text
Eviction
→ 메모리 정책에 의한 강제 제거
```

---

## RAM과 HashMap

```text
RAM
→ 데이터를 어디에 저장하는가
```

```text
HashMap
→ 데이터를 어떤 구조로 찾는가
```

Redis가 빠른 이유를 설명하려면 둘을 구분해야 한다.

---

# 67. Redis가 왜 빠른가?

이 과제를 끝내고 다음 질문에 답할 수 있어야 한다.

> Redis는 왜 빠른가요?

이번 프로젝트 수준에서는 다음처럼 설명할 수 있다.

> Redis는 데이터를 주로 메모리에 저장하기 때문에 디스크 기반 접근보다 빠르게 데이터를 읽고 쓸 수 있습니다.
>
> 또한 Key 기반 조회에 적합한 효율적인 자료구조를 사용합니다. 이번 Mini Redis에서는 이를 HashMap으로 단순화해 구현하며, 평균적으로 O(1)에 Key를 찾을 수 있습니다.
>
> 메모리 관리에서도 이중 연결 리스트 같은 자료구조를 이용하면 LRU 순서를 효율적으로 관리할 수 있고, TTL에서는 Heap 같은 자료구조를 이용해 빠른 만료 시간을 관리할 수 있습니다.
>
> 따라서 Redis의 성능은 단순히 RAM을 사용한다는 점뿐 아니라, 목적에 맞는 자료구조를 사용하는 것과도 밀접하게 관련되어 있습니다.

---

# 68. 이번 과제에서 반드시 설명할 수 있어야 하는 것

## 1. Redis란?

> 메모리를 중심으로 동작하는 Key-Value 데이터 저장소다.

## 2. 왜 빠른가?

> 메모리를 사용하고 효율적인 자료구조를 이용하기 때문이다.

## 3. SET / GET은 무엇인가?

> Key-Value 저장 및 조회 명령이다.

## 4. TTL은 무엇인가?

> Key가 얼마나 오래 살아 있을지를 나타내는 만료 시간이다.

## 5. EXPIRE는 무엇인가?

> Key에 만료 시간을 지정하는 명령이다.

## 6. maxmemory는 무엇인가?

> Redis가 사용할 수 있는 최대 메모리 제한이다.

## 7. Eviction은 무엇인가?

> 메모리가 부족할 때 기존 데이터를 자동으로 제거하는 것이다.

## 8. LRU란 무엇인가?

> 가장 오랫동안 사용하지 않은 데이터를 먼저 제거하는 정책이다.

## 9. Expiration과 Eviction 차이는?

> Expiration은 TTL 때문이고, Eviction은 메모리 부족 때문이다.

## 10. 왜 HashMap을 사용하는가?

> Key를 평균 O(1)에 찾기 위해서다.

## 11. 왜 Doubly Linked List가 필요한가?

> LRU 순서를 O(1)에 변경하고 오래된 데이터를 O(1)에 찾기 위해서다.

## 12. 왜 Min Heap이 필요한가?

> 가장 빠른 만료 시간을 효율적으로 찾기 위해서다.

---

# 69. 전체 흐름 한 번에 보기

최종적으로 Mini Redis는 다음처럼 이해하면 된다.

```text
사용자

SET user:1 Alice
       │
       ▼
┌──────────────────────┐
│      Mini Redis      │
├──────────────────────┤
│                      │
│ HashMap              │
│ user:1 → Alice       │
│                      │
│ LRU List             │
│ [user:1] ⇄ [...]     │
│                      │
│ TTL Heap             │
│ (expire_at, user:1)  │
│                      │
│ used_memory          │
│ maxmemory            │
│ evicted_keys         │
│                      │
└──────────────────────┘
```

그리고 명령에 따라 이 상태들이 함께 변경된다.

---

# 70. 이 과제의 진짜 학습 목표

겉으로 보면:

```text
Redis 만들기
```

지만 실제 학습 목표는 다음에 가깝다.

```text
HashMap을 왜 사용하는가?

Linked List가 언제 유용한가?

Heap은 어떤 문제를 해결하는가?

서로 다른 자료구조를 어떻게 조합하는가?

시간복잡도가 실제 기능 설계에 어떻게 연결되는가?

메모리라는 제한된 자원을 어떻게 관리하는가?
```

즉 Redis는 자료구조와 알고리즘을 **실제 서비스 문제에 연결해서 공부하기 위한 좋은 예제**다.

---

# 71. 한 문장으로 정리

> 이번 Mini Redis 프로젝트는 메모리에 Key-Value 데이터를 저장하고, HashMap으로 데이터를 빠르게 찾으며, TTL로 데이터의 수명을 관리하고, 메모리가 부족하면 LRU 정책으로 오래 사용하지 않은 데이터를 제거하는 작은 In-Memory 데이터 저장소를 직접 구현하는 과제다.