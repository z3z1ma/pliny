---
id: initiative:skills-corpus-template-grammar-safety-pass
kind: initiative
status: active
created_at: 2026-05-02T22:03:13Z
updated_at: 2026-05-02T22:03:13Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  plan:
    - plan:skills-corpus-template-grammar-safety-pass
  ticket:
    - ticket:pktsupp1
    - ticket:critgate2
    - ticket:drvgram3
    - ticket:pktprov4
    - ticket:tkrout5
    - ticket:accspec6
    - ticket:sibpkt7
    - ticket:phsafe8
    - ticket:critrec9
    - ticket:routewf10
    - ticket:readme11
external_refs: {}
---

# Objective

Turn the next council review of `skills/` and `README.md` into an evidence-backed,
critique-reviewed safety pass that sharpens template grammar, lifecycle wording,
closure gates, and public package framing without adding runtime enforcement,
command-wrapper truth, hidden helper requirements, or new canonical owner layers.

# Why Now

The prior precision pass closed route/support/packet/template/evidence and
command-route drift. The latest council review found a narrower frontier: copied
templates and cross-reference grammar can still make fresh agents guess about
packet support lifecycle, critique gates, drive handoff metadata, route fields,
acceptance ownership, sibling packet anchors, and public package boundaries.

# In Scope

- Clarify packet support-artifact lifecycle ownership without making packets own
  project truth.
- Tighten mandatory critique closure wording in bootstrap doctrine.
- Document or simplify drive outer-loop handoff metadata.
- Split packet source-fingerprint provenance from packet source sets.
- Remove ticket route-field duplication and acceptance placeholder ambiguity.
- Make critique/wiki packet ticket anchors explicitly optional where the workflow
  does not require a ticket.
- Harden remaining placeholder and accepted-status defaults that can be saved
  unsafely.
- Normalize critique recommendation vocabulary away from ticket-state confusion.
- Audit workflow route tokens for first-class workflow coordinators.
- Clarify README product-surface framing.

# Out Of Scope

- Do not add a runtime validator, schema engine, CLI, daemon, database, MCP
  dependency, command wrapper, or hidden helper as protocol truth.
- Do not create a new canonical owner layer.
- Do not rewrite the corpus for style alone.
- Do not make packets, support artifacts, README, examples, adapters, or external
  systems own Loom truth.

# Success Metrics

- OBJ-001: Packet/support lifecycle wording says packets own their own support
  lifecycle status while not owning project truth or ticket live state.
- OBJ-002: Bootstrap closure guidance cannot be read as allowing mandatory
  critique to be deferred before closure.
- OBJ-003: Drive outer-loop handoff metadata is documented or simplified so fresh
  agents do not guess field semantics.
- OBJ-004: Packet `source_fingerprint.compiled_from` and `sources` have a clear
  split, and packet templates follow it.
- OBJ-005: Ticket templates have one owner for the route token; readiness sections
  describe route-specific readiness without duplicating route truth.
- OBJ-006: Ticket acceptance placeholders distinguish spec-owned acceptance from
  ticket-local `ACC-*` criteria.
- OBJ-007: Critique and wiki packet templates make ticket refs optional when the
  target is not ticket-centered.
- OBJ-008: Remaining copyable placeholders and default accepted statuses fail
  closed instead of looking save-ready.
- OBJ-009: Critique recommendation vocabulary is distinct from canonical ticket
  states and route tokens.
- OBJ-010: Shared route vocabulary covers first-class workflow coordinator routes
  that downstream surfaces need, without becoming a runtime enum.
- OBJ-011: README product-surface wording clearly distinguishes `skills/` from
  explanatory, maintainer, adapter, example, and packaging support files.
- OBJ-012: Every child ticket is closed with evidence, oracle critique,
  retrospective disposition, semantic commit, and push.

# Milestones

- Milestone 1: Owner records and 11 bounded tickets exist.
- Milestone 2: Packet lifecycle and critique closure gates are sharpened.
- Milestone 3: Drive, packet, and ticket grammar surfaces are aligned.
- Milestone 4: Sibling packet, placeholder, critique recommendation, and route
  vocabulary safety issues are closed.
- Milestone 5: README framing closes and the initiative is accepted.

# Dependencies

- Depends on council review session `ses_215579f84ffep0yb0xX8Cg3W07`.
- Starts from pushed baseline `6a9f9fdc0ddbd858f2e7406aa7ae673bc0a17ff6`
  (`chore: close skills corpus precision pass`).

# Risks

- Over-correcting route grammar can make ordinary prose feel like a rigid enum.
- Packet lifecycle clarification can accidentally make packets look canonical.
- Critique closure tightening can overstate recommended critique requirements if
  mandatory and recommended policies are not kept distinct.
- Template hardening can reduce usability if placeholders become too noisy.

# Linked Work

- Plan: `plan:skills-corpus-template-grammar-safety-pass`
- Tickets: `ticket:pktsupp1`, `ticket:critgate2`, `ticket:drvgram3`,
  `ticket:pktprov4`, `ticket:tkrout5`, `ticket:accspec6`, `ticket:sibpkt7`,
  `ticket:phsafe8`, `ticket:critrec9`, `ticket:routewf10`, and `ticket:readme11`

# Status Summary

Active. Council finding set `NC-001` through `NC-011` has been decomposed into 11
Ralph-sized tickets. Execute sequentially with Ralph/fixer, oracle critique,
retrospective disposition, semantic commits, and pushes for each ticket.

# Completion Basis

When `status: completed`, cite child tickets, evidence, oracle critique records,
retrospective dispositions, semantic commits, pushes, accepted residual risks, and
any follow-up tickets.
