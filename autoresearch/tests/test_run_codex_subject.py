import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from autoresearch import run_codex_subject


REPO_ROOT = Path(__file__).resolve().parents[2]


class CodexSubjectRunnerTest(unittest.TestCase):
    def test_plan_records_live_subject_samples_without_score_artifacts(self):
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
            self.assertNotIn("planned_score_artifact_path", sample)
            self.assertIn("--disable", sample["planned_codex_argv"])
            self.assertIn("--ignore-user-config", sample["planned_codex_argv"])
            self.assertIn("scenario_prompt", sample)
            self.assertTrue(sample["prompt_path"].endswith(".prompt.txt"))

    def test_plan_adds_definition_writable_add_dirs_to_codex_argv(self):
        definition = _definition()
        definition["writable_add_dirs"] = [".agents/skills"]

        with tempfile.TemporaryDirectory() as tmp:
            plan = run_codex_subject.build_plan(
                definition,
                repo_root=REPO_ROOT,
                out_dir=Path(tmp),
            )

        for sample in plan["samples"]:
            argv = sample["planned_codex_argv"]
            add_dir_index = argv.index("--add-dir")
            self.assertEqual([".agents/skills"], sample["writable_add_dirs"])
            self.assertLess(add_dir_index, len(argv) - 1)
            self.assertEqual(
                str(Path(sample["planned_workspace_dir"]) / ".agents/skills"),
                argv[add_dir_index + 1],
            )

    def test_rejects_unsafe_writable_add_dirs(self):
        unsafe_values = [
            "not-a-list",
            [""],
            ["."],
            ["../outside"],
            ["/tmp/outside"],
        ]

        for value in unsafe_values:
            with self.subTest(value=value):
                definition = _definition()
                definition["writable_add_dirs"] = value

                with self.assertRaises(run_codex_subject.ExperimentError):
                    run_codex_subject.build_plan(definition, repo_root=REPO_ROOT)

    def test_live_run_writes_trial_outputs_without_instruction_contamination(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch("subprocess.run", side_effect=_fake_run):
                summary = run_codex_subject.run_live(
                    _definition(),
                    Path(tmp),
                    repo_root=REPO_ROOT,
                )

            output_root = Path(tmp)
            raw_paths = sorted((output_root / "raw").glob("*.json"))
            command_paths = sorted((output_root / "codex").glob("*.command.json"))
            manifests = sorted((output_root / "workspaces").glob("*/workspace-manifest.json"))

            self.assertEqual(3, summary["samples_written"])
            self.assertEqual(3, summary["live_codex_calls"])
            self.assertNotIn("score_artifact_dir", summary)
            self.assertEqual(3, len(raw_paths))
            self.assertFalse((output_root / "scores").exists())
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
                self.assertEqual(1, len(raw["tool_invocations"]))
                self.assertEqual(
                    "command_execution",
                    raw["tool_invocations"][0]["item"]["type"],
                )
                self.assertNotIn("scores", raw)
                self.assertIn(str(raw_path), raw["raw_artifact_refs"])
                self.assertIn(
                    "not promotion authority",
                    raw["harness_metadata"]["promotion_limit"],
                )

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

    def test_live_run_applies_writable_add_dirs_to_actual_codex_argv(self):
        observed_add_dirs = []

        def fake_run(argv, stdout, stderr, text, timeout=None):
            workspace = Path(argv[argv.index("--cd") + 1])
            add_dir_index = argv.index("--add-dir")
            observed_add_dirs.append(Path(argv[add_dir_index + 1]))
            last_message = Path(argv[argv.index("--output-last-message") + 1])
            last_message.parent.mkdir(parents=True, exist_ok=True)
            last_message.write_text("Done.", encoding="utf-8")
            self.assertEqual(workspace / ".agents/skills", observed_add_dirs[-1])
            return mock.Mock(
                returncode=0,
                stdout='{"type":"turn.completed","usage":{"input_tokens":1,"output_tokens":1}}\n',
                stderr="",
            )

        definition = _definition()
        definition["writable_add_dirs"] = [".agents/skills"]
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch("subprocess.run", side_effect=fake_run):
                run_codex_subject.run_live(
                    definition,
                    Path(tmp),
                    repo_root=REPO_ROOT,
                )

            command_paths = sorted((Path(tmp) / "codex").glob("*.command.json"))
            manifests = sorted((Path(tmp) / "workspaces").glob("*/workspace-manifest.json"))
            command_argvs = [
                json.loads(command_path.read_text(encoding="utf-8"))["argv"]
                for command_path in command_paths
            ]
            manifest_add_dirs = [
                json.loads(manifest_path.read_text(encoding="utf-8"))["writable_add_dirs"]
                for manifest_path in manifests
            ]

        self.assertEqual(3, len(observed_add_dirs))
        self.assertEqual(3, len(command_paths))
        self.assertEqual(3, len(manifests))
        for argv in command_argvs:
            self.assertIn("--add-dir", argv)
        self.assertEqual([[".agents/skills"], [".agents/skills"], [".agents/skills"]], manifest_add_dirs)

    def test_live_run_hides_sibling_arm_workspaces_during_execution(self):
        visible_sibling_markers = []

        def fake_run(argv, stdout, stderr, text, timeout=None):
            workspace = Path(argv[argv.index("--cd") + 1])
            visible_sibling_markers.append(
                [
                    str(path)
                    for path in workspace.parent.rglob("arm-marker.txt")
                    if workspace not in path.parents
                ]
            )
            (workspace / "arm-marker.txt").write_text("marker", encoding="utf-8")
            last_message = Path(argv[argv.index("--output-last-message") + 1])
            last_message.parent.mkdir(parents=True, exist_ok=True)
            last_message.write_text("Done.", encoding="utf-8")
            return mock.Mock(
                returncode=0,
                stdout='{"type":"turn.completed","usage":{"input_tokens":1,"output_tokens":1}}\n',
                stderr="",
            )

        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch("subprocess.run", side_effect=fake_run):
                run_codex_subject.run_live(
                    _definition(),
                    Path(tmp),
                    repo_root=REPO_ROOT,
                )

            manifests = sorted((Path(tmp) / "workspaces").glob("*/workspace-manifest.json"))
            self.assertEqual(3, len(manifests))
            for manifest_path in manifests:
                workspace = Path(json.loads(manifest_path.read_text(encoding="utf-8"))["workspace"])
                self.assertEqual(Path(tmp) / "workspaces", workspace.parent)
                self.assertTrue((workspace / "arm-marker.txt").exists())

        self.assertEqual([[], [], []], visible_sibling_markers)

    def test_runner_uses_exactly_the_listed_arms(self):
        definition = _definition()
        definition["arms"] = definition["arms"][:2]

        plan = run_codex_subject.build_plan(definition, repo_root=REPO_ROOT)

        self.assertEqual(2, plan["live_codex_calls"])
        self.assertEqual(
            ["no-10x-control", "current-10x"],
            [arm["id"] for arm in plan["arms"]],
        )
        self.assertEqual(
            ["no-10x-control", "current-10x"],
            [sample["variant_id"] for sample in plan["samples"]],
        )

    def test_single_current_arm_smoke_run_needs_no_special_mode(self):
        definition = _definition()
        definition["arms"] = [
            {
                "id": "current-10x",
                "instruction_source": "test current",
                "instruction_text": "Current-only salience check.",
            }
        ]
        definition["budget"]["max_harness_runs"] = 1

        with tempfile.TemporaryDirectory() as tmp:
            plan = run_codex_subject.build_plan(
                definition,
                repo_root=REPO_ROOT,
                out_dir=Path(tmp),
            )

        self.assertEqual(1, plan["live_codex_calls"])
        self.assertEqual(["current-10x"], [arm["id"] for arm in plan["arms"]])
        self.assertEqual(["current-10x"], [sample["variant_id"] for sample in plan["samples"]])

    def test_evaluation_only_field_is_rejected(self):
        definition = _definition()
        definition["evaluation_only"] = True

        with self.assertRaisesRegex(run_codex_subject.ExperimentError, "evaluation_only is retired"):
            run_codex_subject.build_plan(definition, repo_root=REPO_ROOT)

    def test_scientific_contract_is_required(self):
        definition = _definition()
        del definition["scientific_contract"]

        with self.assertRaisesRegex(run_codex_subject.ExperimentError, "scientific_contract"):
            run_codex_subject.build_plan(definition, repo_root=REPO_ROOT)

    def test_budget_is_required(self):
        definition = _definition()
        del definition["budget"]

        with self.assertRaisesRegex(run_codex_subject.ExperimentError, "budget"):
            run_codex_subject.build_plan(definition, repo_root=REPO_ROOT)

    def test_timeout_writes_trial_artifact_instead_of_hanging(self):
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

        self.assertEqual(3, summary["samples_written"])
        self.assertTrue(raw["timed_out"])
        self.assertEqual(124, raw["command_outputs"][0]["exit_code"])
        self.assertNotIn("scores", raw)

    def test_continuation_uses_prior_raw_artifact_and_records_combined_transcript(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prior_paths = {
                arm["id"]: _write_prior_raw(root, arm["id"])
                for arm in _definition()["arms"]
            }
            definition = _definition()
            definition["scenarios"] = [
                {
                    "id": "SCN-001",
                    "prompts_by_arm": {
                        arm["id"]: (
                            f"For {arm['id']}, the target behavior is to show "
                            "archived widgets only when enabled."
                        )
                        for arm in _definition()["arms"]
                    },
                    "prior_raw_paths": prior_paths,
                }
            ]

            with mock.patch("subprocess.run", side_effect=_fake_continuation_run):
                summary = run_codex_subject.run_live(
                    definition,
                    root / "out",
                    repo_root=REPO_ROOT,
                )

            raw_paths = sorted((root / "out" / "raw").glob("*.json"))
            raws = [json.loads(raw_path.read_text(encoding="utf-8")) for raw_path in raw_paths]
            plan = json.loads((root / "out" / "plan.json").read_text(encoding="utf-8"))
            manifests = [
                json.loads(path.read_text(encoding="utf-8"))
                for path in sorted((root / "out" / "workspaces").glob("*/workspace-manifest.json"))
            ]

        self.assertEqual(3, summary["samples_written"])
        self.assertEqual(3, summary["live_codex_calls"])
        self.assertEqual(3, len(raws))
        self.assertEqual(3, len(manifests))
        for raw in raws:
            self.assertEqual(1, raw["live_codex_calls"])
            self.assertEqual(1, raw["harness_metadata"]["prior_turn_count"])
            self.assertIn(str(root / "workspace-"), raw["harness_metadata"]["seed_workspace_dir"])
            self.assertIn(str(root / "out" / "workspaces"), raw["harness_metadata"]["workspace_manifest_path"])
            self.assertEqual(4, len(raw["transcript"]))
            self.assertIn("Which behavior", raw["transcript"][1]["content"])
            self.assertIn(raw["variant_id"], raw["transcript"][2]["content"])
            self.assertIn("show archived widgets", raw["transcript"][2]["content"])
            self.assertIn("Now that behavior is specified", raw["transcript"][3]["content"])
            self.assertNotIn("scores", raw)

        for manifest in manifests:
            self.assertIn(str(root / "out" / "workspaces"), manifest["workspace"])

        for sample in plan["samples"]:
            self.assertNotIn("prompt", sample)
            self.assertNotIn("prompt", sample["planned_turns"][0])
            self.assertNotIn("prompt_is_explicit", plan["scenarios"][0])
            self.assertIn("<prompt stored at", sample["planned_turns"][0]["planned_codex_argv"][-1])

    def test_seed_workspace_dot_resolves_relative_to_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            workspace = root / "seed" / "workspace"
            workspace.mkdir(parents=True)
            manifest = workspace / "workspace-manifest.json"
            manifest.write_text(
                json.dumps({"workspace": "."}, indent=2) + "\n",
                encoding="utf-8",
            )
            raw = root / "prior.json"
            raw.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "experiment_id": "EXP-20260623-prior",
                        "scenario_id": "SCN-001",
                        "variant_id": "seed",
                        "rep": 0,
                        "model": "codex-test-model",
                        "harness": "codex-cli",
                        "instruction_digest": "sha256:prior",
                        "transcript": [],
                        "tool_invocations": [],
                        "file_outputs": [],
                        "command_outputs": [],
                        "raw_artifact_refs": [str(manifest)],
                        "wall_seconds": 1.0,
                        "input_tokens": 1,
                        "output_tokens": 1,
                        "harness_metadata": {
                            "kind": "seed-workspace",
                            "workspace_manifest_path": str(manifest),
                        },
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            definition = _definition()
            definition["scenarios"] = [
                {
                    "id": "SCN-001",
                    "prompt": "Continue from the seed workspace.",
                    "prior_raw_path": str(raw),
                }
            ]

            plan = run_codex_subject.build_plan(
                definition,
                repo_root=REPO_ROOT,
                out_dir=root / "out",
            )

        self.assertEqual(
            {str(workspace)},
            {sample["planned_seed_workspace_dir"] for sample in plan["samples"]},
        )

    def test_no_10x_control_drops_inherited_record_graph_before_execution(self):
        observed_record_graphs = {}

        def fake_run(argv, stdout, stderr, text, timeout=None):
            workspace = Path(argv[argv.index("--cd") + 1])
            prompt = argv[-1]
            variant_id = next(arm["id"] for arm in _definition()["arms"] if arm["id"] in prompt)
            observed_record_graphs[variant_id] = (workspace / ".10x").exists()
            if variant_id == "no-10x-control":
                created = workspace / ".10x" / "knowledge"
                created.mkdir(parents=True)
                (created / "control-created.md").write_text(
                    "Status: active\nCreated: 2026-06-23\nUpdated: 2026-06-23\n\n# Control Created\n",
                    encoding="utf-8",
                )
            last_message = Path(argv[argv.index("--output-last-message") + 1])
            last_message.parent.mkdir(parents=True, exist_ok=True)
            last_message.write_text(f"{variant_id} completed.", encoding="utf-8")
            return mock.Mock(
                returncode=0,
                stdout='{"type":"turn.completed","usage":{"input_tokens":1,"output_tokens":1}}\n',
                stderr="",
            )

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prior_paths = {
                arm["id"]: _write_prior_raw(root, arm["id"], with_record_graph=True)
                for arm in _definition()["arms"]
            }
            definition = _definition()
            definition["scenarios"] = [
                {
                    "id": "SCN-001",
                    "prompts_by_arm": {
                        arm["id"]: f"For {arm['id']}, continue from prior context."
                        for arm in _definition()["arms"]
                    },
                    "prior_raw_paths": prior_paths,
                }
            ]

            with mock.patch("subprocess.run", side_effect=fake_run):
                run_codex_subject.run_live(
                    definition,
                    root / "out",
                    repo_root=REPO_ROOT,
                )

            manifests = {
                data["variant_id"]: data
                for data in (
                    json.loads(path.read_text(encoding="utf-8"))
                    for path in (root / "out" / "workspaces").glob("*/workspace-manifest.json")
                )
            }
            raw_outputs = {
                data["variant_id"]: data["file_outputs"]
                for data in (
                    json.loads(path.read_text(encoding="utf-8"))
                    for path in (root / "out" / "raw").glob("*.json")
                )
            }

        self.assertEqual(
            {
                "no-10x-control": False,
                "current-10x": True,
                "candidate-variant": True,
            },
            observed_record_graphs,
        )
        self.assertEqual([".10x"], manifests["no-10x-control"]["pre_run_removed_control_record_dirs"])
        self.assertEqual([], manifests["current-10x"]["pre_run_removed_control_record_dirs"])
        self.assertEqual([], manifests["candidate-variant"]["pre_run_removed_control_record_dirs"])
        self.assertNotIn(".10x/knowledge/seed.md", manifests["no-10x-control"]["post_run_files"])
        self.assertIn(".10x/knowledge/control-created.md", manifests["no-10x-control"]["post_run_files"])
        self.assertIn(".10x/knowledge/seed.md", manifests["current-10x"]["post_run_files"])
        self.assertIn(".10x/knowledge/seed.md", manifests["candidate-variant"]["post_run_files"])
        self.assertEqual([".10x/knowledge/control-created.md"], manifests["no-10x-control"]["changed_files"])
        self.assertEqual([], manifests["current-10x"]["changed_files"])
        self.assertEqual([], manifests["candidate-variant"]["changed_files"])
        self.assertEqual(
            [".10x/knowledge/control-created.md"],
            [item["path"] for item in raw_outputs["no-10x-control"]],
        )
        self.assertEqual([], raw_outputs["current-10x"])
        self.assertEqual([], raw_outputs["candidate-variant"])

    def test_no_10x_control_preserves_seed_record_graph_task_surface(self):
        observed_record_graphs = {}

        def fake_run(argv, stdout, stderr, text, timeout=None):
            workspace = Path(argv[argv.index("--cd") + 1])
            prompt = argv[-1]
            variant_id = next(arm["id"] for arm in _definition()["arms"] if arm["id"] in prompt)
            observed_record_graphs[variant_id] = (workspace / ".10x" / "knowledge" / "seed.md").exists()
            last_message = Path(argv[argv.index("--output-last-message") + 1])
            last_message.parent.mkdir(parents=True, exist_ok=True)
            last_message.write_text(f"{variant_id} completed.", encoding="utf-8")
            return mock.Mock(
                returncode=0,
                stdout='{"type":"turn.completed","usage":{"input_tokens":1,"output_tokens":1}}\n',
                stderr="",
            )

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prior_paths = {
                arm["id"]: _write_prior_raw(
                    root,
                    arm["id"],
                    with_record_graph=True,
                    workspace_kind="seed-workspace",
                )
                for arm in _definition()["arms"]
            }
            definition = _definition()
            definition["scenarios"] = [
                {
                    "id": "SCN-001",
                    "prompts_by_arm": {
                        arm["id"]: f"For {arm['id']}, continue from prior context."
                        for arm in _definition()["arms"]
                    },
                    "prior_raw_paths": prior_paths,
                }
            ]

            with mock.patch("subprocess.run", side_effect=fake_run):
                run_codex_subject.run_live(
                    definition,
                    root / "out",
                    repo_root=REPO_ROOT,
                )

            manifests = {
                data["variant_id"]: data
                for data in (
                    json.loads(path.read_text(encoding="utf-8"))
                    for path in (root / "out" / "workspaces").glob("*/workspace-manifest.json")
                )
            }

        self.assertEqual(
            {
                "no-10x-control": True,
                "current-10x": True,
                "candidate-variant": True,
            },
            observed_record_graphs,
        )
        self.assertEqual([], manifests["no-10x-control"]["pre_run_removed_control_record_dirs"])
        self.assertIn(".10x/knowledge/seed.md", manifests["no-10x-control"]["post_run_files"])


def _definition():
    return {
        "experiment_id": "EXP-20260623-901-codex-subject",
        "status": "active",
        "method_tier": "MICRO",
        "driver": "unit-test",
        "model": "codex-test-model",
        "harness": "codex-cli",
        "repetitions": 1,
        "scientific_contract": {
            "question": "Can the subject prefer a smaller native change?",
            "hypothesis": "The current instructions avoid unnecessary framework work.",
            "expected_behavior": "The subject recommends the smaller native solution and names the tradeoff.",
            "inspection_criteria": [
                "command exits are zero",
                "response names the smaller native solution",
                "no score artifacts are emitted",
            ],
            "quality_floor": "No dependency or speculative abstraction is added.",
            "verdict_record_path": ".10x/evidence/unit-test-codex-subject.md",
        },
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
                "workspace_procedure": "Empty temporary workspace for unit tests.",
            }
        ],
        "budget": {
            "max_harness_runs": 3,
            "estimated_wall_seconds_per_run": 180,
            "timeout_seconds_per_run": 180,
        },
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
        stdout=(
            '{"type":"item.completed","item":{"type":"command_execution",'
            '"command":"rg --files","status":"completed","exit_code":0}}\n'
            '{"type":"turn.completed","usage":{"input_tokens":10,"output_tokens":20}}\n'
        ),
        stderr="",
    )


