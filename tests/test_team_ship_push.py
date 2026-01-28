import contextlib
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from agent_loom.team import core as team
from agent_loom.team.errors import TeamError


class TestTeamShipPush(unittest.TestCase):
    def _run_ctx(self, run: dict):
        @contextlib.contextmanager
        def _locked_run(_paths, *, save: bool = True):
            _ = save
            yield run

        return _locked_run

    def test_ship_respects_push_override_false(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            paths = team.RunPaths(repo_root=repo_root, team="CobraKai")
            run = {
                "team": "CobraKai",
                "run_id": "rid",
                "repo_root": str(repo_root),
                "session": "sess",
                "merge": {
                    "branch": "team/merge-queue",
                    "config": {
                        "target_branch": "main",
                        "remote": "origin",
                        "push": True,
                    },
                    "items": [],
                },
            }

            merge_result = mock.Mock()
            merge_result.merged = True
            merge_result.to_dict.return_value = {"merged": True}

            with (
                mock.patch.object(team, "_require_bin"),
                mock.patch.object(team, "resolve_run_paths", return_value=paths),
                mock.patch.object(team, "locked_run", self._run_ctx(run)),
                mock.patch.object(
                    team, "repo_merge_attempt", return_value=merge_result
                ),
                mock.patch.object(team, "_ensure_tickets_synced"),
                mock.patch.object(team, "_ensure_compound_synced"),
                mock.patch.object(team, "safe_write_event"),
                mock.patch.object(team, "write_event"),
                mock.patch.object(team, "inbox_write_message"),
                mock.patch.object(team, "tmux_signal"),
                mock.patch.object(team, "_run") as run_cmd,
            ):
                team.ship(team="CobraKai", repo=repo_root, push=False)

            for call in run_cmd.call_args_list:
                argv = list(call.args[0]) if call.args else []
                self.assertNotEqual(argv[:2], ["git", "push"])

    def test_ship_respects_push_override_true(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            paths = team.RunPaths(repo_root=repo_root, team="CobraKai")
            run = {
                "team": "CobraKai",
                "run_id": "rid",
                "repo_root": str(repo_root),
                "session": "sess",
                "merge": {
                    "branch": "team/merge-queue",
                    "config": {
                        "target_branch": "main",
                        "remote": "origin",
                        "push": False,
                    },
                    "items": [],
                },
            }

            merge_result = mock.Mock()
            merge_result.merged = True
            merge_result.to_dict.return_value = {"merged": True}

            with (
                mock.patch.object(team, "_require_bin"),
                mock.patch.object(team, "resolve_run_paths", return_value=paths),
                mock.patch.object(team, "locked_run", self._run_ctx(run)),
                mock.patch.object(
                    team, "repo_merge_attempt", return_value=merge_result
                ),
                mock.patch.object(team, "_ensure_tickets_synced"),
                mock.patch.object(team, "_ensure_compound_synced"),
                mock.patch.object(team, "safe_write_event"),
                mock.patch.object(team, "write_event"),
                mock.patch.object(team, "inbox_write_message"),
                mock.patch.object(team, "tmux_signal"),
                mock.patch.object(team, "_run") as run_cmd,
            ):
                team.ship(team="CobraKai", repo=repo_root, push=True)

            self.assertTrue(
                any(
                    list(c.args[0])[:2] == ["git", "push"]
                    for c in run_cmd.call_args_list
                    if c.args
                )
            )

    def test_ship_raises_on_push_failure_when_enabled(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            paths = team.RunPaths(repo_root=repo_root, team="CobraKai")
            run = {
                "team": "CobraKai",
                "run_id": "rid",
                "repo_root": str(repo_root),
                "session": "sess",
                "merge": {
                    "branch": "team/merge-queue",
                    "config": {
                        "target_branch": "main",
                        "remote": "origin",
                        "push": True,
                    },
                    "items": [],
                },
            }

            merge_result = mock.Mock()
            merge_result.merged = True
            merge_result.to_dict.return_value = {"merged": True}

            def boom(argv, **kwargs):
                _ = kwargs
                if list(argv)[:2] == ["git", "push"]:
                    raise RuntimeError("push failed")
                return mock.Mock(stdout="", returncode=0)

            with (
                mock.patch.object(team, "_require_bin"),
                mock.patch.object(team, "resolve_run_paths", return_value=paths),
                mock.patch.object(team, "locked_run", self._run_ctx(run)),
                mock.patch.object(
                    team, "repo_merge_attempt", return_value=merge_result
                ),
                mock.patch.object(team, "_ensure_tickets_synced"),
                mock.patch.object(team, "_ensure_compound_synced"),
                mock.patch.object(team, "safe_write_event"),
                mock.patch.object(team, "write_event"),
                mock.patch.object(team, "inbox_write_message"),
                mock.patch.object(team, "tmux_signal"),
                mock.patch.object(team, "_run", side_effect=boom),
            ):
                with self.assertRaises(TeamError) as ctx:
                    team.ship(team="CobraKai", repo=repo_root)

            self.assertEqual(str(getattr(ctx.exception, "code", "")), "PUSH")


if __name__ == "__main__":
    unittest.main()
