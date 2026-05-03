---
id: plan:skills-corpus-template-grammar-safety-pass
kind: plan
status: completed
created_at: 2026-05-02T22:03:13Z
updated_at: 2026-05-03T00:24:08Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-template-grammar-safety-pass
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

# Purpose

Preserve the next council review as an execution strategy and route each template
or grammar safety issue into one bounded ticket. This plan keeps the next
refinement loop recoverable from files while tickets remain the live execution
ledger.

# Strategy

Work from cross-cutting safety semantics toward templates and public framing:

1. Clarify packet support lifecycle and mandatory critique closure gates first.
2. Align drive handoff and packet provenance grammar before downstream templates
   rely on them.
3. Repair ticket template route and acceptance ownership ambiguity.
4. Harden sibling packet templates, placeholder defaults, critique recommendations,
   and workflow route tokens.
5. Finish with README product-surface framing after the grammar decisions settle.

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

The council found the corpus coherent and runtime-safe. Remaining issues are
mostly places where copied templates or cross-reference grammar can still teach a
fresh agent to overclaim, duplicate route truth, guess support metadata, confuse
packet lifecycle with project truth, or blur public product-surface boundaries.

# Workstreams

- Safety gates: tickets `pktsupp1` and `critgate2`.
- Support/packet grammar: tickets `drvgram3` and `pktprov4`.
- Ticket templates: tickets `tkrout5` and `accspec6`.
- Sibling workflow/template polish: tickets `sibpkt7`, `phsafe8`, and `critrec9`.
- Route/public framing: tickets `routewf10` and `readme11`.

# Milestones

- M1: Plan and tickets created.
- M2: Packet lifecycle and critique closure wording sharpened.
- M3: Drive handoff, packet provenance, and ticket templates aligned.
- M4: Sibling packet, placeholder, critique recommendation, and route vocabulary
  safety issues closed.
- M5: README framing closed and initiative accepted.

# Sequencing

`ticket:pktsupp1` and `ticket:critgate2` come first because lifecycle and closure
semantics constrain downstream packet, critique, and acceptance wording.

`ticket:drvgram3` and `ticket:pktprov4` come next because handoff and packet
metadata grammar should settle before template-specific cleanup.

`ticket:tkrout5` precedes `ticket:accspec6` because both touch ticket templates,
and route ownership should be stable before acceptance placeholder branches are
reshaped.

`ticket:sibpkt7`, `ticket:phsafe8`, and `ticket:critrec9` then repair sibling
packet anchors, remaining placeholder defaults, and critique recommendation
language.

`ticket:routewf10` should run after ticket route fields are clarified. `ticket:readme11`
runs last so README framing can inherit the final product-surface and route
grammar.

# Execution Waves

Wave 1:

- `ticket:pktsupp1`: packet support lifecycle ownership.
- `ticket:critgate2`: mandatory critique closure gate.

Wave 2:

- `ticket:drvgram3`: drive handoff metadata grammar.
- `ticket:pktprov4`: packet provenance/source split.

Wave 3:

- `ticket:tkrout5`: ticket route field ownership.
- `ticket:accspec6`: spec-owned vs ticket-local acceptance placeholders.

Wave 4:

- `ticket:sibpkt7`: critique/wiki packet optional ticket anchors.
- `ticket:phsafe8`: remaining placeholder / accepted-status safety.
- `ticket:critrec9`: critique recommendation vocabulary.

Wave 5:

- `ticket:routewf10`: workflow route-token audit.
- `ticket:readme11`: README product-surface framing.

Parallel execution: none for this drive. The user requested strict sequential
progress only after each ticket is closed and oracle issues are resolved. Write
scopes overlap enough that sequential execution is safer.

# Risks

- Lifecycle wording can accidentally make packets canonical instead of support
  artifacts.
- Closure wording can accidentally block closure over recommended critique when
  only mandatory critique should be hard-blocking.
- Route-token expansion can look like a runtime enum if not framed as grep-friendly
  vocabulary.
- README cleanup can over-explain internals at the expense of public clarity.

# Evidence Strategy

Each ticket should record structural evidence with the smallest honest checks:

- `git diff --check`;
- targeted `rg` queries before/after for the normalized terms;
- manual comparison against owning references/templates;
- ticket-specific checks listed in each ticket;
- no runtime tests because this corpus has no app runtime or test suite.

