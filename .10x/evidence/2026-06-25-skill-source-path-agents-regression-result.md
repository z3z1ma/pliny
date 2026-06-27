Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-skill-source-path-agents-regression-scn012-live-micro.md, autoresearch/candidates/2026-06-25-skill-source-path-shape.md

# Skill Source Path Agents Regression Result

## What Was Observed

Ran:

```text
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-skill-source-path-agents-regression-scn012-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/191-skill-source-path-agents-regression-scn012-live-micro --require-clean-canonical
```

The runner completed 3 live Codex subject calls for no-10x-control,
current-10x, and candidate-variant.

Automated Trust Level 1 first-pass scores:

| Arm | S002 | S006 |
| --- | ---: | ---: |
| candidate-variant | 85 | 85 |
| current-10x | 100 | 85 |
| no-10x-control | 80 | 20 |

Manual inspection of candidate artifact
`.10x/evidence/.storage/2026-06-23-skill-autoresearch/191-skill-source-path-agents-regression-scn012-live-micro/raw/sha256-154658fa6181578abafcc39b19ee327299fd4427f823e8551e0590c071815daf.json`
found:

- Candidate read the seeded
  `.agents/skills/skill-writing-governor/SKILL.md`.
- Candidate created
  `.10x/skills/ledger-import-fixture-replay/SKILL.md`.
- Candidate created the mirror
  `.agents/skills/ledger-import-fixture-replay/SKILL.md`.
- `cmp` showed the source skill and `.agents` exposure copy were
  byte-equivalent.
- `rg "\.10x/(tickets|evidence|reviews|research|specs|decisions)"` found no
  prohibited record references inside either skill copy.
- Candidate created no `.claude` or `.opencode` mirror directories.
- Candidate made no implementation edits.
- Candidate additionally created validation evidence and a blocked follow-up
  ticket for the out-of-scope archive malformed-currency gap.

The canonical guard reported `SKILL.md` and `autoresearch/program.md` unchanged
before and after the run.

## Procedure

The run used the registered EXP-991 research definition and the seeded
`.agents/skills` workspace fixture at
`autoresearch/trial-seeds/skill-authoring-agents-mirror/raw.json`.
Manual inspection checked the saved raw transcript, saved workspace file list,
source skill body, mirror body, byte comparison, prohibited-reference search,
directory tree, and canonical guard.

## What This Supports Or Challenges

Supports keeping `candidate-skill-source-path-shape-v1` alive for `.opencode`
and `.claude` mirror regressions. It shows the candidate did not weaken governed
`.agents` skill exposure while enforcing the directory-shaped source skill path.

Challenges immediate promotion: current canonical 10x also passed the `.agents`
regression in this run, and candidate scored lower than current on the
heuristic S002 score.

## Limits

This is one live Codex repetition per arm and one seeded `.agents` fixture. The
prompt and seeded governor explicitly name the required path, so this regression
proves non-regression more strongly than generalization. Promotion still depends
on the remaining `.opencode` and `.claude` mirror regressions plus final
semantic review of the candidate.
