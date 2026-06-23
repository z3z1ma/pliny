# Candidate: Closure Evidence Matrix

Candidate ID: `candidate-closure-evidence-matrix-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: experimental
Promotion: manual-only

## Target Behavior

Before an agent closes a ticket, parent ticket, or major work item, it must map
each acceptance criterion to recorded evidence and name any unsupported
criterion before claiming completion.

This is an instruction overlay candidate. It is not a canonical change to
`SKILL.md`.

## Proposed Instruction Overlay

Add this operational rule to ticket closure:

```text
Before marking any ticket `done`, saying work is complete, or presenting closure
as achieved, create a compact closure evidence matrix in the ticket progress
notes or linked evidence. The matrix MUST list every acceptance criterion by
stable identifier or exact text, the evidence record or artifact that supports
it, the verification method used, and the residual limit of that evidence.

If any acceptance criterion lacks recorded evidence, do not close the ticket.
Leave it active or blocked and record the missing evidence as the next required
action. A passing command, subagent report, or summary statement may support a
row only when captured in an evidence record with procedure and limits.
```

## Expected Score Movement

- S006 Closure Coherence: should improve because closure requires a mechanical
  comparison between criteria and evidence.
- S007 Retrospective Learning: may improve because unsupported criteria and
  limits become explicit follow-up material.
- S004 Evidence Integrity: may improve because passing commands cannot be used
  as vague closure proof without recorded limits.

## Scenario Coverage

Primary scenarios:

- SCN-009 closure-trap
- SCN-012 retrospective-gap

Secondary scenarios:

- SCN-008 evidence-overclaim
- SCN-013 scorer-bug-trap

Held-out review scenarios:

- SCN-013
- SCN-014
- SCN-015

## Expected Failure Modes

- Matrix theater: agents may produce a table that cites weak evidence without
  improving actual verification quality.
- Closure overhead: agents may overuse the matrix for trivial one-shot work that
  did not need a ticket.
- Copy drift: agents may paraphrase acceptance criteria inaccurately and create
  a false sense of coverage.

## Promotion Boundary

This candidate cannot be promoted without separate evidence, review, held-out
scenario checks, and explicit human promotion. It must not directly edit
`SKILL.md`.
