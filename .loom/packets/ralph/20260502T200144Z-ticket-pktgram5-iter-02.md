---
id: packet:ralph-ticket-pktgram5-20260502T200144Z
kind: packet
packet_kind: ralph
status: consumed
target: ticket:pktgram5
mode: execution
change_class: protocol-authority
style: reference-first
verification_posture: observation-first
iteration: 2
created_at: 2026-05-02T20:01:44Z
updated_at: 2026-05-02T20:06:00Z
scope:
  kind: repository
  repositories:
    - repo:root
child_write_scope:
  records:
    - ticket:pktgram5
    - evidence:packet-grammar-template-alignment-validation
    - packet:ralph-ticket-pktgram5-20260502T200144Z
  paths:
    - skills/loom-records/references/packet-frontmatter.md
    - skills/loom-records/references/naming-and-ids.md
    - skills/loom-critique/templates/critique-packet.md
    - .loom/tickets/20260502-pktgram5-align-packet-grammar-templates.md
    - .loom/evidence/20260502-packet-grammar-template-alignment-validation.md
    - .loom/packets/ralph/20260502T200144Z-ticket-pktgram5-iter-02.md
parent_merge_scope:
  records:
    - ticket:pktgram5
    - evidence:packet-grammar-template-alignment-validation
    - packet:ralph-ticket-pktgram5-20260502T200144Z
  paths:
    - .loom/critique/packet-grammar-template-alignment-review.md
    - .loom/critique/packet-grammar-template-alignment-rereview.md
source_fingerprint:
  git_commit: cceb6422bf5c95cfaf2c45983bb6a412c748c94f
  integration_remote: origin
  integration_ref: origin/main
  integration_commit: cceb6422bf5c95cfaf2c45983bb6a412c748c94f
  git_status_summary: dirty
  compiled_from:
    - initiative:skills-corpus-council-precision-pass
    - plan:skills-corpus-council-precision-pass
    - ticket:pktgram5
    - critique:packet-grammar-template-alignment-review
    - packet:ralph-ticket-pktgram5-20260502T195332Z
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
  max_source_files: 8
  max_excerpt_lines_per_file: 120
  avoid_full_file_reads: true
sources:
  constitution:
    - constitution:main
  initiative:
    - initiative:skills-corpus-council-precision-pass
  plan:
    - plan:skills-corpus-council-precision-pass
  ticket:
    - ticket:pktgram5
  critique:
    - critique:packet-grammar-template-alignment-review
  packet:
    - packet:ralph-ticket-pktgram5-20260502T195332Z
  references:
    - skills/loom-records/references/packet-frontmatter.md
    - skills/loom-records/references/naming-and-ids.md
    - skills/loom-critique/templates/critique-packet.md
links:
  initiative:
    - initiative:skills-corpus-council-precision-pass
  plan:
    - plan:skills-corpus-council-precision-pass
  ticket:
    - ticket:pktgram5
  critique:
    - critique:packet-grammar-template-alignment-review
---

# Mission

Repair the two oracle findings from `critique:packet-grammar-template-alignment-review`
without widening packet lifecycle or review-target cleanup beyond this ticket.

# Bound Context

This is repair iteration 2 for `ticket:pktgram5`. Iteration 1 aligned packet
grammar but oracle critique found two medium issues that block closure:
dogfood-specific ticket examples leaked into product guidance, and critique packet
naming wording conflated packet target naming with the structured `review_target`
field.

# Source Snapshot

Current finding targets:

- `PKTGRAM5-CRIT-001`: replace product-surface examples using `ticket:pktgram5`
  with neutral fictional examples.
- `PKTGRAM5-CRIT-002`: clarify that critique packet IDs/filenames encode the
  packet `target` or an explicitly chosen change slug, not the structured
  `review_target` field.

# Change Class

Declared as `protocol-authority`; this repair changes packet grammar wording.

# Verification Targets

