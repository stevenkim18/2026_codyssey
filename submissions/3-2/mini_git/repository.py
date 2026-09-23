"""메모리 기반 Mini Git 저장소와 명령 처리기."""

from datetime import datetime
from typing import Callable, Dict, List, Optional, Set

from .algorithms import collect_ancestors, merge_sort, shortest_path, topological_order
from .model import Commit


class MiniGit:
    """브랜치, 커밋 그래프, 탐색 및 검색 기능을 제공한다."""

    def __init__(self, clock: Optional[Callable[[], datetime]] = None) -> None:
        self.commits = {}  # type: Dict[str, Commit]
        self.branches = {}  # type: Dict[str, Optional[str]]
        self.children = {}  # type: Dict[str, List[str]]
        self.keyword_index = {}  # type: Dict[str, List[str]]
        self.author_index = {}  # type: Dict[str, List[str]]
        self.current_branch = None  # type: Optional[str]
        self.current_user = None  # type: Optional[str]
        self._next_sequence = 1
        self._clock = clock if clock is not None else datetime.now

    @property
    def initialized(self) -> bool:
        """저장소가 초기화되었는지 반환한다."""
        return self.current_branch is not None

    def execute(self, raw_command: str, arguments: List[str]) -> str:
        """파싱된 명령과 인자를 실행하고 출력 문자열을 반환한다."""
        command = raw_command.upper()

        if command == "INIT":
            return self._init(arguments)
        if not self.initialized:
            return "Repository not initialized."
        if command == "BRANCH":
            return self._branch(arguments)
        if command == "SWITCH":
            return self._switch(arguments)
        if command == "COMMIT":
            return self._commit(arguments)
        if command == "LOG":
            return self._log(arguments)
        if command == "PATH":
            return self._path(arguments)
        if command == "ANCESTORS":
            return self._ancestors(arguments)
        if command == "SEARCH":
            return self._search(arguments)
        return "Unknown command: {}".format(raw_command)

    def _init(self, arguments: List[str]) -> str:
        if len(arguments) != 1 or not arguments[0].strip():
            return "Invalid args"
        if self.initialized:
            return "Repository already initialized."

        self.current_user = arguments[0]
        self.current_branch = "main"
        self.branches["main"] = None
        return "\n".join([
            "Initialized repository.",
            "Current branch: main",
            "Current user: {}".format(self.current_user),
        ])

    def _branch(self, arguments: List[str]) -> str:
        if len(arguments) != 1 or not arguments[0].strip():
            return "Invalid args"
        branch_name = arguments[0]
        if branch_name in self.branches:
            return "Branch already exists: {}".format(branch_name)

        self.branches[branch_name] = self._head_hash()
        return "Created branch: {}".format(branch_name)

    def _switch(self, arguments: List[str]) -> str:
        if len(arguments) != 1 or not arguments[0].strip():
            return "Invalid args"
        branch_name = arguments[0]
        if branch_name not in self.branches:
            return "Unknown branch: {}".format(branch_name)

        self.current_branch = branch_name
        return "Switched to branch: {}".format(branch_name)

    def _commit(self, arguments: List[str]) -> str:
        if len(arguments) != 1 or not arguments[0].strip():
            return "Invalid args"

        sequence = self._next_sequence
        commit_hash = "c{:06d}".format(sequence)
        parent_hash = self._head_hash()
        parents = () if parent_hash is None else (parent_hash,)
        commit = Commit(
            hash=commit_hash,
            message=arguments[0],
            author=self.current_user or "",
            timestamp=self._clock(),
            parents=parents,
            sequence=sequence,
        )

        self.commits[commit_hash] = commit
        self.children[commit_hash] = []
        for commit_parent in parents:
            self.children[commit_parent].append(commit_hash)
        self.branches[self.current_branch or "main"] = commit_hash
        self._index_commit(commit)
        self._next_sequence += 1
        return "[{} {}] {}".format(self.current_branch, commit_hash, commit.message)

    def _log(self, arguments: List[str]) -> str:
        commits = list(self.commits.values())
        if not arguments:
            commits = topological_order(self.commits, self.children)
        elif len(arguments) == 1 and arguments[0].lower() == "--sort-by=date":
            commits = merge_sort(commits, key=lambda commit: (commit.timestamp, commit.sequence))
        elif len(arguments) == 1 and arguments[0].lower() == "--sort-by=author":
            commits = merge_sort(
                commits,
                key=lambda commit: (commit.author.lower(), commit.sequence),
            )
        else:
            return "Invalid args"
        return self._format_commit_list(commits, "No commits.")

    def _path(self, arguments: List[str]) -> str:
        if len(arguments) != 2:
            return "Invalid args"
        for commit_hash in arguments:
            if commit_hash not in self.commits:
                return "Unknown commit: {}".format(commit_hash)

        path = shortest_path(arguments[0], arguments[1], self.commits, self.children)
        if path is None:
            return "No path"
        return "Path: {}".format(" -> ".join(path))

    def _ancestors(self, arguments: List[str]) -> str:
        if len(arguments) != 1:
            return "Invalid args"
        commit_hash = arguments[0]
        if commit_hash not in self.commits:
            return "Unknown commit: {}".format(commit_hash)

        hashes = collect_ancestors(commit_hash, self.commits)
        commits = topological_order(self.commits, self.children, hashes)
        return self._format_commit_list(commits, "No ancestors.")

    def _search(self, arguments: List[str]) -> str:
        if len(arguments) != 1 or not arguments[0].strip():
            return "Invalid args"

        raw_query = arguments[0]
        if raw_query.lower().startswith("--author="):
            author = raw_query[len("--author="):].strip().lower()
            if not author:
                return "Invalid args"
            hashes = list(self.author_index.get(author, []))
        elif raw_query.startswith("--"):
            return "Invalid args"
        else:
            tokens = self._message_tokens(raw_query)
            if not tokens:
                return "Invalid args"
            hashes = self._keyword_matches(tokens)

        commits = [self.commits[commit_hash] for commit_hash in hashes]
        if not commits:
            return "No commits found."
        lines = ["Found {} commit(s):".format(len(commits)), ""]
        for commit in commits:
            lines.append("- {}: {}".format(commit.hash, commit.message))
        return "\n".join(lines)

    def _keyword_matches(self, tokens: List[str]) -> List[str]:
        """각 토큰의 posting list를 교집합해 생성 순서로 반환한다."""
        matching = set(self.keyword_index.get(tokens[0], []))  # type: Set[str]
        for token in tokens[1:]:
            matching.intersection_update(self.keyword_index.get(token, []))
        return [commit_hash for commit_hash in self.commits if commit_hash in matching]

    def _index_commit(self, commit: Commit) -> None:
        """작성자와 메시지 토큰의 역색인에 새 커밋을 추가한다."""
        author_key = commit.author.lower()
        self.author_index.setdefault(author_key, []).append(commit.hash)
        seen = set()  # type: Set[str]
        for token in self._message_tokens(commit.message):
            if token in seen:
                continue
            self.keyword_index.setdefault(token, []).append(commit.hash)
            seen.add(token)

    @staticmethod
    def _message_tokens(message: str) -> List[str]:
        return [token.lower() for token in message.split()]

    def _head_hash(self) -> Optional[str]:
        if self.current_branch is None:
            return None
        return self.branches[self.current_branch]

    @staticmethod
    def _format_commit_list(commits: List[Commit], empty_message: str) -> str:
        if not commits:
            return empty_message
        blocks = []  # type: List[str]
        for commit in commits:
            blocks.append("\n".join([
                "commit {} ({}, {})".format(
                    commit.hash,
                    commit.author,
                    commit.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                ),
                commit.message,
            ]))
        return "\n\n".join(blocks)
