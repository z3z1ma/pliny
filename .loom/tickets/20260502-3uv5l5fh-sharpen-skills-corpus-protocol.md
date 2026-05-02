---
id: ticket:3uv5l5fh
kind: ticket
status: ready
change_class: protocol-authority
risk_class: high
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
  plan:
    - plan:skills-corpus-protocol-sharpening
external_refs: {}
depends_on: []
---

# Summary

Execute the first comprehensive council-driven sharpening pass over Loom's
`skills/` corpus and directly related public framing so the shipped Markdown
protocol teaches Loom with stronger consistency, grammar, routing safety,
operator ergonomics, and validation discipline.

This ticket owns the live execution state for the first pass. The tied plan owns
sequencing. Research owns the reusable council synthesis. Evidence owns the
observed council output and later validation artifacts. Critique will own the
mandatory adversarial review before acceptance.

# Context

The user asked for an adversarial council review of `skills/` because the entire
corpus should approach exceptional precision in defining and instructing on Loom.
The council reviewed README context and the skill package and concluded that the
corpus is already strong, but the next improvement frontier is protocol
sharpening: eliminate drift, complete shared grammar, make cold-start recovery
first-class, reduce duplication, and make fresh agents less likely to mis-route
or invent shadow truth.

The active constitutional and roadmap frame already supports this direction:

- `constitution:main` says the product surface is `skills/`, Loom is a
  Markdown-native source-of-truth type system plus transaction protocol, tickets
  are the live ledger, and new workflows should route through existing owners.
- `roadmap:bootstrap-the-markdown-first-protocol-corpus` says the next phase is
  protocol sharpening rather than platform expansion.
- `research:skills-corpus-council-review` preserves the council findings as
  reusable research.
- `plan:skills-corpus-protocol-sharpening` sequences the work into staged waves.

# Why Now

The repo has moved past merely having the right files. It now needs the shipped
skills corpus, README-level framing, templates, references, and dogfood records to
read like one coherent operating manual. The council found that most gaps are not
fundamental architecture gaps; they are precision gaps that matter because Loom's
users are disposable agent contexts entering cold.

If this ticket is not done, future agents may still succeed by inference, but
that misses Loom's product promise: the repository itself should teach what truth
belongs where, what route comes next, what evidence is needed, and what not to
let become a second ledger.

# Scope

## A. Planning And Durable Context

- Preserve the council output as evidence and research before implementation.
- Keep this ticket tied to `plan:skills-corpus-protocol-sharpening`.
- Keep the strategic outcome tied to
  `initiative:skills-corpus-protocol-sharpening` and the active roadmap.
- If implementation discovers a finding is incorrect or stale, update the
  research or ticket rather than silently ignoring it.

## B. Low-Risk Public And Routing Alignment

- Add `loom-drive` wherever the product enumerates shipped workflow skills and it
  is currently missing.
- Check and update at least:
  - `README.md` skill map and shipped-skill descriptions,
  - `PROTOCOL.md` workflow examples or skill-route summaries when they enumerate
    workflow skills,
  - `ARCHITECTURE.md` if it lists the workflow skill surface,
  - `skills/loom-bootstrap/**` route summaries if they need a drive route.
- Reconcile README's outer-loop diagram so it does not imply a single linear
  sequence of `research -> spec -> plan -> ticket -> evidence -> critique -> wiki
  -> memory` when bootstrap doctrine teaches `constitution -> initiative -> plan
  -> ticket` as the backbone with research/spec as conditional strengthening
  layers and evidence/critique/wiki/memory as routed follow-through.
- Replace or qualify wording that makes packet and memory sound like canonical
  project-truth layers rather than durable/support surfaces.
- Preserve README's product clarity without letting README outrank bootstrap
  doctrine.

## C. Shared Coverage, Record, And Link Grammar

- Update `skills/loom-records/references/claim-coverage.md` to teach `OBJ-*`
  objective coverage if the corpus continues using initiative objective IDs.
- Decide and document whether cross-record objective references should be written
  as `initiative:skills-corpus-protocol-sharpening#OBJ-001`, as
  `initiative:skills-corpus-protocol-sharpening` `OBJ-001`, or both during a
  transition.
