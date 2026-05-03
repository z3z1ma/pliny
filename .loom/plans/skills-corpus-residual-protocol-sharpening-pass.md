---
id: plan:skills-corpus-residual-protocol-sharpening-pass
kind: plan
status: active
created_at: 2026-05-03T00:56:36Z
updated_at: 2026-05-03T00:56:36Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-residual-protocol-sharpening-pass
  research:
    - research:skills-corpus-residual-audit-synthesis
  ticket:
    - ticket:routebd1
    - ticket:promdisp2
    - ticket:critfail3
    - ticket:wssupp4
    - ticket:claimmx5
    - ticket:wsalias6
    - ticket:ralphchk7
    - ticket:evfresh8
    - ticket:driveref9
    - ticket:minpol10
external_refs: {}
---

# Purpose

Sequence the residual protocol-sharpening findings into ten bounded tickets so
the next refinement loop remains recoverable from owner records instead of chat.

# Strategy

Work from vocabulary and closure semantics toward templates and copyability:

1. Decide route/vocabulary boundaries first because downstream ticket and drive
   surfaces cite route tokens and `ask_user` behavior.
2. Align retrospective / promotion wording and mandatory critique gates before
   acceptance templates are treated as stable.
3. Repair workspace/support and claim matrix copy surfaces.
4. Tighten Ralph and evidence template mechanics.
5. Move drive transport detail into a reference and finish with minor polish.

For each ticket:

- compile a Ralph packet;
- launch a `fixer` child worker;
- inspect and reconcile child output;
- record structural evidence;
- run `oracle` critique with required profiles;
- resolve all findings before closure;
- record retrospective disposition in the ticket;
- commit and push with a semantic message before continuing.

# Strategy Snapshot

The current corpus is coherent and runtime-safe. Remaining findings are narrow
places where copied templates, route wording, support/query grammar, or checklist
omissions can still teach a fresh agent to conflate vocabularies, overclaim
closure, under-record freshness, duplicate scope truth, or miss a promotion route.

# Workstreams

- Vocabulary and routing: `ticket:routebd1`.
- Closure and promotion gates: `ticket:promdisp2` and `ticket:critfail3`.
- Workspace and ticket templates: `ticket:wssupp4`, `ticket:claimmx5`, and
  `ticket:wsalias6`.
- Packet/evidence mechanics: `ticket:ralphchk7` and `ticket:evfresh8`.
- Drive/polish: `ticket:driveref9` and `ticket:minpol10`.

# Milestones

- M1: Plan and tickets created.
- M2: Route and promotion boundary tickets closed.
- M3: Ticket/workspace template tickets closed.
- M4: Ralph/evidence mechanics tickets closed.
- M5: Drive reference extraction and minor polish closed.

# Sequencing

`ticket:routebd1` comes first because it may affect route-token and `ask_user`
wording in later surfaces.

`ticket:promdisp2` and `ticket:critfail3` follow because closure and critique gate
language should be stable before template-specific cleanup.

`ticket:wssupp4`, `ticket:claimmx5`, and `ticket:wsalias6` then repair workspace
and ticket copy surfaces.

`ticket:ralphchk7` and `ticket:evfresh8` tighten packet and evidence mechanics
after claim/status grammar is stable.

`ticket:driveref9` and `ticket:minpol10` finish with progressive disclosure and
small copyability polish.

# Execution Waves

Wave 1:

- `ticket:routebd1`: route vocabulary and `ask_user` boundary.

Wave 2:

- `ticket:promdisp2`: retrospective / promotion disposition wording.
- `ticket:critfail3`: mandatory critique fail-closed template guidance.

Wave 3:

- `ticket:wssupp4`: workspace/support lifecycle and query grammar.
- `ticket:claimmx5`: claim matrix status guidance.
- `ticket:wsalias6`: workspace alias template dedupe.

Wave 4:

