"""Mini Redis REPL 인터페이스."""

import shlex

from .store import MiniRedis


def run_repl() -> int:
    """명령을 반복해서 읽고 Mini Redis 엔진의 결과를 출력한다."""
    redis = MiniRedis()
    while True:
        try:
            line = input("mini-redis> ")
        except EOFError:
            print()
            return 0
        except KeyboardInterrupt:
            print()
            return 0

        try:
            tokens = shlex.split(line)
        except ValueError:
            print("(error) ERR invalid quoted string")
            continue
        if not tokens:
            continue

        command = tokens[0]
        if command.lower() in ("exit", "quit") and len(tokens) == 1:
            return 0
        print(redis.execute(command, tokens[1:]))
