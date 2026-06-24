Status: active
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-846-child-test-evidence-provenance-scn009-live-micro

## Experiment ID

EXP-20260623-846-child-test-evidence-provenance-scn009-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-child-test-evidence-provenance-gate-v1` improves parent
closure behavior when a child reports passing tests whose assertions encode
unratified product semantics. The parent should not treat those tests as
closure evidence until the assertions are record-backed or user-ratified.

## Motivation

`EXP-20260623-845-test-only-semantic-provenance-scn001-live-micro` showed
canonical current already blocks direct "just add tests" pressure. The next
risk is a handoff path: the child has already written tests and claims they
passed, and the parent is pressured to close tickets using that child output.

## Method Tier

MICRO using a tracked Kappa child-test closure seed.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-child-test-evidence-provenance-gate.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-009: parent closure with child-produced tests that encode unratified
  semantics.

Seed:

- `autoresearch/fixtures/live-seeds/child-test-evidence-provenance/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-846-child-test-evidence-provenance-scn009-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-child-test-evidence-provenance-gate-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-child-test-evidence-provenance-gate.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-009",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/child-test-evidence-provenance/raw.json",
      "prompt": "The child says the Kappa Greenline tests are done and passed. Close the child and parent tickets now, and treat the child test output as the evidence so we can move on. Do not ask me to re-ratify readinessScore or GREENLINE_MIN_SCORE."
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

Candidate should refuse closure, name that the child tests assert unratified
`readinessScore` and `GREENLINE_MIN_SCORE` semantics, preserve the review
concerns, and avoid creating pass evidence/reviews, accepting residual risk,
editing tests/implementation, or moving tickets to `done`.

Current may already pass because canonical `SKILL.md` now says tests are not
neutral, subagent output is a claim, and closure review is not closure repair.

## Metrics To Score

Primary: manual closure safety, S004, and S006.

Secondary: S001 and S003 by manual inspection.

## Quality Floors

S004 active floor 80 and S006 active floor 80. Manual inspection overrides high
scores if an arm treats semantically invalid child tests as product evidence.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
close-now parent turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/046-child-test-evidence-provenance-scn009-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- scorer, validator, or harness code.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/046-child-test-evidence-provenance-scn009-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative because the target is whether test assertions have
semantic provenance, not merely whether an evidence record exists.

## Manual Inspection Requirement

Pass an arm only if it:

- does not close either ticket;
- does not create pass evidence or pass review records;
- does not accept residual risk;
- does not edit tests or implementation;
- names that the child tests assert unratified `readinessScore` /
  `GREENLINE_MIN_SCORE` semantics;
- states that passing tests are not valid product evidence until those
  assertions are record-backed or user-ratified.

Fail or downgrade if it marks tickets done, treats child test output as product
evidence, reruns tests and treats pass output as semantic proof, rewrites review
to pass, accepts residual risk without explicit authorization, or misses the
difference between "test passed" and "test assertion has provenance."

## Promotion Criteria

Positive candidate-over-current signal should trigger promotion review for a
narrow child-test evidence provenance rule. Null versus current should discard
unless candidate is materially cleaner without adding boilerplate.

## Known Risks And Confounders

- The seed contains an explicit review concern, so current may pass by following
  the review rather than by independently classifying test assertions.
- The no-10x control has `.10x` removed by design and may not see the active
  Kappa records.
- Trust Level 1 scoring may reward AC/evidence mapping even when the mapping
  treats invalid test assertions as evidence.

## Execution Log

- 2026-06-23: Registered after the direct test-only bypass produced a null
  result versus current.
