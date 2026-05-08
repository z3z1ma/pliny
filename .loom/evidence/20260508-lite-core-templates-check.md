---
id: evidence:lite-core-templates-check
kind: evidence
status: recorded
created_at: 2026-05-08T07:50:31Z
updated_at: 2026-05-08T07:50:31Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:iq03bxg5
  spec:
    - spec:point-of-use-ergonomics-and-mechanical-simplicity
  plan:
    - plan:point-of-use-ergonomics-and-mechanical-simplicity
  packet:
    - packet:ralph:20260508T074551Z-ticket-iq03bxg5-iter-01
external_refs: {}
---

# Summary

This records structural observations for the lite core template implementation in
`ticket:iq03bxg5`. The evidence supports the existence, frontmatter, heading, and
guidance claims for `ticket-lite.md`, `spec-lite.md`, and `evidence-lite.md`.

Evidence records the observations only. The ticket owns acceptance and critique
disposition.

# Procedure

Observed at: 2026-05-08T07:50:31Z

Source state: commit `7cb65c63c90fe53da1c29a10ad51f33aeb290fb2` on branch
`main`, with uncommitted scoped product edits for `ticket:iq03bxg5`, new Loom
planning/ticket/packet records, and unrelated untracked `loom.zip` left untouched.

Procedure:

- Ralph child executed packet
  `packet:ralph:20260508T074551Z-ticket-iq03bxg5-iter-01` and returned
  `Outcome: stop`.
- Parent read the three new lite templates.
- Parent searched the three owning skill files for lite/full guidance and required
  escalation triggers.
- Parent ran scoped whitespace, generic-template diff, status, inventory,
  heading, and package smoke checks.

Expected result:

- `ticket-lite.md`, `spec-lite.md`, and `evidence-lite.md` exist with YAML
  frontmatter and required headings.
- `ticket.md`, `spec.md`, and `evidence.md` remain unchanged full copy targets.
- No `ticket-full.md`, `spec-full.md`, or `evidence-full.md` aliases exist.
- Owning skill guidance explains lite/full choice and all required escalation
  triggers.
- No package-script enforcement is added by this ticket.

Actual observed result:

- The three new lite templates exist.
- The three new lite templates include frontmatter fences at the top of the file.
- Heading scans matched the required section order for each lite template.
- `git diff -- loom-core/skills/loom-tickets/templates/ticket.md loom-core/skills/loom-specs/templates/spec.md loom-core/skills/loom-evidence/templates/evidence.md` produced no output, so generic full templates were unchanged.
- `loom-core/skills/loom-tickets/SKILL.md`, `loom-core/skills/loom-specs/SKILL.md`, and `loom-core/skills/loom-evidence/SKILL.md` mention lite templates, full copy targets, and the required escalation triggers.
- `glob` found no `loom-core/skills/loom-{tickets,specs,evidence}/templates/*-full.md` files.
- `npm run smoke` in `loom-core/` passed.

Procedure verdict / exit code: pass. The smoke check exited successfully; scoped
`git diff --check` produced no output.

# Artifacts

Changed product files observed:

- `loom-core/skills/loom-tickets/SKILL.md`
- `loom-core/skills/loom-tickets/templates/ticket-lite.md`
- `loom-core/skills/loom-specs/SKILL.md`
- `loom-core/skills/loom-specs/templates/spec-lite.md`
- `loom-core/skills/loom-evidence/SKILL.md`
- `loom-core/skills/loom-evidence/templates/evidence-lite.md`

Structural checks observed:

- `glob loom-core/skills/loom-{tickets,specs,evidence}/templates/*-lite.md` found
  the three lite templates.
- `glob loom-core/skills/loom-{tickets,specs,evidence}/templates/*-full.md` found
  no files.
- `grep '^---$|^# ' ticket-lite.md` reported frontmatter fences and exactly:
  `Summary`, `Scope`, `Acceptance`, `Evidence`, `Status / Next Move`, `Journal`.
