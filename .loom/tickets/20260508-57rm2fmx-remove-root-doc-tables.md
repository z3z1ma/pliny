---
id: ticket:57rm2fmx
kind: ticket
status: closed
change_class: documentation-explanation
risk_class: medium
created_at: 2026-05-08T07:41:56Z
updated_at: 2026-05-08T15:51:22Z
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
    - evidence:root-doc-table-removal-check
  critique:
    - critique:root-doc-table-removal-review
external_refs: {}
depends_on:
  - ticket:58h4o1qo
  - ticket:xulgzs52
---

# Summary

Remove Markdown tables from root public docs and briefly mention the lite/full
template distinction without turning root docs into the operational owner.

# Context

Root docs summarize Loom for users, but `loom-core` skills own template behavior
and doctrine. This ticket updates public framing only after core and playbook
surfaces settle.

# Scope

In:

- Rewrite pipe tables in `README.md`, `PROTOCOL.md`, and `ARCHITECTURE.md`.
- Add a concise public-doc note that lite templates support small work while
  generic templates remain full.
- Preserve no-runtime, split-package, and owner-layer framing.

Out:

- No detailed template-selection guide in root docs.
- No `loom-core` or `loom-playbooks` edits except loopback notes if public docs
  reveal drift.
- No examples or eval automation.

Assumptions / decision triggers:

- If root docs need more than a brief note to explain lite/full behavior, loop
  back to the spec or create a docs follow-up instead of expanding this ticket.

# Acceptance

Owner: spec-owned.

Covered IDs:

- `spec:point-of-use-ergonomics-and-mechanical-simplicity#ACC-005` for the root
  docs portion.

Ticket-local criteria:

- ACC-LOCAL-001: `rg -n '^\|.*\|$' README.md PROTOCOL.md ARCHITECTURE.md`
  returns no pipe-table rows or evidence justifies any remaining non-table
  pipe-delimited line.
- ACC-LOCAL-002: Public docs briefly mention lite templates and generic full
  templates without redefining skill-owned behavior.

# Current State

Status rationale: closed; root public-doc table conversion, brief README lite/full
framing, structural evidence, recommended critique, and ticket acceptance are
complete.

Blockers: None. Dependencies `ticket:58h4o1qo` and `ticket:xulgzs52` are closed.

Execution notes: Converted Markdown tables in `README.md` and `PROTOCOL.md` to
non-table lists. `ARCHITECTURE.md` had no matching table rows and was unchanged.
Added a brief README note about lite templates versus generic full templates.

Continuation note: After dependencies close, update root docs as summary surfaces
only and validate with targeted table scans.

# Evidence

Disposition: sufficient.

Records:

- `evidence:root-doc-table-removal-check` - supports no remaining root-doc
  pipe-table rows, no deleted rows, and the brief README lite/full note.

Gaps / limits: Evidence is structural plus source comparison; critique should
review public framing and owner-layer safety before closure.

# Review And Follow-Through

Critique policy: recommended.
Critique rationale: public docs shape first impressions and must not overstate or
relocate skill-owned behavior.
Critique disposition: completed.

Required critique profiles:

- public-framing
- owner-layer-safety

Findings:

- None - `critique:root-doc-table-removal-review` returned `pass` with no
  findings.

Promotion disposition: not_required.
Promotion / deferral rationale: this ticket changed root public docs directly and
did not create separate accepted explanation that needs wiki promotion.

Promoted / deferred:

- None - not required for this bounded public-doc slice.

Wiki disposition: not_required - no separate wiki explanation is needed.

# Acceptance Decision

Accepted by: OpenCode agent per user-delegated implementation authority.
Accepted at: 2026-05-08T15:51:22Z
Basis: `evidence:root-doc-table-removal-check` reports no remaining Markdown
pipe-table rows in root public docs, no deleted rows, diff-check pass, and a
brief README lite/full note; `critique:root-doc-table-removal-review` returned
`pass` with no findings.
Residual risks: No rendered Markdown visual review was performed; review was
source/diff based.

# Dependencies

Hard prerequisites are in frontmatter `depends_on`.

# Journal

- 2026-05-08T07:41:56Z: Created as a ready execution ticket from the active spec
  and plan.
- 2026-05-08T15:47:42Z: Moved to active after core and playbook table-removal
  dependencies closed.
- 2026-05-08T15:49:00Z: Converted root public-doc tables, added brief README
  lite/full template note, recorded `evidence:root-doc-table-removal-check`, and
  moved ticket to `review_required`.
- 2026-05-08T15:51:22Z: Recorded `critique:root-doc-table-removal-review` with
  verdict `pass` and no findings, marked promotion/wiki follow-through not
  required, accepted the ticket, and closed it.
