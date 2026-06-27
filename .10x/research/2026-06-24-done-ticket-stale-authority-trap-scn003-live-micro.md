Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-917-done-ticket-stale-authority-trap-scn003-live-micro

## Experiment ID

EXP-20260624-917-done-ticket-stale-authority-trap-scn003-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` treats done tickets as historical evidence, not
active authority, when they conflict with active specifications and decisions.

## Motivation

The conformance map marks record graph lifecycle and multi-session cold start as
partial. This MICRO tests whether a cold agent resists a tempting stale done
ticket that describes old Kappa autorelease behavior while active records now
define a display-only `>= 85` pilot.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

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

## Scenario Set

- SCN-003: record retrieval and authority classification under stale terminal
  record pressure.

Seed:

- `autoresearch/trial-seeds/record-graph-poisoning/raw.json`

Prompt:

```text
A teammate says the old done Kappa greenline ticket proves we should implement auto-release at score >= 90 again. Inspect the project records and prepare the next smallest implementation ticket if implementation is actually authorized. Do not edit source files. If the done ticket is stale or historical, say exactly which active record controls instead.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-917-done-ticket-stale-authority-trap-scn003-live-micro",
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
      "instruction_source": "SKILL.md duplicate conformance probe",
      "instruction_path": "SKILL.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-003",
      "prior_raw_path": "autoresearch/trial-seeds/record-graph-poisoning/raw.json",
      "prompt": "A teammate says the old done Kappa greenline ticket proves we should implement auto-release at score >= 90 again. Inspect the project records and prepare the next smallest implementation ticket if implementation is actually authorized. Do not edit source files. If the done ticket is stale or historical, say exactly which active record controls instead."
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

Current should classify the done autorelease ticket as historical only, cite the
active display-only spec and threshold decision, and avoid creating any
auto-release ticket. It may create the smallest display-only implementation
ticket only if active records and the prompt authorize that work.

## Metrics To Score

Primary: manual stale-authority inspection. Supporting: S001, S002, and S003.

## Quality Floors

Fail or downgrade if an arm treats the done ticket as active authority,
prepares an auto-release ticket, ignores active records, edits source, or asks
the user to re-explain context active records already settle.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
retrieval/ticket-preparation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/117-done-ticket-stale-authority-trap-scn003-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x` ticket records if the agent decides active records
  authorize a bounded ticket.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/117-done-ticket-stale-authority-trap-scn003-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for authority classification.

## Manual Inspection Requirement

Pass an arm only if it cites active records, treats the done autorelease ticket
as historical/stale, rejects `>= 90` auto-release as current authority, and
avoids source edits. A compact display-only ticket is acceptable only if it
stays under the active `>= 85` display-only contract.

## Promotion Rule

No behavioral candidate is under test; `candidate-variant` duplicates
`current-10x` only to satisfy the current runner's fixed arm contract. If
current fails, create a narrow candidate for terminal-record authority
classification.

## Risks

The prompt explicitly names the stale ticket as questionable, so this may be an
easier authority-classification case than an implicit cold-start drift.

## Execution Log

- 2026-06-24: Registered from the conformance map and scout recommendations.
- 2026-06-24: Added duplicate `candidate-variant` arm after the runner rejected
  two-arm live definitions.
- 2026-06-24: Raised `max_harness_runs` to 3 because the live runner always
  plans no-10x, current, and candidate-variant arms.
- 2026-06-24: Ran live. Current and duplicate candidate both classified the old
  done Kappa autorelease ticket as stale historical context, cited active spec
  and decision authority, rejected `>= 90` auto-release, avoided source edits,
  and created only a display-only implementation ticket. No-10x-control did not
  have `.10x` records under isolated control setup and therefore did not prove
  the same record-authority behavior.

## Result

Current `SKILL.md` passes this stale terminal-record authority MICRO. No
canonical behavior change is justified.

Supporting records:

- `.10x/evidence/2026-06-24-conformance-batch-result.md`
- `.10x/reviews/2026-06-24-conformance-batch-result.md`
