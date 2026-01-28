import contextlib
import os
import unittest
from pathlib import Path
from unittest import mock

from agent_loom.team import core as team
from agent_loom.team.run_state import RunPaths


class TestManagerWaitCheckin(unittest.TestCase):
    def test_checkins_after_two_timeouts_with_cooldown(self) -> None:
        paths = RunPaths(repo_root=Path("/repo"), team="CobraKai")
        run = {
            "team": "CobraKai",
            "run_id": "1234567890abcdef",
            "session": "team-cobrakai",
            "workers": {
                "w1": {"worker_id": "w1", "role": "worker", "retired": False},
                "w2": {"worker_id": "w2", "role": "worker", "retired": False},
                "w3": {"worker_id": "w3", "role": "worker", "retired": False},
            },
        }

        @contextlib.contextmanager
        def fake_locked_run(_paths: RunPaths, *, _save: bool = True):
            yield run

        sent: list[str] = []

        def fake_inbox_write_and_maybe_nudge(**kwargs):
            self.assertEqual(str(kwargs.get("sender") or ""), "manager")
            self.assertEqual(str(kwargs.get("kind") or ""), "checkin")
            self.assertTrue(str(kwargs.get("message") or ""))
            target = str(kwargs.get("target") or "")
            sent.append(target)
            return ({"id": "m-1"}, target, True, "", {})

        with (
            mock.patch.object(team, "_paths_for", return_value=paths),
            mock.patch.object(team, "load_run", return_value=run),
            mock.patch.object(team, "locked_run", fake_locked_run),
            mock.patch.object(team, "safe_write_event"),
            mock.patch.object(team, "write_event"),
            mock.patch.object(team, "tmux_available", return_value=True),
            mock.patch.object(team, "tmux_has_session", return_value=True),
            mock.patch.object(team, "tmux_wait_for", return_value=False),
            mock.patch.object(
                team, "_inbox_write_and_maybe_nudge", fake_inbox_write_and_maybe_nudge
            ),
            mock.patch.object(team.time, "time", return_value=1000.0),
            mock.patch.dict(os.environ, {"TMUX": ""}, clear=False),
        ):
            # 1st timeout: record streak only.
            team.wait(team="CobraKai", duration="5m")
            self.assertEqual(sent, [])

            # 2nd consecutive timeout: check in with max_targets=2.
            team.wait(team="CobraKai", duration="5m")
            self.assertEqual(sent, ["w1", "w2"])

            # Two more consecutive timeouts: cooldown blocks w1/w2, so w3 is nudged.
            team.wait(team="CobraKai", duration="5m")
            team.wait(team="CobraKai", duration="5m")
            self.assertEqual(sent, ["w1", "w2", "w3"])

    def test_signal_resets_streak(self) -> None:
        paths = RunPaths(repo_root=Path("/repo"), team="CobraKai")
        run = {
            "team": "CobraKai",
            "run_id": "1234567890abcdef",
            "session": "team-cobrakai",
            "workers": {
                "w1": {"worker_id": "w1", "role": "worker", "retired": False},
            },
            "ops": {"manager": {"checkin": {"timeout_streak": 1}}},
        }

        @contextlib.contextmanager
        def fake_locked_run(_paths: RunPaths, *, _save: bool = True):
            yield run

        sent: list[str] = []

        def fake_inbox_write_and_maybe_nudge(**kwargs):
            sent.append(str(kwargs.get("target") or ""))
            return ({"id": "m-1"}, str(kwargs.get("target") or ""), True, "", {})

        with (
            mock.patch.object(team, "_paths_for", return_value=paths),
            mock.patch.object(team, "load_run", return_value=run),
            mock.patch.object(team, "locked_run", fake_locked_run),
            mock.patch.object(team, "safe_write_event"),
            mock.patch.object(team, "write_event"),
            mock.patch.object(team, "tmux_available", return_value=True),
            mock.patch.object(team, "tmux_has_session", return_value=True),
            mock.patch.object(team, "tmux_wait_for", return_value=True),
            mock.patch.object(
                team, "_inbox_write_and_maybe_nudge", fake_inbox_write_and_maybe_nudge
            ),
            mock.patch.object(team.time, "time", return_value=1000.0),
            mock.patch.dict(os.environ, {"TMUX": ""}, clear=False),
        ):
            res = team.wait(team="CobraKai", duration="5m")
            self.assertEqual(res.wake_reason, "signal")

        self.assertEqual(sent, [])
        streak = (
            ((run.get("ops") or {}).get("manager") or {}).get("checkin") or {}
        ).get("timeout_streak") or 0
        self.assertEqual(int(streak), 0)


if __name__ == "__main__":
    unittest.main()
