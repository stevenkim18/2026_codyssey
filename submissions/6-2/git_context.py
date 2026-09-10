"""Git 변경사항을 수집하고 AI 전송 전에 안전하게 정제하는 모듈."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import subprocess


MAX_SAFE_FILES = 10
MAX_SAFE_LINES = 200


class GitContextError(RuntimeError):
    """Git 저장소를 읽는 중 발생한 사용자에게 설명 가능한 오류."""


@dataclass(frozen=True)
class GitSnapshot:
    """AI 프롬프트에 사용할 Git 상태 스냅샷."""

    status: str
    diff: str
    changed_files: tuple[str, ...]
    diff_lines: int

    @property
    def has_changes(self) -> bool:
        return bool(self.status.strip() or self.diff.strip())


def _run_git(arguments: list[str], cwd: Path) -> str:
    try:
        completed = subprocess.run(
            ["git", *arguments],
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError as error:
        raise GitContextError("Git 명령을 찾을 수 없습니다. Git 설치 상태를 확인하세요.") from error
    except subprocess.CalledProcessError as error:
        detail = (error.stderr or "").strip()
        message = "Git 프로젝트 루트에서 실행하세요."
        if detail:
            message = f"{message} ({detail})"
        raise GitContextError(message) from error
    return completed.stdout


def _parse_changed_files(status: str) -> tuple[str, ...]:
    files: list[str] = []
    for line in status.splitlines():
        if not line.strip():
            continue
        path = line[3:] if len(line) > 3 else line.strip()
        if " -> " in path:
            path = path.rsplit(" -> ", maxsplit=1)[-1]
        files.append(path.strip())
    return tuple(files)


def collect_git_snapshot(cwd: Path | None = None) -> GitSnapshot:
    """현재 디렉터리에서 ``git status``와 ``git diff`` 결과를 수집한다."""

    working_directory = (cwd or Path.cwd()).resolve()
    status = _run_git(["status", "--short"], working_directory)
    diff = _run_git(["diff", "--no-color"], working_directory)
    return GitSnapshot(
        status=status,
        diff=diff,
        changed_files=_parse_changed_files(status),
        diff_lines=len(diff.splitlines()),
    )


_OPENAI_KEY_PATTERN = re.compile(r"\bsk-[A-Za-z0-9_-]{8,}\b")
_BEARER_PATTERN = re.compile(r"(?i)(\bBearer\s+)[A-Za-z0-9._~+/=-]+")
_EMAIL_PATTERN = re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b")
_ASSIGNMENT_PATTERN = re.compile(
    r"(?i)(\b(?:api[_-]?key|secret|token|password|passwd)\b\s*[:=]\s*)([^\s,;]+)"
)


def mask_sensitive(text: str) -> str:
    """diff에 흔히 포함되는 키·토큰·이메일을 표시 문자열로 치환한다."""

    masked = _OPENAI_KEY_PATTERN.sub("[MASKED_API_KEY]", text)
    masked = _BEARER_PATTERN.sub(r"\1[MASKED_BEARER_TOKEN]", masked)
    masked = _ASSIGNMENT_PATTERN.sub(r"\1[MASKED_SECRET]", masked)
    return _EMAIL_PATTERN.sub("[MASKED_EMAIL]", masked)


def _limit_status(status: str, max_files: int) -> str:
    lines = status.splitlines()
    if len(lines) <= max_files:
        return status
    kept = lines[:max_files]
    kept.append(f"... [safe-mode: 상태 파일 {len(lines) - max_files}개 생략]")
    return "\n".join(kept) + "\n"


def limit_diff(diff: str, max_files: int = MAX_SAFE_FILES, max_lines: int = MAX_SAFE_LINES) -> str:
    """diff를 파일 수와 줄 수 기준으로 제한한다."""

    lines = diff.splitlines()
    if not lines:
        return diff

    kept: list[str] = []
    file_count = 0
    truncated_by_file = False
    truncated_by_line = False

    for line in lines:
        if line.startswith("diff --git "):
            if file_count >= max_files:
                truncated_by_file = True
                break
            file_count += 1
        if len(kept) >= max_lines:
            truncated_by_line = True
            break
        kept.append(line)

    if len(kept) < len(lines) and not (truncated_by_file or truncated_by_line):
        truncated_by_line = True

    result = kept
    if truncated_by_file:
        result.append(f"... [safe-mode: 파일 {max_files}개 초과분 생략]")
    elif truncated_by_line:
        result.append(f"... [safe-mode: diff {max_lines}줄 초과분 생략]")
    return "\n".join(result) + "\n"


def sanitize_snapshot(snapshot: GitSnapshot, safe_mode: bool) -> GitSnapshot:
    """safe-mode에 따라 스냅샷을 마스킹하고 전송량을 제한한다."""

    if not safe_mode:
        return snapshot

    status = _limit_status(mask_sensitive(snapshot.status), MAX_SAFE_FILES)
    diff = limit_diff(mask_sensitive(snapshot.diff))
    files = tuple(mask_sensitive(path) for path in snapshot.changed_files[:MAX_SAFE_FILES])
    return GitSnapshot(
        status=status,
        diff=diff,
        changed_files=files,
        diff_lines=len(diff.splitlines()),
    )
