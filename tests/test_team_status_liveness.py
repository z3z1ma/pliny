from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from agent_loom.team import core as team
from agent_loom.team.io import _atomic_write_json
from agent_loom.team.team_config import default_team_config_spec


def _base_run(*, repo_root: Path, paths: team.RunPaths) -> dict:
    return {
        "team": paths.team,
        "run_id": "run-123",
        "session": f"team-{paths.team}",
        "repo_root": str(repo_root),
        "run_dir": str(paths.run_dir),
        "tickets_dir": str(repo_root / ".loom" / "ticket"),
        "team_config": {"source": "", "loaded_at": "", "spec": default_team_config_spec()},
        "manager": {"window": "manager", "pane_id": "%m"},
        "workers": {
            "w1": {
                "worker_id": "w1",
                "role": "worker",
                "ticket_id": "al-1",
                "window": "w1-al-1",
                "pane_id": "%1",
                "retired": False,
            }
        },
        "merge": {"config": {"target_branch": "main", "remote": "origin", "push": True}},
    }


def _write_sidecar_pid(
    *, paths: team.RunPaths, run_id: str, recipient: str, pane_id: str
) -> None:
    _atomic_write_json(
        team._sidecar_pid_file(paths, recipient),
        {
            "pid": os.getpid(),
            "recipient": recipient,
            "pane_id": pane_id,
            "agent_bin": "",
            "run_id": run_id,
            "started_at": "2026-02-17T00:00:00Z",
        },
    )


class TestTeamStatusLiveness(unittest.TestCase):
    def test_status_uses_sidecar_pid_fallback_for_missing_heartbeat(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            paths = team.RunPaths(repo_root=repo_root, team="cobra")
            (repo_root / ".loom" / "ticket").mkdir(parents=True, exist_ok=True)
            run = _base_run(repo_root=repo_root, paths=paths)
            team.save_run(paths, run)
            _write_sidecar_pid(paths=paths, run_id="run-123", recipient="manager", pane_id="%m")
            _write_sidecar_pid(paths=paths, run_id="run-123", recipient="w1", pane_id="%1")

            panes = {
                "%m": {"pane_id": "%m", "dead": "0", "current_command": "python3.14"},
                "%1": {"pane_id": "%1", "dead": "0", "current_command": "python3.14"},
            }
            with (
                mock.patch.object(team, "_require_bin"),
                mock.patch.object(team, "tmux_has_session", return_value=True),
                mock.patch.object(team, "tmux_list_panes", return_value=panes),
                mock.patch.object(team, "inbox_list_messages", return_value=[]),
                mock.patch.object(team, "merge_list_items", return_value=[]),
            ):
                res = team.status(team="cobra", repo=repo_root)

            worker = dict(res.workers.get("w1") or {})
            health = dict(worker.get("health") or {})
            self.assertTrue(bool(worker.get("alive")))
            self.assertEqual(str(health.get("state") or ""), "alive")
            self.assertEqual(str(health.get("heartbeat_state") or ""), "missing")
            self.assertEqual(str(health.get("state_source") or ""), "sidecar_pid")

    def test_doctor_does_not_flag_stale_when_sidecar_fallback_is_alive(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            paths = team.RunPaths(repo_root=repo_root, team="cobra")
            (repo_root / ".loom" / "ticket").mkdir(parents=True, exist_ok=True)
            run = _base_run(repo_root=repo_root, paths=paths)
            team.save_run(paths, run)
            _write_sidecar_pid(paths=paths, run_id="run-123", recipient="manager", pane_id="%m")
            _write_sidecar_pid(paths=paths, run_id="run-123", recipient="w1", pane_id="%1")

            panes = {
                "%m": {"pane_id": "%m", "dead": "0", "current_command": "python3.14"},
                "%1": {"pane_id": "%1", "dead": "0", "current_command": "python3.14"},
            }
            with (
                mock.patch.object(team, "tmux_has_session", return_value=True),
                mock.patch.object(team, "tmux_list_panes", return_value=panes),
                mock.patch.object(team, "merge_list_items", return_value=[]),
                mock.patch.object(team, "tmux_window_exists", return_value=True),
            ):
                res = team.doctor(team="cobra", repo=repo_root)

            issue_codes = {str((it or {}).get("code") or "") for it in res.issues}
            self.assertFalse(any(c.startswith("MANAGER_") for c in issue_codes))
            self.assertFalse(any(c.startswith("WORKER_") for c in issue_codes))


if __name__ == "__main__":
    unittest.main()
