Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-868-ticket-assumption-ledger-scn006-live-micro

## Experiment ID

EXP-20260624-868-ticket-assumption-ledger-scn006-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: `candidate-ticket-assumption-ledger-v1` improves executable ticket
quality by making mixed provenance visible to cold-start executors.

## Motivation

Current `SKILL.md` requires execution-relevant assumptions to be record-backed,
user-ratified, or blocked, and ticket-readiness work now creates stronger
executable tickets. The remaining risk is that provenance classification remains
private to the parent agent and is not visible inside the ticket that a child
executor reads.

## Method Tier

MICRO using a live Codex subject harness and seeded billing export workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: canonical `SKILL.md` plus
  `autoresearch/candidates/2026-06-24-ticket-assumption-ledger.md`.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-006: executable ticket boundary with mixed provenance.

Seed:

- `autoresearch/fixtures/live-seeds/ticket-assumption-ledger/raw.json`

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-868-ticket-assumption-ledger-scn006-live-micro",
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
      "instruction_source": "SKILL.md plus candidate-ticket-assumption-ledger-v1",
      "base_instruction_path": "SKILL.md",
      "instruction_path": "autoresearch/candidates/2026-06-24-ticket-assumption-ledger.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-006",
      "prior_raw_path": "autoresearch/fixtures/live-seeds/ticket-assumption-ledger/raw.json",
      "prompt": "Create the executable child ticket for implementing the billing exceptions CSV export. Use the active spec and decision. I also confirm the export should include the existing ownerEmail field as an added owner_email column after account_id. Do not implement yet."
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

Current should create a bounded executable ticket and avoid implementation.
Candidate should do the same, but include a compact assumption provenance
section that separates record-backed requirements from the current
user-ratified `owner_email` column and confirms there are no unresolved
execution-critical assumptions.

## Metrics To Score

Primary: manual ticket provenance inspection and S003. Supporting: S002.

## Quality Floors

S003 active floor 80. Manual inspection is authoritative for whether the ticket
makes provenance visible.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one
subject-agent turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/068-ticket-assumption-ledger-scn006-live-micro/`;
- subject workspace `.10x/tickets/` executable ticket records;
- this research record execution log updates;
- untracked `results.tsv`;
- evidence/review records after inspection.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- implementation source files;
- dependency additions.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/068-ticket-assumption-ledger-scn006-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection required for provenance ledger quality.

## Manual Inspection Requirement

Pass an arm only if it:

- inspects the active spec, active decision, and source;
- creates exactly one executable child ticket and does not implement;
- includes scope, exclusions, acceptance criteria, evidence expectations, and
  governing references;
- correctly incorporates `owner_email` as user-ratified current-workstream
  behavior, not as pre-existing record-backed behavior;
- does not infer additional source fields as export columns.

Candidate promotion requires the ticket to include a compact assumption
provenance section that classifies record-backed, user-ratified, and blocked
items accurately. Current can pass general ticket readiness but still lose the
target behavior if provenance remains implicit.

## Promotion Criteria

Promote only if candidate materially improves over current on visible assumption
provenance without adding broad boilerplate or blocking executable ticket
creation.

## Known Risks And Confounders

- Current ticket-readiness language may already cause enough provenance
  visibility through references and acceptance criteria.
- A provenance ledger may be useful here but too noisy for trivial tickets; the
  candidate is intentionally scoped to mixed-provenance or high-impact tickets.

## Execution Log

- 2026-06-24: Registered after safety-rail and high-fanout candidates were
  discarded as already handled by current `SKILL.md`.

## Results

Runner output:

- Artifact root:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/068-ticket-assumption-ledger-scn006-live-micro/`
- Canonical guard: unchanged for `SKILL.md` and `autoresearch/program.md`.
- Automated score report:
  - current-10x: `S003=100`
  - candidate-variant: `S003=100`
  - no-10x-control: `S003=80`

Manual inspection:

- no-10x-control created an executable ticket but had inherited `.10x` removed
  by control isolation and therefore recorded that the active spec/decision
  paths needed to be attached before execution.
- current-10x inspected the active spec, active decision, and source; created
  one bounded executable ticket; incorporated the user-ratified `owner_email`
  column; avoided source edits; and recorded no blockers. Its ticket implied
  provenance through references and progress notes but did not include a
  dedicated provenance ledger.
- candidate-variant inspected the same context, created one bounded executable
  ticket, incorporated the user-ratified `owner_email` column, avoided source
  edits, recorded no blockers, and added a compact `Assumption Provenance`
  section with record-backed, source-observed, user-ratified, and blocked
  categories.

## Conclusions

Promote `candidate-ticket-assumption-ledger-v1` into `SKILL.md`.

The canonical change should stay narrow: require a compact provenance section
only for executable tickets with high-impact semantics or mixed provenance. Do
not make a ledger mandatory for trivial tickets with one obvious authority
source.
