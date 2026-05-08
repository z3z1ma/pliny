---
id: evidence:using-loom-compression-check
kind: evidence
status: recorded
created_at: 2026-05-08T08:07:10Z
updated_at: 2026-05-08T08:07:10Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:nlzaqhrm
  spec:
    - spec:point-of-use-ergonomics-and-mechanical-simplicity
  packet:
    - packet:ralph:20260508T075921Z-ticket-nlzaqhrm-iter-01a-entry-outer
    - packet:ralph:20260508T075921Z-ticket-nlzaqhrm-iter-01b-authority-trust
    - packet:ralph:20260508T075921Z-ticket-nlzaqhrm-iter-01c-ralph-critique
    - packet:ralph:20260508T075921Z-ticket-nlzaqhrm-iter-01d-tools-validation
external_refs: {}
---

# Summary

This records parent-side evidence for the parallel `using-loom` compression pass
under `ticket:nlzaqhrm`. Four parallel Ralph packets compressed non-overlapping
file groups. The combined word count is inside the 5,000 to 6,000 acceptance
band.

Evidence records observed checks only. The ticket owns acceptance, and critique
owns the review verdict.

# Procedure

Observed at: 2026-05-08T08:07:10Z

Source state: commit `7cb65c63c90fe53da1c29a10ad51f33aeb290fb2` on branch
`main`, with uncommitted product edits from `ticket:iq03bxg5`, uncommitted
parallel `using-loom` compression edits from `ticket:nlzaqhrm`, current Loom
records, and unrelated untracked `loom.zip` left untouched.

Procedure:

- Superseded unlaunched single-worker packet
  `packet:ralph:20260508T075804Z-ticket-nlzaqhrm-iter-01`.
- Launched four parallel Ralph workers with non-overlapping write scopes.
- Gathered child before/after word counts and invariant checklists.
- Ran parent `wc -l -w` across `using-loom/SKILL.md` plus all eight ordered
  references.
- Searched for essential invariant terms across `loom-core/skills/using-loom`.
- Searched for Markdown pipe-table rows in `loom-core/skills/using-loom`.
- Ran scoped `git diff --check` for `loom-core/skills/using-loom`.
- Ran `npm run smoke` in `loom-core/`.

Expected result:

- The full `using-loom` doctrine remains the entry skill plus eight ordered
  references.
- Total word count lands inside 5,000 to 6,000 words.
- Essential invariants remain present.
- No pipe-table rows are introduced or retained in `using-loom`.
- Package smoke still reports the eight ordered references and succeeds.

Actual observed result:

- `wc -l -w` reported 922 lines and 5,750 words total.
- The eight ordered references remain present and smoke output still reports
  `usingLoomReferenceCount: 8`, `instructionCount: 8`, and
  `instructionsAreDeduped: true`.
- Invariant search found terms for owner-layer truth, instruction authority,
  tickets as live ledger, Ralph, evidence, critique, wiki, retrospective,
  validation, trust, secrets, filesystem, runtime, and packets.
- `grep '^\|.*\|$'` equivalent search in `using-loom` found no pipe-table rows.
- `git diff --check -- loom-core/skills/using-loom` produced no output.
- `npm run smoke` in `loom-core/` passed with `ok: true`.

Procedure verdict / exit code: pass. Mandatory critique remains required before
ticket closure.

# Artifacts

Baseline word count from the packet:

- `using-loom/SKILL.md`: 778 words.
- `01-core-identity.md`: 1042 words.
- `02-truth-and-authority.md`: 1591 words.
- `03-outer-loop.md`: 1016 words.
- `04-ralph-inner-loop.md`: 1499 words.
- `05-critique-and-wiki.md`: 1480 words.
- `06-filesystem-and-tooling.md`: 930 words.
- `07-validation-and-honesty.md`: 910 words.
- `08-trust-boundaries.md`: 565 words.
- Total: 9811 words.

Observed compressed word count:

