Status: recorded
Created: 2026-06-27
Updated: 2026-06-27
Relates-To: .10x/tickets/done/2026-06-27-tighten-autoresearch-happy-path-ergonomics.md, .10x/reviews/2026-06-27-current-skill-smoke-tooling-review.md

# Autoresearch Ergonomics Tightening Result

## Summary

Tightened the active autoresearch setup so a fresh scientist can express a
current-skill smoke, a regression run, or a comparative experiment through one
runner schema.

Result: pass.

## Changes Verified

- `arms` is now exact: the runner uses exactly the ordered list in the
  experiment definition. One-arm current-skill runs need no special mode.
- Experiment definitions now require a `scientific_contract` with question,
  hypothesis, expected behavior, inspection criteria, quality floor, and verdict
  record path.
- Scenarios must provide either prior raw artifacts or a workspace procedure, so
  seed provenance is explicit.
- Budgets must explicitly include maximum harness runs, estimated per-run wall
  seconds, and per-run timeout.
- Raw artifacts and summaries preserve the scientific contract.
- Raw trial metadata records `archived_workspace_dir`.
- Reports include a Scientific Contract section and show durable archived
  workspace paths beside each trial artifact.
- The active spec, program, README, experiment template, manual inspection
  template, and catalogs now align with live-trial scientist inspection.

## Ergonomics Proof

Definition:

- `.10x/evidence/.storage/2026-06-27-autoresearch-ergonomics/experiment.json`

Command:

```text
python3 autoresearch/run_codex_subject.py --experiment .10x/evidence/.storage/2026-06-27-autoresearch-ergonomics/experiment.json --out .10x/evidence/.storage/2026-06-27-autoresearch-ergonomics/dry-run-out --dry-run
```

Observed dry-run result:

- Exit code: 0.
- `mode`: `plan`.
- `scientific_contract`: present in the public plan and the planned sample.
- Planned samples: 1.
- Planned arm: `current-10x`.
- Planned scenario: `SCN-010`.
- Seed provenance: `autoresearch/trial-seeds/exact-trivial-edit/raw.json`.
- Planned archived workspace path: under
  `.10x/evidence/.storage/2026-06-27-autoresearch-ergonomics/dry-run-out/workspaces/`.

## Verification

Commands run:

```text
python3 autoresearch/validate.py
python3 -m py_compile autoresearch/run_codex_subject.py autoresearch/report.py autoresearch/validate.py
python3 -m unittest discover -s autoresearch/tests
```

Results:

- `autoresearch contracts valid`.
- `py_compile` exited 0.
- Full autoresearch test suite: 44 tests passed.

## Limits

The proof used the planning path rather than another live Codex call. The prior
live current-skill smoke already proved live execution and artifact capture on
the same seed family; this result proves the revised schema and ergonomics.
