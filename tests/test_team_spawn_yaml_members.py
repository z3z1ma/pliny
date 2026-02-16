from __future__ import annotations

import dataclasses
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from agent_loom.team import core as team


@dataclasses.dataclass
class _Ticket:
    id: str
    title: str
    status: str


@dataclasses.dataclass
class _TicketPayload:
    ticket: _Ticket


class TestTeamSpawnYamlMembers(unittest.TestCase):
    def _write_run(self, repo_root: Path, *, composition_spec: dict, harness: str = "opencode") -> team.RunPaths:
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
            "composition": {
                "source": str(repo_root / "composition.yaml"),
                "loaded_at": "2026-01-01T00:00:00Z",
                "spec": composition_spec,
            },
            "opencode": {
                "model": "",
                "models": {
                    "manager": "",
                    "worker": "",
                    "investigator": "",
                    "integrator": "",
                },
                "manager_agent": team.DEFAULT_MANAGER_AGENT,
                "worker_agent": team.DEFAULT_WORKER_AGENT,
                "investigator_agent": team.DEFAULT_INVESTIGATOR_AGENT,
                "integrator_agent": team.DEFAULT_INTEGRATOR_AGENT,
                "bin": "",
            },
            "codex": {
                "model": "",
                "models": {
                    "manager": "",
                    "worker": "",
                    "investigator": "",
                    "integrator": "",
                },
                "manager_agent": team.DEFAULT_MANAGER_AGENT,
                "worker_agent": team.DEFAULT_WORKER_AGENT,
                "investigator_agent": team.DEFAULT_INVESTIGATOR_AGENT,
                "integrator_agent": team.DEFAULT_INTEGRATOR_AGENT,
                "bin": "",
            },
        }
        paths.run_file.write_text(json.dumps(run), encoding="utf-8")
        return paths

    def test_spawn_uses_mapped_yaml_member_harness_and_agent(self) -> None:
        spec = {
            "version": 1,
            "metadata": {"name": "x"},
            "members": [
                {
                    "id": "worker-template",
                    "role": "worker",
                    "lifecycle": "ephemeral",
                    "source": "byo",
                    "agent": "custom-worker",
                    "harness": "codex",
                }
            ],
            "worktree_mappings": [{"pattern": "al-1234", "member": "worker-template"}],
            "communication": {
                "channel": "inbox_only",
                "require_ack": True,
                "escalation": {"target_role": "manager", "timeout_seconds": 60, "max_retries": 1},
            },
            "byo_agents": {"custom-worker": {"command": "codex --mode worker"}},
        }

        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            self._write_run(repo_root, composition_spec=spec)

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
                mock.patch.object(team, "ticket_show", return_value=_TicketPayload(ticket=_Ticket(id="al-1234", title="x", status="open"))),
                mock.patch.object(team, "_ensure_worktree", side_effect=fake_ensure_worktree),
                mock.patch.object(team, "tmux_unique_window_name", return_value="w1-al-1234"),
                mock.patch.object(team, "tmux_cmd"),
                mock.patch.object(team, "tmux_format", return_value="%11"),
                mock.patch.object(team, "tmux_mark_pane"),
                mock.patch.object(team, "write_event"),
                mock.patch.object(team, "_team_tui_argv", side_effect=fake_team_tui_argv),
            ):
                res = team.spawn(team="MiyagiDo", ticket_id="al-1234", repo=repo_root)

            self.assertEqual(str((res.worker or {}).get("composition_member_id") or ""), "worker-template")
            self.assertEqual(str((res.worker or {}).get("composition_source") or ""), "byo")
            self.assertTrue(argv_calls)
            self.assertEqual(argv_calls[0].get("harness"), "codex")
            self.assertEqual(argv_calls[0].get("agent"), "custom-worker")

    def test_spawn_rejects_always_on_worker_member(self) -> None:
        spec = {
            "version": 1,
            "metadata": {"name": "x"},
            "members": [
                {
                    "id": "worker-always",
                    "role": "worker",
                    "lifecycle": "always_on",
                    "source": "loom",
                    "agent": "loom-team-worker",
                    "harness": "opencode",
                }
            ],
            "worktree_mappings": [{"pattern": "al-2000", "member": "worker-always"}],
            "communication": {
                "channel": "inbox_only",
                "require_ack": True,
                "escalation": {"target_role": "manager", "timeout_seconds": 60, "max_retries": 1},
            },
            "byo_agents": {},
        }

        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            self._write_run(repo_root, composition_spec=spec)

            def fake_ensure_worktree(**kwargs):
                wt_path = Path(str(kwargs["path"]))
                wt_path.mkdir(parents=True, exist_ok=True)
                return {"path": str(wt_path), "branch": "team/al-2000", "base": "main"}

            with (
                mock.patch("agent_loom.team.run_state.canonical_repo_root", return_value=repo_root),
                mock.patch.object(team, "_require_role"),
                mock.patch.object(team, "_require_bin"),
                mock.patch.object(team, "tmux_has_session", return_value=True),
                mock.patch.object(team, "ticket_show", return_value=_TicketPayload(ticket=_Ticket(id="al-2000", title="x", status="open"))),
                mock.patch.object(team, "_ensure_worktree", side_effect=fake_ensure_worktree),
                mock.patch.object(team, "tmux_unique_window_name", return_value="w1-al-2000"),
            ):
                with self.assertRaises(team.TeamError) as ctx:
                    team.spawn(team="MiyagiDo", ticket_id="al-2000", repo=repo_root)

            self.assertIn("must use ephemeral", str(ctx.exception))

    def test_spawn_fails_on_ambiguous_yaml_member_mapping(self) -> None:
        spec = {
            "version": 1,
            "metadata": {"name": "x"},
            "members": [
                {
                    "id": "worker-a",
                    "role": "worker",
                    "lifecycle": "ephemeral",
                    "source": "loom",
                    "agent": "loom-team-worker",
                    "harness": "opencode",
                },
                {
                    "id": "worker-b",
                    "role": "worker",
                    "lifecycle": "ephemeral",
                    "source": "loom",
                    "agent": "loom-team-worker",
                    "harness": "opencode",
                },
            ],
            "worktree_mappings": [
                {"pattern": "al-9999", "member": "worker-a"},
                {"pattern": "al-*", "member": "worker-b"},
            ],
            "communication": {
                "channel": "inbox_only",
                "require_ack": True,
                "escalation": {"target_role": "manager", "timeout_seconds": 60, "max_retries": 1},
            },
            "byo_agents": {},
        }

        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            self._write_run(repo_root, composition_spec=spec)

            def fake_ensure_worktree(**kwargs):
                wt_path = Path(str(kwargs["path"]))
                wt_path.mkdir(parents=True, exist_ok=True)
                return {"path": str(wt_path), "branch": "team/al-9999", "base": "main"}

            with (
                mock.patch("agent_loom.team.run_state.canonical_repo_root", return_value=repo_root),
                mock.patch.object(team, "_require_role"),
                mock.patch.object(team, "_require_bin"),
                mock.patch.object(team, "tmux_has_session", return_value=True),
                mock.patch.object(team, "ticket_show", return_value=_TicketPayload(ticket=_Ticket(id="al-9999", title="x", status="open"))),
                mock.patch.object(team, "_ensure_worktree", side_effect=fake_ensure_worktree),
                mock.patch.object(team, "tmux_unique_window_name", return_value="w1-al-9999"),
            ):
                with self.assertRaises(team.TeamError) as ctx:
                    team.spawn(team="MiyagiDo", ticket_id="al-9999", repo=repo_root)

            self.assertIn("ambiguous", str(ctx.exception).lower())


if __name__ == "__main__":
    unittest.main()
