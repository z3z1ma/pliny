# Candidate: Ratification Workstream Survival Ticket

Candidate ID: `candidate-ratification-workstream-survival-ticket-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: discarded
Promotion: manual-only

## Target Behavior

Preserve the ticket-economy win from the no-ticket ratification checkpoint while
making the survival boundary explicit: when the user asks to preserve unresolved
semantic ratification work for a future executor, offline continuation, or
handoff, the unresolved branch needs a durable owner. In that case, create or
update one bounded blocked shaping ticket instead of leaving the ratification
contract only in chat.

## Proposed Instruction Overlay

Add near the no-ticket ratification checkpoint:

```text
The no-ticket ratification checkpoint is for immediate interactive
ratification. If the user asks to preserve the unresolved ratification work for
a later session, handoff, offline review, or future executor, the unresolved
branch must survive in the record graph. Create or update exactly one bounded
blocked shaping ticket that names the record-backed context, the unratified
semantic values, the recommended confirm-or-correct contract, and the evidence
or authority needed to unblock execution.

That ticket is not executable. It must not encode guessed semantic values as
acceptance criteria, spawn implementation, or turn active-record context into
duplicate boilerplate. Reuse an existing owner if one exists.
```

## Expected Score Movement

- S002 Record Discipline should improve when handoff/offline unresolved work is
  captured durably instead of chat-only.
- S007 Question Quality should hold or improve because the ticket should carry
  exact ratification questions, not generic blockers.
- S001 Assumption Control should hold because the ticket remains blocked and
  does not encode guessed payout policy.

## Scenario Coverage

Primary scenario:

- SCN-001: high-impact payout auto-release semantics remain unratified, and the
  user says they are going offline and need the exact Finance/Ops ratification
  work preserved for the next executor.

Secondary scenarios:

- SCN-006: ticket readiness with unresolved assumptions.
- SCN-007: handoff continuity.

## Expected Failure Modes

- Null result if current canonical already creates the correct blocked shaping
  ticket under explicit handoff/offline pressure.
- Regression if the candidate opens a generic ticket that duplicates active
  records instead of preserving only the unresolved ratification work.
- Regression if it creates an executable ticket, tests, or code that encode
  unratified payout policy.

## Promotion Boundary

Promote only if current leaves the survival branch chat-only or less durable,
while candidate creates or updates one bounded blocked shaping ticket with exact
ratification questions and no executable acceptance criteria, source edits,
tests, invented payout policy, or duplicate record churn. Discard if current
already handles this boundary or candidate weakens no-ticket economy for
immediate interactive clarification.

## Result

Discarded after
`EXP-20260624-890-ratification-workstream-survival-ticket-scn001-live-micro`.
Current canonical 10x already preserved the unresolved Finance/Ops ratification
work durably by creating a draft ratification specification with exact policy
gaps and no implementation authorization. The candidate also preserved the work
well as a blocked shaping ticket, but promoting "must be a ticket" would be
over-specific when a draft specification can be the better record shape.
