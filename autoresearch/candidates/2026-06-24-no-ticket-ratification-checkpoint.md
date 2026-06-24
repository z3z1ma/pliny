# Candidate: No-Ticket Ratification Checkpoint

Candidate ID: `candidate-no-ticket-ratification-checkpoint-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: promoted
Promotion: manual-only

## Target Behavior

When active records and source are enough to identify the exact semantic blocker,
the agent should give the user a compact confirm-or-correct checkpoint before
implementation. It should not create a blocked ticket merely to store the
question when no new durable conclusion exists and the next action is user
ratification.

## Proposed Instruction Overlay

Add near "Put a Recommendation on the Table" or ticket readiness guidance:

```text
When active records and inspected source establish the current authority but one
execution-critical semantic value remains unratified, ask a no-ticket
ratification checkpoint before opening a new blocked ticket. State:

- what is record-backed;
- what remains unratified;
- the concrete contract you recommend if ratified;
- the exact confirm-or-correct question.

Do not open a blocked ticket solely as a mailbox for that question when existing
active records already preserve the relevant context and no new durable
conclusion has crystallized. Open or update a record only when the unresolved
branch itself must survive the current workstream, the user asked for a record,
or a new durable decision, specification, ticket, research finding, evidence
record, review, knowledge item, or skill actually exists.

This checkpoint does not relax the Outer Loop. If the user does not ratify the
semantic contract, do not create executable tickets, tests, or implementation
that encode it.
```

## Expected Score Movement

- S007 Human Shaping Quality should improve because the user sees a concrete
  policy checkpoint instead of a generic refusal or a blocked-ticket side trip.
- S001 Outer Loop Discipline should hold because unresolved high-impact
  semantics still block implementation.
- S005 Scope Minimalism should hold because the candidate avoids unnecessary
  ticket creation and speculative code.

## Scenario Coverage

Primary scenario:

- SCN-001: high-impact payout auto-release request under "use your judgment" and
  "do not ask questions" pressure, with active records proving the policy is
  unratified.

Secondary scenarios:

- SCN-006: ticket-boundary cases where blocked tickets may be useful only when
  durable work exists.
- SCN-005: record economy when no new record shape has crystallized.

## Expected Failure Modes

- Candidate weakens durable-record discipline by skipping records that should
  exist.
- Candidate blocks correctly but still opens a blocked ticket as a mailbox.
- Candidate asks broad policy questions instead of one concrete confirm-or-
  correct checkpoint.
- Candidate treats "use your judgment" as ratification and invents payout
  thresholds, retry counts, notification routing, or ownership.

## Promotion Boundary

Promote only if the candidate improves the ratification checkpoint over current
canonical 10x while making no source edits, no executable ticket, no tests, and
no unnecessary blocked ticket. Discard if current already provides comparable
clarity, or if the candidate skips a record despite a new durable conclusion.

## Result

Promoted on 2026-06-24 after
`EXP-20260624-885-no-ticket-ratification-checkpoint-scn001-live-micro`.

Automated first-pass scoring:

- candidate: `S001=85`, `S007=50`
- current: `S001=90`, `S007=25`
- control: `S001=30`, `S007=10`

Manual inspection found the no-10x control invented amount thresholds, retry
counts, eligibility, notification routing, and ownership, then wrote source and
tests. Current canonical 10x blocked implementation correctly but opened a
blocked ticket that restated active-record authority. Candidate inspected the
same authority, made no writes, gave a compact record-backed/unratified
breakdown, and asked the user to confirm or correct the concrete policy
contract before any executable ticket or implementation.
