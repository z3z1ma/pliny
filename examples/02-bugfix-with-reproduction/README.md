# 02 - Bugfix With Reproduction

## Starting `.loom` Slice

- `spec:ticket-acceptance`
- `plan:acceptance-hardening`
- `ticket:<token>` in `ready`
- no evidence yet for the failing behavior

## Operator Request

"Investigate why `/loom-accept` closes tickets with unresolved high-severity
critique and fix it."

## Expected Route

Use the debug workflow:

1. capture reproduction evidence
2. create or update research if root cause is not obvious
3. update spec if intended behavior is ambiguous
4. tighten the fix ticket
5. compile a Ralph packet with `verification_posture: test-first`
6. preserve red and green evidence
7. route to critique before acceptance
8. run retrospective if the failure reveals a repeated mistake

## Expected Artifacts

- evidence record for reproduction
- research record when cause was investigated
- updated spec if behavior needed clarification
- updated ticket journal and coverage
- Ralph packet with verification targets
- evidence record for the fix
- critique record if risk warrants

## Expected Final State

- ticket is `review_required` or `complete_pending_acceptance`
- high-severity critique is not silently ignored
- evidence supports the acceptance IDs

## Common Wrong Behavior

- fixing first and trying to infer reproduction afterward
- leaving root cause only in chat
- closing the ticket from the child worker
- skipping critique because the test passed
