from __future__ import annotations

import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from urllib import error as urllib_error


SOURCE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE_DIR))

from ai_client import AIClientError, GenerationOptions, OpenAIChatClient  # noqa: E402
from drafts import parse_commit_draft, parse_pr_draft, render_pr  # noqa: E402
from git_context import GitSnapshot, collect_git_snapshot, sanitize_snapshot  # noqa: E402
import main  # noqa: E402


def git(cwd: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *arguments],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )


def create_repo() -> tempfile.TemporaryDirectory[str]:
    directory = tempfile.TemporaryDirectory()
    repo = Path(directory.name)
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Test User")
    (repo / "example.py").write_text("print('before')\n", encoding="utf-8")
    git(repo, "add", "example.py")
    git(repo, "commit", "-q", "-m", "초기 파일 추가")
    (repo / "example.py").write_text("print('after')\n", encoding="utf-8")
    return directory


class FakeClient:
    def __init__(self, response: str) -> None:
        self.response = response
        self.calls = 0
        self.last_options: GenerationOptions | None = None

    def generate(self, messages: object, options: GenerationOptions) -> str:
        self.calls += 1
        self.last_options = options
        return self.response


class FakeResponse:
    def __init__(self, payload: bytes) -> None:
        self.payload = payload

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self) -> bytes:
        return self.payload


class GitContextTests(unittest.TestCase):
    def test_collects_status_and_diff_from_repository(self) -> None:
        directory = create_repo()
        self.addCleanup(directory.cleanup)

        snapshot = collect_git_snapshot(Path(directory.name))

        self.assertTrue(snapshot.has_changes)
        self.assertEqual(snapshot.changed_files, ("example.py",))
        self.assertIn(" M example.py", snapshot.status)
        self.assertIn("+print('after')", snapshot.diff)
        self.assertGreater(snapshot.diff_lines, 0)

    def test_safe_mode_masks_secrets_and_limits_diff(self) -> None:
        diff = "\n".join(
            [
                f"diff --git a/file{index}.py b/file{index}.py\n+API_KEY = 'sk-proj-1234567890'\n+email = 'person{index}@example.com'"
                for index in range(12)
            ]
            + [f"+line-{index}" for index in range(220)]
        )
        snapshot = GitSnapshot(
            status="\n".join(f" M file{index}.py" for index in range(12)),
            diff=diff,
            changed_files=tuple(f"file{index}.py" for index in range(12)),
            diff_lines=len(diff.splitlines()),
        )

        safe = sanitize_snapshot(snapshot, safe_mode=True)

        self.assertNotIn("sk-proj-", safe.diff)
        self.assertNotIn("person0@example.com", safe.diff)
        self.assertLessEqual(len(safe.changed_files), 10)
        self.assertLessEqual(len(safe.diff.splitlines()), 201)
        self.assertLessEqual(safe.diff.count("diff --git "), 10)


class AIClientTests(unittest.TestCase):
    def test_sends_expected_chat_completion_payload(self) -> None:
        captured: dict[str, object] = {}

        def opener(request: object, timeout: float) -> FakeResponse:
            captured["request"] = request
            captured["timeout"] = timeout
            return FakeResponse(
                json.dumps({"choices": [{"message": {"content": "TITLE: 결과"}}]}).encode("utf-8")
            )

        client = OpenAIChatClient("test-key", opener=opener)
        result = client.generate(
            [{"role": "user", "content": "변경사항"}],
            GenerationOptions(model="gpt-4.1-mini", temperature=0.2, max_tokens=600),
        )

        request = captured["request"]
        self.assertEqual(result, "TITLE: 결과")
        self.assertEqual(getattr(request, "method"), "POST")
        self.assertEqual(getattr(request, "full_url"), "https://api.openai.com/v1/chat/completions")
        self.assertEqual(getattr(request, "headers")["Authorization"], "Bearer test-key")
        payload = json.loads(getattr(request, "data").decode("utf-8"))
        self.assertEqual(payload["model"], "gpt-4.1-mini")
        self.assertEqual(payload["temperature"], 0.2)
        self.assertEqual(payload["max_completion_tokens"], 600)

    def test_reports_http_authentication_error(self) -> None:
        def opener(request: object, timeout: float) -> FakeResponse:
            raise urllib_error.HTTPError(
                "https://api.openai.com/v1/chat/completions",
                401,
                "Unauthorized",
                {},
                io.BytesIO(b'{"error":{"message":"invalid api key"}}'),
            )

        client = OpenAIChatClient("bad-key", opener=opener)
        with self.assertRaisesRegex(AIClientError, "HTTP 401.*AI_API_KEY"):
            client.generate([], GenerationOptions())

    def test_reports_invalid_json_response(self) -> None:
        client = OpenAIChatClient("test-key", opener=lambda request, timeout: FakeResponse(b"not-json"))
        with self.assertRaisesRegex(AIClientError, "JSON"):
            client.generate([], GenerationOptions())

    def test_reports_network_error(self) -> None:
        def opener(request: object, timeout: float) -> FakeResponse:
            raise urllib_error.URLError("offline")

        client = OpenAIChatClient("test-key", opener=opener)
        with self.assertRaisesRegex(AIClientError, "네트워크"):
            client.generate([], GenerationOptions())

    def test_reports_missing_content_in_response(self) -> None:
        client = OpenAIChatClient(
            "test-key",
            opener=lambda request, timeout: FakeResponse(b'{"choices":[{"message":null}]}'),
        )
        with self.assertRaisesRegex(AIClientError, r"choices\[0\].message.content"):
            client.generate([], GenerationOptions())


