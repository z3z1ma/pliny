---
id: ticket:vocabx08
kind: ticket
status: closed
change_class: records-grammar
risk_class: medium
created_at: 2026-05-03T04:09:51Z
updated_at: 2026-05-03T05:01:50Z
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
    - research:skills-corpus-context-integrity-hardening-review
external_refs: {}
depends_on:
  - ticket:trustbd2
---

# Summary

Consolidate route/status/disposition vocabulary boundaries so agents do not mix
route tokens, lifecycle statuses, ticket states, child outcomes, critique states,
or ticket-owned dispositions.

# Context

Council found the vocabulary model strong but vulnerable to duplicated lists and
`continue`/`stop` ambiguity.

# Why Now

Template and workflow edits later in this pass should point at canonical
vocabulary instead of spreading drift.

# Scope

- Strengthen `route-vocabulary` and `status-lifecycle` as canonical references.
- Update nearby surfaces that duplicate or blur vocabulary boundaries.
- Explicitly distinguish route tokens from Ralph child outcomes when useful.

# Out Of Scope

- Do not create runtime enums, validators, command routers, or schemas.
- Do not rename existing route tokens unless unavoidable.

# Acceptance Criteria

- ACC-001: Canonical route and status sources are clear and cross-linked.
- ACC-002: Guidance distinguishes route tokens, ticket states, record statuses,
  packet statuses, child outcomes, critique finding states, and ticket-owned
  dispositions.
- ACC-003: `continue` and `stop` route-token examples cannot be confused with
  Ralph child outcomes.
- ACC-004: Evidence records targeted vocabulary searches and `git diff --check`.
- ACC-005: Mandatory critique passes with no unresolved findings.

# Coverage

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-003`
- `ticket:vocabx08#ACC-001`
- `ticket:vocabx08#ACC-002`
- `ticket:vocabx08#ACC-003`
- `ticket:vocabx08#ACC-004`
- `ticket:vocabx08#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-003` | `evidence:route-status-vocabulary-validation` | `critique:route-status-vocabulary-review` | supported |
| `ticket:vocabx08#ACC-001` | `evidence:route-status-vocabulary-validation` | `critique:route-status-vocabulary-review` | supported |
| `ticket:vocabx08#ACC-002` | `evidence:route-status-vocabulary-validation` | `critique:route-status-vocabulary-review` | supported |
| `ticket:vocabx08#ACC-003` | `evidence:route-status-vocabulary-validation` | `critique:route-status-vocabulary-review` | supported |
| `ticket:vocabx08#ACC-004` | `evidence:route-status-vocabulary-validation` | `critique:route-status-vocabulary-review` | supported |
| `ticket:vocabx08#ACC-005` | None - critique outcome is the acceptance instrument | `critique:route-status-vocabulary-review` | supported |

# Execution Notes

Likely touched files: `skills/loom-records/references/route-vocabulary.md`,
`skills/loom-records/references/status-lifecycle.md`, and small dependent
cross-references if needed.

# Blockers

None.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to `ticket:tplsave3`.

Ralph packet `packet:ralph-ticket-vocabx08-20260503T045534Z` was consumed in
scope, evidence was recorded, mandatory critique passed with no findings, and
acceptance is complete.

# Route Readiness

Acceptance review readiness:
Evidence `evidence:route-status-vocabulary-validation` and mandatory critique
`critique:route-status-vocabulary-review` support closure with no findings.

# Evidence

Recorded: `evidence:route-status-vocabulary-validation`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: vocabulary drift can mislead ticket closure and route selection.

Required critique profiles:

- records-grammar
- routing-safety
- operator-clarity

Findings:

`critique:route-status-vocabulary-review` - no findings; mandatory critique
passed.

Disposition status: completed

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- Route/status vocabulary boundaries were promoted directly into
  `skills/loom-records/references/route-vocabulary.md` and
  `skills/loom-records/references/status-lifecycle.md`.
- Dependent ticket, Ralph, and critique references now point to the canonical
  vocabulary sources where ambiguity is likely.

Deferred / not-required rationale:

No separate wiki, research, spec, constitution, or memory record is needed. The
durable lesson is shared record grammar and lives in the records skill
references.

# Wiki Disposition

N/A - no separate wiki promotion route. The accepted explanation lives in the
records references.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-03T05:01:50Z
Basis: Ralph packet `packet:ralph-ticket-vocabx08-20260503T045534Z`; evidence
`evidence:route-status-vocabulary-validation`; mandatory critique
`critique:route-status-vocabulary-review` with no findings.
Residual risks: Low residual copy-drift risk remains in downstream templates and
workflows until later tickets consume these canonical references.

# Dependencies

- `ticket:trustbd2`

# Journal

- 2026-05-03T04:09:51Z: Created from council vocabulary consolidation finding.
- 2026-05-03T04:55:34Z: Started Ralph iteration
  `packet:ralph-ticket-vocabx08-20260503T045534Z` from clean `main` at
  `bd06422`.
- 2026-05-03T04:57:59Z: Ralph iteration
  `packet:ralph-ticket-vocabx08-20260503T045534Z` completed in scope. Evidence
  recorded in `evidence:route-status-vocabulary-validation`; next route is
  mandatory critique.
- 2026-05-03T05:01:50Z: Mandatory critique
  `critique:route-status-vocabulary-review` passed with no findings. Parent
  recorded retrospective / promotion disposition and accepted closure.
