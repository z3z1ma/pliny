---
id: evidence:ship-drive-decoupling-validation
kind: evidence
status: recorded
created_at: 2026-05-03T17:02:36Z
updated_at: 2026-05-03T17:04:52Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:shipdec2
external_refs: {}
---

# Summary

Structural validation for decoupling `loom-ship` precondition wording from
`loom-drive` hard preflight gates.

# Procedure

Observed at: 2026-05-03T17:02:36Z

Source state: dirty working tree on `main` with the fourth-pass audit patch and
the `ticket:shipdec2` follow-up correction.

Procedure:

- Searched `skills/loom-ship` for stale drive-gate wording and new ship-owned
  precondition wording.
- Searched `skills/loom-drive/references/checkpoint-resume-protocol.md` for
  drive-owned `ship` gate language.
- Ran `git diff --check` for tracked diff whitespace.
- Ran a trailing-whitespace scan for the new `ticket:shipdec2` record.
- Parsed frontmatter for `ticket:shipdec2` and `loom-ship/SKILL.md`.

Expected result when applicable: `loom-ship` uses ship-owned precondition wording
and mentions drive gates only conditionally when `loom-drive` is the parent;
`loom-drive` still gates `ship` inside drive; whitespace and frontmatter checks
pass.

Actual observed result: checks matched expectations.

Procedure verdict / exit code: pass.

# Artifacts

- `skills/loom-ship` wording search found ship-owned preconditions and conditional
  drive-parent language; no unconditional "run the drive hard preflight gates"
  wording remained.
- `skills/loom-drive/references/checkpoint-resume-protocol.md` search found drive
  hard gates still run before `ship` inside drive-managed work.
- `git diff --check`: exit 0, no output.
- New ticket trailing-whitespace scan: `checked 1 new shipdec2 record for trailing
  whitespace`.
- Frontmatter parse: `parsed 2 frontmatter blocks`.

# Supports Claims

- Supports `ticket:shipdec2#ACC-001`.
- Supports `ticket:shipdec2#ACC-002`.
- Supports `ticket:shipdec2#ACC-003`.
- Supports `ticket:shipdec2#ACC-004` through mandatory critique
  `critique:ship-drive-decoupling-review`.

# Challenges Claims

None observed.

# Environment

Commit: current HEAD not re-queried for this narrow follow-up; same dirty working
tree session as the fourth-pass audit patch.

Branch: `main`

Runtime: no app runtime or automated test suite; structural Markdown validation
only.

OS: macOS via Darwin shell environment.

Relevant config: dirty working tree, no commit created.

External service / harness / data source when applicable: none.

# Validity

Valid for: the dirty working tree at observation time and the narrow
`loom-ship`/`loom-drive` wording correction.

Fresh enough for: mandatory critique input for `ticket:shipdec2`.

Recheck when: `skills/loom-ship`, `skills/loom-drive` gate wording, or linked
ticket/evidence/critique records change before acceptance.

Invalidated by: new edits that reintroduce unconditional drive-gate requirements
inside `loom-ship` or remove drive's parent-workflow gate authority.

Supersedes / superseded by: none.

# Limitations

This is textual evidence. It does not prove future agents will choose the correct
workflow under pressure.

# Result

The observed corpus now keeps `loom-ship` independent while preserving conditional
drive gate requirements when drive invokes ship.

# Interpretation

The correction is ready for mandatory critique.

# Related Records

- `ticket:shipdec2`
