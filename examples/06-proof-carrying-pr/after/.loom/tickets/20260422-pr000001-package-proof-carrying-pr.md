---
id: ticket:pr000001
kind: ticket
status: complete_pending_acceptance
change_class: release-packaging
created_at: 2026-04-22T00:00:00Z
updated_at: 2026-04-22T00:05:00Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  spec:
    - spec:proof-carrying-pr
  evidence:
    - evidence:proof-carrying-pr-package
  critique:
    - critique:proof-carrying-pr-review
  wiki:
    - wiki:proof-carrying-pr
external_refs: {}
depends_on: []
---

# Summary

Package a proof-carrying PR body from Loom records.

# Acceptance Criteria

- PR body cites ticket, claims, evidence, critique, residual risks, and
  follow-ups.
- Ticket closure remains with acceptance.

# Coverage

Covers:
- spec:proof-carrying-pr#ACC-001
- spec:proof-carrying-pr#ACC-002

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| spec:proof-carrying-pr#ACC-001 | evidence:proof-carrying-pr-package | critique:proof-carrying-pr-review no blocking findings | supported |
| spec:proof-carrying-pr#ACC-002 | evidence:proof-carrying-pr-package | critique:proof-carrying-pr-review no blocking findings | supported |

# Evidence

- evidence:proof-carrying-pr-package

# Critique Disposition

Risk class: medium

Required critique profiles:
- operator-clarity

Findings:
- none

Status: completed

# Wiki Disposition

Promoted to `wiki:proof-carrying-pr` because the packaging route is reusable.

# Acceptance Decision

Accepted by:
Accepted at:
Basis:
Residual risks:
