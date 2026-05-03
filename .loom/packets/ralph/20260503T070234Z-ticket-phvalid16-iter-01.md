---
id: packet:ralph-ticket-phvalid16-20260503T070234Z
kind: packet
packet_kind: ralph
status: consumed
target: ticket:phvalid16
mode: execution
change_class: protocol-authority
risk_class: medium
style: reference-first
verification_posture: observation-first
iteration: 1
created_at: 2026-05-03T07:02:34Z
updated_at: 2026-05-03T07:04:42Z
scope:
  kind: repository
  repositories:
    - repo:root
child_write_scope:
  records:
    - None - child returns output only; parent reconciles ticket, evidence, critique, and packet status.
  paths:
    - skills/loom-records/references/validation.md
parent_merge_scope:
  records:
    - ticket:phvalid16
  paths:
    - .loom/tickets/20260503-phvalid16-add-placeholder-validation.md
    - .loom/evidence/20260503-placeholder-validation-guidance-validation.md
    - .loom/critique/placeholder-validation-guidance-review.md
    - .loom/packets/ralph/20260503T070234Z-ticket-phvalid16-iter-01.md
source_fingerprint:
  git_commit: 43cd5a384e9d7dcbeb07c279cc150e1cf92990bd
  integration_remote: origin
  integration_ref: origin/main
  integration_commit: 43cd5a384e9d7dcbeb07c279cc150e1cf92990bd
  git_status_summary: clean
  git_status_detail: clean working tree at packet compile time
  compiled_from:
    - ticket:phvalid16
    - plan:skills-corpus-context-integrity-hardening-pass
    - initiative:skills-corpus-context-integrity-hardening-pass
    - research:skills-corpus-third-pass-follow-up-validation
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
  max_source_files: 4
  max_excerpt_lines_per_file: 180
  avoid_full_file_reads: true
sources:
  initiative:
    - initiative:skills-corpus-context-integrity-hardening-pass
  research:
    - research:skills-corpus-third-pass-follow-up-validation
  plan:
    - plan:skills-corpus-context-integrity-hardening-pass
  ticket:
    - ticket:phvalid16
  files:
    - skills/loom-records/references/validation.md
links: {}
---

# Mission

Add saved-record placeholder validation guidance so saved `.loom` project records
do not retain unresolved template placeholders, example IDs, or generic TODO/TBD
tokens unless explicitly documenting observed source text.

# Bound Context

Templates intentionally carry `<TBD: ...>` placeholders. This ticket is about
saved project records under `.loom/`, not template files under `skills/**/templates`.
The guidance must preserve intentional template placeholders while preventing
placeholder leakage from becoming fake project truth.

# Source Snapshot

- `skills/loom-records/references/validation.md` has spot-check recipes for
  missing IDs, missing statuses, status vocabulary, claim coverage, changed graph
  edges, evidence records, and escalation.
- It currently has no saved-record placeholder scan or explicit rule separating
  saved `.loom` records from templates.

# Verification Targets

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-017`
- `ticket:phvalid16#ACC-001`
- `ticket:phvalid16#ACC-002`
- `ticket:phvalid16#ACC-003`
- `ticket:phvalid16#ACC-004`

# Task For This Iteration

Make the smallest coherent validation-reference edit:

1. Add a placeholder scan recipe for saved `.loom` records.
2. State that saved records must not contain unresolved template placeholders,
   example IDs, or generic TODO/TBD tokens unless explicitly documented as
   observed source text.
3. State that intentional template placeholders under `skills/**/templates` are
   not failures of saved-record validation.
4. Do not add a validator runtime, schema engine, command wrapper, generated
   index, or template rewrite.

# Verification Posture

Observation-first. Before and after editing, report targeted observations for:

- placeholder scan recipe;
- saved-record rule and observed-source-text exception;
- template placeholder exception;
- absence of validator runtime, schema engine, command wrapper, generated index,
  or template rewrite.

Run `git diff --check` after editing.

# Stop Conditions

Stop and report `blocked` or `escalate` if satisfying the ticket would require a
validator runtime/schema engine, rewriting templates, or treating intentional
template placeholders as failures.

# Output Contract

Return outcome, files changed, records changed, before/after observations,
`git diff --check` result, self-review, blockers/residual risks, and recommended
ticket state/next route.

# Working Notes

Parent compiled from clean `main` at `43cd5a3` after closing and pushing
`ticket:wroute15`.

# Child Output

Outcome: `stop`

Files changed:

- `skills/loom-records/references/validation.md`

Records changed by child:

- None. Parent retained ticket, evidence, critique, and packet reconciliation.

Observed result:

- Added a saved `.loom` record rule for unresolved template placeholders, example
  IDs, and generic TODO/TBD tokens.
- Added an observed-source-text exception for documented quoted or observed
  source material.
- Added a `skills/**/templates` exception so intentional template placeholders are
  not saved-record validation failures.
- Added a saved-record placeholder leakage recipe.
- No validator runtime, schema engine, command wrapper, generated index, or
  template rewrite was added.

Verification:

- `git diff --check` passed with no output.
- `git diff --name-only -- 'skills/**/templates/**'` produced no output,
  confirming templates were not rewritten.

Blockers or residual risks:

- No blockers.
- The recipe is heuristic and requires operator review of hits.

Recommendation:

- Move `ticket:phvalid16` to mandatory critique.

# Parent Merge Notes

- 2026-05-03T07:04:42Z: Parent accepted the bounded implementation output,
  recorded `evidence:placeholder-validation-guidance-validation`, marked this
  packet `consumed`, and moved `ticket:phvalid16` to `review_required` for
  mandatory critique.
