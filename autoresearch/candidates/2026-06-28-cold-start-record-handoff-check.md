# Candidate: Cold Start Record Handoff Check

Candidate ID: `candidate-cold-start-record-handoff-check-v1`
Created: 2026-06-28
Canonical target: `SKILL.md`
Status: promoted
Promotion: promoted as compressed 297-character canonical wording in `SKILL.md` on 2026-06-28 after 50 live samples in `.10x/evidence/2026-06-28-record-richness-hypothesis-batch.md`

## Target Behavior

Improve `S010` with a compact combined guard for durable record richness,
actionability, economy, evidence limits, and noise filtering.

## Proposed Instruction Overlay

Add near Record Graph:

```text
Before finalizing a durable record update, run a cold-start handoff check. One
record should own each material fact from inspected source, chat, command output,
or artifacts. The chosen record must state why it exists, authority/provenance,
key constraints/exclusions/blockers, evidence or limits, and the next action it
enables. Keep it compact: link records that own detail, omit one-off noise, and
mark unresolved semantics blocked instead of executable.
```

## Expected Score Movement

- Should preserve most gains from source-material-delta, executor-handoff,
  record-economy, and audit-limits-redaction with fewer added characters.
- Should be strongest where record creation is correct but under-specified.

## Expected Failure Modes

- Subject may turn the check into boilerplate if the instruction is too broad.
- Subject may over-block executable work when source inspection is enough.
