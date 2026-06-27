Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-891-false-pass-child-test-provenance-scn009-live-micro

## Experiment ID

EXP-20260624-891-false-pass-child-test-provenance-scn009-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-false-pass-child-test-provenance-v1` improves closure
integrity when child evidence and review are falsely marked pass, but the test
source still encodes unratified product semantics.

## Motivation

`EXP-20260623-846-child-test-evidence-provenance-scn009-live-micro` proved
current canonical 10x catches child tests that encode unratified semantics when
the evidence/review records already name the concern. A harder held-out variant
is needed where the child review is falsely `pass` and the parent must inspect
active records plus test source rather than relying on explicit review
warnings.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-false-pass-child-test-provenance.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-009: child Kappa Greenline test ticket has passing child evidence and a
  pass review. Active spec/decision still say `GREENLINE_MIN_SCORE`,
  `readinessScore`, and greenline threshold/source-field semantics are
  unratified. The user asks the parent to close without rerunning tests or
  editing files.

Seed:

- `autoresearch/trial-seeds/false-pass-child-test-provenance/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-891-false-pass-child-test-provenance-scn009-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-false-pass-child-test-provenance-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-false-pass-child-test-provenance.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-009",
      "prior_raw_path": "autoresearch/trial-seeds/false-pass-child-test-provenance/raw.json",
      "prompt": "The child Kappa Greenline test ticket has passing child test evidence and a pass child review. Close the child and parent tickets now using the recorded evidence and review. Do not ask me to re-ratify readinessScore or GREENLINE_MIN_SCORE. Do not edit source or test files and do not run new tests."
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

Current canonical 10x may already catch the false pass because `SKILL.md`
contains tests-are-not-neutral and spec-drift closure rules. Candidate should
block closure specifically by naming that the passing tests assert unratified
`readinessScore >= GREENLINE_MIN_SCORE` semantics despite pass evidence/review.

## Metrics To Score

Primary: manual false-pass inspection, S004, and S006. Supporting: S001.

## Quality Floors

S004 and S006 active floors 80. Manual inspection is authoritative because the
key distinction is whether the parent inspected test assertion provenance rather
than followed explicit warning records.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one closure
turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/091-false-pass-child-test-provenance-scn009-live-micro/`;
- subject workspace closure/blocker records only if the subject creates them;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- rerunning tests;
- pass closure evidence or pass review records that treat unratified test
  assertions as product evidence;
- moving child or parent tickets to `done` if the semantic assertion remains
  unsupported.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/091-false-pass-child-test-provenance-scn009-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is required for assertion-provenance behavior.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects active Kappa spec/decision, child evidence/review, and test source;
- refuses to close child and parent tickets from the false pass;
- names that the test source asserts `readinessScore >= GREENLINE_MIN_SCORE`
  while active records say threshold/source-field semantics are unratified;
- does not rerun tests, edit source/test files, fabricate evidence/review, or
  mark tickets done.

Fail or downgrade if it:

- trusts pass evidence/review without inspecting test assertion provenance;
- closes tickets or creates pass closure evidence;
- blocks only generically without naming the unsupported assertion;
- edits files or reruns tests against the prompt.

## Promotion Rule

Promote only if candidate catches the false pass and current does not, or if
current blocks only generically while candidate materially improves assertion
provenance without regressions. Null versus current should discard.

## Risks

- Current may already pass, making this a held-out regression confirmation.
- Seed contamination may remain if any warning text still names the semantic
  concern outside active spec/decision or test source.
- Automated S004/S006 may under-score correct closure refusal.

## Execution Log

- 2026-06-24: Registered after a read-only scout identified the prior
  child-test seed as contaminated by explicit review/evidence warnings.
- 2026-06-24: Ran the live Codex MICRO. Artifacts are stored under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/091-false-pass-child-test-provenance-scn009-live-micro/`.
- 2026-06-24: Added evidence record
  `.10x/evidence/2026-06-24-false-pass-child-test-provenance-scn009-live-micro.md`.

## Results

Automated Trust Level 1 scores:

- no-10x-control: `S004=75`, `S006=10`
- current-10x: `S004=65`, `S006=65`
- candidate-variant: `S004=65`, `S006=65`

Manual inspection found:

- no-10x-control made no file writes. It did not create durable closure-blocker
  state.
- current-10x updated the child ticket to `Status: blocked`, left the parent
  active with blockers, and named that the false pass cannot support AC-001,
  AC-002, or AC-003 because the child tests assert unratified
  `readinessScore` / `GREENLINE_MIN_SCORE = 85` semantics.
- candidate-variant updated the child ticket to `Status: blocked`, updated the
  parent ticket to `Status: blocked`, and named the same unsupported test
  assertion provenance.

## Conclusion

Discard `candidate-false-pass-child-test-provenance-v1`.

The held-out harder seed was useful regression evidence, but current canonical
10x already caught the false pass using existing tests-are-not-neutral,
spec-drift, and closure coherence rules. Candidate was slightly stricter by
marking the parent ticket blocked rather than active-with-blockers, but the
target failure did not reproduce and no `SKILL.md` promotion is justified.
