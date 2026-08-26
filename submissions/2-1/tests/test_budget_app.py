from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from budget_app.models import AppError, ValidationError
from budget_app.services import BudgetService


class BudgetServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_dir = Path(self.temp_dir.name) / "data"
        self.service = BudgetService(self.data_dir)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def add(self, **overrides: object):
        values: dict[str, object] = {
            "date": "2024-01-15", "transaction_type": "expense", "category": "food", "amount": 15000,
        }
        values.update(overrides)
        return self.service.add_transaction(**values)  # type: ignore[arg-type]

    def test_initial_files_and_categories_are_created(self) -> None:
        self.assertEqual(self.service.list_categories(), ["etc", "food", "rent", "salary", "transport"])
        for filename in ("transactions.jsonl", "categories.jsonl", "budgets.jsonl"):
            self.assertTrue((self.data_dir / filename).exists())

    def test_transaction_validation(self) -> None:
        with self.assertRaises(ValidationError):
            self.add(date="2024-99-01")
        with self.assertRaises(ValidationError):
            self.add(amount=0)
        with self.assertRaises(ValidationError):
            self.add(transaction_type="saving")
        with self.assertRaises(AppError):
            self.add(category="unknown")

    def test_crud_and_recent_stream_order(self) -> None:
        first = self.add(memo="first")
        second = self.add(memo="second", amount=20000)
        self.assertEqual([item.id for item in self.service.list_transactions(1)], [second.id])
        self.service.update_transaction(first.id, amount=30000, tags="meal, lunch")
        updated = next(item for item in self.service.list_transactions(5) if item.id == first.id)
        self.assertEqual((updated.amount, updated.tags), (30000, ["meal", "lunch"]))
        self.service.delete_transaction(second.id)
        self.assertEqual([item.id for item in self.service.list_transactions(5)], [first.id])
        with self.assertRaises(AppError):
            self.service.delete_transaction("TX-999999")

    def test_search_summary_budget_and_category_removal(self) -> None:
        self.add(memo="lunch", tags="meal")
        self.add(date="2024-01-20", transaction_type="income", category="salary", amount=3000000)
        self.add(date="2024-02-01", category="transport", amount=5000, memo="bus")
        found = list(self.service.search(from_date="2024-01-01", to_date="2024-01-31", tag="meal"))
        self.assertEqual(len(found), 1)
        self.service.set_budget("2024-01", 10000)
        summary = self.service.summary("2024-01", 3)
        self.assertEqual((summary["income"], summary["expense"], summary["balance"]), (3000000, 15000, 2985000))
        self.assertEqual(summary["budget"].amount, 10000)  # type: ignore[union-attr]
        with self.assertRaises(AppError):
            self.service.remove_category("food")

    def test_import_skips_invalid_rows_and_export_writes_schema(self) -> None:
        source = Path(self.temp_dir.name) / "import.csv"
        with source.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["date", "type", "category", "amount", "memo", "tags"])
            writer.writeheader()
            writer.writerow({"date": "2024-01-01", "type": "expense", "category": "food", "amount": "1000", "memo": "ok", "tags": "meal"})
            writer.writerow({"date": "bad", "type": "expense", "category": "food", "amount": "1000", "memo": "bad", "tags": ""})
        self.assertEqual(self.service.import_csv(source)[:2], (1, 1))
        output = Path(self.temp_dir.name) / "export.csv"
        self.assertEqual(self.service.export_csv(output, month="2024-01"), 1)
        with output.open(encoding="utf-8", newline="") as file:
            self.assertEqual(next(csv.reader(file)), ["date", "type", "category", "amount", "memo", "tags"])
        february_output = Path(self.temp_dir.name) / "february.csv"
        self.assertEqual(self.service.export_csv(february_output, month="2024-02"), 0)


if __name__ == "__main__":
    unittest.main()
