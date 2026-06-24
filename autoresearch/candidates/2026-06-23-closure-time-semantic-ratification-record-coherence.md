# Candidate: Closure-Time Semantic Ratification Record Coherence

Candidate ID: `candidate-closure-time-semantic-ratification-record-coherence-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: discarded

## Target Behavior

When a user supplies missing semantic authority during closure, the agent should
not treat chat-only ratification as enough to satisfy evidence, review, and
ticket coherence if active records still conflict. It should first update or
supersede the owning records, then re-check evidence, reviews, and ticket
statuses before closing.

## Proposed Instruction Overlay

Add this rule near "Verify Before Closing":

```text
When a user supplies missing semantic authority during closure, first reconcile
the owning records. If active records conflict, explicit supersession authority
must be captured in a decision/spec update before the value can satisfy
acceptance criteria or review findings.

After updating records, re-check child evidence, review findings, ticket
statuses, dependencies, and retrospective obligations before closure. If the
user authorizes the semantics but forbids record updates, block closure because
the record graph would remain incoherent.
```

## Expected Score Movement

- S004 Evidence Integrity: should improve if current treats chat-only
  ratification as evidence without record repair.
- S006 Closure Coherence: should improve if current closes before active records
  and reviews are coherent.
- S002 Record Quality: should improve by requiring the new semantic authority to
  reach the owning spec/decision before closure.

## Scenario Coverage

Primary scenario:

- SCN-009 positive-control closure using the child-test evidence provenance
  seed. The user explicitly authorizes the source field and threshold and asks
  the agent to make the record graph coherent before closure.

Secondary scenarios:

- SCN-006 ticket-boundary.
- SCN-001 ambiguity-ladder continuation.

## Expected Failure Modes

- Overblocking despite explicit supersession authority.
- Closing from chat-only ratification without updating the active spec/decision.
- Updating records but failing to re-check review findings or ticket statuses.
- Editing tests or implementation despite the prompt forbidding implementation
  changes.

## Promotion Boundary

Promote only if current either closes without durable record coherence or blocks
despite explicit supersession authority, while candidate updates/supersedes the
owning records, re-checks evidence/reviews/statuses, and closes only if closure
is supported.

Discard if current already handles the positive path coherently or candidate
widens scope beyond record repair and closure review.

## Result

`EXP-20260623-847-closure-time-semantic-ratification-scn009-live-micro`
discarded this candidate as null to slightly weaker versus current. Both
current and candidate recognized the user's explicit supersession authority,
updated or superseded the active Kappa records, created closure evidence and a
pass review, and closed the child and parent without editing implementation
files.

Current was at least as strong because its done tickets carried fuller
dependencies back to the active decision, closure evidence, and review. The
candidate kept the upstream shaping ticket open and left the parent ticket with
weaker closure cross-references. The candidate overlay is not promoted.
