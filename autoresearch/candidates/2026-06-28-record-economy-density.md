# Candidate: Record Economy Density

Candidate ID: `candidate-record-economy-density-v1`
Created: 2026-06-28
Canonical target: `SKILL.md`
Status: draft
Promotion: manual-only

## Target Behavior

Improve `S010` without encouraging record spam by optimizing for useful context
per durable record.

## Proposed Instruction Overlay

Add near Write durable context or Record Graph:

```text
Optimize record density, not record count. For each durable fact, choose one
owning record and make that owner rich enough to be useful. Do not split a
small conclusion into ticket/spec/evidence/knowledge placeholders merely
because each type could apply. Do not make a record terse by pushing essential
context into chat, filenames, or vague references. A good small record states
why it exists, what future decision or action it supports, the authority it
depends on, and why adjacent possible records are unnecessary.
```

## Expected Score Movement

- Strongest on `SCN-005` record-spam traps and small triage tasks.
- Should improve the quality/cost frontier by preserving richness while
  reducing unnecessary records.

## Expected Failure Modes

- Subject under-records needed evidence or tickets in the name of density.
- Subject over-explains why it avoided records.
