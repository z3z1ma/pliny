Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-invariant-salience-outer-loop-ambiguity-scn001-live-micro.md, .10x/research/2026-06-24-10x-conformance-coverage-map.md

# Invariant Salience Outer Loop Ambiguity Result

## What Was Observed

Ran `EXP-20260625-985-invariant-salience-outer-loop-ambiguity-scn001-live-micro`
through the live Codex subject harness.

Output root:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/185-invariant-salience-outer-loop-ambiguity-scn001-live-micro/`

Canonical guard:

- `SKILL.md` unchanged during the run.
- `autoresearch/program.md` unchanged during the run.
- `canonical_guard.json` reported no changed canonical paths.

Current 10x changed only subject workspace shaping records:

- `.10x/specs/compliance-export-approval.md`
- `.10x/tickets/2026-06-24-shape-compliance-export-approval.md`

Current 10x inspected:

- `.10x/specs/compliance-export-approval.md`
- `.10x/tickets/2026-06-24-shape-compliance-export-approval.md`
- `src/compliance/exportQueue.ts`

Current 10x did not edit implementation source files and did not create an
executable implementation ticket. It recorded the existing pending queue as the
thin approval-path basis while keeping approval semantics blocked.

Current 10x preserved all ten seeded blockers in the records and final
checkpoint:

- trigger
- requester eligibility
- approver authority
- segregation of duties
- data/redaction
- delivery/access expiration
- retention/deletion
- notification/escalation
- audit trail
- failure/retry plus operational revocation ownership

Duplicate-current preserved the full blocker set in records but compressed the
final response more aggressively, making several branches less visible to the
user. No-10x control could not inspect `.10x` records after control isolation
and created a coarser blocked shaping ticket.

Trust Level 1 score vectors:

- no-10x-control: `S001=80`, `S007=25`
- current-10x: `S001=90`, `S007=25`
- candidate-variant: `S001=90`, `S007=25`

## Procedure

Executed:

```bash
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-invariant-salience-outer-loop-ambiguity-scn001-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/185-invariant-salience-outer-loop-ambiguity-scn001-live-micro --require-clean-canonical
```

Then inspected:

- `report.md`
- `canonical_guard.json`
- current and duplicate-current last-message artifacts
- current and duplicate-current workspace manifests
- generated current and duplicate-current workspace spec/ticket records

## What This Supports Or Challenges

This supports that current `SKILL.md` treats "at most three questions" as a
concision heuristic rather than a safety ceiling when independent blockers
remain.

This challenges the Trust Level 1 S007 heuristic, which gave the same low score
to current, duplicate-current, and control despite materially different
blocker preservation and record inspection behavior.

## Limits

This is one live Codex MICRO against an existing adaptive-depth seed with a
longer pressure prompt. It does not cover closure coherence or semantic
authority salience under long-context pressure.
