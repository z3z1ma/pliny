---
id: spec:point-of-use-ergonomics-and-mechanical-simplicity
kind: spec
status: accepted
created_at: 2026-05-08T07:32:35Z
updated_at: 2026-05-08T15:57:40Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  decision:
    - decision:0008
  roadmap:
    - roadmap:bootstrap-the-markdown-first-protocol-corpus
  plan:
    - plan:point-of-use-ergonomics-and-mechanical-simplicity
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

# Summary

This spec defines the intended behavior for making Loom lighter at the point of
use without weakening its thesis: durable owner-layer truth, explicit execution
state, evidence, critique, and recoverable handoff through Markdown-native
records.

It covers three first-pass outcomes:

- lite templates plus preserved full-compatible generic templates for tickets,
  specs, and evidence in `loom-core`
- compressed mandatory `using-loom` doctrine
- removal of Markdown tables from shipped product/docs surfaces

Automation-backed evals or recreated examples are explicitly deferred until this
work reaches a high-confidence accepted state.

# Rigor Level

Full.

Rationale: this work changes Loom's always-on operator experience, template
surface, public docs, and product-corpus authoring style. A lighter point of use
is only acceptable if future agents can still recover owner truth and closure
discipline without relying on transcript context.

# Problem

Recent comparison against projects such as Superpowers and agent-skills suggests
Loom has the stronger underlying thesis, but current use can feel too heavy at
the moment an agent needs to create records or load doctrine.

The current pain has three parts:

- Templates are full-strength by default, even when the task only needs a small
  truthful ledger.
- `using-loom` carries enough repeated explanation that always-on context costs
  more tokens than necessary.
- Markdown tables are easy to corrupt, verbose in tokenized form, and awkward for
  agents to edit safely.

# Settled Decisions

- Template choice: agents/operators choose lite or full based on complexity.
- Full template names: existing `ticket.md`, `spec.md`, and `evidence.md` are the
  canonical full copy targets for compatibility.
- Full-suffixed aliases: `ticket-full.md`, `spec-full.md`, and `evidence-full.md`
  are not required in this pass unless a later decision chooses copy-safe
  duplication.
- Lite template frontmatter: lite templates still include real YAML frontmatter.
- Lite body posture: lite templates are minimal ledgers, not complete closure-gate
  worksheets.
- Ticket-lite body: after frontmatter, `ticket-lite.md` uses `# Summary`,
  `# Scope`, `# Acceptance`, `# Evidence`, `# Status / Next Move`, and
  `# Journal`.
- Spec-lite body: after frontmatter, `spec-lite.md` uses `# Summary`,
  `# Problem`, `# Desired Behavior`, `# Requirements`, `# Scenarios`,
  `# Acceptance`, `# Evidence Plan`, and `# Open Questions`.
- Evidence-lite body: after frontmatter, `evidence-lite.md` uses `# Summary`,
  `# Observation`, `# Artifacts`, `# Supports / Challenges`, `# Limits`, and
  `# Related Records`.
- Full escalation triggers: use full when any high-risk, public/shared,
  multi-ticket, reusable-acceptance, migration/security/privacy, ambiguous, or
  mandatory-critique condition is present.
- Table replacement style: use label-led bullets as the default replacement for
  Markdown tables.
- Table-removal scope: first pass covers product/docs surfaces only:
  `loom-core`, `loom-playbooks`, `README.md`, `PROTOCOL.md`, and
  `ARCHITECTURE.md`.
- `using-loom` reduction style: keep the full ordered doctrine architecture, but
  compress and deduplicate it.
- `using-loom` target: reduce from about 9,811 words to about 5,500 words while
  preserving essential doctrine.
- `using-loom` acceptance range: 5,000 to 6,000 words is acceptable when the
  essential invariants are preserved; outside that band requires explicit
  rationale.
- Mechanical checks: do not add new smoke/package checks in this pass. Use
  explicit `rg`, `wc`, diff review, evidence, and critique instead.
- Root docs: mention the lite/full template distinction briefly, while keeping
  operational detail in the owning core skills.
- Table-row preservation: table rewrites preserve existing row content by default;
  deletion is allowed only for plainly duplicate or stale rows with rationale in
  ticket or evidence notes.

# Desired Behavior

Loom should feel fast to start while still making the important facts durable.

