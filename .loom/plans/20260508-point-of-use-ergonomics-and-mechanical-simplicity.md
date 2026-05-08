---
id: plan:point-of-use-ergonomics-and-mechanical-simplicity
kind: plan
status: completed
created_at: 2026-05-08T07:32:35Z
updated_at: 2026-05-08T15:57:40Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  spec:
    - spec:point-of-use-ergonomics-and-mechanical-simplicity
  decision:
    - decision:0008
  roadmap:
    - roadmap:bootstrap-the-markdown-first-protocol-corpus
  ticket:
    - ticket:iq03bxg5
    - ticket:nlzaqhrm
    - ticket:58h4o1qo
    - ticket:xulgzs52
    - ticket:57rm2fmx
    - ticket:esszigx8
  evidence:
    - evidence:point-of-use-ergonomics-final-check
  critique:
    - critique:point-of-use-ergonomics-final-review
external_refs: {}
---

# Purpose

Decompose the point-of-use ergonomics pass into safe implementation slices:

- add lite core templates without weakening existing generic full template names
- compress `using-loom` without losing essential doctrine
- remove Markdown tables from product/docs surfaces
- validate and critique before moving toward examples or eval automation

# Strategy

Treat this as protocol-authority work with an ergonomics goal. The plan should
reduce ceremony where the user feels it, not weaken Loom's truth model.

The execution route is:

1. finish spec grilling for template shape, `using-loom` compression boundaries,
   and table replacement details
2. add explicit lite templates and update core skill guidance
3. compress `using-loom` against a word-count target and invariant checklist
4. rewrite Markdown tables in scoped product/docs surfaces to label-led bullets
5. update public/root docs only where they need to mention the new template or
   no-table convention
6. record evidence and run critique before accepting the pass

# Settled Constraints

- Existing `ticket.md`, `spec.md`, and `evidence.md` remain the canonical full
  copy targets.
- Lite templates still include YAML frontmatter.
- Lite templates are minimal ledgers, not frontmatter-free notes and not full gate
  worksheets.
- `ticket-lite.md` uses `# Summary`, `# Scope`, `# Acceptance`, `# Evidence`,
  `# Status / Next Move`, and `# Journal` after frontmatter.
- `spec-lite.md` uses `# Summary`, `# Problem`, `# Desired Behavior`,
  `# Requirements`, `# Scenarios`, `# Acceptance`, `# Evidence Plan`, and
  `# Open Questions` after frontmatter.
- `evidence-lite.md` uses `# Summary`, `# Observation`, `# Artifacts`,
  `# Supports / Challenges`, `# Limits`, and `# Related Records` after
  frontmatter.
- Full templates are required or escalation is required for high-risk,
  public/shared, multi-ticket, reusable-acceptance, migration/security/privacy,
  ambiguous, or mandatory-critique work.
- `using-loom` keeps the same ordered doctrine architecture and targets a 5,000 to
  6,000 word acceptance band.
- Table removal scope is `loom-core`, `loom-playbooks`, `README.md`,
  `PROTOCOL.md`, and `ARCHITECTURE.md`.
- Table replacement style defaults to label-led bullets.
- No new mechanical package checks or hidden validators are added in this pass.
- Root docs mention the lite/full template distinction briefly; detailed template
  selection guidance stays in owning core skills.
- Table rewrites preserve existing row content by default; deletion needs a
  duplicate/stale rationale in ticket or evidence notes.
- Evals/examples automation is deferred until this work is accepted.

# Workstreams

Spec grilling and record readiness:

- Resolve the remaining open questions in
  `spec:point-of-use-ergonomics-and-mechanical-simplicity`.
- No remaining plan-level grilling blockers before execution ticket creation.

Lite templates and full-compatible generics:

- Add `ticket-lite.md` under `loom-core/skills/loom-tickets/templates/`.
- Add `spec-lite.md` under `loom-core/skills/loom-specs/templates/`.
- Add `evidence-lite.md` under `loom-core/skills/loom-evidence/templates/`.
- Preserve full-template behavior for existing generic template names.
- Update skill read-order and creation guidance so agents know when to choose lite
  or full.

Compressed `using-loom`:

- Rewrite `loom-core/skills/using-loom/SKILL.md` and the eight ordered references
  for density.
- Remove duplicated explanations that are already owned by task-specific skills.
- Preserve the non-negotiables and owner-boundary doctrine from the current
  references.
- Measure word count before and after.

Product/docs table removal:

- Replace Markdown pipe tables in `loom-core` with label-led bullets or other
  non-table structures.
- Replace Markdown pipe tables in `loom-playbooks` with the same style.
- Replace Markdown pipe tables in `README.md`, `PROTOCOL.md`, and
  `ARCHITECTURE.md`.
- Leave dogfood `.loom` history and examples out of scope unless a later explicit
  ticket expands scope.

Evidence and critique:

- Record template inventory, frontmatter spot checks, word-count results,
  table-search results, and diff-scope review.
- Run critique with at least these lenses: point-of-use ergonomics, doctrine
  completeness, owner-layer safety, and mechanical verifiability.
- Convert unresolved medium/high findings into ticket-owned dispositions before
  closure.

# Candidate Ticket Slices

