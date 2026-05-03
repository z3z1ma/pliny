---
id: ticket:routewf10
kind: ticket
status: closed
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-02T22:03:13Z
updated_at: 2026-05-03T00:10:20Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-template-grammar-safety-pass
  plan:
    - plan:skills-corpus-template-grammar-safety-pass
  packet:
    - packet:ralph-ticket-routewf10-20260502T234101Z
    - packet:ralph-ticket-routewf10-20260502T235105Z
    - packet:ralph-ticket-routewf10-20260503T000116Z
  evidence:
    - evidence:workflow-route-token-validation
  critique:
    - critique:workflow-route-token-review
    - critique:workflow-route-token-rereview
    - critique:workflow-route-token-final-rereview
external_refs: {}
depends_on:
  - ticket:tkrout5
---

# Summary

Audit shared route vocabulary and dependent route lists for first-class workflow
coordinators such as ship, spike, codemap, and debugging.

# Context

Council finding `NC-010` found that some workflow coordinators may be absent from
shared route-token lists, inviting inconsistent local route grammar.

# Why Now

Route vocabulary should give fresh agents stable next-route tokens without
becoming a runtime enum or command router.

# Scope

- Audit `route-vocabulary.md` and downstream route-token lists/examples.
- Add or clarify workflow route tokens only when they name existing first-class
  workflow moves.
- Preserve the non-runtime, grep-friendly vocabulary framing.

# Out Of Scope

- Do not add a command router or runtime enum.
- Do not turn every skill display name into a route token.

# Acceptance Criteria

- ACC-001: Existing first-class workflow coordinator routes are either represented
  in shared route vocabulary or explicitly routed through existing tokens.
- ACC-002: Downstream route-token examples/lists align with the shared vocabulary.
- ACC-003: Route vocabulary remains grep-friendly guidance, not runtime schema.
- ACC-004: Evidence records route-token audits and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-010`
- `ticket:routewf10#ACC-001`
- `ticket:routewf10#ACC-002`
- `ticket:routewf10#ACC-003`
- `ticket:routewf10#ACC-004`
- `ticket:routewf10#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-template-grammar-safety-pass#OBJ-010` | `evidence:workflow-route-token-validation` | `critique:workflow-route-token-final-rereview` | supported |
| `ticket:routewf10#ACC-001` | `evidence:workflow-route-token-validation` | `critique:workflow-route-token-final-rereview` | supported |
| `ticket:routewf10#ACC-002` | `evidence:workflow-route-token-validation` | `critique:workflow-route-token-review#FIND-001` resolved; `critique:workflow-route-token-final-rereview` passed | supported |
| `ticket:routewf10#ACC-003` | `evidence:workflow-route-token-validation` | `critique:workflow-route-token-final-rereview` | supported |
| `ticket:routewf10#ACC-004` | `evidence:workflow-route-token-validation` | `critique:workflow-route-token-final-rereview` | supported |
| `ticket:routewf10#ACC-005` | `critique:workflow-route-token-final-rereview` | oracle final re-review passed with no findings | supported |

# Execution Notes

Likely touched surfaces include `skills/loom-records/references/route-vocabulary.md`,
drive references, and ticket route examples.

# Blockers

None - dependency `ticket:tkrout5` is closed.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to `ticket:readme11`.

# Route Readiness

Acceptance review readiness:
Evidence `evidence:workflow-route-token-validation`, critique findings resolved,
and final oracle re-review `critique:workflow-route-token-final-rereview` support
closure with no findings.

# Evidence

Recorded: `evidence:workflow-route-token-validation` supports
`initiative:skills-corpus-template-grammar-safety-pass#OBJ-010` and
`ticket:routewf10#ACC-001` through `ticket:routewf10#ACC-004` with before/after
route-token searches and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: inconsistent route tokens can degrade workspace recovery.

Required critique profiles:

- routing-safety
- operator-clarity
- records-grammar

Findings:

`critique:workflow-route-token-review#FIND-001` - remediated in the third Ralph
iteration after `critique:workflow-route-token-rereview`; resolved by
`critique:workflow-route-token-final-rereview`.
`critique:workflow-route-token-review#FIND-002` - resolved by remediation and
confirmed by `critique:workflow-route-token-rereview` and
`critique:workflow-route-token-final-rereview`.

