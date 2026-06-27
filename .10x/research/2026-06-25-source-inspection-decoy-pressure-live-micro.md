Status: done
Created: 2026-06-25
Updated: 2026-06-25

# EXP-20260625-711-source-inspection-decoy-pressure-live-micro

## Experiment ID

EXP-20260625-711-source-inspection-decoy-pressure-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: under source-inspection decoy pressure, canonical `SKILL.md` should
use records and import authority to converge on the few source files that
matter, rather than reading every plausible UI, analytics, legacy, fixture,
test, API, or job file just because it appears in the repository inventory.

## Motivation

EXP-710 passed the shell-native source-inspection economy gate: current 10x used
`rg`/`sed`, answered correctly, and made no writes. One current repetition still
read more files than necessary, including fixtures/tests and a second
line-numbered pass. This follow-up tests whether that residual issue becomes
material when the workspace contains more tempting decoys.

The scenario prompt must not mention bash, `rg`, shell-native tools, one-liners,
or over-reading. A pass must come from canonical 10x behavior, not prompt
coaching.

## Method Tier

MICRO using a live Codex subject harness and a tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus a no-op sanity overlay.

## Control

Runner-shaped conformance probe. Compare current-10x to the minimal control and
the no-op candidate overlay, but the main verdict is current canonical behavior.

## Scenario Set

1. SCN-003 source-inspection decoy pressure:
   `autoresearch/trial-seeds/source-inspection-decoy-pressure/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260625-711-source-inspection-decoy-pressure-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 2,
  "arms": [
    {
      "id": "no-10x-control",
      "instruction_source": "minimal Codex instruction",
      "instruction_text": "You are a coding agent. Answer the user's task directly."
    },
    {
      "id": "current-10x",
      "instruction_source": "SKILL.md",
      "instruction_path": "SKILL.md"
    },
    {
      "id": "candidate-variant",
      "instruction_source": "SKILL.md plus no-op sanity overlay",
      "base_instruction_path": "SKILL.md",
      "instruction_text": "No additional behavior changes. This arm exists only for post-promotion sanity comparison."
    }
  ],
  "scenarios": [
    {
      "id": "SCN-003",
      "prior_raw_path": "autoresearch/trial-seeds/source-inspection-decoy-pressure/raw.json",
      "prompt": "Fresh session. Inspect this workspace's records and source to answer: Which source path owns refund risk summary behavior, what risk levels can it return, and which source files define escalation and threshold semantics? Also call out any tempting but non-authoritative sources you deliberately ignored. Keep the answer concise and cite paths. Do not edit files, run tests, or open records or tickets."
    }
  ],
  "budget": {
    "max_harness_runs": 6,
    "estimated_wall_seconds_per_run": 900,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Current 10x should:

- inspect active `.10x` records before answering;
- locate source authority through repository-native inventory/search and import
  tracing;
- answer that `src/risk/refundRiskSummary.js` owns the summary surface and
  delegates scoring to `src/risk/refundRiskScore.js`;
- identify risk levels `critical`, `high`, `medium`, `low`, and `unknown`;
- cite escalation semantics in `src/risk/rules/escalationRules.js`;
- cite threshold semantics in `src/risk/rules/refundThresholds.js`;
- call out UI labels, analytics dashboard buckets, legacy risk source, tests,
  and fixtures as non-authoritative;
- avoid writes, tests, new records, and tickets.

## Metrics To Score

Primary: manual operation quality under decoy pressure and source/record answer
correctness. Supporting: S001, S002, S003, S005, and S006.

## Quality Floors

Manual inspection is authoritative.

Current fails if:

- it edits files, runs tests, or opens records/tickets;
- it answers from UI labels, analytics names, legacy source, tests, fixtures, or
  guesses instead of source and active records;
- it misses the ownership path, risk-level set, escalation rules, or threshold
  rules;
- after records/imports identify authority, it still reads most unrelated
  decoy files in full rather than treating them as candidate non-authority from
  search/inventory context.

Current does not fail merely for reading one or two tempting decoys to verify
non-authority. The failure mode is broad sequential source browsing when the
record graph and import chain already name the authoritative files.

## Budget And Stop Conditions

Maximum 6 live Codex calls. Timeout 7200 seconds per run. Stop after two
repetitions per arm.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/188-source-inspection-decoy-pressure-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test/docs edits;
- subject workspace `.10x` record edits;
- tests, build outputs, generated artifacts, new tickets, or new records inside
  the subject workspace.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/188-source-inspection-decoy-pressure-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required.

## Promotion Rule

If current over-reads materially under decoy pressure while answering
correctly, create a targeted candidate for source-inspection precision. If
current passes, record coverage and return to the ranked conformance backlog.

## Risks

- Tool-call count alone is not enough; some extra reads may be reasonable for
  non-authority verification.
- The seed is still small compared with a production repository.
- Trust Level 1 scores may not measure operation-quality precision.

## Execution Log

- 2026-06-25: Registered after EXP-710 showed shell-native source inspection
  but one current repetition over-read non-authoritative files.
- 2026-06-25: Ran 6 live Codex calls. Raw artifacts are under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/188-source-inspection-decoy-pressure-live-micro/`.
- 2026-06-25: Manual inspection found current-10x answered correctly and made
  no writes, but failed the operation-quality precision floor by reading most
  decoy files in full after active records/imports identified authority.

## Result

Concerns raised; targeted candidate required.

Evidence:

- `.10x/evidence/2026-06-25-source-inspection-decoy-pressure-result.md`

Review:

- `.10x/reviews/2026-06-25-source-inspection-decoy-pressure-result.md`

Candidate:

- `autoresearch/candidates/2026-06-25-source-inspection-target-precision.md`
