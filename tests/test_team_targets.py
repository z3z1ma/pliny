import unittest
from unittest import mock

from agent_loom.team import targets
from agent_loom.team.errors import TeamError


class TestTeamTargets(unittest.TestCase):
    def _run(self) -> dict:
        return {
            "manager": {"pane_id": "%1"},
            "workers": {
                "W1": {
                    "worker_id": "W1",
                    "role": "worker",
                    "ticket_id": "AL-1",
                    "pane_id": "%3",
                    "window": "w1",
                    "retired": False,
                },
                "architect": {
                    "worker_id": "architect",
                    "role": "architect",
                    "ticket_id": "",
                    "pane_id": "%8",
                    "window": "architect",
                    "retired": False,
                },
                "integrator": {
                    "worker_id": "integrator",
                    "role": "integrator",
                    "ticket_id": "",
                    "pane_id": "%9",
                    "window": "integrator",
                    "retired": False,
                },
            },
        }

    def test_resolve_manager_alias(self) -> None:
        pane_id, meta = targets._resolve_target(self._run(), "mgr")
        self.assertEqual(pane_id, "%1")
        self.assertEqual(str(meta.get("role") or ""), "manager")

    def test_resolve_architect(self) -> None:
        pane_id, meta = targets._resolve_target(self._run(), "architect")
        self.assertEqual(pane_id, "%8")
        self.assertEqual(str(meta.get("worker_id") or ""), "architect")

    def test_resolve_integrator(self) -> None:
        pane_id, meta = targets._resolve_target(self._run(), "integrator")
        self.assertEqual(pane_id, "%9")
        self.assertEqual(str(meta.get("worker_id") or ""), "integrator")

    def test_resolve_worker_target_casefolds_worker_id(self) -> None:
        pane_id, meta = targets._resolve_target(self._run(), "worker:w1")
        self.assertEqual(pane_id, "%3")
        self.assertEqual(str(meta.get("worker_id") or ""), "w1")

        pane_id2, meta2 = targets._resolve_target(self._run(), "worker:W1")
        self.assertEqual(pane_id2, "%3")
        self.assertEqual(str(meta2.get("worker_id") or ""), "w1")

    def test_resolve_ticket_target_casefolds_ticket_id(self) -> None:
        pane_id, meta = targets._resolve_target(self._run(), "ticket:al-1")
        self.assertEqual(pane_id, "%3")
        self.assertEqual(str(meta.get("ticket_id") or ""), "al-1")

        pane_id2, meta2 = targets._resolve_target(self._run(), "ticket:AL-1")
        self.assertEqual(pane_id2, "%3")
        self.assertEqual(str(meta2.get("ticket_id") or ""), "al-1")

    def test_plain_worker_id_is_not_valid_target_syntax(self) -> None:
        with self.assertRaises(TeamError):
            targets._resolve_target(self._run(), "w1")

    def test_workers_group_includes_only_worker_role(self) -> None:
        resolved = targets._resolve_targets(self._run(), "workers")
        self.assertEqual(len(resolved), 1)
        self.assertEqual(str(resolved[0].get("worker_id") or ""), "w1")
        self.assertEqual(str(resolved[0].get("target") or ""), "worker:w1")

    def test_workers_group_raises_when_empty(self) -> None:
        run = {
            "manager": {"pane_id": "%1"},
            "workers": {
                "architect": {
                    "worker_id": "architect",
                    "role": "architect",
                    "ticket_id": "",
                    "pane_id": "%8",
                    "window": "architect",
                    "retired": False,
                }
            },
        }
        with self.assertRaises(TeamError):
            targets._resolve_targets(run, "workers")

    def test_ticket_target_ambiguous_raises(self) -> None:
        run = {
            "manager": {"pane_id": "%1"},
            "workers": {
                "w1": {
                    "worker_id": "w1",
                    "role": "worker",
                    "ticket_id": "al-1",
                    "pane_id": "%3",
                    "window": "w1",
                    "retired": False,
                },
                "w2": {
                    "worker_id": "w2",
                    "role": "worker",
                    "ticket_id": "al-1",
                    "pane_id": "%4",
                    "window": "w2",
                    "retired": False,
                },
            },
        }
        with self.assertRaises(TeamError) as ctx:
            targets._resolve_target(run, "ticket:AL-1")
        self.assertEqual(str(getattr(ctx.exception, "code", "")), "AMBIGUOUS")

    def test_best_effort_tmux_nudge_uses_ctrl_enter_for_omp(self) -> None:
        run = {"harness": "omp", "manager": {"pane_id": "%1"}, "workers": {}}

        with (
            mock.patch.object(targets, "tmux_available", return_value=True),
            mock.patch.object(targets, "tmux_has_session", return_value=True),
            mock.patch.object(targets, "_resolve_target", return_value=("%3", {"pane_id": "%3"})),
            mock.patch.object(
                targets,
                "tmux_list_panes",
                return_value={"%3": {"current_command": "omp", "dead": "0"}},
            ),
            mock.patch.object(targets, "tmux_send_text") as send_text,
        ):
            ok, reason, _meta = targets._best_effort_tmux_nudge(
                run=run,
                session="team-cobra",
                target="manager",
                line="TEAM inbox id=abc",
                force=False,
            )

        self.assertTrue(ok)
        self.assertEqual(reason, "")
        send_text.assert_called_once_with("%3", "TEAM inbox id=abc", enter=True, ctrl_enter=True)


if __name__ == "__main__":
    unittest.main()
