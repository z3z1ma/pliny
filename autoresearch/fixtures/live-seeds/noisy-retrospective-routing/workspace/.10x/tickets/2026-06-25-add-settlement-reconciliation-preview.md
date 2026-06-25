Status: active
Created: 2026-06-25
Updated: 2026-06-25
Parent: .10x/tickets/2026-06-25-settlement-reconciliation-parent.md
Depends-On: .10x/specs/settlement-reconciliation-preview.md, .10x/evidence/2026-06-25-settlement-reconciliation-child-test-output.md, .10x/reviews/2026-06-25-settlement-reconciliation-child-review.md

# Add Settlement Reconciliation Preview

## Scope

Implement settlement reconciliation preview behavior for Finance Operations.

Included:

- Preserve imported row `settlementRef`.
- Normalize settlement amounts into integer cents.
- Preserve processor lifecycle state.

Excluded:

- Historical FX rounding tolerance.
- Live processor API calls.
- UI rendering.

## Acceptance Criteria

- AC-001: Preview output includes each row's `settlementRef`.
- AC-002: Preview output includes normalized cent amounts.
- AC-003: Preview output preserves lifecycle state.
- AC-004: Closure captures retrospective obligations before the parent closes.

## Progress And Notes

- 2026-06-25: Child executor reported implementation complete and focused tests
  passed.
- 2026-06-25: Evidence covers `settlementRef`, cent amounts, and lifecycle
  state preservation.
- 2026-06-25: Review passed for the settlement reconciliation preview scope.
- 2026-06-25: Durable procedure candidate: stable settlement mismatch tests
  require tracked NDJSON fixtures under `testdata/settlements/`, a frozen
  settlement date of `2026-04-30`, and the offline processor replay adapter.
  This was learned after two failed attempts that used inline JSON and the live
  processor sandbox.
- 2026-06-25: Durable vocabulary candidate: imported settlement references are
  named `settlementRef`, not `externalTransferId`.
- 2026-06-25: Durable vocabulary candidate: `pending_release` is a processor
  lifecycle state, not a risk tier.
- 2026-06-25: Follow-up candidate: historical FX rounding tolerance still lacks
  coverage and is outside this ticket.
- 2026-06-25: Noise: one failed run was caused by a local shell alias named
  `nr`; do not preserve that as project knowledge.
- 2026-06-25: Noise: one rerun used `--runInBand` because the developer's laptop
  was under heavy load; do not preserve that as a procedure unless repeated
  evidence shows project-level test flake.
- 2026-06-25: Noise: Mara prefers terse local debug logs; this did not affect
  product behavior, tests, or project conventions.

## Blockers

- None for settlement reconciliation preview scope.
