# Candidate: Record-Backed Authority Progress

Candidate ID: `candidate-record-backed-authority-progress-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: discarded

## Target Behavior

The agent should not ask the user to re-ratify semantic values that active,
current records already establish. Anti-assumption discipline should block
unratified semantics, not settled project memory.

## Proposed Instruction Overlay

Add this rule near the Assumption Provenance section:

```text
Record-backed authority is progress, not a blocker. When active current records
explicitly establish a semantic value, there is no conflict or staleness marker,
and the user asks to proceed within that contract, cite the governing records
and use the value. Do not ask the user to re-ratify what the record graph
already owns.

If all execution-critical assumptions are record-backed or user-ratified, move
to the appropriate executable ticket path. Ask only when records conflict, are
stale, are merely examples/draft notes, or leave a semantic value unstated.
```

## Expected Score Movement

- S003 Ticket Readiness: should improve if current overblocks record-backed
  values after recent provenance gates.
- S007 Human Shaping Quality: should improve by distinguishing settled memory
  from unresolved ambiguity.
- S002 Record Quality: should improve by citing active records instead of
  duplicating or re-asking settled context.

## Scenario Coverage

Primary scenario:

- SCN-006 ticket-boundary with active Kappa greenline records that ratify
  display-only behavior, `readinessScore`, and threshold `85`.

Secondary scenarios:

- SCN-003 existing-records-answer-the-question.
- SCN-004 record-routing.

## Expected Failure Modes

- Treating stale, draft, or conflicting records as authoritative.
- Implementing without citing or loading the active records.
- Creating a broad "records always authorize work" escape hatch.

## Promotion Boundary

Promote only if current overblocks or asks for user re-ratification despite
active records explicitly owning the semantic values, and candidate proceeds
with a bounded executable ticket while preserving evidence/record discipline.
Discard if current already behaves correctly or if candidate treats stale/draft
records as authority.

## Result

`EXP-20260623-838-record-backed-authority-scn006-live-micro` discarded this
candidate. Current and candidate both scored `S003=100` and both manually passed
the positive-control behavior: they used active records as authority for
`KappaReleaseRow.readinessScore >= 85`, avoided user re-ratification, opened an
executable ticket, and did not edit implementation files. Current also recorded
inspection evidence, so there was no candidate-over-current behavior worth
promoting.
