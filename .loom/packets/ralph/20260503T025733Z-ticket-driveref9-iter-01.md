---
id: packet:ralph-ticket-driveref9-20260503T025733Z
kind: packet
packet_kind: ralph
status: consumed
target: ticket:driveref9
mode: execution
change_class: documentation-explanation
risk_class: medium
style: reference-first
verification_posture: observation-first
iteration: 1
created_at: 2026-05-03T02:57:34Z
updated_at: 2026-05-03T03:00:29Z
scope:
  kind: repository
  repositories:
    - repo:root
child_write_scope:
  records:
    - None - child returns output only; parent reconciles ticket, evidence, critique, and packet status.
  paths:
    - skills/loom-drive/SKILL.md
    - skills/loom-drive/references/outer-loop-subagent-transport.md
parent_merge_scope:
  records:
    - ticket:driveref9
  paths:
    - .loom/tickets/20260503-driveref9-move-drive-transport-reference.md
    - .loom/evidence/20260503-drive-transport-reference-validation.md
    - .loom/critique/drive-transport-reference-review.md
    - .loom/packets/ralph/20260503T025733Z-ticket-driveref9-iter-01.md
source_fingerprint:
  git_commit: 559aeea1c73a77c7a18152ac019a5e8553ab3467
  integration_remote: origin
  integration_ref: origin/main
  integration_commit: 559aeea1c73a77c7a18152ac019a5e8553ab3467
  git_status_summary: clean
  git_status_detail: clean working tree at packet compile time
  compiled_from:
    - ticket:driveref9
    - plan:skills-corpus-residual-protocol-sharpening-pass
    - research:skills-corpus-residual-audit-synthesis
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
  max_source_files: 8
  max_excerpt_lines_per_file: 120
  avoid_full_file_reads: true
sources:
  constitution:
    - constitution:main
    - decision:0001
    - decision:0002
    - decision:0006
  initiative:
    - initiative:skills-corpus-residual-protocol-sharpening-pass
  research:
    - research:skills-corpus-residual-audit-synthesis
  spec: []
  plan:
    - plan:skills-corpus-residual-protocol-sharpening-pass
  ticket:
    - ticket:driveref9
  files:
    - skills/loom-drive/SKILL.md
    - skills/loom-drive/templates/outer-loop-handoff.md
links: {}
---

# Mission

Fix `ticket:driveref9` by moving detailed optional outer-loop subagent transport
mechanics out of `skills/loom-drive/SKILL.md` and into a discoverable reference,
while preserving behavior and support-surface boundaries.

# Bound Context

The governing plan is `plan:skills-corpus-residual-protocol-sharpening-pass`.
This ticket follows `ticket:srcmeta13` in the strict sequential pass.

Keep these boundaries:

- `loom-drive` remains a workflow coordinator, not a truth owner;
- tickets retain live execution ownership;
- saved outer-loop handoffs remain optional support artifacts, not packets and
  not canonical truth owners;
- parent reconciliation remains mandatory before dependent work launches;
- do not shorten frontmatter activation descriptions;
- do not change drive behavior, handoff metadata semantics, support ownership,
  or route vocabulary;
- do not add validators, schemas, command wrappers, helper scripts, runtime
  enforcement, or new canonical owner layers.

# Source Snapshot

Current relevant state at baseline `559aeea`:

- `skills/loom-drive/SKILL.md` contains a long `## Optional Outer-Loop Subagent
  Transport` section with detailed support-artifact mechanics.
- The read order currently points to `templates/outer-loop-handoff.md` only when
  launching an optional bounded outer-loop synthesis subagent.
- `skills/loom-drive/templates/outer-loop-handoff.md` already preserves detailed
  support-local metadata and parent reconciliation wording. Treat it as context,
  not a required edit target.

# Change Class

Declared above as `documentation-explanation` with medium risk because moving
workflow guidance can accidentally drop support-surface or parent-reconciliation
constraints.

# Verification Targets

- `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-011`
- `ticket:driveref9#ACC-001`
- `ticket:driveref9#ACC-002`
- `ticket:driveref9#ACC-003`
- `ticket:driveref9#ACC-004`

