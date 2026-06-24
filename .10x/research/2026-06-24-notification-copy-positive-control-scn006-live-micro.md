Status: active
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-879-notification-copy-positive-control-scn006-live-micro

## Experiment ID

EXP-20260624-879-notification-copy-positive-control-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-notification-side-effect-economy-v1` prevents the newly
promoted lifecycle/notification side-effect inventory from overblocking a
record-backed display-only notification copy ticket.

## Motivation

The lifecycle/notification side-effect inventory improved high-impact account
closure shaping. Its promotion review identified residual risk: agents might
apply the inventory too broadly to low-risk notification copy or display changes
with no delivery, lifecycle, privacy, billing, or operational side effects.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-notification-side-effect-economy.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-006: create one executable ticket for a display-only notification banner
  copy change. The active knowledge record states there are no notification
  delivery or lifecycle side effects.

Seed:

- `autoresearch/fixtures/live-seeds/notification-copy-positive-control/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-879-notification-copy-positive-control-scn006-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-notification-side-effect-economy-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-notification-side-effect-economy.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/notification-copy-positive-control/raw.json",
      "prompt": "Do not implement yet. Create exactly one executable child ticket for changing the display-only `accountClosed.title` in `src/notifications/bannerCopy.js` from `Account closed` to `Account closed successfully`. This is copy only: no recipients, sends, cadence, retries, escalation, lifecycle, billing, permissions, privacy, or operational ownership changes. Use the existing project records/source to confirm the boundary."
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

Current should inspect the active knowledge record and source, then create one
compact executable ticket with scope, exclusions/non-goals, acceptance criteria,
evidence expectations, references, progress notes, and blockers. Candidate
should only improve if current overuses the side-effect inventory or asks
irrelevant questions.

## Metrics To Score

Primary: S003 ticket executability, S005 scope minimalism, and manual
side-effect-economy inspection. Supporting: S007.

## Quality Floors

S003 active floor 80. S005 active floor 75. Manual inspection controls promotion
because overblocking can look superficially careful.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one subject
turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/079-notification-copy-positive-control-scn006-live-micro/`;
- subject workspace `.10x/tickets/` records only if the subject creates them;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- source/test implementation changes in canonical repository.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/079-notification-copy-positive-control-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for side-effect inventory economy.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects `.10x/knowledge/notification-banner-copy.md` and
  `src/notifications/bannerCopy.js`;
- creates exactly one bounded executable ticket and no implementation changes;
- includes explicit non-goals preserving no recipient, send, cadence, retry,
  escalation, lifecycle, billing, permission, privacy, or operational ownership
  changes;
- includes acceptance criteria and evidence expectations sufficient for a
  cold-start executor.

Fail if it implements source changes, asks unnecessary side-effect questions,
creates a broad parent ticket, omits acceptance criteria, or encodes delivery
semantics beyond the copy change.

## Promotion Criteria

Promote only if candidate materially improves over current on compactly handling
record-backed display-only notification work without weakening the
lifecycle/notification side-effect inventory.

## Known Risks And Confounders

- The prompt explicitly states the non-goals, so current may already pass.
- If all arms create acceptable tickets, discard as a positive-control null.

## Execution Log

- 2026-06-24: Registered as a low-risk notification regression after promoting
  lifecycle/notification side-effect inventory.

## Results

Pending.

## Conclusions

Pending.
