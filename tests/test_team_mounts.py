import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from agent_loom.team import core as team


class TestTeamMounts(unittest.TestCase):
    def test_start_persists_mounts_and_clear_mounts(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)

            # Mount sources live in the canonical repo root.
            (repo_root / ".env").write_text("KEY=VALUE\n", encoding="utf-8")
            (repo_root / ".venv").mkdir(parents=True, exist_ok=True)

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
                    mounts=[".env", ".venv:.shared/.venv"],
                )

                run_path = Path(res.run_dir) / "run.json"
                run = json.loads(run_path.read_text(encoding="utf-8"))
                self.assertEqual(
                    list(run.get("mounts") or []),
                    [
                        {"src": ".env", "dst": ".env"},
                        {"src": ".venv", "dst": ".shared/.venv"},
                    ],
                )

                team.start(team="CobraKai", repo=repo_root, clear_mounts=True)
                run2 = json.loads(run_path.read_text(encoding="utf-8"))
                self.assertEqual(list(run2.get("mounts") or []), [])

    def test_apply_mounts_is_idempotent_when_symlink_already_present(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            wt = repo_root / "wt"
            wt.mkdir(parents=True, exist_ok=True)

            (repo_root / ".venv").mkdir(parents=True, exist_ok=True)
            (wt / ".venv").symlink_to((repo_root / ".venv").resolve())

            team._apply_mounts(
                repo_root=repo_root,
                worktree_root=wt,
                mounts=[{"src": ".venv", "dst": ".venv"}],
            )

            mounted = wt / ".venv"
            self.assertTrue(mounted.is_symlink())
            self.assertEqual(mounted.resolve(), (repo_root / ".venv").resolve())

    def test_apply_mounts_refuses_parent_symlink_escape(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            wt = repo_root / "wt"
            wt.mkdir(parents=True, exist_ok=True)

            outside = repo_root / "outside"
            outside.mkdir(parents=True, exist_ok=True)

            (repo_root / ".venv").mkdir(parents=True, exist_ok=True)
            (wt / ".shared").symlink_to(outside)

            with self.assertRaises(team.TeamError) as cm:
                team._apply_mounts(
                    repo_root=repo_root,
                    worktree_root=wt,
                    mounts=[{"src": ".venv", "dst": ".shared/.venv"}],
                )

            self.assertIn("Refusing to mount outside worktree", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
