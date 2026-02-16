import contextlib
import unittest
from pathlib import Path
from unittest import mock

from agent_loom.team import core as team
from agent_loom.team.run_state import RunPaths


class TestTeamObjectiveParity(unittest.TestCase):
    def test_objective_set_mutates_state_and_notifies_manager(self) -> None:
        paths = RunPaths(repo_root=Path("/repo"), team="CobraKai")
        run = {
            "team": "CobraKai",
            "run_id": "1234567890abcdef",
            "session": "team-cobrakai",
            "objective": "old objective\n",
            "objective_rev": 1,
            "done_reminder": {"sent_at": "2026-02-15T00:00:00Z"},
        }

        @contextlib.contextmanager
        def fake_locked_run(_paths: RunPaths, *, save: bool = True):
            _ = save
            yield run

        with (
            mock.patch.object(team, "_require_role"),
            mock.patch.object(team, "_paths_for", return_value=paths),
            mock.patch.object(team, "locked_run", fake_locked_run),
            mock.patch.object(team, "_iso_z", return_value="2026-02-16T12:00:00Z"),
            mock.patch.object(team, "_write_charter", return_value=Path("/repo/CHARTER.md")),
            mock.patch.object(
                team,
                "_inbox_write_and_maybe_nudge",
                return_value=({"id": "m-1"}, "manager", True, "", {}),
            ),
            mock.patch.object(team, "write_event"),
        ):
            res = team.objective_set(team="CobraKai", message="Ship parity", nudge=True)

        self.assertEqual(res.mode, "set")
        self.assertEqual(res.objective_rev, 2)
        self.assertEqual(res.inbox_id, "m-1")
        self.assertTrue(res.nudged)
        self.assertEqual(run["objective"], "Ship parity\n")
        self.assertEqual(run["done_reminder"], {})

    def test_objective_append_appends_block_and_updates_revision(self) -> None:
        paths = RunPaths(repo_root=Path("/repo"), team="CobraKai")
        run = {
            "team": "CobraKai",
            "run_id": "1234567890abcdef",
            "session": "team-cobrakai",
            "objective": "Initial objective\n",
            "objective_rev": 3,
            "done_reminder": {"sent_at": "2026-02-15T00:00:00Z"},
        }

        @contextlib.contextmanager
        def fake_locked_run(_paths: RunPaths, *, save: bool = True):
            _ = save
            yield run

        with (
            mock.patch.object(team, "_require_role"),
            mock.patch.object(team, "_paths_for", return_value=paths),
            mock.patch.object(team, "locked_run", fake_locked_run),
            mock.patch.object(team, "_iso_z", return_value="2026-02-16T12:00:00Z"),
            mock.patch.object(team, "_write_charter", return_value=Path("/repo/CHARTER.md")),
            mock.patch.object(
                team,
                "_inbox_write_and_maybe_nudge",
                return_value=({"id": "m-2"}, "manager", False, "tmux_missing", {}),
            ),
            mock.patch.object(team, "write_event"),
        ):
            res = team.objective_append(
                team="CobraKai",
                message="Add regression guardrails",
                nudge=True,
            )

        self.assertEqual(res.mode, "append")
        self.assertEqual(res.objective_rev, 4)
        self.assertEqual(res.inbox_id, "m-2")
        self.assertFalse(res.nudged)
        self.assertIn("## Update 2026-02-16T12:00:00Z", run["objective"])
        self.assertIn("Add regression guardrails", run["objective"])
        self.assertEqual(run["done_reminder"], {})


if __name__ == "__main__":
    unittest.main()
