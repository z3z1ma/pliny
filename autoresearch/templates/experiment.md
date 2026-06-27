Status: draft
Created: YYYY-MM-DD
Updated: YYYY-MM-DD

# EXP-YYYYMMDD-NNN-short-slug

## Experiment ID

EXP-YYYYMMDD-NNN-short-slug

## Driver

Name or role responsible for experiment design and verdict.

## Question Or Hypothesis

The precise question or hypothesis registered before execution.

## Motivation

Why this behavior matters to 10x.

## Method Tier

MINE, MICRO, or FULL. Use MINE before MICRO and MICRO before FULL whenever the
cheaper tier can honestly answer the question.

## Arms

List the exact ordered arms to run. A one-arm current-skill regression lists one
arm. A comparative experiment lists every control, baseline, current, and
candidate arm explicitly.

- no-10x-control:
- current-10x:
- candidate-variant:

## Control

Define the control arm before execution. For the no-10x control, state how
project-level 10x instruction files such as `AGENTS.md`, `CLAUDE.md`, or
equivalent files are suppressed.

## Scenario Set

List scenario IDs and live prompts for subject-agent execution.

Choose seeds from `autoresearch/trial-seeds/index.json`; copy `raw_path` into
`prior_raw_path` and copy `workspace_procedure` into the runner definition.

For a continuation after subject-agent questions, list the prior raw artifact
for each arm and the next user message for that arm. Do not use fixed follow-up
arrays; the LLM researcher decides each next turn after reading the transcript.

## Scientific Contract

Register the question, hypothesis, expected behavior, inspection criteria,
quality floor, and verdict record path before execution.

## Runner Definition

For MICRO or FULL execution, fill this JSON block or provide an equivalent
local JSON definition to `autoresearch/run_codex_subject.py`. MICRO and FULL
are scenario breadth tiers. A MICRO can still call Codex; it is micro because
the scenario isolates one behavior.

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-YYYYMMDD-NNN-short-slug",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Name or role",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 1,
  "scientific_contract": {
    "question": "Does the current skill avoid unnecessary framework work in a trivial toggle request?",
    "hypothesis": "The current skill will prefer the smallest native edit and explain why a framework is unnecessary.",
    "expected_behavior": "The subject chooses a native toggle implementation or directly rejects the unnecessary framework.",
    "inspection_criteria": [
      "command exits are zero",
      "response or diff avoids adding a framework dependency",
      "archived workspace contains only task-relevant edits"
    ],
    "quality_floor": "No dependency, architecture rewrite, or unrelated record mutation is introduced.",
    "verdict_record_path": ".10x/evidence/EXP-YYYYMMDD-NNN-short-slug-result.md"
  },
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
      "instruction_source": "SKILL.md plus candidate overlay",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/YYYY-MM-DD-candidate.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-010",
      "prompt": "Add a framework so the toggle can show or hide details.",
      "workspace_procedure": "Use a clean seed workspace with a small existing toggle implementation, then archive the resulting workspace."
    }
  ],
  "budget": {
    "max_harness_runs": 3,
    "estimated_wall_seconds_per_run": 600,
    "timeout_seconds_per_run": 1800
  }
}
```
<!-- codex-subject-runner-definition:end -->

Continuation scenario shape:

```json
{
  "id": "SCN-001",
  "prior_raw_paths": {
    "no-10x-control": ".10x/evidence/.storage/<run>/raw/<control>.json",
    "current-10x": ".10x/evidence/.storage/<run>/raw/<current>.json",
    "candidate-variant": ".10x/evidence/.storage/<run>/raw/<candidate>.json"
  },
  "prompts_by_arm": {
    "no-10x-control": "Answer the control arm's actual question.",
    "current-10x": "Answer the current arm's actual question.",
    "candidate-variant": "Answer the candidate arm's actual question."
  }
}
```

## Subject Agent And Model

Record the actual subject agent, model, instruction set, and instruction digest
used per run. Do not bake model names into score semantics.

## Harness Target

Harness name, version when known, tools available, and relevant environment.

## Scenario And Workspace Procedure

Prompts, workspace generation procedure, reset procedure, realism limits, and
material digests required to reproduce the run.

## Repetition Count

Number of repetitions per scenario and arm. Label single-run FULL results
preliminary unless an accepted exception applies.

## Prediction

Expected rubric movement, expected failure elicitation, and what would count as
backfire.

## Rubric Criteria

Score IDs or plain-language rubric criteria and any active floors. Use
`autoresearch/catalogs/scores.json` for the manual scoring rubric. The runner
does not emit a verdict; the scientist inspects the artifacts against these
criteria and records confidence, rationale, evidence references, unsupported
assumptions, and floor triggers.

## Quality Floors

List active floors that apply to the experiment and whether they are draft or
accepted gates.

## Budget And Stop Conditions

Default caps unless overridden by a decision:

- MICRO: 300 subject-agent samples or 10 wall-clock hours.
- FULL: 20 harness runs or 36 wall-clock hours; suggested 3-hour cap per FULL
  run.
- Subscription-backed Codex, Claude, OpenCode, or oh-my-pi: no monetary cap.
- Metered APIs or paid cloud resources: require a new budget decision before
  exceeding USD 250 estimated spend.

State any additional stop condition.

## Write Boundary

Allowed and disallowed write paths. Include raw artifact destinations.

## Raw Output Destination

Claim-supporting raw artifacts belong under `.10x/evidence/.storage/`.
Exploratory source material belongs under `.10x/research/.storage/`.

## Rubric And Inspection Configuration

Declare score IDs or rubric criteria, required observations, known false
positives, known false negatives, confidence labels, and manual inspection
requirements.

## Manual Inspection Requirement

State what must be inspected and whether inspection is full or sampled.
Promotion-supporting claims require manual inspection unless an accepted
governance decision delegates that authority.

## Promotion Criteria

Promotion is separate from verdict. Define quality floors, control validity,
inspection requirements, negative side-effect checks, required review, and any
spec or decision updates required before promotion.

## Known Risks And Confounders

Known rubric limits, seed-state limits, harness contamination risks,
instruction contamination risks, privacy risks, and expected false positives or
false negatives.

## Execution Log

Append commands, tool invocations, outputs, artifact paths, failures, retries,
deviations from plan, spend or time if tracked, and current status.

## Trial Artifacts

Link summary JSON, plan JSON, raw outputs, command metadata, prompts, workspace
manifests, archived workspaces, and cost or token summaries.

## Manual Inspection Findings

Record inspection observations, rubric mismatches, surprising results, controls
that failed to fail, backfires, and limits.

## Final Verdict

One of: confirmed, refuted, backfired, inconclusive, already optimal,
confounded, candidate, promoted, or cancelled. Include limits.
