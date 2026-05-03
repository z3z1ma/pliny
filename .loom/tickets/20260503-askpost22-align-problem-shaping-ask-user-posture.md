---
id: ticket:askpost22
kind: ticket
status: ready
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-03T06:20:11Z
updated_at: 2026-05-03T06:20:11Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-context-integrity-hardening-pass
  plan:
    - plan:skills-corpus-context-integrity-hardening-pass
  research:
    - research:skills-corpus-third-pass-follow-up-validation
external_refs: {}
depends_on:
  - ticket:shipacc1
---

# Summary

Align problem-shaping ambiguous-choice guidance with the newer `ask_user` posture.

# Context

Problem shaping currently says not to silently choose between ambiguous readings.
That is directionally right but too absolute for low-risk reversible assumptions
inside delegated authority.

# Why Now

The corpus now distinguishes unsafe material ambiguity from low-risk reversible
assumptions that can be recorded and carried forward.

# Scope

- Qualify the ambiguous-choice guardrail.
- Preserve mandatory questioning for material, irreversible, high-risk,
  authority-changing, or owner-record-affecting ambiguity.
- Allow low-risk reversible assumptions inside delegated authority when recorded
  in the owner record.

# Out Of Scope

- Do not weaken `ask_user` for material decisions.
- Do not let chat summaries replace owner records.

# Acceptance Criteria

- ACC-001: Problem-shaping guardrail distinguishes material ambiguity from
  low-risk reversible assumptions.
- ACC-002: Low-risk assumption path requires recording the assumption in the
  owning record.
- ACC-003: `ask_user` remains required when proceeding would invent authority or
  accept material risk.
- ACC-004: Evidence records targeted problem-shaping / ask-user searches and
  `git diff --check`.
- ACC-005: Mandatory critique passes with no unresolved findings.

# Coverage

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-023`
- `ticket:askpost22#ACC-001`
- `ticket:askpost22#ACC-002`
- `ticket:askpost22#ACC-003`
- `ticket:askpost22#ACC-004`
- `ticket:askpost22#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-023` | pending | pending | open |
| `ticket:askpost22#ACC-001` | pending | pending | open |
| `ticket:askpost22#ACC-002` | pending | pending | open |
| `ticket:askpost22#ACC-003` | pending | pending | open |
| `ticket:askpost22#ACC-004` | pending | pending | open |
| `ticket:askpost22#ACC-005` | pending | pending | open |

# Execution Notes

Likely touched file: `skills/loom-workspace/references/problem-shaping.md`.

# Blockers

Blocked until `ticket:shipacc1` closes.

# Next Move / Next Route

Next route: ralph

# Route Readiness

Ralph readiness:
Bounded iteration: problem-shaping ask-user posture alignment.
Write boundary: workspace problem-shaping reference only.
Likely verification posture: observation-first structural validation.
Expected output contract: changed file, ambiguity posture observations, and
critique recommendation.

# Evidence

Expected: targeted searches for ambiguous readings, material/high-risk,
low-risk reversible assumptions, owner record, ask_user, and `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: problem shaping controls when agents ask versus proceed.

Required critique profiles:

- operator-clarity
- authority-boundary
- workflow-boundary

Findings:

None - no critique yet.

Disposition status: pending

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Pending after critique.

# Wiki Disposition

Pending retrospective decision after critique.

# Acceptance Decision

Accepted by:
Accepted at:
Basis:
Residual risks:

# Dependencies

- `ticket:shipacc1`

# Journal

- 2026-05-03T06:20:11Z: Created from third-pass audit finding 11.
