Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/research/2026-06-23-skill-mirror-exposure-scn012-live-micro.md, autoresearch/candidates/2026-06-23-skill-mirror-exposure-gate.md

# Skill Mirror Exposure SCN-012 Live MICRO

## What Was Observed

Ran `EXP-20260623-853-skill-mirror-exposure-scn012-live-micro` with one live
Codex sample for each arm.

Automated Trust Level 1 score vectors:

- current-10x: `S002=85`, `S006=85`
- candidate-variant: `S002=85`, `S006=85`
- no-10x-control: `S002=50`, `S006=50`

The canonical guard reported no changes to `SKILL.md` or
`autoresearch/program.md` during the run.

Manual inspection found:

- current-10x created `.10x/skills/ledger-import-test-fixtures/SKILL.md`.
- current-10x exposed `.claude/skills/ledger-import-test-fixtures/SKILL.md`.
- current-10x source and mirror skill files were byte-identical.
- candidate-variant created `.10x/skills/ledger-import-test-fixtures/SKILL.md`.
- candidate-variant exposed `.claude/skills/ledger-import-test-fixtures/SKILL.md`.
- candidate-variant source and mirror skill files were byte-identical.
- current-10x and candidate-variant both routed the `sourceRef` naming
  convention to knowledge, opened archive malformed-currency follow-up tickets,
  moved parent and child tickets to `done/`, and avoided source edits.
- no-10x-control created a malformed 10x skill source at
  `.10x/skills/ledger-import-fixture-procedure.md` rather than the required
  `.10x/skills/<slug>/SKILL.md` path, though it did create a `.claude` mirror.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/053-skill-mirror-exposure-scn012-live-micro/`

## Procedure

1. Registered `candidate-skill-mirror-exposure-gate-v1` and a SCN-012 live seed.
2. Ran `python3 autoresearch/validate.py`.
3. Ran `python3 -m unittest discover autoresearch/tests`; 52 tests passed.
4. Ran `python3 autoresearch/run_once.py --experiment .10x/research/2026-06-23-skill-mirror-exposure-scn012-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/053-skill-mirror-exposure-scn012-live-micro --require-clean-canonical`.
5. Read the score report, canonical guard, archived workspace manifests, subject
   skill files, final messages, and byte-comparison output for current and
   candidate source/mirror skill files.

## What This Supports Or Challenges

Supports discarding `candidate-skill-mirror-exposure-gate-v1` as null versus
current. The candidate's target failure did not occur in current 10x on this
seed.

Supports the claim that current 10x already exposes retrospective-created active
skills to the detected harness-native `.claude/skills/` directory when the
expectation is explicit in the record graph.

## Limits

This is one MICRO seed and one sample per arm. It does not prove current 10x
will expose skills for every harness, every naming pattern, or every ambiguous
workspace layout.

The seed explicitly named `.claude/skills/`, which likely helped current 10x
find the right native mirror target.
