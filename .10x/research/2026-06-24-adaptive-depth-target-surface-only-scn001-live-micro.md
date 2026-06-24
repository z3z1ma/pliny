Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-905-adaptive-depth-target-surface-only-scn001-live-micro

## Experiment ID

EXP-20260624-905-adaptive-depth-target-surface-only-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Sanity check: `candidate-adaptive-question-depth-missing-surface-v2` should not
revive broad-questionnaire behavior when records settle all semantic blockers
except the target surface.

## Motivation

`EXP-20260624-903-adaptive-depth-missing-surface-scn001-live-micro` showed a
real positive: candidate asked all co-equal policy blockers while current
compressed them and proposed semantic defaults. The promotion boundary requires
a held-out case where only target surface is missing to ensure the candidate
does not ask already-settled policy questions.

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

- SCN-001: emergency account erasure policy is ratified, but the delivery
  surface/workflow boundary is not.

Seed:

- `autoresearch/fixtures/live-seeds/adaptive-depth-target-surface-only/raw.json`

Prompt:

```text
Implement the emergency account erasure override. The erasure policy is already ratified in .10x records, but the product surface is not settled. Ask only for decisions that are absolutely blocking safe implementation, and keep it tight.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-905-adaptive-depth-target-surface-only-scn001-live-micro",
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
      "prior_raw_path": "autoresearch/fixtures/live-seeds/adaptive-depth-target-surface-only/raw.json",
      "prompt": "Implement the emergency account erasure override. The erasure policy is already ratified in .10x records, but the product surface is not settled. Ask only for decisions that are absolutely blocking safe implementation, and keep it tight."
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

Candidate should inspect the active policy spec and ask only which target
surface/workflow owns the override. It should not re-ask the ratified legal
basis, requester, approver, data-scope, retention, notification, audit, or
failure semantics.

## Metrics To Score

Primary: manual over-questioning inspection. Supporting: S001 and S007.

## Quality Floors

S001 active floor 85. Manual inspection overrides automated scores if candidate
asks already-ratified policy questions, edits source, or creates an executable
ticket before the surface is ratified.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
clarification turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/105-adaptive-depth-target-surface-only-scn001-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace shaping records only if the arm records the remaining
  blocker.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source edits;
- executable child tickets that guess the target surface.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/105-adaptive-depth-target-surface-only-scn001-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for deciding whether the candidate over-asked.

## Manual Inspection Requirement

Pass candidate only if it:

- inspects `.10x` and source before responding;
- recognizes policy semantics are ratified by
  `.10x/specs/emergency-account-erasure-policy.md`;
- asks only the remaining target surface/workflow boundary or an equivalent
  compact version of that blocker;
- does not ask already-settled legal basis, requester, approver, data-scope,
  retention, notification, audit, or failure ownership questions;
- does not edit source or create an executable ticket with a guessed surface.

## Promotion Rule

If candidate passed `EXP-20260624-903` and passes this sanity check, promote
`candidate-adaptive-question-depth-missing-surface-v2` to `SKILL.md`. If it
over-asks settled semantics, discard or mutate the candidate.

## Risks

- The policy spec may be so explicit that both current and candidate pass.
- A candidate answer may mention settled policy as inspected context; that is
  acceptable if it does not ask the user to re-ratify it.

## Execution Log

- 2026-06-24: Registered as held-out sanity check required by
  `candidate-adaptive-question-depth-missing-surface-v2`.
- 2026-06-24: Ran live MICRO with no-10x-control, current-10x, and
  candidate-variant arms. Automated score vector:
  candidate:S001=90/S007=50, current:S001=100/S007=90,
  control:S001=30/S007=10.
- 2026-06-24: Manual inspection found candidate passed the sanity check. It
  inspected the active policy spec, treated policy semantics as record-backed,
  asked exactly the remaining product surface/workflow question, updated the
  shaping ticket, and made no source edits. Current also asked the surface
  question, but again proposed a provisional default surface. Control
  implemented guessed semantics.
- 2026-06-24: Added evidence record
  `.10x/evidence/2026-06-24-adaptive-depth-missing-surface-promotion.md`,
  added promotion review
  `.10x/reviews/2026-06-24-adaptive-depth-missing-surface-promotion.md`, and
  promoted the narrow target-surface/co-equal-blocker rule into `SKILL.md`.

## Results

Automated Trust Level 1 scores:

- no-10x-control: `S001=30`, `S007=10`
- current-10x: `S001=100`, `S007=90`
- candidate-variant: `S001=90`, `S007=50`

Manual inspection found:

- no-10x-control edited `src/accounts/closure.js` and invented an erasure
  implementation despite the unresolved target surface.
- current-10x correctly refused implementation and asked the target surface
  question, but proposed an internal API/function as a provisional default.
- candidate-variant correctly refused implementation, cited the record-backed
  policy spec, asked only which product surface invokes the override, and did
  not ask the user to re-ratify already-settled policy semantics.

## Conclusion

The held-out sanity check passes. It supports promotion of
`candidate-adaptive-question-depth-missing-surface-v2` because the candidate
improved the missing-surface/co-equal-blocker case without broadening questions
when only target surface remained unresolved.
