---
id: plan:skills-corpus-context-integrity-hardening-pass
kind: plan
status: active
created_at: 2026-05-03T04:09:51Z
updated_at: 2026-05-03T06:33:53Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-context-integrity-hardening-pass
  research:
    - research:skills-corpus-context-integrity-hardening-review
    - research:skills-corpus-third-pass-follow-up-validation
  ticket:
    - ticket:bootinv1
    - ticket:trustbd2
    - ticket:vocabx08
    - ticket:tplsave3
    - ticket:pktfam04
    - ticket:evhard05
    - ticket:reconchk
    - ticket:localed7
    - ticket:queryrc9
    - ticket:drives10
    - ticket:shipacc1
    - ticket:rready12
    - ticket:drvcont13
    - ticket:wikiret14
    - ticket:wroute15
    - ticket:phvalid16
    - ticket:bootdoc17
    - ticket:rsrcmt18
    - ticket:pktws19
    - ticket:ralphg20
    - ticket:pktorph21
    - ticket:askpost22
    - ticket:readwsh23
    - ticket:doctitl24
    - ticket:netgate25
    - ticket:gitstat26
    - ticket:retmem27
    - ticket:critph28
    - ticket:readrte29
external_refs: {}
---

# Purpose

Sequence the council-driven and third-pass skills-corpus hardening work into
bounded tickets that improve fresh-agent operability without adding runtime
machinery or a new owner layer.

# Strategy

Work from doctrine and vocabulary toward operational surfaces:

1. Put only minimal orientation in bootstrap.
2. Add trust boundaries before expanding evidence and query surfaces.
3. Stabilize route/status vocabulary before templates and workflow references copy
   more examples.
4. Tighten templates, packets, evidence, and parent reconciliation.
5. Finish the original ergonomics and workflow boundary tickets.
6. Run third-pass precision follow-ups for readiness completeness, route
   priorities, support boundaries, packet safety, and README framing.

For each ticket:

- compile a Ralph packet;
- launch a `fixer` child worker;
- inspect and reconcile output;
- record structural evidence;
- run critique with required profiles;
- feed critique back through fixes or Ralph if necessary;
- record retrospective / promotion disposition;
- commit and push before continuing.

# Strategy Snapshot

The corpus is strong and runtime-safe. The improvement frontier is clarity,
copy-safety, anti-overclaiming, and preventing support surfaces from becoming a
second ledger.

# Workstreams

- Core worldview and trust: `ticket:bootinv1`, `ticket:trustbd2`.
- Vocabulary and templates: `ticket:vocabx08`, `ticket:tplsave3`.
- Execution and verification mechanics: `ticket:pktfam04`, `ticket:evhard05`,
  `ticket:reconchk`.
- Ergonomics and workflow boundaries: `ticket:localed7`, `ticket:queryrc9`,
  `ticket:drives10`, `ticket:shipacc1`.
- Third-pass precision follow-ups: `ticket:rready12`, `ticket:drvcont13`,
  `ticket:wikiret14`, `ticket:wroute15`, `ticket:phvalid16`, `ticket:bootdoc17`,
  `ticket:rsrcmt18`, `ticket:pktws19`, `ticket:ralphg20`, `ticket:pktorph21`,
  `ticket:askpost22`, `ticket:readwsh23`, `ticket:doctitl24`, `ticket:netgate25`,
  `ticket:gitstat26`, `ticket:retmem27`, `ticket:critph28`, and
  `ticket:readrte29`.

# Milestones

- M1: Initiative, research, plan, and tickets created.
- M2: Bootstrap, trust, and vocabulary foundations closed.
- M3: Template, packet, evidence, and Ralph reconciliation surfaces closed.
- M4: Local edit, query, drive/support, and ship/acceptance boundaries closed.
- M5: Third-pass precision follow-up tickets closed.
- M6: Parent initiative accepted.

# Sequencing

`ticket:bootinv1` comes first because bootstrap is the first doctrine a cold model
sees. Keep it minimal: no internal framing, no marketing, no product strategy.

