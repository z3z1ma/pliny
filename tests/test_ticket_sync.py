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


class TestTicketSync(unittest.TestCase):
    def test_noop(self) -> None:
        with _temp_git_repo() as (root, env):
            env = {**env, "TICKET_DIR": str(root / ".tickets")}
            (root / ".tickets").mkdir(parents=True)
            (root / ".tickets" / "a.md").write_text("# A\n", encoding="utf-8")
            _git(["add", "-A"], cwd=root, env=env)
            _git(["commit", "-m", "init"], cwd=root, env=env)

            before = _git(["rev-parse", "HEAD"], cwd=root, env=env)
            code, payload = _ticket_json(
                ["--json", "--no-audit", "sync"], cwd=root, env=env
            )
            after = _git(["rev-parse", "HEAD"], cwd=root, env=env)

            self.assertEqual(code, 0)
            self.assertTrue(payload.get("ok"))
            self.assertEqual(payload.get("committed"), False)
            self.assertEqual(before, after)

    def test_creates_commit(self) -> None:
        with _temp_git_repo() as (root, env):
            env = {**env, "TICKET_DIR": str(root / ".tickets")}
            (root / ".tickets").mkdir(parents=True)
            (root / ".tickets" / "a.md").write_text("# A\n", encoding="utf-8")
            _git(["add", "-A"], cwd=root, env=env)
            _git(["commit", "-m", "init"], cwd=root, env=env)

            (root / ".tickets" / "a.md").write_text(
                "# A\n\nupdated\n", encoding="utf-8"
            )
            code, payload = _ticket_json(
                ["--json", "--no-audit", "sync"], cwd=root, env=env
            )

            self.assertEqual(code, 0)
            self.assertTrue(payload.get("ok"))
            self.assertEqual(payload.get("committed"), True)
            self.assertEqual(payload.get("message"), "chore: tickets")
            self.assertEqual(payload.get("files"), [".tickets/a.md"])

            self.assertEqual(
                _git(["log", "-1", "--pretty=%B"], cwd=root, env=env), "chore: tickets"
            )
            shown = _git(["show", "--name-only", "--pretty=format:"], cwd=root, env=env)
            self.assertEqual(
                [p for p in shown.splitlines() if p.strip()], [".tickets/a.md"]
            )
            self.assertEqual(_git(["status", "--porcelain"], cwd=root, env=env), "")

    def test_commits_tickets_even_when_other_changes_present(self) -> None:
        with _temp_git_repo() as (root, env):
            env = {**env, "TICKET_DIR": str(root / ".tickets")}
            (root / ".tickets").mkdir(parents=True)
            (root / ".tickets" / "a.md").write_text("# A\n", encoding="utf-8")
            (root / "other.txt").write_text("x\n", encoding="utf-8")
            _git(["add", "-A"], cwd=root, env=env)
            _git(["commit", "-m", "init"], cwd=root, env=env)

            (root / ".tickets" / "a.md").write_text(
                "# A\n\nupdated\n", encoding="utf-8"
            )
            (root / "other.txt").write_text("y\n", encoding="utf-8")
            code, payload = _ticket_json(
                ["--json", "--no-audit", "sync"], cwd=root, env=env
            )

            self.assertEqual(code, 0)
            self.assertTrue(payload.get("ok"))
            self.assertEqual(payload.get("committed"), True)

            shown = _git(["show", "--name-only", "--pretty=format:"], cwd=root, env=env)
            self.assertEqual(
                [p for p in shown.splitlines() if p.strip()], [".tickets/a.md"]
            )

            status = _git(["status", "--porcelain"], cwd=root, env=env)
            self.assertIn("other.txt", status)
            self.assertNotIn(".tickets/a.md", status)


if __name__ == "__main__":
    unittest.main()
