Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-skill-source-path-opencode-regression-scn012-live-micro.md, autoresearch/candidates/2026-06-25-skill-source-path-shape.md

# Skill Source Path OpenCode Regression Result

## What Was Observed

Ran:

```text
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-skill-source-path-opencode-regression-scn012-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/192-skill-source-path-opencode-regression-scn012-live-micro --require-clean-canonical
```

The runner completed 3 live Codex subject calls for no-10x-control,
current-10x, and candidate-variant.

Automated Trust Level 1 first-pass scores:

| Arm | S002 | S006 |
| --- | ---: | ---: |
| candidate-variant | 85 | 85 |
| current-10x | 85 | 85 |
| no-10x-control | 80 | 20 |

Manual inspection of candidate artifact
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/192-skill-source-path-opencode-regression-scn012-live-micro/raw/sha256-dd85f49887d406755055acde9701f088c0a288ed53fa559fb0baf15755f3533a.json`
found:

- Candidate read the seeded
  `.opencode/skills/skill-writing-governor/SKILL.md`.
- Candidate created
  `.10x/skills/ledger-import-fixture-replay/SKILL.md`.
- Candidate created the OpenCode mirror
  `.opencode/skills/ledger-import-fixture-replay/SKILL.md`.
- `cmp` showed the source skill and `.opencode` exposure copy were
  byte-equivalent.
- `rg "\.10x/(tickets|evidence|reviews|research|specs|decisions)"` found no
  prohibited record references inside either skill copy.
- Candidate created no `.agents` or `.claude` mirror directories.
- Candidate made no implementation edits.
- Candidate additionally recorded validation evidence, updated the subject
  parent ticket for the actual `.opencode/skills` exposure directory, and opened
  a blocked follow-up ticket for the out-of-scope archive malformed-currency
  gap.

The canonical guard reported `SKILL.md` and `autoresearch/program.md` unchanged
before and after the run.

## Procedure

The run used the registered EXP-992 research definition and the seeded
OpenCode workspace fixture at
`autoresearch/trial-seeds/skill-authoring-opencode-mirror/raw.json`.
Manual inspection checked the saved raw transcript, saved workspace file list,
source skill body, mirror body, byte comparison, prohibited-reference search,
directory tree, and canonical guard.

## What This Supports Or Challenges

Supports keeping `candidate-skill-source-path-shape-v1` alive for the final
`.claude` mirror regression. It shows the candidate did not weaken governed
OpenCode skill exposure while enforcing the directory-shaped source skill path.

Challenges immediate promotion: current canonical 10x also passed the
`.opencode` regression in this run.

## Limits

This is one live Codex repetition per arm and one seeded `.opencode` fixture.
The prompt and seeded governor explicitly name the required path, so this
regression proves non-regression more strongly than generalization. Promotion
still depends on the `.claude` regression and final semantic review of the
candidate.
