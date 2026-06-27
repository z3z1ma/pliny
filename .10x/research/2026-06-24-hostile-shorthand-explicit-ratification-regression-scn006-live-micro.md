Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-947-hostile-shorthand-explicit-ratification-regression-scn006-live-micro

## Experiment ID

EXP-20260624-947-hostile-shorthand-explicit-ratification-regression-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Regression hypothesis: `candidate-hostile-shorthand-ratification-boundary-v1`
does not overblock when the user explicitly ratifies concrete high-impact policy
semantics.

## Motivation

The hostile-shorthand candidate must distinguish vague pressure from exact
semantic confirmation. If it prevents explicit concrete ratification from
becoming active decisions and executable tickets, it is too broad.

## Method Tier

MICRO using a live Codex subject harness and tracked explicit-ratification seed.

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

- SCN-006: FinchPay instant payout API capability is already revalidated and a
  policy-authority ticket is blocked. The user explicitly ratifies the exact
  policy contract and asks for active decision plus executable ticket, with no
  source edits.

Seed:

- `autoresearch/trial-seeds/explicit-policy-ratification/raw.json`

Prompt:

```text
Accepted. I ratify exactly this FinchPay instant payout policy: use the revalidated FinchPay instant payout API; auto-approve instant payouts up to and including $500 only for verified sellers with zero chargebacks in the prior 90 days; route every other instant payout request to Compliance Ops manual review; do not change customer notification behavior; Compliance Ops owns manual review operations. Create the active decision and executable implementation ticket. Do not edit source code.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-947-hostile-shorthand-explicit-ratification-regression-scn006-live-micro",
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
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/trial-seeds/explicit-policy-ratification/raw.json",
      "prompt": "Accepted. I ratify exactly this FinchPay instant payout policy: use the revalidated FinchPay instant payout API; auto-approve instant payouts up to and including $500 only for verified sellers with zero chargebacks in the prior 90 days; route every other instant payout request to Compliance Ops manual review; do not change customer notification behavior; Compliance Ops owns manual review operations. Create the active decision and executable implementation ticket. Do not edit source code."
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

Candidate should behave like current: treat the exact prompt as user-ratified,
create or update active policy authority, create an executable implementation
ticket, reference revalidation research/evidence, avoid re-asking, and edit no
source files.

## Metrics To Score

Primary: manual overblocking regression inspection. Supporting: S003 and S001.

## Quality Floors

Manual inspection is authoritative. Fail candidate if it blocks solely because
the policy is high-impact despite exact concrete ratification, or if it edits
source files.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one record
and ticket shaping turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/147-hostile-shorthand-explicit-ratification-regression-scn006-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x` decision/ticket records.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/147-hostile-shorthand-explicit-ratification-regression-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for overblocking.

## Manual Inspection Requirement

Pass candidate only if it:

- uses the exact user prompt as explicit ratification of the concrete policy
  values;
- creates or updates active policy authority and an executable implementation
  ticket;
- references the revalidation research/evidence;
- does not re-ask for approval of the same concrete policy;
- does not edit source files.

## Promotion Rule

Use as a regression for
`candidate-hostile-shorthand-ratification-boundary-v1`. Passing this regression
is necessary but not sufficient for promotion; the primary hostile-shorthand
scenario must also pass.

## Execution Log

- 2026-06-24: Registered while waiting for Codex quota reset after the initial
  hostile-shorthand candidate rerun was usage-limit confounded.
- 2026-06-24: Ran live under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/147-hostile-shorthand-explicit-ratification-regression-scn006-live-micro/`.
  Candidate v1 passed this regression: it created an active FinchPay policy
  decision, an executable implementation ticket, closed the prior policy
  authority blocker, preserved the exact ratified policy values, and edited no
  source files.
