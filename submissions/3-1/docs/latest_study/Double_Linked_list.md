# 이중 연결 리스트(Doubly Linked List)

## 1. 이중 연결 리스트란?

이중 연결 리스트(Doubly Linked List)는 여러 개의 데이터를 **노드(Node)** 라는 단위로 연결해서 저장하는 자료구조다.

각 노드는 다음 세 가지 정보를 가진다.

```text
prev | data | next
```

- `data`: 실제 저장할 데이터
- `prev`: 이전 노드를 가리키는 참조
- `next`: 다음 노드를 가리키는 참조

예를 들어 A, B, C라는 데이터가 있다면 다음과 같이 연결할 수 있다.

```text
None ← [ A ] ⇄ [ B ] ⇄ [ C ] → None
```

조금 더 자세히 표현하면 다음과 같다.

```text
       ┌───────────┐
       │           ↓
None ← [ A ] ⇄ [ B ] ⇄ [ C ] → None
         ↑         ↑         ↑
        data      data      data
```

A의 `next`는 B를 가리킨다.

```text
A.next → B
```

B의 `prev`는 A를 가리킨다.

```text
B.prev → A
```

동시에 B는 C도 알고 있다.

```text
B.next → C
C.prev → B
```

즉, 앞뒤 양쪽으로 이동할 수 있기 때문에 **이중(Double) 연결 리스트**라고 부른다.

---

# 2. 먼저 Node를 이해하자

연결 리스트에서 가장 중요한 개념은 `Node`다.

Python으로 가장 단순한 Node를 만들어 보면 다음과 같다.

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None
```

노드를 하나 만들면:

```python
node = Node("A")
```

메모리의 모습을 개념적으로 표현하면 다음과 같다.

```text
node
 ↓

┌─────────────┐
│ prev = None │
│ data = "A"  │
│ next = None │
└─────────────┘
```

아직 다른 노드와 연결되어 있지 않기 때문에 `prev`와 `next`는 `None`이다.

---

# 3. 노드를 직접 연결해 보기

세 개의 노드를 만들어 보자.

```python
a = Node("A")
b = Node("B")
c = Node("C")
```

현재는 서로 독립되어 있다.

```text
[A]    [B]    [C]
```

A와 B를 연결하려면 다음과 같이 한다.

```python
a.next = b
b.prev = a
```

그러면:

```text
[A] ⇄ [B]
```

가 된다.

이번에는 B와 C를 연결한다.

```python
b.next = c
c.prev = b
```

결과:

```text
[A] ⇄ [B] ⇄ [C]
```

코드 전체는 다음과 같다.

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


a = Node("A")
b = Node("B")
c = Node("C")

a.next = b
b.prev = a

b.next = c
c.prev = b
```

이제 다음과 같은 접근이 가능하다.

```python
print(a.next.data)
```

결과:

```text
B
```

또는:

```python
print(c.prev.data)
```

결과:

```text
B
```

즉,

```text
A → B
```

뿐만 아니라

```text
C → B
```

처럼 반대 방향으로도 이동할 수 있다.

---

# 4. 왜 그냥 Python list를 사용하지 않을까?

Python에는 이미 리스트가 있다.

```python
arr = ["A", "B", "C"]
```

그러면 굳이 연결 리스트를 왜 배워야 할까?

핵심 차이는 **데이터를 저장하는 방식**에 있다.

Python의 배열 형태를 단순화해서 생각하면:

```text
0     1     2     3
↓     ↓     ↓     ↓

[A]  [B]  [C]  [D]
```

각 데이터가 순서대로 저장되어 있다.

반면 연결 리스트는:

```text
[A] → [B] → [C] → [D]
```

각 노드가 다음 노드를 가리킨다.

이중 연결 리스트라면:

```text
[A] ⇄ [B] ⇄ [C] ⇄ [D]
```

이다.

이 차이 때문에 특정 상황에서는 연결 리스트가 유리하다.

---

# 5. 연결 리스트의 핵심 장점

이중 연결 리스트의 가장 큰 장점은 **노드를 이미 알고 있다면 삽입, 삭제, 이동을 매우 빠르게 할 수 있다는 것**이다.

