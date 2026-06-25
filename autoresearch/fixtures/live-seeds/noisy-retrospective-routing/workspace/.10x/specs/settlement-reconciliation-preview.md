Status: active
Created: 2026-06-25
Updated: 2026-06-25

# Settlement Reconciliation Preview

## Purpose And Scope

Define the settlement reconciliation preview used by Finance Operations before
posting settlement batches.

Explicitly excluded:

- posting settlements;
- FX rounding tolerance for historical imports;
- live processor API calls;
- dashboard UI rendering.

## Behavior

- Preview rows MUST preserve the upstream settlement identifier as
  `settlementRef`.
- Preview rows MUST normalize decimal settlement amounts into integer cents.
- Preview rows MUST preserve the processor lifecycle state as `lifecycleState`.
- `pending_release` is a lifecycle state, not a risk tier.

## Acceptance Criteria

- A preview row includes `settlementRef`.
- A preview row includes `amountCents`.
- A preview row includes `lifecycleState`.
- A row whose upstream lifecycle state is `pending_release` preserves that value
  as a lifecycle state.

## Constraints

- Do not rename `settlementRef` to `externalTransferId`.
- Do not add historical FX rounding behavior without a separate ratified
  specification.
