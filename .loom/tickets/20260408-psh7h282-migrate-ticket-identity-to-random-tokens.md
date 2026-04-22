---
id: ticket:psh7h282
kind: ticket
status: closed
change_class: protocol-authority
created_at: 2026-04-08T15:25:50Z
updated_at: 2026-04-22T17:20:00Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  plan:
    - plan:simplify-ticket-identity-to-random-tokens
external_refs: {}
depends_on: []
---

# Summary

Replace Loom's autoincremented ticket numbering with short random ticket tokens,
update the shipped ticket CLI to use that identity model, and reconcile the
existing corpus so ticket refs and filenames all tell one consistent story.

# Context

The user explicitly wants ticket names and ids to stop using an autoincrementing
heuristic and instead use random short strings.

Investigation for `plan:simplify-ticket-identity-to-random-tokens` found that the
main behavioral coupling to numeric ids lives in
`skills/loom-tickets/scripts/tickets.py`, while the larger migration cost is the
written corpus and canonical `.loom/` graph that still teaches or stores numeric
ticket refs.

The current repository also had naming drift already: the docs and existing
ticket files still described repository-prefixed numeric filenames, while the
shipped helper had already drifted to a different numeric filename shape. This
change simplifies that drift away rather than layering another identity rule on
top of it.

# Why This Work Matters Now

Ticket identity is a foundational cross-surface convention. It is cheaper to fix
while the corpus is still small and before more packet, verification, critique,
and docs artifacts accumulate around the numeric ticket scheme.

This work also directly affects the ergonomics of creating and referencing new
tickets. If Loom is going to switch to random short ticket tokens, it is better
to do it now and reconcile the docs/examples truthfully instead of continuing to
grow around the numbered format.

# Scope

- choose the random ticket token contract inside the requested 6-8 character
  range
- update `skills/loom-tickets/scripts/tickets.py` so ticket creation and ticket
  lookup use opaque random-token refs rather than numeric ids
- settle one filename pattern that reuses the same token instead of depending on
  numbering or repository-prefix heuristics
- migrate the current ticket records and direct references to them across the
  canonical `.loom/` graph and affected product docs
- run the structural and behavioral checks needed to show the new model works

# Non-goals

- redesign record ids for non-ticket artifact kinds such as plans, specs,
  initiatives, decisions, or docs
- introduce a broad migration framework or new helper CLI unless the current
  corpus proves too painful to reconcile directly
- widen the work into unrelated packet or workflow redesign beyond the ticket-ref
  fallout this change causes

# Acceptance Criteria

- creating a new ticket produces a `ticket:<random-token>` ref using a random
  6-8 character token instead of an autoincremented number
- the generated ticket filename uses the UTC creation date plus the same random
  token and no longer depends on the current numeric or repository-prefix
  heuristics
- `scripts/tickets.py link`, `scripts/tickets.py depends-on`, and ticket-target
  resolution continue to work against the new opaque ticket refs
- the existing canonical ticket records and the direct references to them in the
  touched `.loom/` records are migrated to the new ticket identity scheme
- the touched product docs and examples stop teaching numbered ticket refs as the
  current Loom behavior
- `uvx ruff check skills/*/scripts/*.py` passes after the script change

# Implementation Plan

1. Confirm the exact token shape to implement first, keeping it within the
   requested 6-8 character range and preferring the simplest fixed-width option
   unless a strong reason appears otherwise.
2. Rewrite `skills/loom-tickets/scripts/tickets.py` so create, resolve,
   dependency normalization, and id validation all treat ticket refs as
   `ticket:<token>` rather than numbered ticket refs.
3. Update the ticket-layer docs and the shared rules/examples that still teach
   numbered ticket refs or numbered ticket filenames.
4. Rename existing ticket files and update their frontmatter ids.
5. Reconcile all direct references to those tickets across `.loom/` and the
   touched product docs.
6. Run the lint and behavioral smoke checks, then update this ticket with the
   resulting evidence and any remaining migration gaps.

# Dependencies

- Governing plan: `plan:simplify-ticket-identity-to-random-tokens`
- No hard upstream ticket blocker is known yet.
- This ticket should stay aligned with the plan's migration posture: one-pass
  reconciliation rather than a long-lived dual identity model.

# Risks / Edge Cases

- token collisions need deterministic retry behavior in ticket creation
- partial migration could leave mixed numeric and random ticket identities in the
  same graph, which would be confusing for future agents
- some references may exist in example packets, README snippets, or older
  canonical records that are easy to overlook during migration
- future run, critique, docs, or verification artifacts may eventually need the
  same style of migration once more ticket-linked history exists

# Verification

- `uvx ruff check skills/*/scripts/*.py`
- `uvx ruff format --check skills/*/scripts/*.py`
- disposable smoke workspace at `/tmp/loom-ticket-smoke.YZU5me/` produced
  `ticket:s43p0gux` in `.loom/tickets/20260408-s43p0gux-first-smoke.md`
- the same smoke workspace produced `ticket:ozy0n8yo` in
  `.loom/tickets/20260408-ozy0n8yo-second-smoke.md`, then proved `link` and
  `depends-on` mutation against opaque ticket refs while keeping the new
  date-prefixed filename shape
- repo-wide grep after migration found no remaining numbered ticket refs or old
  numbered ticket filenames outside this migration's own historical notes

# Documentation Disposition

Documentation updates were required and landed as part of the same slice.

This ticket updated the affected skill references, rules, README snippets, and
canonical `.loom/` records so the shipped bundle now teaches the random-token
ticket identity model directly.

The filename contract was then tightened further so ticket files use a UTC date
prefix as `YYYYMMDD-<token>-<slug>.md`.

# Journal

- 2026-04-08: created `ticket:psh7h282` in `ready` state and linked it to
  `plan:simplify-ticket-identity-to-random-tokens` after investigating the
  existing numeric ticket-id surface.
- 2026-04-08: implemented the fixed-width 8-character lowercase alphanumeric
  ticket token contract in `skills/loom-tickets/scripts/tickets.py` and removed
  autoincremented ticket-id generation and numeric ticket validation.
- 2026-04-08: migrated the six canonical ticket ids and filenames, reconciled the
  linked `.loom/` graph, and updated shipped docs so the bundle no longer teaches
  numbered ticket refs as current behavior.
- 2026-04-08: revised the filename contract again to remove the `ticket-` prefix
  and use `YYYYMMDD-<token>-<slug>.md`, then renamed the canonical ticket files
  accordingly.
- 2026-04-08: verified the shipped scripts with Ruff and smoke-tested ticket
  creation, linking, and dependency mutation in a disposable temp workspace;
  moved the ticket to `complete_pending_acceptance`.
- 2026-04-19: closed per user confirmation that this ticket is completed.