Ticket slice 1: finalize behavior contract and plan.

- Outcome: spec open questions resolved enough for execution tickets.
- Scope: `.loom/specs/point-of-use-ergonomics-and-mechanical-simplicity.md` and
  this plan.
- Evidence: record diff review and explicit operator decisions.
- Stop condition: template shape or doctrine compression target remains materially
  ambiguous.

Ticket slice 2: add lite templates and template-selection guidance.

- Outcome: three new lite templates exist; generic template names remain full copy
  targets; core skills teach full escalation triggers.
- Scope: `loom-core/skills/loom-tickets/**`, `loom-core/skills/loom-specs/**`,
  `loom-core/skills/loom-evidence/**`, and narrow links from `loom-records` only
  if needed.
- Evidence: template inventory, frontmatter spot checks, and diff review.
- Critique: recommended because this changes point-of-use record behavior.

Ticket slice 3: compress `using-loom` doctrine.

- Outcome: entry skill and ordered references are within the 5,000 to 6,000 word
  band while preserving essential invariants, or evidence records explicit
  rationale for an out-of-band result.
- Scope: `loom-core/skills/using-loom/**`.
- Evidence: before/after `wc -l -w`, invariant checklist, and diff review.
- Critique: mandatory because this changes always-on doctrine.

Ticket slice 4: remove tables from `loom-core`.

- Outcome: no scoped pipe tables remain in `loom-core`; templates and references
  use label-led bullets or clearer non-table structures.
- Scope: `loom-core/**/*.md`.
- Evidence: targeted `rg` table scan and diff review.
- Critique: recommended, mandatory if core doctrine or owner-boundary wording is
  materially changed beyond format.

Ticket slice 5: remove tables from `loom-playbooks`.

- Outcome: no scoped pipe tables remain in `loom-playbooks`; optional playbooks
  keep routing truth back to core owner layers.
- Scope: `loom-playbooks/**/*.md`.
- Evidence: targeted `rg` table scan and diff review.
- Critique: recommended because playbook examples can drift from core vocabulary.

Ticket slice 6: remove tables from root public docs and align public framing.

- Outcome: `README.md`, `PROTOCOL.md`, and `ARCHITECTURE.md` are table-free and
  briefly mention lite/full templates without contradicting split-package or
  no-runtime posture.
- Scope: root public Markdown docs only.
- Evidence: targeted table scan and source comparison against the spec.
- Critique: recommended for public-facing clarity.

Ticket slice 7: final evidence, critique, and acceptance reconciliation.

- Outcome: one acceptance dossier proves template inventory, word-count target,
  product/docs table removal, no new mechanical checks, and no examples/evals
  automation.
- Scope: `.loom/evidence/**`, `.loom/critique/**`, `.loom/tickets/**`, and narrow
  product-surface fixes only if critique finds issues.
- Evidence: final search/count outputs and diff-scope review.
- Critique: mandatory for final acceptance.

# Sequencing

Template work should land before table removal so new templates can be authored in
the desired table-free style from the start.

`using-loom` compression can run in parallel with template work only if the write
scopes do not overlap. It should finish before final public-doc alignment because
root docs may need to mirror the compressed doctrine framing.

`loom-core` table removal should precede `loom-playbooks` table removal so
playbooks can mirror the final core vocabulary. Root docs should be last among
product-surface edits because they summarize the product after core/playbook
surfaces settle.

# Risks

- Lite templates could invite under-specified records. Mitigation: keep
  frontmatter, minimal required ledger sections, and hard full-escalation triggers.
- `using-loom` compression could remove a safety invariant. Mitigation: use an
  invariant checklist and mandatory critique.
- Table rewrites could make dense reference material harder to scan. Mitigation:
  use label-led bullets and preserve stable vocabulary, IDs, and examples.
- Broad table removal could create noisy diffs. Mitigation: split core,
  playbooks, and root docs into separate tickets.
- Avoiding mechanical checks could let regressions return. Mitigation: record
  explicit validation commands and leave future enforcement as a separate decision
  after this pass proves the convention.

# Validation Plan

- `wc -l -w` for `using-loom` entry skill and ordered references before and after.
- Template inventory check for `ticket-lite.md`, `spec-lite.md`, and
  `evidence-lite.md`, plus existing generic full template names.
- Spot-check lite template frontmatter and minimal required sections.
- `rg -n '^\|.*\|$' loom-core loom-playbooks README.md PROTOCOL.md ARCHITECTURE.md`
  after table removal.
- Diff review for no new package checks, no hidden runtime, and no examples/evals
  automation.

# Open Decisions Before Execution

None - current decisions are sufficient to create execution tickets.

# Completion

Completed at: 2026-05-08T15:57:40Z

Outcome:

- Lite core templates were added while generic template filenames remained full
  copy targets.
- `using-loom` was compressed into the accepted 5,000 to 6,000 word band.
- Markdown tables were removed from `loom-core`, `loom-playbooks`, and root public
  docs in scoped tickets.
- Final validation and mandatory critique passed with no unresolved findings.

Residual risks:

- No rendered Markdown pass or operator usability eval was performed.
- Any future examples/eval automation remains deferred to separate accepted work.