# Plan Readiness Review

Spec / acceptance coverage:

- No separate spec is needed. Initiative `OBJ-*` metrics and ticket-local `ACC-*`
  criteria are sufficient because this pass refines protocol/operator guidance,
  not external software behavior.

Ticket-sized slices:

- Eleven slices map one-to-one to council findings `NC-001` through `NC-011`.

Likely write scopes:

- `ticket:pktsupp1`: `skills/loom-records/references/naming-and-ids.md`,
  `skills/loom-workspace/references/workspace-tree.md`, and
  `skills/loom-records/references/status-lifecycle.md`.
- `ticket:critgate2`: bootstrap critique/validation references.
- `ticket:drvgram3`: drive handoff template and drive continuity/checkpoint
  references.
- `ticket:pktprov4`: packet frontmatter reference and Ralph/critique/wiki packet
  templates.
- `ticket:tkrout5`: ticket template/readiness reference.
- `ticket:accspec6`: ticket template and claim-coverage reference.
- `ticket:sibpkt7`: critique/wiki packet templates and sibling workflow notes.
- `ticket:phsafe8`: remaining unsafe placeholder surfaces found by targeted scan.
- `ticket:critrec9`: critique template and finding/recommendation references.
- `ticket:routewf10`: route vocabulary and dependent route lists.
- `ticket:readme11`: README product-surface framing.

Likely verification posture:

- Observation-first structural validation for every ticket. `none` is not
  acceptable because these are operator-guidance and template-safety changes.

Evidence and critique route:

- Oracle critique is mandatory for every ticket by user instruction.
- Required profiles are named by each ticket and should include the relevant mix
  of `operator-clarity`, `routing-safety`, `records-grammar`,
  `template-safety`, `closure-honesty`, and `owner-boundary`.

Stop / loopback conditions:

- Stop and ask the user only if a ticket requires new product direction, accepts
  material unresolved risk, adds runtime/new owner layer, or contradicts the
  skills-only product boundary.
- Loop back to plan if a finding splits into multiple independent changes.
- Loop back to constitution if a proposed fix contradicts no-runtime, skills-only,
  packet-support, or ticket-ledger boundaries.

# Exit Criteria

- All 11 tickets are closed with evidence, oracle critique, and retrospective
  disposition.
- All medium/high critique findings are resolved, accepted as risk with ticket
  provenance, superseded by evidence, or converted into linked follow-up tickets.
- Initiative success metrics have a truthful completion basis.
- No runtime creep, command-wrapper truth, hidden helper requirement, or new
  canonical owner layer is introduced.
- The final commit for each ticket is pushed.

# Completion Basis

Completed at: 2026-05-03T00:24:08Z.

Basis:

- All 11 child tickets are `closed`: `ticket:pktsupp1`, `ticket:critgate2`,
  `ticket:drvgram3`, `ticket:pktprov4`, `ticket:tkrout5`, `ticket:accspec6`,
  `ticket:sibpkt7`, `ticket:phsafe8`, `ticket:critrec9`, `ticket:routewf10`, and
  `ticket:readme11`.
- Each child ticket acceptance dossier links its evidence record, mandatory oracle
  critique record, consumed Ralph packet, retrospective / promotion disposition,
  and acceptance decision.
- Pushed per-ticket commits: `52cc82e` (`ticket:pktsupp1`), `63d587f`
  (`ticket:critgate2`), `c70983f` (`ticket:drvgram3`), `f0491f2`
  (`ticket:pktprov4`), `26964ce` (`ticket:tkrout5`), `4dde3b7`
  (`ticket:accspec6`), `4b85062` (`ticket:sibpkt7`), `cac7c7c`
  (`ticket:phsafe8`), `3bfbe92` (`ticket:critrec9`), `2de8a2e`
  (`ticket:routewf10`), and `f95ff6b` (`ticket:readme11`).
- No accepted residual risk or follow-up tickets were recorded for this plan.
- Exit criteria are satisfied: all tickets are closed with evidence, oracle
  critique, retrospective disposition, semantic commit, and push; no runtime creep,
  command-wrapper truth, hidden helper requirement, or new canonical owner layer
  was introduced.
