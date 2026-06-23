from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from autoresearch import canonical_guard, report, run_full_codex, run_micro
except ImportError:  # pragma: no cover - supports direct script execution.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from autoresearch import canonical_guard, report, run_full_codex, run_micro


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
    for loader in (run_micro.load_definition, run_full_codex.load_definition):
        try:
            return loader(definition_path)
        except (run_micro.ExperimentError, run_full_codex.ExperimentError, json.JSONDecodeError) as exc:
            errors.append(str(exc))
    raise RunOnceError("could not load experiment definition: " + " | ".join(errors))


def run_once(
    definition: dict[str, Any],
    out_dir: str | Path,
    *,
    tier: str = "auto",
    write_report: bool = True,
    campaign_path: str | Path | None = None,
    guard_canonical: bool = True,
    require_clean_canonical: bool = False,
    repo_root: Path = REPO_ROOT,
) -> dict[str, Any]:
    selected_tier = _selected_tier(definition, tier)
    output_root = Path(out_dir)
    output_root.mkdir(parents=True, exist_ok=True)
    guard_before = None
    guard_path = None
    if guard_canonical:
        if require_clean_canonical:
            canonical_guard.require_clean_git(repo_root)
        guard_before = canonical_guard.snapshot(repo_root)
        guard_path = output_root / "canonical_guard.json"

    if selected_tier == "MICRO":
        runner_summary = run_micro.run_fixture_backed(definition, output_root, repo_root=repo_root)
        runner = "autoresearch/run_micro.py"
    elif selected_tier == "FULL":
        runner_summary = run_full_codex.run_fixture_smoke(definition, output_root, repo_root=repo_root)
        runner = "autoresearch/run_full_codex.py"
    else:
        raise RunOnceError(f"unsupported method_tier: {selected_tier}")

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
        "method_tier": selected_tier,
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
        "limits": [
            "run_once.py does not loop, resume, generate candidates, or mutate canonical SKILL.md.",
            "canonical_guard.json records SKILL.md and autoresearch/program.md pre/post hashes when guard_canonical is enabled.",
            "Fixture-backed scores remain limited by scorer trust and scenario coverage.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run exactly one 10x autoresearch MICRO or FULL experiment."
    )
    parser.add_argument("--experiment", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--tier", choices=("auto", "MICRO", "FULL"), default="auto")
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
            tier=args.tier,
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
        run_micro.ExperimentError,
        run_full_codex.ExperimentError,
    ) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


def _selected_tier(definition: dict[str, Any], tier: str) -> str:
    if tier != "auto":
        return tier
    method_tier = definition.get("method_tier")
    if not isinstance(method_tier, str):
        raise RunOnceError("experiment definition missing method_tier")
    return method_tier


if __name__ == "__main__":
    raise SystemExit(main())
