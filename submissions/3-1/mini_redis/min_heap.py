"""TTL 만료 시각을 빠르게 찾기 위한 배열 기반 최소 힙."""

from typing import Any, List, Optional


class MinHeap:
    """비교 가능한 요소를 저장하는 최소 힙.

    TTL 엔진은 ``(expire_at, key, version)`` 튜플을 넣어 가장 이른 만료
    시각을 ``peek``으로 O(1)에 확인하고 삽입·삭제를 O(log n)에 수행한다.
    """

    def __init__(self) -> None:
        self._items = []  # type: List[Any]

    def push(self, item: Any) -> None:
        """요소를 넣고 힙 속성을 복구한다."""
        self._items.append(item)
        self._heapify_up(len(self._items) - 1)

    def pop(self) -> Optional[Any]:
        """최솟값을 제거해 반환한다. 비어 있으면 ``None``을 반환한다."""
        if not self._items:
            return None
        minimum = self._items[0]
        last_item = self._items.pop()
        if self._items:
            self._items[0] = last_item
            self._heapify_down(0)
        return minimum

    def peek(self) -> Optional[Any]:
        """최솟값을 제거하지 않고 반환한다. 비어 있으면 ``None``이다."""
        if not self._items:
            return None
        return self._items[0]

    def size(self) -> int:
        """현재 요소 수를 반환한다."""
        return len(self._items)

    def _heapify_up(self, index: int) -> None:
        while index > 0:
            parent = (index - 1) // 2
            if self._items[parent] <= self._items[index]:
                return
            self._items[parent], self._items[index] = self._items[index], self._items[parent]
            index = parent

    def _heapify_down(self, index: int) -> None:
        size = len(self._items)
        while True:
            smallest = index
            left = index * 2 + 1
            right = index * 2 + 2
            if left < size and self._items[left] < self._items[smallest]:
                smallest = left
            if right < size and self._items[right] < self._items[smallest]:
                smallest = right
            if smallest == index:
                return
            self._items[index], self._items[smallest] = self._items[smallest], self._items[index]
            index = smallest
