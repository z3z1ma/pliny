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


def _ticket_json(argv: list[str], *, cwd: Path, env: dict[str, str]) -> tuple[int, dict]:
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


class TestTicketSprintContext(unittest.TestCase):
    def test_create_precedence_context_over_env_then_none(self) -> None:
        with _temp_git_repo() as (root, env):
            tickets_dir = root / ".loom" / "ticket"
            env_with_sprint = {
                **env,
                "TICKET_DIR": str(tickets_dir),
                "TEAM_SPRINT_TAG": "sprint:env",
            }

            code, created_env = _ticket_json(
                ["--json", "--no-audit", "create", "Env ticket"],
                cwd=root,
                env=env_with_sprint,
            )
            self.assertEqual(code, 0)
            tid_env = str(created_env.get("id") or "")
            self.assertTrue(tid_env)

            code, shown_env = _ticket_json(
                ["--json", "--no-audit", "show", tid_env],
                cwd=root,
                env=env_with_sprint,
            )
            self.assertEqual(code, 0)
            self.assertIn("sprint:env", shown_env["ticket"]["tags"])

            code, _ = _ticket_json(
                [
                    "--json",
                    "--no-audit",
                    "sprint",
                    "set",
                    "--name",
                    "YAML Sprint Foundations",
                    "--tag",
                    "sprint:ctx",
                ],
                cwd=root,
                env=env_with_sprint,
            )
            self.assertEqual(code, 0)

            code, created_ctx = _ticket_json(
                ["--json", "--no-audit", "create", "Context ticket"],
                cwd=root,
                env=env_with_sprint,
            )
            self.assertEqual(code, 0)
            tid_ctx = str(created_ctx.get("id") or "")
            self.assertTrue(tid_ctx)

            code, shown_ctx = _ticket_json(
                ["--json", "--no-audit", "show", tid_ctx],
                cwd=root,
                env=env_with_sprint,
            )
            self.assertEqual(code, 0)
            self.assertIn("sprint:ctx", shown_ctx["ticket"]["tags"])
            self.assertNotIn("sprint:env", shown_ctx["ticket"]["tags"])

            code, _ = _ticket_json(
                ["--json", "--no-audit", "sprint", "clear"],
                cwd=root,
                env=env_with_sprint,
            )
            self.assertEqual(code, 0)

            env_no_sprint = {**env_with_sprint, "TEAM_SPRINT_TAG": ""}
            code, created_none = _ticket_json(
                ["--json", "--no-audit", "create", "No sprint ticket"],
                cwd=root,
                env=env_no_sprint,
            )
            self.assertEqual(code, 0)
            tid_none = str(created_none.get("id") or "")
            self.assertTrue(tid_none)

            code, shown_none = _ticket_json(
                ["--json", "--no-audit", "show", tid_none],
                cwd=root,
                env=env_no_sprint,
            )
            self.assertEqual(code, 0)
            self.assertEqual(list(shown_none["ticket"]["tags"]), [])

    def test_list_precedence_context_over_env_then_none(self) -> None:
        with _temp_git_repo() as (root, env):
            tickets_dir = root / ".loom" / "ticket"
            env_with_sprint = {
                **env,
                "TICKET_DIR": str(tickets_dir),
                "TEAM_SPRINT_TAG": "sprint:env",
            }

            code, created_env = _ticket_json(
                ["--json", "--no-audit", "create", "Env ticket"],
                cwd=root,
                env=env_with_sprint,
            )
            self.assertEqual(code, 0)
            tid_env = str(created_env.get("id") or "")

            code, created_plain = _ticket_json(
                ["--json", "--no-audit", "create", "Plain ticket", "--no-sprint-tag"],
                cwd=root,
                env=env_with_sprint,
            )
            self.assertEqual(code, 0)
            tid_plain = str(created_plain.get("id") or "")

            code, listed_env = _ticket_json(
                ["--json", "--no-audit", "list"],
                cwd=root,
                env=env_with_sprint,
            )
            self.assertEqual(code, 0)
            ids_env = [str(t.get("id") or "") for t in (listed_env.get("tickets") or [])]
            self.assertIn(tid_env, ids_env)
            self.assertNotIn(tid_plain, ids_env)

            code, _ = _ticket_json(
                [
                    "--json",
                    "--no-audit",
                    "sprint",
                    "set",
                    "--name",
                    "YAML Sprint Foundations",
                    "--tag",
                    "sprint:ctx",
                ],
                cwd=root,
                env=env_with_sprint,
            )
            self.assertEqual(code, 0)

            code, created_ctx = _ticket_json(
                ["--json", "--no-audit", "create", "Context ticket"],
                cwd=root,
                env=env_with_sprint,
            )
            self.assertEqual(code, 0)
            tid_ctx = str(created_ctx.get("id") or "")

            code, listed_ctx = _ticket_json(
                ["--json", "--no-audit", "list"],
                cwd=root,
                env=env_with_sprint,
            )
            self.assertEqual(code, 0)
            ids_ctx = [str(t.get("id") or "") for t in (listed_ctx.get("tickets") or [])]
            self.assertIn(tid_ctx, ids_ctx)
            self.assertNotIn(tid_env, ids_ctx)
            self.assertNotIn(tid_plain, ids_ctx)

            code, _ = _ticket_json(
                ["--json", "--no-audit", "sprint", "clear"],
                cwd=root,
                env=env_with_sprint,
            )
            self.assertEqual(code, 0)

            env_no_sprint = {**env_with_sprint, "TEAM_SPRINT_TAG": ""}
            code, listed_none = _ticket_json(
                ["--json", "--no-audit", "list"],
                cwd=root,
                env=env_no_sprint,
            )
            self.assertEqual(code, 0)
            ids_none = [str(t.get("id") or "") for t in (listed_none.get("tickets") or [])]
            self.assertIn(tid_env, ids_none)
            self.assertIn(tid_ctx, ids_none)
            self.assertIn(tid_plain, ids_none)

    def test_list_explicit_tag_overrides_default_sprint_filter(self) -> None:
        with _temp_git_repo() as (root, env):
            tickets_dir = root / ".loom" / "ticket"
            env_with_sprint = {
                **env,
                "TICKET_DIR": str(tickets_dir),
                "TEAM_SPRINT_TAG": "sprint:env",
            }

            code, created_env_manual = _ticket_json(
                [
                    "--json",
                    "--no-audit",
                    "create",
                    "Env manual",
                    "--no-sprint-tag",
                    "--tags",
                    "sprint:env",
                ],
                cwd=root,
                env=env_with_sprint,
            )
            self.assertEqual(code, 0)
            tid_env_manual = str(created_env_manual.get("id") or "")

            code, _ = _ticket_json(
                [
                    "--json",
                    "--no-audit",
                    "sprint",
                    "set",
                    "--name",
                    "YAML Sprint Foundations",
                    "--tag",
                    "sprint:ctx",
                ],
                cwd=root,
                env=env_with_sprint,
            )
            self.assertEqual(code, 0)

            code, created_ctx = _ticket_json(
                ["--json", "--no-audit", "create", "Context ticket"],
                cwd=root,
                env=env_with_sprint,
            )
            self.assertEqual(code, 0)
            tid_ctx = str(created_ctx.get("id") or "")

            code, listed_default = _ticket_json(
                ["--json", "--no-audit", "list"],
                cwd=root,
                env=env_with_sprint,
            )
            self.assertEqual(code, 0)
            ids_default = [
                str(t.get("id") or "") for t in (listed_default.get("tickets") or [])
            ]
            self.assertIn(tid_ctx, ids_default)
            self.assertNotIn(tid_env_manual, ids_default)

            code, listed_explicit = _ticket_json(
                ["--json", "--no-audit", "list", "--tag", "sprint:env"],
                cwd=root,
                env=env_with_sprint,
            )
            self.assertEqual(code, 0)
            ids_explicit = [
                str(t.get("id") or "") for t in (listed_explicit.get("tickets") or [])
            ]
            self.assertIn(tid_env_manual, ids_explicit)
            self.assertNotIn(tid_ctx, ids_explicit)


if __name__ == "__main__":
    unittest.main()