- `using-loom/SKILL.md`: 384 words.
- `01-core-identity.md`: 578 words.
- `02-truth-and-authority.md`: 946 words.
- `03-outer-loop.md`: 686 words.
- `04-ralph-inner-loop.md`: 826 words.
- `05-critique-and-wiki.md`: 826 words.
- `06-filesystem-and-tooling.md`: 498 words.
- `07-validation-and-honesty.md`: 652 words.
- `08-trust-boundaries.md`: 354 words.
- Total: 5750 words.

Parallel Ralph slices:

- `packet:ralph:20260508T075921Z-ticket-nlzaqhrm-iter-01a-entry-outer` returned
  `stop`; slice word count went from 2836 to 1648.
- `packet:ralph:20260508T075921Z-ticket-nlzaqhrm-iter-01b-authority-trust`
  returned `stop`; slice word count went from 2156 to 1300.
- `packet:ralph:20260508T075921Z-ticket-nlzaqhrm-iter-01c-ralph-critique`
  returned `stop`; slice word count went from 2979 to 1652.
- `packet:ralph:20260508T075921Z-ticket-nlzaqhrm-iter-01d-tools-validation`
  returned `stop`; slice word count went from 1840 to 1150.

Smoke output excerpt:

- `ok: true`
- `usingLoomReferenceCount: 8`
- `instructionCount: 8`
- `instructionsAreDeduped: true`
- `skillCount: 15`

# Raw Artifact Store

- Path: `None - command outputs are summarized in this record`.
- Captured artifacts: None.
- Key excerpts / index: word-count totals and smoke output above.
- Redaction / sensitivity: No sensitive data observed.
- Retention / tracking: Not applicable.

# Visual / Product Evidence

N/A - this is doctrine text, not UI/product visual work.

# Supports Claims

- Supports `spec:point-of-use-ergonomics-and-mechanical-simplicity#ACC-004` for
  word-count reduction into the accepted band and preservation of ordered
  references.
- Supports `ticket:nlzaqhrm#ACC-LOCAL-001` because before/after word counts are
  recorded.
- Partially supports `ticket:nlzaqhrm#ACC-LOCAL-002` because invariant terms were
  observed; mandatory critique must still judge doctrine completeness and clarity.

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

Valid for: the uncommitted source state observed at 2026-05-08T08:07:10Z and the
word-count/order/smoke claims listed above.

Fresh enough for: mandatory critique of `ticket:nlzaqhrm` and ticket acceptance
review after critique disposition.

Recheck when: any `loom-core/skills/using-loom/**` file, package smoke behavior,
or the governing word-count acceptance band changes.

Invalidated by: edits that move total word count outside the accepted band without
rationale, remove ordered references, remove essential invariants, or break core
smoke.

Supersedes / superseded by: None.

# Limitations

- This evidence does not prove operator comprehension; it records structural and
  text-presence checks.
- Invariant term search cannot prove doctrine sufficiency by itself; mandatory
  critique is required before closure.
- This evidence does not cover table removal outside `using-loom`.

# Result

The `using-loom` doctrine is compressed from 9,811 to 5,750 words while retaining
the entry skill plus eight ordered reference architecture and passing core smoke.

# Interpretation

The compression pass is ready for mandatory critique focused on doctrine
completeness, protocol authority, and operator clarity.

# Related Records

- `ticket:nlzaqhrm`
- `spec:point-of-use-ergonomics-and-mechanical-simplicity`
- `plan:point-of-use-ergonomics-and-mechanical-simplicity`
- `packet:ralph:20260508T075921Z-ticket-nlzaqhrm-iter-01a-entry-outer`
- `packet:ralph:20260508T075921Z-ticket-nlzaqhrm-iter-01b-authority-trust`
- `packet:ralph:20260508T075921Z-ticket-nlzaqhrm-iter-01c-ralph-critique`
- `packet:ralph:20260508T075921Z-ticket-nlzaqhrm-iter-01d-tools-validation`