- Update `skills/loom-initiatives/**` as needed so initiative objective criteria
  are explicitly owned there while tickets own in-scope coverage and closure
  disposition.
- Add a canonical or current-supported `kind:` / ID / path table to
  `loom-records`, covering at least constitution, decision, roadmap, initiative,
  research, spec, plan, ticket, evidence, critique, wiki, packet, workspace, and
  workspace-support forms if they remain in use.
- Clarify the memory frontmatter/status exception if memory records intentionally
  differ from canonical record frontmatter expectations.
- Clarify semantic link usage for relationships such as `superseded_by`,
  `promoted_to`, follow-up tickets, accepted risk, and external references.
- Update validation guidance so future agents can check the new grammar with
  ordinary grep/rg queries.

## D. Packet, Handoff, And Scope Grammar

- Normalize packet ID families and naming guidance for Ralph, critique, and wiki
  packets, not only Ralph packets.
- Add or point to packet terminal statuses `consumed`, `superseded`, and
  `abandoned` in the surfaces where packet users are most likely to look,
  including `skills/loom-ralph/SKILL.md` if needed.
- Clarify whether critique and wiki packets use `verification_posture`, another
  posture field, or domain-specific review/synthesis expectations.
- Resolve `write_scope` versus `child_write_scope` drift, especially in drive
  handoff templates and packet guidance.
- Decide whether `skills/loom-drive/templates/outer-loop-handoff.md` is a durable
  packet-like support artifact, a transient handoff note, or something that needs
  frontmatter. Record the decision in the relevant owner surface.
- Add guidance for rejected, corrupted, or overscoped Ralph iterations: how the
  parent should update the ticket, evidence, packet status, and follow-up route.

## E. Ticket Risk, Change Class, Acceptance, And Follow-Up Grammar

- Decide whether `change_class` and `risk_class` are required for every ticket or
  required when they affect evidence, critique, or packet posture.
- Preserve the council-recommended direction unless implementation finds a better
  local fit: strict for tickets, flexible or narrowing for packets.
- Remove or explain duplication between frontmatter `risk_class` and the body
  `# Critique Disposition` risk class.
- Clarify critique finding disposition grammar:
  - resolved,
  - accepted as risk,
  - deferred with rationale when allowed,
  - converted into a linked follow-up ticket.
- Ensure ticket acceptance gate guidance still fails closed over unresolved
  required critique and missing evidence.

## F. Cold-Start, Resume, Compaction, And Workspace Entry

- Add first-class workspace-entry guidance for cold-start and post-compaction
  recovery.
- The guidance should teach a fresh agent to:
  - load bootstrap doctrine,
  - read `constitution:main`,
  - inspect active tickets with a query shaped like `rg -n 'status:
    (active|blocked|review_required|complete_pending_acceptance)' .loom/tickets`,
  - follow the active ticket's upstream initiative/research/spec/plan chain,
  - read linked evidence and critique before claiming progress,
  - continue from owner records rather than chat memory.
- Add pre-compaction checkpoint guidance where it belongs, likely workspace,
  tickets, memory, or drive, without creating a second ledger.
- Keep resume guidance fail-closed: if active owner records conflict, reconcile the
  owning layer instead of guessing from transcript context.

## G. Scratchpad, External Reference, And Concurrency Ergonomics

- Add an explicit anti-pattern warning against generic `scratch.md`, `notes.md`,
  and junk-drawer files.
- Route scratchpad-like content precisely:
  - observations and validation output to evidence,
  - hypotheses, rejected options, and null results to research,
  - live execution state to tickets,
  - accepted explanations to wiki,
  - support-only retrieval cues, preferences, reminders, and hot context to
    memory.
- Expand external-reference lifecycle guidance so GitHub, Jira, Linear, PRs,
  URLs, dashboards, or generated context files can mirror or package Loom work
  without owning Loom truth.
- Add lightweight concurrent-edit safety for file-first work:
  - re-read before writing when another actor may have touched a file,
  - fail closed on conflicting edits,
  - do not revert unrelated user or agent changes,
  - reconcile stale records instead of assuming the latest prose wins.

