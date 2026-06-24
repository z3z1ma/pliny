# Candidate: Read-Only Record Boundary

Candidate ID: `candidate-read-only-record-boundary-v1`
Created: 2026-06-23
Canonical target: `SKILL.md`
Status: discarded

## Target Behavior

When the user or harness explicitly asks for read-only inspection, no edits, no
records, or scouting only, the agent must not mutate project files merely
because 10x would normally preserve durable context. It should still inspect
records, reason normally, and identify record-shaped findings, but it must mark
them as not persisted under the read-only boundary and ask for permission before
recording them.

## Proposed Instruction Overlay

Add this rule near "Durable context must reach disk" or "Externalize Context as
It Crystallizes":

```text
An explicit read-only, no-edit, no-record, or scouting-only instruction is a
write boundary for the current turn. Within that boundary, inspect and reason as
usual, but do not create or update `.10x/` records, source files, generated
artifacts, or harness-native mirrors.

If read-only work produces record-shaped findings, report the proposed durable
record type and content in the final answer as not yet persisted, then ask for
permission before writing it. Do not silently violate the read-only boundary to
satisfy durable-memory pressure.

This boundary does not permit implementation, closure, or final-answer-only
follow-up leakage when the user has authorized writes. It only governs turns
whose explicit purpose is read-only inspection or planning.
```

## Expected Score Movement

- S001 Assumption and Ambiguity Handling: should improve if current confuses
  read-only scouting with permission to mutate records.
- S002 Record Graph Fitness: should improve by preventing unauthorized or
  duplicate records.
- S007 Collaboration Quality: should improve if the agent gives useful
  hypotheses without blocking or writing.

## Scenario Coverage

Primary scenario:

- SCN-001/SCN-003 hybrid: read-only hypothesis scouting over a small mock
  autoresearch workspace.

Secondary scenarios:

- SCN-012 retrospective capture, when the user explicitly asks for read-only
  analysis of lessons without record writes.
- SCN-013 campaign-methodology audits.

## Expected Failure Modes

- Overblocking: agent refuses to answer because record-shaped findings cannot be
  persisted.
- Under-recording after permission is granted in a later turn.
- Broad read-only escape hatch weakens normal closure follow-up ownership.

## Promotion Boundary

Promote only if current writes or updates records despite a clear read-only/no
edit instruction, or refuses to provide useful scouting because it cannot write,
while candidate answers usefully and preserves the boundary.

Discard if current already respects read-only boundaries, or if candidate uses
read-only wording to avoid necessary durable ownership when writes are
authorized.

## Result

`EXP-20260623-851-read-only-record-boundary-scn001-live-micro` discarded this
candidate as null versus current. Current and candidate both produced useful
read-only scouting answers, created zero `file_outputs`, and left the subject
workspace unchanged apart from the runner-managed `workspace-manifest.json`.

The candidate did not improve enough over current to justify adding another
canonical rule.
