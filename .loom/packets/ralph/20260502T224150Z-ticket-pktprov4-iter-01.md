---
id: packet:ralph-ticket-pktprov4-20260502T224150Z
kind: packet
packet_kind: ralph
status: consumed
target: ticket:pktprov4
mode: execution
change_class: protocol-authority
risk_class: medium
style: reference-first
verification_posture: observation-first
iteration: 1
created_at: 2026-05-02T22:41:50Z
updated_at: 2026-05-02T22:45:58Z
scope:
  kind: repository
  repositories:
    - repo:root
child_write_scope:
  records:
    - ticket:pktprov4
    - evidence:packet-provenance-sources-validation
    - packet:ralph-ticket-pktprov4-20260502T224150Z
  paths:
    - skills/loom-records/references/packet-frontmatter.md
    - skills/loom-ralph/templates/ralph-packet.md
    - skills/loom-critique/templates/critique-packet.md
    - skills/loom-wiki/templates/wiki-packet.md
    - .loom/tickets/20260502-pktprov4-split-packet-provenance-sources.md
    - .loom/evidence/20260502-packet-provenance-sources-validation.md
    - .loom/packets/ralph/20260502T224150Z-ticket-pktprov4-iter-01.md
parent_merge_scope:
  records:
    - ticket:pktprov4
    - evidence:packet-provenance-sources-validation
    - packet:ralph-ticket-pktprov4-20260502T224150Z
  paths: []
source_fingerprint:
  git_commit: c70983ffd03d56c5fcf74475c9bc454071e1ae5d
  integration_remote: origin
  integration_ref: origin/main
  integration_commit: c70983ffd03d56c5fcf74475c9bc454071e1ae5d
  git_status_summary: clean
  compiled_from:
    - initiative:skills-corpus-template-grammar-safety-pass
    - plan:skills-corpus-template-grammar-safety-pass
    - ticket:pktprov4
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
  max_source_files: 7
  max_excerpt_lines_per_file: 160
  avoid_full_file_reads: false
sources:
  initiative:
    - initiative:skills-corpus-template-grammar-safety-pass
  plan:
    - plan:skills-corpus-template-grammar-safety-pass
  ticket:
    - ticket:pktprov4
  records:
    - skills/loom-records/references/packet-frontmatter.md
    - skills/loom-ralph/templates/ralph-packet.md
    - skills/loom-critique/templates/critique-packet.md
    - skills/loom-wiki/templates/wiki-packet.md
links:
  ticket:
    - ticket:pktprov4
---

# Mission

Define the split between packet `source_fingerprint.compiled_from` provenance and
the packet `sources` context set, then align the Ralph, critique, and wiki packet
templates with that split.

# Bound Context

This is the fourth ticket in `plan:skills-corpus-template-grammar-safety-pass` and
covers `initiative:skills-corpus-template-grammar-safety-pass#OBJ-004`. Packets
remain support artifacts; the split must not make critique/wiki packets
Ralph-governed or add runtime/schema enforcement.

# Source Snapshot

Baseline commit: `c70983ffd03d56c5fcf74475c9bc454071e1ae5d`, matching
`origin/main`. Worktree was clean before packet creation.

Initial parent inspection found shared packet frontmatter documenting both
`source_fingerprint.compiled_from` and `sources`, but the prose only says
`compiled_from` is part of the compilation baseline and `sources` are the source
record set compiled into or referenced by the packet. Packet templates may not
make the provenance/context distinction obvious enough when copied.

# Change Class

Declared as `protocol-authority`; risk is medium because packet provenance
grammar affects replayability, freshness checks, and sibling packet family
boundaries.

# Verification Targets

- `initiative:skills-corpus-template-grammar-safety-pass#OBJ-004`
- `ticket:pktprov4#ACC-001`
- `ticket:pktprov4#ACC-002`
- `ticket:pktprov4#ACC-003`
- `ticket:pktprov4#ACC-004`

# Task For This Iteration

1. Capture before-state searches for `compiled_from`, `sources:`,
   `source_fingerprint`, and packet family template mentions in the targeted
   packet frontmatter reference and Ralph/critique/wiki packet templates.
2. Clarify shared packet grammar so `source_fingerprint.compiled_from` means the
   owner records or artifacts used to compile the packet baseline/provenance, and
   `sources` means the context source set the packet consumer should read or trust
   for the bounded task.
3. Align the Ralph, critique, and wiki packet templates so copied packets preserve
   that split without performative duplicate source lists.
4. Preserve packet family boundaries:
   - Ralph packets remain implementation packets;
   - critique packets remain critique-owned review packets;
   - wiki packets remain wiki-owned synthesis packets;
   - critique/wiki packets do not inherit Ralph verification posture or child
     obligations merely because they share packet grammar.
