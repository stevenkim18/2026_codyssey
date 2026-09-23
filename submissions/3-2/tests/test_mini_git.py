"""Mini Git의 저장소, 알고리즘, CLI 통합 테스트."""

import subprocess
import sys
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from mini_git.algorithms import merge_sort, shortest_path
from mini_git.model import Commit
from mini_git.repository import MiniGit


class StepClock:
    """호출할 때마다 1초씩 증가하는 테스트용 시계."""

    def __init__(self) -> None:
        self.current = datetime(2026, 1, 1, 9, 0, 0)

    def __call__(self) -> datetime:
        result = self.current
        self.current += timedelta(seconds=1)
        return result


class MiniGitTest(unittest.TestCase):
    def setUp(self) -> None:
        self.git = MiniGit(clock=StepClock())

    def initialize(self) -> None:
        self.git.execute("INIT", ["Alice Kim"])

    def commit(self, message: str) -> str:
        output = self.git.execute("COMMIT", [message])
        return output.split()[1].rstrip("]")

    def test_init_creates_main_branch_and_user(self) -> None:
        output = self.git.execute("init", ["Alice Kim"])

        self.assertIn("Initialized repository.", output)
        self.assertEqual(self.git.current_branch, "main")
        self.assertEqual(self.git.current_user, "Alice Kim")
        self.assertIsNone(self.git.branches["main"])

    def test_branches_keep_independent_heads(self) -> None:
        self.initialize()
        first_hash = self.commit("Initial commit")
        self.assertEqual("Created branch: feature", self.git.execute("BRANCH", ["feature"]))
        self.git.execute("SWITCH", ["feature"])
        feature_hash = self.commit("Feature work")
        self.git.execute("SWITCH", ["main"])
        main_hash = self.commit("Main work")

        self.assertEqual(self.git.branches["feature"], feature_hash)
        self.assertEqual(self.git.branches["main"], main_hash)
        self.assertEqual(self.git.commits[feature_hash].parents, (first_hash,))
        self.assertEqual(self.git.commits[main_hash].parents, (first_hash,))

    def test_commit_hashes_are_unique_and_deterministic(self) -> None:
        self.initialize()

        self.assertEqual(self.commit("One"), "c000001")
        self.assertEqual(self.commit("Two"), "c000002")
        self.assertEqual(len(self.git.commits), 2)

    def test_log_places_parent_before_children(self) -> None:
        self.initialize()
        root = self.commit("Root")
        self.git.execute("BRANCH", ["feature"])
        main_child = self.commit("Main child")
        self.git.execute("SWITCH", ["feature"])
        feature_child = self.commit("Feature child")

        output = self.git.execute("LOG", [])

        self.assertLess(output.index(root), output.index(main_child))
        self.assertLess(output.index(root), output.index(feature_child))
        self.assertLess(output.index(main_child), output.index(feature_child))

    def test_merge_sort_is_stable_and_supports_different_keys(self) -> None:
        commits = [
            Commit("c3", "third", "Bob", datetime(2026, 1, 2), (), 3),
            Commit("c1", "first", "alice", datetime(2026, 1, 1), (), 1),
            Commit("c2", "second", "Alice", datetime(2026, 1, 1), (), 2),
        ]

        by_date = merge_sort(commits, key=lambda commit: commit.timestamp)
        by_author = merge_sort(commits, key=lambda commit: commit.author.lower())

        self.assertEqual([commit.hash for commit in by_date], ["c1", "c2", "c3"])
        self.assertEqual([commit.hash for commit in by_author], ["c1", "c2", "c3"])

    def test_path_uses_undirected_edges(self) -> None:
        self.initialize()
        root = self.commit("Root")
        child = self.commit("Child")

        self.assertEqual(
            self.git.execute("PATH", [child, root]),
            "Path: {} -> {}".format(child, root),
        )
        self.assertEqual(self.git.execute("PATH", [root, root]), "Path: {}".format(root))

    def test_path_returns_no_path_between_disconnected_roots(self) -> None:
        self.initialize()
        self.git.execute("BRANCH", ["other"])
        main_root = self.commit("Main root")
        self.git.execute("SWITCH", ["other"])
        other_root = self.commit("Other root")

        self.assertEqual(self.git.execute("PATH", [main_root, other_root]), "No path")

    def test_path_chooses_lexicographically_smallest_shortest_route(self) -> None:
        commits = {
            "start": Commit("start", "", "A", datetime(2026, 1, 1), (), 1),
            "alpha": Commit("alpha", "", "A", datetime(2026, 1, 1), ("start",), 2),
            "beta": Commit("beta", "", "A", datetime(2026, 1, 1), ("start",), 3),
            "end": Commit("end", "", "A", datetime(2026, 1, 1), ("alpha", "beta"), 4),
        }
        children = {
            "start": ["beta", "alpha"],
            "alpha": ["end"],
            "beta": ["end"],
            "end": [],
        }

        self.assertEqual(
            shortest_path("start", "end", commits, children),
            ["start", "alpha", "end"],
        )

    def test_ancestors_lists_every_reachable_parent_once(self) -> None:
        self.initialize()
        first = self.commit("First")
        second = self.commit("Second")
        third = self.commit("Third")

        output = self.git.execute("ANCESTORS", [third])

        self.assertIn(first, output)
        self.assertIn(second, output)
        self.assertNotIn(third, output)
        self.assertLess(output.index(first), output.index(second))
        self.assertEqual(self.git.execute("ANCESTORS", [first]), "No ancestors.")

    def test_keyword_search_uses_normalized_token_intersection(self) -> None:
        self.initialize()
        matching_hash = self.commit("Add Login Feature login")
        self.commit("Add payment feature")

        one_token = self.git.execute("SEARCH", ["LOGIN"])
        two_tokens = self.git.execute("SEARCH", ["login feature"])

        self.assertIn(matching_hash, one_token)
        self.assertIn(matching_hash, two_tokens)
        self.assertEqual(two_tokens.count(matching_hash), 1)
        self.assertEqual(self.git.execute("SEARCH", ["missing"]), "No commits found.")

    def test_author_search_is_case_insensitive(self) -> None:
        self.initialize()
        commit_hash = self.commit("Work")

        output = self.git.execute("search", ["--author=alice kim"])

        self.assertIn(commit_hash, output)

    def test_invalid_operations_return_standard_errors(self) -> None:
        self.assertEqual(self.git.execute("LOG", []), "Repository not initialized.")
        self.initialize()

        self.assertEqual(self.git.execute("INIT", ["Bob"]), "Repository already initialized.")
        self.assertEqual(self.git.execute("BRANCH", ["main"]), "Branch already exists: main")
        self.assertEqual(self.git.execute("SWITCH", ["missing"]), "Unknown branch: missing")
        self.assertEqual(self.git.execute("PATH", ["bad", "also-bad"]), "Unknown commit: bad")
        self.assertEqual(self.git.execute("LOG", ["--sort-by=message"]), "Invalid args")
        self.assertEqual(self.git.execute("SEARCH", ["--wrong=value"]), "Invalid args")

    def test_production_python_does_not_use_standard_sorting_apis(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        source_paths = [project_root / "main.py"]
        source_paths.extend((project_root / "mini_git").glob("*.py"))
        forbidden_function = "sort" + "ed("
        forbidden_method = "." + "sort("

        for source_path in source_paths:
            source = source_path.read_text(encoding="utf-8")
            self.assertNotIn(forbidden_function, source, source_path.name)
            self.assertNotIn(forbidden_method, source, source_path.name)

    def test_cli_readme_scenario(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        commands = "\n".join([
            'init "Alice Kim"',
            'commit "Initial commit"',
            "branch feature",
            "switch feature",
            'commit "Add login feature"',
            'search "login"',
            "quit",
            "",
        ])

        completed = subprocess.run(
            [sys.executable, "main.py"],
            cwd=project_root,
            input=commands,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("Initialized repository.", completed.stdout)
        self.assertIn("[feature c000002] Add login feature", completed.stdout)
        self.assertIn("Found 1 commit(s):", completed.stdout)


if __name__ == "__main__":
    unittest.main()
