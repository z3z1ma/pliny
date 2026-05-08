---
id: ticket:<token>
kind: ticket
status: proposed
change_class: "<TBD: choose one change class before saving>"
risk_class: "<TBD: choose low, medium, or high before saving>"
created_at: <UTC timestamp>
updated_at: <UTC timestamp>
scope:
  kind: repository
  repositories:
    - repo:root
links: {}
external_refs: {}
depends_on: []
---

# Summary

One or two sentences naming the bounded work, why it exists now, and the outcome
it should produce.

Use this lite template only for local, low-risk, single-ticket work with no
reusable acceptance contract, material ambiguity, mandatory critique, migration,
security/privacy boundary, or public/shared surface. Escalate to `ticket.md` when
any full-template trigger applies.

# Scope

In:

- <TBD: what belongs in this ticket>

Out:

- <TBD: what must not happen in this ticket>

Assumptions / decision triggers:

- <TBD or None - no material assumptions>

# Acceptance

Owner: <TBD: spec-owned or ticket-local>

Covered IDs or ticket-local criteria:

- <TBD: spec:<slug>#ACC-001 or ticket:<token>#ACC-001>

# Evidence

Disposition: <TBD: pending, sufficient, insufficient, challenged, stale, superseded, or not_required>

Records / expected observations:

- <TBD: evidence:<slug>, command/output to gather, or None - reason>

Gaps / limits:

- <TBD or None>

# Status / Next Move

Status rationale:

Blockers:

Next move:

Critique / promotion disposition when applicable:

# Journal

- <UTC timestamp>: <material update>
