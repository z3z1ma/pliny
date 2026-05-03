# Repair And Drift

Repair is graph hygiene. It fixes or routes drift in Loom records without
creating a second source of truth.

## Drift Classes

1. Broken references: typed IDs that no longer resolve to an existing record.
2. Stale supersessions: records marked `superseded` without a clear successor.
3. Status mismatch: record status disagrees with the body, journal, or evidence.
4. Orphan packets: packets whose target is closed, deleted, or no longer current.
5. Owner-layer conflicts: one layer carrying truth that belongs to another.
6. Structural failures: missing frontmatter fields, malformed IDs, or filename
   and ID mismatch.
7. Dangling follow-up: critique findings or acceptance gaps with no ticket.
8. Lifecycle drift: non-ticket statuses outside the shared lifecycle grammar.
9. Coverage drift: claim IDs that no longer resolve to the intended source.
10. Stale or contradictory records: two records, support surfaces, or working
    notes disagree about the same fact.

## Repair Risk

Safe repairs:

- obvious broken-link repair after a rename
- supersession forward-link repair
- filename-vs-ID typo
- dead reference in a retired record

Route instead of editing when the repair would:

- change owner-layer truth
- reopen or close a ticket
- amend constitution
- rewrite a wiki page substantively
- invalidate a critique verdict
- change intended behavior

## Native Scan

```bash
find .loom -type f -name '*.md' | sort
rg -n '^(id|kind|status|links|target):' .loom --glob '*.md'
rg -n 'OBJ-[0-9]{3}|REQ-[0-9]{3}|ACC-[0-9]{3}|CLAIM-[0-9]{3}' .loom --glob '*.md'
```

## Routing

- owner-layer conflict -> owning skill for that layer
- status mismatch -> `loom-tickets` for tickets, owning skill for other records
- orphan packet -> inspect `packet_kind` and the path family under
  `.loom/packets/<family>/` before routing:
  - `packet_kind: ralph` or `.loom/packets/ralph/` -> `loom-ralph` packet
    lifecycle and stale packet recovery guidance; mark the packet support
    artifact `superseded` or `abandoned` only when that is the truthful packet
    lifecycle disposition
  - `packet_kind: critique` or `.loom/packets/critique/` -> `loom-critique`
    review-packet repair; do not route critique packets through Ralph merely
    because they use packet grammar
  - `packet_kind: wiki` or `.loom/packets/wiki/` -> `loom-wiki`
    synthesis-packet repair; do not route wiki packets through Ralph merely
    because they use packet grammar
  - missing, unknown, or contradictory packet family metadata ->
    `records_repair` / `loom-records` first, then route to the downstream
    workflow only after the packet family is resolved
  Orphan packet repair may repair packet support-artifact lifecycle state, but
  it does not reopen, close, or otherwise own live ticket execution truth.
- dangling critique follow-up -> `loom-tickets`
- lifecycle ambiguity -> `loom-records`
- coverage drift -> `loom-specs`, `loom-tickets`, or
  `skills/loom-tickets/references/acceptance-gate.md`
- stale or contradictory records -> identify which layer owns the disputed fact,
  update or route that owner, and simplify the non-owner

Do not resolve drift by newest timestamp, most recent file edit, or external
surface recency. Loom does not use latest-file-wins semantics. The owning layer
for the disputed truth decides the repair path.

## Done Means

- each finding has evidence
- safe repairs are small and verified
- routed repairs name the owning layer
- no semantic contradiction is hidden by deletion
