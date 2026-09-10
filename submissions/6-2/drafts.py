"""AI가 반환한 텍스트를 커밋·PR 출력 형식으로 검증하고 정규화한다."""

from __future__ import annotations

from dataclasses import dataclass
import re
from collections.abc import Sequence


class DraftFormatError(ValueError):
    """AI 초안을 해석할 수 없을 때 발생하는 오류."""


@dataclass(frozen=True)
class Draft:
    title: str
    body: str = ""


def _clean_lines(text: str) -> list[str]:
    lines: list[str] = []
    for raw_line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        line = raw_line.strip()
        if line.startswith("```"):
            continue
        lines.append(line)
    return lines


def _remove_label(line: str, labels: tuple[str, ...]) -> str:
    for label in labels:
        if line.lower().startswith(label.lower()):
            return line[len(label) :].lstrip(" :")
    return line


def _shorten_title(title: str, maximum: int) -> str:
    normalized = " ".join(title.split())
    if len(normalized) > maximum:
        normalized = normalized[:maximum].rstrip()
    if not normalized:
        raise DraftFormatError("AI 응답에서 제목을 찾을 수 없습니다.")
    return normalized


def _first_title(lines: list[str], body_start: int | None, maximum: int) -> tuple[str, int]:
    limit = body_start if body_start is not None else len(lines)
    for index, line in enumerate(lines[:limit]):
        if not line:
            continue
        lower = line.strip("-# ").lower().rstrip(":")
        if lower in {
            "commit",
            "commit message",
            "commit title",
            "commit body",
            "pr",
            "pr title",
            "pr body",
            "pull request",
            "body",
        }:
            continue
        candidate = _remove_label(
            line,
            ("TITLE:", "PR TITLE:", "COMMIT TITLE:", "COMMIT MESSAGE:"),
        )
        if candidate:
            return _shorten_title(candidate, maximum), index
    raise DraftFormatError("AI 응답에서 제목을 찾을 수 없습니다.")


def parse_commit_draft(text: str) -> Draft:
    lines = _clean_lines(text)
    body_start = next(
        (index for index, line in enumerate(lines) if line.lower() in {"body", "body:"}),
        None,
    )
    title, title_index = _first_title(lines, body_start, 72)
    start = body_start + 1 if body_start is not None else title_index + 1
    body_lines = [line for line in lines[start:] if line and line.lower() not in {"body", "body:"}]
    body = "\n".join(body_lines).strip()

    if body and not any(re.match(r"^(?:[-*+]\s+|\d+[.)]\s+)", line) for line in body_lines):
        body = ""
    return Draft(title=title, body=body)


_SECTION_PATTERN = re.compile(r"^#{0,6}\s*(why|what|how\s+to\s+test)\s*:?$", re.IGNORECASE)


def _section_key(line: str) -> str | None:
    match = _SECTION_PATTERN.match(line.strip())
    if not match:
        return None
    normalized = re.sub(r"\s+", " ", match.group(1).lower())
    return {"why": "Why", "what": "What", "how to test": "How to Test"}[normalized]


def _as_bullets(lines: list[str], fallback: str) -> list[str]:
    content = [line.strip() for line in lines if line.strip()]
    if not content:
        return [fallback]

    bullets: list[str] = []
    for line in content:
        if re.match(r"^(?:[-*+]\s+|\d+[.)]\s+)", line):
            line = re.sub(r"^(?:[-*+]\s+|\d+[.)]\s+)", "", line).strip()
        if line:
            bullets.append(f"- {line}")
    return bullets or [fallback]


def parse_pr_draft(text: str, changed_files: Sequence[str] = ()) -> Draft:
    lines = _clean_lines(text)
    first_section = next((index for index, line in enumerate(lines) if _section_key(line)), None)
    title, title_index = _first_title(lines, first_section, 80)

    sections: dict[str, list[str]] = {"Why": [], "What": [], "How to Test": []}
    current: str | None = None
    loose_body: list[str] = []
    for index, line in enumerate(lines):
        if index == title_index:
            continue
        if line.lower() in {"body", "body:"} or line.strip("-# ").lower() in {"pr body", "commit body"}:
            continue
        key = _section_key(line)
        if key is not None:
            current = key
            continue
        if not line:
            continue
        if current is None:
            loose_body.append(line)
        else:
            sections[current].append(line)

    if loose_body and not any(sections.values()):
        sections["What"] = loose_body

    file_names = ", ".join(path for path in changed_files[:3] if path) or "변경 파일"
    fallbacks = {
        "Why": "- 변경 배경은 Git diff에 명시되지 않아 검토가 필요합니다.",
        "What": f"- 변경 파일: {file_names}",
        "How to Test": "- 관련 테스트를 실행하고 결과를 확인합니다.",
    }
    body_parts: list[str] = []
    for section_name in ("Why", "What", "How to Test"):
        body_parts.append(f"## {section_name}")
        body_parts.extend(_as_bullets(sections[section_name], fallbacks[section_name]))
        body_parts.append("")
    return Draft(title=title, body="\n".join(body_parts).rstrip())


def render_commit(draft: Draft) -> str:
    parts = ["--- Commit Message ---", draft.title]
    if draft.body:
        parts.extend(["", draft.body])
    parts.append("----------------------")
    return "\n".join(parts)


def render_pr(draft: Draft) -> str:
    return "\n".join(
        [
            "--- PR Title ---",
            draft.title,
            "",
            "--- PR Body ---",
            draft.body,
            "----------------------",
        ]
    )
