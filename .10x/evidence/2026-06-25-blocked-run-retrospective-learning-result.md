Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-blocked-run-retrospective-learning-scn012-live-micro.md

# Blocked-Run Retrospective Learning Result

## What Was Observed

`EXP-20260625-972-blocked-run-retrospective-learning-scn012-live-micro` ran
three live Codex subject arms over the ACME billing blocked-run retrospective
fixture:

- no-10x-control:
  `sha256-b00bf584400e9b9c13d0dcc46778c1d493d44eb32062562157ffe0a4e2bc395a`
- current-10x:
  `sha256-d371da2cd62ede7cc36d0961f76926d0091ece37b5134af633d4998e06de5d2d`
- candidate-variant duplicate current:
  `sha256-81a8c758c98ba106f3b18b37410736a5cdd971bf8c543cc020e40e2d5eb5cec0`

The current-10x arm passed manual inspection:

- left
  `.10x/tickets/2026-06-25-implement-acme-billing-event-import.md`
  `Status: blocked`;
- left
  `.10x/tickets/2026-06-25-acme-billing-import-parent.md`
  `Status: active`;
- preserved the duplicate invoice event reject-row versus quarantine-file
  decision as an unresolved blocker;
- created `.10x/skills/acme-429-fixture-replay.md` with a concrete tracked
  fixture, frozen-date, and `Retry-After` replay procedure;
- created `.10x/knowledge/acme-billing-vendor-event-id.md` for the
  `vendorEventId` vocabulary;
- opened `.10x/tickets/2026-06-25-cover-malformed-discount-amount.md` for the
  out-of-scope malformed discount amount coverage risk;
- left `src/billing/importAcmeEvents.js` and
  `src/billing/importAcmeEvents.test.js` unchanged versus the seed fixture.

The duplicate-current arm also passed manual inspection with equivalent child
status, parent status, skill, knowledge, follow-up ticket, and no source edits.

The no-10x-control arm created some `.10x` records after control cleanup but
misrouted the out-of-scope risk to a follow-up about automating 429 fixture
replay rather than malformed discount amount coverage.

Trust Level 1 heuristic scores undercounted the current and duplicate-current
arms at S002=70 and S006=75 despite the manual pass. no-10x-control scored
S002=50 and S006=50.

## Procedure

1. Created the seed workspace under
   `autoresearch/trial-seeds/blocked-run-retrospective-learning/`.
2. Registered
   `.10x/research/2026-06-25-blocked-run-retrospective-learning-scn012-live-micro.md`.
3. Ran:
   `python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-blocked-run-retrospective-learning-scn012-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/172-blocked-run-retrospective-learning-scn012-live-micro --require-clean-canonical`
4. Inspected the generated `summary.json`, `report.md`, `plan.json`, last
   messages, current/candidate subject records, and `diff -qr` source checks.

Raw artifacts:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/172-blocked-run-retrospective-learning-scn012-live-micro/`

## What This Supports Or Challenges

This supports the conclusion that current `SKILL.md` generalizes the promoted
"durable learning is not closure-gated" rule beyond the original Ledger fixture.
It also supports upgrading retrospective learning extraction coverage from
`Partial` to `Partial-strong`.

## Limits

This is one MICRO scenario with an explicit prompt that names the durable
learning. It does not prove multi-session or lower-assistance blocked-run
learning behavior. It also does not test skill mirroring into a harness-native
directory because the seed workspace did not provide one.
