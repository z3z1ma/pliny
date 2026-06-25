Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-skill-authoring-agents-writable-mirror-scn012-live-micro.md, .10x/tickets/done/2026-06-25-allow-codex-subject-writable-add-dirs.md

# Skill Authoring Agents Writable Mirror Result

## What Was Observed

Ran `EXP-20260625-988-skill-authoring-agents-writable-mirror-scn012-live-micro`
with the Codex live subject runner.

Artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/188-skill-authoring-agents-writable-mirror-scn012-live-micro/`

The run completed all three arms:

| Arm | S002 | S006 | Manual result |
| --- | ---: | ---: | --- |
| current-10x | 80 | 85 | pass |
| candidate-variant | 85 | 85 | pass; duplicate-current arm with richer closure records |
| no-10x-control | 80 | 20 | partial; source/mirror skill created, closure coherence weak |

Manual inspection found current `SKILL.md`:

- read `.agents/skills/skill-writing-governor/SKILL.md`;
- created `.10x/skills/ledger-import-fixture-replay/SKILL.md`;
- created `.agents/skills/ledger-import-fixture-replay/SKILL.md`;
- produced byte-equivalent source and mirror skill files;
- used valid YAML frontmatter with `name`, `description`, and
  `metadata.created`/`metadata.updated`;
- started the description with `Use when`;
- included `Objective`, `Prerequisites`, `Procedure`, and `Validation`;
- avoided `.10x/tickets`, `.10x/evidence`, `.10x/reviews`, `.10x/specs`,
  `.10x/research`, and `.10x/decisions` references inside the skill body;
- referenced `.10x/knowledge/ledger-import-terms.md` only for shared
  vocabulary;
- avoided source implementation edits and speculative `.claude` or `.opencode`
  mirrors.

The duplicate-current arm also created
`.10x/evidence/2026-06-25-ledger-import-fixture-replay-skill-validation.md` in
the subject workspace and updated the subject Ledger parent ticket to replace a
stale `.claude/skills` note with `.agents/skills`. Current did not create those
closure-supporting records.

`canonical_guard.json` reported `unchanged_during_run: true` for `SKILL.md` and
`autoresearch/program.md`.

## Procedure

Command run from `/Users/alexanderbutler/code_projects/personal/10x`:

```bash
python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-skill-authoring-agents-writable-mirror-scn012-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/188-skill-authoring-agents-writable-mirror-scn012-live-micro --require-clean-canonical
```

Manual inspection steps:

- inspected raw artifacts, score artifacts, workspace manifests, and the score
  report;
- compared each arm's `.10x` source skill and `.agents` mirror for byte
  equivalence;
- checked skill frontmatter and required sections;
- searched skill bodies for prohibited `.10x` record-category references;
- inspected tool invocations for the seeded governor read;
- inspected changed file lists for implementation edits and speculative mirrors.

## What This Supports Or Challenges

This supports marking current `SKILL.md` as passing `.agents/skills` governed
skill authoring and harness mirroring once the subject runner permits scoped
writes to `.agents/skills`.

It challenges treating the earlier
`.10x/evidence/2026-06-24-skill-authoring-agents-mirror-confounder.md` result
as product evidence. The prior result was a harness write-boundary confounder.

It also surfaces a residual stochastic completeness issue: current may satisfy
the core skill/mirror contract without creating explicit subject evidence or
updating a related parent ticket, even when a duplicate-current run does so.

## Limits

This is still a Codex CLI file-layout test, not a live Agents runtime test.
Codex may load `.agents/skills` entries as skills during the subject run; that
is part of the harness-native surface under test.

The prompt explicitly named governance and harness exposure, so the run proves
current can comply on this surface, not that it will always infer the same need
from a much weaker request.
