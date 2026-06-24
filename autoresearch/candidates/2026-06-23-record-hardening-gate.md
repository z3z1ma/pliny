# Candidate: Record Hardening Gate

Candidate ID: `candidate-record-hardening-gate-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: experimental

## Target Behavior

The agent should not launder unratified semantics into durable authority. A
record can preserve an unresolved semantic value as a blocker, candidate
meaning, or draft note, but it must not convert that value into active spec
behavior, an active decision, or executable-ticket acceptance criteria.

## Proposed Instruction Overlay

Add this rule near the record-shape and ticket-readiness guidance:

```text
Record hardening does not ratify semantics. Before marking a specification
active, writing an active decision, or opening an executable ticket, classify
each behavioral claim and acceptance criterion as record-backed, user-ratified,
or blocked.

If a semantic value is unratified, record it only as an unresolved blocker,
candidate meaning, or draft note. Do not place it in active spec behavior,
active decisions, or executable-ticket acceptance criteria.

A shaping ticket may preserve the request, answered branches, and blockers. An
executable ticket may not encode guessed thresholds, source fields, lifecycle
effects, permissions, notifications, approvers, failure behavior, or product
acceptance criteria.
```

## Expected Score Movement

- S003 Ticket Readiness: should improve manually by preventing executable
  tickets whose apparent readiness comes from guessed semantics.
- S007 Human Shaping Quality: should improve manually by explaining the record
  status boundary clearly.
- S002 Record Quality: should improve manually by preventing active records
  from laundering unresolved semantics.

## Scenario Coverage

Primary scenario:

- SCN-006 ticket-boundary.

Secondary scenarios:

- SCN-001 ambiguous-implementation-request.
- SCN-004 record-routing.

## Expected Failure Modes

- Overblocking harmless draft-record updates.
- Avoiding records entirely despite durable context crystallizing.
- Treating all active spec edits as forbidden, even when the behavior is
  record-backed or user-ratified.

## Promotion Boundary

No promotion from one MICRO unless current creates active/executable authority
from unratified semantics and candidate preserves those semantics only as
blockers or draft notes. Manual inspection is authoritative because S003 can
reward concrete-looking tickets even when they are semantically invented.
