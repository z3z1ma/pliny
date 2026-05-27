# Update Loom Mill README Positioning

ID: ticket:20260526-update-loom-mill-readme
Type: Ticket
Status: closed
Created: 2026-05-26
Updated: 2026-05-26
Risk: low - docs-only update with a narrow README write boundary and simple inspection evidence

## Summary

Update `loom-mill/README.md` so it reflects the current Loom Mill state instead of describing it as a "Factory Floor" MVP scaffold. The bounded closure claim is that the README's positioning language is current enough for a reader to understand what Loom Mill is now, while preserving accurate development instructions.

## Scope

Read `loom-mill/README.md` and the nearby Loom Mill package/source structure only as needed to describe the current state accurately. Write scope is limited to `loom-mill/README.md` unless inspection reveals a directly stale README-adjacent reference that must be called out before changing scope.

Out of scope: product redesign, Loom Mill feature changes, frontend/backend implementation, packaging changes, broader root documentation rewrites, or reintroducing Factory Floor naming as the primary positioning.

Stop and return to shaping if the current Loom Mill role is not clear from source and records, or if the README needs a larger product-direction decision rather than a stale wording update.

## Acceptance

- ACC-001: `loom-mill/README.md` no longer labels Loom Mill as a "Factory Floor" MVP or scaffold.
  - Evidence: inspect the README diff and search the updated README for `Factory Floor` and stale MVP scaffold wording.
  - Audit: docs-only review should challenge whether the new description matches the current Loom Mill surface without inventing unsupported product claims.

- ACC-002: The README gives a concise current-state description of Loom Mill while preserving accurate existing development setup and server instructions unless inspection proves they are stale.
  - Evidence: inspect the README and, if development instructions are edited, run the smallest relevant command or static check available for the changed Markdown.
  - Audit: review should check for overclaiming, stale setup commands, and accidental scope expansion beyond the Loom Mill README.

- ACC-003: The docs change is clean enough to commit or hand off.
  - Evidence: run `git diff --check` after the README edit.
  - Audit: separate Ralph audit is optional for closure because the change is low-risk and documentation-only, but the closing agent should still perform a focused self-review against ACC-001 through ACC-003.

## Current State

Closed. `loom-mill/README.md` now describes Loom Mill as a local Loom workspace UI/backend for browsing and editing `.loom` records, working in the Design Room, and coordinating ticket-owned workstations through factory, scheduling, and shipping views. The development setup and server instructions were preserved unchanged. Acceptance evidence: the README diff was inspected, `Factory Floor`, `MVP`, and `scaffold` no longer appear in `loom-mill/README.md`, and `git diff --check` passed with no output. Separate Ralph audit was not performed because the ticket explicitly allowed optional audit for this low-risk documentation-only change; focused self-review found ACC-001 through ACC-003 satisfied. Residual follow-up: `loom-mill/pyproject.toml` still contains stale package metadata wording, but changing it is outside this ticket's README-only write scope.

## Journal

- 2026-05-26: Created ticket from operator request to update the Loom Mill README so it no longer reflects the stale Factory Floor MVP framing.
- 2026-05-26: Marked active for bounded Ralph implementation run against `loom-mill/README.md`.
- 2026-05-26: Ralph implementation run updated only `loom-mill/README.md`, inspected nearby Loom Mill source/package shape, and reported clean README stale-wording checks plus `git diff --check`.
- 2026-05-26: Focused closure review confirmed ACC-001 through ACC-003. Closed with separate audit omitted as optional for this low-risk docs-only change; noted stale `loom-mill/pyproject.toml` description as out-of-scope follow-up.
