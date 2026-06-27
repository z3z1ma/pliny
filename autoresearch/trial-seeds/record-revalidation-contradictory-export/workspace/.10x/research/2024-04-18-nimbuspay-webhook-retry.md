Status: done
Created: 2024-04-18
Updated: 2024-04-18

# NimbusPay Webhook Retry Research

## Question

What webhook retry behavior did NimbusPay document for API version
`2024-02-01`?

## Sources And Methods

Read a local export of NimbusPay webhook docs on 2024-04-18 and inspected the
then-current implementation.

## Findings

- Events used `event.dedupeId` as the stable duplicate identifier.
- NimbusPay retried all non-`2xx` responses.
- NimbusPay retried for 72 hours.
- Tests passed for local behavior that retried HTTP `409`.

## Conclusions

The 2024 implementation used `event.dedupeId`, a 72 hour retry window, and
all-non-`2xx` retry handling.

These conclusions are version-sensitive. Revalidate before using them for new
implementation work.
