from __future__ import annotations

import dataclasses
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from agent_loom.team import core as team
from agent_loom.team import worker_planning
from agent_loom.team.composition_runtime import list_always_on_member_profiles


@dataclasses.dataclass
class _Ticket:
    id: str
    title: str
    status: str


@dataclasses.dataclass
class _TicketPayload:
    ticket: _Ticket


class TestTeamSpawnYamlMembers(unittest.TestCase):
    def test_worker_planning_always_on_profiles_dedup_by_member_id(self) -> None:
        run = {
            "harness": "opencode",
            "roster": {
                "spec": {
                    "version": 3,
                    "builtins": {
                        "manager": {"harness": "opencode", "agent": "loom-team-manager"},
                        "worker": {"harness": "opencode", "agent": "loom-team-worker"},
                        "integrator": {"harness": "opencode", "agent": "loom-team-integrator"},
                    },
                    "members": [
                        {
                            "id": "designer",
                            "role": "designer",
                            "always_on": True,
                            "workspace": "repo_root",
                        },
                        {
                            "id": "designer",
                            "role": "reviewer",
                            "always_on": True,
                            "workspace": "worktree",
                            "worktree_key": "review-lane",
                        },
                    ],
                }
            },
            "opencode": {
                "architect_agent": team.DEFAULT_ARCHITECT_AGENT,
            },
        }

        profiles = worker_planning.always_on_profiles_for_run(run)
        by_member = {str(profile.member_id): profile for profile in profiles}
        self.assertIn("architect", by_member)
        self.assertIn("designer", by_member)
        self.assertEqual(str(by_member["designer"].role), "reviewer")

    def test_worker_planning_workspace_mapping_defaults(self) -> None:
        profile = list(
            list_always_on_member_profiles(
                {
                    "roster": {
                        "spec": {
                            "version": 3,
                            "builtins": {
                                "manager": {"harness": "opencode", "agent": "loom-team-manager"},
                                "worker": {"harness": "opencode", "agent": "loom-team-worker"},
                                "architect": {
                                    "harness": "opencode",
                                    "agent": "loom-team-architect",
                                },
                                "integrator": {
                                    "harness": "opencode",
                                    "agent": "loom-team-integrator",
                                },
                            },
                            "members": [
                                {
                                    "id": "ux",
                                    "role": "reviewer",
                                    "always_on": True,
                                    "workspace": "unknown",
                                }
                            ],
                        }
                    }
                }
            )
        )[0]
        workspace, key = worker_planning.workspace_for_always_on_profile(profile)
        self.assertEqual(workspace, "repo_root")
        self.assertEqual(key, "")

    def _write_run(
        self,
        repo_root: Path,
        *,
        roster_spec: dict,
        harness: str = "opencode",
    ) -> team.RunPaths:
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
            "roster": {
                "source": str(repo_root / "roster.yaml"),
                "loaded_at": "2026-01-01T00:00:00Z",
                "spec": roster_spec,
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
                "worker_agent": team.DEFAULT_WORKER_AGENT,
                "architect_agent": team.DEFAULT_ARCHITECT_AGENT,
                "integrator_agent": team.DEFAULT_INTEGRATOR_AGENT,
                "bin": "",
            },
        }
        paths.run_file.write_text(json.dumps(run), encoding="utf-8")
        return paths

    def test_spawn_uses_builtin_worker_profile_harness_and_agent(self) -> None:
        spec = {
            "version": 3,
            "builtins": {
                "manager": {"harness": "opencode", "agent": "loom-team-manager"},
                "architect": {"harness": "opencode", "agent": "loom-team-architect"},
                "worker": {"harness": "codex", "agent": "custom-worker"},
                "integrator": {"harness": "claude", "agent": "loom-team-integrator"},
            },
        }

        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            self._write_run(repo_root, roster_spec=spec)

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
                    return_value=_TicketPayload(
                        ticket=_Ticket(id="al-1234", title="x", status="open")
                    ),
                ),
                mock.patch.object(team, "_ensure_worktree", side_effect=fake_ensure_worktree),
                mock.patch.object(team, "tmux_unique_window_name", return_value="w1-al-1234"),
                mock.patch.object(team, "tmux_cmd"),
                mock.patch.object(team, "tmux_format", return_value="%11"),
                mock.patch.object(team, "tmux_mark_pane"),
                mock.patch.object(team, "write_event"),
                mock.patch.object(team, "_team_tui_argv", side_effect=fake_team_tui_argv),
            ):
                res = team.spawn(team="MiyagiDo", ticket_id="al-1234", repo=repo_root)

            self.assertEqual(str((res.worker or {}).get("roster_member_id") or ""), "worker")
            self.assertEqual(str((res.worker or {}).get("roster_source") or ""), "loom")
            self.assertTrue(argv_calls)
            self.assertEqual(argv_calls[0].get("harness"), "codex")
            self.assertEqual(argv_calls[0].get("agent"), "custom-worker")

    def test_spawn_ignores_custom_members_for_worker_resolution(self) -> None:
        spec = {
            "version": 3,
            "builtins": {
                "manager": {"harness": "opencode", "agent": "loom-team-manager"},
                "architect": {"harness": "opencode", "agent": "loom-team-architect"},
                "worker": {"harness": "opencode", "agent": "loom-team-worker"},
                "integrator": {"harness": "claude", "agent": "loom-team-integrator"},
            },
            "members": [
                {
                    "id": "designer",
                    "role": "designer",
                    "harness": "codex",
                    "agent": "loom-team-worker",
                    "always_on": True,
                    "workspace": "worktree",
                }
            ],
            "communication": {"routes": []},
        }

        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            self._write_run(repo_root, roster_spec=spec)

            argv_calls: list[dict[str, str]] = []

            def fake_ensure_worktree(**kwargs):
                wt_path = Path(str(kwargs["path"]))
                wt_path.mkdir(parents=True, exist_ok=True)
                agents = wt_path / ".opencode" / "agents"
                agents.mkdir(parents=True, exist_ok=True)
                (agents / "loom-team-worker.md").write_text("---\n---\n", encoding="utf-8")
                return {"path": str(wt_path), "branch": "team/al-9999", "base": "main"}

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
                    return_value=_TicketPayload(
                        ticket=_Ticket(id="al-9999", title="x", status="open")
                    ),
                ),
                mock.patch.object(team, "_ensure_worktree", side_effect=fake_ensure_worktree),
                mock.patch.object(team, "tmux_unique_window_name", return_value="w1-al-9999"),
                mock.patch.object(team, "tmux_cmd"),
                mock.patch.object(team, "tmux_format", return_value="%11"),
                mock.patch.object(team, "tmux_mark_pane"),
                mock.patch.object(team, "write_event"),
                mock.patch.object(team, "_team_tui_argv", side_effect=fake_team_tui_argv),
            ):
                res = team.spawn(team="MiyagiDo", ticket_id="al-9999", repo=repo_root)

            self.assertEqual(str((res.worker or {}).get("roster_member_id") or ""), "worker")
            self.assertEqual(argv_calls[0].get("harness"), "opencode")
            self.assertEqual(argv_calls[0].get("agent"), "loom-team-worker")

    def test_on_demand_member_not_in_always_on_profiles(self) -> None:
        run = {
            "roster": {
                "spec": {
                    "version": 3,
                    "builtins": {
                        "manager": {"harness": "opencode", "agent": "loom-team-manager"},
                        "architect": {"harness": "opencode", "agent": "loom-team-architect"},
                        "worker": {"harness": "opencode", "agent": "loom-team-worker"},
                        "integrator": {"harness": "claude", "agent": "loom-team-integrator"},
                    },
                    "members": [
                        {
                            "id": "designer",
                            "role": "designer",
                            "harness": "codex",
                            "agent": "loom-team-worker",
                            "always_on": True,
                            "workspace": "worktree",
                        },
                        {
                            "id": "ux",
                            "role": "reviewer",
                            "harness": "codex",
                            "agent": "loom-team-worker",
                            "always_on": False,
                        },
                    ],
                }
            }
        }

        profiles = list(list_always_on_member_profiles(run))
        member_ids = {str(p.member_id) for p in profiles}
        self.assertNotIn("ux", member_ids)
        self.assertIn("designer", member_ids)

    def test_spawn_persona_registers_member(self) -> None:
        spec = {
            "version": 3,
            "builtins": {
                "manager": {"harness": "opencode", "agent": "loom-team-manager"},
                "architect": {"harness": "opencode", "agent": "loom-team-architect"},
                "worker": {"harness": "opencode", "agent": "loom-team-worker"},
                "integrator": {"harness": "claude", "agent": "loom-team-integrator"},
            },
            "members": [
                {
                    "id": "ux",
                    "role": "reviewer",
                    "harness": "codex",
                    "agent": "loom-team-worker",
                    "always_on": False,
                    "workspace": "repo_root",
                }
            ],
            "communication": {"routes": []},
        }

        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            paths = self._write_run(repo_root, roster_spec=spec)
            agents = repo_root / ".opencode" / "agents"
            agents.mkdir(parents=True, exist_ok=True)
            (agents / "loom-team-worker.md").write_text("---\n---\n", encoding="utf-8")

            argv_calls: list[dict[str, str]] = []

            def fake_team_tui_argv(**kwargs):
                argv_calls.append({k: str(v) for k, v in kwargs.items()})
                return ["loom", "team", "tui"]

            with (
                mock.patch("agent_loom.team.run_state.canonical_repo_root", return_value=repo_root),
                mock.patch("agent_loom.team.personas._require_role"),
                mock.patch("agent_loom.team.personas._require_bin"),
                mock.patch("agent_loom.team.personas.tmux_has_session", return_value=True),
                mock.patch("agent_loom.team.personas.tmux_window_exists", return_value=False),
                mock.patch(
                    "agent_loom.team.personas.tmux_unique_window_name",
                    return_value="w1-ux",
                ),
                mock.patch("agent_loom.team.personas.tmux_cmd"),
                mock.patch("agent_loom.team.personas.tmux_format", return_value="%99"),
                mock.patch("agent_loom.team.personas.tmux_mark_pane"),
                mock.patch.object(team, "_team_tui_argv", side_effect=fake_team_tui_argv),
            ):
                res = team.spawn_persona(team="MiyagiDo", member_id="ux", repo=repo_root)

            self.assertEqual(res.member_id, "ux")
            self.assertEqual(res.role, "reviewer")
            self.assertTrue(argv_calls)

            run_doc = json.loads(paths.run_file.read_text(encoding="utf-8"))
            workers = dict(run_doc.get("workers") or {})
            self.assertIn("ux", workers)
            self.assertEqual(str((workers.get("ux") or {}).get("role") or ""), "reviewer")


if __name__ == "__main__":
    unittest.main()
