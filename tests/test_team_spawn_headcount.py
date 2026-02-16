import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from agent_loom.team import core as team
from agent_loom.team import worker_planning


class TestTeamSpawnHeadcount(unittest.TestCase):
    def test_worker_planning_headcount_helpers(self) -> None:
        run = {
            "limits": {"max_headcount": "2"},
            "workers": {
                "w2": {"role": team.ROLE_WORKER, "retired": False},
                "w1": {"role": team.ROLE_WORKER, "retired": False},
                "w3": {"role": team.ROLE_WORKER, "retired": True},
                "integrator": {"role": team.ROLE_INTEGRATOR, "retired": False},
            },
        }

        self.assertEqual(worker_planning.max_headcount(run), 2)
        active_count, active_ids, active_roles = worker_planning.active_spawn_headcount(
            run
        )
        self.assertEqual(active_count, 2)
        self.assertEqual(active_ids, ["w1", "w2"])
        self.assertEqual(
            active_roles,
            {"w1": team.ROLE_WORKER, "w2": team.ROLE_WORKER},
        )

    def test_spawn_fails_forward_when_at_max_headcount(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            team_name = "CobraKai"

            paths = team.RunPaths(
                repo_root=repo_root, team=team.sanitize(team_name) or "cobrakai"
            )
            paths.run_dir.mkdir(parents=True, exist_ok=True)

            run = {
                "team": team_name,
                "run_id": "abcdef1234567890",
                "session": f"team-{paths.team}",
                "repo_root": str(repo_root),
                "limits": {"max_headcount": 1},
                "workers": {
                    "w1": {
                        "worker_id": "w1",
                        "role": team.ROLE_WORKER,
                        "retired": False,
                    },
                    "w2": {
                        "worker_id": "w2",
                        "role": team.ROLE_WORKER,
                        "retired": True,
                    },
                    "integrator": {
                        "worker_id": "integrator",
                        "role": team.ROLE_INTEGRATOR,
                        "retired": False,
                    },
                },
                "opencode": {"bin": ""},
            }
            paths.run_file.write_text(json.dumps(run), encoding="utf-8")

            with (
                mock.patch(
                    "agent_loom.team.run_state.canonical_repo_root",
                    return_value=repo_root,
                ),
                mock.patch.object(team, "_require_bin"),
                mock.patch.object(team, "_require_role"),
                mock.patch.object(team, "tmux_has_session", return_value=True),
                mock.patch.object(team, "ticket_show") as ticket_show,
            ):
                with self.assertRaises(team.TeamError) as ctx:
                    team.spawn(team=team_name, ticket_id="t-1", repo=repo_root)

            ticket_show.assert_not_called()
            self.assertEqual(ctx.exception.code, "HEADCOUNT")
            self.assertEqual(int(ctx.exception.exit_code), 2)
            data = ctx.exception.data or {}
            self.assertEqual(int(data.get("max_headcount") or 0), 1)
            self.assertEqual(int(data.get("active_count") or 0), 1)
            self.assertEqual(list(data.get("active_worker_ids") or []), ["w1"])

    def test_spawn_allows_unlimited_headcount(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            team_name = "CobraKai"

            paths = team.RunPaths(
                repo_root=repo_root, team=team.sanitize(team_name) or "cobrakai"
            )
            paths.run_dir.mkdir(parents=True, exist_ok=True)

            run = {
                "team": team_name,
                "run_id": "abcdef1234567890",
                "session": f"team-{paths.team}",
                "repo_root": str(repo_root),
                "limits": {"max_headcount": 0},
                "workers": {
                    "w1": {
                        "worker_id": "w1",
                        "role": team.ROLE_WORKER,
                        "retired": False,
                    },
                    "w2": {
                        "worker_id": "w2",
                        "role": team.ROLE_WORKER,
                        "retired": False,
                    },
                },
                "opencode": {"bin": ""},
            }
            paths.run_file.write_text(json.dumps(run), encoding="utf-8")

            def sentinel_ticket_show(*_a, **_k):
                raise team.TeamError("sentinel", code="SENTINEL", exit_code=2)

            with (
                mock.patch(
                    "agent_loom.team.run_state.canonical_repo_root",
                    return_value=repo_root,
                ),
                mock.patch.object(team, "_require_bin"),
                mock.patch.object(team, "_require_role"),
                mock.patch.object(team, "tmux_has_session", return_value=True),
                mock.patch.object(
                    team, "ticket_show", side_effect=sentinel_ticket_show
                ),
            ):
                with self.assertRaises(team.TeamError) as ctx:
                    team.spawn(team=team_name, ticket_id="t-1", repo=repo_root)

            self.assertEqual(ctx.exception.code, "SENTINEL")


if __name__ == "__main__":
    unittest.main()
