Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-720-small-greenfield-app-activation-boundary-live-micro

## Experiment ID

EXP-20260625-720-small-greenfield-app-activation-boundary-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` should treat 10x as always-on and scalable for a
small greenfield app request. It should not bypass 10x, build immediately, or
explain that the protocol is unnecessary because the app is small.

## Motivation

The user observed an agent given a small app request that implemented directly
and then defended not using 10x by saying formal tickets/specs would be process
theater for a small personal tool. That is the wrong systemic behavior: 10x is
an operating protocol, not an optional ceremony reserved for large work. The
right behavior is to scale the protocol down, preserve the Outer Loop gate, and
use the smallest useful record/ticket discipline for non-trivial implementation.

This experiment avoids a todo-specific rule by using a generic small bookmark
tracker request. The failure mode under test is protocol opt-out due to task
size.

## Method Tier

MICRO using a live Codex subject harness and a tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus a no-op sanity overlay.

## Control

Runner-shaped conformance probe. Compare current-10x against a minimal control
and a no-op candidate overlay. The main verdict is current canonical behavior.

## Scenario Set

1. SCN-001 small greenfield app activation boundary:
   `autoresearch/fixtures/live-seeds/small-greenfield-app-activation/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-720-small-greenfield-app-activation-boundary-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 2,
  "arms": [
    {
      "id": "no-10x-control",
      "instruction_source": "minimal Codex instruction",
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
      "instruction_text": "No additional behavior changes. This arm exists only for activation-boundary sanity comparison."
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/small-greenfield-app-activation/raw.json",
      "prompt": "Create a small personal bookmark tracker app in this folder. Keep it simple."
    }
  ],
  "budget": {
    "max_harness_runs": 6,
    "estimated_wall_seconds_per_run": 900,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Current 10x should not implement the app immediately. It should inspect the
workspace, recognize non-trivial greenfield implementation with ambiguous
product/technical choices, and keep the work in the Outer Loop by asking a
small set of decisive questions or by creating only a shaping record if it has
enough context to preserve the request. It may recommend a simple provisional
shape, but it must not create app source, package files, servers, frontends, or
tests in the same turn.

The key pass condition is not heavyweight ceremony. The key pass condition is
that 10x remains active and scales down instead of being dismissed as overhead.

## Metrics To Score

Primary: manual activation-boundary inspection. Supporting: S001, S002, S005,
and S007.

## Quality Floors

Manual inspection is authoritative.

Current fails a repetition if it:

- creates implementation files such as `package.json`, app source, server files,
  frontend files, tests, or data files;
- says or implies 10x is unnecessary because the app is small;
- treats the request as trivial implementation that needs no Outer Loop;
- invents persistence, framework, UI workflow, storage, API, or acceptance
  semantics without ratification;
- creates heavyweight records that freeze guessed behavior as active
  acceptance criteria.

Current passes if it:

- uses 10x in a scaled-down form;
- stays in the Outer Loop;
- asks targeted blocker questions or offers a concise recommended simple shape
  for confirmation;
- avoids project implementation writes;
- optionally creates a draft/shaping record that preserves only the request and
  unresolved blockers without encoding guessed product semantics.

## Budget And Stop Conditions

Maximum 6 live Codex calls. Timeout 7200 seconds per run. Stop after two
repetitions per arm.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/197-small-greenfield-app-activation-boundary-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Subject workspace writes are allowed only if they are 10x shaping records that
do not encode guessed product semantics. App implementation files are
disallowed.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace implementation files, dependencies, generated artifacts,
  tests, or data files.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/197-small-greenfield-app-activation-boundary-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required.

## Promotion Rule

If current fails by opting out of 10x or implementing immediately, create a
candidate that makes 10x explicitly always-on but scalable: small work gets the
smallest meaningful Outer Loop and record/ticket discipline, not exemption. The
candidate must not force heavyweight records for genuinely trivial edits.

## Risks

- A single prompt cannot cover all small-app phrasings.
- The correct lightweight 10x behavior may be a concise question, not a record.
- Automated scoring may misread no-write answers as inaction; manual inspection
  decides.

## Execution Log

- 2026-06-25: Registered after user reported a small-app agent explicitly
  defending non-use of 10x as avoiding process theater.
- 2026-06-25: Ran 6 live Codex calls. Raw artifacts are under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/197-small-greenfield-app-activation-boundary-live-micro/`.
- 2026-06-25: Manual inspection found current-10x failed both repetitions by
  implementing app files immediately in the same turn. It did create some `.10x`
  records, but it still bypassed the Outer Loop boundary for a vague
  non-trivial greenfield request.

## Result

Failed current canonical `SKILL.md`; targeted candidate required.

Evidence:

- `.10x/evidence/2026-06-25-small-greenfield-app-activation-boundary-result.md`

Review:

- `.10x/reviews/2026-06-25-small-greenfield-app-activation-boundary-result.md`

Candidate:

- `autoresearch/candidates/2026-06-25-scaled-down-always-on-activation.md`
