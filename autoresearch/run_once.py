from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from autoresearch import canonical_guard, report, run_codex_subject
except ImportError:  # pragma: no cover - supports direct script execution.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from autoresearch import canonical_guard, report, run_codex_subject


REPO_ROOT = Path(__file__).resolve().parents[1]


class RunOnceError(ValueError):
    pass


def load_definition(path: str | Path) -> dict[str, Any]:
    definition_path = Path(path)
    if definition_path.suffix == ".json":
        data = json.loads(definition_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise RunOnceError("experiment definition must be a JSON object")
        return data

    errors = []
    for loader in (run_codex_subject.load_definition,):
        try:
            return loader(definition_path)
        except (
            run_codex_subject.ExperimentError,
            json.JSONDecodeError,
        ) as exc:
            errors.append(str(exc))
    raise RunOnceError("could not load experiment definition: " + " | ".join(errors))


def run_once(
    definition: dict[str, Any],
    out_dir: str | Path,
    *,
    write_report: bool = True,
    campaign_path: str | Path | None = None,
    guard_canonical: bool = True,
    require_clean_canonical: bool = False,
    repo_root: Path = REPO_ROOT,
) -> dict[str, Any]:
    method_tier = definition.get("method_tier")
    if not isinstance(method_tier, str):
        raise RunOnceError("experiment definition missing method_tier")
    output_root = Path(out_dir)
    output_root.mkdir(parents=True, exist_ok=True)
    guard_before = None
    guard_path = None
    if guard_canonical:
        if require_clean_canonical:
            canonical_guard.require_clean_git(repo_root)
        guard_before = canonical_guard.snapshot(repo_root)
        guard_path = output_root / "canonical_guard.json"

    if _uses_live_codex_subject(definition):
        runner_summary = run_codex_subject.run_live(definition, output_root, repo_root=repo_root)
        runner = "autoresearch/run_codex_subject.py"
    else:
        raise RunOnceError("unsupported experiment definition")

    report_path = None
    if write_report:
        report_path = output_root / "report.md"
        report.write_report(output_root, report_path, campaign_path=campaign_path)

    if guard_before is not None and guard_path is not None:
        guard_after = canonical_guard.snapshot(repo_root)
        canonical_guard.write_guard_report(
            guard_path,
            before=guard_before,
            after=guard_after,
            require_clean=require_clean_canonical,
        )
        changed = canonical_guard.diff_snapshots(guard_before, guard_after)
        if changed:
            raise RunOnceError(
                "canonical files changed during run: " + ", ".join(changed)
            )

    return {
        "experiment_id": runner_summary.get("experiment_id", definition.get("experiment_id")),
        "method_tier": method_tier,
        "runner": runner,
        "mode": runner_summary.get("mode"),
        "out_dir": str(output_root),
        "summary_path": str(output_root / "summary.json"),
        "plan_path": runner_summary.get("plan_path"),
        "raw_output_dir": runner_summary.get("raw_output_dir"),
        "score_artifact_dir": runner_summary.get("score_artifact_dir"),
        "report_path": str(report_path) if report_path else None,
        "canonical_guard_path": str(guard_path) if guard_path else None,
        "samples_written": runner_summary.get("samples_written"),
        "promotion_decision": "not-performed",
        "loop_controller": "LLM reasoning engine; this command runs exactly one iteration",
        "limits": _limits_for_runner(runner_summary),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run exactly one 10x autoresearch MICRO or FULL experiment."
    )
    parser.add_argument("--experiment", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--campaign", type=Path)
    parser.add_argument("--no-report", action="store_true")
    parser.add_argument("--no-canonical-guard", action="store_true")
    parser.add_argument("--require-clean-canonical", action="store_true")
    args = parser.parse_args(argv)

    if args.no_report and args.campaign:
        print("--campaign requires report generation", file=sys.stderr)
        return 2
    if args.no_canonical_guard and args.require_clean_canonical:
        print("--require-clean-canonical requires the canonical guard", file=sys.stderr)
        return 2

    try:
        definition = load_definition(args.experiment)
        result = run_once(
            definition,
            args.out,
            write_report=not args.no_report,
            campaign_path=args.campaign,
            guard_canonical=not args.no_canonical_guard,
            require_clean_canonical=args.require_clean_canonical,
        )
    except (
        OSError,
        json.JSONDecodeError,
        RunOnceError,
        canonical_guard.CanonicalGuardError,
        report.ReportError,
        run_codex_subject.ExperimentError,
    ) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


def _uses_live_codex_subject(definition: dict[str, Any]) -> bool:
    if str(definition.get("harness", "")).lower() != "codex-cli":
        return False
    for scenario in definition.get("scenarios", []):
        if isinstance(scenario, dict) and scenario.get("fixtures"):
            return False
    return True


def _limits_for_runner(runner_summary: dict[str, Any]) -> list[str]:
    limits = [
        "run_once.py does not loop, resume, generate candidates, or mutate canonical SKILL.md.",
        "canonical_guard.json records SKILL.md and autoresearch/program.md pre/post hashes when guard_canonical is enabled.",
    ]
    if runner_summary.get("mode") == "live":
        limits.extend(
            [
                "Live subject outputs are candidate-quality evidence, but scores remain Trust Level 1 offline scoring until manually inspected.",
                "Codex system context and authenticated home state are outside complete runner control; inspect workspace manifests and command artifacts.",
            ]
        )
    return limits


if __name__ == "__main__":
    raise SystemExit(main())
