---
id: evidence:root-doc-table-removal-check
kind: evidence
status: recorded
created_at: 2026-05-08T15:49:00Z
updated_at: 2026-05-08T15:49:00Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:57rm2fmx
  spec:
    - spec:point-of-use-ergonomics-and-mechanical-simplicity
external_refs: {}
---

# Summary

This records evidence for removing Markdown pipe tables from root public docs
under `ticket:57rm2fmx` and adding a brief public note about lite templates versus
generic full templates.

# Procedure

Observed at: 2026-05-08T15:49:00Z

Source state: commit `7cb65c63c90fe53da1c29a10ad51f33aeb290fb2` on branch
`main`, with uncommitted product edits from prior closed tickets, current root-doc
edits, current Loom records, unrelated untracked `loom.zip`, and unrelated
untracked `examples/00-todo-app/**` left untouched.

Procedure:

- Inspected `ticket:57rm2fmx` and the active plan/spec constraints.
- Scanned `README.md`, `PROTOCOL.md`, and `ARCHITECTURE.md` for Markdown
  pipe-table rows before editing.
- Converted root-doc tables in `README.md` and `PROTOCOL.md` to bullets or
  orientation lists while preserving row content by default.
- Added a concise README note that core skills ship explicit lite ticket/spec/evidence
  templates for small, low-risk work while generic `ticket.md`, `spec.md`, and
  `evidence.md` remain the full templates.
- Ran targeted root-doc table scan, lite/full note search, diff whitespace check,
  changed-file review, and diff stat.

Expected result:

- `README.md`, `PROTOCOL.md`, and `ARCHITECTURE.md` contain no Markdown
  pipe-table rows.
- Public docs briefly mention lite templates and generic full templates without
  redefining skill-owned behavior.
- No table rows are deleted without duplicate/stale rationale.
- No `loom-core`, `loom-playbooks`, examples, package scripts, or automation files
  are touched by this root-doc ticket.

Actual observed result:

- `grep '^\s*\|.*\|\s*$'` equivalent search over `README.md`, `PROTOCOL.md`, and
  `ARCHITECTURE.md` found no files.
- Targeted README search found the lite/full note at the `Templates are reasoning
  tools` section.
- `git diff --check -- README.md PROTOCOL.md ARCHITECTURE.md ...` produced no
  output.
- `git diff --name-only -- README.md PROTOCOL.md ARCHITECTURE.md` listed only
  `README.md` and `PROTOCOL.md`.
- `git diff --stat -- README.md PROTOCOL.md ARCHITECTURE.md` reported 2 files
  changed, 151 insertions, and 108 deletions.
- `ARCHITECTURE.md` had no matching table rows and was not changed.
- No rows were deleted as stale or duplicate; table header/separator syntax was
  removed as part of conversion.

Procedure verdict / exit code: pass for structural root-doc table removal and
brief lite/full public framing. Critique remains recommended before ticket closure
because public docs shape first impressions.

# Artifacts

Root public-doc changes:

- `README.md`: quick navigation, product benefits, layer/support lists, work
  routing orientation, adjacent-tool comparison, skill map, and lite/full template
  note.
- `PROTOCOL.md`: transaction-state, owner/route/transport, and claim-coverage
  lists.
- `ARCHITECTURE.md`: no table rows found and no changes made.

Final observed checks:

- `grep '^\s*\|.*\|\s*$'` over root public docs: no files found.
- README lite/full note search: found.
- `git diff --check -- README.md PROTOCOL.md ARCHITECTURE.md`: no output.

# Raw Artifact Store

- Path: `None - command outputs are summarized in this record`.
- Captured artifacts: None.
- Key excerpts / index: README note says generic `ticket.md`, `spec.md`, and
  `evidence.md` names remain the full templates.
- Redaction / sensitivity: No sensitive data observed.
- Retention / tracking: Not applicable.

# Visual / Product Evidence

N/A - this is Markdown public-document structure, not UI/product visual work.

# Supports Claims

- Supports `spec:point-of-use-ergonomics-and-mechanical-simplicity#ACC-005` for
  the root public-doc portion.
- Supports `ticket:57rm2fmx#ACC-LOCAL-001` because the root-doc table scan found
  no pipe-table rows.
- Supports `ticket:57rm2fmx#ACC-LOCAL-002` because README briefly mentions lite
  templates and the generic full template names while pointing selection behavior
  back to owning skills.

# Challenges Claims

None observed.

# Environment

Commit: `7cb65c63c90fe53da1c29a10ad51f33aeb290fb2`

Branch: `main`

Runtime: N/A - no package/runtime check is required for Markdown-only root docs.

OS: darwin

Relevant config: N/A

External service / harness / data source when applicable: OpenCode local editing
session.

# Validity

Valid for: the uncommitted source state observed at 2026-05-08T15:49:00Z and the
root public-doc table-removal claim.

Fresh enough for: critique and acceptance review of `ticket:57rm2fmx`.

Recheck when: any of `README.md`, `PROTOCOL.md`, or `ARCHITECTURE.md` changes
before ticket closure.

Invalidated by: new or restored Markdown pipe tables in root public docs or later
discovery that row content was deleted without rationale.

Supersedes / superseded by: None.

# Limitations

- This evidence does not cover product-surface table removal in `loom-core` or
  `loom-playbooks`; those have separate evidence records.
- This evidence does not prove public-doc prose quality beyond structural checks
  and source comparison; critique should review representative framing.

# Result

No Markdown pipe-table rows remain in root public docs, no rows were deleted as
stale or duplicate, and README contains a brief lite/full template note that keeps
behavior ownership in core skills.

# Interpretation

The root public-doc table-removal implementation is structurally ready for
critique and ticket acceptance review.

# Related Records

- `ticket:57rm2fmx`
- `spec:point-of-use-ergonomics-and-mechanical-simplicity`
