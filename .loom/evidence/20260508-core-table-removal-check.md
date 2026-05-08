---
id: evidence:core-table-removal-check
kind: evidence
status: recorded
created_at: 2026-05-08T08:17:20Z
updated_at: 2026-05-08T08:17:20Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:58h4o1qo
  spec:
    - spec:point-of-use-ergonomics-and-mechanical-simplicity
  packet:
    - packet:ralph:20260508T081302Z-ticket-58h4o1qo-iter-01a-records
    - packet:ralph:20260508T081302Z-ticket-58h4o1qo-iter-01b-ticket-spec-plan
    - packet:ralph:20260508T081302Z-ticket-58h4o1qo-iter-01c-owner-skills
    - packet:ralph:20260508T081302Z-ticket-58h4o1qo-iter-01d-ralph-workspace
external_refs: {}
---

# Summary

This records evidence for removing Markdown pipe tables from the `loom-core`
product surface under `ticket:58h4o1qo`. Four parallel Ralph packets converted
tables in non-overlapping file groups to non-table structures.

# Procedure

Observed at: 2026-05-08T08:17:20Z

Source state: commit `7cb65c63c90fe53da1c29a10ad51f33aeb290fb2` on branch
`main`, with uncommitted product edits from prior closed tickets, current core
table-removal edits, current Loom records, and unrelated untracked `loom.zip`
left untouched.

Procedure:

- Ran initial `rg -c '^\|.*\|$' loom-core` and `rg -l '^\|.*\|$' loom-core` to
  identify remaining core Markdown table rows and files.
- Compiled four parallel Ralph packets with exact non-overlapping file lists.
- Each child converted scoped tables to label-led bullets or clearer non-table
  structures, preserving rows by default.
- Parent ran whole-core pipe-table scan, diff whitespace check, smoke check, diff
  stat, and scoped status review.

Expected result:

- `loom-core` contains no Markdown pipe-table rows.
- No table rows are deleted without rationale.
- Core smoke still passes.
- Rewrites stay inside `loom-core` and do not touch playbooks, root docs,
  examples, `.loom` history, or package scripts.

Actual observed result:

- `grep '^\s*\|.*\|\s*$'` equivalent search over `loom-core` found no files.
- `git diff --check -- loom-core` produced no output.
- `npm run smoke` in `loom-core/` passed with `ok: true`,
  `usingLoomReferenceCount: 8`, `instructionCount: 8`, and `skillCount: 15`.
- All four child workers reported `Outcome: stop`.
- All four child workers reported deleted rows: none.
- The scoped diff is limited to `loom-core` product files, including prior
  template and `using-loom` changes already accepted by their tickets.

Procedure verdict / exit code: pass for structural table removal. Critique remains
recommended before ticket closure because many core guidance surfaces changed.

# Artifacts

Initial table-bearing file groups were partitioned into:

- Records references packet: `loom-records` skill and references.
- Ticket/spec/plan packet: ticket, spec, and plan skills, templates, and local
  execution / plan-shape references.
- Owner-skills packet: constitution, critique, evidence, initiatives, memory,
  research, retrospective, and wiki surfaces.
- Ralph/workspace packet: Ralph skill/template and workspace skill/routing catalog.

Final observed checks:

- `grep '^\s*\|.*\|\s*$'` over `loom-core`: no files found.
- `git diff --check -- loom-core`: no output.
- `npm run smoke` in `loom-core`: `ok: true`.

# Raw Artifact Store

- Path: `None - command outputs are summarized in this record`.
- Captured artifacts: None.
- Key excerpts / index: smoke output reported `ok: true`.
- Redaction / sensitivity: No sensitive data observed.
- Retention / tracking: Not applicable.

# Visual / Product Evidence

N/A - this is Markdown product-surface structure, not UI/product visual work.

# Supports Claims

- Supports `spec:point-of-use-ergonomics-and-mechanical-simplicity#ACC-005` for
  the `loom-core` portion.
- Supports `ticket:58h4o1qo#ACC-LOCAL-001` because the whole-core table scan found
  no pipe-table rows.
- Supports `ticket:58h4o1qo#ACC-LOCAL-002` because all child workers reported no
  deleted rows.

# Challenges Claims

None observed.

# Environment

Commit: `7cb65c63c90fe53da1c29a10ad51f33aeb290fb2`

Branch: `main`

Runtime: Node through `npm run smoke` in `loom-core/`

OS: darwin

Relevant config: `loom-core/open-loom-core.mjs` smoke entrypoint

External service / harness / data source when applicable: four opencode Ralph
child workers launched from the listed packet records.

# Validity

Valid for: the uncommitted source state observed at 2026-05-08T08:17:20Z and the
`loom-core` table-removal claim.

Fresh enough for: critique and acceptance review of `ticket:58h4o1qo`.

Recheck when: any `loom-core/**/*.md` file changes before ticket closure.

Invalidated by: new or restored Markdown pipe tables in `loom-core`, failing core
smoke, or later discovery that row content was deleted without rationale.

Supersedes / superseded by: None.

# Limitations

- This evidence does not cover `loom-playbooks` or root public docs.
- This evidence does not prove semantic equivalence beyond structural checks and
  child reports; critique should review representative diffs.

# Result

No Markdown pipe-table rows remain in `loom-core`, no rows were reported deleted,
and core smoke passes.

# Interpretation

The core table-removal implementation is structurally ready for critique and
ticket acceptance review.

# Related Records

- `ticket:58h4o1qo`
- `spec:point-of-use-ergonomics-and-mechanical-simplicity`
- `packet:ralph:20260508T081302Z-ticket-58h4o1qo-iter-01a-records`
- `packet:ralph:20260508T081302Z-ticket-58h4o1qo-iter-01b-ticket-spec-plan`
- `packet:ralph:20260508T081302Z-ticket-58h4o1qo-iter-01c-owner-skills`
- `packet:ralph:20260508T081302Z-ticket-58h4o1qo-iter-01d-ralph-workspace`
