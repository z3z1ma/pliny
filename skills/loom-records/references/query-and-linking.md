# Query And Linking

Loom is intentionally grep-friendly.

## Common Queries

### Find all IDs

```bash
rg -n '^id:' .loom
```

### List current supported kind declarations

```bash
rg -n '^kind:' .loom skills/loom-*/templates skills/loom-*/references
```

### Discover supported ID/path shapes

```bash
rg -n '^id: (constitution:main|decision:[0-9]{4}|roadmap:|initiative:|research:|spec:|plan:|ticket:|packet:(ralph|critique|wiki)-|critique:|wiki:|evidence:|workspace:main|workspace:harness|support:[a-z0-9-]+)' .loom
rg -n '^packet_kind: (ralph|critique|wiki)$' .loom/packets skills/loom-*/templates
rg -n '\.loom/(constitution/(constitution\.md|decisions/|roadmap/)|initiatives/|research/|specs/|plans/|tickets/|critique/|wiki/|packets/(ralph|critique|wiki)/|evidence/|memory/|workspace\.md|harness\.md|support/)' .loom skills
```

These are broad discovery queries for the currently supported corpus families,
not a schema validator. Read `naming-and-ids.md` and the owning template before
repairing a specific record.

The discovery set intentionally includes canonical owner paths and support
surfaces. `workspace:main`, `workspace:harness`, packet IDs, memory paths, and
`support:<domain>-<slug>` handles help agents find workspace metadata, harness
profiles, handoffs, and packets; they do not make those surfaces canonical
project-truth owners.

### Discover workspace and optional support metadata

```bash
rg -n '^id: workspace:main|^kind: workspace$|^status:' .loom/workspace.md 2>/dev/null
rg -n '^id: workspace:harness|^kind: workspace-support$|^status:' .loom/harness.md 2>/dev/null
rg -n '^id: support:|^kind: support-artifact$|^support_kind:|^handoff_kind:|^status:' .loom/support 2>/dev/null
rg -n '^kind: support-artifact$|^support_kind:|^handoff_kind:' skills/loom-*/templates 2>/dev/null
find .loom/support/drive-handoffs -type f -name '*.md' 2>/dev/null | sort
```

Use these as optional support-surface queries. A missing `.loom/workspace.md`,
`.loom/harness.md`, `.loom/support/`, or `.loom/support/drive-handoffs/` directory
is not by itself a validation failure: support artifacts are lazy-materialized
when a workflow intentionally saves them.

### Find every reference to one record

```bash
rg -n 'ticket:<token>' .loom
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
rg -n 'spec:<slug>#ACC-002' .loom
```

### Trace one initiative objective criterion

```bash
rg -n 'initiative:<slug>#OBJ-001' .loom
```

### Find objective criteria in initiatives

```bash
rg -n '\bOBJ-[0-9]{3}\b' .loom/initiatives
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

## Semantic Relationship Queries

```bash
rg -n '^external_refs:|github_issue:|github_pr:|linear:|jira:' .loom
rg -n 'status: superseded|supersedes|superseded by' .loom
rg -n 'accepted_risk|accepted risk' .loom/tickets .loom/critique
rg -n 'follow[- ]up|related ticket|ticket:[a-z0-9]+' .loom/tickets .loom/critique
rg -n 'promoted to|promotion|promote' .loom/memory .loom/wiki .loom/research .loom/tickets
```

Use these as discovery queries, not proof by themselves. Read the owning record
before deciding what truth changed.

## Reference Reconciliation

When you rename, split, or delete something:

```bash
rg -n 'ticket:<token>' .loom
rg -n '<YYYYMMDD>-<token>-<short-slug>.md' .loom
```

Update references before removing or moving the file.

## Wide Audits

For large audit passes, inline Python is acceptable if it is clearer than shell.
The important thing is that the method remains local and inspectable, not hidden in a shipped runtime.
