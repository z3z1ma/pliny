---
name: ledger-import-fixture-replay
description: "Use when replaying the legacy Ledger import v1 CSV fixture to verify sourceRef preservation, cent normalization, and deterministic posting dates."
metadata:
  created: 2026-06-10
  updated: 2026-06-10
---

# Ledger Import Fixture Replay

## Objective

Replay the tracked Ledger import v1 fixture and verify stable preview output
without depending on inline CSV construction or the current system date.

## Prerequisites

- The fixture file exists at `testdata/ledger/import-preview.csv`.
- The posting date is frozen to `2026-01-15`.
- Ledger import terminology follows `.10x/knowledge/ledger-import-terms.md`;
  imported row identifiers are `sourceRef`.
- Run commands from the repository root.

## Procedure

1. Confirm the fixture exists at `testdata/ledger/import-preview.csv`.
2. Run the legacy v1 replay:

   ```bash
   python3 scripts/ledger_preview.py --fixture testdata/ledger/import-preview.csv --posting-date 2026-01-15
   ```

3. Inspect the JSON output.
4. Record evidence that includes the command, output, and validation result.

## Validation

- Fixture replay uses `testdata/ledger/import-preview.csv`.
- Fixture replay does not construct CSV content inline.
- Fixture replay does not read or depend on the wall-clock date.
- Preview output contains `sourceRef` values `LEDGER-001` and `LEDGER-002`.
- Preview output contains normalized cent amounts `12345` and `-678`.
- Preview output uses posting date `2026-01-15` for every row.
