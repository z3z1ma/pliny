Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-929-external-pr-discussion-decision-index-scn004-live-micro

## Experiment ID

EXP-20260624-929-external-pr-discussion-decision-index-scn004-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can index an external PR discussion that has the
force of a durable engineering decision without copying the whole thread or
creating implementation work.

## Motivation

External artifact coverage currently includes a Google Doc PRD thin index and a
positive control where local `.10x` becomes canonical. The conformance map still
marks PR-discussion decisions as a gap. This MICRO tests external decision
indexing rather than external specification indexing.

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

- SCN-004: an exported GitHub PR discussion is the canonical review artifact but
  contains an accepted idempotency-key decision that should be locally
  discoverable through `.10x`.

Seed:

- `autoresearch/trial-seeds/external-pr-discussion-decision-index/raw.json`

Prompt:

```text
The exported PR discussion at `external-artifacts/github/PR-482-acme-webhook-retry-thread.md` contains an accepted engineering decision about ACME webhook idempotency keys. The PR discussion remains the canonical review artifact. Make the local `.10x` record graph aware of the decision so future agents can find and classify it. Do not implement anything, do not edit source files, and do not copy the whole PR discussion into `.10x`. Create the minimal durable `.10x` record needed.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-929-external-pr-discussion-decision-index-scn004-live-micro",
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
      "id": "SCN-004",
      "prior_raw_path": "autoresearch/trial-seeds/external-pr-discussion-decision-index/raw.json",
      "prompt": "The exported PR discussion at `external-artifacts/github/PR-482-acme-webhook-retry-thread.md` contains an accepted engineering decision about ACME webhook idempotency keys. The PR discussion remains the canonical review artifact. Make the local `.10x` record graph aware of the decision so future agents can find and classify it. Do not implement anything, do not edit source files, and do not copy the whole PR discussion into `.10x`. Create the minimal durable `.10x` record needed."
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

Current should read the PR discussion, create one decision-class `.10x` record
with context, decision, alternatives/tradeoff, consequences, and a durable
pointer to the PR discussion. It should state that the PR discussion remains the
canonical review artifact, avoid copying the full thread, and avoid
implementation work.

## Metrics To Score

Primary: manual external decision indexing inspection. Supporting: S002, S003,
and S005.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm ignores the PR
discussion, creates the wrong record type without decision classification,
copies the whole thread, omits the canonical pointer, treats `.10x` as replacing
the PR artifact, edits source, or opens implementation work.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one record
creation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/129-external-pr-discussion-decision-index-scn004-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x/decisions/` index record.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- implementation tickets.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/129-external-pr-discussion-decision-index-scn004-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for external decision indexing.

## Manual Inspection Requirement

Pass an arm only if it:

- reads `external-artifacts/github/PR-482-acme-webhook-retry-thread.md`;
- creates exactly one decision-class `.10x/decisions/` record or equivalent
  durable decision index;
- includes `Status`, `Created`, and `Updated` headers;
- names the accepted decision: ACME webhook idempotency uses
  `provider_delivery_id`, not `event_id`;
- includes context, decision, alternatives/tradeoff, and consequences;
- includes the PR URL, PR/thread identifier, export path, and observed status;
- states the PR discussion remains the canonical review artifact;
- avoids copying the full discussion;
- avoids source/test edits and implementation tickets.

Fail or downgrade if it ignores the artifact, creates only a vague knowledge
note, copies the whole thread, omits the durable pointer, treats local `.10x` as
replacing the PR artifact, or opens implementation work.

## Promotion Rule

No behavioral candidate is under test; `candidate-variant` duplicates
`current-10x` only to satisfy the current runner's fixed arm contract. If
current fails, create a narrow candidate targeting external decision indexing.

## Risks

- The prompt is direct, so this is a conformance coverage case more than an
  adversarial ambiguity case.
- The no-10x control may still create a plausible `.10x` record because the
  prompt explicitly names `.10x`.

## Execution Log

- 2026-06-24: Registered from the external artifact indexing backlog after the
  Google Doc PRD thin-index and local-canonical positive controls.
- 2026-06-24: Ran live. All arms created one
  `.10x/decisions/acme-webhook-idempotency-key.md` record and avoided source
  edits or implementation tickets. Current captured the accepted decision and
  tradeoff but omitted available canonical URL/thread/status/export metadata.

## Results

Automated Trust Level 1 score vectors:

- current-10x: `S002=60`
- candidate-variant: `S002=60`
- no-10x-control: `S002=60`

Manual inspection found current `SKILL.md` partially passed:

- created a decision-class `.10x/decisions/` record;
- identified `provider_delivery_id` as the accepted ACME webhook idempotency
  key and `event_id` as rejected;
- included context, decision, alternatives, and consequences;
- stated the PR discussion remains the canonical review artifact;
- avoided copying the whole PR discussion;
- avoided source/test edits and implementation tickets.

Manual concern:

- current omitted the canonical PR discussion URL, thread id, observed PR status,
  and export timestamp even though the seed artifact exposed all four.

The duplicate-current arm included the canonical URL but still omitted explicit
PR status and thread id fields. This indicates a stochastic provenance-quality
weakness, not a complete inability to index external decisions.

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/129-external-pr-discussion-decision-index-scn004-live-micro/`

Supporting records:

- `.10x/evidence/2026-06-24-external-pr-discussion-decision-index-result.md`
- `.10x/reviews/2026-06-24-external-pr-discussion-decision-index-result.md`

## Conclusions

Current `SKILL.md` handles external PR discussions as decision-shaped durable
context, but the external provenance language is too loose. Create and test a
narrow candidate that requires external index records to preserve available
canonical URL, external id, observed status, revision/export date, local export
path, and explicit canonical-authority statement.
