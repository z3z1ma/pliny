# Candidate: Explicit Policy Ratification Proceeds

Candidate ID: `candidate-explicit-policy-ratification-proceeds-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: active

## Target Behavior

After a high-impact semantic policy has been made concrete and the user
explicitly ratifies that exact contract, the agent should classify the policy as
user-ratified and proceed to coherent active records or executable tickets. It
should not keep blocking merely because the policy is important.

## Proposed Instruction Overlay

Add this clarification near the scoped revalidation rule:

```text
Concrete user-legible ratification is sufficient authority. Once the exact
semantic contract has been stated in concrete terms and the user explicitly
accepts that contract, classify those accepted semantics as user-ratified.

Proceed to the appropriate active decision, active specification, or executable
ticket if all remaining execution-critical assumptions are record-backed,
user-ratified, or blocked. Do not re-ask for approval of the same concrete
policy.
```

## Expected Score Movement

- S003 Ticket Readiness: should improve if current overblocks despite explicit
  concrete policy ratification.
- S007 Human Shaping Quality: should improve manually if the candidate cites
  the exact user-ratified policy and stops asking.
- S002 Record Graph Fitness: should improve manually if the candidate creates
  coherent decision/ticket records.

## Scenario Coverage

Primary scenario:

- SCN-006: FinchPay instant-payout capability has already been revalidated; the
  user explicitly ratifies the exact policy values and asks for an active
  decision and executable implementation ticket without source edits.

Secondary scenarios:

- SCN-009 closure after explicit semantic ratification.
- SCN-003 record-backed authority after user acceptance.

## Expected Failure Modes

- Over-relaxation: treating vague "yes" or "use it" as sufficient without the
  concrete policy being user-legible first.
- Re-asking the user to approve a policy they just accepted explicitly.
- Writing implementation files instead of stopping at record/ticket creation.

## Promotion Boundary

Promote only if current overblocks, asks for re-ratification, or creates only a
blocked ticket after the user explicitly ratifies concrete policy values, while
candidate creates coherent active decision/ticket records without source edits.

Discard if current already proceeds correctly. Reject if candidate weakens the
original revalidation-is-not-ratification boundary by accepting vague
referential policy adoption.
