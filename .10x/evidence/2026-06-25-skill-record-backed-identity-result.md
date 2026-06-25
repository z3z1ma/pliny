Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-skill-record-backed-identity-scn012-live-micro.md, autoresearch/candidates/2026-06-25-skill-record-backed-identity.md

# Skill Record-Backed Identity Result

## What was observed

Ran `EXP-20260625-997-skill-record-backed-identity-scn012-live-micro` with:

```bash
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-skill-record-backed-identity-scn012-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/197-skill-record-backed-identity-scn012-live-micro --require-clean-canonical
```

The runner wrote nine live Codex subject samples. `canonical_guard.json`
reported `SKILL.md` and `autoresearch/program.md` unchanged during the run.

Trust Level 1 telemetry recorded:

- no-10x-control: `S002=70` average, `S006=50` average;
- current-10x: `S002=85` average, `S006=70` average;
- candidate-variant: `S002=85` average, `S006=70` average.

Manual inspection found:

- candidate-variant created
  `.10x/skills/ledger-import-fixture-replay/SKILL.md` in all three
  repetitions;
- current-10x created
  `.10x/skills/ledger-import-fixture-replay/SKILL.md` in two repetitions and
  `.10x/skills/ledger-fixture-replay/SKILL.md` in one repetition;
- every candidate repetition created parent closure/validation evidence;
- candidate repetitions created no `.claude`, `.agents`, `.opencode`, or other
  speculative harness-native mirror directories;
- `rg` found no forbidden generated-skill references to `.10x/tickets`,
  `.10x/evidence`, `.10x/reviews`, `.10x/specs`, `.10x/research`, or
  `.10x/decisions`;
- candidate repetitions avoided implementation file edits.

## Procedure

Inspected:

- `report.md`;
- `summary.json`;
- `canonical_guard.json`;
- raw artifact arm/rep mapping;
- generated skill paths across all workspaces;
- candidate evidence records and parent tickets;
- harness-native mirror paths;
- forbidden `.10x` record references inside generated skills.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/197-skill-record-backed-identity-scn012-live-micro/`

## What this supports or challenges

This supports `candidate-skill-record-backed-identity-v1` improving exact skill
identity stability on the primary closure-completeness scenario where current
still drifted to a near-synonym slug.

It also supports preserving closure evidence behavior while adding the candidate
overlay.

## Limits

This is one no-native-dir fixture. The candidate is not promotion-ready until
it passes the weak-request slug-stability control and harness-native mirror
regressions for `.agents`, `.opencode`, and `.claude`.
