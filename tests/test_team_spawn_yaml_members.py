from __future__ import annotations

import dataclasses
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from agent_loom.team import core as team
from agent_loom.team import worker_planning


@dataclasses.dataclass
class _Ticket:
    id: str
    title: str
    status: str


@dataclasses.dataclass
class _TicketPayload:
    ticket: _Ticket


class TestWorkerPlanning(unittest.TestCase):
    def test_agent_for_role_uses_selected_harness(self) -> None:
        run = {
            "codex": {
                "manager_agent": "m-codex",
                "worker_agent": "w-codex",
                "architect_agent": "a-codex",
                "integrator_agent": "i-codex",
            }
        }
        self.assertEqual(worker_planning.agent_for_role(run, "worker", harness="codex"), "w-codex")
        self.assertEqual(worker_planning.agent_for_role(run, "architect", harness="codex"), "a-codex")

    def test_model_for_role_prefers_role_override(self) -> None:
        run = {
            "opencode": {
                "model": "gpt-default",
                "models": {"worker": "gpt-worker"},
            }
        }
        self.assertEqual(worker_planning.model_for_role(run, "worker", harness="opencode"), "gpt-worker")
        self.assertEqual(worker_planning.model_for_role(run, "manager", harness="opencode"), "gpt-default")


class TestTeamSpawnCoreModel(unittest.TestCase):
    def _write_run(self, repo_root: Path, harness: str = "codex") -> team.RunPaths:
        team_name = "MiyagiDo"
        paths = team.RunPaths(repo_root=repo_root, team=team.sanitize(team_name) or "miyagido")
        paths.run_dir.mkdir(parents=True, exist_ok=True)
        run = {
            "team": team_name,
            "run_id": "run-123",
            "session": f"team-{paths.team}",
            "repo_root": str(repo_root),
            "harness": harness,
            "workers": {},
            "mounts": [],
            "team_config": {
                "source": "",
                "loaded_at": "2026-01-01T00:00:00Z",
                "spec": team.default_team_config_spec(),
            },
            "opencode": {
                "model": "",
                "models": {
                    "manager": "",
                    "worker": "",
                    "architect": "",
                    "integrator": "",
                },
                "manager_agent": team.DEFAULT_MANAGER_AGENT,
                "worker_agent": team.DEFAULT_WORKER_AGENT,
                "architect_agent": team.DEFAULT_ARCHITECT_AGENT,
                "integrator_agent": team.DEFAULT_INTEGRATOR_AGENT,
                "bin": "",
            },
            "codex": {
                "model": "",
                "models": {
                    "manager": "",
                    "worker": "",
                    "architect": "",
                    "integrator": "",
                },
                "manager_agent": team.DEFAULT_MANAGER_AGENT,
                "worker_agent": "custom-worker",
                "architect_agent": team.DEFAULT_ARCHITECT_AGENT,
                "integrator_agent": team.DEFAULT_INTEGRATOR_AGENT,
                "bin": "",
            },
            "merge": {"items": [], "branch": "", "config": {}},
            "limits": {"max_headcount": 0},
            "defaults": {"base_ref": "main"},
        }
        paths.run_file.write_text(json.dumps(run), encoding="utf-8")
        return paths

    def test_spawn_uses_core_worker_profile_and_canonical_worker_id(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            self._write_run(repo_root)

            argv_calls: list[dict[str, str]] = []

            def fake_ensure_worktree(**kwargs):
                wt_path = Path(str(kwargs["path"]))
                wt_path.mkdir(parents=True, exist_ok=True)
                agents = wt_path / ".opencode" / "agents"
                agents.mkdir(parents=True, exist_ok=True)
                (agents / "custom-worker.md").write_text("---\n---\n", encoding="utf-8")
                return {"path": str(wt_path), "branch": "team/al-1234", "base": "main"}

            def fake_team_tui_argv(**kwargs):
                argv_calls.append({k: str(v) for k, v in kwargs.items()})
                return ["loom", "team", "tui"]

            with (
                mock.patch("agent_loom.team.run_state.canonical_repo_root", return_value=repo_root),
                mock.patch.object(team, "_require_role"),
                mock.patch.object(team, "_require_bin"),
                mock.patch.object(team, "tmux_has_session", return_value=True),
                mock.patch.object(
                    team,
                    "ticket_show",
                    return_value=_TicketPayload(ticket=_Ticket(id="al-1234", title="x", status="open")),
                ),
                mock.patch.object(team, "_ensure_worktree", side_effect=fake_ensure_worktree),
                mock.patch.object(team, "tmux_unique_window_name", return_value="w-alpha-al-1234"),
                mock.patch.object(team, "tmux_cmd"),
                mock.patch.object(team, "tmux_format", return_value="%11"),
                mock.patch.object(team, "tmux_mark_pane"),
                mock.patch.object(team, "write_event"),
                mock.patch.object(team, "_team_tui_argv", side_effect=fake_team_tui_argv),
            ):
                res = team.spawn(
                    team="MiyagiDo",
                    ticket_id="al-1234",
                    worker_id="W-ALPHA",
                    repo=repo_root,
                )

            self.assertEqual(str((res.worker or {}).get("worker_id") or ""), "w-alpha")
            self.assertTrue("roster_member_id" not in (res.worker or {}))
            self.assertTrue(argv_calls)
            self.assertEqual(argv_calls[0].get("harness"), "codex")
            self.assertEqual(argv_calls[0].get("agent"), "custom-worker")


if __name__ == "__main__":
    unittest.main()
