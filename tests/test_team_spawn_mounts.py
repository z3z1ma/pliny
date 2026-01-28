import json
import subprocess
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path
from unittest import mock

from agent_loom.team import core as team


@dataclass(frozen=True)
class _Ticket:
    id: str
    title: str
    status: str


@dataclass(frozen=True)
class _TicketPayload:
    ticket: _Ticket


class TestTeamSpawnMounts(unittest.TestCase):
    def test_spawn_applies_mount_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            team_name = "MiyagiDo"

            # Source artifact in the canonical repo root.
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
                "workers": {},
                "opencode": {"bin": ""},
                "mounts": [{"src": ".venv", "dst": ".venv"}],
            }
            paths.run_file.write_text(json.dumps(run), encoding="utf-8")

            def fake_tmux_cmd(argv, **kwargs):
                _ = kwargs
                return subprocess.CompletedProcess(list(argv), 0, stdout="", stderr="")

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

            def fake_ticket_show(*_a, **_k):
                return _TicketPayload(
                    ticket=_Ticket(id="t-1", title="T", status="open")
                )

            with (
                mock.patch(
                    "agent_loom.team.run_state.canonical_repo_root",
                    return_value=repo_root,
                ),
                mock.patch.object(team, "_require_bin"),
                mock.patch.object(team, "tmux_has_session", return_value=True),
                mock.patch.object(team, "tmux_cmd", side_effect=fake_tmux_cmd),
                mock.patch.object(team, "tmux_unique_window_name", return_value="w1"),
                mock.patch.object(team, "tmux_format", return_value="%71"),
                mock.patch.object(team, "tmux_mark_pane"),
                mock.patch.object(team, "ticket_show", side_effect=fake_ticket_show),
                mock.patch.object(
                    team, "_ensure_worktree", side_effect=fake_ensure_worktree
                ),
                mock.patch.object(team, "render_worker_prompt", return_value="prompt"),
                mock.patch.object(team, "_team_tui_argv", return_value=["opencode"]),
                mock.patch.object(team, "write_event"),
                mock.patch.object(team, "_ensure_opencode_worktree_runtime"),
            ):
                res = team.spawn(team=team_name, ticket_id="t-1", repo=repo_root)

            wt = Path(str(res.worker.get("worktree") or "")).resolve()
            self.assertTrue(wt.is_dir())
            mounted = wt / ".venv"
            self.assertTrue(mounted.is_symlink())
            self.assertEqual(mounted.resolve(), (repo_root / ".venv").resolve())


if __name__ == "__main__":
    unittest.main()
