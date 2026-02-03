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


def _ticket_text(argv: list[str], *, cwd: Path, env: dict[str, str]) -> tuple[int, str]:
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

    return code, out.getvalue()


class TestTicketUx(unittest.TestCase):
    def test_priority_accepts_p_prefix_and_words(self) -> None:
        with _temp_git_repo() as (root, env):
            env = {**env, "TICKET_DIR": str(root / ".tickets")}

            code, created = _ticket_json(
                ["--json", "--no-audit", "create", "Test", "-p", "P1"],
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

            code, created2 = _ticket_json(
                ["--json", "--no-audit", "create", "Test2", "-p", "high"],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 0)
            tid2 = str(created2.get("id") or "")
            code, shown2 = _ticket_json(
                ["--json", "--no-audit", "show", tid2],
                cwd=root,
                env=env,
            )
            self.assertEqual(int(shown2["ticket"]["priority"]), 1)

    def test_update_priority_accepts_words(self) -> None:
        with _temp_git_repo() as (root, env):
            env = {**env, "TICKET_DIR": str(root / ".tickets")}

            _, created = _ticket_json(
                ["--json", "--no-audit", "create", "Test"], cwd=root, env=env
            )
            tid = str(created.get("id") or "")

            code, upd = _ticket_json(
                ["--json", "--no-audit", "update", tid, "--priority", "low"],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertTrue(upd.get("ok"))

            code, shown = _ticket_json(
                ["--json", "--no-audit", "show", tid], cwd=root, env=env
            )
            self.assertEqual(code, 0)
            self.assertEqual(int(shown["ticket"]["priority"]), 3)

    def test_status_accepts_common_aliases(self) -> None:
        with _temp_git_repo() as (root, env):
            env = {**env, "TICKET_DIR": str(root / ".tickets")}

            _, created = _ticket_json(
                ["--json", "--no-audit", "create", "Test"], cwd=root, env=env
            )
            tid = str(created.get("id") or "")

            code, st = _ticket_json(
                ["--json", "--no-audit", "status", tid, "done"],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertEqual(st.get("status"), "closed")

            code, shown = _ticket_json(
                ["--json", "--no-audit", "show", tid], cwd=root, env=env
            )
            self.assertEqual(code, 0)
            self.assertEqual(shown["ticket"]["status"], "closed")

    def test_status_accepts_canonical_workflow_states(self) -> None:
        with _temp_git_repo() as (root, env):
            env = {**env, "TICKET_DIR": str(root / ".tickets")}

            _, created = _ticket_json(
                ["--json", "--no-audit", "create", "Test"], cwd=root, env=env
            )
            tid = str(created.get("id") or "")
            self.assertTrue(tid)

            for st in ["ready", "blocked", "review"]:
                code, payload = _ticket_json(
                    ["--json", "--no-audit", "status", tid, st], cwd=root, env=env
                )
                self.assertEqual(code, 0)
                self.assertTrue(payload.get("ok"))
                self.assertEqual(payload.get("status"), st)

                code, shown = _ticket_json(
                    ["--json", "--no-audit", "show", tid], cwd=root, env=env
                )
                self.assertEqual(code, 0)
                self.assertTrue(shown.get("ok"))
                self.assertEqual(shown["ticket"]["status"], st)

    def test_status_rejects_invalid(self) -> None:
        with _temp_git_repo() as (root, env):
            env = {**env, "TICKET_DIR": str(root / ".tickets")}

            _, created = _ticket_json(
                ["--json", "--no-audit", "create", "Test"], cwd=root, env=env
            )
            tid = str(created.get("id") or "")

            code, err = _ticket_json(
                ["--json", "--no-audit", "status", tid, "nope"], cwd=root, env=env
            )
            self.assertEqual(code, 2)
            self.assertFalse(err.get("ok"))
            self.assertEqual(err.get("code"), "ARG")
            msg = str(err.get("error") or "")
            for required in [
                "open",
                "ready",
                "in_progress",
                "blocked",
                "review",
                "closed",
            ]:
                self.assertIn(required, msg)

    def test_create_title_flag_and_positional_conflict(self) -> None:
        with _temp_git_repo() as (root, env):
            env = {**env, "TICKET_DIR": str(root / ".tickets")}

            code, created = _ticket_json(
                [
                    "--json",
                    "--no-audit",
                    "create",
                    "Hello",
                    "--title",
                    "Hello",
                ],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 0)
            tid = str(created.get("id") or "")
            code, shown = _ticket_json(
                ["--json", "--no-audit", "show", tid], cwd=root, env=env
            )
            self.assertEqual(shown["ticket"]["title"], "Hello")

            code, err = _ticket_json(
                [
                    "--json",
                    "--no-audit",
                    "create",
                    "Positional",
                    "--title",
                    "Flag",
                ],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 2)
            self.assertFalse(err.get("ok"))

    def test_create_auto_adds_sprint_tag_when_set(self) -> None:
        with _temp_git_repo() as (root, env):
            env = {
                **env,
                "TICKET_DIR": str(root / ".tickets"),
                "TEAM_SPRINT_TAG": "sprint:alpha",
            }

            _, created = _ticket_json(
                ["--json", "--no-audit", "create", "Test"], cwd=root, env=env
            )
            tid = str(created.get("id") or "")
            self.assertTrue(tid)

            _, shown = _ticket_json(
                ["--json", "--no-audit", "show", tid], cwd=root, env=env
            )
            self.assertIn("sprint:alpha", shown["ticket"]["tags"])

            _, created2 = _ticket_json(
                [
                    "--json",
                    "--no-audit",
                    "create",
                    "Test2",
                    "--tags",
                    "foo,bar",
                ],
                cwd=root,
                env=env,
            )
            tid2 = str(created2.get("id") or "")
            _, shown2 = _ticket_json(
                ["--json", "--no-audit", "show", tid2], cwd=root, env=env
            )
            self.assertIn("sprint:alpha", shown2["ticket"]["tags"])
            self.assertIn("foo", shown2["ticket"]["tags"])
            self.assertIn("bar", shown2["ticket"]["tags"])

            _, created3 = _ticket_json(
                ["--json", "--no-audit", "create", "Test3", "--no-sprint-tag"],
                cwd=root,
                env=env,
            )
            tid3 = str(created3.get("id") or "")
            _, shown3 = _ticket_json(
                ["--json", "--no-audit", "show", tid3], cwd=root, env=env
            )
            self.assertNotIn("sprint:alpha", shown3["ticket"]["tags"])

    def test_resolve_id_accepts_md_suffix_paths_and_hash(self) -> None:
        with _temp_git_repo() as (root, env):
            env = {**env, "TICKET_DIR": str(root / ".tickets")}

            _, created = _ticket_json(
                ["--json", "--no-audit", "create", "Test"], cwd=root, env=env
            )
            tid = str(created.get("id") or "")

            for ref in [f"{tid}.md", f".tickets/{tid}.md", f"#{tid}"]:
                code, shown = _ticket_json(
                    ["--json", "--no-audit", "show", ref], cwd=root, env=env
                )
                self.assertEqual(code, 0)
                self.assertEqual(shown["ticket"]["id"], tid)

    def test_list_limit_restricts_results(self) -> None:
        with _temp_git_repo() as (root, env):
            env = {**env, "TICKET_DIR": str(root / ".tickets")}

            code, created1 = _ticket_json(
                ["--json", "--no-audit", "create", "One"], cwd=root, env=env
            )
            self.assertEqual(code, 0)
            self.assertTrue(str(created1.get("id") or ""))

            code, created2 = _ticket_json(
                ["--json", "--no-audit", "create", "Two"], cwd=root, env=env
            )
            self.assertEqual(code, 0)
            self.assertTrue(str(created2.get("id") or ""))

            code, listed = _ticket_json(
                ["--json", "--no-audit", "list", "--limit", "1"],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertTrue(listed.get("ok"))
            self.assertEqual(int(listed.get("count") or 0), 1)
            self.assertEqual(len(list(listed.get("tickets") or [])), 1)

    def test_list_limit_rejects_negative(self) -> None:
        with _temp_git_repo() as (root, env):
            env = {**env, "TICKET_DIR": str(root / ".tickets")}

            code, err = _ticket_json(
                ["--json", "--no-audit", "list", "--limit", "-1"], cwd=root, env=env
            )
            self.assertEqual(code, 2)
            self.assertFalse(err.get("ok"))
            self.assertEqual(str(err.get("code") or ""), "ARG")

    def test_error_payload_includes_code_and_hint(self) -> None:
        with _temp_git_repo() as (root, env):
            env = {**env, "TICKET_DIR": str(root / ".tickets")}

            code, payload = _ticket_json(
                ["--json", "--no-audit", "show", "nope"], cwd=root, env=env
            )
            self.assertEqual(code, 2)
            self.assertFalse(payload.get("ok"))
            self.assertEqual(payload.get("code"), "NOT_FOUND")
            self.assertTrue(str(payload.get("hint") or ""))

    def test_add_note_empty_has_actionable_hint(self) -> None:
        with _temp_git_repo() as (root, env):
            env = {**env, "TICKET_DIR": str(root / ".tickets")}
            _, created = _ticket_json(
                ["--json", "--no-audit", "create", "Test"], cwd=root, env=env
            )
            tid = str(created.get("id") or "")

            code, payload = _ticket_json(
                ["--json", "--no-audit", "add-note", tid], cwd=root, env=env
            )
            self.assertEqual(code, 2)
            self.assertEqual(payload.get("code"), "ARG")
            self.assertIn("pipe", str(payload.get("hint") or "").lower())

    def test_add_note_accepts_note_and_body_flags(self) -> None:
        with _temp_git_repo() as (root, env):
            env = {**env, "TICKET_DIR": str(root / ".tickets")}
            _, created = _ticket_json(
                ["--json", "--no-audit", "create", "Test"], cwd=root, env=env
            )
            tid = str(created.get("id") or "")

            code, payload = _ticket_json(
                ["--json", "--no-audit", "add-note", tid, "--note", "Hello"],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertTrue(payload.get("ok"))

            code, payload2 = _ticket_json(
                ["--json", "--no-audit", "add-note", tid, "--body", "World"],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertTrue(payload2.get("ok"))

            _, shown = _ticket_json(
                ["--json", "--no-audit", "show", tid], cwd=root, env=env
            )
            self.assertIn("Hello", str(shown.get("body") or ""))
            self.assertIn("World", str(shown.get("body") or ""))

    def test_add_note_rejects_conflicting_positional_and_flag(self) -> None:
        with _temp_git_repo() as (root, env):
            env = {**env, "TICKET_DIR": str(root / ".tickets")}
            _, created = _ticket_json(
                ["--json", "--no-audit", "create", "Test"], cwd=root, env=env
            )
            tid = str(created.get("id") or "")

            code, payload = _ticket_json(
                [
                    "--json",
                    "--no-audit",
                    "add-note",
                    tid,
                    "positional",
                    "--note",
                    "flag",
                ],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 2)
            self.assertFalse(payload.get("ok"))
            self.assertEqual(payload.get("code"), "ARG")

    def test_note_command_is_alias_for_add_note(self) -> None:
        with _temp_git_repo() as (root, env):
            env = {**env, "TICKET_DIR": str(root / ".tickets")}
            _, created = _ticket_json(
                ["--json", "--no-audit", "create", "Test"], cwd=root, env=env
            )
            tid = str(created.get("id") or "")

            code, payload = _ticket_json(
                ["--json", "--no-audit", "note", tid, "Hello"], cwd=root, env=env
            )
            self.assertEqual(code, 0)
            self.assertTrue(payload.get("ok"))

            _, shown = _ticket_json(
                ["--json", "--no-audit", "show", tid], cwd=root, env=env
            )
            self.assertIn("Hello", str(shown.get("body") or ""))

    def test_update_add_note_alias_routes_to_add_note(self) -> None:
        with _temp_git_repo() as (root, env):
            env = {**env, "TICKET_DIR": str(root / ".tickets")}
            _, created = _ticket_json(
                ["--json", "--no-audit", "create", "Test"], cwd=root, env=env
            )
            tid = str(created.get("id") or "")

            code, payload = _ticket_json(
                [
                    "--json",
                    "--no-audit",
                    "update",
                    tid,
                    "--add-note",
                    "Hello",
                ],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertTrue(payload.get("ok"))

            _, shown = _ticket_json(
                ["--json", "--no-audit", "show", tid], cwd=root, env=env
            )
            self.assertIn("Hello", str(shown.get("body") or ""))

    def test_update_add_note_empty_has_actionable_hint(self) -> None:
        with _temp_git_repo() as (root, env):
            env = {**env, "TICKET_DIR": str(root / ".tickets")}
            _, created = _ticket_json(
                ["--json", "--no-audit", "create", "Test"], cwd=root, env=env
            )
            tid = str(created.get("id") or "")

            code, payload = _ticket_json(
                ["--json", "--no-audit", "update", tid, "--add-note"],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 2)
            self.assertEqual(payload.get("code"), "ARG")
            self.assertIn("pipe", str(payload.get("hint") or "").lower())

    def test_argv_normalization_accepts_ticket_dir_alias_and_glued_priority(
        self,
    ) -> None:
        with _temp_git_repo() as (root, env):
            tickets_dir = root / ".tickets"
            env = {**env}

            code, created = _ticket_json(
                [
                    "--json",
                    "--no-audit",
                    "--ticket-dir",
                    str(tickets_dir),
                    "create",
                    "Test",
                    "-p1",
                ],
                cwd=root,
                env=env,
            )
            self.assertEqual(code, 0)
            self.assertTrue(created.get("ok"))

    def test_ambiguous_id_returns_matches(self) -> None:
        with _temp_git_repo() as (root, env):
            env = {**env, "TICKET_DIR": str(root / ".tickets")}

            _, created1 = _ticket_json(
                ["--json", "--no-audit", "create", "A"], cwd=root, env=env
            )
            _, created2 = _ticket_json(
                ["--json", "--no-audit", "create", "B"], cwd=root, env=env
            )
            tid1 = str(created1.get("id") or "")
            tid2 = str(created2.get("id") or "")
            self.assertTrue(tid1)
            self.assertTrue(tid2)

            prefix = tid1.split("-")[0] + "-"
            code, payload = _ticket_json(
                ["--json", "--no-audit", "show", prefix], cwd=root, env=env
            )
            self.assertEqual(code, 2)
            self.assertEqual(payload.get("code"), "ARG")
            details = payload.get("details") or {}
            self.assertIn("matches", details)
            matches = list(details.get("matches") or [])
            self.assertIn(tid1, matches)
            self.assertIn(tid2, matches)

    def test_require_claim_enforcement_has_actionable_error(self) -> None:
        with _temp_git_repo() as (root, env):
            env0 = {**env, "TICKET_DIR": str(root / ".tickets")}
            _, created = _ticket_json(
                ["--json", "--no-audit", "create", "A"], cwd=root, env=env0
            )
            tid = str(created.get("id") or "")

            env1 = {**env0, "TK_REQUIRE_CLAIM": "1"}
            code, payload = _ticket_json(
                ["--json", "--no-audit", "update", tid, "--title", "B"],
                cwd=root,
                env=env1,
            )
            self.assertEqual(code, 2)
            self.assertEqual(payload.get("code"), "PERMISSION")
            self.assertIn("claim", str(payload.get("error") or "").lower())

    def test_prime_prints_cookbook(self) -> None:
        with _temp_git_repo() as (root, env):
            code, text = _ticket_text(["prime"], cwd=root, env=env)
            self.assertEqual(code, 0)
            self.assertIn("Ticket Cookbook", text)
            self.assertIn("loom ticket create", text)

    def test_prime_json_includes_markdown(self) -> None:
        with _temp_git_repo() as (root, env):
            code, payload = _ticket_json(["--json", "prime"], cwd=root, env=env)
            self.assertEqual(code, 0)
            self.assertTrue(payload.get("ok"))
            content = str((payload.get("payload") or {}).get("markdown") or "")
            self.assertIn("Ticket Cookbook", content)


if __name__ == "__main__":
    unittest.main()
