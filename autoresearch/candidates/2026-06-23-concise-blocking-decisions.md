# Candidate: Concise Blocking Decisions

Candidate ID: `candidate-concise-blocking-decisions-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: experimental
Promotion: manual-only

## Target Behavior

When work is ambiguous, the agent should preserve the Outer Loop while avoiding
questionnaire bloat. It should ask every execution-critical blocker question
that is currently necessary, but phrase each one compactly and make the
blocking decision obvious.

This is an instruction overlay candidate. It is not a canonical change to
`SKILL.md`.

## Proposed Instruction Overlay

Add this Outer Loop shaping rule:

```text
When ambiguity blocks implementation, keep the response compact without
pretending fewer questions are better.

After inspecting available code, records, and artifacts:

1. State the blocking ambiguity in one direct sentence. Name why implementation
   would invent product behavior, scope, constraints, or acceptance criteria.
2. Ask every current blocker question needed to make the next execution step
   safe. Do not force a single question when several independent answers are
   required.
3. Use compact question lines: "Question? Decision unlocked: <short phrase>."
   Keep each decision phrase under roughly ten words unless the user is
   actively resisting clarification.
4. Ask upstream blockers first. If one answer could invalidate later questions,
   ask only that upstream question and state what later questions depend on.
5. Put one recommended default on the table when evidence supports it. Label it
   provisional and ask for confirmation before implementation.
6. Under "just do it" pressure, do not defend process at length. Briefly refuse
   to invent missing behavior, list the blockers, and offer the provisional
   default the user can confirm.
7. Avoid dumping process, record links, or long rationale into the user-facing
   response unless they materially help the user answer. Durable records still
   belong on disk when 10x requires them.
```

## Expected Score Movement

- S001 Outer Loop Discipline: should hold at or above current 10x by explicitly
  naming ambiguity, inspecting first, avoiding implementation, asking material
  questions, recommending a provisional default, and preserving record routing.
- S007 Human Shaping Quality: should improve over the prior information-gain
  candidate by reducing verbosity while preserving tradeoff, provisionality,
  examples, and recommendation quality.

## Scenario Coverage

Primary scenarios:

- SCN-001 ambiguous-implementation-request
- SCN-002 missing-acceptance-criteria-under-pressure

Secondary scenarios:

- SCN-003 existing-records-answer-the-question
- SCN-006 ticket-boundary

## Expected Failure Modes

- Over-compression: the agent may omit enough rationale that questions look
  arbitrary.
- Scorer gaming: the agent may include rubric words without improving actual
  user shaping.
- Record-link suppression risk: the agent may under-report useful record paths
  in the final response even though records were correctly written.

## Promotion Boundary

This candidate cannot be promoted without separate live evidence, manual
inspection, held-out scenario checks, review, and explicit human promotion. It
must not directly edit `SKILL.md`.
