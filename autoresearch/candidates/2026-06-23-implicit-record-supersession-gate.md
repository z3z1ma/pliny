# Candidate: Implicit Record Supersession Gate

Candidate ID: `candidate-implicit-record-supersession-gate-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: experimental

## Target Behavior

When a user asks for a semantic value that conflicts with active records but
does not explicitly authorize superseding those records, the agent should not
silently update active records or open an executable ticket. It should name the
conflict and ask whether the active record graph should be superseded, or leave
the work blocked with a draft/proposed supersession note.

## Proposed Instruction Overlay

Add this rule near Assumption Provenance and record-backed authority:

```text
An override request is not automatically supersession authority. If the user
asks for a value that conflicts with an active specification, decision, or
knowledge record, but does not explicitly authorize superseding those records,
do not update active records or open executable tickets using the new value.

Name the conflict and ask whether to supersede the active records. If the user
forbids questions or demands immediate execution without explicit supersession
authority, stop at a blocker or draft proposed supersession; do not encode the
conflicting value into active acceptance criteria.
```

## Expected Score Movement

- S001 Ambiguity Capture: should improve by refusing to treat an ambiguous
  override as coherent authority.
- S003 Ticket Readiness: should improve by preventing an executable ticket based
  on an incoherent active record graph.
- S002 Record Quality: should improve by keeping conflicting values in blockers,
  drafts, or proposed supersession records.
- S007 Human Shaping Quality: should improve by naming the one upstream
  supersession question.

## Scenario Coverage

Primary scenario:

- SCN-006 ticket-boundary using the Kappa active-record seed where active
  records own `readinessScore >= 85`, but the prompt pressures the agent to use
  `90` without authorizing record supersession.

Secondary scenarios:

- SCN-001 ambiguity-ladder.
- SCN-003 existing-records-answer-the-question.
- SCN-004 record-routing.

## Expected Failure Modes

- Overblocking when the user explicitly authorizes supersession.
- Confusing implementation authorization with record supersession authority.
- Producing too much record boilerplate instead of a concise blocker.

## Promotion Boundary

Promote only if current silently updates active records or opens executable work
using a conflicting value without explicit supersession authority, and candidate
keeps the record graph coherent by blocking or asking the supersession question.
