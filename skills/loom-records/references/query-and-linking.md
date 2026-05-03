# Query And Linking

Loom is intentionally grep-friendly.

The recipes below are examples for discovery and orientation. They are not a
mandatory runtime, generated index, schema validator, or proof by themselves.
After a query finds something relevant, read the owning record before changing
truth or claiming validation.

## Common Queries

### Find all IDs

```bash
rg -n '^id:' .loom
```

### Cold-start orientation

```bash
rg -n '^id:|^kind:|^status:|^target:|^links:|^  [a-z_]+:|^    - (constitution|decision|roadmap|initiative|research|spec|plan|ticket|packet|critique|wiki|evidence|workspace|support):' .loom/constitution .loom/initiatives .loom/research .loom/specs .loom/plans .loom/tickets .loom/packets .loom/critique .loom/evidence .loom/wiki 2>/dev/null
find .loom/initiatives .loom/research .loom/specs .loom/plans .loom/tickets .loom/packets .loom/critique .loom/evidence .loom/wiki -type f -name '*.md' 2>/dev/null | sort
```

Use this to build a first map of the active owner graph, including conditional
research/spec owners and typed link targets. It does not replace reading the
constitution, governing initiative / research / spec / plan / ticket chain,
packet, evidence, or critique records that apply to the current work.

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

### List active/open tickets

```bash
rg -n '^id: ticket:|^status: (proposed|ready|active|blocked|review_required|complete_pending_acceptance)$|^updated_at:|^links:' .loom/tickets
rg -l '^status: (proposed|ready|active|blocked|review_required|complete_pending_acceptance)$' .loom/tickets
```

These statuses are the non-terminal ticket ledger states. Read the ticket before
deciding whether the work is actually ready, blocked, waiting for review, or
pending acceptance.

### Find pending or stale compiled packets

```bash
rg -l '^status: compiled$' .loom/packets
rg -n '^id: packet:|^target:|^updated_at:|^  (git_commit|integration_ref|integration_commit|git_status_summary):|^child_write_scope:|^parent_merge_scope:' .loom/packets
```

Use this as stale-packet discovery, not disposition by query. Read each matching
packet and compare its source fingerprint, governing records, target ticket,
write scopes, and intended iteration against current owner truth before launch.
Then leave the packet `compiled`, mark it `superseded`, or mark it `abandoned`
according to `status-lifecycle.md`; do not create a generated index or separate
reconciliation ledger.

### Find stale or superseded records

```bash
rg -n '^status: (stale|superseded|abandoned)$|^supersedes:|superseded by|replaced by' .loom
rg -l '^status: stale$' .loom/wiki
```

Treat these as lifecycle-discovery queries. Read `status-lifecycle.md`, the
record itself, and inbound references before deleting, renaming, or relying on a
stale or superseded artifact.

### Trace one acceptance claim

```bash
rg -n 'spec:<slug>#ACC-002' .loom
```

### Trace one initiative objective criterion

```bash
rg -n 'initiative:<slug>#OBJ-001' .loom
```

### Trace a claim through tickets, packets, evidence, and critique

```bash
claim='spec:<slug>#ACC-002'
rg -n "$claim" .loom/specs .loom/tickets .loom/packets .loom/evidence .loom/critique .loom/wiki 2>/dev/null
rg -n '^# Supports Claims|^Supports:|^Challenges:|^Evidence:|^Critique:' .loom/tickets .loom/evidence .loom/critique 2>/dev/null
```

Use the first query when you know the exact claim ID. Use the second query to
find nearby coverage declarations. Evidence and critique can support or
challenge claims; they do not redefine the acceptance contract owned by specs or
tickets.

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
rg -n '(^# .*Challenges|^Challenges:|^- .*challenges|#FIND-[0-9]+|\b(challenges|contradicts|unsupported|insufficient)\b)' .loom/critique
```

Use this as a broad first pass, not an exhaustive proof that no critique
challenges exist.

### Find critique-owned open findings and verdict risk

```bash
rg -n '^id: critique:|^status:|^review_target:|^target:|^verdict:|^severity:|^confidence:|^State: open|\bopen\b|\bunresolved\b' .loom/critique
```

### Find ticket-owned critique dispositions

```bash
rg -n 'resolved|accepted_risk|superseded|converted_to_follow_up|requires_follow_up|blocked' .loom/tickets
```

Use these to discover possible unresolved review work. The critique record owns
findings and verdicts; the ticket owns whether each relevant finding blocks
acceptance, is resolved, is accepted risk, is superseded, or becomes follow-up.

### Find unreplaced placeholders

Saved project and support placeholder check:

```bash
rg -n '(<[^>[:cntrl:]]+>|\bTODO\b|\bTBD\b|example:[a-z0-9-]+)' .loom
```

Skill-package authoring placeholder audit:

```bash
rg -n '(<[^>[:cntrl:]]+>|\bTODO\b|\bTBD\b|example:[a-z0-9-]+)' skills \
  --glob '!**/templates/**'
```

Templates are expected to contain placeholders. Saved `.loom` records, workspace
metadata, saved support artifacts, and copied examples should not leave
placeholders that pretend to be real truth. Skill-package hits outside templates
are review signals for authoring, not automatic failures.

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
