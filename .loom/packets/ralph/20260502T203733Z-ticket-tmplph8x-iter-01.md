---
id: packet:ralph-ticket-tmplph8x-20260502T203733Z
kind: packet
packet_kind: ralph
status: consumed
target: ticket:tmplph8x
mode: execution
change_class: record-hygiene
style: reference-first
verification_posture: observation-first
iteration: 1
created_at: 2026-05-02T20:37:33Z
updated_at: 2026-05-02T20:43:02Z
scope:
  kind: repository
  repositories:
    - repo:root
child_write_scope:
  records:
    - ticket:tmplph8x
    - evidence:template-placeholder-validation
    - packet:ralph-ticket-tmplph8x-20260502T203733Z
  paths:
    - skills/**/templates/*.md
    - .loom/tickets/20260502-tmplph8x-harden-template-placeholders.md
    - .loom/evidence/20260502-template-placeholder-validation.md
    - .loom/packets/ralph/20260502T203733Z-ticket-tmplph8x-iter-01.md
parent_merge_scope:
  records:
    - ticket:tmplph8x
    - evidence:template-placeholder-validation
    - packet:ralph-ticket-tmplph8x-20260502T203733Z
  paths:
    - .loom/critique/template-placeholder-safety-review.md
source_fingerprint:
  git_commit: dab8a56fed213d83770d7715d58445684c36cae1
  integration_remote: origin
  integration_ref: origin/main
  integration_commit: dab8a56fed213d83770d7715d58445684c36cae1
  git_status_summary: clean
  compiled_from:
    - initiative:skills-corpus-council-precision-pass
    - plan:skills-corpus-council-precision-pass
    - ticket:tmplph8x
    - ticket:retrod3p
    - ticket:authst4p
    - ticket:pktgram5
execution_context:
  branch: main
  push_remote: origin
  worktree: /Users/alexanderbutler/code_projects/personal/agent-loom
  isolation: none
  git_shared_metadata_mutations: forbidden
  destructive_commands: forbidden
  network: forbidden
context_budget:
  posture: normal
  max_source_files: 28
  max_excerpt_lines_per_file: 120
  avoid_full_file_reads: false
sources:
  constitution:
    - constitution:main
  initiative:
    - initiative:skills-corpus-council-precision-pass
  plan:
    - plan:skills-corpus-council-precision-pass
  ticket:
    - ticket:tmplph8x
  references:
    - skills/**/templates/*.md
links:
  initiative:
    - initiative:skills-corpus-council-precision-pass
  plan:
    - plan:skills-corpus-council-precision-pass
  ticket:
    - ticket:tmplph8x
---

# Mission

Harden copied Loom templates so placeholders cannot be mistaken for accepted
record content, while preserving useful examples where they are clearly examples.

# Bound Context

This is the eighth ticket in `plan:skills-corpus-council-precision-pass` and
covers `initiative:skills-corpus-council-precision-pass#OBJ-008`. Dependencies
`ticket:retrod3p`, `ticket:authst4p`, and `ticket:pktgram5` are closed. The
product surface is `skills/`; this ticket is expected to touch templates only.

# Source Snapshot

Baseline is clean `main` at `dab8a56fed213d83770d7715d58445684c36cae1`.

Parent observed 27 files under `skills/**/templates/*.md`. A broad placeholder
search found many expected placeholders and examples, so the child must classify
dangerous saveable defaults rather than mechanically replacing every placeholder.

# Change Class

Declared as `record-hygiene`; the change improves template safety without adding
schema validation, runtime validation, or new owner layers.

# Verification Targets

- `initiative:skills-corpus-council-precision-pass#OBJ-008`
- `ticket:tmplph8x#ACC-001`
- `ticket:tmplph8x#ACC-002`
- `ticket:tmplph8x#ACC-003`
- `ticket:tmplph8x#ACC-004`

# Task For This Iteration

1. Audit `skills/**/templates/*.md` for placeholders that look like valid saved
   record truth, especially generic `ACC-001`, pipe-style enum defaults, empty
   fields that look accepted, and example values without clear example framing.
2. Replace dangerous placeholders with unmistakable `<TBD: replace before
   saving>`-style text or instructional text that cannot be confused with
   canonical truth.
3. Preserve useful examples when they are clearly examples rather than default
   accepted content.
4. Create `.loom/evidence/20260502-template-placeholder-validation.md` with
   before/after placeholder searches and `git diff --check`.
5. Update `ticket:tmplph8x` to `review_required` with evidence links, claim
   matrix, retrospective/promotion disposition pending, and mandatory critique
   recommendation. Do not close it.

# Verification Posture

`observation-first`.

Record before/after searches for high-risk placeholder patterns, including at
least `ACC-001`, `low | medium | high`, `open | withdrawn`, enum-like pipe
tokens in frontmatter, `<TBD`, and `git diff --check`.

# Stop Conditions

Stop and return `blocked` or `escalate` if:

- the audit would require changing non-template product references;
- preserving useful examples conflicts with placeholder safety in a way that
  needs product direction;
- resolving placeholder safety would require schema/runtime validation;
- the change would rewrite templates beyond placeholder safety.

# Output Contract

Return outcome, files changed, records changed, before/after observations,
validation commands/results, risks, and ticket recommendation. Include whether
the ticket should proceed to mandatory oracle critique profiles
`records-grammar` and `operator-clarity`.

# Working Notes

Keep the change minimal. Do not remove examples solely because they contain angle
brackets or pipe characters; remove or reframe only values that can plausibly be
saved unchanged as record truth.

# Child Output

Outcome: stop

Files changed:

- `skills/loom-critique/templates/critique-packet.md`
- `skills/loom-critique/templates/critique.md`
- `skills/loom-drive/templates/outer-loop-handoff.md`
- `skills/loom-ralph/templates/ralph-packet.md`
- `skills/loom-specs/templates/spec.md`
- `skills/loom-tickets/templates/ticket.md`
- `skills/loom-wiki/templates/wiki-packet.md`

Records changed:

- `ticket:tmplph8x`
- `evidence:template-placeholder-validation`
- `packet:ralph-ticket-tmplph8x-20260502T203733Z`

Before/after observations:

- Generic `ACC-001` acceptance text existed in ticket and spec templates before;
  after, those lines use explicit `<TBD: ...>` replacement text while
  instructional reference examples remain clearly examples.
- `low | medium | high` and `open | withdrawn` appeared in saveable body fields
  before; after, targeted searches for those exact pipe-style enum defaults return
  no output.
- High-risk frontmatter pipe enums and empty write-scope defaults in packet and
  handoff templates were replaced with quoted TBD selections or explicit TBD list
  items.
- Remaining pipe hits are table syntax, support-memory examples, quoted harness
  examples, and legacy metadata placeholders such as `<name|unknown>` that were
  outside the high-risk acceptance/default enum set for this bounded iteration.

Validation:

- `rg -n "ACC-001" -g "**/templates/*.md" "skills"`: remaining hits are TBD
  acceptance placeholders or instructional reference examples.
- `rg -n "low \\| medium \\| high" -g "**/templates/*.md" "skills"`: no output.
- `rg -n "open \\| withdrawn" -g "**/templates/*.md" "skills"`: no output.
- `rg -n "records: \\[\\]|paths: \\[\\]" -g "**/templates/*.md" "skills"`:
  remaining hits are warning prose only.
- `rg -n "<TBD" -g "**/templates/*.md" "skills"`: explicit TBD placeholders
  are present in the hardened template fields.
- `git diff --check`: no output.

Residual risks:

- Search-based evidence cannot prove every placeholder is semantically ideal.
- Some useful examples and legacy metadata placeholders still contain angle
  brackets or pipe characters where they are examples, support-memory shorthand,
  table syntax, or compact unknown/none options.
- Mandatory critique still needs to inspect operator clarity and records grammar.

Ticket recommendation:

- Keep `ticket:tmplph8x` in `review_required`.
- Proceed to mandatory oracle critique profiles `records-grammar` and
  `operator-clarity` before acceptance or closure.

# Parent Merge Notes

Parent accepted the bounded child output for critique handoff. Ticket
`ticket:tmplph8x` truthfully reflects `review_required`, links
`evidence:template-placeholder-validation`, and leaves acceptance/closure pending
mandatory oracle critique.
