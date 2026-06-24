# Candidate: Ticket Assumption Ledger

Candidate ID: `candidate-ticket-assumption-ledger-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: active
Promotion: manual-only

## Target Behavior

When an executable ticket contains high-impact semantics or mixes provenance
sources, the ticket should make assumption ownership visible to the cold-start
executor. The agent already must classify behavioral claims before ticket
creation; this candidate tests whether that classification should be present in
the ticket rather than remaining private to the current agent.

## Proposed Instruction Overlay

Add near ticket readiness:

```text
When an executable ticket includes high-impact semantics or combines behavior
from inspected records, source-observed facts, and current user ratification,
include a compact assumption provenance section. Classify execution-relevant
claims as record-backed, user-ratified, or blocked. The section is not required
for trivial tickets with a single obvious provenance source.

No unresolved assumption may appear in an executable ticket if it could change
implementation or acceptance. If a blocked item remains, the ticket is a shaping
or blocked ticket, not executable.
```

## Expected Score Movement

- S003 Ticket Readiness should improve because executable tickets become safer
  for cold-start subagents.
- S006 Closure Coherence may improve later because evidence can map acceptance
  criteria back to the authority that made them valid.

## Scenario Coverage

Primary scenario:

- SCN-006: create an executable ticket from mixed provenance: active spec,
  active decision, source state, and a current user-ratified column.

Secondary scenarios:

- SCN-007: parent/child handoff quality.
- SCN-009: closure evidence mapping.

## Expected Failure Modes

- Boilerplate: candidate adds a ledger to trivial tickets where provenance is
  obvious.
- False certainty: candidate labels source-observed fields as record-backed
  product semantics.
- Overblocking: candidate refuses ticket creation even though records and the
  prompt fully settle the implementation contract.

## Promotion Boundary

Promote only if current creates an executable ticket that is otherwise
reasonable but leaves the mixed provenance implicit, while candidate creates a
bounded executable ticket with a compact, accurate provenance ledger and no
unresolved assumptions.
