"""가계부에서 사용하는 데이터 모델과 입력 검증 함수."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date, datetime
from typing import Any


class AppError(Exception):
    """사용자에게 원인과 해결 방법을 안내할 수 있는 오류."""

    def __init__(self, message: str, hint: str) -> None:
        super().__init__(message)
        self.message = message
        self.hint = hint


class ValidationError(AppError):
    """입력값이 도메인 규칙을 만족하지 않을 때 발생한다."""


def validate_date(value: str) -> str:
    try:
        return date.fromisoformat(value).isoformat()
    except (TypeError, ValueError) as error:
        raise ValidationError(
            "날짜 형식이 올바르지 않습니다 (YYYY-MM-DD).", "예: 2024-01-15"
        ) from error


def validate_month(value: str) -> str:
    try:
        return datetime.strptime(value, "%Y-%m").strftime("%Y-%m")
    except (TypeError, ValueError) as error:
        raise ValidationError(
            "월 형식이 올바르지 않습니다 (YYYY-MM).", "예: 2024-01"
        ) from error


def validate_type(value: str) -> str:
    if value not in {"income", "expense"}:
        raise ValidationError(
            "거래 타입은 income 또는 expense만 사용할 수 있습니다.",
            "income(수입) 또는 expense(지출)를 입력하세요.",
        )
    return value


def validate_amount(value: int | str) -> int:
    try:
        amount = int(value)
    except (TypeError, ValueError) as error:
        raise ValidationError("금액은 양의 정수여야 합니다.", "예: 15000") from error
    if amount <= 0:
        raise ValidationError("금액은 0보다 커야 합니다.", "1 이상의 정수를 입력하세요.")
    return amount


def normalize_tags(value: str | list[str] | None) -> list[str]:
    if value is None:
        return []
    raw_tags = value.split(",") if isinstance(value, str) else value
    return [tag.strip() for tag in raw_tags if tag.strip()]


@dataclass(frozen=True)
class Transaction:
    id: str
    date: str
    type: str
    amount: int
    category: str
    memo: str = ""
    tags: list[str] | None = None
    created_at: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "date", validate_date(self.date))
        object.__setattr__(self, "type", validate_type(self.type))
        object.__setattr__(self, "amount", validate_amount(self.amount))
        if not self.id.startswith("TX-"):
            raise ValidationError("거래 ID 형식이 올바르지 않습니다.", "TX-000001 형식을 사용하세요.")
        if not self.category.strip():
            raise ValidationError("카테고리를 입력해야 합니다.", "등록된 카테고리를 입력하세요.")
        object.__setattr__(self, "category", self.category.strip())
        object.__setattr__(self, "memo", self.memo.strip())
        object.__setattr__(self, "tags", normalize_tags(self.tags))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Transaction":
        return cls(
            id=str(value["id"]),
            date=str(value["date"]),
            type=str(value["type"]),
            amount=value["amount"],
            category=str(value["category"]),
            memo=str(value.get("memo", "")),
            tags=value.get("tags", []),
            created_at=str(value.get("created_at", "")),
        )


@dataclass(frozen=True)
class Budget:
    month: str
    amount: int

    def __post_init__(self) -> None:
        object.__setattr__(self, "month", validate_month(self.month))
        object.__setattr__(self, "amount", validate_amount(self.amount))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

