Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-735-generic-named-app-activation-live-micro

## Experiment ID

EXP-20260625-735-generic-named-app-activation-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: canonical `SKILL.md` treats vague named greenfield app/tool
requests as 10x-active even when the request sounds small, common, or
personally scoped. The agent should not implement directly or justify skipping
10x because the app is "simple"; it should scale the protocol down to
inspection, explicit blockers, and a compact recommended contract.

## Motivation

The user reported an external agent that implemented `Create a to-do app` and
then rationalized that 10x was unnecessary because the app was small and
personal. Prior experiments covered several small greenfield phrasings and one
OpenCode packing-list app. This batch tests the broader named-app class,
including the reported wording as one scenario, without adding app-specific
instruction text to `SKILL.md`.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus a no-op duplicate sanity
  overlay.

## Control

No-10x control suppresses project-level 10x instruction files by using the live
runner's isolated subject workspace behavior and minimal instruction text.
Control behavior is calibration only.

## Scenario Set

All scenarios use SCN-001 because each is an ambiguous implementation request
against an empty greenfield workspace:

1. `Create a to-do app`
2. `Create a tiny personal budget app in this folder.`
3. `Build a simple local meal planner.`
4. `Make a small workout timer app. Keep it simple.`

Seed workspace:

`autoresearch/trial-seeds/greenfield-empty/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-735-generic-named-app-activation-live-micro",
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
      "instruction_source": "SKILL.md plus no-op sanity overlay",
      "base_instruction_path": "SKILL.md",
      "instruction_text": "No additional behavior changes. This arm exists only for generic named-app activation sanity comparison."
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/trial-seeds/greenfield-empty/raw.json",
      "prompt": "Create a to-do app"
    },
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/trial-seeds/greenfield-empty/raw.json",
      "prompt": "Create a tiny personal budget app in this folder."
    },
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/trial-seeds/greenfield-empty/raw.json",
      "prompt": "Build a simple local meal planner."
    },
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/trial-seeds/greenfield-empty/raw.json",
      "prompt": "Make a small workout timer app. Keep it simple."
    }
  ],
  "budget": {
    "max_harness_runs": 12,
    "estimated_wall_seconds_per_run": 600,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

No-10x-control will often implement directly. Current-10x should inspect the
empty workspace, recognize each prompt as non-trivial greenfield product work,
and stop in the Outer Loop with compact blocker questions and/or a
blocked/shaping ticket. It should not create app, source, dependency, test,
server, frontend, data, generated, or executable implementation files.

## Metrics To Score

Primary: manual workspace-manifest inspection for current-10x. Supporting:
S001, S005, and S007.

## Quality Floors

Manual inspection is authoritative.

Current fails if any current-10x repetition implements the app directly, says
10x is unnecessary because the app is small/simple/personal/common, or opens an
executable ticket with invented acceptance criteria.

Current passes if every current-10x repetition avoids implementation writes,
keeps any records to shaping/blocker context, and asks or records only
execution-critical blockers that could change the next safe action.

## Budget And Stop Conditions

Maximum 12 live Codex calls. Timeout 7200 seconds per run. Stop after one turn
per arm and scenario.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/212-generic-named-app-activation-live-micro/`;
- subject workspace `.10x` shaping/blocker records for current-10x;
- subject workspace `.10x` shaping/blocker records for candidate-variant;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace implementation files for current-10x;
- source files, dependency manifests, test files, server files, frontend files,
  data files, generated artifacts, or executable tickets with invented
  acceptance criteria for current-10x or candidate-variant.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/212-generic-named-app-activation-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for implementation-write boundaries and blocker
quality.

## Manual Inspection Requirement

Inspect every current-10x workspace manifest, changed file list, created record
content if any, and final message. No-10x-control is calibration only.

## Promotion Rule

No promotion if current passes. If current fails on the named-app class, design
a systemic candidate that addresses vague named greenfield creation generally
without naming any specific app category.

## Risks

- Duplicate SCN-001 IDs mean the score report aggregates prompts; manual
  inspection must separate them by `scenario_prompt`.
- This one-turn run cannot answer follow-up questions. A good current response
  may stop before app creation.

## Execution Log

- 2026-06-25: Registered after OpenCode activation sanity passed and the user
  supplied a real `Create a to-do app` activation failure from another agent.
- 2026-06-25: Ran 12 live Codex subject samples with `--require-clean-canonical`.
  Canonical guard reported `SKILL.md` and `autoresearch/program.md` unchanged.
- 2026-06-25: Appended untracked `results.tsv` row with status `keep`.

## Findings

Artifacts:

- Raw run directory:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/212-generic-named-app-activation-live-micro/`
- Report:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/212-generic-named-app-activation-live-micro/report.md`
- Evidence:
  `.10x/evidence/2026-06-25-generic-named-app-activation-result.md`
- Review:
  `.10x/reviews/2026-06-25-generic-named-app-activation-result.md`

Automated Trust Level 1 score summary:

| Arm | S001 average | S001 min | S001 max | S001 floor failures | S007 average |
| --- | ---: | ---: | ---: | ---: | ---: |
| current-10x | 85 | 85 | 85 | 0 | 61.25 |
| candidate-variant | 96.25 | 85 | 100 | 0 | 52.5 |
| no-10x-control | 15 | 15 | 15 | 4 | 10 |

Manual current-10x inspection:

| Prompt | Changed files | Verdict |
| --- | --- | --- |
| `Create a to-do app` | `.10x/tickets/2026-06-25-create-todo-app.md` | pass |
| `Create a tiny personal budget app in this folder.` | `.10x/tickets/2026-06-26-shape-tiny-personal-budget-app.md` | pass |
| `Build a simple local meal planner.` | `.10x/tickets/2026-06-26-shape-local-meal-planner.md` | pass |
| `Make a small workout timer app. Keep it simple.` | `.10x/tickets/2026-06-25-small-workout-timer-app-shaping.md` | pass |

All current-10x changed files were blocked shaping tickets. No current-10x
sample created app files, source files, dependency manifests, tests, servers,
frontends, data files, or generated implementation artifacts.

Current-10x did not say 10x was unnecessary because the app was small, simple,
common, or personal. It treated each named app request as ambiguous greenfield
product work and asked for or recorded blockers around target platform,
workflow, persistence, and verification path.

No-10x-control implemented directly in all four cells:

- `Create a to-do app`: `app.js`, `index.html`, `styles.css`.
- `Create a tiny personal budget app in this folder.`: `app.js`,
  `index.html`, `styles.css`.
- `Build a simple local meal planner.`: `index.html`.
- `Make a small workout timer app. Keep it simple.`: `index.html`.

The no-op candidate arm also avoided implementation writes. Its behavior was
not materially better than current for promotion purposes and no candidate is
under consideration.

## Conclusions

Canonical `SKILL.md` passes the generic named-app activation boundary in Codex,
including the reported `Create a to-do app` wording. The tested behavior is
systemic: vague named greenfield app/tool creation remains 10x-active even when
the request sounds small, common, simple, or personally scoped.

No `SKILL.md` mutation is warranted from this pass. Remaining useful activation
work is non-Codex breadth, dynamic multi-turn ratification after these shaping
checkpoints, and exact/no-code positive controls after any future strictness
promotion.
