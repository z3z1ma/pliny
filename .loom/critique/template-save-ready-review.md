---
id: critique:template-save-ready-review
kind: critique
status: final
created_at: 2026-05-03T05:08:15Z
updated_at: 2026-05-03T05:08:15Z
scope:
  kind: repository
  repositories:
    - repo:root
review_target: "ticket:tplsave3 diff e5abe40..working-tree"
links:
  ticket:
    - ticket:tplsave3
  evidence:
    - evidence:template-save-ready-validation
  packet:
    - packet:ralph-ticket-tplsave3-20260503T050338Z
external_refs: {}
---

# Summary

Mandatory critique for `ticket:tplsave3` after adding save-ready pruning rules to
the ticket and plan templates.

# Review Target

Current working-tree diff from baseline
`e5abe407d9ba526af48dde2e519bc1a1901fc734`, covering ticket and plan template
edits, `ticket:tplsave3`, `evidence:template-save-ready-validation`, and Ralph
packet `packet:ralph-ticket-tplsave3-20260503T050338Z`.

Required critique profiles: `template-safety`, `closure-honesty`, and
`operator-clarity`.

# Verdict

`pass` - no findings.

# Findings

None - no findings.

# Profile Results

- `template-safety`: pass. The ticket template now tells agents to replace
  placeholders and remove unused acceptance/readiness branches; the plan template
  now tells agents to remove unused wave examples/placeholders or write meaningful
  `None - reason`.
- `closure-honesty`: pass. Evidence, critique, retrospective/promotion,
  acceptance, and closure gates remain intact.
- `operator-clarity`: pass. The guidance is concise and does not add generators,
  schemas, or separate minimal/full template families.

# Evidence Reviewed

- Targeted diff from baseline `e5abe407d9ba526af48dde2e519bc1a1901fc734`
- `git diff --check`: passed with no output
- `evidence:template-save-ready-validation`
- `skills/loom-tickets/templates/ticket.md`
- `skills/loom-plans/templates/plan.md`
- `ticket:tplsave3`
- `packet:ralph-ticket-tplsave3-20260503T050338Z`

# Acceptance Coverage

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-004`:
  supported.
- `ticket:tplsave3#ACC-001`: supported. Ticket template tells agents to replace
  placeholders and remove unused acceptance/readiness branches before saving.
- `ticket:tplsave3#ACC-002`: supported. Plan template tells agents to remove
  unused wave examples/placeholders or replace them with meaningful
  `None - reason`.
- `ticket:tplsave3#ACC-003`: supported. Evidence, critique, acceptance,
  retrospective/promotion, and closure gates remain present.
- `ticket:tplsave3#ACC-004`: supported. Evidence records targeted template checks
  and `git diff --check`.
- `ticket:tplsave3#ACC-005`: supported. Mandatory critique passed with no
  unresolved findings.

# Residual Risks

- Existing route-readiness guidance still permits marking unrelated route sections
  `N/A`; the new save-ready rule is clear enough for this ticket, but later
  template tightening may prefer removal-only wording.

# Required Follow-up

None for this ticket.

# Acceptance Recommendation

`no-critique-blockers`
