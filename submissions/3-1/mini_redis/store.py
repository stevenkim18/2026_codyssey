"""직접 구현한 자료구조를 조합한 메모리 기반 Mini Redis 엔진."""

import time
from typing import Callable, List, Optional, Tuple

from .hash_map import ChainedHashMap
from .linked_list import DoublyLinkedList, Node
from .min_heap import MinHeap


class CacheEntry:
    """하나의 문자열 키에 대한 데이터·LRU·TTL 메타데이터."""

    def __init__(self, key: str, value: str, memory_size: int) -> None:
        self.key = key
        self.value = value
        self.memory_size = memory_size
        self.lru_node = None  # type: Optional[Node]
        self.expire_at = None  # type: Optional[float]
        self.ttl_version = 0


class MiniRedis:
    """String, LRU 메모리 관리, TTL을 제공하는 작은 Redis 엔진."""

    _INTEGER_ERROR = "(error) ERR value is not an integer or out of range"
    _OOM_ERROR = "(error) OOM command not allowed when used_memory > 'maxmemory'"

    def __init__(self, clock: Optional[Callable[[], float]] = None) -> None:
        self._data = ChainedHashMap()
        self._lru = DoublyLinkedList()
        self._expiry_heap = MinHeap()
        self._clock = clock if clock is not None else time.monotonic
        self.used_memory = 0
        self.maxmemory = 0
        self.evicted_keys = 0

    def execute(self, raw_command: str, arguments: List[str]) -> str:
        """파싱된 명령을 실행하고 Redis 스타일 문자열 결과를 반환한다."""
        self._purge_expired()
        command = raw_command.upper()

        if command == "SET":
            if len(arguments) != 2:
                return self._wrong_argument_count(command)
            return self._set(arguments[0], arguments[1])
        if command == "GET":
            if len(arguments) != 1:
                return self._wrong_argument_count(command)
            return self._get(arguments[0])
        if command == "DEL":
            if len(arguments) != 1:
                return self._wrong_argument_count(command)
            return self._delete(arguments[0])
        if command == "EXISTS":
            if len(arguments) != 1:
                return self._wrong_argument_count(command)
            return self._exists(arguments[0])
        if command == "DBSIZE":
            if arguments:
                return self._wrong_argument_count(command)
            return self._dbsize()
        if command == "KEYS":
            if arguments:
                return self._wrong_argument_count(command)
            return self._keys()
        if command == "CONFIG":
            return self._config(arguments)
        if command == "INFO":
            return self._info(arguments)
        if command == "EXPIRE":
            if len(arguments) != 2:
                return self._wrong_argument_count(command)
            return self._expire(arguments[0], arguments[1])
        if command == "TTL":
            if len(arguments) != 1:
                return self._wrong_argument_count(command)
            return self._ttl(arguments[0])
        return "(error) ERR unknown command '{}'".format(raw_command)

    def _set(self, key: str, value: str) -> str:
        memory_size = self._entry_memory_size(key, value)
        if self.maxmemory > 0 and memory_size > self.maxmemory:
            return self._OOM_ERROR

        entry = self._live_entry(key)
        if entry is None:
            entry = CacheEntry(key, value, memory_size)
            entry.lru_node = self._lru.insert_front(entry)
            self._data.put(key, entry)
            self.used_memory += memory_size
        else:
            self.used_memory -= entry.memory_size
            entry.value = value
            entry.memory_size = memory_size
            self.used_memory += memory_size
            self._clear_ttl(entry)
            self._touch(entry)

        self._evict_until_within_limit()
        return "OK"

    def _get(self, key: str) -> str:
        entry = self._live_entry(key)
        if entry is None:
            return "(nil)"
        self._touch(entry)
        return '"{}"'.format(self._escape_output(entry.value))

    def _delete(self, key: str) -> str:
        entry = self._live_entry(key)
        if entry is None:
            return "(integer) 0"
        self._delete_key(key)
        return "(integer) 1"

    def _exists(self, key: str) -> str:
        return "(integer) {}".format(1 if self._live_entry(key) is not None else 0)

    def _dbsize(self) -> str:
        self._remove_entries_that_expired_between_commands()
        return "(integer) {}".format(self._data.size())

    def _keys(self) -> str:
        keys = []  # type: List[str]
        for key in self._data.keys():
            if self._live_entry(key) is not None:
                keys.append(key)
        if not keys:
            return "(empty array)"
        lines = []  # type: List[str]
        for index, key in enumerate(keys, start=1):
            lines.append('{}. "{}"'.format(index, self._escape_output(key)))
        return "\n".join(lines)

    def _config(self, arguments: List[str]) -> str:
        if len(arguments) != 3:
            return self._wrong_argument_count("CONFIG")
        if arguments[0].upper() != "SET" or arguments[1].lower() != "maxmemory":
            return "(error) ERR syntax error"
        try:
            maxmemory = int(arguments[2])
        except ValueError:
            return self._INTEGER_ERROR
        if maxmemory < 0:
            return self._INTEGER_ERROR
        self.maxmemory = maxmemory
        self._evict_until_within_limit()
        return "OK"

    def _info(self, arguments: List[str]) -> str:
        if len(arguments) != 1:
            return self._wrong_argument_count("INFO")
        if arguments[0].lower() != "memory":
            return "(error) ERR syntax error"
        self._remove_entries_that_expired_between_commands()
        return "\n".join([
            "used_memory:{}".format(self.used_memory),
            "maxmemory:{}".format(self.maxmemory),
            "evicted_keys:{}".format(self.evicted_keys),
        ])

    def _expire(self, key: str, raw_seconds: str) -> str:
        try:
            seconds = int(raw_seconds)
        except ValueError:
            return self._INTEGER_ERROR
        entry = self._live_entry(key)
        if entry is None:
            return "(integer) 0"
        if seconds <= 0:
            self._delete_key(key)
            return "(integer) 1"

        entry.ttl_version += 1
        entry.expire_at = self._clock() + seconds
        self._expiry_heap.push((entry.expire_at, key, entry.ttl_version))
        return "(integer) 1"

    def _ttl(self, key: str) -> str:
        entry = self._live_entry(key)
        if entry is None:
            return "(integer) -2"
        if entry.expire_at is None:
            return "(integer) -1"
        remaining = entry.expire_at - self._clock()
        if remaining <= 0:
            self._delete_key(key)
            return "(integer) -2"
        return "(integer) {}".format(int(remaining))

    def _live_entry(self, key: str) -> Optional[CacheEntry]:
        """키의 만료를 한 번 더 확인한 뒤 살아 있는 엔트리만 반환한다."""
        entry = self._data.get(key)
        if entry is None:
            return None
        if entry.expire_at is not None and entry.expire_at <= self._clock():
            self._delete_key(key)
            return None
        return entry

    def _purge_expired(self) -> None:
        """힙의 최솟값부터 현재 시각보다 이른 TTL을 모두 정리한다."""
        now = self._clock()
        while True:
            ticket = self._expiry_heap.peek()
            if ticket is None or ticket[0] > now:
                return
            self._expiry_heap.pop()
            expire_at, key, version = ticket  # type: Tuple[float, str, int]
            entry = self._data.get(key)
            if entry is None:
                continue
            if entry.ttl_version == version and entry.expire_at is not None and entry.expire_at <= now:
                self._delete_key(key)

    def _remove_entries_that_expired_between_commands(self) -> None:
        """명령 시작 직후와 응답 생성 사이의 미세한 시간차를 보정한다."""
        self._purge_expired()
        for key in self._data.keys():
            self._live_entry(key)

    def _delete_key(self, key: str, evicted: bool = False) -> bool:
        """데이터, LRU, TTL 상태와 메모리 카운터를 함께 정리한다."""
        entry = self._data.remove(key)
        if entry is None:
            return False
        if entry.lru_node is not None:
            self._lru.remove_node(entry.lru_node)
            entry.lru_node = None
        entry.ttl_version += 1
        entry.expire_at = None
        self.used_memory -= entry.memory_size
        if evicted:
            self.evicted_keys += 1
        return True

    def _clear_ttl(self, entry: CacheEntry) -> None:
        """기존 TTL을 무효화해 이후 힙에서 lazy deletion 되게 한다."""
        entry.ttl_version += 1
        entry.expire_at = None

    def _touch(self, entry: CacheEntry) -> None:
        if entry.lru_node is None:
            raise RuntimeError("LRU 노드가 없는 캐시 엔트리입니다.")
        self._lru.move_to_front(entry.lru_node)

    def _evict_until_within_limit(self) -> None:
        while self.maxmemory > 0 and self.used_memory > self.maxmemory:
            lru_node = self._lru.last_node()
            if lru_node is None:
                return
            entry = lru_node.data
            self._delete_key(entry.key, evicted=True)

    @staticmethod
    def _entry_memory_size(key: str, value: str) -> int:
        return len(key.encode("utf-8")) + len(value.encode("utf-8"))

    @staticmethod
    def _escape_output(value: str) -> str:
        return value.replace("\\", "\\\\").replace('"', '\\"')

    @staticmethod
    def _wrong_argument_count(command: str) -> str:
        return "(error) ERR wrong number of arguments for '{}' command".format(command)