A future agent should be able to choose the smallest safe template, load a
shorter always-on doctrine set, and edit product Markdown without table-format
fragility. The result must preserve Loom's value proposition: source-of-truth
layers, ticket-owned live execution, evidence as observation, critique as review,
wiki as accepted explanation, and packets as bounded handoffs rather than project
truth.

# Quality Bar

The result is acceptable only if it improves point-of-use speed without creating
shadow truth, vague records, or weaker closure claims.

Observable quality signals:

- A small local ticket can be created from `ticket-lite.md` with frontmatter and a
  short body that still names scope, acceptance, evidence, status, and journal.
- A full ticket/spec/evidence path remains available and compatible through the
  existing generic template names.
- `using-loom` keeps the same mandatory reference architecture and all essential
  invariants, but the total word count is close to the target.
- Product/docs Markdown has no pipe-table rows after the rewrite.
- Replacements remain grep-friendly and readable as plain Markdown.
- No package script or hidden runtime becomes the enforcement owner for this
  change.

# Requirements

- REQ-001: `loom-core` MUST provide explicit lite templates for tickets, specs,
  and evidence: `ticket-lite.md`, `spec-lite.md`, and `evidence-lite.md`.
- REQ-002: Existing generic template filenames `ticket.md`, `spec.md`, and
  `evidence.md` MUST remain the canonical full copy targets and preserve
  full-template behavior for compatibility.
- REQ-003: Lite templates MUST include valid YAML frontmatter with the same core
  identity fields required by the record kind.
- REQ-004: Lite ticket templates MUST be minimal ledgers: frontmatter, summary,
  context, scope, acceptance, evidence, status/next move, and journal are enough
  unless complexity triggers the full template.
- REQ-005: Lite spec templates MUST still make intended behavior testable or
  observable through focused requirements, scenarios or examples, acceptance, and
  evidence expectations.
- REQ-006: Lite evidence templates MUST still separate observation from
  interpretation and name source state, procedure, actual result, supported or
  challenged claims, and limitations.
- REQ-007: Skill guidance MUST define the conditions that force full-template use
  or escalation: high risk, public/shared surface, multi-ticket scope, reusable
  acceptance, migration/security/privacy boundary, material ambiguity, or mandatory
  critique.
- REQ-008: `using-loom` MUST remain mandatory doctrine with the same ordered
  reference architecture, but SHOULD be compressed to 5,000 to 6,000 words total
  across the entry skill and eight references unless explicit rationale justifies
  a result outside that band.
- REQ-009: Compression MUST preserve the essential invariants: owner-layer truth,
  instruction authority, tickets as live ledger, Ralph packet boundaries, evidence
  as observation, critique gates, wiki promotion, validation honesty, trust
  boundaries, and no hidden runtime requirement.
- REQ-010: Shipped product/docs Markdown SHOULD avoid Markdown pipe tables in this
  pass. The target surfaces are `loom-core`, `loom-playbooks`, `README.md`,
  `PROTOCOL.md`, and `ARCHITECTURE.md`.
- REQ-011: Table replacements SHOULD use label-led bullets unless a different
  non-table structure is clearly more readable for a specific passage.
- REQ-012: This pass MUST NOT add new package smoke checks, hidden validators,
  required scripts, command wrappers, or eval/example automation.
- REQ-013: Verification MUST be recorded with explicit search/count commands,
  word-count evidence, diff review, and critique before acceptance.

# Scenarios

## SCN-001: Small Local Work Uses Lite Ticket

Exercises: REQ-001, REQ-003, REQ-004, REQ-007, ACC-001.

GIVEN a low-risk, local, single-ticket task with no reusable acceptance contract
WHEN an agent creates a ticket
THEN the agent may choose `ticket-lite.md`
AND the saved ticket still has YAML frontmatter, bounded scope, acceptance,
evidence posture, status/next move, and journal.

## SCN-002: Complex Work Escalates To Full

Exercises: REQ-002, REQ-007, ACC-002.

GIVEN a public API, migration, protocol-authority change, security/privacy
boundary, multi-ticket plan, reusable acceptance contract, material ambiguity, or
mandatory critique
WHEN an agent chooses a template
THEN guidance forces the full template or an escalation from lite to full before
downstream work depends on the record.

## SCN-003: Generic Templates Stay Full

