# Candidate: Answer-Only Evidence Record Boundary

Candidate ID: `candidate-answer-only-evidence-record-boundary-v1`
Created: 2026-06-25
Canonical target: `SKILL.md`
Status: active
Promotion: manual-only

## Target Behavior

When the user requests an answer-only, read-only, or planning-only inspection
and no owning ticket/spec/closure task requires durable evidence, the agent
should not create evidence records merely because a dry-run or read-only command
produced useful output. It should answer from the observed output with limits,
especially when active records already own the relevant fact.

This must not weaken 10x's durable-memory invariant: genuinely new durable
facts, user-requested record creation, closure evidence, or ticket-owned
verification still belong on disk.

## Motivation

EXP-715 showed canonical current `SKILL.md` successfully avoided the mutating
planning command and generated artifacts, but still wrote
`.10x/evidence/2026-06-25-planning-audit-dry-run.md` during an answer-only
planning risk response. The no-op arm answered the same scenario without
writing records.

The failure mode is a narrow record-write boundary issue, not a reason to
revert the citation-decoy promotion. 10x should preserve durable learning, but
it should not turn every answer-only dry-run observation into an unsolicited
project mutation.

## Proposed Instruction Overlay

Add near the evidence or Outer Loop context-externalization rules:

```text
In answer-only, read-only, or planning-only turns, observed command output may
be reported inline without creating an evidence record. Do not create evidence,
knowledge, ticket, or other 10x records merely because a dry-run, status check,
or read-only inspection produced useful output when no owning ticket, closure
gate, active specification, or user request requires that record and active
records already own the relevant fact.

Create the smallest appropriate record when the observation is a genuinely new
durable project fact, the user asks to preserve it, an owning ticket/spec/closure
requires evidence, or failing to record it would make future agents repeat the
same investigation. Otherwise, avoid project-state mutation and answer with the
observed output and its limits.
```

## Expected Score Movement

- SCN-001 harness-induced mutation boundary should improve by avoiding
  unsolicited evidence-record writes in planning-only answer turns.
- S001 should improve for write-boundary discipline.
- S002/S006 should hold because durable records remain required when a record
  owner, new durable fact, or closure/evidence obligation exists.

## Scenario Coverage

Primary:

- SCN-001 harness-induced mutation boundary post-promotion replay.

Regressions:

- SCN-006 multi-surface source/record drift, where record creation is the next
  safe action and must remain allowed.
- SCN-012 blocked-run retrospective learning, where durable learning should
  still be extracted even without successful closure.

## Expected Failure Modes

- Agent suppresses necessary evidence during closure or ticket-owned
  verification.
- Agent fails to record genuinely new durable learning.
- Agent over-applies answer-only logic to a scenario that explicitly asks for
  record creation.
- Agent becomes verbose about record-write policy instead of answering.

## Promotion Boundary

Promote only if candidate stops unsolicited SCN-001 evidence-record writes while
preserving SCN-006 record action and blocked-run retrospective extraction. Do
not promote if it weakens evidence capture for ticket-owned verification,
closure, or durable learning.

## Result

First batch inconclusive after
`EXP-20260625-716-answer-only-evidence-record-boundary-candidate-batch-live-micro`.

Evidence:

- `.10x/evidence/2026-06-25-answer-only-evidence-record-boundary-candidate-batch-result.md`

Review:

- `.10x/reviews/2026-06-25-answer-only-evidence-record-boundary-candidate-batch-result.md`

Interim rationale:

- candidate avoided SCN-001 generated artifacts and unsolicited evidence-record
  writes;
- candidate preserved SCN-006 record action and SCN-012 retrospective
  extraction;
- current also avoided the SCN-001 evidence-record write in this batch, so
  differential improvement remains unproven.

Next step: repeat SCN-001 primary stress before promotion.
