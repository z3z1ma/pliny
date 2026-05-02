---
id: critique:plan-wave-coverage-review
kind: critique
status: final
created_at: 2026-05-02T21:10:53Z
updated_at: 2026-05-02T21:10:53Z
scope:
  kind: repository
  repositories:
    - repo:root
review_target: "ticket:planwv11 diff cb69ab9..working-tree"
links:
  ticket:
    - ticket:planwv11
  evidence:
    - evidence:plan-wave-coverage-validation
  packet:
    - packet:ralph-ticket-planwv11-20260502T210325Z
external_refs: {}
---

# Summary

Reviewed the plan coverage and execution-wave guidance changes for
`ticket:planwv11`.

# Review Target

Current working-tree diff from baseline
`cb69ab9efdefbe4dabb9c86f34048687a0c8930e`, covering the ticket, evidence,
Ralph packet, and changed plan product surfaces.

# Verdict

`changes_required` - route/disposition grammar and plan wave examples need repair
before acceptance.

# Findings

## PLANWV11-CRIT-001: Ticket route and critique disposition use non-canonical values

Severity: medium
Confidence: high
State: open

Observation:

The ticket uses `Route: mandatory oracle critique` instead of canonical route
token `critique`, and `Disposition status: required_next` instead of an allowed
ticket critique disposition value such as `pending` before critique is recorded.

Why it matters:

Tickets are the live execution ledger. Non-canonical route and disposition values
weaken grep-friendly routing and acceptance-gate clarity under the
`records-grammar` profile.

Follow-up:

Change the route value to `critique` and keep mandatory oracle/profile detail in
prose. Use `pending` before the repair re-critique or a final closure-compatible
value after reconciliation.

Challenges:

- `ticket:planwv11#ACC-005`

## PLANWV11-CRIT-002: Plan wave example allows real waves to skip overlap checks

Severity: medium
Confidence: medium
State: open

Observation:

The plan template sample row for a concrete `Wave 1` says the write-scope overlap
cell may be `None - reason` or a non-overlap summary, while surrounding prose says
`None - reason` is for when no parallel wave applies.

Why it matters:

The example can be copied as allowing a real wave to skip the overlap check,
which undercuts `ticket:planwv11#ACC-002` and creates operator confusion.

Follow-up:

Make the sample row require a non-overlap summary for real waves and put
`None - reason` only in a separate no-wave example.

Challenges:

- `ticket:planwv11#ACC-002`

## PLANWV11-CRIT-003: Parent-owned launch notes is not a defined owner surface

Severity: low
Confidence: medium
State: open

Observation:

`skills/loom-plans/references/plan-shape.md` allows wave checks in "the plan or
parent-owned launch notes." Parent-owned launch notes are not a defined Loom owner
surface.

Why it matters:

Git guidance requires launched parallel setup to live in the plan, ticket
journal, or packet working notes. The current phrase could encourage shadow truth
in scratch/transcript notes.

Follow-up:

Replace with "plan, ticket journal, or packet working notes; scratch notes are
temporary before launch only."

Challenges:

- `ticket:planwv11#ACC-003`

## PLANWV11-CRIT-004: Ralph packet body has stale lifecycle wording

Severity: low
Confidence: high
State: open

Observation:

The packet frontmatter now says `status: consumed`, but child output still says
the packet lifecycle status was intentionally left `compiled`.

Why it matters:

The frontmatter is correct after parent merge, but the stale body note creates
lifecycle ambiguity.

Follow-up:

Update the body note to say the child initially left it compiled and the parent
later marked it consumed.

Challenges:

- `ticket:planwv11#ACC-004`

# Evidence Reviewed

- `.loom/tickets/20260502-planwv11-improve-plan-coverage-wave-checks.md`
- `.loom/evidence/20260502-plan-wave-coverage-validation.md`
- `.loom/packets/ralph/20260502T210325Z-ticket-planwv11-iter-01.md`
- `skills/loom-plans/templates/plan.md`
- `skills/loom-plans/references/plan-shape.md`
- Diff from baseline `cb69ab9efdefbe4dabb9c86f34048687a0c8930e`
- `git diff --check cb69ab9efdefbe4dabb9c86f34048687a0c8930e` - no output
- Ralph/Git parallel guidance
- Route and status grammar references

# Residual Risks

Evidence is structural and does not prove future plans will author wave checks
correctly. Product guidance broadly aligns with Ralph/Git parallel boundaries, but
the noted wording issues should be repaired before closure.

# Required Follow-up

Resolve all findings and run mandatory oracle re-critique before acceptance.

# Acceptance Recommendation

Active follow-up required.
