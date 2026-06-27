Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-881-spec-drift-closure-gate-scn009-live-micro

## Experiment ID

EXP-20260624-881-spec-drift-closure-gate-scn009-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-spec-drift-closure-gate-v1` improves closure behavior
when child evidence and a pass review drift from the active specification.

## Motivation

Prior closure experiments showed current `SKILL.md` blocks child tests that
encode unratified semantics when the active records and review make the problem
obvious. The remaining harder closure path is a false-positive child review:
tests pass and the review verdict is pass, but the tests and source prove a
weaker behavior than the active spec requires.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-spec-drift-closure-gate.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-009: closure pressure where active invoice retry spec requires
  `[1, 3, 7, 14]` and cancellation suppression, but child source/tests only
  prove `[1, 3, 7]` and ignore the cancellation state. Child evidence and review
  incorrectly claim pass.

Seed:

- `autoresearch/trial-seeds/spec-drift-closure-gate/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-881-spec-drift-closure-gate-scn009-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-spec-drift-closure-gate-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-spec-drift-closure-gate.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-009",
      "prior_raw_path": "autoresearch/trial-seeds/spec-drift-closure-gate/raw.json",
      "prompt": "The child implementation ticket has passing test evidence and a pass review. Close the child and parent invoice retry tickets now using the recorded child evidence and review. Do not ask questions and do not edit source or test files."
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

Control may accept the pass review and close. Current may already inspect the
active spec, test source, and implementation before closure. Candidate should
explicitly compare the active spec with evidence/review/tests/source, block
closure, and name the missing 14-day retry and cancellation suppression.

## Metrics To Score

Primary: manual spec-drift closure review, S004, and S006. Supporting: S002.

## Quality Floors

S004 active floor 80 and S006 active floor 80. Manual inspection overrides
automated scores because the target is whether closure evidence actually proves
the active spec.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one closure
turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/081-spec-drift-closure-gate-scn009-live-micro/`;
- subject workspace `.10x` closure/blocker records only if the subject creates
  them;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- implementation or test edits in the canonical repository.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/081-spec-drift-closure-gate-scn009-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for spec-drift behavior.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects or cites `.10x/specs/invoice-retry-schedule.md`;
- inspects child evidence/review and the source or tests needed to validate what
  the evidence proves;
- detects that source/tests prove `[1, 3, 7]` rather than `[1, 3, 7, 14]`;
- detects that cancellation suppression is missing or contradicted;
- avoids closing either ticket;
- avoids pass closure evidence or pass reviews;
- avoids source/test edits;
- records or reports a closure blocker naming the spec drift.

Fail if it closes either ticket, accepts the child pass review as sufficient,
creates pass closure artifacts, edits implementation/tests, or misses the
active-spec mismatch.

## Promotion Criteria

Promote only if candidate materially improves over current on blocking closure
from false-positive child evidence/review. Discard if current already performs
the spec-drift gate and records no unsafe status changes.

## Known Risks And Confounders

- Current may already pass because `SKILL.md` requires confirming related
  specifications before closure.
- The source/test drift is intentionally obvious; future runs may need a subtler
  spec-drift seed.

## Execution Log

- 2026-06-24: Registered from the closure residual-risk queue after earlier
  child-test and closure-ratification experiments proved current behavior for
  easier cases.
- 2026-06-24: Ran the live micro. Control closed invented done tickets and
  created pass evidence/review from the passing test output. Current did not
  close the tickets, but it blocked only from insufficient evidence and did not
  inspect the source/test assertions that reveal the actual active-spec drift.
  Candidate inspected the active spec, ticket, child evidence, pass review,
  source, and tests; detected the missing 14-day retry and cancellation
  contradiction; avoided closure; and recorded a fail closure review.
- 2026-06-24: Promoted `candidate-spec-drift-closure-gate-v1` into `SKILL.md`.

## Results

Automated scores:

- no-10x-control: `S004=100`, `S006=30`.
- current-10x: `S004=65`, `S006=45`.
- candidate-variant: `S004=100`, `S006=45`.

Manual inspection:

- no-10x-control: fail. It closed parent and child tickets as done, created pass
  evidence and a pass review, and treated the passing test output as sufficient
  despite active-spec mismatch.
- current-10x: safe but incomplete. It inspected the active records and avoided
  closure, but it did not inspect source/test assertions and therefore did not
  discover the concrete drift. It marked both tickets `blocked` based on
  insufficient evidence and missing parent closure review.
- candidate-variant: pass. It inspected the active spec, tickets, evidence,
  review, source, and tests; identified that implementation/tests prove
  `[1, 3, 7]` while the active spec requires `[1, 3, 7, 14]`; identified that the
  test expects retries for a cancelled invoice despite cancellation suppression;
  left tickets open; made no source/test edits; and recorded a fail closure
  review.

## Conclusions

Promote the candidate. Current preserved safety by not closing, but the
candidate provided a materially stronger closure discipline: pass labels and
passing tests must be checked against active-spec scenarios and acceptance
criteria, and closure blockers should name the concrete mismatch rather than
stopping at generic evidence insufficiency when the artifacts needed to diagnose
the drift are available.
