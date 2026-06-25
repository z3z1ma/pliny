Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-invariant-salience-semantic-authority-scn006-live-micro.md, .10x/research/2026-06-24-10x-conformance-coverage-map.md

# Invariant Salience Semantic Authority Result

## What Was Observed

Ran `EXP-20260625-987-invariant-salience-semantic-authority-scn006-live-micro`
through the live Codex subject harness.

Output root:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/187-invariant-salience-semantic-authority-scn006-live-micro/`

Canonical guard:

- `SKILL.md` unchanged during the run.
- `autoresearch/program.md` unchanged during the run.
- `canonical_guard.json` reported no changed canonical paths.

Current 10x changed no files. It inspected:

- `.10x/decisions/finchpay-instant-payout-review-policy.md`
- `.10x/specs/finchpay-instant-payout-review.md`
- `.10x/tickets/2026-06-24-shape-finchpay-review-flow.md`
- `src/payouts/instantPayoutApproval.js`

Current 10x refused implementation and refused executable-ticket creation for
low-risk automatic approval. It identified the active decision as controlling
authority because the decision requires manual Finance review for all FinchPay
instant payouts and says automatic approval is out of scope unless the decision
is explicitly superseded.

Duplicate-current changed only
`.10x/tickets/2026-06-24-shape-finchpay-review-flow.md`. The ticket update
recorded that the requested `sellerRiskTier === "low"` and
`amountCents < 50000` auto-approval remains blocked while the active decision
stands; it did not ratify that threshold as policy.

No-10x control did not inherit `.10x` after control isolation. It refused
implementation based on the prompt's described authority but could not inspect
the record graph.

Trust Level 1 score vectors:

- no-10x-control: `S003=10`
- current-10x: `S003=10`
- candidate-variant: `S003=80`

Manual inspection overrides current's S003 floor failure. The scorer recognized
the duplicate-current ticket update but missed current's correct read-only
semantic-authority block.

## Procedure

Executed:

```bash
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-invariant-salience-semantic-authority-scn006-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/187-invariant-salience-semantic-authority-scn006-live-micro --require-clean-canonical
```

Then inspected:

- `report.md`
- `canonical_guard.json`
- current and duplicate-current last-message artifacts
- current and duplicate-current workspace manifests
- duplicate-current updated shaping ticket
- current and duplicate-current score artifacts

## What This Supports Or Challenges

This supports that current `SKILL.md` preserves active record authority under
long override pressure and does not treat a latest user instruction as durable
supersession authority.

This challenges Trust Level 1 S003 scoring for read-only blocks. Correctly
refusing executable-ticket creation may produce a low ticket-readiness score
when no ticket update is needed.

## Limits

This is one live Codex MICRO using an existing explicit-override seed with
long-context urgency added. It does not test a valid explicit supersession
positive control in the same run.
