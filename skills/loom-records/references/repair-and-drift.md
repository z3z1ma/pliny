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
rg -n 'REQ-[0-9]{3}|ACC-[0-9]{3}|CLAIM-[0-9]{3}' .loom --glob '*.md'
```

## Routing

- owner-layer conflict -> owning skill for that layer
- status mismatch -> `loom-tickets` for tickets, owning skill for other records
- orphan packet -> `loom-ralph` or mark the packet `superseded` / `abandoned`
- dangling critique follow-up -> `loom-tickets`
- lifecycle ambiguity -> `loom-records`
- coverage drift -> `loom-specs`, `loom-tickets`, or
  `skills/loom-tickets/references/acceptance-gate.md`

## Done Means

- each finding has evidence
- safe repairs are small and verified
- routed repairs name the owning layer
- no semantic contradiction is hidden by deletion
