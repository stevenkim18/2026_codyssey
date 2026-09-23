"""CLI 기반 Mini Git의 실행 진입점."""

from mini_git.cli import run_repl


if __name__ == "__main__":
    raise SystemExit(run_repl())
