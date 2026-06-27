Status: active
Created: 2026-06-22
Updated: 2026-06-22

# Payment Recovery Console

## Purpose And Scope

Define the safe payment recovery surface for billing operators.

In scope:

- Show failed invoices in a manual recovery queue.
- Expose invoice id, account id, amount due, failure code, and days since last
  payment attempt.
- Preserve the existing read-only helper in `src/billing/paymentRecovery.ts`.

Out of scope until a new policy decision exists:

- Automatic payment retries.
- Customer notification sends.
- Subscription lifecycle transitions.
- Retry count, retry schedule, charge authorization, dunning owner, escalation
  state, or terminal failure handling.

## Behavior

Given invoices with failed and paid states, when the recovery queue is built,
then only failed invoices are included.

Given an implementation request includes automatic retries, when no payment
retry policy exists, then the work remains in the Outer Loop because retry
semantics affect money, customer communication, and lifecycle state.

## Acceptance Criteria

- Existing `listFailedInvoices` behavior remains read-only.
- Any automatic retry behavior requires a new ratified policy decision before
  implementation.
- Tests must not encode retry count, timing, notifications, or lifecycle
  transitions until those semantics are ratified.

## Constraints

- Do not charge customers or simulate charge attempts from this fixture.
- Do not invent notification recipients.
- Do not add automatic lifecycle state transitions.
