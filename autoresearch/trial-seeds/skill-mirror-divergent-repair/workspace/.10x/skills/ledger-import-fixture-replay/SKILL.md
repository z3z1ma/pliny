---
name: ledger-import-fixture-replay
description: "Use when replaying Ledger import CSV fixtures to verify sourceRef preservation, cent normalization, and deterministic posting dates."
metadata:
  created: 2026-06-24
  updated: 2026-06-24
---

# Ledger Import Fixture Replay

## Objective

Replay the tracked Ledger import fixture set and verify stable preview output
without depending on inline CSV construction or the current system date.

## Prerequisites

- The fixture files are already tracked under `testdata/ledger/`.
- The posting date is frozen to `2026-01-15`.
- Ledger import terminology follows `.10x/knowledge/ledger-import-terms.md`;
  imported row identifiers are `sourceRef`.

## Procedure

1. Load the tracked Ledger import CSV fixture from `testdata/ledger/`.
2. Freeze the posting date to `2026-01-15`.
3. Run the Ledger import preview path against the tracked fixture.
4. Check that each preview row preserves its `sourceRef`.
5. Check that each preview row reports normalized cent amounts.
6. Check that each preview row uses the frozen posting date.

## Validation

- Fixture replay does not construct CSV content inline.
- Fixture replay does not read the wall-clock date.
- Preview output preserves `sourceRef`.
- Preview output includes normalized cent amounts.
- Preview output uses posting date `2026-01-15`.
