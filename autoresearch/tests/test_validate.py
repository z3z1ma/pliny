import json
import shutil
import tempfile
import unittest
from pathlib import Path

from autoresearch import validate


REPO_ROOT = Path(__file__).resolve().parents[2]


class ValidateContractsTest(unittest.TestCase):
    def test_checked_in_contracts_validate(self):
        result = validate.validate_contracts(REPO_ROOT)

        self.assertEqual([], result.errors)

    def test_missing_score_id_fails_validation(self):
        with copied_contract_root() as root:
            scores_path = root / "autoresearch" / "catalogs" / "scores.json"
            data = json.loads(scores_path.read_text(encoding="utf-8"))
            data["scores"] = [
                score for score in data["scores"] if score["id"] != "S009"
            ]
            scores_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

            result = validate.validate_contracts(root)

        self.assertIn("scores.json: missing score IDs: S009", result.errors)

    def test_missing_scenario_id_fails_validation(self):
        with copied_contract_root() as root:
            scenarios_path = root / "autoresearch" / "catalogs" / "scenarios.json"
            data = json.loads(scenarios_path.read_text(encoding="utf-8"))
            data["scenarios"] = [
                scenario
                for scenario in data["scenarios"]
                if scenario["id"] != "SCN-015"
            ]
            scenarios_path.write_text(
                json.dumps(data, indent=2) + "\n", encoding="utf-8"
            )

            result = validate.validate_contracts(root)

        self.assertIn("scenarios.json: missing scenario IDs: SCN-015", result.errors)

    def test_unknown_split_scenario_fails_validation(self):
        with copied_contract_root() as root:
            split_path = root / "autoresearch" / "splits" / "skill-improvement-v1.json"
            data = json.loads(split_path.read_text(encoding="utf-8"))
            data["held_out_scenarios"].append("SCN-999")
            split_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

            result = validate.validate_contracts(root)

        self.assertIn(
            "splits/skill-improvement-v1.json: held_out_scenarios unknown scenario SCN-999",
            result.errors,
        )

    def test_live_seed_manifest_without_workspace_fails_validation(self):
        with copied_contract_root() as root:
            manifest_path = (
                root
                / "autoresearch"
                / "fixtures"
                / "live-seeds"
                / "explicit-policy-ratification"
                / "workspace"
                / "workspace-manifest.json"
            )
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            del data["workspace"]
            manifest_path.write_text(
                json.dumps(data, indent=2) + "\n", encoding="utf-8"
            )

            result = validate.validate_contracts(root)

        self.assertIn(
            "autoresearch/fixtures/live-seeds/explicit-policy-ratification/workspace/workspace-manifest.json: seed workspace manifest requires workspace",
            result.errors,
        )


class copied_contract_root:
    def __enter__(self):
        self._tmp = tempfile.TemporaryDirectory()
        root = Path(self._tmp.name)
        source = REPO_ROOT / "autoresearch"
        target = root / "autoresearch"
        target.mkdir()
        for child in ("catalogs", "schemas", "templates", "splits", "fixtures"):
            shutil.copytree(source / child, target / child)
        spec_target = root / ".10x" / "specs"
        spec_target.mkdir(parents=True)
        shutil.copy2(
            REPO_ROOT / ".10x" / "specs" / "10x-autoresearch-loop.md",
            spec_target / "10x-autoresearch-loop.md",
        )
        return root

    def __exit__(self, exc_type, exc, tb):
        self._tmp.cleanup()


if __name__ == "__main__":
    unittest.main()
