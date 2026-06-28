# Candidate: Record Regeneration Check

Candidate ID: `candidate-record-regeneration-check-v1`
Created: 2026-06-28
Canonical target: `SKILL.md`
Status: promoted-compressed
Promotion: manual-only

## Target Behavior

Improve `S010` / Record Regeneration Quality by making the existing "write for
cold readers" rule operational at the moment records are created or materially
updated.

## Motivation

Canonical `SKILL.md` already says records should be written for cold readers,
but the concrete ingredients of a regeneration-grade record are scattered
across record type descriptions. The hypothesis is that a short cold-start
checklist near the record graph rules will improve ticket, evidence, research,
and handoff record richness without encouraging record bloat.

## Proposed Instruction Overlay

Add near the Record Graph cold-reader rule:

```text
Before leaving any new or materially updated record, run a cold-start
regeneration check. A future agent should be able to answer, from the record
graph and its references, the current objective and state; authority and
provenance; constraints, exclusions, and edge cases; evidence and limits;
blockers, assumptions, and semantic authority; and the next action, owner, and
verification path.

Add only missing material context. Do not pad headings, duplicate external
canonical documents, or preserve secrets. If source, chat, or artifact context
contains material information you omit, the record is too thin. If a thin index
points to an external canonical artifact, include status, revision or timestamp,
pointer, provenance, and whether the local record or external artifact is
authoritative.
```

## Expected Score Movement

- `S010` should improve on ticket/spec shaping cases because executable records
  should preserve policy authority, edge cases, exclusions, evidence
  expectations, blockers, and next actions.
- `S010` should improve on evidence-capture cases because evidence records
  should preserve enough raw-output structure and limits to audit the claim
  while redacting secrets.
- `S002`, `S004`, `S005`, and `S006` should hold because the candidate does not
  authorize extra records, weaker evidence, broader implementation, or
  premature closure.

## Expected Failure Modes

- Candidate creates longer records without adding useful context.
- Candidate duplicates external documents instead of indexing provenance.
- Candidate leaks secrets while trying to preserve raw evidence.
- Candidate treats the checklist as permission to create unnecessary records.

## Promotion Boundary

Promote only if raw artifacts show record richness improves or is preserved
without floor triggers, extra implementation, record spam, or secret leakage.

## Result

Promoted in compressed form after:

- `EXP-20260628-record-regeneration-check`
- `EXP-20260628-record-regeneration-check-continuation`

The full overlay was not promoted. The canonical change replaced the existing
Record Graph cold-reader paragraph with a compact regeneration checklist that
keeps the useful behavior while staying within the `SKILL.md` size budget.
