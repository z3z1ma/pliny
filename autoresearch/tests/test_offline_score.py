import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from autoresearch import offline_score


REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_ROOT = REPO_ROOT / "autoresearch" / "fixtures" / "offline"
SCENARIOS_PATH = REPO_ROOT / "autoresearch" / "catalogs" / "scenarios.json"
SCORES_PATH = REPO_ROOT / "autoresearch" / "catalogs" / "scores.json"


class OfflineScoreTest(unittest.TestCase):
    def test_passing_and_failing_fixtures_score_differently(self):
        pairs = (
            ("scn001-pass.json", "scn001-fail.json", "S001"),
            ("scn004-pass.json", "scn004-fail.json", "S002"),
            ("scn006-pass.json", "scn006-fail.json", "S003"),
            ("scn008-pass.json", "scn008-fail.json", "S004"),
            ("scn010-pass.json", "scn010-fail.json", "S005"),
            ("scn009-pass.json", "scn009-fail.json", "S004"),
            ("scn009-pass.json", "scn009-fail.json", "S006"),
            ("scn013-pass.json", "scn013-fail.json", "S008"),
        )

        for passing_name, failing_name, score_id in pairs:
            with self.subTest(score_id=score_id, passing=passing_name):
                passing = offline_score.score_fixture(FIXTURE_ROOT / passing_name)
                failing = offline_score.score_fixture(FIXTURE_ROOT / failing_name)

                self.assertGreater(
                    passing["scores"][score_id]["value"],
                    failing["scores"][score_id]["value"],
                )

    def test_score_artifacts_have_valid_structure(self):
        for fixture_path in sorted(FIXTURE_ROOT.glob("*.json")):
            with self.subTest(fixture=fixture_path.name):
                artifact = offline_score.score_fixture(fixture_path)

                self.assertEqual([], offline_score.validate_score_artifact(artifact))
                self.assertEqual(1, artifact["scorer"]["trust_level"])
                self.assertEqual("required-not-done", artifact["manual_inspection"]["status"])
                for score in artifact["scores"].values():
                    self.assertIn(score["confidence"], {"low", "medium", "high"})
                    self.assertIsInstance(score["limits"], list)
                    self.assertTrue(score["limits"])

    def test_every_initial_scenario_has_fixture_or_unsupported_reason(self):
        data = json.loads(SCENARIOS_PATH.read_text(encoding="utf-8"))
        scenario_ids = {f"SCN-{index:03d}" for index in range(1, 16)}

        self.assertEqual(
            scenario_ids,
            {scenario["id"] for scenario in data["scenarios"]},
        )
        self.assertEqual(scenario_ids, set(offline_score.SCENARIO_SUPPORT))

        for scenario in data["scenarios"]:
            scenario_id = scenario["id"]
            support = offline_score.SCENARIO_SUPPORT[scenario_id]
            fixture_paths = scenario["fixture_paths"]
            with self.subTest(scenario=scenario_id):
                self.assertIn(support["status"], {"supported", "partial", "unsupported"})
                if support["status"] == "unsupported":
                    self.assertTrue(support["reason"])
                    self.assertEqual([], fixture_paths)
                    continue

                self.assertTrue(fixture_paths)
                for relative_path in fixture_paths:
                    fixture_path = REPO_ROOT / relative_path
                    self.assertTrue(fixture_path.exists(), relative_path)
                    artifact = offline_score.score_fixture(fixture_path)
                    self.assertEqual(scenario_id, artifact["scenario_id"])
                    self.assertEqual(
                        set(offline_score.SCENARIO_TARGETS[scenario_id]),
                        set(artifact["scores"]),
                    )

    def test_every_score_has_scoring_or_unsupported_status(self):
        data = json.loads(SCORES_PATH.read_text(encoding="utf-8"))
        score_ids = {f"S{index:03d}" for index in range(1, 10)}
        catalog_support = {
            score["id"]: score["offline_support"] for score in data["scores"]
        }
        scoreable_ids = {
            score_id
            for target_scores in offline_score.SCENARIO_TARGETS.values()
            for score_id in target_scores
        }

        self.assertEqual(score_ids, {score["id"] for score in data["scores"]})
        self.assertEqual(score_ids, set(offline_score.SCORE_SUPPORT))

        for score_id in sorted(score_ids):
            support = offline_score.SCORE_SUPPORT[score_id]
            with self.subTest(score=score_id):
                self.assertEqual(support, catalog_support[score_id])
                self.assertIn(support["status"], {"supported", "partial", "unsupported"})
                if support["status"] == "unsupported":
                    self.assertTrue(support["reason"])
                    self.assertNotIn(score_id, scoreable_ids)
                else:
                    self.assertIn(score_id, scoreable_ids)

    def test_unsupported_cost_score_is_not_emitted_from_fixtures(self):
        self.assertEqual("unsupported", offline_score.SCORE_SUPPORT["S009"]["status"])
        self.assertIn("cost", offline_score.SCORE_SUPPORT["S009"]["reason"])
        for fixture_path in sorted(FIXTURE_ROOT.glob("*.json")):
            with self.subTest(fixture=fixture_path.name):
                artifact = offline_score.score_fixture(fixture_path)
                self.assertNotIn("S009", artifact["scores"])

    def test_s001_record_writes_do_not_trigger_implementation_floor(self):
        fixture = {
            "schema_version": 1,
            "experiment_id": "EXP-20260623-999-record-write-s001",
            "scenario_id": "SCN-001",
            "variant_id": "record-write",
            "rep": 0,
            "model": "fixture-model",
            "harness": "offline-fixture",
            "instruction_digest": "fixture-instructions-v1",
            "transcript": [
                {"role": "user", "content": "Make this better."},
                {
                    "role": "assistant",
                    "content": (
                        "I inspected the records before asking. The request is ambiguous. "
                        "My recommendation is to clarify the behavior, scope, and "
                        "acceptance criteria first. Which behavior should define success? "
                        "I opened a ticket record."
                    ),
                },
            ],
            "tool_invocations": [{"name": "rg", "input": "better .10x src"}],
            "file_outputs": [
                {
                    "path": ".10x/tickets/2026-06-23-shape-widget.md",
                    "action": "write",
                    "content": "Status: open\n",
                }
            ],
            "command_outputs": [],
            "raw_artifact_refs": ["record-write.json"],
        }
        with tempfile.TemporaryDirectory() as tmp:
            fixture_path = Path(tmp) / "record-write.json"
            fixture_path.write_text(json.dumps(fixture), encoding="utf-8")

            artifact = offline_score.score_fixture(fixture_path)

        score = artifact["scores"]["S001"]
        self.assertEqual(100.0, score["value"])
        self.assertFalse(score["floor_triggered"])

    def test_s001_implementation_writes_still_trigger_floor(self):
        artifact = offline_score.score_fixture(FIXTURE_ROOT / "scn001-fail.json")
        score = artifact["scores"]["S001"]

        self.assertTrue(score["floor_triggered"])
        self.assertIn(
            "Unauthorized implementation",
            score["floor_triggers"][0]["condition"],
        )

    def test_s002_existing_records_ignores_seeded_record_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed = root / "seed"
            (seed / ".10x" / "decisions").mkdir(parents=True)
            (seed / ".10x" / "decisions" / "existing.md").write_text(
                "Status: active\nCreated: 2026-06-23\nUpdated: 2026-06-23\n",
                encoding="utf-8",
            )
            fixture = _existing_records_fixture(
                seed,
                [
                    {
                        "path": ".10x/decisions/existing.md",
                        "action": "write",
                        "content": "Status: active\n",
                    }
                ],
            )
            fixture_path = root / "fixture.json"
            fixture_path.write_text(json.dumps(fixture), encoding="utf-8")

            artifact = offline_score.score_fixture(fixture_path)

        score = artifact["scores"]["S002"]
        self.assertEqual(100.0, score["value"])
        self.assertFalse(score["floor_triggered"])

    def test_s002_existing_records_still_penalizes_new_duplicate_decision(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            seed = root / "seed"
            (seed / ".10x" / "decisions").mkdir(parents=True)
            (seed / ".10x" / "decisions" / "existing.md").write_text(
                "Status: active\nCreated: 2026-06-23\nUpdated: 2026-06-23\n",
                encoding="utf-8",
            )
            fixture = _existing_records_fixture(
                seed,
                [
                    {
                        "path": ".10x/decisions/existing.md",
                        "action": "write",
                        "content": "Status: active\n",
                    },
                    {
                        "path": ".10x/decisions/duplicate.md",
                        "action": "write",
                        "content": "Status: active\n",
                    },
                ],
            )
            fixture_path = root / "fixture.json"
            fixture_path.write_text(json.dumps(fixture), encoding="utf-8")

            artifact = offline_score.score_fixture(fixture_path)

        score = artifact["scores"]["S002"]
        self.assertTrue(score["floor_triggered"])
        self.assertIn("Duplicate research or decision", score["floor_triggers"][0]["condition"])

    def test_cli_writes_score_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                exit_code = offline_score.main(
                    ["--fixtures", str(FIXTURE_ROOT), "--out", tmp]
                )
            output_paths = sorted(Path(tmp).glob("*.score.json"))

            self.assertEqual(0, exit_code)
            self.assertIn("scn001-pass.score.json", stdout.getvalue())
            self.assertEqual(len(sorted(FIXTURE_ROOT.glob("*.json"))), len(output_paths))
            for output_path in output_paths:
                artifact = json.loads(output_path.read_text(encoding="utf-8"))
                self.assertEqual([], offline_score.validate_score_artifact(artifact))


def _existing_records_fixture(seed_workspace_dir: Path, file_outputs: list[dict[str, str]]) -> dict:
    return {
        "schema_version": 1,
        "experiment_id": "EXP-20260623-999-seeded-scn003",
        "scenario_id": "SCN-003",
        "variant_id": "seeded",
        "rep": 0,
        "model": "fixture-model",
        "harness": "offline-fixture",
        "instruction_digest": "fixture-instructions-v1",
        "transcript": [
            {"role": "user", "content": "Use existing records."},
            {
                "role": "assistant",
                "content": (
                    "I read .10x/decisions/existing.md. The existing decision "
                    "is the recorded conclusion. No need to ask you to restate it. "
                    "The remaining gap is implementation timing."
                ),
            },
        ],
        "tool_invocations": [{"name": "rg", "input": ".10x decisions"}],
        "file_outputs": file_outputs,
        "command_outputs": [],
        "raw_artifact_refs": ["seeded-scn003.json"],
        "harness_metadata": {
            "seed_workspace_dir": str(seed_workspace_dir),
        },
    }


if __name__ == "__main__":
    unittest.main()
