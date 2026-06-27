Status: active
Created: 2026-06-22
Updated: 2026-06-23

# Nimbus Release Token

## Context

The pilot needed a stable release-token display for operator review. Earlier
notes left the token label unresolved, which caused repeated discussions in
ticket shaping.

## Decision

Use `RUNE-42-ION` as the release token policy label for the first pilot and log
the exact ledger note `ion-green` in operator-facing test data.

## Alternatives Considered

- Generate release-token labels per account. Rejected because it makes the
  pilot harder to inspect and does not test a meaningful behavior.
- Hide the token until launch. Rejected because account operations needs to
  verify release-token display before any launch-mode decision.

## Consequences

The release-token label is no longer a blocker. Future work may change token
generation after the pilot, but the first pilot should not ask the operator to
restate this policy.
