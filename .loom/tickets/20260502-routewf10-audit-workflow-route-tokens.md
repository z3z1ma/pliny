---
id: ticket:routewf10
kind: ticket
status: ready
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-02T22:03:13Z
updated_at: 2026-05-02T22:03:13Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-template-grammar-safety-pass
  plan:
    - plan:skills-corpus-template-grammar-safety-pass
external_refs: {}
depends_on:
  - ticket:tkrout5
---

# Summary

Audit shared route vocabulary and dependent route lists for first-class workflow
coordinators such as ship, spike, codemap, and debugging.

# Context

Council finding `NC-010` found that some workflow coordinators may be absent from
shared route-token lists, inviting inconsistent local route grammar.

# Why Now

Route vocabulary should give fresh agents stable next-route tokens without
becoming a runtime enum or command router.

# Scope

- Audit `route-vocabulary.md` and downstream route-token lists/examples.
- Add or clarify workflow route tokens only when they name existing first-class
  workflow moves.
- Preserve the non-runtime, grep-friendly vocabulary framing.

# Out Of Scope

- Do not add a command router or runtime enum.
- Do not turn every skill display name into a route token.

# Acceptance Criteria

- ACC-001: Existing first-class workflow coordinator routes are either represented
  in shared route vocabulary or explicitly routed through existing tokens.
- ACC-002: Downstream route-token examples/lists align with the shared vocabulary.
- ACC-003: Route vocabulary remains grep-friendly guidance, not runtime schema.
- ACC-004: Evidence records route-token audits and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-010`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-template-grammar-safety-pass#OBJ-010` | pending | pending | open |
| `ticket:routewf10#ACC-001` through `ticket:routewf10#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces include `skills/loom-records/references/route-vocabulary.md`,
drive references, and ticket route examples.

# Blockers

Depends on `ticket:tkrout5`.

# Next Move / Next Route

Ralph implementation packet after dependencies close.

# Route Readiness

Route: ralph

Bounded iteration: workflow route-token audit and alignment.
Write boundary: targeted route vocabulary/dependent route examples, this ticket,
one evidence record, one critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: before/after searches for `ship`, `spike`, `codemap`, `debugging`, route
token lists, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: inconsistent route tokens can degrade workspace recovery.

Required critique profiles:

- routing-safety
- operator-clarity
- records-grammar

Findings:

None - no critique yet.

Disposition status: pending

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Pending after critique.

# Wiki Disposition

Pending retrospective decision after critique.

# Acceptance Decision

Accepted by:
Accepted at:
Basis:
Residual risks:

# Dependencies

- `ticket:tkrout5`

# Journal

- 2026-05-02T22:03:13Z: Created from council finding `NC-010`.
