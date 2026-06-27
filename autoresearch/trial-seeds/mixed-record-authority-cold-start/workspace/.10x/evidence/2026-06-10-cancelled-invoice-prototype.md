Status: recorded
Created: 2026-06-10
Updated: 2026-06-10
Relates-To: .10x/tickets/done/2026-06-10-include-cancelled-invoice-retries.md

# Cancelled Invoice Prototype Evidence

## What Was Observed

The old prototype exported cancelled delinquent invoices and used
`invoice_id,account_id,amount_cents` as the header.

## Procedure

Ran the V1 prototype node test during the completed historical ticket.

## What This Supports Or Challenges

Supports that the done historical ticket implemented cancelled-invoice
visibility for the superseded V1 contract.

## Limits

This evidence relates to a done ticket and superseded specification. It does not
establish current behavior after the active invoice retry export policy.