class DraftTests(unittest.TestCase):
    def test_commit_title_and_optional_body_are_normalized(self) -> None:
        draft = parse_commit_draft(
            """```text
TITLE: feat: 변경사항을 반영합니다
BODY:
- example.py의 핵심 로직을 수정했습니다.
```"""
        )

        self.assertEqual(draft.title, "feat: 변경사항을 반영합니다")
        self.assertIn("- example.py", draft.body)
        self.assertLessEqual(len(draft.title), 72)

    def test_pr_has_all_required_sections_and_bullets(self) -> None:
        draft = parse_pr_draft("""TITLE: 기능 개선
BODY:
## Why
배경 설명
## What
- 변경 내용
""", ["example.py"])

        rendered = render_pr(draft)
        for section in ("## Why", "## What", "## How to Test"):
            self.assertIn(section, rendered)
        self.assertGreaterEqual(rendered.count("\n- "), 3)
        self.assertLessEqual(len(draft.title), 80)


class CLITests(unittest.TestCase):
    def test_commit_calls_api_once_and_prints_result(self) -> None:
        directory = create_repo()
        self.addCleanup(directory.cleanup)
        client = FakeClient("TITLE: fix: 변경사항 반영\nBODY:\n- example.py 수정")
        output = io.StringIO()
        errors = io.StringIO()

        result = main.main(
            ["commit", "--temperature", "0.4", "--max-tokens", "300"],
            cwd=Path(directory.name),
            client=client,
            environ={"AI_API_KEY": "test-key"},
            output=output,
            error_output=errors,
        )

        self.assertEqual(result, 0)
        self.assertEqual(client.calls, 1)
        self.assertEqual(client.last_options.temperature, 0.4)  # type: ignore[union-attr]
        self.assertIn("--- Commit Message ---", output.getvalue())
        self.assertEqual(errors.getvalue(), "")

    def test_pr_calls_api_once_and_prints_required_sections(self) -> None:
        directory = create_repo()
        self.addCleanup(directory.cleanup)
        client = FakeClient(
            "TITLE: feat: PR 초안 생성\nBODY:\n## Why\n- 변경 배경\n## What\n- 핵심 변경\n## How to Test\n- 테스트 실행"
        )
        output = io.StringIO()

        result = main.main(
            ["pr", "--safe-mode"],
            cwd=Path(directory.name),
            client=client,
            environ={"AI_API_KEY": "test-key"},
            output=output,
            error_output=io.StringIO(),
        )

        rendered = output.getvalue()
        self.assertEqual(result, 0)
        self.assertEqual(client.calls, 1)
        self.assertIn("safe-mode", rendered)
        self.assertIn("## Why", rendered)
        self.assertIn("## What", rendered)
        self.assertIn("## How to Test", rendered)

    def test_no_changes_skips_api_key_and_api_call(self) -> None:
        directory = create_repo()
        self.addCleanup(directory.cleanup)
        repo = Path(directory.name)
        (repo / "example.py").write_text("print('after')\n", encoding="utf-8")
        git(repo, "add", "example.py")
        git(repo, "commit", "-q", "-m", "변경 반영")
        client = FakeClient("TITLE: 사용되지 않음")
        output = io.StringIO()

        result = main.main(
            ["commit"],
            cwd=repo,
            client=client,
            environ={},
            output=output,
            error_output=io.StringIO(),
        )

        self.assertEqual(result, 0)
        self.assertEqual(client.calls, 0)
        self.assertIn("변경 사항이 없습니다", output.getvalue())

    def test_missing_api_key_is_reported(self) -> None:
        directory = create_repo()
        self.addCleanup(directory.cleanup)
        errors = io.StringIO()

        result = main.main(
            ["commit"],
            cwd=Path(directory.name),
            environ={},
            output=io.StringIO(),
            error_output=errors,
        )

        self.assertEqual(result, 1)
        self.assertIn("AI_API_KEY", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
