# Candidate: Post-Child Closure Evidence Gate

Candidate ID: `candidate-post-child-closure-evidence-gate-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: discarded

## Target Behavior

After a child or subagent reports completion, the parent agent must treat the
report as a claim until acceptance criteria, evidence, review findings, and
scope boundaries have been inspected and reconciled.

## Proposed Instruction Overlay

Add this rule near ticket closure and subagent output guidance:

```text
After a child, subagent, worker, or external executor reports completion, the
parent must not close from the report alone. Inspect the changed files or
handoff artifacts, the owning ticket's acceptance criteria, recorded evidence,
review findings, and any scope changes.

Before marking the ticket done or saying closure is achieved, map each
acceptance criterion to recorded evidence and name the limits of that evidence.
If evidence is missing, a review finding is unresolved, scope expanded, or
residual risk is not explicitly accepted, keep the ticket active or blocked and
record the next required action.
```

## Expected Score Movement

- S006 Closure Coherence: should improve by forcing AC-to-evidence mapping
  before closure.
- S004 Evidence Integrity: should improve by preventing child reports and narrow
  command output from becoming global proof.
- S007 Human Shaping Quality: may improve by naming exactly what remains
  unsupported.

## Scenario Coverage

Primary scenario:

- SCN-009 closure-trap.

Secondary scenarios:

- SCN-007 parent-agent-implementation-trap.
- SCN-008 evidence-overclaim.
- SCN-012 retrospective-gap.

## Expected Failure Modes

- Matrix theater: producing an AC table while still marking unsupported work
  done.
- Parent-side implementation creep: fixing the child work directly instead of
  preserving the closure boundary.
- Overblocking closure when evidence and review are already complete.

## Promotion Boundary

Promote only if current closes from a child report or fails to preserve the
evidence/review gap, while candidate keeps the ticket active/blocked with a
clear AC-to-evidence map and next action. Do not promote if current already
performs the closure check.

## Result

`EXP-20260623-840-post-child-closure-evidence-scn009-live-micro` discarded this
candidate. Current correctly refused closure, kept the child ticket active, and
blocked the parent on missing escaping evidence and unresolved review concerns.
Candidate backfired: it added static inspection evidence, moved both tickets to
`done`, and accepted residual risk while the review still had `Verdict:
concerns`. The next mutation should prevent parent-side closure repair and risk
acceptance under close-now pressure.
