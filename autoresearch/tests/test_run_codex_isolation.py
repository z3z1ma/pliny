import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from autoresearch import run_codex_isolation


class RunCodexIsolationTest(unittest.TestCase):
    def test_dry_run_plan_records_isolation_args(self):
        plan = run_codex_isolation.build_plan(2)

        self.assertEqual(2, len(plan["planned_runs"]))
        self.assertEqual(
            ["codex", "--ask-for-approval", "never", "--disable", "plugins", "exec"],
            plan["argv_policy"],
        )
        self.assertIn("--ignore-user-config", plan["exec_args"])
        self.assertIn("CODEX_HOME", plan["env_policy"])

    def test_run_battery_records_outputs_without_workspace_contamination(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch("subprocess.run", side_effect=_fake_run):
                summary = run_codex_isolation.run_battery(tmp, 1)

            root = Path(tmp)
            run_dir = root / "run-0001"
            self.assertEqual(1, summary["run_count"])
            self.assertTrue(summary["all_exit_zero"])
            self.assertTrue(summary["all_expected_fragments_present"])
            self.assertFalse(summary["any_workspace_contamination"])
            self.assertTrue((run_dir / "command.json").exists())
            self.assertTrue((run_dir / "workspace-manifest.json").exists())
            command = json.loads((run_dir / "command.json").read_text())
            self.assertIn("--disable", command["argv"])
            self.assertIn("--ignore-user-config", command["argv"])

    def test_invalid_max_runs_is_rejected(self):
        with self.assertRaises(run_codex_isolation.IsolationError):
            run_codex_isolation.build_plan(0)


def _fake_run(argv, stdout, stderr, text):
    last_message = Path(argv[argv.index("--output-last-message") + 1])
    last_message.parent.mkdir(parents=True, exist_ok=True)
    last_message.write_text("CODEX_ISOLATION_SMOKE_1_OK", encoding="utf-8")
    return mock.Mock(
        returncode=0,
        stdout=(
            '{"type":"thread.started","thread_id":"test"}\n'
            '{"type":"turn.completed","usage":{"input_tokens":10,"output_tokens":3}}\n'
        ),
        stderr="",
    )


if __name__ == "__main__":
    unittest.main()
