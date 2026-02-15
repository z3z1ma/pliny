import contextlib
import io
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Callable, cast

from agent_loom.ticket import cli as ticket


_ticket_cli = cast(Callable[[list[str]], int], ticket)


def _git(args: list[str], *, cwd: Path, env: dict[str, str], check: bool = True) -> str:
    p = subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=check,
    )
    return (p.stdout or "").strip()


@contextlib.contextmanager
def _temp_git_repo():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        env = os.environ.copy()
        env.update(
            {
                "GIT_AUTHOR_NAME": "Test",
                "GIT_AUTHOR_EMAIL": "test@example.com",
                "GIT_COMMITTER_NAME": "Test",
                "GIT_COMMITTER_EMAIL": "test@example.com",
                "TEAM_SPRINT_NAME": "",
                "TEAM_SPRINT_TAG": "",
            }
        )
        _git(["init"], cwd=root, env=env)
        yield root, env


@contextlib.contextmanager
def _patched_env(env: dict[str, str]):
    before = os.environ.copy()
    os.environ.update(env)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(before)


def _ticket_json(
    argv: list[str], *, cwd: Path, env: dict[str, str]
) -> tuple[int, dict]:
    out = io.StringIO()
    err = io.StringIO()
    cwd0 = Path.cwd()
    try:
        os.chdir(cwd)
        with _patched_env(env):
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                try:
                    _ticket_cli(argv)
                    code = 0
                except SystemExit as e:
                    code = int(e.code or 0)
    finally:
        os.chdir(cwd0)

    payload = out.getvalue().strip()
    return code, (json.loads(payload) if payload else {})


