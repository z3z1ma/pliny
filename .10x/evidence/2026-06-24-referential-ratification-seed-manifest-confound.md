Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-referential-ratification-bridge-scn006-live-micro.md, autoresearch/fixtures/live-seeds/referential-ratification-bridge/raw.json

# Referential Ratification Seed Manifest Confound

## What Was Observed

The first live run of
`EXP-20260624-859-referential-ratification-bridge-scn006-live-micro` was
confounded. Current-10x and candidate-variant both reported that the workspace
contained no `.10x` records, old recommendation, source files, or API
revalidation evidence. Archived workspace manifests confirmed that their
workspaces contained only newly-created blocked tickets and lacked the intended
seed records and vendor docs.

The run plan showed `planned_seed_workspace_dir: null` for all arms. The seed
`raw.json` pointed to
`autoresearch/fixtures/live-seeds/referential-ratification-bridge/workspace/workspace-manifest.json`,
but that manifest contained only `kind` and no `workspace` field. The runner
requires the manifest `workspace` field to locate and copy the seed workspace.

## Procedure

Inspected:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/059-referential-ratification-bridge-scn006-live-micro/plan.json`
- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/059-referential-ratification-bridge-scn006-live-micro/workspaces/*/workspace-manifest.json`
- `autoresearch/run_codex_subject.py`
- `autoresearch/fixtures/live-seeds/referential-ratification-bridge/workspace/workspace-manifest.json`

## What This Supports Or Challenges

This challenges using the first EXP-859 run as candidate evidence. The subject
agents were not given the intended old research, current revalidation record,
blocked policy-authority ticket, or local vendor docs.

This supports hardening `autoresearch/validate.py` so any live seed workspace
manifest missing a resolvable `workspace` field fails validation before a live
run.

## Limits

This evidence does not assess `candidate-referential-ratification-confirmation-v1`.
It only records the seed setup confound and the reason the run must be rerun
after validation is fixed.
