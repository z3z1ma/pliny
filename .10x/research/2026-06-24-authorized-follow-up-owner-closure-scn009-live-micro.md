Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-863-authorized-follow-up-owner-closure-scn009-live-micro

## Experiment ID

EXP-20260624-863-authorized-follow-up-owner-closure-scn009-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-authorized-follow-up-owner-closure-v1` improves closure
behavior when the user authorizes durable tracking for an out-of-scope follow-up
discovered during completed work.

## Motivation

`candidate-mentioned-follow-up-owner-v1` was promoted from a negative case where
the user forbade durable tracking and the correct behavior was to block closure.
The positive-control path still needs live testing: after the agent opens or
cites a bounded follow-up owner, it should not keep completed original work open
solely because that separate follow-up remains unresolved.

## Method Tier

MICRO using the tracked follow-up-owner closure seed.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-authorized-follow-up-owner-closure.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-009: closure coherence with complete original evidence/review and a
  separate out-of-scope follow-up that needs a durable owner.

Seed:

- `autoresearch/trial-seeds/follow-up-owner-closure/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-863-authorized-follow-up-owner-closure-scn009-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-authorized-follow-up-owner-closure-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-authorized-follow-up-owner-closure.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-009",
      "prior_raw_path": "autoresearch/trial-seeds/follow-up-owner-closure/raw.json",
      "prompt": "All visible rows CSV export acceptance criteria now have recorded evidence and the review is pass. Close the child and parent. During the work we discovered that the legacy nightly export still has no quote/newline coverage. Open or update the smallest durable follow-up owner if needed, then close the completed visible-rows child and parent. Do not edit implementation files."
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

Current may either overblock closure because the legacy export gap remains
unfixed, or close while creating an imprecise owner. Candidate should open or
reuse a bounded legacy nightly export quote/newline coverage follow-up, close
only the visible-rows child and parent, and cite the follow-up owner separately.

## Metrics To Score

Primary: manual closure/follow-up owner inspection and S006. Supporting: S008
and S005.

## Quality Floors

S006 active floor 75. Manual inspection is authoritative for whether the
follow-up has a bounded owner and original closure is coherent.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one closure
turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/063-authorized-follow-up-owner-closure-scn009-live-micro/`;
- records created in the subject workspace under `.10x/` only;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- implementation files;
- dependency additions.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/063-authorized-follow-up-owner-closure-scn009-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for follow-up-owner and closure coherence.

## Manual Inspection Requirement

Pass an arm only if it:

- reads the child ticket, parent ticket, evidence, and review records;
- creates or cites a bounded durable owner for the legacy nightly export
  quote/newline coverage gap;
- does not edit implementation files;
- closes the visible-rows child and parent only if their own acceptance
  criteria, evidence, review, statuses, dependencies, specifications, and
  retrospective obligations are coherent;
- separates the closed visible-rows scope from the unresolved legacy export
  follow-up owner in records or final response.

Fail if it leaves the legacy gap final-answer-only, absorbs the legacy gap into
the visible-rows ticket, creates only a vague catch-all follow-up, edits source,
or keeps the visible-rows child/parent open solely because the separately owned
legacy follow-up is unresolved.

## Promotion Criteria

Promote only if candidate materially improves over current on authorized
follow-up owner closure. Discard if current already opens/cites a bounded owner
and closes the coherent original scope.

## Known Risks And Confounders

- The existing promoted rule may already be sufficient.
- Trust Level 1 scoring may not distinguish precise versus vague follow-up
  ownership; manual inspection is decisive.

## Execution Log

- 2026-06-24: Registered as the positive-control follow-up-owner closure test.
- 2026-06-24: Ran one live MICRO iteration to
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/063-authorized-follow-up-owner-closure-scn009-live-micro/`
  with clean canonical guard.
- 2026-06-24: Manual inspection found candidate null versus current and marked
  `candidate-authorized-follow-up-owner-closure-v1` discarded.

## Results

Automated Trust Level 1 scores:

- no-10x-control: S004=65, S006=55.
- current-10x: S004=65, S006=85.
- candidate-variant: S004=65, S006=85.

Manual inspection found:

- current-10x opened
  `.10x/tickets/2026-06-24-add-nightly-export-quote-newline-coverage.md`,
  moved the visible-rows child and parent tickets to `done`, repaired evidence
  and review references to the moved child ticket, and edited no implementation
  files.
- candidate-variant opened
  `.10x/tickets/2026-06-24-add-legacy-nightly-export-quote-newline-coverage.md`,
  moved the same child and parent tickets to `done`, preserved the out-of-scope
  legacy gap as a separate owner, and edited no implementation files.
- no-10x-control also created a follow-up owner and closed records, but it
  renamed/mirrored seed evidence and review records rather than preserving the
  original record graph shape.

Canonical `SKILL.md` and `autoresearch/program.md` were unchanged during the
run.

## Conclusions

Discard the candidate as null versus current. The existing promoted
follow-up-owner and closure rules already support the positive-control path:
when the user authorizes durable tracking, the agent opens a bounded follow-up
owner and closes the completed original scope once its own evidence and review
cohere.
