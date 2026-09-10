"""Git 변경사항으로 커밋 메시지와 PR 초안을 생성하는 CLI."""

from __future__ import annotations

import argparse
from collections.abc import Mapping, Sequence
import os
from pathlib import Path
import sys
from typing import TextIO

from ai_client import AIClientError, GenerationOptions, OpenAIChatClient
from drafts import DraftFormatError, parse_commit_draft, parse_pr_draft, render_commit, render_pr
from git_context import GitContextError, collect_git_snapshot, sanitize_snapshot
from prompts import build_messages


DEFAULT_MODEL = "gpt-4.1-mini"
DEFAULT_TEMPERATURE = 0.2
DEFAULT_MAX_TOKENS = 600


def _temperature(value: str) -> float:
    try:
        parsed = float(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("temperature는 숫자여야 합니다.") from error
    if not 0 <= parsed <= 2:
        raise argparse.ArgumentTypeError("temperature는 0부터 2 사이여야 합니다.")
    return parsed


def _positive_integer(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("max-tokens는 정수여야 합니다.") from error
    if parsed <= 0:
        raise argparse.ArgumentTypeError("max-tokens는 양수여야 합니다.")
    return parsed


def _add_common_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"사용할 모델 (기본값: {DEFAULT_MODEL})")
    parser.add_argument(
        "--temperature",
        type=_temperature,
        default=DEFAULT_TEMPERATURE,
        help=f"응답 다양성, 0~2 (기본값: {DEFAULT_TEMPERATURE})",
    )
    parser.add_argument(
        "--max-tokens",
        type=_positive_integer,
        default=DEFAULT_MAX_TOKENS,
        help=f"최대 출력 토큰 수 (기본값: {DEFAULT_MAX_TOKENS})",
    )
    parser.add_argument(
        "--safe-mode",
        action="store_true",
        help="민감정보 마스킹 및 diff를 최대 10개 파일·200줄로 제한",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python main.py",
        description="Git 변경사항 기반 AI 커밋 메시지·PR 초안 생성기",
        epilog=(
            "공통 옵션: --model MODEL, --temperature VALUE, --max-tokens COUNT, --safe-mode. "
            "자세한 내용은 각 명령의 --help에서 확인할 수 있습니다."
        ),
    )
    commands = parser.add_subparsers(dest="command")

    commit = commands.add_parser("commit", help="커밋 메시지 생성")
    _add_common_options(commit)

    pr = commands.add_parser("pr", help="PR 제목·본문 생성")
    _add_common_options(pr)
    return parser


def execute(
    args: argparse.Namespace,
    *,
    cwd: Path | None = None,
    client: OpenAIChatClient | None = None,
    environ: Mapping[str, str] | None = None,
    output: TextIO | None = None,
    error_output: TextIO | None = None,
) -> int:
    out = output or sys.stdout
    err = error_output or sys.stderr
    environment = os.environ if environ is None else environ

    try:
        snapshot = collect_git_snapshot(cwd)
        print(f"[INFO] Git status 수집 완료: {len(snapshot.changed_files)}개 파일 변경 감지", file=out)
        print(f"[INFO] Git diff 수집 완료: {snapshot.diff_lines}줄", file=out)
        if not snapshot.has_changes:
            print("[INFO] 변경 사항이 없습니다. 커밋 메시지를 생성하지 않고 종료합니다.", file=out)
            return 0

        prepared = sanitize_snapshot(snapshot, args.safe_mode)
        if args.safe_mode:
            print("[INFO] safe-mode 적용: 민감정보 마스킹, 최대 10개 파일·200줄 전송", file=out)

        api_key = environment.get("AI_API_KEY", "").strip()
        if not api_key:
            raise AIClientError("AI_API_KEY 환경변수가 설정되지 않았습니다. 예: export AI_API_KEY=\"YOUR_KEY\"")

        options = GenerationOptions(
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
        )
        api_client = client or OpenAIChatClient(api_key, timeout=options.timeout)
        print("[INFO] AI API 요청 중... (1회)", file=out)
        response_text = api_client.generate(build_messages(args.command, prepared), options)

        if args.command == "commit":
            draft = parse_commit_draft(response_text)
            print("[DONE] 커밋 메시지 생성 완료", file=out)
            print(render_commit(draft), file=out)
        else:
            draft = parse_pr_draft(response_text, prepared.changed_files)
            print("[DONE] PR 초안 생성 완료", file=out)
            print(render_pr(draft), file=out)
        print("[INFO] API 호출 횟수: 1", file=out)
        return 0
    except (GitContextError, AIClientError, DraftFormatError) as error:
        print(f"[ERROR] {error}", file=err)
        return 1
    except Exception as error:  # pragma: no cover - 예측하지 못한 운영 오류의 최종 안전망
        print(f"[ERROR] 예상하지 못한 오류가 발생했습니다: {error}", file=err)
        return 1


def main(
    argv: Sequence[str] | None = None,
    *,
    cwd: Path | None = None,
    client: OpenAIChatClient | None = None,
    environ: Mapping[str, str] | None = None,
    output: TextIO | None = None,
    error_output: TextIO | None = None,
) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help(file=output or sys.stdout)
        return 2
    return execute(
        args,
        cwd=cwd,
        client=client,
        environ=environ,
        output=output,
        error_output=error_output,
    )


if __name__ == "__main__":
    raise SystemExit(main())
