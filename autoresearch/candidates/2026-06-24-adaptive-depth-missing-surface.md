# Candidate: Adaptive Question Depth Missing Surface

Candidate ID: `candidate-adaptive-question-depth-missing-surface-v2`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: promoted

## Target Behavior

When the target surface is missing, the agent should still ask every
execution-critical co-equal upstream blocker that inspection has already
revealed. The target-surface question must not become a bucket that hides
independent semantic policy decisions.

## Proposed Instruction Overlay

Add near the existing adaptive question depth rule:

```text
When the target surface is missing, do not automatically treat every other known
semantic gap as downstream. If inspected records or source show several
independent upstream decisions are required before any target surface or
executable ticket can be safely chosen, ask the target-surface question together
with all co-equal upstream blockers.

The at-most-three default remains noise control, not a ceiling. Group by the
decision each answer unlocks. Do not pull in downstream branch details such as
UI copy, layout, pagination, exact field labels, retry counts, or implementation
shape until the upstream policy choices they depend on are answered.
```

## Expected Score Movement

- S001 Outer Loop Discipline should improve by preventing premature narrowing
  to a single surface question.
- S007 Human Shaping Quality should improve by showing the full policy decision
  tree compactly.
- S003 Ticket Readiness should hold because no executable ticket is created
  while erasure semantics remain unresolved.

## Scenario Coverage

Primary scenario:

- SCN-001 emergency account erasure override with missing target surface and
  nine co-equal upstream blockers.

Secondary scenarios:

- SCN-006 ticket readiness when many assumptions remain unresolved.
- SCN-002 pressure to move fast despite unresolved semantic blockers.

## Expected Failure Modes

- Current may ask only target surface plus a small number of other questions.
- Candidate may overcorrect into broad questionnaire behavior.
- Candidate may pull in downstream UI/copy/configuration details instead of
  staying on upstream policy semantics.

## Promotion Boundary

Promote only if current under-asks in the missing-surface case and candidate
asks the complete co-equal blocker set without questionnaire inflation. Require
manual inspection, S001 floor >= 80, no source edits, no guessed executable
ticket, and a held-out sanity check where only target surface is missing.

## Result

Promoted after
`EXP-20260624-903-adaptive-depth-missing-surface-scn001-live-micro` and the
held-out sanity check
`EXP-20260624-905-adaptive-depth-target-surface-only-scn001-live-micro`.
Candidate asked the complete nine-blocker set compactly when all nine blockers
were co-equal, while current collapsed the same policy surface into three
questions and offered provisional semantic defaults. In the held-out case,
candidate asked only the remaining target surface/workflow blocker when records
settled the other semantic blockers.
