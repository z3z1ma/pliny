# Packet Frontmatter

Packet frontmatter is shared record grammar for durable packet support artifacts.

This reference owns the common packet metadata shape used by Ralph, critique, and
wiki packet templates. Workflow skills still own their workflow-specific body
contracts, family-specific frontmatter additions, review lenses, synthesis rules,
and reconciliation procedure.

Packets remain support artifacts. They are bounded handoff contracts and working
pads; they do not become canonical truth owners for intended behavior, live
execution state, critique verdicts, accepted explanation, or evidence.

## Common Packet Shape

Core packet templates should use this shared frontmatter shape unless a workflow
skill records a narrower packet-family exception.

```yaml
---
id: packet:<packet-kind>-<encoded-target>-<UTC compact timestamp>
kind: packet
packet_kind: <ralph|critique|wiki>
status: compiled
target: <record ref or page slug>
mode: <execution|review|synthesis>
style: <reference-first|snapshot-first|hermetic>
# Optional or family-specific fields may appear here, such as:
# change_class, risk_class, iteration, verification_posture, review_target
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
  records:
    - <record ref | None - rationale>
  paths:
    - <path | None - rationale>
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
  isolation: <none|branch|worktree|sandbox|unknown>
  git_shared_metadata_mutations: <forbidden|allowed|unknown>
  destructive_commands: <forbidden|allowed|unknown>
  network: <allowed|forbidden|unknown>
context_budget:
  posture: <tight|normal|expansive>
  max_source_files: <integer or unknown>
  max_excerpt_lines_per_file: <integer or unknown>
  avoid_full_file_reads: <true|false>
sources: {}
links: {}
---
```

## Required Shared Fields

- `id`
- `kind: packet`
- `packet_kind`
- `status`
- `target`
- `mode`
- `style`
- `created_at`
- `updated_at`
- `scope`
- `child_write_scope`
- `parent_merge_scope`
- `source_fingerprint`
- `execution_context`
- `context_budget`
- `sources`
- `links`

These fields are required for every current packet family. They make the support
artifact routable, replayable enough for review, and explicit about child write
authority and parent reconciliation authority.

## Optional Shared And Family Fields

The common shape intentionally separates required shared fields from additions
that belong to particular packet families:

- `change_class` is required by current Ralph and critique templates because
  implementation and review packets use it to choose evidence, verification, and
  critique posture. Wiki packets omit it by default; add it only when the wiki
  workflow intentionally needs to carry the source change class for synthesis.
- `risk_class` is optional shared grammar. Add it when the parent wants a packet
  to repeat or narrow the ticket risk for the bounded handoff. It does not
  replace ticket-owned critique disposition or acceptance gates.
- `iteration` is required for Ralph packets. It is a positive integer naming the
  bounded implementation iteration, and Ralph filenames should mirror it as an
  `iter-<NN>` suffix. Critique and wiki packets omit it unless their owning skill
  later defines a family-local sequence field.
- `verification_posture` is required for Ralph packets and omitted by critique
  and wiki packets unless those owning workflows define their own equivalent.
- `review_target` is critique-family grammar. Critique templates include it so a
  reviewer can identify the code change, artifact, PR, branch, commit, or record
  under review.

Do not make a field required for all packet families merely because one workflow
needs it. Shared packet grammar coordinates handoff support; workflow ownership
still follows `packet_kind` and the route selected by the truth being changed.

## Packet Family Values

Use `packet_kind` to route the packet to its owning workflow:

- `ralph` — implementation packet owned by the Ralph inner loop.
- `critique` — review packet owned by the critique workflow.
- `wiki` — synthesis packet owned by the wiki workflow.

Critique and wiki packets may reuse packet discipline without becoming
Ralph-governed. Do not infer Ralph child obligations merely because a critique or
wiki packet has `kind: packet`.

Use `mode` to declare the packet's immediate work posture:

- `execution` for Ralph implementation packets.
- `review` for critique packets.
- `synthesis` for wiki packets.

Future packet families may define additional `packet_kind` or `mode` values in
their owning skills, but shared templates should not invent values casually.

## Packet IDs And Filenames

Packet IDs use this shape:

```text
packet:<packet-kind>-<encoded-target-or-change-slug>-<UTC compact timestamp>
```

Encode record references for IDs and filenames by replacing `:` with `-` and by
using lowercase slug/token text. For example, `ticket:abc123xy` becomes
`ticket-abc123xy`.

For critique packets, the encoded portion should name the packet `target` when
the review is anchored to a Loom record, or an explicitly chosen lowercase
change slug when the packet target is not the clearest discovery handle. Do not
derive packet IDs or filenames from the structured `review_target` field by
default; `review_target` describes the artifact, diff, PR, branch, commit, or
record under review inside the packet body contract.

Current family filename patterns are:

- Ralph: `.loom/packets/ralph/<UTC compact timestamp>-ticket-<token>-iter-<NN>.md`
- Critique: `.loom/packets/critique/<UTC compact timestamp>-<encoded-target-or-change-slug>.md`
- Wiki: `.loom/packets/wiki/<UTC compact timestamp>-<encoded-target>.md`

Use the same compact UTC timestamp in the packet ID and filename. Ralph packet
IDs do not need to repeat `iteration`; the frontmatter `iteration` field and the
filename `iter-<NN>` suffix carry that sequence for human and agent discovery.
See `skills/loom-records/references/naming-and-ids.md` for the wider naming
table.

## Packet Status Values

