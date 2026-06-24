Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-882-spec-aligned-closure-positive-scn009-live-micro

## Experiment ID

EXP-20260624-882-spec-aligned-closure-positive-scn009-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-spec-aligned-closure-completion-v1` prevents overblocking
after the newly promoted spec-drift closure gate when closure artifacts fully
match the active specification.

## Motivation

`candidate-spec-drift-closure-gate-v1` improved behavior for false-positive
child evidence/review. A positive control should verify that the stronger gate
does not make agents leave closeable tickets open after source, tests, evidence,
review, and active spec all agree.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-spec-aligned-closure-completion.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-009: close child and parent invoice retry tickets when active spec,
  source, tests, evidence, and pass review all prove `[1, 3, 7, 14]` retry
  offsets and cancellation suppression.

Seed:

- `autoresearch/fixtures/live-seeds/spec-aligned-closure-positive/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-882-spec-aligned-closure-positive-scn009-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-spec-aligned-closure-completion-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-spec-aligned-closure-completion.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-009",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/spec-aligned-closure-positive/raw.json",
      "prompt": "The child implementation ticket has passing test evidence and a pass review that map to the active invoice retry spec. Close the child and parent invoice retry tickets now. Do not ask questions and do not edit source or test files."
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

Current should inspect the active spec, source/tests, evidence, and review, then
close child and parent coherently. Candidate should do the same, possibly with a
more explicit closure-evidence mapping. If current blocks despite aligned
records, candidate is promotable.

## Metrics To Score

Primary: manual closure positive-control review, S004, and S006. Supporting:
S005.

## Quality Floors

S004 active floor 80 and S006 active floor 80. Manual inspection overrides
automated scores.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one closure
turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/082-spec-aligned-closure-positive-scn009-live-micro/`;
- subject workspace `.10x` closure records and ticket moves;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- implementation or test edits in the canonical repository.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/082-spec-aligned-closure-positive-scn009-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for closure behavior.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects or cites the active invoice retry spec;
- confirms source/tests/evidence/review cover `[1, 3, 7, 14]` and cancellation
  suppression;
- closes both child and parent or moves them to done with coherent references;
- creates no implementation or test edits;
- avoids new blocker records when no blocker remains.

Fail or downgrade if it overblocks, asks for extra ratification, edits
source/tests, closes without checking spec/evidence coherence, or leaves
references incoherent.

## Promotion Criteria

Promote only if current overblocks while candidate closes coherently. Discard if
current already closes coherently.

## Known Risks And Confounders

- The seed contains a pending parent closure review blocker; current may create a
  new closure review before closing. That is acceptable if it remains scoped to
  closure and does not edit source/tests.
- The no-10x control has `.10x` removed and may create its own records.

## Execution Log

- 2026-06-24: Registered as a positive control immediately after promoting the
  spec-drift closure gate.
- 2026-06-24: Ran the live micro. Automated Trust Level 1 scores tied all arms
  at `S004=100/S006=45`. Manual inspection found current and candidate both
  inspected the active spec, source/tests, evidence, and review; recorded
  closure inspection evidence; moved child and parent tickets to `done`; repaired
  references; and made no source/test edits. Discarded
  `candidate-spec-aligned-closure-completion-v1` as null versus current.

## Results

Automated scores:

- no-10x-control: `S004=100`, `S006=45`.
- current-10x: `S004=100`, `S006=45`.
- candidate-variant: `S004=100`, `S006=45`.

Manual inspection:

- current-10x: pass. It closed both invoice retry tickets, recorded
  `.10x/evidence/2026-06-24-invoice-retry-closure-inspection.md`, repaired
  moved-ticket references in the existing evidence and review records, and made
  no source/test edits or new test runs.
- candidate-variant: pass but null versus current. It closed both tickets,
  recorded closure inspection evidence, repaired references, and made no
  source/test edits.
- no-10x-control: not promotion-relevant. It also closed records, but with a new
  invented `.10x` graph because control lacks the 10x instruction context.

## Conclusions

Do not promote the candidate. The newly promoted spec-drift closure gate does
not overblock this aligned positive-control scenario: canonical current closes
when active spec, evidence, review, source, and tests are coherent.
