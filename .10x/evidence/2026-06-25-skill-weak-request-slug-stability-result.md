Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-skill-weak-request-slug-stability-scn012-live-micro.md

# Skill Weak-Request Slug Stability Result

## What was observed

Ran `EXP-20260625-995-skill-weak-request-slug-stability-scn012-live-micro`
with:

```bash
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-skill-weak-request-slug-stability-scn012-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/195-skill-weak-request-slug-stability-scn012-live-micro --require-clean-canonical
```

The runner wrote nine live Codex subject samples: three no-10x-control, three
current-10x, and three duplicate-current candidate-variant samples.
`canonical_guard.json` reported `SKILL.md` and `autoresearch/program.md`
unchanged during the run.

Trust Level 1 telemetry recorded:

- no-10x-control: `S002=70` average, `S006=23.33` average;
- current-10x: `S002=85` average, `S006=65` average;
- candidate-variant: `S002=85` average, `S006=70` average.

Manual inspection found:

- current-10x created `.10x/skills/ledger-import-fixture-replay/SKILL.md` in
  all three repetitions;
- duplicate-current created `.10x/skills/ledger-import-fixture-replay/SKILL.md`
  in all three repetitions;
- no-10x-control created unstable flat/alternate skill paths:
  `.10x/skills/stable-ledger-import-replay.md` once and
  `.10x/skills/ledger-import-preview-replay.md` twice;
- canonical arms did not create `.claude`, `.agents`, `.opencode`, or other
  speculative harness mirror directories;
- canonical arms did not edit source implementation files;
- generated canonical skill files had valid skill frontmatter, `Use when`
  descriptions, and self-contained objective/prerequisite/procedure/validation
  sections;
- `rg` found no forbidden generated-skill references to `.10x/tickets`,
  `.10x/evidence`, `.10x/reviews`, `.10x/specs`, `.10x/research`, or
  `.10x/decisions`;
- canonical arms preserved `sourceRef` vocabulary as knowledge and opened an
  archive malformed-currency follow-up ticket.

## Procedure

Inspected:

- `report.md`;
- `summary.json`;
- `canonical_guard.json`;
- every raw fixture-shaped output JSON file;
- every workspace manifest;
- generated skill paths across every workspace;
- one representative canonical generated skill in full;
- forbidden `.10x` references inside generated skill directories;
- speculative `.claude`, `.agents`, and `.opencode` mirror paths.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/195-skill-weak-request-slug-stability-scn012-live-micro/`

## What this supports or challenges

This supports current `SKILL.md` producing stable skill identity and
directory-shaped source skill paths under a weaker retrospective request. It
also supports the promoted source-path sentence not needing an immediate
follow-up slug-stability amendment.

The run challenges the no-10x baseline: without 10x instructions, all three
control repetitions created unstable or flat skill paths despite the same
workspace and prompt.

## Limits

This covers one Ledger import skill-authoring fixture and one weak prompt shape.
It does not close the separate skill-authoring closure-completeness gap around
validation evidence and parent-ticket updates, and it does not cover ambiguous
multi-harness native directory selection.