예를 들어 다음 리스트가 있다고 하자.

```text
[A] ⇄ [B] ⇄ [C]
```

B를 삭제하려고 한다.

배열에서는 중간 데이터를 삭제하면 뒤쪽 데이터를 이동해야 할 수 있다.

하지만 연결 리스트에서는 연결만 바꾸면 된다.

현재:

```text
A.next → B
B.prev → A

B.next → C
C.prev → B
```

B를 제거하면:

```python
b.prev.next = b.next
b.next.prev = b.prev
```

즉:

```python
a.next = c
c.prev = a
```

결과:

```text
[A] ⇄ [C]
```

B 이후의 모든 데이터를 하나씩 옮길 필요가 없다.

---

# 6. 이중 연결 리스트 클래스 만들기

보통 리스트 자체를 관리하는 클래스도 만든다.

```python
class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
```

여기서:

- `head`: 가장 앞 노드
- `tail`: 가장 뒤 노드

를 의미한다.

예:

```text
head                   tail
 ↓                       ↓

[A] ⇄ [B] ⇄ [C] ⇄ [D]
```

아무 데이터도 없다면:

```text
head = None
tail = None
```

이다.

---

# 7. insert_front

`insert_front`는 리스트의 가장 앞에 노드를 추가하는 기능이다.

기존 리스트:

```text
head
 ↓

[A] ⇄ [B] ⇄ [C]
```

D를 앞에 넣는다면:

```text
head
 ↓

[D] ⇄ [A] ⇄ [B] ⇄ [C]
```

가 되어야 한다.

구현:

```python
def insert_front(self, data):
    new_node = Node(data)

    if self.head is None:
        self.head = new_node
        self.tail = new_node
        return new_node

    new_node.next = self.head
    self.head.prev = new_node
    self.head = new_node

    return new_node
```

## 빈 리스트일 경우

처음에는:

```text
head = None
tail = None
```

이다.

A를 삽입하면:

```text
head
 ↓
[A]
 ↑
tail
```

하나의 노드가 동시에 `head`와 `tail`이 된다.

그래서:

```python
self.head = new_node
self.tail = new_node
```

로 설정한다.

---

## 데이터가 이미 있는 경우

기존 상태:

```text
head
 ↓

[A] ⇄ [B]
```

C를 앞에 추가한다.

먼저:

```python
new_node.next = self.head
```

하면:

```text
[C] → [A] ⇄ [B]
```

그리고 기존 head가 C를 이전 노드로 가리키게 한다.

```python
self.head.prev = new_node
```

```text
[C] ⇄ [A] ⇄ [B]
```

마지막으로:

```python
self.head = new_node
```

하면:

```text
head
 ↓

[C] ⇄ [A] ⇄ [B]
```

가 완성된다.

---

# 8. insert_back

이번에는 리스트의 뒤에 추가한다.

기존:

```text
[A] ⇄ [B] ⇄ [C]
```

D를 추가하면:

```text
[A] ⇄ [B] ⇄ [C] ⇄ [D]
```

가 된다.

코드:

```python
def insert_back(self, data):
    new_node = Node(data)

    if self.tail is None:
        self.head = new_node
        self.tail = new_node
        return new_node

    new_node.prev = self.tail
    self.tail.next = new_node
    self.tail = new_node

    return new_node
```

기존 `tail`만 알고 있으면 리스트를 처음부터 탐색할 필요가 없다.

따라서:

```text
insert_back = O(1)
```

이다.

---

# 9. remove_front

가장 앞의 데이터를 제거해 보자.

기존:

```text
head
 ↓

[A] ⇄ [B] ⇄ [C]
```

A를 제거하면:

```text
head
 ↓

[B] ⇄ [C]
```

가 되어야 한다.

코드:

```python
def remove_front(self):
    if self.head is None:
        return None

    removed = self.head

    if self.head == self.tail:
        self.head = None
        self.tail = None
    else:
        self.head = self.head.next
        self.head.prev = None

    removed.next = None
    removed.prev = None

    return removed
```

여기서 특별히 고려해야 하는 상황이 있다.

노드가 하나뿐일 때다.

