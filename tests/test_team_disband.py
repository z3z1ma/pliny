import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from agent_loom.team import core as team


class TestTeamDisband(unittest.TestCase):
    def test_disband_clears_sidecar_pidfiles_without_killing_process(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            team_name = team.sanitize("CobraKai", max_len=80) or "cobrakai"
            paths = team.RunPaths(repo_root=repo_root, team=team_name)
            paths.run_dir.mkdir(parents=True, exist_ok=True)
            paths.sidecars_dir.mkdir(parents=True, exist_ok=True)

            run = {
                "team": "CobraKai",
                "run_id": "1234567890abcdef",
                "session": f"team-{team_name}",
            }
            paths.run_file.write_text(json.dumps(run), encoding="utf-8")

            p = subprocess.Popen(
                [sys.executable, "-c", "import time; time.sleep(60)"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            try:
                pidfile = paths.sidecars_dir / "w1.pid.json"
                pidfile.write_text(json.dumps({"pid": int(p.pid)}), encoding="utf-8")

                with (
                    mock.patch.object(team, "_require_bin"),
                    mock.patch.object(
                        team, "canonical_repo_root", return_value=repo_root
                    ),
                    mock.patch.object(team, "tmux_has_session", return_value=False),
                    mock.patch.object(team, "safe_write_event"),
                ):
                    res = team.disband(team="CobraKai", repo=repo_root, keep_state=True)

                # Disband should not attempt PID-based cleanup (tmux session kill is enough).
                self.assertIsNone(
                    p.poll(), "expected pidfile process to still be running"
                )
                self.assertFalse(pidfile.exists(), "expected pidfile to be removed")

                term = (res.process_cleanup or {}).get("termination") or {}
                self.assertEqual(term, {}, "expected no pid-based termination data")
            finally:
                if p.poll() is None:
                    try:
                        p.kill()
                    except Exception:
                        pass

    def test_disband_kills_tmux_session_only(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            team_name = team.sanitize("Miyagi", max_len=80) or "miyagi"
            paths = team.RunPaths(repo_root=repo_root, team=team_name)
            paths.run_dir.mkdir(parents=True, exist_ok=True)
            paths.sidecars_dir.mkdir(parents=True, exist_ok=True)

            run = {
                "team": "Miyagi",
                "run_id": "abcdef1234567890",
                "session": f"team-{team_name}",
            }
            paths.run_file.write_text(json.dumps(run), encoding="utf-8")

            with (
                mock.patch.object(team, "_require_bin"),
                mock.patch.object(team, "canonical_repo_root", return_value=repo_root),
                mock.patch.object(team, "tmux_has_session", return_value=True),
                mock.patch.object(team, "tmux_kill_session") as kill_sess,
                mock.patch.object(team, "safe_write_event"),
            ):
                team.disband(team="Miyagi", repo=repo_root, keep_state=True)

            kill_sess.assert_called()


if __name__ == "__main__":
    unittest.main()
