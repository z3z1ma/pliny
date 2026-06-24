Status: active
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-908-record-graph-supersession-reference-repair-scn004-live-micro

## Experiment ID

EXP-20260624-908-record-graph-supersession-reference-repair-scn004-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-record-lifecycle-reference-repair-v1` improves record
graph maintenance when a decision is superseded and references must be repaired
by occurrence role rather than blind path replacement.

## Motivation

Prior record-reference tests showed current can repair stale closure paths.
This experiment tests a harder lifecycle operation: superseding an active
decision while active records, review/evidence headers, historical prose, and
fenced command-output examples all mention the old decision path.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-record-lifecycle-reference-repair.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-004: FinchPay manual-review decision is explicitly superseded; record
  references must be selectively repaired.

Seed:

- `autoresearch/fixtures/live-seeds/record-graph-supersession-reference-repair/raw.json`

Prompt:

```text
Finance has now explicitly ratified a new FinchPay policy: auto-approve verified sellers with `sellerRiskTier === "low"` and `amountCents <= 50000`; route all other instant payouts to manual Finance review; no customer notification changes. Supersede `.10x/decisions/finchpay-instant-payout-review-policy.md` with a new active decision and make the record graph coherent. Repair live `.10x` references that should follow the supersession, but do not broad-rewrite historical notes, quoted command output, or fenced code blocks that mention the old path as history. Do not edit source files and do not run tests.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-908-record-graph-supersession-reference-repair-scn004-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-record-lifecycle-reference-repair-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-record-lifecycle-reference-repair.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-004",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/record-graph-supersession-reference-repair/raw.json",
      "prompt": "Finance has now explicitly ratified a new FinchPay policy: auto-approve verified sellers with `sellerRiskTier === \"low\"` and `amountCents <= 50000`; route all other instant payouts to manual Finance review; no customer notification changes. Supersede `.10x/decisions/finchpay-instant-payout-review-policy.md` with a new active decision and make the record graph coherent. Repair live `.10x` references that should follow the supersession, but do not broad-rewrite historical notes, quoted command output, or fenced code blocks that mention the old path as history. Do not edit source files and do not run tests."
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

Candidate should supersede the old decision, keep active references coherent,
update review/evidence headers that continue to point at the old decision, and
leave historical body text and fenced command output unchanged. Current may
already do this or may either leave stale live references or over-broaden path
replacement.

## Metrics To Score

Primary: manual record-reference lifecycle inspection. Supporting: S002, S003,
and S006.

## Quality Floors

S002 active floor 80. Manual inspection overrides automated scores if an arm
leaves stale live references, broad-rewrites historical/code-block mentions,
duplicates active decisions, edits source, or runs tests.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one record
maintenance turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/108-record-graph-supersession-reference-repair-scn004-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x` record supersession and reference repair.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source edits;
- test execution.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/108-record-graph-supersession-reference-repair-scn004-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for occurrence-role reference repair.

## Manual Inspection Requirement

Pass an arm only if it:

- creates a new active decision for the ratified policy;
- moves the old decision to `.10x/decisions/superseded/` and marks it
  `Status: superseded`;
- keeps active spec/ticket references pointed at the active governing decision;
- updates review/evidence headers that target the old decision to the moved
  superseded path where appropriate;
- leaves historical prose and fenced code blocks unchanged when they mention
  the old path as history;
- avoids source/test edits, test runs, duplicate active decisions, and unrelated
  formatting churn.

Fail or downgrade if it leaves dangling live references, performs blind global
replacement inside historical notes/code blocks, rewrites unrelated content,
creates duplicate active decisions, edits source, or runs tests.

## Promotion Rule

Promote only if current leaves stale live references or performs broad
replacement in historical/code-block text while candidate repairs references
selectively. If candidate wins, run a no-replacement negative control before
promotion.

## Risks

- Reusing the same active decision path for the new decision can make active
  spec/ticket references trivially coherent.
- Some historical prose is subjective; manual inspection must distinguish live
  links from history.

## Execution Log

- 2026-06-24: Registered from reused Kierkegaard scout recommendation.
