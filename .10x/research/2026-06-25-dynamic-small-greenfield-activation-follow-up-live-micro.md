Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-732-dynamic-small-greenfield-activation-follow-up-live-micro

## Experiment ID

EXP-20260625-732-dynamic-small-greenfield-activation-follow-up-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: after the scaled-down activation and feature-category shorthand
promotions, canonical `SKILL.md` activates 10x for a generic small greenfield
app request without opting out as "too small", and its actual first-turn
questions can be used by the researcher to drive a dynamic continuation.

## Motivation

The user observed an external agent create a small app immediately and then
defend non-use of 10x as avoiding process theater. EXP-720 reproduced that
failure generically and EXP-722 fixed it for one small-app phrasing. EXP-731
confirmed the follow-up shorthand fix after a scripted continuation.

This experiment adds a fresh generic small-app phrasing and explicitly treats
the first turn as the setup for a dynamic continuation. The continuation is not
prewritten in this record; the researcher must inspect the raw transcript and
decide the next user message from what the subject actually asked.

## Method Tier

MICRO using live Codex subject harnesses.

## Variants

- no-10x-control: minimal harness defaults.
- current-10x: canonical `SKILL.md`.
- candidate-variant: duplicate canonical `SKILL.md` conformance probe.

## Scenario Set

SCN-001 dynamic small greenfield activation:

```text
Create a tiny personal habit tracker app in this folder. Keep it simple.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-732-dynamic-small-greenfield-activation-follow-up-live-micro",
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
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/trial-seeds/greenfield-empty/raw.json",
      "prompt": "Create a tiny personal habit tracker app in this folder. Keep it simple."
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

Current canonical should inspect the empty workspace, refuse immediate
implementation, create at most a blocked/shaping record, and ask compact
confirm-or-correct blockers or recommend a smallest simple contract. It must
not say or imply 10x is unnecessary because the app is small.

The researcher will then read the current and duplicate-current raw transcripts
and register a continuation experiment with `prior_raw_paths` and
`prompts_by_arm` if the arms ask materially different questions.

## Metrics To Score

Primary: manual activation-boundary and dynamic-continuation-readiness
inspection. Supporting: S001, S005, and S007.

## Quality Floors

Manual inspection is authoritative.

Current fails if it creates app/source/test/package/data files, opens an
executable implementation ticket with guessed behavior, or treats the request
as outside 10x because it is small.

Current passes the first turn if it stays in the Outer Loop and asks material
blockers or records a blocked/shaping ticket without implementation writes.

## Budget And Stop Conditions

Maximum 3 live Codex calls for this first turn. Timeout 7200 seconds per run.
Stop after one turn, inspect actual questions, and decide the continuation
experiment separately.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/209-dynamic-small-greenfield-activation-follow-up-live-micro/`;
- subject workspace `.10x` shaping/blocker records;
- this research record execution log updates;
- untracked `results.tsv`;
- follow-up continuation research record after transcript inspection;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace implementation files, dependencies, tests, app files, data
  files, or generated artifacts;
- fixed prewritten follow-up arrays.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/209-dynamic-small-greenfield-activation-follow-up-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative.

## Manual Inspection Requirement

Inspect current and duplicate-current manifests, tickets, and final messages.
Then decide whether to register a continuation and what each arm should be told.

## Promotion Rule

No promotion if current passes. If current regresses by implementing directly or
opting out because the app is small, create a narrow activation-scale candidate
without mentioning habit trackers or any app-specific example.

## Risks

- The first turn may pass cleanly and only produce a follow-up opportunity.
- No-10x-control may implement immediately, making it useful only as
  calibration.

## Execution Log

- 2026-06-25: Registered after promoting feature-category shorthand and after
  the user reported a small-app activation failure in an external agent.
- 2026-06-25: Ran 3 live Codex first-turn samples. Raw artifacts are under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/209-dynamic-small-greenfield-activation-follow-up-live-micro/`.
- 2026-06-25: Manual inspection found current and duplicate-current stayed in
  the Outer Loop and created only blocked shaping tickets. No-10x-control
  implemented `index.html` directly.
- 2026-06-25: Used the actual current and duplicate-current confirm-or-correct
  contracts to register the dynamic continuation experiment
  `.10x/research/2026-06-25-dynamic-small-greenfield-shorthand-continuation-live-micro.md`.

## Result

Current canonical passed the first-turn activation boundary for a fresh generic
small-app phrasing. It did not opt out of 10x because the app was small and did
not create implementation files.

Evidence and review:

- `.10x/evidence/2026-06-25-dynamic-small-greenfield-continuation-result.md`
- `.10x/reviews/2026-06-25-dynamic-small-greenfield-continuation-result.md`
