Status: done
Created: 2025-12-01
Updated: 2025-12-01

# Retired Invoice Status API

## Question

Which invoice status value did the old retry API expose for invoices needing
retry review?

## Sources And Methods

Inspected the retired 2025 invoice API export and old queue worker logs.

## Findings

The retired API used `delinquent` for invoices that needed retry review.

## Conclusions

Historical work before the 2026 source migration may mention `delinquent`.
Before reusing this research, revalidate it against active records and current
source contracts.
