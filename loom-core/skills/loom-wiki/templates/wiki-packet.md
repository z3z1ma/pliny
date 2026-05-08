---
id: "packet:wiki-<TBD: encoded target>-<TBD: UTC compact timestamp>"
kind: packet
packet_kind: wiki
status: compiled
target: "<TBD: wiki ref, source record ref, ticket ref, or synthesis target slug>"
mode: synthesis
style: reference-first
created_at: "<TBD: UTC timestamp>"
updated_at: "<TBD: UTC timestamp>"
scope:
  kind: repository
  repositories:
    - repo:root
child_write_scope:
  records:
    - "wiki:<TBD: slug>"
  paths:
    - "<TBD: wiki page paths the child may modify, or None - rationale>"
parent_merge_scope:
  records:
    - "wiki:<TBD: slug>"
    - "<TBD: ticket ref when a ticket owns follow-through, originating owner ref, or None - rationale>"
  paths:
    - "<TBD: wiki page path, other owner path, or None - rationale>"
source_fingerprint:
  git_commit: "<TBD: sha or unknown with rationale>"
  integration_remote: "<TBD: remote name, none, or unknown with rationale>"
  integration_ref: "<TBD: ref, tag, commit, or unknown with rationale>"
  integration_commit: "<TBD: sha or unknown with rationale>"
  git_status_summary: "<TBD: clean, dirty_tracked, dirty_untracked, dirty_mixed, or unknown>"
  git_status_detail: "<TBD: short status detail or unknown - rationale>"
  compiled_from:
    - "<TBD: record ref>"
execution_context:
  branch: "<TBD: branch name or unknown with rationale>"
  push_remote: "<TBD: remote name, same_as_integration, none, or unknown with rationale>"
  worktree: "<TBD: path, none, or unknown with rationale>"
  isolation: "<TBD: none, branch, worktree, sandbox, or unknown with rationale>"
  git_shared_metadata_mutations: "<TBD: forbidden, allowed, or unknown with rationale>"
  destructive_commands: "<TBD: forbidden, allowed, or unknown with rationale>"
  network: "<TBD: choose allowed, forbidden, or unknown - rationale that makes launch safe before saving>"
context_budget:
  posture: normal
  max_source_files: 8
  max_excerpt_lines_per_file: 80
  avoid_full_file_reads: true
sources:
  owner_records:
    - "<TBD: owner record ref to trust, or None - rationale>"
  evidence:
    - "<TBD: evidence ref to trust, or None - rationale>"
  critique:
    - "<TBD: critique ref to trust, or None - rationale>"
  research:
    - "<TBD: research ref to trust, or None - rationale>"
links: {}
---

# Mission

What accepted understanding should be promoted or updated in the wiki.

# Accepted Truth Sources

Which canonical records and evidence this packet should trust.

- Source: <TBD>
  - Owner status: <kind-valid lifecycle status such as active, accepted, completed, concluded, recorded, final, or closed>
  - Acceptance/evidence basis: <evidence or acceptance basis>
  - Freshness check: <timestamp/commit/check>
  - Limits: <limit>

Do not promote unsettled research, unresolved critique, stale evidence, or draft
specs into accepted explanation unless the packet names the gap and stops or routes repair.

# Target Pages

Which wiki pages should be created or updated.

# Gaps To Fill

What the current wiki does not yet explain well.

# Stop Conditions

Stop or return `blocked` if source truth is unsettled, contradicted, stale,
outside scope, or if the requested page would own policy, intended behavior, live
execution state, observed artifacts, or critique verdicts.

# Output Contract

Return:

- pages created or updated;
- key claims promoted;
- sources used;
- remaining gaps or uncertainty.

# Working Notes

Optional parent notes.

# Child Output

To be filled after the synthesis pass.

# Parent Merge Notes

How the parent accepted or revised the resulting pages and moved packet status to
`consumed`, `superseded`, or `abandoned`.
