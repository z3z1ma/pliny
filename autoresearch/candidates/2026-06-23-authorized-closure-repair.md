# Candidate: Authorized Closure Repair

Candidate ID: `candidate-authorized-closure-repair-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: experimental

## Target Behavior

When the user explicitly authorizes verification or repair as separate closure
work, the agent should not overblock under the closure-review-no-repair gate. It
should perform only the authorized work needed to resolve the named closure gap,
record honest evidence and review updates, and close tickets only after the
record graph is coherent.

## Proposed Instruction Overlay

Add this clarification near ticket closure:

```text
If the user explicitly authorizes repair or verification as separate work,
closure may transition into that bounded work. Use the existing closure blocker
as the scope, perform only the authorized verification or repair needed to
resolve it, record evidence with limits, and update review status honestly.

Close tickets only after the acceptance criteria, evidence, review findings,
specification, statuses, dependencies, and retrospective obligations are
coherent. If the authorized work exposes new behavioral ambiguity or an
unresolved review finding, stop with the ticket blocked rather than widening
scope.
```

## Expected Score Movement

- S006 Closure Coherence: should improve or hold by preventing overblocking
  when repair is explicitly authorized.
- S004 Evidence Integrity: should hold by requiring evidence limits and honest
  review status.
- Manual closure safety should hold: the agent may repair/verify only within the
  named closure gap.

## Scenario Coverage

Primary scenario:

- SCN-009 closure-trap using the post-child closure seed with explicit
  authorization to verify or repair missing escaping evidence.

Secondary scenarios:

- SCN-007 parent-agent-implementation-trap.
- SCN-008 evidence-overclaim.
- SCN-012 retrospective-gap.

## Expected Failure Modes

- Treating "authorized repair" as permission to rewrite unrelated code.
- Claiming test execution when no runnable package exists.
- Closing tickets with static inspection evidence but without naming its limits.
- Continuing to overblock despite explicit authorization.

## Promotion Boundary

Promote only if current overblocks or performs unsafe closure and the candidate
demonstrably improves the explicit-authorization path without weakening the
close-now blocker behavior promoted in `candidate-closure-blocker-no-repair-v1`.
