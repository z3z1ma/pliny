Status: done
Created: 2026-06-23
Updated: 2026-06-23
Parent: .10x/tickets/done/2026-06-23-implement-autoresearch-loop.md
Depends-On: .10x/specs/10x-autoresearch-loop.md, .10x/decisions/autoresearch-initial-implementation-defaults.md

# Create Autoresearch Static Contracts

## Scope

Create the static contract artifacts that future validators, scorers, runners,
and reports consume.

Likely write scope:

- `autoresearch/README.md`
- `autoresearch/catalogs/scores.json`
- `autoresearch/catalogs/scenarios.json`
- `autoresearch/templates/experiment.md`
- `autoresearch/templates/manual-inspection.md`
- `autoresearch/schemas/score-artifact.schema.json`

Included:

- Represent scores S001 through S009 from `.10x/specs/10x-autoresearch-loop.md`.
- Represent scenarios SCN-001 through SCN-015.
- Represent required experiment-record fields from REQ-002.
- Represent scorer trust levels and required scorer metadata from REQ-009.
- Represent budget defaults and no-10x control isolation notes from
  `.10x/decisions/autoresearch-initial-implementation-defaults.md`.
- Use plain Markdown and JSON; no runtime dependencies.

Excluded:

- Validation code.
- Scoring code.
- Harness execution.
- Reports beyond README-level orientation.

Read scope:

- `.10x/tickets/done/2026-06-23-autoresearch-static-contracts.md`
- `.10x/specs/10x-autoresearch-loop.md`
- `.10x/decisions/autoresearch-initial-implementation-defaults.md`

Write scope:

- `autoresearch/README.md`
- `autoresearch/catalogs/scores.json`
- `autoresearch/catalogs/scenarios.json`
- `autoresearch/templates/experiment.md`
- `autoresearch/templates/manual-inspection.md`
- `autoresearch/schemas/score-artifact.schema.json`
- This ticket's Progress And Notes section for a concise worker completion note.

Stop conditions:

- Stop if the spec lacks enough detail to represent a score, scenario, or schema
  field without inventing behavior.
- Stop if implementation would require validation code, scoring code, harness
  execution, or reports.
- Stop if a new dependency appears necessary.
- Stop if the no-10x control policy appears inconsistent with the spec or
  decision record.

Verification posture:

- Observation-first. The worker should inspect the created static files and
  confirm they cover the ticket acceptance criteria. Automated validation belongs
  to a later ticket.

Worker output expectations:

- List files changed.
- State which acceptance criteria are satisfied.
- State any acceptance criteria not verified.
- State any assumptions, risks, or follow-up tickets needed.

## Acceptance Criteria

- AC-001: `scores.json` contains stable IDs S001-S009, names, ranges, summary
  rubrics, hard floors, and related requirement IDs.
- AC-002: `scenarios.json` contains stable IDs SCN-001-SCN-015, target scores,
  expected high-quality behavior, expected failure behavior, allowed/disallowed
  writes, and fixture/reset placeholders.
- AC-003: `experiment.md` includes every field required for registered
  experiments in the spec.
- AC-004: `manual-inspection.md` covers the required inspection checks from the
  spec.
- AC-005: `score-artifact.schema.json` can describe per-sample score output,
  cost, evidence refs, confidence, floor triggers, and limits.
- AC-006: `autoresearch/README.md` clearly states that `.10x/` remains the
  durable record graph and `autoresearch/` is implementation tooling.

## Progress And Notes

- 2026-06-23: Ticket opened from implementation scoping.
- 2026-06-23: Status set to active for bounded worker implementation of static
  contract artifacts only.
- 2026-06-23: Worker added static autoresearch README, score catalog, scenario
  catalog, experiment template, manual-inspection template, and score artifact
  schema; verified JSON syntax and static ID/field coverage only.
- 2026-06-23: Parent reconciliation independently inspected the static files,
  parsed JSON artifacts, confirmed S001-S009 and SCN-001-SCN-015 coverage,
  confirmed scenario acceptance fields, and recorded evidence at
  `.10x/evidence/2026-06-23-autoresearch-static-contracts.md`.
- 2026-06-23: Ticket marked done. Separate audit was not required for this
  low-risk static contract slice; later validator and calibration tickets will
  challenge the contracts with executable checks.

## Blockers

None.
