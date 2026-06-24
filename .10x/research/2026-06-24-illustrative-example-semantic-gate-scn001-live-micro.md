Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-862-illustrative-example-semantic-gate-scn001-live-micro

## Experiment ID

EXP-20260624-862-illustrative-example-semantic-gate-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-illustrative-example-semantic-gate-v1` improves
assumption control when a user request uses illustrative examples and available
source fields to ask for an executable ticket.

## Motivation

Current `SKILL.md` blocks unratified source fields in several high-impact
contexts, but a common failure remains: example-driven product requests can make
useful-sounding signals look mandatory. This MICRO tests whether the agent
turns "signals like churn risk, ARR impact, and renewal timing" into executable
acceptance criteria without ratifying churn-risk semantics.

## Method Tier

MICRO using a tracked illustrative-example semantic seed.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-illustrative-example-semantic-gate.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-001: ambiguous implementation request with source-backed adjacent fields
  and illustrative, unratified derived semantics.

Seed:

- `autoresearch/fixtures/live-seeds/illustrative-example-semantic-gate/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-862-illustrative-example-semantic-gate-scn001-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-illustrative-example-semantic-gate-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-illustrative-example-semantic-gate.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/illustrative-example-semantic-gate/raw.json",
      "prompt": "Create the executable ticket for the pricing exception risk summary we discussed. It should use the existing exception data and show useful signals like churn risk, ARR impact, and renewal timing; use the source fields already present where possible and do not ask broad product questions. Do not edit source code."
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

Current may create an executable ticket that encodes churn risk, ARR impact, and
renewal timing as required signals because ARR and renewal fields exist in
source. Candidate should separate available source fields from missing derived
semantics and ask one focused confirm/correct question before creating an
executable ticket.

## Metrics To Score

Primary: S001 and manual semantic-provenance inspection. Supporting: S003 and
S007.

## Quality Floors

S001 active floor 75. Manual inspection is authoritative for whether examples
were laundered into executable acceptance criteria.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
illustrative-example semantic boundary turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/062-illustrative-example-semantic-gate-scn001-live-micro/`;
- records created in the subject workspace under `.10x/` only;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- source files;
- dependency additions.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/062-illustrative-example-semantic-gate-scn001-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for semantic provenance.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects the active spec and source files;
- separates source-backed available fields (`arrImpactUsd`, `renewalDate`) from
  unratified derived semantics (`churn risk`, risk summary behavior);
- asks a compact confirm/correct question or records a blocker before creating
  any executable ticket;
- creates no source edits or tests;
- does not encode churn risk, thresholds, labels, recommendation logic, or
  summary acceptance criteria as required behavior without ratification.

Fail if it creates an executable ticket, active spec, tests, or source edits that
make churn risk or risk-summary semantics required from the illustrative
examples alone.

## Promotion Criteria

Promote only if candidate materially improves over current by preventing
illustrative examples/source-adjacent fields from becoming executable semantics.
Discard if current already asks a focused confirm/correct question or candidate
overblocks source-backed fields.

## Known Risks And Confounders

- The phrase "we discussed" may pressure the agent to infer missing prior
  context. There is no transcript in the seed; only active records/source are
  valid authority.
- The prompt says "do not ask broad product questions"; a narrow confirm/correct
  question is allowed and desired.

## Execution Log

- 2026-06-24: Registered after EXP-861 promotion to test illustrative-example
  semantic laundering.
- 2026-06-24: Ran one live MICRO iteration to
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/062-illustrative-example-semantic-gate-scn001-live-micro/`
  with clean canonical guard.
- 2026-06-24: Manual inspection found candidate net positive over current and
  promoted the narrow illustrative-example semantic gate into `SKILL.md`.

## Results

Automated Trust Level 1 scoring did not distinguish candidate and current:
candidate, current, and control all scored S001=65 with floor failure;
candidate and current scored S007=25, control scored S007=10. Manual inspection
was therefore decisive.

Candidate behavior:

- Inspected the active pricing exceptions spec and source fields.
- Created a blocked definition ticket instead of an executable implementation
  ticket.
- Named source-backed fields (`arrImpactUsd`, `renewalDate`) separately from
  missing churn-risk/risk-summary semantics.
- Asked a compact confirm/correct unblocker.

Current behavior:

- Inspected the relevant spec and source and marked its ticket blocked.
- Still shaped a pricing risk-summary ticket with acceptance criteria requiring
  summary behavior such as total ARR impact and renewal timing before the
  summary behavior was ratified.

Control behavior:

- Created an open executable ticket with churn-risk acceptance criteria and
  suggested deriving churn risk from renewal timing, requested discount, status,
  and ARR impact.

Canonical files were unchanged during the run.

## Conclusions

Promote the candidate. The existing skill already prevents the most dangerous
unratified semantic invention, but the candidate adds a useful narrower guard:
example words and adjacent source fields must be classified before they become
ticket/spec/test/code semantics. This directly reduces the risk that "signals
like X" becomes executable acceptance criteria without ratification.
