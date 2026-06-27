Status: recorded
Created: 2026-06-10
Updated: 2026-06-10
Relates-To: .10x/skills/ledger-import-fixture-replay/SKILL.md

# Ledger Import V1 Fixture Replay Evidence

## What Was Observed

The legacy v1 fixture replay command produced stable preview output:

```bash
python3 scripts/ledger_preview.py --fixture testdata/ledger/import-preview.csv --posting-date 2026-01-15
```

Observed output:

```json
[
  {
    "amountCents": 12345,
    "postingDate": "2026-01-15",
    "sourceRef": "LEDGER-001"
  },
  {
    "amountCents": -678,
    "postingDate": "2026-01-15",
    "sourceRef": "LEDGER-002"
  }
]
```

## Procedure

Ran the legacy v1 replay command from the repository root against
`testdata/ledger/import-preview.csv`.

## What This Supports Or Challenges

This supports the historical v1 replay procedure captured in
`.10x/skills/ledger-import-fixture-replay/SKILL.md`.

## Limits

This evidence does not verify Ledger import preview v2, does not use
`testdata/ledger/import-preview-v2.csv`, and does not establish posting date
`2026-02-20`.
