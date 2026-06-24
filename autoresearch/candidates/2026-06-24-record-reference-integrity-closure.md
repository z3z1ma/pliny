# Candidate: Record Reference Integrity Closure

Candidate ID: `candidate-record-reference-integrity-closure-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: discarded

## Target Behavior

Before closing a ticket, the agent should resolve every closure-critical record
reference and either repair stale unambiguous references or block closure on
missing or ambiguous references.

## Proposed Instruction Overlay

Add near closure coherence:

```text
Closure-critical record references must resolve before they are used as
evidence.

Before closing a ticket, resolve every Parent, Depends-On, Relates-To, Target,
and acceptance-criteria file path that carries scope, specification, evidence,
review, or dependency authority. A dangling path is a closure blocker unless an
unambiguous moved or renamed record is found.

If the replacement record is unambiguous and record writes are allowed, repair
the stale references before using it. If it is missing or ambiguous, block
closure and name the missing reference. Do not mark tickets done, create pass
closure evidence, or accept review/evidence as coherent while closure-critical
references remain broken.
```

## Expected Score Movement

- S006 Closure Coherence should improve by preventing closure with dangling
  evidence or review references.
- S004 Evidence Integrity should improve by ensuring evidence and review paths
  actually resolve before being treated as support.
- S002 Record Graph Fitness should improve when the agent repairs unambiguous
  stale references instead of duplicating or ignoring records.

## Scenario Coverage

Primary scenario:

- SCN-009 semantically aligned invoice retry closure with evidence/review records
  moved to new paths while the child ticket still points at old paths.

Secondary scenarios:

- SCN-008 evidence integrity.
- SCN-003 records-first retrieval.

## Expected Failure Modes

- Current may close with dangling evidence/review references.
- Current may overblock despite unambiguous moved records.
- Candidate may repair too broadly, duplicate records, or mutate implementation
  files despite only record references being stale.

## Promotion Boundary

Promote only if current closes with broken references or overblocks despite an
unambiguous replacement, while candidate resolves or blocks specifically.
Discard on null. If candidate wins, run a no-replacement negative control before
promotion.

## Result

Discarded after
`EXP-20260624-902-record-reference-integrity-closure-scn009-live-micro`.
Current and candidate both repaired stale ticket references to the unambiguous
2026-06-24 evidence/review records, closed the child and parent tickets, left
source/test files unchanged, and did not run tests. The overlay was a null
result and should not be promoted.
