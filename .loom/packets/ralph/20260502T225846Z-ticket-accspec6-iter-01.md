---
id: packet:ralph-ticket-accspec6-20260502T225846Z
kind: packet
packet_kind: ralph
status: consumed
target: ticket:accspec6
mode: execution
change_class: protocol-authority
risk_class: medium
style: reference-first
verification_posture: observation-first
iteration: 1
created_at: 2026-05-02T22:58:46Z
updated_at: 2026-05-02T23:03:12Z
scope:
  kind: repository
  repositories:
    - repo:root
child_write_scope:
  records:
    - ticket:accspec6
    - evidence:acceptance-placeholder-validation
    - packet:ralph-ticket-accspec6-20260502T225846Z
  paths:
    - skills/loom-tickets/templates/ticket.md
    - skills/loom-records/references/claim-coverage.md
    - .loom/tickets/20260502-accspec6-split-spec-ticket-acceptance-placeholders.md
    - .loom/evidence/20260502-acceptance-placeholder-validation.md
    - .loom/packets/ralph/20260502T225846Z-ticket-accspec6-iter-01.md
parent_merge_scope:
  records:
    - ticket:accspec6
    - evidence:acceptance-placeholder-validation
    - packet:ralph-ticket-accspec6-20260502T225846Z
  paths: []
source_fingerprint:
  git_commit: 26964cef5ba528eb70cb1e4ece42efcf812c97c0
  integration_remote: origin
  integration_ref: origin/main
  integration_commit: 26964cef5ba528eb70cb1e4ece42efcf812c97c0
  git_status_summary: clean
  compiled_from:
    - initiative:skills-corpus-template-grammar-safety-pass
    - plan:skills-corpus-template-grammar-safety-pass
    - ticket:accspec6
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
  max_source_files: 6
  max_excerpt_lines_per_file: 160
  avoid_full_file_reads: false
sources:
  initiative:
    - initiative:skills-corpus-template-grammar-safety-pass
  plan:
    - plan:skills-corpus-template-grammar-safety-pass
  ticket:
    - ticket:accspec6
  records:
    - skills/loom-tickets/templates/ticket.md
    - skills/loom-records/references/claim-coverage.md
    - skills/loom-records/references/route-vocabulary.md
links:
  ticket:
    - ticket:accspec6
---

# Mission

Make copied tickets fail closed on acceptance ownership by separating spec-owned
acceptance from ticket-local `ACC-*` criteria.

# Bound Context

This is the sixth ticket in `plan:skills-corpus-template-grammar-safety-pass` and
covers `initiative:skills-corpus-template-grammar-safety-pass#OBJ-006`. Specs own
reusable behavior acceptance contracts. Tickets own live execution state, scoped
coverage disposition, and ticket-local acceptance only when no spec owns the
contract.

# Source Snapshot

Baseline commit: `26964cef5ba528eb70cb1e4ece42efcf812c97c0`, matching
`origin/main`. Worktree was clean before packet creation.

Parent before-state search over the targeted ticket template and claim-coverage
reference found:

- `skills/loom-tickets/templates/ticket.md:38-50` has one `# Acceptance Criteria`
  section that mentions spec-owned acceptance first, then immediately presents
  ticket-local `ACC-*` placeholders.
- `skills/loom-tickets/templates/ticket.md:52-61` tells tickets to cite
  spec-owned acceptance IDs, ticket-local acceptance IDs, and initiative
  objectives under `# Coverage`.
- `skills/loom-records/references/claim-coverage.md:86-106` correctly says
  ticket-local `ACC-*` criteria are only for no-spec work and must not replace a
  reusable spec-owned acceptance contract.

# Change Class

Declared as `protocol-authority`; risk is medium because confusing acceptance
ownership can make downstream agents close tickets against the wrong contract.

# Verification Targets

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-006`
- `ticket:accspec6#ACC-001`
- `ticket:accspec6#ACC-002`
- `ticket:accspec6#ACC-003`
- `ticket:accspec6#ACC-004`

# Task For This Iteration

1. Capture before-state searches for `ACC-*`, spec-owned acceptance,
   ticket-local acceptance, `acceptance contract`, `# Acceptance Criteria`, and
   `# Coverage` in the targeted ticket template and claim-coverage reference.
2. Update `skills/loom-tickets/templates/ticket.md` so copied tickets explicitly
   choose between a spec-owned acceptance branch and a ticket-local acceptance
   branch.
3. Keep `ACC-*` placeholders only in the ticket-local branch. Do not present
   ticket-local `ACC-*` examples as the default when a spec owns acceptance.