## H. Memory Boundary, Pruning, And Frontmatter Expectations

- Clarify when memory can be pruned, promoted, linked, or left stale.
- Tie memory pruning or promotion to ticket closure or retrospective when that is
  the least surprising route.
- Clarify whether memory records require full common frontmatter or may remain a
  lighter support recall surface.
- Ensure memory guidance keeps optionality as a correctness boundary: absent or
  stale memory cannot make canonical project truth false.

## I. Owner-Surface Consolidation

- Make atlas page shape canonical in the wiki surface, then adjust codemap to
  point to that owner shape instead of duplicating full atlas doctrine.
- Move or point retrospective mechanics to `loom-retrospective`, while keeping
  `loom-records` focused on shared grammar and link/status validation.
- Let `loom-research` define spike/sketch as research variants at a high level;
  let `loom-spike` own the detailed spike/sketch workflow.
- Tighten `loom-skill-authoring` metadata guidance for `skill_kind`,
  `compatibility`, activation descriptions, and skill frontmatter expectations.
- Avoid deleting nuance until the chosen owner surface contains an equivalent or
  better instruction.

## J. Skill-By-Skill Review Actions

- `loom-bootstrap`: add `loom-drive` routing if missing; keep local-work nuance
  close to mandatory doctrine; avoid making README or packets outrank bootstrap.
- `loom-workspace`: add cold-start/post-compaction resume guidance and active
  ticket discovery route.
- `loom-records`: add objective coverage, `kind:`/ID/path enumeration, packet
  family IDs, semantic link clarity, memory exception, and validation queries.
- `loom-constitution`: no major change expected; inspect only for conflicts with
  proposed protocol-authority changes.
- `loom-initiatives`: clarify objective criteria and coverage ownership if
  `OBJ-*` grammar is added.
- `loom-research`: reduce spike/sketch duplication and point to workflow owner
  where appropriate.
- `loom-specs`: inspect for consistency with updated coverage grammar; no major
  change expected.
- `loom-plans`: inspect sequencing/readiness language against plan waves and
  drive/resume routes; no broad rewrite expected.
- `loom-tickets`: resolve risk/change class strictness, critique disposition,
  finding-to-follow-up grammar, and acceptance gate wording.
- `loom-evidence`: add or point to freshness/recheck guidance if currently too
  thin.
- `loom-critique`: clarify critique packet source, review profiles, and finding
  disposition expectations.
- `loom-wiki`: make atlas template or reference the canonical atlas owner shape.
- `loom-memory`: clarify pruning, promotion, optionality, and frontmatter/status
  expectations.
- `loom-ralph`: add packet terminal status visibility and rejected/overscoped
  iteration route if missing.
- `loom-git`: inspect for file-first concurrency, re-read, and provenance wording;
  minor cleanup only if needed.
- `loom-debugging`: inspect for evidence/research/spec/ticket route consistency;
  no major change expected.
- `loom-spike`: consolidate detailed spike/sketch procedure ownership here.
- `loom-codemap`: point atlas shape to wiki owner surface and preserve codemap's
  evidence/research/wiki route.
- `loom-ship`: inspect external-reference, PR, release, handoff, and follow-up
  packaging language; no closure authority drift.
- `loom-retrospective`: centralize retrospective mechanics and promotion routing.
- `loom-skill-authoring`: define or intentionally leave open metadata vocabulary.
- `loom-drive`: surface in public maps, consider moving long procedure out of
  `SKILL.md` into references, clarify handoff template status, and keep it a
  coordinator rather than a truth owner.

## K. Validation, Evidence, Critique, And Reconciliation

- Run structural validation queries before claiming the ticket is ready for
  acceptance.
- Record a new evidence artifact for the final implementation diff.
- Run mandatory critique before acceptance using at least:
  - `protocol-change`,
  - `operator-clarity`,
  - `records-grammar`,
  - `routing-safety`.
- Resolve critique findings in the product surface, accept them explicitly as
  ticket-owned risk, or convert them into linked follow-up tickets.
