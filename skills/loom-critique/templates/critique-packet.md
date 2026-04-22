---
id: packet:critique-<target>-<UTC compact timestamp>
kind: packet
packet_kind: critique
status: compiled
target: <record ref>
mode: review
style: reference-first
created_at: <UTC timestamp>
updated_at: <UTC timestamp>
scope:
  kind: repository
  repositories:
    - repo:root
write_scope:
  records: []
  paths: []
source_fingerprint:
  git_commit: <sha or unknown>
  git_status_summary: <clean|dirty|unknown>
  compiled_from:
    - <record ref>
context_budget:
  posture: normal
  max_source_files: 8
  max_excerpt_lines_per_file: 80
  avoid_full_file_reads: true
sources: {}
links: {}
---

# Mission

What should be reviewed and why.

# Review Lens

What kinds of weakness or risk the reviewer should focus on.

Named critique profiles to apply:
- operator-clarity

# Source Snapshot

Curated records, evidence, or changed files that matter most.

# Required Questions

The questions the reviewer must answer.

# Stop Conditions

When the reviewer should escalate rather than keep guessing.

# Output Contract

Return:
- verdict
- findings with severity/confidence
- evidence reviewed
- residual risks
- follow-up recommendation

# Working Notes

Optional parent notes.

# Reviewer Output

To be filled after the review.

# Parent Merge Notes

How the parent reconciled the critique into the graph.
