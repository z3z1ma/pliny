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
    - "<TBD: ticket ref when a ticket owns follow-through, originating owner ref, or None - no additional parent record reconciliation needed>"
    # or: None - <rationale for no parent record reconciliation>
  paths:
    - "<TBD: wiki page path, other owner path, or None - no parent path reconciliation needed>"
    # or: None - <rationale for no parent path reconciliation>
source_fingerprint:
  git_commit: "<TBD: sha or unknown with rationale>"
  integration_remote: "<TBD: remote name, none, or unknown with rationale>"
  integration_ref: "<TBD: ref, tag, commit, or unknown with rationale>"
  integration_commit: "<TBD: sha or unknown with rationale>"
  git_status_summary: "<TBD: clean, dirty_tracked, dirty_untracked, dirty_mixed, or unknown with rationale>"
  git_status_detail: "<TBD: short status detail or unknown with rationale>"
  # Provenance: owner records or artifacts used to compile this synthesis baseline.
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
# Context: source set the wiki synthesizer should read or trust for this bounded synthesis.
sources: {}
links: {}
---

# Mission

What understanding should be promoted or updated in the wiki.

Name the originating ticket only when a ticket owns follow-through. Otherwise
name the critique, research, initiative, wiki page, source record, or other owner
ref in `target` and `parent_merge_scope.records` when parent reconciliation is
expected. `parent_merge_scope` must name parent reconciliation targets or
explicitly say `None - <rationale>` when no parent merge target exists. Do not
leave it empty or as placeholder-only `records: []` / `paths: []`.

# Accepted Truth Sources

Which canonical records and evidence this packet should trust.

Frontmatter follows `skills/loom-records/references/packet-frontmatter.md`.
Wiki owns this synthesis packet's workflow; using packet grammar does not make
the synthesis Ralph-governed.

Keep enough packet metadata for the synthesizer and parent to identify the target,
accepted sources, child write boundary, and parent reconciliation targets. Use
`unknown`, `none`, or an explicit rationale when exact Git or execution details
are unavailable or not material to the synthesis; do not invent branch, remote,
worktree, or command-policy precision. For `execution_context.network`, bare
`unknown` is launch-blocking unless the packet records why that uncertainty is
safe for the bounded synthesis. Omit or mark common support blocks inapplicable
only when `loom-wiki` explicitly allows that for the synthesis shape.

Use `source_fingerprint.compiled_from` for packet compilation provenance and
`sources` for accepted truth sources the wiki synthesizer should read or trust.
The lists may overlap, but wiki packets should not duplicate source inventories
unless the same source is both provenance and synthesis context.

Encode the target in packet IDs and filenames using
`skills/loom-records/references/naming-and-ids.md`; for example,
`wiki:operator-guide` becomes `wiki-operator-guide` in
`.loom/packets/wiki/<UTC compact timestamp>-wiki-operator-guide.md`.

Wiki packets do not use Ralph `verification_posture`. Synthesis quality comes
from accepted source records, cited evidence, clear gaps, and parent
reconciliation into wiki pages. Add no posture field unless `loom-wiki` later
defines one for wiki-owned packets.

Wiki packets also omit `change_class` by default. Add optional `change_class` or
`risk_class` only when the wiki workflow intentionally needs to carry source
change context; those fields do not make synthesis a Ralph implementation route.

# Target Pages

Which wiki pages should be created or updated.

# Gaps To Fill

What the current wiki does not yet explain well.

# Stop Conditions

Stop or return `blocked` if:

- the truth is unsettled or contradicted by owner records
- source records are stale, missing, or outside the declared scope
- the source fingerprint, accepted truth sources, target pages, or declared write
  boundary appear materially stale or inconsistent with the packet
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

After parent reconciliation, the parent records `# Parent Merge Notes` and moves
this packet's `status` away from non-terminal `compiled` to the truthful terminal
packet status: `consumed`, `superseded`, or `abandoned`. That lifecycle discipline
does not make this wiki packet a Ralph implementation packet.

# Working Notes

Optional parent notes.

# Child Output

To be filled after the synthesis pass.

# Parent Merge Notes

How the parent accepted or revised the resulting pages.
