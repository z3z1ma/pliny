# Naming And IDs

Loom uses canonical IDs for reference integrity and filenames for discovery.

Use both.

## Canonical Owner-Record ID Families

These ID families belong to canonical owner records: records in owner layers that
can own the kind of truth named by Loom's layer model. Packet IDs and
support-local IDs may be stable enough to cite for routing, transport, recall, or
workspace metadata, but they are not canonical truth-owner IDs.

- `constitution:main`
- `decision:0001`
- `roadmap:<slug>`
- `initiative:<slug>`
- `research:<slug>`
- `spec:<slug>`
- `plan:<slug>`
- `ticket:<token>`
- `critique:<slug>`
- `wiki:<slug>`
- `evidence:<slug>`

## Stable Support And Packet ID Families

These ID families may be durable and citeable, but they remain non-owner support
grammar. They do not own objective state, live ticket state, acceptance, evidence
sufficiency, critique verdicts, wiki truth, canonical truth, or packet lifecycle.

- `packet:ralph-<encoded-target>-<UTC compact timestamp>`
- `packet:critique-<encoded-target-or-change-slug>-<UTC compact timestamp>`
- `packet:wiki-<encoded-target>-<UTC compact timestamp>`
- `workspace:main`
- support-local `workspace:<slug>` such as `workspace:harness`
- support-local `support:<domain>-<slug>`

## Current Supported Kinds, IDs, And Paths

This table describes the record and support kinds currently supported by this
corpus. It is not a closed global vocabulary: project-local skills may add kinds
when their owner boundary and path conventions are explicit.

| `kind:` | ID shape | Authority boundary | Typical path |
| --- | --- | --- | --- |
| `constitution` | `constitution:main` | canonical owner record | `.loom/constitution/constitution.md` |
| `decision` | `decision:0001` | canonical owner record | `.loom/constitution/decisions/decision-0001-<slug>.md` |
| `roadmap` | `roadmap:<slug>` | canonical owner record | `.loom/constitution/roadmap/<slug>.md` |
| `initiative` | `initiative:<slug>` | canonical owner record | `.loom/initiatives/<slug>.md` |
| `research` | `research:<slug>` | canonical owner record | `.loom/research/<slug>.md` |
| `spec` | `spec:<slug>` | canonical owner record | `.loom/specs/<slug>.md` |
| `plan` | `plan:<slug>` | canonical owner record | `.loom/plans/<slug>.md` |
| `ticket` | `ticket:<token>` | canonical live execution ledger | `.loom/tickets/<YYYYMMDD>-<token>-<short-slug>.md` |
| `packet` with `packet_kind: ralph` | `packet:ralph-<encoded-target>-<UTC compact timestamp>` | non-canonical bounded contract | `.loom/packets/ralph/<UTC compact timestamp>-ticket-<token>-iter-<NN>.md` |
| `packet` with `packet_kind: critique` | `packet:critique-<encoded-target-or-change-slug>-<UTC compact timestamp>` | non-canonical bounded contract | `.loom/packets/critique/<UTC compact timestamp>-<encoded-target-or-change-slug>.md` |
| `packet` with `packet_kind: wiki` | `packet:wiki-<encoded-target>-<UTC compact timestamp>` | non-canonical bounded contract | `.loom/packets/wiki/<UTC compact timestamp>-<encoded-target>.md` |
| `critique` | `critique:<slug>` | canonical owner record | `.loom/critique/<slug>.md` |
| `wiki` | `wiki:<slug>` | canonical owner record | `.loom/wiki/<category>/<slug>.md` |
| `evidence` | `evidence:<slug>` | canonical owner record | `.loom/evidence/<slug>.md` |
| `workspace` | `workspace:main` | stable workspace metadata, not canonical project truth | `.loom/workspace.md` |
| `workspace-support` | support-local `workspace:<slug>` such as `workspace:harness` | support-local transport metadata | project-local workspace support path such as `.loom/harness.md` |
| `support-artifact` | optional support-local `support:<domain>-<slug>` | support-local workflow metadata | `.loom/support/<domain>/<slug>.md` |
| optional `memory` support metadata | usually no canonical ID | support-only recall metadata | `.loom/memory/<domain>/<memory-file>.md` |

Memory support files are intentionally listed as support files rather than
canonical records. They usually have no YAML frontmatter. When optional memory
frontmatter exists, validators may see `kind: memory`, but that remains
support-layer metadata rather than a canonical truth owner. See `frontmatter.md`
for the memory frontmatter exception.

