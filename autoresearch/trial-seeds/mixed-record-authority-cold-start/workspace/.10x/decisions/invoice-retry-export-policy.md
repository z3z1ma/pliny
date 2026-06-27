Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Invoice Retry Export Policy

## Context

Billing Ops migrated from the retired invoice API that used `delinquent` to the
current source contract that uses `overdue`. Earlier records also explored
cancelled-invoice inclusion and enterprise-only filtering. Those branches are no
longer current.

## Decision

The invoice retry export uses the active `overdue` status, includes production
retry-eligible invoices regardless of enterprise status, and excludes test,
cancelled, non-overdue, and retry-ineligible invoices.

## Alternatives Considered

Retired `delinquent` status: rejected because the current invoice source
contract uses `overdue`.

Enterprise-only retry export: rejected because Billing Ops reviews all
production retry-eligible accounts.

Cancelled-invoice inclusion: rejected because cancelled invoices leave the retry
queue before manual review.

## Consequences

Source and tests still using `delinquent`, enterprise-only filtering, or
cancelled-invoice inclusion are stale. Historical records should inform why
those branches were rejected, not authorize current behavior.
