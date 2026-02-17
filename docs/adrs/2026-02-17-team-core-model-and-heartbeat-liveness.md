# Adopt Team Core Model + Heartbeat Liveness

Date: 2026-02-17

## Status

Accepted

## Context

The Team module accumulated parallel orchestration surfaces (roster members,
custom routes, broadcast groups, investigator-era aliases) that made the
default flow harder to reason about and harder to operate reliably.

Two concrete problems drove this change:

- Targeting correctness drift: case normalization and mixed target grammars
  made valid recipients fail resolution in some paths.
- Runtime health ambiguity: start/resume idempotency often treated existing
  tmux windows as healthy without verifying interactivity/liveness.

Prompt ownership also drifted between runtime templates and pack-managed agent
files, producing role-token inconsistencies.

## Decision

Team now uses one fixed collaboration model and one config surface:

- Core roles only: manager + architect + workers + integrator.
- `loom team start --config` replaces roster composition as runtime input.
- Runtime state persists `team_config` (not roster/composition).

Team config is intentionally small:

- run defaults: `harness`, `model`
- prompt extensions: `role_prompts.append.{manager,architect,worker,integrator}`
- worker policy: `worker.subagents = encouraged`
- liveness thresholds: heartbeat/stale/dead/recovery controls

Targeting and communication are reduced to canonical core targets:

- `manager`
- `architect`
- `integrator`
- `workers`
- `worker:<id>`
- `ticket:<id>`

Recipient IDs are canonicalized and validated at command boundaries.

Liveness now uses explicit heartbeat artifacts per recipient under
`run/health/*.json` with health states `alive|stale|dead|missing`. Recovery is
bounded by run-level gates:

- `recovery_in_flight`
- `cooldown_until`
- `recoveries_in_window`

Prompt source-of-truth is `team/prompts.py`; managed pack agent blocks are
synced from canonical templates during `loom team init`.

No compatibility layer is provided for legacy composition routing or
investigator aliases.

## Consequences

- Happy path is simpler and more predictable for operators.
- Core communication is easier to test and less error-prone.
- Existing roster/persona-route workflows are intentionally breaking changes.
- Liveness diagnostics and recovery are more explicit (`status`/`doctor`).
- Prompt behavior is consistent between runtime rendering and packaged agents.
