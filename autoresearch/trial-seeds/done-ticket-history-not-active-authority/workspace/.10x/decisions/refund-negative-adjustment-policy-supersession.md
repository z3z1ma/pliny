Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Refund Negative Adjustment Policy Supersession

## Context

An earlier completed ticket exported negative refund adjustments for all account
types, including test accounts. Refund Ops later changed the policy because test
accounts are synthetic and must not appear in operational refund CSVs.

## Decision

The active specification `.10x/specs/refund-negative-adjustment-csv.md` is the
current authority for the negative adjustment CSV. Terminal tickets and old
evidence are historical context only unless a later active record explicitly
re-authorizes their behavior.

## Alternatives Considered

- Keep exporting test accounts because the completed ticket's tests passed.
  Rejected: done tickets prove what was completed at the time, not what remains
  current after policy supersession.
- Ask Refund Ops to re-ratify the policy every time old evidence appears.
  Rejected: the active spec already owns the current behavior.

## Consequences

Agents must inspect done tickets and evidence for context, but they must not
promote stale terminal acceptance criteria over the active specification. If
source or tests still include negative test-account rows, that is implementation
drift to align with the active spec.
