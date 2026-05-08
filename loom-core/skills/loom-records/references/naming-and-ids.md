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
grammar. Packet IDs identify packet records whose `status` field owns only that
packet's lifecycle status: `compiled`, `consumed`, `superseded`, or `abandoned`.
Neither packet IDs nor support-local IDs own objective state, live ticket state,
acceptance, evidence sufficiency, critique verdicts, wiki truth, or canonical
truth. Support-local IDs also do not own packet lifecycle surfaces.

- `packet:ralph-<encoded-target>-<UTC compact timestamp>`
- `packet:critique-<encoded-target-or-change-slug>-<UTC compact timestamp>`
- `packet:wiki-<encoded-target>-<UTC compact timestamp>`
- `workspace:main`
- support-local `workspace:<slug>` such as `workspace:harness`
- support-local `support:<domain>-<slug>`

## Current Supported Kinds, IDs, And Paths

This catalog describes the record and support kinds currently supported by this
corpus. It is not a closed global vocabulary: project-local skills may add kinds
when their owner boundary and path conventions are explicit.

- `constitution`
  - ID shape: `constitution:main`
  - Authority boundary: canonical owner record
  - Typical path: `.loom/constitution/constitution.md`
- `decision`
  - ID shape: `decision:0001`
  - Authority boundary: canonical owner record
  - Typical path: `.loom/constitution/decisions/decision-0001-<slug>.md`
- `roadmap`
  - ID shape: `roadmap:<slug>`
  - Authority boundary: canonical owner record
  - Typical path: `.loom/constitution/roadmap/<slug>.md`
- `initiative`
  - ID shape: `initiative:<slug>`
  - Authority boundary: canonical owner record
  - Typical path: `.loom/initiatives/<YYYYMMDD>-<slug>.md`
- `research`
  - ID shape: `research:<slug>`
  - Authority boundary: canonical owner record
  - Typical path: `.loom/research/<slug>.md`
- `spec`
  - ID shape: `spec:<slug>`
  - Authority boundary: canonical owner record
  - Typical path: `.loom/specs/<slug>.md`
- `plan`
  - ID shape: `plan:<slug>`
  - Authority boundary: canonical owner record
  - Typical path: `.loom/plans/<YYYYMMDD>-<slug>.md`
- `ticket`
  - ID shape: `ticket:<token>`
  - Authority boundary: canonical live execution ledger
  - Typical path: `.loom/tickets/<YYYYMMDD>-<token>-<short-slug>.md`
- `packet` with `packet_kind: ralph`
  - ID shape: `packet:ralph-<encoded-target>-<UTC compact timestamp>`
  - Authority boundary: non-canonical bounded contract
  - Typical path: `.loom/packets/ralph/<UTC compact timestamp>-ticket-<token>-iter-<NN>.md`
- `packet` with `packet_kind: critique`
  - ID shape: `packet:critique-<encoded-target-or-change-slug>-<UTC compact timestamp>`
  - Authority boundary: non-canonical bounded contract
  - Typical path: `.loom/packets/critique/<UTC compact timestamp>-<encoded-target-or-change-slug>.md`
- `packet` with `packet_kind: wiki`
  - ID shape: `packet:wiki-<encoded-target>-<UTC compact timestamp>`
  - Authority boundary: non-canonical bounded contract
  - Typical path: `.loom/packets/wiki/<UTC compact timestamp>-<encoded-target>.md`
- `critique`
  - ID shape: `critique:<slug>`
  - Authority boundary: canonical owner record
  - Typical path: `.loom/critique/<YYYYMMDD>-<slug>.md`
- `wiki`
  - ID shape: `wiki:<slug>`
  - Authority boundary: canonical owner record
  - Typical path: `.loom/wiki/<category>/<slug>.md`
- `evidence`
  - ID shape: `evidence:<slug>`
  - Authority boundary: canonical owner record
  - Typical path: `.loom/evidence/<YYYYMMDD>-<slug>.md`
- `workspace`
  - ID shape: `workspace:main`
  - Authority boundary: stable workspace metadata, not canonical project truth
  - Typical path: `.loom/workspace.md`
- `workspace-support`
  - ID shape: support-local `workspace:<slug>` such as `workspace:harness`
  - Authority boundary: support-local transport metadata
  - Typical path: project-local workspace support path such as `.loom/harness.md`
- `support-artifact`
  - ID shape: optional support-local `support:<domain>-<slug>`
  - Authority boundary: support-local workflow metadata
  - Typical path: `.loom/support/<domain>/<slug>.md`
- Optional `memory` support metadata
  - ID shape: usually no canonical ID
  - Authority boundary: support-only recall metadata
  - Typical path: `.loom/memory/<domain>/<memory-file>.md`

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

## Raw Artifact Support Directories

Evidence and research may use gitignored raw artifact directories for bulky or
volatile source material:

- `.loom/evidence/artifacts/<evidence-slug>/` for logs, traces, responses,
  screenshots, command captures, reports, fixtures, and other raw observations
- `.loom/research/artifacts/<research-slug>/` for articles, web fetches, PDFs,
  papers, repository snapshots, exported notes, generated source analyses, and
  other investigation inputs

These directories are support caches. They do not have canonical IDs, do not need
frontmatter, and do not create new owner layers merely because they sit under
canonical owner directories. Records may cite paths inside them, but the evidence
or research Markdown record remains the primary understanding. A future agent
should check the store when the record points to it and the files exist, but must
not require the store to exist in order to understand the record's claims,
limitations, and conclusions.

Projects should gitignore these stores by default. Intentionally tracked raw
artifacts need explicit record-level rationale, sanitization, and retention notes.

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
through critique, and accepted explanation through wiki. Packet records share the
packet lifecycle values from `status-lifecycle.md`, but each workflow owns its own
packet body shape and route semantics. Packets remain bounded contracts for child
work; their status owns only that packet's support lifecycle, not project truth or
live execution state.

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
- `.loom/wiki/workflows/<slug>.md`

### Date-prefixed owner records

Use UTC date + slug for owner records whose temporal relevance is important for
review, cleanup, or future retention policy:

- `.loom/initiatives/<YYYYMMDD>-<slug>.md`
- `.loom/plans/<YYYYMMDD>-<slug>.md`
- `.loom/critique/<YYYYMMDD>-<slug>.md`
- `.loom/evidence/<YYYYMMDD>-<slug>.md`

The date prefix is a filename discovery and retention aid. It does not become
part of the canonical ID:

- `.loom/plans/20260503-protocol-sharpening.md` uses `id: plan:protocol-sharpening`
- `.loom/critique/20260503-protocol-sharpening-review.md` uses `id: critique:protocol-sharpening-review`

Use the record creation date for `<YYYYMMDD>`. Do not rewrite the filename date
when `updated_at` changes. Existing older records without a date prefix are
legacy-compatible; rename them only as an intentional reconciliation pass that
updates or confirms inbound path references.

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
