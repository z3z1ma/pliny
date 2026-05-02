---
id: packet:wiki-<encoded-target>-<UTC compact timestamp>
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
  paths:
    - "<TBD: wiki page paths the child may modify, or None - rationale>"
parent_merge_scope:
  records:
    - wiki:<slug>
    - ticket:<token>
    # or: None - <rationale for no parent record reconciliation>
  paths:
    - .loom/wiki/<slug>.md
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

What understanding should be promoted or updated in the wiki.

Name the originating ticket, critique, research, initiative, or other owner ref
in `parent_merge_scope.records` when parent reconciliation is expected.
`parent_merge_scope` must name parent reconciliation targets or explicitly say
`None - <rationale>` when no parent merge target exists. Do not leave it empty or
as placeholder-only `records: []` / `paths: []`.

# Accepted Truth Sources

Which canonical records and evidence this packet should trust.

Frontmatter follows `skills/loom-records/references/packet-frontmatter.md`.
Wiki owns this synthesis packet's workflow; using packet grammar does not make
the synthesis Ralph-governed.

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
