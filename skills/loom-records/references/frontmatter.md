# Common Frontmatter

Loom uses YAML frontmatter because it is human-editable and widely understood.

## Common Fields

Most canonical Loom records should carry these fields:

```yaml
---
id: ticket:<token>
kind: ticket
status: proposed
created_at: <UTC timestamp>
updated_at: <UTC timestamp>
scope:
  kind: repository
  repositories:
    - repo:root
links:
  plan:
    - plan:<slug>
---
```

Replace every placeholder before saving a real record.

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
- packets add packet-family fields such as `packet_kind`, `target`, `mode`,
  `style`, `child_write_scope`, `parent_merge_scope`, `source_fingerprint`,
  `execution_context`, `context_budget`, and `sources`; use
  `references/packet-frontmatter.md` for the shared packet grammar and valid
  values
- wiki pages may add `page_type`
- critique records may add `review_target`

New packet records should use `child_write_scope` for the child mutation
boundary. Older packet records may still contain `write_scope`; treat that as
legacy packet compatibility unless the packet explicitly says otherwise. A
support handoff outside `.loom/packets/`, such as a drive outer-loop handoff
proposal, may use its own `write_scope` without becoming a packet family or a
canonical truth owner.

Packet frontmatter is support-artifact grammar. It does not make packets
canonical truth owners, and it does not make critique or wiki packets
Ralph-governed.

Most canonical records may also carry optional `external_refs` when outside
systems request, mirror, package, or help navigate the work. Templates may omit
`external_refs` when outside references are uncommon for that record kind. Omitted
means no external references are declared; add `external_refs: {}` or a populated
mapping when a saved record needs an explicit outside-reference surface.

## Support Artifact Frontmatter

Support artifacts may use YAML frontmatter for routing, provenance, and parent
reconciliation, but that metadata is support-local. It does not create a new
canonical owner layer and must not own objective state, live ticket state,
acceptance, evidence sufficiency, critique verdicts, wiki truth, canonical truth,
or packet lifecycle.

`.loom/support/` is an optional, lazy-materialized support surface for saved
support artifacts. Create it only when a workflow intentionally saves such an
artifact; its presence never makes the support artifact canonical truth.

When a support template includes frontmatter, keep these fields explicit enough
for ordinary search tools:

```yaml
---
id: support:<domain>-<slug>
kind: support-artifact
support_kind: <skill-local support kind>
status: draft
created_at: <UTC timestamp>
updated_at: <UTC timestamp>
scope:
  kind: repository
  repositories:
    - repo:root
links: {}
---
```

`id` is a support-local handle for support artifacts. Do not treat a support ID
as canonical merely because the current supported-kinds table in
`naming-and-ids.md` includes support rows; canonical owner-record ID families are
listed separately from packet and support-local ID families there. The `kind:
support-artifact` field is generic support metadata; use a narrower field such
as `support_kind` or `handoff_kind` for the skill-local route.

Saved drive outer-loop handoffs use this support frontmatter under
`.loom/support/drive-handoffs/` and set:

```yaml
support_kind: drive-outer-loop-handoff
```

They are prompt-only by default and durable support artifacts only when
intentionally saved for reviewability or context recovery.

Workspace harness profiles use `id: workspace:harness` and
`kind: workspace-support`. That record documents fresh-context invocation
mechanics only; it does not own objective state, live ticket state, acceptance,
evidence sufficiency, critique verdicts, wiki truth, canonical truth, packet
contents, or packet lifecycle.

## Support-Layer Memory Exception

Memory is a support recall layer, not canonical project truth. Default memory
files may use the lightweight `<!-- L0: ... -->` header from `loom-memory`
templates instead of YAML frontmatter, and they do not need canonical `id`,
`kind`, `status`, `created_at`, `updated_at`, `scope`, or `links` fields merely
to exist. Canonical record validators should not fail memory files for missing
canonical frontmatter.

If a project chooses to wrap a memory support file in YAML, validators should
accept support-only metadata such as `kind: memory`, a local retrieval-oriented
`status`, timestamps, and links back to canonical owners. Memory files still
usually have no canonical `id`, and `kind: memory` does not make them canonical
records. Do not treat that metadata as creating a new canonical truth owner. If
the content must satisfy acceptance, define behavior, track live state, prove a
claim, or preserve accepted explanation, promote it to the owning canonical layer
instead.

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
    - initiative:<slug>
  plan:
    - plan:<slug>
```

Acceptable empty form:

```yaml
links: {}
```

Typed links are not a substitute for prose, but they make the graph legible to search tools.

## External References

Use `external_refs` for outside systems. Issue trackers, pull requests, URLs,
dashboards, generated context files, harness artifacts, and package or release
surfaces can request, mirror, package, or help navigate Loom work. They do not
own Loom truth unless the constitution says so.

Example:

```yaml
external_refs:
  github_issue:
    - <owner>/<repo>#<issue-number>
  github_pr:
    - <owner>/<repo>#<pr-number>
  linear:
    - <project-key>-<number>
  jira:
    - <project-key>-<number>
```

Keep external IDs exact enough that a future agent can find the outside record.
Do not duplicate live execution state from those systems into Loom unless a
Loom owner record needs to preserve it.

External references are support surfaces. They may prove provenance or help a
future operator find a mirrored request, issue, pull request, package, document,
generated context artifact, dashboard, harness artifact, release surface, or
board card, but they do not outrank canonical Loom records.

If an external reference disagrees with Loom, update or route the canonical owner
record first, then mirror or correct the external surface as follow-through. Do
not let external references own live state, intended behavior, evidence
sufficiency, critique verdicts, or closure.
