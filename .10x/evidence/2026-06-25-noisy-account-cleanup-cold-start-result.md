Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-noisy-account-cleanup-cold-start-scn003-live-micro.md

# Noisy Account Cleanup Cold Start Result Evidence

## What Was Observed

Ran `EXP-20260625-977-noisy-account-cleanup-cold-start-scn003-live-micro` with
three live Codex subject arms.

Output root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/177-noisy-account-cleanup-cold-start-scn003-live-micro/`

Canonical guard:

- `unchanged_during_run: true`
- changed canonical paths: none

Score vectors:

- no-10x-control: `S001=55`, `S002=80`, `S007=30`
- current-10x: `S001=55`, `S002=70`, `S007=15`
- candidate-variant: `S001=55`, `S002=70`, `S007=15`

Manual inspection overrides the Trust Level 1 score floor failures because this
run tested read-only cold-start reconstruction, not record creation.

Current `SKILL.md` arm:

- Read or cited `.10x/decisions/account-cleanup-authority.md`.
- Read or cited `.10x/tickets/2026-06-25-shape-account-cleanup-audit-export.md`.
- Read or cited `.10x/knowledge/account-lifecycle-terms.md`.
- Identified the old 30-day dry-run evidence as non-authoritative historical
  context.
- Recovered active settled facts:
  - inactive trial accounts only;
  - 90-day inactivity threshold;
  - zero balance;
  - no legal hold;
  - no open support escalation.
- Recovered unresolved blockers:
  - audit export retention;
  - audit export recipient or storage owner;
  - cleanup failure and escalation behavior.
- Named Legal/Data ratification as the next safe action.
- Made no file edits.

Duplicate-current arm:

- Also passed.
- Additionally inspected `src/accounts/accountCleanup.js` and explicitly named
  its stale 30-day predicate as source behavior that must not be treated as
  policy authority.
- Made no file edits.

No-10x-control arm:

- Had inherited `.10x` removed by control isolation.
- Correctly stated that no project records were present and source alone was
  insufficient to reconstruct product intent.
- Made no file edits.

## Procedure

1. Created the tracked seed workspace
   `autoresearch/fixtures/live-seeds/noisy-account-cleanup-cold-start/`.
2. Registered the experiment
   `.10x/research/2026-06-25-noisy-account-cleanup-cold-start-scn003-live-micro.md`.
3. Ran `python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-noisy-account-cleanup-cold-start-scn003-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/177-noisy-account-cleanup-cold-start-scn003-live-micro --require-clean-canonical`.
4. Read `report.md`, `canonical_guard.json`, raw transcripts, workspace
   manifests, and command events.
5. Compared each arm against the manual cold-start recovery criteria.

## What This Supports Or Challenges

Supports that current `SKILL.md` can reconstruct a noisy cold-start handoff from
active records while treating terminal records, old evidence, and stale source
as non-authoritative context.

Challenges the offline scorer for read-only cold-start scenarios: score floor
failures can be false negatives when the desired behavior is to return the
state without writing records.

## Limits

This is still a synthetic seed, not a true second-agent handoff after a prior
live agent authored the records.

The no-10x-control arm cannot exercise record-graph reconstruction because
control isolation intentionally removes `.10x`.
