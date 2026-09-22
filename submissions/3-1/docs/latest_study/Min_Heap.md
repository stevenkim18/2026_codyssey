# 최소 힙(Min Heap)

## 1. 힙(Heap)이란?

힙은 **가장 작은 값이나 가장 큰 값을 빠르게 찾기 위한 트리 기반 자료구조**다.

대표적으로 두 종류가 있다.

```text
Min Heap
→ 가장 작은 값이 루트에 위치

Max Heap
→ 가장 큰 값이 루트에 위치
```

이번 Mini Redis 과제에서는:

```text
Min Heap
```

즉 **최소 힙**을 사용한다.

---

# 2. 최소 힙이란?

최소 힙은 부모 노드가 항상 자식 노드보다 작거나 같은 구조다.

예:

```text
        1
       / \
      3   5
     / \
    7   9
```

조건을 보면:

```text
1 < 3
1 < 5

3 < 7
3 < 9
```

부모가 자식보다 작다.

따라서 가장 작은 값은 항상 가장 위에 있다.

```text
        1
        ↑
     최소값
```

그래서:

```text
가장 작은 값을 찾는 것
```

이 매우 빠르다.

---

# 3. 왜 Redis TTL에서 Min Heap을 사용할까?

이번 Mini Redis에서 TTL을 관리해야 한다.

예를 들어:

```text
A → 10초 후 만료
B → 3초 후 만료
C → 20초 후 만료
D → 7초 후 만료
```

가 있다고 하자.

우리가 가장 자주 알고 싶은 것은:

> 어떤 Key가 가장 먼저 만료되는가?

이다.

위에서는:

```text
B → 3초
```

가 가장 먼저 만료된다.

만료 시간을 기준으로 최소 힙에 넣으면:

```text
        B:3
       /   \
     D:7   C:20
     /
   A:10
```

루트만 보면:

```text
B:3
```

가 가장 빨리 만료된다는 것을 알 수 있다.

---

# 4. TTL에서는 절대 시간을 저장한다

실제로는:

```text
10초 남음
3초 남음
```

처럼 계속 줄어드는 숫자를 저장하기보다:

```text
expire_at
```

즉 실제 만료 시각을 저장하는 것이 좋다.

예를 들어 현재 시간이:

```text
100초
```

라고 하자.

```text
EXPIRE A 10
```

이면:

```text
expire_at = 100 + 10
          = 110
```

이다.

따라서 Heap에는:

```text
(110, "A")
```

형태로 저장할 수 있다.

예:

```text
(103, "B")
(107, "D")
(110, "A")
(120, "C")
```

최소 힙에서는 가장 작은:

```text
(103, "B")
```

가 맨 위에 있게 된다.

---

# 5. 힙은 이진 트리다

힙은 기본적으로 **완전 이진 트리(Complete Binary Tree)** 형태를 가진다.

이진 트리는 각 노드가 최대 두 개의 자식을 가진다.

```text
        A
       / \
      B   C
```

완전 이진 트리는 위에서부터, 왼쪽부터 빈칸 없이 채우는 형태다.

예:

```text
        1
       / \
      3   5
     / \  /
    7  9 8
```

이건 완전 이진 트리다.

하지만:

```text
        1
       / \
      3   5
       \
        7
```

처럼 왼쪽을 비워두고 오른쪽부터 채우면 힙 구조로 적절하지 않다.

---

# 6. 그런데 실제 구현에서는 트리 Node를 만들지 않는다

연결 리스트에서는:

```python
class Node:
    ...
```

같은 Node 객체를 만들었다.

힙은 보통 **배열**로 구현한다.

예를 들어:

```text
        1
       / \
      3   5
     / \
    7   9
```

를 배열로 표현하면:

```python
[1, 3, 5, 7, 9]
```

이다.

index를 표시하면:

```text
값:      1   3   5   7   9
index:   0   1   2   3   4
```

---

# 7. 왜 배열로 트리를 표현할 수 있을까?

완전 이진 트리이기 때문이다.

배열 index를 이용하면 부모와 자식 위치를 계산할 수 있다.

