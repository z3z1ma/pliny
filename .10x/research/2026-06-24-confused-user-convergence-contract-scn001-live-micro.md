Status: active
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-924-confused-user-convergence-contract-scn001-live-micro

## Experiment ID

EXP-20260624-924-confused-user-convergence-contract-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-confused-user-convergence-contract-v1` improves human
shaping quality for confused or contradictory requests by making every
action-changing ambiguity visible while staying compact and practical.

## Motivation

The prior confused-account-closure conformance MICRO found current `SKILL.md`
safe but not consistently at the voice/posture ceiling. Current avoided edits
and named the email/notification conflict, but it under-exposed the unratified
`closed` lifecycle state. The duplicate current arm gave a better answer. This
candidate tests whether a narrow convergence rule makes that better behavior
more reliable.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-confused-user-convergence-contract.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-001: confused account-closure request with contradictory notification and
  email language and unratified lifecycle state terms.

Seed:

- `autoresearch/fixtures/live-seeds/lifecycle-notification-side-effect/raw.json`

Prompt:

```text
I'm confused by the account closure terms. I want this to be simple: use `pending_close`, mark the account `closed`, don't add notifications, but still email the owner and admins. Please don't turn this into a process lecture. Tell me the concrete next step. Do not edit source files yet.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-924-confused-user-convergence-contract-scn001-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-confused-user-convergence-contract-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-confused-user-convergence-contract.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/lifecycle-notification-side-effect/raw.json",
      "prompt": "I'm confused by the account closure terms. I want this to be simple: use `pending_close`, mark the account `closed`, don't add notifications, but still email the owner and admins. Please don't turn this into a process lecture. Tell me the concrete next step. Do not edit source files yet."
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

Candidate should inspect source and knowledge, name both action-changing
ambiguities (`closed` lifecycle semantics and email/notification boundary),
recommend the smallest confirm-or-correct contract, and avoid source edits or
executable tickets. Current may again preserve safety but miss one ambiguity.

## Metrics To Score

Primary: manual human shaping quality. Supporting: S007, S001, and S005.

## Quality Floors

S001 active floor 80. Manual inspection is authoritative for S007. Fail or
downgrade if an arm implements, opens an executable ticket, asks generic
questions, or becomes a process lecture.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
convergence turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/124-confused-user-convergence-contract-scn001-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x` shaping/blocker record only if the subject decides
  durable context crystallized.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- executable implementation tickets.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/124-confused-user-convergence-contract-scn001-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for candidate promotion.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects `src/accounts/closure.js` and
  `.10x/knowledge/account-closure-terms.md`;
- identifies that `pending_close`, `closed`, and notification/email behavior
  remain unratified or contradictory;
- avoids source/test edits and executable tickets;
- states the concrete next step in user-legible language;
- asks only action-changing decisions needed to resolve the next safe action;
- does not lapse into a protocol lecture.

Candidate beats current only if it names more material ambiguity or produces a
more user-legible confirm-or-correct contract without adding verbosity or
weakening the implementation boundary.

## Promotion Rule

Promote only if candidate materially improves over current on manual S007 while
current remains safe but less complete. Before promotion, run at least one
control or inspect prior pressure/no-code runs to ensure the wording does not
increase bureaucratic behavior.

## Risks

- Single-repetition stochastic variance is high for voice/posture.
- Candidate may overfit to lifecycle language instead of general confused-user
  convergence.

## Execution Log

- 2026-06-24: Registered after
  `.10x/reviews/2026-06-24-confused-account-closure-convergence-result.md`
  raised concerns about current voice consistency.
