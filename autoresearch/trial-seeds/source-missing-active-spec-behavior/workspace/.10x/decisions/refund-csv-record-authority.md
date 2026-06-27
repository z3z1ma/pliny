Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Refund CSV Record Authority

## Context

Refund Ops approved the local `.10x` refund CSV specification as the source of
truth for negative adjustment CSV export behavior. The implementation and tests
may lag the approved records.

## Decision

The active `.10x/specs/refund-negative-adjustment-csv.md` specification is the
canonical implementation contract for the next refund negative adjustment CSV
work.

## Alternatives Considered

- Treat current source/tests as canonical: rejected because Refund Ops
  explicitly approved the active specification after the source/tests were
  written.
- Ask the user to re-ratify every CSV column and exclusion: rejected because the
  active specification already owns those details.

## Consequences

If source or tests disagree with the active specification, the next executable
ticket should identify that drift and align source/tests to the active spec
without reopening settled product semantics.
