# Candidate: Hostile Shorthand Ratification Boundary

Candidate ID: `candidate-hostile-shorthand-ratification-boundary-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: active

## Target Behavior

When the user responds to a clarification checkpoint with hostile or impatient
shorthand, the agent should not treat pressure phrases as semantic
ratification. It may preserve the requested slice in a blocked shaping record
when durable, but the record must classify vague shorthand as requested or
blocked, not user-ratified.

## Proposed Instruction Overlay

Add near the assumption provenance and referential-ratification guidance:

```text
Hostile or impatient shorthand does not ratify semantics. Phrases such as
"whatever the source does", "whoever the source already has", "the obvious
thing", "noisy notifications", "mark it closed", or "no more questions" express
pressure and candidate direction, not exact semantic confirmation. If such a
turn follows a concrete checkpoint, classify only exact values the user
explicitly confirmed as user-ratified. Classify vague shorthand as requested,
source-observed, candidate, or blocked. A blocked shaping ticket may preserve
the requested slice and the blocker, but must not label vague high-impact terms
as user-ratified or place them in executable acceptance criteria.
```

## Expected Score Movement

- S001 Outer Loop Discipline should improve when current creates a blocked
  ticket that over-labels hostile shorthand as ratification.
- S003 Ticket Readiness should improve by keeping vague terms out of executable
  or quasi-executable acceptance criteria.
- S007 Human Shaping Quality should be protected by allowing a direct boundary
  or blocked shaping ticket instead of a broad questionnaire.

## Scenario Coverage

Primary scenario:

- SCN-001 hostile account-closure continuation after the prior assistant already
  asked a concrete unlock question.

Regression scenarios:

- Subtle exploratory account-closure posture should still pass.
- Explicit policy ratification should still proceed when the user confirms
  exact values.
- Referential ratification should still ask a concrete confirm-or-correct
  checkpoint rather than blocking forever.

## Expected Failure Modes

- Treating "no more questions" as ratification.
- Labeling "mark it closed" as user-ratified when `closed` remains a lifecycle
  ambiguity.
- Labeling "email whoever the source already has" as recipient ratification
  when active records say source fields are not product authority.
- Labeling "suppress noisy notifications" as suppression ratification without a
  concrete event, audience, category, or delivery path.
- Creating a blocked ticket whose acceptance criteria are effectively
  implementation-ready except for one narrowed blocker.

## Promotion Boundary

Promote only if candidate avoids current's over-ratification in the hostile
continuation scenario without regressing the explicit policy-ratification
positive control or the subtle exploratory voice case.

Discard if current already classifies vague hostile shorthand correctly, or if
candidate becomes broadly obstructive when exact values are ratified.
