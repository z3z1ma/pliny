---
id: ticket:phvalid16
kind: ticket
status: closed
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-03T06:20:11Z
updated_at: 2026-05-03T07:14:50Z
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
  critique:
    - critique:placeholder-validation-guidance-review
    - critique:placeholder-validation-guidance-rereview
external_refs: {}
depends_on:
  - ticket:shipacc1
---

# Summary

Add saved-record placeholder validation guidance.

# Context

Templates intentionally use `<TBD: ...>` placeholders, but saved `.loom` records
should not retain unresolved template placeholders unless explicitly documenting
observed source text.

# Why Now

Placeholder leakage can make a saved record look valid while carrying fake truth.

# Scope

- Add a placeholder scan recipe to record validation guidance.
- State the saved-record rule and exception for documented observed text.
- Preserve intentional template placeholders.

# Out Of Scope

- Do not add a validator runtime or schema engine.
- Do not rewrite all templates.

# Acceptance Criteria

- ACC-001: Validation guidance includes a saved `.loom` placeholder scan.
- ACC-002: Guidance states saved records must not contain unresolved template
  placeholders, example IDs, or generic TODO/TBD tokens unless explicitly
  documented as observed source text.
- ACC-003: Guidance does not make intentional template placeholders failures.
- ACC-004: Evidence records targeted placeholder validation searches and
  `git diff --check`.
- ACC-005: Mandatory critique passes with no unresolved findings.

# Coverage

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-017`
- `ticket:phvalid16#ACC-001`
- `ticket:phvalid16#ACC-002`
- `ticket:phvalid16#ACC-003`
- `ticket:phvalid16#ACC-004`
- `ticket:phvalid16#ACC-005`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-017` | `evidence:placeholder-validation-guidance-validation` | `critique:placeholder-validation-guidance-rereview` | supported |
| `ticket:phvalid16#ACC-001` | `evidence:placeholder-validation-guidance-validation` | `critique:placeholder-validation-guidance-rereview` | supported |
| `ticket:phvalid16#ACC-002` | `evidence:placeholder-validation-guidance-validation` | `critique:placeholder-validation-guidance-rereview` | supported |
| `ticket:phvalid16#ACC-003` | `evidence:placeholder-validation-guidance-validation` | `critique:placeholder-validation-guidance-rereview` | supported |
| `ticket:phvalid16#ACC-004` | `evidence:placeholder-validation-guidance-validation` | `critique:placeholder-validation-guidance-review#FIND-001` resolved; `critique:placeholder-validation-guidance-rereview` | supported |
| `ticket:phvalid16#ACC-005` | `evidence:placeholder-validation-guidance-validation` | `critique:placeholder-validation-guidance-review#FIND-001` resolved; `critique:placeholder-validation-guidance-rereview` | supported |

# Execution Notes

Likely touched file: `skills/loom-records/references/validation.md`.

# Blockers

None.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to `ticket:bootdoc17`.

Ralph packet `packet:ralph-ticket-phvalid16-20260503T070234Z` completed in
scope, evidence was recorded, initial critique finding was resolved, mandatory
re-critique passed with no findings, and acceptance is complete.

# Route Readiness

Acceptance review readiness:
Evidence `evidence:placeholder-validation-guidance-validation`, resolved initial
finding `critique:placeholder-validation-guidance-review#FIND-001`, and mandatory
re-critique `critique:placeholder-validation-guidance-rereview` support closure.

# Evidence

Recorded:

- `evidence:placeholder-validation-guidance-validation`

The evidence records the corrected saved-record placeholder scan, targeted
searches for placeholder scan, saved record rule, template exception, and `git
diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: validation guidance controls closure honesty.

Required critique profiles:

- validation-honesty
- template-safety
- workflow-boundary

Findings:

- `critique:placeholder-validation-guidance-review#FIND-001` - resolved by
  correcting the saved-record placeholder scan glob to prefix `.loom/` and
  updating adjacent saved-record validation recipes plus
  `evidence:placeholder-validation-guidance-validation` with the corrected
  command and observed non-empty output.
- `critique:placeholder-validation-guidance-rereview` - no findings; mandatory
  re-critique passed.

Disposition status: completed

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- Saved-record placeholder validation guidance was promoted into
  `skills/loom-records/references/validation.md`.

Deferred / not-required rationale:

No separate wiki, research, spec, constitution, or memory record is needed. The
durable lesson is local to record validation guidance.

# Wiki Disposition

N/A - no separate wiki promotion route. The accepted explanation lives in record
validation guidance.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-03T07:14:50Z
Basis: Ralph packet `packet:ralph-ticket-phvalid16-20260503T070234Z`; evidence
`evidence:placeholder-validation-guidance-validation`; initial critique
`critique:placeholder-validation-guidance-review` with `FIND-001` resolved;
mandatory re-critique `critique:placeholder-validation-guidance-rereview` with no
findings.
Residual risks: Placeholder detection remains heuristic and depends on operator
review of hits. Evidence is structural/textual, appropriate for Markdown protocol
validation guidance.

# Dependencies

- `ticket:shipacc1`

# Journal

- 2026-05-03T06:20:11Z: Created from third-pass audit finding 5.
- 2026-05-03T07:02:34Z: Started Ralph iteration
  `packet:ralph-ticket-phvalid16-20260503T070234Z` from clean `main` at
  `43cd5a3`.
- 2026-05-03T07:04:42Z: Ralph iteration consumed. Product edit landed inside
  packet write scope, `evidence:placeholder-validation-guidance-validation`
  recorded, and ticket moved to `review_required` for mandatory critique.
- 2026-05-03T07:10:28Z: Initial mandatory critique
  `critique:placeholder-validation-guidance-review` returned `changes_required`
  because the placeholder scan glob missed saved `.loom` paths. Parent corrected
  the scan glob and evidence, and kept the ticket in `review_required` for
  re-review.
- 2026-05-03T07:11:55Z: Parent also corrected the adjacent missing-ID and
  missing-status saved-record globs to use the same `.loom/...` path prefix so the
  validation reference does not preserve contradictory no-op recipes.
- 2026-05-03T07:14:50Z: Mandatory re-critique
  `critique:placeholder-validation-guidance-rereview` passed with no findings.
  Parent recorded retrospective / promotion disposition and accepted closure.
