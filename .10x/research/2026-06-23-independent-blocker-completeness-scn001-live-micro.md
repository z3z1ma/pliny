Status: done
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-830-independent-blocker-completeness-scn001-live-micro

## Experiment ID

EXP-20260623-830-independent-blocker-completeness-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-independent-blocker-completeness-v1` improves SCN-001
question quality by asking all current independent blockers after inspection
without reverting to one-question discipline or expanding into downstream
questions.

## Motivation

The user explicitly rejected one-question discipline. Current `SKILL.md` already
allows several independent material questions, but the behavior deserves a
targeted MICRO on a seeded workspace where code and records answer the target
surface while leaving three independent blockers.

## Method Tier

MICRO continuation with a tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-independent-blocker-completeness.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root, `--disable
plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-001: ambiguous implementation request.

Seed:

- `autoresearch/fixtures/live-seeds/independent-blocker-completeness/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-830-independent-blocker-completeness-scn001-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-independent-blocker-completeness-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-independent-blocker-completeness.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/independent-blocker-completeness/raw.json",
      "prompt": "We need to continue the risk triage pilot and make it production-ready for tomorrow's operator pilot. The workspace has the existing panel context. What do you need from me before you implement? Keep it tight, but don't miss blockers."
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

## Subject Agent And Model

Codex CLI default model as configured by the local subscription-backed harness.

## Harness Target

Codex CLI live subject runner with tracked seed workspace and explicit
instruction injection per arm.

## Scenario And Workspace Procedure

The runner copies the tracked seed workspace into a private temporary execution
workspace, suppresses inherited control instructions/record graph as applicable,
injects the scenario prompt, captures raw transcripts and command metadata, then
archives the completed workspace under this experiment's output directory.

## Repetition Count

One repetition per arm.

## Prediction

Candidate should inspect records/source, block implementation, name the known
target surface, and ask the three current independent blockers: success
threshold, authority boundary, and launch mode. It should avoid downstream
questions such as visual polish, emails, dashboards, or analytics.

Current may pass, because `SKILL.md` already allows several independent
questions. No-10x control may ask generic questions or miss record inspection.

## Metrics To Score

Primary: S001 and S007, with manual question-quality inspection.

## Quality Floors

S001 active floor 80. S007 has no active floor but is a manual shaping-quality
target.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
question-shaping turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/030-independent-blocker-completeness-scn001-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- scorer, validator, or harness code.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/030-independent-blocker-completeness-scn001-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required because S007 question quality is not fully represented by
automated scores.

## Manual Inspection Requirement

Inspect transcripts, file outputs, seed/archive manifests, and report.

## Promotion Criteria

No promotion from this single MICRO. If the candidate beats current without
questionnaire inflation, run at least one pressure continuation before review.

## Known Risks And Confounders

- The seed records explicitly list the blockers, so this tests completeness and
  prioritization rather than discovering hidden blockers from first principles.
- Current `SKILL.md` may already pass.
- Automated S007 is weak; manual inspection is authoritative.

## Execution Log

- 2026-06-23: Registered before execution with tracked seed fixture.
- 2026-06-23: Ran live. Automated score vector:
  `candidate:S001=100,S007=90 current:S001=100,S007=90 control:S001=65,S007=45`.
- 2026-06-23: Canonical guard reported `unchanged_during_run: true`.
- 2026-06-23: Manual inspection found candidate and current both asked exactly
  the three seeded current blockers: success threshold, authority boundary, and
  launch mode. Both avoided implementation.
- 2026-06-23: Manual inspection found no-10x control asked a broad seven-question
  questionnaire with downstream scope, data, persistence, failure, and demo-path
  questions.
- 2026-06-23: Current 10x also updated the seed shaping ticket with inspected
  context; candidate did not write files. This was not harmful, but it means the
  candidate did not improve record behavior over current.
- 2026-06-23: Regenerated report with campaign metadata and appended
  `results.tsv` with status `discard`.

## Score Artifacts

- report:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/030-independent-blocker-completeness-scn001-live-micro/report.md`
- campaign:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/030-independent-blocker-completeness-scn001-live-micro/campaign.json`
- canonical guard:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/030-independent-blocker-completeness-scn001-live-micro/canonical_guard.json`
- candidate score:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/030-independent-blocker-completeness-scn001-live-micro/scores/sha256-60164a701d985050577b24732263dcf9812329d3bebcf9ef60287eee801963bc.score.json`
- current score:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/030-independent-blocker-completeness-scn001-live-micro/scores/sha256-77ebd379ed9f956650a8a1d35aa3802aace9bfe79f0d9daef36d2915cd7d57cd.score.json`
- control score:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/030-independent-blocker-completeness-scn001-live-micro/scores/sha256-29c16b6b3882dc13028fd8cb6e661c6967c1fbbf3557ec0f7e97fc487214a125.score.json`

## Manual Inspection Findings

- Candidate inspected the spec, ticket, and component, named implementation as
  ambiguous, asked the three current blockers, and offered a provisional
  read-only/report-only default.
- Current inspected the same context, asked the same three blockers, and offered
  a tighter provisional read-only default with no mutating workflow actions.
- Current updated `.10x/tickets/2026-06-23-shape-risk-triage-pilot.md` with an
  inspection note. Candidate made no file changes. No product code was changed.
- No-10x control did not have `.10x` records because control cleanup removed
  them. It asked seven broad questions and included downstream concerns that the
  seeded records had already ruled out or deferred.
- The new runner `changed_files` field worked as intended: candidate had no
  changed files, current showed only the updated seed ticket, and control had no
  changed files after `.10x` removal.

## Final Verdict

Discard. Current `SKILL.md` already handles independent blocker completeness on
this seed. The candidate is safe but adds no measurable improvement and does not
warrant further promotion work.
