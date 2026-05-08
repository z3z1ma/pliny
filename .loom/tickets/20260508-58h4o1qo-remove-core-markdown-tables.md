---
id: ticket:58h4o1qo
kind: ticket
status: closed
change_class: documentation-explanation
risk_class: medium
created_at: 2026-05-08T07:41:56Z
updated_at: 2026-05-08T08:22:46Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  spec:
    - spec:point-of-use-ergonomics-and-mechanical-simplicity
  plan:
    - plan:point-of-use-ergonomics-and-mechanical-simplicity
  evidence:
    - evidence:core-table-removal-check
  critique:
    - critique:core-table-removal-review
external_refs: {}
depends_on:
  - ticket:iq03bxg5
  - ticket:nlzaqhrm
---

# Summary

Replace Markdown pipe tables in `loom-core` with label-led bullets or clearer
non-table structures after template and `using-loom` work settle.

# Context

Tables are fragile for agents and costly in tokens. This ticket handles the core
package after the higher-risk template and doctrine tickets finish, so formatting
changes do not fight overlapping edits.

# Scope

In:

- Rewrite pipe tables in `loom-core/**/*.md`.
- Preserve existing row content by default.
- Delete only plainly duplicate or stale rows, with rationale in evidence or
  ticket notes.
- Preserve stable IDs, vocabulary, and owner-layer semantics.

Out:

- No `loom-playbooks` edits.
- No root public docs edits.
- No examples or dogfood `.loom` history edits.
- No semantic doctrine changes beyond what is necessary to keep rewritten prose
  truthful.

Assumptions / decision triggers:

- If a rewrite changes protocol authority rather than presentation, update this
  ticket's critique requirements before closure.

# Acceptance

Owner: spec-owned.

Covered IDs:

- `spec:point-of-use-ergonomics-and-mechanical-simplicity#ACC-005` for the
  `loom-core` portion.

Ticket-local criteria:

- ACC-LOCAL-001: `rg -n '^\|.*\|$' loom-core` returns no pipe-table rows or
  evidence justifies any remaining non-table pipe-delimited line.
- ACC-LOCAL-002: Evidence records any deleted rows and their duplicate/stale
  rationale.

# Current State

Status rationale: closed; parallel Ralph conversion, structural evidence,
recommended critique, and ticket acceptance are complete for the `loom-core`
table-removal slice.

Blockers: None. Prior dependencies `ticket:iq03bxg5` and `ticket:nlzaqhrm` are
closed.

Execution notes: Four parallel Ralph packets converted scoped `loom-core` tables
to non-table structures. Whole-core scan now finds no Markdown pipe-table rows.

Continuation note: After dependencies close, run a targeted table scan, rewrite
core tables, and preserve content unless deletion rationale is explicit.

# Evidence

Disposition: sufficient.

Records:

- `evidence:core-table-removal-check` — supports no remaining core pipe-table rows
  and no deleted rows reported by child workers.

Gaps / limits: Evidence is structural; critique should review representative
semantic preservation because many guidance surfaces changed.

# Review And Follow-Through

Critique policy: recommended.
Critique rationale: table rewrites in core can accidentally change operator
guidance even when intended as format-only.
Critique disposition: completed.

Required critique profiles:

- operator-clarity
- owner-layer-safety when semantics changed

Findings:

- None - `critique:core-table-removal-review` returned `pass` with no findings.

Promotion disposition: not_required.
Promotion / deferral rationale: this ticket changed Markdown structure within the
owning product surface and did not create new accepted explanation beyond those
files. Root docs and playbooks have their own downstream tickets.

Promoted / deferred:

- None - not required for this bounded product-surface slice.

Wiki disposition: not_required - no separate wiki explanation is needed.

# Acceptance Decision

Accepted by: OpenCode agent per user-delegated implementation authority.
Accepted at: 2026-05-08T08:22:46Z
Basis: `evidence:core-table-removal-check` reports no remaining Markdown
pipe-table rows in `loom-core`, no deleted rows, diff-check pass, and smoke pass;
`critique:core-table-removal-review` returned `pass` with no findings.
Residual risks: Evidence and critique used structural scans plus representative
diff review, not exhaustive row-by-row semantic proof.

# Dependencies

Hard prerequisites are in frontmatter `depends_on`.

# Journal

- 2026-05-08T07:41:56Z: Created as a ready execution ticket from the active spec
  and plan.
- 2026-05-08T08:13:02Z: Moved to active after dependencies closed and compiled
  four parallel Ralph packets for core table removal.
- 2026-05-08T08:17:20Z: Four parallel Ralph workers returned `stop`; parent ran
  whole-core table scan, diff-check, smoke, and status review, recorded
  `evidence:core-table-removal-check`, and moved ticket to `review_required`.
- 2026-05-08T08:22:46Z: Recorded `critique:core-table-removal-review` with
  verdict `pass` and no findings, marked promotion/wiki follow-through not
  required, accepted the ticket, and closed it.
