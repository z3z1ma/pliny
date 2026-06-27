import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from autoresearch import report


class ReportTest(unittest.TestCase):
    def test_report_includes_trial_artifacts_and_inspection_prompt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_dir = root / "raw"
            raw_dir.mkdir()
            (root / "summary.json").write_text(
                json.dumps(
                    {
                        "experiment_id": "EXP-20260627-001-reporting",
                        "mode": "live",
                        "samples_written": 2,
                        "raw_output_dir": str(raw_dir),
                        "workspace_dir": str(root / "workspaces"),
                        "codex_artifact_dir": str(root / "codex"),
                        "prompt_dir": str(root / "prompts"),
                        "live_codex_calls": 2,
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            (root / "canonical_guard.json").write_text(
                json.dumps({"unchanged_during_run": True}, indent=2) + "\n",
                encoding="utf-8",
            )
            _write_raw(raw_dir / "current.json", _artifact(variant_id="current-10x"))
            _write_raw(raw_dir / "candidate.json", _artifact(variant_id="candidate-variant"))

            markdown = report.build_report(root)

        self.assertIn("# 10x Autoresearch Trial Report", markdown)
        self.assertIn("## Summary", markdown)
        self.assertIn("EXP-20260627-001-reporting", markdown)
        self.assertIn("## Trial Artifacts", markdown)
        self.assertIn("## Scientific Contract", markdown)
        self.assertIn("Can the subject stay minimal?", markdown)
        self.assertIn("## Artifact Inspection Checklist", markdown)
        self.assertIn("canonical_guard.json", markdown)
        self.assertIn("2 found", markdown)
        self.assertIn("current-10x", markdown)
        self.assertIn("candidate-variant", markdown)
        self.assertIn("app.py", markdown)
        self.assertIn("workspaces/current", markdown)
        self.assertIn("in=100; out=50", markdown)
        self.assertIn("## Scientist Inspection", markdown)
        self.assertIn("does not grade, aggregate, or promote", markdown)
        self.assertNotIn("## Score Vectors", markdown)

    def test_missing_fields_render_unknown(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw_path = Path(tmp) / "partial.json"
            _write_raw(raw_path, {"scenario_id": "SCN-999", "variant_id": "partial-arm"})

            markdown = report.build_report(raw_path)

        self.assertIn("partial.json", markdown)
        self.assertIn("partial-arm", markdown)
        self.assertIn("unknown", markdown)

    def test_cli_writes_markdown_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_dir = root / "raw"
            raw_dir.mkdir()
            out_path = root / "report.md"
            _write_raw(raw_dir / "current.json", _artifact())
            stdout = io.StringIO()

            with contextlib.redirect_stdout(stdout):
                exit_code = report.main(["--artifacts", str(root), "--out", str(out_path)])

            self.assertEqual(0, exit_code)
            self.assertTrue(out_path.exists())
            self.assertIn("wrote", stdout.getvalue())
            self.assertIn("# 10x Autoresearch Trial Report", out_path.read_text(encoding="utf-8"))

    def test_campaign_metadata_renders_without_changing_trial_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            raw_dir = root / "raw"
            raw_dir.mkdir()
            campaign_path = root / "campaign.json"
            _write_raw(raw_dir / "candidate.json", _artifact())
            campaign_path.write_text(
                json.dumps(
                    {
                        "campaign_id": "EXP-20260627-002-campaign",
                        "candidate_id": "candidate-variant",
                        "baseline_id": "current-10x",
                        "verdict": "inconclusive",
                        "result_status": "confounded",
                        "statuses": ["confounded"],
                        "promotion_decision": "not-performed",
                        "manual_inspection": {
                            "status": "recorded-in-evidence",
                            "by": "parent-review",
                        },
                        "evidence_refs": [
                            ".10x/evidence/2026-06-27-trial-tooling-cleanup.md"
                        ],
                        "limits": ["campaign metadata is not runner output"],
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            markdown = report.build_report(root, campaign_path=campaign_path)

        self.assertIn("## Campaign Verdict", markdown)
        self.assertIn("EXP-20260627-002-campaign", markdown)
        self.assertIn("inconclusive", markdown)
        self.assertIn("confounded", markdown)
        self.assertIn("Campaign verdict metadata is manual/contextual", markdown)

    def test_report_without_campaign_metadata_has_no_campaign_section(self):
        with tempfile.TemporaryDirectory() as tmp:
            raw_dir = Path(tmp) / "raw"
            raw_dir.mkdir()
            _write_raw(raw_dir / "current.json", _artifact())

            markdown = report.build_report(raw_dir.parent)

        self.assertNotIn("## Campaign Verdict", markdown)


def _artifact(*, variant_id="current-10x"):
    return {
        "schema_version": 1,
        "experiment_id": "EXP-20260627-001-reporting",
        "scenario_id": "SCN-001",
        "variant_id": variant_id,
        "rep": 0,
        "model": "codex-test-model",
        "harness": "codex-cli",
        "instruction_digest": "sha256:test",
        "scientific_contract": _scientific_contract(),
        "transcript": [
            {"role": "user", "content": "Make it clearer."},
            {"role": "assistant", "content": "I inspected the app and changed one label."},
        ],
        "tool_invocations": [{"type": "item.completed", "item": {"type": "command_execution"}}],
        "file_outputs": [{"path": "app.py", "action": "write", "content": "print('hi')"}],
        "command_outputs": [{"command": "python3 -m unittest", "exit_code": 0, "output": "OK"}],
        "raw_artifact_refs": ["raw/current.json", "codex/current.command.json"],
        "wall_seconds": 1.5,
        "input_tokens": 100,
        "output_tokens": 50,
        "timed_out": False,
        "live_codex_calls": 1,
        "harness_metadata": {
            "kind": "codex-live-subject",
            "archived_workspace_dir": "workspaces/current",
            "workspace_manifest_path": "workspaces/current/workspace-manifest.json",
        },
    }


def _scientific_contract():
    return {
        "question": "Can the subject stay minimal?",
        "hypothesis": "The subject will avoid unnecessary work.",
        "expected_behavior": "Only the required small change is made.",
        "inspection_criteria": ["changed files match scope", "command exits are zero"],
        "quality_floor": "No unrelated files change.",
        "verdict_record_path": ".10x/evidence/unit-test-report.md",
    }


def _write_raw(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