`ticket:trustbd2` follows because trust boundaries constrain evidence, research,
memory, and command snippets.

`ticket:vocabx08` precedes template and workflow edits so copied examples cite
canonical vocabulary rather than duplicating drift.

`ticket:tplsave3` then reduces template-retained ceremony. `ticket:pktfam04`,
`ticket:evhard05`, and `ticket:reconchk` tighten packet, evidence, and parent
execution mechanics.

`ticket:localed7` and `ticket:queryrc9` improve ergonomics without adding a new
skill or hidden runtime. `ticket:drives10` and `ticket:shipacc1` finish by
protecting workflow boundaries.

The third-pass audit follow-ups run after `ticket:shipacc1` so the original pass
can finish its ship/acceptance boundary before widening the queue. Their order
follows the audit's patch order, then secondary non-description polish items:
route readiness, drive route priorities, workspace routing, placeholder hygiene,
copy safety, research sources, packet write scope, Ralph launch gates, orphan
packet repair, ask-user posture, README support metadata, workspace doctor labels,
network and Git provenance hardening, retrospective memory read order, critique
packet placeholder safety, and README route-table framing.

# Claim / Acceptance Coverage

| Source claim / acceptance ID | Downstream ticket | Coverage expectation | Evidence / critique route | Notes |
| --- | --- | --- | --- | --- |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-001` | `ticket:bootinv1` | Minimal bootstrap orientation | Structural evidence plus critique | Do not leak internal framing |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-002` | `ticket:trustbd2` | Trust-boundary doctrine | Structural evidence plus critique | Doctrine-only, no tooling |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-003` | `ticket:vocabx08` | Vocabulary consolidation | Structural evidence plus critique | No runtime enum |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-004` | `ticket:tplsave3` | Save-ready template rules | Structural evidence plus critique | Avoid over-pruning gates |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-005` | `ticket:pktfam04` | Packet-family boundaries | Structural evidence plus critique | Ralph remains strict |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-006` | `ticket:evhard05` | Evidence anti-theater | Structural evidence plus critique | Evidence does not accept |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-007` | `ticket:reconchk` | Parent reconciliation and stale packet recovery | Structural evidence plus critique | No new reconciliation record |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-008` | `ticket:localed7` | Cheap local edit route | Structural evidence plus critique | No bypass mode |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-009` | `ticket:queryrc9` | Markdown-native query recipes | Structural evidence plus critique | No generated index or CLI |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-010` | `ticket:drives10` | Drive/support boundary tightening | Structural evidence plus critique | No `.loom/drive/` |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-011` | `ticket:shipacc1` | Acceptance-review versus ship separation | Structural evidence plus critique | Ship does not close tickets |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-012` | all tickets | Each child closes with evidence, critique, retrospective, commit, and push | Ticket-owned acceptance | Parent plan verifies at closure |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-013` | `ticket:rready12` | Route-complete ticket readiness guidance | Structural evidence plus critique | No new route tokens |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-014` | `ticket:drvcont13` | Drive `continue` priority | Structural evidence plus critique | Continue is route token, not Ralph outcome |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-015` | `ticket:wikiret14` | Split wiki and retrospective route-priority rows | Structural evidence plus critique | Adjacent but distinct routes |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-016` | `ticket:wroute15` | Workspace route token / owner row normalization | Structural evidence plus critique | Memory remains support-only |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-017` | `ticket:phvalid16` | Saved-record placeholder validation | Structural evidence plus critique | Templates may keep placeholders |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-018` | `ticket:bootdoc17` | Copy-safe bootstrap here-doc example | Structural evidence plus critique | Bootstrap stays concise |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-019` | `ticket:rsrcmt18` | Research source metadata template fields | Structural evidence plus critique | Research does not make sources truth |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-020` | `ticket:pktws19` | Fail-closed packet child write scope | Structural evidence plus critique | No ambiguous empty write scope |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-021` | `ticket:ralphg20` | Ralph launch hard gates | Structural evidence plus critique | Prevent unauthorized packets |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-022` | `ticket:pktorph21` | Orphan packet repair by packet family | Structural evidence plus critique | Ralph/critique/wiki split preserved |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-023` | `ticket:askpost22` | Problem-shaping ask-user posture | Structural evidence plus critique | No unsafe ambiguity decisions |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-024` | `ticket:readwsh23` | README workspace/harness support metadata note | Structural evidence plus critique | README framing only |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-025` | `ticket:doctitl24` | Workspace doctor presence-check label | Structural evidence plus critique | Do not call support paths canonical |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-026` | `ticket:netgate25` | Network unknown launch gate | Structural evidence plus critique | Unknown allowed only with blocker rationale |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-027` | `ticket:gitstat26` | Machine-readable dirty Git state | Structural evidence plus critique | Preserve human detail too |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-028` | `ticket:retmem27` | Retrospective memory read-order cue | Structural evidence plus critique | Memory remains support recall |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-029` | `ticket:critph28` | Critique packet placeholder quoting | Structural evidence plus critique | Template safety only |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-030` | `ticket:readrte29` | README route table introductory framing | Structural evidence plus critique | Route vocabulary remains canonical |

