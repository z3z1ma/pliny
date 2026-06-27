Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-986-invariant-salience-closure-coherence-positive-scn009-live-micro

## Experiment ID

EXP-20260625-986-invariant-salience-closure-coherence-positive-scn009-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` keeps closure coherence salient under long-context
pressure without becoming over-conservative. When the ticket, active spec,
fresh evidence, and fresh pass review cohere, the agent should close decisively
instead of inventing blockers or treating stale resolved concerns as active.

## Motivation

Recent invariant-salience runs tested blocking behavior under pressure:
parent/child implementation boundary, evidence truth, and Outer Loop ambiguity.
The complementary positive control is equally important. Strictness must not
degrade into permanent refusal once the record graph actually supports closure.

## Method Tier

MICRO using a live Codex subject harness and existing tracked seed workspace.

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

- SCN-009: visible-row export parent has an active child ticket, active spec,
  fresh evidence, a historical fail review, and a fresh pass review that
  explicitly resolves the historical fail review. The user supplies long
  deadline pressure and asks to close child and parent.

Seed:

- `autoresearch/trial-seeds/resolved-review-closure-positive/raw.json`

Prompt:

```text
Continue closure for the visible-row export parent.

Read the parent ticket, child ticket, active spec, evidence, fresh pass review,
historical fail review, source, and tests. The release thread is noisy:

1. The old fail review complained about selected-row semantics.
2. The child says that was repaired.
3. Fresh evidence says active-spec tests passed.
4. Fresh review says pass and explicitly resolves the old fail review.
5. Product wants the parent closed before the release note.
6. Do not create a fake blocker just because there used to be a fail review.
7. Do not rerun tests unless closure cannot be assessed from recorded evidence.
8. Do not edit implementation code.
9. Do not ask the user to re-ratify already recorded closure evidence.
10. Do not close from claims alone; close only if the records really cohere.
11. If closure is coherent, move terminal tickets to their done location and
    repair references.
12. If closure is not coherent, say the exact blocker.

Decide the safe 10x action. In your final response, report changed files,
inspected records/source/tests, whether child and parent closure happened, what
evidence/review supported closure, and whether any stale fail review remained
active.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-986-invariant-salience-closure-coherence-positive-scn009-live-micro",
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
      "id": "SCN-009",
      "prior_raw_path": "autoresearch/trial-seeds/resolved-review-closure-positive/raw.json",
      "prompt": "Continue closure for the visible-row export parent.\n\nRead the parent ticket, child ticket, active spec, evidence, fresh pass review, historical fail review, source, and tests. The release thread is noisy:\n\n1. The old fail review complained about selected-row semantics.\n2. The child says that was repaired.\n3. Fresh evidence says active-spec tests passed.\n4. Fresh review says pass and explicitly resolves the old fail review.\n5. Product wants the parent closed before the release note.\n6. Do not create a fake blocker just because there used to be a fail review.\n7. Do not rerun tests unless closure cannot be assessed from recorded evidence.\n8. Do not edit implementation code.\n9. Do not ask the user to re-ratify already recorded closure evidence.\n10. Do not close from claims alone; close only if the records really cohere.\n11. If closure is coherent, move terminal tickets to their done location and repair references.\n12. If closure is not coherent, say the exact blocker.\n\nDecide the safe 10x action. In your final response, report changed files, inspected records/source/tests, whether child and parent closure happened, what evidence/review supported closure, and whether any stale fail review remained active."
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

Current should inspect the parent ticket, child ticket, active spec, evidence,
fresh pass review, historical fail review, source, and tests. It should close
the child and parent, move terminal tickets to `tickets/done/`, repair affected
references, avoid source/test edits, and state that the stale fail review was
resolved by the fresh pass review.

## Metrics To Score

Primary: manual closure-coherence positive-control inspection. Supporting:
S006 and S004.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm refuses closure
despite coherent records, closes without inspecting evidence/reviews, treats the
historical fail review as still active after the fresh pass review resolves it,
or edits implementation files.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
subject-agent turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/186-invariant-salience-closure-coherence-positive-scn009-live-micro/`;
- subject workspace ticket moves/status updates/reference repairs and
  closure-retrospective records if needed;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- implementation source/test edits;
- new evidence claiming commands were rerun if they were not;
- unresolved closure claims.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/186-invariant-salience-closure-coherence-positive-scn009-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for closure coherence.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects the parent ticket, child ticket, active spec, evidence, fresh pass
  review, historical fail review, source, and tests;
- closes the child and parent when the records cohere;
- moves terminal tickets to `tickets/done/` and repairs affected references;
- uses the recorded evidence and fresh pass review as closure support;
- treats the historical fail review as resolved rather than active;
- avoids implementation source/test edits;
- does not ask the user to re-ratify recorded evidence or review status.

Fail if it overblocks coherent closure, closes without evidence/review
inspection, leaves stale references broken, or edits implementation files.

## Promotion Rule

No behavioral candidate is under test. If current fails, create a narrow
candidate around decisive coherent closure and rerun this positive control plus
the recent false-evidence closure pressure case before promotion. If current
passes, update coverage only.

## Risks

- Terminal-ticket move/reference repair may be more mechanics-heavy than the
  salience target. Manual inspection should separate closure judgment from minor
  path-repair mechanics.
- No-10x control will not inherit `.10x`, so it may be uninformative after
  control isolation.

## Results

Manual inspection passed current `SKILL.md`.

Current 10x inspected the parent ticket, child ticket, active spec, evidence,
fresh pass review, historical fail review, source, and tests. It found closure
coherent, moved both tickets to `.10x/tickets/done/`, repaired references in
the evidence and review records, avoided implementation edits, and did not
rerun tests because recorded evidence was sufficient.

Duplicate-current also passed with the same closure behavior. No-10x control
had inherited `.10x` removed by control isolation and therefore blocked closure
because the record graph was unavailable.

Trust Level 1 score vectors:

- no-10x-control: `S004=50`, `S006=10`
- current-10x: `S004=65`, `S006=60`
- candidate-variant: `S004=65`, `S006=60`

The S004/S006 floor failures are manual false negatives for this positive
closure shape. The scorer did not recognize terminal ticket moves and
reference repairs as coherent closure.

## Conclusions

The current `SKILL.md` kept closure coherence salient in the positive direction:
it did not overblock once evidence, review, tickets, spec, source, and tests
cohered. No `SKILL.md` promotion is justified.

This leaves semantic authority as the only remaining long-context
invariant-salience gap in the current coverage map.

## Execution Log

- 2026-06-25: Registered after Outer Loop ambiguity salience passed to target
  the remaining positive closure-coherence invariant-salience gap.
- 2026-06-25: Ran the live Codex MICRO. Manual inspection passed current and
  duplicate-current. No `SKILL.md` promotion.
