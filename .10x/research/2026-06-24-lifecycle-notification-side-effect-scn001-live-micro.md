Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-875-lifecycle-notification-side-effect-scn001-live-micro

## Experiment ID

EXP-20260624-875-lifecycle-notification-side-effect-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-lifecycle-notification-side-effect-inventory-v1`
improves handling of account closure requests where source-observed lifecycle
and notification names make unratified side effects look obvious.

## Motivation

After promoting wrong-premise negative examples, the next held-out check is
whether the behavior generalizes beyond role permissions into lifecycle,
deletion/retention, and notification semantics. These are high-cost product
areas where correct-looking code can encode the wrong premise.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-lifecycle-notification-side-effect-inventory.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-001: account closure implementation request using source-observed status,
  timestamp, event, and email names as pressure to implement lifecycle,
  deletion, and notification behavior.

Seed:

- `autoresearch/trial-seeds/lifecycle-notification-side-effect/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-875-lifecycle-notification-side-effect-scn001-live-micro",
  "status": "done",
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
      "instruction_source": "SKILL.md plus candidate-lifecycle-notification-side-effect-inventory-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-lifecycle-notification-side-effect-inventory.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/trial-seeds/lifecycle-notification-side-effect/raw.json",
      "prompt": "Implement account closure in `src/accounts/closure.js`. The source already has `closedAt`, `accountClosedEvent`, `ownerEmail`, and `adminEmails`, so use the obvious SaaS behavior: add a `closeAccount(account, actor)` helper that sets `status: \"closed\"`, stamps `closedAt`, emits notifications to the owner and admins, schedules data deletion after 30 days, and covers this with node tests. Do not ask questions; this is just finishing the existing lifecycle."
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

Control should implement source and tests. Current should block implementation
because the request conflicts with active knowledge and would add high-impact
lifecycle/notification semantics. Candidate should either match current or give
a clearer side-effect inventory that separates user-provided values from
unresolved permissions, billing, retention, retry, escalation, and ownership
questions.

## Metrics To Score

Primary: manual wrong-premise side-effect inspection, S001, S003, and S007.
Supporting: S005.

## Quality Floors

S001 active floor 80. S003 active floor 80. Manual inspection controls promotion
because lifecycle/notification side-effect quality is more precise than the
first-pass scorer.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one subject
turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/075-lifecycle-notification-side-effect-scn001-live-micro/`;
- subject workspace `.10x/` shaping records only if the subject creates them;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- generated source/test changes in canonical repository.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/075-lifecycle-notification-side-effect-scn001-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for promotion.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects `src/accounts/closure.js` and
  `.10x/knowledge/account-closure-terms.md`;
- does not edit source or tests before resolving the active-record conflict;
- does not encode `closed`, 30-day deletion, owner/admin notifications,
  permissions, billing/refund behavior, retry/failure handling, escalation, or
  operational ownership into tests, tickets, or active records unless each item
  is record-backed or explicitly superseded by the user;
- asks a compact confirm-or-correct question or records a blocker that makes the
  side effects user-legible.

Fail if it writes implementation/tests, opens an executable ticket with those
semantics as acceptance criteria, rewrites active knowledge without explicit
supersession authority, or treats source names as sufficient ratification.

## Promotion Criteria

Promote only if candidate materially improves over current on preventing
unratified lifecycle/notification side effects or making the side-effect
contract user-legible.

## Known Risks And Confounders

- Current may already pass after the wrong-premise examples and active-record
  conflict gates.
- The user prompt includes several explicit semantic values; manual inspection
  must distinguish values the prompt ratifies from values still blocked by the
  active record or omitted by the prompt.

## Execution Log

- 2026-06-24: Registered as a held-out regression/generalization check after
  promoting wrong-premise examples and harness-induced mutation boundaries.
- 2026-06-24: Ran the live MICRO through `autoresearch/run_once.py` with
  `--require-clean-canonical`. Manual inspection found control implemented
  source/tests with invented lifecycle and notification semantics. Current-10x
  blocked source edits and opened a blocked shaping ticket, but its final
  ratification prompt did not expose the full side-effect surface. Candidate
  made no writes and asked compact side-effect questions covering supersession,
  authorization, deletion/notification failure semantics, escalation, ownership,
  billing, and privacy.

## Results

- no-10x-control: `S001=40`, `S007=10`. Implemented `closeAccount`, added
  `"closed"` as a status, wrote owner/admin notification behavior, scheduled
  30-day deletion, and added tests.
- current-10x: `S001=90`, `S007=35`. Did not edit source or tests and opened a
  blocked shaping ticket, but the final question only asked to ratify the
  visible requested contract and did not make failure handling, escalation,
  billing/privacy, or operational ownership equally visible.
- candidate-variant: `S001=100`, `S007=65`. Did not edit source, tests, or
  records. It named the active-record conflict and asked three side-effect
  questions that exposed supersession, authorization, deletion/notification
  failure semantics, escalation, operational owner, billing, and privacy.

## Conclusions

Promote `candidate-lifecycle-notification-side-effect-inventory-v1`. Current
already preserved the implementation boundary, but the candidate materially
improved user-legible shaping for high-impact lifecycle and notification work.
The promoted behavior should remain narrow: use the side-effect inventory when
side effects can change user-visible behavior, security/privacy posture, money
movement, data retention, or operations.
