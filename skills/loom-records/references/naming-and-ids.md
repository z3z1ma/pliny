# Naming And IDs

Loom uses canonical IDs for reference integrity and filenames for discovery.

Use both.

## Canonical ID Families

- `constitution:main`
- `decision:0001`
- `roadmap:bootstrap-packets`
- `initiative:prove-core-loop`
- `research:scope-audit`
- `spec:packet-discipline`
- `plan:bootstrap-core`
- `ticket:abcd1234`
- `critique:packet-discipline-review`
- `wiki:ralph`
- `evidence:packet-smoke-test`
- `packet:ralph-ticket-abcd1234-20260417T190500Z`
- `workspace:main`

## Filename Guidance

### Stable semantic records

Use a semantic slug:

- `.loom/specs/packet-discipline.md`
- `.loom/plans/bootstrap-core.md`
- `.loom/wiki/workflows/ralph-loop.md`

### Tickets

Use date + token + slug:

- `.loom/tickets/20260417-abcd1234-tighten-packet-scope.md`

The ticket's canonical ID should be only the token:

- `ticket:abcd1234`

### Packets

Use timestamp + subsystem + target:

- `.loom/packets/ralph/20260417T190500Z-ticket-abcd1234-iter-01.md`

### Decisions

Use an ordered prefix:

- `.loom/constitution/decisions/decision-0001-packet-discipline.md`

## Why Both Matter

Canonical IDs make references durable.

Filenames make discovery cheap.

One is for graph integrity.
One is for human and agent navigation.

## Slug Guidance

Prefer lowercase, words separated by hyphens, and filenames that say what the record is about.