5. Do not add a parser, schema, runtime, command wrapper, hidden helper, or new
   owner layer.
6. Update `ticket:pktprov4` to `review_required` with evidence linked, claim
   matrix current, and next route `critique`.
7. Record `evidence:packet-provenance-sources-validation` with before/after
   searches and `git diff --check`.
8. Fill this packet's `# Child Output`. The parent will mark the packet consumed
   after reconciliation.

# Verification Posture

`observation-first`.

Capture before/after searches for the provenance/context terms above. Run
`git diff --check` after edits.

# Stop Conditions

Stop and return `blocked` or `escalate` if:

- the fix would require runtime validation, a parser, schema enforcement, or a
  new owner layer;
- aligning templates would make critique/wiki packets Ralph-governed;
- the source/context split cannot be explained without broader packet grammar
  redesign;
- the source fingerprint is materially stale before launch.

# Output Contract

Return outcome, files changed, records changed, before/after observation
commands/results, `git diff --check` result, residual risks, and ticket
recommendation. Include whether the ticket should proceed to mandatory oracle
critique with profiles `records-grammar`, `routing-safety`, and `owner-boundary`.

# Working Notes

Parent created this packet after confirming `ticket:drvgram3` was closed and
pushed and the worktree was clean at the source fingerprint.

# Child Output

Outcome: `stop`.

## Changed Files / Records

- `skills/loom-records/references/packet-frontmatter.md`: Added explicit
  provenance versus context-source grammar for `source_fingerprint.compiled_from`
  and `sources`, plus comments in YAML examples.
- `skills/loom-ralph/templates/ralph-packet.md`: Added copied-template guidance
  that Ralph `compiled_from` is provenance and `sources` is child context.
- `skills/loom-critique/templates/critique-packet.md`: Added copied-template
  guidance that critique `compiled_from` is review-baseline provenance and
  `sources` is reviewer context without making the packet Ralph-governed.
- `skills/loom-wiki/templates/wiki-packet.md`: Added copied-template guidance
  that wiki `compiled_from` is synthesis-baseline provenance and `sources` is
  accepted-truth context without making the packet Ralph-governed.
- `.loom/tickets/20260502-pktprov4-split-packet-provenance-sources.md`
  (`ticket:pktprov4`): Moved to `review_required`, linked evidence, updated
  claim matrix, and set next route to mandatory oracle critique.
- `.loom/evidence/20260502-packet-provenance-sources-validation.md`
  (`evidence:packet-provenance-sources-validation`): Recorded before/after
  searches and `git diff --check`.
- `.loom/packets/ralph/20260502T224150Z-ticket-pktprov4-iter-01.md`: Filled
  child output only; parent merge notes remain for the parent.

## Before / After Observation Highlights

- Before `compiled_from|sources:|source_fingerprint` search showed the fields in
  the shared frontmatter reference and packet templates, but no explicit prose
  separating provenance from consumer context.
- After the same search showed new shared reference prose at
  `packet-frontmatter.md` under `## Provenance Versus Context Sources` and
  template guidance in the Ralph, critique, and wiki packet templates.
- Before packet-family search already showed Ralph/critique/wiki ownership
  boundaries and critique/wiki omission of Ralph `verification_posture`.
- After packet-family search showed those boundaries still present, plus
  family-specific context comments for Ralph child, critique reviewer, and wiki
  synthesizer sources.

Full observation output is recorded in
`evidence:packet-provenance-sources-validation`.

## Validation

- Source fingerprint freshness: `git rev-parse HEAD` matched
  `c70983ffd03d56c5fcf74475c9bc454071e1ae5d`; the only pre-existing dirty
  surfaces observed were the parent-updated ticket and this untracked packet.
- `git diff --check`: passed with no output.

## Residual Risks / Concerns

- No parser, schema, runtime, command wrapper, hidden helper, or new owner layer
  was added.
- The change is structural Markdown guidance. Mandatory oracle critique should
  still review the grammar with profiles `records-grammar`, `routing-safety`, and
  `owner-boundary` before acceptance.

## Ticket Recommendation

Keep `ticket:pktprov4` in `review_required` and route next to mandatory oracle
critique with profiles `records-grammar`, `routing-safety`, and
`owner-boundary`. Do not close until `ticket:pktprov4#ACC-005` is satisfied and
the ticket owns any critique finding dispositions.

# Parent Merge Notes

Parent accepted the child output as scoped and routed the ticket to mandatory
oracle critique. Parent reconciliation normalized `ticket:pktprov4` claim matrix
statuses to canonical claim-coverage vocabulary, expanded
`evidence:packet-provenance-sources-validation` with support and validity
sections, and left the ticket in `review_required` because required critique has
not yet run.
