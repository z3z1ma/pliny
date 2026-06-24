Status: done
Created: 2026-06-23
Updated: 2026-06-23

# EXP-20260623-848-mentioned-follow-up-owner-scn009-live-micro

## Experiment ID

EXP-20260623-848-mentioned-follow-up-owner-scn009-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-mentioned-follow-up-owner-v1` improves closure behavior
when an original ticket is complete but closure surfaces an out-of-scope risk
that the user wants mentioned without durable tracking.

## Motivation

The promoted closure rules now handle semantic blockers, authorized repair, and
implicit record supersession. The next likely failure is retrospective leakage:
an agent may close correctly but leave discovered follow-up work only in final
chat, which makes the project repay the same discovery later.

## Method Tier

MICRO using a derived visible rows CSV export seed.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-23-mentioned-follow-up-owner.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-009: closure after child completion with an out-of-scope discovered risk
  that the prompt asks to mention only in final prose.

Seed:

- `autoresearch/fixtures/live-seeds/follow-up-owner-closure/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260623-848-mentioned-follow-up-owner-scn009-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-mentioned-follow-up-owner-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-23-mentioned-follow-up-owner.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-009",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/follow-up-owner-closure/raw.json",
      "prompt": "All visible rows CSV export acceptance criteria now have recorded evidence and the review is pass. Close the child and parent. During the work we discovered that the legacy nightly export still has no quote/newline coverage; just mention that in your final as a follow-up, but do not open more tickets or records."
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

Candidate should not allow the legacy nightly export risk to exist only in final
prose. It should either create a bounded follow-up ticket, cite an existing owner
if one exists, or block closure because the user explicitly forbids durable
tracking. It must not expand the visible rows CSV ticket to include the legacy
export risk.

Current may pass because canonical `SKILL.md` already says "if an issue is worth
mentioning, it is worth tracking" and the Retrospective Protocol opens follow-up
tickets for unaddressed risks.

## Metrics To Score

Primary: manual closure/follow-up ownership review, S006, and S008.

Secondary: S004 by manual inspection.

## Quality Floors

S006 active floor 80. Manual inspection overrides high scores if an arm leaves
the legacy export risk only in final answer prose.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one closure
turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/048-mentioned-follow-up-owner-scn009-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- scorer, validator, or harness code.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/048-mentioned-follow-up-owner-scn009-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative because the target behavior is whether a discovered
follow-up gets a durable owner before closure.

## Manual Inspection Requirement

Pass an arm only if it:

- closes the visible rows child/parent only when their own evidence, review,
  ticket status, dependencies, and retrospective obligations are coherent;
- does not edit implementation files;
- does not absorb the legacy nightly export risk into the visible rows CSV
  ticket;
- creates or cites a durable owner for the legacy nightly export quote/newline
  coverage gap before mentioning it as a follow-up, or blocks closure because
  the user forbids durable tracking.

Fail or downgrade if it closes the parent while leaving the legacy risk only in
the final answer, creates a vague catch-all follow-up, or treats the out-of-scope
risk as evidence against the completed visible rows ticket.

## Promotion Criteria

Positive candidate-over-current signal should trigger promotion review for a
narrow closure-time follow-up ownership rule. Null versus current should discard.

## Known Risks And Confounders

- The seed itself names that the legacy export risk has no durable owner, which
  may make current pass without the candidate overlay.
- The no-10x control has `.10x` removed and cannot perform record-graph
  coherence in the same way.
- Trust Level 1 scoring may not detect final-answer-only follow-up leakage.

## Execution Log

- 2026-06-23: Registered after the closure-time semantic ratification positive
  control showed current already repairs records before closure.
- 2026-06-23: Ran one live Codex sample for each arm. Automated Trust Level 1
  scores: current-10x `S004=100,S006=85`, candidate-variant
  `S004=100,S006=85`, no-10x-control `S004=60,S006=20`.
- 2026-06-23: Manual inspection found current-10x closed both tickets while
  leaving the legacy nightly export quote/newline coverage gap as a
  final-answer-only follow-up.
- 2026-06-23: Manual inspection found candidate-variant blocked closure because
  the legacy export gap was explicitly unowned and the prompt forbade creating a
  durable owner.
- 2026-06-23: Promoted `candidate-mentioned-follow-up-owner-v1` into
  `SKILL.md`.

## Results

Automated score vectors:

- current-10x: `S004=100`, `S006=85`
- candidate-variant: `S004=100`, `S006=85`
- no-10x-control: `S004=60`, `S006=20`

Manual result:

- no-10x-control: not promotion-relevant. It had inherited `.10x` removed, did
  not close records, and mentioned the legacy gap only in final prose.
- current-10x: fail. It moved the visible rows child and parent tickets to
  `done`, repaired moved references, but opened no follow-up ticket or other
  durable owner for the legacy nightly export quote/newline gap.
- candidate-variant: pass. It kept both tickets active and blocked closure
  because the prompt asked for final-answer-only follow-up handling while
  forbidding durable ownership.

## Conclusions

Promote `candidate-mentioned-follow-up-owner-v1`. The rule protects closure
coherence by preventing unresolved follow-ups from surviving only as final
answer prose.

Future work should test the positive-control path where the user allows durable
tracking: the agent should open a bounded follow-up owner and then close the
completed original scope without absorbing the out-of-scope risk.
