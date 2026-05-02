---
id: ticket:cmdroute
kind: ticket
status: ready
change_class: record-hygiene
risk_class: medium
created_at: 2026-05-02T18:58:43Z
updated_at: 2026-05-02T18:58:43Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-council-precision-pass
  plan:
    - plan:skills-corpus-council-precision-pass
external_refs: {}
depends_on:
  - ticket:rtvocab1
  - ticket:supp0x2a
  - ticket:retrod3p
  - ticket:authst4p
  - ticket:pktgram5
  - ticket:pktlife6
  - ticket:revtgt7x
  - ticket:tmplph8x
  - ticket:evshape9
  - ticket:dwhand10
  - ticket:planwv11
---

# Summary

Remove optional-command wording that presents command surfaces as peers to owner
layers or workflow routes.

# Context

Council finding `CR-012` found some output contracts ask for “workflow, owner
layer, or optional command,” which risks making command wrappers look like
protocol truth.

# Why Now

This final hygiene ticket should inherit the settled route vocabulary and avoid
creating command-wrapper truth in the cleaned corpus.

# Scope

- Search for optional-command/adaptor wording that appears as route peer language.
- Replace with owner-layer/workflow-route wording and mention adapters only after
  the route is named when useful.
- Preserve existing no-runtime/no-command-truth doctrine.

# Out Of Scope

- Do not remove legitimate examples of shell commands as filesystem tools.
- Do not remove harness adapter documentation where it is clearly transport.
- Do not add command wrappers or command surfaces.

# Acceptance Criteria

- ACC-001: No product guidance presents optional commands as peers to owner layers
  or workflow routes.
- ACC-002: Adapter/command references that remain are clearly transport or
  convenience surfaces, not protocol truth.
- ACC-003: Final wording aligns with the shared route vocabulary.
- ACC-004: Evidence records command/adaptor wording searches and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-council-precision-pass#OBJ-012`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-council-precision-pass#OBJ-012` | pending | pending | open |
| `ticket:cmdroute#ACC-001` through `ticket:cmdroute#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces include workspace status snapshot, wiki guidance, ship
guidance, and any references where optional commands appear as route peers.

# Blockers

Depends on all prior tickets in this plan.

# Next Move / Next Route

Ralph implementation packet after dependencies close.

# Route Readiness

Route: Ralph implementation packet

Bounded iteration: final command/adaptor route-wording hygiene.
Write boundary: targeted `skills/**` wording, this ticket, one evidence record,
one critique record, and one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: searches for optional command/adaptor route wording and
`git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: user requires oracle critique; command-wrapper truth is an
explicit non-goal.

Required critique profiles:

- operator-clarity
- routing-safety
- records-grammar

Findings:

None - no critique yet.

Disposition status: pending

Deferral / not-required rationale:

Not deferred.

# Wiki Disposition

Pending retrospective decision after critique.

# Acceptance Decision

Accepted by:
Accepted at:
Basis:
Residual risks:

# Dependencies

- `ticket:rtvocab1`
- `ticket:supp0x2a`
- `ticket:retrod3p`
- `ticket:authst4p`
- `ticket:pktgram5`
- `ticket:pktlife6`
- `ticket:revtgt7x`
- `ticket:tmplph8x`
- `ticket:evshape9`
- `ticket:dwhand10`
- `ticket:planwv11`

# Journal

- 2026-05-02T18:58:43Z: Created from council finding `CR-012`.
