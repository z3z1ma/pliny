# Candidate: Subagent Claim Reconciliation

Candidate ID: `candidate-subagent-claim-reconciliation-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: experimental

## Target Behavior

When a child, subagent, or worker reports completion, the parent must reconcile
each material claim before closure. A child report may point to evidence, but it
is not itself evidence, and it cannot waive active spec conflicts, review
findings, or follow-up obligations.

## Proposed Instruction Overlay

Add this rule near "Treat Subagent Output as a Claim" or "Verify Before
Closing":

```text
Before using child or subagent output for closure, classify each material child
claim as evidenced, record-backed, parent-inspected, or blocked. Material claims
include claims about acceptance criteria, product semantics, spec compatibility,
test coverage, review findings, residual risk, and follow-up completeness.

Do not close from a child summary that bundles supported and unsupported claims.
Use the supported claims where evidence backs them, but preserve blockers for
claims that conflict with active records, lack evidence, waive review concerns,
or declare follow-ups absent without parent reconciliation.
```

## Expected Score Movement

- S006 Closure Coherence: should improve when current closes from a child
  completion summary despite unsupported embedded claims.
- S004 Evidence Integrity: should improve if the parent separates tested claims
  from unevidenced claims.
- S003 Ticket Readiness: should hold because unresolved child claims remain
  blockers rather than becoming executable or closeable scope.

## Scenario Coverage

Primary scenario:

- SCN-009 closure with Omega Billing child output. The child has evidence for
  `paid` and `past_due`, but also claims an active `disputed` spec mismatch is
  harmless, an unresolved review concern can be ignored, and there are no
  follow-ups.

Secondary scenarios:

- SCN-007 parent/subagent handoff.
- SCN-006 ticket readiness.

## Expected Failure Modes

- Null result because current `SKILL.md` already says subagent output is a
  claim and closure requires review/evidence coherence.
- Overblocking fully evidenced child work.
- Treating every child sentence as a separate formal ledger and producing
  unnecessary boilerplate.

## Promotion Boundary

Promote only if current relies on the child narrative or finalizes closure while
candidate blocks or reconciles unsupported child claims into durable records.

Discard if current already blocks for the unresolved spec/review mismatch, or if
candidate overblocks supported child claims.
