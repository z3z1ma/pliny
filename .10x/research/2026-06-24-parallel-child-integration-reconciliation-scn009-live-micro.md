Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-911-parallel-child-integration-reconciliation-scn009-live-micro

## Experiment ID

EXP-20260624-911-parallel-child-integration-reconciliation-scn009-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-parallel-child-integration-reconciliation-v1` improves
parent closure when multiple child artifacts share one semantic invariant and
their separate pass labels hide the same drift.

## Motivation

The conformance map marks real subagent orchestration and parallel coherence as
weakly tested. The current runner cannot invoke Codex app subagent tools because
it runs Codex CLI with `--disable plugins` and `--ignore-user-config`, so this
MICRO is intentionally a simulated parallel-child artifact test. It tests parent
reconciliation of child outputs; it does not claim real subagent coverage.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-parallel-child-integration-reconciliation.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-009: two parallel-shaped child tickets have pass evidence/reviews, but
  both child surfaces encode `selected` as visibility while the active spec
  defines visibility as `uiVisible === true && policyHidden !== true`.

Seed:

- `autoresearch/trial-seeds/parallel-child-integration-reconciliation/raw.json`

Prompt:

```text
You are the parent coordinator for the visible-row export integration ticket. The fixture contains two parallel child tickets: one for CSV row inclusion and one for export-button enabled state. Both child tickets report complete and have pass evidence and pass reviews.

Close the parent only if the active spec, source, tests, evidence, and reviews are coherent across both child surfaces. Do not edit source or tests and do not run commands; inspect the records/files and update only the smallest 10x record needed for closure or blocker state.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-911-parallel-child-integration-reconciliation-scn009-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-parallel-child-integration-reconciliation-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-parallel-child-integration-reconciliation.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-009",
      "prior_raw_path": "autoresearch/trial-seeds/parallel-child-integration-reconciliation/raw.json",
      "prompt": "You are the parent coordinator for the visible-row export integration ticket. The fixture contains two parallel child tickets: one for CSV row inclusion and one for export-button enabled state. Both child tickets report complete and have pass evidence and pass reviews.\n\nClose the parent only if the active spec, source, tests, evidence, and reviews are coherent across both child surfaces. Do not edit source or tests and do not run commands; inspect the records/files and update only the smallest 10x record needed for closure or blocker state."
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

Candidate should compare both child surfaces to the shared active spec, detect
that both use `selected` as visibility, block parent closure, and create or
update one integration owner. Current may already catch this from child-claim
and closure coherence rules.

## Metrics To Score

Primary: manual parent integration reconciliation. Supporting: S006, S004, and
S007.

## Quality Floors

S006 active floor 80. Manual inspection overrides automated scores if an arm
closes the parent based on child pass labels, reviews only one child, edits
source/tests, runs commands against the prompt, duplicates follow-ups, or claims
real subagent behavior.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one parent
closure/blocker turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/111-parallel-child-integration-reconciliation-scn009-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x` parent blocker, evidence, review, or follow-up owner
  needed for closure/blocker state.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- command execution in the subject workspace.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/111-parallel-child-integration-reconciliation-scn009-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for parallel child reconciliation.

## Manual Inspection Requirement

Pass an arm only if it:

- reads the active spec, parent ticket, both child tickets, child evidence,
  child reviews, and relevant source/test files;
- identifies the shared invariant violation in both child surfaces;
- blocks parent closure;
- creates or updates one smallest integration blocker/owner naming both
  affected child surfaces;
- avoids source/test edits and command execution;
- avoids duplicate follow-ups;
- does not claim this proves real subagent behavior.

Fail or downgrade if it closes the parent based on child pass labels, reviews
only one child, treats sibling pass reviews as independent proof, opens
duplicate follow-ups for the same semantic drift, edits source/tests, runs
commands, or claims real Codex subagents were tested.

## Promotion Rule

Do not promote from this MICRO alone. Promote only if current misses the
cross-child integration issue, candidate catches it, manual inspection confirms
no fake subagent claim, and a later positive control proves ordinary
spec-aligned child closure is not overblocked.

## Risks

- This is simulated child-output coverage, not real subagent orchestration.
- Current likely already has enough closure and child-claim discipline to pass.
- The prompt forbids command execution; some agents may run `sed`/`rg` anyway
  because they treat inspection commands as harmless. Manual inspection should
  record that separately from semantic judgment.

## Execution Log

- 2026-06-24: Registered from reused Tesla scout recommendation and the latest
  researcher backlog.
- 2026-06-24: Live run wrote artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/111-parallel-child-integration-reconciliation-scn009-live-micro/`.
  Current and candidate both scored `S004=100` and `S006=55`; no-10x-control
  scored `S004=60` and `S006=10`. Manual inspection found current and candidate
  both blocked parent closure and identified both child surfaces as sharing the
  same visibility invariant drift. Candidate discarded as null versus current.
