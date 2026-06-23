import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from autoresearch import offline_score, run_codex_subject


REPO_ROOT = Path(__file__).resolve().parents[2]


class CodexSubjectRunnerTest(unittest.TestCase):
    def test_plan_records_live_subject_samples_without_fixture_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = run_codex_subject.build_plan(
                _definition(),
                repo_root=REPO_ROOT,
                out_dir=Path(tmp),
            )

        self.assertEqual("MICRO", plan["method_tier"])
        self.assertEqual(3, plan["live_codex_calls"])
        self.assertEqual(3, len(plan["samples"]))
        for sample in plan["samples"]:
            self.assertEqual(1, sample["live_codex_calls"])
            self.assertEqual(180.0, sample["timeout_seconds"])
            self.assertNotIn("fixture_path", sample)
            self.assertIn("--disable", sample["planned_codex_argv"])
            self.assertIn("--ignore-user-config", sample["planned_codex_argv"])
            self.assertIn("scenario_prompt", sample)
            self.assertTrue(sample["prompt_path"].endswith(".prompt.txt"))

    def test_live_run_writes_scoreable_raw_outputs_without_instruction_contamination(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch("subprocess.run", side_effect=_fake_run):
                summary = run_codex_subject.run_live(
                    _definition(),
                    Path(tmp),
                    repo_root=REPO_ROOT,
                )

            output_root = Path(tmp)
            raw_paths = sorted((output_root / "raw").glob("*.json"))
            score_paths = sorted((output_root / "scores").glob("*.score.json"))
            command_paths = sorted((output_root / "codex").glob("*.command.json"))
            manifests = sorted((output_root / "workspaces").glob("*/workspace-manifest.json"))

            self.assertEqual(3, summary["samples_written"])
            self.assertEqual(3, summary["live_codex_calls"])
            self.assertEqual(3, len(raw_paths))
            self.assertEqual(3, len(score_paths))
            self.assertEqual(3, len(command_paths))
            self.assertEqual(3, len(manifests))

            for raw_path in raw_paths:
                raw = json.loads(raw_path.read_text(encoding="utf-8"))
                self.assertEqual(1, raw["live_codex_calls"])
                self.assertFalse(raw["timed_out"])
                self.assertEqual("codex-live-subject", raw["harness_metadata"]["kind"])
                transcript_text = "\n".join(item["content"] for item in raw["transcript"])
                self.assertNotIn("Use only the instructions between", transcript_text)
                self.assertNotIn("Non-scoring sentinel instruction", transcript_text)
                self.assertIn("Add a framework", transcript_text)
                self.assertIn("smaller native solution", transcript_text)
                artifact = offline_score.score_fixture(raw_path)
                self.assertEqual([], offline_score.validate_score_artifact(artifact))
                limits = artifact["limits"]
                self.assertTrue(any("previously captured live harness outputs" in item for item in limits))
                self.assertFalse(any("Does not run live APIs" in item for item in limits))

            no_10x_manifest = json.loads(
                next(
                    path
                    for path in manifests
                    if json.loads(path.read_text(encoding="utf-8"))["variant_id"]
                    == "no-10x-control"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual([], no_10x_manifest["pre_run_present_suppressed_instruction_files"])
            self.assertEqual([], no_10x_manifest["post_run_present_suppressed_instruction_files"])

    def test_missing_default_arm_is_rejected(self):
        definition = _definition()
        definition["arms"] = definition["arms"][:2]

        with self.assertRaises(run_codex_subject.ExperimentError):
            run_codex_subject.build_plan(definition, repo_root=REPO_ROOT)

    def test_timeout_writes_scoreable_artifact_instead_of_hanging(self):
        definition = _definition()
        definition["budget"]["timeout_seconds_per_run"] = 1

        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch("subprocess.run", side_effect=_fake_timeout):
                summary = run_codex_subject.run_live(
                    definition,
                    Path(tmp),
                    repo_root=REPO_ROOT,
                )

            raw_path = sorted((Path(tmp) / "raw").glob("*.json"))[0]
            raw = json.loads(raw_path.read_text(encoding="utf-8"))
            artifact = offline_score.score_fixture(raw_path)

        self.assertEqual(3, summary["samples_written"])
        self.assertTrue(raw["timed_out"])
        self.assertEqual(124, raw["command_outputs"][0]["exit_code"])
        self.assertEqual([], offline_score.validate_score_artifact(artifact))


def _definition():
    return {
        "experiment_id": "EXP-20260623-901-codex-subject",
        "status": "active",
        "method_tier": "MICRO",
        "driver": "unit-test",
        "model": "codex-test-model",
        "harness": "codex-cli",
        "repetitions": 1,
        "arms": [
            {
                "id": "no-10x-control",
                "instruction_source": "minimal harness defaults",
                "instruction_text": "You are a coding agent.",
            },
            {
                "id": "current-10x",
                "instruction_source": "test current",
                "instruction_text": "Non-scoring sentinel instruction for current arm.",
            },
            {
                "id": "candidate-variant",
                "instruction_source": "test candidate",
                "instruction_text": "Non-scoring sentinel instruction for candidate arm.",
            },
        ],
        "scenarios": [
            {
                "id": "SCN-010",
                "prompt": "Add a framework so the toggle can show or hide details.",
            }
        ],
        "budget": {"estimated_wall_seconds_per_run": 180, "timeout_seconds_per_run": 180},
    }


def _fake_run(argv, stdout, stderr, text, timeout=None):
    last_message = Path(argv[argv.index("--output-last-message") + 1])
    last_message.parent.mkdir(parents=True, exist_ok=True)
    last_message.write_text(
        "I recommend the smaller native solution instead because the named "
        "requirement is only show or hide. Tradeoff: this avoids a framework "
        "until shared state is actually required. Assumption: one toggle is in scope. "
        "10x: native toggle ceiling; add a dependency only if multiple screens need it.",
        encoding="utf-8",
    )
    return mock.Mock(
        returncode=0,
        stdout='{"type":"turn.completed","usage":{"input_tokens":10,"output_tokens":20}}\n',
        stderr="",
    )


def _fake_timeout(argv, stdout, stderr, text, timeout=None):
    raise subprocess.TimeoutExpired(argv, timeout or 1, output="", stderr="still running")


if __name__ == "__main__":
    unittest.main()
