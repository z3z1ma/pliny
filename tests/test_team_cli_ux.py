import contextlib
import io
import importlib
import json
import os
import unittest
import tempfile
from pathlib import Path
from typing import Callable, cast
from unittest import mock

from agent_loom.team.models import InboxAckResult

team = importlib.import_module("agent_loom.team.cli")


_team_cli = cast(Callable[[list[str]], int], getattr(team, "main"))


@contextlib.contextmanager
def _patched_env(env: dict[str, str]):
    before = os.environ.copy()
    os.environ.update(env)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(before)


def _team_json(argv: list[str]) -> tuple[int, dict]:
    out = io.StringIO()
    err = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = _team_cli(argv)
    payload = out.getvalue().strip()
    return code, (json.loads(payload) if payload else {})


def _team_text(argv: list[str]) -> tuple[int, str, str]:
    out = io.StringIO()
    err = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = _team_cli(argv)
    return code, out.getvalue(), err.getvalue()


class TestTeamCliUx(unittest.TestCase):
    def test_init_is_json_contract(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            with (
                mock.patch(
                    "agent_loom.team.core.canonical_repo_root", return_value=repo_root
                ),
                mock.patch("agent_loom.team.core._require_bin"),
            ):
                code, payload = _team_json(["--json", "--repo", td, "init"])
        self.assertEqual(code, 0)
        self.assertTrue(bool(payload.get("ok")))
        self.assertEqual(str(payload.get("repo_root") or ""), str(repo_root))
        self.assertFalse(list(payload.get("missing") or []))
        self.assertTrue(
            list(payload.get("wrote") or []) or list(payload.get("updated") or [])
        )

    def test_start_errors_when_agents_not_initialized(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            with (
                mock.patch(
                    "agent_loom.team.core.canonical_repo_root", return_value=repo_root
                ),
                mock.patch("agent_loom.team.core._require_bin"),
            ):
                code, payload = _team_json(["--json", "--repo", td, "start", "MyTeam"])
        self.assertEqual(code, 2)
        self.assertFalse(bool(payload.get("ok")))
        self.assertEqual(str(payload.get("code") or ""), "AGENTS")
        self.assertIn("loom team init", str(payload.get("hint") or ""))

    def test_unknown_command_is_json_contract(self) -> None:
        with _patched_env({"TMUX": ""}):
            code, payload = _team_json(["--json", "nope"])
        self.assertEqual(code, 2)
        self.assertFalse(payload.get("ok"))
        self.assertEqual(payload.get("code"), "ARGPARSE")
        self.assertTrue(str(payload.get("error") or ""))
        self.assertTrue(str(payload.get("hint") or ""))

    def test_wait_requires_team_outside_tmux(self) -> None:
        with _patched_env({"TMUX": ""}):
            code, payload = _team_json(["--json", "wait", "5m"])
        self.assertEqual(code, 2)
        self.assertFalse(payload.get("ok"))
        self.assertEqual(payload.get("code"), "ARG")
        self.assertIn("team", str(payload.get("error") or "").lower())
        self.assertTrue(str(payload.get("hint") or ""))

    def test_normalize_objective_positional_message(self) -> None:
        argv = ["objective", "MyTeam", "set", "Ship", "it"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "message", "") or ""), "Ship it")

    def test_normalize_inbox_send_positional_to_message(self) -> None:
        argv = ["inbox", "MyTeam", "send", "manager", "hello", "there"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "to", "") or ""), "manager")
        self.assertEqual(str(getattr(args, "message", "") or ""), "hello there")

    def test_normalize_inbox_defaults_to_list(self) -> None:
        argv = ["inbox", "MyTeam"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "inbox_cmd", "") or ""), "list")

    def test_normalize_inbox_list_alias_ls(self) -> None:
        argv = ["inbox", "MyTeam", "ls"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "inbox_cmd", "") or ""), "list")

    def test_normalize_inbox_list_alias_queue(self) -> None:
        argv = ["inbox", "MyTeam", "queue"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "inbox_cmd", "") or ""), "list")

    def test_normalize_inbox_list_flag_without_subcommand(self) -> None:
        argv = ["inbox", "MyTeam", "--unacked"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "inbox_cmd", "") or ""), "list")
        self.assertTrue(bool(getattr(args, "unacked", False)))

    def test_normalize_inbox_list_limit_positional(self) -> None:
        argv = ["inbox", "MyTeam", "list", "10"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(int(getattr(args, "limit", 0)), 10)

    def test_normalize_inbox_list_unread_positional(self) -> None:
        argv = ["inbox", "MyTeam", "list", "unread"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertTrue(bool(getattr(args, "unacked", False)))

    def test_normalize_inbox_show_id_flag(self) -> None:
        argv = ["inbox", "MyTeam", "show", "--id", "abc123"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "msg_id", "") or ""), "abc123")

    def test_normalize_inbox_ack_id_flag(self) -> None:
        argv = ["inbox", "MyTeam", "ack", "--id", "abc123"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "msg_id", "") or ""), "abc123")

    def test_normalize_inbox_send_flags_after_message(self) -> None:
        argv = ["inbox", "MyTeam", "send", "manager", "hello", "--kind", "note"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "to", "") or ""), "manager")
        self.assertEqual(str(getattr(args, "message", "") or ""), "hello")
        self.assertEqual(str(getattr(args, "kind", "") or ""), "note")

    def test_normalize_inbox_send_flags_before_message(self) -> None:
        argv = ["inbox", "MyTeam", "send", "manager", "--kind", "note", "hello"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "to", "") or ""), "manager")
        self.assertEqual(str(getattr(args, "message", "") or ""), "hello")
        self.assertEqual(str(getattr(args, "kind", "") or ""), "note")

    def test_normalize_inbox_send_positional_message_with_to_flag(self) -> None:
        argv = ["inbox", "MyTeam", "send", "--to", "manager", "hello"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "to", "") or ""), "manager")
        self.assertEqual(str(getattr(args, "message", "") or ""), "hello")

    def test_normalize_inbox_send_message_flag_with_positional_to(self) -> None:
        argv = ["inbox", "MyTeam", "send", "manager", "--message", "hello"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "to", "") or ""), "manager")
        self.assertEqual(str(getattr(args, "message", "") or ""), "hello")

    def test_normalize_merge_enqueue_positional_branch(self) -> None:
        argv = ["merge", "MyTeam", "enqueue", "team/abc"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "branch", "") or ""), "team/abc")

    def test_normalize_merge_list_alias_ls(self) -> None:
        argv = ["merge", "MyTeam", "ls"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "merge_cmd", "") or ""), "list")

    def test_normalize_merge_list_alias_queue(self) -> None:
        argv = ["merge", "MyTeam", "queue"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "merge_cmd", "") or ""), "list")

    def test_normalize_merge_defaults_to_list(self) -> None:
        argv = ["merge", "MyTeam"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "merge_cmd", "") or ""), "list")

    def test_normalize_merge_list_all_flag_without_subcommand(self) -> None:
        argv = ["merge", "MyTeam", "--all"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "merge_cmd", "") or ""), "list")
        self.assertTrue(bool(getattr(args, "all", False)))

    def test_normalize_merge_list_include_done_flag_alias(self) -> None:
        argv = ["merge", "MyTeam", "list", "--include-done"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertTrue(bool(getattr(args, "all", False)))

    def test_normalize_merge_list_all_positional(self) -> None:
        argv = ["merge", "MyTeam", "list", "all"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertTrue(bool(getattr(args, "all", False)))

    def test_normalize_merge_enqueue_positional_branch_with_flags(self) -> None:
        argv = ["merge", "MyTeam", "enqueue", "team/abc", "--ticket", "tk-1"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "branch", "") or ""), "team/abc")
        self.assertEqual(str(getattr(args, "ticket", "") or ""), "tk-1")

    def test_normalize_merge_done_positional_result(self) -> None:
        argv = ["merge", "MyTeam", "done", "item123", "MERGED"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "result", "") or ""), "merged")

    def test_normalize_merge_done_positional_result_with_note(self) -> None:
        argv = [
            "merge",
            "MyTeam",
            "done",
            "item123",
            "blocked",
            "--note",
            "needs rebase",
        ]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "result", "") or ""), "blocked")
        self.assertEqual(str(getattr(args, "note", "") or ""), "needs rebase")

    def test_normalize_merge_next_positional_claim_by(self) -> None:
        argv = ["merge", "MyTeam", "next", "integrator"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "claim_by", "") or ""), "integrator")

    def test_send_accepts_message_flag(self) -> None:
        argv = ["send", "MyTeam", "manager", "--message", "hello there"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "team", "") or ""), "MyTeam")
        self.assertEqual(str(getattr(args, "target", "") or ""), "manager")
        self.assertEqual(str(getattr(args, "message_opt", "") or ""), "hello there")

    def test_normalize_role_alias_inv(self) -> None:
        argv = ["spawn", "MyTeam", "tk-123", "--role", "inv"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "role", "") or ""), "investigator")

    def test_normalize_clock_in_two_words(self) -> None:
        argv = ["clock", "in", "MyTeam"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "cmd", "") or ""), "clock-in")
        self.assertEqual(str(getattr(args, "team", "") or ""), "MyTeam")

    def test_normalize_clock_out_two_words(self) -> None:
        argv = ["clock", "out", "MyTeam"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "cmd", "") or ""), "clock-out")
        self.assertEqual(str(getattr(args, "team", "") or ""), "MyTeam")

    def test_resume_is_team_resume(self) -> None:
        argv = ["resume", "MyTeam"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "cmd", "") or ""), "resume")
        self.assertEqual(str(getattr(args, "team", "") or ""), "MyTeam")

    def test_resume_worker_is_worker_resume(self) -> None:
        argv = ["resume-worker", "MyTeam", "w1"]
        norm = team._normalize_argv(argv)
        args = team.build_parser().parse_args(norm)
        self.assertEqual(str(getattr(args, "cmd", "") or ""), "resume-worker")
        self.assertEqual(str(getattr(args, "team", "") or ""), "MyTeam")
        self.assertEqual(str(getattr(args, "worker_id", "") or ""), "w1")

    def test_inbox_ack_prints_full_message_body(self) -> None:
        res = InboxAckResult(
            team="MyTeam",
            message={
                "id": "abc123",
                "created_at": "2026-01-31T00:00:00Z",
                "from": "manager",
                "to": "worker-1",
                "kind": "note",
                "message": "hello\nthere",
                "acked_at": "2026-01-31T00:01:00Z",
            },
        )

        with (
            _patched_env({"TMUX": ""}),
            mock.patch.object(team, "inbox_ack", return_value=res),
        ):
            code, out, err = _team_text(["inbox", "MyTeam", "ack", "abc123"])

        self.assertEqual(code, 0)
        self.assertEqual(err, "")
        self.assertEqual(
            out,
            "".join(
                [
                    "id: abc123\n",
                    "from: manager\n",
                    "to: worker-1\n",
                    "kind: note\n",
                    "created_at: 2026-01-31T00:00:00Z\n",
                    "acked_at: 2026-01-31T00:01:00Z\n",
                    "\n",
                    "hello\n",
                    "there\n",
                    "\n",
                    "acked id=abc123\n",
                ]
            ),
        )

    def test_inbox_ack_json_includes_full_message(self) -> None:
        res = InboxAckResult(
            team="MyTeam",
            message={
                "id": "abc123",
                "created_at": "2026-01-31T00:00:00Z",
                "from": "manager",
                "to": "worker-1",
                "kind": "note",
                "message": "hello\nthere",
                "acked_at": "2026-01-31T00:01:00Z",
            },
        )

        with (
            _patched_env({"TMUX": ""}),
            mock.patch.object(team, "inbox_ack", return_value=res),
        ):
            code, payload = _team_json(["--json", "inbox", "MyTeam", "ack", "abc123"])

        self.assertEqual(code, 0)
        msg = payload.get("message") or {}
        self.assertEqual(str(msg.get("id") or ""), "abc123")
        self.assertEqual(str(msg.get("message") or ""), "hello\nthere")

    def test_prime_prints_cookbook(self) -> None:
        code, out, err = _team_text(["prime"])
        self.assertEqual(code, 0)
        self.assertEqual(err, "")
        self.assertIn("Team Cookbook", out)
        self.assertIn("loom team start", out)

    def test_prime_json_includes_markdown(self) -> None:
        code, payload = _team_json(["--json", "prime"])
        self.assertEqual(code, 0)
        self.assertTrue(payload.get("ok"))
        content = str(payload.get("markdown") or "")
        self.assertIn("Team Cookbook", content)
