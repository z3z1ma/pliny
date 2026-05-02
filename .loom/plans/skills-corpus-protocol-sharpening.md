---
id: plan:skills-corpus-protocol-sharpening
kind: plan
status: active
created_at: 2026-05-02T07:58:42Z
updated_at: 2026-05-02T07:58:42Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  roadmap:
    - roadmap:bootstrap-the-markdown-first-protocol-corpus
  initiative:
    - initiative:skills-corpus-protocol-sharpening
  research:
    - research:skills-corpus-council-review
  evidence:
    - evidence:skills-corpus-council-review
  ticket:
    - ticket:3uv5l5fh
---

# Purpose

Sequence the council-driven sharpening of Loom's `skills/` corpus so improvements
land in a safe order: first align obvious drift, then tighten shared grammar, then
improve operator routes, then consolidate duplicated doctrine, then validate and
critique before acceptance.

# Strategy

Treat the work as high-risk protocol-authority maintenance over a Markdown-native
product surface.

The route is:

1. preserve the council findings as evidence and research,
2. align public framing with existing shipped skills,
3. update shared grammar before downstream skills depend on it,
4. update workflow skills and references that teach operators what to do,
5. consolidate duplicated doctrine under the correct owner skill,
6. run structural validation queries and diff review,
7. run mandatory critique before ticket acceptance,
8. convert unresolved medium/high findings into follow-up tickets or accepted
   risks.

The plan deliberately avoids adding a runtime, command surface, database, or new
canonical layer. It sharpens visible Markdown instructions and templates.

# Strategy Snapshot

The upstream council consensus is that Loom is already strong. The immediate
failure risk is not missing architecture; it is cross-surface drift and
under-specified grammar that can make fresh agents infer behavior instead of
recovering it from owner records.

This plan serves `initiative:skills-corpus-protocol-sharpening` and drives
`ticket:3uv5l5fh` as the first comprehensive pass. The ticket may split later
follow-ups if implementation proves too broad, but live execution truth remains
with the ticket and any explicitly created child tickets.

# Workstreams

Public framing alignment:

- Add `loom-drive` to skill maps and shipped-skill summaries where omitted.
- Reconcile README's outer-loop explanation with bootstrap doctrine.
- Replace misleading canonical-layer wording with owner-layer/support-surface
  wording where packet or memory would otherwise appear canonical.

Shared record grammar:

- Add or clarify `OBJ-*` objective coverage and its qualified reference shape.
- Enumerate valid or currently supported `kind:` values and canonical ID/path
  forms.
- Normalize packet family IDs, terminal statuses, critique/wiki packet guidance,
  and handoff terminology.
- Resolve ticket `change_class` and `risk_class` strictness.
- Clarify semantic links such as `superseded_by`, `promoted_to`, and follow-up
  relationships.
- Tighten external-reference provenance and lifecycle guidance.

Operator ergonomics:

- Add cold-start and post-compaction resume guidance to workspace entry and
  summarize it in bootstrap or README only where necessary.
- Teach pre-compaction checkpoints without making memory or handoff notes a
  second ledger.
- Ban generic scratchpads and route observations, hypotheses, execution state,
  and support recall to the correct owners.
- Add guidance for concurrent file-first edits, re-read-before-write discipline,
  stale records, and rejected or overscoped Ralph iterations.
- Clarify critique finding conversion into resolved, accepted risk, or linked
  follow-up ticket states.
- Clarify memory pruning cadence and frontmatter/status expectations.

Owner-surface consolidation:

- Make atlas page shape canonical in the wiki surface and have codemap point to
  it instead of duplicating the whole shape.
- Move or point retrospective mechanics to `loom-retrospective` rather than
  spreading them through shared records unnecessarily.
- Let research define spike/sketch as research variants while `loom-spike` owns
  procedural workflow detail.
- Tighten skill metadata conventions in `loom-skill-authoring`.

Validation and review:

