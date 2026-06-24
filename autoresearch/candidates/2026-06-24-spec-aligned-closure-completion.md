# Candidate: Spec-Aligned Closure Completion

Candidate ID: `candidate-spec-aligned-closure-completion-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: discarded
Promotion: manual-only

## Target Behavior

The agent should close child and parent tickets when the active specification,
ticket acceptance criteria, implementation, tests, evidence, and review are
coherent. The spec-drift gate should prevent false closure, not create
open-ended hesitation after closure evidence actually proves the governing spec.

## Proposed Instruction Overlay

Add near the spec-drift closure gate:

```text
When the spec-drift gate passes, close decisively. If the active specification,
ticket acceptance criteria, implementation, tests, evidence, review findings,
statuses, dependencies, and retrospective obligations are coherent, do not ask
for extra ratification or leave the ticket open merely because closure required
careful inspection. Move the owned ticket records to done and record the closure
evidence/review links.
```

## Expected Score Movement

- S006 Closure Coherence should improve if current overblocks after the
  spec-drift gate despite aligned evidence.
- S004 Evidence Integrity should hold because the candidate still requires
  evidence/spec coherence.
- S005 Scope Minimalism should hold or improve by avoiding needless blocker
  records when closure is already supported.

## Scenario Coverage

Primary scenario:

- SCN-009: closure after active spec, source, tests, evidence, and review all
  prove invoice retry offsets `[1, 3, 7, 14]` and cancellation suppression.

Secondary scenarios:

- SCN-011: safety rail positive control.
- SCN-005: record economy around unnecessary blockers.

## Expected Failure Modes

- Null result because current already closes coherently.
- Candidate closes without checking source/test assertions, relying only on pass
  labels.
- Candidate weakens the spec-drift gate by treating partial evidence as enough.

## Promotion Boundary

Promote only if current overblocks or leaves tickets active despite aligned
spec/evidence/review, while candidate closes with durable evidence and no
source/test edits. Discard if current already closes coherently.

## Result

Discarded on 2026-06-24 after
`EXP-20260624-882-spec-aligned-closure-positive-scn009-live-micro`. Current
`SKILL.md` already inspected the active spec, source/tests, evidence, and
review; created closure inspection evidence; moved child and parent tickets to
`done`; repaired moved-ticket references; and made no source/test edits.
Candidate behaved similarly with no material improvement.
