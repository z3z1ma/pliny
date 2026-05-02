---
id: packet:wiki-<target>-<UTC compact timestamp>
kind: packet
packet_kind: wiki
status: compiled
target: <record ref or page slug>
mode: synthesis
style: reference-first
created_at: <UTC timestamp>
updated_at: <UTC timestamp>
scope:
  kind: repository
  repositories:
    - repo:root
child_write_scope:
  records:
    - wiki:<slug>
  paths: []
parent_merge_scope:
  records: []
  paths: []
source_fingerprint:
  git_commit: <sha or unknown>
  git_status_summary: <clean|dirty|unknown>
  compiled_from:
    - <record ref>
execution_context:
  branch: <name|unknown>
  worktree: <path|none|unknown>
  isolation: none
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

What understanding should be promoted or updated in the wiki.

Name the originating ticket, critique, research, initiative, or other owner ref
in `parent_merge_scope.records` when parent reconciliation is expected.

# Accepted Truth Sources

Which canonical records and evidence this packet should trust.

Wiki packets do not use Ralph `verification_posture`. Synthesis quality comes
from accepted source records, cited evidence, clear gaps, and parent
reconciliation into wiki pages. Add no posture field unless `loom-wiki` later
defines one for wiki-owned packets.

# Target Pages

Which wiki pages should be created or updated.

# Gaps To Fill

What the current wiki does not yet explain well.

# Stop Conditions

Stop or return `blocked` if:

- the truth is unsettled or contradicted by owner records
- source records are stale, missing, or outside the declared scope
- the requested page would define policy, intended behavior, live execution state,
  observed artifacts, or critique verdicts instead of explaining accepted understanding
- a substantive rewrite needs critique, ticket disposition, or retrospective
  routing before promotion

# Output Contract

Return:
- pages created or updated
- key claims promoted
- sources used
- remaining gaps or uncertainty

# Working Notes

Optional parent notes.

# Child Output

To be filled after the synthesis pass.

# Parent Merge Notes

How the parent accepted or revised the resulting pages.
