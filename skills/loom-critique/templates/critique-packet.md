---
id: packet:critique-<encoded-target-or-change-slug>-<UTC compact timestamp>
kind: packet
packet_kind: critique
status: compiled
target: ticket:<token>
review_target:
  kind: "<TBD: choose record, code_change, pull_request, branch, commit, diff, external_summary, release_package, or handoff_package>"
  summary: <one-line human-readable review target>
  ref: "<TBD: record ref, path, branch, commit, PR, package ID, or none>"
  diff: "<TBD: branch, commit range, PR, diff target, or none>"
  paths:
    - "<TBD: changed paths under review, or None - no path-specific target>"
mode: review
change_class: "<TBD: choose one change class before saving>"
# Optional when the parent wants packet-local risk carried explicitly:
# risk_class: "<TBD: choose low, medium, or high before saving>"
style: reference-first
created_at: <UTC timestamp>
updated_at: <UTC timestamp>
scope:
  kind: repository
  repositories:
    - repo:root
child_write_scope:
  records:
    - "<TBD: critique child write refs, or None - reviewer returns output only>"
  paths:
    - "<TBD: critique child write paths, or None - reviewer returns output only>"
parent_merge_scope:
  records:
    - ticket:<token>
    - critique:<slug>
    # or: None - <rationale for no parent record reconciliation>
  paths:
    - .loom/critique/<slug>.md
    # or: None - <rationale for no parent path reconciliation>
source_fingerprint:
  git_commit: <sha or unknown>
  integration_remote: <remote name|none|unknown>
  integration_ref: <ref, tag, commit, or unknown>
  integration_commit: <sha or unknown>
  git_status_summary: <clean|dirty|unknown>
  compiled_from:
    - <record ref>
execution_context:
  branch: <name|unknown>
  push_remote: <remote name|same_as_integration|none|unknown>
  worktree: <path|none|unknown>
  isolation: none
  git_shared_metadata_mutations: forbidden
  destructive_commands: forbidden
  network: unknown
context_budget:
  posture: normal
  max_source_files: 8
  max_excerpt_lines_per_file: 80
  avoid_full_file_reads: true
sources: {}
links: {}
---

# Mission

What code or behavior change should be reviewed and why.

# Governing Context

The ticket, parent plan or initiative, relevant spec/research/evidence, prior
Ralph packet output, and acceptance or claim coverage targets that constrain
the review.

Frontmatter follows `skills/loom-records/references/packet-frontmatter.md`.
This template describes new critique packet authoring; older consumed critique
packets may retain the legacy-compatible `review_target` mapping documented in
that reference.
Critique owns this review packet's workflow; using packet grammar does not make
the review Ralph-governed.

`parent_merge_scope` must name the ticket, critique record, evidence record, or
other owner-layer targets the parent expects to reconcile, or explicitly say
`None - <rationale>` when no parent merge target exists. Do not leave it empty or
as placeholder-only `records: []` / `paths: []`.

Encode the packet `target` in packet IDs and filenames using
`skills/loom-records/references/naming-and-ids.md`; for example,
`ticket:abc123xy` becomes `ticket-abc123xy` in
`.loom/packets/critique/<UTC compact timestamp>-ticket-abc123xy.md`. When a
specific reviewed change needs a clearer discovery handle than the record target,
choose an explicit lowercase change slug and use it consistently in the packet ID
and filename.

Do not conflate this encoded packet name with the structured `review_target`
frontmatter field. Critique packet `review_target` is a mapping so fresh-context
reviewers can inspect the target type, stable reference, diff handle, and changed
paths without parsing prose. Keep `summary` as a one-line human-readable search
handle, set unavailable fields to `none` rather than omitting the target, and use
the packet body for longer rationale. The packet ID and filename name the support
packet for routing and discovery.

# Review Lens

What kinds of weakness or risk the reviewer should focus on.

Named critique profiles to apply:
- operator-clarity

# Change Class

Declared above as `change_class`. Use it to choose the evidence and critique
profiles most relevant to this review. If optional `risk_class` is present, use
it as review context only; the ticket still owns critique disposition.

# Evidence Expectations

Critique packets do not use Ralph `verification_posture`. Review quality comes
from the critique lens, named profiles, actual diff/artifact inspection, evidence
sufficiency checks, and explicit findings. Add no posture field unless
`loom-critique` later defines one for critique-owned packets.

# Source Snapshot

Curated records, evidence, diffs, tests, or changed files that matter most.

# Diff Under Review

Where the reviewer should find the git diff, changed-file list, branch, commit,
or pull request.

# Required Questions

The questions the reviewer must answer.

- Did the actual diff or artifact satisfy the ticket, spec, acceptance coverage,
  and declared write boundary?
- Did the change add unrequested behavior, scope creep, or a new owner-layer
  claim in the wrong place?
- Does the evidence support the implementation and completion claims, or is it
  stale, partial, missing, or overclaimed?
- Did the reviewer inspect the actual files, records, tests, and diff rather than
  trusting the child or implementer report?
- Are tests or observations checking real behavior rather than only mock behavior
  or implementation trivia?
- Are there unresolved risks that should block acceptance, become accepted risk,
  or turn into linked follow-up work?

# Stop Conditions

When the reviewer should escalate rather than keep guessing.

Stop or return `blocked` if the declared `review_target`, source fingerprint,
governing records, diff under review, or child/reviewer write boundary appears
materially stale or inconsistent with the packet. Ask the parent for a fresh
critique packet instead of silently reviewing a different change.

# Output Contract

Return:
- verdict
- findings with severity/confidence
- evidence reviewed
- file and line references for code findings when practical
- residual risks
- follow-up recommendation

The parent creates or updates real critique and ticket records during
reconciliation; do not leave placeholder IDs in `parent_merge_scope`.

After parent reconciliation, the parent records `# Parent Merge Notes` and moves
this packet's `status` away from non-terminal `compiled` to the truthful terminal
packet status: `consumed`, `superseded`, or `abandoned`. That lifecycle discipline
does not make this critique packet a Ralph implementation packet.

# Working Notes

Optional parent notes.

# Reviewer Output

To be filled after the review.

# Parent Merge Notes

How the parent reconciled the critique into the graph.
