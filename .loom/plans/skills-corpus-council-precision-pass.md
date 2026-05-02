---
id: plan:skills-corpus-council-precision-pass
kind: plan
status: active
created_at: 2026-05-02T18:58:43Z
updated_at: 2026-05-02T18:58:43Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-council-precision-pass
  ticket:
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
    - ticket:cmdroute
external_refs: {}
---

# Purpose

Preserve the latest council review as an execution strategy and route each corpus
improvement into a bounded ticket. This plan exists so the refinement pass can run
without relying on transcript context, while live execution remains in tickets.

# Strategy

Work from vocabulary and owner-boundary foundations toward templates and final
hygiene:

1. Normalize route vocabulary so downstream drive, ticket, workspace, and plan
   guidance can cite one grammar.
2. Make support-surface handling explicit before further drive handoff cleanup.
3. Strengthen closure and autonomy owner records: ticket retrospective disposition
   and initiative delegated authority.
4. Align packet grammar and packet lifecycle across Ralph, critique, and wiki.
5. Harden critique target shape, templates, and evidence quality guidance.
6. Repair drive handoff write-scope collision and plan parallel/coverage checks.
7. Run final command-route wording hygiene.

For each ticket:

- compile a Ralph packet;
- launch a `fixer` child worker;
- inspect and reconcile child output;
- record structural evidence;
- run `oracle` critique with required profiles;
- resolve all findings before closure;
- record retrospective disposition in the ticket and any owner surfaces needed;
- commit and push with a semantic message before continuing.

# Strategy Snapshot

The council found the corpus strong and runtime-safe. Remaining defects are mostly
lexical drift, template defaults, packet lifecycle parity, evidence sufficiency,
and route/owner-layer clarity. The plan should sharpen these without adding a
runtime, hidden schema, command truth, or a new owner layer.

# Workstreams

- Route/support/drive foundation: tickets `rtvocab1`, `supp0x2a`, `authst4p`, and
  `dwhand10`.
- Closure and evidence: tickets `retrod3p` and `evshape9`.
- Packet and critique grammar: tickets `pktgram5`, `pktlife6`, and `revtgt7x`.
- Template and plan hardening: tickets `tmplph8x` and `planwv11`.
- Final command-route hygiene: ticket `cmdroute`.

# Milestones

- M1: Plan and tickets created.
- M2: Route/support/closure/autonomy grammar normalized.
- M3: Packet and critique grammar aligned.
- M4: Templates, evidence, drive handoff, and plan guidance hardened.
- M5: Command-route hygiene closed and initiative accepted.

# Sequencing

`ticket:rtvocab1` comes first because route vocabulary should be inherited by
drive, ticket, workspace, plan, and command-route cleanup.

`ticket:supp0x2a` comes second because support-surface discoverability constrains
drive handoff wording.

`ticket:retrod3p` and `ticket:authst4p` strengthen owner records before template
and drive cleanup depend on closure/autonomy fields.

`ticket:pktgram5` precedes `ticket:pktlife6` and `ticket:revtgt7x` because shared
packet grammar should settle before lifecycle and critique-target shape changes.

`ticket:tmplph8x` and `ticket:evshape9` harden copied artifacts and evidence after
owner/packet grammar is clearer.

`ticket:dwhand10` depends on route and support decisions. `ticket:planwv11`
depends on route and evidence/ticket clarity. `ticket:cmdroute` runs last as final
hygiene.

# Execution Waves

Wave 1:

- `ticket:rtvocab1`: normalize route vocabulary. Expected write scope:
  `skills/loom-records`, `skills/loom-drive`, `skills/loom-tickets`,
  `skills/loom-workspace`, and touched templates.

Wave 2:

- `ticket:supp0x2a`: canonicalize optional `.loom/support/` handling. Depends on
  `ticket:rtvocab1` for route wording.
- `ticket:retrod3p`: add ticket retrospective/promotion disposition. Depends on
  `ticket:rtvocab1` for route wording.
- `ticket:authst4p`: add initiative delegated authority/stop-condition cues.
  Depends on `ticket:rtvocab1` for route wording.

Wave 3:

- `ticket:pktgram5`: align packet grammar/templates. Depends on `ticket:rtvocab1`.
- `ticket:pktlife6`: strengthen critique/wiki packet lifecycle. Depends on
  `ticket:pktgram5`.
- `ticket:revtgt7x`: canonicalize `review_target`. Depends on `ticket:pktlife6`.

Wave 4:

- `ticket:tmplph8x`: harden templates against placeholder pollution. Depends on
  tickets `retrod3p`, `authst4p`, and `pktgram5`.
