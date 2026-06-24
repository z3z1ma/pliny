# Candidate: Record Lifecycle Reference Repair

Candidate ID: `candidate-record-lifecycle-reference-repair-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: discarded

## Target Behavior

When moving, renaming, superseding, or deleting a `.10x` record, the agent
should repair references by occurrence role rather than blindly replacing every
matching path string.

## Proposed Instruction Overlay

Add near record reference and lifecycle rules:

```text
When moving, renaming, superseding, or deleting a `.10x` record, repair
references by occurrence role, not by blind string replacement. First classify
matches as live record links, active governing prose, historical prose, or
quoted/code-block content. Repair live links such as Parent, Depends-On,
Relates-To, Target, active specs, active decisions, and executable tickets.
Preserve historical notes and fenced examples unless their purpose is an active
reference. Keep edits minimal and record why any old path intentionally remains.
```

## Expected Score Movement

- S002 Record Graph Fitness should improve by eliminating stale live links.
- S003 Ticket Readiness should hold because active ticket dependencies remain
  coherent after supersession.
- S006 Closure Coherence should improve in later closure cases with moved
  records.

## Scenario Coverage

Primary scenario:

- SCN-004 FinchPay decision supersession with active links, review/evidence
  headers, historical prose, and fenced command output mentioning the old path.

Secondary scenarios:

- SCN-003 records-first retrieval after moved records.
- SCN-009 closure with moved evidence/review records.

## Expected Failure Modes

- Current may leave stale live references to a moved decision.
- Current may blindly replace historical notes or fenced code blocks.
- Candidate may overclassify active prose as historical and leave stale links.

## Promotion Boundary

Promote only if current leaves stale live references or performs broad
replacement in historical/code-block text while candidate repairs references
selectively. If candidate wins, run a no-replacement negative control before
promotion.

## Result

`EXP-20260624-908-record-graph-supersession-reference-repair-scn004-live-micro`
discarded this candidate as null to slightly worse versus current. The initial
run had a confounded `candidate-variant` arm because Codex returned a temporary
usage-limit failure before execution. The clean rerun showed current and
candidate both repairing live references by occurrence role while preserving
historical path mentions. Current did so with less workflow churn. Candidate
also cancelled the old shaping ticket and opened an implementation follow-up,
which was not needed for the requested record-graph repair turn.

Evidence:

- `.10x/evidence/2026-06-24-record-lifecycle-reference-repair-result.md`
- `.10x/reviews/2026-06-24-record-lifecycle-reference-repair-result.md`
