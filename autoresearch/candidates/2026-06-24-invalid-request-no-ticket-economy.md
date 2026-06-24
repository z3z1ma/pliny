# Candidate: Invalid Request No-Ticket Economy

Candidate ID: `candidate-invalid-request-no-ticket-economy-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: active

## Target Behavior

When inspected active records or source prove a requested implementation is
invalid, redundant, or already rejected, the agent should not create a blocked
ticket merely to memorialize the rejected request. It should answer from the
existing durable owner and recommend the smallest valid path.

## Proposed Instruction Overlay

Add near request-validity challenge, fish-before-opening, or ticket-opening
guidance:

```text
When inspected active records or source prove a requested implementation is
invalid, redundant, or already rejected, do not create a blocked ticket merely to
memorialize the rejected request.

Answer from the existing record owner instead: cite the active record or source,
name the conflict, and recommend the smallest valid path.

Create or update a ticket only when the current turn adds distinct durable
context or actionable work not already owned by existing records, such as an
explicit supersession request, a newly discovered defect, missing wiring, missing
documentation, or a user-approved follow-up.

A request to "open a ticket if needed" does not make a ticket needed. If no new
durable owner is required, the correct record-economy action is a no-record
answer.
```

## Expected Score Movement

- S002 Record Graph Fitness: should improve if current creates a redundant
  blocked ticket for an invalid request already owned by active records.
- S005 Minimalism: should remain high or improve by avoiding unnecessary records.
- S007 Human Shaping Quality: may improve through a cleaner answer from
  existing authority.

## Scenario Coverage

Primary scenario:

- SCN-010: active decision and knowledge reject client-side report CSV
  generation, source already exposes a server export URL helper, and the user
  asks for a planning record for a client-side CSV framework.

Secondary scenarios:

- SCN-005 fish-before-opening record-owner discipline.
- SCN-003 records-first authority.

## Expected Failure Modes

- Creating a blocked ticket solely to preserve an already-owned invalid request.
- Suppressing a real new follow-up or supersession request.
- Weakening challenge-request-validity behavior by answering without citing the
  active records/source that make the request invalid.

## Promotion Boundary

Promote only if current creates an unnecessary blocked ticket while candidate
creates no record, cites the existing active decision/source, recommends the
server-export path, and avoids source/dependency edits.

Discard if current also gives a no-record answer. Reject if candidate
under-records a real new issue, ignores the user's request, or weakens the
existing challenge-validity safety behavior.