- `ticket:ralphchk7`: Ralph launch checklist.
- `ticket:evfresh8`: evidence freshness and challenge examples.

Wave 5:

- `ticket:driveref9`: drive outer-loop transport reference extraction.
- `ticket:minpol10`: minor template/path polish.

Parallel execution: none for this drive. The continuing operator preference is
strict sequential progress only after each ticket is closed and oracle issues are
resolved. Several tickets touch shared templates and references, so sequential
execution is safer.

# Risks

- Vocabulary work can make route tokens look like runtime schema if not framed as
  grep-friendly Markdown guidance.
- Template hardening can become noisy if it adds ceremony without sharper stop
  conditions.
- Drive refactoring can accidentally change behavior while trying to move prose.
- Minor polish can expand into style rewriting if not kept tightly scoped.

# Evidence Strategy

Each ticket should record structural evidence with the smallest honest checks:

- `git diff --check`;
- targeted `rg` queries before/after for the ticket-specific vocabulary or
  template surface;
- manual comparison against owning references/templates;
- ticket-specific checks listed in each ticket;
- no runtime tests because this corpus has no app runtime or test suite.

# Plan Readiness Review

Spec / acceptance coverage:

- No separate spec is needed. Initiative `OBJ-*` metrics and ticket-local `ACC-*`
  criteria are sufficient because this pass refines protocol/operator guidance,
  not external software behavior.

Placeholder scan:

- Relevant older audit placeholders were reviewed in
  `research:skills-corpus-residual-audit-synthesis`. No save-ready plain `TBD`
  record was found in the bootstrap here-doc; remaining placeholder polish is
  bounded by `ticket:minpol10`.

Ticket-sized slices:

- Ten slices map to the combined council and older-audit findings without creating
  a runtime or platform pass.

Likely write scopes:

- `ticket:routebd1`: `skills/loom-records/references/route-vocabulary.md`,
  `skills/loom-records/references/status-lifecycle.md`, workspace/drive routing
  references, and ticket route snippets if needed.
- `ticket:promdisp2`: bootstrap validation/critique references, Ralph work driver,
  ship/git guidance, and README workflow snippet if still stale.
- `ticket:critfail3`: `skills/loom-tickets/templates/ticket.md` and possibly
  ticket acceptance-gate reference.
- `ticket:wssupp4`: status lifecycle, query/linking, naming/IDs, workspace tree,
  and workspace template lifecycle references.
- `ticket:claimmx5`: ticket template and claim-coverage reference.
- `ticket:wsalias6`: workspace template and workspace references.
- `ticket:ralphchk7`: Ralph packet template, Ralph packet contract, and shared
  packet frontmatter.
- `ticket:evfresh8`: evidence template, evidence skill/reference guidance, and
  claim-coverage examples.
- `ticket:driveref9`: `skills/loom-drive/SKILL.md` and a new drive reference.
- `ticket:minpol10`: memory entity template, wiki path reference wording,
  records skill wording, and any directly related placeholder warning surface.

Likely verification posture:

- Observation-first structural validation for every ticket. `none` is not
  acceptable because these are operator-guidance and template-safety changes.

Evidence and critique route:

- Oracle critique is mandatory for every ticket by continuing user instruction.
- Required profiles are named by each ticket and should include the relevant mix
  of `operator-clarity`, `routing-safety`, `records-grammar`, `template-safety`,
  `closure-honesty`, `owner-boundary`, `packet-safety`, and `evidence-quality`.

Stop / loopback conditions:

- Stop and ask the user only if a ticket requires new product direction, accepts
  material unresolved risk, adds runtime/new owner layer, or contradicts the
  skills-only product boundary.
- Loop back to plan if a finding splits into multiple independent changes.
- Loop back to constitution if a proposed fix contradicts no-runtime,
  skills-only, packet-support, or ticket-ledger boundaries.

# Exit Criteria

- All ten tickets are closed with evidence, oracle critique, and retrospective
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
