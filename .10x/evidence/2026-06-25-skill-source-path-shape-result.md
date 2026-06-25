Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-skill-source-path-shape-scn012-live-micro.md, autoresearch/candidates/2026-06-25-skill-source-path-shape.md

# Skill Source Path Shape Result

## What Was Observed

Ran `EXP-20260625-990-skill-source-path-shape-scn012-live-micro` with two
repetitions per arm.

Artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/190-skill-source-path-shape-scn012-live-micro/`

Manual source-path results:

| Arm | Rep | Source path result | Speculative mirrors |
| --- | ---: | --- | --- |
| candidate-variant | 0 | `.10x/skills/ledger-import-fixture-replay/SKILL.md` | none |
| candidate-variant | 1 | `.10x/skills/replay-ledger-import-fixtures/SKILL.md` | none |
| current-10x | 0 | `.10x/skills/ledger-import-fixture-replay.md` | none |
| current-10x | 1 | `.10x/skills/ledger-import-fixture-replay/SKILL.md` | none |
| no-10x-control | 0 | `.10x/skills/ledger-import-fixture-replay.md` | none |
| no-10x-control | 1 | `.10x/skills/ledger-import-fixture-replay/SKILL.md` | none |

Automated S002 averages:

- candidate-variant: `100`
- current-10x: `65`
- no-10x-control: `47.5`

All candidate-created skill files used YAML frontmatter and contained
`Objective`, `Prerequisites`, `Procedure`, and `Validation` sections. No
candidate run created `.claude`, `.agents`, `.opencode`, or another mirror
directory.

`canonical_guard.json` reported `unchanged_during_run: true` for `SKILL.md` and
`autoresearch/program.md`.

## Procedure

Command run from `/Users/alexanderbutler/code_projects/personal/10x`:

```bash
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-skill-source-path-shape-scn012-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/190-skill-source-path-shape-scn012-live-micro --require-clean-canonical
```

Manual inspection steps:

- checked each archived workspace for
  `.10x/skills/ledger-import-fixture-replay/SKILL.md`;
- checked each archived workspace for flat
  `.10x/skills/ledger-import-fixture-replay.md`;
- checked for `.claude`, `.agents`, `.opencode`, and other mirror directories;
- inspected generated skill frontmatter and required sections;
- inspected score report and canonical guard.

## What This Supports Or Challenges

This supports `candidate-skill-source-path-shape-v1` improving source skill path
shape. Candidate avoided the flat-file source shape in both repetitions while
current repeated the flat-file failure once.

It also challenges immediate promotion because candidate rep 1 used a different
directory-shaped slug. The candidate fixes path shape, not slug consistency.

## Limits

This experiment does not prove the candidate preserves harness mirroring when a
native directory exists. `.claude`, `.opencode`, and `.agents` regressions are
required before promotion.

The no-native-dir prompt explicitly forbade speculative mirrors, so mirror
absence here is a control, not proof under weaker prompts.
