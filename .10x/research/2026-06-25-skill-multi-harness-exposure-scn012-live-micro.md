Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-964-skill-multi-harness-exposure-scn012-live-micro

## Experiment ID

EXP-20260625-964-skill-multi-harness-exposure-scn012-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can expose a newly authored project skill to all
and only the harness-native skill directories that exist in a workspace. When
multiple native roots are present, the agent should mirror the same canonical
source skill into each present root without inventing an absent root or drifting
skill identity.

## Motivation

Prior skill-authoring regressions covered `.agents`, `.opencode`, and `.claude`
one at a time. The remaining multi-harness gap is selective exposure under
partial presence: a workspace may contain more than one native skill root while
another target harness root is absent. The agent must not treat "expose to the
harness" as a single-root choice, and it must not create speculative absent
harness directories.

## Method Tier

MICRO using a live Codex subject harness, tracked seed workspace, and five
repetitions per arm.

## Variants

- no-10x-control: minimal Codex instruction. This arm is a required runner
  comparator, but it is not the promotion authority.
- current-10x: canonical `SKILL.md`.
- candidate-variant: duplicate current canonical `SKILL.md`, used as a
  repeatability arm. No candidate overlay is under test.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, `--ignore-user-config`, and scoped writable add dirs for
the two existing native skill roots:

- `--add-dir <subject-workspace>/.agents/skills`
- `--add-dir <subject-workspace>/.opencode/skills`

The seed intentionally does not contain `.claude/skills`.

## Scenario Set

- SCN-012: Ledger import parent closure after child completion. Existing
  records contain a done child ticket at a top-level path, active parent ticket,
  pass evidence and review, active preview spec, active skill identity knowledge,
  settled `sourceRef` vocabulary, skill-writing governors in `.agents/skills`
  and `.opencode/skills`, no `.claude/skills`, and an out-of-scope archive
  malformed-currency gap.

Seed:

- `autoresearch/trial-seeds/skill-authoring-multi-harness-exposure/raw.json`

Prompt:

```text
Wrap up the Ledger import parent now. The child is done with evidence and review. Preserve the reusable fixture replay procedure, the `sourceRef` naming convention, and the archive malformed-currency follow-up in the right durable records. Before authoring any skill, inspect this workspace for skill-writing governance and follow it. Expose any active skill appropriately for the harness-native skill roots that exist in this workspace. Use existing records to choose names and record types. Do not edit implementation files.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-964-skill-multi-harness-exposure-scn012-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 5,
  "writable_add_dirs": [
    ".agents/skills",
    ".opencode/skills"
  ],
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
      "instruction_source": "SKILL.md duplicate-current post-promotion",
      "instruction_path": "SKILL.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-012",
      "prior_raw_path": "autoresearch/trial-seeds/skill-authoring-multi-harness-exposure/raw.json",
      "prompt": "Wrap up the Ledger import parent now. The child is done with evidence and review. Preserve the reusable fixture replay procedure, the `sourceRef` naming convention, and the archive malformed-currency follow-up in the right durable records. Before authoring any skill, inspect this workspace for skill-writing governance and follow it. Expose any active skill appropriately for the harness-native skill roots that exist in this workspace. Use existing records to choose names and record types. Do not edit implementation files."
    }
  ],
  "budget": {
    "max_harness_runs": 15,
    "estimated_wall_seconds_per_run": 900,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Current and duplicate-current should create:

- `.10x/skills/ledger-import-fixture-replay/SKILL.md`;
- `.agents/skills/ledger-import-fixture-replay/SKILL.md`;
- `.opencode/skills/ledger-import-fixture-replay/SKILL.md`.

The three files should be byte-equivalent. The agent should not create
`.claude/skills`, alternate skill slugs, flat skill files, or implementation
edits. It should preserve `sourceRef` as knowledge and create or update a
bounded archive malformed-currency follow-up owner.

## Metrics To Score

Primary: manual multi-harness exposure inspection. Supporting: S002, S006, and
S008.

## Quality Floors

Manual inspection is authoritative. Pass current only if every current and
duplicate-current repetition:

- creates `.10x/skills/ledger-import-fixture-replay/SKILL.md`;
- creates `.agents/skills/ledger-import-fixture-replay/SKILL.md`;
- creates `.opencode/skills/ledger-import-fixture-replay/SKILL.md`;
- keeps source, `.agents`, and `.opencode` skill contents byte-equivalent;
- creates no `.claude/skills` directory or `.claude` mirror;
- creates no alternate skill slug or flat skill file for the Ledger import
  fixture replay procedure;
- avoids forbidden references to `.10x/tickets`, `.10x/evidence`,
  `.10x/reviews`, `.10x/specs`, `.10x/research`, and `.10x/decisions` inside
  authored skill bodies;
- preserves `sourceRef` as knowledge;
- opens or updates a bounded archive malformed-currency follow-up owner;
- avoids implementation file edits.

Closure evidence and terminal ticket movement should be inspected as supporting
signals, but they are not primary floors for this micro.

## Budget And Stop Conditions

Maximum 15 live Codex calls. Timeout 7200 seconds per run. Stop after five
repetitions per arm.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/208-skill-multi-harness-exposure-scn012-live-micro/`

## Promotion Rule

This is a conformance gate. It cannot promote a duplicate-current candidate.
If current fails by omitting one existing native root, inventing `.claude`, or
drifting source/mirror identity in more than one repetition, open a narrow
candidate that makes "all and only existing harness-native skill roots" more
salient without changing skill record ontology or broad retrospective behavior.

## Execution Log

- 2026-06-25: Registered after EXP-965 removed terminal ticket path maintenance
  as a primary skill-authoring gap and left ambiguous multi-harness exposure as
  the next runnable CLI lane.
- 2026-06-25: Ran 15 live Codex samples into
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/208-skill-multi-harness-exposure-scn012-live-micro/`.
  `canonical_guard.json` reported `SKILL.md` and `autoresearch/program.md`
  unchanged during the run.
- 2026-06-25: Manual inspection found the multi-harness exposure target passed
  in all current and duplicate-current repetitions: source skill plus `.agents`
  and `.opencode` mirrors existed, all three were byte-equivalent, no `.claude`
  mirror was invented, no alternate skill slug appeared, no forbidden
  non-knowledge `.10x` references appeared inside skill bodies, `sourceRef`
  knowledge and archive malformed-currency follow-up ownership were preserved,
  and no implementation files changed.
- 2026-06-25: Supporting lifecycle inspection found residual terminal movement
  variance outside the primary floor. One current repetition and one
  duplicate-current repetition closed the parent but left the already-done child
  ticket at top-level `.10x/tickets/`; all repetitions created fresh closure or
  validation evidence.

## Result

Current `SKILL.md` passes the ambiguous multi-harness exposure gate. It can
mirror a governed source skill into more than one existing harness-native skill
root while avoiding absent-root invention.

This run does not justify a `SKILL.md` promotion. The duplicate-current arm
matched current on the primary target, and the control also performed the
mechanical mirror behavior because the seed and prompt contained explicit
governance. The durable value is conformance breadth, not a candidate win.

The run does preserve a residual lifecycle signal: terminal child-ticket
movement and reference repair are still stochastic when the prompt combines
skill authoring, multi-harness exposure, closure evidence, and parent wrap-up.

## Evidence And Review

- `.10x/evidence/2026-06-25-skill-multi-harness-exposure-result.md`
- `.10x/reviews/2026-06-25-skill-multi-harness-exposure-result.md`
