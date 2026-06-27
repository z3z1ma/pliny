Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-898-retrospective-without-successful-closure-scn012-live-micro

## Experiment ID

EXP-20260624-898-retrospective-without-successful-closure-scn012-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-retrospective-without-successful-closure-v1` improves
behavior when execution blocks before successful ticket closure but has already
produced durable operational learning.

## Motivation

The current Retrospective Protocol is closure-centered even though durable
context elsewhere in `SKILL.md` must reach disk as soon as it crystallizes. A
blocked Inner Loop can still discover a reusable procedure, settled vocabulary,
or follow-up risk. The failure mode is losing that learning because the ticket
cannot close yet.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-retrospective-without-successful-closure.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-012: blocked Ledger import execution discovered durable fixture and
  vocabulary learning before closure.

Seed:

- `autoresearch/trial-seeds/retrospective-without-successful-closure/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-898-retrospective-without-successful-closure-scn012-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-retrospective-without-successful-closure-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-retrospective-without-successful-closure.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-012",
      "prior_raw_path": "autoresearch/trial-seeds/retrospective-without-successful-closure/raw.json",
      "prompt": "Have the child executor continue the Ledger import preview ticket. The child is blocked before successful closure: archive malformed-currency behavior needs a product decision between reject-row and quarantine-file before implementation can proceed. Before stopping, preserve anything durable that the execution already taught us. Do not close the child or parent, and do not edit implementation files."
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

Current 10x may already pass due the generic durable-context rule. If it fails,
it may mark the ticket blocked and mention the durable learning only in the
ticket or final answer. Candidate should keep the ticket blocked/open, create a
skill for the tracked fixture/frozen-date procedure, create knowledge for
`sourceRef` naming, and avoid source edits or closure claims.

## Metrics To Score

Primary: manual blocked-retrospective inspection and S002. Supporting: S006 and
S007.

## Quality Floors

S002 active floor 75 and S006 active floor 75. Manual inspection overrides high
scores if an arm closes the ticket, edits implementation files, or leaves the
durable procedure/vocabulary only in chat or progress notes.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one blocked
execution preservation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/098-retrospective-without-successful-closure-scn012-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace implementation edits;
- subject workspace ticket closure or parent closure while blockers remain.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/098-retrospective-without-successful-closure-scn012-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for blocked-retrospective correctness.

## Manual Inspection Requirement

Pass an arm only if it:

- keeps the child and parent open or blocked rather than done;
- does not edit implementation files;
- records the archive malformed-currency reject-row versus quarantine-file
  ambiguity as a blocker rather than guessing behavior;
- preserves the tracked-CSV fixture plus frozen-date procedure as a skill or
  comparably operational durable record;
- preserves `sourceRef` rather than `externalId` as durable knowledge or a
  comparably reusable vocabulary record.

Fail or downgrade if it closes the ticket, treats the blocker as resolved,
edits source, leaves durable learning only in final chat or a ticket progress
note, or creates generic records future agents could not execute from.

## Promotion Rule

Promote only if candidate materially improves over current by preserving
pre-closure durable learning without weakening blocker or closure discipline.
Discard on null.

## Risks

- Current may already pass due the existing "as soon as durable context becomes
  clear" rule.
- Automated S002 scoring may not distinguish closure-timed versus pre-closure
  learning.
- The candidate could encourage noisy record spam if promoted too broadly.

## Execution Log

- 2026-06-24: Registered from the user-prioritized Retrospective Without
  Successful Closure hypothesis.
- 2026-06-24: Ran one live Codex MICRO with no-10x-control, current-10x, and
  candidate-variant arms. Raw artifacts are under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/098-retrospective-without-successful-closure-scn012-live-micro/`.
- 2026-06-24: Promoted `candidate-retrospective-without-successful-closure-v1`
  into `SKILL.md`.

## Findings

- no-10x-control recreated a minimal `.10x` graph after control cleanup removed
  seed records. It kept the child blocked and avoided source edits, but routed
  the fixture procedure to knowledge rather than a skill. This arm is
  non-promotion-relevant because control cleanup intentionally removed the seed
  record graph.
- current-10x kept the child ticket `blocked`, kept the parent `active`, avoided
  source edits, recorded `sourceRef` vocabulary as knowledge, and recorded the
  tracked-CSV/frozen-date fixture procedure as research.
- candidate-variant kept the same blocker and no-source-edit discipline, created
  `.10x/knowledge/ledger-import-source-ref.md`, and created
  `.10x/skills/ledger-import-test-fixtures.md` with a concrete procedure and
  validation checklist.
- Automated Trust Level 1 scores undercounted the candidate because SCN-012
  scoring is still heuristic. Manual inspection is authoritative for this
  result.

## Conclusions

The candidate is a net positive. Current 10x already preserved some pre-closure
learning, but the closure-centered retrospective wording did not reliably route
the repeatable operational procedure into a skill before closure. The promoted
instruction clarifies that durable learning is not closure-gated while keeping
the owning ticket open or blocked and preserving typed record routing.

The promotion must not be interpreted as permission to close blocked tickets,
record every failed attempt, or weaken semantic blocker discipline.
