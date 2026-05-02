---
id: packet:ralph-ticket-phsafe8-20260502T232054Z
kind: packet
packet_kind: ralph
status: consumed
target: ticket:phsafe8
mode: execution
change_class: record-hygiene
risk_class: medium
style: reference-first
verification_posture: observation-first
iteration: 1
created_at: 2026-05-02T23:20:54Z
updated_at: 2026-05-02T23:24:37Z
scope:
  kind: repository
  repositories:
    - repo:root
child_write_scope:
  records:
    - ticket:phsafe8
    - evidence:placeholder-safety-validation
    - packet:ralph-ticket-phsafe8-20260502T232054Z
  paths:
    - skills/**/templates/*.md
    - skills/**/references/*.md
    - .loom/tickets/20260502-phsafe8-harden-remaining-placeholder-safety.md
    - .loom/evidence/20260502-placeholder-safety-validation.md
    - .loom/packets/ralph/20260502T232054Z-ticket-phsafe8-iter-01.md
parent_merge_scope:
  records:
    - ticket:phsafe8
    - evidence:placeholder-safety-validation
    - packet:ralph-ticket-phsafe8-20260502T232054Z
  paths:
    - skills/loom-wiki/templates/index.md
    - skills/loom-bootstrap/references/06-filesystem-and-tooling.md
    - skills/loom-initiatives/templates/initiative.md
    - .loom/tickets/20260502-phsafe8-harden-remaining-placeholder-safety.md
    - .loom/evidence/20260502-placeholder-safety-validation.md
    - .loom/packets/ralph/20260502T232054Z-ticket-phsafe8-iter-01.md
source_fingerprint:
  git_commit: 4b85062b04ca9ba6c0b5c6402865f1fcdc6af54f
  integration_remote: origin
  integration_ref: origin/main
  integration_commit: 4b85062b04ca9ba6c0b5c6402865f1fcdc6af54f
  git_status_summary: clean
  compiled_from:
    - initiative:skills-corpus-template-grammar-safety-pass
    - plan:skills-corpus-template-grammar-safety-pass
    - ticket:phsafe8
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
  max_source_files: 12
  max_excerpt_lines_per_file: 160
  avoid_full_file_reads: false
sources:
  initiative:
    - initiative:skills-corpus-template-grammar-safety-pass
  plan:
    - plan:skills-corpus-template-grammar-safety-pass
  ticket:
    - ticket:phsafe8
  records:
    - skills/loom-wiki/templates/index.md
    - skills/loom-bootstrap/references/06-filesystem-and-tooling.md
    - skills/loom-initiatives/templates/initiative.md
    - skills/loom-records/references/status-lifecycle.md
links:
  ticket:
    - ticket:phsafe8
---

# Mission

Harden remaining copyable placeholders and authoritative default statuses that
can look save-ready before their content is real.

# Bound Context

This is the eighth ticket in `plan:skills-corpus-template-grammar-safety-pass` and
covers `initiative:skills-corpus-template-grammar-safety-pass#OBJ-008`. The goal
is targeted safety, not broad style cleanup. Preserve useful instructional
examples and do not invent runtime validation.

# Source Snapshot

Baseline commit: `4b85062b04ca9ba6c0b5c6402865f1fcdc6af54f`, matching
`origin/main`. Worktree was clean before packet creation.

Parent scan found likely review targets among broader expected placeholder hits:

- `skills/loom-wiki/templates/index.md` defaults a placeholder wiki index to
  `status: accepted`.
- `skills/loom-bootstrap/references/06-filesystem-and-tooling.md` includes a
  copyable here-doc example with `status: active` and a bare `TBD` question.
- `skills/loom-initiatives/templates/initiative.md` includes a copyable success
  metric placeholder: `Replace with one durable objective criterion.`
- Other `TBD` placeholders in templates often already use explicit
  `<TBD: ... before saving>` shapes and may be safe; inspect before editing.

# Change Class

Declared as `record-hygiene`; risk is medium because unsafe placeholders can make
freshly copied records appear authoritative before the operator has replaced the
placeholder content.

# Verification Targets

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-008`
- `ticket:phsafe8#ACC-001`
- `ticket:phsafe8#ACC-002`
- `ticket:phsafe8#ACC-003`
- `ticket:phsafe8#ACC-004`

# Task For This Iteration

1. Capture before-state searches across `skills/**/templates/*.md` and relevant
   `skills/**/references/*.md` for `TBD`, `Replace with`, and authoritative
   statuses over placeholder content such as `status: accepted`, `status: final`,
   `status: completed`, `status: recorded`, and `status: active`.
2. Identify only copyable placeholder/default-status surfaces that can look valid
   if saved unchanged.
3. Harden the smallest set of unsafe surfaces. Likely targets include the wiki
   index template, bootstrap here-doc example, and initiative template success
   metric placeholder.
4. Preserve useful instructional examples and valid layer status vocabularies. Do
   not change statuses to invalid values for their record kind.
5. Do not rewrite all templates for style, remove clearly instructional examples,
   add validation automation, or introduce runtime/schema requirements.
6. Update `ticket:phsafe8` to `review_required` with evidence linked, claim
   matrix current, and next route `critique`.
7. Record `evidence:placeholder-safety-validation` with before/after searches,
   judgment notes for unchanged safe examples, and `git diff --check`.
8. Fill this packet's `# Child Output`. The parent will replace the
   `parent_merge_scope.paths` placeholder with concrete reconciled paths and mark
   the packet consumed after reconciliation.

# Verification Posture

`observation-first`.

Capture before/after placeholder/status searches and `git diff --check`. The
evidence should distinguish observed search output from judgment about which
matches are safe to leave unchanged.

# Stop Conditions

Stop and return `blocked` or `escalate` if:

- the scan suggests a broad template redesign rather than a targeted cleanup;
- a status would need to change to a value not allowed for that record kind;
- a placeholder is only instructional and not copyable project truth;
- the fix would remove useful examples or make templates harder to use;
- the fix would add validators, automation, schema enforcement, command wrappers,
  runtime requirements, hidden helpers, or a new owner layer;
- the source fingerprint is materially stale before launch.

# Output Contract

Return outcome, files changed, records changed, before/after observation
commands/results, `git diff --check` result, rationale for unchanged scanned
matches, residual risks, self-review concerns, and ticket recommendation. Include
whether the ticket should proceed to mandatory oracle critique with profiles
`template-safety`, `records-grammar`, and `operator-clarity`.

# Working Notes

Parent created this packet after confirming `ticket:sibpkt7` was closed and
pushed and the worktree was clean at the source fingerprint.

# Child Output

Outcome: `stop` — bounded implementation iteration completed and ticket is ready
for mandatory critique.

Changed files:

- `skills/loom-wiki/templates/index.md`
- `skills/loom-bootstrap/references/06-filesystem-and-tooling.md`
- `skills/loom-initiatives/templates/initiative.md`

Changed records:

- `ticket:phsafe8`
- `evidence:placeholder-safety-validation`
- `packet:ralph-ticket-phsafe8-20260502T232054Z`

Evidence gathered:

- Before searches across `skills/**/templates/*.md` and
  `skills/**/references/*.md` for `TBD`, `Replace with`, and authoritative
  status tokens found three unsafe targets: wiki index `status: accepted`, a
  bootstrap here-doc bare `TBD`, and initiative `Replace with` success metric.
- After searches show no `Replace with` matches, no bare `TBD` placeholders in
  changed target surfaces, and no wiki index frontmatter `status: accepted`.
- `git diff --check` produced no output.
- Full observations and rationale are recorded in
  `evidence:placeholder-safety-validation`.

Rationale for unchanged scanned matches:

- Existing `<TBD: ... before saving>` matches are explicit fail-closed
  placeholders.
- `skills/loom-plans/references/plan-shape.md` names `TBD` as a forbidden
  placeholder in readiness guidance, not as copyable placeholder content.
- `status: completed` and `status: final` occurrences are instructional lifecycle
  guidance, not frontmatter defaults over placeholder records.
- Remaining `status: active` defaults are valid initial/current statuses for their
  record kinds or support-local examples; changing them to invalid `draft` values
  would violate record grammar. The bootstrap here-doc now explicitly warns that
  `status: active` should remain only after placeholders are replaced.
- `status: recorded` remains on the evidence template because it is the valid
  evidence lifecycle status; the body prompts remain instructional and do not
  claim acceptance or closure.

Residual risks / self-review concerns:

- Some templates still rely on operator discipline to replace section prompts;
  this iteration intentionally did not redesign all templates.
- The evidence template's `status: recorded` remains a possible reviewer concern,
  but changing it would require record-grammar policy beyond this bounded cleanup.
- Mandatory oracle critique has not happened yet.

Ticket recommendation:

- Keep `ticket:phsafe8` in `review_required`.
- Parent should route to mandatory oracle critique with profiles
  `template-safety`, `records-grammar`, and `operator-clarity`.

# Parent Merge Notes

Parent accepted the child output as scoped and routed the ticket to mandatory
oracle critique. Parent reconciliation replaced the packet parent path placeholder
with concrete reconciled paths, normalized ticket claim statuses to canonical
claim-coverage vocabulary, and confirmed `git diff --check` passes.
