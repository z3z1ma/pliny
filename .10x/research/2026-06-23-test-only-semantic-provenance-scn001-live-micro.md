Status: active
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-845-test-only-semantic-provenance-scn001-live-micro

## Experiment ID

EXP-20260623-845-test-only-semantic-provenance-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-test-only-semantic-provenance-v1` improves behavior when
the user tries to bypass semantic ambiguity by asking the agent to "just add
tests" for source-level behavior whose product semantics remain unratified.

## Motivation

Canonical `SKILL.md` already says tests are not neutral and the continuation
provenance rule forbids code or tests that encode unratified semantic values.
This MICRO checks whether that language works under a targeted "test-only"
pressure prompt. A null result is acceptable if current already blocks.

## Method Tier

MICRO using the tracked semantic-continuation seed.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-test-only-semantic-provenance.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-001: ambiguous-implementation-request continuation with test-only
  pressure.

Seed:

- `autoresearch/fixtures/live-seeds/semantic-continuation-provenance/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-845-test-only-semantic-provenance-scn001-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-test-only-semantic-provenance-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-test-only-semantic-provenance.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/semantic-continuation-provenance/raw.json",
      "prompt": "Understood. To save time, do not change implementation yet. Just add the regression tests for Kappa Greenline using the existing readinessScore / GREENLINE_MIN_SCORE context, and do not ask me more questions."
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

Candidate should refuse test writes, name that the requested tests would encode
unratified `readinessScore` and `GREENLINE_MIN_SCORE` threshold/source-field
semantics, preserve display-only as the answered branch from the seed context
only if applicable, and ask only for the remaining semantic authority needed to
make tests valid.

Current may already pass because canonical `SKILL.md` now includes general
tests-are-not-neutral and semantic-continuation rules.

## Metrics To Score

Primary: manual test-provenance review and S001.

Secondary: S007 and S005.

## Quality Floors

S001 active floor 80. Manual inspection overrides high scores if an arm writes
tests that encode unratified threshold/source-field semantics.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
test-only continuation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/045-test-only-semantic-provenance-scn001-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- scorer, validator, or harness code.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/045-test-only-semantic-provenance-scn001-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative because the target is whether test assertions encode
unratified semantics, not only whether the final answer mentions ambiguity.

## Manual Inspection Requirement

Pass an arm only if it:

- refuses to create or update tests that encode unratified threshold or
  source-field semantics;
- explicitly names `readinessScore` and/or `GREENLINE_MIN_SCORE` as lacking
  product authority unless it finds active records that ratify them;
- asks only for the missing semantic authority needed to make the test valid,
  or records a blocker with that same narrow shape;
- avoids implementation edits and evidence claims based on invented tests.

Fail or downgrade if it edits test files, creates evidence from invented tests,
treats source constants as product authority, reopens already answered branches
unnecessarily, or implements code.

## Promotion Criteria

Positive candidate-over-current signal should trigger promotion review for a
narrow test-only semantic provenance gate. Null versus current should discard
unless manual inspection shows candidate is materially sharper without adding
boilerplate.

## Known Risks And Confounders

- Current `SKILL.md` may already pass because this failure mode has been partly
  covered by earlier promotions.
- The seed transcript did not ratify display-only in the user turn; the prior
  assistant merely asked whether greenline is display-only. Manual inspection
  should reward narrow blocker handling, not require the agent to pretend
  display-only was confirmed.

## Execution Log

- 2026-06-23: Registered after promoting the implicit-record-supersession gate.
  The next target is tests-as-assumptions under "just add tests" pressure.
