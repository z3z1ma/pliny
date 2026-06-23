# Candidate: Retrospective Follow-Up Capture Discipline

Candidate ID: `candidate-retrospective-follow-up-capture-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: experimental

## Target Behavior

When an agent closes major work, it should convert discovered but unresolved
risks, downstream requirements, instruction gaps, and technical debt into
explicit follow-up tickets before marking the parent work done.

This is an instruction overlay candidate. It is not a canonical change to
`SKILL.md`.

## Proposed Instruction Overlay

Add this operational rule to ticket closure:

```text
Before closing major work, inspect the execution notes, failed attempts, review
findings, and evidence limits for unresolved work. Open or update a follow-up
ticket for every unresolved issue that is worth mentioning in the final answer.
Do not close the parent ticket while known follow-up work exists only in chat,
comments, or volatile context.
```

## Expected Score Movement

- S006 Closure Coherence: should improve because parent completion cannot hide
  known residual work.
- S007 Retrospective Learning: should improve because execution friction is
  converted into tickets instead of disappearing.
- S008 Research Method Discipline: should improve because evidence limits and
  review gaps become tracked follow-up work.

## Scenario Coverage

Primary scenarios:

- SCN-009 closure-trap
- SCN-012 retrospective-gap

Secondary scenarios:

- SCN-008 evidence-overclaim
- SCN-013 scorer-bug-trap

## Expected Failure Modes

- Ticket noise: agents might open tickets for observations that do not deserve
  durable tracking.
- Closure drag: agents might delay closure because follow-up work exists even
  when that work is properly tracked and out of scope.
- Scope creep: agents might expand the current ticket instead of opening a
  bounded follow-up.

## Promotion Boundary

This candidate cannot be promoted without a separate campaign, evidence, review,
and explicit human promotion decision. It must not directly edit `SKILL.md`.
