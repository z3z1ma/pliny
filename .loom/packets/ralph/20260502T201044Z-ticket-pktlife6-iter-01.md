---
id: packet:ralph-ticket-pktlife6-20260502T201044Z
kind: packet
packet_kind: ralph
status: consumed
target: ticket:pktlife6
mode: execution
change_class: protocol-authority
style: reference-first
verification_posture: observation-first
iteration: 1
created_at: 2026-05-02T20:10:44Z
updated_at: 2026-05-02T20:14:18Z
scope:
  kind: repository
  repositories:
    - repo:root
child_write_scope:
  records:
    - ticket:pktlife6
    - evidence:packet-lifecycle-parity-validation
    - packet:ralph-ticket-pktlife6-20260502T201044Z
  paths:
    - skills/loom-critique/SKILL.md
    - skills/loom-critique/templates/critique-packet.md
    - skills/loom-wiki/SKILL.md
    - skills/loom-wiki/templates/wiki-packet.md
    - skills/loom-records/references/packet-frontmatter.md
    - skills/loom-records/references/status-lifecycle.md
    - .loom/tickets/20260502-pktlife6-strengthen-packet-lifecycle-parity.md
    - .loom/evidence/20260502-packet-lifecycle-parity-validation.md
    - .loom/packets/ralph/20260502T201044Z-ticket-pktlife6-iter-01.md
parent_merge_scope:
  records:
    - ticket:pktlife6
    - evidence:packet-lifecycle-parity-validation
    - packet:ralph-ticket-pktlife6-20260502T201044Z
  paths:
    - .loom/critique/packet-lifecycle-parity-review.md
source_fingerprint:
  git_commit: 3b65266ffe67195bb548c8aa4a8e8db481fd92e1
  integration_remote: origin
  integration_ref: origin/main
  integration_commit: 3b65266ffe67195bb548c8aa4a8e8db481fd92e1
  git_status_summary: clean
  compiled_from:
    - initiative:skills-corpus-council-precision-pass
    - plan:skills-corpus-council-precision-pass
    - ticket:pktlife6
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
  max_source_files: 10
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
    - ticket:pktlife6
  references:
    - skills/loom-records/references/packet-frontmatter.md
    - skills/loom-records/references/status-lifecycle.md
    - skills/loom-critique/SKILL.md
    - skills/loom-critique/templates/critique-packet.md
    - skills/loom-wiki/SKILL.md
    - skills/loom-wiki/templates/wiki-packet.md
links:
  initiative:
    - initiative:skills-corpus-council-precision-pass
  plan:
    - plan:skills-corpus-council-precision-pass
  ticket:
    - ticket:pktlife6
---

# Mission

Strengthen critique and wiki packet lifecycle parity so those packet families
declare parent merge targets or rationale, move away from `compiled` after
reconciliation, and route outcomes back into owner layers without becoming Ralph
implementation packets.

# Bound Context

This is the sixth ticket in `plan:skills-corpus-council-precision-pass` and
covers `initiative:skills-corpus-council-precision-pass#OBJ-006`. Dependency
`ticket:pktgram5` is closed and established aligned packet grammar.

# Source Snapshot

Council finding `CR-006` observed that critique/wiki packet templates can leave
`parent_merge_scope` empty and do not strongly require status movement from
`compiled` after reconciliation. Shared lifecycle grammar already says packet
terminal statuses are `consumed`, `superseded`, and `abandoned`; the domain packet
templates and Done Means guidance should teach that explicitly for critique and
wiki packets.

Current source observations:

- `skills/loom-critique/templates/critique-packet.md` and
  `skills/loom-wiki/templates/wiki-packet.md` include empty
  `parent_merge_scope` placeholders.
- Critique and wiki skill Done Means sections do not yet mention terminal packet
  lifecycle status after packetized work.
- `skills/loom-records/references/status-lifecycle.md` already defines packet
  terminal statuses and the need for parent merge notes.

# Change Class

Declared as `protocol-authority`; this affects packet lifecycle discipline and
parent reconciliation.

# Verification Targets

- `initiative:skills-corpus-council-precision-pass#OBJ-006`
- `ticket:pktlife6#ACC-001`
- `ticket:pktlife6#ACC-002`
- `ticket:pktlife6#ACC-003`
- `ticket:pktlife6#ACC-004`

