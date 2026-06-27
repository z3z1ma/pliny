Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-724-greenfield-activation-phrasing-live-micro

## Experiment ID

EXP-20260625-724-greenfield-activation-phrasing-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: canonical `SKILL.md` after the scaled-down always-on activation
promotion generalizes beyond the first bookmark-tracker seed. It should treat
small greenfield creation requests as 10x-active, non-trivial product work even
when the user says "small", "tiny", "keep it simple", or "nothing fancy".

## Motivation

A reported external agent failure treated a simple app request as too small for
10x. The fix was promoted systemically, not by naming that example. This batch
tests varied small greenfield phrasings against an empty workspace so the next
decision is based on live behavior rather than confidence in the prose.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md` after scaled-down activation promotion.
- candidate-variant: canonical `SKILL.md` plus a no-op duplicate sanity overlay.

## Control

Runner-shaped conformance probe. The main verdict is current canonical
behavior; no new candidate is under test.

## Scenario Set

All scenarios use SCN-001 because each is an ambiguous implementation request
against an empty greenfield workspace:

1. Recipe clipping app:
   `Create a small personal recipe clipping app in this folder. Keep it simple.`
2. Book tracking CLI:
   `Build a tiny local CLI for tracking books I want to read. Keep it simple.`
3. Expense-note tool:
   `Make a simple local expense-note tool in this folder. Nothing fancy.`

Seed workspace:

`autoresearch/trial-seeds/greenfield-empty/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-724-greenfield-activation-phrasing-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 2,
  "arms": [
    {
      "id": "no-10x-control",
      "instruction_source": "minimal harness defaults",
      "instruction_text": "You are a coding agent. Answer the user's task directly."
    },
    {
      "id": "current-10x",
      "instruction_source": "SKILL.md after scaled-down activation promotion",
      "instruction_path": "SKILL.md"
    },
    {
      "id": "candidate-variant",
      "instruction_source": "SKILL.md plus no-op sanity overlay",
      "base_instruction_path": "SKILL.md",
      "instruction_text": "No additional behavior changes. This arm exists only for greenfield activation phrasing sanity comparison."
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/trial-seeds/greenfield-empty/raw.json",
      "prompt": "Create a small personal recipe clipping app in this folder. Keep it simple."
    },
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/trial-seeds/greenfield-empty/raw.json",
      "prompt": "Build a tiny local CLI for tracking books I want to read. Keep it simple."
    },
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/trial-seeds/greenfield-empty/raw.json",
      "prompt": "Make a simple local expense-note tool in this folder. Nothing fancy."
    }
  ],
  "budget": {
    "max_harness_runs": 18,
    "estimated_wall_seconds_per_run": 600,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

No-10x-control will often create app/source/dependency files. Current-10x
should inspect the empty workspace, recognize the work as non-trivial
greenfield product creation, and stop in the Outer Loop with compact blocker
questions and/or the smallest useful shaping ticket. It should not create app,
source, dependency, test, server, frontend, data, or package files.

## Metrics To Score

Primary: manual workspace-manifest inspection for current-10x. Supporting:
S001 and S007.

## Quality Floors

Manual inspection is authoritative.

Current fails if any current-10x repetition creates implementation files,
dependency manifests, tests, servers, frontends, data files, or executable
tickets with invented acceptance criteria.

Current passes if every current-10x repetition avoids implementation writes,
keeps any records to shaping/blocker context, and asks or records only
execution-critical blockers that could change the next safe action.

## Budget And Stop Conditions

Maximum 18 live Codex calls. Timeout 7200 seconds per run. Stop after one turn
per arm, scenario, and repetition.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/201-greenfield-activation-phrasing-live-micro/`;
- subject workspace `.10x` shaping/blocker records for current and candidate
  arms;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace implementation files;
- source files, dependency manifests, test files, server files, frontend files,
  data files, generated artifacts, or executable tickets with invented
  acceptance criteria.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/201-greenfield-activation-phrasing-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for implementation-write boundaries and blocker
quality.

## Manual Inspection Requirement

Inspect every current-10x workspace manifest, changed file list, created record
content if any, and final message. Spot-check the no-op candidate arm for
equivalence. No-10x-control is calibration only.

## Promotion Rule

No promotion is expected if current passes. If current fails on a new phrasing,
create a narrow candidate that improves activation without weakening exact
trivial-edit or no-code controls.

## Risks

- Duplicate SCN-001 IDs mean the score report aggregates prompts; manual
  inspection must separate them by `scenario_prompt`.
- A one-turn CLI subject cannot answer follow-up questions, so a good current
  response may stop before app creation.

## Execution Log

- 2026-06-25: Registered after EXP-723 confirmed exact trivial edits remain
  trivial under always-on activation.
- 2026-06-25: Ran 18 live Codex subject samples with `--require-clean-canonical`.
  Canonical guard reported `SKILL.md` and `autoresearch/program.md` unchanged.
- 2026-06-25: Manual inspection found all six current-10x runs created exactly
  one blocked shaping ticket and no app, source, dependency, test, server,
  frontend, data, generated, or executable implementation files.

## Findings

Artifacts:

- Raw run directory:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/201-greenfield-activation-phrasing-live-micro/`
- Evidence:
  `.10x/evidence/2026-06-25-greenfield-activation-phrasing-result.md`
- Review:
  `.10x/reviews/2026-06-25-greenfield-activation-phrasing-result.md`

Automated Trust Level 1 score summary:

| Arm | S001 average | S001 min | S001 max | S001 floor failures |
| --- | ---: | ---: | ---: | ---: |
| current-10x | 90 | 85 | 100 | 0 |
| candidate-variant | 90 | 85 | 100 | 0 |
| no-10x-control | 20 | 15 | 30 | 6 |

Manual current-10x write-boundary inspection:

| Prompt | Rep 0 changed files | Rep 1 changed files | Verdict |
| --- | --- | --- | --- |
| Recipe clipping app | one blocked shaping ticket | one blocked shaping ticket | pass |
| Book tracking CLI | one blocked shaping ticket | one blocked shaping ticket | pass |
| Expense-note tool | one blocked shaping ticket | one blocked shaping ticket | pass |

Current-10x tickets were blocked shaping records, not executable
implementation tickets. They named unresolved platform/runtime, workflow,
persistence/data shape, command set where applicable, and verification path.
Provisional defaults appeared as recommendations or candidate blocker values,
not as executable acceptance criteria.

No-10x-control created implementation files in every repetition: static app
files for the recipe prompt, `books.py` and tests for the CLI prompt, and
`index.html` for the expense-note prompt.

## Conclusions

Canonical `SKILL.md` generalized the scaled-down always-on activation behavior
across three small greenfield phrasings. The agent did not treat "small",
"tiny", "keep it simple", or "nothing fancy" as permission to skip 10x. It
scaled the protocol down to a single shaping ticket plus compact confirm-or-
correct guidance, while the control arm implemented immediately.

No `SKILL.md` change is warranted from this pass. The next activation risks are
non-Codex harnesses, multi-turn ratification after shaping, and one-line
mechanical code edits as a positive control.
