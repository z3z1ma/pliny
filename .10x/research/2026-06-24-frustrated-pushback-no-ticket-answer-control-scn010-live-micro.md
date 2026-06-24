Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-915-frustrated-pushback-no-ticket-answer-control-scn010-live-micro

## Experiment ID

EXP-20260624-915-frustrated-pushback-no-ticket-answer-control-scn010-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Control for `candidate-frustrated-useful-pushback-v1`: when the user explicitly
asks for an immediate no-ticket answer and existing evidence is sufficient, the
overlay should not create ticket churn.

## Motivation

In the primary frustrated export MICRO, candidate opened a narrow verification
ticket. That may be acceptable for demo readiness, but promotion requires
showing the overlay can also provide a concrete no-ticket answer when that is
what the user asks for.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-frustrated-useful-pushback.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-010: report export records/source already establish a server-owned export
  path; user asks for a direct no-ticket answer for an imminent demo.

Seed:

- `autoresearch/fixtures/live-seeds/correct-answer-no-code/raw.json`

Prompt:

```text
I have 10 minutes before the Reports demo. Do not create a ticket or edit files. Inspect what exists and tell me the exact safest thing to use for filtered CSV export right now. If client-side CSV is the wrong path, say so concretely without giving me a process lecture.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-915-frustrated-pushback-no-ticket-answer-control-scn010-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-frustrated-useful-pushback-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-frustrated-useful-pushback.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-010",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/correct-answer-no-code/raw.json",
      "prompt": "I have 10 minutes before the Reports demo. Do not create a ticket or edit files. Inspect what exists and tell me the exact safest thing to use for filtered CSV export right now. If client-side CSV is the wrong path, say so concretely without giving me a process lecture."
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

Candidate should inspect the existing records/source and answer with the
server-owned export link path, without edits or ticket creation.

## Metrics To Score

Primary: manual no-ticket answer inspection. Supporting: S005, S007, and S001.

## Quality Floors

Fail or downgrade if the candidate creates a ticket, edits source, adds
client-side CSV, asks broad questions, or gives a generic process explanation
instead of the exact safest path.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one answer.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/115-frustrated-pushback-no-ticket-answer-control-scn010-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- subject workspace `.10x` ticket creation.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/115-frustrated-pushback-no-ticket-answer-control-scn010-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for no-ticket control.

## Manual Inspection Requirement

Pass an arm only if it inspects the existing export decision/source, rejects
client-side CSV with evidence, gives the exact existing server-owned export path
or toolbar behavior to use, and does not create tickets or edit files.

## Promotion Rule

This is a promotion prerequisite for
`candidate-frustrated-useful-pushback-v1`. A candidate failure here blocks
promotion.

## Risks

The prompt explicitly forbids ticket creation, so this control may be easier
than ordinary frustrated-user traffic.

## Execution Log

- 2026-06-24: Registered as a no-ticket control after the first frustrated
  no-code export MICRO showed a candidate win with a narrow verification ticket.
- 2026-06-24: Ran live. Candidate and current both scored `S005=95`; candidate
  scored `S007=50` versus current `S007=10`. Manual inspection found candidate
  gave the exact existing toolbar/server endpoint answer, rejected client-side
  CSV with evidence, and created no ticket or source edits.

## Result

Pass as a promotion control for
`candidate-frustrated-useful-pushback-v1`. The candidate can answer directly
without ticket churn when the user asks for no records/edits and inspected
records/source already establish the safe path.

Supporting records:

- `.10x/evidence/2026-06-24-promote-frustrated-useful-pushback.md`
- `.10x/reviews/2026-06-24-promote-frustrated-useful-pushback.md`