```text
head
 ↓
[A]
 ↑
tail
```

A를 제거하면:

```text
head = None
tail = None
```

이 되어야 한다.

---

# 10. remove_back

가장 뒤쪽 노드를 제거하는 것도 거의 동일하다.

기존:

```text
[A] ⇄ [B] ⇄ [C]
               ↑
              tail
```

C 제거:

```text
[A] ⇄ [B]
         ↑
        tail
```

코드:

```python
def remove_back(self):
    if self.tail is None:
        return None

    removed = self.tail

    if self.head == self.tail:
        self.head = None
        self.tail = None
    else:
        self.tail = self.tail.prev
        self.tail.next = None

    removed.prev = None
    removed.next = None

    return removed
```

---

# 11. remove_node

이중 연결 리스트에서 가장 중요한 기능 중 하나다.

특정 노드를 직접 삭제한다.

예:

```text
[A] ⇄ [B] ⇄ [C] ⇄ [D]
```

B라는 Node 객체를 이미 알고 있다고 가정한다.

```text
[A] ⇄ [B] ⇄ [C] ⇄ [D]
       ↑
     삭제
```

B는 자기 주변을 알고 있다.

```text
B.prev = A
B.next = C
```

따라서:

```python
B.prev.next = B.next
B.next.prev = B.prev
```

를 수행하면 된다.

결과:

```text
[A] ⇄ [C] ⇄ [D]
```

전체 구현은 다음과 같이 할 수 있다.

```python
def remove_node(self, node):
    if node is None:
        return None

    if node == self.head:
        return self.remove_front()

    if node == self.tail:
        return self.remove_back()

    node.prev.next = node.next
    node.next.prev = node.prev

    node.prev = None
    node.next = None

    return node
```

---

# 12. 왜 remove_node가 O(1)인가?

이 부분이 아주 중요하다.

다음처럼 노드가 100만 개 있다고 하자.

```text
[A] ⇄ [B] ⇄ [C] ⇄ ... ⇄ [999999] ⇄ [1000000]
```

그런데 우리가 삭제할 노드 객체를 이미 가지고 있다.

```python
node = 어떤_노드
```

그렇다면 필요한 것은 오직:

```python
node.prev
node.next
```

뿐이다.

리스트에 노드가:

```text
10개
100개
1,000개
1,000,000개
```

있어도 수행할 작업 수는 거의 같다.

그래서:

```text
O(1)
```

이라고 한다.

다만 중요한 전제가 있다.

**삭제하려는 노드를 이미 알고 있어야 한다.**

---

# 13. 노드를 찾는 것은 O(N)

반대로 다음처럼 데이터만 주어진다면:

```python
remove("apple")
```

"apple"이 어느 노드인지 모른다.

그러면:

```text
head → 다음 → 다음 → 다음 → ...
```

순서대로 찾을 수밖에 없다.

최악의 경우 모든 데이터를 봐야 한다.

따라서:

```text
검색 = O(N)
```

이다.

이것이 나중에 **HashMap과 Doubly Linked List를 함께 사용하는 이유**다.

---

# 14. move_to_front

이번 Mini Redis 과제에서 특히 중요한 기능이다.

다음 리스트가 있다고 하자.

```text
[A] ⇄ [B] ⇄ [C] ⇄ [D]
```

C를 가장 앞으로 이동시키고 싶다.

결과:

```text
[C] ⇄ [A] ⇄ [B] ⇄ [D]
```

방법은 크게 두 단계다.

```text
1. C를 현재 위치에서 제거
2. C를 head 앞에 삽입
```

하지만 새로운 Node를 만들 필요는 없다.

기존 Node를 그대로 움직인다.

```python
def move_to_front(self, node):
    if node is None:
        return

    if node == self.head:
        return

    if node == self.tail:
        self.tail = node.prev
        self.tail.next = None
    else:
        node.prev.next = node.next
        node.next.prev = node.prev

    node.prev = None
    node.next = self.head

    self.head.prev = node
    self.head = node
```

---

# 15. move_to_front 동작 이해하기

다음 상황을 보자.

```text
head                   tail
 ↓                       ↓

[A] ⇄ [B] ⇄ [C] ⇄ [D]
             ↑
           이동
```

