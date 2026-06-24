Status: recorded
Created: 2026-06-24
Updated: 2026-06-24
Relates-To: .10x/research/2026-06-24-spec-aligned-closure-positive-scn009-live-micro.md, autoresearch/candidates/2026-06-24-spec-aligned-closure-completion.md

# Spec-Aligned Closure Positive Control Live Micro

## What Was Observed

`EXP-20260624-882-spec-aligned-closure-positive-scn009-live-micro` ran three
live Codex subject arms against SCN-009. The canonical guard recorded unchanged
hashes for `SKILL.md` and `autoresearch/program.md` during the run.

Automated scores tied all arms at `S004=100` and `S006=45`.

Manual inspection:

- current-10x
  (`sha256-9b7eaf44fe7dc9f14ca974bf6bd8d0f22727e41b3a9da4f51b1a850bae76be4b`)
  closed both invoice retry tickets under `.10x/tickets/done/`, created
  `.10x/evidence/2026-06-24-invoice-retry-closure-inspection.md`, repaired
  moved-ticket references in existing evidence/review records, and made no
  source/test edits.
- candidate-variant
  (`sha256-b45de7e1ff2e3d7b75738b4f578ba5a50d269421785875cde356f46aa4329398`)
  also closed child and parent tickets, created closure inspection evidence,
  repaired moved-ticket references, and made no source/test edits.
- no-10x-control
  (`sha256-e0eb9e83f32702a6112c9d9d1c2d16651e6bef58720325f68de429da70d3c693`)
  created a new `.10x` closure graph and closed invented done tickets; this is
  not promotion-relevant because control suppresses the seed `.10x` records.

## Procedure

The experiment was run with:

```bash
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-24-spec-aligned-closure-positive-scn009-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/082-spec-aligned-closure-positive-scn009-live-micro --require-clean-canonical
```

The report, score artifacts, raw transcripts, command traces, prompts, and
archived workspaces are under
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/082-spec-aligned-closure-positive-scn009-live-micro/`.

## What This Supports Or Challenges

This supports discarding
`candidate-spec-aligned-closure-completion-v1` as null versus current. It also
serves as regression evidence that the promoted spec-drift closure gate does not
prevent closure when active spec, evidence, review, source, and tests are
coherent.

## Limits

This is one live MICRO repetition on a simple aligned closure fixture. It does
not prove behavior for larger parent graphs, multiple child tickets, or
partially superseded specifications. Offline scores remain Trust Level 1 and
manual inspection is authoritative.
