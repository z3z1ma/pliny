---
id: evidence:placeholder-validation-guidance-validation
kind: evidence
status: recorded
created_at: 2026-05-03T07:04:42Z
updated_at: 2026-05-03T07:14:50Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:phvalid16
  packet:
    - packet:ralph-ticket-phvalid16-20260503T070234Z
  critique:
    - critique:placeholder-validation-guidance-review
    - critique:placeholder-validation-guidance-rereview
external_refs: {}
---

# Summary

Validation observations for `ticket:phvalid16`, checking that record validation
now includes a saved `.loom` placeholder scan and rule while preserving template
placeholders.

# Procedure

- Inspected the scoped diff for `ticket:phvalid16`.
- Searched records validation guidance for placeholder, TODO/TBD, observed-source,
  template exception, and example-ID wording.
- Ran the corrected saved-record placeholder leakage scan:
  `rg -n '(<[^>[:cntrl:]]+>|\bTODO\b|\bTBD\b|[a-z]+:<[^>]+>|example:[a-z0-9-]+)' .loom --glob '.loom/{constitution,initiatives,research,specs,plans,tickets,critique,wiki,evidence,packets}/**/*.md'`.
- Searched records validation guidance for runtime, schema-engine, command-wrapper,
  generated-index, or template-rewrite additions.
- Ran `git add -N .loom/packets/ralph/20260503T070234Z-ticket-phvalid16-iter-01.md`.
- Ran `git diff --check -- .loom/tickets/20260503-phvalid16-add-placeholder-validation.md .loom/packets/ralph/20260503T070234Z-ticket-phvalid16-iter-01.md .loom/evidence/20260503-placeholder-validation-guidance-validation.md .loom/critique/placeholder-validation-guidance-review.md .loom/critique/placeholder-validation-guidance-rereview.md skills/loom-records/references/validation.md`.

# Artifacts

Scoped changed tracked files:

- `.loom/tickets/20260503-phvalid16-add-placeholder-validation.md`
- `skills/loom-records/references/validation.md`

Scoped new Loom record files:

- `.loom/packets/ralph/20260503T070234Z-ticket-phvalid16-iter-01.md`
- `.loom/evidence/20260503-placeholder-validation-guidance-validation.md`
- `.loom/critique/placeholder-validation-guidance-review.md`
- `.loom/critique/placeholder-validation-guidance-rereview.md`

Targeted observations:

- `skills/loom-records/references/validation.md:18-20` says saved `.loom` records
  should avoid unresolved template placeholders, example IDs, and generic
  TODO/TBD tokens unless the record explicitly documents them as observed source
  text.
- `skills/loom-records/references/validation.md:22-24` says intentional
  placeholders in `skills/**/templates` are template source and are not failures
  of saved-record validation unless copied into saved `.loom` records without
  observed-source framing.
- `skills/loom-records/references/validation.md:70-83` uses `.loom/...`-prefixed
  globs for saved-record spot checks, including missing IDs, missing status, and
  the saved-record placeholder leakage recipe.
- `skills/loom-records/references/validation.md:86-90` requires operator review of
  placeholder scan hits.
- Corrected saved-record placeholder scan result: non-empty output. Representative
  hits came from saved evidence and packet records that explicitly document
  template placeholders, example references, harness output, or scan output as
  observed source text, for example
  `.loom/evidence/20260502-placeholder-safety-validation.md:161`,
  `.loom/evidence/20260502-acceptance-placeholder-validation.md:62`, and
  `.loom/packets/ralph/20260503T022401Z-ticket-pktmeta12-iter-01.md:107`.
  This confirms the corrected recipe traverses saved `.loom` records and exposes
  hits for operator review; it does not establish that the whole workspace is free
  of every unresolved placeholder.
- A targeted search for `runtime|schema engine|command wrapper|generated index|template rewrite`
  returned no matches in the edited validation reference.

`git diff --check` result: passed with no output.

# Supports Claims

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-017`
- `ticket:phvalid16#ACC-001`
- `ticket:phvalid16#ACC-002`
- `ticket:phvalid16#ACC-003`
- `ticket:phvalid16#ACC-004`

# Challenges Claims

None - the observations did not weaken the scoped claims.

# Environment

Commit: `43cd5a384e9d7dcbeb07c279cc150e1cf92990bd` plus uncommitted scoped
`ticket:phvalid16` changes.
Branch: `main`
Runtime: Markdown/static repository; no app runtime.
OS: macOS/Darwin
Relevant config: no generated files, lockfiles, runtime, command wrapper, schema
engine, generated index, or template rewrite observed in the scoped diff.

# Validity

Valid for: the scoped `ticket:phvalid16` diff at 2026-05-03T07:14:50Z.
Recheck when: any scoped file changes before closure or before the commit is
created.

# Limitations

This evidence is structural and textual. The scan recipe is heuristic and still
requires operator review of hits. The corrected scan produced workspace hits; this
evidence records the recipe and representative observed-source hits, not a full
workspace cleanup.

# Result

Records validation now includes a saved `.loom` placeholder leakage scan, a
saved-record rule, an observed-source-text exception, a template-placeholder
exception, and corrected `.loom/...` globs for the adjacent saved-record spot
checks. The scoped diff passes `git diff --check`.

# Interpretation

The evidence supports the ticket's placeholder-validation claims. It does not
close the ticket; mandatory critique and the ticket-owned acceptance decision
remain separate gates.

# Related Records

- `ticket:phvalid16`
- `packet:ralph-ticket-phvalid16-20260503T070234Z`
