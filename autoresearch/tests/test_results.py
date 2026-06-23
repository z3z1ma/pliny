import tempfile
import unittest
from pathlib import Path

from autoresearch import results


class ResultsTest(unittest.TestCase):
    def test_init_and_append_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "results.tsv"
            results.init_ledger(path)
            results.append_row(
                path,
                timestamp="2026-06-23T00:00:00Z",
                experiment_id="EXP-20260623-001-test",
                tier="MICRO",
                candidate="candidate-a",
                score_vector="S001=90;S006=80",
                status="keep",
                description="baseline improvement",
            )

            lines = path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(
                "timestamp\texperiment_id\ttier\tcandidate\tscore_vector\tstatus\tdescription",
                lines[0],
            )
            self.assertIn("candidate-a", lines[1])

    def test_rejects_commas_and_invalid_status(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "results.tsv"
            results.init_ledger(path)
            with self.assertRaises(results.ResultsError):
                results.append_row(
                    path,
                    experiment_id="EXP-20260623-001-test",
                    tier="MICRO",
                    candidate="candidate-a",
                    score_vector="S001=90",
                    status="win",
                    description="bad status",
                )
            with self.assertRaises(results.ResultsError):
                results.append_row(
                    path,
                    experiment_id="EXP-20260623-001-test",
                    tier="MICRO",
                    candidate="candidate-a",
                    score_vector="S001=90",
                    status="keep",
                    description="contains, comma",
                )


if __name__ == "__main__":
    unittest.main()
