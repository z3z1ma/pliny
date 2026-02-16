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
                "workers": {
                    "arch-1": {
                        "worker_id": "arch-1",
                        "role": "architect",
                        "ticket_id": "",
                        "pane_id": "%9",
                        "window": "architect",
                        "retired": False,
                    }
                },
                "merge": {"items": [], "config": {}},
                "sprint": {},
            }

            @contextlib.contextmanager
            def fake_locked_run(_paths: RunPaths, *, _save: bool = True):
                yield run

            with (
                mock.patch.object(team, "_require_role"),
                mock.patch.object(team, "_paths_for", return_value=paths),
                mock.patch.object(team, "locked_run", fake_locked_run),
                mock.patch.object(team, "run_root", return_value=repo_root),
                mock.patch.object(
                    team,
                    "ensure_run_tickets_dir",
                    return_value=repo_root / ".loom" / "ticket",
                ),
                mock.patch.object(team, "_write_charter"),
                mock.patch.object(team, "write_event"),
                mock.patch.object(
                    team,
                    "ticket_create",
                    return_value=TicketCreateResult(id="t-1", path="t-1.md"),
                ) as create,

                mock.patch.object(team, "load_run", return_value=run),
                mock.patch.object(team, "_inbox_write_and_maybe_nudge"),
            ):
                res = team.prep_sprint(team="CobraKai", name="Alpha Sprint")

            self.assertEqual(res.ticket_id, "t-1")
            self.assertTrue(res.spawned)
            self.assertEqual(res.worker_id, "arch-1")
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
            mock.patch.object(team, "_require_role"),
            mock.patch.object(team, "_paths_for", return_value=paths),
            mock.patch.object(team, "locked_run", fake_locked_run),
        ):
            with self.assertRaises(team.TeamError):
                team.prep_sprint(team="CobraKai", name="New")


class TestSprintStateCommands(unittest.TestCase):
    def test_sprint_set_defaults_tag_from_slug(self) -> None:
        paths = RunPaths(repo_root=Path("/repo"), team="CobraKai")
        run = {
            "team": "CobraKai",
            "run_id": "1234567890abcdef",
            "session": "team-cobrakai",
            "sprint": {},
        }

        @contextlib.contextmanager
        def fake_locked_run(_paths: RunPaths, *, _save: bool = True):
            yield run

        with (
            mock.patch.object(team, "_require_role"),
            mock.patch.object(team, "_paths_for", return_value=paths),
            mock.patch.object(team, "locked_run", fake_locked_run),
            mock.patch.object(team, "_write_charter", return_value=Path("/repo/CHARTER.md")),
            mock.patch.object(team, "write_event"),
        ):
            result = team.sprint_set(team="CobraKai", name="Alpha Sprint")

        self.assertEqual(result.rev, 1)
        self.assertEqual(result.sprint["name"], "Alpha Sprint")
        self.assertEqual(result.sprint["slug"], "Alpha-Sprint")
        self.assertEqual(result.sprint["tag"], "sprint:Alpha-Sprint")

    def test_sprint_clear_increments_rev(self) -> None:
        paths = RunPaths(repo_root=Path("/repo"), team="CobraKai")
        run = {
            "team": "CobraKai",
            "run_id": "1234567890abcdef",
            "session": "team-cobrakai",
            "sprint": {"name": "Alpha", "tag": "sprint:alpha", "rev": 2},
        }

        @contextlib.contextmanager
        def fake_locked_run(_paths: RunPaths, *, _save: bool = True):
            yield run

        with (
            mock.patch.object(team, "_require_role"),
            mock.patch.object(team, "_paths_for", return_value=paths),
            mock.patch.object(team, "locked_run", fake_locked_run),
            mock.patch.object(team, "_write_charter", return_value=Path("/repo/CHARTER.md")),
            mock.patch.object(team, "write_event"),
        ):
            result = team.sprint_clear(team="CobraKai")

        self.assertEqual(result.rev, 3)
        self.assertEqual(run["sprint"], {})


if __name__ == "__main__":
    unittest.main()