어떤 노드의 index가 `i`라고 하면:

```python
left = i * 2 + 1
right = i * 2 + 2
```

부모는:

```python
parent = (i - 1) // 2
```

이다.

---

# 8. 예제로 이해하기

배열:

```python
[1, 3, 5, 7, 9]
```

트리:

```text
        1
       / \
      3   5
     / \
    7   9
```

index:

```text
        0
       / \
      1   2
     / \
    3   4
```

index 1의 자식은:

```python
left = 1 * 2 + 1
     = 3

right = 1 * 2 + 2
      = 4
```

그래서:

```text
index 1 → 값 3

왼쪽 자식 index 3 → 값 7
오른쪽 자식 index 4 → 값 9
```

가 된다.

---

# 9. 부모 index 구하기

index 4의 부모를 찾으면:

```python
parent = (4 - 1) // 2
       = 1
```

따라서:

```text
index 4 → 값 9

부모 index 1 → 값 3
```

실제 트리에서도:

```text
      3
       \
        9
```

이다.

---

# 10. Min Heap의 핵심 규칙

최소 힙에서 중요한 규칙은 단 하나다.

> 부모는 자식보다 작거나 같아야 한다.

예:

```text
        2
       / \
      5   7
     / \
    9   10
```

정상이다.

하지만:

```text
        10
       /  \
      5    7
```

은 최소 힙이 아니다.

왜냐하면:

```text
10 > 5
```

이고 부모가 자식보다 크기 때문이다.

---

# 11. 중요한 점: 전체가 정렬되어 있는 것은 아니다

최소 힙을 보고:

```text
모든 값이 정렬되어 있다
```

라고 생각하면 안 된다.

예:

```text
        1
       / \
      4   2
     / \
    10  8
```

이것도 정상적인 최소 힙이다.

왜냐하면:

```text
1 <= 4
1 <= 2

4 <= 10
4 <= 8
```

이기 때문이다.

하지만 배열은:

```python
[1, 4, 2, 10, 8]
```

이고 정렬된 배열은 아니다.

즉 Heap은:

```text
전체 정렬 X

최소값만 빠르게 찾기 O
```

를 위한 자료구조다.

---

# 12. Heap의 주요 기능

이번 과제에서 구현할 것은:

```python
push()
pop()
peek()
size()
```

그리고 내부 기능:

```python
_heapify_up()
_heapify_down()
```

이다.

---

# 13. peek()

가장 쉬운 기능이다.

최소 힙의 가장 작은 값은 항상:

```text
index 0
```

에 있다.

따라서:

```python
def peek(self):
    if self.size() == 0:
        return None

    return self.data[0]
```

이다.

시간 복잡도:

```text
O(1)
```

이다.

---

# 14. size()

배열에 데이터가 몇 개 있는지 반환한다.

```python
def size(self):
    return len(self.data)
```

학습용 동적 배열을 직접 구현한다면 별도의 `count`를 관리할 수도 있다.

---

# 15. push()

새로운 값을 Heap에 넣는 기능이다.

현재:

```text
        2
       / \
      5   7
     /
    9
```

배열:

```python
[2, 5, 7, 9]
```

여기에:

```text
3
```

을 넣어보자.

---

# 16. 새로운 값은 우선 맨 뒤에 넣는다

완전 이진 트리 모양을 유지하기 위해 무조건 배열 마지막에 추가한다.

```python
[2, 5, 7, 9, 3]
```

트리:

```text
        2
       / \
      5   7
     / \
    9   3
```

그런데 문제가 있다.

```text
5 > 3
```

이라서 최소 힙 규칙이 깨졌다.

그래서 위로 올라가면서 부모와 비교해야 한다.

이 작업이:

```text
Heapify Up
```

이다.

---

# 17. heapify_up

현재:

```text
        2
       / \
      5   7
     / \
    9   3
```

3의 부모는 5다.

```text
3 < 5
```

이므로 둘을 교환한다.

```text
        2
       / \
      3   7
     / \
    9   5
```

이제 3의 부모는 2다.

```text
3 >= 2
```

이므로 멈춘다.

최소 힙 조건이 다시 만족되었다.

