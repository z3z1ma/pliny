---
id: packet:critique-<ticket-or-change>-<UTC compact timestamp>
kind: packet
packet_kind: critique
status: compiled
target: ticket:<token>
review_target:
  kind: code_change
  diff: <branch | commit | PR | diff target>
mode: review
change_class: <record-hygiene|documentation-explanation|behavior-contract|code-behavior|protocol-authority|data-migration|security-sensitive|release-packaging>
style: reference-first
created_at: <UTC timestamp>
updated_at: <UTC timestamp>
scope:
  kind: repository
  repositories:
    - repo:root
child_write_scope:
  records: []
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

What code or behavior change should be reviewed and why.

# Governing Context

The ticket, parent plan or initiative, relevant spec/research/evidence, prior
Ralph packet output, and acceptance or claim coverage targets that constrain
the review.

# Review Lens

What kinds of weakness or risk the reviewer should focus on.

Named critique profiles to apply:
- operator-clarity

# Change Class

Declared above as `change_class`. Use it to choose the evidence and critique
profiles most relevant to this review.

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

# Working Notes

Optional parent notes.

# Reviewer Output

To be filled after the review.

# Parent Merge Notes

How the parent reconciled the critique into the graph.