Disposition status: completed

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- Workflow route-token guidance was promoted directly into shared route vocabulary,
  ticket route guidance, workspace routing, drive guidance, plan/Ralph route
  references, bootstrap outer-loop doctrine, and `PROTOCOL.md`.

Deferred / not-required rationale:

No separate wiki page, research record, spec, constitution decision, or memory
entry is needed. The durable lesson is the product guidance itself.

# Wiki Disposition

N/A - no separate wiki promotion route. The accepted explanation lives in the
touched route vocabulary and workflow guidance.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-03T00:10:20Z
Basis: Ralph packets `packet:ralph-ticket-routewf10-20260502T234101Z`,
`packet:ralph-ticket-routewf10-20260502T235105Z`, and
`packet:ralph-ticket-routewf10-20260503T000116Z`; evidence
`evidence:workflow-route-token-validation`; oracle critiques
`critique:workflow-route-token-review`, `critique:workflow-route-token-rereview`,
and `critique:workflow-route-token-final-rereview` with all findings resolved.
Residual risks: validation is structural/search-based and does not prove
real-world operator comprehension; no runtime validator is intentionally added.

# Dependencies

- `ticket:tkrout5`

# Journal

- 2026-05-02T22:03:13Z: Created from council finding `NC-010`.
- 2026-05-02T23:41:02Z: Confirmed dependency `ticket:tkrout5` is closed,
  compiled Ralph packet `packet:ralph-ticket-routewf10-20260502T234101Z`, and
  moved ticket to `active`.
- 2026-05-02T23:42:42Z: Ralph iteration added explicit `debugging`, `spike`,
  `codemap`, and `ship` route tokens where they are first-class workflow moves,
  aligned dependent route lists/examples, recorded
  `evidence:workflow-route-token-validation`, and moved ticket to
  `review_required` with next route `critique`.
- 2026-05-02T23:46:47Z: Parent reconciled Ralph output, marked
  `packet:ralph-ticket-routewf10-20260502T234101Z` consumed, and recorded a scope
  note for dependent drive route-list files that were task-scoped but omitted
  from packet frontmatter `child_write_scope.paths`.
- 2026-05-02T23:51:06Z: Mandatory oracle critique
  `critique:workflow-route-token-review` found two medium routing/operator-clarity
  issues. Parent recorded findings as blocking and compiled remediation packet
  `packet:ralph-ticket-routewf10-20260502T235105Z`.
- 2026-05-02T23:53:35Z: Ralph remediation iteration updated downstream route
  readiness/route-option guidance, narrowed route priority so debugging/spike/
  codemap precede implementation routing when they own the next move, refreshed
  evidence, and moved ticket to `review_required` with next route `critique`.
- 2026-05-02T23:56:20Z: Parent reconciled remediation packet
  `packet:ralph-ticket-routewf10-20260502T235105Z`, marked it consumed, and kept
  next route as mandatory oracle re-review.
- 2026-05-03T00:01:16Z: Mandatory oracle re-review
  `critique:workflow-route-token-rereview` confirmed `FIND-002` resolved but kept
  `FIND-001` open for broader active route-option guidance. Parent recorded the
  finding as blocking and compiled remediation packet
  `packet:ralph-ticket-routewf10-20260503T000116Z`.
- 2026-05-03T00:03:31Z: Third Ralph remediation updated broader active route
  guidance in `skills/loom-drive/SKILL.md`, `skills/loom-ralph/SKILL.md`,
  `skills/loom-bootstrap/references/03-outer-loop.md`, and `PROTOCOL.md`,
  refreshed evidence, and moved the ticket to `review_required` with next route
  `critique` for mandatory oracle re-review.
- 2026-05-03T00:06:39Z: Parent reconciled remediation packet
  `packet:ralph-ticket-routewf10-20260503T000116Z`, marked it consumed, and
  corrected critique disposition status to canonical ticket-owned vocabulary.
- 2026-05-03T00:10:20Z: Mandatory oracle final re-review
  `critique:workflow-route-token-final-rereview` passed with no findings and
  confirmed both prior findings resolved. Parent recorded retrospective /
  promotion disposition and accepted closure.
