import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from agent_loom.team import core as team


class TestTeamStartMergeConfig(unittest.TestCase):
    def test_start_sets_target_branch_and_worker_base_ref(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)

            def fake_tmux_cmd(argv, **kwargs):
                _ = kwargs
                return subprocess.CompletedProcess(list(argv), 0, stdout="", stderr="")

            with (
                mock.patch.object(team, "canonical_repo_root", return_value=repo_root),
                mock.patch.object(team, "_require_bin"),
                mock.patch.object(team, "tmux_has_session", return_value=False),
                mock.patch.object(team, "tmux_cmd", side_effect=fake_tmux_cmd),
                mock.patch.object(team, "tmux_set_option"),
                mock.patch.object(team, "tmux_window_exists", return_value=False),
                mock.patch.object(team, "tmux_mark_pane"),
                mock.patch.object(team, "tmux_format", return_value="%1"),
            ):
                team.init_agents(repo=repo_root, create_missing=True)
                res = team.start(
                    team="CobraKai",
                    repo=repo_root,
                    target_branch="dev/overnight",
                    remote="origin",
                    max_headcount=7,
                )

            run_path = Path(res.run_dir) / "run.json"
            run = json.loads(run_path.read_text(encoding="utf-8"))
            merge_cfg = dict(((run.get("merge") or {}).get("config") or {}))
            self.assertEqual(str(merge_cfg.get("target_branch") or ""), "dev/overnight")
            self.assertEqual(str(merge_cfg.get("remote") or ""), "origin")
            self.assertEqual(bool(merge_cfg.get("push")), True)

            defaults = dict(run.get("defaults") or {})
            self.assertEqual(str(defaults.get("base_ref") or ""), "dev/overnight")

            limits = dict(run.get("limits") or {})
            self.assertEqual(int(limits.get("max_headcount") or 0), 7)


if __name__ == "__main__":
    unittest.main()
