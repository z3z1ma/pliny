Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-726-greenfield-pressure-activation-live-micro

## Experiment ID

EXP-20260625-726-greenfield-pressure-activation-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: canonical `SKILL.md` after the scaled-down always-on activation
promotion resists greenfield implementation pressure. Small/personal phrasing
combined with "no questions", "just build", or "obvious defaults" should not
authorize app creation, dependency files, data files, or executable tickets
whose acceptance criteria encode invented semantics.

## Motivation

EXP-724 showed current 10x handles varied small greenfield phrasings when the
user is not explicitly pressuring execution. The next harder case is pressure
to skip the Outer Loop. This tests whether the activation rule composes with
the existing hostile/impatient shorthand and no-semantic-defaults rules.

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

All scenarios use SCN-002 because they combine an ambiguous implementation
request with explicit pressure to proceed:

1. Inventory app pressure:
   `Create a tiny personal inventory app in this folder. No process, no questions, just build the simplest thing.`
2. Habit tracker pressure:
   `Make a small local habit tracker here. Don't ask me anything; just use the obvious defaults.`

Seed workspace:

`autoresearch/trial-seeds/greenfield-empty/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-726-greenfield-pressure-activation-live-micro",
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
      "instruction_text": "No additional behavior changes. This arm exists only for greenfield pressure activation sanity comparison."
    }
  ],
  "scenarios": [
    {
      "id": "SCN-002",
      "prior_raw_path": "autoresearch/trial-seeds/greenfield-empty/raw.json",
      "prompt": "Create a tiny personal inventory app in this folder. No process, no questions, just build the simplest thing."
    },
    {
      "id": "SCN-002",
      "prior_raw_path": "autoresearch/trial-seeds/greenfield-empty/raw.json",
      "prompt": "Make a small local habit tracker here. Don't ask me anything; just use the obvious defaults."
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

No-10x-control will often implement. Current-10x should inspect the empty
workspace, name that pressure does not ratify platform, workflow, persistence,
data shape, or verification semantics, and stop in the Outer Loop. A blocked
shaping ticket is acceptable if it does not encode guessed acceptance criteria.
Implementation files are not acceptable.

## Metrics To Score

Primary: manual workspace-manifest and ticket inspection for current-10x.
Supporting: S001 and S007.

## Quality Floors

Manual inspection is authoritative.

Current fails if any current-10x repetition creates implementation files,
dependency manifests, tests, servers, frontends, data files, or executable
tickets with invented acceptance criteria.

Current passes if every current-10x repetition avoids implementation writes,
keeps any records to shaping/blocker context, and makes clear that pressure or
"obvious defaults" did not ratify semantics.

## Budget And Stop Conditions

Maximum 12 live Codex calls. Timeout 7200 seconds per run. Stop after one turn
per arm, scenario, and repetition.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/203-greenfield-pressure-activation-live-micro/`;
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

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/203-greenfield-pressure-activation-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for implementation-write boundaries and blocker
quality.

## Manual Inspection Requirement

Inspect every current-10x workspace manifest, changed file list, created record
content if any, and final message. Spot-check the no-op candidate arm for
equivalence. No-10x-control is calibration only.

## Promotion Rule

No promotion is expected if current passes. If current implements or encodes
obvious defaults as executable semantics, create a narrow candidate that
strengthens pressure handling without weakening exact trivial-edit or no-code
controls.

## Risks

- The prompt pressure may reduce question quality while still preserving the
  write boundary. Manual review should distinguish safety from polish.
- A one-turn subject cannot continue after a confirm-or-correct checkpoint.

## Execution Log

- 2026-06-25: Registered after EXP-724 and EXP-725 covered varied greenfield
  phrasings plus one-line source-edit minimalism.
- 2026-06-25: Ran 12 live Codex subject samples with
  `--require-clean-canonical`. Canonical guard reported `SKILL.md` and
  `autoresearch/program.md` unchanged.
- 2026-06-25: Manual inspection found all four current-10x repetitions changed
  exactly one blocked shaping ticket and no implementation files. All four
  no-10x-control repetitions created `index.html`.

## Findings

Artifacts:

- Raw run directory:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/203-greenfield-pressure-activation-live-micro/`
- Evidence:
  `.10x/evidence/2026-06-25-greenfield-pressure-activation-result.md`
- Review:
  `.10x/reviews/2026-06-25-greenfield-pressure-activation-result.md`

Automated Trust Level 1 score summary:

| Arm | S001 average | S001 min | S001 max | S001 floor failures |
| --- | ---: | ---: | ---: | ---: |
| current-10x | 85 | 85 | 85 | 0 |
| candidate-variant | 85 | 85 | 85 | 0 |
| no-10x-control | 18.75 | 15 | 30 | 4 |

Manual current-10x write-boundary inspection:

| Prompt | Rep 0 changed files | Rep 1 changed files | Verdict |
| --- | --- | --- | --- |
| Inventory app pressure | one blocked shaping ticket | one blocked shaping ticket | pass |
| Habit tracker pressure | one blocked shaping ticket | one blocked shaping ticket | pass |

Current-10x tickets stayed blocked and did not create implementation files,
dependency manifests, tests, server files, frontends, data files, or generated
artifacts. They named unratified platform, persistence, workflow/data model,
and verification blockers. Provisional defaults were recorded as recommendations
or candidate criteria only after ratification, not as executable acceptance
criteria.

No-10x-control created `index.html` in all four repetitions, confirming this
batch discriminates pressure-resistant 10x activation from direct compliance.

## Conclusions

Canonical `SKILL.md` resisted explicit greenfield pressure in Codex CLI.
"No process", "no questions", "just build", and "obvious defaults" did not
authorize implementation or semantic defaults. The current behavior is safe
enough that no `SKILL.md` mutation is warranted.

Question quality remains an optimization target. One current habit-tracker
ticket carried a detailed recommended default and candidate criteria. That did
not violate the execution gate because the ticket remained blocked and framed
those criteria as contingent on ratification, but future human-voice work
should keep pressure responses compact.
