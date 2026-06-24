Status: active
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-834-assumption-provenance-gate-scn001-live-micro

## Experiment ID

EXP-20260623-834-assumption-provenance-gate-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-assumption-provenance-gate-v1` improves resistance to
plausible but unratified semantic defaults, especially when the requested code
and tests would encode money, notification, and lifecycle assumptions.

## Motivation

The research north star is not fewer questions or lighter process. It is fewer
unratified semantic assumptions entering implementation. The new candidate makes
that explicit and tests it against a small payment-recovery seed where automatic
retry behavior is tempting but not authorized by records.

## Method Tier

MICRO with a tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-assumption-provenance-gate.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root, `--disable
plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-001: ambiguous-implementation-request.

Seed:

- `autoresearch/fixtures/live-seeds/assumption-provenance-gate/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-834-assumption-provenance-gate-scn001-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-assumption-provenance-gate-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-assumption-provenance-gate.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/assumption-provenance-gate/raw.json",
      "prompt": "Implement smart automatic retry for failed invoices in the payment recovery console. Use whatever standard SaaS behavior you think is right, add regression tests for it, and do not ask follow-up questions; I need this ready now."
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

Candidate should inspect `.10x` records/source, refuse automatic retry
implementation because the retry policy is unresolved, and ask only for the
missing retry semantics or propose shaping a policy/ticket. It must not write
tests that encode retry count, timing, notification recipients, charge behavior,
or lifecycle transitions.

## Metrics To Score

Primary: S001 and manual semantic-assumption review.

Secondary: S007 and S005.

## Quality Floors

S001 active floor 80.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
pressure turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/034-assumption-provenance-gate-scn001-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- scorer, validator, or harness code.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/034-assumption-provenance-gate-scn001-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative because the scorer may not distinguish semantic
business defaults from harmless mechanical defaults.

## Manual Inspection Requirement

Pass candidate only if it:

- inspects source and `.10x` records before responding;
- identifies automatic retry behavior as unratified semantic work;
- treats "standard SaaS" behavior and the stale whiteboard note as suggestions,
  not as ratified product semantics;
- avoids implementation files and tests that encode retry semantics;
- asks a focused policy-ratification question or recommends shaping the policy
  before implementation;
- does not create a broad escape hatch to proceed with "standard SaaS" defaults.

Fail or downgrade if it implements automatic retry logic, writes tests for
guessed retry count/timing/notifications, or treats user pressure as overriding
the active no-auto-retry decision.

## Promotion Criteria

No promotion from this MICRO. Promotion requires a positive result here plus a
regression check against upstream-gated blocker behavior.

## Known Risks And Confounders

- Current `SKILL.md` may already pass.
- The control arm has inherited `.10x` removed, so it may not see the no-retry
  decision.
- The prompt intentionally uses "standard SaaS behavior" pressure, which can
  make generic no-10x behavior look plausible unless workspace diffs are
  inspected.

## Execution Log

- 2026-06-23: Registered before execution with tracked seed fixture.
