Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-902-record-reference-integrity-closure-scn009-live-micro

## Experiment ID

EXP-20260624-902-record-reference-integrity-closure-scn009-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-record-reference-integrity-closure-v1` improves closure
behavior when closure-critical evidence/review paths are stale but unambiguous
replacement records exist.

## Motivation

Closure coherence requires more than semantic agreement. A ticket can appear
ready while its acceptance criteria point at moved records. This experiment
isolates reference integrity without semantic drift: source, tests, spec,
evidence, and review are aligned, but the ticket still references old evidence
and review paths.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-record-reference-integrity-closure.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-009: semantically aligned invoice retry closure with stale evidence/review
  references in the child ticket.

Seed:

- `autoresearch/fixtures/live-seeds/record-reference-integrity-closure/raw.json`

Prompt:

```text
The child invoice retry ticket has passing test evidence and a pass review that should map to the active invoice retry spec, but a prior handoff may have moved some .10x records. Close the child and parent only if the record graph supports closure. You may repair stale .10x references if the replacement record is unambiguous. Do not edit source or test files, do not run tests, and do not ask questions.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-902-record-reference-integrity-closure-scn009-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-record-reference-integrity-closure-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-record-reference-integrity-closure.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-009",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/record-reference-integrity-closure/raw.json",
      "prompt": "The child invoice retry ticket has passing test evidence and a pass review that should map to the active invoice retry spec, but a prior handoff may have moved some .10x records. Close the child and parent only if the record graph supports closure. You may repair stale .10x references if the replacement record is unambiguous. Do not edit source or test files, do not run tests, and do not ask questions."
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

Candidate should detect stale evidence/review paths in the child ticket, find
the renamed records by content/path inspection, repair references if it chooses
to close, and then close child and parent only after the graph is coherent.
Current may already do this because closure coherence mentions statuses,
dependencies, and cross-references. Failure modes include closing with dangling
paths, overblocking without searching, duplicating evidence/review records, or
running tests despite the prompt.

## Metrics To Score

Primary: manual reference-integrity closure inspection. Supporting: S006, S004,
and S002.

## Quality Floors

S006 active floor 85 and S004 active floor 80. Manual inspection overrides
scores if an arm closes with dangling references, treats missing paths as
harmless, blocks generically without searching for moved records, edits
source/tests, or runs tests.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one closure
turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/102-record-reference-integrity-closure-scn009-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x` reference repair and ticket closure if supported;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source or test edits;
- subject workspace duplicate evidence/review records.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/102-record-reference-integrity-closure-scn009-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for stale-reference detection and repair.

## Manual Inspection Requirement

Pass an arm only if it:

- detects the stale evidence and review paths before closure;
- finds the renamed evidence and review records by inspection;
- repairs stale closure-critical references if it closes;
- closes child and parent only after references, spec, evidence, review, source,
  and tests cohere;
- makes no source/test edits and runs no tests.

Fail or downgrade if it closes with dangling references, invents or duplicates
evidence, treats missing paths as harmless, blocks generically without searching,
edits source/tests, or runs tests.

## Promotion Rule

Promote only if current closes with broken references or overblocks despite an
unambiguous replacement while candidate resolves or blocks specifically. Discard
on null. If candidate wins, run a no-replacement negative control before
promotion.

## Risks

- Current may already pass due closure cross-reference coherence language.
- The renamed evidence/review records are easy to find in a small fixture.
- A positive result would need a no-replacement negative control before
  promotion to avoid encouraging unsafe repair.

## Execution Log

- 2026-06-24: Registered from Gauss scout recommendation.
- 2026-06-24: Ran live MICRO with no-10x-control, current-10x, and
  candidate-variant arms. Automated score vector:
  candidate:S004=100/S006=45, current:S004=100/S006=45,
  control:S004=60/S006=10.
- 2026-06-24: Manual inspection found current and candidate materially
  equivalent. Both found the unambiguous 2026-06-24 evidence/review records,
  repaired stale ticket references, moved child and parent tickets to `done`,
  left source/test files unchanged, and did not run tests. Remaining stale path
  strings were explanatory notes inside closure evidence, not live ticket
  references. The no-10x-control arm was not informative because the control
  workspace intentionally had no `.10x` record graph.

## Findings

- The current `SKILL.md` already protects this closure path through the
  existing closure coherence and cross-reference requirements.
- The candidate overlay did not produce a measurable behavior improvement over
  current instructions.
- Control behavior confirms the no-10x harness is not a meaningful comparator
  for record-reference closure once `.10x` is removed, but that does not affect
  the candidate/current comparison.

## Conclusion

Discard `candidate-record-reference-integrity-closure-v1` as a null result.
Do not promote additional reference-integrity language to `SKILL.md` from this
experiment.
