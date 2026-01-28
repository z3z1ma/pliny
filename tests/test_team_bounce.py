import unittest
from pathlib import Path
from unittest import mock

from agent_loom.team import core as team
from agent_loom.team.constants import CONTROL_OP_BOUNCE, INBOX_KIND_CONTROL


class TestTeamBounce(unittest.TestCase):
    def test_bounce_writes_control_message_and_signals(self) -> None:
        paths = team.RunPaths(repo_root=Path("/repo"), team="CobraKai")
        run = {
            "team": "CobraKai",
            "run_id": "1234567890abcdef",
            "session": "team-cobrakai",
            "manager": {"pane_id": "%1"},
            "workers": {
                "w1": {
                    "worker_id": "w1",
                    "role": team.ROLE_WORKER,
                    "ticket_id": "t-1",
                    "pane_id": "%2",
                    "window": "w1-t-1",
                    "retired": False,
                }
            },
        }

        with (
            mock.patch.object(team, "_require_bin"),
            mock.patch.object(team, "_paths_for", return_value=paths),
            mock.patch.object(team, "load_run", return_value=run),
            mock.patch.object(team, "tmux_has_session", return_value=True),
            mock.patch.object(
                team,
                "tmux_list_panes",
                return_value={
                    "%2": {
                        "pane_id": "%2",
                        "dead": "0",
                        "current_command": "opencode",
                    }
                },
            ),
            mock.patch.object(
                team, "inbox_write_message", return_value={"id": "abc123"}
            ) as inbox,
            mock.patch.object(team, "tmux_signal") as sig,
            mock.patch.object(team, "safe_write_event"),
        ):
            res = team.bounce(team="CobraKai", target="w1", reason="wedged")

        inbox.assert_called_once()
        _args, kwargs = inbox.call_args
        self.assertEqual(kwargs["to"], "w1")
        self.assertEqual(kwargs["kind"], INBOX_KIND_CONTROL)
        self.assertEqual(kwargs["message"], CONTROL_OP_BOUNCE)
        self.assertEqual(kwargs["meta"]["op"], CONTROL_OP_BOUNCE)
        self.assertEqual(kwargs["meta"]["reason"], "wedged")

        sig.assert_called_once_with("team:1234567890ab:to:w1")
        self.assertEqual(res.worker_id, "w1")
        self.assertEqual(res.inbox_id, "abc123")

    def test_bounce_rejects_manager(self) -> None:
        paths = team.RunPaths(repo_root=Path("/repo"), team="CobraKai")
        run = {
            "team": "CobraKai",
            "run_id": "1234567890abcdef",
            "session": "team-cobrakai",
            "manager": {"pane_id": "%1"},
            "workers": {},
        }
        with (
            mock.patch.object(team, "_require_bin"),
            mock.patch.object(team, "_paths_for", return_value=paths),
            mock.patch.object(team, "load_run", return_value=run),
            mock.patch.object(team, "tmux_has_session", return_value=True),
        ):
            with self.assertRaises(team.TeamError):
                team.bounce(team="CobraKai", target="manager")

    def test_bounce_rejects_retired_worker(self) -> None:
        paths = team.RunPaths(repo_root=Path("/repo"), team="CobraKai")
        run = {
            "team": "CobraKai",
            "run_id": "1234567890abcdef",
            "session": "team-cobrakai",
            "manager": {"pane_id": "%1"},
            "workers": {"w1": {"worker_id": "w1", "pane_id": "%2", "retired": True}},
        }
        with (
            mock.patch.object(team, "_require_bin"),
            mock.patch.object(team, "_paths_for", return_value=paths),
            mock.patch.object(team, "load_run", return_value=run),
            mock.patch.object(team, "tmux_has_session", return_value=True),
        ):
            with self.assertRaises(team.TeamError):
                team.bounce(team="CobraKai", target="w1")

    def test_bounce_errors_when_pane_not_interactive(self) -> None:
        paths = team.RunPaths(repo_root=Path("/repo"), team="CobraKai")
        run = {
            "team": "CobraKai",
            "run_id": "1234567890abcdef",
            "session": "team-cobrakai",
            "manager": {"pane_id": "%1"},
            "workers": {
                "w1": {
                    "worker_id": "w1",
                    "role": team.ROLE_WORKER,
                    "ticket_id": "t-1",
                    "pane_id": "%2",
                    "window": "w1-t-1",
                    "retired": False,
                }
            },
        }
        with (
            mock.patch.object(team, "_require_bin"),
            mock.patch.object(team, "_paths_for", return_value=paths),
            mock.patch.object(team, "load_run", return_value=run),
            mock.patch.object(team, "tmux_has_session", return_value=True),
            mock.patch.object(
                team,
                "tmux_list_panes",
                return_value={
                    "%2": {
                        "pane_id": "%2",
                        "dead": "1",
                        "current_command": "bash",
                    }
                },
            ),
        ):
            with self.assertRaises(team.TeamError) as ctx:
                team.bounce(team="CobraKai", target="w1")
        self.assertEqual(ctx.exception.code, "DEAD_PANE")


if __name__ == "__main__":
    unittest.main()
