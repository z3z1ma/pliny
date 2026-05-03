---
id: "packet:critique-<TBD: encoded-target-or-change-slug>-<TBD: UTC compact timestamp>"
kind: packet
packet_kind: critique
status: compiled
target: "<TBD: ticket:<token>, record ref, review target slug, diff handle, or external summary ID>"
review_target:
  kind: "<TBD: choose record, code_change, pull_request, branch, commit, diff, external_summary, release_package, or handoff_package>"
  summary: "<TBD: one-line human-readable review target>"
  ref: "<TBD: record ref, path, branch, commit, PR, package ID, or none>"
  diff: "<TBD: branch, commit range, PR, diff target, or none>"
  paths:
    - "<TBD: changed paths under review, or None - no path-specific target>"
mode: review
change_class: "<TBD: choose one change class before saving>"
# Optional when the parent wants packet-local risk carried explicitly:
# risk_class: "<TBD: choose low, medium, or high before saving>"
style: reference-first
created_at: "<TBD: UTC timestamp>"
updated_at: "<TBD: UTC timestamp>"
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
    - "<TBD: critique:<slug> for the critique record the parent will create or update>"
    - "<TBD: ticket:<token> when a ticket owns execution, owner record ref, or None - no parent record reconciliation needed>"
    # or: None - <rationale for no additional parent record reconciliation>
  paths:
    - "<TBD: .loom/critique/<slug>.md, other owner path, or None - no parent path reconciliation needed>"
    # or: None - <rationale for no parent path reconciliation>
source_fingerprint:
  git_commit: "<TBD: sha or unknown>"
  integration_remote: "<TBD: remote name, none, or unknown>"
  integration_ref: "<TBD: ref, tag, commit, or unknown>"
  integration_commit: "<TBD: sha or unknown>"
  git_status_summary: "<TBD: clean, dirty_tracked, dirty_untracked, dirty_mixed, or unknown>"
  git_status_detail: "<TBD: short status detail, or unknown - rationale>"
  # Provenance: owner records or artifacts used to compile this review baseline.
  compiled_from:
    - "<TBD: record ref or artifact used to compile this review baseline>"
execution_context:
  branch: "<TBD: branch name or unknown>"
  push_remote: "<TBD: remote name, same_as_integration, none, or unknown>"
  worktree: "<TBD: path, none, or unknown>"
  isolation: "<TBD: none, branch, worktree, sandbox, or unknown>"
  git_shared_metadata_mutations: "<TBD: forbidden, allowed, or unknown>"
  destructive_commands: "<TBD: forbidden, allowed, or unknown>"
  network: "<TBD: choose allowed, forbidden, or unknown - rationale that makes launch safe before saving>"
context_budget:
  posture: normal
  max_source_files: 8
  max_excerpt_lines_per_file: 80
  avoid_full_file_reads: true
# Context: source set the critique reviewer should read or trust for this bounded review.
sources: {}
links: {}
---

# Mission

What code or behavior change should be reviewed and why.

# Governing Context

The ticket when one owns execution, parent plan or initiative, relevant
spec/research/evidence, prior packet output, and acceptance or claim coverage
targets that constrain the review.

Frontmatter follows `skills/loom-records/references/packet-frontmatter.md`.
This template describes new critique packet authoring; older consumed critique
packets may retain the legacy-compatible `review_target` mapping documented in
that reference.
Critique owns this review packet's workflow; using packet grammar does not make
the review Ralph-governed.

Keep enough packet metadata for the reviewer and parent to identify the target,
source baseline, child/reviewer write boundary, and parent reconciliation targets.
Use `unknown`, `none`, or an explicit rationale when exact Git or execution
details are unavailable or not material to the review; do not invent branch,
remote, worktree, or command-policy precision. For `execution_context.network`,
bare `unknown` is launch-blocking unless the packet records why that uncertainty
is safe for the bounded review. Omit or mark common support blocks inapplicable
only when `loom-critique` explicitly allows that for the review shape.

Use `source_fingerprint.compiled_from` for packet compilation provenance and
`sources` for review context such as governing records, evidence, diffs, prior
packet output, or changed files. The lists may overlap, but critique packets do
not need duplicate source inventories to satisfy shared packet grammar.

`target` may name `ticket:<token>` when the ticket itself is the review target,
but critique packets may also target a record, diff, path set, external summary,
or handoff package without a ticket anchor. Encode path-set reviews with existing
`review_target` fields: choose the closest existing `kind`, such as `record`,
`code_change`, or `diff`; set unavailable scalar fields such as `ref` or `diff`
to `none`; and list the reviewed paths under `review_target.paths`.
`parent_merge_scope` must name the ticket when a ticket owns execution, the
critique record, evidence record, or other owner-layer targets the parent expects
to reconcile, or explicitly say `None - <rationale>` when no parent merge target
exists. Do not leave it empty or as placeholder-only `records: []` / `paths: []`.

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