---

# 18. heapify_up 코드

```python
def _heapify_up(self, index):
    while index > 0:
        parent = (index - 1) // 2

        if self.data[parent] <= self.data[index]:
            break

        self.data[parent], self.data[index] = (
            self.data[index],
            self.data[parent],
        )

        index = parent
```

핵심 흐름은:

```text
현재 노드
 ↓
부모 확인
 ↓
내가 부모보다 작음?
 ↓
YES → 교환
 ↓
다시 위쪽 부모 확인
```

이다.

---

# 19. push 전체 코드

```python
def push(self, value):
    self.data.append(value)

    index = len(self.data) - 1

    self._heapify_up(index)
```

즉:

```text
맨 뒤에 추가
→ Heapify Up
```

두 단계다.

---

# 20. 왜 push가 O(log N)인가?

Heap은 완전 이진 트리다.

노드가 8개 정도면 높이는 약 3이고:

```text
       *
      / \
     *   *
    / \ / \
   *  * *  *
```

노드가 두 배가 되어도 높이는 1 정도만 증가한다.

즉 트리의 높이는:

```text
log N
```

수준이다.

새로운 노드가 최악의 경우:

```text
맨 아래 → 루트
```

까지 이동한다.

그래서:

```text
push = O(log N)
```

이다.

---

# 21. pop()

`pop()`은 **최소값을 제거하고 반환하는 기능**이다.

현재:

```text
        1
       / \
      3   5
     / \
    7   9
```

배열:

```python
[1, 3, 5, 7, 9]
```

최소값:

```text
1
```

을 제거하고 싶다.

그런데 단순히 index 0을 제거하면 배열 구조를 유지하기가 어려워진다.

그래서 보통 다음 방법을 사용한다.

---

# 22. 마지막 값을 루트로 옮긴다

현재:

```python
[1, 3, 5, 7, 9]
```

최소값 1을 기억해둔다.

```text
minimum = 1
```

그리고 마지막 값 9를 루트로 옮긴다.

```python
[9, 3, 5, 7]
```

트리:

```text
        9
       / \
      3   5
     /
    7
```

하지만:

```text
9 > 3
```

이라서 최소 힙 규칙이 깨졌다.

이번에는 아래 방향으로 내려가면서 수정한다.

이것이:

```text
Heapify Down
```

이다.

---

# 23. heapify_down

현재:

```text
        9
       / \
      3   5
     /
    7
```

9의 자식:

```text
3
5
```

중 더 작은 값은:

```text
3
```

이다.

9와 3을 교환한다.

```text
        3
       / \
      9   5
     /
    7
```

아직:

```text
9 > 7
```

이다.

다시 교환:

```text
        3
       / \
      7   5
     /
    9
```

이제 조건이 만족된다.

---

# 24. 왜 두 자식 중 더 작은 자식과 바꾸는가?

현재:

```text
        9
       / \
      3   5
```

9를 5와 바꾸면:

```text
        5
       / \
      3   9
```

가 된다.

그런데:

```text
5 > 3
```

이라 여전히 최소 힙 조건이 깨져 있다.

그래서 반드시:

```text
더 작은 자식
```

과 교환해야 한다.

---

# 25. heapify_down 코드

```python
def _heapify_down(self, index):
    size = len(self.data)

    while True:
        left = index * 2 + 1
        right = index * 2 + 2

        smallest = index

        if left < size and self.data[left] < self.data[smallest]:
            smallest = left

        if right < size and self.data[right] < self.data[smallest]:
            smallest = right

        if smallest == index:
            break

        self.data[index], self.data[smallest] = (
            self.data[smallest],
            self.data[index],
        )

        index = smallest
```

흐름:

```text
현재 노드
 ↓
왼쪽 자식 확인
 ↓
오른쪽 자식 확인
 ↓
셋 중 가장 작은 위치 찾기
 ↓
현재가 가장 작음?
 ├─ YES → 종료
 └─ NO  → 가장 작은 자식과 교환
```

이다.

---

# 26. pop 전체 코드