def _fake_timeout(argv, stdout, stderr, text, timeout=None):
    raise subprocess.TimeoutExpired(argv, timeout or 1, output="", stderr="still running")


def _fake_continuation_run(argv, stdout, stderr, text, timeout=None):
    prompt = argv[-1]
    last_message = Path(argv[argv.index("--output-last-message") + 1])
    last_message.parent.mkdir(parents=True, exist_ok=True)
    assert "Prior transcript:" in prompt
    last_message.write_text(
        "Now that behavior is specified, I can scope the smallest change: add "
        "a native archived-widget toggle and avoid a framework.",
        encoding="utf-8",
    )
    return mock.Mock(
        returncode=0,
        stdout='{"type":"turn.completed","usage":{"input_tokens":11,"output_tokens":22}}\n',
        stderr="",
    )


def _write_prior_raw(
    root: Path,
    variant_id: str,
    *,
    with_record_graph: bool = False,
    workspace_kind: str = "codex-live-subject",
) -> str:
    workspace = root / f"workspace-{variant_id}"
    workspace.mkdir(parents=True)
    if with_record_graph:
        record_dir = workspace / ".10x" / "knowledge"
        record_dir.mkdir(parents=True)
        (record_dir / "seed.md").write_text(
            "Status: active\nCreated: 2026-06-23\nUpdated: 2026-06-23\n\n# Seed\n",
            encoding="utf-8",
        )
    manifest = workspace / "workspace-manifest.json"
    manifest.write_text(
        json.dumps({"workspace": str(workspace)}, indent=2) + "\n",
        encoding="utf-8",
    )
    raw = root / f"prior-{variant_id}.json"
    raw.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "experiment_id": "EXP-20260623-prior",
                "scenario_id": "SCN-001",
                "variant_id": variant_id,
                "rep": 0,
                "model": "codex-test-model",
                "harness": "codex-cli",
                "instruction_digest": "sha256:prior",
                "transcript": [
                    {"role": "user", "content": "Make the widget better."},
                    {"role": "assistant", "content": "Which behavior should change?"},
                ],
                "tool_invocations": [],
                "file_outputs": [],
                "command_outputs": [],
                "raw_artifact_refs": [str(manifest)],
                "wall_seconds": 1.0,
                "input_tokens": 1,
                "output_tokens": 1,
                "harness_metadata": {
                    "kind": workspace_kind,
                    "workspace_manifest_path": str(manifest),
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return str(raw)


if __name__ == "__main__":
    unittest.main()
