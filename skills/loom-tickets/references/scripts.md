# Ticket Script Reference

Use package-local script paths from this skill bundle.

The examples below assume invocation through `scripts/tickets.py` inside `loom-tickets`.

## `scripts/tickets.py create`

Purpose:

- create a ticket scaffold under `.loom/tickets/`
- with no slug, validate all ticket records instead of creating one

Arguments:

- `slug`: ticket slug used in the generated filename
- `--status`: optional ticket status override
- `--link=KEY=REF` or `--link=kind:ref`: repeatable typed link assignment; plain refs infer their link key from the ref prefix
- `--path`, `--repository`, `--workspace-scope`: scope controls

Example:

```bash
scripts/tickets.py create inventory-shared-script-clis --status ready --path "repos/admin-ui/src/main.ts" --link "plan:bootstrap-cli-reference-docs"
```

## `scripts/tickets.py link`

Purpose:

- add or remove typed ticket links such as verification, critique, docs, or related work

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
