Status: active
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-864-distinct-near-duplicate-owner-scn005-live-micro

## Experiment ID

EXP-20260624-864-distinct-near-duplicate-owner-scn005-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-distinct-near-duplicate-owner-v1` improves record graph
fitness when an existing ticket is related to but does not own a newly requested
follow-up.

## Motivation

Recent promotions strengthened record economy, fish-before-opening behavior, and
invalid-request no-ticket handling. The residual risk is over-deduplication:
the agent may refuse to open a needed follow-up because an existing ticket uses
similar words even though its scope excludes the requested behavior.

## Method Tier

MICRO using the tracked fish-before-opening seed.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-distinct-near-duplicate-owner.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-005: an existing visible-rows CSV quote/newline ticket is related to but
  explicitly excludes archive export behavior.

Seed:

- `autoresearch/fixtures/live-seeds/fish-before-opening/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-864-distinct-near-duplicate-owner-scn005-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-distinct-near-duplicate-owner-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-distinct-near-duplicate-owner.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-005",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/fish-before-opening/raw.json",
      "prompt": "Open a follow-up ticket for the legacy nightly/archive CSV export quote/newline coverage gap. Do not touch source code. There may already be a ticket about visible-rows CSV quote/newline coverage; inspect before deciding whether it owns this request."
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

Current may over-deduplicate by treating the existing visible-rows CSV
quote/newline ticket as the owner for legacy/archive export coverage. Candidate
should read the existing ticket, identify archive behavior as explicitly
excluded, create exactly one bounded legacy/archive follow-up ticket, and cite
the existing visible-rows ticket as related but insufficient.

## Metrics To Score

Primary: manual ownership comparison, S002, and S005. Supporting: S007.

## Quality Floors

S002 active floor 75. Manual inspection is authoritative because the target is
ownership precision rather than generic ticket count.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
ticket-tracking turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/064-distinct-near-duplicate-owner-scn005-live-micro/`;
- records created or updated in the subject workspace under `.10x/` only;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- source files;
- dependency additions.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/064-distinct-near-duplicate-owner-scn005-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for near-duplicate ownership behavior.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects the existing visible-rows CSV quote/newline ticket;
- recognizes that archive/legacy export behavior is excluded or not covered by
  that ticket's acceptance criteria;
- creates exactly one bounded durable owner for legacy nightly/archive CSV
  quote/newline coverage, or updates an existing owner if one truly exists;
- cross-references the related visible-rows ticket if creating a new owner;
- edits no source files.

Fail if it treats the visible-rows ticket as the owner for archive/legacy
coverage, creates a vague catch-all CSV escaping ticket, creates a duplicate
visible-rows ticket, or edits implementation files.

## Promotion Criteria

Promote only if candidate materially improves over current on distinct
near-duplicate ownership. Discard if current already creates the bounded
archive/legacy owner and explains why the visible-rows ticket is related but
insufficient.

## Known Risks And Confounders

- The existing ticket's progress note mentions a "legacy quote/newline gap"
  while its scope excludes archive behavior. Manual inspection must judge
  ownership from scope and acceptance criteria, not that note alone.
- Trust Level 1 scoring may reward both over- and under-deduplication because it
  mainly counts records and keywords.

## Execution Log

- 2026-06-24: Registered after EXP-862 promotion and during EXP-863 execution to
  test the residual over-deduplication risk introduced by stronger record
  economy rules.

## Results

Pending.

## Conclusions

Pending.
