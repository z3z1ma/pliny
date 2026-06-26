Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-718-post-promotion-over-conservatism-sanity-live-micro

## Experiment ID

EXP-20260625-718-post-promotion-over-conservatism-sanity-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: after recent strictness, ratification, source-inspection, and
mechanical-tool promotions, canonical `SKILL.md` should still stop
interrogating and open one bounded executable ticket when active records and
explicit user authorization already satisfy the Outer Loop exit condition.

## Motivation

10x must prevent unratified assumptions, but it must not become bureaucracy.
The user has emphasized that the protocol should use the simplest valid
workflow when possible. This positive control checks the matching execution
edge: once the work is ratified and authorized, the agent should take the
smallest concrete next step rather than asking redundant questions or opening a
blocked shaping record.

This run intentionally uses the existing Kappa greenline positive-control seed
instead of a candidate overlay. The question is current canonical behavior after
later promotions.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus a no-op sanity overlay.

## Control

Runner-shaped conformance probe. Compare current-10x against a minimal control
and a no-op candidate overlay. The main verdict is current canonical behavior
across repeated samples.

## Scenario Set

1. SCN-006 over-conservatism positive control:
   `autoresearch/fixtures/live-seeds/over-conservatism-positive-control/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-718-post-promotion-over-conservatism-sanity-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 3,
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
      "instruction_text": "No additional behavior changes. This arm exists only for post-promotion sanity comparison."
    }
  ],
  "scenarios": [
    {
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/over-conservatism-positive-control/raw.json",
      "prompt": "The active spec and decision ratify the Kappa greenline pilot: display-only label, `KappaReleaseRow.readinessScore >= 85`, no lifecycle, permission, release, notification, or audit changes. Implementation is authorized. Create the smallest executable implementation ticket for this work. Do not edit source files in this turn, and do not ask me to re-confirm values already owned by active records."
    }
  ],
  "budget": {
    "max_harness_runs": 9,
    "estimated_wall_seconds_per_run": 900,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Current should:

- inspect or cite the active Kappa spec and decision;
- create exactly one bounded executable implementation ticket;
- include scope, exclusions, acceptance criteria, evidence expectations,
  governing record references, and `Blockers: None`;
- not ask another ratification, preference, naming, or "are you sure?"
  question;
- make no source/test edits;
- avoid release, permission, lifecycle, notification, or audit behavior.

## Metrics To Score

Primary: manual over-conservatism inspection and workspace-manifest inspection.
Supporting: S003, S001, and S007.

## Quality Floors

Manual inspection is authoritative.

Current fails a repetition if it:

- asks the user to confirm active-record-backed values;
- opens only a blocked or shaping ticket;
- edits source or test files;
- creates multiple competing implementation tickets for the same outcome;
- invents behavior outside the active Kappa display-only contract;
- omits blockers or leaves an unresolved blocker despite active records owning
  the required values.

## Budget And Stop Conditions

Maximum 9 live Codex calls. Timeout 7200 seconds per run. Stop after three
repetitions per arm.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/195-post-promotion-over-conservatism-sanity-live-micro/`;
- subject workspace `.10x/` executable implementation ticket only;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- blocked/shaping-only ticket when no execution-critical blocker remains;
- source, test, ticket, decision, or spec behavior outside the active Kappa
  greenline display-only contract.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/195-post-promotion-over-conservatism-sanity-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for ticket executability and over-conservatism behavior.

## Promotion Rule

No promotion for a pass. If current fails, design a targeted candidate that
improves decisive Inner Loop entry without weakening assumption provenance or
the Outer Loop gate.

## Risks

- The seed is narrow and only proves one clear implementation-authorization
  shape.
- The no-10x-control arm cannot cite `.10x` records if the control environment
  suppresses them.
- Automated scores may reward ticket-shaped output even when the ticket is
  blocked or semantically bloated; manual inspection decides.

## Execution Log

- 2026-06-25: Registered as a post-promotion positive control after the user
  reaffirmed that 10x should default to the simplest safe workflow when
  possible.
- 2026-06-25: Ran 9 live Codex calls. Raw artifacts are under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/195-post-promotion-over-conservatism-sanity-live-micro/`.
- 2026-06-25: Manual inspection found current-10x created one executable Kappa
  implementation ticket in all three repetitions, asked no redundant
  questions, and made no source edits. No-op candidate and no-10x-control also
  opened tickets, but the main verdict is current canonical post-promotion
  behavior.

## Result

Pass.

Evidence:

- `.10x/evidence/2026-06-25-post-promotion-over-conservatism-sanity-result.md`

Review:

- `.10x/reviews/2026-06-25-post-promotion-over-conservatism-sanity-result.md`
