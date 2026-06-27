Status: active
Created: 2026-06-23
Updated: 2026-06-23

# Ledger Import Preview

## Purpose And Scope

Define the Ledger import preview behavior covered by the completed child ticket.

## Behavior

Ledger import preview tests replay tracked CSV fixtures, freeze expected posting
dates, and expose source-row identity as `sourceRef`.

## Acceptance Criteria

- Preview import tests replay tracked CSV fixtures.
- Expected posting date is frozen.
- Preview output uses `sourceRef`.

## Constraints

Archive import malformed-currency behavior is outside this preview scope.
