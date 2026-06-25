Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-996-skill-closure-completeness-scn012-live-micro

## Experiment ID

EXP-20260625-996-skill-closure-completeness-scn012-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can complete a skill-authoring retrospective
without leaving closure evidence or parent-ticket state thin. When the parent
ticket is ready to close, the agent should create the self-contained source
skill, preserve adjacent knowledge and follow-up ownership, record a parent
closure or skill-validation evidence record, update ticket status/progress
coherently, and avoid speculative harness-native mirrors.

## Motivation

Prior skill-authoring runs established correct source path shape and mirror
behavior, but closure completeness remained stochastic. In
`EXP-20260625-988-skill-authoring-agents-writable-mirror-scn012-live-micro`,
duplicate-current recorded validation evidence and updated the parent ticket
while current did not. In
`EXP-20260625-995-skill-weak-request-slug-stability-scn012-live-micro`, current
created stable skill slugs, but at least one current repetition moved the parent
to `tickets/done/` without adding a new parent-closure evidence record.

This experiment isolates the closure-completeness question instead of treating
it as a secondary scorer artifact.

## Method Tier

MICRO using a live Codex subject harness, tracked seed workspace, and three
repetitions per arm to expose stochastic parent-closure evidence variance.

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

- SCN-012: Ledger import parent closure after child completion. Existing records
  contain a done child ticket, pass review, recorded child evidence, active
  preview spec, a parent acceptance criterion requiring retrospective
  extraction, a known `sourceRef` naming convention, a reusable fixture replay
  procedure, and an out-of-scope archive malformed-currency gap.

Seed:

- `autoresearch/fixtures/live-seeds/skill-authoring-no-native-dir/raw.json`

Prompt:

```text
Finish the Ledger import parent closure now. The child ticket is done and has pass evidence and review. Preserve the reusable fixture replay procedure as the correct source skill, preserve the `sourceRef` naming convention as knowledge, open or update a bounded follow-up owner for archive malformed-currency coverage, record the closure or validation evidence needed to prove the parent closure, and move/update the parent records only if the record graph supports closure. Do not edit implementation files. If there is no harness-native skills directory in this workspace, record that fact and do not create one.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-996-skill-closure-completeness-scn012-live-micro",
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
      "prior_raw_path": "autoresearch/fixtures/live-seeds/skill-authoring-no-native-dir/raw.json",
      "prompt": "Finish the Ledger import parent closure now. The child ticket is done and has pass evidence and review. Preserve the reusable fixture replay procedure as the correct source skill, preserve the `sourceRef` naming convention as knowledge, open or update a bounded follow-up owner for archive malformed-currency coverage, record the closure or validation evidence needed to prove the parent closure, and move/update the parent records only if the record graph supports closure. Do not edit implementation files. If there is no harness-native skills directory in this workspace, record that fact and do not create one."
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

Current should inspect the parent ticket, done child ticket, child evidence,
review, active spec, knowledge, skill directories, and active ticket list. It
should create `.10x/skills/ledger-import-fixture-replay/SKILL.md`, preserve
`sourceRef` in knowledge, open or update a separate archive malformed-currency
follow-up, create a closure/validation evidence record under `.10x/evidence/`,
move or update the parent ticket to done only when every acceptance criterion is
accounted for, and avoid `.claude`, `.agents`, `.opencode`, or implementation
file edits.

## Metrics To Score

Primary: manual closure-completeness inspection. Supporting: S002, S006.

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
- records new evidence that explicitly supports parent closure or skill
  validation and names the limits of that evidence;
- updates or moves the Ledger import parent ticket so its status, progress,
  dependencies, blockers, and evidence references are coherent;
- creates no `.claude`, `.agents`, `.opencode`, or other harness mirror
  directory;
- avoids implementation file edits.

Fail an arm if it moves the parent to `tickets/done/` without a new evidence
record supporting closure or validation, even if the progress notes summarize
the work.

## Budget And Stop Conditions

Maximum 9 live Codex calls. Timeout 7200 seconds per run. Stop after three
repetitions for each arm.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/196-skill-closure-completeness-scn012-live-micro/`;
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

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/196-skill-closure-completeness-scn012-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for parent-closure evidence and record coherence.

## Manual Inspection Requirement

Inspect every repetition's workspace manifest, final message, generated skill,
knowledge/follow-up records, evidence records, parent ticket, child ticket
reference paths, and changed file set. The automated scorer is not trusted for
closure-completeness pass/fail.

## Promotion Rule

No promotion if current and duplicate-current are stable across canonical
repetitions. If canonical repetitions still move the parent to done without new
closure/validation evidence, create a narrow candidate requiring retrospective
closure that creates or updates skills to record evidence for the closure claim
before the parent ticket moves to done. Rerun this experiment plus skill
source-path and mirror regressions before promotion.

## Risks

- The prompt is more explicit than natural closure requests, so passing this
  run will not fully close weaker-prompt closure variance.
- The evidence requirement may be stricter than a minimal parent progress note,
  but it is justified because the parent closure itself is the claim under
  test.
- The no-native fixture has no harness mirror target, so this run does not
  retest `.claude`, `.agents`, or `.opencode` exposure.

## Execution Log

- 2026-06-25: Registered from the skill-authoring residual closure-completeness
  gap after slug stability passed but prior current repetitions showed uneven
  parent-closure evidence.
- 2026-06-25: Ran live Codex subject harness under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/196-skill-closure-completeness-scn012-live-micro/`.
  Canonical guard reported `SKILL.md` and `autoresearch/program.md` unchanged.
- 2026-06-25: Manual inspection found all six canonical repetitions created
  parent closure/validation evidence and avoided speculative harness-native
  mirrors. The isolated failure was skill identity drift: current rep 1 created
  `.10x/skills/replay-ledger-import-fixtures/SKILL.md`, and duplicate-current
  rep 1 created `.10x/skills/ledger-fixture-replay/SKILL.md`.

## Result

Current `SKILL.md` passes the parent closure-evidence behavior under this
explicit prompt, but fails stable record-backed skill identity. The right
follow-up is not a generic closure guardrail; it is a narrow skill identity
candidate that tells agents to preserve a workstream's established skill
slug/path/name instead of coining a near-synonym.

Automated Trust Level 1 telemetry undercounted closure quality but correctly
showed no S002 candidate advantage because slug identity is not encoded in the
generic scorer:

- current-10x: `S002=85`, `S006=65` average;
- duplicate-current candidate arm: `S002=85`, `S006=65` average;
- no-10x-control: `S002=75`, `S006=50` average.

Follow-up candidate:

- `autoresearch/candidates/2026-06-25-skill-record-backed-identity.md`

Supporting records:

- `.10x/evidence/2026-06-25-skill-closure-completeness-result.md`
- `.10x/reviews/2026-06-25-skill-closure-completeness-result.md`
