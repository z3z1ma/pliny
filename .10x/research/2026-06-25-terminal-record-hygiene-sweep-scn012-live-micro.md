Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-962-terminal-record-hygiene-sweep-scn012-live-micro

## Experiment ID

EXP-20260625-962-terminal-record-hygiene-sweep-scn012-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-terminal-record-hygiene-sweep-v1` improves closure
hygiene under rich skill-authoring wrap-up pressure by making terminal ticket
movement and live reference repair more salient after primary retrospective and
skill exposure work.

## Motivation

EXP-964 passed the primary multi-harness skill exposure target, but one current
and one duplicate-current repetition closed the parent while leaving an
already-done child ticket at top-level `.10x/tickets/`. EXP-965 showed terminal
movement can pass when isolated. This experiment tests whether a narrow
terminal-record hygiene overlay improves the richer combined closure case
without weakening skill behavior.

## Method Tier

MICRO using a live Codex subject harness, tracked seed workspace, and five
repetitions per arm.

## Variants

- no-10x-control: minimal Codex instruction. This arm is a required runner
  comparator but is not promotion authority.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `candidate-terminal-record-hygiene-sweep-v1`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, `--ignore-user-config`, and scoped writable add dirs for
the two existing native skill roots:

- `--add-dir <subject-workspace>/.agents/skills`
- `--add-dir <subject-workspace>/.opencode/skills`

## Scenario Set

- SCN-012: same rich Ledger import parent closure used by EXP-964. Existing
  records contain a done child ticket at a top-level path, active parent ticket,
  pass evidence and review, active preview spec, active skill identity knowledge,
  settled `sourceRef` vocabulary, skill-writing governors in `.agents/skills`
  and `.opencode/skills`, no `.claude/skills`, and an out-of-scope archive
  malformed-currency gap.

Seed:

- `autoresearch/fixtures/live-seeds/skill-authoring-multi-harness-exposure/raw.json`

Prompt:

```text
Wrap up the Ledger import parent now. The child is done with evidence and review. Preserve the reusable fixture replay procedure, the `sourceRef` naming convention, and the archive malformed-currency follow-up in the right durable records. Before authoring any skill, inspect this workspace for skill-writing governance and follow it. Expose any active skill appropriately for the harness-native skill roots that exist in this workspace. Use existing records to choose names and record types. Do not edit implementation files.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-962-terminal-record-hygiene-sweep-scn012-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-terminal-record-hygiene-sweep-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-25-terminal-record-hygiene-sweep.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-012",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/skill-authoring-multi-harness-exposure/raw.json",
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

Candidate should preserve the EXP-964 primary skill behavior while improving
terminal lifecycle behavior:

- exact source skill path;
- exact `.agents` and `.opencode` mirrors;
- byte-equivalent source and mirror files;
- no `.claude` mirror;
- no forbidden non-knowledge `.10x` references inside skill bodies;
- parent and child tickets moved to `.10x/tickets/done/`;
- no done-status parent or child left at top-level `.10x/tickets/`;
- live `Parent`, `Depends-On`, `Relates-To`, and `Target` references repaired
  to moved paths;
- no implementation file edits.

## Metrics To Score

Primary: manual terminal lifecycle and multi-harness skill inspection.
Supporting: S002, S006, and S008.

## Quality Floors

Manual inspection is authoritative. Candidate is promising only if every
candidate repetition:

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
- moves both parent and child tickets to `.10x/tickets/done/`;
- leaves no done-status parent or child at top-level `.10x/tickets/`;
- repairs live `Parent`, `Depends-On`, `Relates-To`, and `Target` references to
  moved parent and child paths;
- avoids implementation file edits.

Current is the baseline. Promote only if candidate improves terminal hygiene
without losing primary skill behavior.

## Budget And Stop Conditions

Maximum 15 live Codex calls. Timeout 7200 seconds per run. Stop after five
repetitions per arm.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/210-terminal-record-hygiene-sweep-scn012-live-micro/`

## Promotion Rule

If candidate achieves clean terminal hygiene in all repetitions and current
repeats terminal child path or live-reference failures, run at least two
regression controls before promotion: isolated terminal path maintenance and
positive closure coherence. Discard as null if current also passes cleanly and
candidate offers no measurable reliability gain.

## Execution Log

- 2026-06-25: Registered after EXP-964 reproduced terminal child-ticket movement
  variance under rich skill-authoring wrap-up pressure.
- 2026-06-25: Ran 15 live Codex subject samples, five each for no-10x-control,
  current-10x, and candidate-variant. Raw artifacts are under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/210-terminal-record-hygiene-sweep-scn012-live-micro/`.
- 2026-06-25: Manual inspection found current and candidate both clean on the
  targeted terminal-record hygiene floor. Candidate discarded as null; no
  `SKILL.md` promotion.

## Results

All samples completed without timeout. `canonical_guard.json` reported
`SKILL.md` and `autoresearch/program.md` unchanged during the run.

Trust Level 1 telemetry:

- candidate-variant: `S002=85` average, `S006=65` average;
- current-10x: `S002=85` average, `S006=65` average;
- no-10x-control: `S002=85` average, `S006=32` average.

Manual inspection found all five current repetitions and all five candidate
repetitions:

- created `.10x/skills/ledger-import-fixture-replay/SKILL.md`;
- created byte-equivalent `.agents/skills/ledger-import-fixture-replay/SKILL.md`
  and `.opencode/skills/ledger-import-fixture-replay/SKILL.md`;
- created no `.claude/skills` directory;
- left no done-status ticket at top-level `.10x/tickets/`;
- left no stale live references to the pre-move parent or child ticket paths;
- edited no implementation files.

The no-10x-control arm also passed these mechanical floors in this explicit
seed/prompt shape, so the control is not a promotion comparator here.

## Conclusion

`candidate-terminal-record-hygiene-sweep-v1` is a null result. The previous
multi-harness run exposed stochastic terminal-child movement variance, but the
canonical current arm passed the richer rerun cleanly in five of five samples.
Adding more terminal-hygiene prose to `SKILL.md` would increase instruction
surface without measured reliability gain.

This does not prove terminal lifecycle behavior is impossible to fail under
longer or different closure prompts. It does prove this specific overlay should
not be promoted.

Supporting records:

- `.10x/evidence/2026-06-25-terminal-record-hygiene-sweep-result.md`
- `.10x/reviews/2026-06-25-terminal-record-hygiene-sweep-result.md`
