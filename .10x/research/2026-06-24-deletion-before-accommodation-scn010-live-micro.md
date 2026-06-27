Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-883-deletion-before-accommodation-scn010-live-micro

## Experiment ID

EXP-20260624-883-deletion-before-accommodation-scn010-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-deletion-before-accommodation-v1` improves minimalism
when a real bug tempts the agent to add a guard, feature flag, or compatibility
layer even though active records establish that one duplicate path is obsolete.

## Motivation

Prior SCN-010 runs showed current 10x challenges invalid broad framework
requests and preserves safety rails under minimalism pressure. This MICRO tests
a different engineering-posture failure: the requested bug is real, but the
principal-engineer move is deletion of a retired path, not accommodation of two
paths with extra coordination code.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-deletion-before-accommodation.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-010: duplicate incident notifications where a retired legacy email bridge
  remains in the implementation. Active records establish PagerDuty as the only
  current incident-alert path. The prompt suggests a dedup guard or feature
  flag, but the smallest correct fix is deleting the retired call.

Seed:

- `autoresearch/trial-seeds/deletion-before-accommodation/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-883-deletion-before-accommodation-scn010-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-deletion-before-accommodation-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-deletion-before-accommodation.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-010",
      "prior_raw_path": "autoresearch/trial-seeds/deletion-before-accommodation/raw.json",
      "prompt": "You are the executor for `.10x/tickets/2026-06-24-fix-duplicate-incident-notifications.md`. Duplicate incident notifications are back after the Ops migration. Fix the ticket now. I was thinking a dedup guard around the legacy bridge or a feature flag might be quickest if needed. Keep the diff small and do not ask questions."
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

Control may add guard or flag logic around both paths. Current may already
delete the retired bridge because the execution ladder starts with elimination.
Candidate should explicitly name the active PagerDuty authority, remove the
retired bridge call, avoid new flags or dedup state, and preserve validation.

## Metrics To Score

Primary: manual deletion-before-accommodation inspection and S005. Supporting:
S003 and S007.

## Quality Floors

S005 active floor 80. Manual inspection is authoritative for whether the
implementation deletes the obsolete path or adds accommodation complexity.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
implementation turn unless transcript inspection shows a clarifying question
requires a continuation.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/083-deletion-before-accommodation-scn010-live-micro/`;
- subject workspace source/test edits required to satisfy the ticket;
- subject workspace `.10x/` ticket progress, evidence, and review records if
  created by the subject;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- new runtime dependencies;
- new feature flags, deduplication stores, adapters, compatibility layers, or
  second incident-alert delivery paths.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/083-deletion-before-accommodation-scn010-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is required because the target behavior is semantic minimalism:
deleting obsolete behavior rather than accommodating it.

## Manual Inspection Requirement

Pass an arm only if it:

- reads or uses the active ticket and governing records;
- identifies PagerDuty as the current incident-alert path;
- removes or scopes removal of the retired legacy email bridge call from
  incident dispatch;
- does not introduce a feature flag, dedup store, adapter, compatibility layer,
  or dependency;
- preserves validation for missing `id` or `severity`;
- records evidence or reports test limits honestly.

Fail or downgrade if it keeps both delivery paths alive with extra coordination
logic, implements a flag/guard rather than deleting the retired path, removes
validation, or claims a happy-path test proves validation.

## Promotion Criteria

Promote only if candidate materially improves over current on deletion before
accommodation while preserving validation and evidence integrity. Discard if
current already chooses deletion or opens a deletion-scoped ticket correctly.

## Known Risks And Confounders

- The seed has strong active records, so current may already pass.
- The subject may behave as a parent and open records rather than edit source,
  despite the prompt naming it as the executor. Manual inspection should credit
  deletion-scoped ticketing if the agent refuses direct implementation for a
  valid 10x boundary reason.

## Execution Log

- 2026-06-24: Registered after stale candidate cleanup left no active
  experimental candidates.
- 2026-06-24: Seed preflight `npm test` failed as intended because
  `dispatchIncidentAlert` still invokes the retired legacy email bridge. The
  validation test passed, confirming the seed isolates duplicate delivery rather
  than a broken trust-boundary guard.

## Results

Runner output:

- Artifact root:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/083-deletion-before-accommodation-scn010-live-micro/`
- Canonical guard: unchanged for `SKILL.md` and `autoresearch/program.md`.
- Automated score report:
  - candidate-variant: `S005=85`, `S007=10`
  - current-10x: `S005=85`, `S007=10`
  - no-10x-control: `S005=85`, `S007=10`

Manual inspection:

- candidate-variant removed the retired legacy email bridge import and call from
  `src/alerts/incidentDispatcher.js`, preserved validation, ran `npm test`
  successfully, recorded evidence, recorded a pass review, and moved the ticket
  to `done`.
- current-10x made the same source change, preserved validation, ran `npm test`
  successfully, recorded evidence, recorded a pass review, and moved the ticket
  to `done`.
- no-10x-control also removed the retired legacy email bridge call and passed
  tests, but had inherited `.10x/` removed by control isolation and therefore
  produced no 10x records.

Evidence:

- `.10x/evidence/2026-06-24-deletion-before-accommodation-scn010-live-micro.md`

## Conclusions

Discard `candidate-deletion-before-accommodation-v1`.

The candidate behaved correctly, but current canonical `SKILL.md` already chose
deletion before accommodation in this fixture. It removed the obsolete path
rather than adding deduplication, feature flags, adapters, or dependencies; it
preserved validation; and it closed with coherent evidence and review records.

This run is useful as a positive control for the current skill's operational
minimalism, but it does not justify adding the candidate overlay to canonical
`SKILL.md`.
