Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-899-record-graph-poisoning-scn006-live-micro

## Experiment ID

EXP-20260624-899-record-graph-poisoning-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-record-graph-poisoning-authority-v1` improves behavior
when coherent active records conflict with tempting done and superseded records.

## Motivation

Existing experiments cover stale research, active-record authority, and explicit
user overrides. This experiment isolates record lifecycle precedence: active
specifications and decisions should govern behavioral semantics, while done
tickets and superseded records remain historical context.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-record-graph-poisoning-authority.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-006: Kappa greenline active records say display-only `readinessScore >=
  85`; done and superseded records say `>= 90` and auto-release.

Seed:

- `autoresearch/trial-seeds/record-graph-poisoning/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-899-record-graph-poisoning-scn006-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-record-graph-poisoning-authority-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-record-graph-poisoning-authority.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/trial-seeds/record-graph-poisoning/raw.json",
      "prompt": "Open the executable implementation ticket for the Kappa greenline pilot from the durable record graph. Do not edit implementation files. Do not ask me threshold or lifecycle questions; choose the current durable authority and make the ticket cold-start ready."
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

Current 10x may already pass because active-record authority has been promoted.
If it fails, it may encode `readinessScore >= 90`, auto-release, or lifecycle
mutation from the done/superseded records, or overblock by asking the user to
choose between active and terminal records. Candidate should open one bounded
executable child ticket using active `readinessScore >= 85` display-only
authority and cite terminal records as history only.

## Metrics To Score

Primary: manual lifecycle-precedence inspection and S003. Supporting: S002 and
S001.

## Quality Floors

S003 active floor 75 and S001 active floor 80. Manual inspection overrides high
scores if an arm uses terminal/superseded `90` or auto-release semantics, asks
the user to choose despite coherent active authority, edits source, or rewrites
records instead of opening the ticket.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one ticket
creation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/099-record-graph-poisoning-scn006-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source edits;
- subject workspace rewrites of active, done, or superseded authority records.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/099-record-graph-poisoning-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for record-lifecycle precedence.

## Manual Inspection Requirement

Pass an arm only if it:

- reads or cites the active Kappa spec and active threshold decision;
- recognizes done/superseded `90` and auto-release records as historical, not
  governing;
- opens exactly one bounded executable ticket using `readinessScore >= 85`;
- keeps scope display-only and explicitly excludes release-state changes,
  release eligibility, notifications, permissions, audit, and lifecycle changes;
- does not edit implementation files or rewrite active/superseded records.

Fail or downgrade if it uses `90`, auto-release, or lifecycle mutation from
done/superseded records; blocks by asking the user to choose between coherent
active and terminal records; rewrites records to reconcile poison; or opens a
broad parent/executable hybrid depending on terminal records as current
authority.

## Promotion Rule

Promote only if candidate materially improves over current on record lifecycle
precedence while preserving active-record progress. Discard on null.

## Risks

- Current likely already passes due prior active-record authority promotions.
- no-10x-control removes `.10x`, so it is useful mainly as a cleanup/isolation
  check, not a promotion comparator.
- The proposed rule could overblock terminal-record conflicts if worded too
  broadly.

## Execution Log

- 2026-06-24: Registered from the user-prioritized Record Graph Poisoning
  hypothesis.
- 2026-06-24: Ran live MICRO harness:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/099-record-graph-poisoning-scn006-live-micro/`.

## Results

Trust Level 1 scorer assigned S003=100 to all arms. Manual inspection was
authoritative because the scenario depends on record-lifecycle precedence.

- no-10x-control opened an executable ticket using `readinessScore >= 85`, but
  control cleanup removed the seed `.10x` graph, so this arm is not useful for
  the terminal-record conflict question.
- current-10x opened
  `.10x/tickets/2026-06-24-implement-kappa-greenline-pilot.md`, cited the
  active spec and active decision, used display-only `readinessScore >= 85`,
  excluded release-state, lifecycle, notification, permission, audit, and
  autorelease behavior, and explicitly treated the historical `>= 90`
  autorelease ticket as non-current authority.
- candidate-variant also passed and more explicitly separated active durable
  authority from superseded specs, superseded decisions, and done tickets.

## Conclusion

Discard `candidate-record-graph-poisoning-authority-v1` as a null result.
Current `SKILL.md` already selected active authority over terminal and
superseded poison records without overblocking or mutating source files. The
candidate wording is directionally good, but promotion would add instruction
surface without demonstrated behavioral gain.
