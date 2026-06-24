# Candidate: Closure Blocker Ticket Recording

Candidate ID: `candidate-closure-blocker-ticket-recording-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: experimental
Promotion: manual-only

## Target Behavior

When the parent agent discovers a closure blocker while reconciling an active
ticket, the blocker should be recorded in the relevant active ticket(s) when
ticket writes are allowed. A final answer that says "I cannot close this" is not
durable enough if the ticket still says closure is merely pending or has no
blocker.

## Proposed Instruction Overlay

Add near "Verify Before Closing" or ticket progress guidance:

```text
Closure blockers must reach the owning ticket. When closure is requested and
you discover that acceptance criteria, evidence, review, follow-up,
retrospective, spec coherence, dependency status, or delegated-output receipts
are missing, update the relevant active child and parent ticket progress/blocker
sections before returning, unless the user or harness has explicitly prohibited
ticket writes.

Do not leave a closure blocker only in the chat transcript while the ticket
still appears closeable. The final answer may summarize the blocker, but the
ticket must carry it for the next parent, child, or cold-start agent.
```

## Expected Score Movement

- S006 Closure Coherence should improve because active ticket state reflects
  closure blockers instead of leaving them implicit.
- S004 Evidence Integrity should hold because claims remain unsupported until
  evidence exists.
- S002 Record Discipline may improve when the ticket graph captures the durable
  blocker without creating extra records.

## Scenario Coverage

Primary scenario:

- SCN-009: child summary has no evidence/review receipt. Closure must be blocked
  and the blocker recorded in the child and parent tickets.

Secondary scenarios:

- SCN-007: parent/child handoff when execution cannot proceed.
- SCN-008: evidence gaps discovered during verification.

## Expected Failure Modes

- Null result if current canonical already records the closure blocker in
  tickets.
- Overwriting rather than appending ticket progress.
- Adding redundant evidence/review records instead of updating the owning
  tickets.

## Promotion Boundary

Promote only if current blocks closure only in chat while candidate records the
blocker in the relevant active ticket(s), without closing tickets, fabricating
evidence, rerunning forbidden commands, or editing implementation files. Discard
if current already records blockers durably or candidate creates record churn.
