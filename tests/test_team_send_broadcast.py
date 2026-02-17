import contextlib
import unittest
from pathlib import Path
from unittest import mock

from agent_loom.team import core as team
from agent_loom.team.run_state import RunPaths


class TestTeamSendWorkersFanout(unittest.TestCase):
    def test_send_workers_fanout_reports_partial_delivery(self) -> None:
        paths = RunPaths(repo_root=Path("/repo"), team="CobraKai")
        run = {
            "team": "CobraKai",
            "run_id": "1234567890abcdef",
            "session": "team-cobrakai",
            "workers": {
                "w1": {
                    "worker_id": "w1",
                    "role": "worker",
                    "ticket_id": "tk-1",
                    "pane_id": "%3",
                    "window": "w1",
                    "retired": False,
                },
                "w2": {
                    "worker_id": "w2",
                    "role": "worker",
                    "ticket_id": "tk-2",
                    "pane_id": "%4",
                    "window": "w2",
                    "retired": False,
                },
            },
        }

        @contextlib.contextmanager
        def fake_locked_run(_paths: RunPaths, *, save: bool = True):
            _ = save
            yield run

        calls: list[str] = []

        def fake_inbox_write_and_maybe_nudge(**kwargs):
            target = str(kwargs.get("target") or "")
            calls.append(target)
            if target == "worker:w1":
                return ({"id": "m-1"}, target, True, "", {"worker_id": "w1", "role": "worker"})
            return (
                {"id": "m-2"},
                target,
                False,
                "pane_missing",
                {"worker_id": "w2", "role": "worker"},
            )

        with (
            mock.patch.object(team, "_paths_for", return_value=paths),
            mock.patch.object(team, "locked_run", fake_locked_run),
            mock.patch.object(
                team,
                "_inbox_write_and_maybe_nudge",
                side_effect=fake_inbox_write_and_maybe_nudge,
            ),
            mock.patch.object(team, "write_event"),
            mock.patch.dict("os.environ", {"TEAM_ROLE": "manager"}, clear=False),
        ):
            result = team.send(team="CobraKai", target="workers", message="status check")

        self.assertEqual(calls, ["worker:w1", "worker:w2"])
        self.assertFalse(result.delivered)
        self.assertEqual(result.delivery_reason, "partial_delivery")
        self.assertEqual(len(result.deliveries), 2)
        self.assertEqual(result.inbox.get("count"), 2)
        self.assertIn("loom team status CobraKai --show-dead", result.suggestions)


if __name__ == "__main__":
    unittest.main()
