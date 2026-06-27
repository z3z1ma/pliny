---
name: ledger-import-fixture-replay
description: "Use when replaying Ledger import CSV fixtures to check externalId output."
metadata:
  created: 2026-06-23
  updated: 2026-06-23
---

# Ledger Import Fixture Replay

## Objective

Replay Ledger import examples using inline CSV strings and check external
ledger identifiers.

## Prerequisites

- Inline CSV content may be built inside the test.
- The current system date may be used for posting-date expectations.
- Imported row identifiers are `externalId`.

## Procedure

1. Build an inline Ledger import CSV string.
2. Run the Ledger import preview path against the inline fixture.
3. Check that each preview row exposes an `externalId`.

## Validation

- Preview output exposes `externalId`.
- Preview output includes an amount.
