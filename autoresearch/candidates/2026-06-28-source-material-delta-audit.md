# Candidate: Source Material Delta Audit

Candidate ID: `candidate-source-material-delta-audit-v1`
Created: 2026-06-28
Canonical target: `SKILL.md`
Status: draft
Promotion: manual-only

## Target Behavior

Improve `S010` by reducing loss between inspected source/chat/artifacts and the
durable records created from them.

## Proposed Instruction Overlay

Add near the Record Graph or Evidence rules:

```text
When creating or materially updating records from source, chat, command output,
or external artifacts, do a material-fact delta pass: what facts were available,
which record now owns each durable fact, and what was deliberately omitted as
noise, external canon, secret, or out of scope. A record can stay concise, but
it must not force a future agent to reopen the transcript or artifact merely to
recover an available objective, authority, constraint, edge case, blocker,
evidence limit, or next action. For external canonical artifacts, preserve
status, revision or timestamp, pointer, local authority, and what behavior is
delegated to the external source instead of copying the whole artifact.
```

## Expected Score Movement

- Strongest on external-artifact index records, evidence/research capture, and
  retrospective extraction.
- Should not increase record count; it asks for a delta pass inside the chosen
  record owner.

## Expected Failure Modes

- Subject writes verbose material-fact inventories instead of concise records.
- Subject duplicates external artifacts instead of indexing authority.
- Subject over-preserves noisy facts.
