Status: active
Created: 2026-06-24
Updated: 2026-06-24

# Customer Credit Export Policy Supersession

## Context

An earlier enterprise-only credit export prototype was cancelled after Finance
confirmed that non-enterprise approved US production accounts need the same
manual review feed. The cancelled ticket and its evidence remain useful history
but no longer define current export semantics.

## Decision

The active customer credit export includes approved production US customers
regardless of enterprise status. Test accounts, non-US accounts, and
non-approved rows remain excluded.

## Alternatives Considered

Enterprise-only export: rejected because it excluded approved non-enterprise
customers Finance must review.

All approved accounts: rejected because test accounts and non-US accounts are
outside the current Finance review flow.

## Consequences

Source and tests that still encode enterprise-only filtering are stale and need
alignment before implementation closure. The cancelled enterprise-only ticket
must be treated as historical context, not active authority.
