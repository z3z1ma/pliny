---
id: "packet:ralph-ticket-<TBD: ticket token>-<TBD: UTC compact timestamp>"
kind: packet
packet_kind: ralph
status: compiled
target: "ticket:<TBD: token>"
mode: execution
change_class: "<TBD: choose one change class before saving>"
# Optional when the parent wants packet-local risk carried explicitly:
# risk_class: "<TBD: choose low, medium, or high before saving>"
style: "<TBD: choose reference-first, snapshot-first, or hermetic before saving>"
verification_posture: "<TBD: choose test-first, observation-first, or none before saving>"
iteration: "<TBD: positive integer>"
created_at: "<TBD: UTC timestamp>"
updated_at: "<TBD: UTC timestamp>"
scope:
  kind: repository
  repositories:
    - repo:root
child_write_scope:
  records:
    - "None - child returns output only unless parent grants exact narrow record refs"
  paths:
    - "<TBD: paths or globs the child may modify, or None - rationale>"
parent_merge_scope:
  records:
    - "ticket:<TBD: token>"
  paths:
    - "<TBD: paths the parent must reconcile, or None - rationale>"
source_fingerprint:
  git_commit: "<TBD: sha or unknown with rationale>"
  integration_remote: "<TBD: remote name, none, or unknown with rationale>"
  integration_ref: "<TBD: ref, tag, commit, or unknown with rationale>"
  integration_commit: "<TBD: sha or unknown with rationale>"
  git_status_summary: "<TBD: clean, dirty_tracked, dirty_untracked, dirty_mixed, or unknown>"
  git_status_detail: "<TBD: short status detail or unknown - rationale>"
  compiled_from:
    - "ticket:<TBD: token>"
execution_context:
  branch: "<TBD: branch name or unknown with rationale>"
  push_remote: "<TBD: remote name, same_as_integration, none, or unknown with rationale>"
  worktree: "<TBD: path, none, or unknown with rationale>"
  isolation: none
  git_shared_metadata_mutations: forbidden
  destructive_commands: forbidden
  network: "<TBD: choose allowed, forbidden, or unknown - rationale that makes launch safe before saving>"
context_budget:
  posture: normal
  max_source_files: 8
  max_excerpt_lines_per_file: 80
  avoid_full_file_reads: true
sources:
  constitution:
    - constitution:main
  initiative: []
  research: []
  spec: []
  plan: []
  ticket:
    - "ticket:<TBD: token>"
links: {}
---

# Mission

What this one bounded iteration should achieve and why it is the next safe step.

# Bound Context

The owner chain that constrains the child. Name intended behavior separately from
current implementation reality. Use `skills/loom-ralph/references/packet-contract.md`
for field-level rules when compiling or reviewing this packet.

# Parent Launch Checklist

Before launch, the parent verifies:

- target ticket is Ralph-ready and matches this packet's scope;
- source fingerprint still matches governing records and child-write-scope files;
- child write scope and parent merge scope are exact or explicitly `None - reason`;
- Git, network, destructive-command, and shared-metadata posture are safe;
- verification posture fits the change class and evidence expectation;
- stop conditions and output contract are complete;
- no unresolved template placeholders or example IDs remain.

If any check fails, reconcile the ticket or supersede the packet before launch.

# Source Snapshot

Curated excerpts, summaries, or directions to the source records and files the child should read.

# Assumptions / Decision Triggers

- Assumption or question: `<TBD or None - no material assumptions>`
  - Reversible: `<yes/no>`
  - Blocks child work: `<yes/no>`
  - Disposition: `<accepted, ask parent/user, or route to owner>`

# Change Class

Declared above as `change_class`. Explain how it affects evidence, critique,
verification posture, and write-scope risk for this iteration.

# Quality Delta

Baseline/current state:

Expected improvement:

How the parent will judge the delta:

Known non-goals:

# Verification Targets

Stable claim or acceptance IDs this iteration should satisfy or exercise. List
real qualified IDs, or write `None - reason`.

# Task For This Iteration

The exact bounded task for the child.

# Verification Posture

Declared above as `verification_posture`.

- `test-first`: name the failing check, expected failure reason, red command or procedure, green command or procedure, and broader regression command if expected.
- `observation-first`: name the before-state observation, after-state observation, and artifact capture method.
- `none`: justify why this iteration is genuinely verification-neutral.

# Stop Conditions

When the child should stop, block, or escalate instead of widening scope.

Include freshness, write-scope, execution-context, and posture-specific stops. For
`test-first`, the failing check must exist before implementation and be driven to
green inside this iteration. For `observation-first`, before and after evidence
must be captured.

# Output Contract

The child must return:

- outcome (`continue|stop|blocked|escalate`);
- files changed;
- records changed;
- evidence gathered, including red/green or before/after artifacts when applicable;
- quality delta achieved or not achieved;
- uncertainty discovered or questions that should have been asked earlier;
- self-review findings, risks, and maintainability concerns;
- ticket recommendation. The child recommends; the parent commits ticket truth.

# Working Notes

Optional parent notes before launch.

# Child Output

To be filled by the child or copied back by the parent.

# Parent Merge Notes

What the parent concluded after reconciliation, including packet lifecycle status.
