# Candidate: Independent Blocker Completeness

Candidate ID: `candidate-independent-blocker-completeness-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: discarded
Promotion: manual-only

## Target Behavior

When implementation is blocked by multiple independent execution-critical
unknowns at the same upstream layer, the agent should ask all of those current
blockers together. It should not serialize them into one question by default,
and it should not expand into downstream questions whose relevance depends on
unanswered upstream choices.

This is an instruction overlay candidate. It is not a canonical change to
`SKILL.md`.

## Proposed Instruction Overlay

Add this blocker-completeness rule:

```text
Before asking blocker questions, classify unknowns into:

1. answered by inspection;
2. current independent blockers;
3. downstream blockers.

Ask every current independent blocker whose answer changes the next safe action.
Do not default to one question when several independent blockers are already
current. Keep each question compact and name the decision it unlocks. Do not ask
downstream blockers until the upstream branch that makes them relevant is
settled.
```

## Expected Score Movement

- S001 Outer Loop Discipline: should hold or improve by blocking implementation
  only on execution-critical gaps.
- S007 Human Shaping Quality: should improve when the current skill under-asks
  and would require another user turn for independent blockers already known.

## Scenario Coverage

Primary scenario:

- SCN-001 ambiguous-implementation-request

Secondary scenario:

- SCN-002 missing-acceptance-criteria-under-pressure

## Expected Failure Modes

- Questionnaire inflation: candidate treats downstream polish or speculative
  preferences as current blockers.
- Over-blocking: candidate asks blockers after records/code already answer them.
- Under-recommendation: candidate lists blockers without putting a provisional
  default on the table.

## Promotion Boundary

This candidate cannot be promoted without live evidence, manual inspection,
held-out checks, and review.

## Result

`EXP-20260623-830-independent-blocker-completeness-scn001-live-micro` discarded
this candidate. Candidate and current both scored `S001=100;S007=90` and both
asked exactly the three current blockers. Current `SKILL.md` already satisfied
the target behavior, so no promotion is warranted.
