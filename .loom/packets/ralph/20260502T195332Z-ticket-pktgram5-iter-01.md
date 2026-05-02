---
id: packet:ralph-ticket-pktgram5-20260502T195332Z
kind: packet
packet_kind: ralph
status: consumed
target: ticket:pktgram5
mode: execution
change_class: protocol-authority
style: reference-first
verification_posture: observation-first
iteration: 1
created_at: 2026-05-02T19:53:33Z
updated_at: 2026-05-02T19:58:59Z
scope:
  kind: repository
  repositories:
    - repo:root
child_write_scope:
  records:
    - ticket:pktgram5
    - evidence:packet-grammar-template-alignment-validation
    - packet:ralph-ticket-pktgram5-20260502T195332Z
  paths:
    - skills/loom-records/references/packet-frontmatter.md
    - skills/loom-records/references/naming-and-ids.md
    - skills/loom-ralph/templates/ralph-packet.md
    - skills/loom-ralph/references/packet-contract.md
    - skills/loom-critique/templates/critique-packet.md
    - skills/loom-wiki/templates/wiki-packet.md
    - .loom/tickets/20260502-pktgram5-align-packet-grammar-templates.md
    - .loom/evidence/20260502-packet-grammar-template-alignment-validation.md
    - .loom/packets/ralph/20260502T195332Z-ticket-pktgram5-iter-01.md
parent_merge_scope:
  records:
    - ticket:pktgram5
    - evidence:packet-grammar-template-alignment-validation
    - packet:ralph-ticket-pktgram5-20260502T195332Z
  paths:
    - .loom/critique/packet-grammar-template-alignment-review.md
source_fingerprint:
  git_commit: cceb6422bf5c95cfaf2c45983bb6a412c748c94f
  integration_remote: origin
  integration_ref: origin/main
  integration_commit: cceb6422bf5c95cfaf2c45983bb6a412c748c94f
  git_status_summary: clean
  compiled_from:
    - initiative:skills-corpus-council-precision-pass
    - plan:skills-corpus-council-precision-pass
    - ticket:pktgram5
    - ticket:rtvocab1
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
  max_excerpt_lines_per_file: 140
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
  references:
    - skills/loom-records/references/packet-frontmatter.md
    - skills/loom-records/references/naming-and-ids.md
    - skills/loom-ralph/templates/ralph-packet.md
    - skills/loom-critique/templates/critique-packet.md
    - skills/loom-wiki/templates/wiki-packet.md
links:
  initiative:
    - initiative:skills-corpus-council-precision-pass
  plan:
    - plan:skills-corpus-council-precision-pass
  ticket:
    - ticket:pktgram5
---

# Mission

Align shared packet frontmatter grammar with Ralph, critique, and wiki packet
templates so packet fields, ID/filename mapping, context budget defaults, and
freshness expectations teach one coherent packet contract.

# Bound Context

This is the fifth ticket in `plan:skills-corpus-council-precision-pass` and
covers `initiative:skills-corpus-council-precision-pass#OBJ-005`. Dependency
`ticket:rtvocab1` is closed. This ticket must preserve the distinction between
Ralph implementation packets and critique/wiki sibling packet workflows.

# Source Snapshot

Council finding `CR-005` observed drift around `context_budget.posture`,
`iteration`, `change_class`, optional `risk_class`, source freshness checks, and
packet ID versus filename mapping.

Current source observations:

- `skills/loom-records/references/packet-frontmatter.md` defines common packet
  shape but does not include `change_class`, `risk_class`, `iteration`, or
  `verification_posture` in the common shape; later sections explain some of
  those as family-specific or optional.
- `skills/loom-ralph/templates/ralph-packet.md` includes `change_class`,
  `verification_posture`, and `iteration: 1`.
- `skills/loom-critique/templates/critique-packet.md` includes `change_class` and
  `review_target`, and intentionally omits Ralph `verification_posture`.
- `skills/loom-wiki/templates/wiki-packet.md` omits `change_class` and Ralph
  `verification_posture`.
- `skills/loom-records/references/naming-and-ids.md` already contains packet ID
  and filename patterns; this ticket may align wording if the packet-frontmatter
  reference and templates do not point at that convention clearly enough.

# Change Class

Declared as `protocol-authority`; this governs packet authority and fresh-context
handoff contracts.

# Verification Targets

