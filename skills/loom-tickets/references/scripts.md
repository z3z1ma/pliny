# Ticket Script Reference

Use package-local script paths from this skill bundle.

The examples below assume invocation through `scripts/tickets.py` inside `loom-tickets`.

## Direct Ticket Query Ideas

The bundled CLI scaffolds, links, and verifies ticket artifacts. It does not provide a separate "list open tickets" command.

When you need to inspect ticket state directly, query the frontmatter in `.loom/tickets/`.

The CLI does provide first-class dependency management through `depends_on`.

The queries below are examples, not a canonical command surface. They are meant as portable operator patterns you can adapt to the current ticket corpus and the question you are trying to answer.

`open` is not a first-class stored status. Treat every non-terminal status as open:

- `proposed`
- `ready`
- `active`
- `blocked`
- `review_required`
- `complete_pending_acceptance`

Terminal statuses are:

- `closed`
- `cancelled`

These examples intentionally use native shell tooling directly against `.loom/tickets/`.

### Example Status Queries

Open tickets:

```bash
rg -l '"status":\s*"(proposed|ready|active|blocked|review_required|complete_pending_acceptance)"' .loom/tickets
```

Not-yet-started tickets:

```bash
rg -l '"status":\s*"(proposed|ready)"' .loom/tickets
```

Needs-attention queue:

```bash
rg -l '"status":\s*"(blocked|review_required|complete_pending_acceptance)"' .loom/tickets
```

### Example Status Rollups

Count tickets by status:

```bash
rg --no-filename -o '"status":\s*"[^"]+"' .loom/tickets | sort | uniq -c
```

Show newest ticket updates first:

```bash
rg -H -o '"updated_at":\s*"[^"]+"' .loom/tickets | sort -t'"' -k4,4r
```

### Example Dependency Queries

Tickets with first-class upstream dependencies:

```bash
rg --multiline -P -l '"depends_on":\s*\[\s*"ticket:\d+' .loom/tickets
```

Tickets that depend on one specific upstream ticket:

```bash
rg --multiline -P -l '"depends_on":\s*\[(?:(?!\]).)*"ticket:0003"' .loom/tickets
```

Use `--multiline -P` for dependency queries because `depends_on` is formatted as a multi-line JSON array in frontmatter.

### Example Evidence And Structure Checks

Tickets with no linked verification refs yet:

```bash
rg --files-without-match 'verification:' .loom/tickets
```

Tickets missing the `Verification` section:

```bash
rg --files-without-match '^# Verification$' .loom/tickets
```

Tickets missing the `Documentation Disposition` section:

```bash
rg --files-without-match '^# Documentation Disposition$' .loom/tickets
```

## `scripts/tickets.py create`

Purpose:

- create a ticket scaffold under `.loom/tickets/`
- with no slug, validate all ticket records instead of creating one

Arguments:

- `slug`: ticket slug used in the generated filename
- `--status`: optional ticket status override
- `--depends-on`: repeatable upstream ticket dependency; accepts a ticket ref or an existing ticket path and stores the canonical `ticket:NNNN` ref in `depends_on`
- `--link=KEY=REF` or `--link=kind:ref`: repeatable typed link assignment; plain refs infer their link key from the ref prefix
- `--path`, `--repository`, `--workspace-scope`: scope controls

Example:

```bash
scripts/tickets.py create inventory-shared-script-clis --status ready --path "repos/admin-ui/src/main.ts" --link "plan:bootstrap-cli-reference-docs"
```

## `scripts/tickets.py depends-on`

Purpose:

- add or remove first-class upstream ticket dependencies in `depends_on`

Arguments:

- `target`: ticket ref or path to mutate
- `--add`: repeatable upstream dependency to append
- `--remove`: repeatable upstream dependency to remove

Behavior:

- dependencies are stored as canonical `ticket:NNNN` refs in frontmatter `depends_on`
- the CLI resolves refs or ticket paths to existing tickets before writing
- a ticket cannot depend on itself

Example:

```bash
scripts/tickets.py depends-on "ticket:0005" --add "ticket:0003"
```

## `scripts/tickets.py link`

Purpose:

- add or remove typed ticket links such as verification, critique, docs, or related work

Use `depends-on` for hard upstream ticket prerequisites. Use `link` for non-dependency relationships.

Arguments:

- `target`: ticket ref to mutate
- `--add=KEY=REF` or `--add=kind:ref`: repeatable link addition
- `--remove=KEY=REF` or `--remove=kind:ref`: repeatable link removal

Example:

```bash
scripts/tickets.py link "ticket:0002" --add "verification:admin-query-contract-sync-validation"
```

## `scripts/tickets.py verify`

Purpose:

- create a verification record and link it to ticket work

Arguments:

- `slug`: verification slug
- `--link`: verification frontmatter links
- `--path`, `--repository`, `--workspace-scope`: scope inputs

Example:

```bash
scripts/tickets.py verify admin-query-contract-sync-validation --link "ticket:0002"
```
