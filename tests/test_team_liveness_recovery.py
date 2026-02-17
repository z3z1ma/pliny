from __future__ import annotations

import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path
from unittest import mock

from agent_loom.team import core as team


class TestTeamLivenessRecovery(unittest.TestCase):
    def test_manager_bootstrap_recovers_unhealthy_existing_window(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            paths = team.RunPaths(repo_root=repo_root, team="cobra")
            paths.run_dir.mkdir(parents=True, exist_ok=True)
            tickets_dir = repo_root / ".loom" / "ticket"
            tickets_dir.mkdir(parents=True, exist_ok=True)

            run = {
                "team": "cobra",
                "run_id": "run-123",
                "harness": "opencode",
                "opencode": {
                    "bin": "",
                    "manager_agent": team.DEFAULT_MANAGER_AGENT,
                    "models": {"manager": ""},
                    "model": "",
                },
                "manager": {"window": "manager", "pane_id": "%1"},
                "merge": {"config": {"target_branch": "main", "remote": "origin", "push": True}},
            }

            with (
                mock.patch.object(team, "_require_bin"),
                mock.patch.object(team, "render_manager_prompt", return_value="prompt"),
                mock.patch.object(team, "_team_tui_argv", return_value=["loom", "team", "tui"]),
                mock.patch.object(team, "_model_for_role", return_value=""),
                mock.patch.object(team, "tmux_has_session", return_value=True),
                mock.patch.object(team, "tmux_window_exists", return_value=True),
                mock.patch.object(team, "_recipient_health", return_value=("dead", {}, {})),
                mock.patch.object(team, "_recovery_gate_allows", return_value=(True, "")),
                mock.patch.object(team, "tmux_kill_window") as kill_window,
                mock.patch.object(team, "tmux_cmd") as tmux_cmd,
                mock.patch.object(team, "tmux_set_option"),
                mock.patch.object(team, "tmux_format", return_value="%99"),
                mock.patch.object(team, "tmux_mark_pane"),
            ):
                team._start_boot_manager_session(
                    paths=paths,
                    run=run,
                    root=repo_root,
                    team="cobra",
                    session="team-cobra",
                    requested_harness="opencode",
                    manager_window="manager",
                    force=False,
                    tickets_dir=tickets_dir,
                    charter_path=paths.charter_file,
                )

            kill_window.assert_called_once_with("team-cobra", "manager")
            self.assertTrue(any("new-window" in call.args[0] for call in tmux_cmd.call_args_list))

    def test_respawn_worker_recovers_unhealthy_existing_window(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            paths = team.RunPaths(repo_root=repo_root, team="cobra")
            paths.run_dir.mkdir(parents=True, exist_ok=True)

            worktree = paths.worktrees_dir / "al-1"
            (worktree / ".opencode" / "agents").mkdir(parents=True, exist_ok=True)
            (worktree / ".opencode" / "agents" / f"{team.DEFAULT_WORKER_AGENT}.md").write_text(
                "---\n---\n", encoding="utf-8"
            )

            run = {
                "team": "cobra",
                "run_id": "run-123",
                "harness": "opencode",
                "opencode": {
                    "bin": "",
                    "worker_agent": team.DEFAULT_WORKER_AGENT,
                    "models": {"worker": ""},
                    "model": "",
                },
                "workers": {},
                "sprint": {},
            }
            worker = {
                "worker_id": "w1",
                "role": "worker",
                "ticket_id": "al-1",
                "worktree": str(worktree),
                "window": "w1-al-1",
                "pane_id": "%1",
                "branch": "team/al-1",
                "base": "main",
                "retired": False,
            }

            @dataclass
            class _Ticket:
                id: str
                title: str
                status: str

            @dataclass
            class _Payload:
                ticket: _Ticket

            with (
                mock.patch.object(team, "_require_bin"),
                mock.patch.object(team, "tmux_window_exists", return_value=True),
                mock.patch.object(team, "tmux_format", return_value="%2"),
                mock.patch.object(team, "_recipient_health", return_value=("stale", {}, {})),
                mock.patch.object(team, "_recovery_gate_allows", return_value=(True, "")),
                mock.patch.object(team, "tmux_kill_window") as kill_window,
                mock.patch.object(
                    team,
                    "ticket_show",
                    return_value=_Payload(ticket=_Ticket(id="al-1", title="x", status="open")),
                ),
                mock.patch.object(team, "render_worker_prompt", return_value="prompt"),
                mock.patch.object(team, "_team_tui_argv", return_value=["loom", "team", "tui"]),
                mock.patch.object(team, "tmux_unique_window_name", return_value="w1-al-1-new"),
                mock.patch.object(team, "tmux_cmd"),
                mock.patch.object(team, "tmux_mark_pane"),
            ):
                did, updated = team._respawn_active_worker_if_missing(
                    paths=paths,
                    run=run,
                    worker_id="w1",
                    worker=worker,
                    session="team-cobra",
                    repo_root=repo_root,
                )

            self.assertTrue(did)
            self.assertEqual(str(updated.get("window") or ""), "w1-al-1-new")
            kill_window.assert_called_once_with("team-cobra", "w1-al-1")


if __name__ == "__main__":
    unittest.main()
