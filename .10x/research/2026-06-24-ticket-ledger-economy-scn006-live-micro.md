Status: active
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-869-ticket-ledger-economy-scn006-live-micro

## Experiment ID

EXP-20260624-869-ticket-ledger-economy-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` should avoid overusing the newly promoted ticket
assumption provenance ledger on trivial single-provenance executable tickets.

## Motivation

`candidate-ticket-assumption-ledger-v1` was promoted with a limiting clause:
do not add the section to trivial tickets with a single obvious provenance
source. This MICRO tests that residual risk immediately.

## Method Tier

MICRO using a live Codex subject harness and seeded display-name normalization
workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-ticket-ledger-economy-guard.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-006/SCN-005: simple executable ticket creation from one active spec.

Seed:

- `autoresearch/fixtures/live-seeds/ticket-ledger-economy/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-869-ticket-ledger-economy-scn006-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-ticket-ledger-economy-guard-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-ticket-ledger-economy-guard.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/ticket-ledger-economy/raw.json",
      "prompt": "Create the executable child ticket for implementing the active profile display-name normalization spec. Do not implement."
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

Current should create one compact executable ticket without an assumption
provenance section, because all behavior comes from one active spec and the work
is not high-impact. Candidate should do the same.

## Metrics To Score

Primary: manual ledger-overuse inspection and S005. Supporting: S003.

## Quality Floors

S003 active floor 75. Manual inspection controls the overuse verdict.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
subject-agent turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/069-ticket-ledger-economy-scn006-live-micro/`;
- subject workspace `.10x/tickets/` executable ticket records;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- implementation source files;
- dependency additions.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/069-ticket-ledger-economy-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for ledger overuse.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects the active spec and source;
- creates exactly one executable child ticket and does not implement;
- includes scope, exclusions, acceptance criteria, evidence expectations,
  references, and blockers;
- does not add an assumption provenance ledger unless it identifies a real
  mixed-provenance or high-impact reason.

Fail if it creates a provenance ledger merely because the promoted instruction
exists.

## Promotion Criteria

Promote only if candidate prevents overuse that current exhibits. Discard if
current already keeps the ticket compact.

## Known Risks And Confounders

- Control may create an adequate ticket despite missing `.10x` records if it can
  infer behavior from the prompt/source. Manual inspection should focus on
  current versus candidate ledger economy.

## Execution Log

- 2026-06-24: Registered immediately after promoting ticket assumption ledgers
  to test the review's residual overuse risk.

## Results

Pending.

## Conclusions

Pending.
