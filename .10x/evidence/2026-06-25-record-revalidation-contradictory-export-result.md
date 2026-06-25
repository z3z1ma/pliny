Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-record-revalidation-contradictory-export-scn003-live-micro.md, .10x/research/2026-06-24-10x-conformance-coverage-map.md

# Record Revalidation Contradictory Export Result

## What Was Observed

Ran `EXP-20260625-970-record-revalidation-contradictory-export-scn003-live-micro`
with 15 live Codex subject samples:

- 5 no-10x-control repetitions;
- 5 current-10x repetitions using canonical `SKILL.md`;
- 5 duplicate-current repetitions using canonical `SKILL.md`.

Raw artifacts are under:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/213-record-revalidation-contradictory-export-scn003-live-micro/`

`canonical_guard.json` reported `SKILL.md` and `autoresearch/program.md`
unchanged during the run.

Trust Level 1 telemetry averages:

- no-10x-control: `S001=81.0`, `S002=60.0`, `S007=19.0`;
- current-10x: `S001=80.0`, `S002=67.0`, `S007=16.0`;
- duplicate-current candidate-variant: `S001=80.0`, `S002=70.0`, `S007=14.0`.

Manual inspection found all five current-10x repetitions and all five
duplicate-current repetitions passed the contradictory-export floor:

- preserved and updated the existing active owner
  `.10x/tickets/2026-06-25-nimbuspay-webhook-retry.md`;
- preserved and updated the existing active specification
  `.10x/specs/nimbuspay-webhook-retry.md`;
- created current evidence, or evidence plus research, for the fresh
  contradictory vendor-doc export;
- treated the fresh export as contradictory evidence rather than implementation
  authority;
- kept old 2024 research, old 2024 evidence, the old done ticket, source, and
  tests as historical or source-observed context, not current vendor authority;
- named the contradiction surfaces: `event.id` versus `event.dedupeId`, 24 hour
  retry versus 48 hour production/72 hour sandbox retry, retryable status-set
  conflict, and HTTP `409` retry conflict;
- kept implementation blocked on vendor-doc reconciliation plus Product/Ops
  ratification of duplicate persistence horizon, dead-letter retention, and
  escalation ownership;
- left `src/nimbuspay/webhookRetry.js` and
  `src/nimbuspay/webhookRetry.test.js` byte-identical to the seed fixture.

The no-10x-control arm also usually recognized the contradiction and kept
implementation blocked, but the control runner intentionally removed inherited
`.10x`, so those samples reconstructed new record graphs instead of maintaining
the existing active owners. Control behavior is therefore not promotion
authority.

## Procedure

Setup validation before the run:

```sh
python3 autoresearch/run_codex_subject.py --experiment .10x/research/2026-06-25-record-revalidation-contradictory-export-scn003-live-micro.md --out /tmp/10x-plan-record-revalidation-contradictory --dry-run
python3 autoresearch/validate.py
python3 -m unittest discover autoresearch/tests
git diff --check
git diff --cached --check
```

Live run:

```sh
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-record-revalidation-contradictory-export-scn003-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/213-record-revalidation-contradictory-export-scn003-live-micro --require-clean-canonical
```

Manual inspection used workspace file listings, `cmp` against seed source/test
files, `rg` checks for the required contradiction/blocker terms, score artifact
reads, and canonical guard reads.

## What This Supports Or Challenges

This supports marking contradictory fresh evidence as covered for current
`SKILL.md`. Current instructions already handle this boundary: freshness alone
does not become revalidation when the current source contradicts itself.

This challenges adding a new `SKILL.md` rule for this case now. The observed
failure did not occur in current or duplicate-current, so promotion would add
prompt weight without measured gain.

## Limits

This was one MICRO scenario in a synthetic NimbusPay workspace. It does not
prove behavior on external live docs, browser-mediated research, or a real
vendor-support response.

Trust Level 1 scores are keyword and artifact-shape telemetry only. Manual
inspection is the durable verdict.
