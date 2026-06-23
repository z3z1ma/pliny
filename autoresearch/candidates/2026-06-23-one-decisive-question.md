# Candidate: One Decisive Question

Candidate ID: `candidate-one-decisive-question-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: experimental
Promotion: manual-only

## Target Behavior

When work is ambiguous, the agent should avoid both premature implementation and
questionnaire sprawl. After inspecting available context, it should ask the one
upstream question most likely to change execution, with a concrete recommended
default when evidence supports one.

This is an instruction overlay candidate. It is not a canonical change to
`SKILL.md`.

## Proposed Instruction Overlay

Add this Outer Loop clarification rule:

```text
When work remains execution-critically ambiguous after inspection, ask the next
upstream blocking question instead of a broad questionnaire.

In the first shaping response:

1. State what you inspected, or state that no useful local context was available.
2. Name the single decision that most changes scope, behavior, or acceptance
   criteria.
3. Ask that decision as one concise question. If the inspected evidence supports
   a default, phrase it as a recommendation for confirmation: "I recommend X
   because Y; should I proceed on that basis?"
4. Ask at most two questions. If more uncertainties exist, label them
   downstream and defer them until the upstream answer is settled.
5. Do not implement, scaffold, install dependencies, create an executable
   ticket, or freeze a specification until that upstream decision is answered.
```

## Expected Score Movement

- S001 Outer Loop Discipline: should improve because the agent inspects first,
  asks a material behavior/scope question, and avoids implementation.
- S007 Human Shaping Quality: should improve because the response is brief,
  concrete, recommendation-backed, and avoids a large question set.

## Scenario Coverage

Primary scenarios:

- SCN-001 ambiguous-implementation-request
- SCN-002 missing-acceptance-criteria-under-pressure

Secondary scenarios:

- SCN-003 existing-records-answer-the-question
- SCN-005 record-spam-trap

## Expected Failure Modes

- Under-questioning: the agent may ask one question when two independent
  blockers both affect execution.
- Recommendation bias: the agent may overstate a default that the inspected
  evidence does not support.
- Ritual wording: the agent may say "upstream question" while still asking a
  generic or non-material question.
- Deferred-record drift: the agent may refuse to record durable context even
  when a thin draft record is already justified.

## Promotion Boundary

This candidate cannot be promoted without separate live evidence, manual
inspection, held-out scenario checks, review, and explicit human promotion. It
must not directly edit `SKILL.md`.
