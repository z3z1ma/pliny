# 03 - Feature With Spec, Plan, Ticket, And Ralph

## Starting `.loom` Slice

- `initiative:operator-workflows`
- no accepted spec for the requested behavior
- proposed ticket exists but is not ready for Ralph until the spec and route are
  clear

## Operator Request

"Add a packaging workflow that summarizes completed work for a PR."

## Expected Route

1. create or update a spec for intended behavior
2. create or update a plan if sequencing spans multiple tickets
3. create one bounded ticket
4. compile a Ralph packet with explicit write scope
5. execute one bounded implementation slice
6. reconcile child output back into ticket truth
7. route to critique
8. update wiki only for accepted explanation

## Expected Artifacts

- spec with `REQ-*` and `ACC-*` IDs
- plan with sequencing or execution waves if needed
- ticket with `# Coverage`
- Ralph packet with source fingerprint and context budget
- evidence for observed behavior
- critique record
- wiki page only if the accepted workflow needs durable explanation

## Expected Final State

- implementation state lives in the ticket
- acceptance IDs trace through packet and evidence
- ship workflow packages work but does not close tickets

## Common Wrong Behavior

- adding a command without a spec or ticket when behavior is unclear
- making PR text the execution ledger
- skipping packet freshness checks
- adding a new canonical layer for shipping
