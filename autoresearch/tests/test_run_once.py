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
    def test_live_subject_micro_run_uses_candidate_executing_runner(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch("autoresearch.run_once.run_codex_subject.run_live") as run_live:
                run_live.return_value = {
                    "experiment_id": "EXP-20260623-703-run-once-live",
                    "mode": "live",
                    "samples_written": 3,
                    "plan_path": str(Path(tmp) / "plan.json"),
                    "raw_output_dir": str(Path(tmp) / "raw"),
                    "score_artifact_dir": str(Path(tmp) / "scores"),
                    "live_codex_calls": 3,
                }
                with mock.patch("autoresearch.run_once.report.write_report"):
                    result = run_once.run_once(
                        _live_subject_definition(),
                        tmp,
                        repo_root=REPO_ROOT,
                    )

            self.assertEqual("MICRO", result["method_tier"])
            self.assertEqual("autoresearch/run_codex_subject.py", result["runner"])
            self.assertEqual(3, result["samples_written"])
            self.assertTrue(any("Live subject outputs" in item for item in result["limits"]))
            self.assertFalse(any("Fixture-backed" in item for item in result["limits"]))

    def test_live_subject_full_run_uses_candidate_executing_runner(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch("autoresearch.run_once.run_codex_subject.run_live") as run_live:
                run_live.return_value = {
                    "experiment_id": "EXP-20260623-704-run-once-live-full",
                    "mode": "live",
                    "samples_written": 3,
                    "plan_path": str(Path(tmp) / "plan.json"),
                    "raw_output_dir": str(Path(tmp) / "raw"),
                    "score_artifact_dir": str(Path(tmp) / "scores"),
                    "live_codex_calls": 3,
                }
                with mock.patch("autoresearch.run_once.report.write_report"):
                    result = run_once.run_once(
                        _live_subject_definition(method_tier="FULL"),
                        tmp,
                        repo_root=REPO_ROOT,
                    )

            self.assertEqual("FULL", result["method_tier"])
            self.assertEqual("autoresearch/run_codex_subject.py", result["runner"])
            self.assertEqual(3, result["samples_written"])

    def test_unsupported_tier_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(run_once.RunOnceError):
                run_once.run_once(_unsupported_definition(), tmp, repo_root=REPO_ROOT)

    def test_cli_writes_json_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            experiment = root / "experiment.json"
            out_dir = root / "out"
            experiment.write_text(json.dumps(_live_subject_definition()), encoding="utf-8")
            stdout = io.StringIO()

            with mock.patch("autoresearch.run_once.run_codex_subject.run_live") as run_live:
                run_live.return_value = {
                    "experiment_id": "EXP-20260623-703-run-once-live",
                    "mode": "live",
                    "samples_written": 3,
                    "plan_path": str(out_dir / "plan.json"),
                    "raw_output_dir": str(out_dir / "raw"),
                    "score_artifact_dir": str(out_dir / "scores"),
                    "live_codex_calls": 3,
                }
                with mock.patch("autoresearch.run_once.report.write_report"):
                    with contextlib.redirect_stdout(stdout):
                        exit_code = run_once.main(
                            ["--experiment", str(experiment), "--out", str(out_dir)]
                        )

            self.assertEqual(0, exit_code)
            result = json.loads(stdout.getvalue())
            self.assertEqual("MICRO", result["method_tier"])

    def test_load_definition_accepts_live_subject_markdown_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "experiment.md"
            path.write_text(
                "<!-- codex-subject-runner-definition:start -->\n"
                "```json\n"
                + json.dumps(_live_subject_definition())
                + "\n```\n"
                "<!-- codex-subject-runner-definition:end -->\n",
                encoding="utf-8",
            )

            definition = run_once.load_definition(path)

        self.assertEqual("codex-cli", definition["harness"])

    def test_cli_rejects_campaign_without_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            experiment = root / "experiment.json"
            campaign = root / "campaign.json"
            experiment.write_text(json.dumps(_live_subject_definition()), encoding="utf-8")
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
                    "experiment_id": "EXP-20260623-703-run-once-live",
                    "mode": "live",
                    "samples_written": 0,
                    "plan_path": str(Path(out_dir) / "plan.json"),
                    "raw_output_dir": str(Path(out_dir) / "raw"),
                    "score_artifact_dir": str(Path(out_dir) / "scores"),
                }

            with mock.patch("autoresearch.run_once.run_codex_subject.run_live", side_effect=mutate):
                with mock.patch("autoresearch.run_once.report.write_report"):
                    with self.assertRaises(run_once.RunOnceError):
                        run_once.run_once(
                            _live_subject_definition(),
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

            with mock.patch("autoresearch.run_once.run_codex_subject.run_live"):
                with self.assertRaises(run_once.canonical_guard.CanonicalGuardError):
                    run_once.run_once(
                        _live_subject_definition(),
                        root / "out",
                        repo_root=root,
                        require_clean_canonical=True,
                    )


def _live_subject_definition(*, method_tier="MICRO"):
    definition = {
        "experiment_id": "EXP-20260623-703-run-once-live",
        "status": "active",
        "method_tier": method_tier,
        "driver": "unit-test",
        "model": "codex-cli-default",
        "harness": "codex-cli",
        "repetitions": 1,
        "arms": _arms(),
        "scenarios": [{"id": "SCN-010", "prompt": "Add a framework."}],
        "budget": {"estimated_wall_seconds_per_run": 0},
    }
    definition["experiment_id"] = "EXP-20260623-703-run-once-live"
    return definition


def _unsupported_definition():
    definition = _live_subject_definition()
    definition["method_tier"] = "LONG"
    definition["harness"] = "unsupported-harness"
    return definition


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
