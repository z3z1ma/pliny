---
id: evidence:spec-contract-grammar-check
kind: evidence
status: recorded
created_at: 2026-05-07T20:25:56Z
updated_at: 2026-05-07T20:25:56Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  tickets:
    - ticket:specgram
  critiques:
    - critique:spec-contract-grammar-review
external_refs: {}
---

# Summary

Observed structural validation and targeted text searches for the `ticket:specgram`
Loom spec/plan guidance changes. This evidence supports the ticket-local
acceptance criteria but does not decide ticket closure.

# Procedure

Observed at: 2026-05-07T20:25:56Z

Source state: branch `main`, commit `076693c`, dirty worktree with scoped changes
under `skills/loom-specs`, `skills/loom-plans`, `.loom/critique`, `.loom/evidence`,
and `.loom/tickets`; unrelated untracked example files existed before validation.

Procedure:

- Ran `git diff --check`.
- Ran `git diff --stat -- skills/loom-specs skills/loom-plans .loom/tickets/20260507-specgram-sharpen-spec-contract-grammar.md`.
- Searched `skills/**/*.md` for `ExecPlan|execplan|OpenAI-style`.
- Searched `skills/**/*.md` for `REQ-001|SCN-001|Rigor Level|Amendment Notes|Contract Review|Self-Orienting Plan Discipline`.
- Performed scoped diff review over changed spec and plan skill surfaces.
- Ran focused critique and re-review for `protocol-change` and `operator-clarity`.

Expected result when applicable: no whitespace errors; no external-specific
`ExecPlan`, `execplan`, or `OpenAI-style` vocabulary in `skills/**/*.md`; new spec
contract grammar and plan boundary surfaces present; critique blockers resolved.

Actual observed result: expected results were observed.

Procedure verdict / exit code: pass for `git diff --check`; targeted search and
diff review results support the scoped claims.

# Artifacts

- `git diff --check`: no output.
- Scoped diff stat: five skill/reference/template files changed with 261
  insertions and 9 deletions before critique-record/evidence-record/ticket updates.
- External-specific vocabulary search for `ExecPlan|execplan|OpenAI-style`: no
  files found under `skills/**/*.md`.
- Contract grammar search found the expected new surfaces in `skills/loom-specs`
  and `skills/loom-plans`.
- Critique record: `critique:spec-contract-grammar-review`.

# Raw Artifact Store

- Path: `None - record summary is sufficient`
- Captured artifacts: None - outputs were small and are summarized above.
- Key excerpts / index: See `# Artifacts`.
- Redaction / sensitivity: No sensitive output observed.
- Retention / tracking: Markdown evidence record only.

# Visual / Product Evidence

N/A - Markdown protocol guidance change.

# Supports Claims

- `ticket:specgram#ACC-001`: requirement/scenario/acceptance grammar appears in
  `skills/loom-specs/SKILL.md`, `skills/loom-specs/references/spec-shape.md`, and
  `skills/loom-specs/templates/spec.md` without converting specs into delivery
  plans.
- `ticket:specgram#ACC-002`: progressive-rigor guidance appears in the spec skill,
  reference, and template.
- `ticket:specgram#ACC-003`: amendment guidance covers added, modified, removed,
  renamed, and superseded behavior, with stable-ID reconciliation guidance.
- `ticket:specgram#ACC-004`: plan wording keeps live execution and acceptance truth
  in tickets/packets and explicitly prevents plan/evidence ownership drift.

# Challenges Claims

None - no challenged ticket acceptance claims remain after critique fixes.

# Environment

Commit: `076693c`

Branch: `main`

Runtime: N/A

OS: macOS / darwin

Relevant config: N/A

External service / harness / data source when applicable: local OpenCode tool
execution and read-only critique subagent output summarized in
`critique:spec-contract-grammar-review`.

# Validity

Valid for: the scoped Markdown diff and targeted searches observed at the source
state above.

Fresh enough for: `ticket:specgram` acceptance review of `ACC-001` through
`ACC-004`.

Recheck when: any changed skill/reference/template/ticket/critique/evidence file
is edited again before acceptance.

Invalidated by: substantive changes to the scoped files, new external-specific
vocabulary in `skills/**/*.md`, or new critique findings.

Supersedes / superseded by: None.

# Limitations

This evidence does not prove rendered Markdown aesthetics, downstream examples,
or every future spec authoring case. It is structural and review evidence for the
specific protocol guidance diff.

# Result

The observed structural checks, targeted searches, diff review, and critique pass
support the ticket-local acceptance criteria for the scoped change.

# Interpretation

The evidence supports acceptance review for `ticket:specgram`. The ticket remains
the owner of acceptance and closure.

# Related Records

- `ticket:specgram`
- `critique:spec-contract-grammar-review`
