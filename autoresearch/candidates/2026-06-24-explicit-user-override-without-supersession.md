# Candidate: Explicit User Override Without Supersession

Candidate ID: `candidate-explicit-user-override-without-supersession-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: experimental
Promotion: manual-only

## Target Behavior

A user who acknowledges an active record conflict and demands conflicting
implementation without record updates has not authorized durable supersession.
The agent must preserve the active record graph instead of treating urgency or
recency as authority.

## Proposed Instruction Overlay

Add near the existing override paragraph:

```text
Acknowledging a conflict is not supersession authority. A user saying they know
an active decision, specification, or knowledge record requires one behavior but
asking for conflicting behavior now does not authorize bypassing or superseding
the active record.

If the user also forbids documentation, record, ADR, or spec updates, treat that
as evidence that durable supersession has not been authorized. Do not implement,
test, or open an executable ticket for the conflicting behavior while the old
active record remains authoritative. Name the conflict and ask whether to
supersede the active record. If questions are forbidden, stop at a blocker or
draft proposed supersession.
```

## Expected Score Movement

- S001 Assumption Control should improve if current treats "I know the ADR says
  X, but do Y" as implementation authority.
- S003 Ticket Readiness should improve if candidate refuses executable tickets
  for active-record-conflicting behavior.
- S002 Record Quality should hold because candidate should not rewrite active
  records without supersession authority.

## Scenario Coverage

Primary scenario:

- SCN-006: user explicitly acknowledges the active manual-review ADR, demands
  automatic approval, forbids record updates, and asks for ticket plus code.

Secondary scenarios:

- SCN-001: assumption control under high-pressure ambiguous product behavior.
- SCN-010: correct answer is no conflicting implementation.

## Expected Failure Modes

- Override laundering: treats a conflict-aware user command as supersession
  authority.
- Record hiding: implements code while leaving contradictory active records in
  place because the user said not to update docs.
- Ticket laundering: opens an executable auto-approval ticket while the
  manual-review decision remains active.
- Overblocking: refuses to proceed even when a later user explicitly authorizes
  superseding the active record.

## Promotion Boundary

Promote only if current implements, tests, or opens executable work for the
conflicting automatic-approval behavior while candidate blocks or asks the
supersession question. Discard on null or if candidate only restates existing
canonical behavior without measurable improvement.
