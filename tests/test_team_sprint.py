import contextlib
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from agent_loom.team import core as team
from agent_loom.team.run_state import RunPaths
from agent_loom.ticket.models import TicketCreateResult


class TestInboxSprintPrefix(unittest.TestCase):
    def test_inbox_write_and_maybe_nudge_prefixes_message_and_sets_meta(self) -> None:
        paths = RunPaths(repo_root=Path("/repo"), team="CobraKai")
        run = {
            "team": "CobraKai",
            "run_id": "1234567890abcdef",
            "session": "team-cobrakai",
            "sprint": {"name": "Alpha", "tag": "sprint:alpha", "rev": 1},
        }

        from agent_loom.team import inbox as inbox

        with (
            mock.patch.object(
                inbox, "inbox_write_message", return_value={"id": "abc"}
            ) as write,
            mock.patch.object(inbox, "tmux_signal"),
            mock.patch.object(
                inbox, "_best_effort_tmux_nudge", return_value=(True, "", {})
            ),
        ):
            inbox._inbox_write_and_maybe_nudge(
                paths=paths,
                run=run,
                target="manager",
                message="Hello",
                sender="team",
                kind="note",
                meta_extra={"x": 1},
                nudge=True,
                force=False,
                line_info="",
            )

        _args, kwargs = write.call_args
        self.assertTrue(str(kwargs["message"]).startswith("[Sprint: Alpha] "))
        meta = kwargs["meta"]
        self.assertEqual(meta["sprint"]["name"], "Alpha")
        self.assertEqual(meta["sprint"]["tag"], "sprint:alpha")


class TestPrepSprint(unittest.TestCase):
    def test_prep_sprint_sets_state_and_creates_ticket(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            repo_root = Path(d)
            paths = RunPaths(repo_root=repo_root, team="CobraKai")
            paths.run_dir.mkdir(parents=True, exist_ok=True)
            paths.events_dir.mkdir(parents=True, exist_ok=True)
            paths.inbox_dir.mkdir(parents=True, exist_ok=True)
            paths.inbox_read_dir.mkdir(parents=True, exist_ok=True)
            paths.worktrees_dir.mkdir(parents=True, exist_ok=True)
            paths.snapshots_dir.mkdir(parents=True, exist_ok=True)
            paths.captures_dir.mkdir(parents=True, exist_ok=True)

            run = {
                "team": "CobraKai",
                "run_id": "1234567890abcdef",
                "session": "team-cobrakai",
                "objective": "Do the thing.",
                "objective_rev": 1,
                "objective_updated_at": "",
                "harness": "opencode",
                "opencode": {"model": "", "models": {}},
                "workers": {},
                "merge": {"items": [], "config": {}},
                "sprint": {},
            }

            @contextlib.contextmanager
            def fake_locked_run(_paths: RunPaths, *, _save: bool = True):
                yield run

            with (
                mock.patch.object(team, "_paths_for", return_value=paths),
                mock.patch.object(team, "locked_run", fake_locked_run),
                mock.patch.object(team, "run_root", return_value=repo_root),
                mock.patch.object(
                    team, "ensure_run_tickets_dir", return_value=repo_root / ".tickets"
                ),
                mock.patch.object(team, "_write_charter"),
                mock.patch.object(team, "write_event"),
                mock.patch.object(
                    team,
                    "ticket_create",
                    return_value=TicketCreateResult(id="t-1", path="t-1.md"),
                ) as create,
                mock.patch.object(
                    team,
                    "spawn",
                    return_value=team.SpawnResult(
                        team="CobraKai",
                        session="team-cobrakai",
                        repo_root=str(repo_root),
                        run_dir=str(paths.run_dir),
                        tickets_dir=str(repo_root / ".tickets"),
                        worker={"worker_id": "w9"},
                        ticket={"id": "t-1"},
                    ),
                ),
                mock.patch.object(team, "load_run", return_value=run),
                mock.patch.object(team, "_inbox_write_and_maybe_nudge"),
            ):
                res = team.prep_sprint(team="CobraKai", name="Alpha Sprint")

            self.assertEqual(res.ticket_id, "t-1")
            self.assertTrue(res.spawned)
            self.assertEqual(res.worker_id, "w9")
            self.assertEqual(run["sprint"]["name"], "Alpha Sprint")
            self.assertTrue(str(run["sprint"]["tag"]).startswith("sprint:"))

            _args, kwargs = create.call_args
            self.assertIn(run["sprint"]["tag"], str(kwargs["tags"]))

    def test_prep_sprint_rejects_existing_without_force(self) -> None:
        paths = RunPaths(repo_root=Path("/repo"), team="CobraKai")
        run = {
            "team": "CobraKai",
            "run_id": "1234567890abcdef",
            "session": "team-cobrakai",
            "sprint": {"name": "Already", "rev": 1},
        }

        @contextlib.contextmanager
        def fake_locked_run(_paths: RunPaths, *, _save: bool = True):
            yield run

        with (
            mock.patch.object(team, "_paths_for", return_value=paths),
            mock.patch.object(team, "locked_run", fake_locked_run),
        ):
            with self.assertRaises(team.TeamError):
                team.prep_sprint(team="CobraKai", name="New")


if __name__ == "__main__":
    unittest.main()
