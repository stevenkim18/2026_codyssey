"""LRU와 해시 충돌 체이닝에 사용하는 이중 연결 리스트."""

from typing import Any, Iterator, Optional


class Node:
    """이중 연결 리스트의 노드.

    ``prev``, ``next``, ``data``를 직접 보관해 노드를 알고 있을 때는
    탐색 없이 O(1)로 삭제하거나 위치를 옮길 수 있다.
    """

    def __init__(self, data: Any = None) -> None:
        self.prev = None  # type: Optional[Node]
        self.next = None  # type: Optional[Node]
        self.data = data


class DoublyLinkedList:
    """앞뒤 센티널 노드를 사용하는 이중 연결 리스트."""

    def __init__(self) -> None:
        self._head = Node()
        self._tail = Node()
        self._head.next = self._tail
        self._tail.prev = self._head
        self._size = 0

    def insert_front(self, data: Any) -> Node:
        """새 데이터를 맨 앞에 넣고 생성된 노드를 반환한다."""
        node = Node(data)
        self._insert_after(self._head, node)
        self._size += 1
        return node

    def insert_back(self, data: Any) -> Node:
        """새 데이터를 맨 뒤에 넣고 생성된 노드를 반환한다."""
        node = Node(data)
        previous = self._tail.prev
        if previous is None:
            raise RuntimeError("연결 리스트의 센티널 연결이 손상되었습니다.")
        self._insert_after(previous, node)
        self._size += 1
        return node

    def remove_front(self) -> Optional[Any]:
        """맨 앞 데이터를 제거해 반환한다. 비어 있으면 ``None``을 반환한다."""
        node = self.first_node()
        if node is None:
            return None
        return self.remove_node(node)

    def remove_back(self) -> Optional[Any]:
        """맨 뒤 데이터를 제거해 반환한다. 비어 있으면 ``None``을 반환한다."""
        node = self.last_node()
        if node is None:
            return None
        return self.remove_node(node)

    def remove_node(self, node: Node) -> Any:
        """주어진 연결된 노드를 O(1)에 제거하고 그 데이터를 반환한다."""
        self._validate_attached_node(node)
        self._detach(node, clear_links=True)
        self._size -= 1
        return node.data

    def move_to_front(self, node: Node) -> None:
        """주어진 연결된 노드를 O(1)에 맨 앞으로 옮긴다."""
        self._validate_attached_node(node)
        if node.prev is self._head:
            return
        self._detach(node, clear_links=False)
        self._insert_after(self._head, node)

    def first_node(self) -> Optional[Node]:
        """첫 번째 실제 노드를 반환한다. 비어 있으면 ``None``이다."""
        node = self._head.next
        if node is self._tail:
            return None
        return node

    def last_node(self) -> Optional[Node]:
        """마지막 실제 노드를 반환한다. 비어 있으면 ``None``이다."""
        node = self._tail.prev
        if node is self._head:
            return None
        return node

    def iter_nodes(self) -> Iterator[Node]:
        """앞에서 뒤 순서로 실제 노드를 순회한다."""
        node = self._head.next
        while node is not None and node is not self._tail:
            yield node
            node = node.next

    def size(self) -> int:
        """현재 실제 노드 수를 반환한다."""
        return self._size

    def is_empty(self) -> bool:
        """리스트가 비어 있는지 반환한다."""
        return self._size == 0

    def _insert_after(self, previous: Node, node: Node) -> None:
        following = previous.next
        if following is None:
            raise RuntimeError("연결 리스트의 센티널 연결이 손상되었습니다.")
        node.prev = previous
        node.next = following
        previous.next = node
        following.prev = node

    def _detach(self, node: Node, clear_links: bool) -> None:
        previous = node.prev
        following = node.next
        if previous is None or following is None:
            raise ValueError("연결되지 않은 노드는 제거할 수 없습니다.")
        previous.next = following
        following.prev = previous
        if clear_links:
            node.prev = None
            node.next = None

    def _validate_attached_node(self, node: Node) -> None:
        if node is self._head or node is self._tail or node.prev is None or node.next is None:
            raise ValueError("연결 리스트에 포함된 실제 노드가 필요합니다.")
