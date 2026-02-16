import contextlib
import io
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Callable, cast
from unittest import mock

from agent_loom.team import core as team
from agent_loom.team.run_state import RunPaths
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
    @staticmethod
    def _seed_team_run(root: Path, *, team_name: str = "CobraKai") -> RunPaths:
        paths = RunPaths(repo_root=root, team=team_name)
        paths.run_dir.mkdir(parents=True, exist_ok=True)
        paths.events_dir.mkdir(parents=True, exist_ok=True)
        run_payload = {
            "team": team_name,
            "run_id": "1234567890abcdef",
            "session": f"team-{team_name.lower()}",
            "repo_root": str(root),
            "objective": "Ship sprint context sync.",
            "objective_rev": 1,
            "objective_updated_at": "",
            "harness": "opencode",
            "opencode": {"model": "", "models": {}},
            "workers": {},
            "merge": {"items": [], "config": {}},
            "sprint": {},
        }
        paths.run_file.write_text(json.dumps(run_payload, indent=2), encoding="utf-8")
        return paths

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

    def test_team_sprint_set_syncs_context_for_stale_env_ticket_create(self) -> None:
        with _temp_git_repo() as (root, env):
            paths = self._seed_team_run(root)
            with (
                mock.patch.object(team, "_require_role"),
                mock.patch.object(team, "_paths_for", return_value=paths),
            ):
                result = team.sprint_set(team=paths.team, name="Refinement Sprint")

            stale_env = {
                **env,
                "TICKET_DIR": str(root / ".loom" / "ticket"),
                "TEAM_SPRINT_TAG": "sprint:stale-pane",
            }
            code, created = _ticket_json(
                ["--json", "--no-audit", "create", "Ticket after team sprint set"],
                cwd=root,
                env=stale_env,
            )
            self.assertEqual(code, 0)
            ticket_id = str(created.get("id") or "")
            self.assertTrue(ticket_id)

            code, shown = _ticket_json(
                ["--json", "--no-audit", "show", ticket_id],
                cwd=root,
                env=stale_env,
            )
            self.assertEqual(code, 0)
            self.assertIn(str(result.sprint["tag"]), shown["ticket"]["tags"])
            self.assertNotIn("sprint:stale-pane", shown["ticket"]["tags"])

    def test_team_prep_sprint_syncs_context_for_stale_env_ticket_create(self) -> None:
        with _temp_git_repo() as (root, env):
            paths = self._seed_team_run(root)
            with (
                mock.patch.object(team, "_require_role"),
                mock.patch.object(team, "_paths_for", return_value=paths),
                mock.patch.object(team, "_inbox_write_and_maybe_nudge"),
            ):
                result = team.prep_sprint(
                    team=paths.team,
                    name="Prep Sprint",
                    notify_architect=False,
                )

            stale_env = {
                **env,
                "TICKET_DIR": str(root / ".loom" / "ticket"),
                "TEAM_SPRINT_TAG": "sprint:stale-pane",
            }
            code, created = _ticket_json(
                ["--json", "--no-audit", "create", "Ticket after team prep sprint"],
                cwd=root,
                env=stale_env,
            )
            self.assertEqual(code, 0)
            ticket_id = str(created.get("id") or "")
            self.assertTrue(ticket_id)

            code, shown = _ticket_json(
                ["--json", "--no-audit", "show", ticket_id],
                cwd=root,
                env=stale_env,
            )
            self.assertEqual(code, 0)
            self.assertIn(str(result.sprint["tag"]), shown["ticket"]["tags"])
            self.assertNotIn("sprint:stale-pane", shown["ticket"]["tags"])


if __name__ == "__main__":
    unittest.main()
