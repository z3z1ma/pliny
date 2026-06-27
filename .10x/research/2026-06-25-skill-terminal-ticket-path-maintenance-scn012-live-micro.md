Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-965-skill-terminal-ticket-path-maintenance-scn012-live-micro

## Experiment ID

EXP-20260625-965-skill-terminal-ticket-path-maintenance-scn012-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` reliably performs terminal ticket path
maintenance during a skill-authoring parent closure. When both child and parent
tickets are done, the agent should move them to `.10x/tickets/done/` and repair
live references instead of leaving `Status: done` tickets at active top-level
paths.

## Motivation

Skill-authoring closure runs have repeatedly passed the primary skill behavior
while exposing terminal path variance. In the weak-request identity regression,
candidate repetitions sometimes left done-status tickets at top-level paths. In
the post-promotion superseded-identity gate, one current repetition left both
done-status tickets at top-level paths. This MICRO isolates that residual from
skill slug identity and mirror exposure.

## Method Tier

MICRO using a live Codex subject harness, tracked seed workspace, and five
repetitions per arm.

## Variants

- no-10x-control: minimal Codex instruction. This arm is a required runner
  comparator but is not meaningful for the terminal-path verdict because the
  runner removes `.10x/` for control isolation.
- current-10x: canonical `SKILL.md`.
- candidate-variant: duplicate current canonical `SKILL.md`, used as a
  repeatability arm. No candidate overlay is under test.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, tracked seed workspace copied as input but archived under this
experiment's output root, `--disable plugins`, and `--ignore-user-config`.

The `no-10x-control` arm is retained only to satisfy the live runner's arm
contract. Because the runner intentionally removes `.10x/` for control
isolation, the control arm removes the terminal records this MICRO tests and
must not be used for the terminal-path verdict.

No `writable_add_dirs` are configured. The subject workspace intentionally has
no harness-native skill directory.

## Scenario Set

- SCN-012: Ledger import parent closure after child completion. Existing
  records contain a done child ticket at a top-level path, active parent ticket,
  pass evidence and review, active preview spec, active skill identity knowledge,
  settled `sourceRef` vocabulary, no harness-native skill directory, and an
  out-of-scope archive malformed-currency gap.

Seed:

- `autoresearch/trial-seeds/skill-authoring-terminal-ticket-path/raw.json`

Prompt:

```text
Wrap up the Ledger import parent now. The child is done with evidence and review. Preserve the reusable fixture replay procedure, the `sourceRef` naming convention, and the archive malformed-currency follow-up in the right durable records. Use existing records to choose names and record types. Do not edit implementation files. If there is no harness-native skills directory in this workspace, do not create one.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-965-skill-terminal-ticket-path-maintenance-scn012-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 5,
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
      "prior_raw_path": "autoresearch/trial-seeds/skill-authoring-terminal-ticket-path/raw.json",
      "prompt": "Wrap up the Ledger import parent now. The child is done with evidence and review. Preserve the reusable fixture replay procedure, the `sourceRef` naming convention, and the archive malformed-currency follow-up in the right durable records. Use existing records to choose names and record types. Do not edit implementation files. If there is no harness-native skills directory in this workspace, do not create one."
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

Current and duplicate-current should infer terminal ticket movement from
canonical record rules, even though the prompt does not mention moving tickets.
They should create the source skill at
`.10x/skills/ledger-import-fixture-replay/SKILL.md`, preserve `sourceRef`
knowledge, create or update a malformed-currency follow-up owner, create
closure/validation evidence, move the child and parent tickets to
`.10x/tickets/done/`, repair live references to the moved paths, create no
harness-native mirror, and avoid implementation edits.

## Metrics To Score

Primary: manual terminal ticket path maintenance inspection. Supporting: S002
and S006.

## Quality Floors

Manual inspection is authoritative. Pass current only if every current and
duplicate-current repetition:

- creates `.10x/skills/ledger-import-fixture-replay/SKILL.md`;
- creates no alternate skill slug or flat skill file;
- creates no speculative native skill mirror;
- preserves `sourceRef` as knowledge;
- opens or updates a bounded archive malformed-currency follow-up owner;
- records closure or validation evidence with limits;
- moves both the child ticket and parent ticket to `.10x/tickets/done/` if it
  sets them to `Status: done`;
- leaves no done-status parent or child ticket at top-level `.10x/tickets/`;
- repairs live `Parent`, `Depends-On`, `Relates-To`, and `Target` references to
  terminal paths after the move;
- avoids implementation file edits.

Fail a repetition if it marks the parent or child `Status: done` but leaves the
record at a top-level active-ticket path.

## Budget And Stop Conditions

Maximum 15 live Codex calls. Timeout 7200 seconds per run. Stop after five
repetitions per arm.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/207-skill-terminal-ticket-path-maintenance-scn012-live-micro/`

## Promotion Rule

This is a conformance gate. It cannot promote a duplicate-current candidate.
If current fails terminal ticket path movement in more than one repetition, open
a narrow candidate that makes terminal record movement at closure more salient
without changing broad record graph mechanics or skill identity rules.

## Execution Log

- 2026-06-25: Registered after EXP-998 and EXP-966 both surfaced terminal ticket
  path-maintenance variance during skill-authoring closure.
- 2026-06-25: Ran 15 live Codex samples into
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/207-skill-terminal-ticket-path-maintenance-scn012-live-micro/`.
  `canonical_guard.json` reported `SKILL.md` and `autoresearch/program.md`
  unchanged during the run.
- 2026-06-25: Manual inspection found the terminal ticket path target passed in
  all current and duplicate-current repetitions: both the child and parent
  moved to `.10x/tickets/done/`, no done-status parent or child remained at
  top-level paths, live references were repaired, the exact `.10x` source skill
  was created, no native mirrors were invented, and no implementation files
  changed.
- 2026-06-25: Strict floor inspection raised a closure-evidence concern. Current
  created fresh closure or validation evidence in three of five repetitions;
  two current repetitions relied on record/coherence inspection and final-message
  claims without adding a new durable evidence record. Duplicate-current created
  fresh closure evidence in all five repetitions.

## Result

Terminal ticket path maintenance passed for current `SKILL.md`. The prior
variance from EXP-966 did not reproduce when isolated across five current and
five duplicate-current repetitions.

This run does not justify a `SKILL.md` promotion. It was a duplicate-current
conformance gate, and the only residual was not terminal movement but
closure-evidence salience under a weak wrap-up prompt.

## Evidence And Review

- `.10x/evidence/2026-06-25-skill-terminal-ticket-path-maintenance-result.md`
- `.10x/reviews/2026-06-25-skill-terminal-ticket-path-maintenance-result.md`
