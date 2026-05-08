---
id: ticket:<token>
kind: ticket
status: proposed
change_class: "<TBD: choose one change class before saving>"
risk_class: "<TBD: choose low, medium, or high before saving>"
created_at: <UTC timestamp>
updated_at: <UTC timestamp>
scope:
  kind: repository
  repositories:
    - repo:root
links: {}
external_refs: {}
depends_on: []
---

# Summary

One or two sentences naming the bounded work and the outcome it should produce.

Save-ready rule: replace every placeholder before saving. Keep the gates below,
but write `None - reason` when a gate is genuinely not applicable.

# Context

Why this exists now. Cite upstream initiative, research, spec, or plan records
when they constrain the work.

# Scope

In:

- <TBD: what belongs in this ticket>

Out:

- <TBD: what must not happen in this ticket>

Assumptions / decision triggers:

- <TBD or None - no material assumptions>:
  - Reversible: <yes/no>
  - Blocks execution: <yes/no>
  - Disposition: <accepted, ask user, route to owner, or reason>

# Acceptance

Owner: <TBD: spec-owned or ticket-local>

Criteria / covered IDs:

- <TBD: spec:<slug>#ACC-001, initiative:<slug>#OBJ-001, or ticket:<token>#ACC-001>

Ticket-local criteria, only when no spec owns the reusable contract:

- ACC-001: <TBD: specific, testable ticket-local criterion, or remove>

Optional claim matrix: add a compact table only when several claims, evidence
records, or critique findings make the coverage state hard to read inline. Use
`skills/loom-records/references/claim-coverage.md` for status vocabulary.

# Current State

Status rationale:

Blockers:

Execution notes:

Continuation note:

Name the owner facts that make the next action obvious. Do not serialize a route
token or let this note replace ticket status, blockers, evidence, or critique
disposition.

# Evidence

Disposition: <TBD: pending, sufficient, insufficient, challenged, stale, superseded, or not_required>

Records:

- <TBD: evidence:<slug> — supports/challenges <claim IDs>, or None - no evidence yet>

Gaps / limits:

# Review And Follow-Through

Critique policy: <TBD: optional, recommended, or mandatory>
Critique rationale: <TBD: why this policy fits the change and risk, or why review is not required>
Critique disposition: <TBD: pending, blocking, completed, deferred, or not_required>

Required critique profiles:

- <TBD: profile names, or None - reason>

Findings:

- <TBD: critique:<slug>#FIND-001 — ticket-owned disposition, or None - no critique yet>

Promotion disposition: <TBD: pending, blocking, completed, deferred, or not_required>
Promotion / deferral rationale: <TBD: what was promoted, why deferred, or why not required>

Promoted / deferred:

Wiki disposition: <TBD: N/A, wiki:<slug>, deferred, or not_required with reason>

# Acceptance Decision

Required before closure when acceptance, accepted risk, or operator provenance
needs to be explicit.

Accepted by:
Accepted at:
Basis:
Residual risks:

# Dependencies

Hard prerequisites belong in frontmatter `depends_on`; explain important context
here when useful.

# Journal

- <UTC timestamp>: <material update>