class TestTicketUx(unittest.TestCase):
    def test_create_creates_top_level_ticket_file(self) -> None:
        with _temp_git_repo() as (root, env):
            tickets_dir = root / ".loom" / "ticket"
            env = {**env, "TICKET_DIR": str(tickets_dir)}

            code, created = _ticket_json(
                ["--json", "--no-audit", "create", "Test", "--no-sprint-tag"],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertTrue(created.get("ok"))
            tid = str(created.get("id") or "")
            self.assertTrue(tid)

            self.assertTrue((tickets_dir / f"{tid}.md").exists())
            self.assertFalse((tickets_dir / "closed" / f"{tid}.md").exists())

    def test_status_closed_moves_ticket_to_closed_dir(self) -> None:
        with _temp_git_repo() as (root, env):
            tickets_dir = root / ".loom" / "ticket"
            env = {**env, "TICKET_DIR": str(tickets_dir)}

            _, created = _ticket_json(
                ["--json", "--no-audit", "create", "Test", "--no-sprint-tag"],
                cwd=root,
                env=env,
            )
            tid = str(created.get("id") or "")
            self.assertTrue(tid)
            self.assertTrue((tickets_dir / f"{tid}.md").exists())

            code, st = _ticket_json(
                ["--json", "--no-audit", "status", tid, "done"],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertEqual(str(st.get("status") or ""), "closed")

            self.assertFalse((tickets_dir / f"{tid}.md").exists())
            self.assertTrue((tickets_dir / "closed" / f"{tid}.md").exists())

    def test_status_non_terminal_does_not_move_ticket_file(self) -> None:
        with _temp_git_repo() as (root, env):
            tickets_dir = root / ".loom" / "ticket"
            env = {**env, "TICKET_DIR": str(tickets_dir)}

            _, created = _ticket_json(
                ["--json", "--no-audit", "create", "Test", "--no-sprint-tag"],
                cwd=root,
                env=env,
            )
            tid = str(created.get("id") or "")
            self.assertTrue(tid)
            p = tickets_dir / f"{tid}.md"
            self.assertTrue(p.exists())

            code, _payload = _ticket_json(
                ["--json", "--no-audit", "status", tid, "review"],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertTrue(p.exists())
            self.assertFalse((tickets_dir / "closed" / f"{tid}.md").exists())

    def test_resolve_id_accepts_hash_and_md_path(self) -> None:
        with _temp_git_repo() as (root, env):
            tickets_dir = root / ".loom" / "ticket"
            env = {**env, "TICKET_DIR": str(tickets_dir)}

            _, created = _ticket_json(
                ["--json", "--no-audit", "create", "Test", "--no-sprint-tag"],
                cwd=root,
                env=env,
            )
            tid = str(created.get("id") or "")
            self.assertTrue(tid)

            for ref in [f"#{tid}", f"{tid}.md", f".loom/ticket/{tid}.md"]:
                code, shown = _ticket_json(
                    ["--json", "--no-audit", "show", ref],
                    cwd=root,
                    env=env,
                )
                self.assertEqual(code, 0)
                self.assertTrue(shown.get("ok"))
                self.assertEqual(shown["ticket"]["id"], tid)

    def test_priority_accepts_p_prefix_and_words(self) -> None:
        with _temp_git_repo() as (root, env):
            tickets_dir = root / ".loom" / "ticket"
            env = {**env, "TICKET_DIR": str(tickets_dir)}

            code, created = _ticket_json(
                [
                    "--json",
                    "--no-audit",
                    "create",
                    "Test",
                    "-p",
                    "P1",
                    "--no-sprint-tag",
                ],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertTrue(created.get("ok"))
            tid = str(created.get("id") or "")
            self.assertTrue(tid)

            code, shown = _ticket_json(
                ["--json", "--no-audit", "show", tid],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertTrue(shown.get("ok"))
            self.assertEqual(int(shown["ticket"]["priority"]), 1)

            code, _payload = _ticket_json(
                ["--json", "--no-audit", "update", tid, "--priority", "low"],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 0)

            code, shown2 = _ticket_json(
                ["--json", "--no-audit", "show", tid],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertEqual(int(shown2["ticket"]["priority"]), 3)

    def test_ready_excludes_review_and_blocked_and_supports_limit(self) -> None:
        with _temp_git_repo() as (root, env):
            tickets_dir = root / ".loom" / "ticket"
            env = {**env, "TICKET_DIR": str(tickets_dir)}

            _, created_open = _ticket_json(
                [
                    "--json",
                    "--no-audit",
                    "create",
                    "Open",
                    "--no-sprint-tag",
                ],
                cwd=root,
                env=env,
            )
            tid_open = str(created_open.get("id") or "")
            self.assertTrue(tid_open)

            _, created_review = _ticket_json(
                [
                    "--json",
                    "--no-audit",
                    "create",
                    "Review",
                    "--no-sprint-tag",
                ],
                cwd=root,
                env=env,
            )
            tid_review = str(created_review.get("id") or "")
            self.assertTrue(tid_review)

            _, created_blocked = _ticket_json(
                [
                    "--json",
                    "--no-audit",
                    "create",
                    "Blocked",
                    "--no-sprint-tag",
                ],
                cwd=root,
                env=env,
            )
            tid_blocked = str(created_blocked.get("id") or "")
            self.assertTrue(tid_blocked)

            code, _ = _ticket_json(
                ["--json", "--no-audit", "status", tid_review, "review"],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 0)

            code, _ = _ticket_json(
                ["--json", "--no-audit", "status", tid_blocked, "blocked"],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 0)

            code, ready_all = _ticket_json(
                ["--json", "--no-audit", "ready"],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 0)
            ids = [str(r.get("id") or "") for r in (ready_all.get("tickets") or [])]
            self.assertIn(tid_open, ids)
            self.assertNotIn(tid_review, ids)
            self.assertNotIn(tid_blocked, ids)

            code, ready_limited = _ticket_json(
                ["--json", "--no-audit", "ready", "--limit", "1"],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertEqual(int(ready_limited.get("count") or 0), 1)
            self.assertEqual(len(ready_limited.get("tickets") or []), 1)

            code, ready_limited_short = _ticket_json(
                ["--json", "--no-audit", "ready", "-N1"],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertEqual(int(ready_limited_short.get("count") or 0), 1)
            self.assertEqual(len(ready_limited_short.get("tickets") or []), 1)

            code, list_limited_short = _ticket_json(
                ["--json", "--no-audit", "list", "-N1"],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertEqual(int(list_limited_short.get("count") or 0), 1)
            self.assertEqual(len(list_limited_short.get("tickets") or []), 1)

    def test_sprint_context_show_set_clear(self) -> None:
        with _temp_git_repo() as (root, env):
            tickets_dir = root / ".loom" / "ticket"
            env = {**env, "TICKET_DIR": str(tickets_dir)}

            code, shown_empty = _ticket_json(
                ["--json", "--no-audit", "sprint", "show"],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertEqual(str(shown_empty.get("name") or ""), "")
            self.assertEqual(str(shown_empty.get("tag") or ""), "")

            code, set_payload = _ticket_json(
                [
                    "--json",
                    "--no-audit",
                    "sprint",
                    "set",
                    "--name",
                    "YAML Sprint Foundations",
                    "--tag",
                    "sprint:YAML-Sprint-Foundations",
                ],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertEqual(
                str(set_payload.get("name") or ""),
                "YAML Sprint Foundations",
            )
            self.assertEqual(
                str(set_payload.get("tag") or ""),
                "sprint:YAML-Sprint-Foundations",
            )

            code, shown_set = _ticket_json(
                ["--json", "--no-audit", "sprint", "show"],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertEqual(
                str(shown_set.get("name") or ""),
                "YAML Sprint Foundations",
            )
            self.assertEqual(
                str(shown_set.get("tag") or ""),
                "sprint:YAML-Sprint-Foundations",
            )

            code, cleared = _ticket_json(
                ["--json", "--no-audit", "sprint", "clear"],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertEqual(str(cleared.get("name") or ""), "")
            self.assertEqual(str(cleared.get("tag") or ""), "")


if __name__ == "__main__":
    unittest.main()
