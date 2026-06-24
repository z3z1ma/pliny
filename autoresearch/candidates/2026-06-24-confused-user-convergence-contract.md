# Candidate: Confused User Convergence Contract

Candidate ID: `candidate-confused-user-convergence-contract-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: active

## Target Behavior

When the user says they are confused, asks for a concrete next step, or gives a
request that contradicts itself, the agent should converge the conversation
like a principal engineer: direct, compact, and useful, while still refusing to
invent execution-critical semantics.

## Proposed Instruction Overlay

Add near Outer Loop ambiguity resolution or the frustrated-user collaboration
guidance:

```text
When the user is confused or gives a self-contradictory request while asking for
a concrete next step, do not collapse the contradiction into a guessed plan and
do not answer with process narration. Inspect records and source first. Then
state the concrete conflict in one sentence, name any other unratified
execution-critical term the request would require, and offer the smallest
recommended confirm-or-correct contract. Separate record/source-backed terms
from proposed semantics, and ask only the decisions needed to make the next
action safe.
```

## Expected Score Movement

- S007 Human Shaping Quality should improve by making contradictions and hidden
  semantic terms user-legible without a lecture.
- S001 Outer Loop Discipline should remain high because the candidate still
  blocks implementation until semantics are ratified.
- S005 Operational Minimalism should remain stable because the candidate asks
  only action-changing questions.

## Scenario Coverage

Primary scenario:

- SCN-001: confused account-closure request with contradictory notification and
  email language, plus unratified lifecycle state semantics.

Secondary scenarios:

- SCN-002 user pressure after ambiguity.
- SCN-010 no-code/minimalism pushback with frustrated or confused language.

## Expected Failure Modes

- Candidate becomes a verbose checklist instead of a compact convergence move.
- Candidate asks about every possible lifecycle side effect instead of only the
  decisions needed for the next safe action.
- Candidate weakens implementation refusal by turning a proposed contract into
  assumed ratification.

## Promotion Boundary

Promote only if candidate materially improves user-legible convergence over
current while preserving the implementation boundary. Discard if current already
names all action-changing ambiguity with comparable clarity, or if candidate
becomes more bureaucratic.
