---
id: evidence:playbook-table-removal-check
kind: evidence
status: recorded
created_at: 2026-05-08T15:40:41Z
updated_at: 2026-05-08T15:45:58Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:xulgzs52
  spec:
    - spec:point-of-use-ergonomics-and-mechanical-simplicity
  packet:
    - packet:ralph:20260508T153613Z-ticket-xulgzs52-iter-01a-engineering-playbooks
    - packet:ralph:20260508T153613Z-ticket-xulgzs52-iter-01b-product-ui-performance
    - packet:ralph:20260508T153613Z-ticket-xulgzs52-iter-01c-drive-ship-git-docs
    - packet:ralph:20260508T153613Z-ticket-xulgzs52-iter-01d-support-authoring-security
external_refs: {}
---

# Summary

This records evidence for removing Markdown pipe tables from the
`loom-playbooks` product surface under `ticket:xulgzs52`. Four parallel Ralph
packets converted tables in non-overlapping file groups to non-table structures.

# Procedure

Observed at: 2026-05-08T15:40:41Z

Source state: commit `7cb65c63c90fe53da1c29a10ad51f33aeb290fb2` on branch
`main`, with uncommitted product edits from prior closed tickets, current
playbook table-removal edits, current Loom records, unrelated untracked
`loom.zip`, and unrelated untracked `examples/00-todo-app/**` left untouched.

Procedure:

- Ran initial table scans over `loom-playbooks` to identify table-bearing files.
- Compiled four parallel Ralph packets with exact non-overlapping file lists.
- Each child converted scoped tables to label-led bullets or clearer non-table
  structures, preserving rows by default.
- Parent ran whole-playbook pipe-table scan, diff whitespace check, smoke check,
  diff stat, and scoped changed-file review.

Expected result:

- `loom-playbooks` contains no Markdown pipe-table rows.
- No table rows are deleted without rationale.
- Playbook smoke still passes.
- Rewrites stay inside `loom-playbooks` and do not touch `loom-core`, root docs,
  examples, package scripts, or dogfood history.

Actual observed result:

- `grep '^\s*\|.*\|\s*$'` equivalent search over `loom-playbooks` found no
  files.
- `git diff --check -- loom-playbooks` produced no output.
- `npm run smoke` in `loom-playbooks/` passed with `ok: true`,
  `doesNotPreloadCoreDoctrine: true`, `skillCount: 22`, and
  `skillPathsAreDeduped: true`.
- All four child workers reported `Outcome: stop`.
- All four child workers reported deleted rows: none.
- `git diff --name-only -- loom-playbooks` listed the 36 scoped playbook files
  touched by the four packets.
- After critique follow-up, targeted stale table-terminology scans over the cited
  `loom-git` and `loom-drive` references found no matches, `git diff --check --
  loom-playbooks ...` produced no output, and `npm run smoke` in
  `loom-playbooks/` passed again with `ok: true`.

Procedure verdict / exit code: pass for structural table removal and the
post-critique terminology fix.

# Artifacts

Initial table-bearing file groups were partitioned into:

- Engineering playbooks packet: architecture, CI/CD, code review, debugging,
  incremental implementation, and TDD surfaces.
- Product/UI/performance packet: codemap, performance, product discovery,
  simplification, spike, and UI browser surfaces.
- Drive/ship/Git/docs packet: docs sync, drive, Git, and ship surfaces.
- Support/authoring/security packet: agent orchestration, context engineering,
  migration, security, skill authoring, and source grounding surfaces.

Final observed checks:

- `grep '^\s*\|.*\|\s*$'` over `loom-playbooks`: no files found.
- `git diff --check -- loom-playbooks`: no output.
- `npm run smoke` in `loom-playbooks`: `ok: true`.
- `git diff --stat -- loom-playbooks`: 36 files changed, 531 insertions, 305
  deletions.

# Raw Artifact Store

- Path: `None - command outputs are summarized in this record`.
- Captured artifacts: None.
- Key excerpts / index: smoke output reported `ok: true` and `skillCount: 22`.
- Redaction / sensitivity: No sensitive data observed.
- Retention / tracking: Not applicable.

# Visual / Product Evidence

N/A - this is Markdown product-surface structure, not UI/product visual work.

# Supports Claims

- Supports `spec:point-of-use-ergonomics-and-mechanical-simplicity#ACC-005` for
  the `loom-playbooks` portion.
- Supports `ticket:xulgzs52#ACC-LOCAL-001` because the whole-playbook table scan
  found no pipe-table rows.
- Supports `ticket:xulgzs52#ACC-LOCAL-002` because all child workers reported no
  deleted rows.

# Challenges Claims

None observed.

# Environment

Commit: `7cb65c63c90fe53da1c29a10ad51f33aeb290fb2`

Branch: `main`

Runtime: Node through `npm run smoke` in `loom-playbooks/`

OS: darwin

Relevant config: `loom-playbooks/open-loom-playbooks.mjs` smoke entrypoint

External service / harness / data source when applicable: four opencode Ralph
child workers launched from the listed packet records.

# Validity

Valid for: the uncommitted source state observed at 2026-05-08T15:40:41Z and the
`loom-playbooks` table-removal claim.

Fresh enough for: acceptance review of `ticket:xulgzs52` after
`critique:playbook-table-removal-review`.

Recheck when: any `loom-playbooks/**/*.md` file changes before ticket closure.

Invalidated by: new or restored Markdown pipe tables in `loom-playbooks`, failing
playbook smoke, or later discovery that row content was deleted without rationale.

Supersedes / superseded by: None.

# Limitations

- This evidence does not cover `loom-core` or root public docs.
- This evidence does not prove semantic equivalence beyond structural checks and
  child reports; critique should review representative diffs.

# Result

No Markdown pipe-table rows remain in `loom-playbooks`, no rows were reported
deleted, and playbook smoke passes.

# Interpretation

The playbook table-removal implementation is structurally ready for critique and
ticket acceptance review.

# Related Records

- `ticket:xulgzs52`
- `spec:point-of-use-ergonomics-and-mechanical-simplicity`
- `packet:ralph:20260508T153613Z-ticket-xulgzs52-iter-01a-engineering-playbooks`
- `packet:ralph:20260508T153613Z-ticket-xulgzs52-iter-01b-product-ui-performance`
- `packet:ralph:20260508T153613Z-ticket-xulgzs52-iter-01c-drive-ship-git-docs`
- `packet:ralph:20260508T153613Z-ticket-xulgzs52-iter-01d-support-authoring-security`
