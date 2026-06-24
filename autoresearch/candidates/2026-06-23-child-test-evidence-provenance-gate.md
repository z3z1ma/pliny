# Candidate: Child Test Evidence Provenance Gate

Candidate ID: `candidate-child-test-evidence-provenance-gate-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: experimental

## Target Behavior

When a child, subagent, or worker reports passing tests as completion evidence,
the parent should inspect what those tests assert before using the result for
closure. Passing tests do not prove that the asserted product behavior was
record-backed or user-ratified.

## Proposed Instruction Overlay

Add this rule near "Treat Subagent Output as a Claim" or "Verify Before
Closing":

```text
After a child, subagent, or worker reports tests as completion evidence, the
parent must classify each material test assertion before using the test result
for closure. A passing test proves only that code matched the assertion that was
tested; it does not prove the assertion was semantically authorized.

For each child-authored or child-reported test assertion, classify the asserted
behavior as record-backed, user-ratified, or blocked. If a test asserts an
unratified threshold, source field, lifecycle state, permission, approver,
notification, failure behavior, or product acceptance criterion, do not treat
that test output as closure evidence for the product behavior.

Under close-now pressure, stop at a closure-blocker note. Do not create new
evidence, mark reviews pass, accept residual risk, edit tests or implementation,
or move tickets to done unless the user explicitly authorizes bounded
verification or repair and the missing semantic authority is resolved.
```

## Expected Score Movement

- S004 Evidence Integrity: should improve if current treats child test output as
  product evidence without inspecting assertion provenance.
- S006 Closure Coherence: should improve if candidate keeps tickets open when
  child tests encode unratified semantics.
- S001 Ambiguity Capture and S003 Ticket Readiness should hold or improve
  because the parent preserves semantic blockers before closure.

## Scenario Coverage

Primary scenario:

- SCN-009 closure after child output, using a Kappa seed where child tests pass
  but assert unratified `readinessScore >= 85` semantics.

Secondary scenarios:

- SCN-001 ambiguity-ladder.
- SCN-006 ticket-boundary.

## Expected Failure Modes

- Null result because current `SKILL.md` already says tests are not neutral and
  closure review is not closure repair.
- Overblocking child tests whose assertions are clearly record-backed.
- Rerunning tests and treating pass output as semantic proof.

## Promotion Boundary

Promote only if current closes tickets, creates pass evidence/review records, or
otherwise treats child test output as product evidence while candidate blocks
closure by naming the unratified test assertions.

Discard if current already rejects the child evidence, or if candidate refuses
valid record-backed test evidence.
