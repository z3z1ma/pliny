Status: recorded
Created: 2026-06-27
Updated: 2026-06-27
Relates-To: .10x/decisions/autoresearch-live-trial-scientist-inspection.md, .10x/evidence/2026-06-27-retire-fixture-backed-autoresearch.md

# Current Skill Smoke Trial

## Summary

Ran one live `current-10x` trial through `autoresearch/run_once.py` using the
current canonical `SKILL.md`, one SCN-010 scenario, and one repetition.

Result: pass.

## Procedure

Experiment definition:

- `.10x/evidence/.storage/2026-06-27-current-skill-smoke/experiment.json`

Command:

```text
python3 autoresearch/run_once.py --experiment .10x/evidence/.storage/2026-06-27-current-skill-smoke/experiment.json --out .10x/evidence/.storage/2026-06-27-current-skill-smoke/EXP-20260627-001-current-skill-smoke-scn010-live-micro
```

Output root:

- `.10x/evidence/.storage/2026-06-27-current-skill-smoke/EXP-20260627-001-current-skill-smoke-scn010-live-micro`

## Observations

- The runner completed successfully and wrote one sample.
- `summary.json` reports `mode: live`, `samples_written: 1`, and
  `live_codex_calls: 1`.
- The command artifact reports `exit_code: 0`, `timed_out: false`, and usage of
  `132450` input tokens and `776` output tokens.
- `canonical_guard.json` reports `unchanged_during_run: true` for `SKILL.md` and
  `autoresearch/program.md`.
- The workspace manifest reports `changed_files: ["README.md"]`,
  `post_run_files: ["README.md"]`, no suppressed instruction files present, no
  workspace contamination, and no timeout.
- Manual diff inspection found exactly one content change: `succesful` became
  `successful` in `README.md`.
- The archived workspace contains only `README.md` and `workspace-manifest.json`.

## Artifact Pointers

- Summary: `.10x/evidence/.storage/2026-06-27-current-skill-smoke/EXP-20260627-001-current-skill-smoke-scn010-live-micro/summary.json`
- Plan: `.10x/evidence/.storage/2026-06-27-current-skill-smoke/EXP-20260627-001-current-skill-smoke-scn010-live-micro/plan.json`
- Report: `.10x/evidence/.storage/2026-06-27-current-skill-smoke/EXP-20260627-001-current-skill-smoke-scn010-live-micro/report.md`
- Raw trial: `.10x/evidence/.storage/2026-06-27-current-skill-smoke/EXP-20260627-001-current-skill-smoke-scn010-live-micro/raw/sha256-97f98cbdad2d10590e2ba5c028d8b2954d1b85df416750a80934528b6412d216.json`
- Workspace manifest: `.10x/evidence/.storage/2026-06-27-current-skill-smoke/EXP-20260627-001-current-skill-smoke-scn010-live-micro/workspaces/sha256-97f98cbdad2d10590e2ba5c028d8b2954d1b85df416750a80934528b6412d216/workspace-manifest.json`

## Limits

This is one smoke trial, not campaign-level proof. It establishes that the
renamed seed path, one-shot runner, live Codex subject execution, artifact
capture, report generation, canonical guard, and current `SKILL.md` positive
control all function for this SCN-010 case.
