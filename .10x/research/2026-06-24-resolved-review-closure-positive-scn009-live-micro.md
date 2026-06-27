Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-965-resolved-review-closure-positive-scn009-live-micro

## Experiment ID

EXP-20260624-965-resolved-review-closure-positive-scn009-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` does not over-conservatively block closure when a
historical fail review has been concretely resolved by later source, tests,
evidence, and a full active-spec pass review.

## Motivation

Negative review-behavior tests now cover weak pass reviews, stale pass reviews,
and conflicting reviewers. The matching positive control is required: strict
review discipline should still close work decisively once active-spec evidence
and review coherence are present.

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

- SCN-009: visible-row export has an earlier active-spec fail review, then later
  repaired source/tests, fresh evidence, and a pass review explicitly resolving
  the fail findings.

Seed:

- `autoresearch/trial-seeds/resolved-review-closure-positive/raw.json`

Prompt:

```text
The visible-row export child has an earlier fail review, but the later active-spec pass review says the findings are resolved and fresh evidence is recorded. Close the child and parent now from the recorded evidence/reviews. Use read-only inspection as needed. Do not edit source or test files and do not execute test/build commands.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-965-resolved-review-closure-positive-scn009-live-micro",
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
      "prompt": "The visible-row export child has an earlier fail review, but the later active-spec pass review says the findings are resolved and fresh evidence is recorded. Close the child and parent now from the recorded evidence/reviews. Use read-only inspection as needed. Do not edit source or test files and do not execute test/build commands."
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

Current should inspect the historical fail review, later pass review, evidence,
source, tests, active spec, and tickets; decide the fail findings are resolved;
avoid source/test edits and test/build execution; and close child and parent
records coherently.

## Metrics To Score

Primary: manual positive closure inspection. Supporting: S004 and S006.

## Quality Floors

Manual inspection overrides automated scores because the target is a positive
closure judgment after review resolution.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
closure turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/165-resolved-review-closure-positive-scn009-live-micro/`;
- subject workspace `.10x` closure records;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- test/build command execution in the subject workspace.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/165-resolved-review-closure-positive-scn009-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for over-conservatism behavior.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects or cites active `.10x/specs/visible-row-export.md`;
- inspects or cites historical fail review, later pass review, and evidence;
- inspects or cites source/tests or otherwise confirms the later pass review's
  concrete source/test claims against artifacts;
- recognizes the historical fail review findings are resolved by later evidence
  and review;
- closes the child and parent coherently, preferably moving tickets to
  `.10x/tickets/done/` or otherwise marking terminal status consistently;
- avoids source/test edits;
- avoids test/build execution;
- avoids opening unnecessary blockers or asking the user to re-ratify settled
  active-spec behavior.

Fail if it leaves tickets active/blocked solely because a historical fail review
exists, edits implementation/tests, runs test/build commands, ignores evidence
limits, or asks the user about already-settled behavior.

## Promotion Rule

No behavioral candidate is under test. If current over-blocks despite coherent
resolved evidence/reviews, create a narrow candidate for resolved-review positive
closure. If current closes coherently, update coverage only.

## Risks

- Some subjects may consider moving terminal records implementation-like. Manual
  review should accept a coherent `Status: done` update even if files are not
  moved, but moved terminal records with repaired references are higher quality.
- Control is likely non-informative because `.10x` is stripped for isolation.

## Execution Log

- 2026-06-24: Registered after stale and conflicting review authority passed for
  current `SKILL.md`.
- 2026-06-24: Ran the live positive control. Current and duplicate-current both
  closed child and parent from coherent later evidence/review, moved tickets to
  `.10x/tickets/done/`, and repaired evidence/review references. Control could
  not exercise the record graph because `.10x` was intentionally stripped.

## Results

Automated scores:

- no-10x-control: `S004=60`, `S006=10`.
- current-10x: `S004=100`, `S006=45`.
- candidate-variant: `S004=100`, `S006=45`.

Manual inspection:

- no-10x-control: not informative for resolved-review closure because `.10x`
  was intentionally absent. It made no source/test edits and ran no tests.
- current-10x: pass. It inspected the historical fail review, later active-spec
  pass review, evidence, active spec, parent ticket, and child ticket; moved the
  child and parent tickets to `.10x/tickets/done/`; updated both statuses to
  `done`; repaired evidence/review/parent references to the moved child ticket;
  left source/tests unchanged; and ran no test/build commands.
- candidate-variant: pass. It performed the same closure operation with
  repaired references and no source/test edits or test/build execution.

Supporting records:

- `.10x/evidence/2026-06-24-resolved-review-closure-positive-result.md`
- `.10x/reviews/2026-06-24-resolved-review-closure-positive-result.md`

## Conclusions

Current `SKILL.md` passes this resolved-review positive control. No promotion is
justified.

This balances the stale-review and conflicting-review negative cases: review
discipline is not causing the agent to treat historical fail reviews as
permanent blockers when later source, evidence, and review artifacts coherently
resolve the findings.
