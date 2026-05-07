---
id: critique:spec-contract-grammar-review
kind: critique
status: final
created_at: 2026-05-07T20:25:34Z
updated_at: 2026-05-07T20:25:34Z
scope:
  kind: repository
  repositories:
    - repo:root
review_target: "ticket:specgram scoped diff for Loom spec contract grammar"
links:
  tickets:
    - ticket:specgram
external_refs: {}
---

# Summary

Reviewed the scoped Markdown protocol changes for `ticket:specgram`, focused on
`protocol-change` and `operator-clarity` risk.

# Review Target

Target: `ticket:specgram` scoped diff over:

- `skills/loom-specs/SKILL.md`
- `skills/loom-specs/references/spec-shape.md`
- `skills/loom-specs/templates/spec.md`
- `skills/loom-plans/SKILL.md`
- `skills/loom-plans/references/plan-shape.md`

The review checked that the changes strengthen requirement/scenario/acceptance
grammar, progressive rigor, amendment discipline, and plan live-ledger boundaries
without adding new runtime, schema, command, artifact kind, external product
vocabulary, or evidence ownership drift.

# Verdict

`pass_with_findings`

Two review findings were raised during the pass and addressed in the current diff.
The ticket should consume both as `resolved` before closure.

# Findings

## FIND-001: Plan wording blurred evidence ownership with execution ownership

Severity: medium
Confidence: high
State: open

Observation:

The first version of the plan guidance said executable detail should move into
"ticket acceptance, packet task text, or evidence expectations." That phrasing
could make evidence sound like an owner of pre-execution contract detail.

Why it matters:

Loom evidence owns observed artifacts. Tickets and packets own live execution
contracts and acceptance scope. Plan guidance should not imply that evidence owns
executable detail.

Follow-up:

Resolved in the current diff by changing the guidance so ticket acceptance and
packet task text own executable detail, while plans may name proof targets for
tickets and packets to validate. Ticket-owned disposition should record this as
`resolved`.

Challenges:

- `ticket:specgram#ACC-004`

## FIND-002: Superseded was inconsistent between amendment type and disposition

Severity: low
Confidence: high
State: open

Observation:

The first version listed Added, Modified, Removed, and Renamed mutation types in
`skills/loom-specs/SKILL.md`, while the reference/template and verification also
treated `superseded` as an amendment type.

Why it matters:

Operators need consistent guidance for ID preservation and successor behavior.
Ambiguity around supersession could lead to stable IDs being silently reused for
different contracts.

Follow-up:

Resolved in the current diff by adding `Superseded` to the skill-level amendment
types and keeping the reference/template aligned. Ticket-owned disposition should
record this as `resolved`.

Challenges:

- `ticket:specgram#ACC-003`

# Evidence Reviewed

- Scoped diff for the five target skill/reference/template files.
- `git diff --check` output with no whitespace errors.
- Targeted search showing no `ExecPlan`, `execplan`, or `OpenAI-style` terms in
  `skills/**/*.md`.
- Targeted search confirming new `Rigor Level`, `REQ-*`, `SCN-*`, `Amendment
  Notes`, `Contract Review`, and `Self-Orienting Plan Discipline` surfaces.
- Focused re-review of the two findings after fixes.

# Residual Risks

- Future examples should reinforce when to use `Superseded` instead of
  `Modified` or `Removed`, but this diff now gives consistent baseline guidance.
- The template is more detailed than before; progressive-rigor guidance mitigates
  the risk of routine specs becoming too heavy.

# Required Follow-up

No critique blockers remain before ticket acceptance. The ticket must record
`resolved` dispositions for `critique:spec-contract-grammar-review#FIND-001` and
`critique:spec-contract-grammar-review#FIND-002`.

# Acceptance Recommendation

`no-critique-blockers`

The scoped changes are acceptable after the ticket records the finding
dispositions and evidence basis.
