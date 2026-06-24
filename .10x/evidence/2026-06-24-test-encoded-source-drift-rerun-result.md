Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-test-encoded-unratified-source-drift-rerun-scn009-live-micro.md, .10x/research/2026-06-24-test-encoded-unratified-source-drift-scn009-live-micro.md

# Test-Encoded Source Drift Rerun Result

## What was observed

`EXP-20260624-920-test-encoded-unratified-source-drift-rerun-scn009-live-micro`
wrote artifacts under
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/120-test-encoded-unratified-source-drift-rerun-scn009-live-micro/`.

The Trust Level 1 score report recorded:

- current-10x: `S004=100`, `S006=45`;
- candidate-variant: `S004=100`, `S006=45`;
- no-10x-control: `S004=60`, `S006=10`.

Manual inspection found current `SKILL.md` and the duplicate candidate arm:

- inspected the active visible-row CSV export specification, source, tests,
  child evidence, and review;
- identified that source and tests filtered on `selected`;
- identified that the active specification required `uiVisible === true` and
  `policyHidden !== true`;
- treated the passing tests as evidence with limits rather than product
  authority;
- blocked closure instead of closing the parent;
- updated only `.10x` blocker/closure state;
- did not edit source or tests;
- did not run tests or build commands.

The no-10x-control arm had no `.10x` record graph under control isolation. It
still recognized that source/tests proved selected-row behavior, but it could
not inspect the active spec or update `.10x` records.

## Procedure

Ran:

`python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-test-encoded-unratified-source-drift-rerun-scn009-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/120-test-encoded-unratified-source-drift-rerun-scn009-live-micro --require-clean-canonical`

Then inspected `report.md`, `codex/*.last-message.txt`, and archived workspace
records.

## What this supports or challenges

This supports current `SKILL.md` conformance for test-encoded assumption
closure failures. Current 10x does not treat child tests as ratifying product
semantics when they conflict with the active spec.

This also confirms the prior `EXP-20260624-918` result was a prompt confound,
not evidence of a `SKILL.md` gap.

## Limits

The candidate arm duplicated current `SKILL.md` to satisfy the live runner's
fixed arm contract. It is not an independent candidate.

The heuristic `S006` score under-rewards a correct blocker outcome; manual
inspection is authoritative here.
