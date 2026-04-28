---
id: ticket:odpl001
kind: ticket
status: ready
change_class: protocol-authority
risk_class: high
created_at: 2026-04-28T00:00:00Z
updated_at: 2026-04-28T00:00:00Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  research:
    - research:gastown-simplified-parent-driver
  specs:
    - spec:objective-driven-parent-loop
  plans:
    - plan:objective-driven-parent-loop-skill
external_refs: {}
depends_on: []
---

# Summary

Create `loom-drive`, the first product surface for Loom's objective-driven
parent loop: a workflow-coordinator skill that lets a chat-initiated
agent clarify a high-level objective, create measurable owner records, decompose
bounded ticket tranches, execute through Ralph/subagents, reconcile truth, and
continue until objective satisfaction or a stop condition.

# Context

`research:gastown-simplified-parent-driver` concludes that the valuable
Gastown-like behavior is objective-driven continuation, not merely polling ready
tickets. `spec:objective-driven-parent-loop` defines the intended behavior and
constraints. `plan:objective-driven-parent-loop-skill` recommends implementing a
visible skill surface first, without scripts or daemons.

# Why Now

The current protocol can describe initiatives, plans, tickets, packets, evidence,
critique, and wiki, but it does not yet provide one explicit workflow for a
high-level user request to keep advancing through those layers with minimal human
prompting. This ticket creates that missing operator surface.

# Scope

- Create `skills/loom-drive/` as the workflow-coordinator skill for this behavior.
- Add the skill `SKILL.md` and any minimal references/templates needed for the
  objective-driven parent loop.
- Define user-questioning posture, objective shaping, tranche decomposition,
  Ralph/subagent delegation, reconciliation, continuation, and stop conditions.
- Include optional dedicated outer-loop subagent guidance as bounded transport,
  not a new canonical truth layer.
- Add targeted links from existing routing surfaces if needed for discoverability.
- Keep implementation within visible Markdown protocol files.

# Non-goals

- Do not add scripts, daemons, CLIs, dashboards, background polling, or hidden
  helper state.
- Do not add a new canonical owner layer.
- Do not implement a full Gastown clone, scheduler, merge queue, persistent agent
  identity system, or federation.
- Do not add a large golden example unless it remains small enough for this
  ticket; otherwise create follow-up work.

# Acceptance Criteria

- ACC-001: The product surface tells agents when to activate the
  objective-driven parent loop for high-level chat requests.
- ACC-002: The surface tells agents how to ask enough focused user questions to
  establish measurable objective/success criteria without requiring approval for
  every downstream step.
- ACC-003: The surface routes durable truth to initiative, research, spec, plan,
  ticket, packet, evidence, critique, wiki, or memory as appropriate.
- ACC-004: The surface defines the repeated loop: shape objective, plan tranche,
  create tickets, execute bounded work, reconcile, reassess objective, continue
  or stop.
- ACC-005: The surface defines optional dedicated outer-loop subagent use and
  requires parent reconciliation of its output.
- ACC-006: The surface preserves the no-script/no-daemon/no-new-layer constraint.
- ACC-007: Existing skill routing points users/agents to the new workflow where
  appropriate.
- ACC-008: Structural validation evidence and critique are recorded before
  acceptance.

# Coverage

Covers:

- `spec:objective-driven-parent-loop` ACC-001
- `spec:objective-driven-parent-loop` ACC-002
- `spec:objective-driven-parent-loop` ACC-003
- `spec:objective-driven-parent-loop` ACC-004
- `spec:objective-driven-parent-loop` ACC-005
- `spec:objective-driven-parent-loop` ACC-006
- `spec:objective-driven-parent-loop` ACC-007

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `spec:objective-driven-parent-loop` ACC-001..ACC-007 | None yet | None yet | open |

# Execution Notes

Likely implementation shape: create `skills/loom-drive/` as a workflow
coordinator skill with `SKILL.md`, a parent-loop reference, and an optional
outer-loop handoff template. Keep it explicit that this skill coordinates
existing owner layers and does not create objective truth outside initiatives,
specs, plans, tickets, packets, evidence, critique, and wiki.

# Blockers

None.

# Next Move / Next Route

Ralph implementation packet.

# Ralph Readiness

Bounded iteration:

Create the first objective-loop skill surface and targeted discovery links. Do
not add examples or broad cross-corpus rewrites unless required for coherence.

Write boundary:

- `skills/loom-drive/**`
- targeted links in `skills/loom-workspace/SKILL.md` or
  `skills/loom-workspace/references/routing.md` if needed
- targeted links in `README.md` only if the new skill would otherwise be hidden
- `.loom/evidence/**` for validation output if the child records evidence

Likely verification posture:

Observation-first structural validation.

Expected output contract:

- files changed
- rationale for skill placement
- validation commands/searches performed
- residual risks
- recommended next route, including whether critique should run immediately

# Evidence

Expected: structural validation evidence after implementation, including diff
review and targeted searches for forbidden runtime/daemon implications and route
discoverability.

# Critique Disposition

Risk class: high

Critique policy: mandatory

Policy rationale:

This changes operator behavior and autonomous continuation boundaries. It could
accidentally create a hidden runtime expectation, new truth layer, or unsafe
scope-widening loop.

Required critique profiles:

- workflow-boundary
- protocol-authority

Findings:

None - no critique yet.

Disposition status: pending

Deferral / not-required rationale:

None.

# Wiki Disposition

Likely needed after critique if the workflow is accepted. A future wiki page may
explain objective-driven parent loops for operators.

# Acceptance Decision

Accepted by:

Accepted at:

Basis:

Residual risks:

# Dependencies

Depends on `spec:objective-driven-parent-loop` and
`plan:objective-driven-parent-loop-skill`, both created before this ticket.

# Journal

- 2026-04-28T00:00:00Z: Created ticket from operator clarification that the
  desired Gastown-like value is high-level objective continuation through Loom
  owner records and Ralph/subagents, without scripts or daemons.
