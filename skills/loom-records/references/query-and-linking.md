# Query And Linking

Loom is intentionally grep-friendly.

## Common Queries

### Find all IDs

```bash
rg -n '^id:' .loom
```

### Find every reference to one record

```bash
rg -n 'ticket:abcd1234' .loom
```

### List open tickets

```bash
rg -l '^status: (proposed|ready|active|blocked|review_required|complete_pending_acceptance)$' .loom/tickets
```

### Find stale wiki pages

```bash
rg -l '^status: stale$' .loom/wiki
```

### Trace one acceptance claim

```bash
rg -n 'ACC-002' .loom
```

### Find evidence support declarations

```bash
rg -n '^# Supports Claims|^Supports:' .loom/evidence
```

### Find critique challenges

```bash
rg -n '^Challenges:' .loom/critique
```

## Linking Rules

Use typed `links:` frontmatter for real structural relationships.

Examples:

- ticket -> plan
- ticket -> spec
- critique -> ticket
- wiki -> evidence
- research -> spec

Also use prose links or ordinary Markdown links where they help reading.
But do not rely on prose alone when the relationship matters to navigation.

Use `external_refs:` for outside systems such as GitHub, Jira, Linear, Trello,
Azure DevOps, Confluence, or project boards. External refs are provenance and
mirrors; they do not replace typed Loom links.

## Reference Reconciliation

When you rename, split, or delete something:

```bash
rg -n 'ticket:abcd1234' .loom
rg -n '20260417-abcd1234-tighten-packet-scope.md' .loom
```

Update references before removing or moving the file.

## Wide Audits

For large audit passes, inline Python is acceptable if it is clearer than shell.
The important thing is that the method remains local and inspectable, not hidden in a shipped runtime.