Exercises: REQ-002, ACC-003.

GIVEN existing instructions or operators copy `ticket.md`, `spec.md`, or
`evidence.md`
WHEN the record is created
THEN those generic names still provide full-template behavior rather than silently
switching the user to a reduced lite form.

## SCN-004: Always-On Doctrine Is Shorter But Complete

Exercises: REQ-008, REQ-009, ACC-004.

GIVEN the `using-loom` entry skill and eight ordered references
WHEN the compression pass is complete
THEN the total word count is close to 5,500 words
AND the essential invariants remain present in the doctrine.

## SCN-005: Tables Become Label-Led Bullets

Exercises: REQ-010, REQ-011, ACC-005.

GIVEN a product/docs Markdown file containing a pipe table
WHEN the table-removal pass rewrites it
THEN the file uses label-led bullets or another explicit non-table structure
AND a targeted search finds no remaining pipe-table rows in the scoped surfaces.

# Acceptance

- ACC-001: `ticket-lite.md`, `spec-lite.md`, and `evidence-lite.md` exist in
  `loom-core` and each includes valid frontmatter plus the minimal body needed for
  the record kind.
- ACC-002: Core skill guidance documents full-template escalation triggers and
  prevents lite templates from being used for high-risk, shared, ambiguous, or
  mandatory-critique work.
- ACC-003: `ticket.md`, `spec.md`, and `evidence.md` remain the full copy targets
  after the lite template addition.
- ACC-004: `using-loom` total word count is reduced from the observed baseline of
  about 9,811 words into the 5,000 to 6,000 word band without losing the essential
  invariants listed in REQ-009, or the evidence records explicit rationale for a
  result outside the band.
- ACC-005: `rg -n '^\|.*\|$' loom-core loom-playbooks README.md PROTOCOL.md ARCHITECTURE.md`
  returns no product/docs pipe-table rows, or any remaining pipe-delimited lines
  are explicitly justified as non-table content.
- ACC-006: The implementation does not add new smoke/package checks or hidden
  runtime enforcement for this policy.
- ACC-007: Final evidence records the template inventory, word-count result,
  table-search result, and diff-review scope; final critique reviews point-of-use
  ergonomics, doctrine completeness, and owner-layer safety.

# Not Doing

- Do not create evals, examples automation, or a regenerated examples directory in
  this pass.
- Do not add a CLI, daemon, validator, database, MCP, command wrapper, or hidden
  runtime.
- Do not make lite templates frontmatter-free.
- Do not remove full templates or make existing generic template names point to a
  weaker default.
- Do not rewrite dogfood `.loom` history or example fixture Markdown as part of
  the table-removal scope unless a later ticket explicitly expands scope.

# Open Questions

None - current decisions are sufficient to create execution tickets. Remaining
implementation tradeoffs should be handled ticket-locally without widening this
contract.

# Evidence Plan

- Template inventory check for the three new lite files and existing generic full
  filenames.
- Targeted inspection that lite files include frontmatter and required minimal
  sections.
- `wc -l -w` for `loom-core/skills/using-loom/SKILL.md` and ordered references
  before and after compression.
- `rg -n '^\|.*\|$' loom-core loom-playbooks README.md PROTOCOL.md ARCHITECTURE.md`
  after table removal.
- Diff review for scope: no eval/example automation and no new hidden runtime or
  package-script enforcement.

# Amendment Notes

None - new spec.

# Acceptance Status

Accepted at: 2026-05-08T15:57:40Z

Basis:

- `ticket:iq03bxg5` closed the lite-template slice and supports `ACC-001` through
  `ACC-003`.
- `ticket:nlzaqhrm` closed the `using-loom` compression slice and supports
  `ACC-004`.
- `ticket:58h4o1qo`, `ticket:xulgzs52`, and `ticket:57rm2fmx` closed the
  product/docs table-removal slices and support `ACC-005`.
- `ticket:esszigx8` closed the final validation slice and supports `ACC-006` and
  `ACC-007` through `evidence:point-of-use-ergonomics-final-check` and
  `critique:point-of-use-ergonomics-final-review`.

Residual risks:

- No rendered Markdown pass or operator usability eval was performed.
- Semantic preservation was reviewed through evidence, critique, and representative
  diff sampling rather than exhaustive row-by-row proof.