- Run targeted grep/rg structural checks for skill maps, coverage IDs, packet
  grammar, frontmatter values, status values, risk/change class usage, metadata,
  empty directories, and source-repo leakage.
- Record validation evidence after product-surface edits.
- Run mandatory critique using protocol-change, operator-clarity, and
  records-grammar/routing-safety lenses before acceptance.

# Milestones

1. Planning records created and linked: initiative, research, evidence, plan, and
   ticket.
2. Low-risk drift corrected: `loom-drive` surfaced and README/public diagrams
   aligned with bootstrap doctrine.
3. Shared grammar hardened: coverage, kinds, IDs, packets, risk/change,
   semantic links, and external refs made coherent.
4. Operator routes strengthened: resume, compaction, scratchpads, concurrency,
   rejected Ralph, follow-up conversion, memory pruning, and evidence freshness
   taught without creating new ledgers.
5. Duplicated doctrine consolidated under owner skills with pointers from related
   skills.
6. Structural evidence recorded from targeted queries and diff review.
7. Mandatory critique completed, with findings resolved, accepted as risk, or
   converted into linked follow-up tickets.

# Sequencing

Start with low-risk alignment because it removes obvious user-facing drift and
does not depend on deeper grammar changes. Then update shared grammar so later
skill edits can cite the right owner surface instead of inventing local variants.
After grammar is clear, update operator workflows. Consolidate duplication only
after the owner surface is explicit, so deletes and pointer edits do not remove
needed instructions. Validate and critique after the full diff is inspectable.

Loop back to research if implementation reveals that a council finding is wrong
or obsolete. Loop back to constitution only if a proposed improvement conflicts
with the no-runtime, skills-only, or owner-layer authority boundaries. Loop back
to tickets if the work becomes too broad for one acceptance dossier.

# Execution Waves

Wave 1:

- `ticket:3uv5l5fh` low-risk alignment pass. Expected write scope:
  `README.md`, `PROTOCOL.md`, `ARCHITECTURE.md` if needed,
  `skills/loom-bootstrap/**`, and skill-map/routing references that enumerate
  workflow skills. The pass should avoid record grammar changes except where
  necessary to keep references truthful.

Wave 2:

- `ticket:3uv5l5fh` shared grammar pass. Expected write scope:
  `skills/loom-records/**`, `skills/loom-tickets/**`, `skills/loom-initiatives/**`,
  packet-related references/templates, and small pointers from affected skills.
  This wave is high risk because it affects claim coverage, packet contracts, and
  acceptance posture.

Wave 3:

- `ticket:3uv5l5fh` operator ergonomics pass. Expected write scope:
  `skills/loom-workspace/**`, `skills/loom-bootstrap/**`, `skills/loom-drive/**`,
  `skills/loom-memory/**`, `skills/loom-ralph/**`, `skills/loom-critique/**`, and
  related references where the operator route is taught.

Wave 4:

- `ticket:3uv5l5fh` consolidation pass. Expected write scope:
  `skills/loom-wiki/**`, `skills/loom-codemap/**`, `skills/loom-retrospective/**`,
  `skills/loom-records/**`, `skills/loom-research/**`, `skills/loom-spike/**`, and
  `skills/loom-skill-authoring/**`.

Wave 5:

- `ticket:3uv5l5fh` validation, evidence, critique, and reconciliation. Expected
  write scope: `.loom/evidence/**`, `.loom/critique/**`, `.loom/tickets/**`, and
  any follow-up ticket records needed for unresolved findings. Product-surface
  edits should be frozen except for critique fixes.

# Risks

- The ticket may be too broad if all findings require deep edits. Mitigation:
  keep `ticket:3uv5l5fh` as the first comprehensive pass but split explicit
  follow-up tickets for work that cannot be accepted safely in this pass.
- README edits could make README appear more authoritative than bootstrap.
  Mitigation: frame README as product overview and keep bootstrap doctrine as the
  operating authority.
