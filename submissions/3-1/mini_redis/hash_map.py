"""체이닝 방식으로 충돌을 처리하는 직접 구현 해시맵."""

from typing import Any, List, Optional

from .linked_list import DoublyLinkedList, Node


class HashMapEntry:
    """해시 버킷의 연결 리스트에 저장되는 키-값 엔트리."""

    __slots__ = ("key", "value")

    def __init__(self, key: str, value: Any) -> None:
        self.key = key
        self.value = value


class ChainedHashMap:
    """이중 연결 리스트 버킷을 사용하는 문자열 키 해시맵.

    Python의 ``list``는 버킷 테이블이라는 인덱스 접근용 저장소로만 사용한다.
    키 조회와 충돌 해결은 이 클래스의 해시 함수와 체이닝 로직이 맡는다.
    """

    _MIN_CAPACITY = 8

    def __init__(self, initial_capacity: int = _MIN_CAPACITY) -> None:
        if initial_capacity < self._MIN_CAPACITY:
            initial_capacity = self._MIN_CAPACITY
        self._buckets = self._new_buckets(initial_capacity)  # type: List[DoublyLinkedList]
        self._size = 0

    def put(self, key: str, value: Any) -> Optional[Any]:
        """키를 저장하고, 기존 값이 있었다면 그 값을 반환한다."""
        node = self._find_node(key)
        if node is not None:
            entry = node.data
            old_value = entry.value
            entry.value = value
            return old_value

        bucket = self._buckets[self._bucket_index(key)]
        bucket.insert_back(HashMapEntry(key, value))
        self._size += 1
        if self._size * 4 > len(self._buckets) * 3:
            self._resize(len(self._buckets) * 2)
        return None

    def get(self, key: str) -> Optional[Any]:
        """키의 값을 반환한다. 키가 없으면 ``None``을 반환한다."""
        node = self._find_node(key)
        if node is None:
            return None
        return node.data.value

    def remove(self, key: str) -> Optional[Any]:
        """키를 삭제하고 값을 반환한다. 키가 없으면 ``None``을 반환한다."""
        bucket = self._buckets[self._bucket_index(key)]
        for node in bucket.iter_nodes():
            entry = node.data
            if entry.key == key:
                bucket.remove_node(node)
                self._size -= 1
                return entry.value
        return None

    def contains(self, key: str) -> bool:
        """키가 존재하는지 반환한다."""
        return self._find_node(key) is not None

    def keys(self) -> List[str]:
        """저장된 모든 키를 버킷 순서로 반환한다."""
        result = []  # type: List[str]
        for bucket in self._buckets:
            for node in bucket.iter_nodes():
                result.append(node.data.key)
        return result

    def size(self) -> int:
        """현재 엔트리 수를 반환한다."""
        return self._size

    @staticmethod
    def _hash_key(key: str) -> int:
        """UTF-8 바이트를 이용한 결정적 DJB2 계열 해시 함수."""
        hash_value = 5381
        for byte in key.encode("utf-8"):
            hash_value = ((hash_value << 5) + hash_value) ^ byte
            hash_value &= 0xFFFFFFFFFFFFFFFF
        return hash_value

    def _bucket_index(self, key: str) -> int:
        return self._hash_key(key) % len(self._buckets)

    def _find_node(self, key: str) -> Optional[Node]:
        bucket = self._buckets[self._bucket_index(key)]
        for node in bucket.iter_nodes():
            if node.data.key == key:
                return node
        return None

    @staticmethod
    def _new_buckets(capacity: int) -> List[DoublyLinkedList]:
        return [DoublyLinkedList() for _ in range(capacity)]

    def _resize(self, new_capacity: int) -> None:
        """버킷 수를 두 배로 늘리고 모든 엔트리를 새 버킷에 재배치한다."""
        old_buckets = self._buckets
        self._buckets = self._new_buckets(new_capacity)
        for bucket in old_buckets:
            for node in bucket.iter_nodes():
                entry = node.data
                self._buckets[self._bucket_index(entry.key)].insert_back(entry)
