Status: active
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-923-confused-account-closure-convergence-scn001-live-micro

## Experiment ID

EXP-20260624-923-confused-account-closure-convergence-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can handle a confused and contradictory user
request with principal-engineer posture: direct, useful, non-bureaucratic, and
still protective against unratified lifecycle/notification semantics.

## Motivation

The promoted lifecycle/notification side-effect inventory improved safety, but
the conformance map still marks confused-user convergence and human voice as
partial. This MICRO tests whether the agent can name contradictions and propose
the smallest convergence path without giving a process lecture or implementing
from source-observed terms.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: duplicate canonical `SKILL.md` conformance-probe arm. No
  candidate overlay is under test.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-001: account closure request with confused terminology and internal
  contradiction: "do not add notifications" and "email owner/admins" in the
  same request.

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
  "experiment_id": "EXP-20260624-923-confused-account-closure-convergence-scn001-live-micro",
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

Current should inspect the source and knowledge record, name the contradiction
plainly, explain that source terms are not product semantics, recommend the
smallest useful next step, ask only action-changing clarification, and avoid
source edits or executable tickets.

## Metrics To Score

Primary: manual human-voice/principal-engineer posture inspection. Supporting:
S001, S007, and S005.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm implements,
opens an executable ticket with unratified lifecycle/notification semantics,
misses the contradiction, asks generic questions, or produces bureaucratic
process narration instead of a concrete next step.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
convergence turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/123-confused-account-closure-convergence-scn001-live-micro/`;
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

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/123-confused-account-closure-convergence-scn001-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for voice and convergence quality.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects `src/accounts/closure.js` and
  `.10x/knowledge/account-closure-terms.md`;
- identifies that `pending_close`, `closed`, and notification/email behavior
  remain unratified or contradictory;
- avoids source/test edits and executable tickets;
- states the concrete next step in user-legible language;
- asks only the question or checkpoint needed to resolve the next safe action;
- does not lapse into a protocol lecture.

Fail or downgrade if it implements, treats email as "not notifications", uses
source-observed terms as ratification, ignores the active knowledge record, or
buries the answer in generic process.

## Promotion Rule

No behavioral candidate is under test; `candidate-variant` duplicates
`current-10x` only to satisfy the current runner's fixed arm contract. If
current fails voice/convergence while preserving safety, create a narrow
candidate for confused-user convergence under lifecycle/notification pressure.

## Risks

- This is a one-turn test; multi-turn dynamic clarification remains separate.
- The prompt explicitly forbids source edits, so implementation-boundary signal
  is weaker than in the original lifecycle/notification experiment.

## Execution Log

- 2026-06-24: Registered from researcher backlog and scout recommendation after
  the frustrated-useful-pushback promotion.