- `grep '^---$|^# ' spec-lite.md` reported frontmatter fences and exactly:
  `Summary`, `Problem`, `Desired Behavior`, `Requirements`, `Scenarios`,
  `Acceptance`, `Evidence Plan`, `Open Questions`.
- `grep '^---$|^# ' evidence-lite.md` reported frontmatter fences and exactly:
  `Summary`, `Observation`, `Artifacts`, `Supports / Challenges`, `Limits`,
  `Related Records`.
- `git diff --check -- loom-core/skills/loom-tickets loom-core/skills/loom-specs loom-core/skills/loom-evidence` produced no output.
- `git status --short -- loom-core/skills/loom-tickets loom-core/skills/loom-specs loom-core/skills/loom-evidence` showed three modified skill files and three untracked lite templates.
- `npm run smoke` in `loom-core/` returned `ok: true`, `skillCount: 15`,
  `usingLoomReferenceCount: 8`, and `instructionsAreDeduped: true`.

# Raw Artifact Store

- Path: `None - raw command output is small and summarized in this record`.
- Captured artifacts: None.
- Key excerpts / index: The smoke output reported `ok: true`.
- Redaction / sensitivity: No sensitive data observed.
- Retention / tracking: Not applicable.

# Visual / Product Evidence

N/A - this is a Markdown protocol/template change, not UI/product visual work.

# Supports Claims

- Supports `spec:point-of-use-ergonomics-and-mechanical-simplicity#ACC-001` for
  existence, frontmatter, and required headings of the three lite templates.
- Supports `spec:point-of-use-ergonomics-and-mechanical-simplicity#ACC-002` for
  owning skill guidance on lite/full choice and escalation triggers.
- Supports `spec:point-of-use-ergonomics-and-mechanical-simplicity#ACC-003` because
  generic full templates were unchanged.
- Supports `ticket:iq03bxg5#ACC-LOCAL-001`, `ticket:iq03bxg5#ACC-LOCAL-002`, and
  `ticket:iq03bxg5#ACC-LOCAL-003` for lite template body shapes.

# Challenges Claims

None observed.

# Environment

Commit: `7cb65c63c90fe53da1c29a10ad51f33aeb290fb2`

Branch: `main`

Runtime: Node through `npm run smoke` in `loom-core/`

OS: darwin

Relevant config: `loom-core/open-loom-core.mjs` smoke entrypoint

External service / harness / data source when applicable: opencode Ralph child
worker via `packet:ralph:20260508T074551Z-ticket-iq03bxg5-iter-01`

# Validity

Valid for: the uncommitted source state observed at 2026-05-08T07:50:31Z and the
template/guidance claims listed above.

Fresh enough for: mandatory critique of `ticket:iq03bxg5` and ticket acceptance
review after critique disposition.

Recheck when: any of the six changed product files, generic full templates,
package scripts, or governing spec/ticket acceptance changes.

Invalidated by: edits that remove or rename lite templates, change heading shapes,
change generic templates, add full-suffixed aliases, remove escalation guidance,
or add package-script enforcement.

Supersedes / superseded by: None.

# Limitations

- This evidence does not prove final project-wide table removal; existing tables
  in touched skill files were intentionally preserved for later tickets.
- This evidence does not prove `using-loom` compression.
- This evidence does not replace mandatory critique for this high-risk
  protocol-authority ticket.

# Result

The lite core template implementation is structurally present and matches the
ticket/spec section-shape requirements. Generic full templates remain unchanged.
Mandatory critique remains pending.

# Interpretation

The implementation is ready for mandatory critique. Acceptance should not close
until critique findings are recorded and dispositioned by the ticket.

# Related Records

- `ticket:iq03bxg5`
- `spec:point-of-use-ergonomics-and-mechanical-simplicity`
- `plan:point-of-use-ergonomics-and-mechanical-simplicity`
- `packet:ralph:20260508T074551Z-ticket-iq03bxg5-iter-01`