## Support Artifact IDs And Paths

Support artifacts may carry frontmatter so agents can route and reconcile them,
but their IDs are support-local handles, not canonical owner-record IDs. A
support artifact must not own objective state, live ticket state, acceptance,
evidence sufficiency, critique verdicts, wiki truth, canonical truth, or packet
lifecycle.

`.loom/support/` is optional and lazy-materialized. Use it only for intentionally
saved support artifacts, and do not treat the directory or its support-local IDs
as a new canonical owner layer.

Use the smallest explicit shape needed by the owning skill:

- workspace harness profiles use `id: workspace:harness` and
  `kind: workspace-support` in a project-local support path such as
  `.loom/harness.md`; this documents transport mechanics only.
- saved drive outer-loop handoffs use
  `id: support:drive-handoff-<UTC compact timestamp>-<slug>`,
  `kind: support-artifact`, `support_kind: drive-outer-loop-handoff`, and
  `handoff_kind: outer-loop-synthesis` under
  `.loom/support/drive-handoffs/<UTC compact timestamp>-<slug>.md`.

Drive outer-loop handoffs are prompt-only by default. Save one only when the
parent wants a durable support artifact for reviewability, context recovery, or
handoff audit. Saving a handoff does not make it a packet family and does not
give it canonical truth ownership.

## Packet Families And Route Ownership

Packet records share `kind: packet` and are separated by `packet_kind` plus path:

- `packet_kind: ralph` under `.loom/packets/ralph/` is the Ralph implementation
  handoff family owned by `loom-ralph`.
- `packet_kind: critique` under `.loom/packets/critique/` is the critique review
  handoff family owned by `loom-critique`.
- `packet_kind: wiki` under `.loom/packets/wiki/` is the wiki synthesis handoff
  family owned by `loom-wiki`.

This naming grammar does not make critique or wiki work Ralph-governed. Choose
the route by the truth being changed: implementation goes through Ralph, review
through critique, and accepted explanation through wiki. Packets remain bounded
contracts for child work; they do not own project truth or live execution state.

Encode packet targets by turning a typed record reference into filename-safe text:
replace the colon with a hyphen and keep the slug or token lowercase. For
example, `ticket:abc123xy` becomes `ticket-abc123xy`, and
`wiki:operator-guide` becomes `wiki-operator-guide`. If the target is already a
page slug or change slug, use that slug directly.

Critique packet IDs and filenames should encode the packet `target` or an
explicitly chosen lowercase change slug for discovery. That encoded name is not
the same thing as the critique packet's structured `review_target` field:
`review_target` records the artifact, diff, PR, branch, commit, or record under
review, while the packet ID and filename provide a stable support-artifact
handle.

Use the same compact UTC timestamp in both packet ID and filename. Ralph packet
filenames also carry `iter-<NN>` for the bounded implementation sequence; that
number must match frontmatter `iteration`. Ralph packet IDs do not need an
iteration suffix because the timestamp and target identify the support artifact,
while `iteration` describes the child handoff sequence.

## Filename Guidance

### Stable semantic records

Use a semantic slug:

- `.loom/specs/<slug>.md`
- `.loom/plans/<slug>.md`
- `.loom/wiki/workflows/<slug>.md`

### Tickets

Use date + token + slug:

- `.loom/tickets/<YYYYMMDD>-<token>-<short-slug>.md`

The ticket's canonical ID should be only the token:

- `ticket:<token>`

### Packets

Use timestamp + subsystem + target:

- `.loom/packets/ralph/<UTC compact timestamp>-ticket-<token>-iter-<NN>.md`
- `.loom/packets/critique/<UTC compact timestamp>-<encoded-target-or-change-slug>.md`
- `.loom/packets/wiki/<UTC compact timestamp>-<encoded-target>.md`

The corresponding ID uses subsystem first and timestamp last, such as
`packet:ralph-ticket-<token>-<UTC compact timestamp>`.

### Decisions

Use an ordered prefix:

- `.loom/constitution/decisions/decision-0001-packet-discipline.md`

## Why Both Matter

Canonical IDs make references durable.

Filenames make discovery cheap.

One is for graph integrity.
One is for human and agent navigation.

## Slug Guidance

Prefer lowercase, words separated by hyphens, and filenames that say what the record is about.
