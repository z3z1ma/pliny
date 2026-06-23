import json
import tempfile
import unittest
from pathlib import Path

from autoresearch import calibrate_scorer


REPO_ROOT = Path(__file__).resolve().parents[2]


class CalibrateScorerTest(unittest.TestCase):
    def test_default_labels_produce_metrics_without_trust_upgrade(self):
        result = calibrate_scorer.calibrate(
            REPO_ROOT / "autoresearch" / "calibration" / "offline-trust-labels.json",
            repo_root=REPO_ROOT,
        )

        self.assertEqual("offline-coverage-v1", result["scorer_id"])
        self.assertEqual(1, result["current_trust_level"])
        self.assertEqual(1, result["recommended_trust_level"])
        self.assertIn("S001", result["metrics"])
        self.assertIn("S004", result["metrics"])
        self.assertIn("S007", result["metrics"])
        self.assertEqual(3, result["metrics"]["S001"]["samples"])
        self.assertEqual(0, result["metrics"]["S001"]["fp"])
        self.assertEqual(0, result["metrics"]["S001"]["fn"])
        self.assertIn("too small", result["recommendation"])

    def test_write_outputs_creates_json_and_markdown(self):
        result = calibrate_scorer.calibrate(
            REPO_ROOT / "autoresearch" / "calibration" / "offline-trust-labels.json",
            repo_root=REPO_ROOT,
        )

        with tempfile.TemporaryDirectory() as tmp:
            paths = calibrate_scorer.write_outputs(result, tmp)
            json_path = Path(paths["json"])
            markdown_path = Path(paths["markdown"])

            self.assertTrue(json_path.exists())
            self.assertTrue(markdown_path.exists())
            self.assertEqual("offline-coverage-v1", json.loads(json_path.read_text())["scorer_id"])
            self.assertIn("# Offline Scorer Calibration", markdown_path.read_text())

    def test_missing_threshold_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            labels = {
                "schema_version": 1,
                "label_set_id": "bad",
                "thresholds": {},
                "labels": [
                    {
                        "fixture": "autoresearch/fixtures/offline/scn001-pass.json",
                        "score_id": "S001",
                        "expected_pass": True,
                    }
                ],
            }
            path = Path(tmp) / "labels.json"
            path.write_text(json.dumps(labels), encoding="utf-8")

            with self.assertRaises(calibrate_scorer.CalibrationError):
                calibrate_scorer.calibrate(path, repo_root=REPO_ROOT)


if __name__ == "__main__":
    unittest.main()
