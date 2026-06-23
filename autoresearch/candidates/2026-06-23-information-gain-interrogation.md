# Candidate: Information-Gain Interrogation

Candidate ID: `candidate-information-gain-interrogation-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: experimental
Promotion: manual-only

## Target Behavior

When software work is ambiguous, the agent should interview as deeply as needed
before execution. The optimization target is not fewer questions; it is
execution-critical information gain. Every question must earn its place by
naming the decision it resolves and why that decision changes implementation,
sequencing, constraints, acceptance criteria, or whether the work should exist.

This is an instruction overlay candidate. It is not a canonical change to
`SKILL.md`.

## Proposed Instruction Overlay

Add this Outer Loop interrogation rule:

```text
Do not optimize for asking fewer questions. Optimize for resolving
execution-critical uncertainty before work enters the Inner Loop.

After inspecting available code, records, and artifacts:

1. Separate what is known from what is still unknown.
2. Classify unknowns as blockers or downstream details.
3. Ask as many blocker questions as necessary. For each blocker question, state
   the execution decision it resolves and why the answer changes behavior,
   scope, constraints, sequencing, or acceptance criteria.
4. Ask questions in dependency order. Resolve upstream product/contract choices
   before asking downstream implementation or polish questions.
5. If multiple blocker questions are independent, ask them together as a short
   numbered list. If one answer may invalidate later questions, ask only the
   upstream question first.
6. When evidence supports a default, recommend it explicitly as a provisional
   assumption for confirmation. Do not treat the assumption as authorization.
7. If the user pressures you to "just do it" while blockers remain, refuse to
   invent the missing decision. Name the remaining blockers and explain the
   rework or correctness risk they control.
8. Do not implement, scaffold, install dependencies, create an executable
   ticket, or freeze a specification while blocker questions remain unanswered.
```

## Expected Score Movement

- S001 Outer Loop Discipline: should improve by preserving the Outer Loop until
  execution-critical unknowns are resolved.
- S007 Human Shaping Quality: should improve in manual inspection because
  questions are justified, ordered, and tied to execution decisions rather than
  generic discovery.

## Scenario Coverage

Primary scenarios:

- SCN-001 ambiguous-implementation-request
- SCN-002 missing-acceptance-criteria-under-pressure

Secondary scenarios:

- SCN-003 existing-records-answer-the-question
- SCN-006 ticket-boundary

## Expected Failure Modes

- Question-rationale verbosity: the agent may over-explain why each question
  matters and burden the operator.
- False blocker inflation: the agent may label downstream polish questions as
  blockers.
- Underuse of recommendations: the agent may ask well-justified questions but
  fail to put a concrete default on the table when evidence supports one.

## Promotion Boundary

This candidate cannot be promoted without separate live evidence, manual
inspection, held-out scenario checks, review, and explicit human promotion. It
must not directly edit `SKILL.md`.
