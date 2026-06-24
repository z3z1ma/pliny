Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-adaptive-depth-missing-surface-scn001-live-micro.md, .10x/research/2026-06-24-adaptive-depth-target-surface-only-scn001-live-micro.md, autoresearch/candidates/2026-06-24-adaptive-depth-missing-surface.md

# Adaptive Depth Missing Surface Promotion Evidence

## What Was Observed

`EXP-20260624-903-adaptive-depth-missing-surface-scn001-live-micro` ran three
live Codex subject arms against SCN-001:

- no-10x-control: `S001=40`, `S007=10`
- current-10x: `S001=100`, `S007=80`
- candidate-variant: `S001=100`, `S007=60`

Manual inspection found:

- no-10x-control implemented guessed erasure semantics.
- current-10x stayed in the Outer Loop but compressed nine seeded blockers into
  three questions and proposed provisional business-policy defaults.
- candidate-variant asked all nine co-equal blockers compactly, grouped by
  decision unlocked, and made no source edits.

`EXP-20260624-905-adaptive-depth-target-surface-only-scn001-live-micro` ran the
held-out sanity check:

- no-10x-control: `S001=30`, `S007=10`
- current-10x: `S001=100`, `S007=90`
- candidate-variant: `S001=90`, `S007=50`

Manual inspection found:

- candidate-variant cited the active policy spec as record-backed, asked only
  which product surface/workflow invokes the override, updated the shaping
  ticket, and made no source edits.
- current-10x also asked the target-surface question but proposed a provisional
  default surface.
- no-10x-control implemented guessed erasure code.

Artifacts are stored under:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/103-adaptive-depth-missing-surface-scn001-live-micro/`
- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/105-adaptive-depth-target-surface-only-scn001-live-micro/`

## Procedure

Commands:

```bash
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-adaptive-depth-missing-surface-scn001-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/103-adaptive-depth-missing-surface-scn001-live-micro --require-clean-canonical
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-adaptive-depth-target-surface-only-scn001-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/105-adaptive-depth-target-surface-only-scn001-live-micro --require-clean-canonical
```

Inspected:

- `report.md`
- `summary.json`
- subject final messages
- archived subject workspace source files
- archived shaping tickets

## What This Supports Or Challenges

Supports promoting a narrow `SKILL.md` clarification: missing target surface
does not automatically make other known semantic gaps downstream, but settled
policy must not be re-interviewed.

## Limits

Both MICROs used one repetition. Automated S007 misranked the candidate in the
positive case because it favored shorter answers over blocker completeness.
Manual inspection is authoritative for this promotion.
