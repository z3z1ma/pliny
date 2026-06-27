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

    def test_retired_top_line_score_policy_fails_validation(self):
        with copied_contract_root() as root:
            scores_path = root / "autoresearch" / "catalogs" / "scores.json"
            data = json.loads(scores_path.read_text(encoding="utf-8"))
            data["shared_rules"]["top_line_rule"] = "retired aggregate"
            scores_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

            result = validate.validate_contracts(root)

        self.assertIn("scores.json:shared_rules: top_line_rule is retired", result.errors)

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
                / "trial-seeds"
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
            "autoresearch/trial-seeds/explicit-policy-ratification/workspace/workspace-manifest.json: seed workspace manifest requires workspace",
            result.errors,
        )

    def test_live_seed_workspace_dot_is_manifest_relative(self):
        with copied_contract_root() as root:
            manifest_path = (
                root
                / "autoresearch"
                / "trial-seeds"
                / "explicit-policy-ratification"
                / "workspace"
                / "workspace-manifest.json"
            )
            manifest_path.write_text(
                json.dumps({"workspace": "."}, indent=2) + "\n",
                encoding="utf-8",
            )

            result = validate.validate_contracts(root)

        self.assertEqual([], result.errors)

    def test_live_seed_workspace_must_contain_manifest(self):
        with copied_contract_root() as root:
            manifest_path = (
                root
                / "autoresearch"
                / "trial-seeds"
                / "explicit-policy-ratification"
                / "workspace"
                / "workspace-manifest.json"
            )
            manifest_path.write_text(
                json.dumps({"workspace": str(root)}, indent=2) + "\n",
                encoding="utf-8",
            )

            result = validate.validate_contracts(root)

        self.assertIn(
            "autoresearch/trial-seeds/explicit-policy-ratification/workspace/workspace-manifest.json: resolved workspace must contain its workspace manifest",
            result.errors,
        )

    def test_trial_seed_index_must_cover_existing_seed(self):
        with copied_contract_root() as root:
            index_path = root / "autoresearch" / "trial-seeds" / "index.json"
            data = json.loads(index_path.read_text(encoding="utf-8"))
            data["seeds"] = []
            index_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

            result = validate.validate_contracts(root)

        self.assertIn("trial-seeds/index.json: seeds must be a non-empty list", result.errors)

    def test_skill_size_budget_excludes_frontmatter(self):
        with copied_contract_root() as root:
            (root / "SKILL.md").write_text(
                "---\n"
                "name: huge-frontmatter\n"
                "description: test\n"
                + ("x" * 50000)
                + "\n---\n"
                + ("y" * validate.SKILL_BODY_CHAR_BUDGET),
                encoding="utf-8",
            )

            result = validate.validate_contracts(root)

        self.assertEqual([], result.errors)

    def test_skill_size_budget_rejects_large_body(self):
        with copied_contract_root() as root:
            (root / "SKILL.md").write_text(
                "---\nname: test\n---\n" + ("x" * (validate.SKILL_BODY_CHAR_BUDGET + 1)),
                encoding="utf-8",
            )

            result = validate.validate_contracts(root)

        self.assertIn(
            "SKILL.md: body character count 40001 exceeds budget 40000",
            result.errors,
        )


class copied_contract_root:
    def __enter__(self):
        self._tmp = tempfile.TemporaryDirectory()
        root = Path(self._tmp.name)
        source = REPO_ROOT / "autoresearch"
        target = root / "autoresearch"
        target.mkdir()
        for child in ("catalogs", "templates", "splits"):
            shutil.copytree(source / child, target / child)
        seed_source = (
            source
            / "trial-seeds"
            / "explicit-policy-ratification"
        )
        seed_target = (
            target
            / "trial-seeds"
            / "explicit-policy-ratification"
        )
        shutil.copytree(seed_source, seed_target)
        shutil.copy2(source / "trial-seeds" / "index.json", target / "trial-seeds" / "index.json")
        self._keep_only_explicit_policy_seed(target / "trial-seeds" / "index.json")
        spec_target = root / ".10x" / "specs"
        spec_target.mkdir(parents=True)
        shutil.copy2(
            REPO_ROOT / ".10x" / "specs" / "10x-autoresearch-loop.md",
            spec_target / "10x-autoresearch-loop.md",
        )
        shutil.copy2(REPO_ROOT / "SKILL.md", root / "SKILL.md")
        return root

    def __exit__(self, exc_type, exc, tb):
        self._tmp.cleanup()

    @staticmethod
    def _keep_only_explicit_policy_seed(index_path: Path) -> None:
        data = json.loads(index_path.read_text(encoding="utf-8"))
        data["seeds"] = [
            seed for seed in data["seeds"] if seed["id"] == "explicit-policy-ratification"
        ]
        for scenario in data.get("scenario_selection_guide", []):
            scenario["seed_count"] = (
                1 if scenario["scenario_id"] == "SCN-006" else 0
            )
        index_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
