import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from agent_loom.team import core as team


class TestTeamSpawnIntegrator(unittest.TestCase):
    def test_spawn_integrator_allows_dirty_worktree_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            team_name = "MiyagiDo"

            paths = team.RunPaths(
                repo_root=repo_root, team=team.sanitize(team_name) or "miyagido"
            )
            paths.run_dir.mkdir(parents=True, exist_ok=True)

            run = {
                "team": team_name,
                "run_id": "abcdef1234567890",
                "session": f"team-{paths.team}",
                "repo_root": str(repo_root),
            }
            paths.run_file.write_text(json.dumps(run), encoding="utf-8")

            called: dict[str, object] = {}

            def fake_ensure_worktree(**kwargs):
                called.update(kwargs)
                wt_path = Path(str(kwargs["path"]))
                wt_path.mkdir(parents=True, exist_ok=True)
                agents_dir = wt_path / ".opencode" / "agents"
                agents_dir.mkdir(parents=True, exist_ok=True)
                for a in (
                    team.DEFAULT_MANAGER_AGENT,
                    team.DEFAULT_WORKER_AGENT,
                    team.DEFAULT_INVESTIGATOR_AGENT,
                    team.DEFAULT_INTEGRATOR_AGENT,
                ):
                    (agents_dir / f"{a}.md").write_text("---\n---\n", encoding="utf-8")
                return {
                    "path": str(wt_path),
                    "branch": str(kwargs.get("branch") or ""),
                    "base": str(kwargs.get("base_ref") or ""),
                }

            with (
                mock.patch(
                    "agent_loom.team.run_state.canonical_repo_root",
                    return_value=repo_root,
                ),
                mock.patch.object(team, "_require_bin"),
                mock.patch.object(team, "tmux_has_session", return_value=True),
                mock.patch.object(team, "tmux_window_exists", return_value=False),
                mock.patch.object(
                    team, "tmux_unique_window_name", return_value="integrator"
                ),
                mock.patch.object(team, "tmux_new_window", return_value="%71"),
                mock.patch.object(team, "tmux_mark_pane"),
                mock.patch.object(
                    team, "_ensure_worktree", side_effect=fake_ensure_worktree
                ),
                mock.patch.object(team, "_ensure_opencode_agents"),
                mock.patch.object(team, "_ensure_opencode_worktree_runtime"),
                mock.patch.object(team, "_ensure_claude_agents"),
                mock.patch.object(
                    team, "render_integrator_prompt", return_value="prompt"
                ),
                mock.patch.object(team, "write_event"),
            ):
                team.spawn_integrator(team=team_name, repo=repo_root)

            self.assertEqual(bool(called.get("allow_dirty")), True)

    def test_spawn_integrator_can_require_clean(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            team_name = "MiyagiDo"

            paths = team.RunPaths(
                repo_root=repo_root, team=team.sanitize(team_name) or "miyagido"
            )
            paths.run_dir.mkdir(parents=True, exist_ok=True)

            run = {
                "team": team_name,
                "run_id": "abcdef1234567890",
                "session": f"team-{paths.team}",
                "repo_root": str(repo_root),
            }
            paths.run_file.write_text(json.dumps(run), encoding="utf-8")

            called: dict[str, object] = {}

            def fake_ensure_worktree(**kwargs):
                called.update(kwargs)
                wt_path = Path(str(kwargs["path"]))
                wt_path.mkdir(parents=True, exist_ok=True)
                agents_dir = wt_path / ".opencode" / "agents"
                agents_dir.mkdir(parents=True, exist_ok=True)
                for a in (
                    team.DEFAULT_MANAGER_AGENT,
                    team.DEFAULT_WORKER_AGENT,
                    team.DEFAULT_INVESTIGATOR_AGENT,
                    team.DEFAULT_INTEGRATOR_AGENT,
                ):
                    (agents_dir / f"{a}.md").write_text("---\n---\n", encoding="utf-8")
                return {
                    "path": str(wt_path),
                    "branch": str(kwargs.get("branch") or ""),
                    "base": str(kwargs.get("base_ref") or ""),
                }

            with (
                mock.patch(
                    "agent_loom.team.run_state.canonical_repo_root",
                    return_value=repo_root,
                ),
                mock.patch.object(team, "_require_bin"),
                mock.patch.object(team, "tmux_has_session", return_value=True),
                mock.patch.object(team, "tmux_window_exists", return_value=False),
                mock.patch.object(
                    team, "tmux_unique_window_name", return_value="integrator"
                ),
                mock.patch.object(team, "tmux_new_window", return_value="%71"),
                mock.patch.object(team, "tmux_mark_pane"),
                mock.patch.object(
                    team, "_ensure_worktree", side_effect=fake_ensure_worktree
                ),
                mock.patch.object(team, "_ensure_opencode_agents"),
                mock.patch.object(team, "_ensure_opencode_worktree_runtime"),
                mock.patch.object(team, "_ensure_claude_agents"),
                mock.patch.object(
                    team, "render_integrator_prompt", return_value="prompt"
                ),
                mock.patch.object(team, "write_event"),
            ):
                team.spawn_integrator(
                    team=team_name, repo=repo_root, require_clean=True
                )

            self.assertEqual(bool(called.get("allow_dirty")), False)

    def test_spawn_integrator_applies_mounts_even_on_refresh(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            team_name = "MiyagiDo"

            (repo_root / ".venv").mkdir(parents=True, exist_ok=True)

            paths = team.RunPaths(
                repo_root=repo_root, team=team.sanitize(team_name) or "miyagido"
            )
            paths.run_dir.mkdir(parents=True, exist_ok=True)

            run = {
                "team": team_name,
                "run_id": "abcdef1234567890",
                "session": f"team-{paths.team}",
                "repo_root": str(repo_root),
                "mounts": [{"src": ".venv", "dst": ".venv"}],
                "workers": {
                    "integrator": {
                        "worker_id": "integrator",
                        "role": team.ROLE_INTEGRATOR,
                        "retired": False,
                        "window": "integrator",
                        "pane_id": "%1",
                    }
                },
                "opencode": {"bin": ""},
            }
            paths.run_file.write_text(json.dumps(run), encoding="utf-8")

            def fake_ensure_worktree(**kwargs):
                wt_path = Path(str(kwargs["path"]))
                wt_path.mkdir(parents=True, exist_ok=True)
                agents_dir = wt_path / ".opencode" / "agents"
                agents_dir.mkdir(parents=True, exist_ok=True)
                for a in (
                    team.DEFAULT_MANAGER_AGENT,
                    team.DEFAULT_WORKER_AGENT,
                    team.DEFAULT_INVESTIGATOR_AGENT,
                    team.DEFAULT_INTEGRATOR_AGENT,
                ):
                    (agents_dir / f"{a}.md").write_text("---\n---\n", encoding="utf-8")
                return {
                    "path": str(wt_path),
                    "branch": str(kwargs.get("branch") or ""),
                    "base": str(kwargs.get("base_ref") or ""),
                }

            with (
                mock.patch(
                    "agent_loom.team.run_state.canonical_repo_root",
                    return_value=repo_root,
                ),
                mock.patch.object(team, "_require_bin"),
                mock.patch.object(team, "tmux_has_session", return_value=True),
                mock.patch.object(team, "tmux_window_exists", return_value=True),
                mock.patch.object(team, "tmux_format", return_value="%71"),
                mock.patch.object(
                    team, "_ensure_worktree", side_effect=fake_ensure_worktree
                ),
                mock.patch.object(team, "_ensure_opencode_agents"),
                mock.patch.object(team, "_ensure_opencode_worktree_runtime"),
                mock.patch.object(team, "_ensure_claude_agents"),
                mock.patch.object(team, "write_event"),
                mock.patch.object(team, "_apply_mounts") as apply_mounts,
            ):
                res = team.spawn_integrator(team=team_name, repo=repo_root)

            self.assertEqual(bool(res.respawned), False)
            apply_mounts.assert_called()


if __name__ == "__main__":
    unittest.main()
