Status: done
Created: 2024-02-14
Updated: 2024-02-14

# Nimbus Webhook Retry Behavior

## Question

What webhook retry and idempotency behavior did NimbusPay expose for merchant
ledger event delivery in February 2024?

## Sources And Methods

- Read NimbusPay API documentation for webhook delivery version `2024-02-01`.
- Tested `nimbuspay-python` `2.3.0` against the staging merchant sandbox on
  2024-02-14.
- Sent five synthetic `ledger.transaction.created` events and returned HTTP
  `500`, `409`, and `200` responses from the receiver.

## Findings

- NimbusPay retried non-`2xx` responses for approximately fifteen minutes.
- A receiver response with status `409` was treated as retryable.
- The event idempotency key appeared at `event.dedupeId`.
- The SDK exposed webhook signature verification through
  `nimbus.webhooks.verify(payload, signature)`.

## Conclusions

As of 2024-02-14, implementation should treat any non-`2xx` receiver response
as retryable for NimbusPay ledger webhooks and should persist `event.dedupeId`
as the idempotency key.

This research is version-sensitive. NimbusPay webhook delivery behavior, SDK
interfaces, and payload fields may change across API versions.
