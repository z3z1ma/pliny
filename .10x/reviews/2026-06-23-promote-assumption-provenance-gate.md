Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Target: SKILL.md, autoresearch/candidates/2026-06-23-assumption-provenance-gate.md
Verdict: pass

# Promote Assumption Provenance Gate Review

## Target

Canonical promotion of the proven spine of
`candidate-assumption-provenance-gate-v1` into `SKILL.md`.

## Findings

- **Pass:** The promoted text targets an observed failure mode: plausible source
  names, stale notes, and common product patterns can pull an agent into
  correct-looking implementation on unratified semantics.
- **Pass:** The change strengthens the Outer Loop rather than creating an exit
  from it. Unresolved execution-relevant assumptions remain blockers.
- **Pass:** The promotion is narrower than the candidate overlay. It promotes
  assumption provenance, semantic defaults, source/stale-note non-authority,
  tests-as-assumptions, and user-legible closure; it does not add broad
  optimizer constraints or process-heavy ledgers.
- **Pass:** The promoted text preserves useful autonomy by allowing mechanical
  defaults while forbidding semantic defaults.
- **Concern accepted:** Current already passed the payment-retry seed. Promotion
  relies on the greenline held-out seed for candidate-over-current signal and
  manual inspection for semantic quality.
- **Concern accepted:** The new section increases prompt length. The added text
  is near the top of the protocol because the failure mode is central to 10x:
  preventing unratified assumptions from entering implementation.

## Verdict

Pass. Promote the assumption-provenance gate and continue with semantic
continuation and record-hardening held-out MICROs.

## Residual Risk

The main residual risk is overblocking when the user has actually ratified a
semantic value. Future scenarios should test continuations where one semantic
branch is ratified and another is still implied by "existing context" or stale
records.
