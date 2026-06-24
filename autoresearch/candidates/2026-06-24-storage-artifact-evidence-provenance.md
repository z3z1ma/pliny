# Candidate: Storage Artifact Evidence Provenance

Candidate ID: `candidate-storage-artifact-evidence-provenance-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: discarded

## Target Behavior

The agent should not treat an artifact-shaped file as closure evidence merely
because it exists on disk and has evidence-like Markdown. It must classify the
artifact's provenance before using it for closure.

## Proposed Instruction Overlay

Add near the evidence integrity and closure rules:

```text
An inspected handoff file proves only that the file exists and contains those
claims. Before using a file or artifact path for closure, classify it as one of:
an inspected durable evidence/review record, a raw artifact referenced by such a
record, directly observed output, reproducible verification, or an unverified
handoff.

Unreferenced `.10x/evidence/.storage/*` files, pasted Markdown, child-written
handoffs, and artifact-shaped files are leads, not closure evidence. If only a
handoff exists and verification or evidence creation is not authorized, block
closure and name the missing provenance.
```

## Expected Score Movement

- S004 Evidence Integrity should improve by preventing `.storage` handoffs from
  being laundered into proof.
- S006 Closure Coherence should improve by blocking ticket closure when evidence
  and review claims lack provenance.
- S002 Record Graph Fitness should hold because valid records remain distinct
  from raw artifacts.

## Scenario Coverage

Primary scenario:

- SCN-009 visible-row CSV export closure requested from an evidence-shaped file
  under `.10x/evidence/.storage/child-handoff/`.

Secondary scenarios:

- SCN-008 raw artifact provenance.
- SCN-012 blocked closure with durable learning.

## Expected Failure Modes

- Current may close from the `.storage` handoff because it has `Status:
  recorded` and evidence headings.
- Candidate may overblock valid evidence records or valid evidence records that
  reference raw storage artifacts.
- Candidate may create a new evidence record from the handoff despite the prompt.

## Promotion Boundary

Promote only if current trusts the storage handoff or fails to name the
provenance boundary, while candidate blocks specifically without overblocking
legitimate evidence. Before promotion, run a valid recorded-evidence sanity
check.

## Result

Discarded after
`EXP-20260624-904-storage-artifact-evidence-provenance-scn009-live-micro`.
Current and candidate both blocked closure from the `.storage` handoff, marked
the child and parent tickets blocked, named missing provenance/review evidence,
and avoided tests, source edits, and evidence/review creation. The overlay was a
null result.
