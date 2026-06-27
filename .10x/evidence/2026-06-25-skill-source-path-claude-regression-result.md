Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-skill-source-path-claude-regression-scn012-live-micro.md, autoresearch/candidates/2026-06-25-skill-source-path-shape.md, SKILL.md

# Skill Source Path Claude Regression Result

## What Was Observed

Ran:

```text
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-skill-source-path-claude-regression-scn012-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/193-skill-source-path-claude-regression-scn012-live-micro --require-clean-canonical
```

The runner completed 3 live Codex subject calls for no-10x-control,
current-10x, and candidate-variant.

Automated Trust Level 1 first-pass scores:

| Arm | S002 | S006 |
| --- | ---: | ---: |
| candidate-variant | 100 | 85 |
| current-10x | 85 | 85 |
| no-10x-control | 80 | 20 |

Manual inspection of candidate artifact
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/193-skill-source-path-claude-regression-scn012-live-micro/raw/sha256-55568273a07e589d01b8809a75c43557c9a3fa0c8c08057169a83daa0e9c72b8.json`
found:

- Candidate read the seeded
  `.claude/skills/skill-writing-governor/SKILL.md`.
- Candidate created
  `.10x/skills/ledger-import-fixture-replay/SKILL.md`.
- Candidate created the Claude mirror
  `.claude/skills/ledger-import-fixture-replay/SKILL.md`.
- `cmp` showed the source skill and `.claude` exposure copy were
  byte-equivalent.
- `rg "\.10x/(tickets|evidence|reviews|research|specs|decisions)"` found no
  prohibited record references inside either skill copy.
- Candidate created no `.agents` or `.opencode` mirror directories.
- Candidate made no implementation edits.
- Candidate additionally opened a blocked follow-up ticket for the out-of-scope
  archive malformed-currency gap.

The canonical guard reported `SKILL.md` and `autoresearch/program.md` unchanged
before and after the run.

## Procedure

The run used the registered EXP-993 research definition and the seeded Claude
workspace fixture at
`autoresearch/trial-seeds/skill-authoring-governor-mirror/raw.json`.
Manual inspection checked the saved raw transcript, saved workspace file list,
source skill body, mirror body, byte comparison, prohibited-reference search,
directory tree, and canonical guard.

## What This Supports Or Challenges

Supports promoting `candidate-skill-source-path-shape-v1` into `SKILL.md` after
EXP-990 showed a real no-native-dir source-path improvement and EXP-991,
EXP-992, and EXP-993 cleared `.agents`, `.opencode`, and `.claude` mirror
regressions.

Challenges remaining: the candidate does not fully prove weak-request slug
stability because all mirror regressions use seeded governors naming the slug.
The promoted line is therefore limited to source-path shape, not slug-selection
semantics.

## Limits

This is one live Codex repetition per arm and one seeded `.claude` fixture. The
prompt and seeded governor explicitly name the required path, so this regression
proves non-regression more strongly than generalization.
