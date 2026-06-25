Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-skill-record-backed-identity-weak-request-regression-scn012-live-micro.md, autoresearch/candidates/2026-06-25-skill-record-backed-identity.md

# Skill Record-Backed Identity Weak-Request Regression Result

## What was observed

Ran `EXP-20260625-998-skill-record-backed-identity-weak-request-regression-scn012-live-micro` with nine live Codex subject samples across `no-10x-control`, `current-10x`, and `candidate-variant`.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/198-skill-record-backed-identity-weak-request-regression-scn012-live-micro/`

`canonical_guard.json` reported `SKILL.md` and `autoresearch/program.md` unchanged during the run.

Trust Level 1 telemetry recorded:

- candidate-variant: `S002=85` average and `S006=65` average;
- current-10x: `S002=85` average and `S006=65` average;
- no-10x-control: `S002=70` average and `S006=30` average.

Manual inspection found:

- candidate-variant created `.10x/skills/ledger-import-fixture-replay/SKILL.md` in all three repetitions;
- current-10x created `.10x/skills/ledger-import-fixture-replay/SKILL.md` in all three repetitions;
- no-10x-control created flat or near-synonym skill files instead of the exact directory-shaped source skill;
- candidate-variant created no `.claude`, `.agents`, `.opencode`, or other speculative harness-native mirror directories;
- `rg` found no generated-skill references to `.10x/tickets`, `.10x/evidence`, `.10x/reviews`, `.10x/specs`, `.10x/research`, or `.10x/decisions`;
- candidate-variant made no implementation file edits.

Manual inspection also found lifecycle inconsistency unrelated to the skill identity target:

- candidate rep 0 moved both completed tickets to `.10x/tickets/done/`;
- candidate rep 1 left the child ticket at the top-level despite `Status: done`;
- candidate rep 2 left both done-status tickets at the top-level;
- current moved both completed tickets to `.10x/tickets/done/` in all three repetitions.

## Procedure

Inspected:

- `report.md`;
- `canonical_guard.json`;
- raw artifact arm and rep mapping;
- every generated skill path;
- generated skill bodies;
- harness-native mirror paths;
- workspace manifests and changed paths;
- final ticket locations and statuses.

## What this supports or challenges

This supports `candidate-skill-record-backed-identity-v1` preserving canonical weak-request slug stability while adding no duplicate, speculative, or implementation-touching behavior in the no-native workspace.

It challenges any claim that the candidate improves closure lifecycle maintenance. The candidate remains an identity candidate, not a terminal-status path-maintenance candidate.

## Limits

This regression did not test harness-native mirror directories. It also did not isolate lifecycle path maintenance, because the candidate sentence targets skill identity and current already contains other closure instructions.