- Grammar edits could silently break existing records. Mitigation: use structural
  queries and explicit transition language for any changed reference shape.
- Resume and scratchpad guidance could become a new ledger. Mitigation: route live
  state to tickets, observations to evidence, synthesis to research/wiki, and
  recall to memory only when support-only.
- Consolidation deletes could remove useful domain nuance. Mitigation: replace
  duplicate detail with pointers only after the owner surface contains the needed
  instruction.

# Evidence Strategy

Use structural and review evidence rather than runtime tests, because this is a
Markdown protocol corpus.

Minimum evidence after implementation:

- `git diff --check`.
- `git diff --stat` and manual diff review of touched product surfaces.
- Targeted `rg` queries for `loom-drive` visibility in public maps.
- Targeted `rg` queries for `OBJ-*`, `REQ-*`, `ACC-*`, and `CLAIM-*` coverage
  grammar.
- Targeted `rg` queries for packet family fields and `write_scope` drift.
- Targeted `rg` queries for `kind:`, `status:`, `skill_kind:`, `compatibility:`,
  `change_class`, and `risk_class` values.
- Empty-directory check for `skills/` directories.
- Source-repo leakage check for `agent-loom`, absolute paths, `.opencode`,
  `examples/`, and `optional-utilities` inside shipped skills.
- Manual comparison against this plan and `ticket:3uv5l5fh` acceptance criteria.

# Plan Readiness Review

Spec / acceptance coverage:

No separate spec exists yet. `initiative:skills-corpus-protocol-sharpening` owns
strategic objective criteria; `ticket:3uv5l5fh` owns ticket-local acceptance for
the first implementation pass. If behavior contracts become reusable or disputed,
promote them into a spec before relying on them across multiple tickets.

Placeholder scan:

This plan intentionally contains no unresolved placeholder acceptance. Open
questions are recorded in `research:skills-corpus-council-review` and routed as
loopback conditions.

Ticket-sized slices:

The first ticket is broad but staged. If any wave cannot be reviewed in one
acceptance dossier, create follow-up tickets and update this plan rather than
expanding scope silently.

Likely write scopes:

- Public framing: `README.md`, `PROTOCOL.md`, `ARCHITECTURE.md`, possibly
  `INSTALL.md` or `AGENTS.md` only if direct drift is found.
- Product surface: `skills/**`.
- Loom execution records: `.loom/evidence/**`, `.loom/critique/**`,
  `.loom/tickets/**`, and follow-up records only as needed.

Likely verification posture:

Observation-first structural validation plus mandatory critique. No code runtime
tests are expected because the changed product is Markdown protocol guidance.

Evidence and critique route:

Evidence must be recorded after the product-surface diff exists. Critique is
mandatory before acceptance because the work changes protocol authority,
operator routing, record grammar, packet contracts, and closure behavior.

Stop / loopback conditions:

- Stop and ask the user if an edit would add a runtime, CLI, database, daemon,
  hidden helper, or new canonical owner layer.
- Loop back to research if a council finding cannot be verified in the current
  corpus.
- Loop back to ticket refinement if implementation needs multiple independently
  reviewable follow-up tickets.
- Loop back to constitution if a proposed change contradicts the anti-runtime,
  skills-only, owner-layer, or ticket-ledger boundaries.

# Exit Criteria

- `ticket:3uv5l5fh` has been accepted or has explicitly spawned follow-up tickets
  for residual work.
- The linked evidence records fresh structural validation from the final diff.
- Mandatory critique exists and all medium/high findings are resolved, accepted as
  risk, or converted into linked follow-up tickets.
- The initiative success metrics have a truthful status summary.
- Any wiki or retrospective promotion decision is recorded in the ticket.

# Completion Basis

When `status: completed`, cite `ticket:3uv5l5fh`, implementation evidence,
mandatory critique, and any follow-up tickets or accepted risks that explain why
the plan can stop.
