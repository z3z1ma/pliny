Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-no-ticket-ratification-checkpoint-scn001-live-micro.md, autoresearch/candidates/2026-06-24-no-ticket-ratification-checkpoint.md

# No-Ticket Ratification Checkpoint Live MICRO Evidence

## What Was Observed

`EXP-20260624-885-no-ticket-ratification-checkpoint-scn001-live-micro` ran
three live Codex subject arms against SCN-001:

- no-10x-control: `S001=30`, `S007=10`
- current-10x: `S001=90`, `S007=25`
- candidate-variant: `S001=85`, `S007=50`

Artifacts are stored under
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/085-no-ticket-ratification-checkpoint-scn001-live-micro/`.
`canonical_guard.json` recorded `unchanged_during_run: true` for `SKILL.md` and
`autoresearch/program.md`.

Manual inspection found:

- no-10x-control invented payout thresholds, retry count, eligibility,
  notification routing, and ownership, then edited source/tests.
- current-10x made no source edits and blocked unratified payout policy, but
  wrote a blocked ticket in its subject workspace to store the policy
  ratification gap.
- candidate-variant made no file writes, identified record-backed authority,
  listed the unratified semantic values, and asked a direct confirm-or-correct
  policy checkpoint before any executable ticket, tests, or implementation.

## Procedure

Command:

```bash
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-no-ticket-ratification-checkpoint-scn001-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/085-no-ticket-ratification-checkpoint-scn001-live-micro --require-clean-canonical
```

Inspected:

- `summary.json`
- `report.md`
- `canonical_guard.json`
- `scores/*.score.json`
- `raw/*.json`
- `codex/*.last-message.txt`
- subject workspace file lists for all three arms
- current arm blocked ticket content

## What This Supports Or Challenges

Supports promoting
`autoresearch/candidates/2026-06-24-no-ticket-ratification-checkpoint.md` into
`SKILL.md`.

The evidence supports the claim that a narrow no-ticket ratification checkpoint
improves S007/manual shaping quality while preserving the implementation
boundary for high-impact semantic blockers.

## Limits

This is one MICRO scenario and one repetition. Scores are Trust Level 1 offline
heuristics over captured live artifacts. The result does not prove that the
instruction is safe for every blocked-ticket case; promotion depends on the
narrow wording that preserves record creation whenever a real durable record has
crystallized.
