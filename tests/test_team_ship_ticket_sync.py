import argparse
import contextlib
import dataclasses
import importlib
import io
import tempfile
import unittest
from pathlib import Path
from typing import Callable, cast
from unittest import mock

from agent_loom.team import core as team

team_cli = importlib.import_module("agent_loom.team.cli")

_ensure_tickets_synced = cast(
    Callable[..., dict], getattr(team, "_ensure_tickets_synced")
)
_cmd_ship = cast(Callable[..., None], getattr(team_cli, "cmd_ship"))


class TestEnsureTicketsSynced(unittest.TestCase):
    def test_noop_when_tickets_clean(self) -> None:
        with (
            mock.patch.object(team, "_git_status_porcelain", return_value="") as gs,
            mock.patch.object(team, "ticket_sync") as sync,
        ):
            out = _ensure_tickets_synced(
                cwd=Path("/repo"), tickets_dir=Path("/repo/.tickets")
            )
            self.assertEqual(out, {"ok": True, "attempted": False, "committed": False})
            gs.assert_called_once()
            sync.assert_not_called()

    def test_calls_ticket_sync_when_tickets_dirty(self) -> None:
        with (
            mock.patch.object(
                team, "_git_status_porcelain", return_value=" M .tickets/a.md\n"
            ),
            mock.patch.object(team, "ticket_sync") as sync,
        ):
            sync_result = dataclasses.make_dataclass(
                "_SyncResult", [("committed", bool)]
            )
            sync.return_value = sync_result(committed=True)
            out = _ensure_tickets_synced(
                cwd=Path("/repo"), tickets_dir=Path("/repo/.tickets")
            )
            self.assertTrue(out.get("ok"))
            self.assertTrue(out.get("attempted"))
            sync.assert_called_once_with(tickets_dir=Path("/repo/.tickets"))


class TestCmdShipTicketSync(unittest.TestCase):
    def test_cmd_ship_invokes_ticket_sync(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            run = {
                "run_id": "rid",
                "repo_root": str(repo_root),
                "session": "sess",
                "team": "CobraKai",
                "merge": {
                    "config": {
                        "target_branch": "main",
                        "remote": "origin",
                        "push": True,
                    }
                },
            }

            @contextlib.contextmanager
            def _locked_run(_paths, *, save: bool = True):
                _ = save
                yield run

            paths = team.RunPaths(repo_root=repo_root, team="CobraKai")
            args = argparse.Namespace(
                team="CobraKai",
                repo=None,
                force_clean=False,
                push=None,
                json=False,
            )

            buf = io.StringIO()
            with (
                mock.patch.object(team, "_require_bin"),
                mock.patch.object(team, "resolve_run_paths", return_value=paths),
                mock.patch.object(team, "locked_run", _locked_run),
                mock.patch.object(team, "repo_merge_attempt") as merge_attempt,
                mock.patch.object(team, "write_event"),
                mock.patch.object(team, "safe_write_event"),
                mock.patch.object(team, "inbox_write_message"),
                mock.patch.object(team, "tmux_signal"),
                mock.patch.object(team, "_ensure_tickets_synced") as sync,
                mock.patch.object(team, "_ensure_compound_synced") as compound_sync,
                contextlib.redirect_stdout(buf),
            ):
                merge_result = mock.Mock()
                merge_result.merged = False
                merge_result.to_dict.return_value = {"merged": False}
                merge_attempt.return_value = merge_result
                _cmd_ship(args)

            sync.assert_called_once()
            compound_sync.assert_called_once()


if __name__ == "__main__":
    unittest.main()
