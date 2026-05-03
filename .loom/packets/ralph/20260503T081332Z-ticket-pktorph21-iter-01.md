---
id: packet:ralph-ticket-pktorph21-20260503T081332Z
kind: packet
packet_kind: ralph
status: consumed
target: ticket:pktorph21
mode: execution
change_class: protocol-authority
risk_class: medium
style: reference-first
verification_posture: observation-first
iteration: 1
created_at: 2026-05-03T08:13:33Z
updated_at: 2026-05-03T08:15:26Z
scope:
  kind: repository
  repositories:
    - repo:root
child_write_scope:
  records:
    - None - child returns output only; parent reconciles ticket, evidence, critique, and packet status.
  paths:
    - skills/loom-records/references/repair-and-drift.md
parent_merge_scope:
  records:
    - ticket:pktorph21
  paths:
    - .loom/tickets/20260503-pktorph21-route-orphan-packets-by-family.md
    - .loom/evidence/20260503-orphan-packet-family-routing-validation.md
    - .loom/critique/orphan-packet-family-routing-review.md
    - .loom/packets/ralph/20260503T081332Z-ticket-pktorph21-iter-01.md
source_fingerprint:
  git_commit: cbd863cbc3e155c4fbb7129aa93d03fdf86f63ca
  integration_remote: origin
  integration_ref: origin/main
  integration_commit: cbd863cbc3e155c4fbb7129aa93d03fdf86f63ca
  git_status_summary: dirty_mixed
  git_status_detail: parent-owned ticket and packet records are modified/untracked for launch; child write-scope file is clean relative to cbd863c
  compiled_from:
    - ticket:pktorph21
    - ticket:ralphg20
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
  posture: tight
  max_source_files: 5
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
    - ticket:pktorph21
  files:
    - skills/loom-records/references/repair-and-drift.md
    - skills/loom-records/references/packet-frontmatter.md
    - skills/loom-ralph/references/packet-contract.md
links: {}
---

# Mission

Route orphan packet repair by packet family instead of defaulting mainly to
Ralph.

# Bound Context

`ticket:pktorph21` covers `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-022`.
Loom now has Ralph, critique, and wiki packet families. Orphan packet repair must
inspect the packet's `packet_kind` or path family and route repair to the owning
workflow, while preserving ticket-owned live execution truth.

# Source Snapshot

- `skills/loom-records/references/repair-and-drift.md` currently routes orphan
  packets to `loom-ralph` or packet lifecycle marking.
- Shared packet grammar names packet families through `packet_kind` values:
  `ralph`, `critique`, and `wiki`.
- Unknown, missing, or contradictory packet family metadata should be records
  repair before downstream workflow repair.

# Change Class

Declared as `protocol-authority` with medium risk. The edit changes repair
routing guidance and must stay Markdown-native: no new packet family, migration,
validator, scanner, command wrapper, generated index, runtime, or owner layer.

# Verification Targets

- `initiative:skills-corpus-context-integrity-hardening-pass#OBJ-022`
- `ticket:pktorph21#ACC-001`
- `ticket:pktorph21#ACC-002`
- `ticket:pktorph21#ACC-003`
- `ticket:pktorph21#ACC-004`

# Task For This Iteration

Make the smallest coherent repair-routing edit in
`skills/loom-records/references/repair-and-drift.md`:

1. Update orphan packet repair routing to inspect `packet_kind` or path family.
2. Route Ralph packets to Ralph packet lifecycle / stale packet recovery guidance,
   critique packets to critique review-packet repair, and wiki packets to wiki
   synthesis-packet repair.
3. Route unknown, missing, or contradictory packet family metadata to
   `records_repair` / `loom-records` before downstream workflow repair.
4. Preserve ticket truth: orphan packet repair can mark packet support artifacts
   `superseded` or `abandoned`, but it does not reopen or close tickets by itself.
5. Do not add packet families or migrate historical packets.
6. Do not add a validator, scanner, schema engine, command wrapper, generated
   index, runtime, hidden helper, or new owner layer.

# Verification Posture

Observation-first. Before and after editing, report targeted observations for:

- orphan packet routing language;
- `packet_kind` or path-family inspection;
- `ralph`, `critique`, and `wiki` repair routes;
- unknown/missing/contradictory packet family route to records repair;
- ticket truth / packet-family ownership separation;
- absence of new packet families, migrations, validators, scanners, or runtime
  mechanisms.

Run `git diff --check` after editing.

# Stop Conditions

Stop and return `blocked` or `escalate` if:

- satisfying the ticket would require adding packet families, migrating historical
  packets, or adding runtime/scanner/validator machinery;
- the change would route critique or wiki packet repair through Ralph by default;
- the change would let orphan packet repair own live ticket execution state;
- the needed edits extend beyond `repair-and-drift.md` in a way that cannot be
  safely summarized for the parent.

Do not run `git fetch`, remote edits, Git config edits, destructive commands, or
shared Git metadata mutations. Do not edit parent-owned `.loom` records.

# Output Contract

Return outcome, files changed, records changed, before/after observations,
`git diff --check` result, self-review, blockers/residual risks, and recommended
ticket state/next route.

# Working Notes

Parent compiled from clean `main` at `cbd863c` after closing and pushing
`ticket:ralphg20`. Saving this packet and activating the ticket made the worktree
`dirty_mixed` before child launch; those parent-owned `.loom` records are outside
child write scope. The product file in `child_write_scope.paths` remains clean
relative to `cbd863c` at launch.

# Child Output

Outcome: `stop`

Files changed:

- `skills/loom-records/references/repair-and-drift.md`

Records changed by child:

- None. Parent retained ticket, evidence, critique, and packet reconciliation.

Before observations:

- Orphan packet routing defaulted to `loom-ralph` or marking packets
  `superseded` / `abandoned`.
- No `packet_kind` or path-family inspection was named.
- No distinct Ralph / critique / wiki packet repair routes were present.
- Unknown, missing, or contradictory packet family metadata had no packet-specific
  records-repair route.
- Ticket truth separation existed generally, but not specifically for orphan
  packet repair.
- No new packet families, migrations, validators, scanners, or runtime mechanisms
  existed.

After observations:

- Orphan packet repair now inspects `packet_kind` and `.loom/packets/<family>/`.
- Ralph packets route to `loom-ralph` packet lifecycle / stale packet recovery
  guidance.
- Critique packets route to `loom-critique` review-packet repair.
- Wiki packets route to `loom-wiki` synthesis-packet repair.
- Missing, unknown, or contradictory packet family metadata routes to
  `records_repair` / `loom-records` before downstream workflow repair.
- Orphan packet repair may update packet support-artifact lifecycle state, but it
  does not reopen, close, or own live ticket execution truth.
- No packet families, migrations, validators, scanners, command wrappers,
  generated indexes, runtimes, hidden helpers, or owner layers were added.

Verification:

- `git diff --check` passed with no output.

Self-review:

- Stayed within `child_write_scope.paths`.
- Did not modify `.loom` records.
- Preserved Markdown-native guidance only.
- Did not route critique or wiki packets through Ralph by default.

Blockers or residual risks:

- No blockers.
- Medium-risk protocol guidance change requires parent-side evidence
  reconciliation and mandatory critique before acceptance.

Recommendation:

- Move `ticket:pktorph21` to `review_required` and route to mandatory critique.

# Parent Merge Notes

- 2026-05-03T08:15:26Z: Parent accepted the bounded implementation output,
  recorded `evidence:orphan-packet-family-routing-validation`, marked this packet
  `consumed`, and moved `ticket:pktorph21` to `review_required` for mandatory
  critique.