```python
def pop(self):
    if len(self.data) == 0:
        return None

    if len(self.data) == 1:
        return self.data.pop()

    minimum = self.data[0]

    last = self.data.pop()

    self.data[0] = last

    self._heapify_down(0)

    return minimum
```

즉:

```text
최소값 저장
 ↓
마지막 값 제거
 ↓
마지막 값을 root로 이동
 ↓
heapify_down
 ↓
기존 최소값 반환
```

이다.

---

# 27. pop도 O(log N)

`heapify_down`은 최대 트리 높이만큼 내려간다.

따라서:

```text
pop = O(log N)
```

이다.

---

# 28. Min Heap 주요 시간 복잡도

| 연산 | 시간복잡도 |
|---|---:|
| peek | O(1) |
| push | O(log N) |
| pop | O(log N) |
| size | O(1) |
| 특정 값 검색 | O(N) |

특히 Min Heap의 가장 중요한 장점은:

```text
최소값 조회 = O(1)
```

이다.

---

# 29. Heap은 검색용 자료구조가 아니다

예를 들어:

```python
[1, 4, 2, 10, 8, 5]
```

에서:

```text
8이 어디 있는가?
```

를 찾고 싶다고 하자.

Heap은 BST처럼 검색을 위한 구조가 아니다.

최악에는 전체 배열을 확인해야 한다.

```text
O(N)
```

이다.

Heap이 잘하는 것은:

```text
최소값 또는 최대값 관리
```

이다.

---

# 30. Min Heap 클래스 기본 구현

```python
class MinHeap:
    def __init__(self):
        self.data = []

    def size(self):
        return len(self.data)

    def peek(self):
        if len(self.data) == 0:
            return None

        return self.data[0]

    def push(self, value):
        self.data.append(value)

        index = len(self.data) - 1

        self._heapify_up(index)

    def pop(self):
        if len(self.data) == 0:
            return None

        if len(self.data) == 1:
            return self.data.pop()

        minimum = self.data[0]

        last = self.data.pop()

        self.data[0] = last

        self._heapify_down(0)

        return minimum

    def _heapify_up(self, index):
        while index > 0:
            parent = (index - 1) // 2

            if self.data[parent] <= self.data[index]:
                break

            self.data[parent], self.data[index] = (
                self.data[index],
                self.data[parent],
            )

            index = parent

    def _heapify_down(self, index):
        size = len(self.data)

        while True:
            left = index * 2 + 1
            right = index * 2 + 2

            smallest = index

            if left < size and self.data[left] < self.data[smallest]:
                smallest = left

            if right < size and self.data[right] < self.data[smallest]:
                smallest = right

            if smallest == index:
                break

            self.data[index], self.data[smallest] = (
                self.data[smallest],
                self.data[index],
            )

            index = smallest
```

---

# 31. 직접 테스트해보기

```python
heap = MinHeap()

heap.push(5)
heap.push(3)
heap.push(10)
heap.push(1)
heap.push(7)
```

내부 배열은 상황에 따라:

```text
[1, 3, 10, 5, 7]
```

같이 될 수 있다.

중요한 것은 배열 전체가 정렬되었는지가 아니다.

```python
print(heap.peek())
```

결과:

```text
1
```

이어야 한다.

---

# 32. pop 테스트

```python
print(heap.pop())
```

결과:

```text
1
```

다음 최소값:

```python
print(heap.peek())
```

결과:

```text
3
```

다시:

```python
print(heap.pop())
```

결과:

```text
3
```

이런 식으로 계속 `pop()` 하면 작은 값부터 나온다.

---

# 33. TTL에서는 숫자 하나가 아니라 Tuple을 저장한다

이번 과제에서는:

```text
(expire_at, key)
```

형태로 저장해야 한다.

예:

```python
heap.push((100, "user:1"))
heap.push((80, "user:2"))
heap.push((120, "user:3"))
```

Python tuple은 앞쪽 값부터 비교할 수 있다.

따라서:

```text
(80, "user:2")
```

가 가장 작은 값이다.

Heap:

```text
           (80, user:2)
            /         \
(100, user:1)       (120, user:3)
```

이런 식으로 관리할 수 있다.

