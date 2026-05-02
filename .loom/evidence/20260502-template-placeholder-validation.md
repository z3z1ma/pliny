---
id: evidence:template-placeholder-validation
kind: evidence
status: recorded
created_at: 2026-05-02T20:40:40Z
updated_at: 2026-05-02T20:40:40Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:tmplph8x
  packet:
    - packet:ralph-ticket-tmplph8x-20260502T203733Z
external_refs: {}
---

# Summary

Observed high-risk placeholder patterns in `skills/**/templates/*.md` before and
after the placeholder-hardening edit for `ticket:tmplph8x`.

# Procedure

Before editing, ran targeted `rg` scans over `skills` with `-g "**/templates/*.md"`
for:

- `ACC-001`
- `low \| medium \| high`
- `open \| withdrawn`
- `<[A-Za-z][^>]*>`
- `\|`

After editing, reran those scans, added an empty write-scope check, and ran
explicit `<TBD` and `git diff --check` checks.

# Artifacts

## Before observations

Command: `rg -n "ACC-001" -g "**/templates/*.md" "skills"`

Result:

```text
skills/loom-tickets/templates/ticket.md:49:- ACC-001: The bounded change produces the intended observable result.
skills/loom-tickets/templates/ticket.md:58:- Use `spec:<slug>#ACC-001` for spec-owned acceptance.
skills/loom-tickets/templates/ticket.md:59:- Use `ticket:<token>#ACC-001` for ticket-local acceptance criteria owned in
skills/loom-specs/templates/spec.md:45:- ACC-001: Given the relevant precondition, the expected outcome is observable
```

Observation: two `ACC-001` occurrences were generic saveable acceptance content;
the other two were clearly instructional references.

Command: `rg -n "low \| medium \| high" -g "**/templates/*.md" "skills"`

Result:

```text
skills/loom-critique/templates/critique.md:48:Severity: low | medium | high
skills/loom-critique/templates/critique.md:49:Confidence: low | medium | high
skills/loom-tickets/templates/ticket.md:129:Risk class: low | medium | high
```

Observation: pipe-style enum text appeared in saveable body fields.

Command: `rg -n "open \| withdrawn" -g "**/templates/*.md" "skills"`

Result:

```text
skills/loom-critique/templates/critique.md:50:State: open | withdrawn
```

Observation: a finding state enum appeared as saveable body content.

Command: `rg -n "\|" -g "**/templates/*.md" "skills"`

High-risk subset observed before editing:

```text
skills/loom-drive/templates/outer-loop-handoff.md:22:  gate_status: <clear|blocked>
skills/loom-ralph/templates/ralph-packet.md:8:change_class: <record-hygiene|documentation-explanation|behavior-contract|code-behavior|protocol-authority|data-migration|security-sensitive|release-packaging>
skills/loom-ralph/templates/ralph-packet.md:10:# risk_class: <low|medium|high>
skills/loom-ralph/templates/ralph-packet.md:11:style: <reference-first|snapshot-first|hermetic>
skills/loom-ralph/templates/ralph-packet.md:12:verification_posture: <test-first|observation-first|none>
skills/loom-critique/templates/critique-packet.md:8:  kind: <record|code_change|pull_request|branch|commit|diff|external_summary|release_package|handoff_package>
skills/loom-critique/templates/critique-packet.md:10:  ref: <record ref | path | branch | commit | PR | package ID | none>
skills/loom-critique/templates/critique-packet.md:11:  diff: <branch | commit range | PR | diff target | none>
skills/loom-critique/templates/critique-packet.md:14:change_class: <record-hygiene|documentation-explanation|behavior-contract|code-behavior|protocol-authority|data-migration|security-sensitive|release-packaging>
skills/loom-critique/templates/critique-packet.md:16:# risk_class: <low|medium|high>
skills/loom-tickets/templates/ticket.md:5:change_class: <record-hygiene|documentation-explanation|behavior-contract|code-behavior|protocol-authority|data-migration|security-sensitive|release-packaging>
skills/loom-tickets/templates/ticket.md:6:risk_class: <low|medium|high>
skills/loom-tickets/templates/ticket.md:91:Route: ask_user | workspace_status | records_repair | research | spec | plan |
skills/loom-tickets/templates/ticket.md:92:ticket | local_edit | ralph | evidence | critique | wiki | retrospective |
skills/loom-tickets/templates/ticket.md:93:acceptance_review | continue | stop
skills/loom-tickets/templates/ticket.md:136:Critique policy: optional | recommended | mandatory
skills/loom-tickets/templates/ticket.md:164:Disposition status: pending | blocking | completed | deferred | not_required
skills/loom-tickets/templates/ticket.md:179:Disposition status: pending | blocking | completed | deferred | not_required
skills/loom-critique/templates/critique.md:48:Severity: low | medium | high
skills/loom-critique/templates/critique.md:49:Confidence: low | medium | high
skills/loom-critique/templates/critique.md:50:State: open | withdrawn
```

Observation: frontmatter and body enum lists used pipe syntax that could be saved
without selecting one value.

## After observations

Command: `rg -n "ACC-001" -g "**/templates/*.md" "skills"`

Result:

```text
skills/loom-tickets/templates/ticket.md:49:- ACC-001: <TBD: write the first ticket-local acceptance criterion>
skills/loom-tickets/templates/ticket.md:58:- Use `spec:<slug>#ACC-001` for spec-owned acceptance.
skills/loom-tickets/templates/ticket.md:59:- Use `ticket:<token>#ACC-001` for ticket-local acceptance criteria owned in
skills/loom-specs/templates/spec.md:45:- ACC-001: <TBD: write the first acceptance criterion before saving>
```

Observation: generic `ACC-001` acceptance content was replaced with explicit TBD
text; remaining non-TBD `ACC-001` hits are instructional reference examples.

Command: `rg -n "low \| medium \| high" -g "**/templates/*.md" "skills"`

Result: no output.

Command: `rg -n "open \| withdrawn" -g "**/templates/*.md" "skills"`

Result: no output.

Command: `rg -n "records: \[\]|paths: \[\]" -g "**/templates/*.md" "skills"`

Result:

```text
skills/loom-wiki/templates/wiki-packet.md:61:as placeholder-only `records: []` / `paths: []`.
skills/loom-critique/templates/critique-packet.md:83:as placeholder-only `records: []` / `paths: []`.
```

Observation: empty write-scope array hits remain only in warning prose; saveable
`child_write_scope` / `write_scope` defaults were replaced with explicit TBD list
items where they were unsafe.

Command: `rg -n "<TBD" -g "**/templates/*.md" "skills"`

Result summary: explicit `<TBD: ...>` placeholders are present in the hardened
ticket, spec, Ralph packet, critique packet, critique, wiki packet, and outer-loop
handoff templates. These hits mark user-filled fields rather than accepted record
truth.

Command: `rg -n "\|" -g "**/templates/*.md" "skills"`

Result summary: remaining pipe hits are table syntax, memory support examples,
quoted examples such as harness mode options, and legacy `<name|unknown>`
placeholders in packet source metadata. The high-risk saveable enum body fields
and changed frontmatter fields listed in the before observation no longer use
pipe-style defaults.

Command: `git diff --check`

Result: no output.

# Supports Claims

- `initiative:skills-corpus-council-precision-pass#OBJ-008`
- `ticket:tmplph8x#ACC-001`
- `ticket:tmplph8x#ACC-002`
- `ticket:tmplph8x#ACC-003`
- `ticket:tmplph8x#ACC-004`

# Challenges Claims

None - the observed after-state supports the placeholder-hardening claims within
the inspected template scope.

# Environment

Commit: `dab8a56fed213d83770d7715d58445684c36cae1`
Branch: `main`
Runtime: Markdown/template inspection with `rg` and `git diff --check`
OS: darwin
Relevant config: no schema, parser, runtime validation, git config, commit, or push used.

# Validity

Valid for: working tree state after the template placeholder hardening edit.
Recheck when: any `skills/**/templates/*.md` file changes, or before ticket
acceptance after critique follow-up.

# Limitations

This evidence is structural and search-based. It does not prove every placeholder
is semantically ideal, and it intentionally preserves useful examples that are
clearly examples or support-only memory/harness notation.

# Result

High-risk generic acceptance text, pipe-style enum defaults, and unsafe empty
write-scope defaults were replaced with explicit TBD or instructional text in the
target templates. `git diff --check` reported no whitespace errors.

# Interpretation

The after-state is sufficient evidence for the bounded record-hygiene iteration
to proceed to mandatory critique. It is not a substitute for critique under the
ticket's `records-grammar` and `operator-clarity` profiles.

# Related Records

- `ticket:tmplph8x`
- `packet:ralph-ticket-tmplph8x-20260502T203733Z`
