"""가계부 도메인 규칙과 유스케이스를 구현하는 서비스 계층."""

from __future__ import annotations

import csv
from calendar import monthrange
from collections import Counter
from collections.abc import Iterator
from datetime import datetime
from pathlib import Path

from .models import AppError, Budget, Transaction, normalize_tags, validate_amount, validate_date, validate_month, validate_type
from .repositories import BudgetRepository, CategoryRepository, JsonlStore, TransactionRepository


class BudgetService:
    def __init__(self, data_dir: str | Path) -> None:
        store = JsonlStore(Path(data_dir))
        self.transactions = TransactionRepository(store)
        self.categories = CategoryRepository(store)
        self.budgets = BudgetRepository(store)

    def _validate_category(self, category: str) -> str:
        cleaned = category.strip()
        if not self.categories.contains(cleaned):
            raise AppError(
                f"등록되지 않은 카테고리입니다: {cleaned}",
                "category list로 목록을 확인하거나 category add로 먼저 등록하세요.",
            )
        return cleaned

    def add_transaction(
        self, *, date: str, transaction_type: str, category: str, amount: int | str,
        memo: str = "", tags: str | list[str] | None = None,
    ) -> Transaction:
        transaction = Transaction(
            id=self.transactions.next_id(), date=validate_date(date), type=validate_type(transaction_type),
            category=self._validate_category(category), amount=validate_amount(amount), memo=memo,
            tags=normalize_tags(tags), created_at=datetime.now().isoformat(timespec="seconds"),
        )
        self.transactions.append(transaction)
        return transaction

    def list_transactions(self, limit: int = 20) -> Iterator[Transaction]:
        if limit <= 0:
            raise AppError("limit은 1 이상이어야 합니다.", "예: --limit 20")
        for index, transaction in enumerate(self.transactions.iter_recent()):
            if index >= limit:
                break
            yield transaction

    def search(
        self, *, from_date: str | None = None, to_date: str | None = None,
        category: str | None = None, transaction_type: str | None = None,
        query: str | None = None, tag: str | None = None,
    ) -> Iterator[Transaction]:
        if from_date:
            from_date = validate_date(from_date)
        if to_date:
            to_date = validate_date(to_date)
        if from_date and to_date and from_date > to_date:
            raise AppError("시작일이 종료일보다 늦습니다.", "--from과 --to를 다시 확인하세요.")
        if transaction_type:
            transaction_type = validate_type(transaction_type)
        query = query.lower() if query else None
        tag = tag.strip() if tag else None
        for transaction in self.transactions.iter_recent():
            if from_date and transaction.date < from_date:
                continue
            if to_date and transaction.date > to_date:
                continue
            if category and transaction.category != category:
                continue
            if transaction_type and transaction.type != transaction_type:
                continue
            if query and query not in transaction.memo.lower():
                continue
            if tag and tag not in transaction.tags:
                continue
            yield transaction

    def update_transaction(self, transaction_id: str, **changes: object) -> None:
        if not changes:
            raise AppError("수정할 항목을 하나 이상 지정해야 합니다.", "예: --amount 15000")
        if "date" in changes:
            changes["date"] = validate_date(str(changes["date"]))
        if "transaction_type" in changes:
            changes["type"] = validate_type(str(changes.pop("transaction_type")))
        if "category" in changes:
            changes["category"] = self._validate_category(str(changes["category"]))
        if "amount" in changes:
            changes["amount"] = validate_amount(changes["amount"])  # type: ignore[arg-type]
        if "tags" in changes:
            changes["tags"] = normalize_tags(changes["tags"])  # type: ignore[arg-type]

        def updater(transaction: Transaction) -> Transaction:
            values = transaction.to_dict()
            values.update(changes)
            return Transaction.from_dict(values)

        if not self.transactions.replace(transaction_id, updater):
            raise AppError(f"거래를 찾을 수 없습니다: {transaction_id}", "id를 다시 확인하세요.")

    def delete_transaction(self, transaction_id: str) -> None:
        if not self.transactions.delete(transaction_id):
            raise AppError(f"거래를 찾을 수 없습니다: {transaction_id}", "id를 다시 확인하세요.")

    def summary(self, month: str, top: int = 5) -> dict[str, object]:
        month = validate_month(month)
        if top <= 0:
            raise AppError("top은 1 이상이어야 합니다.", "예: --top 3")
        income = expense = 0
        expenses_by_category: Counter[str] = Counter()
        count = 0
        for transaction in self.transactions.iter_all():
            if not transaction.date.startswith(month):
                continue
            count += 1
            if transaction.type == "income":
                income += transaction.amount
            else:
                expense += transaction.amount
                expenses_by_category[transaction.category] += transaction.amount
        budget = self.budgets.get(month)
        return {
            "month": month, "count": count, "income": income, "expense": expense,
            "balance": income - expense, "top_expenses": expenses_by_category.most_common(top),
            "budget": budget,
        }

    def set_budget(self, month: str, amount: int | str) -> Budget:
        budget = Budget(month=month, amount=amount)
        self.budgets.set(budget)
        return budget

    def add_category(self, name: str) -> str:
        cleaned = name.strip()
        if not cleaned:
            raise AppError("카테고리명을 입력해야 합니다.", "예: food")
        if self.categories.contains(cleaned):
            raise AppError(f"이미 등록된 카테고리입니다: {cleaned}", "다른 이름을 입력하세요.")
        self.categories.add(cleaned)
        return cleaned

    def list_categories(self) -> list[str]:
        return self.categories.list()

    def remove_category(self, name: str) -> None:
        name = name.strip()
        usage = sum(1 for transaction in self.transactions.iter_all() if transaction.category == name)
        if usage:
            raise AppError(
                f"사용 중인 카테고리는 삭제할 수 없습니다: {name} ({usage}건)",
                "해당 거래를 수정 또는 삭제한 뒤 다시 시도하세요.",
            )
        if not self.categories.remove(name):
            raise AppError(f"카테고리를 찾을 수 없습니다: {name}", "category list로 목록을 확인하세요.")

    def import_csv(self, source: str | Path) -> tuple[int, int, dict[str, int]]:
        source_path = Path(source)
        if not source_path.is_file():
            raise AppError(f"가져올 파일을 찾을 수 없습니다: {source_path}", "--from 경로를 확인하세요.")
        imported = skipped = 0
        reasons: Counter[str] = Counter()
        required = {"date", "type", "category", "amount"}
        with source_path.open("r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            if not reader.fieldnames or not required.issubset(reader.fieldnames):
                raise AppError("CSV 헤더에 필수 열이 없습니다.", "date, type, category, amount 헤더를 포함하세요.")
            for row in reader:
                try:
                    self.add_transaction(
                        date=row.get("date", ""), transaction_type=row.get("type", ""),
                        category=row.get("category", ""), amount=row.get("amount", ""),
                        memo=row.get("memo", ""), tags=row.get("tags", ""),
                    )
                    imported += 1
                except AppError as error:
                    skipped += 1
                    reasons[error.message] += 1
        return imported, skipped, dict(reasons)

    def export_csv(
        self, output: str | Path, *, month: str | None = None,
        from_date: str | None = None, to_date: str | None = None,
    ) -> int:
        if bool(month) == bool(from_date or to_date):
            raise AppError(
                "month 또는 from/to 기간 조건 중 하나를 지정해야 합니다.",
                "예: --month 2024-01 또는 --from 2024-01-01 --to 2024-01-31",
            )
        if month:
            month = validate_month(month)
            year, month_number = (int(part) for part in month.split("-"))
            from_date = f"{month}-01"
            to_date = f"{month}-{monthrange(year, month_number)[1]:02d}"
        if not from_date or not to_date:
            raise AppError("from과 to를 함께 지정해야 합니다.", "두 날짜를 모두 입력하세요.")
        from_date, to_date = validate_date(from_date), validate_date(to_date)
        if from_date > to_date:
            raise AppError("시작일이 종료일보다 늦습니다.", "기간을 다시 확인하세요.")
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        count = 0
        with output_path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["date", "type", "category", "amount", "memo", "tags"])
            writer.writeheader()
            for transaction in self.search(from_date=from_date, to_date=to_date):
                writer.writerow({
                    "date": transaction.date, "type": transaction.type, "category": transaction.category,
                    "amount": transaction.amount, "memo": transaction.memo, "tags": ",".join(transaction.tags),
                })
                count += 1
        return count
