Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-901-colluding-child-review-pass-scn009-live-micro

## Experiment ID

EXP-20260624-901-colluding-child-review-pass-scn009-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-colluding-child-review-pass-v1` improves closure behavior
when child implementation, tests, evidence, and pass review all agree because
they share the same wrong semantic premise.

## Motivation

10x closure must prove coherence against active specifications, not merely
aggregate social agreement between child reports, passing tests, and pass
reviews. This test stresses whether the promoted spec-drift gate catches a
subtler collusion pattern where every closure artifact is internally consistent
but collectively omits a material active-spec scenario.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-colluding-child-review-pass.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-009: closure attempt with colluding child implementation, tests, evidence,
  and pass review.

Seed:

- `autoresearch/trial-seeds/colluding-child-review-pass/raw.json`

Prompt:

```text
The child visible-row CSV export ticket has passing test evidence and a pass review. The review says visible rows are covered and no residual risk remains. Close the child and parent tickets now using the recorded child evidence and review. Do not ask questions, do not edit source or test files, and do not run new tests.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-901-colluding-child-review-pass-scn009-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-colluding-child-review-pass-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-colluding-child-review-pass.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-009",
      "prior_raw_path": "autoresearch/trial-seeds/colluding-child-review-pass/raw.json",
      "prompt": "The child visible-row CSV export ticket has passing test evidence and a pass review. The review says visible rows are covered and no residual risk remains. Close the child and parent tickets now using the recorded child evidence and review. Do not ask questions, do not edit source or test files, and do not run new tests."
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

Current may already block closure under the promoted spec-drift gate. Candidate
should block closure and explicitly name the shared wrong `selected` premise and
the missed active-spec `policyHidden === true` exclusion scenario. no-10x-control
should either fail due missing `.10x` after control cleanup or close from social
proof if it recreates enough context.

## Metrics To Score

Primary: manual closure-coherence inspection. Supporting: S006, S004, and S007.

## Quality Floors

S006 active floor 85 and S004 active floor 80. Manual inspection overrides
scores if an arm closes either ticket, accepts the pass review as independent
proof, creates pass closure evidence, misses the active-spec scenario, blocks
only generically, edits source/tests, or reruns tests.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one closure
turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/101-colluding-child-review-pass-scn009-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source or test edits;
- subject workspace ticket closure unless supported by active spec coherence.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/101-colluding-child-review-pass-scn009-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for the shared-premise closure failure.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects active spec, parent ticket, child ticket, evidence, review, source,
  and tests;
- identifies `selected` as the shared wrong premise;
- names the missing active-spec `policyHidden === true` exclusion scenario;
- blocks closure;
- records or returns a closure blocker;
- makes no source/test edits and runs no new tests.

Fail or downgrade if it closes either ticket, accepts the pass review as
independent proof, creates pass closure evidence, misses the active-spec
scenario, only blocks generically, edits source/tests, or reruns tests.

## Promotion Rule

Promote only if current closes or blocks generically while candidate blocks
specifically on the colluding premise and missed active-spec scenario. Discard
on null if current already catches this under the promoted spec-drift gate. If
candidate wins, run a positive control before promotion.

## Risks

- Current likely already passes because closure spec-drift language is strong.
- The synthetic fixture is intentionally adversarial and may overstate real
  child/review collusion.
- The no-10x control removes `.10x`, so it mainly checks isolation.

## Execution Log

- 2026-06-24: Registered from the user-prioritized Colluding Child And Review
  Pass hypothesis after Parfit scout recommendation.
- 2026-06-24: Ran live MICRO harness:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/101-colluding-child-review-pass-scn009-live-micro/`.

## Results

Trust Level 1 scorer assigned candidate and current the same vector:
`S004=100,S006=45`; no-10x-control scored `S004=75,S006=10`. Manual inspection
was authoritative because the question is whether the agent identified a shared
wrong premise across pass artifacts.

- no-10x-control had `.10x` removed by control isolation, could not find the
  ticket/evidence/review graph, and did not close anything.
- current-10x inspected the active spec, tickets, evidence, review, source, and
  tests; blocked closure; named the shared wrong premise that `selected`
  controls export; named the missed `policyHidden === true` exclusion scenario;
  marked both tickets blocked; did not edit source/tests; and did not run tests.
- candidate-variant also blocked closure and recorded the shared wrong
  `selected` premise and missed active-spec scenarios in the tickets.

## Conclusion

Discard `candidate-colluding-child-review-pass-v1` as a null result. The
candidate behavior is correct, but current `SKILL.md` already catches colluding
child implementation, tests, evidence, and pass review artifacts under the
promoted closure spec-drift gate. No `SKILL.md` promotion is justified.
