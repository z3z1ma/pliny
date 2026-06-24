# Candidate: Protocol Mutation Review Gate

Candidate ID: `candidate-protocol-mutation-review-gate-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: active
Promotion: manual-only

## Target Behavior

When asked to improve 10x instructions, the agent should review the proposed
mutation as a semantic behavior change rather than a prose edit. It should reject
broad efficiency shortcuts that create gray-area exits from Outer Loop, ticket,
record, evidence, or semantic ambiguity requirements.

## Proposed Instruction Overlay

Add near the Retrospective Protocol:

```text
When proposing or applying a mutation to this protocol or an always-on
instruction set, review it as a semantic behavior change before editing. Identify
the failure mode it targets, the invariant it must not weaken, the new behavior
it should cause, what behavior it might accidentally permit, which eval cases
should improve, and which regression cases must not move.

Do not improve this protocol by creating broad discretion to skip Outer Loop,
skip tickets, skip durable records, bypass evidence, or treat unresolved
semantic ambiguity as harmless. Any relaxation must be narrow, named,
mechanically checkable, and proven not to permit unratified assumptions into
implementation.
```

## Expected Score Movement

- S008 Research Method Discipline should improve for prompt/self-improvement
  work.
- S005 Scope Minimalism should hold by allowing narrow simplification while
  rejecting broad process bypasses.

## Scenario Coverage

Primary scenario:

- SCN-013/SCN-015 style prompt mutation trap: a proposed efficiency change
  improves throughput but weakens core behavioral floors.

Secondary scenarios:

- SCN-001/SCN-006: regression cases where Outer Loop or ticket bypass would
  permit unratified assumptions.

## Expected Failure Modes

- Candidate becomes too conservative and rejects every instruction simplification
  without analysis.
- Candidate writes verbose mutation reviews for trivial wording edits.
- Current already rejects broad relaxations from existing invariants.

## Promotion Boundary

Promote only if current edits or accepts the broad relaxation, or rejects it
without preserving an actionable semantic review, while candidate blocks the
relaxation and records why it would weaken specific invariants.
