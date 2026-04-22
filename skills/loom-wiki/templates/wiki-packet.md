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
write_scope:
  records:
    - wiki:<slug>
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

What understanding should be promoted or updated in the wiki.

# Accepted Truth Sources

Which canonical records and evidence this packet should trust.

# Target Pages

Which wiki pages should be created or updated.

# Gaps To Fill

What the current wiki does not yet explain well.

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