Packet status describes the lifecycle of the packet support artifact, not the
ticket or owner-record state.

Valid shared values are:

- `compiled` — ready for launch or pending parent action.
- `consumed` — child or reviewer output returned and parent reconciliation notes
  were recorded.
- `superseded` — governing records, source fingerprint, scope, or write boundary
  changed enough that a newer packet replaces this one.
- `abandoned` — packet will not be launched and no successor is intended.

Tickets still own live execution state and closure.

## Style Values

Use one of:

- `reference-first` — point mostly to canonical records and key source files.
- `snapshot-first` — include more curated excerpts and summaries in the packet.
- `hermetic` — carry nearly everything the worker should need and minimize
  outside reads.

Style controls context packaging only. It does not change owner-layer authority.

## Verification Posture

`verification_posture` is shared grammar for Ralph implementation packets:

```yaml
verification_posture: <test-first|observation-first|none>
```

Valid Ralph values are:

- `test-first`
- `observation-first`
- `none`

Ralph packets must include this field because Ralph uses it to set child evidence
obligations for an implementation iteration.

Critique and wiki packets should omit `verification_posture` unless their owning
workflow later defines a packet-local equivalent. Critique quality comes from the
review lens, evidence sufficiency checks, and findings. Wiki quality comes from
accepted sources, clear citations, and parent reconciliation into wiki pages.

## Change And Risk Fields

Use `change_class` when the packet executes or reviews a change whose evidence,
critique, or verification route depends on the mutation class. Current Ralph and
critique packet templates include it as required family grammar. Wiki packet
templates omit it by default because wiki packets synthesize accepted
understanding rather than execute or review the change itself.

Use values from `skills/loom-records/references/change-class.md`:

- `record-hygiene`
- `documentation-explanation`
- `behavior-contract`
- `code-behavior`
- `protocol-authority`
- `data-migration`
- `security-sensitive`
- `release-packaging`

`risk_class` may be added to any packet family when the parent wants the packet
to carry the ticket's risk posture explicitly. Risk does not replace the ticket's
critique disposition, and critique policy still gates ticket closure through the
ticket.

## Scope And Reconciliation Fields

`child_write_scope` names what the packet consumer may mutate:

```yaml
child_write_scope:
  records:
    - ticket:<token>
  paths:
    - path/or/glob
```

`parent_merge_scope` names what the parent expects to reconcile after the packet:

```yaml
parent_merge_scope:
  records:
    - ticket:<token>
    # or: None - <rationale for no parent record reconciliation>
  paths:
    - .loom/tickets/<ticket-file>.md
    # or: None - <rationale for no parent path reconciliation>
```

Do not leave `parent_merge_scope` empty. If a packet genuinely expects no parent
record or path reconciliation, make that explicit with `None - <rationale>` so a
future operator can tell the omission is intentional rather than forgotten.

The child scope is not blanket authority to change project truth. If the packet
allows a child to update canonical records, the child must still stay within the
owning layer's semantics and the ticket's acceptance boundary. The parent owns
final reconciliation unless the packet explicitly grants a narrower child update.

Legacy packets may contain `write_scope`. Treat that as `child_write_scope` only
for legacy compatibility when the packet does not say otherwise. New packet
templates should use `child_write_scope`.

## Source Fingerprint

`source_fingerprint` makes the compilation baseline inspectable:

```yaml
source_fingerprint:
  git_commit: <sha or unknown>
  integration_remote: <remote name|none|unknown>
  integration_ref: <ref, tag, commit, or unknown>
  integration_commit: <sha or unknown>
  git_status_summary: <clean|dirty|unknown>
  compiled_from:
    - ticket:<token>
```

Before launch, the parent should compare this baseline against governing records,
the resolved integration ref, and child-write-scope files. At execution time, the
packet consumer should stop and report `blocked` or `escalate` if those surfaces
appear materially changed in a way that makes the contract unsafe. If the packet
is materially stale, supersede it rather than asking the consumer to guess.

## Execution Context

`execution_context` describes where and under what tool constraints packet work
is expected to happen:

```yaml
execution_context:
  branch: <name|unknown>
  push_remote: <remote name|same_as_integration|none|unknown>
  worktree: <path|none|unknown>
  isolation: <none|branch|worktree|sandbox|unknown>
  git_shared_metadata_mutations: <forbidden|allowed|unknown>
  destructive_commands: <forbidden|allowed|unknown>
  network: <allowed|forbidden|unknown>
```

For non-Git or read-only packet work, use `none` or `unknown` honestly rather than
omitting the field.

## Context Budget

`context_budget` declares how much source reading the parent expects:

```yaml
context_budget:
  posture: <tight|normal|expansive>
  max_source_files: <integer or unknown>
  max_excerpt_lines_per_file: <integer or unknown>
  avoid_full_file_reads: <true|false>
```

Current templates default to `posture: normal`, `max_source_files: 8`,
`max_excerpt_lines_per_file: 80`, and `avoid_full_file_reads: true`. Use `tight`
for very narrow record or code slices and `expansive` only when the parent is
intentionally granting broader source reading.

The budget is guidance for bounded work, not a substitute for judgment. A packet
consumer may exceed it only when the packet or discovered evidence makes that
necessary and should report the reason.

## Sources And Links

Use `sources` for the source record set compiled into or referenced by the
packet. A typed mapping is preferred when the family has known source categories.

Use `links` for typed graph navigation that should be searchable from the packet
support artifact. Keep it lightweight; canonical owner records still own project
truth.
