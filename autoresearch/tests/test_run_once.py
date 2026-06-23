import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from autoresearch import run_once


REPO_ROOT = Path(__file__).resolve().parents[2]


class RunOnceTest(unittest.TestCase):
    def test_micro_run_writes_scores_and_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_once.run_once(_micro_definition(), tmp, repo_root=REPO_ROOT)

            root = Path(tmp)
            self.assertEqual("MICRO", result["method_tier"])
            self.assertEqual("autoresearch/run_micro.py", result["runner"])
            self.assertEqual(3, result["samples_written"])
            self.assertTrue((root / "summary.json").exists())
            self.assertTrue((root / "plan.json").exists())
            self.assertTrue((root / "report.md").exists())
            self.assertTrue((root / "canonical_guard.json").exists())
            self.assertEqual(3, len(list((root / "scores").glob("*.score.json"))))
            self.assertIn("exactly one iteration", result["loop_controller"])
            self.assertIn("canonical_guard.json", result["canonical_guard_path"])

    def test_full_run_writes_scores_workspaces_and_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_once.run_once(_full_definition(), tmp, repo_root=REPO_ROOT)

            root = Path(tmp)
            self.assertEqual("FULL", result["method_tier"])
            self.assertEqual("autoresearch/run_full_codex.py", result["runner"])
            self.assertEqual(3, result["samples_written"])
            self.assertTrue((root / "workspaces").exists())
            self.assertTrue((root / "report.md").exists())
            self.assertEqual(3, len(list((root / "scores").glob("*.score.json"))))

    def test_unsupported_tier_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            definition = _micro_definition()
            definition["method_tier"] = "LONG"

            with self.assertRaises(run_once.RunOnceError):
                run_once.run_once(definition, tmp, repo_root=REPO_ROOT)

    def test_cli_writes_json_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            experiment = root / "experiment.json"
            out_dir = root / "out"
            experiment.write_text(json.dumps(_micro_definition()), encoding="utf-8")
            stdout = io.StringIO()

            with contextlib.redirect_stdout(stdout):
                exit_code = run_once.main(["--experiment", str(experiment), "--out", str(out_dir)])

            self.assertEqual(0, exit_code)
            result = json.loads(stdout.getvalue())
            self.assertEqual("MICRO", result["method_tier"])
            self.assertTrue((out_dir / "report.md").exists())

    def test_cli_rejects_campaign_without_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            experiment = root / "experiment.json"
            campaign = root / "campaign.json"
            experiment.write_text(json.dumps(_micro_definition()), encoding="utf-8")
            campaign.write_text("{}", encoding="utf-8")
            stderr = io.StringIO()

            with contextlib.redirect_stderr(stderr):
                exit_code = run_once.main(
                    [
                        "--experiment",
                        str(experiment),
                        "--out",
                        str(root / "out"),
                        "--campaign",
                        str(campaign),
                        "--no-report",
                    ]
                )

            self.assertEqual(2, exit_code)
            self.assertIn("--campaign requires report", stderr.getvalue())

    def test_fails_when_canonical_file_changes_during_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "autoresearch").mkdir()
            (root / "SKILL.md").write_text("skill\n", encoding="utf-8")
            (root / "autoresearch/program.md").write_text("program\n", encoding="utf-8")

            def mutate(_definition, out_dir, repo_root):
                (repo_root / "SKILL.md").write_text("changed\n", encoding="utf-8")
                return {
                    "experiment_id": "EXP-20260623-701-run-once-micro",
                    "mode": "fixture-backed",
                    "samples_written": 0,
                    "plan_path": str(Path(out_dir) / "plan.json"),
                    "raw_output_dir": str(Path(out_dir) / "raw"),
                    "score_artifact_dir": str(Path(out_dir) / "scores"),
                }

            with mock.patch("autoresearch.run_once.run_micro.run_fixture_backed", side_effect=mutate):
                with mock.patch("autoresearch.run_once.report.write_report"):
                    with self.assertRaises(run_once.RunOnceError):
                        run_once.run_once(
                            _micro_definition(),
                            root / "out",
                            repo_root=root,
                        )

    def test_require_clean_canonical_refuses_dirty_git_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "autoresearch").mkdir()
            (root / "SKILL.md").write_text("skill\n", encoding="utf-8")
            (root / "autoresearch/program.md").write_text("program\n", encoding="utf-8")
            _git(root, "init")
            _git(root, "add", "SKILL.md", "autoresearch/program.md")
            _git(
                root,
                "-c",
                "user.email=test@example.com",
                "-c",
                "user.name=Test",
                "commit",
                "-m",
                "init",
            )
            (root / "SKILL.md").write_text("dirty\n", encoding="utf-8")

            with mock.patch("autoresearch.run_once.run_micro.run_fixture_backed"):
                with self.assertRaises(run_once.canonical_guard.CanonicalGuardError):
                    run_once.run_once(
                        _micro_definition(),
                        root / "out",
                        repo_root=root,
                        require_clean_canonical=True,
                    )


def _micro_definition():
    return {
        "experiment_id": "EXP-20260623-701-run-once-micro",
        "status": "active",
        "method_tier": "MICRO",
        "driver": "unit-test",
        "model": "fixture-model",
        "harness": "micro-fixture",
        "repetitions": 1,
        "arms": _arms(),
        "scenarios": [
            {
                "id": "SCN-001",
                "fixtures": {
                    "no-10x-control": "autoresearch/fixtures/offline/scn001-fail.json",
                    "current-10x": "autoresearch/fixtures/offline/scn001-pass.json",
                    "candidate-variant": "autoresearch/fixtures/offline/scn001-pass.json",
                },
            }
        ],
        "budget": {"estimated_wall_seconds_per_sample": 0},
    }


def _full_definition():
    return {
        "experiment_id": "EXP-20260623-702-run-once-full",
        "status": "active",
        "method_tier": "FULL",
        "driver": "unit-test",
        "model": "fixture-codex-model",
        "harness": "codex-cli",
        "repetitions": 1,
        "arms": _arms(),
        "scenarios": [
            {
                "id": "SCN-008",
                "fixtures": {
                    "no-10x-control": "autoresearch/fixtures/offline/scn008-pass.json",
                    "current-10x": "autoresearch/fixtures/offline/scn008-pass.json",
                    "candidate-variant": "autoresearch/fixtures/offline/scn008-pass.json",
                },
            }
        ],
        "budget": {"estimated_wall_seconds_per_run": 0},
    }


def _arms():
    return [
        {
            "id": "no-10x-control",
            "instruction_source": "minimal harness defaults",
            "instruction_digest": "sha256:no10x",
        },
        {
            "id": "current-10x",
            "instruction_source": "SKILL.md",
            "instruction_digest": "sha256:current",
        },
        {
            "id": "candidate-variant",
            "instruction_source": "candidate.md",
            "instruction_digest": "sha256:candidate",
        },
    ]


def _git(root: Path, *args: str) -> None:
    import subprocess

    subprocess.run(
        ["git", *args],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )


if __name__ == "__main__":
    unittest.main()
