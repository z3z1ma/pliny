---
id: critique:plan-wave-coverage-rereview
kind: critique
status: final
created_at: 2026-05-02T21:20:05Z
updated_at: 2026-05-02T21:20:05Z
scope:
  kind: repository
  repositories:
    - repo:root
review_target: "ticket:planwv11 repair diff cb69ab9..working-tree"
links:
  ticket:
    - ticket:planwv11
  critique:
    - critique:plan-wave-coverage-review
  evidence:
    - evidence:plan-wave-coverage-validation
  packet:
    - packet:ralph-ticket-planwv11-20260502T210325Z
    - packet:ralph-ticket-planwv11-20260502T211053Z
external_refs: {}
---

# Summary

Re-reviewed `ticket:planwv11` after the first repair iteration.

# Review Target

Current working-tree diff from baseline
`cb69ab9efdefbe4dabb9c86f34048687a0c8930e`, including both Ralph packets, the
first critique, repaired evidence, and changed plan product surfaces.

# Verdict

`changes_required` - original findings are resolved, but new claim-matrix and
repair-packet lifecycle grammar issues need repair before acceptance.

# Findings

## PLANWV11-RCRIT-001: Claim matrix uses non-canonical status values

Severity: medium
Confidence: high
State: open

Observation:

The ticket claim matrix uses freeform status values such as
`repair applied pending re-critique`, `supported pending re-critique`, and
`pending mandatory re-critique` instead of the claim-matrix vocabulary in
`skills/loom-records/references/claim-coverage.md`.

Why it matters:

The ticket owns live claim coverage state. Freeform status values weaken
grep-friendly acceptance review and mix repair narration into the coverage status
field.

Follow-up:

Use claim-matrix status values such as `supported_pending_review`, `open`,
`challenged`, and `supported`; keep repair narration in execution notes, critique
disposition, or evidence prose.

Challenges:

- `ticket:planwv11#ACC-005`

## PLANWV11-RCRIT-002: Repair packet repeats stale lifecycle wording pattern

Severity: low
Confidence: high
State: open

Observation:

The repair packet frontmatter says `status: consumed`, but its body still says
the lifecycle status was left `compiled` for parent reconciliation without saying
the parent later marked it consumed.

Why it matters:

This recreates the lifecycle ambiguity addressed by the first critique, now in
the repair packet.

Follow-up:

Mirror the first packet wording: the child initially left packet lifecycle status
as `compiled`; the parent later marked frontmatter `status: consumed` during
reconciliation.

Challenges:

- `ticket:planwv11#ACC-004`

# Prior Finding Disposition

- `PLANWV11-CRIT-001`: resolved.
- `PLANWV11-CRIT-002`: resolved.
- `PLANWV11-CRIT-003`: resolved.
- `PLANWV11-CRIT-004`: resolved for iteration 1; analogous lifecycle wording in
  iteration 2 is tracked as `PLANWV11-RCRIT-002`.

# Evidence Reviewed

- `.loom/tickets/20260502-planwv11-improve-plan-coverage-wave-checks.md`
- `.loom/critique/plan-wave-coverage-review.md`
- `.loom/evidence/20260502-plan-wave-coverage-validation.md`
- `.loom/packets/ralph/20260502T210325Z-ticket-planwv11-iter-01.md`
- `.loom/packets/ralph/20260502T211053Z-ticket-planwv11-iter-02.md`
- `skills/loom-plans/templates/plan.md`
- `skills/loom-plans/references/plan-shape.md`
- Ralph/Git parallel guidance and route/status/claim-coverage references
- `git diff --check cb69ab9efdefbe4dabb9c86f34048687a0c8930e` - no output

# Residual Risks

Validation remains structural and does not prove future plans will fill in wave
checks correctly.

# Required Follow-up

Resolve both findings and run mandatory oracle re-critique before acceptance.

# Acceptance Recommendation

Active follow-up required.