---

# 34. TTL 전체 흐름

예를 들어 현재 시간이:

```text
100
```

이라고 하자.

사용자가:

```text
EXPIRE A 30
```

을 실행한다.

계산:

```text
expire_at = 100 + 30
          = 130
```

Heap:

```python
heap.push((130, "A"))
```

또:

```text
EXPIRE B 10
```

이면:

```text
expire_at = 110
```

Heap:

```text
(110, B)
(130, A)
```

따라서:

```python
heap.peek()
```

하면:

```text
(110, "B")
```

가 나온다.

즉:

```text
B가 가장 먼저 만료된다
```

는 것을 바로 알 수 있다.

---

# 35. 그런데 Heap만으로 TTL을 관리할 수 있을까?

문제가 하나 있다.

예:

```text
EXPIRE A 10
```

Heap:

```text
(110, A)
```

그런데 다시:

```text
EXPIRE A 100
```

을 실행하면:

```text
(110, A)
(200, A)
```

처럼 같은 Key에 대한 만료 정보가 두 개 생길 수 있다.

그럼 `(110, A)`는 더 이상 유효하지 않은 오래된 정보다.

---

# 36. Lazy Deletion

이 문제를 간단하게 해결하는 방법이:

```text
Lazy Deletion
```

이다.

Heap에서 기존 `(110, A)`를 억지로 찾아 삭제하지 않는다.

그대로 둔다.

나중에:

```text
(110, A)
```

가 Heap의 맨 위로 올라왔을 때 확인한다.

```text
A의 현재 실제 TTL이 정말 110인가?
```

만약 실제 저장된 만료 시간이:

```text
200
```

이라면:

```text
110은 오래된 정보
```

이므로 그냥 버린다.

---

# 37. TTL을 위해 별도의 만료 정보가 필요하다

개념적으로:

```text
expire_map

A → 200
B → 150
```

같은 구조가 필요할 수 있다.

이번 과제에서는 `dict`를 쓸 수 없으므로 이것 역시 직접 구현한 HashMap을 사용할 수 있다.

즉:

```text
TTL Heap
+
HashMap
```

조합을 사용할 수 있다.

예:

```text
expire_map

"A" → 200
```

Heap:

```text
(110, A)
(200, A)
```

현재 시간이 120일 때 Heap top:

```text
(110, A)
```

를 꺼낸다.

그리고:

```text
expire_map["A"] == 110 ?
```

확인한다.

실제는:

```text
200
```

이므로:

```text
오래된 Heap Entry
→ 무시
```

한다.

---

# 38. 왜 Heap 중간에서 직접 삭제하지 않을까?

Heap 배열이:

```python
[
    (100, "A"),
    (120, "B"),
    (130, "C"),
    (200, "D"),
    ...
]
```

이라고 하자.

`C`가 어느 index에 있는지 모른다.

찾으려면:

```text
O(N)
```

검색이 필요하다.

그리고 중간 값을 제거하면:

```text
heapify_up
또는
heapify_down
```

도 다시 해야 한다.

그래서 TTL 같은 상황에서는:

```text
기존 값은 놔두고
나중에 필요할 때 무효인지 확인
```

하는 Lazy Deletion 방식이 구현하기 쉽다.

---

# 39. 만료 Key 정리하기

예를 들어 현재 시간이:

```text
150
```

이고 Heap이:

```text
(100, A)
(120, B)
(200, C)
```

라면:

```text
peek()
```

값이 현재 시간보다 작거나 같을 동안 반복할 수 있다.

개념:

```python
while heap is not empty:
    expire_at, key = heap.peek()

    if expire_at > current_time:
        break

    heap.pop()

    # 실제 TTL과 같은 정보인지 확인
    # 같다면 key 만료 처리
```

즉:

```text
Heap의 가장 빠른 만료 데이터
 ↓
이미 만료되었는지 확인
 ↓
만료되었다면 제거
 ↓
다음 Heap top 확인
```

을 반복한다.

---

# 40. Heap과 HashMap의 역할 차이

TTL에서 이 둘을 혼동하면 안 된다.

## HashMap