- Update this ticket's claim matrix, evidence section, critique disposition, wiki
  disposition, and journal before moving to `complete_pending_acceptance` or
  `closed`.

# Non-goals

- Do not add a required Loom runtime, CLI, background worker, database, dashboard,
  MCP server, telemetry channel, or model router.
- Do not create a new canonical Loom layer for drive, resume, handoffs,
  retrospectives, external references, scratch notes, or compaction checkpoints.
- Do not use this ticket to rewrite every sentence for style if the wording is
  already accurate and not causing routing, grammar, or validation ambiguity.
- Do not update internal examples unless the implementation makes a specific
  fixture stale enough to block truthful review; create follow-up work if example
  reconciliation is broad.
- Do not treat council findings as automatically true after implementation begins;
  revalidate against current files.
- Do not close this ticket without fresh structural evidence and mandatory
  critique disposition.
- Do not let top-level docs redefine product behavior independently from
  `skills/` and bootstrap doctrine.
- Do not make memory, packets, external systems, or generated context files own
  live execution state.

# Acceptance Criteria

- ACC-001: `loom-drive` is visible anywhere the product enumerates shipped Loom
  workflow skills, and its role is described as a workflow coordinator rather than
  a truth owner.
- ACC-002: README and any touched top-level framing accurately distinguish the
  Loom backbone, conditional research/spec routes, evidence/critique/wiki
  follow-through, packet support surface, and memory support surface.
- ACC-003: `loom-records` teaches the shared grammar needed by the corpus for
  `OBJ-*` objective criteria, valid/current `kind:` values, canonical ID/path
  families, semantic links, and external references.
- ACC-004: Packet and handoff guidance consistently covers Ralph, critique, wiki,
  and drive-adjacent handoffs without creating a new truth layer or preserving
  unexplained `write_scope` / `child_write_scope` drift.
- ACC-005: Ticket `change_class`, `risk_class`, critique policy, finding
  disposition, and acceptance-gate rules are explicit enough that a fresh agent
  can select evidence and critique posture without guessing.
- ACC-006: Workspace/resume guidance teaches cold-start recovery, post-compaction
  recovery, active ticket discovery, upstream-chain reading, and owner-record
  continuation from `.loom/` rather than transcript memory.
- ACC-007: Operator guidance explicitly routes scratchpad-like content,
  external-reference mirrors, concurrent edits, stale records, memory pruning,
  and rejected Ralph results to the correct owner layers.
- ACC-008: Duplicated atlas, retrospective, spike/sketch, packet, and metadata
  doctrine is either consolidated under the proper owner skill or intentionally
  left duplicated with a clear reason.
- ACC-009: Every skill directory in `skills/` has been reviewed against the
  council notes, with either a targeted edit or a deliberate no-change rationale
  recorded in this ticket or its evidence.
- ACC-010: Structural validation evidence records the final diff shape, grep/rg
  checks, source-leakage checks, and manual comparison against this ticket's
  acceptance criteria.
- ACC-011: Mandatory critique is complete, and all medium/high findings are
  resolved, explicitly accepted as risk in this ticket, or converted into linked
  follow-up tickets.
- ACC-012: Wiki and retrospective disposition are truthful: durable accepted
  explanations are promoted if needed, or explicitly deferred with rationale.

# Coverage

Covers:

