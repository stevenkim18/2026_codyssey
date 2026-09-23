"""Mini Git의 정렬과 그래프 탐색 알고리즘."""

from collections import deque
from typing import Callable, Dict, Iterable, List, Optional, Set, TypeVar

from .model import Commit


T = TypeVar("T")


def merge_sort(items: Iterable[T], key: Callable[[T], object]) -> List[T]:
    """표준 정렬 API 없이 새 리스트를 반환하는 안정 병합 정렬이다."""
    values = list(items)
    if len(values) <= 1:
        return values

    middle = len(values) // 2
    left = merge_sort(values[:middle], key)
    right = merge_sort(values[middle:], key)
    return _merge(left, right, key)


def _merge(left: List[T], right: List[T], key: Callable[[T], object]) -> List[T]:
    """동일한 키에서는 왼쪽 원소를 먼저 골라 안정성을 유지한다."""
    result = []  # type: List[T]
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        if key(left[left_index]) <= key(right[right_index]):
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1

    result.extend(left[left_index:])
    result.extend(right[right_index:])
    return result


def topological_order(
    commits: Dict[str, Commit],
    children: Dict[str, List[str]],
    included: Optional[Set[str]] = None,
) -> List[Commit]:
    """부모가 자식보다 먼저 나오도록 Kahn 방식으로 커밋을 나열한다."""
    selected = set(commits) if included is None else set(included)
    indegree = {}  # type: Dict[str, int]
    ready = []  # type: List[str]

    for commit_hash in selected:
        commit = commits[commit_hash]
        indegree[commit_hash] = sum(1 for parent in commit.parents if parent in selected)
        if indegree[commit_hash] == 0:
            ready.append(commit_hash)

    result = []  # type: List[Commit]
    while ready:
        ready_index = _earliest_sequence_index(ready, commits)
        current_hash = ready.pop(ready_index)
        result.append(commits[current_hash])

        for child_hash in children.get(current_hash, []):
            if child_hash not in selected:
                continue
            indegree[child_hash] -= 1
            if indegree[child_hash] == 0:
                ready.append(child_hash)

    if len(result) != len(selected):
        raise ValueError("Commit graph contains a cycle")
    return result


def _earliest_sequence_index(hashes: List[str], commits: Dict[str, Commit]) -> int:
    """준비 목록에서 생성 순서가 가장 빠른 원소의 위치를 찾는다."""
    earliest = 0
    for index in range(1, len(hashes)):
        if commits[hashes[index]].sequence < commits[hashes[earliest]].sequence:
            earliest = index
    return earliest


def collect_ancestors(start_hash: str, commits: Dict[str, Commit]) -> Set[str]:
    """주어진 커밋에서 부모 방향으로 도달 가능한 모든 hash를 반환한다."""
    ancestors = set()  # type: Set[str]
    pending = list(commits[start_hash].parents)

    while pending:
        current_hash = pending.pop()
        if current_hash in ancestors:
            continue
        ancestors.add(current_hash)
        pending.extend(commits[current_hash].parents)
    return ancestors


def shortest_path(
    start_hash: str,
    end_hash: str,
    commits: Dict[str, Commit],
    children: Dict[str, List[str]],
) -> Optional[List[str]]:
    """무방향 최단 경로 중 hash 문자열 기준 사전순 최소 경로를 반환한다."""
    if start_hash == end_hash:
        return [start_hash]

    distance_to_end = _breadth_first_distances(end_hash, commits, children)
    if start_hash not in distance_to_end:
        return None

    path = [start_hash]
    current_hash = start_hash
    while current_hash != end_hash:
        next_hash = None  # type: Optional[str]
        target_distance = distance_to_end[current_hash] - 1
        for neighbor in _neighbors(current_hash, commits, children):
            if distance_to_end.get(neighbor) != target_distance:
                continue
            if next_hash is None or neighbor < next_hash:
                next_hash = neighbor
        if next_hash is None:
            return None
        path.append(next_hash)
        current_hash = next_hash
    return path


def _breadth_first_distances(
    start_hash: str,
    commits: Dict[str, Commit],
    children: Dict[str, List[str]],
) -> Dict[str, int]:
    """시작 커밋에서 각 커밋까지의 무방향 최단거리를 BFS로 계산한다."""
    distances = {start_hash: 0}
    pending = deque([start_hash])

    while pending:
        current_hash = pending.popleft()
        for neighbor in _neighbors(current_hash, commits, children):
            if neighbor in distances:
                continue
            distances[neighbor] = distances[current_hash] + 1
            pending.append(neighbor)
    return distances


def _neighbors(
    commit_hash: str,
    commits: Dict[str, Commit],
    children: Dict[str, List[str]],
) -> Iterable[str]:
    """부모와 자식을 합쳐 무방향 그래프의 이웃을 만든다."""
    for parent_hash in commits[commit_hash].parents:
        yield parent_hash
    for child_hash in children.get(commit_hash, []):
        yield child_hash
