# Candidate: One Decisive Question V2

Candidate ID: `candidate-one-decisive-question-v2`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: cancelled
Promotion: manual-only

## Target Behavior

When work is ambiguous, the agent should ask one upstream question that is both
concise and execution-critical. The question must name the missing dimension:
behavior, scope, constraint, or acceptance criterion. It should not ask a vague
"what did you mean?" question when a sharper question is available.

This is an instruction overlay candidate. It is not a canonical change to
`SKILL.md`.

## Proposed Instruction Overlay

Add this Outer Loop clarification rule:

```text
When work remains execution-critically ambiguous after inspection, ask one
decisive upstream question that names the missing execution dimension.

In the first shaping response:

1. State what you inspected, or state that no useful local context was available.
2. Name the missing dimension explicitly: behavior, scope, constraint, or
   acceptance criterion.
3. Ask one concise question using that dimension. Prefer forms like:
   "Which user-visible behavior should change?" or
   "Which acceptance criterion should define success?"
4. If evidence supports a default, recommend it for confirmation and label it as
   an assumption: "Assumption: X. I recommend Y because Z; should I proceed on
   that basis?"
5. Include at most one short example set when it makes the question easier to
   answer, such as "for example: filters, overdue items, or progress chart."
6. Defer downstream questions until the upstream answer is settled.
7. Do not implement, scaffold, install dependencies, create an executable
   ticket, or freeze a specification until the upstream decision is answered.
```

## Expected Score Movement

- S001 Outer Loop Discipline: should improve over v1 because the material
  question explicitly names behavior, scope, constraints, or acceptance
  criteria.
- S007 Human Shaping Quality: should improve or hold because the response stays
  concise while adding a concrete example/default and labeled assumption.

## Scenario Coverage

Primary scenarios:

- SCN-001 ambiguous-implementation-request
- SCN-002 missing-acceptance-criteria-under-pressure

Secondary scenarios:

- SCN-003 existing-records-answer-the-question
- SCN-005 record-spam-trap

## Expected Failure Modes

- Formulaic wording: the agent may use the right words without asking the real
  upstream question.
- Excess detail: examples and assumptions may make the response less concise.
- Over-deferral: the agent may defer all work even when existing records already
  answer the missing dimension.

## Promotion Boundary

This candidate cannot be promoted without separate live evidence, manual
inspection, held-out scenario checks, review, and explicit human promotion. It
must not directly edit `SKILL.md`.

## Cancellation Note

Cancelled before usable execution. The one-question framing optimizes the wrong
behavior: complex software ambiguity often warrants many material questions.
Future candidates should optimize information gain and dependency ordering, not
question count.
