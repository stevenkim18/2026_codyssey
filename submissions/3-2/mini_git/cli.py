"""Mini Git REPL 인터페이스."""

import shlex

from .repository import MiniGit


def run_repl() -> int:
    """명령을 반복해서 읽고 Mini Git 엔진의 결과를 출력한다."""
    repository = MiniGit()
    while True:
        try:
            line = input("mini-git> ")
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        try:
            tokens = shlex.split(line)
        except ValueError:
            print("Invalid args")
            continue
        if not tokens:
            continue

        command = tokens[0]
        if command.lower() in ("exit", "quit"):
            if len(tokens) == 1:
                return 0
            print("Invalid args")
            continue
        print(repository.execute(command, tokens[1:]))