- `ticket:pktgram5#ACC-002`
- `ticket:pktgram5#ACC-003`
- `initiative:skills-corpus-council-precision-pass#OBJ-005`
- `critique:packet-grammar-template-alignment-review#PKTGRAM5-CRIT-001`
- `critique:packet-grammar-template-alignment-review#PKTGRAM5-CRIT-002`

# Task For This Iteration

1. Replace `ticket:pktgram5` examples in product-surface guidance with neutral
   fictional examples such as `ticket:abc123xy` -> `ticket-abc123xy`.
2. Reword critique packet naming guidance so it distinguishes packet `target` or
   explicit change slug from structured `review_target`.
3. Update `evidence:packet-grammar-template-alignment-validation` with repair
   observations and `git diff --check`.
4. Update `ticket:pktgram5` to show repair is complete and critique rerun is next,
   with finding dispositions still pending parent/oracle rerun.
5. Append child output to this packet. Do not close the ticket.

# Verification Posture

`observation-first`.

Record searches showing no product-surface `ticket:pktgram5` examples remain in
the changed product files, critique packet naming distinguishes packet target from
`review_target`, and `git diff --check` passes.

# Stop Conditions

Stop and return `blocked` or `escalate` if:

- the repair would touch broad `review_target` canon that belongs to
  `ticket:revtgt7x`;
- the repair would change packet lifecycle semantics owned by `ticket:pktlife6`;
- the repair would add parser/schema/runtime requirements;
- source changes outside this packet's child write scope are required.

# Output Contract

Return outcome, files changed, records changed, repair observations, validation
commands/results, risks, and ticket recommendation. The expected next route is
oracle re-critique.

# Working Notes

Parent compiled from dirty working tree after iteration 1 and oracle critique.
Dirty state is expected for this repair packet and must not be treated as stale by
itself.

# Child Output

Outcome: `stop` — repair iteration completed inside the declared
`child_write_scope`; oracle re-critique is the recommended next route.

Files changed:

- `skills/loom-records/references/packet-frontmatter.md`
- `skills/loom-records/references/naming-and-ids.md`
- `skills/loom-critique/templates/critique-packet.md`
- `.loom/tickets/20260502-pktgram5-align-packet-grammar-templates.md`
- `.loom/evidence/20260502-packet-grammar-template-alignment-validation.md`
- `.loom/packets/ralph/20260502T200144Z-ticket-pktgram5-iter-02.md`

Repair observations:

- Resolved the product-surface example leak by replacing `ticket:pktgram5` ->
  `ticket-pktgram5` examples with `ticket:abc123xy` -> `ticket-abc123xy` in the
  changed product guidance/template files.
- Clarified that critique packet IDs and filenames encode the packet `target` or
  an explicitly chosen lowercase change slug, while structured `review_target`
  describes the reviewed artifact/diff/PR/branch/commit/record.
- Updated evidence with repair observations and `git diff --check` result.
- Updated the ticket to `review_required`, with repair observed and finding
  dispositions still pending parent/oracle rerun.

Validation:

- Search over changed product surfaces for `ticket[:\-]pktgram5`: no matches.
- Search/inspection of `skills/loom-critique/templates/critique-packet.md`:
  packet naming now distinguishes encoded packet `target` / explicit change slug
  from structured `review_target`.
- `git diff --check`: passed with no output.

Residual risks:

- This child did not edit critique records and did not run oracle re-critique;
  `ticket:pktgram5#ACC-005` remains open pending parent/oracle rerun.

Recommendation:

- Parent should reconcile this packet output, then route to oracle re-critique.

# Parent Merge Notes

Parent inspected the repair output, ticket update, evidence record, and product
diff. The repair stayed inside scope, removed dogfood-specific product examples,
and clarified critique packet naming versus `review_target`. This packet is
marked `consumed`; ticket acceptance remains ticket-owned after oracle
re-critique.
