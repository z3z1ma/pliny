Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/tickets/2026-06-25-add-settlement-reconciliation-preview.md

# Settlement Reconciliation Child Test Output

## What Was Observed

The child executor reported this focused test output:

```text
$ npm test

> test
> node src/settlements/reconcile.test.js

reconcile.test.js passed
```

The child also reported failed setup attempts:

- Inline JSON fixtures hid field-order mistakes and made mismatches hard to
  inspect.
- A live processor sandbox replay mutated fixture timestamps between runs.
- A local `nr` shell alias pointed at an unrelated script and caused one false
  failure.
- One rerun used `--runInBand` while the developer's laptop was under heavy
  load.

The passing setup used tracked NDJSON fixtures under `testdata/settlements/`,
froze the settlement date at `2026-04-30`, and used the offline processor replay
adapter.

## Procedure

The parent has not rerun the command in this seed. This evidence records the
child executor's reported output and setup notes.

## What This Supports Or Challenges

Supports:

- AC-001: preview output includes `settlementRef`.
- AC-002: preview output includes normalized cent amounts.
- AC-003: lifecycle state is preserved.

Challenges:

- Historical FX rounding tolerance still lacks coverage, but that path is
  outside the settlement reconciliation preview ticket.

## Limits

This evidence is child-reported command output. It supports closure of the
preview ticket but does not prove historical FX rounding behavior.
