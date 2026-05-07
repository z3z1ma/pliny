---
id: ticket:specgram
kind: ticket
status: closed
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-07T20:17:28Z
updated_at: 2026-05-07T20:26:34Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  evidence:
    - evidence:spec-contract-grammar-check
  critique:
    - critique:spec-contract-grammar-review
external_refs: {}
depends_on: []
---

# Summary

Sharpen Loom spec authoring guidance so specs produce stronger behavior contracts,
scenario coverage, amendment discipline, and downstream verification cues without
weakening Loom's owner-layer boundaries.

# Context

The operator asked for useful external workflow findings to be assimilated into
Loom's own skill procedure and templates, while preserving Loom's stricter owner
model and avoiding imported artifact vocabulary or live-progress checklist habits.

# Scope

In:

- Strengthen `skills/loom-specs/SKILL.md` with requirement/scenario discipline,
  progressive rigor, and amendment guidance.
- Strengthen `skills/loom-specs/references/spec-shape.md` with copy-ready contract
  grammar and review heuristics.
- Strengthen `skills/loom-specs/templates/spec.md` with requirement/scenario,
  acceptance, evidence, and amendment structure.
- Add only narrow plan guidance if needed to preserve the ticket/packet live-ledger
  boundary.

Out:

- Do not add new runtime, schema, command, or archive/sync machinery.
- Do not add a new artifact kind.
- Do not import external product names or artifact vocabulary into Loom skills.
- Do not turn plans into a live progress ledger.

Assumptions / decision triggers:

| Assumption or question | Reversible? | Blocks execution? | Disposition |
| --- | --- | --- | --- |
| The useful changes can stay in existing `loom-specs` and `loom-plans` surfaces without a new reference file. | yes | no | accepted |

# Acceptance

Owner: ticket-local

Criteria / covered IDs:

- ticket:specgram#ACC-001
- ticket:specgram#ACC-002
- ticket:specgram#ACC-003
- ticket:specgram#ACC-004

Ticket-local criteria, only when no spec owns the reusable contract:

- ACC-001: Spec guidance teaches stable requirement IDs, concrete scenarios, and acceptance/evidence linkage without making specs delivery plans.
- ACC-002: Spec guidance teaches progressive rigor so routine specs can remain light while high-risk contracts gain detail.
- ACC-003: Spec guidance teaches safe amendment of existing behavior contracts, including added, modified, removed, and renamed behavior.
- ACC-004: Plan guidance preserves Loom's rule that tickets and packets own live execution truth.

# Current State

Status rationale: `closed` because scoped spec and plan guidance edits landed,
structural evidence was recorded, recommended critique completed, findings were
resolved, and acceptance was recorded.

Blockers: None.

Execution notes:

- Updated `skills/loom-specs/SKILL.md` with requirement/scenario discipline,
  progressive rigor, and amendment guidance.
- Updated `skills/loom-specs/references/spec-shape.md` and
  `skills/loom-specs/templates/spec.md` with contract grammar, scenario coverage,
  acceptance/evidence mapping, amendment notes, and contract review guidance.
- Updated `skills/loom-plans/SKILL.md` and
  `skills/loom-plans/references/plan-shape.md` to remove imported artifact
  vocabulary and preserve Loom's ticket/packet live-ledger boundary.

Continuation note: No immediate continuation is required for this ticket.

# Evidence

Disposition: sufficient for closure

Records:

- `evidence:spec-contract-grammar-check`

Gaps / limits: Evidence is structural and content-review based. It does not prove
future spec authoring quality or every downstream example.

# Review And Follow-Through

Critique policy: recommended
Critique rationale: This changes operator guidance and templates, but scope is narrow and does not alter Loom's authority model.
Critique disposition: completed

Required critique profiles:

- protocol-change
- operator-clarity

Findings:

- `critique:spec-contract-grammar-review#FIND-001`: resolved by changing plan
  guidance so ticket acceptance and packet task text own executable detail, while
  plans only name proof targets for tickets and packets to validate.
- `critique:spec-contract-grammar-review#FIND-002`: resolved by adding
  `Superseded` to the skill-level amendment type list and keeping the reference
  and template aligned.

Promotion disposition: not_required
Promotion / deferral rationale: The durable learning is being promoted directly into the owning skill surfaces.

Promoted / deferred: Direct updates to `skills/loom-specs` and `skills/loom-plans`.

Wiki disposition: not_required - the accepted explanation is skill procedure, not a reusable concept page.

# Acceptance Decision

Required before closure when acceptance, accepted risk, or operator provenance
needs to be explicit.

Accepted by: OpenCode agent under user-delegated Loom operation
Accepted at: 2026-05-07T20:26:34Z
Basis: `ticket:specgram#ACC-001` through `ticket:specgram#ACC-004` are supported
by scoped skill/reference/template edits, structural evidence
`evidence:spec-contract-grammar-check`, and completed critique
`critique:spec-contract-grammar-review`; no critique blockers remain.
Residual risks: Markdown guidance cannot prove future authoring quality. Future
examples should reinforce when to use `Superseded` versus `Modified` or `Removed`.

# Dependencies

No hard ticket prerequisites.

# Journal

- 2026-05-07T20:17:28Z: Ticket opened for bounded local execution over Loom spec and plan skill surfaces.
- 2026-05-07T20:20:28Z: Added spec requirement/scenario discipline,
  progressive rigor, amendment guidance, and template/reference contract grammar;
  updated plan guidance to remove imported artifact vocabulary and preserve the
  ticket/packet live-ledger boundary.
- 2026-05-07T20:25:34Z: Completed critique pass; two findings were raised and
  resolved in the current diff.
- 2026-05-07T20:25:56Z: Recorded structural validation evidence.
- 2026-05-07T20:26:34Z: Linked evidence and critique, dispositioned findings,
  recorded acceptance, and closed the ticket.
