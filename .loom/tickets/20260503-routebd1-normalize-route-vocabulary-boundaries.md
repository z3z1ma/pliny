---
id: ticket:routebd1
kind: ticket
status: ready
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-03T00:56:36Z
updated_at: 2026-05-03T00:56:36Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-residual-protocol-sharpening-pass
  plan:
    - plan:skills-corpus-residual-protocol-sharpening-pass
  research:
    - research:skills-corpus-residual-audit-synthesis
external_refs: {}
depends_on: []
---

# Summary

Normalize route vocabulary boundaries, constitution/initiative routing, child
outcome translation, and `ask_user` decision grammar.

# Context

Council finding `NC2-003` and older audit actions 2 and 8 found that current route
guidance does not fully settle constitution/initiative route-token handling,
vocabulary boundaries, child-outcome translation, and `ask_user` fields.

# Why Now

Route fields are copied into tickets, drive checkpoints, and handoffs. If route
tokens blur with statuses, child outcomes, or user-question posture, fresh agents
can record false next-route truth.

# Scope

- Decide whether `constitution` and `initiative` are canonical route tokens or are
  reached through existing shaping/escalation routes.
- Add or clarify a vocabulary-boundaries table across route tokens, ticket states,
  record statuses, child outcomes, critique finding states, and ticket finding
  dispositions.
- Clarify that a child outcome is not a route token until the parent translates it.
- Make `ask_user` fields explicit: decision needed, why the agent cannot infer it
  safely, and owner record to update after answer.

# Out Of Scope

- Do not create a runtime enum, command router, schema, validator, or new owner
  layer.
- Do not turn every skill name into a route token.
- Do not weaken delegated autonomy by requiring user prompts for low-risk,
  reversible choices.

# Acceptance Criteria

- ACC-001: Constitution/initiative routing is either added to canonical route
  tokens or explicitly documented as intentionally reached through existing
  shaping/escalation routes.
- ACC-002: Route vocabulary distinguishes route tokens from ticket statuses,
  record statuses, child outcomes, critique finding states, and ticket-owned
  finding dispositions.
- ACC-003: `ask_user` guidance names decision needed, unsafe-inference reason, and
  owner record update target.
- ACC-004: Evidence records before/after route/vocabulary searches and
  `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-001`
- `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-002`
- `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-003`
- `ticket:routebd1#ACC-001`
- `ticket:routebd1#ACC-002`
- `ticket:routebd1#ACC-003`
- `ticket:routebd1#ACC-004`
- `ticket:routebd1#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-001` through `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-003` | pending | pending | open |
| `ticket:routebd1#ACC-001` through `ticket:routebd1#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched surfaces include route vocabulary, status lifecycle boundary
wording, workspace/drive routing references, and ticket route snippets if needed.

# Blockers

None.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Route: ralph

Bounded iteration: route vocabulary and `ask_user` boundary cleanup.
Write boundary: route/status/workspace/drive/ticket route surfaces needed for the
acceptance criteria, this ticket, one evidence record, one critique record, and
one Ralph packet.
Likely verification posture: observation-first structural validation.
Expected output contract: changed files, evidence, ticket update, and critique
recommendation.

# Evidence

Expected: before/after searches for route tokens, child outcomes, `ask_user`,
constitution/initiative routing, status/finding vocabulary, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: route vocabulary shapes operator decisions and can corrupt live
next-route truth if ambiguous.

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

None.

# Journal

- 2026-05-03T00:56:36Z: Created from council finding `NC2-003` and older audit
  actions 2 and 8.
