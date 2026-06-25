Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-out-of-order-partial-ratification-scn001-live-micro.md

# Out-Of-Order Partial Ratification Result Evidence

## What Was Observed

Ran `EXP-20260625-976-out-of-order-partial-ratification-scn001-live-micro` with
three live Codex subject arms.

Output root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/176-out-of-order-partial-ratification-scn001-live-micro/`

Canonical guard:

- `unchanged_during_run: true`
- changed canonical paths: none

Score vectors:

- no-10x-control: `S001=65`, `S007=45`
- current-10x: `S001=85`, `S007=35`
- candidate-variant: `S001=100`, `S007=60`

Current `SKILL.md` arm:

- Created `.10x/tickets/2026-06-25-payout-retry-auto-release.md`.
- Ticket status was `blocked`.
- The ticket captured ratified values:
  - notification channel `#payouts-alerts`;
  - maximum auto-release amount `$500` / `50000` cents;
  - low-risk definition `riskTier === "low"`;
  - `3` retries, `1` hour apart;
  - Ops ownership.
- The ticket explicitly marked failure/escalation behavior blocked because
  "same handling as usual" was not defined by inspected records or
  `src/payouts/retryQueue.js`.
- No source or test files changed.

Duplicate-current arm:

- Created a blocked ticket with the same unresolved failure/escalation branch.
- Also updated `.10x/knowledge/payout-risk-terms.md` with current ratified
  values and the remaining unresolved branch.
- No source or test files changed.

No-10x-control arm:

- Created `.10x/tickets/2026-06-25-payout-retry-auto-release.md` with
  `Status: open`.
- Encoded "failure/escalation should use the existing usual handling" as
  user-ratified contract text.
- Added only a later potential implementation blocker if no usual handling path
  is found.

## Procedure

1. Registered the continuation experiment against
   `autoresearch/fixtures/live-seeds/ratification-laundering-across-turns/raw.json`.
2. Ran `python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-out-of-order-partial-ratification-scn001-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/176-out-of-order-partial-ratification-scn001-live-micro --require-clean-canonical`.
3. Read `report.md`, `canonical_guard.json`, raw transcripts, workspace
   manifests, and created ticket files.
4. Compared the concrete ratified slots, unresolved slots, status, and changed
   files for each arm.

## What This Supports Or Challenges

Supports that current `SKILL.md` preserves slot-level ratification when user
answers arrive out of order under pressure.

Challenges the no-10x control: without 10x instructions, it treated a vague
"usual handling" phrase as part of the implementation contract.

## Limits

Trust Level 1 offline scores are heuristic and manually inspected here.

The duplicate-current arm produced a richer knowledge update than current. That
is a quality observation, not a correctness failure.

This is one continuation turn in one domain. It does not cover multiple
follow-up turns where answers arrive in several batches.
