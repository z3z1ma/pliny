import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from autoresearch import report


class ReportTest(unittest.TestCase):
    def test_report_includes_vectors_floors_statuses_inspection_and_costs(self):
        with tempfile.TemporaryDirectory() as tmp:
            score_dir = Path(tmp)
            _write_score(
                score_dir / "current.score.json",
                _artifact(
                    variant_id="current-10x",
                    scores={
                        "S001": {
                            "value": 91,
                            "confidence": "medium",
                            "floor_triggered": False,
                            "rationale": "inspected before asking",
                            "evidence_refs": ["raw/current.json"],
                            "limits": ["fixture only"],
                        },
                        "S007": {
                            "value": 80,
                            "confidence": "low",
                            "floor_triggered": False,
                            "rationale": "focused question",
                            "evidence_refs": ["raw/current.json"],
                            "limits": ["manual review needed"],
                        },
                    },
                ),
            )
            _write_score(
                score_dir / "candidate.score.json",
                _artifact(
                    variant_id="candidate-variant",
                    verdict="backfired",
                    result_status="negative",
                    statuses=["null", "confounded"],
                    scores={
                        "S001": {
                            "value": 35,
                            "confidence": "low",
                            "floor_triggered": True,
                            "floor_triggers": [
                                {
                                    "score_id": "S001",
                                    "condition": "S001 below active floor 80",
                                    "effect": "non-promotable",
                                    "evidence_refs": ["raw/candidate.json"],
                                }
                            ],
                            "rationale": "premature implementation",
                            "evidence_refs": ["raw/candidate.json"],
                            "limits": ["fixture only"],
                        }
                    },
                    floor_triggers=[
                        {
                            "score_id": "S001",
                            "condition": "S001 below active floor 80",
                            "effect": "non-promotable",
                            "evidence_refs": ["raw/candidate.json"],
                        }
                    ],
                ),
            )

            markdown = report.build_report(score_dir)

        self.assertIn("## Score Vectors", markdown)
        self.assertIn("S001 Outer Loop Discipline=91 (medium, floor ok)", markdown)
        self.assertIn("S001 Outer Loop Discipline=35 (low, floor triggered)", markdown)
        self.assertIn("## Arm Score Comparison", markdown)
        self.assertIn("candidate-variant", markdown)
        self.assertIn("## Quality Floors And Failures", markdown)
        self.assertIn("S001 below active floor 80", markdown)
        self.assertIn("non-promotable", markdown)
        self.assertIn("## Result Statuses", markdown)
        self.assertIn("backfired", markdown)
        self.assertIn("negative", markdown)
        self.assertIn("null", markdown)
        self.assertIn("confounded", markdown)
        self.assertIn("required-not-done", markdown)
        self.assertIn("Trust Level 1", markdown)
        self.assertIn("## Costs", markdown)
        self.assertIn("0.12", markdown)

    def test_missing_fields_render_unknown(self):
        with tempfile.TemporaryDirectory() as tmp:
            score_dir = Path(tmp)
            _write_score(
                score_dir / "partial.score.json",
                {
                    "scenario_id": "SCN-999",
                    "variant_id": "partial-arm",
                    "scores": {"S009": {"value": None}},
                },
            )

            markdown = report.build_report(score_dir)

        self.assertIn("partial.score.json", markdown)
        self.assertIn("S009 Cost Efficiency Index=unknown", markdown)
        self.assertIn("partial-arm", markdown)
        self.assertIn("unknown", markdown)

    def test_cli_writes_markdown_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            score_dir = root / "scores"
            score_dir.mkdir()
            out_path = root / "report.md"
            _write_score(score_dir / "current.score.json", _artifact())
            stdout = io.StringIO()

            with contextlib.redirect_stdout(stdout):
                exit_code = report.main(["--scores", str(score_dir), "--out", str(out_path)])

            self.assertEqual(0, exit_code)
            self.assertTrue(out_path.exists())
            self.assertIn("wrote", stdout.getvalue())
            self.assertIn("# 10x Autoresearch Score Report", out_path.read_text(encoding="utf-8"))

    def test_campaign_metadata_renders_without_changing_score_statuses(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            score_dir = root / "scores"
            score_dir.mkdir()
            campaign_path = root / "campaign.json"
            _write_score(score_dir / "candidate.score.json", _artifact())
            campaign_path.write_text(
                json.dumps(
                    {
                        "campaign_id": "EXP-20260623-301-first-calibration-campaign",
                        "candidate_id": "candidate-variant",
                        "baseline_id": "current-10x",
                        "verdict": "null",
                        "result_status": "confounded",
                        "statuses": ["null", "confounded"],
                        "promotion_decision": "not-performed",
                        "manual_inspection": {
                            "status": "recorded-in-evidence",
                            "by": "parent-review",
                        },
                        "evidence_refs": [
                            ".10x/evidence/2026-06-23-first-autoresearch-calibration-campaign.md"
                        ],
                        "limits": ["campaign metadata is not scorer output"],
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            markdown = report.build_report(score_dir, campaign_path=campaign_path)

        self.assertIn("## Campaign Verdict", markdown)
        self.assertIn("EXP-20260623-301-first-calibration-campaign", markdown)
        self.assertIn("null", markdown)
        self.assertIn("confounded", markdown)
        self.assertIn("Campaign verdict metadata is manual/contextual", markdown)
        self.assertIn("No artifact-embedded result statuses were present", markdown)
        self.assertIn("required-not-done", markdown)

    def test_report_without_campaign_metadata_has_no_campaign_section(self):
        with tempfile.TemporaryDirectory() as tmp:
            score_dir = Path(tmp)
            _write_score(score_dir / "current.score.json", _artifact())

            markdown = report.build_report(score_dir)

        self.assertNotIn("## Campaign Verdict", markdown)


def _artifact(
    *,
    variant_id="current-10x",
    scores=None,
    verdict=None,
    result_status=None,
    statuses=None,
    floor_triggers=None,
):
    artifact = {
        "experiment_id": "EXP-20260623-101-reporting",
        "scenario_id": "SCN-001",
        "variant_id": variant_id,
        "rep": 0,
        "model": "fixture-model",
        "harness": "unit-test",
        "instruction_digest": "sha256:test",
        "fixture_digest": "sha256:fixture",
        "scores": scores
        or {
            "S001": {
                "value": 90,
                "confidence": "medium",
                "floor_triggered": False,
                "rationale": "inspected before asking",
                "evidence_refs": ["raw/current.json"],
                "limits": ["fixture only"],
            }
        },
        "cost": {
            "wall_seconds": 1.5,
            "input_tokens": 100,
            "output_tokens": 50,
            "tool_calls": 2,
            "estimated_usd": 0.12,
            "human_inspection_seconds": None,
        },
        "limits": ["unit test artifact"],
        "scorer": {
            "id": "unit-test-scorer",
            "trust_level": 1,
            "confidence": "low",
            "manual_inspection_required": True,
            "limits": ["test scorer only"],
        },
        "manual_inspection": {
            "status": "required-not-done",
            "limits": ["not manually inspected"],
        },
    }
    if verdict is not None:
        artifact["verdict"] = verdict
    if result_status is not None:
        artifact["result_status"] = result_status
    if statuses is not None:
        artifact["statuses"] = statuses
    if floor_triggers is not None:
        artifact["floor_triggers"] = floor_triggers
    return artifact


def _write_score(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
