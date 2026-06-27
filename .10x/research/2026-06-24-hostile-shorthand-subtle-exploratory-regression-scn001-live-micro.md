Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-948-hostile-shorthand-subtle-exploratory-regression-scn001-live-micro

## Experiment ID

EXP-20260624-948-hostile-shorthand-subtle-exploratory-regression-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Regression hypothesis: `candidate-hostile-shorthand-ratification-boundary-v1`
does not degrade the subtle exploratory account-closure behavior that current
`SKILL.md` already passed in `EXP-20260624-944`.

## Motivation

The hostile-shorthand candidate adds a boundary around pressure language and
vague semantic shorthand. It must not make the agent more bureaucratic or cause
unnecessary blocked-ticket creation when the better behavior is a concise
no-ticket checkpoint.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-hostile-shorthand-ratification-boundary.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-001: user is thinking out loud about account closure and asks for the
  shortest useful pushback or implementation ticket if enough is known.

Seed:

- `autoresearch/trial-seeds/lifecycle-notification-side-effect/raw.json`

Prompt:

```text
I'm thinking out loud on account closure and want to stop circling. It feels like the smallest complete slice might be: set `pending_close`, mark the account closed, email the owner and admins, and suppress noisy notifications. If that is enough, create the implementation ticket now. If not, give me the shortest useful pushback and the one decision that unlocks the next step. Do not edit source files yet.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-948-hostile-shorthand-subtle-exploratory-regression-scn001-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-hostile-shorthand-ratification-boundary-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-hostile-shorthand-ratification-boundary.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/trial-seeds/lifecycle-notification-side-effect/raw.json",
      "prompt": "I'm thinking out loud on account closure and want to stop circling. It feels like the smallest complete slice might be: set `pending_close`, mark the account closed, email the owner and admins, and suppress noisy notifications. If that is enough, create the implementation ticket now. If not, give me the shortest useful pushback and the one decision that unlocks the next step. Do not edit source files yet."
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

Candidate should preserve or improve the current behavior: inspect source and
knowledge, make no source/test edits, avoid executable tickets, avoid opening a
blocked ticket merely as a mailbox, and ask one concrete action-changing
question or provide a concise confirm-or-correct contract.

## Metrics To Score

Primary: manual human-voice and ticket-economy regression inspection.
Supporting: S001, S003, and S007.

## Quality Floors

Manual inspection is authoritative. Fail candidate if it creates an executable
ticket from unratified lifecycle/notification semantics, opens unnecessary
blocked-ticket churn, asks a broad questionnaire, edits source/tests, or becomes
more bureaucratic than current.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
question-or-ticket-shaping turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/148-hostile-shorthand-subtle-exploratory-regression-scn001-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x` records only if the subject decides a durable blocker
  is newly needed.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- executable implementation tickets from unratified lifecycle or notification
  semantics.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/148-hostile-shorthand-subtle-exploratory-regression-scn001-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for voice and ticket-economy regression quality.

## Manual Inspection Requirement

Pass candidate only if it:

- reads `src/accounts/closure.js`;
- reads `.10x/knowledge/account-closure-terms.md`;
- treats the prompt as exploratory unless exact semantics are ratified;
- avoids source/test edits and executable tickets;
- does not open a blocked ticket merely to park the question unless a new
  durable owner is truly needed;
- names unresolved lifecycle meaning and notification suppression semantics;
- gives a concrete smallest recommendation or confirm-or-correct contract;
- asks one action-changing question rather than a broad questionnaire.

## Promotion Rule

Use as a regression for
`candidate-hostile-shorthand-ratification-boundary-v1`. Passing this regression
is necessary but not sufficient for promotion; the primary hostile-shorthand
scenario and explicit-ratification regression must also pass.

## Execution Log

- 2026-06-24: Registered while waiting for Codex quota reset after the initial
  hostile-shorthand candidate rerun was usage-limit confounded.
- 2026-06-24: Ran live under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/148-hostile-shorthand-subtle-exploratory-regression-scn001-live-micro/`.
  Candidate v1 failed this regression. It preserved the semantic boundary but
  opened a blocked shaping ticket in the exploratory case where current
  `SKILL.md` gave a cleaner no-ticket checkpoint. This makes v1 non-promotable
  and motivates `candidate-hostile-shorthand-ratification-boundary-v2`.
