---
id: ticket:xulgzs52
kind: ticket
status: closed
change_class: documentation-explanation
risk_class: medium
created_at: 2026-05-08T07:41:56Z
updated_at: 2026-05-08T15:45:58Z
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
    - evidence:playbook-table-removal-check
  critique:
    - critique:playbook-table-removal-review
external_refs: {}
depends_on:
  - ticket:58h4o1qo
---

# Summary

Replace Markdown pipe tables in `loom-playbooks` with label-led bullets or clearer
non-table structures after the core package table pass settles.

# Context

Playbooks must remain optional routes that depend on core and route durable truth
back to owner layers. Table rewrites should improve editability without
reintroducing vocabulary drift.

# Scope

In:

- Rewrite pipe tables in `loom-playbooks/**/*.md`.
- Preserve existing row content by default.
- Delete only plainly duplicate or stale rows, with rationale in evidence or
  ticket notes.
- Keep playbook vocabulary aligned with core owner-layer and critique grammar.

Out:

- No `loom-core` edits except blocking loopback notes if drift is discovered.
- No root public docs edits.
- No examples or dogfood `.loom` history edits.

Assumptions / decision triggers:

- If a playbook table exposes core/playbook vocabulary drift, fix it only when it
  is inside this ticket's playbook write scope; otherwise create or route a
  follow-up.

# Acceptance

Owner: spec-owned.

Covered IDs:

- `spec:point-of-use-ergonomics-and-mechanical-simplicity#ACC-005` for the
  `loom-playbooks` portion.

Ticket-local criteria:

- ACC-LOCAL-001: `rg -n '^\|.*\|$' loom-playbooks` returns no pipe-table rows or
  evidence justifies any remaining non-table pipe-delimited line.
- ACC-LOCAL-002: Evidence records any deleted rows and their duplicate/stale
  rationale.

# Current State

Status rationale: closed; parallel Ralph conversion, structural evidence,
recommended critique, low finding resolution, and ticket acceptance are complete
for the `loom-playbooks` table-removal slice.

Blockers: None. Dependency `ticket:58h4o1qo` is closed.

Execution notes: Four parallel Ralph packets converted scoped `loom-playbooks`
tables to non-table structures. Whole-playbook scan now finds no Markdown
pipe-table rows, and stale table terminology found by critique was resolved.

Continuation note: After the core pass closes, run the playbook table scan and
rewrite tables while preserving core-aligned vocabulary.

# Evidence

Disposition: sufficient.

Records:

- `evidence:playbook-table-removal-check` - supports no remaining playbook
  pipe-table rows, no reported deleted rows, diff-check pass, and smoke pass.

Gaps / limits: Evidence is structural; critique should review representative
semantic preservation because many playbook guidance surfaces changed.

# Review And Follow-Through

Critique policy: recommended.
Critique rationale: playbook examples can drift from core grammar during format
rewrites.
Critique disposition: completed.

Required critique profiles:

- operator-clarity
- core-alignment

Findings:

- `CRIT-XULGZS52-001` from `critique:playbook-table-removal-review` - resolved by
  changing stale table terminology in the cited Git and drive references to
  checklist or decision-list language.

Promotion disposition: not_required.
Promotion / deferral rationale: this ticket changed Markdown structure within the
owning playbook product surface and did not create new accepted explanation beyond
those files. Root docs have their own downstream ticket.

Promoted / deferred:

- None - not required for this bounded product-surface slice.

Wiki disposition: not_required - no separate wiki explanation is needed.

# Acceptance Decision

Accepted by: OpenCode agent per user-delegated implementation authority.
Accepted at: 2026-05-08T15:45:58Z
Basis: `evidence:playbook-table-removal-check` reports no remaining Markdown
pipe-table rows in `loom-playbooks`, no deleted rows, diff-check pass, and smoke
pass; `critique:playbook-table-removal-review` returned `pass_with_findings` with
the only finding resolved before closure.
Residual risks: Evidence and critique used structural scans plus representative
diff review, not exhaustive row-by-row semantic proof.

# Dependencies

Hard prerequisites are in frontmatter `depends_on`.

# Journal

- 2026-05-08T07:41:56Z: Created as a ready execution ticket from the active spec
  and plan.
- 2026-05-08T15:36:13Z: Moved to active after `ticket:58h4o1qo` closed and
  compiled four parallel Ralph packets for playbook table removal.
- 2026-05-08T15:40:41Z: Four parallel Ralph workers returned `stop`; parent ran
  whole-playbook table scan, diff-check, smoke, diff-stat, and status review,
  recorded `evidence:playbook-table-removal-check`, and moved ticket to
  `review_required`.
- 2026-05-08T15:45:58Z: Recorded `critique:playbook-table-removal-review` with
  verdict `pass_with_findings`, resolved low finding `CRIT-XULGZS52-001` by
  removing stale table terminology, reran checks, marked promotion/wiki
  follow-through not required, accepted the ticket, and closed it.