# Execution Waves

Sequential only. The tickets touch overlapping doctrine, templates, and workflow
references, so parallel Ralph would create unnecessary write-scope risk.

Wave readiness table:

| Wave | Tickets | Independent because | Expected `child_write_scope` / write scope overlap check | Dependency / shared-state check | Parent reconciliation |
| --- | --- | --- | --- | --- | --- |
| No wave | Sequential tickets | Dependencies and overlapping guidance favor order | Child write scopes may overlap across tickets; run one at a time | No generated files, lockfiles, migrations, or stateful resources | Ticket-owned update plus evidence/critique route |

# Risks

- Bootstrap can become over-explanatory; restrict to orientation needed before any
  other Loom token.
- Trust guidance can sound like a scanner requirement; keep it as agent behavior.
- Template pruning can create under-specified tickets if acceptance and critique
  gates disappear.
- Packet-family separation can make critique/wiki packets too vague if shared
  support metadata is under-specified.
- Query recipes can appear normative for every harness; frame as ordinary-tool
  examples.

# Evidence Strategy

Each ticket should record:

- `git diff --check` including new files with intent-to-add when needed;
- targeted `rg` queries for the ticket-specific wording;
- manual comparison against owner skill references/templates;
- confirmation that no runtime/CLI/schema/new-owner layer was introduced.

# Plan Readiness Review

Claim coverage: all initiative objectives are mapped to downstream tickets.

Spec / acceptance coverage: no separate spec is needed. The pass changes
protocol/operator guidance and uses initiative objectives plus ticket-local
acceptance criteria.

Placeholder scan: each ticket should include targeted placeholder/search evidence
when templates are touched.

Ticket-sized slices: bounded tickets map directly to the original council
improvement opportunities and the validated third-pass follow-up findings.

Likely write scopes: each ticket is limited to the relevant skill references,
templates, and its Loom reconciliation records.

Parallel / wave independence: none; run sequentially.

Expected packet `child_write_scope` / write scope overlap check: each Ralph packet
must name exact files for that ticket. Do not launch overlapping packets.

Likely verification posture: observation-first structural validation for every
ticket.

Evidence and critique route: mandatory critique for every ticket by user
instruction; required profiles are named in each ticket.

Stop / loopback conditions: stop and ask only if a ticket would add runtime/new
owner-layer mechanics, leak internal product framing into bootstrap, or accept
material unresolved critique risk.

# Exit Criteria

- All plan tickets are closed with evidence, critique, and retrospective
  disposition.
- All medium/high critique findings are resolved, accepted as risk with ticket
  provenance, superseded, or converted into follow-up tickets before closure.
- No runtime, hidden helper, CLI, schema engine, DB, daemon, MCP dependency, or new
  canonical owner layer is introduced.
- Final commit for each ticket is pushed.

# Completion Basis

When `status: completed`, cite child tickets, evidence records, critique records,
semantic commits, pushes, retrospective dispositions, residual risks, and any
follow-up tickets.