# Task For This Iteration

1. Capture before-state observations for `parent_merge_scope`, `compiled`,
   terminal packet statuses, `Parent Merge Notes`, and domain Done Means guidance
   in critique/wiki packet surfaces.
2. Update critique and wiki packet templates so `parent_merge_scope` must name
   parent reconciliation targets or explicitly say `None - rationale`.
3. Add guidance that packetized critique/wiki work must move packet status away
   from `compiled` after reconciliation, using `consumed`, `superseded`, or
   `abandoned` truthfully.
4. Update critique/wiki skill Done Means so packetized work includes parent merge
   notes, owner-layer reconciliation, and terminal packet status when a packet was
   used.
5. Keep critique/wiki packet workflows owned by critique/wiki, not Ralph.
6. Create `.loom/evidence/20260502-packet-lifecycle-parity-validation.md`.
7. Update `ticket:pktlife6` to `review_required` with evidence, claim matrix,
   retrospective/promotion disposition pending, and critique-next recommendation.
   Do not close it.

# Verification Posture

`observation-first`.

Record before/after searches for `parent_merge_scope`, `compiled`, `consumed`,
`superseded`, `abandoned`, `Parent Merge Notes`, `Done Means`, and
`git diff --check`.

# Stop Conditions

Stop and return `blocked` or `escalate` if:

- the fix would make critique or wiki packets Ralph-governed;
- the fix would require packetization for every critique or wiki pass;
- the fix would change canonical critique/wiki ownership;
- the fix would introduce a parser, schema runtime, or hidden helper;
- scope widens into broad review target cleanup owned by `ticket:revtgt7x`.

# Output Contract

Return outcome, files changed, records changed, before/after observations,
validation commands/results, risks, and ticket recommendation. Include whether
the ticket should proceed to mandatory oracle critique profiles:
`protocol-change`, `records-grammar`, and `routing-safety`.

# Working Notes

Parent compiled from clean `main` at `3b65266ffe67195bb548c8aa4a8e8db481fd92e1`.

# Child Output

Outcome: `stop` — bounded implementation iteration completed and the next route
is mandatory critique, not another implementation pass.

Files changed:

- `skills/loom-critique/SKILL.md`
- `skills/loom-critique/templates/critique-packet.md`
- `skills/loom-wiki/SKILL.md`
- `skills/loom-wiki/templates/wiki-packet.md`
- `skills/loom-records/references/packet-frontmatter.md`
- `skills/loom-records/references/status-lifecycle.md`
- `.loom/evidence/20260502-packet-lifecycle-parity-validation.md`
- `.loom/tickets/20260502-pktlife6-strengthen-packet-lifecycle-parity.md`
- `.loom/packets/ralph/20260502T201044Z-ticket-pktlife6-iter-01.md`

Evidence:

- Created `evidence:packet-lifecycle-parity-validation` with before/after
  lifecycle/template searches, ownership guardrail search, and `git diff --check`
  result.

Validation:

- Before-state `rg` captured empty critique/wiki `parent_merge_scope` placeholders
  and missing Done Means lifecycle language.
- After-state `rg` confirmed explicit parent merge target/rationale guidance,
  terminal packet statuses, `Parent Merge Notes`, and Done Means lifecycle
  language in the expected surfaces.
- Ownership guardrail `rg` confirmed critique/wiki packets remain
  critique/wiki-owned, omit Ralph `verification_posture`, and packetization
  remains optional by route.
- `git diff --check` passed with no output.

Risks:

- Structural evidence supports ACC-001 through ACC-004, but this is a
  `protocol-authority` / high-risk change and still requires oracle critique.
- ACC-005 remains open until mandatory profiles `protocol-change`,
  `records-grammar`, and `routing-safety` pass with no unresolved findings.

Recommended next route:

- Keep `ticket:pktlife6` in `review_required`.
- Run mandatory oracle critique profiles `protocol-change`, `records-grammar`,
  and `routing-safety`.
- Parent should reconcile this packet with parent merge notes and terminal packet
  lifecycle status after reviewing the child output.

# Parent Merge Notes

Parent inspected the child output, ticket update, evidence record, and product
diff. The implementation stayed inside scope and is ready for mandatory oracle
critique. This packet is marked `consumed`; ticket acceptance remains ticket-owned
after critique.
