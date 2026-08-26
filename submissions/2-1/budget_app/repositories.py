"""JSONL 파일을 스트리밍 방식으로 읽고 안전하게 쓰는 저장소 계층."""

from __future__ import annotations

import json
import os
import tempfile
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

from .models import Budget, Transaction


DEFAULT_CATEGORIES = ("food", "transport", "rent", "salary", "etc")


class JsonlStore:
    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def path(self, filename: str) -> Path:
        file_path = self.data_dir / filename
        file_path.touch(exist_ok=True)
        return file_path

    def iter_records(self, filename: str) -> Iterator[dict[str, Any]]:
        with self.path(filename).open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    yield json.loads(line)

    def iter_records_reverse(self, filename: str) -> Iterator[dict[str, Any]]:
        """파일 끝에서부터 블록 단위로 읽어 메모리 사용량을 일정하게 유지한다."""
        file_path = self.path(filename)
        with file_path.open("rb") as file:
            position = file.seek(0, os.SEEK_END)
            remainder = b""
            while position > 0:
                size = min(4096, position)
                position -= size
                file.seek(position)
                chunk = file.read(size) + remainder
                lines = chunk.split(b"\n")
                remainder = lines[0]
                for line in reversed(lines[1:]):
                    if line.strip():
                        yield json.loads(line.decode("utf-8"))
            if remainder.strip():
                yield json.loads(remainder.decode("utf-8"))

    def append(self, filename: str, record: dict[str, Any]) -> None:
        with self.path(filename).open("a", encoding="utf-8") as file:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")

    def rewrite(self, filename: str, records: Iterator[dict[str, Any]]) -> None:
        target = self.path(filename)
        temp_name: str | None = None
        try:
            with tempfile.NamedTemporaryFile(
                "w", encoding="utf-8", dir=self.data_dir, delete=False
            ) as temp_file:
                temp_name = temp_file.name
                for record in records:
                    temp_file.write(json.dumps(record, ensure_ascii=False) + "\n")
            os.replace(temp_name, target)
        finally:
            if temp_name and os.path.exists(temp_name):
                os.unlink(temp_name)


class TransactionRepository:
    FILENAME = "transactions.jsonl"

    def __init__(self, store: JsonlStore) -> None:
        self.store = store
        self.store.path(self.FILENAME)

    def iter_all(self) -> Iterator[Transaction]:
        for record in self.store.iter_records(self.FILENAME):
            yield Transaction.from_dict(record)

    def iter_recent(self) -> Iterator[Transaction]:
        for record in self.store.iter_records_reverse(self.FILENAME):
            yield Transaction.from_dict(record)

    def append(self, transaction: Transaction) -> None:
        self.store.append(self.FILENAME, transaction.to_dict())

    def next_id(self) -> str:
        highest = 0
        for transaction in self.iter_all():
            try:
                highest = max(highest, int(transaction.id.removeprefix("TX-")))
            except ValueError:
                continue
        return f"TX-{highest + 1:06d}"

    def replace(self, transaction_id: str, updater: Callable[[Transaction], Transaction]) -> bool:
        found = False

        def records() -> Iterator[dict[str, Any]]:
            nonlocal found
            for transaction in self.iter_all():
                if transaction.id == transaction_id:
                    found = True
                    yield updater(transaction).to_dict()
                else:
                    yield transaction.to_dict()

        self.store.rewrite(self.FILENAME, records())
        return found

    def delete(self, transaction_id: str) -> bool:
        found = False

        def records() -> Iterator[dict[str, Any]]:
            nonlocal found
            for transaction in self.iter_all():
                if transaction.id == transaction_id:
                    found = True
                    continue
                yield transaction.to_dict()

        self.store.rewrite(self.FILENAME, records())
        return found


class CategoryRepository:
    FILENAME = "categories.jsonl"

    def __init__(self, store: JsonlStore) -> None:
        self.store = store
        if not any(store.iter_records(self.FILENAME)):
            for name in DEFAULT_CATEGORIES:
                store.append(self.FILENAME, {"name": name})

    def list(self) -> list[str]:
        return sorted({str(record["name"]) for record in self.store.iter_records(self.FILENAME)})

    def contains(self, name: str) -> bool:
        return name in self.list()

    def add(self, name: str) -> None:
        self.store.append(self.FILENAME, {"name": name})

    def remove(self, name: str) -> bool:
        found = False

        def records() -> Iterator[dict[str, Any]]:
            nonlocal found
            for record in self.store.iter_records(self.FILENAME):
                if record.get("name") == name:
                    found = True
                    continue
                yield record

        self.store.rewrite(self.FILENAME, records())
        return found


class BudgetRepository:
    FILENAME = "budgets.jsonl"

    def __init__(self, store: JsonlStore) -> None:
        self.store = store
        self.store.path(self.FILENAME)

    def get(self, month: str) -> Budget | None:
        for record in self.store.iter_records_reverse(self.FILENAME):
            budget = Budget(month=str(record["month"]), amount=record["amount"])
            if budget.month == month:
                return budget
        return None

    def set(self, budget: Budget) -> None:
        def records() -> Iterator[dict[str, Any]]:
            for record in self.store.iter_records(self.FILENAME):
                if record.get("month") != budget.month:
                    yield record
            yield budget.to_dict()

        self.store.rewrite(self.FILENAME, records())
