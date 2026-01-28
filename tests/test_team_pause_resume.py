import contextlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from agent_loom.team import core as team
from agent_loom.team.models import SpawnIntegratorResult, StartResult
from agent_loom.team.run_state import RunPaths


class TestTeamPauseResume(unittest.TestCase):
    def test_pause_sets_paused_and_kills_session(self) -> None:
        paths = RunPaths(repo_root=Path("/repo"), team="CobraKai")
        run = {
            "team": "CobraKai",
            "run_id": "123",
            "session": "team-cobrakai",
        }

        @contextlib.contextmanager
        def fake_locked_run(_paths: RunPaths, *, save: bool = True):
            _ = save
            yield run

        with (
            mock.patch.object(team, "_paths_for", return_value=paths),
            mock.patch.object(team, "locked_run", fake_locked_run),
            mock.patch.object(team, "safe_write_event"),
            mock.patch.object(team, "tmux_has_session", return_value=True),
            mock.patch.object(team, "tmux_kill_session") as kill_sess,
            mock.patch.object(team, "_require_bin"),
        ):
            res = team.pause_team(team="CobraKai", repo=None)

        self.assertTrue(bool(run.get("paused")))
        self.assertTrue(str(run.get("paused_at") or ""))
        self.assertEqual(res.team, "CobraKai")
        self.assertEqual(res.session, "team-cobrakai")
        self.assertTrue(res.session_killed)
        kill_sess.assert_called_once_with("team-cobrakai")

    def test_resume_restores_workers_and_integrator(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            paths = RunPaths(repo_root=repo_root, team="CobraKai")
            paths.run_dir.mkdir(parents=True, exist_ok=True)

            run = {
                "team": "CobraKai",
                "run_id": "123",
                "session": "team-cobrakai",
                "repo_root": str(repo_root),
                "paused": True,
                "paused_at": "2026-02-01T00:00:00Z",
                "workers": {
                    "w1": {
                        "worker_id": "w1",
                        "role": "worker",
                        "ticket_id": "tk-1",
                        "worktree": str(repo_root / "wt"),
                        "retired": False,
                    },
                    "integrator": {
                        "worker_id": "integrator",
                        "role": "integrator",
                        "window": "integrator",
                        "worktree_key": "merge-queue",
                        "branch": "team/merge-queue",
                        "retired": False,
                    },
                },
                "merge": {
                    "config": {
                        "target_branch": "main",
                        "remote": "origin",
                        "push": True,
                    }
                },
            }
            paths.run_file.write_text(json.dumps(run), encoding="utf-8")

            @contextlib.contextmanager
            def fake_locked_run(_paths: RunPaths, *, save: bool = True):
                _ = save
                yield run

            start_res = StartResult(
                team="CobraKai",
                session="team-cobrakai",
                run_id="123",
                run_dir=str(paths.run_dir),
                repo_root=str(repo_root),
                tickets_dir=str(repo_root / ".tickets"),
                manager={"window": "manager", "pane_id": "%1"},
                charter=str(paths.charter_file),
                created=False,
            )

            def fake_respawn(**kwargs):
                w = dict(kwargs.get("worker") or {})
                w["pane_id"] = "%9"
                return True, w

            with (
                mock.patch.object(team, "_paths_for", return_value=paths),
                mock.patch.object(team, "locked_run", fake_locked_run),
                mock.patch.object(team, "load_run", return_value=run),
                mock.patch.object(team, "start", return_value=start_res),
                mock.patch.object(team, "tmux_has_session", return_value=True),
                mock.patch.object(team, "safe_write_event"),
                mock.patch.object(
                    team, "_respawn_active_worker_if_missing", side_effect=fake_respawn
                ),
                mock.patch.object(
                    team,
                    "spawn_integrator",
                    return_value=SpawnIntegratorResult(
                        team="CobraKai",
                        worker_id="integrator",
                        window="integrator",
                        pane_id="%10",
                        worktree=str(repo_root / "merge"),
                        respawned=True,
                        worker={},
                    ),
                ) as spawn_int,
                mock.patch.object(team, "_require_bin"),
            ):
                res = team.resume_team(team="CobraKai", repo=repo_root)

            self.assertEqual(res.team, "CobraKai")
            self.assertEqual(res.session, "team-cobrakai")
            self.assertIn("w1", res.resumed_workers)
            self.assertFalse(bool(run.get("paused")))
            self.assertEqual(str(run.get("paused_at") or ""), "")
            spawn_int.assert_called()


if __name__ == "__main__":
    unittest.main()
