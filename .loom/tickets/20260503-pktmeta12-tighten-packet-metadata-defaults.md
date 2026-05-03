---
id: ticket:pktmeta12
kind: ticket
status: closed
change_class: protocol-authority
risk_class: medium
created_at: 2026-05-03T01:57:25Z
updated_at: 2026-05-03T02:28:53Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-residual-protocol-sharpening-pass
  plan:
    - plan:skills-corpus-residual-protocol-sharpening-pass
  research:
    - research:skills-corpus-residual-audit-synthesis
  packet:
    - packet:ralph-ticket-pktmeta12-20260503T022401Z
  evidence:
    - evidence:packet-metadata-defaults-validation
  critique:
    - critique:packet-metadata-defaults-review
external_refs: {}
depends_on: []
---

# Summary

Tighten packet metadata defaults for source state, network permission, and child
write authority.

# Context

Follow-up validation found shared packet templates still rely on a coarse
`source_fingerprint.git_status_summary`, default `network: unknown`, and a Ralph
`child_write_scope.records` placeholder that can invite overbroad canonical-record
writes unless the parent narrows it.

# Why Now

Packet metadata is the launch contract for fresh-context work. Defaults should
teach parents to record enough source-state, tool-permission, and write-authority
detail to prevent stale packets and unsafe child mutations.

# Scope

- Add source-state detail to packet fingerprint guidance without creating a
  runtime validator.
- Make packet template network permission defaults explicit enough that parents
  must choose or justify the value.
- Make Ralph child canonical-record writes fail closed unless the parent grants a
  narrow record write scope.
- Keep packet metadata shared support grammar; packets remain noncanonical support
  artifacts.

# Out Of Scope

- Do not add packet validators, schema engines, command wrappers, or hidden helper
  scripts.
- Do not require network access for packet work.
- Do not change packet truth ownership or make packets acceptance owners.

# Acceptance Criteria

- ACC-001: Shared packet fingerprint guidance or templates capture more useful
  source-state detail than only `clean|dirty|unknown`.
- ACC-002: Ralph, critique, and wiki packet templates require an explicit network
  posture or explicit unknown rationale rather than silently defaulting to
  `network: unknown`.
- ACC-003: Ralph packet child write scope makes canonical-record writes explicit
  and narrow, or says child returns output only when no child record write is
  granted.
- ACC-004: Packet guidance still states packets are support artifacts and do not
  own project truth, acceptance, critique verdicts, or closure.
- ACC-005: Evidence records before/after searches for source fingerprint, network
  posture, child write scope, and `git diff --check`.
- ACC-006: Oracle critique passes with no unresolved findings.

# Coverage

Covers:

- `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-015`
- `ticket:pktmeta12#ACC-001`
- `ticket:pktmeta12#ACC-002`
- `ticket:pktmeta12#ACC-003`
- `ticket:pktmeta12#ACC-004`
- `ticket:pktmeta12#ACC-005`
- `ticket:pktmeta12#ACC-006`

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| `initiative:skills-corpus-residual-protocol-sharpening-pass#OBJ-015` | `evidence:packet-metadata-defaults-validation` | `critique:packet-metadata-defaults-review` | supported |
| `ticket:pktmeta12#ACC-001` through `ticket:pktmeta12#ACC-006` | `evidence:packet-metadata-defaults-validation` | `critique:packet-metadata-defaults-review` | supported |

# Execution Notes

Likely touched surfaces include `skills/loom-records/references/packet-frontmatter.md`,
`skills/loom-ralph/templates/ralph-packet.md`,
`skills/loom-critique/templates/critique-packet.md`,
`skills/loom-wiki/templates/wiki-packet.md`, and
`skills/loom-ralph/references/packet-contract.md`.

# Blockers

None.

# Next Move / Next Route

Closed. Commit and push this ticket before continuing to `ticket:ralphchk7`.

# Route Readiness

Acceptance review readiness:
Evidence `evidence:packet-metadata-defaults-validation` and oracle critique
`critique:packet-metadata-defaults-review` support closure with no findings.

# Evidence

Recorded: `evidence:packet-metadata-defaults-validation`.

# Critique Disposition

Risk class: medium

Critique policy: mandatory

Policy rationale: packet metadata defaults affect child authority, launch safety,
and parent reconciliation honesty.

Required critique profiles:

- packet-safety
- owner-boundary
- operator-clarity

Findings:

`critique:packet-metadata-defaults-review` - no findings; mandatory oracle
critique passed.

Disposition status: completed

Deferral / not-required rationale:

Not deferred.

# Retrospective / Promotion Disposition

Disposition status: completed

Promoted:

- Packet metadata defaults for source-status detail, network posture, and Ralph
  child record-write authority were promoted directly into packet templates,
  shared packet-frontmatter guidance, and Ralph packet contract guidance.

Deferred / not-required rationale:

No separate wiki page, research record, spec, constitution decision, or memory
entry is needed. The durable lesson is the product guidance itself.

# Wiki Disposition

N/A - no separate wiki promotion route. The accepted explanation lives in the
touched packet templates and references.

# Acceptance Decision

Accepted by: OpenCode parent agent
Accepted at: 2026-05-03T02:28:53Z
Basis: Ralph packet `packet:ralph-ticket-pktmeta12-20260503T022401Z`; evidence
`evidence:packet-metadata-defaults-validation`; oracle critique
`critique:packet-metadata-defaults-review` with no findings.
Residual risks: validation is structural/manual; there is no automated
protocol-template test suite. Existing historical packets were intentionally not
migrated; future correctness still depends on packet authors replacing template
placeholders honestly.

# Dependencies

None.

# Journal

- 2026-05-03T01:57:25Z: Created from follow-up validation after `ticket:wssupp4`.
- 2026-05-03T02:26:13Z: Ralph iteration
  `packet:ralph-ticket-pktmeta12-20260503T022401Z` completed in scope. Evidence
  recorded in `evidence:packet-metadata-defaults-validation`; next route is
  mandatory oracle critique.
- 2026-05-03T02:28:53Z: Mandatory oracle critique
  `critique:packet-metadata-defaults-review` passed with no findings. Parent
  recorded retrospective / promotion disposition and accepted closure.
