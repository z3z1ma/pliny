import json
import tempfile
import unittest
from pathlib import Path

from agent_loom.team import core as team


class TestTeamStartRefactorHelpers(unittest.TestCase):
    def _paths(self, repo_root: Path, team_name: str = "cobra") -> team.RunPaths:
        paths = team.RunPaths(repo_root=repo_root, team=team_name)
        team._ensure_start_run_paths(paths)
        return paths

    def _config_state(self, source_root: Path) -> dict:
        return {
            "source": str((source_root / "team-config.yaml").resolve()),
            "loaded_at": "2026-02-17T00:00:00Z",
            "spec": {
                "harness": "opencode",
                "model": "gpt-main",
                "role_prompts": {
                    "append": {
                        "manager": "",
                        "architect": "",
                        "worker": "",
                        "integrator": "",
                    }
                },
                "worker": {"subagents": "encouraged"},
                "liveness": {
                    "heartbeat_interval_s": 20,
                    "stale_after_s": 90,
                    "dead_after_s": 240,
                    "recovery_cooldown_s": 180,
                    "max_recoveries_per_hour": 3,
                },
            },
        }

    def test_validated_start_max_headcount(self) -> None:
        self.assertIsNone(team._validated_start_max_headcount(None))
        self.assertEqual(team._validated_start_max_headcount(3), 3)
        self.assertEqual(team._validated_start_max_headcount("4"), 4)
        with self.assertRaises(team.TeamError) as ctx:
            team._validated_start_max_headcount(-1)
        self.assertEqual(ctx.exception.code, "ARG")

    def test_start_create_run_persists_core_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            paths = self._paths(repo_root)

            run = team._start_create_run(
                paths=paths,
                root=repo_root,
                team="cobra",
                objective="ship phase three",
                session="session-cobra",
                requested_harness="opencode",
                requested_bin="custom-opencode",
                team_config_state=self._config_state(repo_root),
                team_config_model="gpt-main",
                mounts=None,
                clear_mounts=False,
                max_headcount=5,
                target_branch="dev/next",
                remote="origin",
                push=True,
                model="",
                manager_model="gpt-manager",
                architect_model="",
                worker_model="",
                integrator_model="",
            )

            self.assertEqual(str(run.get("harness") or ""), "opencode")
            self.assertEqual(str(run.get("session") or ""), "session-cobra")
            self.assertEqual(
                str(((run.get("merge") or {}).get("config") or {}).get("target_branch") or ""),
                "dev/next",
            )
            self.assertEqual(str((run.get("defaults") or {}).get("base_ref") or ""), "dev/next")
            self.assertEqual(
                str((((run.get("opencode") or {}).get("models") or {}).get("manager") or "")),
                "gpt-manager",
            )
            self.assertEqual(str((run.get("opencode") or {}).get("bin") or ""), "custom-opencode")
            self.assertEqual(int(((run.get("limits") or {}).get("max_headcount") or 0)), 5)
            self.assertIn("team_config", run)

            persisted = json.loads(paths.run_file.read_text(encoding="utf-8"))
            self.assertEqual(str(persisted.get("session") or ""), "session-cobra")

    def test_start_update_existing_run_adopts_persisted_session(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            paths = self._paths(repo_root)
            team._start_create_run(
                paths=paths,
                root=repo_root,
                team="cobra",
                objective="seed",
                session="persisted-session",
                requested_harness="opencode",
                requested_bin="",
                team_config_state=self._config_state(repo_root),
                team_config_model="gpt-main",
                mounts=None,
                clear_mounts=False,
                max_headcount=None,
                target_branch="main",
                remote="origin",
                push=None,
                model="",
                manager_model="",
                architect_model="",
                worker_model="",
                integrator_model="",
            )

            updated_run, adopted_session = team._start_update_existing_run(
                paths=paths,
                root=repo_root,
                session="cli-session",
                session_provided=False,
                config_provided=False,
                requested_harness="opencode",
                requested_bin="",
                harness_provided=False,
                team_config_state=self._config_state(repo_root),
                team_config_harness="",
                team_config_model="gpt-main",
                mounts=None,
                clear_mounts=False,
                max_headcount=None,
                target_branch="",
                remote="",
                push=None,
                model="",
                manager_model="override-manager",
                architect_model="",
                worker_model="",
                integrator_model="",
            )

            self.assertEqual(adopted_session, "persisted-session")
            self.assertEqual(
                str((((updated_run.get("opencode") or {}).get("models") or {}).get("manager") or "")),
                "override-manager",
            )

    def test_start_update_existing_run_respects_explicit_session_and_clear_mounts(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            (repo_root / ".venv").mkdir(parents=True, exist_ok=True)
            paths = self._paths(repo_root)
            team._start_create_run(
                paths=paths,
                root=repo_root,
                team="cobra",
                objective="seed",
                session="persisted-session",
                requested_harness="opencode",
                requested_bin="",
                team_config_state=self._config_state(repo_root),
                team_config_model="",
                mounts=[".venv:.venv"],
                clear_mounts=False,
                max_headcount=None,
                target_branch="main",
                remote="origin",
                push=None,
                model="",
                manager_model="",
                architect_model="",
                worker_model="",
                integrator_model="",
            )

            updated_run, updated_session = team._start_update_existing_run(
                paths=paths,
                root=repo_root,
                session="explicit-session",
                session_provided=True,
                config_provided=False,
                requested_harness="opencode",
                requested_bin="",
                harness_provided=False,
                team_config_state=self._config_state(repo_root),
                team_config_harness="",
                team_config_model="",
                mounts=None,
                clear_mounts=True,
                max_headcount=None,
                target_branch="",
                remote="",
                push=None,
                model="",
                manager_model="",
                architect_model="",
                worker_model="",
                integrator_model="",
            )

            self.assertEqual(updated_session, "explicit-session")
            self.assertEqual(str(updated_run.get("session") or ""), "explicit-session")
            self.assertEqual(list(updated_run.get("mounts") or []), [])

    def test_start_create_run_uses_cli_mounts_when_provided(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            (repo_root / ".env").write_text("KEY=VALUE\n", encoding="utf-8")
            paths = self._paths(repo_root)

            run = team._start_create_run(
                paths=paths,
                root=repo_root,
                team="cobra",
                objective="seed",
                session="persisted-session",
                requested_harness="opencode",
                requested_bin="",
                team_config_state=self._config_state(repo_root),
                team_config_model="",
                mounts=[".env:.env"],
                clear_mounts=False,
                max_headcount=None,
                target_branch="main",
                remote="origin",
                push=None,
                model="",
                manager_model="",
                architect_model="",
                worker_model="",
                integrator_model="",
            )

            self.assertEqual(list(run.get("mounts") or []), [{"src": ".env", "dst": ".env"}])


if __name__ == "__main__":
    unittest.main()
