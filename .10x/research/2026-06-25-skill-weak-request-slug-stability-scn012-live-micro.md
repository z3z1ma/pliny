Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-995-skill-weak-request-slug-stability-scn012-live-micro

## Experiment ID

EXP-20260625-995-skill-weak-request-slug-stability-scn012-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` creates a stable, record-backed skill identity
when the user gives a weaker retrospective request. The agent should derive the
skill slug from the durable Ledger import fixture replay capability, create
`.10x/skills/ledger-import-fixture-replay/SKILL.md`, avoid near-synonym slug
drift, avoid speculative harness mirrors, and preserve adjacent retrospective
items in the correct record types.

## Motivation

`candidate-skill-source-path-shape-v1` was promoted only for directory-shaped
source skill paths. Its promotion review explicitly left weak-request slug
stability open after one EXP-990 candidate repetition created
`.10x/skills/replay-ledger-import-fixtures/SKILL.md`. Path shape is now fixed;
this experiment asks whether canonical `SKILL.md` is also stable about skill
identity when the prompt does not spell out the exact slug.

## Method Tier

MICRO using a live Codex subject harness, tracked seed workspace, and three
repetitions per arm to expose stochastic slug variance.

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

No `writable_add_dirs` are configured. The subject workspace intentionally has
no harness-native skill directory.

## Scenario Set

- SCN-012: weakly phrased Ledger import retrospective request. Existing records
  name repeated fixture replay friction, `sourceRef` vocabulary, and an archive
  malformed-currency follow-up. The prompt asks the agent to wrap up the parent
  without spelling the desired skill slug.

Seed:

- `autoresearch/trial-seeds/skill-authoring-no-native-dir/raw.json`

Prompt:

```text
Wrap up the Ledger import parent now. The child surfaced one reusable replay habit, one naming convention, and one archive-import gap. Preserve each in the right durable place, using the existing records to choose names and record types. Do not edit implementation files. If there is no harness-native skills directory in this workspace, do not create one.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-995-skill-weak-request-slug-stability-scn012-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 3,
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
      "prior_raw_path": "autoresearch/trial-seeds/skill-authoring-no-native-dir/raw.json",
      "prompt": "Wrap up the Ledger import parent now. The child surfaced one reusable replay habit, one naming convention, and one archive-import gap. Preserve each in the right durable place, using the existing records to choose names and record types. Do not edit implementation files. If there is no harness-native skills directory in this workspace, do not create one."
    }
  ],
  "budget": {
    "max_harness_runs": 9,
    "estimated_wall_seconds_per_run": 900,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Current should inspect the parent ticket, child ticket, evidence/review, and
knowledge record. It should create a self-contained source skill at
`.10x/skills/ledger-import-fixture-replay/SKILL.md`, update or preserve
knowledge for `sourceRef`, open a follow-up for archive malformed-currency
coverage, update the parent progress/closure state as supported, and avoid
source edits plus speculative mirror directories.

Slug alternatives such as `replay-ledger-import-fixtures`, `ledger-import-replay`,
or flat-file `.10x/skills/<slug>.md` should count as failures for this
experiment because the durable capability is the Ledger import fixture replay
procedure already named by the workstream.

## Metrics To Score

Primary: manual skill identity and retrospective routing inspection. Supporting:
S008, S002, S006.

## Quality Floors

Manual inspection is authoritative. Pass an arm only if it:

- creates `.10x/skills/ledger-import-fixture-replay/SKILL.md`;
- does not create any alternate skill slug or flat skill file;
- uses valid skill frontmatter with `name`, `description`, and
  `metadata.created`/`metadata.updated`;
- starts `description` with `Use when`;
- includes self-contained `Objective`, `Prerequisites`, `Procedure`, and
  `Validation` sections;
- avoids references from the skill to `.10x/tickets`, `.10x/evidence`,
  `.10x/reviews`, `.10x/specs`, `.10x/research`, or `.10x/decisions`;
- preserves the `sourceRef` naming convention as knowledge, not as a skill;
- opens or updates a bounded follow-up owner for archive malformed-currency
  coverage;
- creates no `.claude`, `.agents`, `.opencode`, or other harness mirror
  directory;
- avoids implementation file edits.

## Budget And Stop Conditions

Maximum 9 live Codex calls. Timeout 7200 seconds per run. Stop after three
repetitions for each arm.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/195-skill-weak-request-slug-stability-scn012-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x/skills/`, `.10x/knowledge/`, `.10x/tickets/`,
  `.10x/evidence/`, and closure records as needed.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- source implementation files;
- subject workspace `.claude/skills/`, `.agents/skills`, `.opencode/skills`,
  or other speculative harness mirror directories.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/195-skill-weak-request-slug-stability-scn012-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for slug stability and retrospective routing.

## Manual Inspection Requirement

Inspect every repetition's workspace manifest, final message, generated skill,
knowledge/follow-up records, parent ticket updates, and changed file set. The
automated scorer is not trusted for slug identity.

## Promotion Rule

No promotion if current is stable across canonical repetitions. If current or
duplicate-current creates alternate slugs or flat files while otherwise routing
records correctly, create a narrow candidate around record-backed skill identity
and rerun this experiment plus the `.agents`, `.opencode`, `.claude`, and
no-native-dir source-path regressions before promotion.

## Risks

- The exact slug floor is stricter than generic skill naming guidance. That is
  intentional because this experiment targets record-backed identity stability,
  not arbitrary acceptable naming.
- The prompt is broader than source-path experiments, so failures may mix slug
  instability with retrospective routing misses.
- Three repetitions improve stochastic signal but are not exhaustive.

## Execution Log

- 2026-06-25: Registered after the source-path promotion left weak-request slug
  stability as the next skill-authoring risk.
- 2026-06-25: Ran live Codex subject harness under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/195-skill-weak-request-slug-stability-scn012-live-micro/`.
  Canonical guard reported `SKILL.md` and `autoresearch/program.md` unchanged.
- 2026-06-25: Manual inspection found current and duplicate-current passed slug
  stability across all six canonical repetitions. Every canonical repetition
  created `.10x/skills/ledger-import-fixture-replay/SKILL.md`, created no
  alternate skill slug, and created no speculative harness mirror directory.

## Results

Trust Level 1 telemetry:

- no-10x-control: `S002=70` average, `S006=23.33` average
- current-10x: `S002=85` average, `S006=65` average
- candidate-variant: `S002=85` average, `S006=70` average

Manual slug/path result:

- current-10x: 3/3 correct `.10x/skills/ledger-import-fixture-replay/SKILL.md`
  source skills, 0/3 alternate slugs, 0/3 flat skill files, 0/3 speculative
  mirrors.
- duplicate-current candidate arm: 3/3 correct
  `.10x/skills/ledger-import-fixture-replay/SKILL.md` source skills, 0/3
  alternate slugs, 0/3 flat skill files, 0/3 speculative mirrors.
- no-10x-control: 0/3 correct source skill paths. It created
  `.10x/skills/stable-ledger-import-replay.md` once and
  `.10x/skills/ledger-import-preview-replay.md` twice.

Manual record-routing result:

- Canonical arms preserved the replay habit as a skill, kept `sourceRef`
  vocabulary in `.10x/knowledge/ledger-import-terms.md`, opened an archive
  malformed-currency follow-up ticket, moved parent/child tickets to
  `.10x/tickets/done/`, repaired evidence/review references, and avoided source
  implementation edits.
- Canonical skill files used valid frontmatter, `Use when` descriptions, and
  self-contained `Objective`, `Prerequisites`, `Procedure`, and `Validation`
  sections.
- `rg` found no forbidden references from generated skill files to
  `.10x/tickets`, `.10x/evidence`, `.10x/reviews`, `.10x/specs`,
  `.10x/research`, or `.10x/decisions`.
- `find` found no `.claude`, `.agents`, or `.opencode` mirror directories in
  any workspace.

S006 undercounted the canonical arms because the scorer expects certain closure
tokens and cannot judge selective reference repair or existing evidence/review
reuse in this skill-authoring scenario. Manual inspection is authoritative.

Supporting records:

- `.10x/evidence/2026-06-25-skill-weak-request-slug-stability-result.md`
- `.10x/reviews/2026-06-25-skill-weak-request-slug-stability-result.md`

## Conclusions

Current `SKILL.md` passes weak-request skill slug stability. The recently
promoted source-path sentence plus existing skill-record prose is sufficient for
this Ledger import fixture replay scenario; no new `SKILL.md` candidate or
promotion is justified.

Remaining skill-authoring risk is not slug stability. The next skill lane should
target closure-completeness variance around validation evidence/parent-ticket
updates or an ambiguous multi-harness workspace.
