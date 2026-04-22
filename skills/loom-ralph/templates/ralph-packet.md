---
id: packet:ralph-<target>-<UTC compact timestamp>
kind: packet
packet_kind: ralph
status: compiled
target: ticket:<token>
mode: execution
style: reference-first
verification_posture: test-first
iteration: 1
created_at: <UTC timestamp>
updated_at: <UTC timestamp>
scope:
  kind: repository
  repositories:
    - repo:root
write_scope:
  records:
    - ticket:<token>
  paths: []
source_fingerprint:
  git_commit: <sha or unknown>
  git_status_summary: <clean|dirty|unknown>
  compiled_from:
    - ticket:<token>
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
    - ticket:<token>
links: {}
---

# Mission

What this iteration is meant to achieve.

# Bound Context

What larger chain constrains the work.

# Source Snapshot

Curated excerpts, summaries, or directions to the important source records.

# Verification Targets

Stable claim or acceptance IDs this iteration should satisfy or exercise.

- ACC-000

# Task For This Iteration

The exact bounded task for the child.

# Verification Posture

Declared above as `verification_posture`. Valid values: `test-first`, `observation-first`, `none`.

Expand here with specifics the child needs:

- for `test-first`: what failing check must exist before implementation, what counts as green, and where the check lives
- for `observation-first`: what must be observed before and after, and how the before/after evidence is captured
- for `none`: a one-line justification of why this iteration is verification-neutral

# Stop Conditions

When the child should stop, block, or escalate instead of widening scope.

Stop if governing records or write-scope files appear materially newer than the
source fingerprint.

For `test-first`, stop conditions must include: a failing check exists before implementation, and the check is driven to green inside this iteration.

For `observation-first`, stop conditions must include: before-state evidence is captured, and after-state evidence confirms the intended change.

# Output Contract

The child must return:
- outcome (`continue|stop|blocked|escalate`)
- files changed
- records changed
- evidence gathered (including red-to-green transition for `test-first`, or before/after observations for `observation-first`)
- blockers or risks
- ticket recommendation

# Working Notes

Optional parent notes before launch.

# Child Output

To be filled by the child or copied back by the parent.

# Parent Merge Notes

What the parent concluded after reconciliation.