4. Align `skills/loom-records/references/claim-coverage.md` only if needed so the
   reference and template teach the same spec-vs-ticket acceptance boundary.
5. Preserve ticket-local acceptance for no-spec work; do not require every ticket
   to have a spec.
6. Update `ticket:accspec6` to `review_required` with evidence linked, claim
   matrix current, and next route `critique`.
7. Record `evidence:acceptance-placeholder-validation` with before/after searches
   and `git diff --check`.
8. Fill this packet's `# Child Output`. The parent will mark the packet consumed
   after reconciliation.

# Verification Posture

`observation-first`.

Capture before/after searches for the acceptance ownership terms above. Run
`git diff --check` after edits.

# Stop Conditions

Stop and return `blocked` or `escalate` if:

- the fix would require every ticket to have a spec;
- the fix would remove ticket-local acceptance for work with no spec-owned
  contract;
- the fix would let a ticket-local `ACC-*` criterion redefine or replace a
  reusable spec-owned acceptance contract;
- the fix would add route automation, validators, schema enforcement, command
  wrappers, or a new owner layer;
- the targeted files cannot be aligned without broader acceptance-contract
  redesign;
- the source fingerprint is materially stale before launch.

# Output Contract

Return outcome, files changed, records changed, before/after observation
commands/results, `git diff --check` result, residual risks, self-review
concerns, and ticket recommendation. Include whether the ticket should proceed to
mandatory oracle critique with profiles `owner-boundary`, `records-grammar`, and
`closure-honesty`.

# Working Notes

Parent created this packet after confirming `ticket:tkrout5` was closed and
pushed and the worktree was clean at the source fingerprint.

# Child Output

Outcome: `stop`.

Files changed:

- `skills/loom-tickets/templates/ticket.md`
- `skills/loom-records/references/claim-coverage.md`
- `.loom/tickets/20260502-accspec6-split-spec-ticket-acceptance-placeholders.md`
- `.loom/evidence/20260502-acceptance-placeholder-validation.md`
- `.loom/packets/ralph/20260502T225846Z-ticket-accspec6-iter-01.md`

Records changed:

- `ticket:accspec6` moved to `review_required`, linked
  `evidence:acceptance-placeholder-validation`, updated coverage and claim
  matrix, and set next route to `critique`.
- `evidence:acceptance-placeholder-validation` recorded before/after searches and
  `git diff --check`.
- `packet:ralph-ticket-accspec6-20260502T225846Z` recorded this child output.

Implementation summary:

- The ticket template now requires choosing exactly one acceptance owner branch.
- The spec-owned branch warns not to create ticket-local `ACC-*` criteria and
  points spec-owned acceptance IDs to `# Coverage`.
- The ticket-local branch preserves ticket-local `ACC-*` placeholders for work
  with no spec-owned acceptance contract.
- Claim coverage now introduces the same owner choice before the spec-owned
  coverage example.

Before/after observation summary:

- Before: the template named spec-owned acceptance first, then immediately showed
  ticket-local `ACC-*` placeholders without an explicit branch choice; claim
  coverage already warned not to replace spec-owned acceptance with ticket-local
  IDs.
- After: the template separates spec-owned and ticket-local branches; `ACC-*`
  placeholders remain only in the ticket-local branch; claim coverage explicitly
  says to cite spec-owned IDs under `# Coverage` and not create ticket-local
  `ACC-*` criteria for that contract.

Validation:

- Before search captured for `ACC-*`, spec-owned acceptance, ticket-local
  acceptance, `acceptance contract`, `# Acceptance Criteria`, and `# Coverage` in
  the targeted template/reference.
- After search captured for the same terms in the targeted template/reference.
- `git diff --check` produced no output and exited successfully.

Residual risks / self-review concerns:

- This was structural Markdown validation only; no oracle critique verdict exists
  yet.
- The wording uses prose branch labels rather than a schema-enforced field, by
  design and per packet constraints.

Ticket recommendation:

- Parent should reconcile this iteration as landed and route `ticket:accspec6` to
  mandatory oracle critique with profiles `owner-boundary`, `records-grammar`,
  and `closure-honesty`.

# Parent Merge Notes

Parent accepted the child output as scoped and routed the ticket to mandatory
oracle critique. Parent reconciliation confirmed the diff is limited to the
declared child write scope, `git diff --check` passes, the ticket claim matrix
uses canonical claim-coverage status vocabulary, and
`evidence:acceptance-placeholder-validation` is sufficient for critique routing.