```text
A → 200
```

를 통해:

> A의 현재 실제 만료 시간이 언제인가?

를 찾는다.

---

## Min Heap

```text
(100, B)
(120, C)
(200, A)
```

를 통해:

> 전체 Key 중에서 가장 빨리 만료되는 것은 무엇인가?

를 빠르게 찾는다.

즉:

```text
HashMap
→ 특정 Key 찾기

Min Heap
→ 최소 expire_at 찾기
```

다.

---

# 41. 이번 Mini Redis 구조

전체 구조를 보면:

```text
                    Mini Redis

   ┌────────────────────┼────────────────────┐
   │                    │                    │
   ▼                    ▼                    ▼

HashMap              LRU List             Min Heap
데이터 저장          사용 순서            만료 시간

Key → Value        최근 ⇄ 오래됨       expire_at 최소값
```

TTL 쪽만 더 자세히 보면:

```text
                   TTL

          ┌─────────┴─────────┐
          ▼                   ▼

     Expire HashMap        Min Heap

     Key → expire_at       (expire_at, key)

          │                   │
          ▼                   ▼

   특정 Key의 실제       가장 빨리 만료될
   TTL 확인              Key 찾기
```

라고 이해하면 좋다.

---

# 42. 연결 리스트와 Heap의 차이

둘 다 순서를 관리하는 것처럼 보여서 헷갈릴 수 있다.

## Doubly Linked List

LRU에서:

```text
최근 사용 순서
```

를 직접 관리한다.

```text
C ⇄ B ⇄ A
```

특정 노드를 알고 있다면:

```text
move_to_front = O(1)
```

이다.

---

## Heap

TTL에서:

```text
가장 작은 만료 시간
```

을 관리한다.

```text
       100
      /   \
    120   150
```

새로운 값을 넣거나 제거하면:

```text
O(log N)
```

으로 Heap 구조를 다시 맞춘다.

---

# 43. HashMap / Linked List / Heap 비교

| 자료구조 | 잘하는 것 | 주요 사용 |
|---|---|---|
| HashMap | Key 빠르게 찾기 | Redis 데이터 저장 |
| Doubly Linked List | 순서 이동 | LRU |
| Min Heap | 최소값 찾기 | TTL |
| Array | index 접근 | Heap 내부 저장 |

이번 과제의 핵심은 이 세 자료구조를 각각 구현하는 것보다:

```text
어떤 문제에 어떤 자료구조를 사용해야 하는가?
```

를 이해하는 것이다.

---

# 44. Heap을 설명한다면

다음 정도로 설명할 수 있으면 좋다.

> 힙은 최댓값이나 최솟값을 빠르게 관리하기 위한 완전 이진 트리 기반 자료구조입니다.
>
> 최소 힙에서는 모든 부모 노드가 자식 노드보다 작거나 같기 때문에 가장 작은 값이 항상 루트에 위치합니다.
>
> 보통 완전 이진 트리의 특성을 이용해 배열로 구현하고, index를 이용해서 부모와 자식의 위치를 계산할 수 있습니다.
>
> 새로운 값을 삽입할 때는 배열 마지막에 추가한 뒤 부모와 비교하며 위로 올리는 `heapify_up`을 수행합니다.
>
> 최소값을 제거할 때는 마지막 값을 루트로 이동시킨 뒤 더 작은 자식과 비교하며 내려가는 `heapify_down`을 수행합니다.
>
> 그래서 최소값 조회는 O(1), 삽입과 삭제는 O(log N)에 처리할 수 있습니다.
>
> 이번 Mini Redis에서는 `(expire_at, key)`를 최소 힙에 저장해서 가장 빨리 만료될 Key를 효율적으로 찾는 데 사용합니다.

---

# 45. 꼭 기억해야 하는 index 공식

0부터 시작하는 배열 기준이다.

현재 index:

```text
i
```

왼쪽 자식:

```python
i * 2 + 1
```

오른쪽 자식:

```python
i * 2 + 2
```

부모:

```python
(i - 1) // 2
```

예:

```text
index 3
```

부모:

```text
(3 - 1) // 2
= 1
```

