Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/specs/stock-adjustment-queue.md, .10x/decisions/inventory-integrity-hold.md

# Stock Adjustment Queue Urgent Path

## What Was Observed

`src/inventory/adjustmentQueue.js` exposes `createStockAdjustmentRequest` and
supports an `expedite` boolean on queue entries.

## Procedure

Inspected `src/inventory/adjustmentQueue.js` in this seed workspace.

## What This Supports Or Challenges

This supports using the existing expedited adjustment queue as the safe path for
urgent same-day stock corrections.

## Limits

This evidence does not prove external warehouse staffing, cycle-count
completion, fulfillment allocation, or downstream approval timing.
