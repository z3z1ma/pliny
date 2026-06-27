Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-952-skill-mirror-divergent-repair-scn012-live-micro

## Experiment ID

EXP-20260624-952-skill-mirror-divergent-repair-scn012-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can repair a stale harness-native skill exposure
copy from the canonical `.10x/skills` source without treating the stale mirror
as authority, creating a new skill, or editing implementation files.

## Motivation

Existing skill-authoring coverage verifies first-time creation and mirroring
for `.claude` and `.opencode` subject workspaces. It does not yet verify the
record-lifecycle case where a source skill already exists and a harness-native
mirror has drifted. The researcher backlog calls out skill creation and harness
mirroring conformance as partial-strong, with divergent mirror repair still
untested.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: duplicate canonical `SKILL.md` conformance-probe arm. No
  candidate overlay is under test.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-012: canonical Ledger import fixture replay skill exists, but the
  `.opencode` exposure copy is stale and contradicts current terminology and
  validation steps.

Seed:

- `autoresearch/trial-seeds/skill-mirror-divergent-repair/raw.json`

Prompt:

```text
The Ledger import fixture replay skill may have a stale OpenCode exposure copy. Inspect the subject workspace, use any existing skill-writing governance that applies, and repair harness-native exposure only if needed.

Treat `.10x/skills/ledger-import-fixture-replay/SKILL.md` as the canonical source skill if it exists. Do not create a new skill or speculative mirrors. Do not edit implementation files. This is a subject workspace only.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-952-skill-mirror-divergent-repair-scn012-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 1,
  "arms": [
    {
      "id": "no-10x-control",
      "instruction_source": "minimal harness defaults",
      "instruction_text": "You are a coding agent. Answer the user's task directly."
    },
    {
      "id": "current-10x",
      "instruction_source": "SKILL.md",
      "instruction_path": "SKILL.md"
    },
    {
      "id": "candidate-variant",
      "instruction_source": "SKILL.md duplicate conformance probe",
      "instruction_path": "SKILL.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-012",
      "prior_raw_path": "autoresearch/trial-seeds/skill-mirror-divergent-repair/raw.json",
      "prompt": "The Ledger import fixture replay skill may have a stale OpenCode exposure copy. Inspect the subject workspace, use any existing skill-writing governance that applies, and repair harness-native exposure only if needed.\n\nTreat `.10x/skills/ledger-import-fixture-replay/SKILL.md` as the canonical source skill if it exists. Do not create a new skill or speculative mirrors. Do not edit implementation files. This is a subject workspace only."
    }
  ],
  "budget": {
    "max_harness_runs": 3,
    "estimated_wall_seconds_per_run": 900,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Current should inspect the source skill, the `.opencode` mirror, and the seeded
governor; detect that the mirror uses stale `externalId`, inline fixture, and
wall-clock-date semantics; repair
`.opencode/skills/ledger-import-fixture-replay/SKILL.md` to match the canonical
`.10x/skills/ledger-import-fixture-replay/SKILL.md`; validate equivalence; and
avoid implementation edits, new skills, and speculative `.claude` or `.agents`
mirrors.

## Metrics To Score

Primary: manual source/mirror drift inspection. Supporting: S002, S006, and
S008.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm treats the
stale mirror as canonical, changes the `.10x` source to match the stale mirror,
creates a second skill, creates speculative harness directories, edits
implementation files, omits equivalence validation, or leaves the source and
mirror divergent.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
mirror-repair turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/152-skill-mirror-divergent-repair-scn012-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.opencode/skills/ledger-import-fixture-replay/SKILL.md`;
- subject workspace evidence/ticket updates only if the arm records why a
  durable owner is needed.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- source implementation files;
- subject workspace `.10x/skills/ledger-import-fixture-replay/SKILL.md` unless
  the arm records a specific source corruption discovered by inspection;
- subject workspace `.claude/skills` or `.agents/skills` mirrors.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/152-skill-mirror-divergent-repair-scn012-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for mirror repair quality.

## Manual Inspection Requirement

Pass an arm only if it:

- reads the canonical `.10x` source skill when available;
- reads the existing `.opencode` mirror;
- reads or accounts for the seeded skill-writing governor;
- identifies the `.opencode` copy as stale or divergent;
- leaves the `.10x` source skill intact;
- repairs `.opencode/skills/ledger-import-fixture-replay/SKILL.md` to
  equivalent content from the `.10x` source;
- validates equivalence through `cmp`, digest comparison, or exact content
  inspection;
- avoids new skill slugs, speculative harness mirrors, and implementation file
  edits.

Fail or downgrade if it edits the source skill to stale semantics, accepts
`externalId` as current terminology, leaves source and mirror divergent, creates
new mirrors for absent harnesses, or treats the prior assistant claim as
evidence without inspecting files.

## Promotion Rule

Promote only if current fails divergent mirror repair in a way a narrow
candidate can fix. A promotion would need regression controls showing first-time
`.opencode` skill creation and skill-vs-knowledge routing still pass.

## Risks

- The prompt explicitly names the canonical source path, so a pass is positive
  conformance coverage, not necessarily a strong differential versus control.
- no-10x-control removes inherited `.10x` records by design, so its failure to
  repair from source is not directly comparable.
- `.opencode/skills` is a file-layout proxy under Codex CLI, not a live
  OpenCode runtime.

## Execution Log

- 2026-06-24: Registered after the researcher backlog and coverage map
  identified divergent mirror repair as an untested skill-mirroring edge.
- 2026-06-24: Ran live under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/152-skill-mirror-divergent-repair-scn012-live-micro/`.
  Trust Level 1 scoring gave current and duplicate-current low `S002=45` and
  `S006=30` because the scorer expected broader SCN-012 retrospective graph
  behavior, but manual inspection is authoritative for this mirror-repair
  scenario.
- 2026-06-24: Manual inspection found current and duplicate-current both passed
  the divergent mirror repair behavior. Each inspected the canonical source and
  OpenCode mirror, repaired only
  `.opencode/skills/ledger-import-fixture-replay/SKILL.md`, left the canonical
  `.10x` source unchanged, validated byte equivalence with `cmp=0`, found no
  forbidden skill references to `.10x/tickets`, `.10x/evidence`,
  `.10x/reviews`, `.10x/research`, `.10x/specs`, or `.10x/decisions`, and
  avoided speculative mirrors and implementation edits.
- 2026-06-24: no-10x-control had inherited `.10x` removed by runner isolation,
  correctly made no repair without a canonical source, and created no new skill
  or speculative mirror.

## Result

Current `SKILL.md` passes this divergent OpenCode skill-mirror repair MICRO.
No canonical `SKILL.md` promotion is justified.

Supporting records:

- `.10x/evidence/2026-06-24-skill-mirror-divergent-repair-result.md`
- `.10x/reviews/2026-06-24-skill-mirror-divergent-repair-result.md`
