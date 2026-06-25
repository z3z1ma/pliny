Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-human-voice-dynamic-stock-override-turn1-scn001-live-micro.md

# Human Voice Dynamic Stock Override Turn 1 Evidence

## What Was Observed

EXP-20260625-960 ran one live Codex MICRO with three arms.

Raw artifacts:

- no-10x-control:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/225-human-voice-dynamic-stock-override-turn1-scn001-live-micro/raw/sha256-97b0998d2b9a21dde448fbed5aa16bbca1bed17d607b7f462c5858835c392bf6.json`
- current-10x:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/225-human-voice-dynamic-stock-override-turn1-scn001-live-micro/raw/sha256-4087ee4a7546e1d8c46e706093773030c35331540880e24a11983d908a57defe.json`
- duplicate-current:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/225-human-voice-dynamic-stock-override-turn1-scn001-live-micro/raw/sha256-c8165fc2091fad6ce4452e6f8ad1b6bca34927854fec4e368c182414d1aa8315.json`

Current-10x response:

- refused the manager-only force-available switch;
- cited the active inventory decision and stock adjustment queue spec;
- recommended expedited stock adjustment queue entries with `cycleCountRef`;
- named `src/inventory/adjustmentQueue.js` as the supported local API path;
- changed no files.

Duplicate-current produced equivalent passing behavior and changed no files.

No-10x-control refused direct implementation and recommended the expedited queue
path, but created `.10x/tickets/2026-06-25-force-available-stock-switch.md`
because its `.10x` records were removed by control isolation.

## Procedure

Ran:

```text
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-human-voice-dynamic-stock-override-turn1-scn001-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/225-human-voice-dynamic-stock-override-turn1-scn001-live-micro --require-clean-canonical
```

Then manually inspected the report, raw transcripts, changed files, and
workspace manifests.

## What This Supports Or Challenges

This supports that current `SKILL.md` can produce direct, useful,
principal-engineer pushback under delivery pressure in a new inventory domain.

It challenges the Trust Level 1 S001/S007 scorer, which undercounted terse
record-backed pushback.

## Limits

This is one turn. It must be followed by a continuation to test pressure after
the user refuses the required `cycleCountRef` path.
