---
id: ticket:cmdroute
kind: ticket
status: closed
change_class: record-hygiene
risk_class: medium
created_at: 2026-05-02T18:58:43Z
updated_at: 2026-05-02T21:37:28Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-council-precision-pass
  plan:
    - plan:skills-corpus-council-precision-pass
  packet:
    - packet:ralph-ticket-cmdroute-20260502T213017Z
  evidence:
    - evidence:command-route-wording-validation
  critique:
    - critique:command-route-wording-review
external_refs: {}
depends_on:
  - ticket:rtvocab1
  - ticket:supp0x2a
  - ticket:retrod3p
  - ticket:authst4p
  - ticket:pktgram5
  - ticket:pktlife6
  - ticket:revtgt7x
  - ticket:tmplph8x
  - ticket:evshape9
  - ticket:dwhand10
  - ticket:planwv11
---

# Summary

Remove optional-command wording that presents command surfaces as peers to owner
layers or workflow routes.

# Context

Council finding `CR-012` found some output contracts ask for “workflow, owner
layer, or optional command,” which risks making command wrappers look like
protocol truth.

# Why Now

This final hygiene ticket should inherit the settled route vocabulary and avoid
creating command-wrapper truth in the cleaned corpus.

# Scope

- Search for optional-command/adaptor wording that appears as route peer language.
- Replace with owner-layer/workflow-route wording and mention adapters only after
  the route is named when useful.
- Preserve existing no-runtime/no-command-truth doctrine.

# Out Of Scope

- Do not remove legitimate examples of shell commands as filesystem tools.
- Do not remove harness adapter documentation where it is clearly transport.
- Do not add command wrappers or command surfaces.

# Acceptance Criteria

- ACC-001: No product guidance presents optional commands as peers to owner layers
  or workflow routes.
- ACC-002: Adapter/command references that remain are clearly transport or
  convenience surfaces, not protocol truth.
- ACC-003: Final wording aligns with the shared route vocabulary.
- ACC-004: Evidence records command/adaptor wording searches and `git diff --check`.
- ACC-005: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-council-precision-pass#OBJ-012`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-council-precision-pass#OBJ-012` | `evidence:command-route-wording-validation` records before/after command-adaptor route wording searches and whitespace validation | `critique:command-route-wording-review` | supported |
| `ticket:cmdroute#ACC-001` | `evidence:command-route-wording-validation` exact after search has no remaining optional-command route-peer matches | `critique:command-route-wording-review` | supported |
| `ticket:cmdroute#ACC-002` | `evidence:command-route-wording-validation` broad after search shows remaining command/adaptor references are transport, invocation convenience, non-route guidance, or shell/non-runtime examples | `critique:command-route-wording-review` | supported |
| `ticket:cmdroute#ACC-003` | `evidence:command-route-wording-validation` and edited wording use owner layer / workflow route language aligned with `skills/loom-records/references/route-vocabulary.md` | `critique:command-route-wording-review` | supported |
| `ticket:cmdroute#ACC-004` | `evidence:command-route-wording-validation` records before/after searches and successful `git diff --check` | `critique:command-route-wording-review` | supported |
| `ticket:cmdroute#ACC-005` | `critique:command-route-wording-review` | oracle critique passed with no findings | supported |

# Execution Notes

Likely touched surfaces include workspace status snapshot, wiki guidance, ship
guidance, and any references where optional commands appear as route peers.

# Blockers

None current. Prior plan dependencies were satisfied before this ticket entered
Ralph execution.

# Next Move / Next Route

Closed. Commit and push this ticket, then close the parent plan and initiative.

# Route Readiness

Route: acceptance_review

Acceptance review readiness:
Evidence `evidence:command-route-wording-validation` and oracle critique
`critique:command-route-wording-review` support closure with no findings.

# Evidence

Recorded:

- `evidence:command-route-wording-validation` — before/after searches for
  optional command/adaptor route wording and successful `git diff --check`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: user requires oracle critique; command-wrapper truth is an
explicit non-goal.

Required critique profiles:

- operator-clarity
- routing-safety
- records-grammar

Findings:

`critique:command-route-wording-review` - no findings; mandatory oracle critique
passed.

Disposition status: completed

Deferral / not-required rationale:

Not deferred. Mandatory oracle critique passed with no findings.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- Command-route peer wording was normalized directly in
  `skills/loom-workspace/references/status-snapshot.md`,
  `skills/loom-wiki/references/wiki-write.md`, and
  `skills/loom-wiki/references/wiki-audit.md`.
- The route/command boundary remains grounded in
  `skills/loom-records/references/route-vocabulary.md`; no new owner layer,
  runtime, command wrapper, or helper requirement was introduced.

Deferred / not-required rationale:

No separate wiki page, research record, spec, constitution decision, or memory
entry is needed. The durable lesson is the product-surface wording itself plus
the route vocabulary reference.

# Wiki Disposition

N/A - no separate wiki promotion route. The accepted explanation lives in the
route vocabulary reference and touched product guidance.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-02T21:37:28Z
Basis: Ralph packet `packet:ralph-ticket-cmdroute-20260502T213017Z`; evidence
`evidence:command-route-wording-validation`; oracle critique
`critique:command-route-wording-review` with no findings.
Residual risks: validation is structural text-search evidence and cannot prevent
future phrasing drift by itself.

# Dependencies

- `ticket:rtvocab1`
- `ticket:supp0x2a`
- `ticket:retrod3p`
- `ticket:authst4p`
- `ticket:pktgram5`
- `ticket:pktlife6`
- `ticket:revtgt7x`
- `ticket:tmplph8x`
- `ticket:evshape9`
- `ticket:dwhand10`
- `ticket:planwv11`

# Journal

- 2026-05-02T18:58:43Z: Created from council finding `CR-012`.
- 2026-05-02T21:30:17Z: Compiled Ralph packet
  `packet:ralph-ticket-cmdroute-20260502T213017Z` and moved ticket to `active`.
- 2026-05-02T21:32:25Z: Ralph iteration replaced route-peer command wording,
  recorded `evidence:command-route-wording-validation`, and moved ticket to
  `review_required` for mandatory oracle critique.
- 2026-05-02T21:37:28Z: Mandatory oracle critique
  `critique:command-route-wording-review` passed with no findings. Recorded
  retrospective / promotion disposition and accepted closure.
