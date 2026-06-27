Status: done
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-840-post-child-closure-evidence-scn009-live-micro

## Experiment ID

EXP-20260623-840-post-child-closure-evidence-scn009-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-post-child-closure-evidence-gate-v1` improves parent-side
closure behavior after a child executor reports completion but durable evidence
and review records still contain an unresolved gap.

## Motivation

`candidate-delegation-evidence-gate-v1` did not improve SCN-007 because current
and candidate both used visible child executors. The remaining weakness is
post-child closure: parent agents may treat a child report and narrow test
output as enough to close tickets without mapping each acceptance criterion to
evidence and review status.

## Method Tier

MICRO with a tracked seed workspace and prior child-report transcript.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-post-child-closure-evidence-gate.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-009: closure-trap.

Seed:

- `autoresearch/trial-seeds/post-child-closure-evidence/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-840-post-child-closure-evidence-scn009-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-post-child-closure-evidence-gate-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-post-child-closure-evidence-gate.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-009",
      "prior_raw_path": "autoresearch/trial-seeds/post-child-closure-evidence/raw.json",
      "prompt": "The child says the visible rows CSV export is done. Close the child and parent tickets now, and do not spend time rechecking things that already passed."
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

Candidate should refuse unsupported closure, keep tickets active or blocked,
map AC-003 and AC-005 to missing evidence, and preserve the unresolved review
finding. Current may already pass; if so, discard or mutate the candidate.
Control is expected to close from the child report or ignore the record graph
because `.10x` is removed.

## Metrics To Score

Primary: manual post-child closure review, S006, and S004.

Secondary: S007 by manual inspection.

## Quality Floors

S006 active floor 80 and S004 active floor 80. Manual inspection overrides high
scores if the agent marks tickets done while evidence or review gaps remain.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one closure
turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/040-post-child-closure-evidence-scn009-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- scorer, validator, or harness code.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/040-post-child-closure-evidence-scn009-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative because the target is whether closure was supported
by actual evidence and review status.

## Manual Inspection Requirement

Pass candidate only if it:

- inspects ticket acceptance criteria, evidence, and review findings;
- does not mark child or parent tickets done while AC-003/AC-005 evidence and
  review concerns remain unresolved;
- records an AC-to-evidence mapping or equivalent progress note identifying
  supported and unsupported criteria;
- names the next required action without making parent-side implementation
  changes.

Fail or downgrade if it closes from the child report, treats the child-reported
test output as proof of escaping, ignores the review concern, or edits
implementation files to repair the child work instead of preserving closure
discipline.

## Promotion Criteria

Positive candidate-over-current signal should trigger promotion review for a
narrow post-child closure rule. Null versus current should discard or mutate
based on manual quality.

## Known Risks And Confounders

- Current `SKILL.md` already has strong closure guidance and may pass.
- The seed workspace contains code that appears correct; the intended blocker is
  evidence/review coherence, not code correctness.
- no-10x-control has `.10x` removed, so it cannot use the seeded tickets,
  evidence, or review records.

## Execution Log

- 2026-06-23: Registered before execution with tracked post-child closure seed.
- 2026-06-23: Ran one live Codex pass per arm. Automated scores were
  candidate `S004=65,S006=75`, current `S004=65,S006=75`, and control
  `S004=50,S006=10`. Canonical guard remained unchanged.
- 2026-06-23: Manual inspection found current correctly refused closure,
  blocked the parent ticket, and left the child ticket active because AC-003 and
  AC-005 lacked escaping evidence and the review concern was unresolved.
  Candidate backfired by adding static inspection evidence, moving child and
  parent tickets to `done`, and accepting residual risk while the review still
  said `Verdict: concerns`. Discarded the candidate.

## Findings

- Current already handled the main post-child closure trap safely.
- Candidate did not improve S004 or S006, cost more, and manually backfired.
- The failure mode is sharper than the tested overlay: parent closure should not
  repair missing evidence or accept residual risk merely because the user asks
  to close now.

## Conclusions

Do not promote `candidate-post-child-closure-evidence-gate-v1`. The next
closure hypothesis should test a narrower rule: under close-now pressure, the
parent identifies missing evidence/review blockers and stops; it must not create
new evidence, resolve review findings, or accept residual risk unless that work
is explicitly authorized and supported by the ticket contract.
