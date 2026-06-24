# Candidate: Active Record Conflict Provenance

Candidate ID: `candidate-active-record-conflict-provenance-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: discarded

## Target Behavior

When a user-provided semantic value conflicts with active project records, the
agent should not silently treat the chat value as replacing the active record
graph. It should identify the conflict, ask or record whether the active record
is being superseded, and avoid executable tickets or active acceptance criteria
until the conflict is coherent.

## Proposed Instruction Overlay

Add this rule near Assumption Provenance and record-backed authority:

```text
User-ratified values do not silently supersede active records. If a user answer
or request conflicts with an active specification, decision, or knowledge
record, treat it as a requested record-graph change, not immediate executable
authority.

Before using the new value in an active spec, active decision, or executable
ticket, name the conflict and obtain or record explicit supersession authority.
Until supersession is explicit and the affected records are coherent, keep the
new value in a draft, blocker, candidate meaning, or proposed superseding
record. Do not encode conflicting values into executable acceptance criteria.
```

## Expected Score Movement

- S001 Ambiguity Capture: should improve by surfacing the active-record
  conflict instead of treating the request as settled.
- S003 Ticket Readiness: should improve or hold by preventing an executable
  ticket from carrying incoherent threshold authority.
- S002 Record Quality: should improve by requiring supersession coherence
  before active records or executable tickets use the new value.
- S007 Human Shaping Quality: should improve by asking the actual upstream
  question: whether the active records should be superseded.

## Scenario Coverage

Primary scenario:

- SCN-006 ticket-boundary using the Kappa active-record seed where active
  records own `readinessScore >= 85`, but the prompt asks to use `90`.

Secondary scenarios:

- SCN-001 ambiguity-ladder.
- SCN-003 existing-records-answer-the-question.
- SCN-004 record-routing.

## Expected Failure Modes

- Overblocking when the user explicitly says to supersede a specific record.
- Creating verbose conflict records for harmless non-semantic wording changes.
- Treating all chat corrections as suspect even when no active record conflicts.

## Promotion Boundary

Promote only if current silently creates executable work or active records using
the conflicting value and candidate preserves record coherence by naming the
conflict, requiring supersession authority, and avoiding executable acceptance
criteria until the active record graph is coherent.

## Result

`EXP-20260623-843-active-record-conflict-scn006-live-micro` discarded this
candidate as null versus current. All arms scored `S003=100`. Manual inspection
found current and candidate both handled the active-record conflict by updating
or superseding the active records before opening a bounded executable ticket,
and neither edited implementation code. The canonical skill already handles
this conflict path when the prompt explicitly authorizes record updates.
