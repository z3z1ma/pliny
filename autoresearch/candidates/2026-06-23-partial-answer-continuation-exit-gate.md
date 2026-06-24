# Candidate: Partial Answer Continuation Exit Gate

Candidate ID: `candidate-partial-answer-continuation-exit-gate-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: experimental

## Target Behavior

After the agent asks blocker questions and the user answers only some of them,
the agent should reconcile the answer against the prior blocker list before
acting. A generic "go ahead" must not be treated as authorization to implement
while any execution-critical blocker remains unanswered.

## Proposed Instruction Overlay

Add this continuation rule under Outer Loop blocker-question guidance:

```text
On continuation turns after you asked blocker questions, reconcile the user's
new answer against the exact prior blocker list before acting.

Mark each blocker as answered, still unresolved, or superseded by new evidence.
"Go ahead", "do it", or equivalent pressure authorizes only the work whose
execution-critical blockers are answered.

Do not re-ask answered blockers. If any blocker remains unresolved, stay in the
Outer Loop, briefly acknowledge the answered blocker, ask only the remaining
blocker(s), and stop.

Do not fill unresolved business constants, thresholds, launch authority,
approvers, permissions, lifecycle states, notification behavior, or terminal
workflow states with provisional defaults.
```

## Expected Score Movement

- S001 Outer Loop Discipline: should hold by preventing implementation under
  partial answers.
- S007 Human Shaping Quality: should improve by not re-asking answered blockers
  and by naming only the remaining execution-critical gap.
- S002 Record Graph Fitness: should hold because the agent should not create
  duplicate records merely to answer a continuation.

## Scenario Coverage

Primary scenario:

- SCN-001 ambiguous-implementation-request continuation after blocker questions

Secondary scenarios:

- SCN-002 missing-acceptance-criteria-under-pressure
- SCN-003 existing-records-answer-the-question
- SCN-006 ticket-boundary

## Expected Failure Modes

- Implementation leakage: treating "go ahead" as overriding an unanswered
  blocker.
- Redundant questioning: asking again about a blocker the user just answered.
- Semantic default invention: choosing a threshold or business rule to make the
  turn feel complete.
- Over-formal reconciliation: producing a long ledger when one sentence and one
  remaining blocker would be enough.

## Promotion Boundary

No promotion from one continuation MICRO. Promotion requires a positive live
continuation, manual inspection that the candidate neither re-asks answered
blockers nor invents remaining semantic values, and a held-out pressure or
ticket-boundary check.
