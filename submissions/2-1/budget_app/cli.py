"""argparse 기반 콘솔 사용자 인터페이스."""

from __future__ import annotations

import argparse
import functools
import sys
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

from .models import AppError
from .services import BudgetService


def command_guard(function: Callable[[argparse.Namespace], int]) -> Callable[[argparse.Namespace], int]:
    """명령의 예외 처리와 실행 시간 측정을 한곳으로 모은 데코레이터."""
    @functools.wraps(function)
    def wrapped(args: argparse.Namespace) -> int:
        started = time.perf_counter()
        try:
            return function(args)
        except AppError as error:
            print(f"[오류] {error.message}", file=sys.stderr)
            print(f"[힌트] {error.hint}", file=sys.stderr)
            return 1
        except OSError as error:
            print(f"[오류] 파일을 처리할 수 없습니다: {error}", file=sys.stderr)
            print("[힌트] 경로와 파일 권한을 확인하세요.", file=sys.stderr)
            return 1
        except Exception:
            print("[오류] 예상하지 못한 문제가 발생했습니다.", file=sys.stderr)
            print("[힌트] 입력값과 저장 파일 형식을 확인하세요.", file=sys.stderr)
            return 1
        finally:
            print(f"[실행 시간] {time.perf_counter() - started:.3f}초", file=sys.stderr)
    return wrapped


def service_for(args: argparse.Namespace) -> BudgetService:
    return BudgetService(Path(args.data_dir))


def print_transaction(transaction: Any) -> None:
    print(
        f"{transaction.id} | {transaction.date} | {transaction.type:<7} | "
        f"{transaction.category} | {transaction.amount} | {transaction.memo}"
    )


def prompt_until(label: str, parser: Callable[[str], Any]) -> Any:
    while True:
        try:
            return parser(input(label))
        except AppError as error:
            print(f"[오류] {error.message}")
            print(f"[힌트] {error.hint}")


@command_guard
def run_add(args: argparse.Namespace) -> int:
    service = service_for(args)
    date = prompt_until("날짜(YYYY-MM-DD): ", lambda value: value if _valid_date(value) else value)
    transaction_type = prompt_until("타입(income/expense): ", lambda value: value if _valid_type(value) else value)
    category = prompt_until("카테고리: ", service._validate_category)
    amount = prompt_until("금액(양수): ", _valid_amount)
    memo = input("메모(선택): ")
    tags = input("태그(쉼표로 구분, 없으면 엔터): ")
    transaction = service.add_transaction(
        date=date, transaction_type=transaction_type, category=category, amount=amount, memo=memo, tags=tags
    )
    print(f"[저장 완료] id={transaction.id}")
    return 0


def _valid_date(value: str) -> bool:
    from .models import validate_date
    validate_date(value)
    return True


def _valid_type(value: str) -> bool:
    from .models import validate_type
    validate_type(value)
    return True


def _valid_amount(value: str) -> int:
    from .models import validate_amount
    return validate_amount(value)


@command_guard
def run_list(args: argparse.Namespace) -> int:
    transactions = list(service_for(args).list_transactions(args.limit))
    if not transactions:
        print("데이터 없음")
    for transaction in transactions:
        print_transaction(transaction)
    return 0


@command_guard
def run_search(args: argparse.Namespace) -> int:
    found = False
    for transaction in service_for(args).search(
        from_date=args.from_date, to_date=args.to_date, category=args.category,
        transaction_type=args.transaction_type, query=args.query, tag=args.tag,
    ):
        print_transaction(transaction)
        found = True
    if not found:
        print("데이터 없음")
    return 0


@command_guard
def run_summary(args: argparse.Namespace) -> int:
    result = service_for(args).summary(args.month, args.top)
    if result["count"] == 0:
        print("데이터 없음")
        return 0
    print(f"총 수입: {result['income']}원")
    print(f"총 지출: {result['expense']}원")
    print(f"잔액: {result['balance']}원")
    budget = result["budget"]
    if budget:
        usage = result["expense"] / budget.amount * 100
        warning = " [경고: 예산 초과]" if result["expense"] > budget.amount else ""
        print(f"예산: {budget.amount}원 (사용률 {usage:.1f}%){warning}")
    print(f"\n지출 TOP {args.top}")
    for index, (category, amount) in enumerate(result["top_expenses"], start=1):
        print(f"{index}) {category} {amount}원")
    return 0


@command_guard
def run_budget_set(args: argparse.Namespace) -> int:
    budget = service_for(args).set_budget(args.month, args.amount)
    print(f"[저장 완료] {budget.month} 예산 {budget.amount}원")
    return 0


@command_guard
def run_category(args: argparse.Namespace) -> int:
    service = service_for(args)
    if args.category_command == "list":
        for category in service.list_categories():
            print(f"- {category}")
    elif args.category_command == "add":
        name = prompt_until("카테고리명: ", service.add_category)
        print(f"[저장 완료] category={name}")
    else:
        service.remove_category(args.name)
        print(f"[삭제 완료] category={args.name}")
    return 0