- `initiative:skills-corpus-council-precision-pass#OBJ-005`
- `ticket:pktgram5#ACC-001`
- `ticket:pktgram5#ACC-002`
- `ticket:pktgram5#ACC-003`
- `ticket:pktgram5#ACC-004`

# Task For This Iteration

1. Capture before-state observations comparing shared packet frontmatter against
   Ralph, critique, and wiki packet templates for required/optional fields,
   `iteration`, `change_class`, optional `risk_class`, context budget defaults,
   source freshness, and ID/filename mapping.
2. Update packet-frontmatter grammar and allowed templates so the shared shape and
   family-specific additions are explicit and consistent.
3. Clarify packet ID and filename conventions by linking or restating the naming
   guidance where packet authors need it.
4. Clarify source freshness stop conditions without making critique/wiki packets
   Ralph-governed.
5. Create `.loom/evidence/20260502-packet-grammar-template-alignment-validation.md`.
6. Update `ticket:pktgram5` to `review_required` with evidence, claim matrix,
   retrospective/promotion disposition pending, and critique-next recommendation.
   Do not close it.

# Verification Posture

`observation-first`.

Record before/after searches for `iteration`, `change_class`, `risk_class`,
`verification_posture`, `context_budget`, `source_fingerprint`,
`child_write_scope`, `parent_merge_scope`, packet IDs, packet filenames, and
`git diff --check`.

# Stop Conditions

Stop and return `blocked` or `escalate` if:

- the fix would make critique or wiki packets Ralph-governed;
- the fix would require a packet parser, schema runtime, or hidden validation
  helper;
- the fix would normalize historical packets instead of current product grammar;
- the fix would widen into lifecycle reconciliation semantics owned by
  `ticket:pktlife6`;
- scope widens into unrelated template placeholder cleanup owned by
  `ticket:tmplph8x`.

# Output Contract

Return outcome, files changed, records changed, before/after observations,
validation commands/results, risks, and ticket recommendation. Include whether
the ticket should proceed to mandatory oracle critique profiles:
`protocol-change`, `records-grammar`, and `routing-safety`.

# Working Notes

Parent compiled from clean `main` at `cceb6422bf5c95cfaf2c45983bb6a412c748c94f`.

# Child Output

Outcome: stop - bounded implementation iteration complete; parent route should
proceed to mandatory critique before acceptance.

Files changed:

- `skills/loom-records/references/packet-frontmatter.md`
- `skills/loom-records/references/naming-and-ids.md`
- `skills/loom-ralph/templates/ralph-packet.md`
- `skills/loom-ralph/references/packet-contract.md`
- `skills/loom-critique/templates/critique-packet.md`
- `skills/loom-wiki/templates/wiki-packet.md`
- `.loom/tickets/20260502-pktgram5-align-packet-grammar-templates.md`
- `.loom/evidence/20260502-packet-grammar-template-alignment-validation.md`
- `.loom/packets/ralph/20260502T195332Z-ticket-pktgram5-iter-01.md`

Records changed:

- `ticket:pktgram5`
- `evidence:packet-grammar-template-alignment-validation`
- `packet:ralph-ticket-pktgram5-20260502T195332Z`

Evidence gathered:

- Before/after comparison captured in
  `evidence:packet-grammar-template-alignment-validation`.
- Targeted searches covered `iteration`, `change_class`, `risk_class`,
  `verification_posture`, `context_budget`, `source_fingerprint`,
  `child_write_scope`, `parent_merge_scope`, packet IDs, and packet filenames.
- `git diff --check` passed with no output.

Self-review / concerns:

- Scope stayed within current packet grammar/templates and did not normalize
  historical packets.
- Critique and wiki packet templates remain owned by their workflows and do not
  gain Ralph `verification_posture` or Ralph child obligations.
- No parser, schema runtime, or hidden validation helper was added.

Blockers or risks:

- Mandatory critique remains pending for `protocol-change`, `records-grammar`,
  and `routing-safety` profiles.

Ticket recommendation:

- Keep `ticket:pktgram5` in `review_required` until mandatory critique and parent
  acceptance reconciliation complete. Do not close from this child output alone.

# Parent Merge Notes

Parent inspected the child output, ticket update, evidence record, and product
diff. Parent corrected the remaining generic Ralph filename examples in
`skills/loom-records/references/naming-and-ids.md` from `iter-01` to `iter-<NN>`
so they match the new iteration grammar. The implementation stayed inside scope
and is ready for mandatory oracle critique. This packet is marked `consumed`;
ticket acceptance remains ticket-owned after critique.