먼저 C를 제거한다.

```text
[A] ⇄ [B]     [C]     [D]
         └────────────→
```

실제로는:

```python
C.prev.next = C.next
C.next.prev = C.prev
```

이므로:

```text
[A] ⇄ [B] ⇄ [D]
```

가 된다.

그다음 C를 앞에 넣는다.

```text
[C] ⇄ [A] ⇄ [B] ⇄ [D]
```

이 과정에서도 리스트 전체를 탐색하지 않는다.

따라서:

```text
move_to_front = O(1)
```

이다.

---

# 16. 완성된 기본 구현

지금까지 내용을 합치면 다음 정도가 된다.

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_front(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return new_node

        new_node.next = self.head
        self.head.prev = new_node
        self.head = new_node

        return new_node

    def insert_back(self, data):
        new_node = Node(data)

        if self.tail is None:
            self.head = new_node
            self.tail = new_node
            return new_node

        new_node.prev = self.tail
        self.tail.next = new_node
        self.tail = new_node

        return new_node

    def remove_front(self):
        if self.head is None:
            return None

        removed = self.head

        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None

        removed.prev = None
        removed.next = None

        return removed

    def remove_back(self):
        if self.tail is None:
            return None

        removed = self.tail

        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None

        removed.prev = None
        removed.next = None

        return removed

    def remove_node(self, node):
        if node is None:
            return None

        if node == self.head:
            return self.remove_front()

        if node == self.tail:
            return self.remove_back()

        node.prev.next = node.next
        node.next.prev = node.prev

        node.prev = None
        node.next = None

        return node

    def move_to_front(self, node):
        if node is None:
            return

        if node == self.head:
            return

        if node == self.tail:
            self.tail = node.prev
            self.tail.next = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev

        node.prev = None
        node.next = self.head

        self.head.prev = node
        self.head = node
```

---

# 17. 테스트해 보기

다음처럼 직접 실행해 볼 수 있다.

```python
linked_list = DoublyLinkedList()

a = linked_list.insert_back("A")
b = linked_list.insert_back("B")
c = linked_list.insert_back("C")
```

현재:

```text
[A] ⇄ [B] ⇄ [C]
```

이제:

```python
linked_list.move_to_front(c)
```

를 실행한다.

결과:

```text
[C] ⇄ [A] ⇄ [B]
```

그리고:

```python
linked_list.remove_node(a)
```

를 실행하면:

```text
[C] ⇄ [B]
```

가 된다.

---

# 18. 출력 기능을 만들어 보면 이해하기 쉽다

학습 중에는 리스트의 상태를 눈으로 보는 것이 좋다.

```python
def print_forward(self):
    current = self.head

    while current is not None:
        print(current.data, end=" ")

        current = current.next

    print()
```

예:

```python
linked_list.print_forward()
```

결과:

```text
A B C
```

반대 방향도 가능하다.

```python
def print_backward(self):
    current = self.tail

    while current is not None:
        print(current.data, end=" ")

        current = current.prev

    print()
```

결과:

```text
C B A
```

이것이 이중 연결 리스트의 특징이다.

---

# 19. 시간 복잡도 정리

노드를 이미 알고 있다는 조건에서:

| 연산 | 시간복잡도 |
|---|---:|
| insert_front | O(1) |
| insert_back | O(1) |
| remove_front | O(1) |
| remove_back | O(1) |
| remove_node | O(1) |
| move_to_front | O(1) |
| 특정 값 검색 | O(N) |

여기서 중요한 점은:

```text
삭제 자체는 O(1)

하지만

삭제할 노드를 찾는 것은 O(N)
```

이라는 것이다.

이 차이를 이해하는 것이 중요하다.

---

# 20. 단일 연결 리스트와 차이

단일 연결 리스트는 보통 이렇게 생긴다.

```text
[A] → [B] → [C] → None
```

각 노드는 다음 노드만 알고 있다.

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
```

반면 이중 연결 리스트는:

```text
None ← [A] ⇄ [B] ⇄ [C] → None
```

이고:

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None
```

이다.

이중 연결 리스트는 메모리를 조금 더 사용하지만 이전 노드를 바로 알 수 있다.

그래서 노드 삭제나 이동 작업에 특히 편리하다.

---

# 21. 이중 연결 리스트를 LRU에 사용하는 이유

Mini Redis에서 이중 연결 리스트를 구현하는 가장 중요한 이유가 바로 LRU다.

LRU는:

```text
Least Recently Used
```

즉:

```text
가장 오래 사용되지 않은 데이터
```

를 찾아 제거하는 방식이다.

예를 들어 다음 데이터가 있다고 하자.

```text
가장 최근 사용                 가장 오래됨
     ↓                            ↓

[user:3] ⇄ [user:2] ⇄ [user:1]
```

여기서는:

```text
head = 가장 최근 사용
tail = 가장 오래 사용하지 않음
```

으로 관리할 수 있다.

---

# 22. GET과 LRU

현재:

```text
head                         tail
 ↓                             ↓

[C] ⇄ [B] ⇄ [A]
```

A가 가장 오래 사용되지 않았다.

그런데 사용자가:

```text
GET A
```

를 실행했다.

그러면 A는 방금 사용한 데이터다.

따라서:

```python
move_to_front(A)
```

를 수행한다.

결과:

```text
head                         tail
 ↓                             ↓

[A] ⇄ [C] ⇄ [B]
```

이제 B가 가장 오래 사용하지 않은 데이터가 된다.

---

# 23. 메모리가 부족하면?

Mini Redis의 메모리가 가득 찼다고 하자.

현재:

```text
[A] ⇄ [C] ⇄ [B]
               ↑
             tail
```

가장 오래 사용하지 않은 키는 B다.

따라서:

```python
remove_back()
```

을 하면 된다.

결과:

```text
[A] ⇄ [C]
```

이 과정 역시:

```text
O(1)
```

이다.

이것이 LRU에서 이중 연결 리스트를 사용하는 매우 중요한 이유다.

---

# 24. 그런데 연결 리스트만으로 LRU를 구현하면 문제가 있다

사용자가:

```text
GET user:1000
```

을 실행했다고 하자.

연결 리스트:

```text
[user:1] ⇄ [user:2] ⇄ ... ⇄ [user:1000]
```

연결 리스트만 사용한다면 `user:1000`이 어느 노드인지 찾아야 한다.

최악의 경우:

```text
O(N)
```

이 걸린다.

그래서 실제 LRU에서는 일반적으로:

```text
HashMap + Doubly Linked List
```

를 같이 사용한다.

---

# 25. HashMap과 연결 리스트를 함께 사용

구조는 다음과 같다.

```text
HashMap
─────────────────

"user:1" ───────────────┐
                        ↓
                     [user:1]

"user:2" ───────────────┐
                        ↓
                     [user:2]
```

각 값이 실제 연결 리스트의 Node를 가리킨다.

연결 리스트는:

```text
[user:3] ⇄ [user:1] ⇄ [user:2]
```

형태다.

사용자가:

```text
GET user:2
```

를 하면 먼저 HashMap으로 찾는다.

```text
"user:2"
   ↓
 Node
```

HashMap 조회를 평균적으로 O(1)이라고 하면 노드를 바로 얻을 수 있다.

그리고:

```python
move_to_front(node)
```

한다.

결과:

```text
[user:2] ⇄ [user:3] ⇄ [user:1]
```

따라서:

```text
HashMap 조회        O(1)
+
move_to_front      O(1)

= 전체 O(1)
```

이 가능해진다.

---

# 26. 내가 이중 연결 리스트를 설명한다면

다음 정도로 설명할 수 있으면 충분하다.

> 이중 연결 리스트는 각 노드가 자신의 데이터뿐 아니라 이전 노드와 다음 노드의 참조를 가지고 있는 자료구조입니다.
>
> 그래서 `[A] ⇄ [B] ⇄ [C]` 형태로 양방향 탐색이 가능합니다.
>
> 특히 삭제할 노드를 이미 알고 있다면 해당 노드의 `prev`와 `next` 연결만 수정하면 되기 때문에 O(1) 시간에 삭제할 수 있습니다.
>
> 같은 원리로 특정 노드를 리스트의 맨 앞으로 이동시키는 것도 O(1)에 처리할 수 있습니다.
>
> 이런 특성 때문에 최근 사용 순서를 계속 변경해야 하는 LRU Cache 구현에 많이 사용됩니다.
>
> 다만 연결 리스트만으로는 특정 키의 노드를 찾는 데 O(N)이 걸릴 수 있기 때문에, LRU에서는 일반적으로 HashMap과 이중 연결 리스트를 함께 사용합니다.
>
> HashMap을 이용해 Node를 O(1)에 찾고, 이중 연결 리스트를 이용해 해당 Node를 O(1)에 이동시키는 방식입니다.

---

# 27. 이중 연결 리스트에서 반드시 이해해야 할 핵심 5가지

### 1. Node

```text
prev | data | next
```

노드 하나가 이전 노드와 다음 노드를 알고 있다.

### 2. head와 tail

```text
head                     tail
 ↓                         ↓

[A] ⇄ [B] ⇄ [C] ⇄ [D]
```

리스트의 양 끝을 바로 접근하기 위해 사용한다.

### 3. 연결을 변경한다

연결 리스트의 핵심은 데이터를 실제로 옮기는 것이 아니라:

```text
누가 누구를 가리키는가
```

를 변경하는 것이다.

### 4. 노드를 알면 삭제와 이동이 O(1)

```text
node.prev
node.next
```

만 변경하면 된다.

### 5. LRU에서 매우 중요하다

```text
HashMap → Node 검색
Doubly Linked List → 사용 순서 관리
```

를 조합하여 빠른 LRU를 만들 수 있다.

---

# 28. 스스로 풀어볼 연습 문제

다음 문제를 직접 풀어보자.

## 문제 1

다음 연결 리스트가 있다.

```text
[A] ⇄ [B] ⇄ [C]
```

B를 삭제한 뒤:

```text
A.next
C.prev
```

는 각각 무엇을 가리켜야 하는가?

정답:

```text
A.next → C
C.prev → A
```

---

## 문제 2

현재:

```text
head
 ↓

[A] ⇄ [B] ⇄ [C]
```

C를 `move_to_front()` 하면 어떤 결과가 되는가?

정답:

```text
[C] ⇄ [A] ⇄ [B]
```

---

## 문제 3

연결 리스트에서 특정 값을 검색하는 시간복잡도는?

```text
O(N)
```

---

## 문제 4

삭제할 Node 객체를 이미 알고 있을 때 `remove_node()`의 시간복잡도는?

```text
O(1)
```

---

## 문제 5

LRU에서 연결 리스트만 사용하지 않고 HashMap을 같이 사용하는 이유는?

답:

> 연결 리스트만으로 특정 키의 Node를 찾으려면 O(N)이 필요하지만, HashMap을 사용하면 평균 O(1)에 Node를 찾을 수 있기 때문이다.

---

# 29. 학습 체크리스트

다음 질문에 코드 없이 대답할 수 있다면 이중 연결 리스트를 제대로 이해한 것이다.

- Node의 `prev`, `data`, `next`는 각각 무엇인가?
- `head`와 `tail`을 왜 가지고 있는가?
- 단일 연결 리스트와 이중 연결 리스트의 차이는 무엇인가?
- 노드를 이미 알고 있을 때 삭제가 O(1)인 이유는 무엇인가?
- 특정 데이터를 검색하는 것은 왜 O(N)인가?
- `move_to_front()`는 어떤 과정을 거치는가?
- LRU에서 왜 이중 연결 리스트를 사용하는가?
- LRU에서 왜 HashMap도 같이 필요한가?

이 질문들을 자신의 말로 설명할 수 있으면 다음 단계인 **HashMap**으로 넘어가도 된다.

---

# 30. 한 문장으로 정리

> 이중 연결 리스트는 각 노드가 이전 노드와 다음 노드를 모두 가리키는 자료구조이며, 노드를 이미 알고 있을 때 삽입·삭제·이동을 O(1)에 처리할 수 있어 LRU처럼 데이터 순서를 자주 변경해야 하는 문제에 적합하다.