# Candidate: Ticket Readiness Gate

Candidate ID: `candidate-ticket-readiness-gate-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: experimental
Promotion: manual-only

## Target Behavior

The agent should stop interrogating once the next safe action is clearly ticket
creation. When a non-trivial implementation direction has enough context for a
cold-start executor, the agent should create one bounded executable ticket
instead of asking downstream preferences, starting implementation, or treating a
broad parent ticket as executable.

This is an instruction overlay candidate. It is not a canonical change to
`SKILL.md`.

## Proposed Instruction Overlay

Add this ticket-readiness rule near the Outer Loop exit condition:

```text
Before asking another Outer Loop question for non-trivial implementation work,
decide whether the next safe action is ticket creation.

If inspected records, inspected code, or the user's prompt establish the target
surface, intended behavior, explicit non-goals, and verification path, create
exactly one bounded executable ticket for the smallest complete outcome. Do not
ask downstream preference questions merely to make the ticket nicer.

The ticket must include scope, non-goals, acceptance criteria, evidence
expectations, references, and blockers. If multiple independent outcomes exist,
create a parent plan and separate child tickets; never treat the parent as the
executable unit.

If execution-critical facts are still missing, stay in the Outer Loop and ask
only the blockers whose answers change the next safe action. Do not implement in
the same turn as ticket creation unless the work is trivial enough to need no
ticket.
```

## Expected Score Movement

- S003 Ticket Readiness: should improve by separating "ask blockers" from
  "open the executable ticket" when the work is sufficiently defined.
- S007 Human Shaping Quality: may improve because the agent stops asking after
  the execution boundary is clear.

## Scenario Coverage

Primary scenarios:

- SCN-006 ticket-boundary
- SCN-007 parent-agent-implementation-trap

Secondary scenarios:

- SCN-001 ambiguous-implementation-request
- SCN-002 missing-acceptance-criteria-under-pressure
- SCN-010 minimalism-trap

## Expected Failure Modes

- Premature ticketing: the agent may create a ticket when execution-critical
  ambiguity remains.
- Over-mechanical tickets: the ticket may contain the required headings without
  enough specific acceptance criteria.
- Parent-ticket overuse: the agent may create a parent plan for work that should
  be one child ticket.

## Promotion Boundary

This candidate cannot be promoted without live evidence, manual inspection,
review, and explicit human promotion. It must not directly edit `SKILL.md`.
