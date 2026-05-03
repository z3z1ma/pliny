---
id: packet:ralph-ticket-tplsave3-20260503T050338Z
kind: packet
packet_kind: ralph
status: consumed
target: ticket:tplsave3
mode: execution
change_class: template-safety
risk_class: medium
style: reference-first
verification_posture: observation-first
iteration: 1
created_at: 2026-05-03T05:03:38Z
updated_at: 2026-05-03T05:05:24Z
scope:
  kind: repository
  repositories:
    - repo:root
child_write_scope:
  records:
    - None - child returns output only; parent reconciles ticket, evidence, critique, and packet status.
  paths:
    - skills/loom-tickets/templates/ticket.md
    - skills/loom-plans/templates/plan.md
    - skills/loom-records/references/frontmatter.md
parent_merge_scope:
  records:
    - ticket:tplsave3
  paths:
    - .loom/tickets/20260503-tplsave3-add-template-save-ready-rules.md
    - .loom/evidence/20260503-template-save-ready-validation.md
    - .loom/critique/template-save-ready-review.md
    - .loom/packets/ralph/20260503T050338Z-ticket-tplsave3-iter-01.md
source_fingerprint:
  git_commit: e5abe407d9ba526af48dde2e519bc1a1901fc734
  integration_remote: origin
  integration_ref: origin/main
  integration_commit: e5abe407d9ba526af48dde2e519bc1a1901fc734
  git_status_summary: clean
  git_status_detail: clean working tree at packet compile time
  compiled_from:
    - ticket:tplsave3
    - plan:skills-corpus-context-integrity-hardening-pass
    - initiative:skills-corpus-context-integrity-hardening-pass
    - research:skills-corpus-context-integrity-hardening-review
execution_context:
  branch: main
  push_remote: origin
  worktree: /Users/alexanderbutler/code_projects/personal/agent-loom
  isolation: none
  git_shared_metadata_mutations: forbidden
  destructive_commands: forbidden
  network: forbidden
context_budget:
  posture: tight
  max_source_files: 5
  max_excerpt_lines_per_file: 140
  avoid_full_file_reads: true
sources:
  initiative:
    - initiative:skills-corpus-context-integrity-hardening-pass
  research:
    - research:skills-corpus-context-integrity-hardening-review
  plan:
    - plan:skills-corpus-context-integrity-hardening-pass
  ticket:
    - ticket:tplsave3
  files:
    - skills/loom-tickets/templates/ticket.md
    - skills/loom-plans/templates/plan.md
    - skills/loom-records/references/frontmatter.md
links: {}
---

# Mission

Add save-ready pruning guidance to copy-heavy ticket and plan templates for
`ticket:tplsave3` without removing acceptance, evidence, critique, retrospective,
or closure gates.

# Bound Context

Templates are copied into real records. The existing ticket template already tells
operators to choose one acceptance owner branch and remove unused route sections.
The plan template already tells operators to write `None - reason` for absent
waves. This ticket asks for concise save-ready rules that reduce placeholder and
unused-branch carryover while preserving the gates that keep closure honest.

# Verification Targets

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-004`
- `ticket:tplsave3#ACC-001`
- `ticket:tplsave3#ACC-002`
- `ticket:tplsave3#ACC-003`
- `ticket:tplsave3#ACC-004`

# Task For This Iteration

Make the smallest coherent template-safety edits:

1. Add save-ready guidance to the ticket template telling agents to replace
   placeholders and remove unused readiness/acceptance branches before saving.
2. Add save-ready guidance to the plan template telling agents to remove unused
   wave examples/placeholders or replace them with meaningful `None - reason`.
3. Preserve evidence, critique, acceptance, retrospective, and closure gates.
4. Update `frontmatter.md` only if a small cross-reference is needed for template
   placeholder hygiene.

# Verification Posture

Observation-first. Before and after editing, report targeted observations for:

- ticket template save-ready wording;
- plan template wave/placeholder wording;
- retained evidence, critique, acceptance, retrospective, and closure gate
  sections;
- absence of template generator/schema/minimal-full template requirements.

Run `git diff --check` after editing.

# Stop Conditions

Stop and report `blocked` or `escalate` if satisfying the ticket would require a
template generator, schema, separate minimal/full template families, or removal of
required acceptance/critique guidance.

# Output Contract

Return outcome, files changed, records changed, before/after observations,
`git diff --check` result, self-review, blockers/residual risks, and recommended
ticket state/next route.

# Working Notes

Parent compiled from clean `main` at `e5abe40` after closing `ticket:vocabx08`.

# Child Output

Outcome: stop - bounded template edits completed within child write scope.

Files changed:

- `skills/loom-tickets/templates/ticket.md`
- `skills/loom-plans/templates/plan.md`

Records changed: none.

Before observations:

- Ticket template already told agents to choose one acceptance owner branch and
  remove the unused branch, and route readiness said to use only applicable route
  sections.
- Ticket template did not have a concise save-ready rule covering all placeholders
  plus unused readiness branches.
- Plan template already used `None - reason` for absent waves, but did not
  explicitly say to remove unused wave examples/placeholders before saving.
- Evidence, critique, acceptance, retrospective/promotion, and closure gate
  sections were present.
- No template generator, schema, or minimal/full template-family requirement was
  present.
- `skills/loom-records/references/frontmatter.md` already said to replace every
  placeholder before saving; no edit was needed.

After observations:

- Ticket template includes a save-ready rule to replace every placeholder, remove
  unused acceptance/readiness branches, and retain evidence/critique/
  retrospective/acceptance/closure gates.
- Plan template includes a save-ready rule to remove unused wave examples and
  placeholder rows or replace them with real content / meaningful
  `None - reason`.
- Evidence, critique, acceptance, retrospective/promotion, and closure gate
  sections remain intact.
- No generator, schema, or separate minimal/full template requirement was added.
- `skills/loom-records/references/frontmatter.md` remains unchanged.

Validation: `git diff --check -- "skills/loom-tickets/templates/ticket.md"
"skills/loom-plans/templates/plan.md"
"skills/loom-records/references/frontmatter.md"` passed with no output.

Self-review: no concerns; edits are concise Markdown-only additions and do not
remove required gates.

Blockers/residual risks: no blockers. Parent still needs evidence, critique, and
ticket reconciliation.

Recommendation: `review_required`; next route is parent evidence recording, then
critique / acceptance review.

# Parent Merge Notes

Accepted child output as in scope. Parent recorded structural evidence and routed
to mandatory critique.