@command_guard
def run_update(args: argparse.Namespace) -> int:
    changes = {
        key: value for key, value in {
            "date": args.date, "transaction_type": args.transaction_type, "category": args.category,
            "amount": args.amount, "memo": args.memo, "tags": args.tags,
        }.items() if value is not None
    }
    service_for(args).update_transaction(args.id, **changes)
    print(f"[수정 완료] id={args.id}")
    return 0


@command_guard
def run_delete(args: argparse.Namespace) -> int:
    service_for(args).delete_transaction(args.id)
    print(f"[삭제 완료] id={args.id}")
    return 0


@command_guard
def run_import(args: argparse.Namespace) -> int:
    imported, skipped, reasons = service_for(args).import_csv(args.source)
    print(f"[완료] imported={imported}, skipped={skipped}")
    for reason, count in reasons.items():
        print(f"- {reason}: {count}건")
    return 0


@command_guard
def run_export(args: argparse.Namespace) -> int:
    count = service_for(args).export_csv(
        args.output, month=args.month, from_date=args.from_date, to_date=args.to_date
    )
    print(f"[완료] {args.output} ({count} records)")
    return 0


def add_data_dir(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--data-dir", default="./data", help="저장 폴더 (기본값: ./data)")


def add_data_dir_override(parser: argparse.ArgumentParser) -> None:
    """상위 명령의 data-dir 기본값을 유지하면서 하위 명령에서도 재지정한다."""
    parser.add_argument("--data-dir", default=argparse.SUPPRESS, help="저장 폴더")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m budget_app", description="파일 기반 콘솔 가계부")
    commands = parser.add_subparsers(dest="command")

    add = commands.add_parser("add", help="대화형으로 거래 추가")
    add_data_dir(add); add.set_defaults(handler=run_add)
    listing = commands.add_parser("list", help="최근 거래 목록")
    add_data_dir(listing); listing.add_argument("--limit", type=int, default=20); listing.set_defaults(handler=run_list)
    search = commands.add_parser("search", help="조건으로 거래 검색")
    add_data_dir(search)
    search.add_argument("--from", dest="from_date"); search.add_argument("--to", dest="to_date")
    search.add_argument("--category"); search.add_argument("--type", dest="transaction_type")
    search.add_argument("--q", dest="query"); search.add_argument("--tag")
    search.set_defaults(handler=run_search)
    summary = commands.add_parser("summary", help="월별 수입·지출 요약")
    add_data_dir(summary); summary.add_argument("--month", required=True); summary.add_argument("--top", type=int, default=5)
    summary.set_defaults(handler=run_summary)
    budget = commands.add_parser("budget", help="월 예산 관리")
    add_data_dir(budget); budget_commands = budget.add_subparsers(dest="budget_command", required=True)
    budget_set = budget_commands.add_parser("set", help="월 예산 설정")
    add_data_dir_override(budget_set)
    budget_set.add_argument("--month", required=True); budget_set.add_argument("--amount", required=True, type=int); budget_set.set_defaults(handler=run_budget_set)
    category = commands.add_parser("category", help="카테고리 관리")
    add_data_dir(category); category_commands = category.add_subparsers(dest="category_command", required=True)
    category_add = category_commands.add_parser("add", help="대화형 카테고리 추가")
    add_data_dir_override(category_add); category_add.set_defaults(handler=run_category)
    category_list = category_commands.add_parser("list", help="카테고리 목록")
    add_data_dir_override(category_list); category_list.set_defaults(handler=run_category)
    category_remove = category_commands.add_parser("remove", help="카테고리 삭제")
    add_data_dir_override(category_remove)
    category_remove.add_argument("name"); category_remove.set_defaults(handler=run_category)
    update = commands.add_parser("update", help="옵션으로 거래 수정")
    add_data_dir(update); update.add_argument("--id", required=True); update.add_argument("--date")
    update.add_argument("--type", dest="transaction_type"); update.add_argument("--category")
    update.add_argument("--amount", type=int); update.add_argument("--memo"); update.add_argument("--tags")
    update.set_defaults(handler=run_update)
    delete = commands.add_parser("delete", help="거래 삭제")
    add_data_dir(delete); delete.add_argument("--id", required=True); delete.set_defaults(handler=run_delete)
    importing = commands.add_parser("import", help="CSV 거래 가져오기")
    add_data_dir(importing); importing.add_argument("--from", dest="source", required=True); importing.set_defaults(handler=run_import)
    exporting = commands.add_parser("export", help="CSV 거래 내보내기")
    add_data_dir(exporting); exporting.add_argument("--out", dest="output", required=True)
    filter_group = exporting.add_mutually_exclusive_group(required=True)
    filter_group.add_argument("--month")
    filter_group.add_argument("--from", dest="from_date")
    exporting.add_argument("--to", dest="to_date")
    exporting.set_defaults(handler=run_export)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "handler"):
        parser.print_help()
        return 2
    if args.command == "export" and args.from_date and not args.to_date:
        parser.error("export --from에는 --to가 필요합니다.")
    if args.command == "export" and args.to_date and not args.from_date:
        parser.error("export --to에는 --from이 필요합니다.")
    return args.handler(args)
