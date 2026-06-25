Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-skill-authoring-no-native-dir-scn012-live-micro.md

# Skill Authoring No Native Dir Result

## What Was Observed

Ran `EXP-20260625-989-skill-authoring-no-native-dir-scn012-live-micro` with the
Codex live subject runner.

Artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/189-skill-authoring-no-native-dir-scn012-live-micro/`

The run completed all three arms:

| Arm | S002 | S006 | Manual result |
| --- | ---: | ---: | --- |
| current-10x | 100 | 65 | pass; S006 false negative for intentionally active parent |
| candidate-variant | 30 | 65 | fail; duplicate-current wrote wrong skill source path |
| no-10x-control | 80 | 20 | partial; source skill created, closure coherence weak |

Manual inspection found current `SKILL.md`:

- created `.10x/skills/ledger-import-fixture-replay/SKILL.md`;
- used valid skill YAML frontmatter;
- started the description with `Use when`;
- included `Objective`, `Prerequisites`, `Procedure`, and `Validation`;
- avoided disallowed `.10x` record-category references inside the skill body;
- updated `.10x/tickets/2026-06-23-ledger-import-parent.md` to record that no
  harness-native skill exposure target exists;
- created no `.claude`, `.agents`, `.opencode`, or other mirror directory;
- avoided implementation edits.

Manual inspection found duplicate-current:

- avoided speculative mirror directories;
- wrote `.10x/skills/ledger-import-fixture-replay.md`;
- did not create the required
  `.10x/skills/ledger-import-fixture-replay/SKILL.md` source path;
- therefore failed the manual skill source-path shape floor.

`canonical_guard.json` reported `unchanged_during_run: true` for `SKILL.md` and
`autoresearch/program.md`.

## Procedure

Command run from `/Users/alexanderbutler/code_projects/personal/10x`:

```bash
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-skill-authoring-no-native-dir-scn012-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/189-skill-authoring-no-native-dir-scn012-live-micro --require-clean-canonical
```

Manual inspection steps:

- inspected score report, raw artifacts, workspace manifests, and canonical
  guard;
- checked each workspace for `.10x/skills/ledger-import-fixture-replay/SKILL.md`;
- checked for speculative `.claude`, `.agents`, `.opencode`, and other mirror
  directories;
- inspected skill frontmatter and required sections;
- searched skill bodies for prohibited `.10x` record-category references;
- inspected changed file lists for implementation edits.

## What This Supports Or Challenges

This supports current `SKILL.md` handling no-native-dir behavior in at least one
live run: it preserved the source skill and did not invent mirror directories.

It challenges robustness of the source skill path shape. The duplicate-current
arm used a flat `.10x/skills/<slug>.md` file, which is not the expected
directory-shaped skill source.

## Limits

The prompt explicitly forbade speculative mirrors, so this is a control, not a
proof that weak requests always avoid mirror creation.

The duplicate-current failure does not show that a candidate improves behavior.
It only identifies a targeted hypothesis worth testing.