- `initiative:skills-corpus-protocol-sharpening` OBJ-001
- `initiative:skills-corpus-protocol-sharpening` OBJ-002
- `initiative:skills-corpus-protocol-sharpening` OBJ-003
- `initiative:skills-corpus-protocol-sharpening` OBJ-004
- `initiative:skills-corpus-protocol-sharpening` OBJ-005
- `research:skills-corpus-council-review#CLAIM-001`
- `research:skills-corpus-council-review#CLAIM-002`
- `research:skills-corpus-council-review#CLAIM-003`
- `research:skills-corpus-council-review#CLAIM-004`
- `research:skills-corpus-council-review#CLAIM-005`
- `research:skills-corpus-council-review#CLAIM-006`
- `research:skills-corpus-council-review#CLAIM-007`
- `research:skills-corpus-council-review#CLAIM-008`
- `research:skills-corpus-council-review#CLAIM-009`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-protocol-sharpening` OBJ-001 | `evidence:skills-corpus-council-review` supports need; implementation evidence pending | mandatory critique pending | open |
| `initiative:skills-corpus-protocol-sharpening` OBJ-002 | `evidence:skills-corpus-council-review` supports need; implementation evidence pending | mandatory critique pending | open |
| `initiative:skills-corpus-protocol-sharpening` OBJ-003 | `evidence:skills-corpus-council-review` supports need; implementation evidence pending | mandatory critique pending | open |
| `initiative:skills-corpus-protocol-sharpening` OBJ-004 | `evidence:skills-corpus-council-review` supports need; implementation evidence pending | mandatory critique pending | open |
| `initiative:skills-corpus-protocol-sharpening` OBJ-005 | `evidence:skills-corpus-council-review` supports critique requirement; implementation evidence pending | mandatory critique pending | open |
| `research:skills-corpus-council-review#CLAIM-001` | `evidence:skills-corpus-council-review` | mandatory critique pending | supported_pending_review |
| `research:skills-corpus-council-review#CLAIM-002` | `evidence:skills-corpus-council-review` | mandatory critique pending | supported_pending_review |
| `research:skills-corpus-council-review#CLAIM-003` | `evidence:skills-corpus-council-review` | mandatory critique pending | supported_pending_review |
| `research:skills-corpus-council-review#CLAIM-004` | `evidence:skills-corpus-council-review` | mandatory critique pending | supported_pending_review |
| `research:skills-corpus-council-review#CLAIM-005` | `evidence:skills-corpus-council-review` | mandatory critique pending | supported_pending_review |
| `research:skills-corpus-council-review#CLAIM-006` | `evidence:skills-corpus-council-review` | mandatory critique pending | supported_pending_review |
| `research:skills-corpus-council-review#CLAIM-007` | `evidence:skills-corpus-council-review` | mandatory critique pending | supported_pending_review |
| `research:skills-corpus-council-review#CLAIM-008` | `evidence:skills-corpus-council-review` | mandatory critique pending | supported_pending_review |
| `research:skills-corpus-council-review#CLAIM-009` | `evidence:skills-corpus-council-review` | mandatory critique pending | supported_pending_review |

# Execution Notes

This ticket is intentionally detailed before implementation begins. It should be
used as the acceptance dossier for the first comprehensive pass, not as a hidden
project plan. The sequencing owner is `plan:skills-corpus-protocol-sharpening`.

Implementation guidance:

- Prefer small, targeted edits over broad rewrites.
- Read the owner skill and relevant references before editing a skill surface.
- Revalidate council claims against current files before changing text.
- If two correct edits are possible, choose the one that adds less ontology,
  fewer terms, and fewer new requirements.
- Keep `skills/` self-contained and use generic `.loom/...` paths.
- Keep top-level docs aligned with `skills/`, but do not make top-level docs the
  source of protocol authority.
- When a proposed edit changes authority, routing, acceptance, packet contracts,
  or truth ownership, treat it as protocol-authority work and preserve the reason
  in evidence or critique.
- If a workstream becomes too large, create a linked follow-up ticket rather than
  hiding incomplete work inside this ticket.

Suggested implementation order:

1. Run baseline grep queries to confirm the council findings in the current tree.
2. Apply low-risk public alignment edits.
3. Apply shared grammar edits.
4. Apply operator ergonomics edits.
5. Apply owner-surface consolidation edits.
6. Review every skill directory against the skill-by-skill checklist.
7. Run structural validation queries.
8. Record implementation evidence.
9. Run mandatory critique.
10. Fix critique findings or create follow-up tickets.
11. Reconcile this ticket and the linked initiative/plan status summaries.

# Blockers

None. The ticket is ready for a governed implementation pass or pre-implementation
critique. Implementation should not start until the operator accepts this planning
package or explicitly asks to proceed.

# Next Move / Next Route

Pause for operator review of the new Loom records. After approval, begin the
implementation pass from `plan:skills-corpus-protocol-sharpening`, starting with
baseline validation queries and the low-risk alignment wave.

