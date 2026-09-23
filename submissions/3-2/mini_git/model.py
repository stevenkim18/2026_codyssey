"""Mini Git에서 사용하는 커밋 모델."""

from dataclasses import dataclass
from datetime import datetime
from typing import Tuple


@dataclass(frozen=True)
class Commit:
    """커밋 하나의 메타데이터와 부모 연결을 나타낸다."""

    hash: str
    message: str
    author: str
    timestamp: datetime
    parents: Tuple[str, ...]
    sequence: int
