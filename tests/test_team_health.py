from __future__ import annotations

import tempfile
import time
import unittest
from pathlib import Path

from agent_loom.team.health import clear_heartbeat, health_state, write_heartbeat
from agent_loom.team.io import _atomic_write_json
from agent_loom.team.run_state import RunPaths
from agent_loom.team.team_config import default_team_config_spec


class TestTeamHealth(unittest.TestCase):
    def _run(self) -> dict:
        spec = default_team_config_spec()
        spec["liveness"] = {
            "heartbeat_interval_s": 1,
            "stale_after_s": 2,
            "dead_after_s": 5,
            "recovery_cooldown_s": 10,
            "max_recoveries_per_hour": 3,
        }
        return {
            "team_config": {
                "source": "",
                "loaded_at": "",
                "spec": spec,
            }
        }

    def test_missing_heartbeat_is_missing_state(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            paths = RunPaths(repo_root=Path(td), team="cobra")
            state, payload = health_state(paths=paths, run=self._run(), recipient="worker:w1")
        self.assertEqual(state, "missing")
        self.assertEqual(payload, {})

    def test_alive_to_stale_to_dead_transitions(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            paths = RunPaths(repo_root=Path(td), team="cobra")
            now = time.time()
            write_heartbeat(
                paths=paths,
                recipient="w1",
                role="worker",
                pane_id="%1",
                pid=123,
                current_command="codex",
            )

            alive, _payload = health_state(paths=paths, run=self._run(), recipient="w1", now_ts=now + 1)
            stale, _payload2 = health_state(paths=paths, run=self._run(), recipient="w1", now_ts=now + 3)
            dead, _payload3 = health_state(paths=paths, run=self._run(), recipient="w1", now_ts=now + 10)

            self.assertEqual(alive, "alive")
            self.assertEqual(stale, "stale")
            self.assertEqual(dead, "dead")

    def test_invalid_heartbeat_timestamp_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            paths = RunPaths(repo_root=Path(td), team="cobra")
            p = paths.health_dir / "w1.json"
            p.parent.mkdir(parents=True, exist_ok=True)
            _atomic_write_json(
                p,
                {
                    "recipient": "w1",
                    "role": "worker",
                    "pane_id": "%1",
                    "pid": 123,
                    "last_seen_at": "not-a-time",
                    "current_command": "codex",
                },
            )

            state, _payload = health_state(paths=paths, run=self._run(), recipient="w1")
            self.assertEqual(state, "missing")

    def test_clear_heartbeat_removes_file(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            paths = RunPaths(repo_root=Path(td), team="cobra")
            write_heartbeat(
                paths=paths,
                recipient="w1",
                role="worker",
                pane_id="%1",
                pid=123,
                current_command="codex",
            )
            clear_heartbeat(paths=paths, recipient="w1")
            state, _payload = health_state(paths=paths, run=self._run(), recipient="w1")
            self.assertEqual(state, "missing")


if __name__ == "__main__":
    unittest.main()