# Task For This Iteration

Make the smallest corpus edits that satisfy `ticket:driveref9`:

1. Create `skills/loom-drive/references/outer-loop-subagent-transport.md` and move
   the detailed optional outer-loop subagent transport mechanics there.
2. Keep `skills/loom-drive/SKILL.md` concise: retain the high-level rule that a
   dedicated outer-loop subagent is optional transport for context management and
   point readers to the new reference for details.
3. Update read order so the new reference is read only when optional outer-loop
   subagent transport is relevant. Keep the handoff template conditional and do
   not make it a normal read for all drive activations.
4. Preserve support-surface boundaries, handoff metadata semantics, parent
   reconciliation requirements, and the distinction from Ralph packets.

Do not update Loom tickets, evidence, critique, or this packet. The parent will
reconcile those after inspecting the returned diff.

# Verification Posture

Declared above as `observation-first`.

Before editing, inspect/report current matches for `Optional Outer-Loop Subagent
Transport`, `support artifact`, `.loom/support/drive-handoffs`, `parent
reconciliation`, `not a packet`, `handoff_write_scope`, and read-order references
in the write-scope files. After editing, report the same targeted observations
and whether `git diff --check` passes.

# Stop Conditions

Stop and report `blocked` or `escalate` if:

- governing records or child-write-scope files differ materially from this packet;
- preserving behavior would require editing templates or other references outside
  the declared child write scope;
- the change would alter handoff frontmatter semantics, route vocabulary, support
  artifact ownership, or parent reconciliation authority;
- the change would make saved handoffs canonical, packet-family artifacts, or
  truth owners;
- the change would add runtime validation, schemas, command wrappers, helper
  scripts, or new canonical owner layers.

# Output Contract

Return:

- outcome (`continue|stop|blocked|escalate`);
- files changed;
- records changed (`None` expected);
- before/after observations and `git diff --check` result;
- self-review findings or concerns;
- blockers or residual risks;
- recommended ticket state and next route.

# Working Notes

Parent compiled from clean `main` at `559aeea` after pushing `ticket:srcmeta13`.

# Child Output

Outcome: stop

Files changed:

- `skills/loom-drive/SKILL.md`
- `skills/loom-drive/references/outer-loop-subagent-transport.md`

Records changed: None.

Before observations:

- `Optional Outer-Loop Subagent Transport`: `SKILL.md:222`
- `support artifact`: `SKILL.md:69`, `SKILL.md:236`
- `.loom/support/drive-handoffs`: `SKILL.md:240`
- `parent reconciliation`: `SKILL.md:234`
- `not a packet`: `SKILL.md:247`
- `handoff_write_scope`: `SKILL.md:71`, `SKILL.md:248`
- read-order references: `SKILL.md:292-317`; handoff template conditional at
  `SKILL.md:317`
- new reference file did not exist

After observations:

- `Optional Outer-Loop Subagent Transport`: `SKILL.md:222`
- `support artifact`: `SKILL.md:69`, new reference lines 31, 41, and 59
- `.loom/support/drive-handoffs`: new reference line 36
- `parent reconciliation`: new reference line 21
- `not a packet`: new reference line 50
- `handoff_write_scope`: `SKILL.md:71`, new reference line 54
- read-order references: `SKILL.md:271-298`; new reference conditional at
  `SKILL.md:296-297`; template remains conditional at `SKILL.md:298-299`

Validation: `git diff --check` passed with no output.

Self-review:

- Detailed transport mechanics were moved into the new reference.
- `SKILL.md` now keeps only concise high-level optional-transport guidance and
  points to the reference.
- Handoff template remains conditional and was not edited.

Blockers/residual risks: no blockers. Parent should review the moved wording for
exact doctrine preservation before record reconciliation.

Recommendation: set ticket to `review_required`; next route is parent
reconciliation followed by critique/acceptance review.

# Parent Merge Notes

Accepted child output as in scope. Parent reviewed the diff, recorded evidence
`evidence:drive-transport-reference-validation`, moved `ticket:driveref9` to
`review_required`, and routed next to mandatory oracle critique.
