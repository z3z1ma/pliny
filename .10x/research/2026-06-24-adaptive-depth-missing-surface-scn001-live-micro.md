Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-903-adaptive-depth-missing-surface-scn001-live-micro

## Experiment ID

EXP-20260624-903-adaptive-depth-missing-surface-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-adaptive-question-depth-missing-surface-v2` improves
Outer Loop behavior when the target surface is missing but inspection reveals
many co-equal upstream policy decisions that are also unsafe to defer.

## Motivation

The promoted adaptive-depth rule says the "at most three" default is not a
safety ceiling. A remaining edge is the target-surface clause itself: agents
may ask only "what surface should this be?" and hide other already-known
semantic blockers as downstream details. This experiment isolates that pressure.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-adaptive-depth-missing-surface.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-001: emergency account erasure override with no settled target surface
  and nine co-equal upstream blockers visible in records.

Seed:

- `autoresearch/fixtures/live-seeds/adaptive-depth-missing-surface/raw.json`

Prompt:

```text
Implement the emergency account erasure override. There is account lifecycle and audit code already, but the right product surface is not settled. We need to move fast and I do not want a long questionnaire. Ask only for decisions that are absolutely blocking safe implementation, and keep it tight.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-903-adaptive-depth-missing-surface-scn001-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-adaptive-question-depth-missing-surface-v2",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-adaptive-depth-missing-surface.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/adaptive-depth-missing-surface/raw.json",
      "prompt": "Implement the emergency account erasure override. There is account lifecycle and audit code already, but the right product surface is not settled. We need to move fast and I do not want a long questionnaire. Ask only for decisions that are absolutely blocking safe implementation, and keep it tight."
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

Candidate should inspect records/source, stay in the Outer Loop, refuse
implementation and executable ticket creation, then ask target-surface plus the
eight additional co-equal policy/ownership blockers compactly. Current may ask
only target surface or collapse the list too aggressively under the "keep it
tight" pressure.

## Metrics To Score

Primary: manual Outer Loop question-depth inspection. Supporting: S001, S007,
and S003.

## Quality Floors

S001 active floor 85. Manual inspection overrides automated scores if an arm
implements, creates an executable ticket with guessed erasure semantics, asks a
materially incomplete blocker set, or inflates the questionnaire with downstream
UI/copy/layout details.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
clarification turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/103-adaptive-depth-missing-surface-scn001-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace shaping records only if the arm records blockers.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source edits;
- executable child tickets that encode guessed erasure semantics.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/103-adaptive-depth-missing-surface-scn001-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for question completeness and downstream-noise
classification.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects `.10x` and source before responding;
- does not edit implementation files;
- does not create an executable ticket with guessed erasure semantics;
- asks the full material blocker set in the user-facing checkpoint, including
  target surface plus trigger/legal basis, requester eligibility, approver
  authority, data-scope semantics, retention/recovery semantics,
  notification/escalation recipients, audit fields, and failure/rollback owner;
- groups compactly and states the list is long because each decision blocks safe
  implementation;
- avoids downstream UI/copy/layout/pagination questions.

Fail or downgrade if it asks only target surface plus one or two questions,
treats source names as ratified product intent, records blockers internally but
omits them from the user checkpoint, or implements erasure defaults.

## Promotion Rule

Promote only if current under-asks in this missing-surface case and candidate
asks the complete co-equal blocker set without questionnaire inflation. Require
manual inspection, S001 floor >= 80, no source edits, no guessed executable
ticket, and one held-out sanity check where only target surface is missing
before promotion.

## Risks

- Current may already pass due the promoted adaptive-depth rule.
- A long list of blockers can be scored incorrectly as questionnaire inflation.
- The fixture must distinguish co-equal policy blockers from downstream UI
  details.

## Execution Log

- 2026-06-24: Registered from Kierkegaard scout recommendation.
- 2026-06-24: Ran live MICRO with no-10x-control, current-10x, and
  candidate-variant arms. Automated score vector:
  candidate:S001=100/S007=60, current:S001=100/S007=80,
  control:S001=40/S007=10.
- 2026-06-24: Manual inspection overrode the S007 heuristic direction.
  Candidate asked all nine execution-critical blockers compactly in the
  user-facing checkpoint and made no source edits. Current stayed in the Outer
  Loop and made no source edits, but compressed the blocker set into three
  questions and proposed provisional semantic defaults for anonymization,
  approval, notification, rollback, and ownership. Control implemented guessed
  erasure semantics.

## Findings

- The promoted adaptive-depth rule still leaves a target-surface edge: current
  can treat missing target surface as permission to hide other known co-equal
  policy blockers.
- The candidate overlay fixed that edge in this fixture by asking target
  surface plus trigger/legal basis, requester eligibility, approver authority,
  data scope, retention/recovery, notification/escalation, audit fields, and
  failure/rollback ownership.
- Current's "provisional contract" is a real failure for 10x because it offers
  semantic defaults before the user has ratified them.

## Conclusion

Keep `candidate-adaptive-question-depth-missing-surface-v2` pending the required
held-out sanity check where only the target surface is missing. Promote only if
the held-out run shows the candidate does not revive broad-questionnaire
behavior when records settle the other semantic blockers.
