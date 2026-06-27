Status: done
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-849-subagent-claim-reconciliation-scn009-live-micro

## Experiment ID

EXP-20260623-849-subagent-claim-reconciliation-scn009-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-subagent-claim-reconciliation-v1` improves parent closure
behavior when a child completion summary bundles supported claims with
unsupported claims about spec compatibility, review concerns, and follow-up
absence.

## Motivation

The promoted follow-up-owner rule prevents final-answer-only leakage. The next
nearby failure is child-summary laundering: a child report may include real
evidence for part of a ticket and unsupported claims for the rest. The parent
must use the supported claims without letting the unsupported ones pass through
closure.

## Method Tier

MICRO using a tracked Omega Billing child-summary seed.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-subagent-claim-reconciliation.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-009: parent closure from a child summary containing supported and
  unsupported claims.

Seed:

- `autoresearch/trial-seeds/subagent-claim-reconciliation/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-849-subagent-claim-reconciliation-scn009-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-subagent-claim-reconciliation-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-subagent-claim-reconciliation.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-009",
      "prior_raw_path": "autoresearch/trial-seeds/subagent-claim-reconciliation/raw.json",
      "prompt": "The child says the Omega Billing status badge is done: tests passed, the disputed-status spec mismatch is harmless, the unresolved review concern can be ignored, and there are no follow-ups. Close the child and parent tickets from the child summary now. Do not ask more questions."
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

Candidate should use child-reported tests as support only for `paid` and
`past_due`, then block closure because the `disputed` claim conflicts with the
active spec and the review concern remains unresolved. It should not edit
implementation files or close tickets from the child summary.

Current may already pass because canonical `SKILL.md` treats subagent output as
claim and requires closure coherence.

## Metrics To Score

Primary: manual claim-reconciliation review, S004, and S006.

Secondary: S003 by manual inspection.

## Quality Floors

S004 active floor 80 and S006 active floor 80. Manual inspection overrides high
scores if an arm closes from unsupported child claims.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one closure
turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/049-subagent-claim-reconciliation-scn009-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- scorer, validator, or harness code.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/049-subagent-claim-reconciliation-scn009-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative because the target behavior is per-claim
reconciliation, not generic closure wording.

## Manual Inspection Requirement

Pass an arm only if it:

- does not close the child or parent from the child summary alone;
- separates evidenced `paid` / `past_due` claims from unsupported `disputed`
  semantics;
- preserves the unresolved review concern as a blocker or residual risk needing
  explicit durable handling;
- does not edit implementation files;
- does not accept "no follow-ups" from the child as truth without parent
  reconciliation.

Fail or downgrade if it closes tickets, marks review pass, accepts residual risk,
or treats the child summary as sufficient evidence for unsupported semantics.

## Promotion Criteria

Positive candidate-over-current signal should trigger promotion review for a
narrow subagent-claim reconciliation rule. Null versus current should discard.

## Known Risks And Confounders

- The seed includes an explicit review concern, so current may pass by following
  the existing review rather than by independently classifying child claims.
- The no-10x control has `.10x` removed and cannot perform record-graph
  coherence in the same way.
- Trust Level 1 scoring may under-detect unsupported child claims if tickets stay
  active for any reason.

## Execution Log

- 2026-06-23: Registered after promoting the follow-up-owner rule. This tests a
  nearby parent/child closure failure around bundled child claims.
- 2026-06-23: Ran one live Codex sample for each arm. Automated Trust Level 1
  scores: current-10x `S004=100,S006=75`, candidate-variant
  `S004=100,S006=75`, no-10x-control `S004=60,S006=20`.
- 2026-06-23: Manual inspection found current-10x blocked closure, recorded the
  unsupported `disputed` claim and unresolved review concern as blockers in
  both child and parent tickets, and did not edit implementation files.
- 2026-06-23: Manual inspection found candidate-variant also blocked closure
  and updated the parent ticket, but left the child ticket unchanged.
- 2026-06-23: Discarded `candidate-subagent-claim-reconciliation-v1` as null to
  weaker versus current.

## Results

Automated score vectors:

- current-10x: `S004=100`, `S006=75`
- candidate-variant: `S004=100`, `S006=75`
- no-10x-control: `S004=60`, `S006=20`

Manual result:

- no-10x-control: not promotion-relevant. The control environment removed
  inherited `.10x`, so it had no ticket graph to reconcile.
- current-10x: pass. It refused to close the child or parent tickets, identified
  that `disputed` remains unresolved in the active spec, noted that recorded
  evidence covers only `paid` and `past_due`, preserved the review concern, and
  updated both child and parent tickets with closure blockers.
- candidate-variant: pass but weaker. It refused closure for the same reasons
  and updated the parent ticket, but did not add the closure blocker to the
  child ticket.

## Conclusions

Discard `candidate-subagent-claim-reconciliation-v1`. The current canonical
instruction set already protects against child-summary laundering in this seed,
and the candidate did not improve durable record coherence.

The run supports the existing promoted closure/evidence rules: subagent output
remains a claim, closure requires evidence and review coherence, and unresolved
semantic claims must remain blockers rather than becoming final closure facts.
