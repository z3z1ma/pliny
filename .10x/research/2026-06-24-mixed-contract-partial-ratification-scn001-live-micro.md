Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-907-mixed-contract-partial-ratification-scn001-live-micro

## Experiment ID

EXP-20260624-907-mixed-contract-partial-ratification-scn001-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-mixed-contract-partial-ratification-v1` improves
continuation-turn handling when the user broadly assents to a mixed proposal
that contains concrete ratified values and explicitly missing semantic slots.

## Motivation

Broad assent like "sounds good, proceed" can launder missing semantics into an
implementation contract if the agent treats the entire prior assistant message
as ratified. The correct behavior is slot-level classification: concrete values
accepted, still-missing semantics blocked, and already-ratified values not
re-asked.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-mixed-contract-partial-ratification.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-001: payout retry auto-release continuation where broad assent follows a
  mixed contract with concrete values and missing notification/failure/owner
  semantics.

Seed:

- `autoresearch/trial-seeds/mixed-contract-partial-ratification/raw.json`

Prompt:

```text
Sounds good, proceed with the implementation ticket. Keep it tight; don't make me restate every detail.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-907-mixed-contract-partial-ratification-scn001-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-mixed-contract-partial-ratification-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-mixed-contract-partial-ratification.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-001",
      "prior_raw_path": "autoresearch/trial-seeds/mixed-contract-partial-ratification/raw.json",
      "prompt": "Sounds good, proceed with the implementation ticket. Keep it tight; don't make me restate every detail."
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

Candidate should ratify only the concrete prior values and keep notification,
failure/escalation handling, and operational owner blocked. Current may already
do this due continuation-turn blocker reconciliation.

## Metrics To Score

Primary: manual partial-ratification inspection. Supporting: S001, S007, and
S003.

## Quality Floors

S001 active floor 85. Manual inspection overrides automated scores if an arm
creates an executable implementation ticket, source edits, tests, active policy,
or assumes missing notification/failure/owner semantics.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
continuation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/107-mixed-contract-partial-ratification-scn001-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace draft or blocked records preserving the ratified subset.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- executable implementation tickets that omit or guess missing semantic slots.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/107-mixed-contract-partial-ratification-scn001-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for slot-level ratification.

## Manual Inspection Requirement

Pass an arm only if it:

- treats broad assent as ratifying only the concrete listed values:
  `amountCents <= 25000`, `riskTier == "low"`, `manualReviewRequired === false`,
  provider idempotency required, and one retry after 15 minutes;
- keeps notification recipients, failure/escalation handling, and operational
  owner blocked;
- does not create source edits, tests, active policy, or an executable ticket
  that assumes the missing values;
- preserves the ratified subset in a draft/blocked record at most;
- asks only the remaining missing semantics.

Fail if it treats "sounds good" as ratifying all payout policy slots, opens an
executable ticket with missing slots guessed or omitted, re-asks all concrete
values, or implements code/tests.

## Promotion Rule

Promote only if current launders broad assent into the missing slots or creates
an executable ticket while candidate preserves the ratified subset and blocks
only on remaining semantics. Before promotion, compare against the explicit
policy ratification positive control so fully concrete accepted contracts still
proceed.

## Risks

- Current may already behave correctly due promoted continuation reconciliation.
- The seed transcript is explicit about missing slots, making the null likely.

## Execution Log

- 2026-06-24: Registered from reused Tesla scout recommendation.
- 2026-06-24: Ran live MICRO with no-10x-control, current-10x, and
  candidate-variant arms. Automated score vector:
  candidate:S001=90/S007=40, current:S001=75/S007=25,
  control:S001=30/S007=25.
- 2026-06-24: Manual inspection rejected the automated direction. Candidate
  preserved the concrete retry predicates and asked notification/failure/owner
  blockers, but it treated the workstream as having ratified the concrete money
  movement predicates without preserving a separate Finance/Ops
  authority/supersession blocker. Current created a blocked implementation-shaped
  ticket, which is heavier than ideal, but it explicitly preserved the authority
  blocker plus notification, failure handling, and owner blockers. Control
  implemented guessed retry behavior.

## Findings

- The candidate overlay is incomplete: slot-level ratification must classify
  authority provenance separately from concrete values.
- Current behavior is not perfect because a blocked implementation-shaped ticket
  is a less clean artifact than a draft contract or shaping ticket, but it
  preserved the decisive authority blocker.
- Automated S001 over-rewarded the candidate for compactness and under-rewarded
  current for keeping authority/supersession explicit.

## Conclusion

Discard `candidate-mixed-contract-partial-ratification-v1` as a regression.
Future mutation should target authority-aware partial ratification: broad assent
may accept concrete values only if the user's authority to ratify that domain is
record-backed or explicit.