- `ticket:evshape9`: strengthen evidence quality guidance. Depends on
  `ticket:retrod3p`.
- `ticket:dwhand10`: remove drive handoff write-scope collision. Depends on
  tickets `rtvocab1`, `supp0x2a`, and `authst4p`.
- `ticket:planwv11`: improve plan coverage and parallel-wave checks. Depends on
  tickets `rtvocab1`, `retrod3p`, and `pktgram5`.

Wave 5:

- `ticket:cmdroute`: final optional-command wording hygiene. Depends on all prior
  tickets so it can inherit final route/owner wording.

Parallel execution: none for this drive. The user requested strict sequential
progress only after each ticket is closed and oracle issues are resolved. Write
scopes overlap enough that sequential execution is safer.

# Risks

- Over-normalization can make Loom feel bureaucratic instead of operational.
- Support-surface wording can accidentally make `.loom/support/` look canonical.
- Packet grammar cleanup can incorrectly make critique/wiki packets Ralph-governed.
- Template placeholder hardening can reduce example usefulness if too abstract.
- Evidence guidance can overclaim if it reads like a schema requirement rather
  than Markdown-native quality doctrine.

# Evidence Strategy

Each ticket should record structural evidence with the smallest honest checks:

- `git diff --check`;
- targeted `rg` queries before/after for the terms being normalized;
- manual comparison of touched templates against owning references;
- ticket-specific checks listed in each ticket;
- no runtime tests because this corpus has no app runtime or test suite.

# Plan Readiness Review

Spec / acceptance coverage:

- No separate spec is needed. Initiative `OBJ-*` metrics and ticket-local `ACC-*`
  criteria are sufficient because this pass refines protocol/operator guidance,
  not an external software behavior contract.

Placeholder scan:

- Each ticket must remove or explicitly improve placeholders it touches. The
  dedicated template-hardening ticket owns broad placeholder pollution review.

Ticket-sized slices:

- Twelve slices map one-to-one to council findings CR-001 through CR-012.

Likely write scopes:

- `ticket:rtvocab1`: route vocabulary references and downstream route examples.
- `ticket:supp0x2a`: workspace tree, drive handoff, records/frontmatter support
  artifact references, and README support-tree mentions if needed.
- `ticket:retrod3p`: ticket template, ticket acceptance gate, bootstrap/wiki/
  retrospective closure guidance.
- `ticket:authst4p`: initiative template/reference and drive continuity guidance.
- `ticket:pktgram5`: packet frontmatter reference and Ralph/critique/wiki packet
  templates/references.
- `ticket:pktlife6`: critique/wiki packet templates and domain skill Done Means.
- `ticket:revtgt7x`: critique templates/frontmatter grammar.
- `ticket:tmplph8x`: templates across `skills/**`.
- `ticket:evshape9`: `loom-evidence` references/template and ticket evidence
  teaching.
- `ticket:dwhand10`: drive handoff template/frontmatter and related packet-scope
  references.
- `ticket:planwv11`: plan template/reference and parallel Ralph/Git cross-links.
- `ticket:cmdroute`: workspace/wiki/status/ship guidance where command surfaces
  appear as route peers.

Likely verification posture:

- Observation-first structural validation for every ticket. `none` is not
  acceptable because protocol/operator guidance changes behavior.

Evidence and critique route:

- Oracle critique is mandatory for every ticket by user instruction.
- Required profiles are named by each ticket and should include at least
  `operator-clarity`; high-risk protocol-authority tickets also require
  `routing-safety` and `protocol-change` or `records-grammar`.

Stop / loopback conditions:

- Stop and ask the user only if a ticket requires new product direction, accepts
  material unresolved risk, adds a runtime/new owner layer, or contradicts the
  skills-only product boundary.
- Loop back to plan if a ticket splits into multiple independent changes.
- Loop back to constitution if a proposed fix contradicts no-runtime,
  skills-only, or ticket-ledger boundaries.

# Exit Criteria

- All 12 tickets are closed with evidence, oracle critique, and retrospective
  disposition.
- All medium/high critique findings are resolved, accepted as risk with ticket
  provenance, superseded by evidence, or converted into linked follow-up tickets.
- Initiative success metrics have a truthful completion basis.
- No runtime creep, command-wrapper truth, hidden helper requirement, or new
  canonical owner layer is introduced.
- The final commit for each ticket is pushed.

# Completion Basis

When `status: completed`, cite child tickets, evidence records, critique records,
semantic commits, pushes, retrospective dispositions, and any follow-up tickets or
accepted risks.