Because this is high-risk protocol-authority work, mandatory critique is required
before acceptance even if the implementation appears structurally clean.

# Ralph Readiness

This ticket is not Ralph-ready as one single child iteration because it spans
multiple protocol surfaces and risk classes. If a fresh worker is used, compile
one Ralph packet per wave or per tightly bounded subset.

Bounded iteration:

- Candidate iteration 1: low-risk public and routing alignment.
- Candidate iteration 2: shared record grammar hardening.
- Candidate iteration 3: workspace/operator ergonomics.
- Candidate iteration 4: owner-surface consolidation.
- Candidate iteration 5: validation evidence and critique reconciliation.

Write boundary:

- Use the wave-specific write scopes in `plan:skills-corpus-protocol-sharpening`.
- Do not let a child edit outside the declared wave without returning to the
  parent for packet or ticket refinement.

Likely verification posture:

- Observation-first structural validation for implementation waves.
- Mandatory critique for acceptance.

Expected output contract:

- changed files,
- validation commands and outputs,
- unresolved ambiguities,
- evidence update recommendation,
- critique readiness recommendation,
- follow-up ticket recommendations if scope splits.

# Evidence

Existing evidence:

- `evidence:skills-corpus-council-review` records the observed council review that
  motivated this ticket and supports the research claims.

Expected implementation evidence:

- a new evidence record after edits, tentatively named
  `evidence:skills-corpus-protocol-sharpening-validation`, containing diff shape,
  structural checks, targeted grep/rg outputs, source-leakage checks, and manual
  acceptance comparison.

Minimum validation query set:

```bash
rg -n '`loom-[a-z-]+`' README.md PROTOCOL.md ARCHITECTURE.md
rg -n 'OBJ-[0-9]{3}|REQ-[0-9]{3}|ACC-[0-9]{3}|CLAIM-[0-9]{3}' skills
rg -n 'packet:(ralph|critique|wiki)|packet_kind|verification_posture|child_write_scope|write_scope' skills
rg -h '^kind: ' skills | sort -u
rg -h '^status: ' skills | sort -u
rg -h '^skill_kind:|^compatibility:' skills | sort -u
rg -n 'change_class|risk_class' skills
find skills -type d -empty
rg -n 'agent-loom|/Users/|\.opencode|examples/|optional-utilities' skills
```

Additional checks expected before acceptance:

- `git diff --check`
- `git diff --stat`
- manual diff review of all touched `skills/**` files
- targeted searches for removed or replaced duplicate doctrine
- targeted searches for stale `loom-drive` omissions after public alignment

# Critique Disposition

Risk class: high

Critique policy: mandatory

Policy rationale:

This ticket changes protocol authority, record grammar, operator routing, packet
contracts, critique/acceptance behavior, and the instructional shape of the
shipped product surface. The diff may be mostly Markdown, but the behavior being
taught is Loom behavior.

Required critique profiles:

- protocol-change
- operator-clarity
- records-grammar
- routing-safety

Findings:

None - no critique has run yet.

Disposition status: pending

Deferral / not-required rationale:

None. Critique is mandatory before acceptance.

# Wiki Disposition

Pending. If implementation produces durable accepted explanation about
cold-start resume, packet grammar, objective coverage, or corpus maintenance that
future agents should consult independently of the skill text, promote it through
wiki or retrospective. If the accepted understanding is fully captured in skills
and references, record a deferral rationale before closure.

# Acceptance Decision

Accepted by:

Accepted at:

Basis:

Residual risks:

# Dependencies

No hard upstream ticket dependencies.

Governed by:

- `constitution:main`
- `roadmap:bootstrap-the-markdown-first-protocol-corpus`
- `initiative:skills-corpus-protocol-sharpening`
- `research:skills-corpus-council-review`
- `plan:skills-corpus-protocol-sharpening`

# Journal

- 2026-05-02T07:58:42Z: Created from the council review requested by the user.
  Implementation has not started. The ticket is ready for operator review and a
  staged protocol-authority implementation pass tied to
  `plan:skills-corpus-protocol-sharpening`.
