---
id: packet:ralph-ticket-<token>-<UTC compact timestamp>
kind: packet
packet_kind: ralph
status: compiled
target: ticket:<token>
mode: execution
change_class: "<TBD: choose one change class before saving>"
# Optional when the parent wants packet-local risk carried explicitly:
# risk_class: "<TBD: choose low, medium, or high before saving>"
style: "<TBD: choose reference-first, snapshot-first, or hermetic before saving>"
verification_posture: "<TBD: choose test-first, observation-first, or none before saving>"
iteration: "<TBD: positive integer>"
created_at: <UTC timestamp>
updated_at: <UTC timestamp>
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
    - ticket:<token>
  paths:
    - "<TBD: paths the parent must reconcile, or None - rationale>"
source_fingerprint:
  git_commit: <sha or unknown>
  integration_remote: <remote name|none|unknown>
  integration_ref: <ref, tag, commit, or unknown>
  integration_commit: <sha or unknown>
  git_status_summary: <clean|dirty|unknown>
  git_status_detail: <short status detail or unknown - rationale>
  # Provenance: owner records or artifacts used to compile this packet baseline.
  compiled_from:
    - ticket:<token>
execution_context:
  branch: <name|unknown>
  push_remote: <remote name|same_as_integration|none|unknown>
  worktree: <path|none|unknown>
  isolation: none
  git_shared_metadata_mutations: forbidden
  destructive_commands: forbidden
  network: "<TBD: choose allowed, forbidden, or unknown - rationale before saving>"
context_budget:
  posture: normal
  max_source_files: 8
  max_excerpt_lines_per_file: 80
  avoid_full_file_reads: true
# Context: source set the Ralph child should read or trust for this bounded iteration.
sources:
  constitution:
    - constitution:main
  initiative: []
  research: []
  spec: []
  plan: []
  ticket:
    - ticket:<token>
links: {}
---

# Mission

What this iteration is meant to achieve.

# Bound Context

What larger chain constrains the work.

Frontmatter follows `skills/loom-records/references/packet-frontmatter.md`;
Ralph-specific body obligations follow `skills/loom-ralph/references/packet-contract.md`.
For Ralph, `source_fingerprint`, `execution_context`, `child_write_scope`,
`parent_merge_scope`, and `verification_posture` are strict launch-safety fields,
not optional packet decoration.

Use `source_fingerprint.compiled_from` for packet compilation provenance and
`sources` for the context the Ralph child should read or trust. The two lists may
overlap, but they do not need to duplicate each other.

Name packets using `packet:ralph-ticket-<token>-<UTC compact timestamp>` and save
them as `.loom/packets/ralph/<UTC compact timestamp>-ticket-<token>-iter-<NN>.md`.
The filename `iter-<NN>` suffix must match frontmatter `iteration`.

Name intended behavior separately from current implementation reality when this
packet touches code.

For Git-backed work, name the branch/worktree/integration-baseline posture here
when the frontmatter is not enough, especially for multi-repo packets.

For fork/upstream or review-system workflows, distinguish integration remote,
push remote, and review target instead of collapsing them into one remote name.

# Parent Launch Checklist

Before launch, the parent verifies:

- source freshness: `source_fingerprint` still matches governing records,
  resolved integration ref, git status expectations, and child-write-scope files;
  supersede this packet instead of launching if the contract is materially stale
- non-overlapping child write scope: `child_write_scope` records and paths are
  exact, narrow, and do not conflict with any parallel packet; canonical-record
  writes fail closed unless exact record refs are granted; empty
  `child_write_scope.records` or `child_write_scope.paths` is ambiguous and
  launch-blocking until replaced with exact entries or explicit
  `None - <rationale>` entries
- parent merge scope: `parent_merge_scope` names the ticket and any evidence,
  critique, packet-status, or other paths the parent must reconcile after return
- Git/execution context: branch, worktree, isolation, network posture, destructive
  command policy, and shared Git metadata policy match the intended run
- verification posture: `verification_posture` fits the change class and names
  the red/green, before/after, or verification-neutral evidence expected
- stop conditions: freshness, scope boundary, execution-context, and
  posture-specific stops are explicit enough for the child to fail closed
- output contract: required return fields are complete enough for parent-side
  ticket truth, evidence, critique, and packet lifecycle reconciliation

# Source Snapshot

Curated excerpts, summaries, or directions to the important source records.

# Change Class

Declared above as `change_class`. Explain how this class affects evidence,
critique, and verification posture for this iteration. If optional `risk_class`
is present, explain whether it repeats or narrows the ticket risk; the ticket
still owns critique disposition and acceptance gates.

# Verification Targets

Stable claim or acceptance IDs this iteration should satisfy or exercise.

List real qualified IDs, or write `None - reason`.

# Task For This Iteration

The exact bounded task for the child.

# Verification Posture

Declared above as `verification_posture`. Valid values: `test-first`, `observation-first`, `none`.

Expand here with specifics the child needs:

- for `test-first`: what failing check must exist before implementation, what counts as green, and where the check lives
- for `observation-first`: what must be observed before and after, and how the before/after evidence is captured
- for `none`: a one-line justification of why this iteration is verification-neutral

For `test-first`, include the expected failure reason, red command or procedure,
green command or procedure, and whether any broader regression command is
expected after the targeted check passes.

Use `none` only for verification-neutral work such as non-semantic record
hygiene, reference reconciliation, packet compilation, or a pure refactor riding
on an already-green suite. Do not use `none` for protocol authority, routing,
acceptance, behavior-contract, or operator-guidance changes merely because they
are written in Markdown.

# Stop Conditions

When the child should stop, block, or escalate instead of widening scope.

Stop if governing records or child-write-scope files appear materially newer or
otherwise materially different from the source fingerprint.

For Git-backed work, stop if the resolved integration ref or worktree state no
longer matches the declared execution context closely enough to trust the packet.

Do not run `git fetch`, `git fetch --prune`, remote edits, Git config edits, or
other shared Git metadata mutations unless this packet explicitly allows them.

For `test-first`, stop conditions must include: a failing check exists before implementation, fails for the expected reason, and is driven to green inside this iteration.

For `observation-first`, stop conditions must include: before-state evidence is captured, and after-state evidence confirms the intended change.

# Output Contract

The child must return:
- outcome (`continue|stop|blocked|escalate`)
- files changed
- records changed
- evidence gathered (including red-to-green transition for `test-first`, or before/after observations for `observation-first`)
- self-review findings or concerns, including any suspected scope, quality,
  verification, or maintainability issues
- blockers or risks
- ticket recommendation
  - The child recommends ticket changes; the parent commits ticket truth.

# Working Notes

Optional parent notes before launch.

# Child Output

To be filled by the child or copied back by the parent.

# Parent Merge Notes

What the parent concluded after reconciliation.
