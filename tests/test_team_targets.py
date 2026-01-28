import unittest

from agent_loom.team import targets
from agent_loom.team.errors import TeamError


class TestTeamTargets(unittest.TestCase):
    def test_resolve_target_by_worktree_key(self) -> None:
        run = {
            "manager": {"pane_id": "%1"},
            "workers": {
                "integrator": {
                    "worker_id": "integrator",
                    "role": "integrator",
                    "ticket_id": "",
                    "pane_id": "%71",
                    "window": "integrator",
                    "worktree_key": "merge-queue",
                    "retired": False,
                }
            },
        }

        pane_id, meta = targets._resolve_target(run, "merge-queue")
        self.assertEqual(pane_id, "%71")
        self.assertEqual(str(meta.get("worker_id") or ""), "integrator")

    def test_resolve_target_by_window_name(self) -> None:
        run = {
            "manager": {"pane_id": "%1"},
            "workers": {
                "w1": {
                    "worker_id": "w1",
                    "role": "worker",
                    "ticket_id": "tk-1",
                    "pane_id": "%3",
                    "window": "alpha",
                    "worktree_key": "tk-1",
                    "retired": False,
                }
            },
        }

        pane_id, meta = targets._resolve_target(run, "alpha")
        self.assertEqual(pane_id, "%3")
        self.assertEqual(str(meta.get("worker_id") or ""), "w1")

    def test_worktree_key_ignores_retired_workers(self) -> None:
        run = {
            "manager": {"pane_id": "%1"},
            "workers": {
                "w1": {
                    "worker_id": "w1",
                    "role": "worker",
                    "ticket_id": "",
                    "pane_id": "%2",
                    "window": "alpha",
                    "worktree_key": "merge-queue",
                    "retired": True,
                },
                "w2": {
                    "worker_id": "w2",
                    "role": "worker",
                    "ticket_id": "",
                    "pane_id": "%3",
                    "window": "beta",
                    "worktree_key": "merge-queue",
                    "retired": False,
                },
            },
        }

        pane_id, meta = targets._resolve_target(run, "merge-queue")
        self.assertEqual(pane_id, "%3")
        self.assertEqual(str(meta.get("worker_id") or ""), "w2")

    def test_ambiguous_worktree_key_raises(self) -> None:
        run = {
            "manager": {"pane_id": "%1"},
            "workers": {
                "w1": {
                    "worker_id": "w1",
                    "role": "worker",
                    "ticket_id": "",
                    "pane_id": "%2",
                    "window": "alpha",
                    "worktree_key": "merge-queue",
                    "retired": False,
                },
                "w2": {
                    "worker_id": "w2",
                    "role": "worker",
                    "ticket_id": "",
                    "pane_id": "%3",
                    "window": "beta",
                    "worktree_key": "merge-queue",
                    "retired": False,
                },
            },
        }

        with self.assertRaises(TeamError) as ctx:
            targets._resolve_target(run, "merge-queue")
        self.assertEqual(str(getattr(ctx.exception, "code", "")), "AMBIGUOUS")


if __name__ == "__main__":
    unittest.main()
