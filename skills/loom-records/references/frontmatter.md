# Common Frontmatter

Loom uses YAML frontmatter because it is human-editable and widely understood.

## Common Fields

Most canonical Loom records should carry these fields:

```yaml
---
id: ticket:abcd1234
kind: ticket
status: ready
created_at: 2026-04-17T00:00:00Z
updated_at: 2026-04-17T00:00:00Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  plan:
    - plan:bootstrap-core
---
```

## Required Common Fields

- `id`
- `kind`
- `status`
- `created_at`
- `updated_at`
- `scope`
- `links`

Some kinds add more:

- tickets add `depends_on`
- packets add `target`, `mode`, `style`, `write_scope`, `sources`,
  `source_fingerprint`, and `context_budget`
- wiki pages may add `page_type`
- critique records may add `review_target`

Most canonical records may also carry optional `external_refs` when outside
systems request, mirror, or package the work.

## Scope Shape

Use this general shape:

```yaml
scope:
  kind: repository
  repositories:
    - repo:root
```

Other valid `kind` values:

- `workspace`
- `multi_repository`

For workspace-scoped records, it is acceptable to omit `repositories` entirely or leave it empty.

## Timestamps

Use UTC with `Z` suffix.

Example:

```yaml
created_at: 2026-04-17T19:05:00Z
```

## Links

`links` is a typed mapping.

Good:

```yaml
links:
  initiative:
    - initiative:prove-core-loop
  plan:
    - plan:bootstrap-core
```

Acceptable empty form:

```yaml
links: {}
```

Typed links are not a substitute for prose, but they make the graph legible to search tools.

## External References

Use `external_refs` for outside systems. External systems can request, mirror,
or package Loom work. They do not own Loom truth unless the constitution says
so.

Example:

```yaml
external_refs:
  github_issue:
    - owner/repo#123
  github_pr:
    - owner/repo#456
  linear:
    - ENG-123
  jira:
    - ENG-123
```

Keep external IDs exact enough that a future agent can find the outside record.
Do not duplicate live execution state from those systems into Loom unless a
Loom owner record needs to preserve it.