이다.

---

# 46. 가장 많이 헷갈리는 부분

## Q1. Min Heap은 정렬된 배열인가?

아니다.

```python
[1, 5, 2, 10, 8, 4]
```

도 최소 힙일 수 있다.

중요한 것은:

```text
부모 <= 자식
```

이다.

---

## Q2. 최소값은 어디 있는가?

항상:

```text
index 0
```

이다.

---

## Q3. 왜 배열 마지막에 삽입하는가?

완전 이진 트리 모양을 유지하기 위해서다.

---

## Q4. 새로 넣은 값이 작으면 어떻게 하는가?

```text
heapify_up
```

으로 부모와 계속 비교하며 위로 올린다.

---

## Q5. root를 삭제한 뒤에는?

마지막 값을 root로 옮기고:

```text
heapify_down
```

으로 내려보낸다.

---

## Q6. 왜 TTL에 Heap을 쓰는가?

전체 Key 중:

```text
가장 빨리 만료될 Key
```

를 빠르게 알기 위해서다.

---

# 47. 연습 문제

## 문제 1

배열:

```python
[2, 5, 7, 9, 10]
```

에서 index 1의 왼쪽 자식 index는?

```python
1 * 2 + 1
= 3
```

정답:

```text
3
```

---

## 문제 2

index 5의 부모는?

```python
(5 - 1) // 2
= 2
```

정답:

```text
2
```

---

## 문제 3

다음은 최소 힙인가?

```text
        1
       / \
      5   3
     / \
    8   9
```

정답:

```text
Yes
```

이유:

```text
1 <= 5
1 <= 3
5 <= 8
5 <= 9
```

이기 때문이다.

형제끼리:

```text
5 > 3
```

인 것은 상관없다.

---

## 문제 4

다음은 최소 힙인가?

```text
        5
       / \
      3   7
```

정답:

```text
No
```

부모 5가 자식 3보다 크기 때문이다.

---

## 문제 5

현재 Heap:

```text
        2
       / \
      4   7
```

여기에 1을 넣으면?

우선:

```text
        2
       / \
      4   7
     /
    1
```

`heapify_up`:

```text
        2
       / \
      1   7
     /
    4
```

다시:

```text
        1
       / \
      2   7
     /
    4
```

최종 결과다.

---

# 48. 학습 체크리스트

다음 질문에 자신의 말로 답할 수 있으면 된다.

- Heap이란 무엇인가?
- Min Heap과 Max Heap의 차이는?
- 최소 힙의 핵심 규칙은?
- 완전 이진 트리는 무엇인가?
- 왜 Heap을 배열로 표현할 수 있는가?
- 부모 index 계산 공식은?
- 왼쪽/오른쪽 자식 index 공식은?
- `push()`는 어떻게 동작하는가?
- `heapify_up`은 무엇인가?
- `pop()`은 어떻게 동작하는가?
- `heapify_down`은 무엇인가?
- 왜 `peek()`은 O(1)인가?
- 왜 `push()`와 `pop()`은 O(log N)인가?
- Heap은 왜 특정 값 검색에는 좋지 않은가?
- TTL에서 왜 Min Heap을 사용하는가?
- `(expire_at, key)`는 무엇을 의미하는가?
- Lazy Deletion은 왜 필요한가?
- TTL에서 HashMap과 Min Heap의 역할 차이는 무엇인가?

---

# 49. 이번 프로젝트에서 핵심만 다시 정리

```text
Heap
│
├─ 완전 이진 트리
│
├─ 배열로 구현
│
├─ 부모 <= 자식
│
├─ 최소값은 index 0
│
├─ push
│    └─ heapify_up
│
├─ pop
│    └─ heapify_down
│
└─ TTL
     └─ (expire_at, key)
```

---

# 50. 한 문장으로 정리

> 최소 힙은 부모가 자식보다 작거나 같은 완전 이진 트리 구조로, 가장 작은 값을 O(1)에 확인하고 삽입·삭제를 O(log N)에 처리할 수 있어 Mini Redis에서 가장 빨리 만료될 TTL 데이터를 관리하는 데 적합하다.