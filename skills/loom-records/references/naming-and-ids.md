# Naming And IDs

Loom uses canonical IDs for reference integrity and filenames for discovery.

Use both.

## Canonical ID Families

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
- `packet:ralph-<target>-<UTC compact timestamp>`
- `packet:critique-<ticket-or-change>-<UTC compact timestamp>`
- `packet:wiki-<target>-<UTC compact timestamp>`
- `workspace:main`

## Current Supported Kinds, IDs, And Paths

This table describes the record kinds currently supported by this corpus. It is
not a closed global vocabulary: project-local skills may add kinds when their
owner layer and path conventions are explicit.

| `kind:` | Canonical ID shape | Typical path |
| --- | --- | --- |
| `constitution` | `constitution:main` | `.loom/constitution/constitution.md` |
| `decision` | `decision:0001` | `.loom/constitution/decisions/decision-0001-<slug>.md` |
| `roadmap` | `roadmap:<slug>` | `.loom/constitution/roadmap/<slug>.md` |
| `initiative` | `initiative:<slug>` | `.loom/initiatives/<slug>.md` |
| `research` | `research:<slug>` | `.loom/research/<slug>.md` |
| `spec` | `spec:<slug>` | `.loom/specs/<slug>.md` |
| `plan` | `plan:<slug>` | `.loom/plans/<slug>.md` |
| `ticket` | `ticket:<token>` | `.loom/tickets/<YYYYMMDD>-<token>-<short-slug>.md` |
| `packet` with `packet_kind: ralph` | `packet:ralph-<target>-<UTC compact timestamp>` | `.loom/packets/ralph/<UTC compact timestamp>-ticket-<token>-iter-01.md` |
| `packet` with `packet_kind: critique` | `packet:critique-<ticket-or-change>-<UTC compact timestamp>` | `.loom/packets/critique/<UTC compact timestamp>-<target>.md` |
| `packet` with `packet_kind: wiki` | `packet:wiki-<target>-<UTC compact timestamp>` | `.loom/packets/wiki/<UTC compact timestamp>-<target>.md` |
| `critique` | `critique:<slug>` | `.loom/critique/<slug>.md` |
| `wiki` | `wiki:<slug>` | `.loom/wiki/<category>/<slug>.md` |
| `evidence` | `evidence:<slug>` | `.loom/evidence/<slug>.md` |
| `workspace` | `workspace:main` | `.loom/workspace.md` or project-local workspace support path |
| optional `memory` support metadata | usually no canonical ID | `.loom/memory/<domain>/<memory-file>.md` |

Memory support files are intentionally listed as support files rather than
canonical records. They usually have no YAML frontmatter. When optional memory
frontmatter exists, validators may see `kind: memory`, but that remains
support-layer metadata rather than a canonical truth owner. See `frontmatter.md`
for the memory frontmatter exception.

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

- `.loom/packets/ralph/<UTC compact timestamp>-ticket-<token>-iter-01.md`
- `.loom/packets/critique/<UTC compact timestamp>-<target>.md`
- `.loom/packets/wiki/<UTC compact timestamp>-<target>.md`

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
